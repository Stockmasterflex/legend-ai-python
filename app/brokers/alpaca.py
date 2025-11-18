"""
Alpaca Broker Integration

Alpaca is a commission-free broker with a developer-friendly API.
Website: https://alpaca.markets/
API Docs: https://alpaca.markets/docs/api-references/trading-api/
"""

import httpx
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

from app.brokers.base import (
    BaseBroker,
    BrokerType,
    Order,
    OrderType,
    OrderSide,
    OrderStatus,
    TimeInForce,
    Position,
    Account,
)

logger = logging.getLogger(__name__)


class AlpacaBroker(BaseBroker):
    """Alpaca broker implementation"""

    # API endpoints
    PAPER_BASE_URL = "https://paper-api.alpaca.markets"
    LIVE_BASE_URL = "https://api.alpaca.markets"
    DATA_BASE_URL = "https://data.alpaca.markets"

    def __init__(self, credentials: Dict[str, str], paper_trading: bool = True):
        """
        Initialize Alpaca broker.

        Args:
            credentials: Dict with 'api_key' and 'api_secret'
            paper_trading: Use paper trading account (default: True)
        """
        super().__init__(credentials, paper_trading)
        self.base_url = self.PAPER_BASE_URL if paper_trading else self.LIVE_BASE_URL
        self.api_key = credentials.get("api_key")
        self.api_secret = credentials.get("api_secret")

        if not self.api_key or not self.api_secret:
            raise ValueError("Alpaca requires 'api_key' and 'api_secret' in credentials")

        self.headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.api_secret,
            "Content-Type": "application/json",
        }
        self.client: Optional[httpx.AsyncClient] = None

    @property
    def broker_type(self) -> BrokerType:
        return BrokerType.ALPACA

    async def connect(self) -> bool:
        """Establish connection to Alpaca"""
        try:
            self.client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=self.headers,
                timeout=30.0,
            )

            # Test connection by getting account
            response = await self.client.get("/v2/account")
            response.raise_for_status()

            self._connected = True
            logger.info(f"Connected to Alpaca ({('paper' if self.paper_trading else 'live')} trading)")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to Alpaca: {e}")
            self._connected = False
            return False

    async def disconnect(self) -> bool:
        """Disconnect from Alpaca"""
        try:
            if self.client:
                await self.client.aclose()
            self._connected = False
            logger.info("Disconnected from Alpaca")
            return True
        except Exception as e:
            logger.error(f"Error disconnecting from Alpaca: {e}")
            return False

    async def get_account(self) -> Account:
        """Get account information"""
        if not self.client:
            raise RuntimeError("Not connected to Alpaca")

        response = await self.client.get("/v2/account")
        response.raise_for_status()
        data = response.json()

        return Account(
            account_id=data["account_number"],
            broker=BrokerType.ALPACA,
            cash=float(data["cash"]),
            buying_power=float(data["buying_power"]),
            portfolio_value=float(data["portfolio_value"]),
            equity=float(data["equity"]),
            last_equity=float(data["last_equity"]),
            unrealized_pl=float(data.get("unrealized_pl", 0)),
            realized_pl_today=float(data.get("realized_pl", 0)),
            pattern_day_trader=data.get("pattern_day_trader", False),
            trading_blocked=data.get("trading_blocked", False),
            account_blocked=data.get("account_blocked", False),
            multiplier=float(data.get("multiplier", 1)),
            initial_margin=float(data.get("initial_margin", 0)) if data.get("initial_margin") else None,
            maintenance_margin=float(data.get("maintenance_margin", 0)) if data.get("maintenance_margin") else None,
            created_at=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")) if data.get("created_at") else None,
            currency=data.get("currency", "USD"),
        )

    async def get_positions(self) -> List[Position]:
        """Get all open positions"""
        if not self.client:
            raise RuntimeError("Not connected to Alpaca")

        response = await self.client.get("/v2/positions")
        response.raise_for_status()
        data = response.json()

        positions = []
        for pos in data:
            positions.append(self._parse_position(pos))

        return positions

    async def get_position(self, symbol: str) -> Optional[Position]:
        """Get position for specific symbol"""
        if not self.client:
            raise RuntimeError("Not connected to Alpaca")

        try:
            response = await self.client.get(f"/v2/positions/{symbol}")
            response.raise_for_status()
            data = response.json()
            return self._parse_position(data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    def _parse_position(self, data: Dict[str, Any]) -> Position:
        """Parse Alpaca position data"""
        qty = float(data["qty"])
        side = OrderSide.BUY if qty > 0 else OrderSide.SELL

        return Position(
            symbol=data["symbol"],
            quantity=abs(qty),
            avg_entry_price=float(data["avg_entry_price"]),
            current_price=float(data["current_price"]),
            market_value=float(data["market_value"]),
            cost_basis=float(data["cost_basis"]),
            unrealized_pl=float(data["unrealized_pl"]),
            unrealized_pl_percent=float(data["unrealized_plpc"]) * 100,
            side=side,
            asset_class=data.get("asset_class", "us_equity"),
            exchange=data.get("exchange"),
            lastday_price=float(data.get("lastday_price")) if data.get("lastday_price") else None,
            change_today=float(data.get("change_today")) if data.get("change_today") else None,
        )

    async def place_order(self, order: Order) -> Order:
        """Place an order"""
        if not self.client:
            raise RuntimeError("Not connected to Alpaca")

        # Build order request
        order_data = {
            "symbol": order.symbol,
            "qty": order.quantity,
            "side": order.side.value,
            "type": self._map_order_type(order.order_type),
            "time_in_force": order.time_in_force.value,
        }

        # Add price fields based on order type
        if order.order_type == OrderType.LIMIT and order.price:
            order_data["limit_price"] = order.price
        elif order.order_type == OrderType.STOP and order.stop_price:
            order_data["stop_price"] = order.stop_price
        elif order.order_type == OrderType.STOP_LIMIT:
            if order.price and order.stop_price:
                order_data["limit_price"] = order.price
                order_data["stop_price"] = order.stop_price
        elif order.order_type == OrderType.TRAILING_STOP:
            if order.trail_percent:
                order_data["trail_percent"] = order.trail_percent
            elif order.trail_amount:
                order_data["trail_price"] = order.trail_amount

        # Client order ID
        if order.client_order_id:
            order_data["client_order_id"] = order.client_order_id

        response = await self.client.post("/v2/orders", json=order_data)
        response.raise_for_status()
        data = response.json()

        return self._parse_order(data)

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
        """Place a bracket order"""
        if not self.client:
            raise RuntimeError("Not connected to Alpaca")

        order_data = {
            "symbol": symbol,
            "qty": quantity,
            "side": side.value,
            "type": "limit" if entry_price else "market",
            "time_in_force": time_in_force.value,
            "order_class": "bracket",
            "take_profit": {"limit_price": take_profit_price},
            "stop_loss": {"stop_price": stop_loss_price},
        }

        if entry_price:
            order_data["limit_price"] = entry_price

        response = await self.client.post("/v2/orders", json=order_data)
        response.raise_for_status()
        data = response.json()

        # Alpaca returns the main order with legs
        orders = [self._parse_order(data)]

        # Parse take profit and stop loss legs
        if "legs" in data:
            for leg in data["legs"]:
                orders.append(self._parse_order(leg))

        return orders

    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        if not self.client:
            raise RuntimeError("Not connected to Alpaca")

        try:
            response = await self.client.delete(f"/v2/orders/{order_id}")
            response.raise_for_status()
            return True
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to cancel order {order_id}: {e}")
            return False

    async def get_order(self, order_id: str) -> Optional[Order]:
        """Get order details"""
        if not self.client:
            raise RuntimeError("Not connected to Alpaca")

        try:
            response = await self.client.get(f"/v2/orders/{order_id}")
            response.raise_for_status()
            data = response.json()
            return self._parse_order(data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    async def get_orders(
        self,
        status: Optional[OrderStatus] = None,
        limit: int = 100,
    ) -> List[Order]:
        """Get orders"""
        if not self.client:
            raise RuntimeError("Not connected to Alpaca")

        params = {"limit": limit}
        if status:
            params["status"] = self._map_status_to_alpaca(status)

        response = await self.client.get("/v2/orders", params=params)
        response.raise_for_status()
        data = response.json()

        return [self._parse_order(order) for order in data]

    async def get_current_price(self, symbol: str) -> float:
        """Get current market price"""
        if not self.client:
            raise RuntimeError("Not connected to Alpaca")

        # Use latest trade endpoint
        async with httpx.AsyncClient(base_url=self.DATA_BASE_URL, headers=self.headers) as data_client:
            response = await data_client.get(f"/v2/stocks/{symbol}/trades/latest")
            response.raise_for_status()
            data = response.json()
            return float(data["trade"]["p"])

    def _parse_order(self, data: Dict[str, Any]) -> Order:
        """Parse Alpaca order data"""
        return Order(
            order_id=data["id"],
            client_order_id=data.get("client_order_id"),
            symbol=data["symbol"],
            side=OrderSide(data["side"]),
            order_type=self._parse_order_type(data["type"]),
            quantity=float(data["qty"]),
            filled_qty=float(data.get("filled_qty", 0)),
            price=float(data["limit_price"]) if data.get("limit_price") else None,
            stop_price=float(data["stop_price"]) if data.get("stop_price") else None,
            trail_percent=float(data["trail_percent"]) if data.get("trail_percent") else None,
            time_in_force=TimeInForce(data["time_in_force"]),
            status=self._parse_status(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")) if data.get("created_at") else None,
            updated_at=datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00")) if data.get("updated_at") else None,
            filled_at=datetime.fromisoformat(data["filled_at"].replace("Z", "+00:00")) if data.get("filled_at") else None,
            avg_fill_price=float(data["filled_avg_price"]) if data.get("filled_avg_price") else None,
        )

    def _map_order_type(self, order_type: OrderType) -> str:
        """Map our OrderType to Alpaca order type"""
        mapping = {
            OrderType.MARKET: "market",
            OrderType.LIMIT: "limit",
            OrderType.STOP: "stop",
            OrderType.STOP_LIMIT: "stop_limit",
            OrderType.TRAILING_STOP: "trailing_stop",
        }
        return mapping.get(order_type, "market")

    def _parse_order_type(self, alpaca_type: str) -> OrderType:
        """Parse Alpaca order type to our OrderType"""
        mapping = {
            "market": OrderType.MARKET,
            "limit": OrderType.LIMIT,
            "stop": OrderType.STOP,
            "stop_limit": OrderType.STOP_LIMIT,
            "trailing_stop": OrderType.TRAILING_STOP,
        }
        return mapping.get(alpaca_type, OrderType.MARKET)

    def _parse_status(self, alpaca_status: str) -> OrderStatus:
        """Parse Alpaca order status to our OrderStatus"""
        mapping = {
            "new": OrderStatus.NEW,
            "accepted": OrderStatus.NEW,
            "pending_new": OrderStatus.PENDING,
            "partially_filled": OrderStatus.PARTIALLY_FILLED,
            "filled": OrderStatus.FILLED,
            "done_for_day": OrderStatus.FILLED,
            "canceled": OrderStatus.CANCELED,
            "expired": OrderStatus.EXPIRED,
            "replaced": OrderStatus.CANCELED,
            "pending_cancel": OrderStatus.PENDING,
            "pending_replace": OrderStatus.PENDING,
            "rejected": OrderStatus.REJECTED,
            "suspended": OrderStatus.REJECTED,
        }
        return mapping.get(alpaca_status, OrderStatus.PENDING)

    def _map_status_to_alpaca(self, status: OrderStatus) -> str:
        """Map our OrderStatus to Alpaca status filter"""
        if status == OrderStatus.NEW:
            return "open"
        elif status == OrderStatus.FILLED:
            return "closed"
        elif status == OrderStatus.CANCELED:
            return "canceled"
        else:
            return "all"
