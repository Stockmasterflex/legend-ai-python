"""Comprehensive unit tests for all 8 pattern detectors."""
import pandas as pd
import numpy as np
import pytest
from datetime import datetime, timedelta

from app.core.detectors.vcp_detector import VCPDetector
from app.core.detectors.cup_handle_detector import CupHandleDetector
from app.core.detectors.triangle_detector import TriangleDetector
from app.core.detectors.wedge_detector import WedgeDetector
from app.core.detectors.head_shoulders_detector import HeadShouldersDetector
from app.core.detectors.double_top_bottom_detector import DoubleTopBottomDetector
from app.core.detectors.channel_detector import ChannelDetector
from app.core.detectors.sma50_pullback_detector import SMA50PullbackDetector
from app.core.detector_base import PatternType


def create_base_df(prices: list[float], start_date: str = "2024-01-01") -> pd.DataFrame:
    """Create a base DataFrame with OHLCV data."""
    dates = pd.date_range(start_date, periods=len(prices), freq="B")
    volumes = np.linspace(1_000_000, 500_000, len(prices))

    return pd.DataFrame({
        "datetime": dates,
        "open": [p - 0.3 for p in prices],
        "high": [p + 0.6 for p in prices],
        "low": [p - 0.6 for p in prices],
        "close": prices,
        "volume": volumes,
    })


# ==================== VCP Detector Tests ====================

def test_vcp_detector_runs_without_error():
    """Test VCP detector runs without errors on valid data."""
    detector = VCPDetector()

    # Build realistic price data (at least 100 bars as required)
    prices = []

    # Run-up phase
    prices.extend(np.linspace(80, 130, 40).tolist())

    # Contraction 1 (largest)
    prices.extend(np.linspace(130, 110, 20).tolist())
    prices.extend(np.linspace(110, 125, 15).tolist())

    # Contraction 2 (medium)
    prices.extend(np.linspace(125, 115, 15).tolist())
    prices.extend(np.linspace(115, 123, 12).tolist())

    # Contraction 3 (smallest)
    prices.extend(np.linspace(123, 118, 10).tolist())
    prices.extend(np.linspace(118, 122, 8).tolist())

    # Breakout
    prices.extend(np.linspace(122, 140, 15).tolist())

    df = create_base_df(prices)

    # Main test: should not crash
    results = detector.find(df, "1D", "TEST")

    # Validate structure
    assert isinstance(results, list)
    for result in results:
        assert hasattr(result, 'pattern_type')
        assert hasattr(result, 'confidence')
        assert hasattr(result, 'lines')
        assert result.pattern_type == PatternType.VCP
        assert 0 <= result.confidence <= 1


def test_vcp_detector_rejects_noise():
    """Test VCP detector rejects random noise."""
    detector = VCPDetector()

    # Random noise without pattern
    prices = np.linspace(100, 140, 160) + np.random.randn(160) * 2
    df = create_base_df(prices.tolist())

    results = detector.find(df, "1D", "NOISE")
    assert len(results) == 0, "VCP detector should not find patterns in noise"


def test_vcp_detector_requires_volume_contraction():
    """Test VCP detector validates volume contraction."""
    detector = VCPDetector()

    # Price pattern OK but volume doesn't contract
    prices = []
    prices.extend(np.linspace(100, 150, 50).tolist())
    prices.extend(np.linspace(150, 135, 20).tolist())
    prices.extend(np.linspace(135, 145, 15).tolist())
    prices.extend(np.linspace(145, 140, 10).tolist())

    df = create_base_df(prices)
    # Override volume to be constant (no contraction)
    df["volume"] = 1_000_000

    results = detector.find(df, "1D", "NO_VOL_CONTRACT")
    # Should either find nothing or have lower confidence
    if len(results) > 0:
        assert results[0].confidence < 0.7


# ==================== Cup & Handle Detector Tests ====================

def test_cup_handle_detector_runs_without_error():
    """Test Cup & Handle detector runs without errors on valid data."""
    detector = CupHandleDetector()

    prices = []
    # Left side of cup
    prices.extend(np.linspace(100, 85, 30).tolist())
    # Bottom of cup (rounded)
    prices.extend(np.linspace(85, 86, 20).tolist())
    # Right side of cup
    prices.extend(np.linspace(86, 99, 30).tolist())
    # Handle (small pullback)
    prices.extend(np.linspace(99, 95, 10).tolist())
    # Breakout
    prices.extend(np.linspace(95, 110, 15).tolist())

    df = create_base_df(prices)
    results = detector.find(df, "1D", "TEST")

    # Should not crash
    assert isinstance(results, list)
    for result in results:
        assert result.pattern_type == PatternType.CUP_HANDLE
        assert 0 <= result.confidence <= 1


def test_cup_handle_detector_validates_symmetry():
    """Test Cup & Handle detector requires cup symmetry."""
    detector = CupHandleDetector()

    # Asymmetric cup (should fail or have low confidence)
    prices = []
    prices.extend(np.linspace(100, 85, 10).tolist())  # Fast drop
    prices.extend(np.linspace(85, 99, 50).tolist())   # Slow recovery

    df = create_base_df(prices)
    results = detector.find(df, "1D", "ASYMMETRIC")

    # Should either find nothing or have low confidence
    if len(results) > 0:
        assert results[0].confidence < 0.6


# ==================== Triangle Detector Tests ====================

def test_triangle_detector_identifies_ascending():
    """Test Triangle detector identifies ascending triangles."""
    detector = TriangleDetector()

    prices = []
    # Flat top, rising bottom
    for i in range(70):
        high = 120.0 if i > 20 else 118 + i * 0.1
        low = 100 + i * 0.25
        mid = (high + low) / 2
        prices.append(mid)

    df = create_base_df(prices)
    results = detector.find(df, "1D", "TEST")

    assert len(results) > 0, "Triangle detector should find ascending triangle"
    result = results[0]
    assert result.pattern_type == PatternType.ASCENDING_TRIANGLE
    assert result.confidence > 0.4


def test_triangle_detector_identifies_descending():
    """Test Triangle detector identifies descending triangles."""
    detector = TriangleDetector()

    prices = []
    # Flat bottom, declining top
    for i in range(70):
        low = 100.0
        high = 130 - i * 0.25
        mid = (high + low) / 2
        prices.append(mid)

    df = create_base_df(prices)
    results = detector.find(df, "1D", "TEST")

    assert len(results) > 0, "Triangle detector should find descending triangle"
    result = results[0]
    assert result.pattern_type == PatternType.DESCENDING_TRIANGLE
    assert result.confidence > 0.4


def test_triangle_detector_identifies_symmetrical():
    """Test Triangle detector identifies symmetrical triangles."""
    detector = TriangleDetector()

    prices = []
    # Converging highs and lows
    for i in range(70):
        high = 130 - i * 0.2
        low = 100 + i * 0.2
        mid = (high + low) / 2
        prices.append(mid)

    df = create_base_df(prices)
    results = detector.find(df, "1D", "TEST")

    assert len(results) > 0, "Triangle detector should find symmetrical triangle"
    result = results[0]
    assert result.pattern_type == PatternType.SYMMETRICAL_TRIANGLE
    assert result.confidence > 0.4


# ==================== Wedge Detector Tests ====================

def test_wedge_detector_identifies_rising():
    """Test Wedge detector identifies rising wedges."""
    detector = WedgeDetector()

    prices = []
    # Both lines rising, but lower line rises faster (converging upward)
    for i in range(60):
        high = 100 + i * 0.15
        low = 98 + i * 0.25
        if i >= 30:
            adjustment = (i - 29) * 0.05
            high -= adjustment
            low += adjustment * 0.8
        mid = (high + low) / 2
        prices.append(mid)

    df = create_base_df(prices)
    results = detector.find(df, "1D", "TEST")

    assert len(results) > 0, "Wedge detector should find rising wedge"
    result = results[0]
    assert result.pattern_type == PatternType.RISING_WEDGE
    assert result.confidence > 0.4


def test_wedge_detector_identifies_falling():
    """Test Wedge detector identifies falling wedges."""
    detector = WedgeDetector()

    prices = []
    # Both lines falling, but upper line falls faster (converging downward)
    for i in range(60):
        high = 150 - i * 0.25
        low = 148 - i * 0.15
        if i >= 30:
            adjustment = (i - 29) * 0.05
            high += adjustment * 0.8
            low -= adjustment
        mid = (high + low) / 2
        prices.append(mid)

    df = create_base_df(prices)
    results = detector.find(df, "1D", "TEST")

    assert len(results) > 0, "Wedge detector should find falling wedge"
    result = results[0]
    assert result.pattern_type == PatternType.FALLING_WEDGE
    assert result.confidence > 0.4


# ==================== Head & Shoulders Detector Tests ====================

def test_head_shoulders_detector_identifies_pattern():
    """Test Head & Shoulders detector identifies classic pattern."""
    detector = HeadShouldersDetector()

    prices = [100 + (i * 0.02) for i in range(120)]

    # Insert head and shoulders pattern
    pattern = [
        104, 106, 108, 109, 108, 106, 104,  # Left shoulder
        107, 110, 114, 116, 114, 110, 107,  # Head (higher)
        105, 107, 109, 110, 108, 106, 104   # Right shoulder
    ]

    start = 70
    for idx, val in enumerate(pattern):
        prices[start + idx] = val

    df = create_base_df(prices)
    results = detector.find(df, "1D", "TEST")

    assert len(results) > 0, "Head & Shoulders detector should find pattern"
    result = results[0]
    assert result.pattern_type == PatternType.HEAD_SHOULDERS
    assert result.confidence > 0.4


def test_head_shoulders_detector_identifies_inverse():
    """Test Head & Shoulders detector identifies inverse pattern."""
    detector = HeadShouldersDetector()

    prices = [100 - (i * 0.01) for i in range(120)]

    # Insert inverse pattern
    pattern = [
        96, 94, 93, 94, 96, 97, 98,        # Left shoulder (low)
        95, 92, 90, 89, 90, 92, 95,        # Head (lower)
        96, 97, 98, 99, 98, 97, 96         # Right shoulder
    ]

    start = 60
    for idx, val in enumerate(pattern):
        prices[start + idx] = val

    df = create_base_df(prices)
    results = detector.find(df, "1D", "TEST")

    assert len(results) > 0, "Head & Shoulders detector should find inverse pattern"
    result = results[0]
    assert result.pattern_type == PatternType.INVERSE_HEAD_SHOULDERS
    assert result.confidence > 0.4


# ==================== Double Top/Bottom Detector Tests ====================

def test_double_top_detector_identifies_pattern():
    """Test Double Top detector identifies two peaks at similar levels."""
    detector = DoubleTopBottomDetector()

    prices = []
    # First peak
    prices.extend(np.linspace(100, 130, 20).tolist())
    prices.extend(np.linspace(130, 110, 15).tolist())
    # Second peak
    prices.extend(np.linspace(110, 129, 20).tolist())
    prices.extend(np.linspace(129, 105, 15).tolist())

    df = create_base_df(prices)
    results = detector.find(df, "1D", "TEST")

    assert len(results) > 0, "Double Top detector should find pattern"
    result = results[0]
    assert result.pattern_type == PatternType.DOUBLE_TOP
    assert result.confidence > 0.4


def test_double_bottom_detector_identifies_pattern():
    """Test Double Bottom detector identifies two troughs at similar levels."""
    detector = DoubleTopBottomDetector()

    prices = []
    # First bottom
    prices.extend(np.linspace(100, 80, 20).tolist())
    prices.extend(np.linspace(80, 95, 15).tolist())
    # Second bottom
    prices.extend(np.linspace(95, 81, 20).tolist())
    prices.extend(np.linspace(81, 100, 15).tolist())

    df = create_base_df(prices)
    results = detector.find(df, "1D", "TEST")

    assert len(results) > 0, "Double Bottom detector should find pattern"
    result = results[0]
    assert result.pattern_type == PatternType.DOUBLE_BOTTOM
    assert result.confidence > 0.4


# ==================== Channel Detector Tests ====================

def test_channel_detector_identifies_ascending():
    """Test Channel detector identifies ascending channels."""
    detector = ChannelDetector()

    prices = []
    # Parallel ascending lines
    for i in range(80):
        high = 100 + i * 0.3
        low = 95 + i * 0.3
        mid = (high + low) / 2 + np.random.randn() * 0.5
        prices.append(mid)

    df = create_base_df(prices)
    results = detector.find(df, "1D", "TEST")

    assert len(results) > 0, "Channel detector should find ascending channel"
    result = results[0]
    assert result.pattern_type == PatternType.ASCENDING_CHANNEL
    assert result.confidence > 0.4


def test_channel_detector_identifies_descending():
    """Test Channel detector identifies descending channels."""
    detector = ChannelDetector()

    prices = []
    # Parallel descending lines
    for i in range(80):
        high = 150 - i * 0.3
        low = 145 - i * 0.3
        mid = (high + low) / 2 + np.random.randn() * 0.5
        prices.append(mid)

    df = create_base_df(prices)
    results = detector.find(df, "1D", "TEST")

    assert len(results) > 0, "Channel detector should find descending channel"
    result = results[0]
    assert result.pattern_type == PatternType.DESCENDING_CHANNEL
    assert result.confidence > 0.4


def test_channel_detector_identifies_horizontal():
    """Test Channel detector identifies horizontal channels."""
    detector = ChannelDetector()

    prices = []
    # Parallel horizontal lines
    for i in range(80):
        high = 120
        low = 110
        mid = (high + low) / 2 + np.random.randn() * 2
        prices.append(mid)

    df = create_base_df(prices)
    results = detector.find(df, "1D", "TEST")

    assert len(results) > 0, "Channel detector should find horizontal channel"
    result = results[0]
    assert result.pattern_type == PatternType.HORIZONTAL_CHANNEL
    assert result.confidence > 0.4


# ==================== SMA50 Pullback Detector Tests ====================

def test_sma50_pullback_detector_identifies_pattern():
    """Test SMA50 Pullback detector identifies pullback to 50-day SMA."""
    detector = SMA50PullbackDetector()

    # Create uptrend with pullback to SMA50
    prices = []
    # Strong uptrend
    prices.extend(np.linspace(100, 150, 60).tolist())
    # Pullback toward SMA
    prices.extend(np.linspace(150, 135, 15).tolist())
    # Bounce
    prices.extend(np.linspace(135, 155, 10).tolist())

    df = create_base_df(prices)
    results = detector.find(df, "1D", "TEST")

    assert len(results) > 0, "SMA50 Pullback detector should find pattern"
    result = results[0]
    assert result.pattern_type == PatternType.SMA50_PULLBACK
    assert result.confidence > 0.4


def test_sma50_pullback_requires_uptrend():
    """Test SMA50 Pullback detector requires prior uptrend."""
    detector = SMA50PullbackDetector()

    # Flat or downtrend - should not trigger
    prices = np.linspace(100, 95, 80).tolist()

    df = create_base_df(prices)
    results = detector.find(df, "1D", "NO_UPTREND")

    # Should not find pattern without uptrend
    assert len(results) == 0 or results[0].confidence < 0.5


# ==================== Edge Cases and Validation Tests ====================

def test_detectors_handle_insufficient_data():
    """Test all detectors gracefully handle insufficient data."""
    detectors = [
        VCPDetector(),
        CupHandleDetector(),
        TriangleDetector(),
        WedgeDetector(),
        HeadShouldersDetector(),
        DoubleTopBottomDetector(),
        ChannelDetector(),
        SMA50PullbackDetector(),
    ]

    # Very short data
    prices = [100, 101, 102]
    df = create_base_df(prices)

    for detector in detectors:
        results = detector.find(df, "1D", "SHORT")
        # Should return empty or handle gracefully
        assert isinstance(results, list)


def test_detectors_handle_extreme_volatility():
    """Test all detectors handle extreme volatility."""
    detectors = [
        VCPDetector(),
        CupHandleDetector(),
        TriangleDetector(),
        WedgeDetector(),
        HeadShouldersDetector(),
        DoubleTopBottomDetector(),
        ChannelDetector(),
        SMA50PullbackDetector(),
    ]

    # Extreme random volatility
    prices = (np.random.randn(100) * 50 + 100).tolist()
    df = create_base_df(prices)

    for detector in detectors:
        results = detector.find(df, "1D", "VOLATILE")
        # Should handle without crashing
        assert isinstance(results, list)


def test_detectors_return_valid_pattern_results():
    """Test all detectors return properly structured PatternResult objects."""
    detectors = [
        VCPDetector(),
        CupHandleDetector(),
        TriangleDetector(),
        WedgeDetector(),
        HeadShouldersDetector(),
        DoubleTopBottomDetector(),
        ChannelDetector(),
        SMA50PullbackDetector(),
    ]

    # Generic pattern
    prices = np.linspace(100, 150, 100).tolist()
    df = create_base_df(prices)

    for detector in detectors:
        results = detector.find(df, "1D", "VALIDATION")
        for result in results:
            # Validate structure
            assert hasattr(result, 'pattern_type')
            assert hasattr(result, 'confidence')
            assert hasattr(result, 'lines')
            assert 0 <= result.confidence <= 1
            assert isinstance(result.lines, dict)
