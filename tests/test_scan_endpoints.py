"""Contract tests for scan alias + top setups endpoint."""
from fastapi import FastAPI
from fastapi.testclient import TestClient
import types

from app.api import universe as universe_mod
from app.api.universe import router as universe_router
import app.api.scan as scan_mod
from app.api.scan import router as scan_router


def _stub_universe_service(monkeypatch):
    """Replace universe service with a fast stub for tests."""

    class _DummyRedis:
        async def get(self, key):  # pragma: no cover - redis stub
            return None

    async def _get_redis():
        return _DummyRedis()

    async def _scan_universe(min_score=7.0, max_results=20, pattern_types=None):
        return [
            {
                "ticker": "NVDA",
                "pattern": "VCP",
                "score": 9.2,
                "entry": 100.0,
                "stop": 95.0,
                "target": 130.0,
                "risk_reward": 6.0,
                "current_price": 104.0,
                "source": "SP500",
            }
        ]

    dummy = types.SimpleNamespace(
        scan_universe=_scan_universe,
        cache=types.SimpleNamespace(_get_redis=_get_redis),
    )

    monkeypatch.setattr(universe_mod, "universe_service", dummy)
    monkeypatch.setattr(scan_mod, "universe_service", dummy)
    return dummy


def _build_test_client():
    app = FastAPI()
    app.include_router(universe_router)
    app.include_router(scan_router)
    return TestClient(app)


def test_scan_alias_matches_universe(monkeypatch):
    _stub_universe_service(monkeypatch)
    client = _build_test_client()
    payload = {"min_score": 7.5, "max_results": 5}

    res_universe = client.post("/api/universe/scan", json=payload)
    res_alias = client.post("/api/scan", json=payload)

    assert res_universe.status_code == 200
    assert res_alias.status_code == 200
    assert res_universe.json() == res_alias.json()


def test_top_setups_endpoint(monkeypatch):
    _stub_universe_service(monkeypatch)
    client = _build_test_client()

    res = client.get("/api/top-setups?limit=5&min_score=7.0")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert data["count"] == 1
    assert data["results"][0]["ticker"] == "NVDA"
    assert data["results"][0]["pattern"] == "VCP"
