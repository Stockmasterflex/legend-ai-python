"""
Configuration and threshold constants for pattern detectors.
All thresholds are tunable via environment variables or CLI flags.
"""
from typing import Dict, Any

# ============================================================================
# PRICE & TIME TOLERANCE
# ============================================================================
# Price tolerance is typically expressed as k * ATR (Average True Range)
# Time tolerance is expressed in bars

ATR_MULTIPLIER = 0.5  # Price tolerance ε = k * ATR for most operations
TIGHT_ATR_MULTIPLIER = 0.4  # Tighter tolerance for specific structures
LOOSE_ATR_MULTIPLIER = 0.6  # Looser tolerance when needed

# Time windows (in bars)
MIN_PATTERN_LENGTH = 20  # Minimum bars to form a valid pattern
MEDIUM_PATTERN_LENGTH = 40  # Medium timeframe for patterns
LONG_PATTERN_LENGTH = 120  # Maximum pattern length

# ============================================================================
# HORIZONTAL SUPPORT / RESISTANCE
# ============================================================================
class HorizontalSRConfig:
    """Horizontal S/R level detection"""
    MIN_TOUCHES = 3  # Minimum touches to form valid level
    MIN_SPAN_BARS = 20  # Minimum bar span for level to be valid
    DBSCAN_EPS_ATR = 0.5  # DBSCAN epsilon = eps_atr * ATR

    # Scoring weights
    TOUCHES_WEIGHT = 0.35
    RECENCY_WEIGHT = 0.35
    REACTION_VOLUME_WEIGHT = 0.30

# ============================================================================
# TRENDLINE SUPPORT / RESISTANCE
# ============================================================================
class TrendlineConfig:
    """Trendline (RANSAC-based) S/R detection"""
    MIN_TOUCHES = 3  # Minimum touches for valid trendline
    MIN_R_SQUARED = 0.85  # Minimum R² fit score
    MAX_DEVIATION_ATR = 0.5  # Max mean deviation = k * ATR

    # Strong criteria
    STRONG_R_SQUARED = 0.90
    STRONG_MIN_TOUCHES = 4

    TOUCHES_WEIGHT = 0.40
    FIT_WEIGHT = 0.40
    RECENCY_WEIGHT = 0.20

# ============================================================================
# TRIANGLES (Ascending / Descending / Symmetrical)
# ============================================================================
class TriangleConfig:
    """Triangle pattern detection"""
    MIN_LENGTH = 30  # Minimum bars
    MAX_LENGTH = 120  # Maximum bars
    MIN_TOUCHES_PER_SIDE = 3  # Min touches on each side
    CONVERGENCE_THRESHOLD = 0.30  # 30% convergence over window

    # Strong criteria
    STRONG_CONVERGENCE = 0.45
    STRONG_MIN_TOUCHES = 4
    BREAKOUT_LOOKBACK = 10  # Check last N bars for breakout

    # Scoring
    TOUCHES_WEIGHT = 0.30
    CONVERGENCE_WEIGHT = 0.35
    STRUCTURE_WEIGHT = 0.25
    RECENCY_WEIGHT = 0.10

# ============================================================================
# CHANNELS (Up / Down / Any)
# ============================================================================
class ChannelConfig:
    """Channel pattern detection"""
    MIN_LENGTH = 30  # Minimum bars
    MIN_TOUCHES_PER_SIDE = 3
    WIDTH_STABILITY_THRESHOLD = 0.15  # std(width) / mean(width) ≤ this

    # Strong criteria
    STRONG_R_SQUARED = 0.90
    STRONG_STABILITY = 0.10
    STRONG_MIN_LENGTH = 60

    # Scoring
    TOUCHES_WEIGHT = 0.30
    FIT_WEIGHT = 0.35
    STABILITY_WEIGHT = 0.25
    RECENCY_WEIGHT = 0.10

# ============================================================================
# WEDGES (Rising / Falling)
# ============================================================================
class WedgeConfig:
    """Wedge pattern detection"""
    MIN_LENGTH = 40  # Minimum bars
    CONVERGENCE_THRESHOLD = 0.30  # 30% convergence
    MIN_TOUCHES_PER_SIDE = 3

    # Volume contraction (20-bar rolling median Kendall τ < 0)
    VOLUME_CONTRACTION_TAU = 0.0  # Kendall τ threshold (< 0 = declining)

    # Strong criteria
    STRONG_CONVERGENCE = 0.45
    STRONG_MIN_TOUCHES = 3

    # Scoring
    TOUCHES_WEIGHT = 0.25
    CONVERGENCE_WEIGHT = 0.35
    VOLUME_WEIGHT = 0.30
    RECENCY_WEIGHT = 0.10

# ============================================================================
# DOUBLE TOP / DOUBLE BOTTOM
# ============================================================================
class DoubleTopBottomConfig:
    """Double Top/Bottom pattern detection"""
    MIN_TIME_SEPARATION = 5  # Bars between peaks/troughs
    MAX_TIME_SEPARATION = 60
    PEAK_PRICE_TOLERANCE = 0.01  # Within 1% or 0.6*ATR
    INTERMEDIATE_SWING_ATR = 1.0  # Swing must be ≥ this * ATR

    # Strong criteria
    STRONG_AMPLITUDE_ATR = 1.5  # Peaks ≥ 1.5*ATR apart
    STRONG_TIME_SYMMETRY = 0.30  # Time diff symmetry within 30%

    # Scoring
    AMPLITUDE_WEIGHT = 0.35
    SYMMETRY_WEIGHT = 0.35
    VOLUME_WEIGHT = 0.20
    RECENCY_WEIGHT = 0.10

# ============================================================================
# MULTIPLE TOP / MULTIPLE BOTTOM
# ============================================================================
class MultipleTopBottomConfig:
    """Multiple Top/Bottom pattern detection"""
    MIN_TOUCHES = 3  # Minimum 3 alternating pivots
    PRICE_TOLERANCE_ATR = 0.5

    # Strong criteria
    STRONG_MIN_TOUCHES = 4
    STRONG_VOLUME_DECLINE = True  # Volume declining into last touch

    # Scoring
    TOUCHES_WEIGHT = 0.40
    TIGHTNESS_WEIGHT = 0.30
    VOLUME_WEIGHT = 0.20
    RECENCY_WEIGHT = 0.10

# ============================================================================
# HEAD & SHOULDERS / INVERSE
# ============================================================================
class HeadShouldersConfig:
    """Head & Shoulders pattern detection"""
    MIN_LENGTH = 40  # Minimum bars
    LEFT_SHOULDER_MIN = 1.0  # LS height as baseline
    HEAD_MIN_RATIO = 1.2  # Head ≥ 1.2 * LS height
    RIGHT_SHOULDER_RATIO_RANGE = (0.8, 1.2)  # RS ∈ [0.8*LS, 1.2*LS]

    NECKLINE_MIN_R_SQUARED = 0.85  # Neckline fit
    NECKLINE_STRONG_R_SQUARED = 0.90

    # Strong criteria (breakout volume z-score ≥ +2)
    BREAKOUT_VOLUME_Z = 2.0

    # Scoring
    SYMMETRY_WEIGHT = 0.30
    NECKLINE_WEIGHT = 0.30
    VOLUME_WEIGHT = 0.25
    RECENCY_WEIGHT = 0.15

# ============================================================================
# VCP (VOLATILITY CONTRACTION PATTERN)
# ============================================================================
class VCPConfig:
    """
    VCP (Volatility Contraction Pattern) detection.
    Minervini-style: N≥3 contractions where percent declines shrink.
    """
    MIN_CONTRACTIONS = 3  # Minimum number of contractions
    MIN_CONTRACTION_DECLINE = 0.06  # Minimum 6% decline per contraction
    SHRINK_RATIO_THRESHOLD = 0.75  # d_{i+1}/d_i ≤ 0.75

    MIN_BASE_LENGTH = 30  # Minimum bars in base
    MAX_BASE_LENGTH = 200

    # Right-side climb tolerance
    RIGHT_SIDE_CLIMB_ATR = 1.0  # Within this * ATR of upper base line

    # Volume analysis
    VOLUME_DECLINE_WINDOW = 20  # Rolling median window (bars)
    VOLUME_DECLINE_TAU = 0.0  # Kendall τ for trend (< 0 = declining)
    VOLUME_SURGE_Z = 2.0  # Breakout volume z-score ≥ this

    # Tight area definition
    FINAL_TIGHT_AREA_ATR = 1.0  # Final contraction width ≤ this * ATR

    # Scoring
    CONTRACTIONS_WEIGHT = 0.35
    VOLUME_WEIGHT = 0.30
    STRUCTURE_WEIGHT = 0.25
    RECENCY_WEIGHT = 0.10

# ============================================================================
# CUP & HANDLE (CAN SLIM-STYLE)
# ============================================================================
class CupHandleConfig:
    """
    Cup & Handle pattern detection (CAN SLIM rules).
    Ref: Minervini, O'Neil
    """
    # Cup parameters
    CUP_DEPTH_MIN = 0.08  # 8% minimum
    CUP_DEPTH_TYPICAL = (0.12, 0.50)  # Typical 12-50%
    CUP_DEPTH_PENALTY = 0.55  # Allow 8-55% with penalty at edges
    CUP_MIN_LENGTH = 30  # Minimum bars
    CUP_MAX_LENGTH = 200  # Maximum bars

    # Roundedness: require smooth bottom (second derivative check)
    # or ≥3 higher lows in bottom third
    ROUNDEDNESS_MIN_SCORE = 0.75  # Curvature quality [0,1]

    # Right side tolerance
    RIGHT_SIDE_ATR = 2.0  # Within 2*ATR of left peak

    # Handle parameters
    HANDLE_MIN_LENGTH = 5  # Minimum bars
    HANDLE_MAX_LENGTH = 15  # Maximum bars
    HANDLE_PULLBACK_RATIO = 0.80  # ≤ 0.8 * cup depth
    HANDLE_MIN_PULLBACK = 0.05  # ≥ 5% pullback

    # Handle neckline should stay above cup midpoint
    HANDLE_MIDPOINT_CHECK = True

    # Scoring
    DEPTH_WEIGHT = 0.25
    ROUNDEDNESS_WEIGHT = 0.25
    HANDLE_WEIGHT = 0.20
    VOLUME_WEIGHT = 0.20
    RECENCY_WEIGHT = 0.10

# ============================================================================
# UNIVERSAL SCORING
# ============================================================================
class ScoringConfig:
    """Unified scoring system for all detectors"""
    # Weights sum to 1.0
    TOUCHES_WEIGHT = 0.30
    FIT_WEIGHT = 0.25
    STRUCTURE_WEIGHT = 0.20  # symmetry, convergence, stability, shrink, roundedness
    RECENCY_WEIGHT = 0.15
    VOLUME_WEIGHT = 0.10

    # Strong flag threshold
    STRONG_CONFIDENCE_THRESHOLD = 0.75

    # Confidence categories
    VERY_LOW = (0.0, 0.40)
    LOW = (0.40, 0.60)
    MEDIUM = (0.60, 0.75)
    STRONG = (0.75, 0.90)
    VERY_STRONG = (0.90, 1.0)

# ============================================================================
# GENERAL VOLUME & ATR CONFIG
# ============================================================================
class VolumeConfig:
    """Volume analysis configuration"""
    VOLUME_Z_SCORE_THRESHOLD = 2.0  # Breakout volume ≥ 2 std devs
    VOLUME_ROLLING_WINDOW = 20  # Bars for median/z-score calculation

class ATRConfig:
    """ATR (Average True Range) configuration"""
    ATR_PERIOD = 14  # Standard ATR period
    ATR_SMOOTHING = "SMA"  # "SMA" or "EMA"

# ============================================================================
# PIVOT DETECTION (ZIGZAG)
# ============================================================================
class PivotConfig:
    """Pivot detection via ZigZag"""
    # Adaptive percentage: max(1.5*ATR/close, 0.5%), clamped to [0.5%, 8%]
    MIN_PERCENT = 0.005  # 0.5%
    MAX_PERCENT = 0.08  # 8%
    ATR_FACTOR = 1.5  # Multiplier for ATR-based pivot threshold

# ============================================================================
# BREAKOUT DETECTION
# ============================================================================
class BreakoutConfig:
    """Breakout criteria"""
    VOLUME_Z_THRESHOLD = 2.0  # Volume surge ≥ 2 std devs
    PRICE_CONFIRMATION_BARS = 1  # Breakout must close outside boundary
    NEAR_BREAKOUT_RANGE_ATR = 1.0  # "Near breakout" if within this * ATR

# ============================================================================
# RESULT DEDUPLICATION
# ============================================================================
class DeduplicationConfig:
    """Remove overlapping results by window IoU"""
    IOU_THRESHOLD = 0.50  # Keep patterns with IoU < this, drop > this
    KEEP_STRATEGY = "highest_confidence"  # Keep pattern with highest confidence

# ============================================================================
# DEFAULT DETECTOR ACTIVATION
# ============================================================================
ACTIVE_DETECTORS = [
    "horizontal_sr",
    "trendline_sr",
    "triangle",
    "channel",
    "wedge",
    "double_top_bottom",
    "multiple_top_bottom",
    "head_shoulders",
    "vcp",
    "cup_handle"
]

# ============================================================================
# HELPER: Get config for a detector
# ============================================================================
def get_detector_config(detector_name: str) -> Dict[str, Any]:
    """Retrieve config object for a given detector"""
    configs = {
        "horizontal_sr": HorizontalSRConfig,
        "trendline_sr": TrendlineConfig,
        "triangle": TriangleConfig,
        "channel": ChannelConfig,
        "wedge": WedgeConfig,
        "double_top_bottom": DoubleTopBottomConfig,
        "multiple_top_bottom": MultipleTopBottomConfig,
        "head_shoulders": HeadShouldersConfig,
        "vcp": VCPConfig,
        "cup_handle": CupHandleConfig,
    }
    return configs.get(detector_name, {})
