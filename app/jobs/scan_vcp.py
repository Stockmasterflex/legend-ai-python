#!/usr/bin/env python3
"""
VCP Pattern Scanner Job
Runs daily at 6:00 PM EST to scan for Volatility Contraction Patterns

Usage:
    python -m app.jobs.scan_vcp
"""
import asyncio
import logging
import sys
import os
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


async def main():
    """Main job entry point"""
    logger.info("=" * 60)
    logger.info("🚀 VCP PATTERN SCANNER JOB STARTED")
    logger.info(f"⏰ Time: {datetime.now().isoformat()}")
    logger.info("=" * 60)

    try:
        from app.services.daily_pattern_scanner import get_daily_scanner, PATTERN_VCP
        from app.config import get_settings

        settings = get_settings()
        scanner = get_daily_scanner()

        # Run VCP scan
        result = await scanner.scan_pattern(
            pattern_type=PATTERN_VCP,
            min_score=7.0,
            max_results=20
        )

        # Send Telegram notification if configured
        if settings.telegram_bot_token and settings.telegram_chat_id:
            await scanner.send_telegram_notification(
                pattern_type=PATTERN_VCP,
                scan_result=result,
                telegram_bot_token=settings.telegram_bot_token,
                telegram_chat_id=settings.telegram_chat_id
            )

        # Log summary
        if result.get("success"):
            logger.info("=" * 60)
            logger.info("✅ VCP SCAN COMPLETED SUCCESSFULLY")
            logger.info(f"📊 Scanned: {result.get('scanned', 0)} tickers")
            logger.info(f"🎯 Found: {result.get('found', 0)} setups")
            logger.info(f"🏆 Top results: {len(result.get('top_results', []))}")
            logger.info(f"⏱ Duration: {result.get('duration_seconds', 0)}s")
            logger.info("=" * 60)

            # Print top 5 setups
            top_results = result.get('top_results', [])[:5]
            if top_results:
                logger.info("\n🏆 TOP 5 VCP SETUPS:")
                for i, setup in enumerate(top_results, 1):
                    logger.info(
                        f"  {i}. {setup['ticker']}: {setup['score']}/10 "
                        f"@ ${setup.get('entry', 0):.2f} "
                        f"(target: ${setup.get('target', 0):.2f})"
                    )
                logger.info("")

            return 0
        else:
            logger.error(f"❌ VCP scan failed: {result.get('error', 'Unknown error')}")
            return 1

    except Exception as e:
        logger.exception(f"💥 VCP scan job failed with exception: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
