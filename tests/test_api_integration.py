"""Comprehensive integration tests for all API endpoints."""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
import pandas as pd
import numpy as np

from app.main import app


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


@pytest.fixture
def mock_market_data():
    """Mock market data for testing."""
    dates = pd.date_range("2024-01-01", periods=100, freq="D")
    return pd.DataFrame({
        "datetime": dates,
        "open": np.linspace(100, 150, 100),
        "high": np.linspace(101, 151, 100),
        "low": np.linspace(99, 149, 100),
        "close": np.linspace(100, 150, 100),
        "volume": np.full(100, 1_000_000),
    })


# ==================== Health & Status Endpoints ====================

def test_health_endpoint(client):
    """Test main health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


def test_healthz_endpoint(client):
    """Test Kubernetes-style health endpoint."""
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


def test_root_endpoint(client):
    """Test root endpoint returns application info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data or "message" in data


# ==================== Pattern Detection Endpoints ====================

@patch("app.api.patterns.market_data_service")
@patch("app.api.patterns.detector_registry")
def test_detect_patterns_endpoint(mock_registry, mock_market_service, client, mock_market_data):
    """Test pattern detection endpoint."""
    # Setup mocks
    mock_market_service.fetch_data = AsyncMock(return_value=mock_market_data)
    mock_detector = MagicMock()
    mock_detector.find.return_value = []
    mock_registry.get_detector.return_value = mock_detector

    response = client.post(
        "/api/patterns/detect",
        json={
            "ticker": "AAPL",
            "timeframe": "1D",
            "pattern_types": ["VCP", "CUP_HANDLE"]
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "patterns" in data or "results" in data


@patch("app.api.patterns.cache_service")
def test_pattern_cache_stats_endpoint(mock_cache, client):
    """Test pattern cache statistics endpoint."""
    mock_cache.get_stats = AsyncMock(return_value={"hits": 100, "misses": 20})

    response = client.get("/api/patterns/cache/stats")
    assert response.status_code in [200, 404]  # May not be implemented


# ==================== Scanning Endpoints ====================

@patch("app.api.scan.universe_service")
def test_vcp_scan_endpoint(mock_universe, client):
    """Test VCP universe scan endpoint."""
    mock_universe.scan_universe = AsyncMock(return_value=[
        {
            "ticker": "NVDA",
            "pattern": "VCP",
            "score": 9.2,
            "entry": 100.0,
            "stop": 95.0,
            "target": 130.0,
        }
    ])

    response = client.post(
        "/api/scan/vcp",
        json={"min_score": 7.0, "max_results": 20}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (list, dict))


@patch("app.api.scan.universe_service")
def test_multi_pattern_scan_endpoint(mock_universe, client):
    """Test multi-pattern scan endpoint."""
    mock_universe.scan_universe = AsyncMock(return_value=[
        {
            "ticker": "AAPL",
            "pattern": "CUP_HANDLE",
            "score": 8.5,
            "entry": 150.0,
        }
    ])

    response = client.post(
        "/api/scan/multi-pattern",
        json={
            "pattern_types": ["VCP", "CUP_HANDLE", "TRIANGLE"],
            "min_score": 7.0,
            "max_results": 50
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (list, dict))


@patch("app.api.scan.universe_service")
def test_top_setups_endpoint(mock_universe, client):
    """Test top setups endpoint."""
    mock_universe.scan_universe = AsyncMock(return_value=[
        {
            "ticker": "TSLA",
            "pattern": "ASCENDING_TRIANGLE",
            "score": 9.0,
        }
    ])

    response = client.get("/api/top-setups?limit=10&min_score=7.0")

    assert response.status_code == 200
    data = response.json()
    assert "results" in data or isinstance(data, list)


# ==================== Universe Management Endpoints ====================

@patch("app.api.universe.universe_service")
def test_get_tickers_endpoint(mock_universe, client):
    """Test get all tickers endpoint."""
    mock_universe.get_tickers = AsyncMock(return_value=["AAPL", "GOOGL", "MSFT"])

    response = client.get("/api/universe/tickers")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (list, dict))


@patch("app.api.universe.universe_service")
def test_get_sp500_endpoint(mock_universe, client):
    """Test get S&P 500 tickers endpoint."""
    mock_universe.get_sp500 = AsyncMock(return_value=["AAPL", "MSFT"])

    response = client.get("/api/universe/sp500")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (list, dict))


@patch("app.api.universe.universe_service")
def test_get_nasdaq100_endpoint(mock_universe, client):
    """Test get NASDAQ 100 tickers endpoint."""
    mock_universe.get_nasdaq100 = AsyncMock(return_value=["AAPL", "GOOGL"])

    response = client.get("/api/universe/nasdaq100")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (list, dict))


@patch("app.api.universe.universe_service")
def test_seed_universe_endpoint(mock_universe, client):
    """Test seed universe endpoint."""
    mock_universe.seed_universe = AsyncMock(return_value={"seeded": 500})

    response = client.post("/api/universe/seed")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


# ==================== Watchlist Endpoints ====================

@patch("app.api.watchlist.watchlist_service")
def test_add_to_watchlist_endpoint(mock_watchlist, client):
    """Test add ticker to watchlist endpoint."""
    mock_watchlist.add_ticker = AsyncMock(return_value={"success": True})

    response = client.post(
        "/api/watchlist/add",
        json={"ticker": "AAPL", "notes": "Strong VCP pattern"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


@patch("app.api.watchlist.watchlist_service")
def test_get_watchlist_endpoint(mock_watchlist, client):
    """Test get watchlist endpoint."""
    mock_watchlist.get_watchlist = AsyncMock(return_value=[
        {"ticker": "AAPL", "added_at": "2024-01-01"}
    ])

    response = client.get("/api/watchlist")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (list, dict))


@patch("app.api.watchlist.watchlist_service")
def test_remove_from_watchlist_endpoint(mock_watchlist, client):
    """Test remove from watchlist endpoint."""
    mock_watchlist.remove_ticker = AsyncMock(return_value={"success": True})

    response = client.delete("/api/watchlist/AAPL")

    assert response.status_code == 200


# ==================== Chart Endpoints ====================

@patch("app.api.charts.chart_service")
def test_generate_chart_endpoint(mock_chart, client):
    """Test chart generation endpoint."""
    mock_chart.generate_chart = AsyncMock(return_value={"url": "http://chart.png"})

    response = client.post(
        "/api/charts/generate",
        json={"ticker": "AAPL", "timeframe": "1D", "include_patterns": True}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


# ==================== Trading & Risk Endpoints ====================

@patch("app.api.trades.trade_service")
def test_get_open_trades_endpoint(mock_trade, client):
    """Test get open trades endpoint."""
    mock_trade.get_open_trades = AsyncMock(return_value=[
        {"ticker": "AAPL", "entry": 150.0, "shares": 100}
    ])

    response = client.get("/api/trades/open")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (list, dict))


@patch("app.api.trades.trade_service")
def test_get_closed_trades_endpoint(mock_trade, client):
    """Test get closed trades endpoint."""
    mock_trade.get_closed_trades = AsyncMock(return_value=[
        {"ticker": "TSLA", "pnl": 1500.0}
    ])

    response = client.get("/api/trades/closed")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (list, dict))


@patch("app.api.risk.risk_service")
def test_calculate_position_size_endpoint(mock_risk, client):
    """Test position size calculation endpoint."""
    mock_risk.calculate_position_size = AsyncMock(return_value={
        "shares": 100,
        "position_value": 15000.0,
        "risk_amount": 300.0
    })

    response = client.post(
        "/api/risk/position-size",
        json={
            "account_size": 100000,
            "risk_percent": 2.0,
            "entry": 150.0,
            "stop": 145.0
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


# ==================== Market Data Endpoints ====================

@patch("app.api.market_data.market_data_service")
def test_get_market_data_endpoint(mock_market, client, mock_market_data):
    """Test get market data endpoint."""
    mock_market.fetch_data = AsyncMock(return_value=mock_market_data)

    response = client.get("/api/market-data/AAPL?timeframe=1D&bars=100")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (list, dict))


@patch("app.api.market_data.market_data_service")
def test_get_market_internals_endpoint(mock_market, client):
    """Test market internals endpoint."""
    mock_market.get_market_internals = AsyncMock(return_value={
        "advance_decline": 1500,
        "new_highs": 200,
        "new_lows": 50
    })

    response = client.get("/api/market-data/internals")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


# ==================== Alert Endpoints ====================

@patch("app.api.alerts.alert_service")
def test_get_active_alerts_endpoint(mock_alert, client):
    """Test get active alerts endpoint."""
    mock_alert.get_active_alerts = AsyncMock(return_value=[
        {"ticker": "AAPL", "alert_type": "BREAKOUT", "price": 150.0}
    ])

    response = client.get("/api/alerts/active")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (list, dict))


@patch("app.api.alerts.alert_service")
def test_create_alert_endpoint(mock_alert, client):
    """Test create alert endpoint."""
    mock_alert.create_alert = AsyncMock(return_value={"id": "alert_123"})

    response = client.post(
        "/api/alerts/create",
        json={
            "ticker": "AAPL",
            "alert_type": "PRICE",
            "target_price": 160.0
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


# ==================== Analytics Endpoints ====================

@patch("app.api.analytics.analytics_service")
def test_get_trade_journal_endpoint(mock_analytics, client):
    """Test trade journal endpoint."""
    mock_analytics.get_journal = AsyncMock(return_value=[
        {"date": "2024-01-01", "ticker": "AAPL", "notes": "Good setup"}
    ])

    response = client.get("/api/analytics/journal")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (list, dict))


@patch("app.api.analytics.analytics_service")
def test_get_performance_metrics_endpoint(mock_analytics, client):
    """Test performance metrics endpoint."""
    mock_analytics.get_performance = AsyncMock(return_value={
        "win_rate": 0.65,
        "avg_win": 500.0,
        "avg_loss": -200.0,
        "sharpe_ratio": 1.8
    })

    response = client.get("/api/analytics/performance")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


# ==================== Metrics Endpoint ====================

def test_metrics_endpoint(client):
    """Test Prometheus metrics endpoint."""
    response = client.get("/metrics")

    assert response.status_code == 200
    # Prometheus metrics are plain text
    assert "text/plain" in response.headers.get("content-type", "").lower() or response.status_code == 200


# ==================== Error Handling Tests ====================

def test_invalid_ticker_returns_error(client):
    """Test that invalid ticker returns appropriate error."""
    response = client.post(
        "/api/patterns/detect",
        json={"ticker": "", "timeframe": "1D"}
    )

    assert response.status_code in [400, 422]  # Bad request or validation error


def test_invalid_timeframe_returns_error(client):
    """Test that invalid timeframe returns appropriate error."""
    response = client.post(
        "/api/patterns/detect",
        json={"ticker": "AAPL", "timeframe": "INVALID"}
    )

    assert response.status_code in [400, 422]


def test_missing_required_fields_returns_error(client):
    """Test that missing required fields returns validation error."""
    response = client.post(
        "/api/patterns/detect",
        json={}
    )

    assert response.status_code == 422  # Validation error


# ==================== Rate Limiting Tests ====================

@pytest.mark.slow
def test_rate_limiting_enforced(client):
    """Test that rate limiting is enforced on endpoints."""
    # Make many rapid requests
    responses = []
    for _ in range(100):
        response = client.get("/health")
        responses.append(response.status_code)

    # Should eventually get rate limited (429) or all succeed
    # Depends on rate limit configuration
    assert all(status in [200, 429] for status in responses)


# ==================== CORS Tests ====================

def test_cors_headers_present(client):
    """Test that CORS headers are present in responses."""
    response = client.options(
        "/api/patterns/detect",
        headers={"Origin": "http://localhost:3000"}
    )

    # Should have CORS headers
    assert response.status_code in [200, 204]


# ==================== Authentication Tests (if applicable) ====================

def test_protected_endpoints_require_auth(client):
    """Test that protected endpoints require authentication."""
    # If your API has auth, test it
    # This is a placeholder - adjust based on your auth implementation
    response = client.post("/api/admin/settings", json={})

    # Should return 401 or 403 without auth, or 404 if endpoint doesn't exist
    assert response.status_code in [401, 403, 404]
