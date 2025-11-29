"""
Double Top/Bottom Pattern Detector
Implements double top (bearish) and double bottom (bullish) reversal patterns
"""

from datetime import datetime
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from app.core.detector_base import (Detector, PatternResult, PatternType,
                                    StatsHelper)
from app.core.detector_config import DoubleTopBottomConfig


class DoubleTopBottomDetector(Detector):
    """
    Detects Double Top and Double Bottom patterns

    Patterns:
    - Double Top: Two peaks at similar levels (bearish reversal)
    - Double Bottom: Two troughs at similar levels (bullish reversal)
    """

    def __init__(self, **kwargs):
        super().__init__("Double Top/Bottom Detector", **kwargs)
        self.cfg = DoubleTopBottomConfig()

        for key, value in kwargs.items():
            if hasattr(self.cfg, key.upper()):
                setattr(self.cfg, key.upper(), value)

    def find(
        self, ohlcv: pd.DataFrame, timeframe: str, symbol: str
    ) -> List[PatternResult]:
        """Detect double top/bottom patterns in OHLCV data"""
        if len(ohlcv) < 20:  # Minimum length for pattern
            return []

        results = []

        try:
            # Calculate ATR
            high = ohlcv["high"].values
            low = ohlcv["low"].values
            close = ohlcv["close"].values
            atr = StatsHelper.atr(high, low, close)

            # Get pivots with tight threshold for double tops/bottoms
            pivots_tuples = StatsHelper.zigzag_pivots(high, low, close, atr)
            pivots = [
                {"index": p[0], "price": p[1], "type": p[2]} for p in pivots_tuples
            ]

            if len(pivots) < 3:  # Need at least peak-valley-peak or valley-peak-valley
                return []

            # Try double top
            double_top = self._detect_double_top(
                ohlcv, pivots, atr[-1], timeframe, symbol
            )
            if double_top:
                results.append(double_top)

            # Try double bottom
            double_bottom = self._detect_double_bottom(
                ohlcv, pivots, atr[-1], timeframe, symbol
            )
            if double_bottom:
                results.append(double_bottom)

        except Exception as e:
            logger.exception(f"Error in Double Top/Bottom detection: {e}")

        return results

    def _detect_double_top(
        self,
        ohlcv: pd.DataFrame,
        pivots: List[Dict],
        atr: float,
        timeframe: str,
        symbol: str,
    ) -> Optional[PatternResult]:
        """
        Double Top: Two peaks at similar prices
        """
        peaks = [p for p in pivots if p["type"] == "high"]
        valleys = [p for p in pivots if p["type"] == "low"]

        if len(peaks) < 2 or len(valleys) < 1:
            return None

        # Look for two consecutive peaks with similar heights
        for i in range(len(peaks) - 1):
            peak1 = peaks[i]
            peak2 = peaks[i + 1]

            # Check peaks are at similar levels (within tolerance)
            price_diff_pct = abs(peak1["price"] - peak2["price"]) / peak1["price"]

            if price_diff_pct > self.cfg.PEAK_PRICE_TOLERANCE:
                continue

            # Find valley between peaks
            valley = None
            for v in valleys:
                if peak1["index"] < v["index"] < peak2["index"]:
                    if valley is None or v["price"] < valley["price"]:
                        valley = v

            if not valley:
                continue

            # Calculate pullback depth
            avg_peak = (peak1["price"] + peak2["price"]) / 2
            pullback_depth = (avg_peak - valley["price"]) / avg_peak

            # Check minimum pullback (use INTERMEDIATE_SWING_ATR converted to percentage)
            min_pullback = self.cfg.INTERMEDIATE_SWING_ATR * atr / avg_peak
            if pullback_depth < min_pullback:
                continue

            # Check time separation
            time_separation = peak2["index"] - peak1["index"]
            if (
                time_separation < self.cfg.MIN_TIME_SEPARATION
                or time_separation > self.cfg.MAX_TIME_SEPARATION
            ):
                continue

            # Check second peak doesn't exceed first significantly (confirming pattern)
            if peak2["price"] > peak1["price"] * 1.02:  # More than 2% higher
                continue

            # Calculate confidence
            confidence = self._calculate_confidence(
                price_diff_pct, pullback_depth, time_separation, "top"
            )

            if confidence < 0.40:
                continue

            # Build pattern
            start_idx = peak1["index"]
            end_idx = peak2["index"]

            window_start = (
                ohlcv.index[start_idx].isoformat()
                if hasattr(ohlcv.index[start_idx], "isoformat")
                else str(ohlcv.index[start_idx])
            )
            window_end = (
                ohlcv.index[end_idx].isoformat()
                if hasattr(ohlcv.index[end_idx], "isoformat")
                else str(ohlcv.index[end_idx])
            )

            return PatternResult(
                symbol=symbol,
                timeframe=timeframe,
                asof=datetime.now().isoformat(),
                pattern_type=PatternType.DOUBLE_TOP,
                strong=confidence >= 0.75 and pullback_depth >= 0.10,
                confidence=confidence,
                window_start=window_start,
                window_end=window_end,
                lines={
                    "peak1_price": peak1["price"],
                    "peak2_price": peak2["price"],
                    "valley_price": valley["price"],
                    "resistance_level": avg_peak,
                },
                touches={"resistance": 2, "peaks": 2},
                breakout=None,
                evidence={
                    "price_similarity": 1.0 - price_diff_pct,
                    "pullback_depth": pullback_depth,
                    "time_separation": time_separation,
                    "atr": atr,
                },
            )

        return None

    def _detect_double_bottom(
        self,
        ohlcv: pd.DataFrame,
        pivots: List[Dict],
        atr: float,
        timeframe: str,
        symbol: str,
    ) -> Optional[PatternResult]:
        """
        Double Bottom: Two troughs at similar prices
        """
        troughs = [p for p in pivots if p["type"] == "low"]
        peaks = [p for p in pivots if p["type"] == "high"]

        if len(troughs) < 2 or len(peaks) < 1:
            return None

        # Look for two consecutive troughs with similar levels
        for i in range(len(troughs) - 1):
            trough1 = troughs[i]
            trough2 = troughs[i + 1]

            # Check troughs are at similar levels
            price_diff_pct = abs(trough1["price"] - trough2["price"]) / trough1["price"]

            if price_diff_pct > self.cfg.PEAK_PRICE_TOLERANCE:
                continue

            # Find peak between troughs
            peak = None
            for p in peaks:
                if trough1["index"] < p["index"] < trough2["index"]:
                    if peak is None or p["price"] > peak["price"]:
                        peak = p

            if not peak:
                continue

            # Calculate rally height
            avg_trough = (trough1["price"] + trough2["price"]) / 2
            rally_height = (peak["price"] - avg_trough) / avg_trough

            # Check minimum rally
            min_rally = self.cfg.INTERMEDIATE_SWING_ATR * atr / avg_trough
            if rally_height < min_rally:
                continue

            # Check time separation
            time_separation = trough2["index"] - trough1["index"]
            if (
                time_separation < self.cfg.MIN_TIME_SEPARATION
                or time_separation > self.cfg.MAX_TIME_SEPARATION
            ):
                continue

            # Check second trough doesn't fall below first significantly
            if trough2["price"] < trough1["price"] * 0.98:  # More than 2% lower
                continue

            # Calculate confidence
            confidence = self._calculate_confidence(
                price_diff_pct, rally_height, time_separation, "bottom"
            )

            if confidence < 0.40:
                continue

            # Build pattern
            start_idx = trough1["index"]
            end_idx = trough2["index"]

            window_start = (
                ohlcv.index[start_idx].isoformat()
                if hasattr(ohlcv.index[start_idx], "isoformat")
                else str(ohlcv.index[start_idx])
            )
            window_end = (
                ohlcv.index[end_idx].isoformat()
                if hasattr(ohlcv.index[end_idx], "isoformat")
                else str(ohlcv.index[end_idx])
            )

            return PatternResult(
                symbol=symbol,
                timeframe=timeframe,
                asof=datetime.now().isoformat(),
                pattern_type=PatternType.DOUBLE_BOTTOM,
                strong=confidence >= 0.75 and rally_height >= 0.10,
                confidence=confidence,
                window_start=window_start,
                window_end=window_end,
                lines={
                    "trough1_price": trough1["price"],
                    "trough2_price": trough2["price"],
                    "peak_price": peak["price"],
                    "support_level": avg_trough,
                },
                touches={"support": 2, "troughs": 2},
                breakout=None,
                evidence={
                    "price_similarity": 1.0 - price_diff_pct,
                    "rally_height": rally_height,
                    "time_separation": time_separation,
                    "atr": atr,
                },
            )

        return None

    def _calculate_confidence(
        self,
        price_diff_pct: float,
        depth_or_height: float,
        time_separation: int,
        pattern_type: str,
    ) -> float:
        """Calculate double top/bottom confidence"""

        # Price similarity score (35%)
        similarity_score = 1.0 - (price_diff_pct / self.cfg.PEAK_PRICE_TOLERANCE)
        similarity_score = max(0, min(1, similarity_score))

        # Depth/height score (35%)
        depth_score = min(1.0, depth_or_height / 0.15)  # Ideal 15% or more

        # Time separation score (20%)
        ideal_sep = (self.cfg.MIN_TIME_SEPARATION + self.cfg.MAX_TIME_SEPARATION) / 2
        sep_score = 1.0 - abs(time_separation - ideal_sep) / ideal_sep
        sep_score = max(0, min(1, sep_score))

        # Structure quality (10%)
        structure_score = 0.7  # Baseline for double top/bottom

        confidence = (
            0.35 * similarity_score
            + 0.35 * depth_score
            + 0.20 * sep_score
            + 0.10 * structure_score
        )

        return np.clip(confidence, 0, 1)
