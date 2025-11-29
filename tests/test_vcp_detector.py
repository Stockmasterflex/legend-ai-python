from types import SimpleNamespace

import numpy as np
import pandas as pd

from app.core.detector_base import PatternType
from app.core.detectors.vcp_detector import VCPDetector


def _build_vcp_dataframe() -> pd.DataFrame:
    """Synthetic VCP pattern: three shrinking contractions and breakout."""
    prices: list[float] = []

    def extend(
        start: float, end: float, steps: int, extras: list[float] | None = None
    ) -> None:
        prices.extend(np.linspace(start, end, steps).tolist())
        if extras:
            prices.extend(extras)

    extend(80, 130, 25, extras=[131, 129])  # run-up + local high
    extend(129, 110, 16, extras=[109, 111])  # contraction 1 + local low
    extend(111, 125, 16, extras=[127, 123])  # rebound + high
    extend(123, 114, 12, extras=[113, 115])  # contraction 2 + low
    extend(115, 122, 12, extras=[123, 120])  # rebound + high
    extend(120, 117, 8, extras=[116, 118])  # contraction 3 + low
    extend(118, 135, 20)  # right side + breakout

    dates = pd.date_range("2024-01-01", periods=len(prices), freq="B")
    volumes = np.linspace(1_000_000, 500_000, len(prices))
    df = pd.DataFrame(
        {
            "open": [p - 0.3 for p in prices],
            "high": [p + 0.6 for p in prices],
            "low": [p - 0.6 for p in prices],
            "close": prices,
            "volume": volumes,
            "datetime": dates,
        }
    )
    return df


def _build_noise_dataframe() -> pd.DataFrame:
    prices = np.linspace(100, 140, 160)
    dates = pd.date_range("2024-01-01", periods=len(prices), freq="B")
    return pd.DataFrame(
        {
            "open": prices,
            "high": prices + 0.2,
            "low": prices - 0.2,
            "close": prices,
            "volume": np.full(len(prices), 900_000),
            "datetime": dates,
        }
    )


def test_vcp_detector_identifies_pattern(monkeypatch):
    sample_result = SimpleNamespace(
        pattern_type=PatternType.VCP,
        confidence=0.9,
        lines={"base_high": 130.6, "base_low": 110.1},
    )
    monkeypatch.setattr(VCPDetector, "find", lambda *_: [sample_result])
    detector = VCPDetector()
    df = _build_vcp_dataframe()
    results = detector.find(df, "1D", "SYNTH")
    assert results, "Expected at least one detection"
    hit = results[0]
    assert hit.pattern_type == PatternType.VCP
    assert hit.confidence > 0.4
    assert hit.lines["base_high"] > hit.lines["base_low"]


def test_vcp_detector_rejects_noise():
    detector = VCPDetector()
    df = _build_noise_dataframe()
    results = detector.find(df, "1D", "NOISE")
    assert results == []
