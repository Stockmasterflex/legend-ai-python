"""
TD Ameritrade Broker Integration

TD Ameritrade (now part of Charles Schwab) broker integration.
API Docs: https://developer.tdameritrade.com/apis

Note: TD Ameritrade API is being phased out and migrated to Charles Schwab.
This implementation uses the TD Ameritrade API while it's still available.
"""

import httpx
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import logging
import json

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


class TDAmeritradeBroker(BaseBroker):
    """TD Ameritrade broker implementation"""

    BASE_URL = "https://api.tdameritrade.com/v1"
    AUTH_URL = "https://api.tdameritrade.com/v1/oauth2/token"

    def __init__(self, credentials: Dict[str, str], paper_trading: bool = True):
        """
        Initialize TD Ameritrade broker.

        Args:
            credentials: Dict with 'api_key', 'refresh_token', 'account_id'
            paper_trading: Not used (TD Ameritrade has separate paper trading accounts)
        """
        super().__init__(credentials, paper_trading)
        self.api_key = credentials.get("api_key")
        self.refresh_token = credentials.get("refresh_token")
        self.account_id = credentials.get("account_id")
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None

        if not self.api_key or not self.refresh_token or not self.account_id:
            raise ValueError(
                "TD Ameritrade requires 'api_key', 'refresh_token', and 'account_id' in credentials"
            )

        self.client: Optional[httpx.AsyncClient] = None

    @property
    def broker_type(self) -> BrokerType:
        return BrokerType.TD_AMERITRADE

    async def _refresh_access_token(self) -> None:
        """Refresh the access token"""
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.api_key,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.AUTH_URL, data=data)
            response.raise_for_status()
            token_data = response.json()

            self.access_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 1800)  # Default 30 minutes
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)

            logger.info("TD Ameritrade access token refreshed")

    async def _ensure_token_valid(self) -> None:
        """Ensure access token is valid, refresh if needed"""
        if not self.access_token or not self.token_expires_at:
            await self._refresh_access_token()
        elif datetime.now() >= self.token_expires_at - timedelta(minutes=5):
            # Refresh 5 minutes before expiry
            await self._refresh_access_token()

    async def connect(self) -> bool:
        """Establish connection to TD Ameritrade"""
        try:
            await self._refresh_access_token()

            self.client = httpx.AsyncClient(
                base_url=self.BASE_URL,
                timeout=30.0,
            )

            # Test connection
            await self.get_account()

            self._connected = True
            logger.info("Connected to TD Ameritrade")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to TD Ameritrade: {e}")
            self._connected = False
            return False

    async def disconnect(self) -> bool:
        """Disconnect from TD Ameritrade"""
        try:
            if self.client:
                await self.client.aclose()
            self._connected = False
            logger.info("Disconnected from TD Ameritrade")
            return True
        except Exception as e:
            logger.error(f"Error disconnecting from TD Ameritrade: {e}")
            return False

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with auth token"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    async def get_account(self) -> Account:
        """Get account information"""
        if not self.client:
            raise RuntimeError("Not connected to TD Ameritrade")

        await self._ensure_token_valid()

        response = await self.client.get(
            f"/accounts/{self.account_id}",
            headers=self._get_headers(),
            params={"fields": "positions"},
        )
        response.raise_for_status()
        data = response.json()

        account_data = data["securitiesAccount"]
        balances = account_data["currentBalances"]

        return Account(
            account_id=account_data["accountId"],
            broker=BrokerType.TD_AMERITRADE,
            cash=balances.get("cashBalance", 0.0),
            buying_power=balances.get("buyingPower", 0.0),
            portfolio_value=balances.get("liquidationValue", 0.0),
            equity=balances.get("equity", 0.0),
            last_equity=balances.get("equity", 0.0),  # TD doesn't provide last equity
            unrealized_pl=balances.get("totalUnrealizedPL", 0.0),
            realized_pl_today=0.0,  # Not provided by TD in account endpoint
            pattern_day_trader=account_data.get("isDayTrader", False),
            trading_blocked=False,  # Not provided
            account_blocked=False,  # Not provided
            multiplier=1.0,  # TD uses different margin system
            currency="USD",
        )

    async def get_positions(self) -> List[Position]:
        """Get all open positions"""
        if not self.client:
            raise RuntimeError("Not connected to TD Ameritrade")

        await self._ensure_token_valid()

        response = await self.client.get(
            f"/accounts/{self.account_id}",
            headers=self._get_headers(),
            params={"fields": "positions"},
        )
        response.raise_for_status()
        data = response.json()

        positions = []
        account_data = data["securitiesAccount"]

        if "positions" in account_data:
            for pos in account_data["positions"]:
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
        """Parse TD Ameritrade position data"""
        instrument = data["instrument"]
        qty = data["longQuantity"] - data.get("shortQuantity", 0)
        side = OrderSide.BUY if qty > 0 else OrderSide.SELL

        return Position(
            symbol=instrument["symbol"],
            quantity=abs(qty),
            avg_entry_price=data["averagePrice"],
            current_price=data.get("marketValue", 0) / abs(qty) if qty != 0 else 0,
            market_value=data.get("marketValue", 0),
            cost_basis=abs(qty) * data["averagePrice"],
            unrealized_pl=data.get("currentDayProfitLoss", 0),
            unrealized_pl_percent=(data.get("currentDayProfitLoss", 0) / data.get("marketValue", 1)) * 100 if data.get("marketValue") else 0,
            side=side,
            asset_class=instrument.get("assetType", "EQUITY"),
        )

    async def place_order(self, order: Order) -> Order:
        """Place an order"""
        if not self.client:
            raise RuntimeError("Not connected to TD Ameritrade")

        await self._ensure_token_valid()

        # Build TD Ameritrade order structure
        order_data = {
            "orderType": self._map_order_type(order.order_type),
            "session": "NORMAL",
            "duration": self._map_time_in_force(order.time_in_force),
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": "BUY" if order.side == OrderSide.BUY else "SELL",
                    "quantity": order.quantity,
                    "instrument": {
                        "symbol": order.symbol,
                        "assetType": "EQUITY",
                    },
                }
            ],
        }

        # Add price based on order type
        if order.order_type == OrderType.LIMIT and order.price:
            order_data["price"] = order.price
        elif order.order_type == OrderType.STOP and order.stop_price:
            order_data["stopPrice"] = order.stop_price
        elif order.order_type == OrderType.STOP_LIMIT:
            if order.price and order.stop_price:
                order_data["price"] = order.price
                order_data["stopPrice"] = order.stop_price

        response = await self.client.post(
            f"/accounts/{self.account_id}/orders",
            headers=self._get_headers(),
            json=order_data,
        )
        response.raise_for_status()

        # TD returns order ID in Location header
        order_id = response.headers.get("Location", "").split("/")[-1]
        order.order_id = order_id
        order.status = OrderStatus.NEW

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
        """Place a bracket order (One-Cancels-Other)"""
        if not self.client:
            raise RuntimeError("Not connected to TD Ameritrade")

        await self._ensure_token_valid()

        # Build OCO (One-Cancels-Other) order
        order_data = {
            "orderType": "LIMIT" if entry_price else "MARKET",
            "session": "NORMAL",
            "duration": self._map_time_in_force(time_in_force),
            "orderStrategyType": "OCO",
            "orderLegCollection": [
                {
                    "instruction": "BUY" if side == OrderSide.BUY else "SELL",
                    "quantity": quantity,
                    "instrument": {
                        "symbol": symbol,
                        "assetType": "EQUITY",
                    },
                }
            ],
            "childOrderStrategies": [
                {
                    "orderType": "LIMIT",
                    "session": "NORMAL",
                    "duration": self._map_time_in_force(time_in_force),
                    "price": take_profit_price,
                    "orderLegCollection": [
                        {
                            "instruction": "SELL" if side == OrderSide.BUY else "BUY",
                            "quantity": quantity,
                            "instrument": {
                                "symbol": symbol,
                                "assetType": "EQUITY",
                            },
                        }
                    ],
                },
                {
                    "orderType": "STOP",
                    "session": "NORMAL",
                    "duration": self._map_time_in_force(time_in_force),
                    "stopPrice": stop_loss_price,
                    "orderLegCollection": [
                        {
                            "instruction": "SELL" if side == OrderSide.BUY else "BUY",
                            "quantity": quantity,
                            "instrument": {
                                "symbol": symbol,
                                "assetType": "EQUITY",
                            },
                        }
                    ],
                },
            ],
        }

        if entry_price:
            order_data["price"] = entry_price

        response = await self.client.post(
            f"/accounts/{self.account_id}/orders",
            headers=self._get_headers(),
            json=order_data,
        )
        response.raise_for_status()

        order_id = response.headers.get("Location", "").split("/")[-1]

        # Return placeholder orders (TD doesn't return full order details immediately)
        return [
            Order(
                order_id=order_id,
                symbol=symbol,
                side=side,
                order_type=OrderType.LIMIT if entry_price else OrderType.MARKET,
                quantity=quantity,
                price=entry_price,
                status=OrderStatus.NEW,
            )
        ]

    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an order"""
        if not self.client:
            raise RuntimeError("Not connected to TD Ameritrade")

        await self._ensure_token_valid()

        try:
            response = await self.client.delete(
                f"/accounts/{self.account_id}/orders/{order_id}",
                headers=self._get_headers(),
            )
            response.raise_for_status()
            return True
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to cancel order {order_id}: {e}")
            return False

    async def get_order(self, order_id: str) -> Optional[Order]:
        """Get order details"""
        if not self.client:
            raise RuntimeError("Not connected to TD Ameritrade")

        await self._ensure_token_valid()

        try:
            response = await self.client.get(
                f"/accounts/{self.account_id}/orders/{order_id}",
                headers=self._get_headers(),
            )
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
            raise RuntimeError("Not connected to TD Ameritrade")

        await self._ensure_token_valid()

        response = await self.client.get(
            f"/accounts/{self.account_id}/orders",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        data = response.json()

        orders = []
        for order_data in data[:limit]:
            order = self._parse_order(order_data)
            if status is None or order.status == status:
                orders.append(order)

        return orders

    async def get_current_price(self, symbol: str) -> float:
        """Get current market price"""
        if not self.client:
            raise RuntimeError("Not connected to TD Ameritrade")

        await self._ensure_token_valid()

        response = await self.client.get(
            f"/marketdata/{symbol}/quotes",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        data = response.json()

        quote = data.get(symbol, {})
        return quote.get("lastPrice", 0.0)

    def _parse_order(self, data: Dict[str, Any]) -> Order:
        """Parse TD Ameritrade order data"""
        leg = data["orderLegCollection"][0] if data.get("orderLegCollection") else {}
        instrument = leg.get("instrument", {})

        return Order(
            order_id=str(data.get("orderId", "")),
            symbol=instrument.get("symbol", ""),
            side=OrderSide.BUY if leg.get("instruction") == "BUY" else OrderSide.SELL,
            order_type=self._parse_order_type(data.get("orderType", "MARKET")),
            quantity=leg.get("quantity", 0),
            filled_qty=leg.get("filledQuantity", 0),
            price=data.get("price"),
            stop_price=data.get("stopPrice"),
            time_in_force=self._parse_time_in_force(data.get("duration", "DAY")),
            status=self._parse_status(data.get("status", "")),
            created_at=datetime.fromisoformat(data["enteredTime"].replace("Z", "+00:00")) if data.get("enteredTime") else None,
        )

    def _map_order_type(self, order_type: OrderType) -> str:
        """Map our OrderType to TD order type"""
        mapping = {
            OrderType.MARKET: "MARKET",
            OrderType.LIMIT: "LIMIT",
            OrderType.STOP: "STOP",
            OrderType.STOP_LIMIT: "STOP_LIMIT",
            OrderType.TRAILING_STOP: "TRAILING_STOP",
        }
        return mapping.get(order_type, "MARKET")

    def _parse_order_type(self, td_type: str) -> OrderType:
        """Parse TD order type to our OrderType"""
        mapping = {
            "MARKET": OrderType.MARKET,
            "LIMIT": OrderType.LIMIT,
            "STOP": OrderType.STOP,
            "STOP_LIMIT": OrderType.STOP_LIMIT,
            "TRAILING_STOP": OrderType.TRAILING_STOP,
        }
        return mapping.get(td_type, OrderType.MARKET)

    def _map_time_in_force(self, tif: TimeInForce) -> str:
        """Map our TimeInForce to TD duration"""
        mapping = {
            TimeInForce.DAY: "DAY",
            TimeInForce.GTC: "GTC",
            TimeInForce.IOC: "IOC",
            TimeInForce.FOK: "FOK",
        }
        return mapping.get(tif, "DAY")

    def _parse_time_in_force(self, td_duration: str) -> TimeInForce:
        """Parse TD duration to our TimeInForce"""
        mapping = {
            "DAY": TimeInForce.DAY,
            "GTC": TimeInForce.GTC,
            "GOOD_TILL_CANCEL": TimeInForce.GTC,
            "FILL_OR_KILL": TimeInForce.FOK,
        }
        return mapping.get(td_duration, TimeInForce.DAY)

    def _parse_status(self, td_status: str) -> OrderStatus:
        """Parse TD order status to our OrderStatus"""
        mapping = {
            "AWAITING_PARENT_ORDER": OrderStatus.PENDING,
            "AWAITING_CONDITION": OrderStatus.PENDING,
            "AWAITING_MANUAL_REVIEW": OrderStatus.PENDING,
            "ACCEPTED": OrderStatus.NEW,
            "AWAITING_UR_OUT": OrderStatus.NEW,
            "PENDING_ACTIVATION": OrderStatus.PENDING,
            "QUEUED": OrderStatus.PENDING,
            "WORKING": OrderStatus.NEW,
            "REJECTED": OrderStatus.REJECTED,
            "PENDING_CANCEL": OrderStatus.PENDING,
            "CANCELED": OrderStatus.CANCELED,
            "PENDING_REPLACE": OrderStatus.PENDING,
            "REPLACED": OrderStatus.CANCELED,
            "FILLED": OrderStatus.FILLED,
            "EXPIRED": OrderStatus.EXPIRED,
        }
        return mapping.get(td_status, OrderStatus.PENDING)
