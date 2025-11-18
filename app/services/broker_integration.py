"""
Broker Integration Module for Paper Trading Automation

Provides stubs for real broker integration with:
- Alpaca API
- Interactive Brokers
- Manual review before execution
- Emergency kill switch
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from abc import ABC, abstractmethod
import logging

from app.services.order_manager import Order, OrderType, OrderSide, OrderStatus

logger = logging.getLogger(__name__)


class BrokerType(Enum):
    """Supported broker types"""
    PAPER = "paper"
    ALPACA = "alpaca"
    INTERACTIVE_BROKERS = "interactive_brokers"


class ExecutionMode(Enum):
    """Execution modes"""
    PAPER_ONLY = "paper_only"
    MANUAL_REVIEW = "manual_review"
    AUTOMATIC = "automatic"


@dataclass
class ExecutionRequest:
    """Request to execute an order"""
    order: Order
    broker: BrokerType
    mode: ExecutionMode
    requested_at: datetime
    approved: bool = False
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    executed: bool = False
    executed_at: Optional[datetime] = None
    execution_price: Optional[float] = None
    notes: str = ""


@dataclass
class BrokerConfig:
    """Broker configuration"""
    broker_type: BrokerType
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    base_url: Optional[str] = None
    paper_trading: bool = True
    enabled: bool = False


class KillSwitch:
    """
    Emergency kill switch to halt all trading
    """

    def __init__(self):
        self._engaged = False
        self._engaged_at: Optional[datetime] = None
        self._engaged_by: Optional[str] = None
        self._reason: str = ""
        self.logger = logging.getLogger(__name__)

    def engage(self, reason: str, engaged_by: str = "system") -> None:
        """Engage the kill switch"""
        self._engaged = True
        self._engaged_at = datetime.now()
        self._engaged_by = engaged_by
        self._reason = reason

        self.logger.critical(
            f"KILL SWITCH ENGAGED by {engaged_by}: {reason}"
        )

    def disengage(self, disengaged_by: str = "system") -> None:
        """Disengage the kill switch"""
        was_engaged = self._engaged
        self._engaged = False

        if was_engaged:
            self.logger.warning(
                f"Kill switch disengaged by {disengaged_by}"
            )

    @property
    def is_engaged(self) -> bool:
        """Check if kill switch is engaged"""
        return self._engaged

    @property
    def status(self) -> Dict[str, Any]:
        """Get kill switch status"""
        return {
            "engaged": self._engaged,
            "engaged_at": self._engaged_at.isoformat() if self._engaged_at else None,
            "engaged_by": self._engaged_by,
            "reason": self._reason
        }


class BrokerInterface(ABC):
    """
    Abstract base class for broker integrations
    """

    def __init__(self, config: BrokerConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def connect(self) -> bool:
        """Connect to broker"""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from broker"""
        pass

    @abstractmethod
    def submit_order(self, order: Order) -> bool:
        """Submit order to broker"""
        pass

    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """Cancel order"""
        pass

    @abstractmethod
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information"""
        pass

    @abstractmethod
    def get_positions(self) -> List[Dict[str, Any]]:
        """Get current positions"""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Check if connected to broker"""
        pass


class PaperBroker(BrokerInterface):
    """
    Paper trading broker (simulated execution)
    """

    def __init__(self, config: BrokerConfig):
        super().__init__(config)
        self._connected = False
        self._account_value = 100000.0  # Default paper account
        self._positions: Dict[str, Any] = {}

    def connect(self) -> bool:
        """Connect to paper broker"""
        self._connected = True
        self.logger.info("Connected to paper broker")
        return True

    def disconnect(self) -> None:
        """Disconnect from paper broker"""
        self._connected = False
        self.logger.info("Disconnected from paper broker")

    def submit_order(self, order: Order) -> bool:
        """Submit order (simulated)"""
        if not self._connected:
            self.logger.error("Not connected to broker")
            return False

        self.logger.info(
            f"Paper order submitted: {order.side.value} {order.quantity} {order.ticker} "
            f"@ ${order.limit_price or 'MARKET'}"
        )
        return True

    def cancel_order(self, order_id: str) -> bool:
        """Cancel order (simulated)"""
        self.logger.info(f"Paper order cancelled: {order_id}")
        return True

    def get_account_info(self) -> Dict[str, Any]:
        """Get account information"""
        return {
            "account_value": self._account_value,
            "cash": self._account_value * 0.5,
            "buying_power": self._account_value * 2,  # Margin
            "positions_value": sum(p.get("value", 0) for p in self._positions.values())
        }

    def get_positions(self) -> List[Dict[str, Any]]:
        """Get current positions"""
        return list(self._positions.values())

    def is_connected(self) -> bool:
        """Check if connected"""
        return self._connected


class AlpacaBroker(BrokerInterface):
    """
    Alpaca API integration stub

    STUB: This is a placeholder for real Alpaca integration.
    To implement:
    1. Install alpaca-trade-api: pip install alpaca-trade-api
    2. Import: from alpaca_trade_api import REST
    3. Initialize API client with credentials
    4. Implement real API calls
    """

    def __init__(self, config: BrokerConfig):
        super().__init__(config)
        self._connected = False
        self._api_client = None

        self.logger.warning(
            "AlpacaBroker is a STUB. Real implementation required for live trading."
        )

    def connect(self) -> bool:
        """Connect to Alpaca API"""
        if not self.config.api_key or not self.config.api_secret:
            self.logger.error("Alpaca API credentials not configured")
            return False

        try:
            # STUB: Real implementation would be:
            # from alpaca_trade_api import REST
            # self._api_client = REST(
            #     key_id=self.config.api_key,
            #     secret_key=self.config.api_secret,
            #     base_url=self.config.base_url or 'https://paper-api.alpaca.markets'
            # )
            # account = self._api_client.get_account()
            # self._connected = True

            self.logger.warning("Alpaca connect() called - STUB ONLY")
            return False

        except Exception as e:
            self.logger.error(f"Failed to connect to Alpaca: {e}")
            return False

    def disconnect(self) -> None:
        """Disconnect from Alpaca"""
        self._connected = False
        self._api_client = None

    def submit_order(self, order: Order) -> bool:
        """Submit order to Alpaca"""
        if not self._connected:
            self.logger.error("Not connected to Alpaca")
            return False

        try:
            # STUB: Real implementation would be:
            # self._api_client.submit_order(
            #     symbol=order.ticker,
            #     qty=order.quantity,
            #     side=order.side.value,
            #     type=order.order_type.value,
            #     time_in_force='gtc',
            #     limit_price=order.limit_price,
            #     stop_price=order.stop_price
            # )

            self.logger.warning(
                f"Alpaca submit_order() called - STUB ONLY: "
                f"{order.side.value} {order.quantity} {order.ticker}"
            )
            return False

        except Exception as e:
            self.logger.error(f"Failed to submit Alpaca order: {e}")
            return False

    def cancel_order(self, order_id: str) -> bool:
        """Cancel Alpaca order"""
        if not self._connected:
            return False

        # STUB: Real implementation would be:
        # self._api_client.cancel_order(order_id)

        self.logger.warning(f"Alpaca cancel_order() called - STUB ONLY: {order_id}")
        return False

    def get_account_info(self) -> Dict[str, Any]:
        """Get Alpaca account information"""
        if not self._connected:
            return {}

        # STUB: Real implementation would be:
        # account = self._api_client.get_account()
        # return {
        #     "account_value": float(account.equity),
        #     "cash": float(account.cash),
        #     "buying_power": float(account.buying_power),
        #     ...
        # }

        self.logger.warning("Alpaca get_account_info() called - STUB ONLY")
        return {}

    def get_positions(self) -> List[Dict[str, Any]]:
        """Get Alpaca positions"""
        if not self._connected:
            return []

        # STUB: Real implementation would be:
        # positions = self._api_client.list_positions()
        # return [...]

        self.logger.warning("Alpaca get_positions() called - STUB ONLY")
        return []

    def is_connected(self) -> bool:
        """Check if connected to Alpaca"""
        return self._connected


class InteractiveBrokersBroker(BrokerInterface):
    """
    Interactive Brokers integration stub

    STUB: This is a placeholder for real IB integration.
    To implement:
    1. Install ib_insync: pip install ib_insync
    2. Import: from ib_insync import IB, Stock, MarketOrder, LimitOrder
    3. Connect to TWS or IB Gateway
    4. Implement real API calls
    """

    def __init__(self, config: BrokerConfig):
        super().__init__(config)
        self._connected = False
        self._ib_client = None

        self.logger.warning(
            "InteractiveBrokersBroker is a STUB. Real implementation required for live trading."
        )

    def connect(self) -> bool:
        """Connect to Interactive Brokers"""
        try:
            # STUB: Real implementation would be:
            # from ib_insync import IB
            # self._ib_client = IB()
            # self._ib_client.connect('127.0.0.1', 7497, clientId=1)  # TWS
            # self._connected = True

            self.logger.warning("IB connect() called - STUB ONLY")
            return False

        except Exception as e:
            self.logger.error(f"Failed to connect to Interactive Brokers: {e}")
            return False

    def disconnect(self) -> None:
        """Disconnect from Interactive Brokers"""
        # STUB: Real implementation would be:
        # if self._ib_client:
        #     self._ib_client.disconnect()

        self._connected = False
        self._ib_client = None

    def submit_order(self, order: Order) -> bool:
        """Submit order to Interactive Brokers"""
        if not self._connected:
            self.logger.error("Not connected to Interactive Brokers")
            return False

        try:
            # STUB: Real implementation would be:
            # from ib_insync import Stock, MarketOrder, LimitOrder
            # contract = Stock(order.ticker, 'SMART', 'USD')
            # if order.order_type == OrderType.MARKET:
            #     ib_order = MarketOrder(order.side.value.upper(), order.quantity)
            # else:
            #     ib_order = LimitOrder(order.side.value.upper(), order.quantity, order.limit_price)
            # trade = self._ib_client.placeOrder(contract, ib_order)

            self.logger.warning(
                f"IB submit_order() called - STUB ONLY: "
                f"{order.side.value} {order.quantity} {order.ticker}"
            )
            return False

        except Exception as e:
            self.logger.error(f"Failed to submit IB order: {e}")
            return False

    def cancel_order(self, order_id: str) -> bool:
        """Cancel IB order"""
        if not self._connected:
            return False

        # STUB: Real implementation would query orders and cancel
        self.logger.warning(f"IB cancel_order() called - STUB ONLY: {order_id}")
        return False

    def get_account_info(self) -> Dict[str, Any]:
        """Get IB account information"""
        if not self._connected:
            return {}

        # STUB: Real implementation would be:
        # account_values = self._ib_client.accountValues()
        # ...

        self.logger.warning("IB get_account_info() called - STUB ONLY")
        return {}

    def get_positions(self) -> List[Dict[str, Any]]:
        """Get IB positions"""
        if not self._connected:
            return []

        # STUB: Real implementation would be:
        # positions = self._ib_client.positions()
        # ...

        self.logger.warning("IB get_positions() called - STUB ONLY")
        return []

    def is_connected(self) -> bool:
        """Check if connected to IB"""
        return self._connected


class BrokerManager:
    """
    Manage broker connections and order execution with safety features
    """

    def __init__(self):
        self.brokers: Dict[BrokerType, BrokerInterface] = {}
        self.kill_switch = KillSwitch()
        self.execution_mode = ExecutionMode.PAPER_ONLY
        self.pending_requests: Dict[str, ExecutionRequest] = {}
        self.logger = logging.getLogger(__name__)

    def add_broker(self, broker: BrokerInterface) -> None:
        """Add a broker"""
        self.brokers[broker.config.broker_type] = broker
        self.logger.info(f"Added broker: {broker.config.broker_type.value}")

    def set_execution_mode(self, mode: ExecutionMode) -> None:
        """Set execution mode"""
        old_mode = self.execution_mode
        self.execution_mode = mode
        self.logger.warning(
            f"Execution mode changed: {old_mode.value} -> {mode.value}"
        )

    def submit_order(
        self,
        order: Order,
        broker_type: BrokerType = BrokerType.PAPER
    ) -> bool:
        """
        Submit order with safety checks

        Args:
            order: Order to submit
            broker_type: Broker to use

        Returns:
            True if submitted successfully
        """
        # Check kill switch
        if self.kill_switch.is_engaged:
            self.logger.error(
                f"Order rejected - Kill switch engaged: {self.kill_switch._reason}"
            )
            return False

        # Check if broker exists
        if broker_type not in self.brokers:
            self.logger.error(f"Broker {broker_type.value} not configured")
            return False

        broker = self.brokers[broker_type]

        # Check if broker is connected
        if not broker.is_connected():
            self.logger.error(f"Broker {broker_type.value} not connected")
            return False

        # Create execution request
        request = ExecutionRequest(
            order=order,
            broker=broker_type,
            mode=self.execution_mode,
            requested_at=datetime.now()
        )

        # Handle based on execution mode
        if self.execution_mode == ExecutionMode.PAPER_ONLY:
            # Always execute in paper mode
            request.approved = True
            request.approved_by = "automatic"
            request.approved_at = datetime.now()
            return self._execute_request(request)

        elif self.execution_mode == ExecutionMode.MANUAL_REVIEW:
            # Queue for manual approval
            request_id = f"REQ_{order.order_id}"
            self.pending_requests[request_id] = request
            self.logger.info(
                f"Order queued for manual review: {request_id}"
            )
            return True

        elif self.execution_mode == ExecutionMode.AUTOMATIC:
            # Execute immediately (DANGEROUS - use with caution!)
            self.logger.warning(
                "Executing order in AUTOMATIC mode - no safety checks!"
            )
            request.approved = True
            request.approved_by = "automatic"
            request.approved_at = datetime.now()
            return self._execute_request(request)

        return False

    def approve_request(self, request_id: str, approved_by: str) -> bool:
        """Approve a pending execution request"""
        if request_id not in self.pending_requests:
            self.logger.error(f"Request {request_id} not found")
            return False

        request = self.pending_requests[request_id]
        request.approved = True
        request.approved_by = approved_by
        request.approved_at = datetime.now()

        # Execute the order
        success = self._execute_request(request)

        # Remove from pending
        del self.pending_requests[request_id]

        return success

    def reject_request(self, request_id: str, reason: str = "") -> bool:
        """Reject a pending execution request"""
        if request_id not in self.pending_requests:
            return False

        request = self.pending_requests[request_id]
        self.logger.info(
            f"Request {request_id} rejected: {reason}"
        )

        del self.pending_requests[request_id]
        return True

    def _execute_request(self, request: ExecutionRequest) -> bool:
        """Execute an approved request"""
        broker = self.brokers[request.broker]

        try:
            success = broker.submit_order(request.order)

            if success:
                request.executed = True
                request.executed_at = datetime.now()
                self.logger.info(
                    f"Order executed: {request.order.ticker} via {request.broker.value}"
                )
            else:
                self.logger.error(
                    f"Order execution failed: {request.order.ticker}"
                )

            return success

        except Exception as e:
            self.logger.error(f"Error executing order: {e}", exc_info=True)
            return False

    def get_pending_requests(self) -> List[ExecutionRequest]:
        """Get all pending execution requests"""
        return list(self.pending_requests.values())

    def engage_kill_switch(self, reason: str, engaged_by: str = "system") -> None:
        """Engage the emergency kill switch"""
        self.kill_switch.engage(reason, engaged_by)

    def disengage_kill_switch(self, disengaged_by: str = "system") -> None:
        """Disengage the kill switch"""
        self.kill_switch.disengage(disengaged_by)

    def get_status(self) -> Dict[str, Any]:
        """Get broker manager status"""
        return {
            "execution_mode": self.execution_mode.value,
            "kill_switch": self.kill_switch.status,
            "brokers": {
                broker_type.value: broker.is_connected()
                for broker_type, broker in self.brokers.items()
            },
            "pending_requests": len(self.pending_requests)
        }
