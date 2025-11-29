"""
Background job entry point for scheduled scans.
"""
from app.services.eod_scanner import get_eod_scanner
import logging

logger = logging.getLogger("eod_scan_job")


async def run_scan_job():
    scanner = get_eod_scanner()
    try:
        result = await scanner.run_scan()
        logger.info("EOD scan job completed: %s patterns", result.get("patterns_found"))
    except Exception as exc:
        logger.error("EOD scan job failed: %s", exc)
