"""
Simulation trading API endpoints
Paper trading and strategy testing
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.services.simulation import SimulationEngine
from app.services.database import DatabaseService
from app.services.market_data import MarketDataService
from app.config import get_settings

router = APIRouter(prefix="/api/simulation", tags=["Simulation Trading"])


# Request/Response Models
class CreateAccountRequest(BaseModel):
    user_id: str = Field(..., description="User identifier")
    name: str = Field(..., description="Account name")
    initial_balance: float = Field(default=100000.0, description="Starting balance")


class EnterTradeRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")
    entry_price: float = Field(..., description="Entry price")
    position_size: int = Field(..., description="Number of shares")
    trade_type: str = Field(default="long", description="Trade type: long or short")
    stop_loss: Optional[float] = Field(None, description="Stop loss price")
    target_price: Optional[float] = Field(None, description="Target price")
    entry_date: Optional[str] = Field(None, description="Entry date (ISO format)")
    notes: Optional[str] = Field(None, description="Trade notes")


class ExitTradeRequest(BaseModel):
    exit_price: float = Field(..., description="Exit price")
    exit_date: Optional[str] = Field(None, description="Exit date (ISO format)")
    exit_reason: str = Field(default="manual", description="Exit reason")


# Dependency injection
def get_simulation_engine() -> SimulationEngine:
    settings = get_settings()
    db_service = DatabaseService(settings.database_url)
    market_data_service = MarketDataService(db_service)
    return SimulationEngine(db_service, market_data_service)


@router.post("/accounts/create")
async def create_account(
    request: CreateAccountRequest,
    engine: SimulationEngine = Depends(get_simulation_engine)
):
    """
    Create a new simulation trading account

    Start paper trading with a virtual account.
    """
    try:
        result = await engine.create_account(
            user_id=request.user_id,
            name=request.name,
            initial_balance=request.initial_balance
        )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/accounts/{account_id}")
async def get_account(
    account_id: int,
    engine: SimulationEngine = Depends(get_simulation_engine)
):
    """
    Get account details with current positions

    Returns account balance, P&L, and open positions.
    """
    try:
        result = await engine.get_account(account_id)
        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/accounts/user/{user_id}")
async def list_accounts(
    user_id: str,
    engine: SimulationEngine = Depends(get_simulation_engine)
):
    """
    List all simulation accounts for a user

    Returns all accounts with summary statistics.
    """
    try:
        result = await engine.list_accounts(user_id)
        return {"success": True, "data": result, "count": len(result)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/accounts/{account_id}/trades/enter")
async def enter_trade(
    account_id: int,
    request: EnterTradeRequest,
    engine: SimulationEngine = Depends(get_simulation_engine)
):
    """
    Enter a new simulated trade

    Opens a new position in the simulation account.
    """
    try:
        entry_date = None
        if request.entry_date:
            entry_date = datetime.fromisoformat(request.entry_date.replace('Z', '+00:00'))

        result = await engine.enter_trade(
            account_id=account_id,
            ticker_symbol=request.ticker,
            entry_price=request.entry_price,
            position_size=request.position_size,
            trade_type=request.trade_type,
            stop_loss=request.stop_loss,
            target_price=request.target_price,
            entry_date=entry_date,
            notes=request.notes
        )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/trades/{trade_id}/exit")
async def exit_trade(
    trade_id: int,
    request: ExitTradeRequest,
    engine: SimulationEngine = Depends(get_simulation_engine)
):
    """
    Exit a simulated trade

    Closes an open position and calculates P&L.
    """
    try:
        exit_date = None
        if request.exit_date:
            exit_date = datetime.fromisoformat(request.exit_date.replace('Z', '+00:00'))

        result = await engine.exit_trade(
            trade_id=trade_id,
            exit_price=request.exit_price,
            exit_date=exit_date,
            exit_reason=request.exit_reason
        )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/accounts/{account_id}/trades")
async def get_trade_history(
    account_id: int,
    status: Optional[str] = None,
    limit: int = 100,
    engine: SimulationEngine = Depends(get_simulation_engine)
):
    """
    Get trade history for an account

    Returns list of trades (open, closed, or all).
    Status options: 'open', 'closed', or None for all
    """
    try:
        result = await engine.get_trade_history(
            account_id=account_id,
            status=status,
            limit=limit
        )

        return {"success": True, "data": result, "count": len(result)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/accounts/{account_id}/statistics")
async def get_statistics(
    account_id: int,
    engine: SimulationEngine = Depends(get_simulation_engine)
):
    """
    Get comprehensive trading statistics

    Returns detailed performance metrics including win rate, profit factor,
    average R multiple, expectancy, and more.
    """
    try:
        result = await engine.get_statistics(account_id)
        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/accounts/{account_id}/equity-curve")
async def get_equity_curve(
    account_id: int,
    engine: SimulationEngine = Depends(get_simulation_engine)
):
    """
    Get equity curve data

    Returns equity progression over time with drawdown analysis.
    """
    try:
        result = await engine.calculate_equity_curve(account_id)
        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
