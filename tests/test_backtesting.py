"""
Comprehensive test suite for backtesting system
Tests strategy execution, performance metrics, Monte Carlo, and walk-forward analysis
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from app.backtesting import (
    BacktestEngine,
    PatternBasedStrategy,
    IndicatorBasedStrategy,
    PerformanceMetrics,
    MonteCarloSimulator,
    WalkForwardAnalyzer,
    BacktestVisualizer,
    StrategySignal,
    SignalType,
    PositionSizingMethod
)
from app.backtesting.metrics import MetricsCalculator


@pytest.fixture
def sample_ohlcv_data():
    """Generate sample OHLCV data for testing"""
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    np.random.seed(42)

    # Generate trending data with some volatility
    base_price = 100
    returns = np.random.normal(0.001, 0.02, len(dates))
    prices = base_price * (1 + returns).cumprod()

    df = pd.DataFrame({
        'open': prices * (1 + np.random.uniform(-0.01, 0.01, len(dates))),
        'high': prices * (1 + np.random.uniform(0, 0.02, len(dates))),
        'low': prices * (1 - np.random.uniform(0, 0.02, len(dates))),
        'close': prices,
        'volume': np.random.randint(1000000, 5000000, len(dates)),
    }, index=dates)

    # Add technical indicators
    df['sma_20'] = df['close'].rolling(20).mean()
    df['sma_50'] = df['close'].rolling(50).mean()
    df['sma_200'] = df['close'].rolling(200).mean()
    df['rsi'] = 50 + np.random.uniform(-20, 20, len(dates))  # Simplified RSI
    df['macd'] = np.random.uniform(-2, 2, len(dates))
    df['macd_signal'] = df['macd'].rolling(9).mean()

    return df


@pytest.fixture
def sample_trades():
    """Generate sample trades for testing metrics"""
    return [
        {
            "profit_loss": 500,
            "profit_loss_pct": 5.0,
            "duration_days": 10,
            "r_multiple": 2.5,
            "status": "closed"
        },
        {
            "profit_loss": -200,
            "profit_loss_pct": -2.0,
            "duration_days": 5,
            "r_multiple": -1.0,
            "status": "closed"
        },
        {
            "profit_loss": 800,
            "profit_loss_pct": 8.0,
            "duration_days": 15,
            "r_multiple": 4.0,
            "status": "closed"
        },
        {
            "profit_loss": -150,
            "profit_loss_pct": -1.5,
            "duration_days": 7,
            "r_multiple": -0.75,
            "status": "closed"
        },
        {
            "profit_loss": 600,
            "profit_loss_pct": 6.0,
            "duration_days": 12,
            "r_multiple": 3.0,
            "status": "closed"
        },
    ]


class TestBacktestEngine:
    """Test the core backtesting engine"""

    def test_engine_initialization(self):
        """Test engine initializes correctly"""
        engine = BacktestEngine(
            initial_capital=100000,
            commission_per_trade=5,
            slippage_percent=0.1
        )

        assert engine.initial_capital == 100000
        assert engine.commission_per_trade == 5
        assert engine.slippage_percent == 0.1
        assert engine.cash == 100000
        assert len(engine.positions) == 0
        assert len(engine.trades) == 0

    def test_simple_backtest(self, sample_ohlcv_data):
        """Test running a simple backtest"""
        strategy = IndicatorBasedStrategy(
            name="Test Strategy",
            use_rsi=True,
            use_macd=True
        )

        engine = BacktestEngine(initial_capital=100000)
        result = engine.run_backtest(
            strategy,
            {"AAPL": sample_ohlcv_data}
        )

        assert result is not None
        assert result.strategy_name == "Test Strategy"
        assert result.initial_capital == 100000
        assert result.final_capital > 0
        assert isinstance(result.metrics, PerformanceMetrics)

    def test_position_sizing(self):
        """Test position sizing calculations"""
        strategy = PatternBasedStrategy()

        signal = StrategySignal(
            signal_type=SignalType.BUY,
            timestamp=datetime.now(),
            price=100,
            ticker="AAPL",
            stop_loss=95,
            target_price=110
        )

        # Risk-based position sizing
        position_size = strategy.calculate_position_size(
            signal,
            current_capital=100000,
            current_price=100,
            account_risk_pct=0.02
        )

        # With 2% risk and $5 stop distance, should risk $2000
        # $2000 / $5 = 400 shares
        assert position_size == 400


class TestPerformanceMetrics:
    """Test performance metrics calculations"""

    def test_metrics_calculation(self, sample_trades):
        """Test calculating performance metrics from trades"""
        # Create equity curve
        initial_capital = 10000
        equity = [initial_capital]
        for trade in sample_trades:
            equity.append(equity[-1] + trade["profit_loss"])

        dates = pd.date_range(start='2023-01-01', periods=len(equity), freq='D')
        equity_curve = pd.Series(equity, index=dates)

        metrics = MetricsCalculator.calculate_all_metrics(
            equity_curve,
            sample_trades,
            initial_capital
        )

        assert metrics.total_trades == 5
        assert metrics.winning_trades == 3
        assert metrics.losing_trades == 2
        assert metrics.win_rate == 60.0
        assert metrics.profit_factor > 1.0
        assert metrics.expectancy > 0

    def test_sharpe_ratio_calculation(self):
        """Test Sharpe ratio calculation"""
        # Create equity curve with positive returns
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        initial_capital = 100000
        returns = np.random.normal(0.001, 0.01, len(dates))
        equity = initial_capital * (1 + returns).cumprod()
        equity_curve = pd.Series(equity, index=dates)

        metrics = MetricsCalculator.calculate_all_metrics(
            equity_curve,
            [],
            initial_capital
        )

        assert metrics.sharpe_ratio > 0 or metrics.sharpe_ratio < 0  # Should be calculated
        assert isinstance(metrics.sharpe_ratio, float)

    def test_drawdown_calculation(self):
        """Test drawdown calculations"""
        # Create equity curve with known drawdown
        equity = pd.Series([100, 110, 120, 100, 90, 110, 130])

        metrics = MetricsCalculator.calculate_all_metrics(
            equity,
            [],
            100
        )

        # Max drawdown should be from 120 to 90 = -30 = -25%
        assert metrics.max_drawdown < 0
        assert abs(metrics.max_drawdown_pct) > 0


class TestMonteCarloSimulator:
    """Test Monte Carlo simulation"""

    def test_monte_carlo_simulation(self, sample_trades):
        """Test running Monte Carlo simulation"""
        result = MonteCarloSimulator.run_simulation(
            sample_trades,
            initial_capital=10000,
            num_simulations=100
        )

        assert result.num_simulations == 100
        assert len(result.all_returns) == 100
        assert result.mean_return != 0
        assert result.prob_profit >= 0 and result.prob_profit <= 1

    def test_monte_carlo_var_calculation(self, sample_trades):
        """Test Value at Risk calculation in Monte Carlo"""
        result = MonteCarloSimulator.run_simulation(
            sample_trades,
            initial_capital=10000,
            num_simulations=1000
        )

        # VaR should be less than original return (worst 5%)
        assert result.var_95 <= result.percentile_95

    def test_statistical_significance(self, sample_trades):
        """Test statistical significance assessment"""
        significance = MonteCarloSimulator.assess_statistical_significance(
            sample_trades,
            initial_capital=10000,
            num_simulations=100
        )

        assert "significant" in significance
        assert "z_score" in significance
        assert "interpretation" in significance


class TestWalkForwardAnalyzer:
    """Test walk-forward analysis"""

    def test_walk_forward_windows(self, sample_ohlcv_data):
        """Test walk-forward window creation"""
        analyzer = WalkForwardAnalyzer(in_sample_ratio=0.7)

        data = {"AAPL": sample_ohlcv_data}
        windows = analyzer._create_windows(data, num_windows=3)

        assert len(windows) > 0
        for window in windows:
            assert window.in_sample_start < window.in_sample_end
            assert window.out_of_sample_start > window.in_sample_end
            assert window.out_of_sample_start < window.out_of_sample_end

    def test_walk_forward_analysis(self, sample_ohlcv_data):
        """Test complete walk-forward analysis"""
        strategy = IndicatorBasedStrategy(name="Test Strategy")
        analyzer = WalkForwardAnalyzer(in_sample_ratio=0.7)

        result = analyzer.run_walk_forward(
            strategy,
            {"AAPL": sample_ohlcv_data},
            num_windows=2,
            initial_capital=100000
        )

        assert result.total_windows == 2
        assert len(result.windows) == 2
        assert result.in_sample_ratio == 0.7

    def test_robustness_assessment(self, sample_ohlcv_data):
        """Test strategy robustness assessment"""
        strategy = IndicatorBasedStrategy(name="Test Strategy")
        analyzer = WalkForwardAnalyzer(in_sample_ratio=0.7)

        wf_result = analyzer.run_walk_forward(
            strategy,
            {"AAPL": sample_ohlcv_data},
            num_windows=2,
            initial_capital=100000
        )

        robustness = WalkForwardAnalyzer.assess_robustness(wf_result)

        assert "robustness_score" in robustness
        assert "rating" in robustness
        assert "recommendations" in robustness
        assert robustness["robustness_score"] >= 0
        assert robustness["robustness_score"] <= 100


class TestBacktestVisualizer:
    """Test visualization data generation"""

    def test_equity_curve_data(self):
        """Test equity curve data generation"""
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        equity = pd.Series(range(100, 100 + len(dates)), index=dates)

        data = BacktestVisualizer.create_equity_curve_data(equity)

        assert data["type"] == "line"
        assert len(data["datasets"]) > 0
        assert len(data["datasets"][0]["data"]) == len(equity)

    def test_drawdown_chart_data(self):
        """Test drawdown chart data generation"""
        equity = pd.Series([100, 110, 105, 115, 110, 120])

        data = BacktestVisualizer.create_drawdown_chart_data(equity)

        assert data["type"] == "area"
        assert len(data["datasets"]) > 0

    def test_trade_distribution_data(self, sample_trades):
        """Test trade distribution histogram data"""
        data = BacktestVisualizer.create_trade_distribution_data(sample_trades)

        assert data["type"] == "histogram"
        assert "statistics" in data

    def test_summary_report_generation(self):
        """Test summary report generation"""
        backtest_result = {
            "strategy_name": "Test Strategy",
            "ticker": "AAPL",
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "initial_capital": 100000,
            "final_capital": 115000,
            "total_return": 15000,
            "total_return_pct": 15.0,
            "metrics": {
                "returns": {"cagr": 15.0},
                "risk": {
                    "sharpe_ratio": 1.5,
                    "max_drawdown_pct": -10.0,
                    "annual_volatility": 15.0
                },
                "trades": {
                    "total_trades": 20,
                    "winning_trades": 12,
                    "losing_trades": 8,
                    "win_rate": 60.0
                },
                "profit_loss": {
                    "profit_factor": 2.0,
                    "expectancy": 750,
                    "avg_win": 1500,
                    "avg_loss": 750
                }
            }
        }

        report = BacktestVisualizer.generate_summary_report(backtest_result)

        assert "strategy_name" in report
        assert "capital" in report
        assert "performance" in report
        assert "risk" in report
        assert "trades" in report
        assert "overall_grade" in report

    def test_grade_calculation(self):
        """Test strategy grading"""
        report = {
            "performance": {"cagr": 25.0, "sharpe_ratio": 2.5},
            "risk": {"max_drawdown_pct": -8.0},
            "trades": {"win_rate": 65.0},
            "profit_loss": {"profit_factor": 2.5}
        }

        grade = BacktestVisualizer._calculate_grade(report)

        assert grade in ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D"]


class TestStrategyFramework:
    """Test strategy framework"""

    def test_pattern_based_strategy(self, sample_ohlcv_data):
        """Test pattern-based strategy"""
        strategy = PatternBasedStrategy(
            name="VCP Strategy",
            pattern_types=["vcp"],
            min_pattern_score=7.0
        )

        assert strategy.name == "VCP Strategy"
        assert strategy.parameters["pattern_types"] == ["vcp"]

    def test_indicator_based_strategy(self, sample_ohlcv_data):
        """Test indicator-based strategy"""
        strategy = IndicatorBasedStrategy(
            name="MA Cross Strategy",
            use_ma_cross=True,
            fast_ma=20,
            slow_ma=50
        )

        # Generate signals
        signals = strategy.generate_signals(
            sample_ohlcv_data,
            "AAPL",
            {}
        )

        assert isinstance(signals, list)

    def test_position_sizing_methods(self):
        """Test different position sizing methods"""
        strategies = [
            PatternBasedStrategy(
                position_sizing_method=PositionSizingMethod.FIXED_SHARES
            ),
            PatternBasedStrategy(
                position_sizing_method=PositionSizingMethod.PERCENT_CAPITAL
            ),
            PatternBasedStrategy(
                position_sizing_method=PositionSizingMethod.RISK_BASED
            ),
        ]

        signal = StrategySignal(
            signal_type=SignalType.BUY,
            timestamp=datetime.now(),
            price=100,
            ticker="AAPL",
            stop_loss=95
        )

        for strategy in strategies:
            size = strategy.calculate_position_size(
                signal,
                current_capital=100000,
                current_price=100
            )
            assert size >= 0


class TestIntegration:
    """Integration tests for complete workflows"""

    def test_complete_backtest_workflow(self, sample_ohlcv_data):
        """Test complete backtest workflow from start to finish"""
        # Create strategy
        strategy = IndicatorBasedStrategy(
            name="Complete Test Strategy",
            use_rsi=True,
            use_macd=True,
            use_ma_cross=True
        )

        # Run backtest
        engine = BacktestEngine(
            initial_capital=100000,
            commission_per_trade=1,
            slippage_percent=0.05
        )

        result = engine.run_backtest(
            strategy,
            {"AAPL": sample_ohlcv_data}
        )

        # Verify results
        assert result.metrics.total_trades >= 0
        assert result.initial_capital == 100000
        assert len(result.equity_curve) > 0

        # Run Monte Carlo
        if result.trades:
            trades_dict = [
                {"profit_loss": t.profit_loss, "profit_loss_pct": t.profit_loss_pct}
                for t in result.trades
            ]
            mc_result = MonteCarloSimulator.run_simulation(
                trades_dict,
                100000,
                100
            )
            assert mc_result.num_simulations == 100

        # Generate visualizations
        viz = BacktestVisualizer.create_equity_curve_data(result.equity_curve)
        assert viz["type"] == "line"

    def test_multi_ticker_backtest(self, sample_ohlcv_data):
        """Test backtesting with multiple tickers"""
        strategy = IndicatorBasedStrategy(name="Multi-Ticker Strategy")

        # Create data for multiple tickers
        data = {
            "AAPL": sample_ohlcv_data,
            "MSFT": sample_ohlcv_data.copy(),
            "GOOGL": sample_ohlcv_data.copy()
        }

        engine = BacktestEngine(initial_capital=100000)
        result = engine.run_backtest(strategy, data)

        assert result is not None
        assert result.metrics.total_trades >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
