"""
Automatic Fibonacci Retracement and Extension Levels
"""

import logging
from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from scipy.signal import argrelextrema

logger = logging.getLogger(__name__)


# Standard Fibonacci ratios
FIBONACCI_RETRACEMENT_LEVELS = [0.236, 0.382, 0.500, 0.618, 0.786]
FIBONACCI_EXTENSION_LEVELS = [1.272, 1.414, 1.618, 2.000, 2.618]


@dataclass
class FibonacciLevels:
    """Fibonacci levels for a swing"""

    swing_high: float
    swing_low: float
    swing_high_idx: int
    swing_low_idx: int
    direction: str  # 'uptrend' or 'downtrend'
    retracement_levels: Dict[float, float]  # ratio -> price
    extension_levels: Dict[float, float]  # ratio -> price
    current_price: float

    def to_dict(self) -> Dict:
        return {
            "swing_high": float(self.swing_high),
            "swing_low": float(self.swing_low),
            "swing_high_idx": int(self.swing_high_idx),
            "swing_low_idx": int(self.swing_low_idx),
            "direction": self.direction,
            "retracement_levels": {
                str(k): float(v) for k, v in self.retracement_levels.items()
            },
            "extension_levels": {
                str(k): float(v) for k, v in self.extension_levels.items()
            },
            "current_price": float(self.current_price),
            "nearest_support": self._find_nearest_support(),
            "nearest_resistance": self._find_nearest_resistance(),
        }

    def _find_nearest_support(self) -> Optional[Dict]:
        """Find nearest Fibonacci support level below current price"""
        if self.direction == "uptrend":
            # In uptrend, retracements are support
            for ratio, level in sorted(self.retracement_levels.items(), reverse=True):
                if level < self.current_price:
                    return {"ratio": ratio, "price": float(level)}
        return None

    def _find_nearest_resistance(self) -> Optional[Dict]:
        """Find nearest Fibonacci resistance level above current price"""
        if self.direction == "uptrend":
            # In uptrend, extensions are resistance
            for ratio, level in sorted(self.extension_levels.items()):
                if level > self.current_price:
                    return {"ratio": ratio, "price": float(level)}
        else:
            # In downtrend, retracements are resistance
            for ratio, level in sorted(self.retracement_levels.items()):
                if level > self.current_price:
                    return {"ratio": ratio, "price": float(level)}
        return None


class FibonacciCalculator:
    """
    Automatically calculate Fibonacci retracement and extension levels
    """

    def __init__(self):
        self.retracement_ratios = FIBONACCI_RETRACEMENT_LEVELS
        self.extension_ratios = FIBONACCI_EXTENSION_LEVELS

    def calculate_auto_fibonacci(
        self, df: pd.DataFrame, lookback: int = 100
    ) -> List[FibonacciLevels]:
        """
        Automatically identify significant swings and calculate Fibonacci levels

        Args:
            df: DataFrame with OHLCV data
            lookback: How far back to look for swings

        Returns:
            List of FibonacciLevels for detected swings
        """
        data = df.tail(lookback) if len(df) > lookback else df

        if len(data) < 20:
            logger.warning("Insufficient data for Fibonacci calculation")
            return []

        fib_levels = []

        # Detect significant swings (uptrends and downtrends)
        swings = self._detect_significant_swings(data)

        for swing in swings:
            fib = self._calculate_fibonacci_for_swing(
                swing["high"],
                swing["low"],
                swing["high_idx"],
                swing["low_idx"],
                swing["direction"],
                df["close"].iloc[-1],
            )
            fib_levels.append(fib)

        logger.info(f"Calculated Fibonacci levels for {len(fib_levels)} swings")

        return fib_levels

    def calculate_manual_fibonacci(
        self,
        high: float,
        low: float,
        direction: str = "uptrend",
        current_price: Optional[float] = None,
    ) -> FibonacciLevels:
        """
        Calculate Fibonacci levels for manually specified swing points

        Args:
            high: Swing high price
            low: Swing low price
            direction: 'uptrend' or 'downtrend'
            current_price: Current price (for finding nearest levels)

        Returns:
            FibonacciLevels object
        """
        current_price = current_price or high

        return self._calculate_fibonacci_for_swing(
            high, low, 0, 0, direction, current_price
        )

    def _detect_significant_swings(self, df: pd.DataFrame) -> List[Dict]:
        """
        Detect significant price swings for Fibonacci analysis

        A swing is a major high followed by a major low (or vice versa)
        """
        highs = df["high"].values
        lows = df["low"].values

        # Find prominent peaks and troughs
        peaks_idx = argrelextrema(highs, np.greater_equal, order=10)[0]
        troughs_idx = argrelextrema(lows, np.less_equal, order=10)[0]

        if len(peaks_idx) == 0 or len(troughs_idx) == 0:
            return []

        swings = []

        # Find most recent significant swings
        # 1. Most recent uptrend (low to high)
        if len(troughs_idx) > 0 and len(peaks_idx) > 0:
            # Find last significant low
            last_trough_idx = troughs_idx[-1]
            last_trough = lows[last_trough_idx]

            # Find highest peak after that low
            peaks_after_trough = [p for p in peaks_idx if p > last_trough_idx]

            if peaks_after_trough:
                last_peak_idx = peaks_after_trough[-1]
                last_peak = highs[last_peak_idx]

                # Significant swing should be > 5% move
                if (last_peak - last_trough) / last_trough > 0.05:
                    swings.append(
                        {
                            "high": last_peak,
                            "low": last_trough,
                            "high_idx": last_peak_idx,
                            "low_idx": last_trough_idx,
                            "direction": "uptrend",
                        }
                    )

        # 2. Most recent downtrend (high to low)
        if len(peaks_idx) > 0 and len(troughs_idx) > 0:
            last_peak_idx = peaks_idx[-1]
            last_peak = highs[last_peak_idx]

            troughs_after_peak = [t for t in troughs_idx if t > last_peak_idx]

            if troughs_after_peak:
                last_trough_idx = troughs_after_peak[-1]
                last_trough = lows[last_trough_idx]

                if (last_peak - last_trough) / last_peak > 0.05:
                    swings.append(
                        {
                            "high": last_peak,
                            "low": last_trough,
                            "high_idx": last_peak_idx,
                            "low_idx": last_trough_idx,
                            "direction": "downtrend",
                        }
                    )

        # 3. Look for larger historical swings
        if len(peaks_idx) >= 2 and len(troughs_idx) >= 2:
            # Previous major uptrend
            if len(troughs_idx) >= 2:
                prev_trough_idx = (
                    troughs_idx[-2] if len(troughs_idx) >= 2 else troughs_idx[0]
                )
                prev_trough = lows[prev_trough_idx]

                peaks_between = [
                    p
                    for p in peaks_idx
                    if p > prev_trough_idx
                    and p < (troughs_idx[-1] if len(troughs_idx) > 1 else len(df))
                ]

                if peaks_between:
                    prev_peak_idx = max(peaks_between, key=lambda p: highs[p])
                    prev_peak = highs[prev_peak_idx]

                    if (prev_peak - prev_trough) / prev_trough > 0.10:  # >10% swing
                        swings.append(
                            {
                                "high": prev_peak,
                                "low": prev_trough,
                                "high_idx": prev_peak_idx,
                                "low_idx": prev_trough_idx,
                                "direction": "uptrend",
                            }
                        )

        return swings

    def _calculate_fibonacci_for_swing(
        self,
        high: float,
        low: float,
        high_idx: int,
        low_idx: int,
        direction: str,
        current_price: float,
    ) -> FibonacciLevels:
        """
        Calculate Fibonacci retracement and extension levels for a swing

        For uptrend (low to high):
        - Retracements are measured from high back down toward low
        - Extensions are measured beyond the high

        For downtrend (high to low):
        - Retracements are measured from low back up toward high
        - Extensions are measured beyond the low
        """
        swing_range = high - low

        retracement_levels = {}
        extension_levels = {}

        if direction == "uptrend":
            # Retracements: high - (ratio * range)
            for ratio in self.retracement_ratios:
                level = high - (ratio * swing_range)
                retracement_levels[ratio] = level

            # Extensions: high + (ratio * range)
            for ratio in self.extension_ratios:
                # Extension ratios are from the swing low
                # e.g., 1.618 extension = low + 1.618 * range
                level = low + (ratio * swing_range)
                extension_levels[ratio] = level

        else:  # downtrend
            # Retracements: low + (ratio * range)
            for ratio in self.retracement_ratios:
                level = low + (ratio * swing_range)
                retracement_levels[ratio] = level

            # Extensions: low - (ratio * range)
            for ratio in self.extension_ratios:
                level = high - (ratio * swing_range)
                extension_levels[ratio] = level

        return FibonacciLevels(
            swing_high=high,
            swing_low=low,
            swing_high_idx=high_idx,
            swing_low_idx=low_idx,
            direction=direction,
            retracement_levels=retracement_levels,
            extension_levels=extension_levels,
            current_price=current_price,
        )


def calculate_fibonacci_time_zones(df: pd.DataFrame, start_idx: int) -> List[int]:
    """
    Calculate Fibonacci time zones (vertical lines at Fibonacci intervals)

    Args:
        df: DataFrame with OHLCV data
        start_idx: Starting index for time zones

    Returns:
        List of indices where Fibonacci time lines should be drawn
    """
    # Fibonacci sequence: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144...
    fib_sequence = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]

    time_zones = []

    for fib in fib_sequence:
        zone_idx = start_idx + fib
        if zone_idx < len(df):
            time_zones.append(zone_idx)
        else:
            break

    return time_zones


def calculate_fibonacci_arcs(
    df: pd.DataFrame, high: float, low: float, high_idx: int, low_idx: int
) -> List[Dict]:
    """
    Calculate Fibonacci arcs (curved support/resistance lines)

    Returns:
        List of arc parameters
    """
    # Fibonacci arcs are complex geometric curves
    # This is a simplified implementation
    swing_range = high - low
    abs(high_idx - low_idx)

    arcs = []

    for ratio in FIBONACCI_RETRACEMENT_LEVELS:
        arc = {
            "ratio": ratio,
            "radius": ratio * swing_range,
            "center_x": (high_idx + low_idx) / 2,
            "center_y": (high + low) / 2,
        }
        arcs.append(arc)

    return arcs


def calculate_fibonacci_fans(
    high: float, low: float, high_idx: int, low_idx: int
) -> List[Dict]:
    """
    Calculate Fibonacci fan lines

    Fan lines are diagonal lines drawn from swing low/high at Fib ratios

    Returns:
        List of fan line parameters (slope, intercept)
    """
    fans = []

    # Calculate base angle (from swing low to swing high)
    base_slope = (high - low) / (high_idx - low_idx) if high_idx != low_idx else 0

    for ratio in FIBONACCI_RETRACEMENT_LEVELS:
        # Fan line at Fibonacci ratio of the base angle
        fan_slope = base_slope * ratio

        # Fan line starts at swing low
        intercept = low - (fan_slope * low_idx)

        fans.append(
            {
                "ratio": ratio,
                "slope": fan_slope,
                "intercept": intercept,
                "start_idx": low_idx,
                "start_price": low,
            }
        )

    return fans
