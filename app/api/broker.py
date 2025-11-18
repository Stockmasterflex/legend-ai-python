"""
Broker API Endpoints

Endpoints for broker connections, live trading, and position management.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from app.brokers.base import (
    BrokerType,
    OrderType,
    OrderSide,
    OrderStatus,
    TimeInForce,
    Order,
    Position,
    Account,
)
from app.brokers.factory import BrokerFactory
from app.services.live_trading import (
    LiveTradingService,
    QuickEntryRequest,
    BracketOrderRequest,
    TrailingStopRequest,
)
from app.services.position_sync import PositionSyncService
from app.services.execution_analytics import ExecutionAnalyticsService
from app.config import get_settings

router = APIRouter(prefix="/api/broker", tags=["broker"])

# Global services (in production, use dependency injection with proper lifecycle)
_broker_connections: Dict[str, Any] = {}
_analytics_service = ExecutionAnalyticsService()


class BrokerConnectionRequest(BaseModel):
    """Request to connect to a broker"""
    broker_type: BrokerType
    paper_trading: bool = True
    credentials: Optional[Dict[str, str]] = None  # Optional, uses config if not provided


class PlaceOrderRequest(BaseModel):
    """Request to place an order"""
    broker_type: BrokerType
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None
    time_in_force: TimeInForce = TimeInForce.DAY


class QuickEntryAPIRequest(BaseModel):
    """Quick entry request for API"""
    broker_type: BrokerType
    symbol: str
    side: OrderSide
    account_size: float
    risk_percent: float = 1.0
    entry_price: Optional[float] = None
    stop_loss_price: float
    target_price: Optional[float] = None
    order_type: OrderType = OrderType.MARKET


class BracketOrderAPIRequest(BaseModel):
    """Bracket order request for API"""
    broker_type: BrokerType
    symbol: str
    side: OrderSide
    quantity: float
    entry_price: Optional[float] = None
    take_profit_price: float
    stop_loss_price: float


def get_broker_credentials(broker_type: BrokerType) -> Dict[str, str]:
    """Get broker credentials from settings"""
    settings = get_settings()

    if broker_type == BrokerType.ALPACA:
        return {
            "api_key": settings.alpaca_api_key or "",
            "api_secret": settings.alpaca_api_secret or "",
        }
    elif broker_type == BrokerType.TD_AMERITRADE:
        return {
            "api_key": settings.td_ameritrade_api_key or "",
            "refresh_token": settings.td_ameritrade_refresh_token or "",
            "account_id": settings.td_ameritrade_account_id or "",
        }
    elif broker_type == BrokerType.INTERACTIVE_BROKERS:
        return {
            "gateway_url": settings.ib_gateway_url or "https://localhost:5000/v1/api",
            "account_id": settings.ib_account_id or "",
        }
    elif broker_type == BrokerType.TRADESTATION:
        return {
            "api_key": settings.tradestation_api_key or "",
            "api_secret": settings.tradestation_api_secret or "",
            "refresh_token": settings.tradestation_refresh_token or "",
            "account_id": settings.tradestation_account_id or "",
        }
    else:
        raise ValueError(f"Unsupported broker type: {broker_type}")


async def get_connected_broker(broker_type: BrokerType):
    """Get or create broker connection"""
    broker_key = f"{broker_type.value}"

    if broker_key not in _broker_connections:
        # Create new connection
        settings = get_settings()
        credentials = get_broker_credentials(broker_type)

        broker = BrokerFactory.create(
            broker_type=broker_type,
            credentials=credentials,
            paper_trading=settings.broker_paper_trading,
        )

        # Connect
        connected = await broker.connect()
        if not connected:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to connect to {broker_type.value}"
            )

        _broker_connections[broker_key] = broker

    return _broker_connections[broker_key]


@router.post("/connect")
async def connect_broker(request: BrokerConnectionRequest):
    """
    Connect to a broker.

    Uses credentials from environment variables by default,
    or accepts credentials in the request.
    """
    try:
        credentials = request.credentials or get_broker_credentials(request.broker_type)

        broker = BrokerFactory.create(
            broker_type=request.broker_type,
            credentials=credentials,
            paper_trading=request.paper_trading,
        )

        connected = await broker.connect()

        if connected:
            broker_key = f"{request.broker_type.value}"
            _broker_connections[broker_key] = broker

            return {
                "status": "connected",
                "broker": request.broker_type.value,
                "paper_trading": request.paper_trading,
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to connect to broker")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/disconnect/{broker_type}")
async def disconnect_broker(broker_type: BrokerType):
    """Disconnect from a broker"""
    broker_key = f"{broker_type.value}"

    if broker_key not in _broker_connections:
        raise HTTPException(status_code=404, detail="Broker not connected")

    broker = _broker_connections[broker_key]
    await broker.disconnect()
    del _broker_connections[broker_key]

    return {"status": "disconnected", "broker": broker_type.value}


@router.get("/account/{broker_type}")
async def get_account(broker_type: BrokerType):
    """Get account information from broker"""
    broker = await get_connected_broker(broker_type)
    account = await broker.get_account()
    return account


@router.get("/positions/{broker_type}")
async def get_positions(broker_type: BrokerType):
    """Get all positions from broker"""
    broker = await get_connected_broker(broker_type)
    positions = await broker.get_positions()
    return {"positions": positions, "count": len(positions)}


@router.get("/positions/{broker_type}/{symbol}")
async def get_position(broker_type: BrokerType, symbol: str):
    """Get position for specific symbol"""
    broker = await get_connected_broker(broker_type)
    position = await broker.get_position(symbol)

    if not position:
        raise HTTPException(status_code=404, detail=f"No position found for {symbol}")

    return position


@router.get("/portfolio/{broker_type}")
async def get_portfolio_summary(broker_type: BrokerType):
    """Get portfolio summary with P&L"""
    broker = await get_connected_broker(broker_type)
    sync_service = PositionSyncService(broker)
    summary = await sync_service.get_portfolio_summary()
    return summary


@router.post("/orders/place")
async def place_order(request: PlaceOrderRequest):
    """Place an order"""
    broker = await get_connected_broker(request.broker_type)

    order = Order(
        symbol=request.symbol,
        side=request.side,
        order_type=request.order_type,
        quantity=request.quantity,
        price=request.price,
        stop_price=request.stop_price,
        time_in_force=request.time_in_force,
    )

    # Get current price for analytics
    try:
        current_price = await broker.get_current_price(request.symbol)
    except Exception:
        current_price = None

    placed_order = await broker.place_order(order)

    # Record execution if filled
    if placed_order.status in [OrderStatus.FILLED, OrderStatus.PARTIALLY_FILLED]:
        _analytics_service.record_execution(placed_order, current_price)

    return placed_order


@router.post("/orders/quick-entry")
async def quick_entry(request: QuickEntryAPIRequest):
    """
    Place a quick entry order with automatic position sizing.
    Perfect for one-click trading from charts.
    """
    broker = await get_connected_broker(request.broker_type)
    trading_service = LiveTradingService(broker)

    quick_entry_request = QuickEntryRequest(
        symbol=request.symbol,
        side=request.side,
        account_size=request.account_size,
        risk_percent=request.risk_percent,
        entry_price=request.entry_price,
        stop_loss_price=request.stop_loss_price,
        target_price=request.target_price,
        order_type=request.order_type,
    )

    result = await trading_service.quick_entry(quick_entry_request)

    # Record execution
    if result["order"].status in [OrderStatus.FILLED, OrderStatus.PARTIALLY_FILLED]:
        _analytics_service.record_execution(result["order"])

    return result


@router.post("/orders/bracket")
async def place_bracket_order(request: BracketOrderAPIRequest):
    """Place a bracket order (entry + take profit + stop loss)"""
    broker = await get_connected_broker(request.broker_type)
    trading_service = LiveTradingService(broker)

    bracket_request = BracketOrderRequest(
        symbol=request.symbol,
        side=request.side,
        quantity=request.quantity,
        entry_price=request.entry_price,
        take_profit_price=request.take_profit_price,
        stop_loss_price=request.stop_loss_price,
    )

    orders = await trading_service.place_bracket_order(bracket_request)

    return {"orders": orders, "count": len(orders)}


@router.delete("/orders/{broker_type}/{order_id}")
async def cancel_order(broker_type: BrokerType, order_id: str):
    """Cancel an order"""
    broker = await get_connected_broker(broker_type)
    success = await broker.cancel_order(order_id)

    if not success:
        raise HTTPException(status_code=400, detail="Failed to cancel order")

    return {"status": "canceled", "order_id": order_id}


@router.get("/orders/{broker_type}")
async def get_orders(
    broker_type: BrokerType,
    status: Optional[OrderStatus] = None,
    limit: int = 100,
):
    """Get orders"""
    broker = await get_connected_broker(broker_type)
    orders = await broker.get_orders(status=status, limit=limit)
    return {"orders": orders, "count": len(orders)}


@router.post("/positions/close/{broker_type}/{symbol}")
async def close_position(
    broker_type: BrokerType,
    symbol: str,
    quantity: Optional[float] = None,
):
    """Close a position (or partial position)"""
    broker = await get_connected_broker(broker_type)
    trading_service = LiveTradingService(broker)

    order = await trading_service.close_position(symbol, quantity)

    return order


@router.get("/analytics/execution")
async def get_execution_analytics(
    symbol: Optional[str] = None,
    days: int = 30,
):
    """Get execution analytics"""
    from datetime import timedelta

    start_date = datetime.now() - timedelta(days=days)
    stats = _analytics_service.get_aggregate_stats(
        symbol=symbol,
        start_date=start_date,
    )

    return stats


@router.get("/analytics/slippage")
async def get_slippage_analysis(symbol: Optional[str] = None):
    """Get slippage analysis"""
    analysis = _analytics_service.get_slippage_analysis(symbol)
    return analysis


@router.get("/brokers/supported")
async def get_supported_brokers():
    """Get list of supported brokers"""
    brokers = BrokerFactory.supported_brokers()

    return {
        "brokers": [
            {
                "type": broker.value,
                "name": broker.value.replace("_", " ").title(),
                "required_credentials": BrokerFactory.get_required_credentials(broker),
            }
            for broker in brokers
        ]
    }


@router.get("/price/{broker_type}/{symbol}")
async def get_current_price(broker_type: BrokerType, symbol: str):
    """Get current market price for symbol"""
    broker = await get_connected_broker(broker_type)
    price = await broker.get_current_price(symbol)

    return {
        "symbol": symbol,
        "price": price,
        "timestamp": datetime.now().isoformat(),
    }
