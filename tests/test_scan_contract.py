from types import SimpleNamespace
from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_scan_disabled_returns_empty(monkeypatch):
    from app.api import scan as scan_mod

    monkeypatch.setattr(scan_mod, "get_legend_flags", lambda: SimpleNamespace(enable_scanner=False))

    app = FastAPI()
    app.include_router(scan_mod.router)
    client = TestClient(app)

    res = client.get("/api/scan")
    assert res.status_code == 200
    payload = res.json()
    assert payload["results"] == []
    assert payload["universe_size"] == 0
    assert payload["meta"]["reason"] == "scanner_disabled"


def test_scan_enabled_contract(monkeypatch):
    from app.api import scan as scan_mod

    monkeypatch.setattr(scan_mod, "get_legend_flags", lambda: SimpleNamespace(enable_scanner=True))

    sample_payload = {
        "as_of": "2025-11-08T00:00:00Z",
        "universe_size": 5,
        "results": [
            {
                "symbol": "AAPL",
                "timeframe": "1D",
                "pattern": "VCP",
                "legend_score": 90,
                "grade": "A",
                "reasons": ["trend ok"],
                "signals": {
                    "vol_contractions": 4,
                    "max_pullback_pct": 12.5,
                    "base_days": 25,
                    "pivot": 230.5,
                    "rs_rank": 88,
                    "ma_dist": {"ema21": 1.5, "sma50": 3.2, "sma200": 12.4},
                },
                "rule_failures": [],
                "atr_plan": {"atr": 3.1, "stop": 224.0, "risk_unit": 1.5},
                "chart_url": None,
            }
        ],
        "meta": {"build_sha": "abc123", "duration_ms": 12.3, "result_count": 1, "total_hits": 1},
    }

    async def fake_scan(*_, **__):
        return sample_payload

    monkeypatch.setattr(scan_mod.scan_service, "run_daily_vcp_scan", fake_scan)

    app = FastAPI()
    app.include_router(scan_mod.router)
    client = TestClient(app)
    res = client.get("/api/scan", params={"limit": 10})
    assert res.status_code == 200
    data = res.json()
    assert data["results"]
    hit = data["results"][0]
    assert hit["symbol"] == "AAPL"
    assert "legend_score" in hit
    assert isinstance(hit["signals"]["ma_dist"], dict)
    assert "meta" in data and "build_sha" in data["meta"]
