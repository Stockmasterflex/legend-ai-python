"""
Base classes and utilities for pattern detectors.
Provides the common Detector interface and shared data structures.
"""
from dataclasses import dataclass, asdict
from typing import Protocol, Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod


class PatternType(str, Enum):
    """All supported pattern types"""
    HORIZONTAL_SR = "Horizontal S/R"
    TRENDLINE_SR = "Trendline S/R"
    TRIANGLE_ASC = "Triangle Ascending"
    TRIANGLE_DESC = "Triangle Descending"
    TRIANGLE_SYM = "Triangle Symmetrical"
    CHANNEL_UP = "Channel Up"
    CHANNEL_DOWN = "Channel Down"
    CHANNEL_ANY = "Channel"
    WEDGE_RISING = "Wedge Rising"
    WEDGE_FALLING = "Wedge Falling"
    DOUBLE_TOP = "Double Top"
    DOUBLE_BOTTOM = "Double Bottom"
    MULTIPLE_TOP = "Multiple Top"
    MULTIPLE_BOTTOM = "Multiple Bottom"
    HEAD_SHOULDERS = "Head & Shoulders"
    HEAD_SHOULDERS_INV = "Head & Shoulders Inverse"
    VCP = "VCP (Volatility Contraction)"
    CUP_HANDLE = "Cup & Handle"


@dataclass
class PricePoint:
    """A point in time-price space"""
    datetime: str  # ISO8601
    price: float
    bar_index: int  # Index in OHLCV series


@dataclass
class LineSegment:
    """A line segment defined by two points"""
    p1: PricePoint
    p2: PricePoint
    r_squared: Optional[float] = None  # Fit quality
    touches: Optional[int] = None  # Number of touches


@dataclass
class PatternResult:
    """
    Standard output for all pattern detectors.
    Follows JSON schema for consistency.
    """
    symbol: str
    timeframe: str
    asof: str  # ISO8601 timestamp
    pattern_type: PatternType
    strong: bool  # Is this a "Strong" pattern (confidence ≥ 0.75)?
    confidence: float  # [0, 1]

    # Pattern geometry
    window_start: str  # ISO8601
    window_end: str  # ISO8601

    # Structure (varies by pattern type)
    lines: Dict[str, Any]  # e.g., {"upper": LineSegment, "lower": LineSegment}
    touches: Dict[str, int]  # e.g., {"upper": 4, "lower": 3}

    # Breakout info (if applicable)
    breakout: Optional[Dict[str, Any]] = None  # {"dir": "up/down", "t": "...", "price": X, "volume_z": Y}

    # Evidence for transparency
    evidence: Optional[Dict[str, Any]] = None  # {"pivots": [...], "metrics": {...}}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, handling nested dataclasses"""
        result = asdict(self)
        result["pattern_type"] = self.pattern_type.value
        # Recursively handle nested PricePoint and LineSegment
        result["lines"] = self._serialize_lines(self.lines)
        if self.breakout:
            result["breakout"] = self._serialize_lines(self.breakout)
        return result

    @staticmethod
    def _serialize_lines(obj: Any) -> Any:
        """Recursively serialize nested dataclass objects"""
        if isinstance(obj, dict):
            return {k: PatternResult._serialize_lines(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [PatternResult._serialize_lines(item) for item in obj]
        elif isinstance(obj, (PricePoint, LineSegment)):
            return asdict(obj)
        else:
            return obj


# ============================================================================
# DETECTOR PROTOCOL
# ============================================================================
class Detector(ABC):
    """
    Base class for all pattern detectors.
    Each detector implements a find() method that analyzes OHLCV data
    and returns a list of PatternResult objects.
    """

    def __init__(self, name: str, **kwargs):
        """
        Initialize detector with configuration.

        Args:
            name: Detector name (used for logging)
            **kwargs: Threshold overrides (e.g., min_length=50)
        """
        self.name = name
        self.params = kwargs
        self._config = kwargs

    @abstractmethod
    def find(self, ohlcv: pd.DataFrame, timeframe: str, symbol: str) -> List[PatternResult]:
        """
        Detect patterns in OHLCV data.

        Args:
            ohlcv: DataFrame with columns ['open','high','low','close','volume','datetime']
            timeframe: Timeframe string (e.g., "1D", "1W")
            symbol: Symbol name (e.g., "AAPL")

        Returns:
            List of PatternResult objects (may be empty)
        """
        pass

    @property
    def config(self):
        """Return configuration object for this detector"""
        return getattr(self, "_config", self.params)

    @config.setter
    def config(self, value):
        self._config = value


# ============================================================================
# HELPER: Geometric calculations
# ============================================================================
class GeometryHelper:
    """Utilities for line fitting, distance calculations, convergence, etc."""

    @staticmethod
    def fit_line_ransac(points: List[tuple], max_iterations: int = 100) -> Optional[tuple]:
        """
        Fit a line to points using RANSAC.
        Returns (slope, intercept, r_squared, inliers_indices)
        """
        if len(points) < 2:
            return None
        try:
            from sklearn.linear_model import RANSACRegressor

            X = np.array([p[0] for p in points]).reshape(-1, 1)
            y = np.array([p[1] for p in points])

            ransac = RANSACRegressor(random_state=42)
            ransac.fit(X, y)

            # R² score
            r2 = ransac.score(X, y)
            slope = ransac.estimator_.coef_[0]
            intercept = ransac.estimator_.intercept_
            inliers = ransac.inlier_mask_

            return (slope, intercept, r2, inliers)
        except (ValueError, ImportError, NameError) as e:
            # RANSAC can fail with insufficient data or numerical issues
            # Also catch ImportError if sklearn is missing
            return None
        except Exception:
             # Catch np.linalg.LinAlgError if np is available, or any other error
            return None

    @staticmethod
    def distance_point_to_line(point: tuple, slope: float, intercept: float) -> float:
        """Distance from point (x, y) to line y = slope*x + intercept"""
        x, y = point
        # Line: slope*x - y + intercept = 0
        # Distance = |slope*x - y + intercept| / sqrt(slope^2 + 1)
        numerator = abs(slope * x - y + intercept)
        denominator = np.sqrt(slope**2 + 1)
        return numerator / denominator

    @staticmethod
    def count_touches(points: List[tuple], slope: float, intercept: float, tolerance: float) -> int:
        """Count how many points are within tolerance of the line"""
        count = 0
        for point in points:
            dist = GeometryHelper.distance_point_to_line(point, slope, intercept)
            if dist <= tolerance:
                count += 1
        return count

    @staticmethod
    def convergence_percent(line1_width: float, line2_width: float, window_len: int) -> float:
        """
        Compute convergence as percentage change in width.
        Higher = more convergence.
        """
        if window_len == 0 or line2_width == 0:
            return 0.0
        return max(0.0, (line1_width - line2_width) / line1_width)

    @staticmethod
    def parallel_offset(slope: float, intercept: float, offset_y: float) -> tuple:
        """
        Return parallel line offset by offset_y in y-direction.
        Returns (slope, new_intercept)
        """
        return (slope, intercept + offset_y)

    @staticmethod
    def line_intersection(s1: float, i1: float, s2: float, i2: float) -> Optional[tuple]:
        """Find intersection of two lines: y = s1*x + i1 and y = s2*x + i2"""
        if s1 == s2:
            return None  # Parallel lines
        x = (i2 - i1) / (s1 - s2)
        y = s1 * x + i1
        return (x, y)


# ============================================================================
# HELPER: Statistical calculations
# ============================================================================
class StatsHelper:
    """Utilities for ATR, volume z-score, Kendall τ, etc."""

    @staticmethod
    def atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> np.ndarray:
        """Calculate Average True Range"""
        tr = np.maximum(
            high - low,
            np.maximum(
                np.abs(high - np.roll(close, 1)),
                np.abs(low - np.roll(close, 1))
            )
        )
        tr[0] = high[0] - low[0]  # First bar has no previous close
        atr = pd.Series(tr).rolling(period).mean().values
        return atr

    @staticmethod
    def volume_z_score(volume: np.ndarray, window: int = 20) -> np.ndarray:
        """Z-score of volume over rolling window"""
        vol_series = pd.Series(volume)
        rolling_mean = vol_series.rolling(window).mean()
        rolling_std = vol_series.rolling(window).std()
        z_score = (vol_series - rolling_mean) / rolling_std.replace(0, 1)
        return z_score.values

    @staticmethod
    def kendall_tau(series: np.ndarray) -> float:
        """Kendall's τ correlation with time index (detects trend)"""
        from scipy.stats import kendalltau
        x = np.arange(len(series))
        tau, _ = kendalltau(x, series)
        return tau

    @staticmethod
    def zigzag_pivots(high: np.ndarray, low: np.ndarray, close: np.ndarray,
                      atr: np.ndarray) -> List[tuple]:
        """
        Detect pivots using ZigZag with adaptive threshold.
        Threshold = max(1.5*ATR/close, 0.5%), clamped to [0.5%, 8%]
        Returns list of (index, price, type) where type = 'high' or 'low'
        """
        pivots = []
        if len(close) < 3:
            return pivots

        # Compute adaptive threshold
        atr_pct = (1.5 * atr[:-1]) / close[:-1]
        threshold = np.clip(atr_pct, 0.005, 0.08)

        # Simple zigzag: find local highs and lows
        for i in range(1, len(close) - 1):
            if high[i] > high[i-1] and high[i] > high[i+1]:
                if not pivots or pivots[-1][2] != 'high':
                    pivots.append((i, high[i], 'high'))
            elif low[i] < low[i-1] and low[i] < low[i+1]:
                if not pivots or pivots[-1][2] != 'low':
                    pivots.append((i, low[i], 'low'))

        return pivots

    @staticmethod
    def find_zigzag_pivots(high: np.ndarray, low: np.ndarray, close: np.ndarray,
                          threshold: float = 0.03) -> List[Dict]:
        """
        Find zigzag pivots using simple percentage threshold.
        Returns list of dicts with keys: index, price, type

        Args:
            high: High prices
            low: Low prices
            close: Close prices
            threshold: Minimum percentage move to qualify as pivot (default 3%)

        Returns:
            List of pivot dictionaries
        """
        pivots = []
        if len(close) < 3:
            return pivots

        # Simple zigzag: find local highs and lows
        for i in range(1, len(close) - 1):
            if high[i] > high[i-1] and high[i] > high[i+1]:
                if not pivots or pivots[-1]['type'] != 'high':
                    pivots.append({'index': i, 'price': high[i], 'type': 'high'})
            elif low[i] < low[i-1] and low[i] < low[i+1]:
                if not pivots or pivots[-1]['type'] != 'low':
                    pivots.append({'index': i, 'price': low[i], 'type': 'low'})

        return pivots

    @staticmethod
    def calculate_atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> np.ndarray:
        """Calculate Average True Range (convenience alias for atr method)"""
        return StatsHelper.atr(high, low, close, period)

    @staticmethod
    def curvature_score(prices: np.ndarray) -> float:
        """
        Score smoothness of price curve (for Cup & Handle roundedness).
        Uses second derivative: score ∈ [0, 1], higher = smoother.
        """
        if len(prices) < 3:
            return 0.0

        # Compute first and second derivatives
        first_deriv = np.diff(prices)
        second_deriv = np.diff(first_deriv)

        # Smoothness = 1 / (1 + mean |second derivative|)
        mean_second_deriv = np.mean(np.abs(second_deriv))
        smoothness = 1.0 / (1.0 + mean_second_deriv / (np.std(prices) + 1e-8))
        return np.clip(smoothness, 0, 1)


# ============================================================================
# RESULT FILTERING & DEDUPLICATION
# ============================================================================
class ResultDeduplicator:
    """Remove overlapping patterns based on window IoU"""

    @staticmethod
    def window_iou(start1: int, end1: int, start2: int, end2: int) -> float:
        """Compute Intersection over Union of two time windows"""
        intersection = min(end1, end2) - max(start1, start2)
        if intersection <= 0:
            return 0.0
        union = max(end1, end2) - min(start1, start2)
        return intersection / union

    @staticmethod
    def deduplicate(results: List[PatternResult], iou_threshold: float = 0.50) -> List[PatternResult]:
        """Remove overlapping results, keeping highest confidence"""
        if len(results) <= 1:
            return results

        # TODO: Implement IoU deduplication
        # For now, return as-is
        return results
