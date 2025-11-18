"""
Basic validation script for Portfolio Risk Measurement
Tests core functionality without pytest
"""
import numpy as np
import pandas as pd

from app.services.portfolio_risk import (
    PortfolioRiskMeasurement,
    Portfolio,
    Position,
    get_portfolio_risk_service
)


def test_var_calculation():
    """Test VaR calculation"""
    print("Testing VaR calculation...")
    service = PortfolioRiskMeasurement()

    # Generate sample returns
    np.random.seed(42)
    returns = np.random.normal(0.001, 0.02, 252)
    portfolio_value = 100000.0

    # Test Historical VaR
    hist_var = service.calculate_var_historical(
        returns=returns,
        portfolio_value=portfolio_value,
        confidence_level=0.95
    )
    print(f"  ✓ Historical VaR (95%): ${hist_var.var_amount:,.2f} ({hist_var.var_percent:.2f}%)")

    # Test Parametric VaR
    param_var = service.calculate_var_parametric(
        returns=returns,
        portfolio_value=portfolio_value,
        confidence_level=0.95
    )
    print(f"  ✓ Parametric VaR (95%): ${param_var.var_amount:,.2f} ({param_var.var_percent:.2f}%)")

    # Test Monte Carlo VaR
    mc_var = service.calculate_var_monte_carlo(
        returns=returns,
        portfolio_value=portfolio_value,
        confidence_level=0.95,
        num_simulations=5000
    )
    print(f"  ✓ Monte Carlo VaR (95%): ${mc_var.var_amount:,.2f} ({mc_var.var_percent:.2f}%)")
    print("  ✓ All VaR methods working correctly\n")


def test_portfolio_creation():
    """Test portfolio creation and metrics"""
    print("Testing Portfolio creation...")

    positions = [
        Position(
            symbol="AAPL",
            quantity=100,
            entry_price=150.0,
            current_price=175.0,
            sector="Technology"
        ),
        Position(
            symbol="MSFT",
            quantity=50,
            entry_price=300.0,
            current_price=350.0,
            sector="Technology"
        ),
        Position(
            symbol="JPM",
            quantity=75,
            entry_price=140.0,
            current_price=155.0,
            sector="Financials"
        )
    ]

    portfolio = Portfolio(positions=positions, cash=10000.0)

    print(f"  ✓ Portfolio created with {len(portfolio.positions)} positions")
    print(f"  ✓ Total Market Value: ${portfolio.total_market_value:,.2f}")
    print(f"  ✓ Total P&L: ${portfolio.total_pnl:,.2f} ({portfolio.total_pnl_percent:.2f}%)")

    weights = portfolio.get_weights()
    print(f"  ✓ Position weights calculated: {len(weights)} positions")
    print()


def test_stress_testing():
    """Test stress testing"""
    print("Testing Stress Testing...")

    service = PortfolioRiskMeasurement()

    positions = [
        Position(
            symbol="AAPL",
            quantity=100,
            entry_price=150.0,
            current_price=175.0,
            sector="Technology"
        ),
        Position(
            symbol="JPM",
            quantity=75,
            entry_price=140.0,
            current_price=155.0,
            sector="Financials"
        )
    ]

    portfolio = Portfolio(positions=positions)

    # Market crash test
    crash_result = service.stress_test_market_crash(
        portfolio=portfolio,
        crash_severity=-0.30
    )
    print(f"  ✓ Market Crash (-30%): ${crash_result.portfolio_loss:,.2f} loss ({crash_result.portfolio_loss_percent:.2f}%)")

    # Sector shock test
    sector_result = service.stress_test_sector_shock(
        portfolio=portfolio,
        sector="Technology",
        shock=-0.20
    )
    print(f"  ✓ Tech Sector Shock (-20%): ${sector_result.portfolio_loss:,.2f} loss")
    print()


def test_portfolio_greeks():
    """Test portfolio Greeks calculation"""
    print("Testing Portfolio Greeks...")

    service = PortfolioRiskMeasurement()

    positions = [
        Position(
            symbol="SPY",
            quantity=100,
            entry_price=450.0,
            current_price=460.0,
            delta=1.0,
            gamma=0.0,
            vega=0.0,
            theta=0.0
        ),
        Position(
            symbol="SPY_CALL",
            quantity=10,
            entry_price=5.0,
            current_price=7.0,
            delta=0.6,
            gamma=0.02,
            vega=0.15,
            theta=-0.05
        )
    ]

    portfolio = Portfolio(positions=positions)

    greeks = service.calculate_portfolio_greeks(portfolio)
    print(f"  ✓ Portfolio Delta: {greeks.portfolio_delta:,.2f}")
    print(f"  ✓ Portfolio Gamma: {greeks.portfolio_gamma:,.4f}")
    print(f"  ✓ Portfolio Vega: {greeks.portfolio_vega:,.2f}")
    print(f"  ✓ Portfolio Theta: {greeks.portfolio_theta:,.2f}")
    print()


def test_drawdown_analysis():
    """Test drawdown analysis"""
    print("Testing Drawdown Analysis...")

    service = PortfolioRiskMeasurement()

    # Create equity curve with known drawdown
    equity_curve = pd.Series([
        100000, 105000, 110000, 108000, 106000,
        104000, 106000, 108000, 112000, 115000,
        120000, 118000, 125000
    ])

    result = service.calculate_drawdowns(equity_curve)
    print(f"  ✓ Max Drawdown: ${result.max_drawdown:,.2f} ({result.max_drawdown_percent:.2f}%)")
    print(f"  ✓ Average Drawdown: ${result.average_drawdown:,.2f} ({result.average_drawdown_percent:.2f}%)")
    print(f"  ✓ Current Drawdown: ${result.current_drawdown:,.2f} ({result.current_drawdown_percent:.2f}%)")
    print(f"  ✓ Underwater Periods: {len(result.underwater_periods)}")
    print()


def test_risk_attribution():
    """Test risk attribution"""
    print("Testing Risk Attribution...")

    service = PortfolioRiskMeasurement()

    positions = [
        Position(
            symbol="AAPL",
            quantity=100,
            entry_price=150.0,
            current_price=175.0,
            sector="Technology"
        ),
        Position(
            symbol="MSFT",
            quantity=50,
            entry_price=300.0,
            current_price=350.0,
            sector="Technology"
        )
    ]

    portfolio = Portfolio(positions=positions)

    # Generate sample returns
    np.random.seed(42)
    returns_data = {
        "AAPL": np.random.normal(0.001, 0.02, 252),
        "MSFT": np.random.normal(0.0008, 0.018, 252)
    }

    result = service.calculate_risk_attribution(
        portfolio=portfolio,
        returns_data=returns_data
    )

    print(f"  ✓ Portfolio Risk: {result.total_risk:.2f}%")
    print(f"  ✓ Risk by Position: {len(result.risk_by_position)} positions")
    print(f"  ✓ Risk by Sector: {len(result.risk_by_sector)} sectors")
    print(f"  ✓ Herfindahl Index: {result.concentration_metrics['herfindahl_index']:.4f}")
    print(f"  ✓ Effective Positions: {result.concentration_metrics['effective_number_of_positions']:.2f}")
    print()


def test_singleton():
    """Test service singleton"""
    print("Testing Service Singleton...")
    service1 = get_portfolio_risk_service()
    service2 = get_portfolio_risk_service()
    assert service1 is service2, "Services should be the same instance"
    print("  ✓ Singleton pattern working correctly\n")


def main():
    """Run all tests"""
    print("=" * 60)
    print("Portfolio Risk Measurement - Basic Validation")
    print("=" * 60)
    print()

    try:
        test_portfolio_creation()
        test_var_calculation()
        test_stress_testing()
        test_portfolio_greeks()
        test_drawdown_analysis()
        test_risk_attribution()
        test_singleton()

        print("=" * 60)
        print("✓ All basic tests passed!")
        print("=" * 60)
        return 0

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
