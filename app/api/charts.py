from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

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


class ChartResponse(BaseModel):
    success: bool
    chart_url: Optional[str] = None
    error: Optional[str] = None
    cached: bool = False
    ticker: str
    interval: str
    processing_time: Optional[float] = None


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
    import time
    start_time = time.time()
    cache = get_cache_service()
    generator = get_chart_generator()

    try:
        logger.info(f"🎨 Generating chart for {request.ticker} with annotations")

        # Create cache key for chart
        cache_key = f"{request.ticker}:{request.interval}:{request.entry or 0}:{request.stop or 0}:{request.target or 0}"

        # Try cache first (15 min TTL)
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

        # Cache miss - generate new chart
        config = ChartConfig(
            ticker=request.ticker,
            interval=request.interval,
            entry=request.entry,
            stop=request.stop,
            target=request.target,
            show_volume=request.show_volume,
            show_ema10=request.show_ema10,
            show_ema21=request.show_ema21,
            show_sma50=request.show_sma50,
            show_sma150=request.show_sma150,
            show_sma200=request.show_sma200
        )

        result = await generator.generate_chart(config)

        if result.get("success"):
            chart_url = result["url"]

            # Cache the chart URL (15 min TTL)
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
            error_msg = result.get("error", "Chart generation failed")
            processing_time = time.time() - start_time
            logger.error(f"🚫 Chart generation failed for {request.ticker}: {error_msg}")

            return ChartResponse(
                success=False,
                error=error_msg,
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


@router.get("/health")
async def charts_health():
    """Health check for charts service"""
    try:
        generator = get_chart_generator()

        # Quick test with a simple chart (no annotations)
        test_config = ChartConfig(ticker="AAPL", interval="1D")
        result = await generator.generate_chart(test_config)

        status = "connected" if result.get("success") else "error"

        return {
            "status": "healthy",
            "chart_img_api": status,
            "test_result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "chart_img_api": "disconnected",
            "error": str(e)
        }
