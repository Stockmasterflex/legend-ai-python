import pytest

from app.services.market_data import market_data_service
from app.services.scanner import ScannerService
from app.services.universe_store import universe_store


async def _fake_spy_series(*args, **kwargs):
    return {
        "c": [1.0, 1.1, 1.2],
        "o": [0.9, 1.0, 1.1],
        "h": [1.1, 1.2, 1.3],
        "l": [0.8, 0.9, 1.0],
        "v": [1000, 1100, 1050],
        "cached": False,
    }


def _fake_detection(symbol: str, metadata: dict) -> dict:
    return {
        "symbol": symbol,
        "timeframe": "1D",
        "pattern": "VCP",
        "legend_score": 90 if symbol.startswith("A") else 70,
        "grade": "A",
        "reasons": ["stubbed"],
        "signals": {
            "vol_contractions": 3,
            "max_pullback_pct": 8.5,
            "base_days": 18,
            "pivot": 120.5,
            "rs_rank": 82,
            "ma_dist": {"ema21": 1.2, "sma50": 2.4, "sma200": 5.1},
        },
        "rule_failures": [],
        "atr_plan": {"atr": 1.1, "stop": 118.8, "risk_unit": 1.5},
        "chart_url": None,
        "sources": {"price": None, "spy": None, "sector": metadata.get("sector")},
    }


@pytest.mark.asyncio
async def test_scanner_service_preserves_missing_data(monkeypatch):
    async def fake_get_all():
        return {
            "AAA": {"symbol": "AAA", "sector": "Health Care"},
            "MISS": {"symbol": "MISS", "sector": "Health Care"},
        }
    monkeypatch.setattr(universe_store, "get_all", fake_get_all)
    monkeypatch.setattr(market_data_service, "get_time_series", _fake_spy_series)

    async def stub_scan_symbol(self, symbol, metadata, spy_closes, sem, missing_symbols, minervini_trend=False, vcp=False):
        if symbol == "MISS":
            missing_symbols.append(symbol)
            return None
        return _fake_detection(symbol, metadata)

    monkeypatch.setattr(ScannerService, "_scan_symbol", stub_scan_symbol)

    service = ScannerService(max_symbols=10)
    payload = await service.run_daily_vcp_scan(limit=2)

    assert payload["meta"]["result_count"] == 2
    assert payload["meta"]["total_hits"] == 1
    assert payload["results"][0]["symbol"] == "AAA"
    placeholder = payload["results"][1]
    assert placeholder["rule_failures"] == ["missing_ohlcv"]
    assert placeholder["signals"]["ma_dist"]["ema21"] is None


@pytest.mark.asyncio
async def test_scanner_service_filters_by_sector(monkeypatch):
    metadata = {
        "AAA": {"symbol": "AAA", "sector": "Health Care"},
        "BBB": {"symbol": "BBB", "sector": "Health Care"},
        "CCC": {"symbol": "CCC", "sector": "Technology"},
    }
    async def fake_get_all():
        return metadata
    monkeypatch.setattr(universe_store, "get_all", fake_get_all)
    monkeypatch.setattr(market_data_service, "get_time_series", _fake_spy_series)

    async def stub_scan_symbol(self, symbol, metadata, spy_closes, sem, missing_symbols, minervini_trend=False, vcp=False):
        return _fake_detection(symbol, metadata)

    monkeypatch.setattr(ScannerService, "_scan_symbol", stub_scan_symbol)

    service = ScannerService(max_symbols=10)
    payload = await service.run_daily_vcp_scan(limit=10, sector="health care")

    assert payload["universe_size"] == 2
    assert all(r["symbol"] in {"AAA", "BBB"} for r in payload["results"])
