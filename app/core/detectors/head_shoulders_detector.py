"""
Head & Shoulders Pattern Detector
Implements both regular (topping) and inverse (bottoming) patterns
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

from app.core.detector_base import (Detector, GeometryHelper, PatternResult,
                                    PatternType, StatsHelper)
from app.core.detector_config import HeadShouldersConfig


class HeadShouldersDetector(Detector):
    """
    Detects Head & Shoulders patterns

    Patterns:
    - Head & Shoulders: Three peaks, middle highest (bearish reversal)
    - Inverse H&S: Three troughs, middle lowest (bullish reversal)
    """

    def __init__(self, **kwargs):
        super().__init__("Head & Shoulders Detector", **kwargs)
        self.cfg = HeadShouldersConfig()

        for key, value in kwargs.items():
            if hasattr(self.cfg, key.upper()):
                setattr(self.cfg, key.upper(), value)

    def find(
        self, ohlcv: pd.DataFrame, timeframe: str, symbol: str
    ) -> List[PatternResult]:
        """Detect H&S patterns in OHLCV data"""
        if len(ohlcv) < self.cfg.MIN_LENGTH:
            return []

        results = []

        try:
            # Calculate ATR
            high = ohlcv["high"].values
            low = ohlcv["low"].values
            close = ohlcv["close"].values
            atr = StatsHelper.atr(high, low, close)

            # Get pivots
            pivots_tuples = StatsHelper.zigzag_pivots(high, low, close, atr)
            pivots = [
                {"index": p[0], "price": p[1], "type": p[2]} for p in pivots_tuples
            ]

            if len(pivots) < 7:  # Need at least 7 pivots for H&S
                return []

            # Try regular H&S
            regular = self._detect_regular_hs(ohlcv, pivots, atr[-1], timeframe, symbol)
            if regular:
                results.append(regular)

            # Try inverse H&S
            inverse = self._detect_inverse_hs(ohlcv, pivots, atr[-1], timeframe, symbol)
            if inverse:
                results.append(inverse)

        except Exception as e:
            logger.exception(f"Error in Head & Shoulders detection: {e}")

        return results

    def _has_prior_uptrend(
        self, ohlcv: pd.DataFrame, pattern_start_idx: int, lookback: int = 30
    ) -> bool:
        """
        Check if there's a prior uptrend before the pattern.
        Required for bearish H&S (reversal pattern - must reverse from uptrend).

        Args:
            ohlcv: Price data
            pattern_start_idx: Index where pattern starts (left shoulder)
            lookback: Number of bars to look back before pattern

        Returns:
            True if prior uptrend exists
        """
        if pattern_start_idx < lookback:
            return False

        # Get prices before pattern
        start = max(0, pattern_start_idx - lookback)
        end = pattern_start_idx
        prior_prices = ohlcv["close"].iloc[start:end]

        if len(prior_prices) < 20:
            return False

        # Check if trend is rising (first half < second half)
        mid = len(prior_prices) // 2
        first_half_avg = prior_prices.iloc[:mid].mean()
        second_half_avg = prior_prices.iloc[mid:].mean()

        # Must have at least 5% rise in the prior period
        trend_rise = (second_half_avg - first_half_avg) / first_half_avg
        return trend_rise > 0.05

    def _has_prior_downtrend(
        self, ohlcv: pd.DataFrame, pattern_start_idx: int, lookback: int = 30
    ) -> bool:
        """
        Check if there's a prior downtrend before the pattern.
        Required for inverse H&S (reversal pattern - must reverse from downtrend).

        Args:
            ohlcv: Price data
            pattern_start_idx: Index where pattern starts (left shoulder)
            lookback: Number of bars to look back before pattern

        Returns:
            True if prior downtrend exists
        """
        if pattern_start_idx < lookback:
            return False

        # Get prices before pattern
        start = max(0, pattern_start_idx - lookback)
        end = pattern_start_idx
        prior_prices = ohlcv["close"].iloc[start:end]

        if len(prior_prices) < 20:
            return False

        # Check if trend is falling (first half > second half)
        mid = len(prior_prices) // 2
        first_half_avg = prior_prices.iloc[:mid].mean()
        second_half_avg = prior_prices.iloc[mid:].mean()

        # Must have at least 5% decline in the prior period
        trend_decline = (first_half_avg - second_half_avg) / first_half_avg
        return trend_decline > 0.05

    def _has_declining_volume(
        self, ohlcv: pd.DataFrame, start_idx: int, end_idx: int
    ) -> bool:
        """
        Check if volume is declining through the pattern.
        H&S patterns typically show declining volume as pattern forms.

        Args:
            ohlcv: Price data
            start_idx: Pattern start index
            end_idx: Pattern end index

        Returns:
            True if volume is declining
        """
        if "volume" not in ohlcv.columns:
            return True  # Skip if no volume data

        pattern_volume = ohlcv["volume"].iloc[start_idx : end_idx + 1]

        if len(pattern_volume) < 10:
            return True

        # Compare first half vs second half volume
        mid = len(pattern_volume) // 2
        first_half_avg = pattern_volume.iloc[:mid].mean()
        second_half_avg = pattern_volume.iloc[mid:].mean()

        # Second half should have at least 10% lower volume
        return second_half_avg < first_half_avg * 0.9

    def _is_below_neckline(
        self, ohlcv: pd.DataFrame, neckline_slope: float, neckline_intercept: float
    ) -> bool:
        """
        Check if current price is below neckline (bearish confirmation).

        Args:
            ohlcv: Price data
            neckline_slope: Neckline slope
            neckline_intercept: Neckline intercept

        Returns:
            True if current price is below neckline
        """
        current_idx = len(ohlcv) - 1
        current_price = ohlcv["close"].iloc[-1]
        expected_neckline = neckline_slope * current_idx + neckline_intercept

        # Price must be at least 1% below neckline for bearish confirmation
        return current_price < expected_neckline * 0.99

    def _is_above_neckline(
        self, ohlcv: pd.DataFrame, neckline_slope: float, neckline_intercept: float
    ) -> bool:
        """
        Check if current price is above neckline (bullish confirmation).

        Args:
            ohlcv: Price data
            neckline_slope: Neckline slope
            neckline_intercept: Neckline intercept

        Returns:
            True if current price is above neckline
        """
        current_idx = len(ohlcv) - 1
        current_price = ohlcv["close"].iloc[-1]
        expected_neckline = neckline_slope * current_idx + neckline_intercept

        # Price must be at least 1% above neckline for bullish confirmation
        return current_price > expected_neckline * 1.01

    def _detect_regular_hs(
        self,
        ohlcv: pd.DataFrame,
        pivots: List[Dict],
        atr: float,
        timeframe: str,
        symbol: str,
    ) -> Optional[PatternResult]:
        """
        Regular Head & Shoulders (topping pattern)
        Pattern: Peak - Valley - Higher Peak - Valley - Peak
        """
        # Filter for high pivots (peaks)
        peaks = [p for p in pivots if p["type"] == "high"]
        valleys = [p for p in pivots if p["type"] == "low"]

        if len(peaks) < 3 or len(valleys) < 2:
            return None

        # Look for three-peak pattern in recent data
        for i in range(len(peaks) - 2):
            left_shoulder = peaks[i]
            head = peaks[i + 1]
            right_shoulder = peaks[i + 2]

            # ✅ VALIDATION 1: Prior uptrend required (bearish H&S is a REVERSAL pattern)
            if not self._has_prior_uptrend(ohlcv, left_shoulder["index"]):
                continue

            # Head must be highest
            if head["price"] <= max(left_shoulder["price"], right_shoulder["price"]):
                continue

            # Check head is sufficiently higher
            head_prominence = (
                head["price"] - max(left_shoulder["price"], right_shoulder["price"])
            ) / atr
            if head_prominence < self.cfg.HEAD_MIN_RATIO:
                continue

            # ✅ VALIDATION 2: Shoulders must be very similar (tightened from 15% to 5% tolerance)
            shoulder_ratio = min(left_shoulder["price"], right_shoulder["price"]) / max(
                left_shoulder["price"], right_shoulder["price"]
            )
            if shoulder_ratio < 0.95:  # Tightened from 0.85 to 0.95 (5% max difference)
                continue

            # Find valleys between peaks for neckline
            left_valley = None
            right_valley = None

            for v in valleys:
                if left_shoulder["index"] < v["index"] < head["index"]:
                    if left_valley is None or v["price"] < left_valley["price"]:
                        left_valley = v

                if head["index"] < v["index"] < right_shoulder["index"]:
                    if right_valley is None or v["price"] < right_valley["price"]:
                        right_valley = v

            if not left_valley or not right_valley:
                continue

            # Fit neckline through valleys
            neckline_points = [
                (left_valley["index"], left_valley["price"]),
                (right_valley["index"], right_valley["price"]),
            ]

            neckline = GeometryHelper.fit_line_ransac(neckline_points)
            if not neckline:
                continue

            slope, intercept = neckline[0], neckline[1]

            # Calculate R² for neckline quality
            expected = [slope * p[0] + intercept for p in neckline_points]
            actual = [p[1] for p in neckline_points]
            ss_res = sum((a - e) ** 2 for a, e in zip(actual, expected))
            ss_tot = sum((a - np.mean(actual)) ** 2 for a in actual)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

            if r_squared < self.cfg.NECKLINE_MIN_R_SQUARED:
                continue

            # Build pattern window for validation
            start_idx = left_shoulder["index"]
            end_idx = right_shoulder["index"]

            # ✅ VALIDATION 3: Volume must be declining through pattern
            if not self._has_declining_volume(ohlcv, start_idx, end_idx):
                continue

            # ✅ VALIDATION 4: Current price must be below neckline (bearish confirmation)
            # Only detect confirmed patterns, not just formations
            if not self._is_below_neckline(ohlcv, slope, intercept):
                continue

            # Calculate confidence
            confidence = self._calculate_confidence(
                head_prominence,
                shoulder_ratio,
                r_squared,
                right_shoulder["index"] - left_shoulder["index"],
            )

            if confidence < 0.40:
                continue

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
                pattern_type=PatternType.HEAD_SHOULDERS,
                strong=confidence >= 0.75 and r_squared >= 0.90,
                confidence=confidence,
                window_start=window_start,
                window_end=window_end,
                lines={
                    "left_shoulder_price": left_shoulder["price"],
                    "head_price": head["price"],
                    "right_shoulder_price": right_shoulder["price"],
                    "neckline_slope": slope,
                    "neckline_intercept": intercept,
                },
                touches={"neckline": 2, "pattern_peaks": 3},
                breakout=None,
                evidence={
                    "head_prominence": head_prominence,
                    "shoulder_symmetry": shoulder_ratio,
                    "neckline_r2": r_squared,
                    "pattern_length": end_idx - start_idx,
                    "atr": atr,
                },
            )

        return None

    def _detect_inverse_hs(
        self,
        ohlcv: pd.DataFrame,
        pivots: List[Dict],
        atr: float,
        timeframe: str,
        symbol: str,
    ) -> Optional[PatternResult]:
        """
        Inverse Head & Shoulders (bottoming pattern)
        Pattern: Trough - Peak - Lower Trough - Peak - Trough
        """
        # Filter for low pivots (troughs)
        troughs = [p for p in pivots if p["type"] == "low"]
        peaks = [p for p in pivots if p["type"] == "high"]

        if len(troughs) < 3 or len(peaks) < 2:
            return None

        # Look for three-trough pattern
        for i in range(len(troughs) - 2):
            left_shoulder = troughs[i]
            head = troughs[i + 1]
            right_shoulder = troughs[i + 2]

            # ✅ VALIDATION 1: Prior downtrend required (inverse H&S is a REVERSAL pattern)
            if not self._has_prior_downtrend(ohlcv, left_shoulder["index"]):
                continue

            # Head must be lowest
            if head["price"] >= min(left_shoulder["price"], right_shoulder["price"]):
                continue

            # Check head is sufficiently lower
            head_depth = (
                min(left_shoulder["price"], right_shoulder["price"]) - head["price"]
            ) / atr
            if head_depth < self.cfg.HEAD_MIN_RATIO:
                continue

            # ✅ VALIDATION 2: Shoulders must be very similar (tightened from 15% to 5% tolerance)
            shoulder_ratio = min(left_shoulder["price"], right_shoulder["price"]) / max(
                left_shoulder["price"], right_shoulder["price"]
            )
            if shoulder_ratio < 0.95:  # Tightened from 0.85 to 0.95 (5% max difference)
                continue

            # Find peaks between troughs for neckline
            left_peak = None
            right_peak = None

            for p in peaks:
                if left_shoulder["index"] < p["index"] < head["index"]:
                    if left_peak is None or p["price"] > left_peak["price"]:
                        left_peak = p

                if head["index"] < p["index"] < right_shoulder["index"]:
                    if right_peak is None or p["price"] > right_peak["price"]:
                        right_peak = p

            if not left_peak or not right_peak:
                continue

            # Fit neckline through peaks
            neckline_points = [
                (left_peak["index"], left_peak["price"]),
                (right_peak["index"], right_peak["price"]),
            ]

            neckline = GeometryHelper.fit_line_ransac(neckline_points)
            if not neckline:
                continue

            slope, intercept = neckline[0], neckline[1]

            # Calculate R² for neckline quality
            expected = [slope * p[0] + intercept for p in neckline_points]
            actual = [p[1] for p in neckline_points]
            ss_res = sum((a - e) ** 2 for a, e in zip(actual, expected))
            ss_tot = sum((a - np.mean(actual)) ** 2 for a in actual)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

            if r_squared < self.cfg.NECKLINE_MIN_R_SQUARED:
                continue

            # Build pattern window for validation
            start_idx = left_shoulder["index"]
            end_idx = right_shoulder["index"]

            # ✅ VALIDATION 3: Volume must be declining through pattern
            if not self._has_declining_volume(ohlcv, start_idx, end_idx):
                continue

            # ✅ VALIDATION 4: Current price must be above neckline (bullish confirmation)
            # Only detect confirmed patterns, not just formations
            if not self._is_above_neckline(ohlcv, slope, intercept):
                continue

            # Calculate confidence
            confidence = self._calculate_confidence(
                head_depth,
                shoulder_ratio,
                r_squared,
                right_shoulder["index"] - left_shoulder["index"],
            )

            if confidence < 0.40:
                continue

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
                pattern_type=PatternType.HEAD_SHOULDERS_INV,
                strong=confidence >= 0.75 and r_squared >= 0.90,
                confidence=confidence,
                window_start=window_start,
                window_end=window_end,
                lines={
                    "left_shoulder_price": left_shoulder["price"],
                    "head_price": head["price"],
                    "right_shoulder_price": right_shoulder["price"],
                    "neckline_slope": slope,
                    "neckline_intercept": intercept,
                },
                touches={"neckline": 2, "pattern_troughs": 3},
                breakout=None,
                evidence={
                    "head_depth": head_depth,
                    "shoulder_symmetry": shoulder_ratio,
                    "neckline_r2": r_squared,
                    "pattern_length": end_idx - start_idx,
                    "atr": atr,
                },
            )

        return None

    def _calculate_confidence(
        self,
        head_prominence: float,
        shoulder_symmetry: float,
        neckline_r2: float,
        pattern_length: int,
    ) -> float:
        """Calculate H&S pattern confidence"""

        # Head prominence score (30%)
        prominence_score = min(1.0, head_prominence / 2.0)

        # Shoulder symmetry score (30%)
        symmetry_score = shoulder_symmetry

        # Neckline quality score (30%)
        neckline_score = neckline_r2

        # Pattern length score (10%)
        ideal_length = 60
        length_score = min(1.0, pattern_length / ideal_length)

        confidence = (
            0.30 * prominence_score
            + 0.30 * symmetry_score
            + 0.30 * neckline_score
            + 0.10 * length_score
        )

        return np.clip(confidence, 0, 1)
