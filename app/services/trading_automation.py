"""
Trading Automation Orchestrator

Main orchestrator that integrates all components:
- Signal generation
- Order management
- Risk management
- Performance tracking
- Broker integration
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
import logging

from app.services.signal_generator import SignalGenerator, TradingSignal, SignalStrength
from app.services.order_manager import OrderManager, BracketOrder
from app.services.portfolio_risk_manager import PortfolioRiskManager, PositionRisk
from app.services.performance_tracker import PerformanceTracker, TradeRecord, TradeOutcome
from app.services.broker_integration import BrokerManager, BrokerType, ExecutionMode
from app.services.risk_calculator import RiskCalculator

logger = logging.getLogger(__name__)


class AutomationMode(Enum):
    """Automation modes"""
    MANUAL = "manual"  # Manual signal generation and execution
    SEMI_AUTO = "semi_auto"  # Auto signals, manual execution
    FULL_AUTO = "full_auto"  # Full automation (paper trading only)


@dataclass
class AutomationConfig:
    """Configuration for trading automation"""
    # Account
    account_size: float = 100000.0

    # Risk parameters
    risk_per_trade_pct: float = 2.0
    max_portfolio_heat_pct: float = 6.0
    max_sector_exposure_pct: float = 25.0

    # Signal filters
    min_signal_strength: SignalStrength = SignalStrength.MODERATE
    min_risk_reward_ratio: float = 2.0
    min_pattern_score: float = 60.0

    # Order management
    use_bracket_orders: bool = True
    use_trailing_stops: bool = True
    trailing_stop_percent: float = 5.0
    scale_out_enabled: bool = False

    # Time-based rules
    max_days_in_trade: int = 30
    max_open_positions: int = 5

    # Execution
    automation_mode: AutomationMode = AutomationMode.SEMI_AUTO
    execution_mode: ExecutionMode = ExecutionMode.PAPER_ONLY
    broker_type: BrokerType = BrokerType.PAPER

    # Safety
    daily_loss_limit: float = 2.0  # % of account
    kill_switch_enabled: bool = True


class TradingAutomation:
    """
    Main trading automation orchestrator

    Coordinates all trading automation components:
    - Generates signals from patterns
    - Manages risk at position and portfolio level
    - Creates and manages orders
    - Tracks performance
    - Executes trades (paper or real with approval)
    """

    def __init__(self, config: AutomationConfig):
        self.config = config

        # Initialize components
        self.risk_calculator = RiskCalculator()
        self.signal_generator = SignalGenerator(self.risk_calculator)
        self.order_manager = OrderManager()
        self.portfolio_risk = PortfolioRiskManager(
            account_size=config.account_size,
            max_risk_per_trade_pct=config.risk_per_trade_pct,
            max_portfolio_heat_pct=config.max_portfolio_heat_pct,
            max_sector_exposure_pct=config.max_sector_exposure_pct
        )
        self.performance_tracker = PerformanceTracker()
        self.broker_manager = BrokerManager()

        # State
        self.active_signals: Dict[str, TradingSignal] = {}
        self.active_brackets: Dict[str, BracketOrder] = {}
        self.signal_to_bracket: Dict[str, str] = {}  # signal_id -> bracket_id

        # Stats
        self.daily_pnl = 0.0
        self.last_reset_date = datetime.now().date()

        self.logger = logging.getLogger(__name__)
        self.logger.info("Trading automation initialized")

    def process_signal(
        self,
        signal: TradingSignal,
        auto_execute: bool = False
    ) -> Optional[BracketOrder]:
        """
        Process a trading signal

        Args:
            signal: Trading signal to process
            auto_execute: Whether to auto-execute (if allowed by config)

        Returns:
            BracketOrder if created, None otherwise
        """
        self.logger.info(
            f"Processing signal: {signal.ticker} {signal.signal_type.value} "
            f"({signal.strength.value})"
        )

        # Validate signal
        if not signal.is_valid:
            self.logger.warning(f"Signal {signal.signal_id} is invalid")
            return None

        # Check if we already have a position in this ticker
        if signal.ticker in [pos.ticker for pos in self.portfolio_risk.get_all_positions()]:
            self.logger.info(f"Already have position in {signal.ticker}, skipping")
            return None

        # Check signal filters
        if not self._meets_filters(signal):
            self.logger.info(f"Signal {signal.signal_id} filtered out")
            return None

        # Check position limits
        open_positions = len(self.portfolio_risk.get_all_positions())
        if open_positions >= self.config.max_open_positions:
            self.logger.warning(
                f"Max positions reached ({self.config.max_open_positions})"
            )
            return None

        # Check portfolio risk
        position_value = signal.position_size.position_size * signal.entry_price
        can_add, reasons = self.portfolio_risk.can_add_new_position(
            risk_amount=signal.position_size.position_size * (signal.entry_price - signal.stop_loss),
            sector=signal.metadata.get("sector"),
            position_value=position_value
        )

        if not can_add:
            self.logger.warning(
                f"Cannot add position for {signal.ticker}: {'; '.join(reasons)}"
            )
            return None

        # Create bracket order
        bracket = self._create_bracket_from_signal(signal)

        if not bracket:
            return None

        # Store signal and bracket
        self.active_signals[signal.signal_id] = signal
        self.active_brackets[bracket.bracket_id] = bracket
        self.signal_to_bracket[signal.signal_id] = bracket.bracket_id

        # Execute if auto-execute is enabled
        if auto_execute and self.config.automation_mode == AutomationMode.FULL_AUTO:
            self._execute_bracket(bracket, signal)

        return bracket

    def execute_signal(self, signal_id: str) -> bool:
        """
        Manually execute a signal

        Args:
            signal_id: Signal ID to execute

        Returns:
            True if executed successfully
        """
        if signal_id not in self.active_signals:
            self.logger.error(f"Signal {signal_id} not found")
            return False

        if signal_id not in self.signal_to_bracket:
            self.logger.error(f"No bracket order for signal {signal_id}")
            return False

        signal = self.active_signals[signal_id]
        bracket_id = self.signal_to_bracket[signal_id]
        bracket = self.active_brackets[bracket_id]

        return self._execute_bracket(bracket, signal)

    def update_positions(self, price_updates: Dict[str, float]) -> None:
        """
        Update position prices and check for exits

        Args:
            price_updates: Dict of ticker -> current price
        """
        for ticker, current_price in price_updates.items():
            # Update portfolio risk manager
            self.portfolio_risk.update_position_price(ticker, current_price)

            # Update trailing stops
            triggered_stops = self.order_manager.update_trailing_stops(ticker, current_price)

            for stop_id in triggered_stops:
                self.logger.info(f"Trailing stop triggered for {ticker}")
                self._exit_position(ticker, current_price, "trailing_stop")

    def check_exits(self) -> None:
        """Check for time-based and other exits"""
        # Check time-based exits
        time_exits = self.order_manager.check_time_based_exits(
            max_days_in_trade=self.config.max_days_in_trade
        )

        for order_id in time_exits:
            order = self.order_manager.get_order(order_id)
            if order:
                self.logger.info(
                    f"Time-based exit for {order.ticker} after {self.config.max_days_in_trade} days"
                )
                # Would need current price to exit - this is a simplified version
                # In real implementation, would fetch current price and exit

    def close_position(
        self,
        ticker: str,
        exit_price: float,
        reason: str = "manual"
    ) -> bool:
        """
        Close a position

        Args:
            ticker: Ticker symbol
            exit_price: Exit price
            reason: Reason for exit

        Returns:
            True if closed successfully
        """
        return self._exit_position(ticker, exit_price, reason)

    def get_portfolio_status(self) -> Dict[str, Any]:
        """Get comprehensive portfolio status"""
        # Get portfolio risk report
        risk_report = self.portfolio_risk.get_portfolio_risk_report()

        # Get performance metrics
        metrics = self.performance_tracker.calculate_metrics()

        # Get order stats
        order_stats = self.order_manager.get_stats()

        # Get broker status
        broker_status = self.broker_manager.get_status()

        return {
            "account_value": self.config.account_size,
            "daily_pnl": self.daily_pnl,
            "portfolio_heat": risk_report.portfolio_heat,
            "risk_level": risk_report.risk_level.value,
            "open_positions": risk_report.total_positions,
            "max_positions": self.config.max_open_positions,
            "can_add_position": risk_report.can_add_position,
            "active_signals": len(self.active_signals),
            "active_brackets": len(self.active_brackets),
            "warnings": risk_report.warnings,
            "performance": {
                "total_trades": metrics.total_trades,
                "win_rate": metrics.win_rate,
                "profit_factor": metrics.profit_factor,
                "expectancy": metrics.expectancy,
                "current_streak": metrics.current_streak
            },
            "orders": order_stats,
            "broker": broker_status,
            "automation_mode": self.config.automation_mode.value
        }

    def generate_report(self, days: int = 30) -> Dict[str, Any]:
        """Generate comprehensive trading report"""
        perf_report = self.performance_tracker.generate_report(days=days)

        return {
            "period": {
                "start": perf_report.period_start.isoformat(),
                "end": perf_report.period_end.isoformat()
            },
            "metrics": {
                "total_trades": perf_report.metrics.total_trades,
                "win_rate": perf_report.metrics.win_rate,
                "total_pnl": perf_report.metrics.total_pnl,
                "average_win": perf_report.metrics.average_win,
                "average_loss": perf_report.metrics.average_loss,
                "profit_factor": perf_report.metrics.profit_factor,
                "expectancy": perf_report.metrics.expectancy,
                "average_r_multiple": perf_report.metrics.average_r_multiple
            },
            "recent_trades": [
                {
                    "ticker": t.ticker,
                    "entry_date": t.entry_date.isoformat(),
                    "exit_date": t.exit_date.isoformat() if t.exit_date else None,
                    "pnl": t.pnl,
                    "pnl_percent": t.pnl_percent,
                    "outcome": t.outcome.value
                }
                for t in perf_report.recent_trades
            ],
            "recommendations": perf_report.recommendations,
            "common_mistakes": perf_report.common_mistakes
        }

    def _meets_filters(self, signal: TradingSignal) -> bool:
        """Check if signal meets configured filters"""
        # Check signal strength
        strength_scores = {
            SignalStrength.WEAK: 1,
            SignalStrength.MODERATE: 2,
            SignalStrength.STRONG: 3,
            SignalStrength.VERY_STRONG: 4
        }

        if strength_scores.get(signal.strength, 0) < strength_scores.get(self.config.min_signal_strength, 0):
            return False

        # Check risk/reward ratio
        if signal.risk_reward_ratio < self.config.min_risk_reward_ratio:
            return False

        # Check pattern score
        if signal.pattern_score and signal.pattern_score < self.config.min_pattern_score:
            return False

        return True

    def _create_bracket_from_signal(self, signal: TradingSignal) -> Optional[BracketOrder]:
        """Create a bracket order from a signal"""
        try:
            bracket = self.order_manager.create_bracket_order(
                ticker=signal.ticker,
                quantity=signal.position_size.position_size,
                entry_price=signal.entry_price,
                stop_loss_price=signal.stop_loss,
                take_profit_price=signal.target_price,
                notes=f"Signal: {signal.signal_type.value}, Pattern: {signal.pattern_type}"
            )

            # Add trailing stop if enabled
            if self.config.use_trailing_stops:
                self.order_manager.create_trailing_stop(
                    ticker=signal.ticker,
                    quantity=signal.position_size.position_size,
                    trail_type="percent",
                    trail_value=self.config.trailing_stop_percent,
                    initial_price=signal.entry_price
                )

            self.logger.info(
                f"Created bracket order for {signal.ticker}: "
                f"Entry=${signal.entry_price:.2f}, Stop=${signal.stop_loss:.2f}, "
                f"Target=${signal.target_price:.2f}"
            )

            return bracket

        except Exception as e:
            self.logger.error(f"Error creating bracket order: {e}", exc_info=True)
            return None

    def _execute_bracket(self, bracket: BracketOrder, signal: TradingSignal) -> bool:
        """Execute a bracket order"""
        try:
            # Simulate entry fill for paper trading
            self.order_manager.fill_order(
                order_id=bracket.entry_order.order_id,
                filled_price=signal.entry_price
            )

            # Add position to portfolio risk manager
            position = PositionRisk(
                ticker=signal.ticker,
                quantity=signal.position_size.position_size,
                entry_price=signal.entry_price,
                current_price=signal.entry_price,
                stop_loss=signal.stop_loss,
                sector=signal.metadata.get("sector"),
                industry=signal.metadata.get("industry")
            )
            self.portfolio_risk.add_position(position)

            # Create trade record
            trade = TradeRecord(
                trade_id=signal.signal_id,
                ticker=signal.ticker,
                entry_date=datetime.now(),
                entry_price=signal.entry_price,
                quantity=signal.position_size.position_size,
                position_value=signal.position_size.position_size * signal.entry_price,
                stop_loss=signal.stop_loss,
                target_price=signal.target_price,
                signal_type=signal.signal_type.value,
                pattern_type=signal.pattern_type,
                setup_quality=signal.pattern_score or 0.0,
                sector=signal.metadata.get("sector"),
                industry=signal.metadata.get("industry")
            )
            self.performance_tracker.add_trade(trade)

            self.logger.info(f"Executed bracket order for {signal.ticker}")
            return True

        except Exception as e:
            self.logger.error(f"Error executing bracket: {e}", exc_info=True)
            return False

    def _exit_position(self, ticker: str, exit_price: float, reason: str) -> bool:
        """Exit a position"""
        try:
            # Find the signal/bracket for this ticker
            signal_id = None
            for sid, sig in self.active_signals.items():
                if sig.ticker == ticker:
                    signal_id = sid
                    break

            if not signal_id:
                self.logger.error(f"No active signal found for {ticker}")
                return False

            # Remove from portfolio risk
            self.portfolio_risk.remove_position(ticker)

            # Close trade in performance tracker
            trade = self.performance_tracker.close_trade(
                trade_id=signal_id,
                exit_price=exit_price,
                notes=f"Exit reason: {reason}"
            )

            if trade:
                # Update daily P&L
                self.daily_pnl += trade.pnl

                # Check daily loss limit
                daily_loss_pct = abs(self.daily_pnl / self.config.account_size) * 100
                if self.daily_pnl < 0 and daily_loss_pct >= self.config.daily_loss_limit:
                    self.logger.critical(
                        f"Daily loss limit reached: {daily_loss_pct:.2f}%"
                    )
                    if self.config.kill_switch_enabled:
                        self.broker_manager.engage_kill_switch(
                            reason=f"Daily loss limit reached: {daily_loss_pct:.2f}%",
                            engaged_by="automation"
                        )

            # Clean up
            if signal_id in self.signal_to_bracket:
                bracket_id = self.signal_to_bracket[signal_id]
                if bracket_id in self.active_brackets:
                    del self.active_brackets[bracket_id]
                del self.signal_to_bracket[signal_id]

            if signal_id in self.active_signals:
                del self.active_signals[signal_id]

            self.logger.info(
                f"Exited position {ticker} @ ${exit_price:.2f} (Reason: {reason})"
            )
            return True

        except Exception as e:
            self.logger.error(f"Error exiting position: {e}", exc_info=True)
            return False

    def reset_daily_stats(self) -> None:
        """Reset daily statistics"""
        today = datetime.now().date()
        if today > self.last_reset_date:
            self.logger.info(f"Resetting daily stats. Previous P&L: ${self.daily_pnl:.2f}")
            self.daily_pnl = 0.0
            self.last_reset_date = today

    def emergency_close_all(self, reason: str = "emergency") -> int:
        """
        Emergency close all positions

        Args:
            reason: Reason for emergency close

        Returns:
            Number of positions closed
        """
        self.logger.critical(f"EMERGENCY CLOSE ALL: {reason}")

        positions = self.portfolio_risk.get_all_positions()
        closed_count = 0

        for position in positions:
            # In real implementation, would fetch current market price
            # For now, using entry price as approximation
            if self._exit_position(position.ticker, position.current_price, f"emergency_{reason}"):
                closed_count += 1

        # Engage kill switch
        if self.config.kill_switch_enabled:
            self.broker_manager.engage_kill_switch(reason=reason, engaged_by="emergency_close")

        return closed_count
