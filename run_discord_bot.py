#!/usr/bin/env python3
"""
Standalone Discord bot runner.
"""
import asyncio
import logging
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.discord_bot import start_bot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('discord_bot.log')
    ]
)

logger = logging.getLogger(__name__)


async def main():
    """Main entry point."""
    logger.info("🤖 Starting Discord Stock Bot...")

    try:
        await start_bot()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
