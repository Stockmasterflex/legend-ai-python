"""
Script to refresh the S&P 500 and NASDAQ 100 universe.
"""
import asyncio
import logging

from app.services.universe_ingestor import UniverseIngestor

logger = logging.getLogger("universe_ingest")
logging.basicConfig(level=logging.INFO)


async def main():
    ingestor = UniverseIngestor()
    symbols = await ingestor.refresh()
    logger.info("Universe ingest complete: %s symbols", len(symbols))


if __name__ == "__main__":
    asyncio.run(main())
