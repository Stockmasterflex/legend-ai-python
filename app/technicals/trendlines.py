"""
Automated Trendline Detection
Replicates TrendSpider's patented automated trendline drawing
"""
import numpy as np
import pandas as pd
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from scipy import stats
from scipy.signal import argrelextrema
import logging

logger = logging.getLogger(__name__)


@dataclass
class Trendline:
    """Represents a detected trendline"""
    slope: float
    intercept: float
    start_idx: int
    end_idx: int
    start_price: float
    end_price: float
    strength: float  # 0-100, based on touches and R²
    type: str  # 'support', 'resistance', 'channel_upper', 'channel_lower'
    touches: int  # Number of price touches
    r_squared: float  # Statistical fit quality
    breaks: int = 0  # Number of times broken

    def get_price_at_index(self, idx: int) -> float:
        """Calculate trendline price at given index"""
        return self.slope * idx + self.intercept

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "slope": float(self.slope),
            "intercept": float(self.intercept),
            "start_idx": int(self.start_idx),
            "end_idx": int(self.end_idx),
            "start_price": float(self.start_price),
            "end_price": float(self.end_price),
            "strength": round(self.strength, 2),
            "type": self.type,
            "touches": int(self.touches),
            "r_squared": round(self.r_squared, 4),
            "breaks": int(self.breaks)
        }


@dataclass
class Channel:
    """Represents a price channel"""
    upper_trendline: Trendline
    lower_trendline: Trendline
    width: float  # Average channel width
    type: str  # 'ascending', 'descending', 'horizontal'
    strength: float

    def to_dict(self) -> Dict:
        return {
            "upper": self.upper_trendline.to_dict(),
            "lower": self.lower_trendline.to_dict(),
            "width": float(self.width),
            "type": self.type,
            "strength": round(self.strength, 2)
        }


class AutoTrendlineDetector:
    """
    Automatically detect trendlines and channels
    Uses machine learning-inspired algorithms to find optimal trendlines
    """

    def __init__(
        self,
        min_touches: int = 3,
        min_r_squared: float = 0.7,
        tolerance: float = 0.02  # 2% price tolerance for "touch"
    ):
        self.min_touches = min_touches
        self.min_r_squared = min_r_squared
        self.tolerance = tolerance

    def detect_all_trendlines(
        self,
        df: pd.DataFrame,
        lookback_period: Optional[int] = None
    ) -> Dict[str, List[Trendline]]:
        """
        Detect all trendlines (support and resistance)

        Args:
            df: DataFrame with OHLCV data
            lookback_period: How far back to look (default: all data)

        Returns:
            Dict with 'support' and 'resistance' trendlines
        """
        if lookback_period:
            data = df.tail(lookback_period).copy()
        else:
            data = df.copy()

        if len(data) < 10:
            logger.warning("Insufficient data for trendline detection")
            return {"support": [], "resistance": []}

        support_lines = self._detect_support_trendlines(data)
        resistance_lines = self._detect_resistance_trendlines(data)

        logger.info(f"Detected {len(support_lines)} support and {len(resistance_lines)} resistance lines")

        return {
            "support": support_lines,
            "resistance": resistance_lines
        }

    def detect_channels(
        self,
        df: pd.DataFrame,
        lookback_period: Optional[int] = None
    ) -> List[Channel]:
        """
        Detect price channels (parallel support/resistance)

        Args:
            df: DataFrame with OHLCV data
            lookback_period: How far back to look

        Returns:
            List of detected channels
        """
        trendlines = self.detect_all_trendlines(df, lookback_period)
        support_lines = trendlines['support']
        resistance_lines = trendlines['resistance']

        channels = []

        # Find parallel trendlines
        for support in support_lines:
            for resistance in resistance_lines:
                # Check if slopes are similar (parallel)
                slope_diff = abs(support.slope - resistance.slope)
                avg_slope = (abs(support.slope) + abs(resistance.slope)) / 2

                if avg_slope > 0:
                    slope_similarity = 1 - (slope_diff / avg_slope)
                else:
                    slope_similarity = 1 if slope_diff < 0.0001 else 0

                # Must be very parallel (>90% similar slopes)
                if slope_similarity > 0.90:
                    # Check if they form a valid channel (resistance above support)
                    # Calculate average vertical distance
                    overlapping_indices = range(
                        max(support.start_idx, resistance.start_idx),
                        min(support.end_idx, resistance.end_idx) + 1
                    )

                    if len(overlapping_indices) < 10:
                        continue

                    distances = []
                    for idx in overlapping_indices:
                        support_price = support.get_price_at_index(idx)
                        resistance_price = resistance.get_price_at_index(idx)
                        if resistance_price > support_price:
                            distances.append(resistance_price - support_price)

                    if distances:
                        avg_width = np.mean(distances)
                        width_std = np.std(distances)

                        # Channel should have consistent width
                        if width_std / avg_width < 0.15:  # Less than 15% variation
                            # Determine channel type
                            if support.slope > 0.001:
                                channel_type = 'ascending'
                            elif support.slope < -0.001:
                                channel_type = 'descending'
                            else:
                                channel_type = 'horizontal'

                            # Channel strength = average of trendline strengths
                            channel_strength = (support.strength + resistance.strength) / 2

                            channel = Channel(
                                upper_trendline=resistance,
                                lower_trendline=support,
                                width=avg_width,
                                type=channel_type,
                                strength=channel_strength
                            )
                            channels.append(channel)

        # Sort by strength
        channels.sort(key=lambda x: x.strength, reverse=True)

        logger.info(f"Detected {len(channels)} price channels")

        return channels

    def _detect_support_trendlines(self, df: pd.DataFrame) -> List[Trendline]:
        """Detect support trendlines (drawn under price)"""
        trendlines = []

        lows = df['low'].values
        closes = df['close'].values

        # Find local minima (potential support pivot points)
        minima_idx = argrelextrema(lows, np.less_equal, order=5)[0]

        if len(minima_idx) < 2:
            return trendlines

        # Try all combinations of pivot points to find valid trendlines
        for i in range(len(minima_idx)):
            for j in range(i + 1, len(minima_idx)):
                idx1, idx2 = minima_idx[i], minima_idx[j]

                # Fit line through these two points
                x = np.array([idx1, idx2])
                y = np.array([lows[idx1], lows[idx2]])

                slope, intercept, r_value, _, _ = stats.linregress(x, y)

                # Extend trendline forward and backward
                start_idx = idx1
                end_idx = min(idx2 + 20, len(df) - 1)  # Extend a bit beyond

                # Count touches and validate
                touches, actual_touches, breaks = self._count_touches_support(
                    df, slope, intercept, start_idx, end_idx
                )

                if touches >= self.min_touches and abs(r_value) >= self.min_r_squared:
                    # Calculate strength score
                    strength = self._calculate_strength(touches, r_value, breaks)

                    trendline = Trendline(
                        slope=slope,
                        intercept=intercept,
                        start_idx=start_idx,
                        end_idx=end_idx,
                        start_price=slope * start_idx + intercept,
                        end_price=slope * end_idx + intercept,
                        strength=strength,
                        type='support',
                        touches=touches,
                        r_squared=r_value ** 2,
                        breaks=breaks
                    )
                    trendlines.append(trendline)

        # Remove duplicate/overlapping trendlines
        trendlines = self._remove_duplicates(trendlines)

        # Sort by strength
        trendlines.sort(key=lambda x: x.strength, reverse=True)

        # Keep top N strongest
        return trendlines[:10]

    def _detect_resistance_trendlines(self, df: pd.DataFrame) -> List[Trendline]:
        """Detect resistance trendlines (drawn above price)"""
        trendlines = []

        highs = df['high'].values
        closes = df['close'].values

        # Find local maxima (potential resistance pivot points)
        maxima_idx = argrelextrema(highs, np.greater_equal, order=5)[0]

        if len(maxima_idx) < 2:
            return trendlines

        # Try all combinations of pivot points
        for i in range(len(maxima_idx)):
            for j in range(i + 1, len(maxima_idx)):
                idx1, idx2 = maxima_idx[i], maxima_idx[j]

                x = np.array([idx1, idx2])
                y = np.array([highs[idx1], highs[idx2]])

                slope, intercept, r_value, _, _ = stats.linregress(x, y)

                start_idx = idx1
                end_idx = min(idx2 + 20, len(df) - 1)

                touches, actual_touches, breaks = self._count_touches_resistance(
                    df, slope, intercept, start_idx, end_idx
                )

                if touches >= self.min_touches and abs(r_value) >= self.min_r_squared:
                    strength = self._calculate_strength(touches, r_value, breaks)

                    trendline = Trendline(
                        slope=slope,
                        intercept=intercept,
                        start_idx=start_idx,
                        end_idx=end_idx,
                        start_price=slope * start_idx + intercept,
                        end_price=slope * end_idx + intercept,
                        strength=strength,
                        type='resistance',
                        touches=touches,
                        r_squared=r_value ** 2,
                        breaks=breaks
                    )
                    trendlines.append(trendline)

        trendlines = self._remove_duplicates(trendlines)
        trendlines.sort(key=lambda x: x.strength, reverse=True)

        return trendlines[:10]

    def _count_touches_support(
        self,
        df: pd.DataFrame,
        slope: float,
        intercept: float,
        start_idx: int,
        end_idx: int
    ) -> Tuple[int, List[int], int]:
        """
        Count how many times price touches a support trendline

        Returns:
            (touch_count, actual_touch_indices, break_count)
        """
        touches = 0
        actual_touches = []
        breaks = 0

        for idx in range(start_idx, end_idx + 1):
            if idx >= len(df):
                break

            trendline_price = slope * idx + intercept
            low = df['low'].iloc[idx]
            close = df['close'].iloc[idx]

            # Touch: low comes within tolerance of trendline
            if abs(low - trendline_price) / trendline_price < self.tolerance:
                touches += 1
                actual_touches.append(idx)

            # Break: close goes below trendline by more than tolerance
            elif close < trendline_price * (1 - self.tolerance):
                breaks += 1

        return touches, actual_touches, breaks

    def _count_touches_resistance(
        self,
        df: pd.DataFrame,
        slope: float,
        intercept: float,
        start_idx: int,
        end_idx: int
    ) -> Tuple[int, List[int], int]:
        """Count how many times price touches a resistance trendline"""
        touches = 0
        actual_touches = []
        breaks = 0

        for idx in range(start_idx, end_idx + 1):
            if idx >= len(df):
                break

            trendline_price = slope * idx + intercept
            high = df['high'].iloc[idx]
            close = df['close'].iloc[idx]

            # Touch: high comes within tolerance of trendline
            if abs(high - trendline_price) / trendline_price < self.tolerance:
                touches += 1
                actual_touches.append(idx)

            # Break: close goes above trendline by more than tolerance
            elif close > trendline_price * (1 + self.tolerance):
                breaks += 1

        return touches, actual_touches, breaks

    def _calculate_strength(
        self,
        touches: int,
        r_value: float,
        breaks: int
    ) -> float:
        """
        Calculate overall strength of trendline

        Factors:
        - More touches = stronger
        - Higher R² = stronger
        - Breaks = weaker
        """
        # Base score from touches (max 50 points)
        touch_score = min(50, touches * 10)

        # R² score (max 40 points)
        r_squared_score = (r_value ** 2) * 40

        # Break penalty (minus 5 points per break)
        break_penalty = breaks * 5

        strength = touch_score + r_squared_score - break_penalty

        # Clamp to 0-100
        return max(0, min(100, strength))

    def _remove_duplicates(self, trendlines: List[Trendline]) -> List[Trendline]:
        """Remove very similar trendlines (likely duplicates)"""
        if len(trendlines) <= 1:
            return trendlines

        unique = []

        for tl in trendlines:
            is_duplicate = False

            for existing in unique:
                # Check if slopes and intercepts are very similar
                slope_diff = abs(tl.slope - existing.slope)
                intercept_diff = abs(tl.intercept - existing.intercept)

                # Also check if they cover similar time periods
                time_overlap = (
                    min(tl.end_idx, existing.end_idx) - max(tl.start_idx, existing.start_idx)
                ) / max(tl.end_idx - tl.start_idx, existing.end_idx - existing.start_idx)

                if (slope_diff < 0.01 and intercept_diff < 5 and time_overlap > 0.7):
                    is_duplicate = True
                    # Keep the stronger one
                    if tl.strength > existing.strength:
                        unique.remove(existing)
                        unique.append(tl)
                    break

            if not is_duplicate:
                unique.append(tl)

        return unique


def detect_horizontal_support_resistance(
    df: pd.DataFrame,
    lookback: int = 100,
    min_touches: int = 3,
    tolerance: float = 0.015  # 1.5% tolerance
) -> Dict[str, List[float]]:
    """
    Detect horizontal support and resistance levels

    These are price levels where price has bounced multiple times

    Returns:
        Dict with 'support' and 'resistance' lists of price levels
    """
    data = df.tail(lookback) if len(df) > lookback else df

    highs = data['high'].values
    lows = data['low'].values

    # Find local minima and maxima
    support_pivots = argrelextrema(lows, np.less_equal, order=5)[0]
    resistance_pivots = argrelextrema(highs, np.greater_equal, order=5)[0]

    # Cluster similar price levels
    support_levels = _cluster_price_levels(lows[support_pivots], tolerance, min_touches)
    resistance_levels = _cluster_price_levels(highs[resistance_pivots], tolerance, min_touches)

    logger.info(f"Found {len(support_levels)} horizontal support and {len(resistance_levels)} resistance levels")

    return {
        "support": support_levels,
        "resistance": resistance_levels
    }


def _cluster_price_levels(
    prices: np.ndarray,
    tolerance: float,
    min_touches: int
) -> List[float]:
    """
    Cluster similar price levels together

    If multiple pivot points are within tolerance, group them as one level
    """
    if len(prices) == 0:
        return []

    # Sort prices
    sorted_prices = np.sort(prices)

    levels = []
    current_cluster = [sorted_prices[0]]

    for i in range(1, len(sorted_prices)):
        # If within tolerance of current cluster, add to it
        if abs(sorted_prices[i] - current_cluster[0]) / current_cluster[0] < tolerance:
            current_cluster.append(sorted_prices[i])
        else:
            # Start new cluster
            if len(current_cluster) >= min_touches:
                # Take average of cluster as the level
                levels.append(float(np.mean(current_cluster)))

            current_cluster = [sorted_prices[i]]

    # Don't forget last cluster
    if len(current_cluster) >= min_touches:
        levels.append(float(np.mean(current_cluster)))

    return levels
