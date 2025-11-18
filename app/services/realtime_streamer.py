"""
Real-Time Data Streaming Service

Background service that fetches live data and pushes to WebSocket subscribers.
"""
import asyncio
import logging
from datetime import datetime, time as dt_time
from typing import List, Set, Optional
from sqlalchemy.orm import Session

from app.services.websocket_manager import get_manager
from app.services.market_data import MarketDataService
from app.services.database import get_db, DatabaseService
from app.models import Watchlist, PatternScan, AlertLog

logger = logging.getLogger(__name__)


class RealtimeStreamer:
    """
    Background service for streaming real-time data to WebSocket clients.

    Responsibilities:
    - Fetch live price updates for all subscribed tickers
    - Monitor for pattern detections
    - Trigger alerts when conditions are met
    - Track market status (open/closed)
    """

    def __init__(
        self,
        update_interval: int = 5,  # Update every 5 seconds during market hours
        after_hours_interval: int = 60  # Update every 60 seconds after hours
    ):
        self.update_interval = update_interval
        self.after_hours_interval = after_hours_interval
        self.market_data_service = MarketDataService()
        self.running = False
        self.tasks: List[asyncio.Task] = []

    async def start(self):
        """Start the real-time streaming service"""
        if self.running:
            logger.warning("Streamer already running")
            return

        self.running = True
        logger.info("Starting real-time streamer...")

        # Initialize WebSocket manager Redis connection
        manager = get_manager()
        await manager.initialize_redis()

        # Start background tasks
        self.tasks = [
            asyncio.create_task(self._price_update_loop()),
            asyncio.create_task(self._alert_check_loop()),
            asyncio.create_task(self._market_status_loop()),
            asyncio.create_task(self._stale_connection_cleanup_loop())
        ]

        logger.info("Real-time streamer started")

    async def stop(self):
        """Stop the real-time streaming service"""
        if not self.running:
            return

        self.running = False
        logger.info("Stopping real-time streamer...")

        # Cancel all background tasks
        for task in self.tasks:
            task.cancel()

        await asyncio.gather(*self.tasks, return_exceptions=True)

        # Cleanup WebSocket manager
        manager = get_manager()
        await manager.cleanup()

        logger.info("Real-time streamer stopped")

    def _is_market_hours(self) -> bool:
        """Check if current time is during market hours (9:30 AM - 4:00 PM ET)"""
        now = datetime.utcnow()
        # Convert to ET (approximate - doesn't handle DST perfectly)
        et_hour = (now.hour - 5) % 24

        # Market hours: 9:30 AM - 4:00 PM ET (14:30 - 21:00 UTC)
        market_open = dt_time(14, 30)  # 9:30 AM ET
        market_close = dt_time(21, 0)  # 4:00 PM ET

        current_time = dt_time(now.hour, now.minute)

        # Check if weekday (0 = Monday, 6 = Sunday)
        is_weekday = now.weekday() < 5

        return is_weekday and market_open <= current_time < market_close

    async def _price_update_loop(self):
        """Background loop to fetch and broadcast price updates"""
        logger.info("Price update loop started")

        while self.running:
            try:
                manager = get_manager()

                # Get all tickers that have active subscribers
                subscribed_tickers = list(manager.ticker_subscriptions.keys())

                if not subscribed_tickers:
                    # No subscribers, wait and continue
                    await asyncio.sleep(self.update_interval)
                    continue

                # Determine update interval based on market hours
                is_market_open = self._is_market_hours()
                interval = self.update_interval if is_market_open else self.after_hours_interval

                # Fetch price data for all subscribed tickers (in batches to avoid rate limits)
                batch_size = 10
                for i in range(0, len(subscribed_tickers), batch_size):
                    batch = subscribed_tickers[i:i + batch_size]

                    # Fetch prices concurrently for this batch
                    tasks = [
                        self._fetch_and_broadcast_price(ticker)
                        for ticker in batch
                    ]

                    await asyncio.gather(*tasks, return_exceptions=True)

                    # Small delay between batches to avoid rate limiting
                    if i + batch_size < len(subscribed_tickers):
                        await asyncio.sleep(0.5)

                # Wait for next update cycle
                await asyncio.sleep(interval)

            except Exception as e:
                logger.error(f"Error in price update loop: {e}")
                await asyncio.sleep(5)  # Wait before retrying

    async def _fetch_and_broadcast_price(self, ticker: str):
        """Fetch current price and broadcast to subscribers"""
        try:
            # Fetch latest quote
            quote = await asyncio.to_thread(
                self.market_data_service.get_quote,
                ticker
            )

            if not quote:
                logger.warning(f"No quote data for {ticker}")
                return

            # Extract price data
            price_data = {
                "price": quote.get("price", 0),
                "change": quote.get("change", 0),
                "change_percent": quote.get("change_percent", 0),
                "volume": quote.get("volume", 0),
                "high": quote.get("high", 0),
                "low": quote.get("low", 0),
                "open": quote.get("open", 0)
            }

            # Broadcast to subscribers
            manager = get_manager()
            await manager.publish_price_update(ticker, price_data)

        except Exception as e:
            logger.error(f"Error fetching price for {ticker}: {e}")

    async def _alert_check_loop(self):
        """Background loop to check for alert triggers"""
        logger.info("Alert check loop started")

        while self.running:
            try:
                # Get all active watchlist items with alerts enabled
                db: Session = next(get_db())
                db_service = DatabaseService()

                watchlist_items = db.query(Watchlist).filter(
                    Watchlist.alerts_enabled == True,
                    Watchlist.status.in_(["Watching", "Breaking Out"])
                ).all()

                # Check each item for alert conditions
                for item in watchlist_items:
                    await self._check_watchlist_alert(item)

                db.close()

                # Check every 10 seconds
                await asyncio.sleep(10)

            except Exception as e:
                logger.error(f"Error in alert check loop: {e}")
                await asyncio.sleep(10)

    async def _check_watchlist_alert(self, watchlist_item: Watchlist):
        """Check if a watchlist item should trigger an alert"""
        try:
            ticker = watchlist_item.ticker.symbol

            # Fetch current price
            quote = await asyncio.to_thread(
                self.market_data_service.get_quote,
                ticker
            )

            if not quote:
                return

            current_price = quote.get("price", 0)

            # Check if price crossed target entry
            if watchlist_item.target_entry and current_price >= watchlist_item.target_entry:
                # Check threshold
                threshold = watchlist_item.alert_threshold or 0.5
                price_diff_percent = abs(
                    (current_price - watchlist_item.target_entry) / watchlist_item.target_entry * 100
                )

                if price_diff_percent <= threshold:
                    # Trigger alert
                    manager = get_manager()
                    await manager.publish_alert_trigger({
                        "ticker": ticker,
                        "alert_type": "breakout",
                        "trigger_price": watchlist_item.target_entry,
                        "current_price": current_price,
                        "message": f"{ticker} breaking out at ${current_price:.2f} (target: ${watchlist_item.target_entry:.2f})"
                    })

                    # Log alert
                    db: Session = next(get_db())
                    alert_log = AlertLog(
                        ticker_id=watchlist_item.ticker_id,
                        alert_type="breakout",
                        trigger_price=watchlist_item.target_entry,
                        trigger_value=current_price,
                        sent_via="websocket",
                        user_id=watchlist_item.user_id,
                        status="sent"
                    )
                    db.add(alert_log)
                    db.commit()
                    db.close()

        except Exception as e:
            logger.error(f"Error checking alert for watchlist item {watchlist_item.id}: {e}")

    async def _market_status_loop(self):
        """Background loop to monitor and broadcast market status changes"""
        logger.info("Market status loop started")

        current_status = None

        while self.running:
            try:
                is_open = self._is_market_hours()
                new_status = "open" if is_open else "closed"

                # Broadcast status change
                if new_status != current_status:
                    manager = get_manager()

                    # Calculate next open/close times (simplified)
                    now = datetime.utcnow()

                    if new_status == "open":
                        # Market just opened
                        next_close = now.replace(hour=21, minute=0, second=0)
                        next_open = None

                        await manager.publish_market_status({
                            "status": "open",
                            "next_close": next_close.isoformat(),
                            "next_open": None
                        })

                    else:
                        # Market closed
                        # Next open is tomorrow at 14:30 UTC (9:30 AM ET)
                        next_open = now.replace(hour=14, minute=30, second=0)
                        if now.hour >= 21:
                            # If after close time, next open is tomorrow
                            from datetime import timedelta
                            next_open = next_open + timedelta(days=1)

                        await manager.publish_market_status({
                            "status": "closed",
                            "next_open": next_open.isoformat(),
                            "next_close": None
                        })

                    current_status = new_status
                    logger.info(f"Market status changed to: {new_status}")

                # Check every 60 seconds
                await asyncio.sleep(60)

            except Exception as e:
                logger.error(f"Error in market status loop: {e}")
                await asyncio.sleep(60)

    async def _stale_connection_cleanup_loop(self):
        """Background loop to clean up stale connections"""
        logger.info("Stale connection cleanup loop started")

        while self.running:
            try:
                manager = get_manager()
                await manager.check_stale_connections()

                # Check every 30 seconds
                await asyncio.sleep(30)

            except Exception as e:
                logger.error(f"Error in stale connection cleanup: {e}")
                await asyncio.sleep(30)


# Global streamer instance
_streamer: Optional[RealtimeStreamer] = None


def get_streamer() -> RealtimeStreamer:
    """Get the global streamer instance"""
    global _streamer
    if _streamer is None:
        _streamer = RealtimeStreamer()
    return _streamer
