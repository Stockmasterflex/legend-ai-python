"""
Triangle Pattern Detector
Implements Ascending, Descending, and Symmetrical Triangle detection
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from app.core.detector_base import (Detector, GeometryHelper, PatternResult,
                                    PatternType, StatsHelper)
from app.core.detector_config import TriangleConfig

logger = logging.getLogger(__name__)


class TriangleDetector(Detector):
    """
    Detects triangle patterns using geometric line fitting

    Patterns:
    - Ascending Triangle: Flat top, rising bottom
    - Descending Triangle: Flat bottom, falling top
    - Symmetrical Triangle: Converging lines
    """

    def __init__(self, **kwargs):
        super().__init__("Triangle Detector", **kwargs)
        self.cfg = TriangleConfig()

        # Override config with kwargs
        for key, value in kwargs.items():
            if hasattr(self.cfg, key.upper()):
                setattr(self.cfg, key.upper(), value)

    def find(
        self, ohlcv: pd.DataFrame, timeframe: str, symbol: str
    ) -> List[PatternResult]:
        """Detect triangle patterns in OHLCV data"""
        if len(ohlcv) < self.cfg.MIN_LENGTH:
            return []

        results = []

        try:
            # Calculate ATR for thresholds
            high = ohlcv["high"].values
            low = ohlcv["low"].values
            close = ohlcv["close"].values
            atr = StatsHelper.atr(high, low, close)

            # Get swing pivots
            pivots_tuples = StatsHelper.zigzag_pivots(high, low, close, atr)
            pivots = [
                {"index": p[0], "price": p[1], "type": p[2]} for p in pivots_tuples
            ]

            if len(pivots) < 4:  # Need at least 4 pivots for a triangle
                return []

            # Try to find triangles in different lookback windows
            for lookback in [40, 60, 80, 100]:
                if len(ohlcv) < lookback:
                    continue

                window = ohlcv.iloc[-lookback:]
                window_pivots = [
                    p for p in pivots if p["index"] >= len(ohlcv) - lookback
                ]

                if len(window_pivots) < 4:
                    continue

                # Separate highs and lows
                highs = [p for p in window_pivots if p["type"] == "high"]
                lows = [p for p in window_pivots if p["type"] == "low"]

                if len(highs) < 2 or len(lows) < 2:
                    continue

                # Try each triangle type
                for pattern_type in ["ascending", "descending", "symmetrical"]:
                    pattern = self._detect_triangle_type(
                        window, highs, lows, pattern_type, atr[-1], timeframe, symbol
                    )
                    if pattern:
                        results.append(pattern)

        except Exception as e:
            logger.exception(f"Error in Triangle detection: {e}")

        return results

    def _detect_triangle_type(
        self,
        window: pd.DataFrame,
        highs: List[Dict],
        lows: List[Dict],
        pattern_type: str,
        atr: float,
        timeframe: str,
        symbol: str,
    ) -> Optional[PatternResult]:
        """Detect specific triangle type"""

        if pattern_type == "ascending":
            return self._detect_ascending(window, highs, lows, atr, timeframe, symbol)
        elif pattern_type == "descending":
            return self._detect_descending(window, highs, lows, atr, timeframe, symbol)
        elif pattern_type == "symmetrical":
            return self._detect_symmetrical(window, highs, lows, atr, timeframe, symbol)

        return None

    def _detect_ascending(
        self,
        window: pd.DataFrame,
        highs: List[Dict],
        lows: List[Dict],
        atr: float,
        timeframe: str,
        symbol: str,
    ) -> Optional[PatternResult]:
        """
        Ascending Triangle: Flat resistance, rising support
        """
        if len(highs) < 2 or len(lows) < 2:
            return None

        # Check if highs form flat resistance (all near same level)
        high_prices = [h["price"] for h in highs]
        high_mean = np.mean(high_prices)
        high_std = np.std(high_prices)

        # Highs should be within 1 ATR of each other (flat)
        flatness_tolerance = getattr(self.cfg, "FLATNESS_TOLERANCE_ATR", 1.0)
        if high_std > atr * flatness_tolerance:
            return None

        # Check if lows form rising support
        low_points = [(low["index"], low["price"]) for low in lows]
        low_line = GeometryHelper.fit_line_ransac(low_points)

        if not low_line:
            return None

        slope, intercept = low_line[0], low_line[1]

        # Support must be rising (positive slope)
        if slope <= 0:
            return None

        # Check convergence
        first_idx = lows[0]["index"]
        last_idx = lows[-1]["index"]

        resistance_level = high_mean
        support_start = slope * first_idx + intercept
        support_end = slope * last_idx + intercept

        # Calculate convergence
        start_gap = resistance_level - support_start
        end_gap = resistance_level - support_end

        if start_gap <= 0 or end_gap <= 0:
            return None

        convergence_ratio = end_gap / start_gap
        max_convergence = self.cfg.CONVERGENCE_THRESHOLD

        if convergence_ratio > (1 - max_convergence):
            return None

        # Count touches
        resistance_touches = sum(
            1 for h in high_prices if abs(h - high_mean) < atr * 0.5
        )

        support_touches = sum(
            1
            for low in lows
            if abs(low["price"] - (slope * low["index"] + intercept)) < atr * 0.5
        )

        min_touches = self.cfg.MIN_TOUCHES_PER_SIDE
        if resistance_touches < min_touches or support_touches < min_touches:
            return None

        # Calculate confidence
        confidence = self._calculate_confidence(
            resistance_touches,
            support_touches,
            1 - convergence_ratio,
            len(window),
            atr,
            high_std,
        )

        if confidence < 0.40:  # Minimum threshold
            return None

        # Build result
        window_start = (
            window.index[0].isoformat()
            if hasattr(window.index[0], "isoformat")
            else str(window.index[0])
        )
        window_end = (
            window.index[-1].isoformat()
            if hasattr(window.index[-1], "isoformat")
            else str(window.index[-1])
        )

        return PatternResult(
            symbol=symbol,
            timeframe=timeframe,
            asof=datetime.now().isoformat(),
            pattern_type=PatternType.TRIANGLE_ASC,
            strong=confidence >= 0.75 and resistance_touches >= 3,
            confidence=confidence,
            window_start=window_start,
            window_end=window_end,
            lines={
                "resistance": resistance_level,
                "support_slope": slope,
                "support_intercept": intercept,
            },
            touches={"resistance": resistance_touches, "support": support_touches},
            breakout=None,
            evidence={
                "convergence": 1 - convergence_ratio,
                "pattern_length": len(window),
                "atr": atr,
            },
        )

    def _detect_descending(
        self,
        window: pd.DataFrame,
        highs: List[Dict],
        lows: List[Dict],
        atr: float,
        timeframe: str,
        symbol: str,
    ) -> Optional[PatternResult]:
        """
        Descending Triangle: Flat support, falling resistance
        """
        if len(highs) < 2 or len(lows) < 2:
            return None

        # Check if lows form flat support
        low_prices = [low["price"] for low in lows]
        low_mean = np.mean(low_prices)
        low_std = np.std(low_prices)

        flatness_tolerance = getattr(self.cfg, "FLATNESS_TOLERANCE_ATR", 1.0)
        if low_std > atr * flatness_tolerance:
            return None

        # Check if highs form falling resistance
        high_points = [(h["index"], h["price"]) for h in highs]
        high_line = GeometryHelper.fit_line_ransac(high_points)

        if not high_line:
            return None

        slope, intercept = high_line[0], high_line[1]

        # Resistance must be falling (negative slope)
        if slope >= 0:
            return None

        # Check convergence
        first_idx = highs[0]["index"]
        last_idx = highs[-1]["index"]

        support_level = low_mean
        resistance_start = slope * first_idx + intercept
        resistance_end = slope * last_idx + intercept

        start_gap = resistance_start - support_level
        end_gap = resistance_end - support_level

        if start_gap <= 0 or end_gap <= 0:
            return None

        convergence_ratio = end_gap / start_gap
        max_convergence = self.cfg.CONVERGENCE_THRESHOLD

        if convergence_ratio > (1 - max_convergence):
            return None

        # Count touches
        support_touches = sum(1 for low_price in low_prices if abs(low_price - low_mean) < atr * 0.5)

        resistance_touches = sum(
            1
            for h in highs
            if abs(h["price"] - (slope * h["index"] + intercept)) < atr * 0.5
        )

        min_touches = self.cfg.MIN_TOUCHES_PER_SIDE
        if support_touches < min_touches or resistance_touches < min_touches:
            return None

        # Calculate confidence
        confidence = self._calculate_confidence(
            resistance_touches,
            support_touches,
            1 - convergence_ratio,
            len(window),
            atr,
            low_std,
        )

        if confidence < 0.40:
            return None

        window_start = (
            window.index[0].isoformat()
            if hasattr(window.index[0], "isoformat")
            else str(window.index[0])
        )
        window_end = (
            window.index[-1].isoformat()
            if hasattr(window.index[-1], "isoformat")
            else str(window.index[-1])
        )

        return PatternResult(
            symbol=symbol,
            timeframe=timeframe,
            asof=datetime.now().isoformat(),
            pattern_type=PatternType.TRIANGLE_DESC,
            strong=confidence >= 0.75 and support_touches >= 3,
            confidence=confidence,
            window_start=window_start,
            window_end=window_end,
            lines={
                "support": support_level,
                "resistance_slope": slope,
                "resistance_intercept": intercept,
            },
            touches={"support": support_touches, "resistance": resistance_touches},
            breakout=None,
            evidence={
                "convergence": 1 - convergence_ratio,
                "pattern_length": len(window),
                "atr": atr,
            },
        )

    def _detect_symmetrical(
        self,
        window: pd.DataFrame,
        highs: List[Dict],
        lows: List[Dict],
        atr: float,
        timeframe: str,
        symbol: str,
    ) -> Optional[PatternResult]:
        """
        Symmetrical Triangle: Both lines converging
        """
        if len(highs) < 2 or len(lows) < 2:
            return None

        # Fit resistance line (through highs)
        high_points = [(h["index"], h["price"]) for h in highs]
        high_line = GeometryHelper.fit_line_ransac(high_points)

        if not high_line:
            return None

        # Fit support line (through lows)
        low_points = [(low["index"], low["price"]) for low in lows]
        low_line = GeometryHelper.fit_line_ransac(low_points)

        if not low_line:
            return None

        high_slope, high_intercept = high_line[0], high_line[1]
        low_slope, low_intercept = low_line[0], low_line[1]

        # For symmetrical triangle:
        # - Resistance should be falling (negative slope)
        # - Support should be rising (positive slope)
        # - Slopes should be roughly symmetric

        if high_slope >= 0 or low_slope <= 0:
            return None

        # Check slope symmetry (absolute values should be similar)
        slope_ratio = abs(high_slope) / abs(low_slope) if low_slope != 0 else 0

        if slope_ratio < 0.5 or slope_ratio > 2.0:
            return None  # Slopes too asymmetric

        # Check convergence
        first_idx = min(highs[0]["index"], lows[0]["index"])
        last_idx = max(highs[-1]["index"], lows[-1]["index"])

        resistance_start = high_slope * first_idx + high_intercept
        resistance_end = high_slope * last_idx + high_intercept
        support_start = low_slope * first_idx + low_intercept
        support_end = low_slope * last_idx + low_intercept

        start_gap = resistance_start - support_start
        end_gap = resistance_end - support_end

        if start_gap <= 0 or end_gap <= 0:
            return None

        convergence_ratio = end_gap / start_gap
        max_convergence = self.cfg.CONVERGENCE_THRESHOLD

        if convergence_ratio > (1 - max_convergence):
            return None

        # Count touches
        resistance_touches = sum(
            1
            for h in highs
            if abs(h["price"] - (high_slope * h["index"] + high_intercept)) < atr * 0.5
        )

        support_touches = sum(
            1
            for low in lows
            if abs(low["price"] - (low_slope * low["index"] + low_intercept)) < atr * 0.5
        )

        min_touches = self.cfg.MIN_TOUCHES_PER_SIDE
        if resistance_touches < min_touches or support_touches < min_touches:
            return None

        # Calculate confidence
        confidence = self._calculate_confidence(
            resistance_touches,
            support_touches,
            1 - convergence_ratio,
            len(window),
            atr,
            0,
        )

        # Bonus for good symmetry
        symmetry_bonus = 0.1 * (1.0 - abs(1.0 - slope_ratio))
        confidence = min(1.0, confidence + symmetry_bonus)

        if confidence < 0.40:
            return None

        window_start = (
            window.index[0].isoformat()
            if hasattr(window.index[0], "isoformat")
            else str(window.index[0])
        )
        window_end = (
            window.index[-1].isoformat()
            if hasattr(window.index[-1], "isoformat")
            else str(window.index[-1])
        )

        return PatternResult(
            symbol=symbol,
            timeframe=timeframe,
            asof=datetime.now().isoformat(),
            pattern_type=PatternType.TRIANGLE_SYM,
            strong=confidence >= 0.75 and min(resistance_touches, support_touches) >= 3,
            confidence=confidence,
            window_start=window_start,
            window_end=window_end,
            lines={
                "resistance_slope": high_slope,
                "resistance_intercept": high_intercept,
                "support_slope": low_slope,
                "support_intercept": low_intercept,
            },
            touches={"resistance": resistance_touches, "support": support_touches},
            breakout=None,
            evidence={
                "convergence": 1 - convergence_ratio,
                "slope_symmetry": slope_ratio,
                "pattern_length": len(window),
                "atr": atr,
            },
        )

    def _calculate_confidence(
        self,
        resistance_touches: int,
        support_touches: int,
        convergence_score: float,
        pattern_length: int,
        atr: float,
        flatness_std: float,
    ) -> float:
        """Calculate pattern confidence score"""

        # Touch score (30%)
        total_touches = resistance_touches + support_touches
        touch_score = min(1.0, total_touches / 8.0)

        # Convergence score (35%)
        convergence_score = min(1.0, convergence_score / self.cfg.CONVERGENCE_THRESHOLD)

        # Structure score (20%) - length
        ideal_length = 60
        length_score = min(1.0, pattern_length / ideal_length)

        # Recency score (10%)
        recency_score = 1.0  # Always at right edge

        # Volume/quality score (5%)
        quality_score = 0.5  # Baseline
        if flatness_std < atr * 0.3:
            quality_score += 0.5

        confidence = (
            0.30 * touch_score
            + 0.35 * convergence_score
            + 0.20 * length_score
            + 0.10 * recency_score
            + 0.05 * quality_score
        )

        return np.clip(confidence, 0, 1)
