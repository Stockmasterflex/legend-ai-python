from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from app.core.pattern_detector import PatternDetector, PatternResult
from app.services.api_clients import twelve_data_client, yahoo_client
from app.services.cache import get_cache_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/patterns", tags=["patterns"])

@router.get("/health")
async def health():
    """Health check for patterns service"""
    cache = get_cache_service()
    try:
        stats = await cache.get_cache_stats()
        return {
            "status": "healthy",
            "cache": {
                "hits": stats.get("redis_hits", 0),
                "misses": stats.get("redis_misses", 0),
                "hit_rate": f"{stats.get('redis_hit_rate', 0):.1f}%" if stats.get("redis_hits", 0) > 0 else "0%",
                "total_keys": stats.get("total_keys", 0),
                "pattern_keys": stats.get("pattern_keys", 0),
                "price_keys": stats.get("price_keys", 0),
                "memory_used": stats.get("memory_used", "unknown")
            }
        }
    except Exception as e:
        return {"status": "degraded", "error": str(e)}


class PatternRequest(BaseModel):
    ticker: str
    interval: str = "1day"
    use_yahoo_fallback: bool = True  # For migration compatibility


class PatternResponse(BaseModel):
    success: bool
    data: Optional[PatternResult]
    error: Optional[str]
    cached: bool = False
    api_used: str = "unknown"
    processing_time: Optional[float] = None


@router.post("/detect", response_model=PatternResponse)
async def detect_pattern(request: PatternRequest):
    """
    Detect pattern setup for a ticker with caching

    Replaces n8n webhook: POST /webhook/pattern-signal

    Args:
        request: Pattern detection request

    Returns:
        Pattern analysis result
    """
    import time
    start_time = time.time()
    cache = get_cache_service()

    try:
        ticker = request.ticker.upper().strip()

        # Validate ticker format
        if not ticker or not ticker.replace(".", "").replace("-", "").isalnum():
            raise HTTPException(
                status_code=400,
                detail="Invalid ticker symbol format"
            )

        logger.info(f"🔍 Analyzing pattern for {ticker}")

        # 1. Try cache first
        cached_result = await cache.get_pattern(ticker=ticker, interval=request.interval)
        if cached_result:
            # Convert cached dict back to PatternResult
            result = PatternResult(**cached_result)
            processing_time = time.time() - start_time

            logger.info(f"⚡ Cache hit for {ticker}: {result.pattern} ({result.score}/10) in {processing_time:.2f}s")

            return PatternResponse(
                success=True,
                data=result,
                error=None,
                cached=True,
                api_used="cache",
                processing_time=round(processing_time, 2)
            )

        # 2. Cache miss - fetch from API
        logger.info(f"📡 Cache miss for {ticker}, fetching from API")

        # Try TwelveData first
        price_data = await twelve_data_client.get_time_series(
            ticker=ticker,
            interval=request.interval,
            outputsize=500  # Get plenty of data for analysis
        )

        api_used = "twelvedata"

        # Fallback to Yahoo Finance if TwelveData fails
        if not price_data and request.use_yahoo_fallback:
            logger.info(f"⚠️ TwelveData failed for {ticker}, trying Yahoo Finance")
            price_data = await yahoo_client.get_time_series(
                ticker=ticker,
                interval="1d",  # Yahoo uses different interval format
                range_param="5y"
            )
            api_used = "yahoo_finance"

        if not price_data:
            raise HTTPException(
                status_code=404,
                detail=f"No price data available for {ticker}"
            )

        # Cache the price data (15 min TTL)
        await cache.set_price_data(ticker, price_data)

        # Get SPY data for RS calculation
        spy_data = await cache.get_price_data("SPY")
        if not spy_data:
        spy_data = await twelve_data_client.get_time_series("SPY", "1day", 500)
        if not spy_data and request.use_yahoo_fallback:
            spy_data = await yahoo_client.get_time_series("SPY", "1d", "5y")
            if spy_data:
                await cache.set_price_data("SPY", spy_data)

        # Run pattern detection
        detector = PatternDetector()
        result = await detector.analyze_ticker(
            ticker=ticker,
            price_data=price_data,
            spy_data=spy_data
        )

        if not result:
            raise HTTPException(
                status_code=500,
                detail=f"Pattern analysis failed for {ticker}"
            )

        # Cache the result (1 hour TTL)
        await cache.set_pattern(ticker, request.interval, result.to_dict())

        processing_time = time.time() - start_time

        logger.info(f"✅ Pattern detected for {ticker}: {result.pattern} ({result.score}/10) in {processing_time:.2f}s")

        return PatternResponse(
            success=True,
            data=result,
            error=None,
            cached=False,
            api_used=api_used,
            processing_time=round(processing_time, 2)
        )

    except HTTPException:
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"💥 Pattern detection failed for {request.ticker}: {e}")

        return PatternResponse(
            success=False,
            data=None,
            error=str(e),
            cached=False,
            api_used="error",
            processing_time=round(processing_time, 2)
        )


@router.get("/health")
async def patterns_health():
    """Health check for patterns service"""
    # Test API clients
    twelvedata_status = "unknown"
    yahoo_status = "unknown"
    cache_status = "unknown"

    try:
        # Quick test with a known ticker
        test_data = await twelve_data_client.get_quote("AAPL")
        twelvedata_status = "connected" if test_data else "error"
    except:
        twelvedata_status = "disconnected"

    try:
        test_data = await yahoo_client.get_time_series("AAPL", "1d", "1mo")
        yahoo_status = "connected" if test_data else "error"
    except:
        yahoo_status = "disconnected"

    try:
        cache = get_cache_service()
        cache_health = await cache.health_check()
        cache_status = cache_health["status"]
    except:
        cache_status = "disconnected"

    return {
        "status": "healthy",
        "twelvedata_api": twelvedata_status,
        "yahoo_finance_api": yahoo_status,
        "redis_cache": cache_status,
        "pattern_detector": "ready",
        "usage": await twelve_data_client.get_usage_stats()
    }


@router.get("/cache/stats")
async def cache_stats():
    """Get cache statistics"""
    try:
        cache = get_cache_service()
        stats = await cache.get_cache_stats()
        return {
            "status": "success",
            "cache_stats": stats
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
    }
