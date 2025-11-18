"""
Competitor Analysis API Router
Endpoints for competitor tracking and peer comparison
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.services.competitor_analysis import competitor_analysis_service
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/competitors", tags=["competitors"])


class CreateGroupRequest(BaseModel):
    """Request to create a competitor group"""
    name: str = Field(..., description="Group name", example="EV Manufacturers")
    symbols: List[str] = Field(..., description="List of ticker symbols", example=["TSLA", "RIVN", "LCID"])
    industry: str = Field(..., description="Industry classification", example="Automotive")
    sector: Optional[str] = Field(None, description="Sector classification", example="Consumer Discretionary")
    description: Optional[str] = Field(None, description="Group description")


class GroupResponse(BaseModel):
    """Response for group operations"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class AnalysisResponse(BaseModel):
    """Response for analysis operations"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@router.post("/groups",
             response_model=GroupResponse,
             summary="Create Competitor Group",
             description="Create a new competitor group for tracking")
async def create_group(
    request: CreateGroupRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new competitor group

    - **name**: Descriptive name for the group
    - **symbols**: List of ticker symbols to include
    - **industry**: Industry classification
    - **sector**: Optional sector classification
    - **description**: Optional description
    """
    try:
        result = await competitor_analysis_service.create_competitor_group(
            db=db,
            name=request.name,
            symbols=request.symbols,
            industry=request.industry,
            sector=request.sector,
            description=request.description
        )

        return GroupResponse(success=True, data=result)

    except Exception as e:
        logger.error(f"Error creating competitor group: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/groups",
            response_model=GroupResponse,
            summary="List Competitor Groups",
            description="Get all competitor groups, optionally filtered by industry")
async def list_groups(
    industry: Optional[str] = Query(None, description="Filter by industry"),
    db: AsyncSession = Depends(get_db)
):
    """
    List all competitor groups

    - **industry**: Optional filter by industry
    """
    try:
        groups = await competitor_analysis_service.get_competitor_groups(
            db=db,
            industry=industry
        )

        return GroupResponse(success=True, data={"groups": groups})

    except Exception as e:
        logger.error(f"Error listing groups: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/groups/{group_id}/analysis",
            response_model=AnalysisResponse,
            summary="Analyze Competitor Group",
            description="Perform comprehensive analysis on a competitor group")
async def analyze_group(
    group_id: int,
    timeframe: str = Query("1day", description="Data timeframe (1day, 1week, etc.)"),
    lookback_days: int = Query(90, description="Days of historical data", ge=1, le=365),
    db: AsyncSession = Depends(get_db)
):
    """
    Analyze all competitors in a group

    Returns:
    - Group statistics
    - Ranked competitors
    - Performance trends
    - Leaders and laggards

    Parameters:
    - **group_id**: Competitor group ID
    - **timeframe**: Data timeframe (1day, 1week, etc.)
    - **lookback_days**: Days of historical data (1-365)
    """
    try:
        analysis = await competitor_analysis_service.analyze_competitor_group(
            db=db,
            group_id=group_id,
            timeframe=timeframe,
            lookback_days=lookback_days
        )

        return AnalysisResponse(success=True, data=analysis)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error analyzing group {group_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compare",
            response_model=AnalysisResponse,
            summary="Compare Stocks",
            description="Compare multiple stocks side-by-side")
async def compare_stocks(
    symbols: List[str] = Query(..., description="List of symbols to compare", min_items=2, max_items=10),
    timeframe: str = Query("1day", description="Data timeframe"),
    lookback_days: int = Query(90, description="Days of historical data", ge=1, le=365)
):
    """
    Compare multiple stocks side-by-side

    Returns comparative metrics including:
    - Price performance
    - Relative strength
    - Pattern scores
    - Volume trends
    - Rankings

    Parameters:
    - **symbols**: 2-10 ticker symbols to compare
    - **timeframe**: Data timeframe
    - **lookback_days**: Days of historical data
    """
    try:
        comparison = await competitor_analysis_service.compare_stocks(
            symbols=symbols,
            timeframe=timeframe,
            lookback_days=lookback_days
        )

        return AnalysisResponse(success=True, data=comparison)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error comparing stocks: {e}")
        raise HTTPException(status_code=500, detail=str(e))
