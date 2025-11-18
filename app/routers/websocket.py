"""
WebSocket Router for Real-Time Streaming
"""
import asyncio
import json
import logging
import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends
from pydantic import BaseModel, Field

from app.services.websocket_manager import get_manager

logger = logging.getLogger(__name__)

router = APIRouter(tags=["websocket"])


# WebSocket Message Models
class WSMessage(BaseModel):
    """Base WebSocket message"""
    type: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class SubscribeMessage(BaseModel):
    """Subscribe to a data stream"""
    type: str = "subscribe"
    channel: str  # ticker, patterns, alerts, market_status
    ticker: Optional[str] = None  # Required if channel is "ticker"


class UnsubscribeMessage(BaseModel):
    """Unsubscribe from a data stream"""
    type: str = "unsubscribe"
    channel: str
    ticker: Optional[str] = None


class PingMessage(BaseModel):
    """Heartbeat ping"""
    type: str = "ping"


class PriceUpdateMessage(WSMessage):
    """Price update message"""
    type: str = "price_update"
    ticker: str
    price: float
    change: float
    change_percent: float
    volume: int
    high: float
    low: float
    open: float


class PatternAlertMessage(WSMessage):
    """Pattern detection alert"""
    type: str = "pattern_alert"
    ticker: str
    pattern_type: str
    score: float
    entry_price: float
    stop_price: float
    target_price: float
    risk_reward_ratio: float
    message: str


class AlertTriggerMessage(WSMessage):
    """Alert trigger notification"""
    type: str = "alert_trigger"
    ticker: str
    alert_type: str
    trigger_price: float
    current_price: float
    message: str


class MarketStatusMessage(WSMessage):
    """Market status change"""
    type: str = "market_status"
    status: str  # open, closed, pre_market, after_hours
    next_open: Optional[str] = None
    next_close: Optional[str] = None


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str = Query(default="default"),
    connection_id: Optional[str] = Query(default=None)
):
    """
    Main WebSocket endpoint for real-time streaming.

    **Connection:**
    ```javascript
    const ws = new WebSocket('ws://localhost:8000/api/ws?user_id=user123');
    ```

    **Message Protocol:**

    1. **Subscribe to ticker price updates:**
    ```json
    {
        "type": "subscribe",
        "channel": "ticker",
        "ticker": "AAPL"
    }
    ```

    2. **Subscribe to pattern alerts:**
    ```json
    {
        "type": "subscribe",
        "channel": "patterns"
    }
    ```

    3. **Subscribe to alert triggers:**
    ```json
    {
        "type": "subscribe",
        "channel": "alerts"
    }
    ```

    4. **Subscribe to market status:**
    ```json
    {
        "type": "subscribe",
        "channel": "market_status"
    }
    ```

    5. **Heartbeat ping:**
    ```json
    {
        "type": "ping"
    }
    ```

    **Server Messages:**

    - Connection acknowledgment
    - Price updates
    - Pattern alerts
    - Alert triggers
    - Market status changes
    - Subscription confirmations
    - Pong responses
    """
    manager = get_manager()

    # Generate connection ID if not provided
    if not connection_id:
        connection_id = f"{user_id}_{uuid.uuid4().hex[:8]}"

    try:
        # Connect to manager
        await manager.connect(websocket, connection_id, user_id)

        # Message handling loop
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                message = json.loads(data)

                message_type = message.get("type")

                if message_type == "subscribe":
                    await _handle_subscribe(manager, connection_id, message)
                elif message_type == "unsubscribe":
                    await _handle_unsubscribe(manager, connection_id, message)
                elif message_type == "ping":
                    await manager.heartbeat(connection_id)
                else:
                    logger.warning(f"Unknown message type: {message_type}")
                    await manager.send_personal_message(connection_id, {
                        "type": "error",
                        "message": f"Unknown message type: {message_type}",
                        "timestamp": datetime.utcnow().isoformat()
                    })

                manager.stats["messages_received"] += 1

            except json.JSONDecodeError:
                logger.error(f"Invalid JSON from {connection_id}")
                await manager.send_personal_message(connection_id, {
                    "type": "error",
                    "message": "Invalid JSON",
                    "timestamp": datetime.utcnow().isoformat()
                })

    except WebSocketDisconnect:
        manager.disconnect(connection_id)
        logger.info(f"Client {connection_id} disconnected")

    except Exception as e:
        logger.error(f"WebSocket error for {connection_id}: {e}")
        manager.disconnect(connection_id)


async def _handle_subscribe(manager, connection_id: str, message: dict):
    """Handle subscription request"""
    channel = message.get("channel")
    ticker = message.get("ticker")

    if channel == "ticker":
        if not ticker:
            await manager.send_personal_message(connection_id, {
                "type": "error",
                "message": "Ticker symbol required for ticker channel",
                "timestamp": datetime.utcnow().isoformat()
            })
            return

        await manager.subscribe_ticker(connection_id, ticker)

    elif channel == "patterns":
        await manager.subscribe_patterns(connection_id)

    elif channel == "alerts":
        await manager.subscribe_alerts(connection_id)

    elif channel == "market_status":
        await manager.subscribe_market_status(connection_id)

    else:
        await manager.send_personal_message(connection_id, {
            "type": "error",
            "message": f"Unknown channel: {channel}",
            "timestamp": datetime.utcnow().isoformat()
        })


async def _handle_unsubscribe(manager, connection_id: str, message: dict):
    """Handle unsubscription request"""
    channel = message.get("channel")
    ticker = message.get("ticker")

    if channel == "ticker" and ticker:
        await manager.unsubscribe_ticker(connection_id, ticker)
    else:
        # For now, just send acknowledgment
        await manager.send_personal_message(connection_id, {
            "type": "subscription",
            "action": "unsubscribed",
            "channel": channel,
            "timestamp": datetime.utcnow().isoformat()
        })


@router.get("/ws/stats")
async def get_websocket_stats():
    """
    Get WebSocket connection statistics.

    Returns connection counts, subscription info, and performance metrics.
    """
    manager = get_manager()
    return manager.get_stats()


@router.post("/ws/broadcast/price")
async def broadcast_price_update(
    ticker: str,
    price: float,
    change: float,
    change_percent: float,
    volume: int,
    high: float,
    low: float,
    open_price: float
):
    """
    Broadcast a price update to all subscribers.

    This is typically called by a background job that fetches real-time prices.
    """
    manager = get_manager()

    price_data = {
        "price": price,
        "change": change,
        "change_percent": change_percent,
        "volume": volume,
        "high": high,
        "low": low,
        "open": open_price
    }

    await manager.publish_price_update(ticker, price_data)

    return {
        "status": "success",
        "ticker": ticker,
        "subscribers": len(manager.ticker_subscriptions.get(ticker.upper(), set()))
    }


@router.post("/ws/broadcast/pattern")
async def broadcast_pattern_alert(
    ticker: str,
    pattern_type: str,
    score: float,
    entry_price: float,
    stop_price: float,
    target_price: float,
    risk_reward_ratio: float,
    message: str
):
    """
    Broadcast a pattern detection alert to all pattern subscribers.
    """
    manager = get_manager()

    pattern_data = {
        "ticker": ticker,
        "pattern_type": pattern_type,
        "score": score,
        "entry_price": entry_price,
        "stop_price": stop_price,
        "target_price": target_price,
        "risk_reward_ratio": risk_reward_ratio,
        "message": message
    }

    await manager.publish_pattern_alert(pattern_data)

    return {
        "status": "success",
        "pattern_type": pattern_type,
        "subscribers": len(manager.pattern_subscriptions)
    }


@router.post("/ws/broadcast/alert")
async def broadcast_alert_trigger(
    ticker: str,
    alert_type: str,
    trigger_price: float,
    current_price: float,
    message: str
):
    """
    Broadcast an alert trigger to all alert subscribers.
    """
    manager = get_manager()

    alert_data = {
        "ticker": ticker,
        "alert_type": alert_type,
        "trigger_price": trigger_price,
        "current_price": current_price,
        "message": message
    }

    await manager.publish_alert_trigger(alert_data)

    return {
        "status": "success",
        "alert_type": alert_type,
        "subscribers": len(manager.alert_subscriptions)
    }


@router.post("/ws/broadcast/market_status")
async def broadcast_market_status(
    status: str,
    next_open: Optional[str] = None,
    next_close: Optional[str] = None
):
    """
    Broadcast market status change to all market status subscribers.
    """
    manager = get_manager()

    status_data = {
        "status": status,
        "next_open": next_open,
        "next_close": next_close
    }

    await manager.publish_market_status(status_data)

    return {
        "status": "success",
        "market_status": status,
        "subscribers": len(manager.market_status_subscriptions)
    }
