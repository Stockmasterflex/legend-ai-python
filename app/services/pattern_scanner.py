"""
Multi-Pattern Scanner Service

Scans stocks using all available pattern detectors and returns the best setups.
"""
import asyncio
import logging
import time
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timezone

from app.core.detector_registry import get_all_detectors
from app.core.detector_base import PatternResult
from app.core.pattern_engine.detector import get_pattern_detector
from app.core.pattern_engine.filter import PatternFilter
from app.core.pattern_engine.scoring import PatternScorer
from app.core.pattern_engine.scanner import ScanConfig, UniverseScanner
from app.services.market_data import market_data_service
from app.services.universe_store import universe_store
from app.services import universe_data
from app.utils.build_info import resolve_build_sha

logger = logging.getLogger(__name__)


class PatternScannerService:
    """
    Service for scanning stocks across all available pattern detectors
    """

    def __init__(
        self,
        *,
        max_symbols: int = 600,
        bars: int = 320,
        max_concurrency: int = 8,
        min_confidence: float = 0.4,
    ):
        self.max_symbols = max_symbols
        self.output_bars = bars
        self.max_concurrency = max_concurrency
        self.min_confidence = min_confidence
        self.engine_scanner = UniverseScanner(
            detector=get_pattern_detector(),
            filter_system=PatternFilter(),
            scorer=PatternScorer(),
        )

    async def scan_symbol(
        self,
        symbol: str,
        timeframe: str = "1day",
        pattern_filter: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        try:
            price_data = await market_data_service.get_time_series(
                ticker=symbol,
                interval=timeframe,
                outputsize=self.output_bars
            )

            if not price_data or not price_data.get("c"):
                return []

            df = self._to_dataframe(price_data)

            if len(df) < 60:
                return []

            detectors = get_all_detectors()
            all_patterns: List[PatternResult] = []
            for detector in detectors:
                try:
                    patterns = detector.find(df, timeframe, symbol)
                    if patterns:
                        all_patterns.extend(patterns)
                except Exception as e:
                    logger.error(f"Detector {detector.name} failed for {symbol}: {e}")

            confident_patterns = [
                p for p in all_patterns
                if p.confidence >= self.min_confidence
            ]

            if pattern_filter:
                pattern_filter_lower = [p.lower() for p in pattern_filter]
                confident_patterns = [
                    p for p in confident_patterns
                    if p.pattern_type.value.lower() in pattern_filter_lower
                ]

            results = []
            for pattern in confident_patterns:
                results.append(self._pattern_to_dict(pattern, symbol, timeframe))

            return results

        except Exception as e:
            logger.error(f"Failed to scan {symbol}: {e}")
            return []

    async def scan_universe(
        self,
        universe: Optional[List[str]] = None,
        limit: int = 50,
        pattern_filter: Optional[List[str]] = None,
        min_score: float = 7.0
    ) -> Dict[str, Any]:
        started = time.perf_counter()

        if universe is None:
            universe_meta = await universe_store.get_all()
            if not universe_meta:
                fallback = universe_data.get_full_universe()
                universe_meta = {symbol: {"symbol": symbol} for symbol in fallback}
            symbols = list(universe_meta.keys())[:self.max_symbols]
        else:
            symbols = universe[:self.max_symbols]

        if not symbols:
            return self._response(started, 0, [])

        logger.info(f"Starting scan of {len(symbols)} symbols")

        sem = asyncio.Semaphore(self.max_concurrency)

        async def scan_with_semaphore(symbol: str):
            async with sem:
                return await self.scan_symbol(symbol, "1day", pattern_filter)

        tasks = [scan_with_semaphore(symbol) for symbol in symbols]
        raw_results = await asyncio.gather(*tasks, return_exceptions=True)

        all_patterns = []
        for result in raw_results:
            if isinstance(result, list):
                all_patterns.extend(result)

        all_patterns.sort(key=lambda x: x.get("score", 0), reverse=True)

        filtered_patterns = [
            p for p in all_patterns
            if p.get("score", 0) >= min_score
        ]

        limited_results = filtered_patterns[:limit]

        return self._response(started, len(symbols), limited_results, len(all_patterns))

    async def scan_with_pattern_engine(
        self,
        tickers: List[str],
        interval: str = "1day",
        apply_filters: bool = True,
        min_score: float = 6.0,
        filter_config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if not tickers:
            return self._response(time.perf_counter(), 0, [])

        config = ScanConfig(
            universe=[t.upper() for t in tickers],
            interval=interval,
            max_concurrent=self.max_concurrency,
            apply_filters=apply_filters,
            apply_scoring=True,
            min_score=min_score,
            filter_config=filter_config,
        )
        return await self.engine_scanner.scan_universe(config)

    def _pattern_to_dict(
        self,
        pattern: PatternResult,
        symbol: str,
        timeframe: str
    ) -> Dict[str, Any]:
        score = pattern.confidence * 10

        def safe_float(v):
            if v is None: return None
            try: return float(v)
            except: return None

        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "pattern": pattern.pattern_type.value,
            "score": round(float(score), 1),
            "confidence": round(float(pattern.confidence), 3),
            "entry": safe_float(pattern.entry),
            "stop": safe_float(pattern.stop),
            "target": safe_float(pattern.target),
            "risk_reward": round((safe_float(pattern.target) - safe_float(pattern.entry)) / (safe_float(pattern.entry) - safe_float(pattern.stop)), 2)
            if safe_float(pattern.entry) and safe_float(pattern.stop) and safe_float(pattern.target) and safe_float(pattern.entry) > safe_float(pattern.stop)
            else None,
            "window_start": pattern.window_start,
            "window_end": pattern.window_end,
            "description": pattern.description,
            "strong": bool(pattern.strong),
            "evidence": self._sanitize(pattern.evidence),
            "detected_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }

    def _sanitize(self, obj: Any) -> Any:
        """Deep clean object to remove numpy types"""
        if obj is None:
            return None
        if isinstance(obj, dict):
            return {k: self._sanitize(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._sanitize(v) for v in obj]
        elif isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        return obj

    @staticmethod
    def _to_dataframe(payload: Dict[str, Any]) -> pd.DataFrame:
        closes = payload.get("c", [])
        opens = payload.get("o", closes)
        highs = payload.get("h", closes)
        lows = payload.get("l", closes)
        volumes = payload.get("v", [0] * len(closes))
        dates = payload.get("t") or []

        df = pd.DataFrame({
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "volume": volumes,
        })

        if dates:
            df["datetime"] = pd.to_datetime(dates, errors="coerce")
        else:
            df["datetime"] = pd.date_range(end=datetime.now(), periods=len(df), freq="B")

        return df.dropna(subset=["close"]).reset_index(drop=True)

    def _response(
        self,
        started: float,
        universe_size: int,
        results: List[Dict[str, Any]],
        total_hits: int = 0
    ) -> Dict[str, Any]:
        duration_ms = (time.perf_counter() - started) * 1000

        # Deep clean the entire response payload
        payload = {
            "success": True,
            "as_of": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "universe_size": universe_size,
            "results": results,
            "meta": {
                "build_sha": resolve_build_sha(),
                "duration_ms": round(duration_ms, 2),
                "result_count": len(results),
                "total_hits": total_hits or len(results),
                "scanner_type": "multi_pattern",
            },
        }
        return self._sanitize(payload)


# Global service instance
pattern_scanner_service = PatternScannerService()

__all__ = ["PatternScannerService", "pattern_scanner_service"]
