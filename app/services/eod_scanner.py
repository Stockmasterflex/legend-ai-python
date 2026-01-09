"""
End-of-day universe scanner.
"""
from __future__ import annotations

import asyncio
import logging
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.services.cache import get_cache_service
from app.services.database import get_database_service
from app.services.pattern_scanner import pattern_scanner_service
from app.config import get_settings
from app.utils.pattern_groups import bucket_name

logger = logging.getLogger(__name__)

SCAN_KEY_TEMPLATE = "scan:results:{date}"
SCAN_LATEST_KEY = "scan:latest"
SCAN_TTL = 24 * 3600  # 24 hours


class EODScanner:
    """Nightly scanner that batches universe pattern detection."""

    def __init__(self):
        self.db_service = get_database_service()
        self.cache = get_cache_service()
        self.scanner_service = pattern_scanner_service
        self.settings = get_settings()

    async def run_scan(self, *, scan_date: Optional[str] = None) -> Dict[str, Any]:
        if scan_date is None:
            scan_date = datetime.now(timezone.utc).strftime("%Y%m%d")

        universe_rows = self.db_service.get_universe_symbols()
        symbols = [row.symbol for row in universe_rows]
        metadata = {row.symbol: {"sector": row.sector, "industry": row.industry} for row in universe_rows}
        total = len(symbols)
        logger.info("Starting EOD scan for %s symbols (date=%s)", total, scan_date)

        results: List[Dict[str, Any]] = []
        errors: List[str] = []

        for chunk in self._chunks(symbols, 25):
            try:
                payload = await self.scanner_service.scan_with_pattern_engine(
                    tickers=chunk,
                    interval="1day",
                    apply_filters=True,
                    min_score=6.0,
                )
                chunk_results = payload.get("results", [])
                for item in chunk_results:
                    symbol = item.get("symbol")
                    item["sector"] = metadata.get(symbol, {}).get("sector")
                    item["industry"] = metadata.get(symbol, {}).get("industry")
                results.extend(chunk_results)
            except Exception as exc:
                logger.error("Chunk scan failed: %s", exc, exc_info=True)
                errors.append(str(exc))
            await asyncio.sleep(2)

        # Deduplicate: keep only the highest-scoring pattern per symbol
        seen_symbols = {}
        for item in results:
            symbol = item.get("symbol")
            score = item.get("score", 0)
            if symbol not in seen_symbols or score > seen_symbols[symbol].get("score", 0):
                seen_symbols[symbol] = item
        results = list(seen_symbols.values())
        logger.info("After deduplication: %s unique symbols", len(results))

        categorized = self._categorize(results)
        summary = self._build_summary(
            scan_date=scan_date,
            total_symbols=total,
            results=results,
            buckets=categorized,
            errors=errors,
        )
        key = SCAN_KEY_TEMPLATE.format(date=scan_date)
        await self.cache.set(key, summary, ttl=SCAN_TTL)
        await self.cache.set(SCAN_LATEST_KEY, summary, ttl=SCAN_TTL)
        logger.info("Scan cached for %s (patterns=%s)", scan_date, len(results))
        return summary

    def _chunks(self, data: List[str], size: int):
        for i in range(0, len(data), size):
            yield data[i : i + size]

    def _categorize(self, patterns: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        bucket_map = defaultdict(list)
        for pattern in patterns:
            name = (pattern.get("pattern") or "").lower()
            bucket = bucket_name(name)
            if bucket:
                bucket_map[bucket].append(self._summarize(pattern))
        return dict(bucket_map)

    def _summarize(self, pattern: Dict[str, any]) -> Dict[str, any]:
        return {
            "symbol": pattern.get("symbol"),
            "pattern": pattern.get("pattern"),
            "score": pattern.get("score"),
            "confidence": pattern.get("confidence"),
            "entry": pattern.get("entry"),
            "stop": pattern.get("stop"),
            "target": pattern.get("target"),
            "sector": pattern.get("sector"),
            "risk_reward": pattern.get("risk_reward"),
        }

    def _build_summary(
        self,
        scan_date: str,
        total_symbols: int,
        results: List[Dict[str, Any]],
        buckets: Dict[str, List[Dict[str, Any]]],
        errors: List[str],
    ) -> Dict[str, Any]:
        sorted_results = sorted(results, key=lambda item: item.get("score", 0), reverse=True)
        top_setups = [self._summarize(item) for item in sorted_results[:10]]
        all_summaries = [self._summarize(item) for item in results]
        return {
            "scan_date": scan_date,
            "total_symbols": total_symbols,
            "patterns_found": len(results),
            "buckets": buckets,
            "top_setups": top_setups,
            "errors": errors,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "results": all_summaries,
        }


_eod_scanner: Optional[EODScanner] = None

def get_eod_scanner() -> EODScanner:
    global _eod_scanner
    if _eod_scanner is None:
        _eod_scanner = EODScanner()
    return _eod_scanner
