"""
Base Broker Interface

Defines the abstract base class and data models for all broker integrations.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class BrokerType(str, Enum):
    """Supported broker types"""
    ALPACA = "alpaca"
    TD_AMERITRADE = "td_ameritrade"
    INTERACTIVE_BROKERS = "interactive_brokers"
    TRADESTATION = "tradestation"


class OrderType(str, Enum):
    """Order types supported across brokers"""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"
    TRAILING_STOP = "trailing_stop"


class OrderSide(str, Enum):
    """Order side - buy or sell"""
    BUY = "buy"
    SELL = "sell"


class OrderStatus(str, Enum):
    """Order status across lifecycle"""
    PENDING = "pending"
    NEW = "new"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELED = "canceled"
    REJECTED = "rejected"
    EXPIRED = "expired"


class TimeInForce(str, Enum):
    """Time in force options"""
    DAY = "day"  # Good for day
    GTC = "gtc"  # Good till canceled
    IOC = "ioc"  # Immediate or cancel
    FOK = "fok"  # Fill or kill


class Order(BaseModel):
    """Order model"""
    order_id: Optional[str] = None
    client_order_id: Optional[str] = None
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    filled_qty: float = 0.0
    price: Optional[float] = None  # For limit orders
    stop_price: Optional[float] = None  # For stop orders
    trail_amount: Optional[float] = None  # For trailing stops
    trail_percent: Optional[float] = None  # For trailing stops
    time_in_force: TimeInForce = TimeInForce.DAY
    status: OrderStatus = OrderStatus.PENDING
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    filled_at: Optional[datetime] = None
    avg_fill_price: Optional[float] = None

    # Bracket order fields
    take_profit_price: Optional[float] = None
    stop_loss_price: Optional[float] = None

    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Position(BaseModel):
    """Position model"""
    symbol: str
    quantity: float
    avg_entry_price: float
    current_price: float
    market_value: float
    cost_basis: float
    unrealized_pl: float
    unrealized_pl_percent: float
    side: OrderSide  # Long (buy) or short (sell)

    # Additional fields
    asset_class: str = "equity"
    exchange: Optional[str] = None
    lastday_price: Optional[float] = None
    change_today: Optional[float] = None


class Account(BaseModel):
    """Account information model"""
    account_id: str
    broker: BrokerType

    # Balances
    cash: float
    buying_power: float
    portfolio_value: float
    equity: float

    # P&L
    last_equity: float
    unrealized_pl: float
    realized_pl_today: float

    # Account status
    pattern_day_trader: bool = False
    trading_blocked: bool = False
    account_blocked: bool = False

    # Margin (if applicable)
    multiplier: float = 1.0  # Buying power multiplier
    initial_margin: Optional[float] = None
    maintenance_margin: Optional[float] = None

    # Metadata
    created_at: Optional[datetime] = None
    currency: str = "USD"


class ExecutionReport(BaseModel):
    """Execution report for analytics"""
    order_id: str
    symbol: str
    side: OrderSide
    quantity: float
    filled_qty: float
    avg_fill_price: float
    limit_price: Optional[float] = None

    # Execution quality metrics
    slippage: Optional[float] = None  # Difference from expected price
    slippage_percent: Optional[float] = None
    slippage_bps: Optional[int] = None  # Basis points

    # Timing metrics
    order_time: datetime
    fill_time: datetime
    execution_duration_ms: int

    # Venue information
    exchange: Optional[str] = None
    execution_venue: Optional[str] = None

    # Fill quality
    fill_quality_score: Optional[float] = None  # 0-100
    price_improvement: Optional[float] = None

    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseBroker(ABC):
    """
    Abstract base class for all broker integrations.

    All broker implementations must inherit from this class and implement
    the abstract methods.
    """

    def __init__(self, credentials: Dict[str, str], paper_trading: bool = True):
        """
        Initialize broker connection.

        Args:
            credentials: API credentials (keys, tokens, etc.)
            paper_trading: Whether to use paper trading (default: True)
        """
        self.credentials = credentials
        self.paper_trading = paper_trading
        self._connected = False

    @property
    @abstractmethod
    def broker_type(self) -> BrokerType:
        """Return the broker type"""
        pass

    @abstractmethod
    async def connect(self) -> bool:
        """
        Establish connection to broker.

        Returns:
            bool: True if connection successful
        """
        pass

    @abstractmethod
    async def disconnect(self) -> bool:
        """
        Disconnect from broker.

        Returns:
            bool: True if disconnection successful
        """
        pass

    @abstractmethod
    async def get_account(self) -> Account:
        """
        Get account information.

        Returns:
            Account: Account details including balances and P&L
        """
        pass

    @abstractmethod
    async def get_positions(self) -> List[Position]:
        """
        Get all open positions.

        Returns:
            List[Position]: List of open positions
        """
        pass

    @abstractmethod
    async def get_position(self, symbol: str) -> Optional[Position]:
        """
        Get position for specific symbol.

        Args:
            symbol: Stock symbol

        Returns:
            Optional[Position]: Position or None if not found
        """
        pass

    @abstractmethod
    async def place_order(self, order: Order) -> Order:
        """
        Place an order.

        Args:
            order: Order to place

        Returns:
            Order: Updated order with order_id and status
        """
        pass

    @abstractmethod
    async def place_bracket_order(
        self,
        symbol: str,
        side: OrderSide,
        quantity: float,
        entry_price: Optional[float],
        take_profit_price: float,
        stop_loss_price: float,
        time_in_force: TimeInForce = TimeInForce.DAY,
    ) -> List[Order]:
        """
        Place a bracket order (entry + take profit + stop loss).

        Args:
            symbol: Stock symbol
            side: Buy or sell
            quantity: Number of shares
            entry_price: Entry price (None for market order)
            take_profit_price: Take profit price
            stop_loss_price: Stop loss price
            time_in_force: Order duration

        Returns:
            List[Order]: List of orders (entry, take profit, stop loss)
        """
        pass

    @abstractmethod
    async def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an order.

        Args:
            order_id: Order ID to cancel

        Returns:
            bool: True if cancellation successful
        """
        pass

    @abstractmethod
    async def get_order(self, order_id: str) -> Optional[Order]:
        """
        Get order details.

        Args:
            order_id: Order ID

        Returns:
            Optional[Order]: Order or None if not found
        """
        pass

    @abstractmethod
    async def get_orders(
        self,
        status: Optional[OrderStatus] = None,
        limit: int = 100,
    ) -> List[Order]:
        """
        Get orders.

        Args:
            status: Filter by status (None for all)
            limit: Maximum number of orders to return

        Returns:
            List[Order]: List of orders
        """
        pass

    @abstractmethod
    async def get_current_price(self, symbol: str) -> float:
        """
        Get current market price for symbol.

        Args:
            symbol: Stock symbol

        Returns:
            float: Current price
        """
        pass

    def is_connected(self) -> bool:
        """Check if broker is connected"""
        return self._connected

    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()
