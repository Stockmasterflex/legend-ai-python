import pytest

from app.services.market_data import market_data_service


@pytest.mark.asyncio
async def test_yahoo_request_includes_user_agent(monkeypatch):
    """Yahoo fallback must send a browser user agent to avoid 429 errors."""
    captured = {}

    async def fake_get(url, params=None, headers=None):
        captured["headers"] = headers or {}

        class FakeResponse:
            status_code = 200

            def json(self_inner):
                quote_values = [100.0 + float(i) for i in range(60)]
                return {
                    "chart": {
                        "result": [
                            {
                                "indicators": {
                                    "quote": [
                                        {
                                            "close": quote_values,
                                            "open": [v - 0.5 for v in quote_values],
                                            "high": [v + 0.5 for v in quote_values],
                                            "low": [v - 1.0 for v in quote_values],
                                            "volume": [1000 + i for i in range(60)],
                                        }
                                    ]
                                },
                                "timestamp": [1700000000 + i * 60 for i in range(60)],
                            }
                        ]
                    }
                }

        return FakeResponse()

    monkeypatch.setattr(market_data_service.client, "get", fake_get)
    result = await market_data_service._get_from_yahoo("AAPL", "1day")

    assert isinstance(result, dict)
    assert len(result.get("c", [])) >= 50
    assert "User-Agent" in captured["headers"]
    assert captured["headers"]["User-Agent"].startswith("Mozilla")
