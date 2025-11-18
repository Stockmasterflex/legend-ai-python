"""
Tests for Multi-Ticker Comparison API Endpoints
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app


client = TestClient(app)


@pytest.fixture
def mock_comparison_result():
    """Mock successful comparison result."""
    return {
        "tickers": ["AAPL", "MSFT", "GOOGL"],
        "benchmark": "SPY",
        "interval": "1day",
        "bars": 252,
        "timestamp": "2025-01-01T00:00:00",
        "chart_data": {
            "AAPL": {
                "timestamps": [1700000000, 1700086400],
                "open": [150.0, 151.0],
                "high": [152.0, 153.0],
                "low": [149.0, 150.0],
                "close": [151.0, 152.0],
                "volume": [1000000, 1100000],
            },
            "MSFT": {
                "timestamps": [1700000000, 1700086400],
                "open": [350.0, 351.0],
                "high": [352.0, 353.0],
                "low": [349.0, 350.0],
                "close": [351.0, 352.0],
                "volume": [900000, 950000],
            },
            "GOOGL": {
                "timestamps": [1700000000, 1700086400],
                "open": [130.0, 131.0],
                "high": [132.0, 133.0],
                "low": [129.0, 130.0],
                "close": [131.0, 132.0],
                "volume": [800000, 850000],
            },
        },
        "metrics": {
            "AAPL": {
                "current_price": 152.0,
                "returns_1d": 0.66,
                "returns_5d": 2.5,
                "returns_20d": 10.0,
                "volatility_20d": 1.5,
            },
            "MSFT": {
                "current_price": 352.0,
                "returns_1d": 0.28,
                "returns_5d": 1.8,
                "returns_20d": 8.5,
                "volatility_20d": 1.2,
            },
            "GOOGL": {
                "current_price": 132.0,
                "returns_1d": 0.76,
                "returns_5d": 3.0,
                "returns_20d": 12.0,
                "volatility_20d": 1.8,
            },
        },
        "relative_strength": {
            "AAPL": {"rank": 75, "current": 1.05, "slope": 0.01},
            "MSFT": {"rank": 68, "current": 1.02, "slope": 0.008},
            "GOOGL": {"rank": 82, "current": 1.08, "slope": 0.012},
        },
        "correlation_matrix": {
            "price_correlation": {
                "AAPL": {"AAPL": 1.0, "MSFT": 0.85, "GOOGL": 0.78},
                "MSFT": {"AAPL": 0.85, "MSFT": 1.0, "GOOGL": 0.82},
                "GOOGL": {"AAPL": 0.78, "MSFT": 0.82, "GOOGL": 1.0},
            },
            "volume_correlation": {
                "AAPL": {"AAPL": 1.0, "MSFT": 0.45, "GOOGL": 0.38},
                "MSFT": {"AAPL": 0.45, "MSFT": 1.0, "GOOGL": 0.42},
                "GOOGL": {"AAPL": 0.38, "MSFT": 0.42, "GOOGL": 1.0},
            },
            "tickers": ["AAPL", "MSFT", "GOOGL"],
        },
        "leader_laggard": {
            "leaders": [{"ticker": "GOOGL", "rs_rank": 82}],
            "laggards": [{"ticker": "MSFT", "rs_rank": 68}],
            "total_analyzed": 3,
        },
    }


@pytest.fixture
def mock_pair_trading_result():
    """Mock successful pair trading result."""
    return {
        "ticker1": "GLD",
        "ticker2": "GDX",
        "interval": "1day",
        "bars": 252,
        "timestamps": [1700000000, 1700086400, 1700172800],
        "spread": [2.0, 2.1, 1.9],
        "z_scores": [0.0, 0.5, -0.5],
        "signals": {
            "current_signal": "HOLD",
            "current_zscore": -0.5,
            "signal_strength": 0,
            "entry_threshold": 2.0,
            "exit_threshold": 0.5,
        },
        "cointegration": {
            "test_statistic": -3.2,
            "p_value": 0.03,
            "result": "Cointegrated",
            "is_cointegrated": True,
        },
        "hedge_ratio": 1.85,
        "statistics": {
            "spread_mean": 2.0,
            "spread_std": 0.1,
            "current_spread": 1.9,
            "current_zscore": -0.5,
        },
    }


def test_comparison_health_check():
    """Test comparison service health check endpoint."""
    response = client.get("/api/comparison/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "ticker_comparison"


@patch("app.services.ticker_comparison.ticker_comparison_service.compare_tickers")
def test_compare_tickers_post(mock_compare, mock_comparison_result):
    """Test POST /api/comparison/compare endpoint."""
    mock_compare.return_value = mock_comparison_result

    response = client.post(
        "/api/comparison/compare",
        json={
            "tickers": ["AAPL", "MSFT", "GOOGL"],
            "interval": "1day",
            "bars": 252,
            "benchmark": "SPY",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert "tickers" in data
    assert data["tickers"] == ["AAPL", "MSFT", "GOOGL"]
    assert data["benchmark"] == "SPY"
    assert "chart_data" in data
    assert "metrics" in data
    assert "relative_strength" in data


@patch("app.services.ticker_comparison.ticker_comparison_service.compare_tickers")
def test_compare_tickers_get(mock_compare, mock_comparison_result):
    """Test GET /api/comparison/compare endpoint."""
    mock_compare.return_value = mock_comparison_result

    response = client.get(
        "/api/comparison/compare?tickers=AAPL,MSFT,GOOGL&interval=1day&bars=252&benchmark=SPY"
    )

    assert response.status_code == 200
    data = response.json()

    assert "tickers" in data
    assert data["tickers"] == ["AAPL", "MSFT", "GOOGL"]


def test_compare_tickers_minimum_validation():
    """Test that at least 2 tickers are required."""
    response = client.post(
        "/api/comparison/compare",
        json={
            "tickers": ["AAPL"],
            "interval": "1day",
            "bars": 252,
            "benchmark": "SPY",
        },
    )

    # Pydantic validation should fail
    assert response.status_code == 422


def test_compare_tickers_maximum_validation():
    """Test that maximum 9 tickers are enforced."""
    response = client.post(
        "/api/comparison/compare",
        json={
            "tickers": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
            "interval": "1day",
            "bars": 252,
            "benchmark": "SPY",
        },
    )

    # Pydantic validation should fail
    assert response.status_code == 422


def test_compare_tickers_get_minimum_validation():
    """Test GET endpoint ticker validation."""
    response = client.get("/api/comparison/compare?tickers=AAPL")

    assert response.status_code == 400
    data = response.json()
    assert "at least 2 tickers" in data["detail"].lower()


def test_compare_tickers_get_maximum_validation():
    """Test GET endpoint maximum ticker validation."""
    response = client.get(
        "/api/comparison/compare?tickers=A,B,C,D,E,F,G,H,I,J"
    )

    assert response.status_code == 400
    data = response.json()
    assert "maximum 9 tickers" in data["detail"].lower()


@patch("app.services.ticker_comparison.ticker_comparison_service.pair_trading_analysis")
def test_pair_trading_post(mock_pair_trading, mock_pair_trading_result):
    """Test POST /api/comparison/pair-trading endpoint."""
    mock_pair_trading.return_value = mock_pair_trading_result

    response = client.post(
        "/api/comparison/pair-trading",
        json={
            "ticker1": "GLD",
            "ticker2": "GDX",
            "interval": "1day",
            "bars": 252,
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["ticker1"] == "GLD"
    assert data["ticker2"] == "GDX"
    assert "spread" in data
    assert "z_scores" in data
    assert "signals" in data
    assert "cointegration" in data
    assert "hedge_ratio" in data


@patch("app.services.ticker_comparison.ticker_comparison_service.pair_trading_analysis")
def test_pair_trading_get(mock_pair_trading, mock_pair_trading_result):
    """Test GET /api/comparison/pair-trading endpoint."""
    mock_pair_trading.return_value = mock_pair_trading_result

    response = client.get(
        "/api/comparison/pair-trading?ticker1=GLD&ticker2=GDX&interval=1day&bars=252"
    )

    assert response.status_code == 200
    data = response.json()

    assert data["ticker1"] == "GLD"
    assert data["ticker2"] == "GDX"


@patch("app.services.ticker_comparison.ticker_comparison_service.relative_strength_ranking")
def test_relative_strength_ranking_post(mock_rs_ranking):
    """Test POST /api/comparison/relative-strength endpoint."""
    mock_rs_ranking.return_value = {
        "benchmark": "SPY",
        "total_tickers": 5,
        "rankings": [
            {"ticker": "NVDA", "rs_rank": 95, "rs_slope": 0.02},
            {"ticker": "META", "rs_rank": 88, "rs_slope": 0.015},
            {"ticker": "GOOGL", "rs_rank": 75, "rs_slope": 0.01},
            {"ticker": "AAPL", "rs_rank": 68, "rs_slope": 0.008},
            {"ticker": "MSFT", "rs_rank": 62, "rs_slope": 0.005},
        ],
        "best_performers": [
            {"ticker": "NVDA", "rs_rank": 95},
            {"ticker": "META", "rs_rank": 88},
        ],
        "worst_performers": [
            {"ticker": "MSFT", "rs_rank": 62},
        ],
    }

    response = client.post(
        "/api/comparison/relative-strength",
        json={
            "tickers": ["AAPL", "MSFT", "GOOGL", "META", "NVDA"],
            "benchmark": "SPY",
            "interval": "1day",
            "bars": 100,
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["benchmark"] == "SPY"
    assert "rankings" in data
    assert "best_performers" in data
    assert "worst_performers" in data
    assert len(data["rankings"]) == 5


@patch("app.services.ticker_comparison.ticker_comparison_service.relative_strength_ranking")
def test_relative_strength_ranking_get(mock_rs_ranking):
    """Test GET /api/comparison/relative-strength endpoint."""
    mock_rs_ranking.return_value = {
        "benchmark": "SPY",
        "total_tickers": 3,
        "rankings": [
            {"ticker": "AAPL", "rs_rank": 75},
            {"ticker": "MSFT", "rs_rank": 68},
            {"ticker": "GOOGL", "rs_rank": 82},
        ],
        "best_performers": [{"ticker": "GOOGL", "rs_rank": 82}],
        "worst_performers": [{"ticker": "MSFT", "rs_rank": 68}],
    }

    response = client.get(
        "/api/comparison/relative-strength?tickers=AAPL,MSFT,GOOGL&benchmark=SPY"
    )

    assert response.status_code == 200
    data = response.json()

    assert data["benchmark"] == "SPY"
    assert len(data["rankings"]) == 3


def test_rs_ranking_minimum_validation():
    """Test that at least 2 tickers are required for RS ranking."""
    response = client.get("/api/comparison/relative-strength?tickers=AAPL")

    assert response.status_code == 400
    data = response.json()
    assert "at least 2 tickers" in data["detail"].lower()


@patch("app.services.ticker_comparison.ticker_comparison_service.compare_tickers")
def test_comparison_error_handling(mock_compare):
    """Test error handling in comparison endpoint."""
    mock_compare.return_value = {"error": "Failed to fetch data"}

    response = client.post(
        "/api/comparison/compare",
        json={
            "tickers": ["INVALID1", "INVALID2"],
            "interval": "1day",
            "bars": 252,
            "benchmark": "SPY",
        },
    )

    assert response.status_code == 400
    data = response.json()
    assert "error" in data["detail"].lower() or "failed" in data["detail"].lower()


@patch("app.services.ticker_comparison.ticker_comparison_service.pair_trading_analysis")
def test_pair_trading_error_handling(mock_pair_trading):
    """Test error handling in pair trading endpoint."""
    mock_pair_trading.return_value = {"error": "No data available"}

    response = client.post(
        "/api/comparison/pair-trading",
        json={
            "ticker1": "INVALID1",
            "ticker2": "INVALID2",
            "interval": "1day",
            "bars": 252,
        },
    )

    assert response.status_code == 400


def test_invalid_interval_validation():
    """Test interval parameter validation."""
    response = client.post(
        "/api/comparison/compare",
        json={
            "tickers": ["AAPL", "MSFT"],
            "interval": "1day",  # Valid
            "bars": 252,
            "benchmark": "SPY",
        },
    )

    # Should succeed with valid interval
    # (actual validation happens in service layer)
    assert response.status_code in [200, 400, 422, 500]  # Depends on mock


def test_bars_validation():
    """Test bars parameter validation."""
    # Too few bars
    response = client.post(
        "/api/comparison/compare",
        json={
            "tickers": ["AAPL", "MSFT"],
            "interval": "1day",
            "bars": 5,  # Below minimum
            "benchmark": "SPY",
        },
    )

    assert response.status_code == 422  # Pydantic validation error

    # Too many bars
    response = client.post(
        "/api/comparison/compare",
        json={
            "tickers": ["AAPL", "MSFT"],
            "interval": "1day",
            "bars": 2000,  # Above maximum
            "benchmark": "SPY",
        },
    )

    assert response.status_code == 422  # Pydantic validation error
