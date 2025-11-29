"""
Cup & Handle (CAN SLIM-style) Detector
Detects rounded bottoms with subsequent shallow pullbacks.

Key features:
- Cup depth 12-50% (typically)
- Rounded bottom (smooth curvature, not V-shaped)
- Handle pullback ≤8-15% with volume dry-up
- Breakout above cup rim with volume surge
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import logging

from app.core.detector_base import (
    Detector, PatternResult, PatternType, PricePoint, LineSegment, StatsHelper, GeometryHelper
)
from app.core.detector_config import CupHandleConfig, BreakoutConfig

logger = logging.getLogger(__name__)


class CupHandleDetector(Detector):
    """
    Cup & Handle (CAN SLIM) pattern detector.

    Identifies:
    - Rounded cup: deep U-shape with smooth bottom
    - Handle: shallow pullback in upper half of cup
    - Breakout: close above cup rim on volume surge
    """

    def __init__(self, **kwargs):
        super().__init__("Cup & Handle", **kwargs)
        self.config = CupHandleConfig()
        # Apply overrides
        for key, value in kwargs.items():
            if hasattr(self.config, key.upper()):
                setattr(self.config, key.upper(), value)

    def find(self, ohlcv: pd.DataFrame, timeframe: str, symbol: str) -> List[PatternResult]:
        """Detect Cup & Handle patterns"""
        results = []

        if len(ohlcv) < 100:
            return results

        try:
            high = ohlcv['high'].values
            low = ohlcv['low'].values
            close = ohlcv['close'].values
            volume = ohlcv['volume'].values
            dates = ohlcv.get('datetime', pd.date_range(end=datetime.now(), periods=len(ohlcv)))

            # Calculate metrics
            atr = StatsHelper.atr(high, low, close, period=14)
            vol_z = StatsHelper.volume_z_score(volume, window=20)

            # Find potential cups (low points)
            lows_idx = self._find_cup_candidates(high, low, close, atr)

            # For each potential cup, check if it's valid and has a handle
            for cup_idx in lows_idx:
                cup_handle = self._analyze_cup_handle(
                    cup_idx, high, low, close, volume, dates, atr, vol_z
                )
                if cup_handle:
                    results.append(cup_handle)

        except Exception as e:
            logger.exception(f"Error in Cup & Handle detection: {e}")

        return results

    def _find_cup_candidates(
        self, high: np.ndarray, low: np.ndarray, close: np.ndarray, atr: np.ndarray
    ) -> List[int]:
        """Find potential cup bottom points (local minima)"""
        candidates = []

        for i in range(
            self.config.CUP_MIN_LENGTH,
            len(low) - self.config.CUP_MIN_LENGTH,
            5
        ):
            # Check if this could be a cup bottom
            left_high = np.max(high[max(0, i - self.config.CUP_MAX_LENGTH):i])
            cup_low = low[i]
            right_high = np.max(high[i:min(len(high), i + self.config.CUP_MIN_LENGTH)])

            # Cup depth
            left_depth = (left_high - cup_low) / left_high
            right_depth = (right_high - cup_low) / right_high

            # Check if depths are reasonable
            if (self.config.CUP_DEPTH_MIN <= left_depth <= 0.60 and
                self.config.CUP_DEPTH_MIN <= right_depth <= 0.60):
                candidates.append(i)

        return candidates

    def _analyze_cup_handle(
        self, cup_idx: int, high: np.ndarray, low: np.ndarray, close: np.ndarray,
        volume: np.ndarray, dates, atr: np.ndarray, vol_z: np.ndarray
    ) -> Optional[PatternResult]:
        """Analyze if a cup candidate is valid and has a handle"""

        # Define cup region
        cup_start = max(0, cup_idx - self.config.CUP_MAX_LENGTH)
        cup_end = cup_idx

        # Get left peak (before cup)
        left_peak_idx = np.argmax(high[cup_start:cup_end])
        left_peak = high[cup_start + left_peak_idx]

        cup_low = low[cup_idx]
        cup_depth = (left_peak - cup_low) / left_peak

        # Check cup depth
        if not (self.config.CUP_DEPTH_MIN <= cup_depth <= 0.60):
            return None

        # Check cup length
        cup_length = cup_idx - (cup_start + left_peak_idx)
        if not (self.config.CUP_MIN_LENGTH <= cup_length <= self.config.CUP_MAX_LENGTH):
            return None

        # Check roundedness (curvature score)
        cup_prices = close[cup_start + left_peak_idx:cup_end + 1]
        roundedness_score = StatsHelper.curvature_score(cup_prices)

        if roundedness_score < self.config.ROUNDEDNESS_MIN_SCORE:
            return None

        # Look for right side recovery
        right_start = cup_end + 1
        right_end = min(len(high), cup_end + 30)

        if right_end <= right_start:
            return None

        right_peak_idx = np.argmax(high[right_start:right_end])
        right_peak = high[right_start + right_peak_idx]

        # Right side should approach left peak
        peak_diff = abs(right_peak - left_peak)
        avg_atr = np.mean(atr[cup_end:right_end])

        if peak_diff > self.config.RIGHT_SIDE_ATR * avg_atr:
            return None

        # Look for handle (pullback from right peak)
        handle_start = right_start + right_peak_idx
        handle_end = min(len(close), handle_start + self.config.HANDLE_MAX_LENGTH)

        if handle_end <= handle_start:
            return None

        handle_prices = close[handle_start:handle_end]
        if len(handle_prices) < self.config.HANDLE_MIN_LENGTH:
            return None

        # Handle should be shallow pullback
        handle_low = np.min(low[handle_start:handle_end])
        handle_depth = (right_peak - handle_low) / right_peak

        if handle_depth < self.config.HANDLE_MIN_PULLBACK:
            return None  # Too little pullback
        if handle_depth > self.config.HANDLE_PULLBACK_RATIO * cup_depth:
            return None  # Too much pullback

        # Handle low should stay above cup midpoint
        cup_midpoint = (left_peak + cup_low) / 2
        if self.config.HANDLE_MIDPOINT_CHECK and handle_low < cup_midpoint:
            return None

        # Check volume on handle (should dry up)
        handle_vol_mean = np.mean(volume[handle_start:handle_end])
        preceding_vol_mean = np.mean(volume[max(0, handle_start - 20):handle_start])

        volume_dryup_ratio = handle_vol_mean / (preceding_vol_mean + 1)

        # Look for breakout (close above left peak + handle)
        breakout_start = handle_end
        breakout_end = min(len(close), handle_end + 10)

        breakout_vol_z = np.max(vol_z[breakout_start:breakout_end]) if breakout_end > breakout_start else 0

        # Compute confidence
        confidence = self._score_cup_handle(
            cup_depth, roundedness_score, handle_depth,
            volume_dryup_ratio, breakout_vol_z, cup_length
        )

        if confidence < 0.40:
            return None

        # Build result
        result = PatternResult(
            symbol=symbol,
            timeframe='1D',
            asof=datetime.now().isoformat(),
            pattern_type=PatternType.CUP_HANDLE,
            strong=confidence >= 0.75,
            confidence=confidence,
            window_start=str(dates[cup_start])[:10] if len(dates) > cup_start else '2025-01-01',
            window_end=str(dates[breakout_end - 1])[:10] if len(dates) > breakout_end - 1 else '2025-01-01',
            lines={
                'cup_start': float(left_peak),
                'cup_bottom': float(cup_low),
                'right_peak': float(right_peak),
                'handle_low': float(handle_low),
                'breakout_level': float(left_peak),
            },
            touches={
                'cup_bars': int(cup_length),
                'handle_bars': int(handle_end - handle_start),
            },
            breakout={
                'direction': 'up',
                'price': float(left_peak),
                'volume_z': float(breakout_vol_z),
                'bar_index': int(breakout_start),
            },
            evidence={
                'cup_depth_pct': float(cup_depth * 100),
                'roundedness_score': float(roundedness_score),
                'handle_depth_pct': float(handle_depth * 100),
                'volume_dryup_ratio': float(volume_dryup_ratio),
                'handle_midpoint_check': float(handle_low - cup_midpoint),
            }
        )
        return result

    def _score_cup_handle(
        self, cup_depth: float, roundedness: float, handle_depth: float,
        volume_dryup: float, breakout_vol_z: float, cup_length: int
    ) -> float:
        """Compute Cup & Handle confidence score"""
        score = 0.0

        # Depth weight: 25%
        # Ideal depth is 15-35%; penalize edges
        ideal_range = (0.15, 0.35)
        if ideal_range[0] <= cup_depth <= ideal_range[1]:
            depth_score = 1.0
        elif self.config.CUP_DEPTH_MIN <= cup_depth < ideal_range[0]:
            depth_score = (cup_depth - self.config.CUP_DEPTH_MIN) / (ideal_range[0] - self.config.CUP_DEPTH_MIN)
        else:
            depth_score = max(0, 1.0 - (cup_depth - ideal_range[1]) / (0.60 - ideal_range[1]))
        score += 0.25 * depth_score

        # Roundedness weight: 25%
        score += 0.25 * min(1.0, roundedness)

        # Handle weight: 20%
        # Ideal handle depth is 5-10%
        handle_ideal_range = (0.05, 0.10)
        if handle_ideal_range[0] <= handle_depth <= handle_ideal_range[1]:
            handle_score = 1.0
        elif handle_depth < handle_ideal_range[0]:
            handle_score = handle_depth / handle_ideal_range[0]
        else:
            handle_score = max(0, 1.0 - (handle_depth - handle_ideal_range[1]) / (0.10))
        score += 0.20 * handle_score

        # Volume weight: 20%
        volume_score = 0.0
        if volume_dryup <= 0.8:  # Volume dried up
            volume_score += 0.5
        if breakout_vol_z >= self.config.BREAKOUT_VOLUME_Z:
            volume_score += 0.5
        score += 0.20 * volume_score

        # Recency & length: 10%
        # Longer cups (30-100 bars) are slightly better
        length_score = min(1.0, (cup_length - 20) / 80.0)
        score += 0.10 * length_score

        return np.clip(score, 0.0, 1.0)
