"""
Tests for Portfolio Risk Measurement Service
"""
import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from app.services.portfolio_risk import (
    PortfolioRiskMeasurement,
    Portfolio,
    Position,
    VaRResult,
    StressTestResult,
    GreeksResult,
    DrawdownResult,
    RiskAttributionResult,
    get_portfolio_risk_service
)


@pytest.fixture
def risk_service():
    """Get portfolio risk service"""
    return PortfolioRiskMeasurement()


@pytest.fixture
def sample_returns():
    """Generate sample returns data"""
    np.random.seed(42)
    return np.random.normal(0.001, 0.02, 252)  # Daily returns for 1 year


@pytest.fixture
def sample_portfolio():
    """Create a sample portfolio"""
    positions = [
        Position(
            symbol="AAPL",
            quantity=100,
            entry_price=150.0,
            current_price=175.0,
            sector="Technology",
            delta=1.0
        ),
        Position(
            symbol="MSFT",
            quantity=50,
            entry_price=300.0,
            current_price=350.0,
            sector="Technology",
            delta=1.0
        ),
        Position(
            symbol="JPM",
            quantity=75,
            entry_price=140.0,
            current_price=155.0,
            sector="Financials",
            delta=1.0
        ),
        Position(
            symbol="XOM",
            quantity=60,
            entry_price=100.0,
            current_price=110.0,
            sector="Energy",
            delta=1.0
        )
    ]
    return Portfolio(positions=positions, cash=10000.0, name="Test Portfolio")


@pytest.fixture
def sample_returns_data():
    """Generate sample returns data for multiple stocks"""
    np.random.seed(42)
    return {
        "AAPL": np.random.normal(0.001, 0.02, 252),
        "MSFT": np.random.normal(0.0008, 0.018, 252),
        "JPM": np.random.normal(0.0012, 0.022, 252),
        "XOM": np.random.normal(0.0015, 0.025, 252)
    }


class TestPortfolioBasics:
    """Test portfolio basic functionality"""

    def test_portfolio_creation(self, sample_portfolio):
        """Test portfolio creation"""
        assert len(sample_portfolio.positions) == 4
        assert sample_portfolio.cash == 10000.0
        assert sample_portfolio.name == "Test Portfolio"

    def test_portfolio_market_value(self, sample_portfolio):
        """Test portfolio market value calculation"""
        # AAPL: 100 * 175 = 17,500
        # MSFT: 50 * 350 = 17,500
        # JPM: 75 * 155 = 11,625
        # XOM: 60 * 110 = 6,600
        # Cash: 10,000
        # Total: 63,225
        expected_value = 17500 + 17500 + 11625 + 6600 + 10000
        assert sample_portfolio.total_market_value == expected_value

    def test_portfolio_pnl(self, sample_portfolio):
        """Test portfolio P&L calculation"""
        # AAPL: (175 - 150) * 100 = 2,500
        # MSFT: (350 - 300) * 50 = 2,500
        # JPM: (155 - 140) * 75 = 1,125
        # XOM: (110 - 100) * 60 = 600
        # Total: 6,725
        expected_pnl = 2500 + 2500 + 1125 + 600
        assert sample_portfolio.total_pnl == expected_pnl

    def test_portfolio_weights(self, sample_portfolio):
        """Test portfolio weight calculation"""
        weights = sample_portfolio.get_weights()
        assert len(weights) == 4
        # Total weight should be close to 1.0 (excluding cash)
        total_weight = sum(weights.values())
        assert 0.84 < total_weight < 0.86  # ~84% invested, 16% cash


class TestVaRCalculations:
    """Test Value at Risk calculations"""

    def test_historical_var(self, risk_service, sample_returns):
        """Test Historical VaR calculation"""
        portfolio_value = 100000.0
        result = risk_service.calculate_var_historical(
            returns=sample_returns,
            portfolio_value=portfolio_value,
            confidence_level=0.95,
            time_horizon_days=1
        )

        assert isinstance(result, VaRResult)
        assert result.confidence_level == 0.95
        assert result.var_amount > 0
        assert result.method == "Historical Simulation"
        assert "mean_return" in result.additional_info
        assert "std_return" in result.additional_info

    def test_parametric_var(self, risk_service, sample_returns):
        """Test Parametric VaR calculation"""
        portfolio_value = 100000.0
        result = risk_service.calculate_var_parametric(
            returns=sample_returns,
            portfolio_value=portfolio_value,
            confidence_level=0.95,
            time_horizon_days=1
        )

        assert isinstance(result, VaRResult)
        assert result.confidence_level == 0.95
        assert result.var_amount > 0
        assert result.method == "Parametric (Normal Distribution)"
        assert "z_score" in result.additional_info
        assert "annualized_volatility" in result.additional_info

    def test_monte_carlo_var(self, risk_service, sample_returns):
        """Test Monte Carlo VaR calculation"""
        portfolio_value = 100000.0
        result = risk_service.calculate_var_monte_carlo(
            returns=sample_returns,
            portfolio_value=portfolio_value,
            confidence_level=0.95,
            time_horizon_days=1,
            num_simulations=5000
        )

        assert isinstance(result, VaRResult)
        assert result.confidence_level == 0.95
        assert result.var_amount > 0
        assert result.method == "Monte Carlo Simulation"
        assert "num_simulations" in result.additional_info
        assert "cvar_amount" in result.additional_info

    def test_all_var_methods(self, risk_service, sample_returns):
        """Test calculating all VaR methods"""
        portfolio_value = 100000.0
        results = risk_service.calculate_all_var_methods(
            returns=sample_returns,
            portfolio_value=portfolio_value,
            confidence_levels=[0.95, 0.99],
            time_horizon_days=1
        )

        assert "historical" in results
        assert "parametric" in results
        assert "monte_carlo" in results
        assert len(results["historical"]) == 2
        assert len(results["parametric"]) == 2
        assert len(results["monte_carlo"]) == 2

    def test_var_with_different_confidence_levels(self, risk_service, sample_returns):
        """Test VaR with different confidence levels"""
        portfolio_value = 100000.0

        var_95 = risk_service.calculate_var_historical(
            returns=sample_returns,
            portfolio_value=portfolio_value,
            confidence_level=0.95
        )

        var_99 = risk_service.calculate_var_historical(
            returns=sample_returns,
            portfolio_value=portfolio_value,
            confidence_level=0.99
        )

        # 99% VaR should be higher than 95% VaR
        assert var_99.var_amount > var_95.var_amount

    def test_var_with_empty_returns(self, risk_service):
        """Test VaR with empty returns array"""
        with pytest.raises(ValueError, match="Returns array cannot be empty"):
            risk_service.calculate_var_historical(
                returns=np.array([]),
                portfolio_value=100000.0
            )


class TestStressTesting:
    """Test stress testing functionality"""

    def test_market_crash_scenario(self, risk_service, sample_portfolio):
        """Test market crash stress scenario"""
        result = risk_service.stress_test_market_crash(
            portfolio=sample_portfolio,
            crash_severity=-0.30
        )

        assert isinstance(result, StressTestResult)
        assert result.scenario_type == "historical"
        assert result.portfolio_loss < 0  # Should be negative (loss)
        assert "Market Crash" in result.scenario_name
        assert len(result.position_impacts) == 4

    def test_sector_shock_scenario(self, risk_service, sample_portfolio):
        """Test sector shock stress scenario"""
        result = risk_service.stress_test_sector_shock(
            portfolio=sample_portfolio,
            sector="Technology",
            shock=-0.20
        )

        assert isinstance(result, StressTestResult)
        assert result.scenario_type == "historical"
        assert "Technology" in result.scenario_name
        # Only tech stocks should be impacted
        assert result.position_impacts["AAPL"] < 0
        assert result.position_impacts["MSFT"] < 0
        assert result.position_impacts["JPM"] == 0
        assert result.position_impacts["XOM"] == 0

    def test_custom_scenario(self, risk_service, sample_portfolio):
        """Test custom stress scenario"""
        custom_shocks = {
            "AAPL": -0.15,
            "MSFT": -0.10,
            "JPM": 0.05,
            "XOM": -0.05
        }

        result = risk_service.stress_test_historical_scenario(
            portfolio=sample_portfolio,
            scenario_shocks=custom_shocks,
            scenario_name="Custom Scenario",
            description="Mixed scenario"
        )

        assert isinstance(result, StressTestResult)
        assert result.scenario_name == "Custom Scenario"
        assert len(result.position_impacts) == 4

    def test_factor_shock(self, risk_service, sample_portfolio):
        """Test factor shock scenario"""
        factor_exposures = {
            "AAPL": 1.2,
            "MSFT": 1.1,
            "JPM": 0.8,
            "XOM": 0.5
        }

        result = risk_service.stress_test_factor_shock(
            portfolio=sample_portfolio,
            factor_name="Market Beta",
            factor_shock=-0.10,
            factor_exposures=factor_exposures
        )

        assert isinstance(result, StressTestResult)
        assert "Market Beta" in result.scenario_name

    def test_reverse_stress_test(self, risk_service, sample_portfolio):
        """Test reverse stress testing"""
        target_loss = -10000.0
        result = risk_service.stress_test_reverse(
            portfolio=sample_portfolio,
            target_loss=target_loss
        )

        assert result["scenario_type"] == "reverse"
        assert result["target_loss"] == target_loss
        assert "uniform_shock_required" in result
        assert "position_specific_shocks" in result

    def test_volatility_spike(self, risk_service, sample_portfolio):
        """Test volatility spike scenario"""
        result = risk_service.stress_test_volatility_spike(
            portfolio=sample_portfolio,
            vol_multiplier=2.0
        )

        assert result["scenario_type"] == "hypothetical"
        assert result["volatility_multiplier"] == 2.0
        assert "current_vega" in result


class TestPortfolioGreeks:
    """Test portfolio Greeks calculations"""

    def test_basic_greeks(self, risk_service, sample_portfolio):
        """Test basic Greeks calculation"""
        result = risk_service.calculate_portfolio_greeks(sample_portfolio)

        assert isinstance(result, GreeksResult)
        assert result.portfolio_delta > 0  # All positions are long
        assert len(result.position_greeks) == 4
        assert "AAPL" in result.position_greeks
        assert "delta" in result.position_greeks["AAPL"]

    def test_greeks_with_options(self, risk_service):
        """Test Greeks with options positions"""
        positions = [
            Position(
                symbol="SPY",
                quantity=10,
                entry_price=450.0,
                current_price=460.0,
                delta=0.6,
                gamma=0.02,
                vega=0.15,
                theta=-0.05
            )
        ]
        portfolio = Portfolio(positions=positions)

        result = risk_service.calculate_portfolio_greeks(portfolio)

        assert result.portfolio_delta == 6.0  # 10 * 0.6
        assert result.portfolio_gamma == 0.2  # 10 * 0.02
        assert result.portfolio_vega == 1.5  # 10 * 0.15
        assert result.portfolio_theta == -0.5  # 10 * -0.05

    def test_hedging_suggestions(self, risk_service, sample_portfolio):
        """Test hedging suggestions"""
        result = risk_service.calculate_hedging_suggestions(
            portfolio=sample_portfolio,
            target_delta=0.0
        )

        assert "current_delta" in result
        assert "target_delta" in result
        assert result["target_delta"] == 0.0

    def test_hedging_for_neutral_portfolio(self, risk_service):
        """Test hedging for already neutral portfolio"""
        positions = [
            Position(
                symbol="SPY",
                quantity=10,
                entry_price=450.0,
                current_price=460.0,
                delta=0.5
            ),
            Position(
                symbol="SPY_PUT",
                quantity=-10,
                entry_price=5.0,
                current_price=4.0,
                delta=-0.5
            )
        ]
        portfolio = Portfolio(positions=positions)

        result = risk_service.calculate_hedging_suggestions(
            portfolio=portfolio,
            target_delta=0.0
        )

        assert result["hedge_needed"] == False


class TestDrawdownAnalysis:
    """Test drawdown analysis"""

    def test_basic_drawdown(self, risk_service):
        """Test basic drawdown calculation"""
        # Create equity curve with known drawdown
        equity_curve = pd.Series([
            100000, 105000, 110000, 108000, 106000,  # Drawdown period
            104000, 106000, 108000, 112000, 115000   # Recovery
        ])

        result = risk_service.calculate_drawdowns(equity_curve)

        assert isinstance(result, DrawdownResult)
        assert result.max_drawdown < 0  # Should be negative
        assert result.max_drawdown_percent < 0
        assert len(result.underwater_periods) > 0

    def test_drawdown_with_dates(self, risk_service):
        """Test drawdown with date index"""
        dates = pd.date_range(start="2023-01-01", periods=10, freq="D")
        equity_values = [
            100000, 105000, 110000, 108000, 106000,
            104000, 106000, 108000, 112000, 115000
        ]
        equity_curve = pd.Series(equity_values, index=dates)

        result = risk_service.calculate_drawdowns(equity_curve)

        assert result.max_drawdown < 0
        assert result.recovery_time_days is not None

    def test_no_drawdown_scenario(self, risk_service):
        """Test with continuously increasing equity curve"""
        equity_curve = pd.Series([100000, 105000, 110000, 115000, 120000])

        result = risk_service.calculate_drawdowns(equity_curve)

        assert result.max_drawdown == 0
        assert result.current_drawdown == 0
        assert len(result.underwater_periods) == 0

    def test_continuous_drawdown(self, risk_service):
        """Test with continuous drawdown (no recovery)"""
        equity_curve = pd.Series([100000, 95000, 90000, 85000, 80000])

        result = risk_service.calculate_drawdowns(equity_curve)

        assert result.max_drawdown < 0
        assert result.current_drawdown < 0
        # Should have one ongoing underwater period
        assert any(p["end_date"] == "Ongoing" for p in result.underwater_periods)

    def test_empty_equity_curve(self, risk_service):
        """Test with empty equity curve"""
        with pytest.raises(ValueError, match="Equity curve cannot be empty"):
            risk_service.calculate_drawdowns(pd.Series([]))


class TestRiskAttribution:
    """Test risk attribution functionality"""

    def test_basic_risk_attribution(self, risk_service, sample_portfolio, sample_returns_data):
        """Test basic risk attribution"""
        result = risk_service.calculate_risk_attribution(
            portfolio=sample_portfolio,
            returns_data=sample_returns_data
        )

        assert isinstance(result, RiskAttributionResult)
        assert result.total_risk > 0
        assert len(result.risk_by_position) == 4
        assert len(result.marginal_risk) == 4
        assert "concentration_metrics" in result.__dict__

    def test_risk_by_sector(self, risk_service, sample_portfolio, sample_returns_data):
        """Test risk attribution by sector"""
        result = risk_service.calculate_risk_attribution(
            portfolio=sample_portfolio,
            returns_data=sample_returns_data
        )

        assert "Technology" in result.risk_by_sector
        assert "Financials" in result.risk_by_sector
        assert "Energy" in result.risk_by_sector

    def test_concentration_metrics(self, risk_service, sample_portfolio, sample_returns_data):
        """Test concentration metrics"""
        result = risk_service.calculate_risk_attribution(
            portfolio=sample_portfolio,
            returns_data=sample_returns_data
        )

        metrics = result.concentration_metrics
        assert "herfindahl_index" in metrics
        assert "effective_number_of_positions" in metrics
        assert "largest_position_weight" in metrics
        assert "top_5_concentration" in metrics

        # Herfindahl index should be between 0 and 1
        assert 0 < metrics["herfindahl_index"] <= 1

    def test_risk_contribution_sums_to_total(self, risk_service, sample_portfolio, sample_returns_data):
        """Test that risk contributions sum to approximately total risk"""
        result = risk_service.calculate_risk_attribution(
            portfolio=sample_portfolio,
            returns_data=sample_returns_data
        )

        total_contribution = sum(result.risk_contribution_percent.values())
        # Should sum to approximately 100%
        assert 95 < total_contribution < 105

    def test_marginal_risk(self, risk_service, sample_portfolio, sample_returns_data):
        """Test marginal risk calculation"""
        result = risk_service.calculate_risk_attribution(
            portfolio=sample_portfolio,
            returns_data=sample_returns_data
        )

        # All positions should have marginal risk values
        for symbol in ["AAPL", "MSFT", "JPM", "XOM"]:
            assert symbol in result.marginal_risk
            assert isinstance(result.marginal_risk[symbol], float)


class TestServiceSingleton:
    """Test service singleton pattern"""

    def test_singleton_instance(self):
        """Test that get_portfolio_risk_service returns same instance"""
        service1 = get_portfolio_risk_service()
        service2 = get_portfolio_risk_service()
        assert service1 is service2


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_single_position_portfolio(self, risk_service):
        """Test portfolio with single position"""
        positions = [
            Position(
                symbol="AAPL",
                quantity=100,
                entry_price=150.0,
                current_price=175.0
            )
        ]
        portfolio = Portfolio(positions=positions)

        greeks = risk_service.calculate_portfolio_greeks(portfolio)
        assert greeks.portfolio_delta == 100.0

    def test_portfolio_with_no_cash(self, risk_service):
        """Test portfolio with zero cash"""
        positions = [
            Position(
                symbol="AAPL",
                quantity=100,
                entry_price=150.0,
                current_price=175.0
            )
        ]
        portfolio = Portfolio(positions=positions, cash=0.0)

        assert portfolio.total_market_value == 17500.0

    def test_negative_returns(self, risk_service):
        """Test VaR with predominantly negative returns"""
        negative_returns = np.random.normal(-0.01, 0.02, 100)
        result = risk_service.calculate_var_historical(
            returns=negative_returns,
            portfolio_value=100000.0
        )

        assert result.var_amount > 0

    def test_zero_volatility_returns(self, risk_service):
        """Test with zero volatility (constant returns)"""
        constant_returns = np.array([0.01] * 100)
        result = risk_service.calculate_var_parametric(
            returns=constant_returns,
            portfolio_value=100000.0
        )

        # VaR should be close to zero with no volatility
        assert result.var_amount < 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
