"""
Backtesting Engine
Event-driven backtesting engine with comprehensive features
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
import asyncio
import pandas as pd
import logging

from .strategy import Strategy, Signal, SignalType
from .portfolio import Portfolio, Position
from .execution import ExecutionSimulator
from .metrics import calculate_metrics, PerformanceMetrics

logger = logging.getLogger(__name__)


@dataclass
class BacktestConfig:
    """Backtest configuration"""
    strategy: Strategy
    start_date: datetime
    end_date: datetime
    initial_capital: float
    universe: List[str]  # List of tickers

    # Portfolio constraints
    max_positions: int = 10
    max_position_size: float = 0.2  # 20% of portfolio

    # Execution
    execution_simulator: Optional[ExecutionSimulator] = None

    # Data
    data_provider: Optional[Callable] = None  # Function to fetch historical data

    # Callbacks
    on_bar: Optional[Callable] = None
    on_order_filled: Optional[Callable] = None
    on_trade_closed: Optional[Callable] = None
    on_progress: Optional[Callable] = None


class BacktestEngine:
    """
    Event-driven backtesting engine
    """

    def __init__(self, config: BacktestConfig):
        """
        Initialize backtesting engine

        Args:
            config: Backtest configuration
        """
        self.config = config
        self.strategy = config.strategy
        self.portfolio = Portfolio(
            initial_capital=config.initial_capital,
            max_positions=config.max_positions,
            max_position_size=config.max_position_size,
        )

        # Execution simulator
        self.execution = config.execution_simulator or ExecutionSimulator()

        # State
        self.current_date: Optional[datetime] = None
        self.is_running = False
        self.progress = 0.0

        # Data cache
        self.historical_data: Dict[str, pd.DataFrame] = {}
        self.current_prices: Dict[str, float] = {}

        # Results
        self.performance: Optional[PerformanceMetrics] = None

    async def run(self) -> Dict:
        """
        Run the backtest

        Returns:
            Dictionary with backtest results
        """
        logger.info(f"Starting backtest: {self.config.start_date} to {self.config.end_date}")
        self.is_running = True

        try:
            # Load historical data for all tickers
            await self._load_historical_data()

            # Get all trading dates
            trading_dates = self._get_trading_dates()
            total_days = len(trading_dates)

            logger.info(f"Backtesting {len(self.config.universe)} tickers over {total_days} days")

            # Event loop: iterate through each trading day
            for i, date in enumerate(trading_dates):
                self.current_date = date

                # Process this trading day
                await self._process_trading_day(date)

                # Update progress
                self.progress = ((i + 1) / total_days) * 100
                if self.config.on_progress:
                    await self.config.on_progress(self.progress, date)

                # Check for stop signals, etc.
                if not self.is_running:
                    break

            # Close any remaining positions at the end
            await self._close_all_positions(trading_dates[-1])

            # Calculate final metrics
            self.performance = calculate_metrics(
                equity_curve=self.portfolio.get_equity_curve(),
                trades=self.portfolio.get_trades(),
                initial_capital=self.config.initial_capital,
            )

            logger.info(f"Backtest completed. Total return: {self.performance.total_return:.2f}%")

            return self._get_results()

        except Exception as e:
            logger.error(f"Backtest failed: {e}")
            raise

        finally:
            self.is_running = False

    async def _load_historical_data(self):
        """Load historical data for all tickers"""
        if self.config.data_provider is None:
            raise ValueError("Data provider not configured")

        logger.info("Loading historical data...")

        for ticker in self.config.universe:
            try:
                # Fetch data from provider
                data = await self.config.data_provider(
                    ticker,
                    self.config.start_date,
                    self.config.end_date,
                )

                if data is not None and len(data) > 0:
                    self.historical_data[ticker] = data
                else:
                    logger.warning(f"No data available for {ticker}")

            except Exception as e:
                logger.error(f"Failed to load data for {ticker}: {e}")

        logger.info(f"Loaded data for {len(self.historical_data)} tickers")

    def _get_trading_dates(self) -> List[datetime]:
        """Get all trading dates from available data"""
        all_dates = set()

        for ticker, data in self.historical_data.items():
            if "timestamp" in data.columns:
                dates = pd.to_datetime(data["timestamp"])
            elif data.index.name == "timestamp" or isinstance(data.index, pd.DatetimeIndex):
                dates = data.index
            else:
                continue

            all_dates.update(dates.tolist())

        # Sort and filter by date range
        trading_dates = sorted([
            d for d in all_dates
            if self.config.start_date <= d <= self.config.end_date
        ])

        return trading_dates

    async def _process_trading_day(self, date: datetime):
        """
        Process a single trading day

        Args:
            date: Trading date
        """
        # Update current prices
        self._update_current_prices(date)

        # Update portfolio with current prices
        self.portfolio.update_position_prices(self.current_prices)

        # Check for stop losses and take profits
        await self._check_stop_loss_take_profit(date)

        # Process each ticker
        for ticker in self.config.universe:
            if ticker not in self.historical_data:
                continue

            # Get historical data up to this date
            ticker_data = self._get_data_up_to_date(ticker, date)

            if ticker_data is None or len(ticker_data) < 2:
                continue

            # Get strategy signals
            try:
                signals = await self.strategy.on_data(
                    ticker=ticker,
                    data=ticker_data,
                    timestamp=date,
                    portfolio_value=self.portfolio.total_value,
                    cash=self.portfolio.cash,
                )

                # Process signals
                for signal in signals:
                    await self._process_signal(signal, date)

            except Exception as e:
                logger.error(f"Error processing {ticker} on {date}: {e}")

            # Callback for each bar
            if self.config.on_bar:
                await self.config.on_bar(ticker, ticker_data.iloc[-1].to_dict(), date)

        # Update portfolio metrics
        self.portfolio.update_metrics(date)

    def _update_current_prices(self, date: datetime):
        """Update current prices for all tickers"""
        for ticker, data in self.historical_data.items():
            # Get price at this date
            if "timestamp" in data.columns:
                data_at_date = data[data["timestamp"] == date]
            elif isinstance(data.index, pd.DatetimeIndex):
                data_at_date = data[data.index == date]
            else:
                continue

            if len(data_at_date) > 0:
                self.current_prices[ticker] = data_at_date.iloc[0]["close"]

    def _get_data_up_to_date(self, ticker: str, date: datetime) -> Optional[pd.DataFrame]:
        """Get historical data up to a specific date"""
        if ticker not in self.historical_data:
            return None

        data = self.historical_data[ticker]

        # Filter data up to this date
        if "timestamp" in data.columns:
            data_filtered = data[data["timestamp"] <= date].copy()
        elif isinstance(data.index, pd.DatetimeIndex):
            data_filtered = data[data.index <= date].copy()
        else:
            return None

        return data_filtered if len(data_filtered) > 0 else None

    async def _check_stop_loss_take_profit(self, date: datetime):
        """Check all positions for stop loss and take profit hits"""
        positions_to_close = []

        for ticker, position in self.portfolio.positions.items():
            if position.should_stop_out():
                positions_to_close.append((ticker, "stop_loss"))
            elif position.should_take_profit():
                positions_to_close.append((ticker, "take_profit"))

        # Close positions
        for ticker, reason in positions_to_close:
            if ticker in self.current_prices:
                await self._close_position(ticker, self.current_prices[ticker], date, reason)

    async def _process_signal(self, signal: Signal, date: datetime):
        """
        Process a trading signal

        Args:
            signal: Trading signal
            date: Current date
        """
        if signal.type == SignalType.BUY:
            await self._process_buy_signal(signal, date)
        elif signal.type in [SignalType.SELL, SignalType.CLOSE]:
            await self._process_sell_signal(signal, date)

    async def _process_buy_signal(self, signal: Signal, date: datetime):
        """Process a buy signal"""
        ticker = signal.ticker

        # Skip if we already have a position
        if self.portfolio.has_position(ticker):
            return

        # Get current price
        if ticker not in self.current_prices:
            logger.warning(f"No price data for {ticker} on {date}")
            return

        current_price = self.current_prices[ticker]

        # Calculate position size
        try:
            quantity = await self.strategy.calculate_position_size(
                signal=signal,
                portfolio_value=self.portfolio.total_value,
                cash=self.portfolio.cash,
                current_price=current_price,
            )

            if quantity <= 0:
                return

            # Get volume for execution simulation
            ticker_data = self._get_data_up_to_date(ticker, date)
            volume = ticker_data.iloc[-1]["volume"] if ticker_data is not None and "volume" in ticker_data.columns else None

            # Execute order
            execution_result = self.execution.execute_order(
                quantity=quantity,
                price=current_price,
                is_buy=True,
                volume=volume,
            )

            # Open position
            position = self.portfolio.open_position(
                ticker=ticker,
                quantity=execution_result["filled_quantity"],
                price=execution_result["final_price"],
                timestamp=date,
                commission=execution_result["commission"],
                slippage=execution_result["slippage"],
                stop_loss=signal.stop_loss,
                take_profit=signal.take_profit,
                entry_signal=signal.reason,
            )

            if position:
                # Notify strategy
                await self.strategy.on_order_filled(
                    signal=signal,
                    filled_price=execution_result["final_price"],
                    filled_quantity=execution_result["filled_quantity"],
                    commission=execution_result["commission"],
                    slippage=execution_result["slippage"],
                )

                # Callback
                if self.config.on_order_filled:
                    await self.config.on_order_filled(position, execution_result)

                logger.debug(f"Opened position: {ticker} x {quantity} @ {execution_result['final_price']:.2f}")

        except Exception as e:
            logger.error(f"Error processing buy signal for {ticker}: {e}")

    async def _process_sell_signal(self, signal: Signal, date: datetime):
        """Process a sell signal"""
        ticker = signal.ticker

        if not self.portfolio.has_position(ticker):
            return

        if ticker not in self.current_prices:
            return

        current_price = self.current_prices[ticker]
        await self._close_position(ticker, current_price, date, signal.reason)

    async def _close_position(
        self,
        ticker: str,
        price: float,
        date: datetime,
        reason: str,
    ):
        """Close a position"""
        position = self.portfolio.get_position(ticker)
        if not position:
            return

        # Get volume for execution simulation
        ticker_data = self._get_data_up_to_date(ticker, date)
        volume = ticker_data.iloc[-1]["volume"] if ticker_data is not None and "volume" in ticker_data.columns else None

        # Execute order
        execution_result = self.execution.execute_order(
            quantity=position.quantity,
            price=price,
            is_buy=False,
            volume=volume,
        )

        # Close position
        trade = self.portfolio.close_position(
            ticker=ticker,
            price=execution_result["final_price"],
            timestamp=date,
            commission=execution_result["commission"],
            slippage=execution_result["slippage"],
            exit_signal=reason,
        )

        if trade:
            # Callback
            if self.config.on_trade_closed:
                await self.config.on_trade_closed(trade)

            logger.debug(f"Closed position: {ticker} - P&L: {trade['net_pnl']:.2f} ({trade['pnl_pct']:.2f}%)")

    async def _close_all_positions(self, date: datetime):
        """Close all remaining positions at the end"""
        tickers_to_close = list(self.portfolio.positions.keys())

        for ticker in tickers_to_close:
            if ticker in self.current_prices:
                await self._close_position(ticker, self.current_prices[ticker], date, "end_of_backtest")

    def _get_results(self) -> Dict:
        """Get backtest results"""
        return {
            "config": {
                "strategy": self.strategy.name,
                "start_date": self.config.start_date.isoformat(),
                "end_date": self.config.end_date.isoformat(),
                "initial_capital": self.config.initial_capital,
                "universe": self.config.universe,
            },
            "portfolio": self.portfolio.get_summary(),
            "performance": {
                "total_return": self.performance.total_return,
                "annualized_return": self.performance.annualized_return,
                "sharpe_ratio": self.performance.sharpe_ratio,
                "sortino_ratio": self.performance.sortino_ratio,
                "calmar_ratio": self.performance.calmar_ratio,
                "max_drawdown": self.performance.max_drawdown,
                "volatility": self.performance.volatility,
                "win_rate": self.performance.win_rate,
                "profit_factor": self.performance.profit_factor,
                "total_trades": self.performance.total_trades,
                "expectancy": self.performance.expectancy,
            } if self.performance else {},
            "equity_curve": self.portfolio.get_equity_curve().to_dict(orient="records"),
            "trades": self.portfolio.get_trades().to_dict(orient="records"),
        }

    def stop(self):
        """Stop the backtest"""
        self.is_running = False

    def get_equity_curve(self) -> pd.DataFrame:
        """Get equity curve"""
        return self.portfolio.get_equity_curve()

    def get_trades(self) -> pd.DataFrame:
        """Get all trades"""
        return self.portfolio.get_trades()

    def get_performance(self) -> Optional[PerformanceMetrics]:
        """Get performance metrics"""
        return self.performance
