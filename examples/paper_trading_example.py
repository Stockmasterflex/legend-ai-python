"""
Example usage of Paper Trading Automation System

This example demonstrates how to use all components of the
paper trading automation system.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from app.services.signal_generator import (
    SignalGenerator,
    create_manual_signal,
    SignalType,
    SignalStrength
)
from app.services.order_manager import OrderManager
from app.services.portfolio_risk_manager import PortfolioRiskManager, PositionRisk
from app.services.performance_tracker import PerformanceTracker, MistakeCategory
from app.services.broker_integration import (
    BrokerManager,
    PaperBroker,
    BrokerConfig,
    BrokerType,
    ExecutionMode
)
from app.services.trading_automation import TradingAutomation, AutomationConfig, AutomationMode
from app.services.risk_calculator import RiskCalculator


def example_1_manual_signal():
    """Example 1: Create and process a manual trading signal"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Manual Signal Generation")
    print("="*60)

    # Create a manual signal
    signal = create_manual_signal(
        ticker="AAPL",
        entry_price=150.00,
        stop_loss=145.00,
        target_price=160.00,
        account_size=100000,
        risk_per_trade_pct=2.0,
        signal_type=SignalType.PATTERN_BREAKOUT,
        notes=["Cup and handle pattern", "Strong volume confirmation"]
    )

    if signal:
        print(f"\n✓ Signal created for {signal.ticker}")
        print(f"  Entry: ${signal.entry_price:.2f}")
        print(f"  Stop: ${signal.stop_loss:.2f}")
        print(f"  Target: ${signal.target_price:.2f}")
        print(f"  R/R Ratio: {signal.risk_reward_ratio:.2f}")
        print(f"  Position Size: {signal.position_size.position_size} shares")
        print(f"  Position Value: ${signal.position_size.position_size_dollars:,.2f}")
        print(f"  Risk Amount: ${signal.position_size.position_size * (signal.entry_price - signal.stop_loss):,.2f}")
        print(f"  Signal Strength: {signal.strength.value}")
        print(f"  Valid: {signal.is_valid}")


def example_2_order_management():
    """Example 2: Create and manage bracket orders"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Order Management")
    print("="*60)

    order_manager = OrderManager()

    # Create a bracket order
    bracket = order_manager.create_bracket_order(
        ticker="MSFT",
        quantity=100,
        entry_price=300.00,
        stop_loss_price=290.00,
        take_profit_price=320.00,
        notes="Trend continuation setup"
    )

    print(f"\n✓ Bracket order created: {bracket.bracket_id}")
    print(f"  Entry Order: {bracket.entry_order.order_id}")
    print(f"  Stop Loss Order: {bracket.stop_loss_order.order_id}")
    print(f"  Take Profit Order: {bracket.take_profit_order.order_id}")
    print(f"  Status: {bracket.status}")

    # Fill the entry order
    order_manager.fill_order(
        order_id=bracket.entry_order.order_id,
        filled_price=300.00
    )

    print(f"\n✓ Entry order filled @ $300.00")
    print(f"  Bracket status: {bracket.status}")

    # Create trailing stop
    trailing_stop = order_manager.create_trailing_stop(
        ticker="MSFT",
        quantity=100,
        trail_type="percent",
        trail_value=5.0,  # 5% trailing stop
        initial_price=300.00
    )

    print(f"\n✓ Trailing stop created")
    print(f"  Initial stop price: ${trailing_stop.current_stop_price:.2f}")

    # Simulate price movement
    prices = [302.00, 305.00, 310.00, 308.00]
    for price in prices:
        triggered = trailing_stop.update(price)
        print(f"  Price: ${price:.2f} -> Stop: ${trailing_stop.current_stop_price:.2f} (Triggered: {triggered})")

    # Get order stats
    stats = order_manager.get_stats()
    print(f"\n✓ Order Statistics:")
    print(f"  Total orders: {stats['total_orders']}")
    print(f"  Active orders: {stats['active_orders']}")
    print(f"  Filled orders: {stats['filled_orders']}")


def example_3_portfolio_risk():
    """Example 3: Portfolio risk management"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Portfolio Risk Management")
    print("="*60)

    portfolio = PortfolioRiskManager(
        account_size=100000,
        max_risk_per_trade_pct=2.0,
        max_portfolio_heat_pct=6.0,
        max_sector_exposure_pct=25.0
    )

    # Add some positions
    positions = [
        PositionRisk(
            ticker="AAPL",
            quantity=100,
            entry_price=150.00,
            current_price=152.00,
            stop_loss=145.00,
            sector="Technology",
            industry="Consumer Electronics"
        ),
        PositionRisk(
            ticker="MSFT",
            quantity=50,
            entry_price=300.00,
            current_price=305.00,
            stop_loss=290.00,
            sector="Technology",
            industry="Software"
        ),
        PositionRisk(
            ticker="JPM",
            quantity=75,
            entry_price=140.00,
            current_price=138.00,
            stop_loss=135.00,
            sector="Financial",
            industry="Banking"
        )
    ]

    for pos in positions:
        portfolio.add_position(pos)

    # Get portfolio risk report
    report = portfolio.get_portfolio_risk_report()

    print(f"\n✓ Portfolio Risk Report:")
    print(f"  Total Positions: {report.total_positions}")
    print(f"  Total Exposure: ${report.total_exposure:,.2f}")
    print(f"  Total Risk: ${report.total_risk_amount:,.2f}")
    print(f"  Portfolio Heat: {report.portfolio_heat:.2f}%")
    print(f"  Risk Level: {report.risk_level.value}")

    print(f"\n  Sector Exposure:")
    for sector, exposure in report.sectors.items():
        print(f"    {sector}: {exposure:.2f}%")

    if report.warnings:
        print(f"\n  ⚠ Warnings:")
        for warning in report.warnings:
            print(f"    - {warning}")

    # Check if can add new position
    can_add, reasons = portfolio.can_add_new_position(
        risk_amount=1000,
        sector="Technology",
        position_value=10000
    )

    print(f"\n✓ Can add new position: {can_add}")
    if not can_add:
        print(f"  Reasons:")
        for reason in reasons:
            print(f"    - {reason}")

    # Calculate max position size
    max_size = portfolio.get_max_position_size(
        entry_price=100.00,
        stop_loss=95.00,
        sector="Healthcare"
    )

    print(f"\n✓ Max position size for new trade:")
    print(f"  Entry: $100, Stop: $95")
    print(f"  Max shares: {max_size}")


def example_4_performance_tracking():
    """Example 4: Performance tracking and reporting"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Performance Tracking")
    print("="*60)

    tracker = PerformanceTracker()

    # Simulate some trades
    from app.services.performance_tracker import TradeRecord

    trades = [
        {
            "trade_id": "TRADE_001",
            "ticker": "AAPL",
            "entry_price": 150.00,
            "exit_price": 155.00,
            "quantity": 100,
            "stop_loss": 145.00,
            "target_price": 160.00
        },
        {
            "trade_id": "TRADE_002",
            "ticker": "MSFT",
            "entry_price": 300.00,
            "exit_price": 295.00,
            "quantity": 50,
            "stop_loss": 290.00,
            "target_price": 320.00
        },
        {
            "trade_id": "TRADE_003",
            "ticker": "GOOGL",
            "entry_price": 120.00,
            "exit_price": 128.00,
            "quantity": 75,
            "stop_loss": 115.00,
            "target_price": 130.00
        }
    ]

    for t in trades:
        trade = TradeRecord(
            trade_id=t["trade_id"],
            ticker=t["ticker"],
            entry_date=datetime.now(),
            entry_price=t["entry_price"],
            quantity=t["quantity"],
            position_value=t["quantity"] * t["entry_price"],
            stop_loss=t["stop_loss"],
            target_price=t["target_price"]
        )
        tracker.add_trade(trade)
        tracker.close_trade(
            trade_id=t["trade_id"],
            exit_price=t["exit_price"]
        )

    # Calculate metrics
    metrics = tracker.calculate_metrics()

    print(f"\n✓ Performance Metrics:")
    print(f"  Total Trades: {metrics.total_trades}")
    print(f"  Winning Trades: {metrics.winning_trades}")
    print(f"  Losing Trades: {metrics.losing_trades}")
    print(f"  Win Rate: {metrics.win_rate:.2f}%")
    print(f"  Total P&L: ${metrics.total_pnl:,.2f}")
    print(f"  Average Win: ${metrics.average_win:,.2f}")
    print(f"  Average Loss: ${metrics.average_loss:,.2f}")
    print(f"  Profit Factor: {metrics.profit_factor:.2f}")
    print(f"  Expectancy: ${metrics.expectancy:,.2f}")
    print(f"  Average R-multiple: {metrics.average_r_multiple:.2f}")
    print(f"  Current Streak: {metrics.current_streak}")

    # Generate report
    report = tracker.generate_report(days=30, top_n=2)

    print(f"\n✓ Performance Report:")
    print(f"  Period: {report.period_start.date()} to {report.period_end.date()}")
    print(f"  Recent Trades: {len(report.recent_trades)}")
    print(f"  Top Performers: {len(report.top_performers)}")

    if report.recommendations:
        print(f"\n  📊 Recommendations:")
        for rec in report.recommendations:
            print(f"    - {rec}")


def example_5_full_automation():
    """Example 5: Full automation workflow"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Full Automation Workflow")
    print("="*60)

    # Configure automation
    config = AutomationConfig(
        account_size=100000,
        risk_per_trade_pct=2.0,
        max_portfolio_heat_pct=6.0,
        max_sector_exposure_pct=25.0,
        min_signal_strength=SignalStrength.MODERATE,
        min_risk_reward_ratio=2.0,
        use_bracket_orders=True,
        use_trailing_stops=True,
        trailing_stop_percent=5.0,
        max_days_in_trade=30,
        max_open_positions=5,
        automation_mode=AutomationMode.SEMI_AUTO,
        execution_mode=ExecutionMode.PAPER_ONLY
    )

    # Create automation system
    automation = TradingAutomation(config)

    print(f"\n✓ Trading Automation initialized")
    print(f"  Account Size: ${config.account_size:,.2f}")
    print(f"  Risk per Trade: {config.risk_per_trade_pct}%")
    print(f"  Max Portfolio Heat: {config.max_portfolio_heat_pct}%")
    print(f"  Automation Mode: {config.automation_mode.value}")

    # Create some signals
    signals = [
        create_manual_signal(
            ticker="AAPL",
            entry_price=150.00,
            stop_loss=145.00,
            target_price=160.00,
            account_size=100000,
            risk_per_trade_pct=2.0
        ),
        create_manual_signal(
            ticker="MSFT",
            entry_price=300.00,
            stop_loss=290.00,
            target_price=325.00,
            account_size=100000,
            risk_per_trade_pct=2.0
        )
    ]

    # Process signals
    for signal in signals:
        if signal:
            bracket = automation.process_signal(signal, auto_execute=False)
            if bracket:
                print(f"\n✓ Processed signal for {signal.ticker}")
                print(f"  Bracket ID: {bracket.bracket_id}")
                print(f"  Status: {bracket.status}")

                # Manually execute
                automation.execute_signal(signal.signal_id)
                print(f"  Executed: ✓")

    # Get portfolio status
    status = automation.get_portfolio_status()

    print(f"\n✓ Portfolio Status:")
    print(f"  Account Value: ${status['account_value']:,.2f}")
    print(f"  Portfolio Heat: {status['portfolio_heat']:.2f}%")
    print(f"  Risk Level: {status['risk_level']}")
    print(f"  Open Positions: {status['open_positions']}/{status['max_positions']}")
    print(f"  Active Signals: {status['active_signals']}")
    print(f"  Can Add Position: {status['can_add_position']}")

    print(f"\n  Performance:")
    print(f"    Total Trades: {status['performance']['total_trades']}")
    print(f"    Win Rate: {status['performance']['win_rate']:.2f}%")
    print(f"    Profit Factor: {status['performance']['profit_factor']:.2f}")

    # Simulate price update and exit
    automation.update_positions({"AAPL": 152.00, "MSFT": 305.00})

    # Close a position
    automation.close_position("AAPL", exit_price=155.00, reason="target_reached")
    print(f"\n✓ Closed AAPL position @ $155.00")

    # Generate report
    report = automation.generate_report(days=30)

    print(f"\n✓ Trading Report:")
    print(f"  Period: {report['period']['start']} to {report['period']['end']}")
    print(f"  Total Trades: {report['metrics']['total_trades']}")
    print(f"  Total P&L: ${report['metrics']['total_pnl']:,.2f}")
    print(f"  Profit Factor: {report['metrics']['profit_factor']:.2f}")

    if report['recommendations']:
        print(f"\n  📊 Recommendations:")
        for rec in report['recommendations'][:3]:
            print(f"    - {rec}")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("PAPER TRADING AUTOMATION SYSTEM - EXAMPLES")
    print("="*60)

    try:
        example_1_manual_signal()
        example_2_order_management()
        example_3_portfolio_risk()
        example_4_performance_tracking()
        example_5_full_automation()

        print("\n" + "="*60)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY! ✓")
        print("="*60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
