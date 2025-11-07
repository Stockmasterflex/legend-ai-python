from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
import time

from app.services.charting import get_charting_service
from app.core.chart_generator import ChartGenerator, ChartConfig, get_chart_generator
from app.services.cache import get_cache_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/charts", tags=["charts"])


class ChartRequest(BaseModel):
    ticker: str
    interval: str = "1D"
    entry: Optional[float] = None
    stop: Optional[float] = None
    target: Optional[float] = None
    show_volume: bool = True
    show_ema10: bool = True
    show_ema21: bool = True
    show_sma50: bool = True
    show_sma150: bool = True
    show_sma200: bool = True


class MultiTimeframeChartRequest(BaseModel):
    ticker: str
    timeframes: List[str] = ["1day", "1week", "60min"]
    entry: Optional[float] = None
    stop: Optional[float] = None
    target: Optional[float] = None
    overlays: Optional[List[str]] = None


class ChartResponse(BaseModel):
    success: bool
    chart_url: Optional[str] = None
    error: Optional[str] = None
    cached: bool = False
    ticker: str
    interval: str
    processing_time: Optional[float] = None


class MultiTimeframeChartResponse(BaseModel):
    success: bool
    ticker: str
    charts: Dict[str, str] = {}  # timeframe -> chart_url
    failed_timeframes: List[str] = []
    processing_time: Optional[float] = None
    message: Optional[str] = None


@router.post("/generate", response_model=ChartResponse)
async def generate_chart(request: ChartRequest):
    """
    Generate annotated chart with entry/stop/target

    Replaces n8n webhook: POST /webhook/chart-generator

    Args:
        request: Chart generation request with trade levels

    Returns:
        Chart URL and metadata
    """
    start_time = time.time()
    cache = get_cache_service()
    charting_service = get_charting_service()

    try:
        logger.info(f"🎨 Generating chart for {request.ticker} with annotations")

        # Try cache first (24 hour TTL for generated charts)
        cached_url = await cache.get_chart(request.ticker, request.interval)
        if cached_url:
            processing_time = time.time() - start_time
            logger.info(f"⚡ Chart cache hit for {request.ticker}: {cached_url[:50]}...")

            return ChartResponse(
                success=True,
                chart_url=cached_url,
                cached=True,
                ticker=request.ticker,
                interval=request.interval,
                processing_time=round(processing_time, 2)
            )

        # Map overlay request flags to indicator list
        overlays = []
        if request.show_volume:
            overlays.append("Volume")
        if request.show_ema10:
            overlays.append("EMA10")
        if request.show_ema21:
            overlays.append("EMA21")
        if request.show_sma50:
            overlays.append("SMA50")
        if request.show_sma150:
            overlays.append("SMA150")
        if request.show_sma200:
            overlays.append("SMA200")

        # Generate new chart using enhanced ChartingService
        chart_url = await charting_service.generate_chart(
            ticker=request.ticker,
            timeframe=request.interval.lower(),
            entry=request.entry,
            stop=request.stop,
            target=request.target,
            overlays=overlays if overlays else None
        )

        if chart_url:
            # Cache the chart URL
            await cache.set_chart(request.ticker, request.interval, chart_url)

            processing_time = time.time() - start_time
            logger.info(f"✅ Chart generated for {request.ticker} in {processing_time:.2f}s")

            return ChartResponse(
                success=True,
                chart_url=chart_url,
                cached=False,
                ticker=request.ticker,
                interval=request.interval,
                processing_time=round(processing_time, 2)
            )
        else:
            processing_time = time.time() - start_time
            logger.error(f"🚫 Chart generation failed for {request.ticker}")

            return ChartResponse(
                success=False,
                error="Chart generation failed - using fallback",
                cached=False,
                ticker=request.ticker,
                interval=request.interval,
                processing_time=round(processing_time, 2)
            )

    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"💥 Chart generation error for {request.ticker}: {e}")

        return ChartResponse(
            success=False,
            error=str(e),
            cached=False,
            ticker=request.ticker,
            interval=request.interval,
            processing_time=round(processing_time, 2)
        )


@router.post("/multi", response_model=MultiTimeframeChartResponse)
async def generate_multi_timeframe_charts(request: MultiTimeframeChartRequest):
    """
    Generate charts for multiple timeframes in one request

    Perfect for multi-timeframe analysis (1D, 1W, 60m)

    Args:
        request: Multi-timeframe chart request

    Returns:
        Chart URLs for each requested timeframe
    """
    start_time = time.time()
    charting_service = get_charting_service()

    try:
        logger.info(f"🎨 Generating multi-timeframe charts for {request.ticker}: {request.timeframes}")

        # Generate charts for all timeframes concurrently
        chart_urls = await charting_service.generate_multi_timeframe_charts(
            ticker=request.ticker,
            timeframes=request.timeframes,
            entry=request.entry,
            stop=request.stop,
            target=request.target,
            overlays=request.overlays
        )

        processing_time = time.time() - start_time

        failed_timeframes = [
            tf for tf in request.timeframes if tf not in chart_urls
        ]

        if chart_urls:
            return MultiTimeframeChartResponse(
                success=True,
                ticker=request.ticker,
                charts=chart_urls,
                failed_timeframes=failed_timeframes,
                processing_time=round(processing_time, 2),
                message=f"Generated {len(chart_urls)}/{len(request.timeframes)} charts"
            )
        else:
            return MultiTimeframeChartResponse(
                success=False,
                ticker=request.ticker,
                charts={},
                failed_timeframes=request.timeframes,
                processing_time=round(processing_time, 2),
                message="Failed to generate any charts"
            )

    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"💥 Multi-timeframe chart error for {request.ticker}: {e}")

        return MultiTimeframeChartResponse(
            success=False,
            ticker=request.ticker,
            charts={},
            failed_timeframes=request.timeframes,
            processing_time=round(processing_time, 2),
            message=f"Error: {str(e)}"
        )


@router.get("/health")
async def charts_health():
    """Health check for charts service"""
    try:
        charting_service = get_charting_service()

        # Check Chart-IMG API connection with a quick chart generation
        # Use fallback mode flag to determine if we're degraded
        status_msg = "connected"
        if charting_service.fallback_mode:
            status_msg = "degraded (fallback mode)"

        return {
            "status": "healthy",
            "chart_img_api": status_msg,
            "call_count": charting_service.call_count,
            "daily_limit": charting_service.daily_limit,
            "remaining_calls": charting_service.daily_limit - charting_service.call_count
        }
    except Exception as e:
        return {
            "status": "error",
            "chart_img_api": "disconnected",
            "error": str(e)
        }
