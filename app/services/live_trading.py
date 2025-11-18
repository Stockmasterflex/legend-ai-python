"""
Live Trading Service

High-level service for live trading operations including:
- Order placement from charts
- One-click entries
- Bracket orders
- Trailing stops
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel

from app.brokers.base import (
    BaseBroker,
    Order,
    OrderType,
    OrderSide,
    OrderStatus,
    TimeInForce,
    Position,
)
from app.services.risk_calculator import RiskCalculator

logger = logging.getLogger(__name__)


class QuickEntryRequest(BaseModel):
    """Quick entry request for one-click trading"""
    symbol: str
    side: OrderSide
    account_size: float
    risk_percent: float = 1.0  # Default 1% risk
    entry_price: Optional[float] = None  # None for market order
    stop_loss_price: float
    target_price: Optional[float] = None
    order_type: OrderType = OrderType.MARKET
    time_in_force: TimeInForce = TimeInForce.DAY


class BracketOrderRequest(BaseModel):
    """Bracket order request"""
    symbol: str
    side: OrderSide
    quantity: float
    entry_price: Optional[float] = None  # None for market entry
    take_profit_price: float
    stop_loss_price: float
    time_in_force: TimeInForce = TimeInForce.DAY


class TrailingStopRequest(BaseModel):
    """Trailing stop order request"""
    symbol: str
    side: OrderSide
    quantity: float
    trail_percent: Optional[float] = None
    trail_amount: Optional[float] = None
    time_in_force: TimeInForce = TimeInForce.DAY


class LiveTradingService:
    """
    Service for live trading operations.

    Provides high-level trading operations with automatic position sizing,
    risk management, and execution tracking.
    """

    def __init__(self, broker: BaseBroker):
        """
        Initialize live trading service.

        Args:
            broker: Connected broker instance
        """
        self.broker = broker
        self.risk_calculator = RiskCalculator()

    async def quick_entry(self, request: QuickEntryRequest) -> Dict[str, Any]:
        """
        Place a quick entry order with automatic position sizing.

        This is designed for one-click trading from charts with automatic
        risk-based position sizing.

        Args:
            request: Quick entry request

        Returns:
            Dict with order details and position sizing info
        """
        if not self.broker.is_connected():
            raise RuntimeError("Broker not connected")

        # Calculate position size based on risk
        position_size_result = self.risk_calculator.calculate_position_size(
            account_size=request.account_size,
            risk_percent=request.risk_percent,
            entry_price=request.entry_price or await self.broker.get_current_price(request.symbol),
            stop_loss_price=request.stop_loss_price,
            target_price=request.target_price,
        )

        # Create order
        order = Order(
            symbol=request.symbol,
            side=request.side,
            order_type=request.order_type,
            quantity=position_size_result.position_size,
            price=request.entry_price,
            time_in_force=request.time_in_force,
        )

        # Add stop loss if provided
        if request.stop_loss_price:
            order.stop_loss_price = request.stop_loss_price

        # Add take profit if provided
        if request.target_price:
            order.take_profit_price = request.target_price

        # Place order
        placed_order = await self.broker.place_order(order)

        logger.info(
            f"Quick entry order placed: {request.symbol} {request.side.value} "
            f"{position_size_result.position_size} @ {request.entry_price or 'market'}"
        )

        return {
            "order": placed_order,
            "position_sizing": position_size_result,
            "risk_amount": position_size_result.risk_per_trade,
            "potential_reward": position_size_result.position_size * (
                abs((request.target_price or 0) - (request.entry_price or 0))
            ) if request.target_price else None,
        }

    async def place_bracket_order(self, request: BracketOrderRequest) -> List[Order]:
        """
        Place a bracket order (entry + take profit + stop loss).

        Args:
            request: Bracket order request

        Returns:
            List of orders (entry, take profit, stop loss)
        """
        if not self.broker.is_connected():
            raise RuntimeError("Broker not connected")

        orders = await self.broker.place_bracket_order(
            symbol=request.symbol,
            side=request.side,
            quantity=request.quantity,
            entry_price=request.entry_price,
            take_profit_price=request.take_profit_price,
            stop_loss_price=request.stop_loss_price,
            time_in_force=request.time_in_force,
        )

        logger.info(
            f"Bracket order placed: {request.symbol} {request.side.value} "
            f"{request.quantity} with TP={request.take_profit_price} SL={request.stop_loss_price}"
        )

        return orders

    async def place_trailing_stop(self, request: TrailingStopRequest) -> Order:
        """
        Place a trailing stop order.

        Args:
            request: Trailing stop request

        Returns:
            Order: Placed order
        """
        if not self.broker.is_connected():
            raise RuntimeError("Broker not connected")

        if not request.trail_percent and not request.trail_amount:
            raise ValueError("Either trail_percent or trail_amount must be provided")

        order = Order(
            symbol=request.symbol,
            side=request.side,
            order_type=OrderType.TRAILING_STOP,
            quantity=request.quantity,
            trail_percent=request.trail_percent,
            trail_amount=request.trail_amount,
            time_in_force=request.time_in_force,
        )

        placed_order = await self.broker.place_order(order)

        logger.info(
            f"Trailing stop placed: {request.symbol} {request.side.value} "
            f"{request.quantity} trail={request.trail_percent or request.trail_amount}"
        )

        return placed_order

    async def close_position(
        self,
        symbol: str,
        quantity: Optional[float] = None,
        order_type: OrderType = OrderType.MARKET,
    ) -> Order:
        """
        Close a position (or partial position).

        Args:
            symbol: Symbol to close
            quantity: Quantity to close (None for full position)
            order_type: Order type for closing (default: MARKET)

        Returns:
            Order: Close order
        """
        if not self.broker.is_connected():
            raise RuntimeError("Broker not connected")

        # Get current position
        position = await self.broker.get_position(symbol)
        if not position:
            raise ValueError(f"No position found for {symbol}")

        # Determine quantity to close
        close_qty = quantity or position.quantity

        # Determine side (opposite of position)
        close_side = OrderSide.SELL if position.side == OrderSide.BUY else OrderSide.BUY

        # Create close order
        order = Order(
            symbol=symbol,
            side=close_side,
            order_type=order_type,
            quantity=close_qty,
        )

        placed_order = await self.broker.place_order(order)

        logger.info(f"Position close order placed: {symbol} {close_side.value} {close_qty}")

        return placed_order

    async def modify_stop_loss(
        self,
        symbol: str,
        new_stop_price: float,
        current_order_id: Optional[str] = None,
    ) -> Order:
        """
        Modify stop loss for a position.

        Args:
            symbol: Symbol
            new_stop_price: New stop loss price
            current_order_id: Existing stop order ID to cancel (optional)

        Returns:
            Order: New stop loss order
        """
        if not self.broker.is_connected():
            raise RuntimeError("Broker not connected")

        # Cancel existing stop if provided
        if current_order_id:
            await self.broker.cancel_order(current_order_id)

        # Get position to determine side and quantity
        position = await self.broker.get_position(symbol)
        if not position:
            raise ValueError(f"No position found for {symbol}")

        # Place new stop loss
        stop_side = OrderSide.SELL if position.side == OrderSide.BUY else OrderSide.BUY

        order = Order(
            symbol=symbol,
            side=stop_side,
            order_type=OrderType.STOP,
            quantity=position.quantity,
            stop_price=new_stop_price,
            time_in_force=TimeInForce.GTC,  # Keep until filled
        )

        placed_order = await self.broker.place_order(order)

        logger.info(f"Stop loss modified for {symbol}: new stop @ {new_stop_price}")

        return placed_order

    async def get_open_orders(self) -> List[Order]:
        """
        Get all open orders.

        Returns:
            List[Order]: Open orders
        """
        if not self.broker.is_connected():
            raise RuntimeError("Broker not connected")

        return await self.broker.get_orders(status=OrderStatus.NEW)

    async def cancel_all_orders(self, symbol: Optional[str] = None) -> int:
        """
        Cancel all open orders (optionally filtered by symbol).

        Args:
            symbol: Symbol to filter by (None for all)

        Returns:
            int: Number of orders canceled
        """
        if not self.broker.is_connected():
            raise RuntimeError("Broker not connected")

        open_orders = await self.get_open_orders()
        canceled_count = 0

        for order in open_orders:
            if symbol is None or order.symbol == symbol:
                success = await self.broker.cancel_order(order.order_id)
                if success:
                    canceled_count += 1

        logger.info(f"Canceled {canceled_count} orders" + (f" for {symbol}" if symbol else ""))

        return canceled_count
