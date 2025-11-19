"""
Multi-Pattern Scanner Service

Scans stocks using all available pattern detectors and returns the best setups.
"""
import asyncio
import logging
import time
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime, timezone

from app.core.detector_registry import get_all_detectors
from app.core.detector_base import PatternResult
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
        min_confidence: float = 0.4,  # Temporarily lowered to debug
    ):
        """
        Initialize the pattern scanner

        Args:
            max_symbols: Maximum number of symbols to scan
            bars: Number of bars to fetch for analysis
            max_concurrency: Maximum concurrent scans
            min_confidence: Minimum confidence threshold (0-1)
        """
        self.max_symbols = max_symbols
        self.output_bars = bars
        self.max_concurrency = max_concurrency
        self.min_confidence = min_confidence

    async def scan_symbol(
        self,
        symbol: str,
        timeframe: str = "1day",
        pattern_filter: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Scan a single symbol with all detectors

        Args:
            symbol: Stock symbol to scan
            timeframe: Timeframe to scan (1day, 1week, etc.)
            pattern_filter: Optional list of pattern names to filter by

        Returns:
            List of detected patterns with metadata
        """
        try:
            # Fetch price data
            price_data = await market_data_service.get_time_series(
                ticker=symbol,
                interval=timeframe,
                outputsize=self.output_bars
            )

            if not price_data or not price_data.get("c"):
                logger.debug(f"No price data for {symbol}")
                return []

            data_points = len(price_data.get("c", []))
            logger.debug(f"Fetched {data_points} data points for {symbol}")

            # Convert to DataFrame
            df = self._to_dataframe(price_data)

            if len(df) < 60:
                logger.debug(f"Insufficient data for {symbol}: {len(df)} bars")
                return []

            # Get all detectors
            detectors = get_all_detectors()
            logger.debug(f"Running {len(detectors)} detectors on {symbol}")

            # Run all detectors
            all_patterns: List[PatternResult] = []
            for detector in detectors:
                try:
                    patterns = detector.find(df, timeframe, symbol)
                    if patterns:
                        all_patterns.extend(patterns)
                        logger.debug(f"Detector {detector.name} found {len(patterns)} patterns for {symbol}")
                except Exception as e:
                    logger.error(f"Detector {detector.name} failed for {symbol}: {e}")

            logger.debug(f"Total patterns found for {symbol}: {len(all_patterns)}")

            # Filter by confidence
            confident_patterns = [
                p for p in all_patterns
                if p.confidence >= self.min_confidence
            ]
            logger.debug(f"After confidence filter (>= {self.min_confidence}): {len(confident_patterns)} patterns")

            # Filter by pattern names if specified
            if pattern_filter:
                pattern_filter_lower = [p.lower() for p in pattern_filter]
                confident_patterns = [
                    p for p in confident_patterns
                    if p.pattern_type.value.lower() in pattern_filter_lower
                ]
                logger.debug(f"After pattern filter {pattern_filter}: {len(confident_patterns)} patterns")

            # Convert to dict format
            results = []
            for pattern in confident_patterns:
                results.append(self._pattern_to_dict(pattern, symbol, timeframe))

            logger.debug(f"Returning {len(results)} patterns for {symbol}")
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
        """
        Scan entire universe for patterns

        Args:
            universe: List of symbols to scan (None = use default universe)
            limit: Maximum number of results to return
            pattern_filter: Optional list of pattern names to filter by
            min_score: Minimum score (0-10) to include in results

        Returns:
            Scan results with metadata
        """
        started = time.perf_counter()

        # Get universe
        if universe is None:
            universe_meta = await universe_store.get_all()
            if not universe_meta:
                fallback = universe_data.get_full_universe()
                universe_meta = {symbol: {"symbol": symbol} for symbol in fallback}
            symbols = list(universe_meta.keys())[:self.max_symbols]
            logger.info(f"Using universe from store: {len(symbols)} symbols")
        else:
            symbols = universe[:self.max_symbols]
            logger.info(f"Using provided universe: {len(symbols)} symbols")

        if not symbols:
            logger.warning("No symbols to scan - universe is empty")
            return self._response(started, 0, [])

        logger.info(f"Starting scan of {len(symbols)} symbols with min_score={min_score}")

        # Scan symbols concurrently
        sem = asyncio.Semaphore(self.max_concurrency)

        async def scan_with_semaphore(symbol: str):
            async with sem:
                return await self.scan_symbol(symbol, "1day", pattern_filter)

        tasks = [scan_with_semaphore(symbol) for symbol in symbols]
        raw_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Flatten results (each symbol can have multiple patterns)
        all_patterns = []
        success_count = 0
        error_count = 0
        for result in raw_results:
            if isinstance(result, list):
                all_patterns.extend(result)
                if result:  # Only count if patterns were found
                    success_count += 1
            elif isinstance(result, Exception):
                logger.error(f"Scan task failed: {result}")
                error_count += 1

        logger.info(f"Scan results: {success_count} symbols with patterns, {error_count} errors, {len(all_patterns)} total patterns")

        # Sort by score
        all_patterns.sort(key=lambda x: x.get("score", 0), reverse=True)

        # Filter by minimum score
        filtered_patterns = [
            p for p in all_patterns
            if p.get("score", 0) >= min_score
        ]

        logger.info(f"After filtering by min_score {min_score}: {len(filtered_patterns)} patterns remain")

        # Limit results
        limited_results = filtered_patterns[:limit]

        duration = time.perf_counter() - started
        logger.info(
            f"✅ Multi-pattern scan complete: {len(symbols)} symbols scanned, "
            f"{len(all_patterns)} patterns found, "
            f"{len(filtered_patterns)} above {min_score}/10, "
            f"{len(limited_results)} returned, "
            f"{duration:.2f}s"
        )

        return self._response(started, len(symbols), limited_results, len(all_patterns))

    def _pattern_to_dict(
        self,
        pattern: PatternResult,
        symbol: str,
        timeframe: str
    ) -> Dict[str, Any]:
        """Convert PatternResult to dictionary"""
        score = pattern.confidence * 10  # Convert 0-1 to 0-10 scale

        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "pattern": pattern.pattern_type.value,
            "score": round(score, 1),
            "confidence": round(pattern.confidence, 3),
            "entry": pattern.entry,
            "stop": pattern.stop,
            "target": pattern.target,
            "risk_reward": round((pattern.target - pattern.entry) / (pattern.entry - pattern.stop), 2)
            if pattern.entry and pattern.stop and pattern.target and pattern.entry > pattern.stop
            else None,
            "window_start": pattern.window_start,
            "window_end": pattern.window_end,
            "description": pattern.description,
            "strong": pattern.strong,
            "evidence": pattern.evidence,
            "detected_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }

    @staticmethod
    def _to_dataframe(payload: Dict[str, Any]) -> pd.DataFrame:
        """Convert market data payload to DataFrame"""
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
        """Build response payload"""
        duration_ms = (time.perf_counter() - started) * 1000

        return {
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


# Global service instance
pattern_scanner_service = PatternScannerService()

__all__ = ["PatternScannerService", "pattern_scanner_service"]
