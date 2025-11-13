import asyncio


import asyncio
import pytest

pytest.importorskip("httpx")
pytest.importorskip("redis")


class _RedisStub:
    @classmethod
    def from_url(cls, *_args, **_kwargs):
        return cls()

    # The helpers below mirror the subset of redis-py's API that ChartingService
    # touches during instantiation and rate-limit checks.
    def pipeline(self):  # pragma: no cover - helper for completeness
        class _Pipe:
            def __init__(self):
                self.count = 0

            def zremrangebyscore(self, *args, **kwargs):
                return self

            def zadd(self, *args, **kwargs):
                self.count += 1
                return self

            def zcard(self, *args, **kwargs):
                return self

            def expire(self, *args, **kwargs):
                return self

            async def execute(self):
                return (None, None, self.count, None)

        return _Pipe()

    async def get(self, *_args, **_kwargs):
        return "0"

    async def incr(self, *_args, **_kwargs):
        return 1

    async def expire(self, *_args, **_kwargs):
        return True


def _service(monkeypatch):
    import app.services.charting as charting_mod

    monkeypatch.setattr(charting_mod, "Redis", _RedisStub)
    return charting_mod.ChartingService()


def test_chart_payload_limits_overlays(monkeypatch):
    service = _service(monkeypatch)
    overlays = ["EMA21", "EMA50", "EMA200", "RSI", "MACD", "SMA50"]

    payload = service._build_chart_payload(
        ticker="nvda",
        timeframe="60m",
        entry=100,
        stop=95,
        target=120,
        overlays=overlays,
    )

    assert payload["symbol"] == "NASDAQ:NVDA"
    assert payload["interval"] == "60"
    assert payload["drawings"] and payload["drawings"][0]["name"] == "Long Position"
    # One slot is reserved for drawings, so studies never exceed MAX_PARAMETERS-1
    assert len(payload["studies"]) <= service.MAX_PARAMETERS - 1
    assert any(s.get("name") == "Volume" for s in payload["studies"])


def test_multi_timeframe_charts_collects_urls(monkeypatch):
    service = _service(monkeypatch)

    async def fake_generate_chart(*args, **kwargs):
        tf = kwargs.get("timeframe")
        return f"https://chart/{tf}"

    service.generate_chart = fake_generate_chart  # type: ignore

    charts = asyncio.run(
        service.generate_multi_timeframe_charts("AAPL", timeframes=["1day", "1week"])
    )
    assert charts == {"1day": "https://chart/1day", "1week": "https://chart/1week"}


def test_fallback_url_normalizes_timeframe(monkeypatch):
    service = _service(monkeypatch)
    url = service._get_fallback_url("spy", "1week")
    assert "symbol=NASDAQ:SPY" in url
    assert "interval=W" in url
