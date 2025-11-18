"""
Supply Chain API Router
Endpoints for supply chain analysis and risk tracking
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.services.supply_chain import supply_chain_service
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/supply-chain", tags=["supply-chain"])


class StandardResponse(BaseModel):
    """Standard API response"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@router.get("/{symbol}/relationships",
            response_model=StandardResponse,
            summary="Get Supply Chain Relationships",
            description="Get supplier, customer, and partner relationships")
async def get_relationships(
    symbol: str,
    relationship_type: Optional[str] = Query(None, description="Filter by type (supplier, customer, partner)"),
    db: AsyncSession = Depends(get_db)
):
    """Get supply chain relationships"""
    try:
        relationships = await supply_chain_service.get_relationships(
            db=db,
            symbol=symbol,
            relationship_type=relationship_type
        )
        return StandardResponse(success=True, data={"relationships": relationships})
    except Exception as e:
        logger.error(f"Error getting relationships: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/dependency-analysis",
            response_model=StandardResponse,
            summary="Analyze Dependencies",
            description="Analyze supplier and customer dependencies")
async def analyze_dependencies(
    symbol: str,
    db: AsyncSession = Depends(get_db)
):
    """Analyze dependencies"""
    try:
        analysis = await supply_chain_service.get_dependency_analysis(
            db=db,
            symbol=symbol
        )
        return StandardResponse(success=True, data=analysis)
    except Exception as e:
        logger.error(f"Error analyzing dependencies: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/risks",
            response_model=StandardResponse,
            summary="Get Supply Chain Risks",
            description="Get supply chain risk events")
async def get_risks(
    symbol: str,
    active_only: bool = Query(True, description="Only return active risks"),
    limit: int = Query(50, description="Maximum number of risks", ge=1, le=200),
    db: AsyncSession = Depends(get_db)
):
    """Get supply chain risks"""
    try:
        risks = await supply_chain_service.get_supply_chain_risks(
            db=db,
            symbol=symbol,
            active_only=active_only,
            limit=limit
        )
        return StandardResponse(success=True, data={"risks": risks})
    except Exception as e:
        logger.error(f"Error getting risks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/risk-summary",
            response_model=StandardResponse,
            summary="Get Risk Summary",
            description="Get comprehensive risk summary")
async def get_risk_summary(
    symbol: str,
    db: AsyncSession = Depends(get_db)
):
    """Get risk summary"""
    try:
        summary = await supply_chain_service.get_risk_summary(
            db=db,
            symbol=symbol
        )
        return StandardResponse(success=True, data=summary)
    except Exception as e:
        logger.error(f"Error getting risk summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}/geographic-exposure",
            response_model=StandardResponse,
            summary="Analyze Geographic Exposure",
            description="Analyze geographic exposure through supply chain")
async def get_geographic_exposure(
    symbol: str,
    db: AsyncSession = Depends(get_db)
):
    """Get geographic exposure"""
    try:
        exposure = await supply_chain_service.get_geographic_exposure(
            db=db,
            symbol=symbol
        )
        return StandardResponse(success=True, data=exposure)
    except Exception as e:
        logger.error(f"Error getting geographic exposure: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compare/stocks",
            response_model=StandardResponse,
            summary="Compare Supply Chain",
            description="Compare supply chain metrics across companies")
async def compare_supply_chain(
    symbols: List[str] = Query(..., description="List of symbols", min_items=2, max_items=10),
    db: AsyncSession = Depends(get_db)
):
    """Compare supply chain"""
    try:
        comparison = await supply_chain_service.compare_supply_chain(
            db=db,
            symbols=symbols
        )
        return StandardResponse(success=True, data=comparison)
    except Exception as e:
        logger.error(f"Error comparing supply chain: {e}")
        raise HTTPException(status_code=500, detail=str(e))
