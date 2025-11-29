import numpy as np

from app.core.pattern_engine.patterns.triple_formations import (
    find_triple_bottoms,
    find_triple_tops,
)
from app.core.pattern_engine.helpers import get_pattern_helpers


def test_find_triple_bottoms_detects_pattern():
    helpers = get_pattern_helpers()
    # Synthetic series with three similar lows and rising highs between
    lows = np.array([12, 11, 10, 11, 12, 10.2, 11.8, 13, 11, 10.1, 11.5, 12.5, 10.05, 11.7, 12.8, 13.5])
    highs = lows + 2
    closes = (highs + lows) / 2
    opens = closes
    volume = np.ones_like(lows) * 1000

    patterns = find_triple_bottoms(opens, highs, lows, closes, volume, helpers, strict=False)
    assert patterns, "Expected triple bottom detection"
    pat = patterns[0]
    assert pat["pattern"] == "Triple Bottom"
    assert pat["entry"] > pat["stop"]
    assert pat["target"] > pat["entry"]


def test_find_triple_tops_detects_pattern():
    helpers = get_pattern_helpers()
    highs = np.array([10, 11, 12.5, 11.8, 12.6, 11.7, 12.55, 11.9, 12.4, 11.6, 10.5])
    lows = highs - 2
    closes = (highs + lows) / 2
    opens = closes
    volume = np.ones_like(highs) * 900

    patterns = find_triple_tops(opens, highs, lows, closes, volume, helpers, strict=False)
    assert patterns, "Expected triple top detection"
    pat = patterns[0]
    assert pat["pattern"] == "Triple Top"
    assert pat["entry"] < pat["stop"]
