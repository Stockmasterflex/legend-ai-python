import numpy as np

from app.core.pattern_engine.helpers import get_pattern_helpers
from app.core.pattern_engine.patterns.broadening import \
    find_broadening_formations


def test_detect_broadening_pattern():
    helpers = get_pattern_helpers()
    # Craft expanding highs and lows
    highs = np.array([10 + i * 0.1 + (i % 2) for i in range(40)], dtype=float)
    lows = np.array([9 - i * 0.05 - (i % 2) * 0.1 for i in range(40)], dtype=float)
    closes = (highs + lows) / 2
    opens = closes
    volume = np.ones_like(highs) * 700

    patterns = find_broadening_formations(
        opens, highs, lows, closes, volume, helpers, strict=False
    )
    assert patterns, "Expected broadening detection"
    assert any("Broadening" in p["pattern"] for p in patterns)
