"""
Wedge Pattern Detector
Implements Rising and Falling Wedge detection
"""
from typing import List, Optional, Dict, Any
import pandas as pd
import numpy as np
from datetime import datetime

from app.core.detector_base import (
    Detector, PatternResult, PatternType, PricePoint, LineSegment,
    GeometryHelper, StatsHelper
)
from app.core.detector_config import WedgeConfig


class WedgeDetector(Detector):
    """
    Detects wedge patterns - converging trendlines moving in same direction

    Patterns:
    - Rising Wedge: Both lines rising, resistance steeper (bearish reversal)
    - Falling Wedge: Both lines falling, support steeper (bullish reversal)
    """

    def __init__(self, **kwargs):
        super().__init__("Wedge Detector", **kwargs)
        self.cfg = WedgeConfig()

        for key, value in kwargs.items():
            if hasattr(self.cfg, key.upper()):
                setattr(self.cfg, key.upper(), value)

    def find(self, ohlcv: pd.DataFrame, timeframe: str, symbol: str) -> List[PatternResult]:
        """Detect wedge patterns in OHLCV data"""
        if len(ohlcv) < self.cfg.MIN_LENGTH:
            return []

        results = []

        try:
            # Calculate ATR
            high = ohlcv['high'].values
            low = ohlcv['low'].values
            close = ohlcv['close'].values
            atr = StatsHelper.atr(high, low, close)

            # Get pivots
            pivots_tuples = StatsHelper.zigzag_pivots(high, low, close, atr)
            pivots = [{'index': p[0], 'price': p[1], 'type': p[2]} for p in pivots_tuples]

            if len(pivots) < 4:
                return []

            # Try different lookback windows
            for lookback in [40, 60, 80]:
                if len(ohlcv) < lookback:
                    continue

                window = ohlcv.iloc[-lookback:]
                window_pivots = [p for p in pivots if p['index'] >= len(ohlcv) - lookback]

                if len(window_pivots) < 4:
                    continue

                highs = [p for p in window_pivots if p['type'] == 'high']
                lows = [p for p in window_pivots if p['type'] == 'low']

                if len(highs) < 2 or len(lows) < 2:
                    continue

                # Try rising wedge
                rising = self._detect_rising_wedge(window, highs, lows, atr[-1], timeframe, symbol)
                if rising:
                    results.append(rising)

                # Try falling wedge
                falling = self._detect_falling_wedge(window, highs, lows, atr[-1], timeframe, symbol)
                if falling:
                    results.append(falling)

        except Exception as e:
            print(f"Error in Wedge detection: {e}")

        return results

    def _detect_rising_wedge(
        self,
        window: pd.DataFrame,
        highs: List[Dict],
        lows: List[Dict],
        atr: float,
        timeframe: str,
        symbol: str
    ) -> Optional[PatternResult]:
        """
        Rising Wedge: Both lines rising, resistance steeper
        Typically bearish reversal pattern
        """
        if len(highs) < 2 or len(lows) < 2:
            return None

        # Fit resistance line (through highs)
        high_points = [(h['index'], h['price']) for h in highs]
        high_line = GeometryHelper.fit_line_ransac(high_points)

        if not high_line:
            return None

        # Fit support line (through lows)
        low_points = [(l['index'], l['price']) for l in lows]
        low_line = GeometryHelper.fit_line_ransac(low_points)

        if not low_line:
            return None

        high_slope, high_intercept = high_line[0], high_line[1]
        low_slope, low_intercept = low_line[0], low_line[1]

        # Both slopes must be positive (rising)
        if high_slope <= 0 or low_slope <= 0:
            return None

        # Resistance must be steeper than support
        if high_slope <= low_slope:
            return None

        # Check convergence
        first_idx = min(highs[0]['index'], lows[0]['index'])
        last_idx = max(highs[-1]['index'], lows[-1]['index'])

        resistance_start = high_slope * first_idx + high_intercept
        resistance_end = high_slope * last_idx + high_intercept
        support_start = low_slope * first_idx + low_intercept
        support_end = low_slope * last_idx + low_intercept

        start_gap = resistance_start - support_start
        end_gap = resistance_end - support_end

        if start_gap <= 0 or end_gap <= 0 or end_gap >= start_gap:
            return None

        convergence = 1 - (end_gap / start_gap)

        if convergence < self.cfg.CONVERGENCE_THRESHOLD:
            return None

        # Count touches
        resistance_touches = sum(
            1 for h in highs
            if abs(h['price'] - (high_slope * h['index'] + high_intercept)) < atr * 0.5
        )

        support_touches = sum(
            1 for l in lows
            if abs(l['price'] - (low_slope * l['index'] + low_intercept)) < atr * 0.5
        )

        min_touches = self.cfg.MIN_TOUCHES_PER_SIDE
        if resistance_touches < min_touches or support_touches < min_touches:
            return None

        # Check volume contraction
        volumes = window['volume'].values
        volume_trend = StatsHelper.kendall_tau(volumes)
        volume_declining = volume_trend < -0.2

        # Calculate confidence
        confidence = self._calculate_confidence(
            resistance_touches,
            support_touches,
            convergence,
            len(window),
            volume_declining
        )

        if confidence < 0.40:
            return None

        window_start = window.index[0].isoformat() if hasattr(window.index[0], 'isoformat') else str(window.index[0])
        window_end = window.index[-1].isoformat() if hasattr(window.index[-1], 'isoformat') else str(window.index[-1])

        return PatternResult(
            symbol=symbol,
            timeframe=timeframe,
            asof=datetime.now().isoformat(),
            pattern_type=PatternType.WEDGE_RISING,
            strong=confidence >= 0.75 and volume_declining,
            confidence=confidence,
            window_start=window_start,
            window_end=window_end,
            lines={
                'resistance_slope': high_slope,
                'resistance_intercept': high_intercept,
                'support_slope': low_slope,
                'support_intercept': low_intercept
            },
            touches={
                'resistance': resistance_touches,
                'support': support_touches
            },
            breakout=None,
            evidence={
                'convergence': convergence,
                'volume_declining': volume_declining,
                'slope_ratio': high_slope / low_slope if low_slope != 0 else 0,
                'pattern_length': len(window),
                'direction': 'rising'
            }
        )

    def _detect_falling_wedge(
        self,
        window: pd.DataFrame,
        highs: List[Dict],
        lows: List[Dict],
        atr: float,
        timeframe: str,
        symbol: str
    ) -> Optional[PatternResult]:
        """
        Falling Wedge: Both lines falling, support steeper
        Typically bullish reversal pattern
        """
        if len(highs) < 2 or len(lows) < 2:
            return None

        # Fit lines
        high_points = [(h['index'], h['price']) for h in highs]
        high_line = GeometryHelper.fit_line_ransac(high_points)

        if not high_line:
            return None

        low_points = [(l['index'], l['price']) for l in lows]
        low_line = GeometryHelper.fit_line_ransac(low_points)

        if not low_line:
            return None

        high_slope, high_intercept = high_line[0], high_line[1]
        low_slope, low_intercept = low_line[0], low_line[1]

        # Both slopes must be negative (falling)
        if high_slope >= 0 or low_slope >= 0:
            return None

        # Support must be steeper (more negative) than resistance
        if abs(low_slope) <= abs(high_slope):
            return None

        # Check convergence
        first_idx = min(highs[0]['index'], lows[0]['index'])
        last_idx = max(highs[-1]['index'], lows[-1]['index'])

        resistance_start = high_slope * first_idx + high_intercept
        resistance_end = high_slope * last_idx + high_intercept
        support_start = low_slope * first_idx + low_intercept
        support_end = low_slope * last_idx + low_intercept

        start_gap = resistance_start - support_start
        end_gap = resistance_end - support_end

        if start_gap <= 0 or end_gap <= 0 or end_gap >= start_gap:
            return None

        convergence = 1 - (end_gap / start_gap)

        if convergence < self.cfg.CONVERGENCE_THRESHOLD:
            return None

        # Count touches
        resistance_touches = sum(
            1 for h in highs
            if abs(h['price'] - (high_slope * h['index'] + high_intercept)) < atr * 0.5
        )

        support_touches = sum(
            1 for l in lows
            if abs(l['price'] - (low_slope * l['index'] + low_intercept)) < atr * 0.5
        )

        min_touches = self.cfg.MIN_TOUCHES_PER_SIDE
        if resistance_touches < min_touches or support_touches < min_touches:
            return None

        # Check volume contraction
        volumes = window['volume'].values
        volume_trend = StatsHelper.kendall_tau(volumes)
        volume_declining = volume_trend < -0.2

        # Calculate confidence
        confidence = self._calculate_confidence(
            resistance_touches,
            support_touches,
            convergence,
            len(window),
            volume_declining
        )

        if confidence < 0.40:
            return None

        window_start = window.index[0].isoformat() if hasattr(window.index[0], 'isoformat') else str(window.index[0])
        window_end = window.index[-1].isoformat() if hasattr(window.index[-1], 'isoformat') else str(window.index[-1])

        return PatternResult(
            symbol=symbol,
            timeframe=timeframe,
            asof=datetime.now().isoformat(),
            pattern_type=PatternType.WEDGE_FALLING,
            strong=confidence >= 0.75 and volume_declining,
            confidence=confidence,
            window_start=window_start,
            window_end=window_end,
            lines={
                'resistance_slope': high_slope,
                'resistance_intercept': high_intercept,
                'support_slope': low_slope,
                'support_intercept': low_intercept
            },
            touches={
                'resistance': resistance_touches,
                'support': support_touches
            },
            breakout=None,
            evidence={
                'convergence': convergence,
                'volume_declining': volume_declining,
                'slope_ratio': abs(low_slope) / abs(high_slope) if high_slope != 0 else 0,
                'pattern_length': len(window),
                'direction': 'falling'
            }
        )

    def _calculate_confidence(
        self,
        resistance_touches: int,
        support_touches: int,
        convergence: float,
        pattern_length: int,
        volume_declining: bool
    ) -> float:
        """Calculate wedge pattern confidence"""

        # Touch score (25%)
        total_touches = resistance_touches + support_touches
        touch_score = min(1.0, total_touches / 8.0)

        # Convergence score (35%)
        convergence_score = min(1.0, convergence / self.cfg.CONVERGENCE_THRESHOLD)

        # Structure score (20%)
        ideal_length = 50
        length_score = min(1.0, pattern_length / ideal_length)

        # Volume score (20%)
        volume_score = 0.8 if volume_declining else 0.3

        confidence = (
            0.25 * touch_score +
            0.35 * convergence_score +
            0.20 * length_score +
            0.20 * volume_score
        )

        return np.clip(confidence, 0, 1)
