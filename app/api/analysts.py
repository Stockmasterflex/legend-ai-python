"""
Analyst Coverage API Router
Endpoints for analyst ratings and price targets
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.services.analyst_coverage import analyst_coverage_service
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/analysts", tags=["analysts"])


class StandardResponse(BaseModel):
    """Standard API response"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@router.get("/{symbol}/ratings",
            response_model=StandardResponse,
            summary="Get Analyst Ratings",
            description="Get analyst ratings for a symbol")
async def get_ratings(
    symbol: str,
    limit: int = Query(50, description="Maximum number of ratings", ge=1, le=200),
    lookback_days: Optional[int] = Query(None, description="Days to look back"),
    db: AsyncSession = Depends(get_db)
):
    """Get analyst ratings"""
    try:
        ratings = await analyst_coverage_service.get_analyst_ratings(
            db=db,
            symbol=symbol,
            limit=limit,
            lookback_days=lookback_days
        )
        return StandardResponse(success=True, data={"ratings": ratings})
    except Exception as e:
        logger.error(f"Error getting analyst ratings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/consensus",
            response_model=StandardResponse,
            summary="Get Analyst Consensus",
            description="Get current analyst consensus")
async def get_consensus(
    symbol: str,
    db: AsyncSession = Depends(get_db)
):
    """Get analyst consensus"""
    try:
        consensus = await analyst_coverage_service.get_consensus(
            db=db,
            symbol=symbol
        )
        return StandardResponse(success=True, data=consensus)
    except Exception as e:
        logger.error(f"Error getting consensus: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/price-target",
            response_model=StandardResponse,
            summary="Analyze Price Targets",
            description="Analyze price targets vs current price")
async def analyze_price_target(
    symbol: str,
    current_price: float = Query(..., description="Current stock price"),
    db: AsyncSession = Depends(get_db)
):
    """Analyze price targets"""
    try:
        analysis = await analyst_coverage_service.get_price_target_analysis(
            db=db,
            symbol=symbol,
            current_price=current_price
        )
        return StandardResponse(success=True, data=analysis)
    except Exception as e:
        logger.error(f"Error analyzing price targets: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/changes/recent",
            response_model=StandardResponse,
            summary="Get Rating Changes",
            description="Get recent analyst rating changes")
async def get_rating_changes(
    symbol: Optional[str] = Query(None, description="Filter by symbol"),
    change_type: Optional[str] = Query(None, description="Filter by change type (Upgrade, Downgrade)"),
    lookback_days: int = Query(30, description="Days to look back", ge=1, le=365),
    limit: int = Query(50, description="Maximum number of changes", ge=1, le=200),
    db: AsyncSession = Depends(get_db)
):
    """Get analyst rating changes"""
    try:
        changes = await analyst_coverage_service.get_rating_changes(
            db=db,
            symbol=symbol,
            change_type=change_type,
            lookback_days=lookback_days,
            limit=limit
        )
        return StandardResponse(success=True, data={"changes": changes})
    except Exception as e:
        logger.error(f"Error getting rating changes: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compare/coverage",
            response_model=StandardResponse,
            summary="Compare Analyst Coverage",
            description="Compare analyst coverage across stocks")
async def compare_coverage(
    symbols: List[str] = Query(..., description="List of symbols", min_items=2, max_items=10),
    db: AsyncSession = Depends(get_db)
):
    """Compare analyst coverage"""
    try:
        comparison = await analyst_coverage_service.compare_analyst_coverage(
            db=db,
            symbols=symbols
        )
        return StandardResponse(success=True, data=comparison)
    except Exception as e:
        logger.error(f"Error comparing coverage: {e}")
        raise HTTPException(status_code=500, detail=str(e))
