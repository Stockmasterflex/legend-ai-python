import numpy as np

from app.core.pattern_engine.helpers import get_pattern_helpers
from app.core.pattern_engine.patterns.channels import find_channels


def test_detect_ascending_channel():
    helpers = get_pattern_helpers()
    base = np.linspace(10, 14, 40)
    lows = base - 0.5
    highs = base + 0.5
    closes = (highs + lows) / 2
    opens = closes
    volume = np.ones_like(highs) * 800

    patterns = find_channels(opens, highs, lows, closes, volume, helpers, strict=False)
    assert patterns, "Expected channel detection"
    assert any(p["pattern"] == "Ascending Channel" for p in patterns)
