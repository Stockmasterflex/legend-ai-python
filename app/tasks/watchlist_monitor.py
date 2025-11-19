#!/usr/bin/env python3
"""
Watchlist Monitoring Background Task
Continuously monitors watchlist and sends alerts
Run this as a background service
"""

import asyncio
import sys
import os
import signal

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from app.services.watchlist_alerts import WatchlistAlertsService
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global service instance
alerts_service = None


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info("Received shutdown signal, stopping monitoring...")
    if alerts_service:
        alerts_service.stop_monitoring()
    sys.exit(0)


async def main():
    """Main monitoring loop"""
    global alerts_service

    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info("Starting watchlist monitoring service...")

    try:
        alerts_service = WatchlistAlertsService()

        # Get interval from environment (default: 5 minutes)
        interval = int(os.getenv("WATCHLIST_CHECK_INTERVAL_MINUTES", "5"))

        logger.info(f"Monitoring interval: {interval} minutes")

        # Start monitoring (runs forever)
        await alerts_service.start_monitoring(interval_minutes=interval)

    except Exception as e:
        logger.error(f"Fatal error in monitoring service: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("Monitoring service stopped by user")
        sys.exit(0)
