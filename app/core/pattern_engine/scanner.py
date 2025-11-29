from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.core.pattern_engine.filter import PatternFilter
from app.core.pattern_engine.scoring import PatternScorer


@dataclass
class ScanConfig:
    universe: List[str]  # Ticker list
    interval: str = "1day"
    max_concurrent: int = 10
    apply_filters: bool = True
    apply_scoring: bool = True
    min_score: float = 6.0
    filter_config: Optional[Dict[str, Any]] = None


class UniverseScanner:
    """Async universe scanner that wires detector, filters, and scoring together."""

    def __init__(self, detector, filter_system: PatternFilter, scorer: PatternScorer):
        self.detector = detector
        self.filter = filter_system
        self.scorer = scorer

    async def scan_universe(self, config: ScanConfig) -> Dict[str, Any]:
        """Scan a list of tickers and return ranked results."""
        started = time.perf_counter()
        sem = asyncio.Semaphore(config.max_concurrent)

        async def _run(ticker: str):
            async with sem:
                try:
                    patterns = await self.scan_ticker(ticker, config.interval)
                    return ticker, patterns, None
                except Exception as exc:  # pragma: no cover - defensive
                    return ticker, [], exc

        tasks = [_run(ticker) for ticker in config.universe]
        raw_results = await asyncio.gather(*tasks)

        aggregated: List[Dict[str, Any]] = []
        errors: Dict[str, str] = {}
        for ticker, patterns, error in raw_results:
            if error:
                errors[ticker] = str(error)
                continue

            if config.apply_filters and patterns:
                patterns = self.filter.apply_filters(patterns, config.filter_config)

            if config.apply_scoring and patterns:
                patterns = self.scorer.score_patterns(patterns)

            for pat in patterns:
                pat.setdefault("ticker", ticker)
            aggregated.extend(patterns)

        ranked = self.rank_results(aggregated)
        if config.apply_scoring:
            ranked = [p for p in ranked if p.get("score", 0.0) >= config.min_score]

        duration_ms = (time.perf_counter() - started) * 1000
        return {
            "as_of": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "universe_size": len(config.universe),
            "results": ranked,
            "errors": errors,
            "meta": {
                "duration_ms": round(duration_ms, 2),
                "result_count": len(ranked),
            },
        }

    async def scan_ticker(self, ticker: str, interval: str) -> List[Dict[str, Any]]:
        """Scan a single ticker for all patterns."""
        from app.services.market_data import market_data_service

        price_data = await market_data_service.get_time_series(
            ticker=ticker,
            interval=interval,
            outputsize=320,
        )
        if not price_data or not price_data.get("c"):
            return []

        return self.detector.detect_all_patterns(price_data, ticker=ticker)

    def rank_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort and rank scan results."""
        if not results:
            return []

        ranked = sorted(
            results,
            key=lambda item: (item.get("score") or 0.0, item.get("confidence") or 0.0),
            reverse=True,
        )
        for idx, item in enumerate(ranked, start=1):
            item.setdefault("rank", idx)
        return ranked
