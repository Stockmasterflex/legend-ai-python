import math

from app.core.pattern_detector import PatternDetector


def build_rising_wedge_series():
    highs = []
    lows = []
    for i in range(60):
        hi = 100 + i * 0.15
        lo = 98 + i * 0.25
        if i >= 30:
            adjustment = (i - 29) * 0.05
            hi -= adjustment
            lo += adjustment * 0.8
        highs.append(hi)
        lows.append(lo)
    return highs, lows


def test_detect_rising_wedge_hits():
    detector = PatternDetector()
    highs, lows = build_rising_wedge_series()
    result = detector._detect_wedge(highs, lows, direction="rising")
    assert result["hit"], f"Expected rising wedge, got {result}"
    assert result["name"] == "Rising Wedge"


def test_detect_ascending_triangle_hits():
    detector = PatternDetector()
    highs = []
    lows = []
    for i in range(70):
        hi = 120.0 if i > 20 else 118 + i * 0.05
        lo = 100 + i * 0.25
        highs.append(hi)
        lows.append(lo)
    result = detector._detect_triangle(highs, lows, kind="ascending")
    assert result["hit"], f"Expected ascending triangle, got {result}"
    assert result["name"] == "Ascending Triangle"


def test_detect_head_shoulders_hits():
    detector = PatternDetector()
    closes = [100 + (i * 0.02) for i in range(120)]
    pattern = [
        104, 106, 108, 109, 108, 106, 104,  # left shoulder
        107, 110, 114, 116, 114, 110, 107,  # head
        105, 107, 109, 110, 108, 106, 104   # right shoulder
    ]
    start = 70
    for idx, val in enumerate(pattern):
        closes[start + idx] = val
    result = detector._detect_head_shoulders(closes, inverted=False)
    assert result["hit"], f"Expected head & shoulders, got {result}"
    assert result["name"] == "Head & Shoulders"


def test_detect_inverse_head_shoulders_hits():
    detector = PatternDetector()
    closes = [100 - (i * 0.01) for i in range(120)]
    pattern = [
        96, 94, 93, 94, 96, 97, 98,        # left shoulder (inverse)
        95, 92, 90, 89, 90, 92, 95,        # head (inverse)
        96, 97, 98, 99, 98, 97, 96         # right shoulder (inverse)
    ]
    start = 60
    for idx, val in enumerate(pattern):
        closes[start + idx] = val
    result = detector._detect_head_shoulders(closes, inverted=True)
    assert result["hit"], f"Expected inverse head & shoulders, got {result}"
    assert result["name"] == "Inverse Head & Shoulders"
