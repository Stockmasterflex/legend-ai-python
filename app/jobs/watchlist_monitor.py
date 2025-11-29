"""
Watchlist monitoring job - checks prices every 5 minutes during market hours
Triggers alerts when watchlist items change state
"""

import asyncio
import logging
from datetime import datetime, time
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo

from app.services.database import get_database_service

logger = logging.getLogger(__name__)

MARKET_OPEN = time(9, 30)  # 9:30 AM ET
MARKET_CLOSE = time(16, 0)  # 4:00 PM ET
ET_TIMEZONE = ZoneInfo("America/New_York")


class WatchlistMonitor:
    """Monitor watchlist items for price alerts"""

    def __init__(self):
        self.db = get_database_service()
        # Market data service will be imported dynamically when needed
        self.market_data = None

    def _get_market_data(self):
        """Lazy load market data service"""
        if self.market_data is None:
            try:
                from app.services.market_data import MarketDataService

                self.market_data = MarketDataService()
            except ImportError:
                logger.error("MarketDataService not available")
                self.market_data = None
        return self.market_data

    def is_market_hours(self) -> bool:
        """Check if currently within market hours (9:30 AM - 4:00 PM ET, Mon-Fri)"""
        now = datetime.now(ET_TIMEZONE)

        # Check if weekend
        if now.weekday() >= 5:  # Saturday=5, Sunday=6
            return False

        # Check if within trading hours
        current_time = now.time()
        return MARKET_OPEN <= current_time <= MARKET_CLOSE

    async def check_watchlist_item(
        self, item: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Check a single watchlist item for state changes
        Returns alert dict if state changed, None otherwise
        """
        ticker = item.get("ticker")
        status = item.get("status", "Watching")
        entry = item.get("target_entry")
        stop = item.get("target_stop")
        target = item.get("target_price")

        if not ticker:
            return None

        # Skip if already completed/triggered
        if status in ["Completed", "Triggered"]:
            return None

        try:
            # Get current price and volume
            market_data = self._get_market_data()
            if not market_data:
                logger.warning("Market data service not available")
                return None

            quote = await market_data.get_quote(ticker)
            if not quote:
                logger.warning(f"No quote data for {ticker}")
                return None

            current_price = quote.get("price")
            volume = quote.get("volume", 0)
            avg_volume = quote.get("avg_volume", volume)

            if not current_price:
                return None

            # Calculate volume ratio
            volume_ratio = volume / avg_volume if avg_volume > 0 else 1.0

            new_status = status
            alert_type = None

            # Check state transitions
            if status == "Watching" and entry:
                # Breakout detection: price > entry AND volume > 1.5x average
                if current_price > entry and volume_ratio > 1.5:
                    new_status = "Breaking Out"
                    alert_type = "breakout"
                    logger.info(
                        f"🚀 {ticker} breaking out at ${current_price:.2f} (entry: ${entry:.2f}, volume: {volume_ratio:.1f}x)"
                    )

            elif status in ["Watching", "Breaking Out"]:
                # Stop hit
                if stop and current_price < stop:
                    new_status = "Triggered"
                    alert_type = "stop_hit"
                    logger.info(
                        f"🛑 {ticker} stop hit at ${current_price:.2f} (stop: ${stop:.2f})"
                    )

                # Target hit
                elif target and current_price > target:
                    new_status = "Triggered"
                    alert_type = "target_hit"
                    logger.info(
                        f"🎯 {ticker} target hit at ${current_price:.2f} (target: ${target:.2f})"
                    )

            # Update status if changed
            if new_status != status:
                self.db.update_watchlist_symbol(ticker, status=new_status)

                # Return alert
                return {
                    "ticker": ticker,
                    "alert_type": alert_type,
                    "old_status": status,
                    "new_status": new_status,
                    "current_price": current_price,
                    "entry": entry,
                    "stop": stop,
                    "target": target,
                    "volume_ratio": volume_ratio,
                    "timestamp": datetime.now(ET_TIMEZONE).isoformat(),
                }

        except Exception as e:
            logger.error(f"Error checking {ticker}: {e}")
            return None

        return None

    async def run_check(self) -> List[Dict[str, Any]]:
        """
        Run watchlist check for all items
        Returns list of alerts triggered
        """
        if not self.is_market_hours():
            logger.debug("Outside market hours, skipping watchlist check")
            return []

        logger.info("🔍 Starting watchlist monitoring check...")

        try:
            # Get all watchlist items
            items = self.db.get_watchlist_items()

            if not items:
                logger.debug("No watchlist items to monitor")
                return []

            logger.info(f"Monitoring {len(items)} watchlist items")

            # Check each item
            alerts = []
            for item in items:
                alert = await self.check_watchlist_item(item)
                if alert:
                    alerts.append(alert)

                    # Log alert to database
                    try:
                        self.db.log_alert(
                            ticker=alert["ticker"],
                            alert_type=alert["alert_type"],
                            message=f"{alert['ticker']} {alert['alert_type']}: ${alert['current_price']:.2f}",
                            metadata=alert,
                        )
                    except Exception as e:
                        logger.warning(
                            f"Failed to log alert for {alert['ticker']}: {e}"
                        )

                # Small delay to avoid rate limits
                await asyncio.sleep(0.1)

            if alerts:
                logger.info(
                    f"✅ Watchlist check complete: {len(alerts)} alerts triggered"
                )
            else:
                logger.debug("Watchlist check complete: no alerts")

            return alerts

        except Exception as e:
            logger.error(f"Watchlist monitoring failed: {e}")
            return []


# Singleton instance
_monitor = None


def get_watchlist_monitor() -> WatchlistMonitor:
    """Get singleton watchlist monitor instance"""
    global _monitor
    if _monitor is None:
        _monitor = WatchlistMonitor()
    return _monitor


async def run_watchlist_check() -> List[Dict[str, Any]]:
    """
    Entry point for scheduled job
    Runs watchlist check and returns alerts
    """
    monitor = get_watchlist_monitor()
    return await monitor.run_check()
