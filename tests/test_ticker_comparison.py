"""
Tests for Multi-Ticker Comparison Service
"""
import pytest
import numpy as np
from unittest.mock import AsyncMock, MagicMock

from app.services.ticker_comparison import TickerComparisonService


@pytest.fixture
def comparison_service():
    """Create a comparison service instance for testing."""
    return TickerComparisonService()


@pytest.fixture
def mock_market_data():
    """Mock market data for testing."""
    def create_data(symbol, bars=100):
        # Generate realistic mock data
        base_price = 100.0
        timestamps = [1700000000 + i * 86400 for i in range(bars)]

        # Random walk for prices
        np.random.seed(hash(symbol) % 2**32)  # Deterministic based on symbol
        returns = np.random.normal(0.001, 0.02, bars)
        closes = [base_price]
        for r in returns[1:]:
            closes.append(closes[-1] * (1 + r))

        highs = [c * 1.02 for c in closes]
        lows = [c * 0.98 for c in closes]
        opens = [c * 1.001 for c in closes]
        volumes = [1000000 + int(np.random.normal(0, 100000)) for _ in range(bars)]

        return {
            "t": timestamps,
            "o": opens,
            "h": highs,
            "l": lows,
            "c": closes,
            "v": volumes,
        }

    return create_data


@pytest.mark.asyncio
async def test_compare_tickers_basic(comparison_service, monkeypatch, mock_market_data):
    """Test basic multi-ticker comparison."""

    async def fake_get_time_series(symbol, interval, bars):
        return mock_market_data(symbol, bars)

    monkeypatch.setattr(
        comparison_service.market_data,
        "get_time_series",
        fake_get_time_series
    )

    result = await comparison_service.compare_tickers(
        tickers=["AAPL", "MSFT", "GOOGL"],
        interval="1day",
        bars=100,
        benchmark="SPY"
    )

    # Verify structure
    assert "tickers" in result
    assert "benchmark" in result
    assert "chart_data" in result
    assert "metrics" in result
    assert "relative_strength" in result
    assert "correlation_matrix" in result

    # Verify tickers
    assert result["tickers"] == ["AAPL", "MSFT", "GOOGL"]
    assert result["benchmark"] == "SPY"

    # Verify chart data
    assert "AAPL" in result["chart_data"]
    assert "MSFT" in result["chart_data"]
    assert "GOOGL" in result["chart_data"]

    # Verify each ticker has OHLCV data
    for ticker in ["AAPL", "MSFT", "GOOGL"]:
        chart = result["chart_data"][ticker]
        assert "timestamps" in chart
        assert "open" in chart
        assert "high" in chart
        assert "low" in chart
        assert "close" in chart
        assert "volume" in chart
        assert len(chart["close"]) > 0


@pytest.mark.asyncio
async def test_compare_tickers_minimum_requirement(comparison_service):
    """Test that at least 2 tickers are required."""

    result = await comparison_service.compare_tickers(
        tickers=["AAPL"],
        interval="1day",
        bars=100,
        benchmark="SPY"
    )

    assert "error" in result
    assert "at least 2 tickers" in result["error"].lower()


@pytest.mark.asyncio
async def test_compare_tickers_maximum_limit(comparison_service):
    """Test that maximum 9 tickers are allowed."""

    result = await comparison_service.compare_tickers(
        tickers=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        interval="1day",
        bars=100,
        benchmark="SPY"
    )

    assert "error" in result
    assert "maximum 9 tickers" in result["error"].lower()


@pytest.mark.asyncio
async def test_metrics_calculation(comparison_service, monkeypatch, mock_market_data):
    """Test that metrics are calculated correctly."""

    async def fake_get_time_series(symbol, interval, bars):
        return mock_market_data(symbol, bars)

    monkeypatch.setattr(
        comparison_service.market_data,
        "get_time_series",
        fake_get_time_series
    )

    result = await comparison_service.compare_tickers(
        tickers=["AAPL", "MSFT"],
        interval="1day",
        bars=100,
        benchmark="SPY"
    )

    # Verify metrics for each ticker
    for ticker in ["AAPL", "MSFT"]:
        metrics = result["metrics"][ticker]

        # Check all expected metrics are present
        assert "current_price" in metrics
        assert "returns_1d" in metrics
        assert "returns_5d" in metrics
        assert "returns_20d" in metrics
        assert "returns_60d" in metrics
        assert "volatility_20d" in metrics
        assert "atr_14" in metrics
        assert "volume_current" in metrics
        assert "high_52w" in metrics
        assert "low_52w" in metrics

        # Verify some values are not None
        assert metrics["current_price"] is not None
        assert metrics["current_price"] > 0


@pytest.mark.asyncio
async def test_relative_strength_calculation(comparison_service, monkeypatch, mock_market_data):
    """Test relative strength calculations."""

    async def fake_get_time_series(symbol, interval, bars):
        return mock_market_data(symbol, bars)

    monkeypatch.setattr(
        comparison_service.market_data,
        "get_time_series",
        fake_get_time_series
    )

    result = await comparison_service.compare_tickers(
        tickers=["AAPL", "MSFT"],
        interval="1day",
        bars=100,
        benchmark="SPY"
    )

    # Verify RS for each ticker
    for ticker in ["AAPL", "MSFT"]:
        rs = result["relative_strength"][ticker]

        assert "rank" in rs
        assert "current" in rs
        assert "slope" in rs
        assert "benchmark" in rs
        assert "strength_label" in rs

        # Verify benchmark
        assert rs["benchmark"] == "SPY"

        # Verify strength label is valid
        assert rs["strength_label"] in [
            "Very Strong", "Strong", "Neutral", "Weak", "Very Weak", "Unknown"
        ]


@pytest.mark.asyncio
async def test_correlation_matrix(comparison_service, monkeypatch, mock_market_data):
    """Test correlation matrix calculation."""

    async def fake_get_time_series(symbol, interval, bars):
        return mock_market_data(symbol, bars)

    monkeypatch.setattr(
        comparison_service.market_data,
        "get_time_series",
        fake_get_time_series
    )

    result = await comparison_service.compare_tickers(
        tickers=["AAPL", "MSFT", "GOOGL"],
        interval="1day",
        bars=100,
        benchmark="SPY"
    )

    corr_matrix = result["correlation_matrix"]

    # Verify structure
    assert "price_correlation" in corr_matrix
    assert "volume_correlation" in corr_matrix
    assert "tickers" in corr_matrix

    # Verify tickers
    assert corr_matrix["tickers"] == ["AAPL", "MSFT", "GOOGL"]

    # Verify price correlation matrix
    price_corr = corr_matrix["price_correlation"]
    for ticker1 in ["AAPL", "MSFT", "GOOGL"]:
        assert ticker1 in price_corr
        for ticker2 in ["AAPL", "MSFT", "GOOGL"]:
            assert ticker2 in price_corr[ticker1]

            # Self-correlation should be 1.0
            if ticker1 == ticker2:
                assert price_corr[ticker1][ticker2] == 1.0
            else:
                # Correlation should be between -1 and 1
                corr_value = price_corr[ticker1][ticker2]
                if corr_value is not None:
                    assert -1.0 <= corr_value <= 1.0


@pytest.mark.asyncio
async def test_pair_trading_analysis(comparison_service, monkeypatch, mock_market_data):
    """Test pair trading analysis."""

    async def fake_get_time_series(symbol, interval, bars):
        return mock_market_data(symbol, bars)

    monkeypatch.setattr(
        comparison_service.market_data,
        "get_time_series",
        fake_get_time_series
    )

    result = await comparison_service.pair_trading_analysis(
        ticker1="GLD",
        ticker2="GDX",
        interval="1day",
        bars=100
    )

    # Verify structure
    assert "ticker1" in result
    assert "ticker2" in result
    assert "spread" in result
    assert "z_scores" in result
    assert "signals" in result
    assert "cointegration" in result
    assert "hedge_ratio" in result
    assert "statistics" in result

    # Verify tickers
    assert result["ticker1"] == "GLD"
    assert result["ticker2"] == "GDX"

    # Verify spread and z-scores
    assert len(result["spread"]) > 0
    assert len(result["z_scores"]) > 0

    # Verify statistics
    stats = result["statistics"]
    assert "spread_mean" in stats
    assert "spread_std" in stats
    assert "current_spread" in stats
    assert "current_zscore" in stats

    # Verify cointegration test
    coint = result["cointegration"]
    assert "test_statistic" in coint
    assert "p_value" in coint
    assert "result" in coint
    assert "is_cointegrated" in coint

    # Verify signals
    signals = result["signals"]
    assert "current_signal" in signals
    assert signals["current_signal"] in [
        "LONG_SPREAD", "SHORT_SPREAD", "EXIT", "HOLD", "NO_SIGNAL"
    ]


@pytest.mark.asyncio
async def test_relative_strength_ranking(comparison_service, monkeypatch, mock_market_data):
    """Test relative strength ranking."""

    async def fake_get_time_series(symbol, interval, bars):
        return mock_market_data(symbol, bars)

    monkeypatch.setattr(
        comparison_service.market_data,
        "get_time_series",
        fake_get_time_series
    )

    result = await comparison_service.relative_strength_ranking(
        tickers=["AAPL", "MSFT", "GOOGL", "META", "NVDA"],
        benchmark="SPY",
        interval="1day",
        bars=100
    )

    # Verify structure
    assert "benchmark" in result
    assert "total_tickers" in result
    assert "rankings" in result
    assert "best_performers" in result
    assert "worst_performers" in result

    # Verify benchmark
    assert result["benchmark"] == "SPY"

    # Verify rankings
    rankings = result["rankings"]
    assert len(rankings) > 0

    # Verify each ranking has required fields
    for ranking in rankings:
        assert "ticker" in ranking
        assert "rs_rank" in ranking
        assert "rs_current" in ranking
        assert "rs_slope" in ranking
        assert "delta_vs_benchmark" in ranking

    # Verify best and worst performers
    assert len(result["best_performers"]) > 0
    assert len(result["worst_performers"]) > 0


@pytest.mark.asyncio
async def test_spread_calculation(comparison_service):
    """Test spread calculation for pair trading."""

    closes1 = [100, 102, 104, 103, 105]
    closes2 = [50, 51, 52, 51.5, 52.5]

    spread = comparison_service._calculate_spread(closes1, closes2)

    # Verify spread calculation
    assert len(spread) == len(closes1)
    assert spread[0] == pytest.approx(100 / 50, rel=1e-6)
    assert spread[1] == pytest.approx(102 / 51, rel=1e-6)

    # Test division by zero handling
    closes_with_zero = [50, 0, 52]
    spread_with_nan = comparison_service._calculate_spread([100, 100, 100], closes_with_zero)
    assert len(spread_with_nan) == 3
    assert np.isnan(spread_with_nan[1])


@pytest.mark.asyncio
async def test_zscore_calculation(comparison_service):
    """Test z-score calculation."""

    # Create a simple spread with known properties
    spread = [1.0, 1.1, 0.9, 1.0, 1.2, 0.8, 1.0, 1.1, 0.9, 1.0] * 3

    z_scores = comparison_service._calculate_zscore(spread, window=10)

    # Verify z-scores length
    assert len(z_scores) == len(spread)

    # First 9 values should be NaN (window - 1)
    for i in range(9):
        assert np.isnan(z_scores[i])

    # Later values should be valid
    assert not np.isnan(z_scores[10])


@pytest.mark.asyncio
async def test_mean_reversion_signals(comparison_service):
    """Test mean reversion signal generation."""

    # Test different z-score scenarios

    # High z-score -> SHORT_SPREAD
    signals = comparison_service._generate_mean_reversion_signals([2.5])
    assert signals["current_signal"] == "SHORT_SPREAD"

    # Low z-score -> LONG_SPREAD
    signals = comparison_service._generate_mean_reversion_signals([-2.5])
    assert signals["current_signal"] == "LONG_SPREAD"

    # Near zero -> EXIT
    signals = comparison_service._generate_mean_reversion_signals([0.3])
    assert signals["current_signal"] == "EXIT"

    # Moderate z-score -> HOLD
    signals = comparison_service._generate_mean_reversion_signals([1.0])
    assert signals["current_signal"] == "HOLD"


@pytest.mark.asyncio
async def test_hedge_ratio_calculation(comparison_service):
    """Test hedge ratio calculation."""

    # Create correlated price series
    closes1 = [100 + i for i in range(50)]
    closes2 = [50 + i * 0.5 for i in range(50)]

    hedge_ratio = comparison_service._calculate_hedge_ratio(closes1, closes2)

    # Verify hedge ratio is reasonable
    assert hedge_ratio > 0
    assert hedge_ratio == pytest.approx(2.0, rel=0.1)  # Should be ~2x


@pytest.mark.asyncio
async def test_error_handling_no_data(comparison_service, monkeypatch):
    """Test error handling when no data is available."""

    async def fake_get_time_series(symbol, interval, bars):
        return {"error": "No data available"}

    monkeypatch.setattr(
        comparison_service.market_data,
        "get_time_series",
        fake_get_time_series
    )

    result = await comparison_service.compare_tickers(
        tickers=["INVALID1", "INVALID2"],
        interval="1day",
        bars=100,
        benchmark="SPY"
    )

    # Should still return a result, but with error indicators in chart_data
    assert "chart_data" in result
    assert "INVALID1" in result["chart_data"]
    assert "error" in result["chart_data"]["INVALID1"]


@pytest.mark.asyncio
async def test_leader_laggard_identification(comparison_service, monkeypatch, mock_market_data):
    """Test leader/laggard identification."""

    async def fake_get_time_series(symbol, interval, bars):
        return mock_market_data(symbol, bars)

    monkeypatch.setattr(
        comparison_service.market_data,
        "get_time_series",
        fake_get_time_series
    )

    result = await comparison_service.compare_tickers(
        tickers=["AAPL", "MSFT", "GOOGL", "META"],
        interval="1day",
        bars=100,
        benchmark="SPY"
    )

    # Verify leader/laggard structure
    assert "leader_laggard" in result
    leader_laggard = result["leader_laggard"]

    assert "leaders" in leader_laggard
    assert "laggards" in leader_laggard
    assert "total_analyzed" in leader_laggard

    # Verify we have some leaders and laggards
    assert len(leader_laggard["leaders"]) > 0
    assert len(leader_laggard["laggards"]) > 0
