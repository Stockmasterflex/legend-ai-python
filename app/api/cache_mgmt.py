"""
Cache Management API
Provides endpoints for cache monitoring, invalidation, and warming
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import logging

from app.services.multi_tier_cache import get_multi_tier_cache, CacheTier
from app.services.cache_warmer import get_cache_warmer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/cache", tags=["cache"])


class CacheInvalidateRequest(BaseModel):
    """Request to invalidate cache entries"""
    key: Optional[str] = None
    pattern: Optional[str] = None
    all_tiers: bool = True


class CacheWarmRequest(BaseModel):
    """Request to warm cache with data"""
    data: List[Dict[str, Any]]


class CacheSetRequest(BaseModel):
    """Request to manually set cache entry"""
    key: str
    value: Any
    data_type: str = "generic"
    tier: Optional[str] = None


@router.get("/stats")
async def get_cache_stats():
    """
    Get comprehensive cache statistics

    Returns detailed metrics including:
    - Hit rates across all tiers
    - Tier distribution
    - Promotions/demotions
    - Redis stats
    - Database cache stats
    - CDN stats
    """
    try:
        cache = get_multi_tier_cache()
        stats = await cache.get_detailed_stats()

        return {
            "status": "success",
            "data": stats
        }

    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics")
async def get_cache_metrics():
    """
    Get high-level cache metrics

    Returns:
    - Hit rate percentage
    - Total requests
    - Hits/misses breakdown
    - Tier distribution
    """
    try:
        cache = get_multi_tier_cache()
        metrics = cache.get_metrics()

        return {
            "status": "success",
            "data": metrics
        }

    except Exception as e:
        logger.error(f"Error getting cache metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/invalidate")
async def invalidate_cache(request: CacheInvalidateRequest):
    """
    Invalidate cache entries

    Args:
        key: Specific cache key to invalidate (optional)
        pattern: Pattern to match multiple keys (e.g., "pattern:*", "ohlcv:AAPL:*")
        all_tiers: If true, invalidates across all cache tiers

    Returns:
        Number of entries invalidated
    """
    try:
        cache = get_multi_tier_cache()
        count = 0

        if request.pattern:
            # Invalidate by pattern
            count = await cache.invalidate_pattern(request.pattern)
            logger.info(f"Invalidated {count} entries matching pattern: {request.pattern}")

        elif request.key:
            # Invalidate specific key
            count = await cache.invalidate(request.key, all_tiers=request.all_tiers)
            logger.info(f"Invalidated {count} entries for key: {request.key}")

        else:
            raise HTTPException(status_code=400, detail="Must provide either 'key' or 'pattern'")

        return {
            "status": "success",
            "invalidated": count,
            "key": request.key,
            "pattern": request.pattern
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error invalidating cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/warm")
async def warm_cache(request: CacheWarmRequest):
    """
    Warm cache with provided data

    Useful for pre-populating cache on startup or after clearing.

    Args:
        data: List of cache entries to warm
              Each entry should have: key, value, data_type

    Returns:
        Statistics on warmed entries
    """
    try:
        cache = get_multi_tier_cache()
        stats = await cache.warm_cache(request.data)

        return {
            "status": "success",
            "stats": stats
        }

    except Exception as e:
        logger.error(f"Error warming cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cleanup")
async def cleanup_cache():
    """
    Clean up expired cache entries across all tiers

    Returns:
        Statistics on cleaned entries
    """
    try:
        cache = get_multi_tier_cache()
        stats = await cache.cleanup_expired()

        return {
            "status": "success",
            "cleaned": stats
        }

    except Exception as e:
        logger.error(f"Error cleaning up cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/set")
async def set_cache_entry(request: CacheSetRequest):
    """
    Manually set a cache entry

    Args:
        key: Cache key
        value: Value to cache
        data_type: Type of data (pattern, price, chart, etc.)
        tier: Force specific tier (hot, warm, cdn) - optional

    Returns:
        Success status
    """
    try:
        cache = get_multi_tier_cache()

        tier = None
        if request.tier:
            tier = CacheTier(request.tier)

        success = await cache.set(
            request.key,
            request.value,
            data_type=request.data_type,
            tier=tier
        )

        if not success:
            raise HTTPException(status_code=500, detail="Failed to set cache entry")

        return {
            "status": "success",
            "key": request.key,
            "tier": request.tier or "auto"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid tier: {request.tier}")
    except Exception as e:
        logger.error(f"Error setting cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get/{key}")
async def get_cache_entry(key: str, data_type: str = Query("generic")):
    """
    Get a cache entry

    Args:
        key: Cache key to retrieve
        data_type: Type of data (for tier selection)

    Returns:
        Cached value or 404 if not found
    """
    try:
        cache = get_multi_tier_cache()
        value = await cache.get(key, data_type=data_type)

        if value is None:
            raise HTTPException(status_code=404, detail="Cache entry not found")

        return {
            "status": "success",
            "key": key,
            "value": value
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting cache entry: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def cache_health():
    """
    Check cache system health

    Returns health status of all cache tiers
    """
    try:
        cache = get_multi_tier_cache()

        # Check Redis health
        redis_health = await cache.cache_service.health_check()

        # Check database health (if available)
        db_health = {"status": "not_configured"}
        if cache.db_service:
            db_health = cache.db_service.health_check()

        # Check CDN path
        cdn_health = {
            "status": "healthy" if cache.cdn_path.exists() else "unhealthy",
            "path": str(cache.cdn_path),
            "writable": cache.cdn_path.exists() and cache.cdn_path.is_dir()
        }

        overall_status = "healthy"
        if redis_health.get("status") != "healthy":
            overall_status = "degraded"

        return {
            "status": overall_status,
            "tiers": {
                "hot": redis_health,
                "warm": db_health,
                "cdn": cdn_health
            }
        }

    except Exception as e:
        logger.error(f"Error checking cache health: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@router.post("/warm/ticker/{ticker}")
async def warm_ticker_cache(ticker: str):
    """
    Warm cache for a specific ticker

    Args:
        ticker: Stock ticker symbol (e.g., AAPL, MSFT)

    Returns:
        Success status
    """
    try:
        warmer = get_cache_warmer()
        success = await warmer.warm_ticker(ticker.upper())

        if not success:
            raise HTTPException(status_code=500, detail=f"Failed to warm cache for {ticker}")

        return {
            "status": "success",
            "ticker": ticker.upper(),
            "message": f"Cache warmed for {ticker.upper()}"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error warming ticker cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/warm/tickers")
async def warm_multiple_tickers(tickers: List[str]):
    """
    Warm cache for multiple tickers

    Args:
        tickers: List of stock ticker symbols

    Returns:
        Statistics on warmed tickers
    """
    try:
        warmer = get_cache_warmer()
        tickers_upper = [t.upper() for t in tickers]
        stats = await warmer.warm_tickers(tickers_upper)

        return {
            "status": "success",
            "tickers": tickers_upper,
            "stats": stats
        }

    except Exception as e:
        logger.error(f"Error warming multiple tickers: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/warm/all")
async def warm_all_cache():
    """
    Warm all cache tiers with popular data

    This endpoint triggers the same cache warming that runs on startup.
    Useful for refreshing cache or warming after a cache clear.

    Returns:
        Statistics on warmed cache entries
    """
    try:
        warmer = get_cache_warmer()
        stats = await warmer.warm_all()

        return {
            "status": "success",
            "stats": stats
        }

    except Exception as e:
        logger.error(f"Error warming all cache: {e}")
        raise HTTPException(status_code=500, detail=str(e))
