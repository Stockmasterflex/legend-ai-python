"""
TradeStation Broker Integration

TradeStation broker integration using their Web API.
API Docs: https://api.tradestation.com/docs/
"""

import httpx
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
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


class TradeStationBroker(BaseBroker):
    """TradeStation broker implementation"""

    # API endpoints
    BASE_URL = "https://api.tradestation.com/v3"
    SIM_BASE_URL = "https://sim-api.tradestation.com/v3"
    AUTH_URL = "https://signin.tradestation.com/oauth/token"

    def __init__(self, credentials: Dict[str, str], paper_trading: bool = True):
        """
        Initialize TradeStation broker.

        Args:
            credentials: Dict with 'api_key', 'api_secret', 'refresh_token', 'account_id'
            paper_trading: Use simulation account (default: True)
        """
        super().__init__(credentials, paper_trading)
        self.base_url = self.SIM_BASE_URL if paper_trading else self.BASE_URL
        self.api_key = credentials.get("api_key")
        self.api_secret = credentials.get("api_secret")
        self.refresh_token = credentials.get("refresh_token")
        self.account_id = credentials.get("account_id")
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None

        if not all([self.api_key, self.api_secret, self.refresh_token]):
            raise ValueError(
                "TradeStation requires 'api_key', 'api_secret', and 'refresh_token' in credentials"
            )

        self.client: Optional[httpx.AsyncClient] = None

    @property
    def broker_type(self) -> BrokerType:
        return BrokerType.TRADESTATION

    async def _refresh_access_token(self) -> None:
        """Refresh the access token"""
        data = {
            "grant_type": "refresh_token",
            "client_id": self.api_key,
            "client_secret": self.api_secret,
            "refresh_token": self.refresh_token,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.AUTH_URL, data=data)
            response.raise_for_status()
            token_data = response.json()

            self.access_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 1200)  # Default 20 minutes
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)

            # Update refresh token if provided
            if "refresh_token" in token_data:
                self.refresh_token = token_data["refresh_token"]

            logger.info("TradeStation access token refreshed")

    async def _ensure_token_valid(self) -> None:
        """Ensure access token is valid, refresh if needed"""
        if not self.access_token or not self.token_expires_at:
            await self._refresh_access_token()
        elif datetime.now() >= self.token_expires_at - timedelta(minutes=2):
            await self._refresh_access_token()

    async def connect(self) -> bool:
        """Establish connection to TradeStation"""
        try:
            await self._refresh_access_token()

            self.client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=30.0,
            )

            # Get account if not provided
            if not self.account_id:
                accounts = await self._get_accounts()
                if accounts:
                    self.account_id = accounts[0]["AccountID"]
                    logger.info(f"Using TradeStation account: {self.account_id}")

            self._connected = True
            logger.info(f"Connected to TradeStation ({('simulation' if self.paper_trading else 'live')} trading)")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to TradeStation: {e}")
            self._connected = False
            return False

    async def disconnect(self) -> bool:
        """Disconnect from TradeStation"""
        try:
            if self.client:
                await self.client.aclose()
            self._connected = False
            logger.info("Disconnected from TradeStation")
            return True
        except Exception as e:
            logger.error(f"Error disconnecting from TradeStation: {e}")
            return False

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with auth token"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    async def _get_accounts(self) -> List[Dict[str, Any]]:
        """Get available accounts"""
        await self._ensure_token_valid()
        response = await self.client.get("/brokerage/accounts", headers=self._get_headers())
        response.raise_for_status()
        data = response.json()
        return data.get("Accounts", [])

    async def get_account(self) -> Account:
        """Get account information"""
        if not self.client or not self.account_id:
            raise RuntimeError("Not connected to TradeStation")

        await self._ensure_token_valid()

        # Get account balances
        response = await self.client.get(
            f"/brokerage/accounts/{self.account_id}/balances",
            headers=self._get_headers()
        )
        response.raise_for_status()
        data = response.json()

        balances = data.get("Balances", [{}])[0] if data.get("Balances") else {}

        return Account(
            account_id=self.account_id,
            broker=BrokerType.TRADESTATION,
            cash=balances.get("CashBalance", 0),
            buying_power=balances.get("BuyingPower", 0),
            portfolio_value=balances.get("Equity", 0),
            equity=balances.get("Equity", 0),
            last_equity=balances.get("Equity", 0),
            unrealized_pl=balances.get("UnclearedDeposit", 0),  # TradeStation uses different fields
            realized_pl_today=balances.get("RealizedProfitLoss", 0),
            pattern_day_trader=False,  # Not provided
            trading_blocked=False,
            account_blocked=False,
            multiplier=1.0,
            currency="USD",
        )

    async def get_positions(self) -> List[Position]:
        """Get all open positions"""
        if not self.client or not self.account_id:
            raise RuntimeError("Not connected to TradeStation")

        await self._ensure_token_valid()

        response = await self.client.get(
            f"/brokerage/accounts/{self.account_id}/positions",
            headers=self._get_headers()
        )
        response.raise_for_status()
        data = response.json()

        positions = []
        for pos in data.get("Positions", []):
            positions.append(self._parse_position(pos))

        return positions

    async def get_position(self, symbol: str) -> Optional[Position]:
        """Get position for specific symbol"""
        positions = await self.get_positions()
        for pos in positions:
            if pos.symbol == symbol:
                return pos
        return None

    def _parse_position(self, data: Dict[str, Any]) -> Position:
        """Parse TradeStation position data"""
        qty = data.get("Quantity", 0)
        side = OrderSide.BUY if qty > 0 else OrderSide.SELL

        avg_price = data.get("AveragePrice", 0)
        current_price = data.get("Last", 0)
        market_value = data.get("MarketValue", 0)

        return Position(
            symbol=data.get("Symbol", ""),
            quantity=abs(qty),
            avg_entry_price=avg_price,
            current_price=current_price,
            market_value=market_value,
            cost_basis=abs(qty) * avg_price,
            unrealized_pl=data.get("UnrealizedProfitLoss", 0),
            unrealized_pl_percent=data.get("UnrealizedProfitLossPercent", 0),
            side=side,
            asset_class=data.get("AssetType", "EQ"),
        )

    async def place_order(self, order: Order) -> Order:
        """Place an order"""
        if not self.client or not self.account_id:
            raise RuntimeError("Not connected to TradeStation")

        await self._ensure_token_valid()

        # Build TradeStation order structure
        order_data = {
            "AccountID": self.account_id,
            "Symbol": order.symbol,
            "Quantity": str(int(order.quantity)),
            "OrderType": self._map_order_type(order.order_type),
            "TradeAction": "BUY" if order.side == OrderSide.BUY else "SELL",
            "TimeInForce": {"Duration": self._map_time_in_force(order.time_in_force)},
            "Route": "Intelligent",  # TradeStation's smart routing
        }

        # Add price fields
        if order.order_type == OrderType.LIMIT and order.price:
            order_data["LimitPrice"] = str(order.price)
        elif order.order_type == OrderType.STOP and order.stop_price:
            order_data["StopPrice"] = str(order.stop_price)
        elif order.order_type == OrderType.STOP_LIMIT:
            if order.price and order.stop_price:
                order_data["LimitPrice"] = str(order.price)
                order_data["StopPrice"] = str(order.stop_price)
        elif order.order_type == OrderType.TRAILING_STOP:
            if order.trail_amount:
                order_data["TrailingStop"] = {"Amount": str(order.trail_amount)}

        response = await self.client.post(
            "/orderexecution/orders",
            headers=self._get_headers(),
            json=order_data
        )
        response.raise_for_status()
        result = response.json()

        if "Orders" in result and result["Orders"]:
            order_result = result["Orders"][0]
            order.order_id = order_result.get("OrderID")
            order.status = OrderStatus.NEW if order_result.get("Message") == "Order successfully placed" else OrderStatus.PENDING

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
        if not self.client or not self.account_id:
            raise RuntimeError("Not connected to TradeStation")

        await self._ensure_token_valid()

        # TradeStation supports OSO (Order Sends Order) for bracket orders
        order_data = {
            "AccountID": self.account_id,
            "Symbol": symbol,
            "Quantity": str(int(quantity)),
            "OrderType": "Limit" if entry_price else "Market",
            "TradeAction": "BUY" if side == OrderSide.BUY else "SELL",
            "TimeInForce": {"Duration": self._map_time_in_force(time_in_force)},
            "Route": "Intelligent",
            "OSOs": [
                {
                    "Symbol": symbol,
                    "Quantity": str(int(quantity)),
                    "OrderType": "Limit",
                    "TradeAction": "SELL" if side == OrderSide.BUY else "BUY",
                    "LimitPrice": str(take_profit_price),
                    "TimeInForce": {"Duration": self._map_time_in_force(time_in_force)},
                },
                {
                    "Symbol": symbol,
                    "Quantity": str(int(quantity)),
                    "OrderType": "StopMarket",
                    "TradeAction": "SELL" if side == OrderSide.BUY else "BUY",
                    "StopPrice": str(stop_loss_price),
                    "TimeInForce": {"Duration": self._map_time_in_force(time_in_force)},
                }
            ]
        }

        if entry_price:
            order_data["LimitPrice"] = str(entry_price)

        response = await self.client.post(
            "/orderexecution/orders",
            headers=self._get_headers(),
            json=order_data
        )
        response.raise_for_status()
        result = response.json()

        # Parse returned orders
        orders = []
        if "Orders" in result:
            for order_result in result["Orders"]:
                orders.append(Order(
                    order_id=order_result.get("OrderID"),
                    symbol=symbol,
                    side=side,
                    order_type=OrderType.LIMIT if entry_price else OrderType.MARKET,
                    quantity=quantity,
                    status=OrderStatus.NEW,
                ))

        return orders

    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        if not self.client:
            raise RuntimeError("Not connected to TradeStation")

        await self._ensure_token_valid()

        try:
            response = await self.client.delete(
                f"/orderexecution/orders/{order_id}",
                headers=self._get_headers()
            )
            response.raise_for_status()
            return True
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to cancel order {order_id}: {e}")
            return False

    async def get_order(self, order_id: str) -> Optional[Order]:
        """Get order details"""
        if not self.client:
            raise RuntimeError("Not connected to TradeStation")

        await self._ensure_token_valid()

        try:
            response = await self.client.get(
                f"/orderexecution/orders/{order_id}",
                headers=self._get_headers()
            )
            response.raise_for_status()
            data = response.json()

            if "Orders" in data and data["Orders"]:
                return self._parse_order(data["Orders"][0])

            return None
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
        if not self.client or not self.account_id:
            raise RuntimeError("Not connected to TradeStation")

        await self._ensure_token_valid()

        response = await self.client.get(
            f"/brokerage/accounts/{self.account_id}/orders",
            headers=self._get_headers()
        )
        response.raise_for_status()
        data = response.json()

        orders = []
        for order_data in data.get("Orders", [])[:limit]:
            order = self._parse_order(order_data)
            if status is None or order.status == status:
                orders.append(order)

        return orders

    async def get_current_price(self, symbol: str) -> float:
        """Get current market price"""
        if not self.client:
            raise RuntimeError("Not connected to TradeStation")

        await self._ensure_token_valid()

        response = await self.client.get(
            f"/marketdata/quotes/{symbol}",
            headers=self._get_headers()
        )
        response.raise_for_status()
        data = response.json()

        if "Quotes" in data and data["Quotes"]:
            return data["Quotes"][0].get("Last", 0)

        return 0.0

    def _parse_order(self, data: Dict[str, Any]) -> Order:
        """Parse TradeStation order data"""
        # Determine side from TradeAction or QuantityOrdered
        trade_action = data.get("TradeAction", "")
        side = OrderSide.BUY if trade_action == "BUY" else OrderSide.SELL

        return Order(
            order_id=data.get("OrderID"),
            symbol=data.get("Symbol", ""),
            side=side,
            order_type=self._parse_order_type(data.get("OrderType", "Market")),
            quantity=float(data.get("QuantityOrdered", 0)),
            filled_qty=float(data.get("FilledQuantity", 0)),
            price=float(data.get("LimitPrice", 0)) if data.get("LimitPrice") else None,
            stop_price=float(data.get("StopPrice", 0)) if data.get("StopPrice") else None,
            status=self._parse_status(data.get("Status", "")),
            avg_fill_price=float(data.get("AveragePrice", 0)) if data.get("AveragePrice") else None,
        )

    def _map_order_type(self, order_type: OrderType) -> str:
        """Map our OrderType to TradeStation order type"""
        mapping = {
            OrderType.MARKET: "Market",
            OrderType.LIMIT: "Limit",
            OrderType.STOP: "StopMarket",
            OrderType.STOP_LIMIT: "StopLimit",
            OrderType.TRAILING_STOP: "TrailingStop",
        }
        return mapping.get(order_type, "Market")

    def _parse_order_type(self, ts_type: str) -> OrderType:
        """Parse TradeStation order type to our OrderType"""
        mapping = {
            "Market": OrderType.MARKET,
            "Limit": OrderType.LIMIT,
            "StopMarket": OrderType.STOP,
            "StopLimit": OrderType.STOP_LIMIT,
            "TrailingStop": OrderType.TRAILING_STOP,
        }
        return mapping.get(ts_type, OrderType.MARKET)

    def _map_time_in_force(self, tif: TimeInForce) -> str:
        """Map our TimeInForce to TradeStation duration"""
        mapping = {
            TimeInForce.DAY: "DAY",
            TimeInForce.GTC: "GTC",
            TimeInForce.IOC: "IOC",
            TimeInForce.FOK: "FOK",
        }
        return mapping.get(tif, "DAY")

    def _parse_status(self, ts_status: str) -> OrderStatus:
        """Parse TradeStation order status to our OrderStatus"""
        mapping = {
            "ACK": OrderStatus.NEW,
            "DON": OrderStatus.FILLED,
            "FLL": OrderStatus.FILLED,
            "FLP": OrderStatus.PARTIALLY_FILLED,
            "FPR": OrderStatus.PARTIALLY_FILLED,
            "CAN": OrderStatus.CANCELED,
            "REJ": OrderStatus.REJECTED,
            "EXP": OrderStatus.EXPIRED,
            "UCN": OrderStatus.PENDING,
            "OPN": OrderStatus.NEW,
        }
        return mapping.get(ts_status, OrderStatus.PENDING)
