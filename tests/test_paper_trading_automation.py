"""
Tests for Paper Trading Automation System
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch

from app.services.signal_generator import (
    SignalGenerator,
    create_manual_signal,
    SignalType,
    SignalStrength,
    TradingSignal
)
from app.services.order_manager import (
    OrderManager,
    Order,
    OrderType,
    OrderSide,
    OrderStatus,
    BracketOrder
)
from app.services.portfolio_risk_manager import (
    PortfolioRiskManager,
    PositionRisk,
    RiskLevel
)
from app.services.performance_tracker import (
    PerformanceTracker,
    TradeRecord,
    TradeOutcome
)
from app.services.broker_integration import (
    BrokerManager,
    PaperBroker,
    BrokerConfig,
    BrokerType,
    KillSwitch
)
from app.services.trading_automation import (
    TradingAutomation,
    AutomationConfig,
    AutomationMode
)
from app.services.risk_calculator import RiskCalculator


class TestSignalGenerator:
    """Test signal generation"""

    def test_create_manual_signal(self):
        """Test creating a manual signal"""
        signal = create_manual_signal(
            ticker="AAPL",
            entry_price=150.00,
            stop_loss=145.00,
            target_price=160.00,
            account_size=100000,
            risk_per_trade_pct=2.0
        )

        assert signal is not None
        assert signal.ticker == "AAPL"
        assert signal.entry_price == 150.00
        assert signal.stop_loss == 145.00
        assert signal.target_price == 160.00
        assert signal.is_valid is True

    def test_invalid_price_levels(self):
        """Test that invalid price levels return None"""
        signal = create_manual_signal(
            ticker="AAPL",
            entry_price=150.00,
            stop_loss=155.00,  # Stop above entry - invalid
            target_price=160.00,
            account_size=100000
        )

        assert signal is None

    def test_signal_risk_reward_ratio(self):
        """Test risk/reward ratio calculation"""
        signal = create_manual_signal(
            ticker="AAPL",
            entry_price=100.00,
            stop_loss=95.00,  # $5 risk
            target_price=110.00,  # $10 reward
            account_size=100000
        )

        assert signal is not None
        assert signal.risk_reward_ratio == 2.0  # 10/5 = 2


class TestOrderManager:
    """Test order management"""

    def test_create_bracket_order(self):
        """Test creating a bracket order"""
        order_manager = OrderManager()

        bracket = order_manager.create_bracket_order(
            ticker="MSFT",
            quantity=100,
            entry_price=300.00,
            stop_loss_price=290.00,
            take_profit_price=320.00
        )

        assert bracket is not None
        assert bracket.ticker == "MSFT"
        assert bracket.entry_order.quantity == 100
        assert bracket.stop_loss_order.stop_price == 290.00
        assert bracket.take_profit_order.limit_price == 320.00
        assert bracket.status == "pending"

    def test_fill_order(self):
        """Test filling an order"""
        order_manager = OrderManager()

        bracket = order_manager.create_bracket_order(
            ticker="MSFT",
            quantity=100,
            entry_price=300.00,
            stop_loss_price=290.00,
            take_profit_price=320.00
        )

        # Fill entry order
        success = order_manager.fill_order(
            order_id=bracket.entry_order.order_id,
            filled_price=300.00
        )

        assert success is True
        assert bracket.entry_order.is_filled is True
        assert bracket.entry_order.filled_price == 300.00
        assert bracket.status == "open"

    def test_trailing_stop(self):
        """Test trailing stop functionality"""
        order_manager = OrderManager()

        trailing_stop = order_manager.create_trailing_stop(
            ticker="AAPL",
            quantity=100,
            trail_type="percent",
            trail_value=5.0,
            initial_price=100.00
        )

        # Initial stop should be 5% below entry
        assert trailing_stop.current_stop_price == 95.00

        # Price goes up to 110
        triggered = trailing_stop.update(110.00)
        assert triggered is False
        assert trailing_stop.current_stop_price == 104.50  # 5% below 110

        # Price drops to 104
        triggered = trailing_stop.update(104.00)
        assert triggered is True  # Should trigger at 104.50


class TestPortfolioRiskManager:
    """Test portfolio risk management"""

    def test_add_position(self):
        """Test adding a position"""
        portfolio = PortfolioRiskManager(
            account_size=100000,
            max_risk_per_trade_pct=2.0,
            max_portfolio_heat_pct=6.0
        )

        position = PositionRisk(
            ticker="AAPL",
            quantity=100,
            entry_price=150.00,
            current_price=150.00,
            stop_loss=145.00
        )

        portfolio.add_position(position)

        assert len(portfolio.positions) == 1
        assert portfolio.positions["AAPL"].ticker == "AAPL"

    def test_portfolio_heat_calculation(self):
        """Test portfolio heat calculation"""
        portfolio = PortfolioRiskManager(
            account_size=100000,
            max_risk_per_trade_pct=2.0,
            max_portfolio_heat_pct=6.0
        )

        # Add position with $1000 risk
        position = PositionRisk(
            ticker="AAPL",
            quantity=100,
            entry_price=150.00,
            current_price=150.00,
            stop_loss=140.00  # $10 risk per share x 100 = $1000
        )

        portfolio.add_position(position)

        heat = portfolio.calculate_portfolio_heat()
        assert heat == 1.0  # $1000 / $100000 = 1%

    def test_can_add_new_position(self):
        """Test checking if new position can be added"""
        portfolio = PortfolioRiskManager(
            account_size=100000,
            max_risk_per_trade_pct=2.0,
            max_portfolio_heat_pct=6.0
        )

        # Should be able to add position with 2% risk
        can_add, reasons = portfolio.can_add_new_position(risk_amount=2000)
        assert can_add is True

        # Should NOT be able to add position with 3% risk (exceeds max per trade)
        can_add, reasons = portfolio.can_add_new_position(risk_amount=3000)
        assert can_add is False
        assert len(reasons) > 0

    def test_sector_exposure_limits(self):
        """Test sector exposure limits"""
        portfolio = PortfolioRiskManager(
            account_size=100000,
            max_sector_exposure_pct=25.0
        )

        # Add position worth $20,000 in Technology sector
        position = PositionRisk(
            ticker="AAPL",
            quantity=100,
            entry_price=200.00,
            current_price=200.00,
            stop_loss=190.00,
            sector="Technology"
        )

        portfolio.add_position(position)

        # Try to add another $10,000 in Technology (would be 30% total, over limit)
        can_add, reasons = portfolio.can_add_new_position(
            risk_amount=500,
            sector="Technology",
            position_value=10000
        )

        assert can_add is False
        assert any("Technology" in r for r in reasons)


class TestPerformanceTracker:
    """Test performance tracking"""

    def test_add_and_close_trade(self):
        """Test adding and closing a trade"""
        tracker = PerformanceTracker()

        trade = TradeRecord(
            trade_id="TEST_001",
            ticker="AAPL",
            entry_date=datetime.now(),
            entry_price=150.00,
            quantity=100,
            position_value=15000.00,
            stop_loss=145.00,
            target_price=160.00
        )

        tracker.add_trade(trade)
        assert len(tracker.open_trades) == 1

        # Close trade at profit
        closed_trade = tracker.close_trade(
            trade_id="TEST_001",
            exit_price=155.00
        )

        assert closed_trade is not None
        assert closed_trade.pnl == 500.00  # (155 - 150) * 100
        assert closed_trade.outcome == TradeOutcome.WIN
        assert len(tracker.open_trades) == 0
        assert len(tracker.closed_trades) == 1

    def test_calculate_metrics(self):
        """Test calculating performance metrics"""
        tracker = PerformanceTracker()

        # Create and close some trades
        trades = [
            (150.00, 155.00),  # Win
            (100.00, 95.00),   # Loss
            (200.00, 210.00),  # Win
        ]

        for i, (entry, exit) in enumerate(trades):
            trade = TradeRecord(
                trade_id=f"TEST_{i:03d}",
                ticker="AAPL",
                entry_date=datetime.now(),
                entry_price=entry,
                quantity=100,
                position_value=entry * 100,
                stop_loss=entry - 5,
                target_price=entry + 10
            )

            tracker.add_trade(trade)
            tracker.close_trade(trade_id=f"TEST_{i:03d}", exit_price=exit)

        metrics = tracker.calculate_metrics()

        assert metrics.total_trades == 3
        assert metrics.winning_trades == 2
        assert metrics.losing_trades == 1
        assert metrics.win_rate == pytest.approx(66.67, rel=0.01)


class TestBrokerIntegration:
    """Test broker integration"""

    def test_kill_switch(self):
        """Test kill switch functionality"""
        kill_switch = KillSwitch()

        assert kill_switch.is_engaged is False

        # Engage kill switch
        kill_switch.engage(reason="Test emergency", engaged_by="test")

        assert kill_switch.is_engaged is True
        assert kill_switch._reason == "Test emergency"

        # Disengage
        kill_switch.disengage()

        assert kill_switch.is_engaged is False

    def test_paper_broker(self):
        """Test paper broker"""
        config = BrokerConfig(
            broker_type=BrokerType.PAPER,
            paper_trading=True,
            enabled=True
        )

        broker = PaperBroker(config)

        # Connect
        assert broker.connect() is True
        assert broker.is_connected() is True

        # Submit order
        order = Order(
            order_id="TEST_001",
            ticker="AAPL",
            order_type=OrderType.MARKET,
            side=OrderSide.BUY,
            quantity=100
        )

        success = broker.submit_order(order)
        assert success is True

        # Get account info
        account_info = broker.get_account_info()
        assert "account_value" in account_info
        assert account_info["account_value"] > 0

        # Disconnect
        broker.disconnect()
        assert broker.is_connected() is False

    def test_broker_manager_with_kill_switch(self):
        """Test broker manager respects kill switch"""
        broker_manager = BrokerManager()

        # Add paper broker
        config = BrokerConfig(broker_type=BrokerType.PAPER, enabled=True)
        paper_broker = PaperBroker(config)
        paper_broker.connect()

        broker_manager.add_broker(paper_broker)

        # Create order
        order = Order(
            order_id="TEST_001",
            ticker="AAPL",
            order_type=OrderType.MARKET,
            side=OrderSide.BUY,
            quantity=100
        )

        # Should work normally
        success = broker_manager.submit_order(order, BrokerType.PAPER)
        assert success is True

        # Engage kill switch
        broker_manager.engage_kill_switch("Test emergency")

        # Should fail now
        order2 = Order(
            order_id="TEST_002",
            ticker="MSFT",
            order_type=OrderType.MARKET,
            side=OrderSide.BUY,
            quantity=50
        )

        success = broker_manager.submit_order(order2, BrokerType.PAPER)
        assert success is False


class TestTradingAutomation:
    """Test full trading automation"""

    def test_automation_initialization(self):
        """Test automation system initialization"""
        config = AutomationConfig(
            account_size=100000,
            risk_per_trade_pct=2.0,
            automation_mode=AutomationMode.SEMI_AUTO
        )

        automation = TradingAutomation(config)

        assert automation.config.account_size == 100000
        assert automation.config.risk_per_trade_pct == 2.0
        assert len(automation.active_signals) == 0

    def test_process_signal(self):
        """Test processing a trading signal"""
        config = AutomationConfig(
            account_size=100000,
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

        # Process signal
        bracket = automation.process_signal(signal, auto_execute=False)

        assert bracket is not None
        assert signal.signal_id in automation.active_signals
        assert bracket.bracket_id in automation.active_brackets

    def test_portfolio_status(self):
        """Test getting portfolio status"""
        config = AutomationConfig(account_size=100000)
        automation = TradingAutomation(config)

        status = automation.get_portfolio_status()

        assert "account_value" in status
        assert "portfolio_heat" in status
        assert "open_positions" in status
        assert "performance" in status
        assert status["account_value"] == 100000

    def test_signal_filtering(self):
        """Test signal filtering based on config"""
        config = AutomationConfig(
            account_size=100000,
            min_signal_strength=SignalStrength.STRONG,  # Require STRONG signals
            min_risk_reward_ratio=3.0  # Require 3:1 R/R
        )

        automation = TradingAutomation(config)

        # Create weak signal with low R/R
        weak_signal = create_manual_signal(
            ticker="WEAK",
            entry_price=100.00,
            stop_loss=95.00,
            target_price=105.00,  # Only 1:1 R/R
            account_size=100000
        )

        # Should be filtered out
        bracket = automation.process_signal(weak_signal) if weak_signal else None
        assert bracket is None

        # Create strong signal with good R/R
        strong_signal = create_manual_signal(
            ticker="STRONG",
            entry_price=100.00,
            stop_loss=95.00,
            target_price=115.00,  # 3:1 R/R
            account_size=100000
        )

        # Should pass filters (though strength might not be STRONG based on R/R alone)
        # This test shows the filtering concept
        assert strong_signal is not None


@pytest.mark.asyncio
async def test_full_workflow():
    """Integration test of full workflow"""
    # Create automation
    config = AutomationConfig(
        account_size=100000,
        risk_per_trade_pct=2.0,
        max_portfolio_heat_pct=6.0,
        automation_mode=AutomationMode.SEMI_AUTO
    )

    automation = TradingAutomation(config)

    # Create and process signal
    signal = create_manual_signal(
        ticker="AAPL",
        entry_price=150.00,
        stop_loss=145.00,
        target_price=160.00,
        account_size=100000
    )

    assert signal is not None

    bracket = automation.process_signal(signal)
    assert bracket is not None

    # Execute signal
    success = automation.execute_signal(signal.signal_id)
    assert success is True

    # Update positions
    automation.update_positions({"AAPL": 155.00})

    # Close position
    success = automation.close_position("AAPL", 155.00, "target_reached")
    assert success is True

    # Get status
    status = automation.get_portfolio_status()
    assert status["performance"]["total_trades"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
