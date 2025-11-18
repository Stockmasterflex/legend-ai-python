"""
GraphQL Subscription Resolvers
Real-time updates via WebSocket
"""

import strawberry
import asyncio
from typing import AsyncGenerator
from datetime import datetime
import json

from .types import (
    PatternDetectedEvent,
    PriceAlertEvent,
    ScanProgressEvent
)
from .context import GraphQLContext


@strawberry.type
class Subscription:
    """Root Subscription type"""

    @strawberry.subscription(description="Subscribe to pattern detection events")
    async def pattern_detected(
        self,
        tickers: list[str] = [],
        min_score: float = 7.0,
        info: strawberry.Info[GraphQLContext] = None
    ) -> AsyncGenerator[PatternDetectedEvent, None]:
        """
        Real-time pattern detection events
        Subscribe to get notified when new patterns are detected
        """
        context = info.context if info else None

        # Subscribe to Redis pub/sub channel
        if context and context.cache:
            pubsub = context.cache.pubsub()
            await pubsub.subscribe("pattern_detected")

            try:
                async for message in pubsub.listen():
                    if message["type"] == "message":
                        try:
                            data = json.loads(message["data"])

                            # Filter by tickers if specified
                            if tickers and data["ticker"] not in tickers:
                                continue

                            # Filter by min score
                            if data["score"] < min_score:
                                continue

                            yield PatternDetectedEvent(
                                ticker=data["ticker"],
                                pattern=data["pattern"],
                                score=data["score"],
                                entry=data["entry"],
                                timestamp=datetime.fromisoformat(data["timestamp"])
                            )
                        except (json.JSONDecodeError, KeyError) as e:
                            print(f"Error parsing pattern event: {e}")
                            continue

            finally:
                await pubsub.unsubscribe("pattern_detected")
                await pubsub.close()
        else:
            # Fallback to demo events if no Redis
            for i in range(5):
                await asyncio.sleep(2)
                yield PatternDetectedEvent(
                    ticker="DEMO",
                    pattern="VCP",
                    score=8.5,
                    entry=100.0,
                    timestamp=datetime.utcnow()
                )

    @strawberry.subscription(description="Subscribe to price alerts")
    async def price_alerts(
        self,
        user_id: str = "default",
        info: strawberry.Info[GraphQLContext] = None
    ) -> AsyncGenerator[PriceAlertEvent, None]:
        """
        Real-time price alert notifications
        Subscribe to get notified when price alerts trigger
        """
        context = info.context if info else None

        if context and context.cache:
            pubsub = context.cache.pubsub()
            channel = f"price_alerts:{user_id}"
            await pubsub.subscribe(channel)

            try:
                async for message in pubsub.listen():
                    if message["type"] == "message":
                        try:
                            data = json.loads(message["data"])

                            yield PriceAlertEvent(
                                ticker=data["ticker"],
                                price=data["price"],
                                alert_type=data["alert_type"],
                                message=data["message"],
                                timestamp=datetime.fromisoformat(data["timestamp"])
                            )
                        except (json.JSONDecodeError, KeyError) as e:
                            print(f"Error parsing alert event: {e}")
                            continue

            finally:
                await pubsub.unsubscribe(channel)
                await pubsub.close()
        else:
            # Demo fallback
            await asyncio.sleep(5)
            yield PriceAlertEvent(
                ticker="DEMO",
                price=105.50,
                alert_type="breakout",
                message="Price broke above resistance at 105.00",
                timestamp=datetime.utcnow()
            )

    @strawberry.subscription(description="Subscribe to scan progress updates")
    async def scan_progress(
        self,
        scan_id: int,
        info: strawberry.Info[GraphQLContext] = None
    ) -> AsyncGenerator[ScanProgressEvent, None]:
        """
        Real-time universe scan progress
        Subscribe to get progress updates during universe scanning
        """
        context = info.context if info else None

        if context and context.cache:
            pubsub = context.cache.pubsub()
            channel = f"scan_progress:{scan_id}"
            await pubsub.subscribe(channel)

            try:
                async for message in pubsub.listen():
                    if message["type"] == "message":
                        try:
                            data = json.loads(message["data"])

                            yield ScanProgressEvent(
                                scan_id=scan_id,
                                progress=data["progress"],
                                tickers_scanned=data["tickers_scanned"],
                                patterns_found=data["patterns_found"],
                                current_ticker=data.get("current_ticker")
                            )

                            # Stop if scan is complete
                            if data["progress"] >= 1.0:
                                break

                        except (json.JSONDecodeError, KeyError) as e:
                            print(f"Error parsing scan progress: {e}")
                            continue

            finally:
                await pubsub.unsubscribe(channel)
                await pubsub.close()
        else:
            # Demo progress updates
            total_steps = 10
            for i in range(total_steps + 1):
                await asyncio.sleep(1)
                yield ScanProgressEvent(
                    scan_id=scan_id,
                    progress=i / total_steps,
                    tickers_scanned=i * 50,
                    patterns_found=i * 5,
                    current_ticker=f"DEMO{i}" if i < total_steps else None
                )

    @strawberry.subscription(description="Subscribe to watchlist updates")
    async def watchlist_updates(
        self,
        user_id: str = "default",
        info: strawberry.Info[GraphQLContext] = None
    ) -> AsyncGenerator[str, None]:
        """
        Real-time watchlist changes
        Get notified when items are added/removed/updated
        """
        context = info.context if info else None

        if context and context.cache:
            pubsub = context.cache.pubsub()
            channel = f"watchlist:{user_id}"
            await pubsub.subscribe(channel)

            try:
                async for message in pubsub.listen():
                    if message["type"] == "message":
                        # Message contains JSON with update details
                        yield message["data"].decode() if isinstance(message["data"], bytes) else message["data"]

            finally:
                await pubsub.unsubscribe(channel)
                await pubsub.close()
        else:
            # Demo
            await asyncio.sleep(5)
            yield json.dumps({
                "action": "added",
                "ticker": "DEMO",
                "timestamp": datetime.utcnow().isoformat()
            })

    @strawberry.subscription(description="Subscribe to market updates")
    async def market_updates(
        self,
        info: strawberry.Info[GraphQLContext] = None
    ) -> AsyncGenerator[str, None]:
        """
        Real-time market breadth and internals
        Updates every minute during market hours
        """
        context = info.context if info else None

        if context and context.cache:
            pubsub = context.cache.pubsub()
            await pubsub.subscribe("market_updates")

            try:
                async for message in pubsub.listen():
                    if message["type"] == "message":
                        yield message["data"].decode() if isinstance(message["data"], bytes) else message["data"]

            finally:
                await pubsub.unsubscribe("market_updates")
                await pubsub.close()
        else:
            # Demo updates
            while True:
                await asyncio.sleep(10)
                yield json.dumps({
                    "timestamp": datetime.utcnow().isoformat(),
                    "advancing": 300,
                    "declining": 200,
                    "new_highs": 50,
                    "new_lows": 20,
                    "breadth": "positive"
                })


# Helper function to publish events (to be called from other parts of the app)
async def publish_pattern_detected(cache, ticker: str, pattern: str, score: float, entry: float):
    """Publish a pattern detection event to subscribers"""
    try:
        await cache.publish(
            "pattern_detected",
            json.dumps({
                "ticker": ticker,
                "pattern": pattern,
                "score": score,
                "entry": entry,
                "timestamp": datetime.utcnow().isoformat()
            })
        )
    except Exception as e:
        print(f"Error publishing pattern event: {e}")


async def publish_price_alert(cache, user_id: str, ticker: str, price: float, alert_type: str, message: str):
    """Publish a price alert event to subscribers"""
    try:
        await cache.publish(
            f"price_alerts:{user_id}",
            json.dumps({
                "ticker": ticker,
                "price": price,
                "alert_type": alert_type,
                "message": message,
                "timestamp": datetime.utcnow().isoformat()
            })
        )
    except Exception as e:
        print(f"Error publishing alert event: {e}")


async def publish_scan_progress(cache, scan_id: int, progress: float, tickers_scanned: int, patterns_found: int, current_ticker: str = None):
    """Publish scan progress update to subscribers"""
    try:
        await cache.publish(
            f"scan_progress:{scan_id}",
            json.dumps({
                "progress": progress,
                "tickers_scanned": tickers_scanned,
                "patterns_found": patterns_found,
                "current_ticker": current_ticker
            })
        )
    except Exception as e:
        print(f"Error publishing scan progress: {e}")
