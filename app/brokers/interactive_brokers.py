"""
Interactive Brokers Integration

Interactive Brokers (IBKR) broker integration using Client Portal API.
API Docs: https://www.interactivebrokers.com/api/doc.html

Note: This uses the Client Portal Gateway API which requires the gateway to be running.
Alternative: Use ib_insync library for TWS/Gateway integration.
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


class InteractiveBrokersBroker(BaseBroker):
    """Interactive Brokers broker implementation using Client Portal API"""

    # Client Portal Gateway default URL (must be running locally or remotely)
    DEFAULT_BASE_URL = "https://localhost:5000/v1/api"

    def __init__(self, credentials: Dict[str, str], paper_trading: bool = True):
        """
        Initialize Interactive Brokers broker.

        Args:
            credentials: Dict with 'gateway_url' (optional), 'account_id' (optional)
            paper_trading: Use paper trading account (default: True)

        Note: IB Client Portal Gateway must be running and authenticated separately.
        """
        super().__init__(credentials, paper_trading)
        self.base_url = credentials.get("gateway_url", self.DEFAULT_BASE_URL)
        self.account_id = credentials.get("account_id")  # Will be fetched if not provided

        self.client: Optional[httpx.AsyncClient] = None

    @property
    def broker_type(self) -> BrokerType:
        return BrokerType.INTERACTIVE_BROKERS

    async def connect(self) -> bool:
        """Establish connection to IB Client Portal Gateway"""
        try:
            # Create client with SSL verification disabled for localhost
            self.client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=30.0,
                verify=False,  # Gateway uses self-signed cert
            )

            # Check authentication status
            response = await self.client.post("/iserver/auth/status")
            response.raise_for_status()
            auth_data = response.json()

            if not auth_data.get("authenticated", False):
                logger.warning("IB Gateway not authenticated. Please authenticate via the gateway UI.")
                return False

            # Get account if not provided
            if not self.account_id:
                accounts_response = await self.client.get("/portfolio/accounts")
                accounts_response.raise_for_status()
                accounts = accounts_response.json()
                if accounts:
                    self.account_id = accounts[0]["accountId"]
                    logger.info(f"Using IB account: {self.account_id}")

            self._connected = True
            logger.info(f"Connected to Interactive Brokers ({('paper' if self.paper_trading else 'live')} trading)")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to Interactive Brokers: {e}")
            self._connected = False
            return False

    async def disconnect(self) -> bool:
        """Disconnect from IB"""
        try:
            if self.client:
                # Logout
                try:
                    await self.client.post("/logout")
                except Exception:
                    pass  # Logout may fail, that's okay

                await self.client.aclose()

            self._connected = False
            logger.info("Disconnected from Interactive Brokers")
            return True
        except Exception as e:
            logger.error(f"Error disconnecting from Interactive Brokers: {e}")
            return False

    async def get_account(self) -> Account:
        """Get account information"""
        if not self.client or not self.account_id:
            raise RuntimeError("Not connected to Interactive Brokers")

        # Get account summary
        response = await self.client.get(f"/portfolio/{self.account_id}/summary")
        response.raise_for_status()
        data = response.json()

        # Parse summary data (IB returns array of key-value pairs)
        summary = {}
        for item in data:
            summary[item["s"]] = float(item.get("v", 0))

        return Account(
            account_id=self.account_id,
            broker=BrokerType.INTERACTIVE_BROKERS,
            cash=summary.get("TotalCashValue", 0),
            buying_power=summary.get("BuyingPower", 0),
            portfolio_value=summary.get("NetLiquidation", 0),
            equity=summary.get("Equity", 0),
            last_equity=summary.get("Equity", 0),
            unrealized_pl=summary.get("UnrealizedPnL", 0),
            realized_pl_today=summary.get("RealizedPnL", 0),
            pattern_day_trader=False,  # Not provided by IB API
            trading_blocked=False,
            account_blocked=False,
            multiplier=summary.get("Leverage", 1.0),
            currency="USD",
        )

    async def get_positions(self) -> List[Position]:
        """Get all open positions"""
        if not self.client or not self.account_id:
            raise RuntimeError("Not connected to Interactive Brokers")

        response = await self.client.get(f"/portfolio/{self.account_id}/positions/0")
        response.raise_for_status()
        data = response.json()

        positions = []
        for pos in data:
            if pos.get("position", 0) != 0:  # Only include non-zero positions
                positions.append(self._parse_position(pos))

        return positions

    async def get_position(self, symbol: str) -> Optional[Position]:
        """Get position for specific symbol"""
        positions = await self.get_positions()
        for pos in positions:
            # IB may use different formats, try to match
            if pos.symbol == symbol or pos.symbol.startswith(symbol):
                return pos
        return None

    def _parse_position(self, data: Dict[str, Any]) -> Position:
        """Parse IB position data"""
        qty = data.get("position", 0)
        side = OrderSide.BUY if qty > 0 else OrderSide.SELL

        current_price = data.get("mktPrice", 0)
        avg_price = data.get("avgPrice", 0)
        market_value = data.get("mktValue", 0)

        return Position(
            symbol=data.get("contractDesc", data.get("ticker", "")),
            quantity=abs(qty),
            avg_entry_price=avg_price,
            current_price=current_price,
            market_value=market_value,
            cost_basis=abs(qty) * avg_price,
            unrealized_pl=data.get("unrealizedPnl", 0),
            unrealized_pl_percent=(data.get("unrealizedPnl", 0) / (abs(qty) * avg_price) * 100) if avg_price != 0 else 0,
            side=side,
            asset_class=data.get("assetClass", "STK"),
            exchange=data.get("listingExchange"),
        )

    async def _get_contract_id(self, symbol: str) -> Optional[int]:
        """Get IB contract ID (conid) for symbol"""
        try:
            # Search for contract
            response = await self.client.get(
                f"/iserver/secdef/search",
                params={"symbol": symbol}
            )
            response.raise_for_status()
            results = response.json()

            if results:
                # Return first match (usually stocks)
                for result in results:
                    if result.get("sections", [{}])[0].get("secType") == "STK":
                        return result.get("conid")

            return None
        except Exception as e:
            logger.error(f"Failed to get contract ID for {symbol}: {e}")
            return None

    async def place_order(self, order: Order) -> Order:
        """Place an order"""
        if not self.client or not self.account_id:
            raise RuntimeError("Not connected to Interactive Brokers")

        # Get contract ID
        conid = await self._get_contract_id(order.symbol)
        if not conid:
            raise ValueError(f"Could not find contract for symbol: {order.symbol}")

        # Build IB order structure
        order_data = {
            "conid": conid,
            "secType": f"{conid}:STK",
            "orderType": self._map_order_type(order.order_type),
            "side": "BUY" if order.side == OrderSide.BUY else "SELL",
            "quantity": order.quantity,
            "tif": self._map_time_in_force(order.time_in_force),
        }

        # Add price fields
        if order.order_type == OrderType.LIMIT and order.price:
            order_data["price"] = order.price
        elif order.order_type == OrderType.STOP and order.stop_price:
            order_data["auxPrice"] = order.stop_price
        elif order.order_type == OrderType.STOP_LIMIT:
            if order.price and order.stop_price:
                order_data["price"] = order.price
                order_data["auxPrice"] = order.stop_price
        elif order.order_type == OrderType.TRAILING_STOP:
            if order.trail_percent:
                order_data["trailingPercent"] = order.trail_percent
            elif order.trail_amount:
                order_data["trailingAmt"] = order.trail_amount

        # Place order
        response = await self.client.post(
            f"/iserver/account/{self.account_id}/orders",
            json={"orders": [order_data]}
        )
        response.raise_for_status()
        result = response.json()

        # IB may return confirmation request
        if result and isinstance(result, list) and result[0].get("id"):
            order.order_id = result[0]["id"]
            order.status = OrderStatus.NEW
        else:
            # May need to confirm
            order.status = OrderStatus.PENDING

        return order

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
        # IB supports bracket orders through One-Cancels-All (OCA) groups
        # This is a simplified implementation
        logger.warning("Bracket orders on IB require OCA group setup - placing individual orders")

        orders = []

        # Entry order
        entry_order = Order(
            symbol=symbol,
            side=side,
            order_type=OrderType.LIMIT if entry_price else OrderType.MARKET,
            quantity=quantity,
            price=entry_price,
            time_in_force=time_in_force,
        )
        entry = await self.place_order(entry_order)
        orders.append(entry)

        return orders

    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        if not self.client or not self.account_id:
            raise RuntimeError("Not connected to Interactive Brokers")

        try:
            response = await self.client.delete(
                f"/iserver/account/{self.account_id}/order/{order_id}"
            )
            response.raise_for_status()
            return True
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to cancel order {order_id}: {e}")
            return False

    async def get_order(self, order_id: str) -> Optional[Order]:
        """Get order details"""
        # IB doesn't have direct order lookup by ID, need to get all orders
        orders = await self.get_orders()
        for order in orders:
            if order.order_id == order_id:
                return order
        return None

    async def get_orders(
        self,
        status: Optional[OrderStatus] = None,
        limit: int = 100,
    ) -> List[Order]:
        """Get orders"""
        if not self.client:
            raise RuntimeError("Not connected to Interactive Brokers")

        response = await self.client.get("/iserver/account/orders")
        response.raise_for_status()
        data = response.json()

        orders = []
        if "orders" in data:
            for order_data in data["orders"][:limit]:
                order = self._parse_order(order_data)
                if status is None or order.status == status:
                    orders.append(order)

        return orders

    async def get_current_price(self, symbol: str) -> float:
        """Get current market price"""
        if not self.client:
            raise RuntimeError("Not connected to Interactive Brokers")

        conid = await self._get_contract_id(symbol)
        if not conid:
            raise ValueError(f"Could not find contract for symbol: {symbol}")

        response = await self.client.get(
            f"/iserver/marketdata/snapshot",
            params={"conids": conid, "fields": "31"}  # Field 31 = last price
        )
        response.raise_for_status()
        data = response.json()

        if data and len(data) > 0:
            return float(data[0].get("31", 0))

        return 0.0

    def _parse_order(self, data: Dict[str, Any]) -> Order:
        """Parse IB order data"""
        return Order(
            order_id=str(data.get("orderId", "")),
            symbol=data.get("ticker", ""),
            side=OrderSide.BUY if data.get("side") == "BUY" else OrderSide.SELL,
            order_type=self._parse_order_type(data.get("orderType", "MKT")),
            quantity=float(data.get("totalSize", 0)),
            filled_qty=float(data.get("filledQuantity", 0)),
            price=float(data.get("price", 0)) if data.get("price") else None,
            status=self._parse_status(data.get("status", "")),
            avg_fill_price=float(data.get("avgPrice", 0)) if data.get("avgPrice") else None,
        )

    def _map_order_type(self, order_type: OrderType) -> str:
        """Map our OrderType to IB order type"""
        mapping = {
            OrderType.MARKET: "MKT",
            OrderType.LIMIT: "LMT",
            OrderType.STOP: "STP",
            OrderType.STOP_LIMIT: "STP LMT",
            OrderType.TRAILING_STOP: "TRAIL",
        }
        return mapping.get(order_type, "MKT")

    def _parse_order_type(self, ib_type: str) -> OrderType:
        """Parse IB order type to our OrderType"""
        mapping = {
            "MKT": OrderType.MARKET,
            "LMT": OrderType.LIMIT,
            "STP": OrderType.STOP,
            "STP LMT": OrderType.STOP_LIMIT,
            "TRAIL": OrderType.TRAILING_STOP,
        }
        return mapping.get(ib_type, OrderType.MARKET)

    def _map_time_in_force(self, tif: TimeInForce) -> str:
        """Map our TimeInForce to IB TIF"""
        mapping = {
            TimeInForce.DAY: "DAY",
            TimeInForce.GTC: "GTC",
            TimeInForce.IOC: "IOC",
            TimeInForce.FOK: "FOK",
        }
        return mapping.get(tif, "DAY")

    def _parse_status(self, ib_status: str) -> OrderStatus:
        """Parse IB order status to our OrderStatus"""
        mapping = {
            "PendingSubmit": OrderStatus.PENDING,
            "PendingCancel": OrderStatus.PENDING,
            "PreSubmitted": OrderStatus.PENDING,
            "Submitted": OrderStatus.NEW,
            "ApiPending": OrderStatus.PENDING,
            "ApiCancelled": OrderStatus.CANCELED,
            "Cancelled": OrderStatus.CANCELED,
            "Filled": OrderStatus.FILLED,
            "Inactive": OrderStatus.CANCELED,
        }
        return mapping.get(ib_status, OrderStatus.PENDING)
