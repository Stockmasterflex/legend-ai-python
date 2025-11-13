import pytest

pytest.importorskip("fastapi")
from fastapi import FastAPI
from fastapi.testclient import TestClient


class _StubUniverseService:
    async def get_full_universe(self):
        return [
            {"ticker": "AAPL", "source": "SP500"},
            {"ticker": "MSFT", "source": "NASDAQ100"},
        ]

    async def scan_universe(self, min_score=7.0, max_results=20, pattern_types=None):
        return [
            {
                "ticker": "AAPL",
                "pattern": "VCP",
                "score": 8.1,
                "entry": 100.0,
                "stop": 95.0,
                "target": 120.0,
                "risk_reward": 5.0,
                "current_price": 102.0,
                "source": "SP500",
            }
        ]

    async def get_sp500_tickers(self):
        return ["AAPL"]

    async def get_nasdaq100_tickers(self):
        return ["MSFT"]


def _client(monkeypatch) -> TestClient:
    import app.api.universe as universe_mod

    monkeypatch.setattr(universe_mod, "universe_service", _StubUniverseService())
    test_app = FastAPI()
    test_app.include_router(universe_mod.router)
    return TestClient(test_app)


def test_universe_tickers(monkeypatch):
    client = _client(monkeypatch)
    res = client.get("/api/universe/tickers")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 2
    assert data["sources"] == {"SP500": 1, "NASDAQ100": 1}


def test_universe_scan_endpoint(monkeypatch):
    client = _client(monkeypatch)
    res = client.post("/api/universe/scan", json={"min_score": 7.5, "max_results": 5})
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["total_found"] == 1
    assert data["results"][0]["ticker"] == "AAPL"
