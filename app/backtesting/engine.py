"""
Backtesting Engine
Core engine for running historical simulations and backtests
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging

from .strategy import Strategy, StrategySignal, SignalType, ExitReason
from .metrics import MetricsCalculator, PerformanceMetrics

logger = logging.getLogger(__name__)


@dataclass
class Position:
    """Represents an open trading position"""
    ticker: str
    entry_date: datetime
    entry_price: float
    shares: int
    stop_loss: Optional[float] = None
    target_price: Optional[float] = None
    signal_type: str = ""
    entry_reason: str = ""

    # Tracking MAE/MFE
    highest_price: float = field(init=False)
    lowest_price: float = field(init=False)

    def __post_init__(self):
        self.highest_price = self.entry_price
        self.lowest_price = self.entry_price

    def update_price_extremes(self, current_price: float):
        """Update MAE/MFE tracking"""
        self.highest_price = max(self.highest_price, current_price)
        self.lowest_price = min(self.lowest_price, current_price)

    def get_current_value(self, current_price: float) -> float:
        """Get current position value"""
        return self.shares * current_price

    def get_unrealized_pnl(self, current_price: float) -> float:
        """Get unrealized profit/loss"""
        return (current_price - self.entry_price) * self.shares

    def get_mae(self) -> float:
        """Maximum Adverse Excursion"""
        return (self.lowest_price - self.entry_price) * self.shares

    def get_mfe(self) -> float:
        """Maximum Favorable Excursion"""
        return (self.highest_price - self.entry_price) * self.shares


@dataclass
class Trade:
    """Completed trade record"""
    ticker: str
    entry_date: datetime
    entry_price: float
    shares: int
    exit_date: datetime
    exit_price: float
    exit_reason: str
    profit_loss: float
    profit_loss_pct: float
    commission: float
    mae: float
    mfe: float
    signal_type: str = ""
    entry_reason: str = ""
    stop_loss: Optional[float] = None
    target_price: Optional[float] = None

    @property
    def duration_days(self) -> int:
        """Trade duration in days"""
        return (self.exit_date - self.entry_date).days

    @property
    def is_win(self) -> bool:
        """Whether trade was profitable"""
        return self.profit_loss > 0

    @property
    def r_multiple(self) -> Optional[float]:
        """R-multiple (profit/loss relative to risk)"""
        if self.stop_loss:
            risk = abs(self.entry_price - self.stop_loss) * self.shares
            if risk > 0:
                return self.profit_loss / risk
        return None


@dataclass
class BacktestResult:
    """Complete backtest results"""
    strategy_name: str
    ticker: str
    start_date: datetime
    end_date: datetime
    initial_capital: float
    final_capital: float

    # Trade history
    trades: List[Trade]

    # Equity curve (time series of portfolio value)
    equity_curve: pd.Series

    # Performance metrics
    metrics: PerformanceMetrics

    # Configuration
    config: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary"""
        return {
            "strategy_name": self.strategy_name,
            "ticker": self.ticker,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "initial_capital": self.initial_capital,
            "final_capital": self.final_capital,
            "total_return": self.final_capital - self.initial_capital,
            "total_return_pct": ((self.final_capital - self.initial_capital) / self.initial_capital) * 100,
            "total_trades": len(self.trades),
            "metrics": self.metrics.to_dict(),
            "config": self.config,
            "trade_count": len(self.trades),
        }


class BacktestEngine:
    """
    Core backtesting engine

    Simulates trading strategy on historical data with realistic execution
    """

    def __init__(
        self,
        initial_capital: float = 100000,
        commission_per_trade: float = 0,
        slippage_percent: float = 0.0,
        margin_requirement: float = 1.0,  # 1.0 = cash account, 0.5 = 2x margin
    ):
        self.initial_capital = initial_capital
        self.commission_per_trade = commission_per_trade
        self.slippage_percent = slippage_percent
        self.margin_requirement = margin_requirement

        # State variables
        self.cash = initial_capital
        self.positions: Dict[str, Position] = {}
        self.trades: List[Trade] = []
        self.equity_history: List[Tuple[datetime, float]] = []

    def run_backtest(
        self,
        strategy: Strategy,
        data: Dict[str, pd.DataFrame],  # ticker -> OHLCV DataFrame
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> BacktestResult:
        """
        Run backtest on historical data

        Args:
            strategy: Trading strategy to test
            data: Dictionary of ticker -> OHLCV DataFrame
            start_date: Backtest start date (None = earliest data)
            end_date: Backtest end date (None = latest data)

        Returns:
            BacktestResult with complete results
        """
        logger.info(f"Starting backtest: {strategy.name}")

        # Reset state
        self._reset_state()

        # Determine date range
        all_dates = set()
        for df in data.values():
            all_dates.update(df.index)
        all_dates = sorted(all_dates)

        if start_date:
            all_dates = [d for d in all_dates if d >= start_date]
        if end_date:
            all_dates = [d for d in all_dates if d <= end_date]

        if not all_dates:
            logger.warning("No data in specified date range")
            return self._empty_result(strategy, list(data.keys())[0] if data else "")

        # Main backtest loop
        for current_date in all_dates:
            self._process_day(strategy, data, current_date)

            # Record equity
            portfolio_value = self._calculate_portfolio_value(data, current_date)
            self.equity_history.append((current_date, portfolio_value))

        # Close any remaining positions
        self._close_all_positions(data, all_dates[-1], "end_of_period")

        # Build result
        result = self._build_result(
            strategy,
            list(data.keys())[0] if len(data) == 1 else "multiple",
            all_dates[0],
            all_dates[-1]
        )

        logger.info(f"Backtest complete: {len(self.trades)} trades, " +
                   f"Return: {result.metrics.total_return_pct:.2f}%")

        return result

    def _process_day(
        self,
        strategy: Strategy,
        data: Dict[str, pd.DataFrame],
        current_date: datetime
    ):
        """Process a single trading day"""
        # Update position extremes (for MAE/MFE)
        for ticker, position in self.positions.items():
            if ticker in data and current_date in data[ticker].index:
                current_price = data[ticker].loc[current_date, 'close']
                position.update_price_extremes(current_price)

        # Check for stop losses and targets
        self._check_exits(data, current_date)

        # Generate signals for each ticker
        for ticker, df in data.items():
            if current_date not in df.index:
                continue

            # Get data up to current date
            historical_data = df.loc[:current_date]

            if len(historical_data) < 20:  # Need minimum data
                continue

            # Get current positions as dict
            current_positions = {
                t: {
                    "entry_price": p.entry_price,
                    "shares": p.shares,
                    "stop_loss": p.stop_loss,
                    "target_price": p.target_price
                }
                for t, p in self.positions.items()
            }

            # Generate signals
            try:
                signals = strategy.generate_signals(
                    historical_data,
                    ticker,
                    current_positions
                )
            except Exception as e:
                logger.error(f"Error generating signals for {ticker}: {e}")
                continue

            # Process signals
            for signal in signals:
                self._process_signal(signal, strategy, current_date)

    def _process_signal(
        self,
        signal: StrategySignal,
        strategy: Strategy,
        current_date: datetime
    ):
        """Process a trading signal"""
        if signal.signal_type == SignalType.BUY:
            self._execute_buy(signal, strategy, current_date)
        elif signal.signal_type == SignalType.EXIT:
            self._execute_exit(signal, current_date)

    def _execute_buy(
        self,
        signal: StrategySignal,
        strategy: Strategy,
        current_date: datetime
    ):
        """Execute buy order"""
        # Check if already in position
        if signal.ticker in self.positions:
            return

        # Apply slippage
        execution_price = signal.price * (1 + self.slippage_percent / 100)

        # Calculate position size
        position_size = strategy.calculate_position_size(
            signal,
            self.cash,
            execution_price,
            strategy.risk_rules.risk_per_trade
        )

        if position_size <= 0:
            return

        # Check if we have enough cash
        position_value = position_size * execution_price
        total_cost = position_value + self.commission_per_trade

        if total_cost > self.cash:
            # Reduce position size to fit available cash
            available_for_position = self.cash - self.commission_per_trade
            position_size = int(available_for_position / execution_price)

            if position_size <= 0:
                return

            position_value = position_size * execution_price
            total_cost = position_value + self.commission_per_trade

        # Validate signal against risk rules
        signal.position_value = position_value
        current_positions = {
            t: {"value": p.get_current_value(execution_price)}
            for t, p in self.positions.items()
        }

        portfolio_value = self.cash + sum(p["value"] for p in current_positions.values())

        if not strategy.validate_signal(signal, current_positions, portfolio_value):
            return

        # Execute trade
        self.cash -= total_cost

        position = Position(
            ticker=signal.ticker,
            entry_date=current_date,
            entry_price=execution_price,
            shares=position_size,
            stop_loss=signal.stop_loss,
            target_price=signal.target_price,
            signal_type=signal.signal_type.value,
            entry_reason=signal.reason
        )

        self.positions[signal.ticker] = position

        logger.debug(f"BUY {position_size} {signal.ticker} @ ${execution_price:.2f}")

    def _execute_exit(
        self,
        signal: StrategySignal,
        current_date: datetime
    ):
        """Execute exit order"""
        if signal.ticker not in self.positions:
            return

        position = self.positions[signal.ticker]

        # Apply slippage
        execution_price = signal.price * (1 - self.slippage_percent / 100)

        # Close position
        proceeds = position.shares * execution_price - self.commission_per_trade
        self.cash += proceeds

        # Calculate P&L
        profit_loss = (execution_price - position.entry_price) * position.shares - (2 * self.commission_per_trade)
        profit_loss_pct = ((execution_price - position.entry_price) / position.entry_price) * 100

        # Create trade record
        trade = Trade(
            ticker=signal.ticker,
            entry_date=position.entry_date,
            entry_price=position.entry_price,
            shares=position.shares,
            exit_date=current_date,
            exit_price=execution_price,
            exit_reason=signal.exit_reason.value if signal.exit_reason else "signal",
            profit_loss=profit_loss,
            profit_loss_pct=profit_loss_pct,
            commission=2 * self.commission_per_trade,
            mae=position.get_mae(),
            mfe=position.get_mfe(),
            signal_type=position.signal_type,
            entry_reason=position.entry_reason,
            stop_loss=position.stop_loss,
            target_price=position.target_price
        )

        self.trades.append(trade)
        del self.positions[signal.ticker]

        logger.debug(f"SELL {trade.shares} {signal.ticker} @ ${execution_price:.2f} " +
                    f"P&L: ${profit_loss:.2f} ({profit_loss_pct:.2f}%)")

    def _check_exits(self, data: Dict[str, pd.DataFrame], current_date: datetime):
        """Check for stop loss and target exits"""
        positions_to_exit = []

        for ticker, position in self.positions.items():
            if ticker not in data or current_date not in data[ticker].index:
                continue

            current_price = data[ticker].loc[current_date, 'close']

            # Check stop loss
            if position.stop_loss and current_price <= position.stop_loss:
                exit_signal = StrategySignal(
                    signal_type=SignalType.EXIT,
                    timestamp=current_date,
                    price=position.stop_loss,  # Assume filled at stop
                    ticker=ticker,
                    exit_reason=ExitReason.STOP_LOSS,
                    reason="Stop loss hit"
                )
                positions_to_exit.append(exit_signal)

            # Check target
            elif position.target_price and current_price >= position.target_price:
                exit_signal = StrategySignal(
                    signal_type=SignalType.EXIT,
                    timestamp=current_date,
                    price=position.target_price,  # Assume filled at target
                    ticker=ticker,
                    exit_reason=ExitReason.TARGET_HIT,
                    reason="Target reached"
                )
                positions_to_exit.append(exit_signal)

        # Execute exits
        for signal in positions_to_exit:
            self._execute_exit(signal, current_date)

    def _close_all_positions(
        self,
        data: Dict[str, pd.DataFrame],
        current_date: datetime,
        reason: str
    ):
        """Close all open positions (end of backtest)"""
        for ticker in list(self.positions.keys()):
            if ticker not in data or current_date not in data[ticker].index:
                continue

            current_price = data[ticker].loc[current_date, 'close']

            exit_signal = StrategySignal(
                signal_type=SignalType.EXIT,
                timestamp=current_date,
                price=current_price,
                ticker=ticker,
                exit_reason=ExitReason.END_OF_PERIOD,
                reason=reason
            )

            self._execute_exit(exit_signal, current_date)

    def _calculate_portfolio_value(
        self,
        data: Dict[str, pd.DataFrame],
        current_date: datetime
    ) -> float:
        """Calculate total portfolio value"""
        portfolio_value = self.cash

        for ticker, position in self.positions.items():
            if ticker in data and current_date in data[ticker].index:
                current_price = data[ticker].loc[current_date, 'close']
                portfolio_value += position.get_current_value(current_price)

        return portfolio_value

    def _build_result(
        self,
        strategy: Strategy,
        ticker: str,
        start_date: datetime,
        end_date: datetime
    ) -> BacktestResult:
        """Build backtest result object"""
        # Create equity curve
        equity_curve = pd.Series(
            [value for _, value in self.equity_history],
            index=[date for date, _ in self.equity_history]
        )

        # Calculate metrics
        trades_dict = [
            {
                "ticker": t.ticker,
                "entry_date": t.entry_date,
                "exit_date": t.exit_date,
                "profit_loss": t.profit_loss,
                "profit_loss_pct": t.profit_loss_pct,
                "duration_days": t.duration_days,
                "r_multiple": t.r_multiple,
                "status": "closed"
            }
            for t in self.trades
        ]

        metrics = MetricsCalculator.calculate_all_metrics(
            equity_curve,
            trades_dict,
            self.initial_capital
        )

        return BacktestResult(
            strategy_name=strategy.name,
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            initial_capital=self.initial_capital,
            final_capital=self.cash,
            trades=self.trades,
            equity_curve=equity_curve,
            metrics=metrics,
            config=strategy.get_config()
        )

    def _reset_state(self):
        """Reset engine state for new backtest"""
        self.cash = self.initial_capital
        self.positions = {}
        self.trades = []
        self.equity_history = []

    def _empty_result(self, strategy: Strategy, ticker: str) -> BacktestResult:
        """Return empty result when no data"""
        metrics = MetricsCalculator.calculate_all_metrics(
            pd.Series([self.initial_capital]),
            [],
            self.initial_capital
        )

        return BacktestResult(
            strategy_name=strategy.name,
            ticker=ticker,
            start_date=datetime.now(),
            end_date=datetime.now(),
            initial_capital=self.initial_capital,
            final_capital=self.initial_capital,
            trades=[],
            equity_curve=pd.Series([self.initial_capital]),
            metrics=metrics,
            config=strategy.get_config()
        )
