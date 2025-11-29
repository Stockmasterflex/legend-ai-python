import numpy as np

from app.core.pattern_engine.helpers import get_pattern_helpers
from app.core.pattern_engine.patterns.rectangles import find_rectangles


def test_rectangle_detects_levels():
    helpers = get_pattern_helpers()
    lows = np.array(
        [10, 10.2, 10.1, 10.3, 10.0, 10.2, 10.1, 10.0, 10.2, 10.1, 10.05, 10.2]
    )
    highs = np.array(
        [12, 11.9, 12.1, 11.95, 12.05, 12.0, 11.9, 12.1, 12.0, 12.05, 12.1, 12.0]
    )
    closes = (highs + lows) / 2
    opens = closes
    volume = np.ones_like(highs) * 1000

    patterns = find_rectangles(
        opens, highs, lows, closes, volume, helpers, strict=False
    )
    assert patterns, "Expected rectangle detection"
    names = {p["pattern"] for p in patterns}
    assert "Rectangle Bullish" in names
    assert "Rectangle Bearish" in names
