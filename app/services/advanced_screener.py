"""
Advanced Stock Screener Service

Provides comprehensive filtering and screening capabilities with:
- Custom filter criteria (price, volume, RS rating, patterns, indicators)
- Pre-built screen templates (Minervini SEPA, CAN SLIM, etc.)
- Advanced technical and fundamental filters
"""
import asyncio
import logging
import time
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from dataclasses import dataclass, asdict

import pandas as pd
import numpy as np

from app.core.detector_registry import get_all_detectors
from app.core.classifiers import minervini_trend_template
from app.core.metrics import (
    compute_atr,
    last_valid,
    percentage_distance,
    relative_strength_metrics,
)
from app.services.market_data import market_data_service
from app.services.universe_store import universe_store
from app.services import universe_data
from app.utils.build_info import resolve_build_sha

logger = logging.getLogger(__name__)


@dataclass
class FilterCriteria:
    """Filter criteria for stock screening"""
    # Price filters
    min_price: Optional[float] = None
    max_price: Optional[float] = None

    # Volume filters
    min_volume: Optional[float] = None
    min_avg_volume: Optional[float] = None  # Average volume over period

    # Relative Strength
    min_rs_rating: Optional[float] = None
    max_rs_rating: Optional[float] = None

    # Pattern detection
    patterns: Optional[List[str]] = None  # List of pattern types to detect
    min_pattern_confidence: float = 0.6

    # Technical indicators
    above_sma_50: Optional[bool] = None
    above_sma_200: Optional[bool] = None
    above_ema_21: Optional[bool] = None
    sma_50_above_sma_200: Optional[bool] = None  # Golden cross

    # Price vs moving averages
    min_pct_above_sma_50: Optional[float] = None
    max_pct_above_sma_50: Optional[float] = None

    # Momentum
    min_price_change_pct: Optional[float] = None  # % change over period
    max_price_change_pct: Optional[float] = None
    price_change_period: int = 20  # days

    # Volatility
    min_atr: Optional[float] = None
    max_atr: Optional[float] = None

    # Fundamental filters
    sectors: Optional[List[str]] = None
    exclude_sectors: Optional[List[str]] = None

    # Minervini criteria
    minervini_template: Optional[bool] = None

    # Gap detection
    gap_up_today: Optional[bool] = None
    min_gap_pct: Optional[float] = None

    # Consolidation
    in_consolidation: Optional[bool] = None
    max_consolidation_days: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {k: v for k, v in asdict(self).items() if v is not None}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FilterCriteria':
        """Create from dictionary"""
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})


class AdvancedScreenerService:
    """
    Advanced stock screener with comprehensive filtering capabilities
    """

    def __init__(
        self,
        max_symbols: int = 600,
        bars: int = 320,
        max_concurrency: int = 8,
    ):
        self.max_symbols = max_symbols
        self.output_bars = bars
        self.max_concurrency = max_concurrency

    async def run_screen(
        self,
        filter_criteria: FilterCriteria,
        universe: Optional[List[str]] = None,
        limit: int = 50,
    ) -> Dict[str, Any]:
        """
        Run a custom screen with specified filter criteria

        Args:
            filter_criteria: FilterCriteria object with screening parameters
            universe: List of symbols to screen (None = use default universe)
            limit: Maximum number of results to return

        Returns:
            Screen results with metadata
        """
        started = time.perf_counter()

        # Get universe
        universe_meta = await universe_store.get_all()
        if not universe_meta:
            fallback = universe_data.get_full_universe()
            universe_meta = {symbol: {"symbol": symbol} for symbol in fallback}

        # Filter by sector
        if filter_criteria.sectors:
            sector_lower = [s.lower() for s in filter_criteria.sectors]
            universe_meta = {
                sym: meta for sym, meta in universe_meta.items()
                if meta.get("sector", "").lower() in sector_lower
            }

        if filter_criteria.exclude_sectors:
            exclude_lower = [s.lower() for s in filter_criteria.exclude_sectors]
            universe_meta = {
                sym: meta for sym, meta in universe_meta.items()
                if meta.get("sector", "").lower() not in exclude_lower
            }

        # Get symbols
        if universe:
            symbols = [sym.upper() for sym in universe if sym.upper() in universe_meta]
        else:
            symbols = list(universe_meta.keys())

        symbols = symbols[:self.max_symbols]

        if not symbols:
            return self._empty_response(started)

        # Get SPY data for RS calculations
        spy_series = await market_data_service.get_time_series("SPY", "1day", self.output_bars)
        spy_closes = spy_series.get("c", []) if spy_series and spy_series.get("c") else []

        # Scan symbols concurrently
        sem = asyncio.Semaphore(self.max_concurrency)
        tasks = [
            self._screen_symbol(
                symbol,
                universe_meta.get(symbol, {}),
                filter_criteria,
                spy_closes,
                sem
            )
            for symbol in symbols
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out None and exceptions
        valid_results = [
            r for r in results
            if r and not isinstance(r, Exception)
        ]

        # Sort by score descending
        valid_results.sort(key=lambda x: x.get("score", 0), reverse=True)

        # Apply limit
        valid_results = valid_results[:limit]

        duration = time.perf_counter() - started

        return {
            "as_of": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "universe_size": len(symbols),
            "results": valid_results,
            "meta": {
                "build_sha": resolve_build_sha(),
                "duration_ms": round(duration * 1000, 2),
                "result_count": len(valid_results),
                "total_scanned": len(symbols),
                "filter_criteria": filter_criteria.to_dict(),
            }
        }

    async def _screen_symbol(
        self,
        symbol: str,
        meta: Dict[str, Any],
        criteria: FilterCriteria,
        spy_closes: List[float],
        sem: asyncio.Semaphore
    ) -> Optional[Dict[str, Any]]:
        """Screen a single symbol against filter criteria"""
        async with sem:
            try:
                # Fetch price data
                price_data = await market_data_service.get_time_series(
                    ticker=symbol,
                    interval="1day",
                    outputsize=self.output_bars
                )

                if not price_data or not price_data.get("c"):
                    return None

                # Convert to DataFrame
                df = self._to_dataframe(price_data)

                if len(df) < 60:
                    return None

                # Apply filters
                match_result = self._apply_filters(df, criteria, spy_closes, meta)

                if not match_result["matches"]:
                    return None

                # Calculate score
                score = self._calculate_score(match_result, criteria)

                # Get current values
                current_price = float(df['close'].iloc[-1])
                current_volume = float(df['volume'].iloc[-1])

                # Pattern detection if requested
                patterns_found = []
                if criteria.patterns:
                    patterns_found = await self._detect_patterns(
                        df, symbol, criteria.patterns, criteria.min_pattern_confidence
                    )

                # Calculate RS rating
                rs_data = relative_strength_metrics(df['close'].tolist(), spy_closes)
                rs_rating = rs_data.get("rank")

                return {
                    "symbol": symbol,
                    "name": meta.get("name", symbol),
                    "sector": meta.get("sector", "Unknown"),
                    "industry": meta.get("industry", "Unknown"),
                    "price": round(current_price, 2),
                    "volume": int(current_volume),
                    "avg_volume": int(df['volume'].tail(20).mean()),
                    "rs_rating": round(rs_rating, 1) if rs_rating else None,
                    "score": round(score, 2),
                    "patterns": patterns_found,
                    "match_data": match_result,
                }

            except Exception as e:
                logger.error(f"Failed to screen {symbol}: {e}")
                return None

    def _apply_filters(
        self,
        df: pd.DataFrame,
        criteria: FilterCriteria,
        spy_closes: List[float],
        meta: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply all filter criteria and return match data"""
        matches = True
        match_details = {}

        current_price = float(df['close'].iloc[-1])
        current_volume = float(df['volume'].iloc[-1])

        # Price filters
        if criteria.min_price and current_price < criteria.min_price:
            matches = False
        if criteria.max_price and current_price > criteria.max_price:
            matches = False

        match_details["price"] = current_price

        # Volume filters
        if criteria.min_volume and current_volume < criteria.min_volume:
            matches = False

        avg_volume = df['volume'].tail(20).mean()
        if criteria.min_avg_volume and avg_volume < criteria.min_avg_volume:
            matches = False

        match_details["volume"] = current_volume
        match_details["avg_volume"] = avg_volume

        # Calculate moving averages
        df['sma_50'] = df['close'].rolling(window=50).mean()
        df['sma_200'] = df['close'].rolling(window=200).mean()
        df['ema_21'] = df['close'].ewm(span=21, adjust=False).mean()

        sma_50 = float(df['sma_50'].iloc[-1]) if not pd.isna(df['sma_50'].iloc[-1]) else None
        sma_200 = float(df['sma_200'].iloc[-1]) if not pd.isna(df['sma_200'].iloc[-1]) else None
        ema_21 = float(df['ema_21'].iloc[-1]) if not pd.isna(df['ema_21'].iloc[-1]) else None

        # Technical indicator filters
        if criteria.above_sma_50 and (sma_50 is None or current_price < sma_50):
            matches = False

        if criteria.above_sma_200 and (sma_200 is None or current_price < sma_200):
            matches = False

        if criteria.above_ema_21 and (ema_21 is None or current_price < ema_21):
            matches = False

        if criteria.sma_50_above_sma_200 and (sma_50 is None or sma_200 is None or sma_50 < sma_200):
            matches = False

        match_details["sma_50"] = sma_50
        match_details["sma_200"] = sma_200
        match_details["ema_21"] = ema_21

        # Price vs SMA filters
        if sma_50:
            pct_above_sma_50 = ((current_price - sma_50) / sma_50) * 100
            match_details["pct_above_sma_50"] = round(pct_above_sma_50, 2)

            if criteria.min_pct_above_sma_50 and pct_above_sma_50 < criteria.min_pct_above_sma_50:
                matches = False
            if criteria.max_pct_above_sma_50 and pct_above_sma_50 > criteria.max_pct_above_sma_50:
                matches = False

        # Momentum filters
        if len(df) > criteria.price_change_period:
            price_change_pct = ((current_price - df['close'].iloc[-criteria.price_change_period]) /
                               df['close'].iloc[-criteria.price_change_period]) * 100
            match_details["price_change_pct"] = round(price_change_pct, 2)

            if criteria.min_price_change_pct and price_change_pct < criteria.min_price_change_pct:
                matches = False
            if criteria.max_price_change_pct and price_change_pct > criteria.max_price_change_pct:
                matches = False

        # RS Rating
        if spy_closes:
            rs_data = relative_strength_metrics(df['close'].tolist(), spy_closes)
            rs_rating = rs_data.get("rank")

            if rs_rating:
                match_details["rs_rating"] = round(rs_rating, 1)

                if criteria.min_rs_rating and rs_rating < criteria.min_rs_rating:
                    matches = False
                if criteria.max_rs_rating and rs_rating > criteria.max_rs_rating:
                    matches = False

        # ATR (volatility)
        highs = df['high'].tolist()
        lows = df['low'].tolist()
        closes = df['close'].tolist()

        atr_values = compute_atr(highs, lows, closes, period=14)
        if atr_values:
            current_atr = atr_values[-1]
            match_details["atr"] = round(current_atr, 2)

            if criteria.min_atr and current_atr < criteria.min_atr:
                matches = False
            if criteria.max_atr and current_atr > criteria.max_atr:
                matches = False

        # Minervini Trend Template
        if criteria.minervini_template:
            template_result = minervini_trend_template(df, "1day", symbol="")
            match_details["minervini_template"] = template_result.get("passes", False)

            if not template_result.get("passes", False):
                matches = False

        # Gap detection
        if criteria.gap_up_today and len(df) > 1:
            prev_close = float(df['close'].iloc[-2])
            current_open = float(df['open'].iloc[-1])
            gap_pct = ((current_open - prev_close) / prev_close) * 100

            match_details["gap_pct"] = round(gap_pct, 2)

            min_gap = criteria.min_gap_pct if criteria.min_gap_pct else 2.0
            if gap_pct < min_gap:
                matches = False

        return {
            "matches": matches,
            "details": match_details
        }

    def _calculate_score(self, match_result: Dict[str, Any], criteria: FilterCriteria) -> float:
        """Calculate a score for the matched stock (0-100)"""
        score = 50.0  # Base score

        details = match_result.get("details", {})

        # RS Rating contributes up to 20 points
        rs_rating = details.get("rs_rating")
        if rs_rating:
            score += (rs_rating / 100) * 20

        # Price momentum contributes up to 15 points
        price_change = details.get("price_change_pct")
        if price_change:
            # Normalize to 0-15 range (assume max 50% change)
            momentum_score = min(abs(price_change) / 50 * 15, 15)
            score += momentum_score if price_change > 0 else -momentum_score

        # Position above SMA50 contributes up to 10 points
        pct_above_sma = details.get("pct_above_sma_50")
        if pct_above_sma is not None:
            # Within 0-10% above SMA50 is ideal
            if 0 <= pct_above_sma <= 10:
                score += 10
            elif pct_above_sma > 10:
                score += max(0, 10 - (pct_above_sma - 10) * 0.5)

        # Minervini template match adds 15 points
        if details.get("minervini_template"):
            score += 15

        # Gap up adds 10 points
        gap_pct = details.get("gap_pct")
        if gap_pct and gap_pct > 2:
            score += min(gap_pct, 10)

        return max(0, min(100, score))

    async def _detect_patterns(
        self,
        df: pd.DataFrame,
        symbol: str,
        pattern_types: List[str],
        min_confidence: float
    ) -> List[Dict[str, Any]]:
        """Detect specified patterns in the data"""
        patterns_found = []

        try:
            detectors = get_all_detectors()
            pattern_types_lower = [p.lower() for p in pattern_types]

            for detector in detectors:
                # Check if this detector matches requested patterns
                if detector.name.lower() not in pattern_types_lower:
                    continue

                try:
                    results = detector.find(df, "1day", symbol)

                    for result in results:
                        if result.confidence >= min_confidence:
                            patterns_found.append({
                                "type": result.pattern_type.value,
                                "confidence": round(result.confidence, 2),
                                "entry_price": round(result.entry_price, 2) if result.entry_price else None,
                                "stop_price": round(result.stop_price, 2) if result.stop_price else None,
                                "target_price": round(result.target_price, 2) if result.target_price else None,
                            })
                except Exception as e:
                    logger.debug(f"Pattern detection failed for {symbol} with {detector.name}: {e}")

        except Exception as e:
            logger.error(f"Pattern detection error for {symbol}: {e}")

        return patterns_found

    def _to_dataframe(self, price_data: Dict[str, Any]) -> pd.DataFrame:
        """Convert price data to DataFrame"""
        df = pd.DataFrame({
            'open': price_data.get('o', []),
            'high': price_data.get('h', []),
            'low': price_data.get('l', []),
            'close': price_data.get('c', []),
            'volume': price_data.get('v', [])
        })

        # Ensure numeric types
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        return df

    def _empty_response(self, started: float) -> Dict[str, Any]:
        """Return empty response"""
        duration = time.perf_counter() - started
        return {
            "as_of": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "universe_size": 0,
            "results": [],
            "meta": {
                "build_sha": resolve_build_sha(),
                "duration_ms": round(duration * 1000, 2),
                "result_count": 0,
                "total_scanned": 0,
            }
        }


# Global service instance
advanced_screener_service = AdvancedScreenerService()
