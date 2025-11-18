"""
What-if analysis API endpoints
Explore alternative trading scenarios
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.services.whatif import WhatIfEngine
from app.services.database import DatabaseService
from app.services.market_data import MarketDataService
from app.config import get_settings

router = APIRouter(prefix="/api/whatif", tags=["What-If Analysis"])


# Request/Response Models
class AnalyzeEntryTimingRequest(BaseModel):
    user_id: str = Field(..., description="User identifier")
    ticker: str = Field(..., description="Stock ticker symbol")
    base_entry_date: str = Field(..., description="Original entry date (ISO format)")
    base_entry_price: float = Field(..., description="Original entry price")
    alternative_entry_date: str = Field(..., description="Alternative entry date (ISO format)")
    exit_date: str = Field(..., description="Exit date (ISO format)")
    position_size: int = Field(default=100, description="Number of shares")
    scenario_name: Optional[str] = Field(None, description="Scenario name")


class AnalyzeExitTimingRequest(BaseModel):
    user_id: str = Field(..., description="User identifier")
    ticker: str = Field(..., description="Stock ticker symbol")
    entry_date: str = Field(..., description="Entry date (ISO format)")
    entry_price: float = Field(..., description="Entry price")
    base_exit_date: str = Field(..., description="Original exit date (ISO format)")
    alternative_exit_date: str = Field(..., description="Alternative exit date (ISO format)")
    position_size: int = Field(default=100, description="Number of shares")
    scenario_name: Optional[str] = Field(None, description="Scenario name")


class AnalyzePositionSizeRequest(BaseModel):
    user_id: str = Field(..., description="User identifier")
    ticker: str = Field(..., description="Stock ticker symbol")
    entry_date: str = Field(..., description="Entry date (ISO format)")
    entry_price: float = Field(..., description="Entry price")
    exit_date: str = Field(..., description="Exit date (ISO format)")
    exit_price: float = Field(..., description="Exit price")
    base_position_size: int = Field(..., description="Original position size")
    alternative_position_size: int = Field(..., description="Alternative position size")
    scenario_name: Optional[str] = Field(None, description="Scenario name")


class AnalyzeStopLossRequest(BaseModel):
    user_id: str = Field(..., description="User identifier")
    ticker: str = Field(..., description="Stock ticker symbol")
    entry_date: str = Field(..., description="Entry date (ISO format)")
    entry_price: float = Field(..., description="Entry price")
    exit_date: str = Field(..., description="Observation end date (ISO format)")
    base_stop_loss: float = Field(..., description="Original stop loss price")
    alternative_stop_loss: float = Field(..., description="Alternative stop loss price")
    position_size: int = Field(default=100, description="Number of shares")
    scenario_name: Optional[str] = Field(None, description="Scenario name")


# Dependency injection
def get_whatif_engine() -> WhatIfEngine:
    settings = get_settings()
    db_service = DatabaseService(settings.database_url)
    market_data_service = MarketDataService(db_service)
    return WhatIfEngine(db_service, market_data_service)


@router.post("/entry-timing")
async def analyze_entry_timing(
    request: AnalyzeEntryTimingRequest,
    engine: WhatIfEngine = Depends(get_whatif_engine)
):
    """
    Compare different entry timings

    Answers the question: "What if I entered earlier/later?"
    Compares P&L outcomes from different entry points.
    """
    try:
        base_entry_date = datetime.fromisoformat(request.base_entry_date.replace('Z', '+00:00'))
        alt_entry_date = datetime.fromisoformat(request.alternative_entry_date.replace('Z', '+00:00'))
        exit_date = datetime.fromisoformat(request.exit_date.replace('Z', '+00:00'))

        result = await engine.analyze_entry_timing(
            user_id=request.user_id,
            ticker_symbol=request.ticker,
            base_entry_date=base_entry_date,
            base_entry_price=request.base_entry_price,
            alternative_entry_date=alt_entry_date,
            exit_date=exit_date,
            position_size=request.position_size,
            scenario_name=request.scenario_name
        )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/exit-timing")
async def analyze_exit_timing(
    request: AnalyzeExitTimingRequest,
    engine: WhatIfEngine = Depends(get_whatif_engine)
):
    """
    Compare different exit timings

    Answers the question: "What if I held longer/exited earlier?"
    Compares P&L outcomes from different exit points.
    """
    try:
        entry_date = datetime.fromisoformat(request.entry_date.replace('Z', '+00:00'))
        base_exit_date = datetime.fromisoformat(request.base_exit_date.replace('Z', '+00:00'))
        alt_exit_date = datetime.fromisoformat(request.alternative_exit_date.replace('Z', '+00:00'))

        result = await engine.analyze_exit_timing(
            user_id=request.user_id,
            ticker_symbol=request.ticker,
            entry_date=entry_date,
            entry_price=request.entry_price,
            base_exit_date=base_exit_date,
            alternative_exit_date=alt_exit_date,
            position_size=request.position_size,
            scenario_name=request.scenario_name
        )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/position-size")
async def analyze_position_size(
    request: AnalyzePositionSizeRequest,
    engine: WhatIfEngine = Depends(get_whatif_engine)
):
    """
    Compare different position sizes

    Answers the question: "What if I traded more/fewer shares?"
    Compares dollar P&L from different position sizes.
    """
    try:
        entry_date = datetime.fromisoformat(request.entry_date.replace('Z', '+00:00'))
        exit_date = datetime.fromisoformat(request.exit_date.replace('Z', '+00:00'))

        result = await engine.analyze_position_size(
            user_id=request.user_id,
            ticker_symbol=request.ticker,
            entry_date=entry_date,
            entry_price=request.entry_price,
            exit_date=exit_date,
            exit_price=request.exit_price,
            base_position_size=request.base_position_size,
            alternative_position_size=request.alternative_position_size,
            scenario_name=request.scenario_name
        )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/stop-loss")
async def analyze_stop_loss(
    request: AnalyzeStopLossRequest,
    engine: WhatIfEngine = Depends(get_whatif_engine)
):
    """
    Compare different stop loss levels

    Answers the question: "What if I used a tighter/wider stop?"
    Analyzes whether different stops would have been hit and impact on P&L.
    """
    try:
        entry_date = datetime.fromisoformat(request.entry_date.replace('Z', '+00:00'))
        exit_date = datetime.fromisoformat(request.exit_date.replace('Z', '+00:00'))

        result = await engine.analyze_stop_loss(
            user_id=request.user_id,
            ticker_symbol=request.ticker,
            entry_date=entry_date,
            entry_price=request.entry_price,
            exit_date=exit_date,
            base_stop_loss=request.base_stop_loss,
            alternative_stop_loss=request.alternative_stop_loss,
            position_size=request.position_size,
            scenario_name=request.scenario_name
        )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/scenarios/{scenario_id}")
async def get_scenario(
    scenario_id: int,
    engine: WhatIfEngine = Depends(get_whatif_engine)
):
    """
    Get a saved scenario by ID

    Returns full details of a what-if analysis scenario.
    """
    try:
        result = await engine.get_scenario(scenario_id)
        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/scenarios/user/{user_id}")
async def list_scenarios(
    user_id: str,
    scenario_type: Optional[str] = None,
    limit: int = 50,
    engine: WhatIfEngine = Depends(get_whatif_engine)
):
    """
    List scenarios for a user

    Returns all what-if scenarios, optionally filtered by type.
    Scenario types: entry_timing, exit_timing, position_size, stop_loss
    """
    try:
        result = await engine.list_scenarios(
            user_id=user_id,
            scenario_type=scenario_type,
            limit=limit
        )

        return {"success": True, "data": result, "count": len(result)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
