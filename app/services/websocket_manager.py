"""
WebSocket Connection Manager with Connection Pooling and Redis Pub/Sub
"""
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Set, Optional, Any, List
from fastapi import WebSocket, WebSocketDisconnect
import redis.asyncio as redis
from collections import defaultdict
import time

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Manages WebSocket connections with connection pooling, heartbeat,
    and Redis Pub/Sub for horizontal scaling.
    """

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        # Active WebSocket connections by connection ID
        self.active_connections: Dict[str, WebSocket] = {}

        # Subscriptions: ticker -> set of connection IDs
        self.ticker_subscriptions: Dict[str, Set[str]] = defaultdict(set)

        # Pattern subscriptions: connection IDs interested in pattern alerts
        self.pattern_subscriptions: Set[str] = set()

        # Alert subscriptions: connection IDs interested in alert triggers
        self.alert_subscriptions: Set[str] = set()

        # Market status subscriptions
        self.market_status_subscriptions: Set[str] = set()

        # Connection metadata (user_id, subscription info, connection time)
        self.connection_metadata: Dict[str, Dict[str, Any]] = {}

        # Heartbeat tracking
        self.last_heartbeat: Dict[str, float] = {}

        # Redis pub/sub
        self.redis_url = redis_url
        self.redis_client: Optional[redis.Redis] = None
        self.pubsub: Optional[redis.client.PubSub] = None

        # Message persistence (for replay)
        self.message_history: Dict[str, List[Dict]] = defaultdict(list)
        self.max_history_per_ticker = 100

        # Performance tracking
        self.stats = {
            "total_connections": 0,
            "messages_sent": 0,
            "messages_received": 0,
            "errors": 0,
            "last_reset": datetime.utcnow()
        }

        # Throttle settings
        self.max_messages_per_second = 10
        self.last_message_time: Dict[str, List[float]] = defaultdict(list)

    async def initialize_redis(self):
        """Initialize Redis connection and pub/sub"""
        try:
            self.redis_client = await redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_keepalive=True
            )

            # Test connection
            await self.redis_client.ping()

            self.pubsub = self.redis_client.pubsub()

            # Subscribe to channels
            await self.pubsub.subscribe(
                "price_updates",
                "pattern_alerts",
                "alert_triggers",
                "market_status"
            )

            logger.info("Redis pub/sub initialized successfully")

            # Start listening for messages in background
            asyncio.create_task(self._redis_listener())

        except Exception as e:
            logger.error(f"Failed to initialize Redis: {e}")
            self.redis_client = None
            self.pubsub = None

    async def _redis_listener(self):
        """Background task to listen for Redis pub/sub messages"""
        if not self.pubsub:
            return

        try:
            async for message in self.pubsub.listen():
                if message["type"] == "message":
                    channel = message["channel"]
                    data = json.loads(message["data"])

                    # Route message to appropriate connections
                    if channel == "price_updates":
                        await self._handle_price_update(data)
                    elif channel == "pattern_alerts":
                        await self._handle_pattern_alert(data)
                    elif channel == "alert_triggers":
                        await self._handle_alert_trigger(data)
                    elif channel == "market_status":
                        await self._handle_market_status(data)

        except Exception as e:
            logger.error(f"Redis listener error: {e}")
            # Attempt to reconnect
            await asyncio.sleep(5)
            await self.initialize_redis()

    async def connect(self, websocket: WebSocket, connection_id: str, user_id: str = "default"):
        """Accept and register a new WebSocket connection"""
        await websocket.accept()

        self.active_connections[connection_id] = websocket
        self.connection_metadata[connection_id] = {
            "user_id": user_id,
            "connected_at": datetime.utcnow().isoformat(),
            "subscriptions": []
        }
        self.last_heartbeat[connection_id] = time.time()

        self.stats["total_connections"] += 1

        logger.info(f"WebSocket connected: {connection_id} (user: {user_id})")

        # Send connection acknowledgment
        await self.send_personal_message(connection_id, {
            "type": "connection",
            "status": "connected",
            "connection_id": connection_id,
            "timestamp": datetime.utcnow().isoformat()
        })

    def disconnect(self, connection_id: str):
        """Remove a WebSocket connection"""
        # Remove from all subscriptions
        for ticker_set in self.ticker_subscriptions.values():
            ticker_set.discard(connection_id)

        self.pattern_subscriptions.discard(connection_id)
        self.alert_subscriptions.discard(connection_id)
        self.market_status_subscriptions.discard(connection_id)

        # Remove connection
        self.active_connections.pop(connection_id, None)
        self.connection_metadata.pop(connection_id, None)
        self.last_heartbeat.pop(connection_id, None)
        self.last_message_time.pop(connection_id, None)

        logger.info(f"WebSocket disconnected: {connection_id}")

    async def subscribe_ticker(self, connection_id: str, ticker: str):
        """Subscribe a connection to ticker price updates"""
        ticker = ticker.upper()
        self.ticker_subscriptions[ticker].add(connection_id)

        # Update metadata
        if connection_id in self.connection_metadata:
            subs = self.connection_metadata[connection_id]["subscriptions"]
            if ticker not in subs:
                subs.append(ticker)

        logger.debug(f"Connection {connection_id} subscribed to {ticker}")

        # Send confirmation
        await self.send_personal_message(connection_id, {
            "type": "subscription",
            "action": "subscribed",
            "ticker": ticker,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Send recent history if available
        if ticker in self.message_history:
            history = self.message_history[ticker][-10:]  # Last 10 messages
            if history:
                await self.send_personal_message(connection_id, {
                    "type": "history",
                    "ticker": ticker,
                    "messages": history,
                    "timestamp": datetime.utcnow().isoformat()
                })

    async def unsubscribe_ticker(self, connection_id: str, ticker: str):
        """Unsubscribe a connection from ticker price updates"""
        ticker = ticker.upper()
        self.ticker_subscriptions[ticker].discard(connection_id)

        # Update metadata
        if connection_id in self.connection_metadata:
            subs = self.connection_metadata[connection_id]["subscriptions"]
            if ticker in subs:
                subs.remove(ticker)

        logger.debug(f"Connection {connection_id} unsubscribed from {ticker}")

        await self.send_personal_message(connection_id, {
            "type": "subscription",
            "action": "unsubscribed",
            "ticker": ticker,
            "timestamp": datetime.utcnow().isoformat()
        })

    async def subscribe_patterns(self, connection_id: str):
        """Subscribe to pattern detection alerts"""
        self.pattern_subscriptions.add(connection_id)
        logger.debug(f"Connection {connection_id} subscribed to pattern alerts")

        await self.send_personal_message(connection_id, {
            "type": "subscription",
            "action": "subscribed",
            "channel": "patterns",
            "timestamp": datetime.utcnow().isoformat()
        })

    async def subscribe_alerts(self, connection_id: str):
        """Subscribe to alert triggers"""
        self.alert_subscriptions.add(connection_id)
        logger.debug(f"Connection {connection_id} subscribed to alerts")

        await self.send_personal_message(connection_id, {
            "type": "subscription",
            "action": "subscribed",
            "channel": "alerts",
            "timestamp": datetime.utcnow().isoformat()
        })

    async def subscribe_market_status(self, connection_id: str):
        """Subscribe to market status changes"""
        self.market_status_subscriptions.add(connection_id)
        logger.debug(f"Connection {connection_id} subscribed to market status")

        await self.send_personal_message(connection_id, {
            "type": "subscription",
            "action": "subscribed",
            "channel": "market_status",
            "timestamp": datetime.utcnow().isoformat()
        })

    def _should_throttle(self, connection_id: str) -> bool:
        """Check if connection should be throttled"""
        now = time.time()
        times = self.last_message_time[connection_id]

        # Remove old timestamps (older than 1 second)
        times[:] = [t for t in times if now - t < 1.0]

        # Check if we've hit the limit
        return len(times) >= self.max_messages_per_second

    def _record_message_sent(self, connection_id: str):
        """Record that a message was sent to this connection"""
        now = time.time()
        self.last_message_time[connection_id].append(now)
        self.stats["messages_sent"] += 1

    async def send_personal_message(self, connection_id: str, message: dict):
        """Send a message to a specific connection"""
        websocket = self.active_connections.get(connection_id)
        if not websocket:
            return

        # Check throttling
        if self._should_throttle(connection_id):
            logger.warning(f"Throttling connection {connection_id}")
            return

        try:
            await websocket.send_json(message)
            self._record_message_sent(connection_id)
        except Exception as e:
            logger.error(f"Error sending message to {connection_id}: {e}")
            self.stats["errors"] += 1

    async def broadcast_to_ticker_subscribers(self, ticker: str, message: dict):
        """Broadcast a message to all subscribers of a ticker"""
        ticker = ticker.upper()
        subscribers = self.ticker_subscriptions.get(ticker, set())

        # Store in history
        self.message_history[ticker].append(message)
        if len(self.message_history[ticker]) > self.max_history_per_ticker:
            self.message_history[ticker] = self.message_history[ticker][-self.max_history_per_ticker:]

        # Send to all subscribers
        tasks = [
            self.send_personal_message(conn_id, message)
            for conn_id in subscribers
        ]

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def broadcast_to_pattern_subscribers(self, message: dict):
        """Broadcast a pattern alert to all pattern subscribers"""
        tasks = [
            self.send_personal_message(conn_id, message)
            for conn_id in self.pattern_subscriptions
        ]

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def broadcast_to_alert_subscribers(self, message: dict):
        """Broadcast an alert trigger to all alert subscribers"""
        tasks = [
            self.send_personal_message(conn_id, message)
            for conn_id in self.alert_subscriptions
        ]

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def broadcast_to_market_status_subscribers(self, message: dict):
        """Broadcast market status to all market status subscribers"""
        tasks = [
            self.send_personal_message(conn_id, message)
            for conn_id in self.market_status_subscriptions
        ]

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _handle_price_update(self, data: dict):
        """Handle price update from Redis pub/sub"""
        ticker = data.get("ticker")
        if ticker:
            await self.broadcast_to_ticker_subscribers(ticker, {
                "type": "price_update",
                **data
            })

    async def _handle_pattern_alert(self, data: dict):
        """Handle pattern alert from Redis pub/sub"""
        await self.broadcast_to_pattern_subscribers({
            "type": "pattern_alert",
            **data
        })

    async def _handle_alert_trigger(self, data: dict):
        """Handle alert trigger from Redis pub/sub"""
        await self.broadcast_to_alert_subscribers({
            "type": "alert_trigger",
            **data
        })

    async def _handle_market_status(self, data: dict):
        """Handle market status change from Redis pub/sub"""
        await self.broadcast_to_market_status_subscribers({
            "type": "market_status",
            **data
        })

    async def publish_price_update(self, ticker: str, price_data: dict):
        """Publish a price update to Redis (for multi-server scaling)"""
        if not self.redis_client:
            # No Redis, broadcast directly
            await self.broadcast_to_ticker_subscribers(ticker, {
                "type": "price_update",
                "ticker": ticker,
                **price_data,
                "timestamp": datetime.utcnow().isoformat()
            })
            return

        try:
            message = {
                "ticker": ticker,
                **price_data,
                "timestamp": datetime.utcnow().isoformat()
            }
            await self.redis_client.publish("price_updates", json.dumps(message))
        except Exception as e:
            logger.error(f"Failed to publish price update to Redis: {e}")
            # Fallback to direct broadcast
            await self.broadcast_to_ticker_subscribers(ticker, {
                "type": "price_update",
                "ticker": ticker,
                **price_data,
                "timestamp": datetime.utcnow().isoformat()
            })

    async def publish_pattern_alert(self, pattern_data: dict):
        """Publish a pattern alert to Redis"""
        if not self.redis_client:
            await self.broadcast_to_pattern_subscribers({
                "type": "pattern_alert",
                **pattern_data,
                "timestamp": datetime.utcnow().isoformat()
            })
            return

        try:
            message = {
                **pattern_data,
                "timestamp": datetime.utcnow().isoformat()
            }
            await self.redis_client.publish("pattern_alerts", json.dumps(message))
        except Exception as e:
            logger.error(f"Failed to publish pattern alert to Redis: {e}")
            await self.broadcast_to_pattern_subscribers({
                "type": "pattern_alert",
                **pattern_data,
                "timestamp": datetime.utcnow().isoformat()
            })

    async def publish_alert_trigger(self, alert_data: dict):
        """Publish an alert trigger to Redis"""
        if not self.redis_client:
            await self.broadcast_to_alert_subscribers({
                "type": "alert_trigger",
                **alert_data,
                "timestamp": datetime.utcnow().isoformat()
            })
            return

        try:
            message = {
                **alert_data,
                "timestamp": datetime.utcnow().isoformat()
            }
            await self.redis_client.publish("alert_triggers", json.dumps(message))
        except Exception as e:
            logger.error(f"Failed to publish alert trigger to Redis: {e}")
            await self.broadcast_to_alert_subscribers({
                "type": "alert_trigger",
                **alert_data,
                "timestamp": datetime.utcnow().isoformat()
            })

    async def publish_market_status(self, status_data: dict):
        """Publish market status change to Redis"""
        if not self.redis_client:
            await self.broadcast_to_market_status_subscribers({
                "type": "market_status",
                **status_data,
                "timestamp": datetime.utcnow().isoformat()
            })
            return

        try:
            message = {
                **status_data,
                "timestamp": datetime.utcnow().isoformat()
            }
            await self.redis_client.publish("market_status", json.dumps(message))
        except Exception as e:
            logger.error(f"Failed to publish market status to Redis: {e}")
            await self.broadcast_to_market_status_subscribers({
                "type": "market_status",
                **status_data,
                "timestamp": datetime.utcnow().isoformat()
            })

    async def heartbeat(self, connection_id: str):
        """Update heartbeat timestamp for a connection"""
        self.last_heartbeat[connection_id] = time.time()

        await self.send_personal_message(connection_id, {
            "type": "pong",
            "timestamp": datetime.utcnow().isoformat()
        })

    async def check_stale_connections(self):
        """Check for stale connections (no heartbeat for 60 seconds)"""
        now = time.time()
        stale_threshold = 60  # 60 seconds

        stale_connections = [
            conn_id for conn_id, last_hb in self.last_heartbeat.items()
            if now - last_hb > stale_threshold
        ]

        for conn_id in stale_connections:
            logger.warning(f"Removing stale connection: {conn_id}")
            self.disconnect(conn_id)

    def get_stats(self) -> dict:
        """Get connection manager statistics"""
        return {
            "active_connections": len(self.active_connections),
            "ticker_subscriptions": {
                ticker: len(subs) for ticker, subs in self.ticker_subscriptions.items()
            },
            "pattern_subscribers": len(self.pattern_subscriptions),
            "alert_subscribers": len(self.alert_subscriptions),
            "market_status_subscribers": len(self.market_status_subscriptions),
            "total_connections": self.stats["total_connections"],
            "messages_sent": self.stats["messages_sent"],
            "messages_received": self.stats["messages_received"],
            "errors": self.stats["errors"],
            "uptime": (datetime.utcnow() - self.stats["last_reset"]).total_seconds()
        }

    async def cleanup(self):
        """Cleanup resources on shutdown"""
        if self.pubsub:
            await self.pubsub.unsubscribe()
            await self.pubsub.close()

        if self.redis_client:
            await self.redis_client.close()

        logger.info("WebSocket manager cleaned up")


# Global connection manager instance
manager: Optional[ConnectionManager] = None


def get_manager() -> ConnectionManager:
    """Get the global connection manager instance"""
    global manager
    if manager is None:
        from app.config import get_settings
        settings = get_settings()
        manager = ConnectionManager(redis_url=settings.REDIS_URL)
    return manager
