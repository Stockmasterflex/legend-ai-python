import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient
from fastapi import FastAPI


class _StubCache:
    def __init__(self):
        self.data = {}

    async def get(self, key):
        return self.data.get(key)

    async def set(self, key, value, ttl=0):
        self.data[key] = value
        return True


def _make_series(n=250):
    # Simple increasing series
    closes = [100 + i * 0.5 for i in range(n)]
    opens = [c - 0.2 for c in closes]
    highs = [c + 0.5 for c in closes]
    lows = [c - 0.5 for c in closes]
    vols = [100000 + i for i in range(n)]
    times = [f"2024-01-{(i%28)+1:02d}" for i in range(n)]
    return {"c": closes, "o": opens, "h": highs, "l": lows, "v": vols, "t": times}


def test_analyze_contract(monkeypatch):
    # Stub settings before importing route that pulls market_data_service
    import types
    import app.config as cfg
    class _StubSettings:
        app_name = "Legend AI"
        debug = False
        secret_key = "dev"
        telegram_bot_token = "dev-token"
        telegram_chat_id = None
        telegram_webhook_url = None
        openrouter_api_key = "dev"
        openai_api_key = None
        chartimg_api_key = "dev"
        twelvedata_api_key = "dev"
        finnhub_api_key = None
        alpha_vantage_api_key = None
        twelvedata_daily_limit = 800
        finnhub_daily_limit = 60
        alpha_vantage_daily_limit = 500
        chartimg_daily_limit = 500
        redis_url = "redis://localhost:6379"
        database_url = None
        google_sheets_id = None
        sendgrid_api_key = None
        alert_email = None
        algorithm = "HS256"
        access_token_expire_minutes = 60
        @property
        def auto_webhook_url(self):
            return "http://localhost:8000"

    monkeypatch.setattr(cfg, "get_settings", lambda: _StubSettings())

    # Now import the router so it uses stubbed settings via market_data_service
    from app.api.analyze import router as analyze_router
    # Monkeypatch market data and cache
    from app.services import market_data as md
    series = _make_series(260)

    async def fake_get_time_series(ticker: str, interval: str = "1day", outputsize: int = 400):
        return series

    monkeypatch.setattr(md.market_data_service, "get_time_series", fake_get_time_series)

    # Patch cache in route module to avoid Redis
    import app.api.analyze as analyze_mod

    def fake_get_cache_service():
        return _StubCache()

    monkeypatch.setattr(analyze_mod, "get_cache_service", fake_get_cache_service)

    # Patch universe store cache/memory to avoid redis/file IO
    import app.services.universe_store as uni_mod
    uni_mod.universe_store.cache = _StubCache()
    uni_mod.universe_store._memory = {
        "TSLA": {
            "symbol": "TSLA",
            "name": "Tesla Inc.",
            "sector": "Consumer Discretionary",
            "industry": "Automobile Manufacturers",
            "universe": "SP500",
        }
    }

    # Stub Chart-IMG rendering to avoid network and assert presence
    async def fake_build_analyze_chart(*args, **kwargs):
        return "https://example.com/chart.png"

    monkeypatch.setattr(analyze_mod, "build_analyze_chart", fake_build_analyze_chart)

    # Mount only the analyze route to avoid heavy app imports / env
    test_app = FastAPI()
    test_app.include_router(analyze_router)
    client = TestClient(test_app)
    res = client.get("/api/analyze", params={"ticker": "TSLA", "tf": "daily"})
    assert res.status_code == 200
    data = res.json()

    # Top-level keys
    assert set(["ticker", "timeframe", "ohlcv", "indicators", "patterns", "plan"]).issubset(data.keys())
    assert data["ticker"] == "TSLA"
    assert data["timeframe"] == "daily"

    # OHLCV shape
    assert isinstance(data["ohlcv"], list) and len(data["ohlcv"]) > 50
    row = data["ohlcv"][-1]
    for k in ["t", "o", "h", "l", "c", "v"]:
        assert k in row

    # Indicators per contract
    ind = data["indicators"]
    assert set(["ema21", "sma50", "rsi14", "rsi_divergences"]).issubset(ind.keys())

    # Patterns
    pats = data["patterns"]
    assert "minervini" in pats and "weinstein" in pats and "vcp" in pats
    assert isinstance(pats["minervini"].get("passed"), bool)
    assert isinstance(pats["weinstein"].get("stage"), int)

    # Plan
    plan = data["plan"]
    for k in ["entry", "stop", "target", "risk_r", "atr14", "atr_percent"]:
        assert k in plan

    # RS metrics
    rs = data.get("relative_strength")
    assert isinstance(rs, dict)
    assert "series" in rs

    # Intel surface
    intel = data.get("intel")
    assert isinstance(intel, dict)
    assert "rule_failures" in intel

    # Universe metadata
    universe_meta = data.get("universe")
    assert isinstance(universe_meta, dict)
    assert universe_meta.get("symbol") == "TSLA"

    # Chart URL present when Chart-IMG is stubbed
    assert data.get("chart_url") == "https://example.com/chart.png"
    # Key should always exist in contract (value may be None)
    assert "chart_url" in data
