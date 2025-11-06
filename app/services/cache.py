from redis.asyncio import Redis
from typing import Optional, Any, Dict
import json
import logging

from app.config import get_settings

logger = logging.getLogger(__name__)


class CacheService:
    """
    Redis caching service matching n8n Cache_Manager functionality

    Cache Strategy (matching n8n):
    - Pattern results: 1 hour TTL (during market hours)
    - Price data: 15 min TTL (ohlcv:{ticker}:1d:5y)
    - Universe data: 24 hour TTL
    - Chart URLs: 15 min TTL
    """

    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis: Optional[Redis] = None

    async def _get_redis(self) -> Redis:
        """Lazy initialization of Redis connection"""
        if self.redis is None:
            self.redis = Redis.from_url(self.redis_url, decode_responses=True)
        return self.redis

    def _generate_cache_key(self, prefix: str, **kwargs) -> str:
        """
        Generate consistent cache key from parameters

        Matches n8n format: ohlcv:{ticker}:1d:5y
        """
        # Sort kwargs for consistent keys
        sorted_items = sorted(kwargs.items())
        key_parts = [f"{k}={v}" for k, v in sorted_items]
        return f"{prefix}:{':'.join(key_parts)}"

    async def get_pattern(
        self,
        ticker: str,
        interval: str = "1day"
    ) -> Optional[Dict[str, Any]]:
        """
        Get cached pattern result

        Key format: pattern:ticker={ticker}:interval={interval}
        """
        redis = await self._get_redis()
        key = self._generate_cache_key("pattern", ticker=ticker, interval=interval)

        try:
            data = await redis.get(key)
            if data:
                logger.debug(f"Cache hit for pattern: {key}")
                return json.loads(data)
            else:
                logger.debug(f"Cache miss for pattern: {key}")
                return None
        except Exception as e:
            logger.error(f"Cache get error for {key}: {e}")
            return None

    async def set_pattern(
        self,
        ticker: str,
        interval: str,
        data: Dict[str, Any],
        ttl: int = 3600  # 1 hour default (matching n8n)
    ) -> bool:
        """
        Cache pattern result

        Key format: pattern:ticker={ticker}:interval={interval}
        """
        redis = await self._get_redis()
        key = self._generate_cache_key("pattern", ticker=ticker, interval=interval)

        try:
            json_data = json.dumps(data)
            await redis.setex(key, ttl, json_data)
            logger.debug(f"Cached pattern result: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Cache set error for {key}: {e}")
            return False

    async def get_price_data(self, ticker: str, interval: str = "1day") -> Optional[Dict[str, Any]]:
        """
        Get cached price data

        Key format: ohlcv:{ticker}:{interval}:5y (matching n8n)
        """
        redis = await self._get_redis()
        # Match n8n key format exactly: ohlcv:{ticker}:1d:5y
        key = f"ohlcv:{ticker}:1d:5y"

        try:
            data = await redis.get(key)
            if data:
                logger.debug(f"Cache hit for price data: {key}")
                return json.loads(data)
            else:
                logger.debug(f"Cache miss for price data: {key}")
                return None
        except Exception as e:
            logger.error(f"Cache get error for {key}: {e}")
            return None

    async def set_price_data(
        self,
        ticker: str,
        data: Dict[str, Any],
        ttl: int = 900  # 15 minutes (matching n8n)
    ) -> bool:
        """
        Cache price data

        Key format: ohlcv:{ticker}:1d:5y (matching n8n exactly)
        """
        redis = await self._get_redis()
        key = f"ohlcv:{ticker}:1d:5y"

        try:
            json_data = json.dumps(data)
            await redis.setex(key, ttl, json_data)
            logger.debug(f"Cached price data: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Cache set error for {key}: {e}")
            return False

    async def get_chart(self, ticker: str, interval: str = "1D") -> Optional[str]:
        """
        Get cached chart URL

        Key format: chart:ticker={ticker}:interval={interval}
        """
        redis = await self._get_redis()
        key = self._generate_cache_key("chart", ticker=ticker, interval=interval)

        try:
            url = await redis.get(key)
            if url:
                logger.debug(f"Cache hit for chart: {key}")
                return url
            return None
        except Exception as e:
            logger.error(f"Cache get error for {key}: {e}")
            return None

    async def set_chart(
        self,
        ticker: str,
        interval: str,
        url: str,
        ttl: int = 900  # 15 minutes
    ) -> bool:
        """
        Cache chart URL

        Key format: chart:ticker={ticker}:interval={interval}
        """
        redis = await self._get_redis()
        key = self._generate_cache_key("chart", ticker=ticker, interval=interval)

        try:
            await redis.setex(key, ttl, url)
            logger.debug(f"Cached chart URL: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.error(f"Cache set error for {key}: {e}")
            return False

    async def invalidate_pattern(self, ticker: str, interval: str = "*") -> int:
        """
        Manually invalidate cached pattern (all intervals)

        Returns number of keys deleted
        """
        redis = await self._get_redis()

        try:
            if interval == "*":
                # Delete all intervals for this ticker
                pattern = f"pattern:ticker={ticker}:interval=*"
                keys = await redis.keys(pattern)
            else:
                # Delete specific interval
                key = self._generate_cache_key("pattern", ticker=ticker, interval=interval)
                keys = [key]

            if keys:
                deleted = await redis.delete(*keys)
                logger.info(f"Invalidated {deleted} pattern cache keys for {ticker}")
                return deleted
            return 0
        except Exception as e:
            logger.error(f"Cache invalidation error for {ticker}: {e}")
            return 0

    async def invalidate_price_data(self, ticker: str) -> int:
        """
        Invalidate cached price data for ticker
        """
        redis = await self._get_redis()

        try:
            key = f"ohlcv:{ticker}:1d:5y"
            deleted = await redis.delete(key)
            logger.info(f"Invalidated price data cache for {ticker}")
            return deleted
        except Exception as e:
            logger.error(f"Price data invalidation error for {ticker}: {e}")
            return 0

    async def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics

        Returns Redis INFO stats plus custom metrics
        """
        redis = await self._get_redis()

        try:
            info = await redis.info("stats")

            # Count our keys
            pattern_keys = len(await redis.keys("pattern:*"))
            price_keys = len(await redis.keys("ohlcv:*"))
            chart_keys = len(await redis.keys("chart:*"))
            total_keys = pattern_keys + price_keys + chart_keys

            return {
                "redis_hits": info.get("keyspace_hits", 0),
                "redis_misses": info.get("keyspace_misses", 0),
                "redis_hit_rate": (info.get("keyspace_hits", 0) /
                                 max(1, info.get("keyspace_hits", 0) + info.get("keyspace_misses", 0)) * 100),
                "total_keys": total_keys,
                "pattern_keys": pattern_keys,
                "price_keys": price_keys,
                "chart_keys": chart_keys,
                "memory_used": info.get("used_memory_human", "unknown")
            }
        except Exception as e:
            logger.error(f"Cache stats error: {e}")
            return {"error": str(e)}

    async def clear_all_cache(self) -> Dict[str, int]:
        """
        Clear all cache data (dangerous - use carefully)

        Returns counts of deleted keys by type
        """
        redis = await self._get_redis()

        try:
            pattern_keys = await redis.delete(*await redis.keys("pattern:*"))
            price_keys = await redis.delete(*await redis.keys("ohlcv:*"))
            chart_keys = await redis.delete(*await redis.keys("chart:*"))

            logger.warning(f"Cleared all cache: {pattern_keys} patterns, {price_keys} price data, {chart_keys} charts")

            return {
                "pattern_keys_deleted": pattern_keys,
                "price_keys_deleted": price_keys,
                "chart_keys_deleted": chart_keys,
                "total_deleted": pattern_keys + price_keys + chart_keys
            }
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return {"error": str(e)}

    async def health_check(self) -> Dict[str, Any]:
        """
        Check Redis connection health
        """
        try:
            redis = await self._get_redis()
            await redis.ping()

            stats = await self.get_cache_stats()

            return {
                "status": "healthy",
                "connection": "connected",
                "stats": stats
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "connection": "disconnected",
                "error": str(e)
            }

    async def close(self):
        """Close Redis connection"""
        if self.redis:
            await self.redis.close()
            self.redis = None


# Global cache instance
def get_cache_service() -> CacheService:
    """Get global cache service instance"""
    settings = get_settings()
    return CacheService(settings.redis_url)
