"""
Cache Warming Service
Pre-populates cache on startup with frequently accessed data
"""

import logging
import asyncio
from typing import List, Dict, Any
from datetime import datetime

from app.config import get_settings
from app.services.multi_tier_cache import get_multi_tier_cache
from app.services.market_data import market_data_service
from app.services.universe_store import universe_store

logger = logging.getLogger(__name__)


class CacheWarmer:
    """
    Intelligent cache warming service

    Warms cache on startup with:
    1. Popular tickers (SPY, QQQ, etc.)
    2. Recent universe data
    3. Common patterns
    """

    # Popular tickers to warm on startup
    POPULAR_TICKERS = [
        "SPY",  # S&P 500 ETF
        "QQQ",  # NASDAQ ETF
        "IWM",  # Russell 2000 ETF
        "DIA",  # Dow Jones ETF
        "AAPL",  # Apple
        "MSFT",  # Microsoft
        "GOOGL",  # Google
        "AMZN",  # Amazon
        "TSLA",  # Tesla
        "NVDA",  # NVIDIA
    ]

    def __init__(self):
        self.settings = get_settings()
        self.cache = None
        self.market_data = None

    async def warm_all(self) -> Dict[str, Any]:
        """
        Warm all cache tiers on startup

        Returns:
            Statistics on warmed cache entries
        """
        if not self.settings.cache_enable_warming:
            logger.info("⚠️ Cache warming disabled in settings")
            return {"status": "disabled"}

        logger.info("🔄 Starting cache warming process...")
        start_time = datetime.utcnow()

        self.cache = get_multi_tier_cache()
        self.market_data = market_data_service

        stats = {
            "market_data": 0,
            "universe": 0,
            "indices": 0,
            "failed": 0,
            "duration_seconds": 0
        }

        # Warm market data for popular tickers
        market_stats = await self._warm_market_data()
        stats["market_data"] = market_stats.get("success", 0)
        stats["failed"] += market_stats.get("failed", 0)

        # Warm universe metadata
        universe_stats = await self._warm_universe_metadata()
        stats["universe"] = universe_stats.get("success", 0)
        stats["failed"] += universe_stats.get("failed", 0)

        # Warm index data (SPY for RS calculations)
        index_stats = await self._warm_index_data()
        stats["indices"] = index_stats.get("success", 0)
        stats["failed"] += index_stats.get("failed", 0)

        # Calculate duration
        end_time = datetime.utcnow()
        stats["duration_seconds"] = (end_time - start_time).total_seconds()

        logger.info(f"✅ Cache warming complete: {stats}")
        return stats

    async def _warm_market_data(self) -> Dict[str, int]:
        """Warm cache with market data for popular tickers"""
        logger.info(f"📊 Warming market data for {len(self.POPULAR_TICKERS)} popular tickers...")

        stats = {"success": 0, "failed": 0}

        for ticker in self.POPULAR_TICKERS:
            try:
                # Fetch and cache OHLCV data
                data = await self.market_data.get_ohlcv(ticker, interval="1day", outputsize=100)

                if data:
                    # Cache in both hot and warm tiers
                    cache_key = f"ohlcv:{ticker}:1d:5y"

                    # Hot tier (Redis) - 15 min
                    await self.cache.set(
                        cache_key,
                        data,
                        data_type="price",
                        tier=None  # Auto-determine
                    )

                    stats["success"] += 1
                    logger.debug(f"✅ Warmed market data for {ticker}")
                else:
                    stats["failed"] += 1
                    logger.warning(f"⚠️ No data returned for {ticker}")

                # Small delay to avoid rate limiting
                await asyncio.sleep(0.1)

            except Exception as e:
                logger.error(f"❌ Failed to warm market data for {ticker}: {e}")
                stats["failed"] += 1

        logger.info(f"📊 Market data warming complete: {stats}")
        return stats

    async def _warm_universe_metadata(self) -> Dict[str, int]:
        """Warm cache with universe metadata"""
        logger.info("🌐 Warming universe metadata...")

        stats = {"success": 0, "failed": 0}

        try:
            # Get universe data
            universe_data = universe_store._memory

            if universe_data:
                # Cache universe list
                cache_key = "universe:all"
                tickers_list = list(universe_data.keys())

                await self.cache.set(
                    cache_key,
                    tickers_list,
                    data_type="generic",
                    tier=None
                )

                stats["success"] += 1

                # Cache sector/industry groupings
                sectors = {}
                industries = {}

                for ticker, info in universe_data.items():
                    sector = info.get("sector", "Unknown")
                    industry = info.get("industry", "Unknown")

                    if sector not in sectors:
                        sectors[sector] = []
                    sectors[sector].append(ticker)

                    if industry not in industries:
                        industries[industry] = []
                    industries[industry].append(ticker)

                # Cache sector data
                await self.cache.set(
                    "universe:sectors",
                    sectors,
                    data_type="generic",
                    tier=None
                )

                # Cache industry data
                await self.cache.set(
                    "universe:industries",
                    industries,
                    data_type="generic",
                    tier=None
                )

                stats["success"] += 2

                logger.info(f"✅ Warmed universe metadata: {len(tickers_list)} tickers, {len(sectors)} sectors, {len(industries)} industries")

            else:
                logger.warning("⚠️ Universe data not available for warming")
                stats["failed"] += 1

        except Exception as e:
            logger.error(f"❌ Failed to warm universe metadata: {e}")
            stats["failed"] += 1

        return stats

    async def _warm_index_data(self) -> Dict[str, int]:
        """Warm cache with index data for RS calculations"""
        logger.info("📈 Warming index data (SPY)...")

        stats = {"success": 0, "failed": 0}

        try:
            # Fetch SPY data for RS calculations
            spy_data = await self.market_data.get_ohlcv("SPY", interval="1day", outputsize=252)

            if spy_data:
                # Cache SPY data with longer TTL (1 day)
                cache_key = "index:spy:daily"

                await self.cache.set(
                    cache_key,
                    spy_data,
                    data_type="price",
                    tier=None
                )

                stats["success"] += 1
                logger.info("✅ Warmed SPY index data")

            else:
                stats["failed"] += 1
                logger.warning("⚠️ Failed to fetch SPY data")

        except Exception as e:
            logger.error(f"❌ Failed to warm index data: {e}")
            stats["failed"] += 1

        return stats

    async def warm_ticker(self, ticker: str) -> bool:
        """
        Warm cache for a specific ticker

        Args:
            ticker: Stock ticker symbol

        Returns:
            True if successful
        """
        try:
            logger.info(f"🔄 Warming cache for {ticker}...")

            # Fetch market data
            data = await self.market_data.get_ohlcv(ticker, interval="1day", outputsize=100)

            if data:
                cache_key = f"ohlcv:{ticker}:1d:5y"
                await self.cache.set(
                    cache_key,
                    data,
                    data_type="price",
                    tier=None
                )

                logger.info(f"✅ Warmed cache for {ticker}")
                return True

            return False

        except Exception as e:
            logger.error(f"❌ Failed to warm cache for {ticker}: {e}")
            return False

    async def warm_tickers(self, tickers: List[str]) -> Dict[str, int]:
        """
        Warm cache for multiple tickers

        Args:
            tickers: List of ticker symbols

        Returns:
            Statistics on warmed tickers
        """
        logger.info(f"🔄 Warming cache for {len(tickers)} tickers...")

        stats = {"success": 0, "failed": 0}

        for ticker in tickers:
            success = await self.warm_ticker(ticker)
            if success:
                stats["success"] += 1
            else:
                stats["failed"] += 1

            # Small delay to avoid rate limiting
            await asyncio.sleep(0.1)

        logger.info(f"✅ Batch warming complete: {stats}")
        return stats


# Global cache warmer instance
_cache_warmer: CacheWarmer = None


def get_cache_warmer() -> CacheWarmer:
    """Get global cache warmer instance"""
    global _cache_warmer
    if _cache_warmer is None:
        _cache_warmer = CacheWarmer()
    return _cache_warmer
