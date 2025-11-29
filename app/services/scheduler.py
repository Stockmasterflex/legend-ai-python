"""
APScheduler integration for periodic jobs.
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
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

def start_scheduler():
    if scheduler.running:
        logger.debug("Scheduler already running")
        return

    logger.info("Starting APScheduler for EOD scanning and universe refresh")
    _ensure_job(
        "eod_scan",
        run_scan_job,
        CronTrigger(day_of_week="mon-fri", hour=16, minute=5),
    )
    _ensure_job(
        "universe_refresh",
        UniverseIngestor().refresh,
        CronTrigger(day_of_week="sun", hour=20, minute=0),
    )
    scheduler.start()

def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
