"""
APScheduler integration for periodic jobs.
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, time
from typing import Callable
import logging

from app.jobs.scan_universe import run_scan_job
from app.services.universe_ingestor import UniverseIngestor

logger = logging.getLogger("scheduler")

scheduler = AsyncIOScheduler(timezone="America/New_York")

def _ensure_job(id: str, func: Callable, trigger: CronTrigger):
    if scheduler.get_job(id):
        scheduler.remove_job(id)
    scheduler.add_job(func, trigger=trigger, id=id, replace_existing=True)

async def _watchlist_monitor_job():
    """Wrapper for watchlist monitoring job"""
    try:
        from app.jobs.watchlist_monitor import run_watchlist_check
        from app.services.telegram_bot import get_telegram_bot
        
        alerts = await run_watchlist_check()
        
        # Send Telegram alerts
        if alerts:
            bot = get_telegram_bot()
            for alert in alerts:
                await bot.send_alert(alert)
    except Exception as e:
        logger.error(f"Watchlist monitor job failed: {e}")

def start_scheduler():
    if scheduler.running:
        logger.debug("Scheduler already running")
        return

    logger.info("Starting APScheduler for EOD scanning, universe refresh, and watchlist monitoring")
    
    # EOD scan: 4:05 PM ET Mon-Fri
    _ensure_job(
        "eod_scan",
        run_scan_job,
        CronTrigger(day_of_week="mon-fri", hour=16, minute=5),
    )
    
    # Universe refresh: 8:00 PM ET Sunday
    _ensure_job(
        "universe_refresh",
        UniverseIngestor().refresh,
        CronTrigger(day_of_week="sun", hour=20, minute=0),
    )
    
    # Watchlist monitor: Every 5 minutes, 9:30 AM - 4:00 PM ET Mon-Fri
    # Using multiple jobs for each 5-minute interval during market hours
    for hour in range(9, 16):  # 9 AM to 3 PM
        for minute in range(0, 60, 5):
            # Skip 9:00-9:25 (market opens at 9:30)
            if hour == 9 and minute < 30:
                continue
            _ensure_job(
                f"watchlist_monitor_{hour:02d}_{minute:02d}",
                _watchlist_monitor_job,
                CronTrigger(day_of_week="mon-fri", hour=hour, minute=minute),
            )
    
    # Add 4:00 PM check
    _ensure_job(
        "watchlist_monitor_16_00",
        _watchlist_monitor_job,
        CronTrigger(day_of_week="mon-fri", hour=16, minute=0),
    )
    
    scheduler.start()

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
