"""
Social Sentiment API Router
Endpoints for social media sentiment tracking
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.services.social_sentiment import social_sentiment_service
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/sentiment", tags=["sentiment"])


class StandardResponse(BaseModel):
    """Standard API response"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@router.get("/{symbol}",
            response_model=StandardResponse,
            summary="Get Social Sentiment",
            description="Get social media sentiment data for a symbol")
async def get_sentiment(
    symbol: str,
    source: Optional[str] = Query(None, description="Filter by source (twitter, reddit, stocktwits)"),
    lookback_days: int = Query(7, description="Days to look back", ge=1, le=90),
    db: AsyncSession = Depends(get_db)
):
    """Get social sentiment data"""
    try:
        sentiment = await social_sentiment_service.get_sentiment(
            db=db,
            symbol=symbol,
            source=source,
            lookback_days=lookback_days
        )
        return StandardResponse(success=True, data={"sentiment": sentiment})
    except Exception as e:
        logger.error(f"Error getting sentiment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/aggregated",
            response_model=StandardResponse,
            summary="Get Aggregated Sentiment",
            description="Get aggregated sentiment across all sources")
async def get_aggregated_sentiment(
    symbol: str,
    lookback_days: int = Query(7, description="Days to look back", ge=1, le=90),
    db: AsyncSession = Depends(get_db)
):
    """Get aggregated sentiment"""
    try:
        sentiment = await social_sentiment_service.get_aggregated_sentiment(
            db=db,
            symbol=symbol,
            lookback_days=lookback_days
        )
        return StandardResponse(success=True, data=sentiment)
    except Exception as e:
        logger.error(f"Error getting aggregated sentiment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/timeline",
            response_model=StandardResponse,
            summary="Get Sentiment Timeline",
            description="Get sentiment timeline for charting")
async def get_timeline(
    symbol: str,
    source: Optional[str] = Query(None, description="Filter by source"),
    lookback_days: int = Query(30, description="Days to look back", ge=1, le=90),
    db: AsyncSession = Depends(get_db)
):
    """Get sentiment timeline"""
    try:
        timeline = await social_sentiment_service.get_sentiment_timeline(
            db=db,
            symbol=symbol,
            source=source,
            lookback_days=lookback_days
        )
        return StandardResponse(success=True, data=timeline)
    except Exception as e:
        logger.error(f"Error getting sentiment timeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compare/stocks",
            response_model=StandardResponse,
            summary="Compare Sentiment",
            description="Compare sentiment across multiple stocks")
async def compare_sentiment(
    symbols: List[str] = Query(..., description="List of symbols", min_items=2, max_items=10),
    lookback_days: int = Query(7, description="Days to look back", ge=1, le=90),
    db: AsyncSession = Depends(get_db)
):
    """Compare sentiment across stocks"""
    try:
        comparison = await social_sentiment_service.get_sentiment_comparison(
            db=db,
            symbols=symbols,
            lookback_days=lookback_days
        )
        return StandardResponse(success=True, data=comparison)
    except Exception as e:
        logger.error(f"Error comparing sentiment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trending/stocks",
            response_model=StandardResponse,
            summary="Get Trending Stocks",
            description="Get currently trending stocks on social media")
async def get_trending(
    source: Optional[str] = Query(None, description="Filter by source"),
    limit: int = Query(20, description="Number of stocks", ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Get trending stocks"""
    try:
        trending = await social_sentiment_service.get_trending_stocks(
            db=db,
            source=source,
            limit=limit
        )
        return StandardResponse(success=True, data={"trending": trending})
    except Exception as e:
        logger.error(f"Error getting trending stocks: {e}")
        raise HTTPException(status_code=500, detail=str(e))
