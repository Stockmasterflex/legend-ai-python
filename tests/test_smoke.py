from fastapi.testclient import TestClient
import pytest

import app.main as main


class _StubCache:
    def __init__(self):
        self.store = {}

    async def get(self, key):
        return self.store.get(key)

    async def set(self, key, value, ttl=0):
        self.store[key] = value
        return True


def _make_series(n=260):
    closes = [100 + i * 0.4 for i in range(n)]
    opens = [c - 0.2 for c in closes]
    highs = [c + 0.5 for c in closes]
    lows = [c - 0.5 for c in closes]
    vols = [1_000_000 + i * 10 for i in range(n)]
    times = [f"2024-01-{(i % 28) + 1:02d}" for i in range(n)]
    return {"c": closes, "o": opens, "h": highs, "l": lows, "v": vols, "t": times}


@pytest.fixture
def client():
    # Keep universe store in-memory during tests
    import app.services.universe_store as uni_mod

    uni_mod.universe_store.cache = _StubCache()
    uni_mod.universe_store._memory = {
        "AAPL": {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "sector": "Information Technology",
            "industry": "Technology Hardware, Storage & Peripherals",
            "universe": "SP500",
        }
    }

    with TestClient(main.app) as test_client:
        yield test_client


def test_version_endpoints(client):
    resp = client.get("/version")
    assert resp.status_code == 200
    payload = resp.json()
    assert "build_sha" in payload

    resp_api = client.get("/api/version")
    assert resp_api.status_code == 200
    payload_api = resp_api.json()
    assert "build_sha" in payload_api and "branch" in payload_api


def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["status"] == "healthy"
    assert "redis" in payload and "universe" in payload


def test_analyze_endpoint_smoke(monkeypatch, client):
    # Stub cache inside analyzer to avoid Redis dependencies
    import app.api.analyze as analyze_mod

    series = _make_series()

    async def fake_get_time_series(ticker: str, interval: str = "1day", outputsize: int = 400):
        return series

    monkeypatch.setattr(analyze_mod.market_data_service, "get_time_series", fake_get_time_series)
    monkeypatch.setattr(analyze_mod, "get_cache_service", lambda: _StubCache())

    async def fake_chart(*args, **kwargs):
        return "https://chart.test/url"

    monkeypatch.setattr(analyze_mod, "build_analyze_chart", fake_chart)

    resp = client.get("/api/analyze", params={"ticker": "AAPL", "tf": "daily"})
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["ticker"] == "AAPL"
    assert "relative_strength" in payload
    assert "plan" in payload and "atr14" in payload["plan"]
