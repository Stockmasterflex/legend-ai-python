#!/usr/bin/env python3
"""
Auto-Validation Task
Automatically validates pattern outcomes by checking historical data
Run this daily via cron or scheduled task
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from app.services.pattern_validation import PatternValidationService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Main task to auto-validate patterns"""
    logger.info("Starting auto-validation task...")

    try:
        validation_service = PatternValidationService()

        # Validate patterns from last 30 days
        validated_count = await validation_service.auto_validate_patterns(lookback_days=30)

        logger.info(f"✅ Validated {validated_count} patterns")

        # Get summary
        summary = await validation_service.get_validation_summary()
        logger.info(f"Summary: {summary}")

        # Check for poor performers
        to_disable = await validation_service.get_patterns_to_disable()

        if to_disable:
            logger.warning(f"⚠️  Patterns with poor performance: {to_disable}")

        return 0

    except Exception as e:
        logger.error(f"❌ Auto-validation failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
