"""
Order Management Module for Paper Trading Automation

Handles bracket orders, trailing stops, scale in/out logic, and time-based exits.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from enum import Enum
from uuid import uuid4
import logging

logger = logging.getLogger(__name__)


class OrderType(Enum):
    """Order types"""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"
    TRAILING_STOP = "trailing_stop"


class OrderSide(Enum):
    """Order side"""
    BUY = "buy"
    SELL = "sell"


class OrderStatus(Enum):
    """Order status"""
    PENDING = "pending"
    SUBMITTED = "submitted"
    PARTIAL = "partial"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class OrderTimeInForce(Enum):
    """Time in force"""
    DAY = "day"
    GTC = "gtc"  # Good till cancelled
    IOC = "ioc"  # Immediate or cancel
    FOK = "fok"  # Fill or kill


@dataclass
class Order:
    """Individual order"""
    order_id: str
    ticker: str
    order_type: OrderType
    side: OrderSide
    quantity: int
    status: OrderStatus = OrderStatus.PENDING

    # Pricing
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    filled_price: Optional[float] = None

    # Quantities
    filled_quantity: int = 0
    remaining_quantity: int = 0

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    submitted_at: Optional[datetime] = None
    filled_at: Optional[datetime] = None

    # Order attributes
    time_in_force: OrderTimeInForce = OrderTimeInForce.DAY
    parent_order_id: Optional[str] = None
    related_order_ids: List[str] = field(default_factory=list)

    # Metadata
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.remaining_quantity = self.quantity

    @property
    def is_filled(self) -> bool:
        """Check if order is completely filled"""
        return self.status == OrderStatus.FILLED and self.filled_quantity == self.quantity

    @property
    def is_active(self) -> bool:
        """Check if order is still active"""
        return self.status in [OrderStatus.PENDING, OrderStatus.SUBMITTED, OrderStatus.PARTIAL]

    @property
    def fill_percentage(self) -> float:
        """Calculate fill percentage"""
        return (self.filled_quantity / self.quantity * 100) if self.quantity > 0 else 0.0


@dataclass
class BracketOrder:
    """
    Bracket order with entry, stop loss, and take profit
    """
    bracket_id: str
    ticker: str

    # Entry order
    entry_order: Order

    # Exit orders
    stop_loss_order: Order
    take_profit_order: Order

    # Optional: Additional take profit orders for scaling out
    additional_targets: List[Order] = field(default_factory=list)

    # Status
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    # Metadata
    notes: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def all_orders(self) -> List[Order]:
        """Get all orders in the bracket"""
        return [self.entry_order, self.stop_loss_order, self.take_profit_order] + self.additional_targets

    @property
    def status(self) -> str:
        """Get overall bracket status"""
        if self.entry_order.status == OrderStatus.FILLED:
            if self.stop_loss_order.is_filled or self.take_profit_order.is_filled:
                return "closed"
            return "open"
        elif self.entry_order.status == OrderStatus.CANCELLED:
            return "cancelled"
        else:
            return "pending"


@dataclass
class TrailingStop:
    """Trailing stop configuration"""
    order_id: str
    ticker: str
    side: OrderSide
    quantity: int

    # Trailing parameters
    trail_type: str = "percent"  # "percent" or "amount"
    trail_value: float = 0.0  # Percentage (e.g., 5.0 for 5%) or dollar amount

    # State tracking
    highest_price: float = 0.0  # For long positions
    lowest_price: float = float('inf')  # For short positions
    current_stop_price: float = 0.0

    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    def update(self, current_price: float) -> bool:
        """
        Update trailing stop based on current price

        Returns:
            True if stop was triggered, False otherwise
        """
        if not self.is_active:
            return False

        # For long positions (sell side)
        if self.side == OrderSide.SELL:
            # Update highest price
            if current_price > self.highest_price:
                self.highest_price = current_price

                # Calculate new stop price
                if self.trail_type == "percent":
                    self.current_stop_price = self.highest_price * (1 - self.trail_value / 100)
                else:
                    self.current_stop_price = self.highest_price - self.trail_value

            # Check if stop triggered
            if current_price <= self.current_stop_price:
                self.is_active = False
                return True

        # For short positions (buy side)
        else:
            # Update lowest price
            if current_price < self.lowest_price:
                self.lowest_price = current_price

                # Calculate new stop price
                if self.trail_type == "percent":
                    self.current_stop_price = self.lowest_price * (1 + self.trail_value / 100)
                else:
                    self.current_stop_price = self.lowest_price + self.trail_value

            # Check if stop triggered
            if current_price >= self.current_stop_price:
                self.is_active = False
                return True

        return False


@dataclass
class ScaleOutPlan:
    """Scale out plan for taking partial profits"""
    ticker: str
    total_quantity: int
    scale_levels: List[Dict[str, Any]]  # [{"price": 100, "percentage": 50}, ...]
    executed_scales: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def remaining_percentage(self) -> float:
        """Calculate remaining position percentage"""
        executed_pct = sum(s["percentage"] for s in self.executed_scales)
        return 100.0 - executed_pct

    @property
    def remaining_quantity(self) -> int:
        """Calculate remaining quantity"""
        return int(self.total_quantity * self.remaining_percentage / 100)


class OrderManager:
    """
    Manage orders for paper trading including bracket orders,
    trailing stops, and scale in/out logic
    """

    def __init__(self):
        self.orders: Dict[str, Order] = {}
        self.bracket_orders: Dict[str, BracketOrder] = {}
        self.trailing_stops: Dict[str, TrailingStop] = {}
        self.scale_out_plans: Dict[str, ScaleOutPlan] = {}
        self.logger = logging.getLogger(__name__)

    def create_bracket_order(
        self,
        ticker: str,
        quantity: int,
        entry_price: float,
        stop_loss_price: float,
        take_profit_price: float,
        entry_type: OrderType = OrderType.LIMIT,
        additional_targets: Optional[List[Dict[str, Any]]] = None,
        notes: str = ""
    ) -> BracketOrder:
        """
        Create a bracket order (entry + stop loss + take profit)

        Args:
            ticker: Stock ticker
            quantity: Number of shares
            entry_price: Entry price
            stop_loss_price: Stop loss price
            take_profit_price: Take profit price
            entry_type: Type of entry order (MARKET or LIMIT)
            additional_targets: Additional profit targets for scaling out
                               [{"price": 105.0, "quantity": 50}, ...]
            notes: Order notes

        Returns:
            BracketOrder object
        """
        bracket_id = str(uuid4())

        # Create entry order
        entry_order = Order(
            order_id=f"{bracket_id}_ENTRY",
            ticker=ticker,
            order_type=entry_type,
            side=OrderSide.BUY,
            quantity=quantity,
            limit_price=entry_price if entry_type == OrderType.LIMIT else None,
            time_in_force=OrderTimeInForce.DAY,
            notes=f"Entry order for bracket {bracket_id}"
        )

        # Create stop loss order (child of entry)
        stop_loss_order = Order(
            order_id=f"{bracket_id}_STOP",
            ticker=ticker,
            order_type=OrderType.STOP,
            side=OrderSide.SELL,
            quantity=quantity,
            stop_price=stop_loss_price,
            time_in_force=OrderTimeInForce.GTC,
            parent_order_id=entry_order.order_id,
            notes=f"Stop loss for bracket {bracket_id}"
        )

        # Create take profit order (child of entry)
        take_profit_order = Order(
            order_id=f"{bracket_id}_TARGET",
            ticker=ticker,
            order_type=OrderType.LIMIT,
            side=OrderSide.SELL,
            quantity=quantity,
            limit_price=take_profit_price,
            time_in_force=OrderTimeInForce.GTC,
            parent_order_id=entry_order.order_id,
            notes=f"Take profit for bracket {bracket_id}"
        )

        # Link orders
        entry_order.related_order_ids = [stop_loss_order.order_id, take_profit_order.order_id]
        stop_loss_order.related_order_ids = [take_profit_order.order_id]
        take_profit_order.related_order_ids = [stop_loss_order.order_id]

        # Create additional target orders
        target_orders = []
        if additional_targets:
            for i, target in enumerate(additional_targets):
                target_order = Order(
                    order_id=f"{bracket_id}_TARGET_{i+1}",
                    ticker=ticker,
                    order_type=OrderType.LIMIT,
                    side=OrderSide.SELL,
                    quantity=target["quantity"],
                    limit_price=target["price"],
                    time_in_force=OrderTimeInForce.GTC,
                    parent_order_id=entry_order.order_id,
                    notes=f"Additional target {i+1} for bracket {bracket_id}"
                )
                target_orders.append(target_order)
                self.orders[target_order.order_id] = target_order

        # Create bracket order
        bracket = BracketOrder(
            bracket_id=bracket_id,
            ticker=ticker,
            entry_order=entry_order,
            stop_loss_order=stop_loss_order,
            take_profit_order=take_profit_order,
            additional_targets=target_orders,
            notes=notes,
            metadata={
                "entry_price": entry_price,
                "stop_price": stop_loss_price,
                "target_price": take_profit_price
            }
        )

        # Store orders
        self.orders[entry_order.order_id] = entry_order
        self.orders[stop_loss_order.order_id] = stop_loss_order
        self.orders[take_profit_order.order_id] = take_profit_order
        self.bracket_orders[bracket_id] = bracket

        self.logger.info(
            f"Created bracket order {bracket_id} for {ticker}: "
            f"Entry=${entry_price:.2f}, Stop=${stop_loss_price:.2f}, Target=${take_profit_price:.2f}"
        )

        return bracket

    def create_trailing_stop(
        self,
        ticker: str,
        quantity: int,
        trail_type: str = "percent",
        trail_value: float = 5.0,
        initial_price: Optional[float] = None
    ) -> TrailingStop:
        """
        Create a trailing stop order

        Args:
            ticker: Stock ticker
            quantity: Number of shares
            trail_type: "percent" or "amount"
            trail_value: Trail percentage or dollar amount
            initial_price: Initial price to start trailing from

        Returns:
            TrailingStop object
        """
        order_id = f"TRAIL_{ticker}_{int(datetime.now().timestamp())}"

        trailing_stop = TrailingStop(
            order_id=order_id,
            ticker=ticker,
            side=OrderSide.SELL,  # Assuming long position
            quantity=quantity,
            trail_type=trail_type,
            trail_value=trail_value,
            highest_price=initial_price or 0.0,
            current_stop_price=0.0 if not initial_price else (
                initial_price * (1 - trail_value / 100) if trail_type == "percent"
                else initial_price - trail_value
            )
        )

        self.trailing_stops[order_id] = trailing_stop

        self.logger.info(
            f"Created trailing stop for {ticker}: {trail_type} trail of {trail_value}"
        )

        return trailing_stop

    def create_scale_out_plan(
        self,
        ticker: str,
        quantity: int,
        targets: List[Dict[str, Any]]
    ) -> ScaleOutPlan:
        """
        Create a scale-out plan for taking partial profits

        Args:
            ticker: Stock ticker
            quantity: Total position size
            targets: List of targets: [{"price": 105.0, "percentage": 50}, ...]

        Returns:
            ScaleOutPlan object
        """
        plan_id = f"SCALE_{ticker}_{int(datetime.now().timestamp())}"

        plan = ScaleOutPlan(
            ticker=ticker,
            total_quantity=quantity,
            scale_levels=targets
        )

        self.scale_out_plans[plan_id] = plan

        self.logger.info(
            f"Created scale-out plan for {ticker} with {len(targets)} levels"
        )

        return plan

    def fill_order(
        self,
        order_id: str,
        filled_price: float,
        filled_quantity: Optional[int] = None,
        partial: bool = False
    ) -> bool:
        """
        Fill an order (simulate execution)

        Args:
            order_id: Order ID
            filled_price: Execution price
            filled_quantity: Quantity filled (None = full fill)
            partial: Whether this is a partial fill

        Returns:
            True if successful, False otherwise
        """
        if order_id not in self.orders:
            self.logger.error(f"Order {order_id} not found")
            return False

        order = self.orders[order_id]

        # Update filled quantities
        if filled_quantity is None:
            filled_quantity = order.remaining_quantity

        order.filled_quantity += filled_quantity
        order.remaining_quantity -= filled_quantity
        order.filled_price = filled_price

        # Update status
        if order.remaining_quantity == 0:
            order.status = OrderStatus.FILLED
            order.filled_at = datetime.now()
        else:
            order.status = OrderStatus.PARTIAL

        self.logger.info(
            f"Filled order {order_id}: {filled_quantity} shares @ ${filled_price:.2f} "
            f"({order.fill_percentage:.1f}% filled)"
        )

        return True

    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        if order_id not in self.orders:
            return False

        order = self.orders[order_id]
        order.status = OrderStatus.CANCELLED

        self.logger.info(f"Cancelled order {order_id}")
        return True

    def update_trailing_stops(self, ticker: str, current_price: float) -> List[str]:
        """
        Update all trailing stops for a ticker

        Args:
            ticker: Stock ticker
            current_price: Current market price

        Returns:
            List of order IDs that were triggered
        """
        triggered = []

        for order_id, trailing_stop in self.trailing_stops.items():
            if trailing_stop.ticker == ticker and trailing_stop.is_active:
                if trailing_stop.update(current_price):
                    triggered.append(order_id)
                    self.logger.info(
                        f"Trailing stop triggered for {ticker} @ ${current_price:.2f}"
                    )

        return triggered

    def check_time_based_exits(self, max_days_in_trade: int = 30) -> List[str]:
        """
        Check for time-based exits

        Args:
            max_days_in_trade: Maximum days to hold a position

        Returns:
            List of order IDs that should be closed
        """
        exits = []
        cutoff_date = datetime.now() - timedelta(days=max_days_in_trade)

        for order_id, order in self.orders.items():
            if (order.is_filled and
                order.side == OrderSide.BUY and
                order.filled_at and
                order.filled_at < cutoff_date):
                exits.append(order_id)
                self.logger.info(
                    f"Time-based exit triggered for {order.ticker} (held {max_days_in_trade}+ days)"
                )

        return exits

    def get_active_orders(self, ticker: Optional[str] = None) -> List[Order]:
        """Get all active orders, optionally filtered by ticker"""
        orders = [o for o in self.orders.values() if o.is_active]
        if ticker:
            orders = [o for o in orders if o.ticker == ticker]
        return orders

    def get_bracket_order(self, bracket_id: str) -> Optional[BracketOrder]:
        """Get bracket order by ID"""
        return self.bracket_orders.get(bracket_id)

    def get_order(self, order_id: str) -> Optional[Order]:
        """Get order by ID"""
        return self.orders.get(order_id)

    def get_stats(self) -> Dict[str, Any]:
        """Get order management statistics"""
        total_orders = len(self.orders)
        active_orders = len([o for o in self.orders.values() if o.is_active])
        filled_orders = len([o for o in self.orders.values() if o.is_filled])
        active_brackets = len([b for b in self.bracket_orders.values() if b.is_active])
        active_trailing = len([t for t in self.trailing_stops.values() if t.is_active])

        return {
            "total_orders": total_orders,
            "active_orders": active_orders,
            "filled_orders": filled_orders,
            "cancelled_orders": total_orders - active_orders - filled_orders,
            "active_bracket_orders": active_brackets,
            "active_trailing_stops": active_trailing,
            "scale_out_plans": len(self.scale_out_plans)
        }
