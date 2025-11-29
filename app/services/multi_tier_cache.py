"""
Multi-Tier Caching Service for Legend AI
Implements intelligent 3-tier caching strategy:
- Tier 1 (Hot): Redis 5-15min TTL for frequently accessed data
- Tier 2 (Warm): Database 1 hour TTL for moderately accessed data
- Tier 3 (CDN): Static files 24 hour TTL for charts/images

Features:
- Automatic tier promotion/demotion based on access patterns
- Smart cache invalidation
- Cache warming on startup
- Hit rate monitoring and metrics
"""

import hashlib
import json
import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from sqlalchemy import Column, DateTime, Index, Integer, String, Text, text
from sqlalchemy.ext.declarative import declarative_base

from app.config import get_settings
from app.services.cache import CacheService
from app.services.database import DatabaseService

logger = logging.getLogger(__name__)

CacheBase = declarative_base()


class CacheTier(Enum):
    """Cache tier definitions"""

    HOT = "hot"  # Redis: 5-15min TTL, ultra-fast access
    WARM = "warm"  # Database: 1 hour TTL, fast access
    CDN = "cdn"  # Static files: 24 hour TTL, cached charts


class CacheEntry(CacheBase):
    """Database model for warm cache tier"""

    __tablename__ = "cache_entries"

    cache_key = Column(String(512), primary_key=True, index=True)
    cache_value = Column(Text, nullable=False)
    cache_tier = Column(String(20), default="warm", index=True)
    hit_count = Column(Integer, default=0)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False, index=True)
    data_type = Column(String(50), index=True)  # pattern, price, chart, etc.

    __table_args__ = (
        Index("idx_tier_expires", "cache_tier", "expires_at"),
        Index("idx_type_expires", "data_type", "expires_at"),
    )


@dataclass
class CacheMetrics:
    """Cache performance metrics"""

    total_requests: int = 0
    hot_hits: int = 0
    warm_hits: int = 0
    cdn_hits: int = 0
    misses: int = 0
    evictions: int = 0
    promotions: int = 0
    demotions: int = 0

    @property
    def total_hits(self) -> int:
        return self.hot_hits + self.warm_hits + self.cdn_hits

    @property
    def hit_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return (self.total_hits / self.total_requests) * 100

    @property
    def tier_distribution(self) -> Dict[str, float]:
        """Percentage of hits per tier"""
        if self.total_hits == 0:
            return {"hot": 0, "warm": 0, "cdn": 0}
        return {
            "hot": (self.hot_hits / self.total_hits) * 100,
            "warm": (self.warm_hits / self.total_hits) * 100,
            "cdn": (self.cdn_hits / self.total_hits) * 100,
        }


class MultiTierCache:
    """
    Intelligent multi-tier cache manager

    Automatically manages data across three cache tiers based on
    access patterns and data characteristics.
    """

    # TTL configurations (seconds)
    TTL_HOT_MIN = 300  # 5 minutes
    TTL_HOT_MAX = 900  # 15 minutes
    TTL_WARM = 3600  # 1 hour
    TTL_CDN = 86400  # 24 hours

    # Promotion thresholds
    PROMOTION_THRESHOLD = 3  # Access count to promote from warm to hot
    HOT_TIER_MAX_SIZE = 10000  # Max keys in hot tier before eviction

    def __init__(
        self, cache_service: CacheService, db_service: Optional[DatabaseService] = None
    ):
        self.cache_service = cache_service
        self.db_service = db_service
        self.metrics = CacheMetrics()
        self.cdn_path = Path("/tmp/legend-ai-cdn")  # Static file cache path
        self.cdn_path.mkdir(exist_ok=True)

        # Initialize database tables for warm cache
        if self.db_service and self.db_service.engine:
            CacheEntry.__table__.create(self.db_service.engine, checkfirst=True)
            logger.info("✅ Multi-tier cache tables initialized")

    async def get(self, key: str, data_type: str = "generic") -> Optional[Any]:
        """
        Get value from cache (checks all tiers in order: hot -> warm -> CDN)

        Args:
            key: Cache key
            data_type: Type of data (pattern, price, chart, etc.)

        Returns:
            Cached value or None if not found
        """
        self.metrics.total_requests += 1
        start_time = time.time()

        # Tier 1: Check hot cache (Redis)
        value = await self._get_hot(key)
        if value is not None:
            self.metrics.hot_hits += 1
            logger.debug(f"🔥 Hot cache HIT: {key} ({time.time() - start_time:.3f}s)")
            return value

        # Tier 2: Check warm cache (Database)
        value = await self._get_warm(key)
        if value is not None:
            self.metrics.warm_hits += 1
            logger.debug(f"🌡️ Warm cache HIT: {key} ({time.time() - start_time:.3f}s)")

            # Promote to hot cache if accessed frequently
            await self._maybe_promote(key, data_type)
            return value

        # Tier 3: Check CDN cache (Static files) - only for charts
        if data_type == "chart":
            value = await self._get_cdn(key)
            if value is not None:
                self.metrics.cdn_hits += 1
                logger.debug(
                    f"📦 CDN cache HIT: {key} ({time.time() - start_time:.3f}s)"
                )
                return value

        # Cache miss
        self.metrics.misses += 1
        logger.debug(f"❌ Cache MISS: {key} ({time.time() - start_time:.3f}s)")
        return None

    async def set(
        self,
        key: str,
        value: Any,
        data_type: str = "generic",
        tier: Optional[CacheTier] = None,
    ) -> bool:
        """
        Set value in appropriate cache tier

        Args:
            key: Cache key
            value: Value to cache
            data_type: Type of data (determines default tier)
            tier: Force specific tier (optional)

        Returns:
            True if cached successfully
        """
        # Determine appropriate tier based on data type if not specified
        if tier is None:
            tier = self._determine_tier(data_type)

        success = False

        if tier == CacheTier.HOT:
            ttl = self._calculate_hot_ttl(data_type)
            success = await self._set_hot(key, value, ttl)
            logger.debug(f"🔥 Set hot cache: {key} (TTL: {ttl}s)")

        elif tier == CacheTier.WARM:
            success = await self._set_warm(key, value, data_type, self.TTL_WARM)
            logger.debug(f"🌡️ Set warm cache: {key} (TTL: {self.TTL_WARM}s)")

        elif tier == CacheTier.CDN:
            success = await self._set_cdn(key, value)
            logger.debug(f"📦 Set CDN cache: {key} (TTL: {self.TTL_CDN}s)")

        return success

    async def invalidate(self, key: str, all_tiers: bool = True) -> int:
        """
        Invalidate cache entry across tiers

        Args:
            key: Cache key to invalidate
            all_tiers: If True, invalidates across all tiers

        Returns:
            Number of entries invalidated
        """
        count = 0

        if all_tiers:
            # Invalidate from all tiers
            redis = await self.cache_service._get_redis()
            hot_deleted = await redis.delete(key)
            count += hot_deleted

            if self.db_service:
                warm_deleted = await self._invalidate_warm(key)
                count += warm_deleted

            cdn_deleted = await self._invalidate_cdn(key)
            count += cdn_deleted

            logger.info(f"🗑️ Invalidated {count} cache entries for key: {key}")

        return count

    async def invalidate_pattern(self, pattern: str) -> int:
        """
        Invalidate all keys matching pattern

        Args:
            pattern: Redis key pattern (e.g., "pattern:*", "ohlcv:AAPL:*")

        Returns:
            Number of entries invalidated
        """
        count = 0

        # Invalidate from Redis
        redis = await self.cache_service._get_redis()
        keys = await redis.keys(pattern)
        if keys:
            count += await redis.delete(*keys)

        # Invalidate from database (warm tier)
        if self.db_service:
            with self.db_service.get_db() as db:
                # Convert Redis pattern to SQL LIKE pattern
                sql_pattern = pattern.replace("*", "%")
                result = db.execute(
                    text("DELETE FROM cache_entries WHERE cache_key LIKE :pattern"),
                    {"pattern": sql_pattern},
                )
                count += result.rowcount
                db.commit()

        logger.info(f"🗑️ Invalidated {count} cache entries matching pattern: {pattern}")
        return count

    async def warm_cache(self, data_to_warm: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Warm cache on startup with frequently accessed data

        Args:
            data_to_warm: List of dicts with keys: key, value, data_type

        Returns:
            Statistics on warmed cache entries
        """
        stats = {"hot": 0, "warm": 0, "failed": 0}

        logger.info(f"🔄 Starting cache warming with {len(data_to_warm)} entries...")

        for item in data_to_warm:
            try:
                key = item["key"]
                value = item["value"]
                data_type = item.get("data_type", "generic")

                # Warm both hot and warm tiers
                hot_success = await self.set(key, value, data_type, tier=CacheTier.HOT)
                warm_success = await self.set(
                    key, value, data_type, tier=CacheTier.WARM
                )

                if hot_success:
                    stats["hot"] += 1
                if warm_success:
                    stats["warm"] += 1

            except Exception as e:
                logger.error(f"Failed to warm cache for key {item.get('key')}: {e}")
                stats["failed"] += 1

        logger.info(f"✅ Cache warming complete: {stats}")
        return stats

    async def cleanup_expired(self) -> Dict[str, int]:
        """
        Clean up expired cache entries from all tiers

        Returns:
            Statistics on cleaned entries
        """
        stats = {"warm": 0, "cdn": 0}

        # Clean expired warm cache entries
        if self.db_service:
            with self.db_service.get_db() as db:
                result = db.execute(
                    text("DELETE FROM cache_entries WHERE expires_at < :now"),
                    {"now": datetime.utcnow()},
                )
                stats["warm"] = result.rowcount
                db.commit()

        # Clean expired CDN files (older than 24 hours)
        cdn_cleaned = 0
        cutoff_time = time.time() - self.TTL_CDN

        for file_path in self.cdn_path.glob("*"):
            if file_path.stat().st_mtime < cutoff_time:
                file_path.unlink()
                cdn_cleaned += 1

        stats["cdn"] = cdn_cleaned
        self.metrics.evictions += stats["warm"] + stats["cdn"]

        logger.info(f"🧹 Cleaned up expired cache: {stats}")
        return stats

    def get_metrics(self) -> Dict[str, Any]:
        """Get comprehensive cache metrics"""
        return {
            "hit_rate_percent": round(self.metrics.hit_rate, 2),
            "total_requests": self.metrics.total_requests,
            "total_hits": self.metrics.total_hits,
            "total_misses": self.metrics.misses,
            "tier_hits": {
                "hot": self.metrics.hot_hits,
                "warm": self.metrics.warm_hits,
                "cdn": self.metrics.cdn_hits,
            },
            "tier_distribution_percent": {
                k: round(v, 2) for k, v in self.metrics.tier_distribution.items()
            },
            "promotions": self.metrics.promotions,
            "demotions": self.metrics.demotions,
            "evictions": self.metrics.evictions,
        }

    async def get_detailed_stats(self) -> Dict[str, Any]:
        """Get detailed cache statistics including Redis and DB stats"""
        redis_stats = await self.cache_service.get_cache_stats()
        multi_tier_stats = self.get_metrics()

        db_stats = {}
        if self.db_service:
            with self.db_service.get_db() as db:
                # Count entries by tier
                result = db.execute(
                    text(
                        "SELECT cache_tier, COUNT(*) as count FROM cache_entries GROUP BY cache_tier"
                    )
                )
                db_stats["entries_by_tier"] = {row[0]: row[1] for row in result}

                # Count entries by type
                result = db.execute(
                    text(
                        "SELECT data_type, COUNT(*) as count FROM cache_entries GROUP BY data_type"
                    )
                )
                db_stats["entries_by_type"] = {row[0]: row[1] for row in result}

                # Get most accessed entries
                result = db.execute(
                    text(
                        """
                        SELECT cache_key, hit_count, data_type
                        FROM cache_entries
                        ORDER BY hit_count DESC
                        LIMIT 10
                    """
                    )
                )
                db_stats["top_accessed"] = [
                    {"key": row[0], "hits": row[1], "type": row[2]} for row in result
                ]

        return {
            "multi_tier": multi_tier_stats,
            "redis": redis_stats,
            "database": db_stats,
            "cdn": {
                "path": str(self.cdn_path),
                "files": len(list(self.cdn_path.glob("*"))),
            },
        }

    # ==================== Private Helper Methods ====================

    def _determine_tier(self, data_type: str) -> CacheTier:
        """Determine appropriate cache tier based on data type"""
        if data_type == "chart":
            return CacheTier.CDN  # Charts go to CDN
        elif data_type in ["price", "pattern"]:
            return CacheTier.HOT  # Frequently accessed data goes to hot tier
        else:
            return CacheTier.WARM  # Everything else goes to warm tier

    def _calculate_hot_ttl(self, data_type: str) -> int:
        """Calculate appropriate TTL for hot cache based on data type"""
        if data_type == "price":
            return self.TTL_HOT_MAX  # 15 minutes for price data
        elif data_type == "pattern":
            return self.TTL_HOT_MAX  # 15 minutes for pattern results
        else:
            return self.TTL_HOT_MIN  # 5 minutes for other data

    async def _get_hot(self, key: str) -> Optional[Any]:
        """Get from hot tier (Redis)"""
        return await self.cache_service.get(key)

    async def _set_hot(self, key: str, value: Any, ttl: int) -> bool:
        """Set in hot tier (Redis)"""
        return await self.cache_service.set(key, value, ttl)

    async def _get_warm(self, key: str) -> Optional[Any]:
        """Get from warm tier (Database)"""
        if not self.db_service:
            return None

        try:
            with self.db_service.get_db() as db:
                result = db.execute(
                    text(
                        """
                        SELECT cache_value, hit_count
                        FROM cache_entries
                        WHERE cache_key = :key
                        AND expires_at > :now
                    """
                    ),
                    {"key": key, "now": datetime.utcnow()},
                ).fetchone()

                if result:
                    # Update hit count and last accessed time
                    db.execute(
                        text(
                            """
                            UPDATE cache_entries
                            SET hit_count = hit_count + 1, last_accessed = :now
                            WHERE cache_key = :key
                        """
                        ),
                        {"key": key, "now": datetime.utcnow()},
                    )
                    db.commit()

                    # Deserialize value
                    try:
                        return json.loads(result[0])
                    except Exception:
                        return result[0]

                return None

        except Exception as e:
            logger.error(f"Error getting from warm cache: {e}")
            return None

    async def _set_warm(self, key: str, value: Any, data_type: str, ttl: int) -> bool:
        """Set in warm tier (Database)"""
        if not self.db_service:
            return False

        try:
            with self.db_service.get_db() as db:
                # Serialize value
                if isinstance(value, (dict, list)):
                    value_str = json.dumps(value)
                else:
                    value_str = str(value)

                expires_at = datetime.utcnow() + timedelta(seconds=ttl)

                # Upsert cache entry
                db.execute(
                    text(
                        """
                        INSERT INTO cache_entries
                        (cache_key, cache_value, cache_tier, data_type, expires_at, created_at, last_accessed, hit_count)
                        VALUES (:key, :value, 'warm', :data_type, :expires_at, :now, :now, 0)
                        ON CONFLICT (cache_key)
                        DO UPDATE SET
                            cache_value = :value,
                            expires_at = :expires_at,
                            last_accessed = :now
                    """
                    ),
                    {
                        "key": key,
                        "value": value_str,
                        "data_type": data_type,
                        "expires_at": expires_at,
                        "now": datetime.utcnow(),
                    },
                )
                db.commit()
                return True

        except Exception as e:
            logger.error(f"Error setting warm cache: {e}")
            return False

    async def _get_cdn(self, key: str) -> Optional[str]:
        """Get from CDN tier (Static files)"""
        cache_file = self.cdn_path / self._hash_key(key)

        if cache_file.exists():
            # Check if expired
            if time.time() - cache_file.stat().st_mtime < self.TTL_CDN:
                return cache_file.read_text()

        return None

    async def _set_cdn(self, key: str, value: Any) -> bool:
        """Set in CDN tier (Static files)"""
        try:
            cache_file = self.cdn_path / self._hash_key(key)

            if isinstance(value, (dict, list)):
                cache_file.write_text(json.dumps(value))
            else:
                cache_file.write_text(str(value))

            return True

        except Exception as e:
            logger.error(f"Error setting CDN cache: {e}")
            return False

    async def _invalidate_warm(self, key: str) -> int:
        """Invalidate from warm tier"""
        if not self.db_service:
            return 0

        with self.db_service.get_db() as db:
            result = db.execute(
                text("DELETE FROM cache_entries WHERE cache_key = :key"), {"key": key}
            )
            db.commit()
            return result.rowcount

    async def _invalidate_cdn(self, key: str) -> int:
        """Invalidate from CDN tier"""
        cache_file = self.cdn_path / self._hash_key(key)
        if cache_file.exists():
            cache_file.unlink()
            return 1
        return 0

    async def _maybe_promote(self, key: str, data_type: str):
        """Promote frequently accessed warm cache entries to hot tier"""
        if not self.db_service:
            return

        try:
            with self.db_service.get_db() as db:
                result = db.execute(
                    text(
                        "SELECT cache_value, hit_count FROM cache_entries WHERE cache_key = :key"
                    ),
                    {"key": key},
                ).fetchone()

                if result and result[1] >= self.PROMOTION_THRESHOLD:
                    # Promote to hot tier
                    value = result[0]
                    try:
                        value = json.loads(value)
                    except Exception:
                        pass

                    ttl = self._calculate_hot_ttl(data_type)
                    await self._set_hot(key, value, ttl)
                    self.metrics.promotions += 1
                    logger.debug(f"⬆️ Promoted to hot cache: {key} (hits: {result[1]})")

        except Exception as e:
            logger.error(f"Error during cache promotion: {e}")

    def _hash_key(self, key: str) -> str:
        """Generate a safe filename from cache key"""
        return hashlib.sha256(key.encode()).hexdigest()


# Global multi-tier cache instance
_multi_tier_cache: Optional[MultiTierCache] = None


def get_multi_tier_cache() -> MultiTierCache:
    """Get global multi-tier cache instance"""
    global _multi_tier_cache

    if _multi_tier_cache is None:
        from app.services.cache import get_cache_service
        from app.services.database import get_database_service

        settings = get_settings()
        cache_service = get_cache_service()

        # Database service is optional
        db_service = None
        if settings.database_url:
            try:
                db_service = get_database_service()
            except Exception as e:
                logger.warning(f"Database not available for warm cache: {e}")

        _multi_tier_cache = MultiTierCache(cache_service, db_service)
        logger.info("✅ Multi-tier cache initialized")

    return _multi_tier_cache
