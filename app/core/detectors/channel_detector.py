"""
Channel Pattern Detector
Implements parallel channel detection (up, down, sideways)
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from app.core.detector_base import (Detector, GeometryHelper, PatternResult,
                                    PatternType, StatsHelper)
from app.core.detector_config import ChannelConfig

logger = logging.getLogger(__name__)


class ChannelDetector(Detector):
    """
    Detects channel patterns with parallel trendlines

    Patterns:
    - Up Channel: Rising parallel lines
    - Down Channel: Falling parallel lines
    - Sideways Channel: Horizontal parallel lines
    """

    def __init__(self, **kwargs):
        super().__init__("Channel Detector", **kwargs)
        self.cfg = ChannelConfig()

        for key, value in kwargs.items():
            if hasattr(self.cfg, key.upper()):
                setattr(self.cfg, key.upper(), value)

    def find(
        self, ohlcv: pd.DataFrame, timeframe: str, symbol: str
    ) -> List[PatternResult]:
        """Detect channel patterns in OHLCV data"""
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

            if len(pivots) < 4:
                return []

            highs = [p for p in pivots if p["type"] == "high"]
            lows = [p for p in pivots if p["type"] == "low"]

            if len(highs) < 2 or len(lows) < 2:
                return []

            # Try different channel types
            for channel_type in ["up", "down", "sideways"]:
                channel = self._detect_channel(
                    ohlcv, highs, lows, channel_type, atr[-1], timeframe, symbol
                )
                if channel:
                    results.append(channel)

        except Exception as e:
            logger.exception(f"Error in Channel detection: {e}")

        return results

    def _detect_channel(
        self,
        ohlcv: pd.DataFrame,
        highs: List[Dict],
        lows: List[Dict],
        channel_type: str,
        atr: float,
        timeframe: str,
        symbol: str,
    ) -> Optional[PatternResult]:
        """Detect specific channel type"""

        # Fit trendlines
        high_points = [(h["index"], h["price"]) for h in highs]
        high_line = GeometryHelper.fit_line_ransac(high_points)

        if not high_line:
            return None

        low_points = [(low["index"], low["price"]) for low in lows]
        low_line = GeometryHelper.fit_line_ransac(low_points)

        if not low_line:
            return None

        high_slope, high_intercept = high_line[0], high_line[1]
        low_slope, low_intercept = low_line[0], low_line[1]

        # Check channel type matches slope criteria
        if channel_type == "up":
            # Both slopes should be positive
            if high_slope <= 0 or low_slope <= 0:
                return None
        elif channel_type == "down":
            # Both slopes should be negative
            if high_slope >= 0 or low_slope >= 0:
                return None
        elif channel_type == "sideways":
            # Both slopes should be near zero
            avg_price = np.mean(
                [h["price"] for h in highs] + [low["price"] for low in lows]
            )
            high_slope_pct = abs(high_slope) / avg_price * 100
            low_slope_pct = abs(low_slope) / avg_price * 100

            if high_slope_pct > 2.0 or low_slope_pct > 2.0:  # More than 2% slope
                return None

        # Check parallelism (slopes should be similar)
        slope_ratio = 1.0
        if low_slope != 0:
            slope_ratio = high_slope / low_slope
            # Allow some variation but not too much
            if slope_ratio < 0.7 or slope_ratio > 1.3:  # Not parallel enough
                return None

        # Calculate channel width
        first_idx = min(highs[0]["index"], lows[0]["index"])
        last_idx = max(highs[-1]["index"], lows[-1]["index"])

        resistance_mid = high_slope * ((first_idx + last_idx) / 2) + high_intercept
        support_mid = low_slope * ((first_idx + last_idx) / 2) + low_intercept
        channel_width = resistance_mid - support_mid

        # Width should be reasonable (not too narrow or too wide)
        width_atr_ratio = channel_width / atr
        if width_atr_ratio < 2 or width_atr_ratio > 15:
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
            slope_ratio,
            last_idx - first_idx,
            width_atr_ratio,
        )

        if confidence < 0.40:
            return None

        # Determine pattern type
        if channel_type == "up":
            pattern_type = PatternType.CHANNEL_UP
        elif channel_type == "down":
            pattern_type = PatternType.CHANNEL_DOWN
        else:
            pattern_type = PatternType.CHANNEL_ANY

        window_start = (
            ohlcv.index[first_idx].isoformat()
            if hasattr(ohlcv.index[first_idx], "isoformat")
            else str(ohlcv.index[first_idx])
        )
        window_end = (
            ohlcv.index[last_idx].isoformat()
            if hasattr(ohlcv.index[last_idx], "isoformat")
            else str(ohlcv.index[last_idx])
        )

        return PatternResult(
            symbol=symbol,
            timeframe=timeframe,
            asof=datetime.now().isoformat(),
            pattern_type=pattern_type,
            strong=confidence >= 0.75 and min(resistance_touches, support_touches) >= 3,
            confidence=confidence,
            window_start=window_start,
            window_end=window_end,
            lines={
                "resistance_slope": high_slope,
                "resistance_intercept": high_intercept,
                "support_slope": low_slope,
                "support_intercept": low_intercept,
                "channel_width": channel_width,
            },
            touches={"resistance": resistance_touches, "support": support_touches},
            breakout=None,
            evidence={
                "slope_parallelism": slope_ratio,
                "channel_width_atr": width_atr_ratio,
                "pattern_length": last_idx - first_idx,
                "direction": channel_type,
            },
        )

    def _calculate_confidence(
        self,
        resistance_touches: int,
        support_touches: int,
        parallelism: float,
        pattern_length: int,
        width_atr_ratio: float,
    ) -> float:
        """Calculate channel confidence"""

        # Touch score (30%)
        total_touches = resistance_touches + support_touches
        touch_score = min(1.0, total_touches / 8.0)

        # Parallelism score (35%)
        parallelism_score = 1.0 - abs(1.0 - parallelism)
        parallelism_score = max(0, min(1, parallelism_score))

        # Length score (20%)
        ideal_length = 50
        length_score = min(1.0, pattern_length / ideal_length)

        # Width quality score (15%)
        ideal_width = 6.0  # ATR multiples
        width_score = 1.0 - abs(width_atr_ratio - ideal_width) / ideal_width
        width_score = max(0, min(1, width_score))

        confidence = (
            0.30 * touch_score
            + 0.35 * parallelism_score
            + 0.20 * length_score
            + 0.15 * width_score
        )

        return np.clip(confidence, 0, 1)
