"""
Head & Shoulders Pattern Detector
Implements both regular (topping) and inverse (bottoming) patterns
"""
from typing import List, Optional, Dict, Any, Tuple
import pandas as pd
import numpy as np
from datetime import datetime

from app.core.detector_base import (
    Detector, PatternResult, PatternType, PricePoint, LineSegment,
    GeometryHelper, StatsHelper
)
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

    def find(self, ohlcv: pd.DataFrame, timeframe: str, symbol: str) -> List[PatternResult]:
        """Detect H&S patterns in OHLCV data"""
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
            print(f"Error in Head & Shoulders detection: {e}")

        return results

    def _detect_regular_hs(
        self,
        ohlcv: pd.DataFrame,
        pivots: List[Dict],
        atr: float,
        timeframe: str,
        symbol: str
    ) -> Optional[PatternResult]:
        """
        Regular Head & Shoulders (topping pattern)
        Pattern: Peak - Valley - Higher Peak - Valley - Peak
        """
        # Filter for high pivots (peaks)
        peaks = [p for p in pivots if p['type'] == 'high']
        valleys = [p for p in pivots if p['type'] == 'low']

        if len(peaks) < 3 or len(valleys) < 2:
            return None

        # Look for three-peak pattern in recent data
        for i in range(len(peaks) - 2):
            left_shoulder = peaks[i]
            head = peaks[i + 1]
            right_shoulder = peaks[i + 2]

            # Head must be highest
            if head['price'] <= max(left_shoulder['price'], right_shoulder['price']):
                continue

            # Check head is sufficiently higher
            head_prominence = (head['price'] - max(left_shoulder['price'], right_shoulder['price'])) / atr
            if head_prominence < self.cfg.HEAD_MIN_RATIO:
                continue

            # Shoulders should be similar height (within tolerance)
            shoulder_ratio = min(left_shoulder['price'], right_shoulder['price']) / max(left_shoulder['price'], right_shoulder['price'])
            if shoulder_ratio < getattr(self.cfg, 'SHOULDER_SYMMETRY', 0.85):
                continue

            # Find valleys between peaks for neckline
            left_valley = None
            right_valley = None

            for v in valleys:
                if left_shoulder['index'] < v['index'] < head['index']:
                    if left_valley is None or v['price'] < left_valley['price']:
                        left_valley = v

                if head['index'] < v['index'] < right_shoulder['index']:
                    if right_valley is None or v['price'] < right_valley['price']:
                        right_valley = v

            if not left_valley or not right_valley:
                continue

            # Fit neckline through valleys
            neckline_points = [
                (left_valley['index'], left_valley['price']),
                (right_valley['index'], right_valley['price'])
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

            # Calculate confidence
            confidence = self._calculate_confidence(
                head_prominence,
                shoulder_ratio,
                r_squared,
                right_shoulder['index'] - left_shoulder['index']
            )

            if confidence < 0.40:
                continue

            # Build pattern window
            start_idx = left_shoulder['index']
            end_idx = right_shoulder['index']

            window_start = ohlcv.index[start_idx].isoformat() if hasattr(ohlcv.index[start_idx], 'isoformat') else str(ohlcv.index[start_idx])
            window_end = ohlcv.index[end_idx].isoformat() if hasattr(ohlcv.index[end_idx], 'isoformat') else str(ohlcv.index[end_idx])

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
                    'left_shoulder_price': left_shoulder['price'],
                    'head_price': head['price'],
                    'right_shoulder_price': right_shoulder['price'],
                    'neckline_slope': slope,
                    'neckline_intercept': intercept
                },
                touches={
                    'neckline': 2,
                    'pattern_peaks': 3
                },
                breakout=None,
                evidence={
                    'head_prominence': head_prominence,
                    'shoulder_symmetry': shoulder_ratio,
                    'neckline_r2': r_squared,
                    'pattern_length': end_idx - start_idx,
                    'atr': atr
                }
            )

        return None

    def _detect_inverse_hs(
        self,
        ohlcv: pd.DataFrame,
        pivots: List[Dict],
        atr: float,
        timeframe: str,
        symbol: str
    ) -> Optional[PatternResult]:
        """
        Inverse Head & Shoulders (bottoming pattern)
        Pattern: Trough - Peak - Lower Trough - Peak - Trough
        """
        # Filter for low pivots (troughs)
        troughs = [p for p in pivots if p['type'] == 'low']
        peaks = [p for p in pivots if p['type'] == 'high']

        if len(troughs) < 3 or len(peaks) < 2:
            return None

        # Look for three-trough pattern
        for i in range(len(troughs) - 2):
            left_shoulder = troughs[i]
            head = troughs[i + 1]
            right_shoulder = troughs[i + 2]

            # Head must be lowest
            if head['price'] >= min(left_shoulder['price'], right_shoulder['price']):
                continue

            # Check head is sufficiently lower
            head_depth = (min(left_shoulder['price'], right_shoulder['price']) - head['price']) / atr
            if head_depth < self.cfg.HEAD_MIN_RATIO:
                continue

            # Shoulders should be similar height
            shoulder_ratio = min(left_shoulder['price'], right_shoulder['price']) / max(left_shoulder['price'], right_shoulder['price'])
            if shoulder_ratio < getattr(self.cfg, 'SHOULDER_SYMMETRY', 0.85):
                continue

            # Find peaks between troughs for neckline
            left_peak = None
            right_peak = None

            for p in peaks:
                if left_shoulder['index'] < p['index'] < head['index']:
                    if left_peak is None or p['price'] > left_peak['price']:
                        left_peak = p

                if head['index'] < p['index'] < right_shoulder['index']:
                    if right_peak is None or p['price'] > right_peak['price']:
                        right_peak = p

            if not left_peak or not right_peak:
                continue

            # Fit neckline through peaks
            neckline_points = [
                (left_peak['index'], left_peak['price']),
                (right_peak['index'], right_peak['price'])
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

            # Calculate confidence
            confidence = self._calculate_confidence(
                head_depth,
                shoulder_ratio,
                r_squared,
                right_shoulder['index'] - left_shoulder['index']
            )

            if confidence < 0.40:
                continue

            # Build pattern window
            start_idx = left_shoulder['index']
            end_idx = right_shoulder['index']

            window_start = ohlcv.index[start_idx].isoformat() if hasattr(ohlcv.index[start_idx], 'isoformat') else str(ohlcv.index[start_idx])
            window_end = ohlcv.index[end_idx].isoformat() if hasattr(ohlcv.index[end_idx], 'isoformat') else str(ohlcv.index[end_idx])

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
                    'left_shoulder_price': left_shoulder['price'],
                    'head_price': head['price'],
                    'right_shoulder_price': right_shoulder['price'],
                    'neckline_slope': slope,
                    'neckline_intercept': intercept
                },
                touches={
                    'neckline': 2,
                    'pattern_troughs': 3
                },
                breakout=None,
                evidence={
                    'head_depth': head_depth,
                    'shoulder_symmetry': shoulder_ratio,
                    'neckline_r2': r_squared,
                    'pattern_length': end_idx - start_idx,
                    'atr': atr
                }
            )

        return None

    def _calculate_confidence(
        self,
        head_prominence: float,
        shoulder_symmetry: float,
        neckline_r2: float,
        pattern_length: int
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
            0.30 * prominence_score +
            0.30 * symmetry_score +
            0.30 * neckline_score +
            0.10 * length_score
        )

        return np.clip(confidence, 0, 1)
