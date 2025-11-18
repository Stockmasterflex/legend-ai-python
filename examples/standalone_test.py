"""
Standalone test of Paper Trading Automation (no external dependencies)

This test demonstrates the core functionality without requiring
database connections or external APIs.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from app.services.signal_generator import create_manual_signal, SignalType, SignalStrength
from app.services.order_manager import OrderManager
from app.services.portfolio_risk_manager import PortfolioRiskManager, PositionRisk
from app.services.performance_tracker import PerformanceTracker, TradeRecord
from app.services.broker_integration import BrokerManager, PaperBroker, BrokerConfig, BrokerType
from app.services.trading_automation import TradingAutomation, AutomationConfig, AutomationMode


def test_signal_generation():
    """Test signal generation"""
    print("\n" + "="*60)
    print("TEST 1: Signal Generation")
    print("="*60)

    signal = create_manual_signal(
        ticker="AAPL",
        entry_price=150.00,
        stop_loss=145.00,
        target_price=160.00,
        account_size=100000,
        risk_per_trade_pct=2.0
    )

    assert signal is not None, "Signal should be created"
    assert signal.ticker == "AAPL", "Ticker should match"
    assert signal.is_valid, "Signal should be valid"
    assert signal.risk_reward_ratio == 2.0, "R/R should be 2.0"

    print(f"✓ Signal created: {signal.ticker}")
    print(f"  Entry: ${signal.entry_price:.2f}")
    print(f"  Stop: ${signal.stop_loss:.2f}")
    print(f"  Target: ${signal.target_price:.2f}")
    print(f"  R/R: {signal.risk_reward_ratio:.2f}")
    print(f"  Position Size: {signal.position_size.position_size} shares")
    print(f"  Valid: {signal.is_valid}")


def test_order_management():
    """Test order management"""
    print("\n" + "="*60)
    print("TEST 2: Order Management")
    print("="*60)

    manager = OrderManager()

    # Create bracket order
    bracket = manager.create_bracket_order(
        ticker="MSFT",
        quantity=100,
        entry_price=300.00,
        stop_loss_price=290.00,
        take_profit_price=320.00
    )

    assert bracket is not None, "Bracket should be created"
    assert bracket.ticker == "MSFT", "Ticker should match"
    assert bracket.status == "pending", "Should be pending"

    # Fill entry order
    manager.fill_order(
        order_id=bracket.entry_order.order_id,
        filled_price=300.00
    )

    assert bracket.entry_order.is_filled, "Entry should be filled"
    assert bracket.status == "open", "Bracket should be open"

    print(f"✓ Bracket order created: {bracket.bracket_id}")
    print(f"  Status: {bracket.status}")
    print(f"  Entry filled at: ${bracket.entry_order.filled_price:.2f}")

    # Test trailing stop
    trailing = manager.create_trailing_stop(
        ticker="MSFT",
        quantity=100,
        trail_type="percent",
        trail_value=5.0,
        initial_price=300.00
    )

    assert trailing.current_stop_price == 285.00, "Initial stop should be 5% below"

    # Update with higher price
    triggered = trailing.update(310.00)
    assert not triggered, "Should not trigger"
    assert trailing.current_stop_price == 294.50, "Stop should move up"

    print(f"✓ Trailing stop created")
    print(f"  Initial stop: $285.00")
    print(f"  After price rise to $310: ${trailing.current_stop_price:.2f}")


def test_portfolio_risk():
    """Test portfolio risk management"""
    print("\n" + "="*60)
    print("TEST 3: Portfolio Risk Management")
    print("="*60)

    portfolio = PortfolioRiskManager(
        account_size=100000,
        max_risk_per_trade_pct=2.0,
        max_portfolio_heat_pct=6.0
    )

    # Add position
    position = PositionRisk(
        ticker="AAPL",
        quantity=100,
        entry_price=150.00,
        current_price=150.00,
        stop_loss=140.00,  # $1000 risk
        sector="Technology"
    )

    portfolio.add_position(position)

    heat = portfolio.calculate_portfolio_heat()
    assert heat == 1.0, "Portfolio heat should be 1%"

    # Check if can add new position
    can_add, reasons = portfolio.can_add_new_position(risk_amount=2000)
    assert can_add, "Should be able to add 2% risk position"

    print(f"✓ Position added: {position.ticker}")
    print(f"  Portfolio heat: {heat:.2f}%")
    print(f"  Can add new position: {can_add}")

    # Get risk report
    report = portfolio.get_portfolio_risk_report()
    print(f"✓ Risk Report:")
    print(f"  Total positions: {report.total_positions}")
    print(f"  Risk level: {report.risk_level.value}")
    print(f"  Can add position: {report.can_add_position}")


def test_performance_tracking():
    """Test performance tracking"""
    print("\n" + "="*60)
    print("TEST 4: Performance Tracking")
    print("="*60)

    tracker = PerformanceTracker()

    # Add and close trades
    trades_data = [
        ("AAPL", 150.00, 155.00, 100),  # Win
        ("MSFT", 300.00, 295.00, 50),   # Loss
        ("GOOGL", 120.00, 128.00, 75),  # Win
    ]

    for ticker, entry, exit, qty in trades_data:
        trade = TradeRecord(
            trade_id=f"TEST_{ticker}",
            ticker=ticker,
            entry_date=datetime.now(),
            entry_price=entry,
            quantity=qty,
            position_value=entry * qty,
            stop_loss=entry - 5,
            target_price=entry + 10
        )

        tracker.add_trade(trade)
        tracker.close_trade(trade_id=f"TEST_{ticker}", exit_price=exit)

    # Calculate metrics
    metrics = tracker.calculate_metrics()

    assert metrics.total_trades == 3, "Should have 3 trades"
    assert metrics.winning_trades == 2, "Should have 2 wins"
    assert metrics.losing_trades == 1, "Should have 1 loss"
    assert metrics.win_rate > 60, "Win rate should be > 60%"

    print(f"✓ Performance Metrics:")
    print(f"  Total trades: {metrics.total_trades}")
    print(f"  Win rate: {metrics.win_rate:.2f}%")
    print(f"  Total P&L: ${metrics.total_pnl:,.2f}")
    print(f"  Profit factor: {metrics.profit_factor:.2f}")
    print(f"  Expectancy: ${metrics.expectancy:,.2f}")


def test_broker_integration():
    """Test broker integration"""
    print("\n" + "="*60)
    print("TEST 5: Broker Integration & Kill Switch")
    print("="*60)

    # Create paper broker
    config = BrokerConfig(broker_type=BrokerType.PAPER, enabled=True)
    broker = PaperBroker(config)

    assert broker.connect(), "Should connect"
    assert broker.is_connected(), "Should be connected"

    print(f"✓ Paper broker connected")

    # Test kill switch
    manager = BrokerManager()
    manager.add_broker(broker)

    assert not manager.kill_switch.is_engaged, "Kill switch should be off"

    # Engage kill switch
    manager.engage_kill_switch("Test emergency")

    assert manager.kill_switch.is_engaged, "Kill switch should be engaged"

    print(f"✓ Kill switch engaged")
    print(f"  Status: {manager.kill_switch.status}")

    # Try to submit order (should fail)
    from app.services.order_manager import Order, OrderType, OrderSide

    order = Order(
        order_id="TEST",
        ticker="AAPL",
        order_type=OrderType.MARKET,
        side=OrderSide.BUY,
        quantity=100
    )

    success = manager.submit_order(order)
    assert not success, "Order should be rejected when kill switch engaged"

    print(f"✓ Order correctly rejected with kill switch engaged")


def test_full_automation():
    """Test full automation workflow"""
    print("\n" + "="*60)
    print("TEST 6: Full Automation Workflow")
    print("="*60)

    # Create automation
    config = AutomationConfig(
        account_size=100000,
        risk_per_trade_pct=2.0,
        max_portfolio_heat_pct=6.0,
        automation_mode=AutomationMode.SEMI_AUTO
    )

    automation = TradingAutomation(config)

    # Create signal
    signal = create_manual_signal(
        ticker="AAPL",
        entry_price=150.00,
        stop_loss=145.00,
        target_price=160.00,
        account_size=100000
    )

    assert signal is not None, "Signal should be created"

    # Process signal
    bracket = automation.process_signal(signal)
    assert bracket is not None, "Bracket should be created"

    print(f"✓ Signal processed: {signal.ticker}")
    print(f"  Bracket ID: {bracket.bracket_id}")

    # Execute signal
    success = automation.execute_signal(signal.signal_id)
    assert success, "Signal should execute"

    print(f"✓ Signal executed")

    # Get status
    status = automation.get_portfolio_status()
    assert status['open_positions'] == 1, "Should have 1 open position"

    print(f"✓ Portfolio status:")
    print(f"  Open positions: {status['open_positions']}")
    print(f"  Portfolio heat: {status['portfolio_heat']:.2f}%")

    # Close position
    success = automation.close_position("AAPL", 155.00, "target")
    assert success, "Position should close"

    print(f"✓ Position closed")

    # Get final status
    final_status = automation.get_portfolio_status()
    assert final_status['performance']['total_trades'] == 1, "Should have 1 completed trade"

    print(f"✓ Final performance:")
    print(f"  Total trades: {final_status['performance']['total_trades']}")
    print(f"  Win rate: {final_status['performance']['win_rate']:.2f}%")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("PAPER TRADING AUTOMATION - STANDALONE TESTS")
    print("="*60)

    try:
        test_signal_generation()
        test_order_management()
        test_portfolio_risk()
        test_performance_tracking()
        test_broker_integration()
        test_full_automation()

        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nPaper Trading Automation System is working correctly!")
        print("\nNext steps:")
        print("1. Review the modules in app/services/")
        print("2. Check out PAPER_TRADING_AUTOMATION.md for documentation")
        print("3. Run pytest tests: pytest tests/test_paper_trading_automation.py")
        print("4. Integrate with Legend AI pattern detection")

        return 0

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
