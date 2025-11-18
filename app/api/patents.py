"""
Patent Analysis API Router
Endpoints for patent filings and R&D tracking
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.services.patent_analysis import patent_analysis_service
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/patents", tags=["patents"])


class StandardResponse(BaseModel):
    """Standard API response"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@router.get("/{symbol}/filings",
            response_model=StandardResponse,
            summary="Get Patent Filings",
            description="Get patent filings for a company")
async def get_filings(
    symbol: str,
    limit: int = Query(50, description="Maximum number of patents", ge=1, le=200),
    technology_category: Optional[str] = Query(None, description="Filter by technology category"),
    db: AsyncSession = Depends(get_db)
):
    """Get patent filings for a symbol"""
    try:
        filings = await patent_analysis_service.get_patent_filings(
            db=db,
            symbol=symbol,
            limit=limit,
            technology_category=technology_category
        )
        return StandardResponse(success=True, data={"filings": filings})
    except Exception as e:
        logger.error(f"Error getting patent filings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/statistics",
            response_model=StandardResponse,
            summary="Get Patent Statistics",
            description="Get patent statistics and trends")
async def get_statistics(
    symbol: str,
    lookback_months: int = Query(12, description="Months to look back", ge=1, le=60),
    db: AsyncSession = Depends(get_db)
):
    """Get patent statistics for a symbol"""
    try:
        stats = await patent_analysis_service.get_patent_statistics(
            db=db,
            symbol=symbol,
            lookback_months=lookback_months
        )
        return StandardResponse(success=True, data=stats)
    except Exception as e:
        logger.error(f"Error getting patent statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/rd-spending",
            response_model=StandardResponse,
            summary="Get R&D Spending",
            description="Get R&D spending data")
async def get_rd_spending(
    symbol: str,
    limit: int = Query(8, description="Number of periods", ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    """Get R&D spending data for a symbol"""
    try:
        spending = await patent_analysis_service.get_rd_spending(
            db=db,
            symbol=symbol,
            limit=limit
        )
        return StandardResponse(success=True, data={"rd_spending": spending})
    except Exception as e:
        logger.error(f"Error getting R&D spending: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compare/innovation",
            response_model=StandardResponse,
            summary="Compare Innovation Metrics",
            description="Compare innovation metrics across companies")
async def compare_innovation(
    symbols: List[str] = Query(..., description="List of symbols", min_items=2, max_items=10),
    lookback_months: int = Query(12, description="Months to look back", ge=1, le=60),
    db: AsyncSession = Depends(get_db)
):
    """Compare innovation metrics across multiple companies"""
    try:
        comparison = await patent_analysis_service.compare_innovation_metrics(
            db=db,
            symbols=symbols,
            lookback_months=lookback_months
        )
        return StandardResponse(success=True, data=comparison)
    except Exception as e:
        logger.error(f"Error comparing innovation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends/technology",
            response_model=StandardResponse,
            summary="Get Technology Trends",
            description="Identify emerging technology trends")
async def get_tech_trends(
    industry: Optional[str] = Query(None, description="Filter by industry"),
    lookback_months: int = Query(12, description="Months to look back", ge=1, le=60),
    limit: int = Query(20, description="Number of top technologies", ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Get technology trends across industry"""
    try:
        trends = await patent_analysis_service.get_technology_trends(
            db=db,
            industry=industry,
            lookback_months=lookback_months,
            limit=limit
        )
        return StandardResponse(success=True, data=trends)
    except Exception as e:
        logger.error(f"Error getting technology trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))
