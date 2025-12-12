import numpy as np

from app.core.pattern_engine.helpers import get_pattern_helpers
from app.core.pattern_engine.patterns.head_shoulders import (
    find_head_shoulders_bottom, find_head_shoulders_top)


def test_head_shoulders_top_detects_pattern():
    helpers = get_pattern_helpers()
    highs = np.array([10, 11, 10.5, 12.5, 11.2, 10.7, 10.9])
    lows = np.array([9.5, 10.2, 9.8, 11.0, 10.1, 9.6, 9.7])
    closes = (highs + lows) / 2
    opens = closes
    volume = np.array([1000, 900, 850, 800, 820, 950, 970])

    patterns = find_head_shoulders_top(
        opens, highs, lows, closes, volume, helpers, strict=False
    )
    assert patterns, "Expected H&S Top detection"
    pat = patterns[0]
    assert "Neckline" not in pat["pattern"]  # sanity field
    assert pat["entry"] < pat["stop"]


def test_head_shoulders_bottom_detects_pattern():
    helpers = get_pattern_helpers()
    lows = np.array([10.5, 9.5, 10.2, 9.0, 9.8, 9.4, 10.1, 10.6])
    highs = lows + 1.5
    closes = (highs + lows) / 2
    opens = closes
    volume = np.array([900, 950, 920, 880, 890, 940, 980, 1100])

    patterns = find_head_shoulders_bottom(
        opens, highs, lows, closes, volume, helpers, strict=False
    )
    assert patterns, "Expected inverse H&S detection"
    pat = patterns[0]
    assert pat["entry"] > pat["stop"]
    assert pat["target"] > pat["entry"]
