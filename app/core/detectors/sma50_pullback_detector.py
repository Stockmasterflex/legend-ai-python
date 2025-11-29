"""
50 SMA Pullback Pattern Detector
Detects bullish pullback opportunities near the 50-period SMA
"""

from datetime import datetime
from typing import List

import numpy as np
import pandas as pd

from app.core.detector_base import Detector, PatternResult, PatternType


class SMA50PullbackDetector(Detector):
    """
    Detects pullback patterns to the 50-period Simple Moving Average

    Criteria:
    - Stock in uptrend (above 50/200 SMA)
    - Price pulls back to 50 SMA
    - Finds support at 50 SMA
    - Volume declining on pullback
    - Bullish bounce setup
    """

    def __init__(self, **kwargs):
        super().__init__("50 SMA Pullback Detector", **kwargs)
        self.max_distance_pct = kwargs.get("max_distance_pct", 3.0)  # 3% from 50 SMA
        self.lookback = kwargs.get("lookback", 10)  # Recent bars to check
        self.min_uptrend_bars = kwargs.get(
            "min_uptrend_bars", 20
        )  # Bars above SMA for uptrend

    def find(
        self, ohlcv: pd.DataFrame, timeframe: str, symbol: str
    ) -> List[PatternResult]:
        """Detect 50 SMA pullback patterns"""
        if len(ohlcv) < 200:  # Need enough history for 200 SMA
            return []

        results = []

        try:
            # Calculate SMAs
            ohlcv = ohlcv.copy()
            ohlcv["sma_50"] = ohlcv["close"].rolling(window=50).mean()
            ohlcv["sma_200"] = ohlcv["close"].rolling(window=200).mean()

            # Need valid SMAs
            if ohlcv["sma_50"].isna().iloc[-1] or ohlcv["sma_200"].isna().iloc[-1]:
                return []

            current_price = ohlcv["close"].iloc[-1]
            sma_50 = ohlcv["sma_50"].iloc[-1]
            sma_200 = ohlcv["sma_200"].iloc[-1]

            # Check uptrend criteria
            if not self._is_in_uptrend(ohlcv):
                return []

            # Check if price is near 50 SMA
            distance_pct = abs(current_price - sma_50) / sma_50 * 100

            if distance_pct > self.max_distance_pct:
                return []

            # Check for pullback (recent high above current price)
            recent_window = ohlcv.iloc[-20:]
            recent_high = recent_window["high"].max()
            pullback_depth = (recent_high - current_price) / recent_high * 100

            if pullback_depth < 3 or pullback_depth > 15:  # 3-15% pullback
                return []

            # Check volume decline on pullback
            volume_declining = self._check_volume_decline(ohlcv)

            # Check for bounce signals
            bounce_signal = self._check_bounce_signals(ohlcv)

            # Calculate confidence
            confidence = self._calculate_confidence(
                distance_pct,
                pullback_depth,
                volume_declining,
                bounce_signal,
                current_price > sma_200,
            )

            if confidence < 0.40:
                return []

            # Build result
            window_start = (
                ohlcv.index[-20].isoformat()
                if hasattr(ohlcv.index[-20], "isoformat")
                else str(ohlcv.index[-20])
            )
            window_end = (
                ohlcv.index[-1].isoformat()
                if hasattr(ohlcv.index[-1], "isoformat")
                else str(ohlcv.index[-1])
            )

            # Create PatternResult (using CHANNEL_UP as a proxy pattern type for SMA pullback)
            result = PatternResult(
                symbol=symbol,
                timeframe=timeframe,
                asof=datetime.now().isoformat(),
                pattern_type=PatternType.CHANNEL_UP,  # Using as proxy for SMA pullback
                strong=confidence >= 0.75 and bounce_signal,
                confidence=confidence,
                window_start=window_start,
                window_end=window_end,
                lines={
                    "current_price": current_price,
                    "sma_50": sma_50,
                    "sma_200": sma_200,
                    "distance_from_sma": distance_pct,
                    "pullback_depth": pullback_depth,
                },
                touches={"sma_50": 1},
                breakout=None,
                evidence={
                    "volume_declining": volume_declining,
                    "bounce_signal": bounce_signal,
                    "above_200sma": current_price > sma_200,
                },
            )

            results.append(result)

        except Exception as e:
            logger.exception(f"Error in 50 SMA Pullback detection: {e}")

        return results

    def _is_in_uptrend(self, ohlcv: pd.DataFrame) -> bool:
        """Check if stock is in uptrend"""
        # Price should be above both SMAs
        if ohlcv["close"].iloc[-1] < ohlcv["sma_50"].iloc[-1]:
            return False

        # 50 SMA should be above 200 SMA
        if ohlcv["sma_50"].iloc[-1] < ohlcv["sma_200"].iloc[-1]:
            return False

        # Price should have been above 50 SMA for most recent bars (uptrend)
        recent = ohlcv.iloc[-self.min_uptrend_bars :]
        bars_above = (recent["close"] > recent["sma_50"]).sum()

        if bars_above < self.min_uptrend_bars * 0.7:  # At least 70% of bars above
            return False

        return True

    def _check_volume_decline(self, ohlcv: pd.DataFrame) -> bool:
        """Check if volume is declining during pullback"""
        recent_vol = ohlcv["volume"].iloc[-5:].mean()
        prior_vol = ohlcv["volume"].iloc[-20:-5].mean()

        return recent_vol < prior_vol * 0.8  # Recent volume 20% below prior

    def _check_bounce_signals(self, ohlcv: pd.DataFrame) -> bool:
        """Check for bullish bounce signals"""
        # Check if recent bar found support
        recent_bars = ohlcv.iloc[-3:]

        # Look for hammer or bullish engulfing near SMA
        for idx in range(len(recent_bars)):
            bar = recent_bars.iloc[idx]

            # Hammer: long lower shadow, small body
            body = abs(bar["close"] - bar["open"])
            lower_shadow = min(bar["open"], bar["close"]) - bar["low"]
            total_range = bar["high"] - bar["low"]

            if total_range > 0:
                if lower_shadow > body * 2 and lower_shadow > total_range * 0.6:
                    return True

                # Bullish bounce: closed near high of bar
                close_position = (bar["close"] - bar["low"]) / total_range
                if close_position > 0.7:
                    return True

        return False

    def _calculate_confidence(
        self,
        distance_pct: float,
        pullback_depth: float,
        volume_declining: bool,
        bounce_signal: bool,
        above_200sma: bool,
    ) -> float:
        """Calculate pullback pattern confidence"""

        # Distance score (30%) - closer is better
        distance_score = 1.0 - (distance_pct / self.max_distance_pct)
        distance_score = max(0, min(1, distance_score))

        # Pullback depth score (25%) - ideal 5-10%
        if 5 <= pullback_depth <= 10:
            depth_score = 1.0
        elif 3 <= pullback_depth < 5:
            depth_score = 0.7
        elif 10 < pullback_depth <= 15:
            depth_score = 0.6
        else:
            depth_score = 0.3

        # Volume score (20%)
        volume_score = 0.8 if volume_declining else 0.3

        # Bounce signal score (15%)
        bounce_score = 0.9 if bounce_signal else 0.4

        # Trend strength score (10%)
        trend_score = 0.9 if above_200sma else 0.6

        confidence = (
            0.30 * distance_score
            + 0.25 * depth_score
            + 0.20 * volume_score
            + 0.15 * bounce_score
            + 0.10 * trend_score
        )

        return np.clip(confidence, 0, 1)
