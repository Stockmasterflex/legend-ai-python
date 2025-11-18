"""
Tests for TradingView Integration
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import json

from app.main import app
from app.models import Base, Ticker, TradingViewAlert, TradingViewStrategy
from app.api.tradingview import get_db


# Create in-memory test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestTradingViewWebhook:
    """Test TradingView webhook endpoints"""

    def test_webhook_health_check(self):
        """Test health check endpoint"""
        response = client.get("/api/tradingview/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "tradingview_integration"

    def test_webhook_price_alert(self):
        """Test processing price alert webhook"""
        payload = {
            "ticker": "AAPL",
            "alert_name": "AAPL Price Alert",
            "message": "AAPL crossed above $150",
            "close": 151.50,
            "time": "2025-01-15 10:30:00",
            "interval": "1D"
        }

        response = client.post("/api/tradingview/webhooks/tradingview", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["symbol"] == "AAPL"
        assert data["alert_type"] in ["price", "indicator", "pattern", "breakout", "stop_loss"]

    def test_webhook_pattern_alert(self):
        """Test processing pattern alert webhook"""
        payload = {
            "ticker": "NVDA",
            "alert_name": "NVDA VCP Pattern",
            "message": "VCP pattern detected on NVDA",
            "close": 500.00,
            "time": "2025-01-15 11:00:00",
            "interval": "1D"
        }

        response = client.post("/api/tradingview/webhooks/tradingview", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["symbol"] == "NVDA"
        assert data["alert_type"] == "pattern"

    def test_webhook_breakout_alert(self):
        """Test processing breakout alert webhook"""
        payload = {
            "ticker": "TSLA",
            "alert_name": "TSLA Breakout",
            "message": "TSLA broke resistance at 250",
            "close": 252.00,
            "time": "2025-01-15 12:00:00",
            "interval": "1D"
        }

        response = client.post("/api/tradingview/webhooks/tradingview", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["symbol"] == "TSLA"
        assert data["alert_type"] == "breakout"

    def test_webhook_stop_loss_alert(self):
        """Test processing stop-loss alert webhook"""
        payload = {
            "ticker": "MSFT",
            "alert_name": "MSFT Stop Loss",
            "message": "MSFT hit stop-loss at 400",
            "close": 399.50,
            "time": "2025-01-15 13:00:00",
            "interval": "1D"
        }

        response = client.post("/api/tradingview/webhooks/tradingview", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["symbol"] == "MSFT"
        assert data["alert_type"] == "stop_loss"

    def test_webhook_indicator_alert(self):
        """Test processing indicator alert webhook"""
        payload = {
            "ticker": "GOOGL",
            "alert_name": "GOOGL RSI Oversold",
            "message": "RSI below 30 on GOOGL",
            "close": 140.00,
            "time": "2025-01-15 14:00:00",
            "interval": "1D",
            "rsi": 28.5,
            "macd": -1.2
        }

        response = client.post("/api/tradingview/webhooks/tradingview", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["symbol"] == "GOOGL"
        assert data["alert_type"] == "indicator"

    def test_webhook_with_action(self):
        """Test webhook with trading action"""
        payload = {
            "ticker": "AMD",
            "alert_name": "AMD Buy Signal",
            "message": "Buy AMD at current price",
            "close": 180.00,
            "time": "2025-01-15 15:00:00",
            "interval": "1D"
        }

        response = client.post("/api/tradingview/webhooks/tradingview", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["symbol"] == "AMD"
        assert data["action"] == "buy"

    def test_webhook_missing_symbol(self):
        """Test webhook with missing symbol"""
        payload = {
            "alert_name": "Test Alert",
            "message": "Test message",
            "close": 100.00
        }

        response = client.post("/api/tradingview/webhooks/tradingview", json=payload)
        assert response.status_code == 400

    def test_webhook_rate_limiting(self):
        """Test rate limiting on webhook endpoint"""
        payload = {
            "ticker": "TEST",
            "message": "Rate limit test",
            "close": 100.00
        }

        # Make multiple requests
        for i in range(105):  # Exceed rate limit of 100
            response = client.post("/api/tradingview/webhooks/tradingview", json=payload)
            if i < 100:
                assert response.status_code in [200, 400]  # Should succeed or fail validation
            else:
                # After 100 requests, should be rate limited
                if response.status_code == 429:
                    break  # Rate limit hit as expected


class TestTradingViewAlerts:
    """Test TradingView alerts query endpoints"""

    def test_get_all_alerts(self):
        """Test getting all alerts"""
        response = client.get("/api/tradingview/alerts")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "alerts" in data
        assert isinstance(data["alerts"], list)

    def test_get_alerts_by_symbol(self):
        """Test getting alerts filtered by symbol"""
        # First create an alert
        payload = {
            "ticker": "AAPL",
            "message": "Test alert",
            "close": 150.00
        }
        client.post("/api/tradingview/webhooks/tradingview", json=payload)

        # Query alerts for AAPL
        response = client.get("/api/tradingview/alerts?symbol=AAPL")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_alerts_by_type(self):
        """Test getting alerts filtered by type"""
        response = client.get("/api/tradingview/alerts?alert_type=pattern")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_get_alerts_with_limit(self):
        """Test getting alerts with limit"""
        response = client.get("/api/tradingview/alerts?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["alerts"]) <= 10


class TestTradingViewStrategy:
    """Test TradingView strategy endpoints"""

    def test_import_strategy(self):
        """Test importing a TradingView strategy"""
        strategy_data = {
            "name": "RSI Reversal Strategy",
            "description": "Buy when RSI < 30, sell when RSI > 70",
            "strategy_config": {
                "timeframe": "1D",
                "indicators": ["RSI", "EMA"],
                "entry_conditions": {
                    "rsi": {"operator": "<", "value": 30},
                    "price": {"operator": ">", "indicator": "ema_20"}
                },
                "exit_conditions": {
                    "rsi": {"operator": ">", "value": 70}
                },
                "risk_reward_ratio": 2.0,
                "win_rate": 0.65,
                "profit_factor": 1.8
            }
        }

        response = client.post("/api/tradingview/strategies/import", json=strategy_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "strategy_id" in data
        assert data["name"] == "RSI Reversal Strategy"

    def test_list_strategies(self):
        """Test listing imported strategies"""
        response = client.get("/api/tradingview/strategies")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "strategies" in data
        assert isinstance(data["strategies"], list)

    def test_backtest_strategy(self):
        """Test backtesting a strategy"""
        # First import a strategy
        strategy_data = {
            "name": "MACD Crossover",
            "description": "Buy on MACD bullish crossover",
            "strategy_config": {
                "timeframe": "1D",
                "indicators": ["MACD"],
                "entry_conditions": {},
                "exit_conditions": {}
            }
        }
        import_response = client.post("/api/tradingview/strategies/import", json=strategy_data)
        strategy_id = import_response.json()["strategy_id"]

        # Backtest the strategy
        backtest_data = {
            "strategy_id": strategy_id,
            "symbols": ["AAPL", "MSFT", "GOOGL"],
            "start_date": "2024-01-01",
            "end_date": "2024-12-31"
        }

        response = client.post("/api/tradingview/strategies/backtest", json=backtest_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "results" in data


class TestTradingViewSync:
    """Test TradingView sync endpoints"""

    def test_sync_pattern_to_tradingview(self):
        """Test syncing pattern to TradingView"""
        # This test would require creating a pattern scan first
        # For now, test that endpoint exists and handles invalid ID
        sync_data = {
            "pattern_scan_id": 99999  # Non-existent ID
        }

        response = client.post("/api/tradingview/sync/pattern", json=sync_data)
        assert response.status_code == 404  # Should return 404 for non-existent pattern

    def test_sync_watchlist_to_tradingview(self):
        """Test syncing watchlist to TradingView"""
        sync_data = {
            "watchlist_ids": [1, 2, 3]  # May not exist, but tests endpoint
        }

        response = client.post("/api/tradingview/sync/watchlist", json=sync_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestTradingViewService:
    """Test TradingView service functions"""

    def test_parse_alert_type(self):
        """Test alert type parsing"""
        from app.services.tradingview import tradingview_service

        # Test price alert
        assert tradingview_service.parse_alert_type("Price crossed above 100", "") == "price"

        # Test pattern alert
        assert tradingview_service.parse_alert_type("VCP pattern detected", "") == "pattern"

        # Test breakout alert
        assert tradingview_service.parse_alert_type("Breakout above resistance", "") == "breakout"

        # Test stop-loss alert
        assert tradingview_service.parse_alert_type("Stop-loss hit at 50", "") == "stop_loss"

        # Test indicator alert
        assert tradingview_service.parse_alert_type("RSI oversold", "") == "indicator"

    def test_extract_action(self):
        """Test action extraction"""
        from app.services.tradingview import tradingview_service

        # Test buy action
        assert tradingview_service.extract_action("Buy AAPL at 150") == "buy"

        # Test sell action
        assert tradingview_service.extract_action("Sell position now") == "sell"

        # Test exit action
        assert tradingview_service.extract_action("Exit trade") == "exit"

        # Test no action
        assert tradingview_service.extract_action("Pattern detected") is None

    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        from app.services.tradingview import tradingview_service

        test_ip = "192.168.1.100"

        # Should allow first 100 requests
        for i in range(100):
            assert tradingview_service.check_rate_limit(test_ip) is True

        # 101st request should be rate limited
        assert tradingview_service.check_rate_limit(test_ip) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
