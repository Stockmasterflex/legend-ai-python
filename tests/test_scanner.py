import pytest

from app.core.pattern_engine.filter import PatternFilter
from app.core.pattern_engine.scanner import ScanConfig, UniverseScanner
from app.core.pattern_engine.scoring import PatternScorer
from app.services import market_data as market_data_module


class _DummyDetector:
    def detect_all_patterns(
        self, ohlcv_data, ticker="UNKNOWN", include_candlesticks=True
    ):
        high_confidence = ticker == "AAPL"
        base_conf = 0.82 if high_confidence else 0.35
        return [
            {
                "ticker": ticker,
                "pattern": "TestPattern",
                "confidence": base_conf,
                "entry": 10.0,
                "stop": 9.5,
                "target": 12.0,
                "height_pct": 0.12 if high_confidence else 0.4,
                "market_cap": 250_000_000_000 if high_confidence else 80_000_000,
                "trend_start_pct": 30 if high_confidence else 3,
                "hcr": 0.8 if high_confidence else 0.3,
                "current_price": 50 if high_confidence else 20,
                "metadata": {
                    "year_high": 60 if high_confidence else 40,
                    "year_low": 30 if high_confidence else 10,
                    "base_depth_pct": 0.15 if high_confidence else 0.4,
                    "trend_strength": base_conf,
                    "volume_trend": -0.6 if high_confidence else 0.2,
                    "throwback_pct": 0.05 if high_confidence else 0.2,
                    "breakout_gap_pct": 0.04 if high_confidence else 0.0,
                },
            }
        ]


async def _fake_time_series(*args, **kwargs):
    return {
        "c": [1.0, 1.1, 1.2],
        "o": [0.9, 1.0, 1.05],
        "h": [1.1, 1.2, 1.25],
        "l": [0.85, 0.95, 1.0],
        "v": [1000, 1100, 1050],
    }


@pytest.mark.asyncio
async def test_scan_ticker(monkeypatch):
    monkeypatch.setattr(
        market_data_module.market_data_service, "get_time_series", _fake_time_series
    )
    scanner = UniverseScanner(_DummyDetector(), PatternFilter(), PatternScorer())

    patterns = await scanner.scan_ticker("AAPL", "1day")
    assert patterns
    assert patterns[0]["ticker"] == "AAPL"


@pytest.mark.asyncio
async def test_scan_universe_applies_scoring_and_filter(monkeypatch):
    monkeypatch.setattr(
        market_data_module.market_data_service, "get_time_series", _fake_time_series
    )
    scanner = UniverseScanner(_DummyDetector(), PatternFilter(), PatternScorer())

    config = ScanConfig(
        universe=["AAPL", "XYZ"],
        interval="1day",
        max_concurrent=2,
        min_score=6.0,
        apply_filters=True,
        apply_scoring=True,
    )

    payload = await scanner.scan_universe(config)

    assert payload["universe_size"] == 2
    assert payload["meta"]["result_count"] == len(payload["results"])
    assert payload["results"][0]["ticker"] == "AAPL"
    assert payload["results"][0]["rank"] == 1
    # Lower quality pattern should be filtered out by min_score
    assert all(res["ticker"] != "XYZ" for res in payload["results"])
