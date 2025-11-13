import asyncio
import math
import pytest

pytest.importorskip("fastapi")


class _StubCache:
    def __init__(self):
        self.store = {}

    async def get(self, key):
        return self.store.get(key)

    async def set(self, key, value, ttl=0):  # pragma: no cover - ttl unused
        self.store[key] = value
        return True


class _StubMarketData:
    def __init__(self):
        base_series = [100 + i for i in range(260)]
        self.spy_series = {
            "c": base_series,
        }
        self.other_series = {
            "c": [50 + i for i in range(260)],
            "h": [55 + i for i in range(260)],
            "l": [45 + i for i in range(260)],
        }

    async def get_time_series(self, ticker, interval="1day", outputsize=200, timeout=None):
        return self.spy_series if ticker == "SPY" else self.other_series

    async def get_quote(self, ticker, timeout=5.0):
        return {"last_price": 15.2}

    async def get_usage_stats(self):
        return {"status": "ok", "remaining": 100}


def test_market_internals_caches_results(monkeypatch):
    import app.api.market as market_mod
    from app.services import universe as universe_mod

    cache = _StubCache()
    monkeypatch.setattr(market_mod, "get_cache_service", lambda: cache)
    monkeypatch.setattr(market_mod, "market_data_service", _StubMarketData())

    class _StubUniverse:
        def get_sp500(self):
            return ["AAPL", "MSFT", "NVDA"]

    monkeypatch.setattr(universe_mod, "universe_service", _StubUniverse())

    async def fake_breadth(_tickers):
        return {"advances": 2, "declines": 1}

    monkeypatch.setattr(market_mod, "_calculate_market_breadth", fake_breadth)

    async def fake_vix():
        return {"vix_level": 15.2, "volatility_status": "Low"}

    monkeypatch.setattr(market_mod, "_fetch_vix_level", fake_vix)

    first = asyncio.run(market_mod.get_market_internals())
    assert first["success"] is True
    assert first["cached"] is False
    assert math.isclose(first["data"]["spy_price"], 100 + 259)

    second = asyncio.run(market_mod.get_market_internals())
    assert second["cached"] is True
    assert second["data"]["spy_price"] == first["data"]["spy_price"]


def test_calculate_market_breadth_counts(monkeypatch):
    import app.api.market as market_mod

    up = {"c": [10, 11, 12, 13, 14, 15], "h": [15] * 6, "l": [9] * 6}
    down = {"c": [20, 19, 18, 17, 16, 15], "h": [22] * 6, "l": [14] * 6}

    class _BreadthMarketData:
        async def get_time_series(self, ticker, *_args, **_kwargs):
            return up if ticker == "UP" else down

    monkeypatch.setattr(market_mod, "market_data_service", _BreadthMarketData())

    result = asyncio.run(
        market_mod._calculate_market_breadth(["UP", "DOWN"], max_tickers=2)
    )
    assert result["advances"] == 1
    assert result["declines"] == 1
    # Only UP is above a rising EMA estimate
    assert result["pct_above_50ema"] == 50.0
