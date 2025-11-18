"""
Portfolio Management
Handles positions, cash, and portfolio-level operations
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd


@dataclass
class Position:
    """Represents a position in a security"""
    ticker: str
    quantity: int
    entry_price: float
    entry_date: datetime
    current_price: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    entry_commission: float = 0.0
    pattern_type: Optional[str] = None
    entry_signal: Optional[str] = None
    metadata: Dict = field(default_factory=dict)

    @property
    def market_value(self) -> float:
        """Current market value of position"""
        return self.quantity * self.current_price

    @property
    def cost_basis(self) -> float:
        """Total cost including commission"""
        return (self.quantity * self.entry_price) + self.entry_commission

    @property
    def unrealized_pnl(self) -> float:
        """Unrealized profit/loss"""
        return self.market_value - self.cost_basis

    @property
    def unrealized_pnl_pct(self) -> float:
        """Unrealized profit/loss percentage"""
        if self.cost_basis == 0:
            return 0.0
        return (self.unrealized_pnl / self.cost_basis) * 100

    @property
    def mae(self) -> float:
        """Maximum Adverse Excursion - track lowest price"""
        return self.metadata.get("mae", 0.0)

    @property
    def mfe(self) -> float:
        """Maximum Favorable Excursion - track highest price"""
        return self.metadata.get("mfe", 0.0)

    def update_price(self, new_price: float):
        """Update current price and MAE/MFE"""
        self.current_price = new_price

        # Update MAE (maximum loss)
        current_mae = self.entry_price - new_price
        if current_mae > self.mae:
            self.metadata["mae"] = current_mae

        # Update MFE (maximum gain)
        current_mfe = new_price - self.entry_price
        if current_mfe > self.mfe:
            self.metadata["mfe"] = current_mfe

    def should_stop_out(self) -> bool:
        """Check if stop loss hit"""
        if self.stop_loss is None:
            return False
        return self.current_price <= self.stop_loss

    def should_take_profit(self) -> bool:
        """Check if take profit hit"""
        if self.take_profit is None:
            return False
        return self.current_price >= self.take_profit


class Portfolio:
    """
    Portfolio manager for backtesting
    Tracks positions, cash, and portfolio value
    """

    def __init__(
        self,
        initial_capital: float,
        max_positions: int = 10,
        max_position_size: float = 0.2,  # 20% of portfolio
    ):
        """
        Initialize portfolio

        Args:
            initial_capital: Starting capital
            max_positions: Maximum number of concurrent positions
            max_position_size: Maximum position size as fraction of portfolio
        """
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.max_positions = max_positions
        self.max_position_size = max_position_size

        # Positions
        self.positions: Dict[str, Position] = {}
        self.closed_positions: List[Dict] = []

        # Performance tracking
        self.equity_curve: List[Dict] = []
        self.trades: List[Dict] = []
        self.daily_returns: List[float] = []

        # Running statistics
        self.peak_value = initial_capital
        self.max_drawdown = 0.0
        self.total_commissions = 0.0
        self.total_slippage = 0.0

    @property
    def positions_value(self) -> float:
        """Total value of all positions"""
        return sum(pos.market_value for pos in self.positions.values())

    @property
    def total_value(self) -> float:
        """Total portfolio value (cash + positions)"""
        return self.cash + self.positions_value

    @property
    def total_return(self) -> float:
        """Total return percentage"""
        return ((self.total_value - self.initial_capital) / self.initial_capital) * 100

    @property
    def current_drawdown(self) -> float:
        """Current drawdown from peak"""
        if self.peak_value == 0:
            return 0.0
        return ((self.peak_value - self.total_value) / self.peak_value) * 100

    @property
    def num_positions(self) -> int:
        """Number of open positions"""
        return len(self.positions)

    @property
    def buying_power(self) -> float:
        """Available buying power"""
        return self.cash

    def can_open_position(self, ticker: str, value: float) -> bool:
        """
        Check if we can open a new position

        Args:
            ticker: Stock ticker
            value: Position value

        Returns:
            True if position can be opened
        """
        # Check if already have position
        if ticker in self.positions:
            return False

        # Check max positions
        if len(self.positions) >= self.max_positions:
            return False

        # Check if enough cash
        if value > self.cash:
            return False

        # Check max position size
        max_value = self.total_value * self.max_position_size
        if value > max_value:
            return False

        return True

    def open_position(
        self,
        ticker: str,
        quantity: int,
        price: float,
        timestamp: datetime,
        commission: float = 0.0,
        slippage: float = 0.0,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        pattern_type: Optional[str] = None,
        entry_signal: Optional[str] = None,
    ) -> Optional[Position]:
        """
        Open a new position

        Args:
            ticker: Stock ticker
            quantity: Number of shares
            price: Entry price (including slippage)
            timestamp: Entry timestamp
            commission: Commission paid
            slippage: Slippage cost
            stop_loss: Stop loss price
            take_profit: Take profit price
            pattern_type: Pattern type (VCP, etc.)
            entry_signal: Entry signal description

        Returns:
            Position object if successful, None otherwise
        """
        total_cost = (quantity * price) + commission + slippage

        if not self.can_open_position(ticker, total_cost):
            return None

        # Deduct from cash
        self.cash -= total_cost

        # Create position
        position = Position(
            ticker=ticker,
            quantity=quantity,
            entry_price=price,
            entry_date=timestamp,
            current_price=price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            entry_commission=commission,
            pattern_type=pattern_type,
            entry_signal=entry_signal,
            metadata={"mae": 0.0, "mfe": 0.0, "slippage": slippage},
        )

        self.positions[ticker] = position

        # Track costs
        self.total_commissions += commission
        self.total_slippage += slippage

        return position

    def close_position(
        self,
        ticker: str,
        price: float,
        timestamp: datetime,
        commission: float = 0.0,
        slippage: float = 0.0,
        exit_signal: Optional[str] = None,
    ) -> Optional[Dict]:
        """
        Close an existing position

        Args:
            ticker: Stock ticker
            price: Exit price (including slippage)
            timestamp: Exit timestamp
            commission: Commission paid
            slippage: Slippage cost
            exit_signal: Exit signal description

        Returns:
            Trade result dictionary
        """
        if ticker not in self.positions:
            return None

        position = self.positions[ticker]

        # Calculate proceeds
        gross_proceeds = position.quantity * price
        net_proceeds = gross_proceeds - commission - slippage

        # Add to cash
        self.cash += net_proceeds

        # Calculate P&L
        gross_pnl = gross_proceeds - (position.quantity * position.entry_price)
        net_pnl = net_proceeds - position.cost_basis - slippage
        pnl_pct = (net_pnl / position.cost_basis) * 100 if position.cost_basis > 0 else 0.0

        # Calculate R-multiple if stop loss was set
        r_multiple = None
        if position.stop_loss:
            initial_risk = abs(position.entry_price - position.stop_loss) * position.quantity
            if initial_risk > 0:
                r_multiple = net_pnl / initial_risk

        # Days held
        days_held = (timestamp - position.entry_date).days

        # Create trade record
        trade = {
            "ticker": ticker,
            "entry_date": position.entry_date,
            "exit_date": timestamp,
            "entry_price": position.entry_price,
            "exit_price": price,
            "quantity": position.quantity,
            "gross_pnl": gross_pnl,
            "net_pnl": net_pnl,
            "pnl_pct": pnl_pct,
            "r_multiple": r_multiple,
            "days_held": days_held,
            "entry_commission": position.entry_commission,
            "exit_commission": commission,
            "total_slippage": position.metadata.get("slippage", 0.0) + slippage,
            "mae": position.mae,
            "mfe": position.mfe,
            "pattern_type": position.pattern_type,
            "entry_signal": position.entry_signal,
            "exit_signal": exit_signal,
            "stop_loss": position.stop_loss,
            "take_profit": position.take_profit,
        }

        # Store trade
        self.trades.append(trade)
        self.closed_positions.append(trade)

        # Track costs
        self.total_commissions += commission
        self.total_slippage += slippage

        # Remove position
        del self.positions[ticker]

        return trade

    def update_position_prices(self, prices: Dict[str, float]):
        """
        Update prices for all positions

        Args:
            prices: Dictionary of ticker -> current price
        """
        for ticker, position in self.positions.items():
            if ticker in prices:
                position.update_price(prices[ticker])

    def update_metrics(self, timestamp: datetime):
        """
        Update portfolio metrics

        Args:
            timestamp: Current timestamp
        """
        total_value = self.total_value

        # Update peak value and max drawdown
        if total_value > self.peak_value:
            self.peak_value = total_value

        current_dd = self.current_drawdown
        if current_dd > self.max_drawdown:
            self.max_drawdown = current_dd

        # Record equity point
        equity_point = {
            "timestamp": timestamp,
            "total_value": total_value,
            "cash": self.cash,
            "positions_value": self.positions_value,
            "num_positions": self.num_positions,
            "drawdown": current_dd,
        }
        self.equity_curve.append(equity_point)

        # Calculate daily return
        if len(self.equity_curve) > 1:
            prev_value = self.equity_curve[-2]["total_value"]
            daily_return = ((total_value - prev_value) / prev_value) * 100 if prev_value > 0 else 0.0
            self.daily_returns.append(daily_return)

    def get_position(self, ticker: str) -> Optional[Position]:
        """Get position for a ticker"""
        return self.positions.get(ticker)

    def has_position(self, ticker: str) -> bool:
        """Check if we have a position"""
        return ticker in self.positions

    def get_equity_curve(self) -> pd.DataFrame:
        """Get equity curve as DataFrame"""
        if not self.equity_curve:
            return pd.DataFrame()

        df = pd.DataFrame(self.equity_curve)
        df.set_index("timestamp", inplace=True)
        return df

    def get_trades(self) -> pd.DataFrame:
        """Get all trades as DataFrame"""
        if not self.trades:
            return pd.DataFrame()

        return pd.DataFrame(self.trades)

    def get_summary(self) -> Dict:
        """Get portfolio summary statistics"""
        trades_df = self.get_trades()

        if len(trades_df) == 0:
            return {
                "total_value": self.total_value,
                "total_return": self.total_return,
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0.0,
                "max_drawdown": self.max_drawdown,
                "total_commissions": self.total_commissions,
                "total_slippage": self.total_slippage,
            }

        winning_trades = len(trades_df[trades_df["net_pnl"] > 0])
        losing_trades = len(trades_df[trades_df["net_pnl"] < 0])
        win_rate = (winning_trades / len(trades_df)) * 100 if len(trades_df) > 0 else 0.0

        avg_win = trades_df[trades_df["net_pnl"] > 0]["net_pnl"].mean() if winning_trades > 0 else 0.0
        avg_loss = trades_df[trades_df["net_pnl"] < 0]["net_pnl"].mean() if losing_trades > 0 else 0.0
        profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else 0.0

        return {
            "initial_capital": self.initial_capital,
            "total_value": self.total_value,
            "total_return": self.total_return,
            "cash": self.cash,
            "positions_value": self.positions_value,
            "num_positions": self.num_positions,
            "total_trades": len(trades_df),
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": win_rate,
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "profit_factor": profit_factor,
            "max_drawdown": self.max_drawdown,
            "total_commissions": self.total_commissions,
            "total_slippage": self.total_slippage,
            "largest_win": trades_df["net_pnl"].max() if len(trades_df) > 0 else 0.0,
            "largest_loss": trades_df["net_pnl"].min() if len(trades_df) > 0 else 0.0,
            "avg_days_held": trades_df["days_held"].mean() if len(trades_df) > 0 else 0.0,
        }
