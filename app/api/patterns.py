from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import logging

from app.core.pattern_detector import PatternDetector, PatternResult
from app.services.market_data import market_data_service
from app.services.cache import get_cache_service
from app.services.charting import get_charting_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/patterns", tags=["patterns"])


class PatternRequest(BaseModel):
    """Request model for pattern detection"""
    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL, TSLA, SPY)", example="AAPL")
    interval: str = Field("1day", description="Time interval: 1min, 5min, 15min, 30min, 1h, 4h, 1day, 1week", example="1day")
    use_yahoo_fallback: bool = Field(True, description="Use Yahoo Finance as fallback data source")

    @field_validator("interval")
    @classmethod
    def validate_interval(cls, v: str) -> str:
        allowed = {"1min", "5min", "15min", "30min", "1h", "4h", "1day", "1week"}
        if v not in allowed:
            raise ValueError(f"Interval must be one of: {', '.join(allowed)}")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "ticker": "AAPL",
                "interval": "1day",
                "use_yahoo_fallback": True
            }
        }


class PatternResponse(BaseModel):
    """Response model for pattern detection"""
    success: bool = Field(..., description="Whether the request was successful")
    data: Optional[PatternResult] = Field(None, description="Pattern analysis result")
    error: Optional[str] = Field(None, description="Error message if request failed")
    cached: bool = Field(False, description="Whether result was served from cache")
    api_used: str = Field("unknown", description="Data source used (cache, twelvedata, finnhub, alphavantage, yahoo)")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "ticker": "AAPL",
                    "pattern": "Cup and Handle",
                    "score": 8.5,
                    "entry": 175.50,
                    "stop": 168.00,
                    "target": 190.25,
                    "support_start": 170.00,
                    "support_end": 172.00,
                    "risk_reward_ratio": 2.1,
                    "chart_url": "https://chart-img.com/AAPL",
                    "timestamp": "2024-01-15T10:30:00"
                },
                "error": None,
                "cached": False,
                "api_used": "twelvedata",
                "processing_time": 1.23
            }
        }


@router.post("/detect",
             response_model=PatternResponse,
             summary="Detect Chart Pattern",
             responses={
                 200: {
                     "description": "Successful pattern detection",
                     "content": {
                         "application/json": {
                             "example": {
                                 "success": True,
                                 "data": {
                                     "ticker": "AAPL",
                                     "pattern": "Cup and Handle",
                                     "score": 8.5,
                                     "entry": 175.50,
                                     "stop": 168.00,
                                     "target": 190.25,
                                     "support_start": 170.00,
                                     "support_end": 172.00,
                                     "risk_reward_ratio": 2.1,
                                     "chart_url": "https://chart-img.com/chart.png",
                                     "timestamp": "2024-01-15T10:30:00"
                                 },
                                 "error": None,
                                 "cached": False,
                                 "api_used": "twelvedata",
                                 "processing_time": 1.23
                             }
                         }
                     }
                 },
                 400: {
                     "description": "Bad Request - Invalid ticker format",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Invalid ticker symbol format"
                             }
                         }
                     }
                 },
                 404: {
                     "description": "Not Found - No price data available",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "No price data available for INVALID"
                             }
                         }
                     }
                 }
             })
async def detect_pattern(request: PatternRequest):
    """
    🎯 **Detect Chart Pattern for Any Stock**

    Analyzes price action and detects bullish chart patterns with AI-powered scoring.

    ## Features

    - ✅ Multi-source data (TwelveData → Finnhub → AlphaVantage → Yahoo)
    - ✅ Smart caching (1-hour TTL)
    - ✅ Automatic chart generation with indicators
    - ✅ Entry, stop, and target levels
    - ✅ Risk/reward ratio calculation

    ## Supported Patterns

    - Cup and Handle
    - Bullish Flag
    - Ascending Triangle
    - Double Bottom
    - And more...

    ## Example Usage

    **Python:**
    ```python
    import requests

    response = requests.post(
        'https://your-api.com/api/patterns/detect',
        json={'ticker': 'AAPL', 'interval': '1day'}
    )

    result = response.json()
    if result['success']:
        print(f"Pattern: {result['data']['pattern']}")
        print(f"Score: {result['data']['score']}/10")
        print(f"Entry: ${result['data']['entry']}")
    ```

    **cURL:**
    ```bash
    curl -X POST "https://your-api.com/api/patterns/detect" \\
      -H "Content-Type: application/json" \\
      -d '{"ticker": "AAPL", "interval": "1day"}'
    ```

    **JavaScript:**
    ```javascript
    const response = await fetch('/api/patterns/detect', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ticker: 'AAPL', interval: '1day'})
    });
    const result = await response.json();
    ```

    ## Response Fields

    | Field | Type | Description |
    |-------|------|-------------|
    | `success` | boolean | Request success status |
    | `data.pattern` | string | Detected pattern name |
    | `data.score` | float | Confidence score (0-10) |
    | `data.entry` | float | Suggested entry price |
    | `data.stop` | float | Stop loss price |
    | `data.target` | float | Target price |
    | `data.chart_url` | string | Generated chart URL |
    | `cached` | boolean | Served from cache? |
    | `processing_time` | float | Processing time (seconds) |

    ## Notes

    - Cached results are refreshed hourly
    - Chart URLs include support/resistance levels
    - Processing time typically < 2 seconds

    ---

    **Replaces legacy endpoint:** `POST /webhook/pattern-signal`
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

            # Always regenerate fresh chart URLs with latest indicators
            try:
                charting = get_charting_service()
                chart_url = await charting.generate_chart(
                    ticker=ticker,
                    timeframe=request.interval,
                    entry=result.entry,
                    stop=result.stop,
                    target=result.target,
                    support=result.support_start,
                    resistance=None  # Could add support_end or resistance level
                )
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

        # Generate chart with indicators and drawings
        try:
            charting = get_charting_service()
            chart_url = await charting.generate_chart(
                ticker=ticker,
                timeframe=request.interval,
                entry=result.entry,
                stop=result.stop,
                target=result.target,
                support=result.support_start,
                resistance=None  # Could add support_end or resistance level
            )
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
    cache_status = "unknown"
    market_data_status = "unknown"

    try:
        cache = get_cache_service()
        cache_health = await cache.health_check()
        cache_status = cache_health["status"]
    except Exception as e:
        logger.warning(f"Cache health check failed: {e}")
        cache_status = "disconnected"

    try:
        # Test market data service with a quick request
        test_data = await market_data_service.get_time_series("AAPL", "1day", 1)
        market_data_status = "connected" if test_data else "error"
    except Exception as e:
        logger.warning(f"Market data health check failed: {e}")
        market_data_status = "disconnected"

    return {
        "status": "healthy",
        "market_data_service": market_data_status,
        "redis_cache": cache_status,
        "pattern_detector": "ready"
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
