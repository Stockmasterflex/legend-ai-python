from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from app.core.pattern_detector import PatternDetector, PatternResult
from app.services.market_data import market_data_service
from app.services.cache import get_cache_service
from app.services.charting import get_charting_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/patterns", tags=["patterns"])


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
            # Convert ISO timestamp string back to datetime
            from datetime import datetime
            if isinstance(cached_result.get("timestamp"), str):
                cached_result["timestamp"] = datetime.fromisoformat(cached_result["timestamp"])

            result = PatternResult(**cached_result)

            # Always regenerate fresh chart URLs (charting service returns TradingView)
            try:
                charting = get_charting_service()
                chart_url = await charting.generate_chart(ticker, request.interval)
                if chart_url:
                    result.chart_url = chart_url
                    logger.info(f"📊 Chart regenerated for {ticker}: {chart_url[:60]}...")
            except Exception as e:
                logger.warning(f"⚠️ Chart regeneration failed for {ticker}: {e}")

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

        # 2. Cache miss - fetch from API (uses smart multi-source fallback)
        logger.info(f"📡 Cache miss for {ticker}, fetching from API")

        # Get price data (tries TwelveData → Finnhub → AlphaVantage → Yahoo)
        price_data = await market_data_service.get_time_series(
            ticker=ticker,
            interval=request.interval,
            outputsize=500
        )

        if not price_data:
            raise HTTPException(
                status_code=404,
                detail=f"No price data available for {ticker}"
            )

        api_used = price_data.get("source", "unknown")

        # Get SPY data for RS calculation
        spy_data = await market_data_service.get_time_series(
            ticker="SPY",
            interval="1day",
            outputsize=500
        )

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

        # Generate chart (with fallback)
        try:
            charting = get_charting_service()
            chart_url = await charting.generate_chart(ticker, request.interval)
            if chart_url:
                result.chart_url = chart_url
                logger.info(f"📊 Chart generated for {ticker}: {chart_url[:60]}...")
            else:
                logger.warning(f"⚠️ Chart service returned None for {ticker}")
                result.chart_url = None
        except Exception as e:
            logger.warning(f"⚠️ Chart generation failed for {ticker}: {e}")
            result.chart_url = None

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
