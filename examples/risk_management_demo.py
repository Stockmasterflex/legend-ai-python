"""
Advanced Risk Management System - Demo Script

Demonstrates all features of the professional risk management system:
1. Kelly Criterion Calculator
2. Fixed Fractional Position Sizing
3. Volatility-Based Sizing (ATR, VIX)
4. Portfolio Heat Monitor
5. Visual Risk Display

Run this script to see all risk management features in action.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.advanced_risk_manager import get_risk_manager
from app.services.portfolio_heat_monitor import get_heat_monitor
from app.services.risk_visualizer import get_visualizer
from app.core.risk_models import PortfolioPosition


def print_section(title: str):
    """Print a section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def demo_kelly_criterion():
    """Demonstrate Kelly Criterion position sizing"""
    print_section("1. KELLY CRITERION CALCULATOR")

    manager = get_risk_manager()

    # Example trading system stats
    account_size = 100000
    win_rate = 0.62  # 62% win rate
    avg_win = 500
    avg_loss = 300
    entry_price = 178.50
    stop_loss = 175.00

    print(f"Account Size: ${account_size:,}")
    print(f"Win Rate: {win_rate * 100:.1f}%")
    print(f"Average Win: ${avg_win}")
    print(f"Average Loss: ${avg_loss}")
    print(f"Entry: ${entry_price} | Stop: ${stop_loss}")
    print()

    # Calculate with different Kelly fractions
    for fraction in ["full", "half", "quarter"]:
        result = manager.calculate_kelly_criterion(
            account_size=account_size,
            win_rate=win_rate,
            avg_win_dollars=avg_win,
            avg_loss_dollars=avg_loss,
            kelly_fraction=fraction,
            entry_price=entry_price,
            stop_loss=stop_loss
        )

        print(f"Kelly {fraction.upper()}:")
        print(f"  - Kelly %: {result.kelly_percentage:.2f}%")
        print(f"  - Adjusted %: {result.adjusted_percentage:.2f}%")
        print(f"  - Position Size: {result.position_size} shares")
        print(f"  - Position $: ${result.position_dollars:,.2f}")
        print(f"  - Trading Edge: ${result.edge:,.2f}")
        print(f"  - Risk of Ruin: {result.risk_of_ruin:.2f}%")
        if result.notes:
            print(f"  - Notes: {result.notes[0]}")
        print()


def demo_fixed_fractional():
    """Demonstrate Fixed Fractional position sizing"""
    print_section("2. FIXED FRACTIONAL POSITION SIZING")

    manager = get_risk_manager()

    account_size = 100000
    entry_price = 178.50
    stop_loss = 175.00

    print(f"Account Size: ${account_size:,}")
    print(f"Entry: ${entry_price} | Stop: ${stop_loss}")
    print()

    # Test different risk percentages
    for risk_pct in [0.01, 0.02, 0.03]:
        result = manager.calculate_fixed_fractional(
            account_size=account_size,
            entry_price=entry_price,
            stop_loss=stop_loss,
            risk_percentage=risk_pct,
            max_positions=10
        )

        print(f"{risk_pct * 100:.0f}% Risk per Trade:")
        print(f"  - Risk $: ${result.risk_dollars:,.2f}")
        print(f"  - Position Size: {result.position_size} shares")
        print(f"  - Position $: ${result.position_dollars:,.2f}")
        print(f"  - Position Heat: {result.position_heat:.2f}%")
        print(f"  - Max Portfolio Risk (10 positions): {result.max_positions * risk_pct * 100:.0f}%")
        print()

    # Test correlation adjustment
    print("With Correlation Adjustment (50% correlated):")
    result = manager.calculate_fixed_fractional(
        account_size=account_size,
        entry_price=entry_price,
        stop_loss=stop_loss,
        risk_percentage=0.02,
        correlation_adjustment=0.5
    )

    print(f"  - Original Size: {result.position_size * 2} shares")
    print(f"  - Adjusted Size: {result.position_size} shares (50% reduction)")
    print(f"  - Notes: {result.notes[-1] if result.notes else 'N/A'}")
    print()


def demo_volatility_based():
    """Demonstrate Volatility-Based position sizing"""
    print_section("3. VOLATILITY-BASED SIZING (ATR & VIX)")

    manager = get_risk_manager()

    account_size = 100000
    entry_price = 178.50
    atr = 3.50  # Average True Range

    print(f"Account Size: ${account_size:,}")
    print(f"Entry Price: ${entry_price}")
    print(f"ATR (14-day): ${atr}")
    print()

    # Test different VIX levels
    vix_scenarios = [
        (12, "Low Volatility"),
        (20, "Normal Volatility"),
        (28, "Elevated Volatility"),
        (45, "High Volatility")
    ]

    for vix, description in vix_scenarios:
        result = manager.calculate_volatility_based(
            account_size=account_size,
            entry_price=entry_price,
            atr=atr,
            atr_multiplier=2.0,
            vix=vix
        )

        print(f"{description} (VIX: {vix}):")
        print(f"  - Volatility Regime: {result.volatility_regime.value}")
        print(f"  - Stop Distance: ${result.stop_distance:.2f} ({result.atr_multiplier}× ATR)")
        print(f"  - Position Adjustment: {result.volatility_adjustment}x")
        print(f"  - Position Size: {result.position_size} shares")
        print(f"  - Position $: ${result.position_dollars:,.2f}")
        print()


def demo_dynamic_scaling():
    """Demonstrate Dynamic position scaling"""
    print_section("4. DYNAMIC POSITION SCALING")

    manager = get_risk_manager()

    account_size = 100000
    entry_price = 178.50
    stop_loss = 175.00

    print(f"Account Size: ${account_size:,}")
    print(f"Entry: ${entry_price} | Stop: ${stop_loss}")
    print(f"Base Risk: 2%")
    print()

    # Test different scenarios
    scenarios = [
        (90, "bull", "High Confidence + Bull Market"),
        (50, "normal", "Medium Confidence + Normal Market"),
        (30, "bear", "Low Confidence + Bear Market")
    ]

    for confidence, regime, description in scenarios:
        result = manager.calculate_dynamic_scaling(
            account_size=account_size,
            entry_price=entry_price,
            stop_loss=stop_loss,
            confidence_score=confidence,
            market_regime=regime,
            base_risk_pct=0.02
        )

        print(f"{description}:")
        print(f"  - Confidence Score: {confidence}/100")
        print(f"  - Market Regime: {regime}")
        print(f"  - Adjusted Risk: {result.risk_percentage:.2f}%")
        print(f"  - Position Size: {result.position_size} shares")
        print(f"  - Position $: ${result.position_dollars:,.2f}")
        print()


def demo_portfolio_heat():
    """Demonstrate Portfolio Heat Monitor"""
    print_section("5. PORTFOLIO HEAT MONITOR")

    # Create sample portfolio
    positions = [
        PortfolioPosition(
            symbol="AAPL",
            shares=100,
            entry_price=150.00,
            current_price=155.00,
            stop_loss=145.00,
            target=165.00,
            entry_date=datetime(2024, 1, 1),
            sector="Technology"
        ),
        PortfolioPosition(
            symbol="MSFT",
            shares=50,
            entry_price=300.00,
            current_price=310.00,
            stop_loss=290.00,
            target=330.00,
            entry_date=datetime(2024, 1, 2),
            sector="Technology"
        ),
        PortfolioPosition(
            symbol="JPM",
            shares=200,
            entry_price=150.00,
            current_price=148.00,
            stop_loss=145.00,
            target=160.00,
            entry_date=datetime(2024, 1, 3),
            sector="Finance"
        ),
        PortfolioPosition(
            symbol="XOM",
            shares=150,
            entry_price=100.00,
            current_price=102.00,
            stop_loss=95.00,
            target=110.00,
            entry_date=datetime(2024, 1, 4),
            sector="Energy"
        ),
        PortfolioPosition(
            symbol="GOOGL",
            shares=80,
            entry_price=125.00,
            current_price=128.00,
            stop_loss=120.00,
            target=135.00,
            entry_date=datetime(2024, 1, 5),
            sector="Technology"
        )
    ]

    cash = 50000

    # Calculate portfolio heat
    monitor = get_heat_monitor(
        max_portfolio_risk_pct=10.0,
        max_single_position_pct=20.0,
        max_sector_concentration_pct=30.0
    )

    heat = monitor.calculate_portfolio_heat(positions, cash)

    print(f"Total Account Value: ${heat.total_account_value:,.2f}")
    print(f"Total Positions Value: ${heat.total_positions_value:,.2f}")
    print(f"Cash: ${heat.total_cash:,.2f}")
    print(f"Number of Positions: {heat.num_positions}")
    print()

    print("RISK METRICS:")
    print(f"  - Total Risk: ${heat.total_risk_dollars:,.2f} ({heat.total_risk_percentage:.2f}%)")
    print(f"  - Largest Position: {heat.largest_position_pct:.2f}%")
    print(f"  - Largest Risk: {heat.largest_risk_pct:.2f}%")
    print(f"  - Heat Score: {heat.heat_score:.1f}/100")
    print()

    print("SECTOR CONCENTRATION:")
    for sector, pct in heat.sector_concentration.items():
        print(f"  - {sector}: {pct:.2f}%")
    print()

    if heat.warnings:
        print("⚠️  WARNINGS:")
        for warning in heat.warnings:
            print(f"  {warning}")
        print()

    # Max drawdown projection
    print("MAX DRAWDOWN PROJECTIONS:")
    projection = monitor.project_max_drawdown(positions, heat.total_account_value)

    for scenario_name, scenario_data in projection['scenarios'].items():
        print(f"  {scenario_name.upper()}:")
        print(f"    - Loss: ${scenario_data['loss_dollars']:,.2f} ({scenario_data['loss_percentage']:.2f}%)")
        print(f"    - Remaining: ${scenario_data['remaining_capital']:,.2f}")
        print(f"    - {scenario_data['description']}")
    print()


def demo_visualization():
    """Demonstrate Risk Visualizations"""
    print_section("6. RISK VISUALIZATION")

    # Create sample portfolio
    positions = [
        PortfolioPosition(
            symbol="AAPL",
            shares=100,
            entry_price=150.00,
            current_price=155.00,
            stop_loss=145.00,
            target=165.00,
            entry_date=datetime(2024, 1, 1),
            sector="Technology"
        ),
        PortfolioPosition(
            symbol="MSFT",
            shares=50,
            entry_price=300.00,
            current_price=310.00,
            stop_loss=290.00,
            target=330.00,
            entry_date=datetime(2024, 1, 2),
            sector="Technology"
        ),
        PortfolioPosition(
            symbol="JPM",
            shares=200,
            entry_price=150.00,
            current_price=148.00,
            stop_loss=145.00,
            target=160.00,
            entry_date=datetime(2024, 1, 3),
            sector="Finance"
        )
    ]

    monitor = get_heat_monitor()
    visualizer = get_visualizer()

    heat = monitor.calculate_portfolio_heat(positions, 50000)
    viz_data = monitor.generate_visualization_data(heat)

    # ASCII Heat Map
    print("ASCII HEAT MAP:")
    print(visualizer.generate_text_heat_map(viz_data))
    print()

    # Heat Gauge
    gauge = visualizer.generate_heat_gauge(heat)
    print(f"HEAT GAUGE: {gauge['value']:.1f}/100 - {gauge['status'].upper()}")
    print(f"  {gauge['message']}")
    print()

    # Risk Pyramid
    pyramid_chart = visualizer.generate_risk_pyramid_chart(viz_data)
    if pyramid_chart:
        print("RISK PYRAMID:")
        for tier in pyramid_chart['tiers']:
            print(f"  {tier['level']}: {tier['allocation']:.0f}%")
            print(f"    Positions: {', '.join(tier['positions'])}")
        print()


def demo_comparison():
    """Demonstrate method comparison"""
    print_section("7. COMPARE ALL METHODS")

    manager = get_risk_manager()

    account_size = 100000
    entry_price = 178.50
    stop_loss = 175.00
    win_rate = 0.62
    avg_win = 500
    avg_loss = 300
    atr = 3.50
    vix = 20.0

    print(f"Account: ${account_size:,} | Entry: ${entry_price} | Stop: ${stop_loss}")
    print(f"Win Rate: {win_rate * 100:.0f}% | Avg Win: ${avg_win} | Avg Loss: ${avg_loss}")
    print(f"ATR: ${atr} | VIX: {vix}")
    print()

    results = manager.compare_methods(
        account_size=account_size,
        entry_price=entry_price,
        stop_loss=stop_loss,
        win_rate=win_rate,
        avg_win=avg_win,
        avg_loss=avg_loss,
        atr=atr,
        vix=vix
    )

    print("METHOD COMPARISON:")
    print(f"{'Method':<25} {'Position Size':<15} {'Position $':<20}")
    print("-" * 60)

    if 'fixed_1pct' in results:
        r = results['fixed_1pct']
        print(f"{'Fixed 1%':<25} {r.position_size:<15} ${r.position_dollars:>18,.2f}")

    if 'fixed_2pct' in results:
        r = results['fixed_2pct']
        print(f"{'Fixed 2%':<25} {r.position_size:<15} ${r.position_dollars:>18,.2f}")

    if 'kelly_quarter' in results:
        r = results['kelly_quarter']
        print(f"{'Kelly Quarter':<25} {r.position_size:<15} ${r.position_dollars:>18,.2f}")

    if 'kelly_half' in results:
        r = results['kelly_half']
        print(f"{'Kelly Half':<25} {r.position_size:<15} ${r.position_dollars:>18,.2f}")

    if 'atr_based' in results:
        r = results['atr_based']
        print(f"{'ATR-Based':<25} {r.position_size:<15} ${r.position_dollars:>18,.2f}")

    print()
    print("RECOMMENDATION: Use conservative methods (Fixed 1-2% or Kelly/4) for safety.")
    print()


def main():
    """Run all demos"""
    print("\n" + "=" * 80)
    print("  PROFESSIONAL RISK MANAGEMENT SYSTEM - DEMONSTRATION")
    print("=" * 80)

    try:
        demo_kelly_criterion()
        demo_fixed_fractional()
        demo_volatility_based()
        demo_dynamic_scaling()
        demo_portfolio_heat()
        demo_visualization()
        demo_comparison()

        print("\n" + "=" * 80)
        print("  DEMO COMPLETE!")
        print("=" * 80)
        print("\nAll risk management features demonstrated successfully.")
        print("\nAPI Endpoints Available:")
        print("  - POST /api/advanced-risk/kelly-criterion")
        print("  - POST /api/advanced-risk/fixed-fractional")
        print("  - POST /api/advanced-risk/volatility-based")
        print("  - POST /api/advanced-risk/dynamic-scaling")
        print("  - POST /api/advanced-risk/portfolio-heat")
        print("  - POST /api/advanced-risk/portfolio-heat/dashboard")
        print("  - POST /api/advanced-risk/compare-methods")
        print("\nVisit /docs for interactive API documentation.")
        print()

    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
