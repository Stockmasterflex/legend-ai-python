"""
Multi-Timeframe Confirmation API endpoints
Provides multi-timeframe analysis and confluence scoring
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from app.services.multitimeframe import get_multitf_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/multitimeframe", tags=["multitimeframe"])


class MultiTFRequest(BaseModel):
    """Request for multi-timeframe analysis"""
    ticker: str


class MultiTFResponse(BaseModel):
    """Response with multi-timeframe analysis"""
    success: bool
    ticker: str
    confluence: float
    signal_quality: str
    strong_signal: bool
    details: Optional[dict] = None


@router.get("/health")
async def multitf_health():
    """Health check for multi-timeframe service"""
    return {
        "status": "healthy",
        "service": "multi-timeframe confirmation",
        "timeframes": ["1D", "1W", "4H", "1H"]
    }


@router.post("/analyze", response_model=MultiTFResponse)
async def analyze_multi_timeframe(request: MultiTFRequest):
    """
    Analyze a stock across multiple timeframes for confluence

    Analyzes 1D, 1W, 4H, and 1H timeframes and scores alignment.
    Higher confluence = stronger signal across all timeframes.

    Args:
        request: Ticker to analyze

    Returns:
        Multi-timeframe analysis with confluence score

    Example:
        POST /api/multitimeframe/analyze
        {
            "ticker": "NVDA"
        }

        Response:
        {
            "success": true,
            "ticker": "NVDA",
            "confluence": 0.82,
            "signal_quality": "Good",
            "strong_signal": true,
            "details": {
                "daily_1d": {...},
                "weekly_1w": {...},
                "four_hour_4h": {...},
                "one_hour_1h": {...},
                "recommendations": [...]
            }
        }
    """
    try:
        ticker = request.ticker.upper().strip()

        if not ticker:
            raise HTTPException(status_code=400, detail="Ticker is required")

        service = get_multitf_service()

        # Run multi-timeframe analysis
        result = await service.analyze_multi_timeframe(ticker)

        # Format response
        return MultiTFResponse(
            success=True,
            ticker=ticker,
            confluence=result.overall_confluence,
            signal_quality=result.signal_quality,
            strong_signal=result.strong_signal,
            details={
                "confluence_score": f"{result.overall_confluence:.1%}",
                "signal_quality": result.signal_quality,
                "strong_signal": result.strong_signal,
                "timeframes": {
                    "1D": {
                        "pattern": result.daily_1d.pattern_type or "None",
                        "confidence": f"{result.daily_1d.confidence:.1%}",
                        "trend": result.daily_1d.trend_direction,
                        "entry": result.daily_1d.entry,
                        "stop": result.daily_1d.stop,
                        "target": result.daily_1d.target
                    },
                    "1W": {
                        "trend": result.weekly_1w.trend_direction,
                        "confidence": f"{result.weekly_1w.confidence:.1%}",
                        "volume_trend": result.weekly_1w.volume_trend
                    },
                    "4H": {
                        "trend": result.four_hour_4h.trend_direction,
                        "confidence": f"{result.four_hour_4h.confidence:.1%}",
                        "volume_trend": result.four_hour_4h.volume_trend
                    },
                    "1H": {
                        "trend": result.one_hour_1h.trend_direction,
                        "confidence": f"{result.one_hour_1h.confidence:.1%}"
                    }
                },
                "alignment": result.alignment_details,
                "recommendations": result.recommendations
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in multi-timeframe analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/quick/{ticker}")
async def quick_multitf_check(ticker: str):
    """
    Quick multi-timeframe check for a ticker

    Shorthand endpoint for quick analysis without JSON body.

    Args:
        ticker: Stock symbol

    Returns:
        Quick confluence check
    """
    try:
        service = get_multitf_service()
        result = await service.analyze_multi_timeframe(ticker)

        return {
            "success": True,
            "ticker": ticker,
            "confluence": f"{result.overall_confluence:.1%}",
            "signal_quality": result.signal_quality,
            "strong_signal": result.strong_signal,
            "recommendation": result.recommendations[0] if result.recommendations else "Analysis complete"
        }

    except Exception as e:
        logger.error(f"Quick check error: {e}")
        return {
            "success": False,
            "error": str(e)
        }
