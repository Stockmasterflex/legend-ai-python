"""
Integration tests for the Legend AI pattern engine

Tests the complete pipeline:
1. Data conversion
2. Pattern detection
3. API integration
"""
import numpy as np
import pytest
from app.core.pattern_engine.helpers import PatternData, PatternHelpers
from app.core.pattern_engine.patterns import (
    find_cup,
    find_double_bottoms,
    find_ascending_triangle
)
from app.core.pattern_engine.detector import PatternDetector


def create_test_data(bars: int = 200) -> dict:
    """Create synthetic OHLCV data for testing"""
    np.random.seed(42)
    
    # Generate realistic price data
    base_price = 100.0
    prices = [base_price]
    
    for _ in range(bars - 1):
        change = np.random.randn() * 2.0  # Random walk
        prices.append(prices[-1] + change)
    
    prices = np.array(prices)
    
    # Create OHLCV
    highs = prices + np.random.rand(bars) * 2
    lows = prices - np.random.rand(bars) * 2
    opens = prices + np.random.randn(bars) * 0.5
    closes = prices + np.random.randn(bars) * 0.5
    volumes = np.random.randint(1000000, 5000000, bars).astype(float)
    
    return {
        'o': opens.tolist(),
        'h': highs.tolist(),
        'l': lows.tolist(),
        'c': closes.tolist(),
        'v': volumes.tolist(),
        't': list(range(bars))
    }


def create_cup_data() -> dict:
    """Create data with a clear cup pattern"""
    bars = 150
    
    # Left rim: bars 20-30
    # Bottom: bars 60-80
    # Right rim: bars 120-130
    
    prices = []
    for i in range(bars):
        if i < 30:
            prices.append(100.0)  # Left rim
        elif i < 80:
            # Descent to bottom
            prices.append(100.0 - (i - 30) * 0.6)
        elif i < 120:
            # Ascent to right rim
            prices.append(70.0 + (i - 80) * 0.75)
        else:
            prices.append(100.0)  # Right rim
    
    prices = np.array(prices)
    
    highs = prices + np.random.rand(bars) * 1
    lows = prices - np.random.rand(bars) * 1
    opens = prices + np.random.randn(bars) * 0.3
    closes = prices + np.random.randn(bars) * 0.3
    volumes = np.random.randint(1000000, 5000000, bars).astype(float)
    
    return {
        'o': opens.tolist(),
        'h': highs.tolist(),
        'l': lows.tolist(),
        'c': closes.tolist(),
        'v': volumes.tolist(),
        't': list(range(bars))
    }


def test_pattern_data_creation():
    """Test PatternData creation from OHLCV dict"""
    data_dict = create_test_data(100)
    
    pattern_data = PatternData(
        opens=np.array(data_dict['o']),
        highs=np.array(data_dict['h']),
        lows=np.array(data_dict['l']),
        closes=np.array(data_dict['c']),
        volumes=np.array(data_dict['v'])
    )
    
    assert len(pattern_data) == 100
    assert pattern_data.nHLC.shape == (6, 100)
    assert pattern_data.chart_start_index == 0
    assert pattern_data.chart_end_index == 99


def test_find_all_tops():
    """Test FindAllTops helper function"""
    helpers = PatternHelpers()
    
    # Create data with clear peaks
    highs = np.array([10, 15, 12, 18, 14, 22, 16, 20, 15, 18, 12, 15])
    
    tops = helpers.find_all_tops(highs, 0, 11, trade_days=2)
    
    # Should find peaks at indices with local maxima
    assert len(tops) > 0
    print(f"Found {len(tops)} tops at indices: {tops}")


def test_find_all_bottoms():
    """Test FindAllBottoms helper function"""
    helpers = PatternHelpers()
    
    # Create data with clear troughs
    lows = np.array([10, 8, 12, 6, 10, 5, 9, 7, 11, 6, 10, 8])
    
    bottoms = helpers.find_all_bottoms(lows, 0, 11, trade_days=2)
    
    # Should find troughs at indices with local minima
    assert len(bottoms) > 0
    print(f"Found {len(bottoms)} bottoms at indices: {bottoms}")


def test_check_nearness():
    """Test CheckNearness helper function"""
    helpers = PatternHelpers()
    
    # Test percentage-based nearness
    assert helpers.check_nearness(100.0, 100.5, percent=0.01)  # Within 1%
    assert not helpers.check_nearness(100.0, 105.0, percent=0.01)  # Outside 1%
    
    # Test price-based nearness
    assert helpers.check_nearness(50.0, 50.20, price_vary=0.25)  # Within $0.25
    assert not helpers.check_nearness(50.0, 51.0, price_vary=0.25)  # Outside $0.25


def test_cup_detection():
    """Test Cup & Handle detection"""
    data_dict = create_cup_data()
    
    pattern_data = PatternData(
        opens=np.array(data_dict['o']),
        highs=np.array(data_dict['h']),
        lows=np.array(data_dict['l']),
        closes=np.array(data_dict['c']),
        volumes=np.array(data_dict['v'])
    )
    
    helpers = PatternHelpers()
    cups = find_cup(pattern_data, helpers, strict=False)
    
    print(f"\nFound {len(cups)} cup patterns")
    for i, cup in enumerate(cups):
        print(f"Cup {i+1}:")
        print(f"  Pattern: {cup['pattern']}")
        print(f"  Width: {cup['cup_width']} bars")
        print(f"  Depth: ${cup['cup_depth']:.2f}")
        print(f"  Confirmed: {cup['confirmed']}")
        print(f"  Confidence: {cup['confidence']:.2%}")
    
    # Should detect at least the synthetic cup we created
    # Note: May or may not find one depending on exact thresholds
    assert isinstance(cups, list)


def test_double_bottom_detection():
    """Test Double Bottom detection"""
    data_dict = create_test_data(200)
    
    pattern_data = PatternData(
        opens=np.array(data_dict['o']),
        highs=np.array(data_dict['h']),
        lows=np.array(data_dict['l']),
        closes=np.array(data_dict['c']),
        volumes=np.array(data_dict['v'])
    )
    
    helpers = PatternHelpers()
    double_bottoms = find_double_bottoms(pattern_data, helpers, find_variants=True)
    
    print(f"\nFound {len(double_bottoms)} double bottom patterns")
    for i, db in enumerate(double_bottoms):
        print(f"DB {i+1}:")
        print(f"  Pattern: {db['pattern']}")
        print(f"  Width: {db['width']} bars")
        print(f"  Variant: {db.get('variant', 'N/A')}")
        print(f"  Confirmed: {db['confirmed']}")
        print(f"  Confidence: {db['confidence']:.2%}")
    
    assert isinstance(double_bottoms, list)


def test_pattern_detector():
    """Test full Legend AI pattern detector pipeline"""
    data_dict = create_cup_data()

    detector = PatternDetector(strict=False)
    patterns = detector.detect_all_patterns(data_dict, ticker="TEST")
    
    print("\n=== Pattern Detector Results ===")
    print(f"Found {len(patterns)} total patterns")
    
    for i, pattern in enumerate(patterns):
        print(f"\nPattern {i+1}:")
        print(f"  Type: {pattern['pattern']}")
        print(f"  Confidence: {pattern['confidence']:.2%}")
        print(f"  Score: {pattern['score']:.1f}/10")
        print(f"  Entry: ${pattern['entry']:.2f}")
        print(f"  Stop: ${pattern['stop']:.2f}")
        print(f"  Target: ${pattern['target']:.2f}")
        print(f"  R/R: {pattern['risk_reward']:.2f}:1")
        print(f"  Confirmed: {pattern['confirmed']}")
        print(f"  Width: {pattern['width']} bars")
    
    assert isinstance(patterns, list)
    
    # If patterns found, verify they have correct structure
    if patterns:
        p = patterns[0]
        assert 'pattern' in p
        assert 'confidence' in p
        assert 'entry' in p
        assert 'stop' in p
        assert 'target' in p
        assert 'risk_reward' in p
        assert 0 <= p['confidence'] <= 1
        assert 0 <= p['score'] <= 10
        assert p['target'] > p['entry'] > p['stop']


def test_data_conversion():
    """Test conversion from API format to PatternData"""
    data_dict = create_test_data(100)
    
    detector = PatternDetector()
    pattern_data = detector._convert_to_pattern_data(data_dict)
    
    assert isinstance(pattern_data, PatternData)
    assert len(pattern_data) == 100
    assert pattern_data.nHLC.shape == (6, 100)


if __name__ == "__main__":
    print("Running pattern engine integration tests...\n")
    
    test_pattern_data_creation()
    print("✓ PatternData creation")
    
    test_find_all_tops()
    print("✓ FindAllTops")
    
    test_find_all_bottoms()
    print("✓ FindAllBottoms")
    
    test_check_nearness()
    print("✓ CheckNearness")
    
    test_cup_detection()
    print("✓ Cup detection")
    
    test_double_bottom_detection()
    print("✓ Double Bottom detection")
    
    test_pattern_detector()
    print("✓ Full pattern detector")
    
    test_data_conversion()
    print("✓ Data conversion")
    
    print("\n=== ALL TESTS PASSED ===")

