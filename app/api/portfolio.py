from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.services.database import get_db
from app.services.portfolio_service import PortfolioService

router = APIRouter(prefix="/api/portfolio", tags=["Portfolio"])


# --- Request Models ---
class CreatePortfolioRequest(BaseModel):
    name: str
    initial_capital: float
    user_id: int = 1  # Default user for single-user mode


class AddPositionRequest(BaseModel):
    portfolio_id: int
    symbol: str
    quantity: float
    entry_price: float
    stop_loss: Optional[float] = None
    target_price: Optional[float] = None
    notes: Optional[str] = None


class RemovePositionRequest(BaseModel):
    position_id: int
    quantity: Optional[float] = None
    exit_price: Optional[float] = None


# --- Endpoints ---


@router.post("/create", summary="Create a new portfolio")
async def create_portfolio(
    request: CreatePortfolioRequest, db: Session = Depends(get_db)
):
    """Create a new portfolio"""
    service = PortfolioService(db)
    portfolio = await service.create_portfolio(
        user_id=request.user_id,
        name=request.name,
        initial_capital=request.initial_capital,
    )
    return {"success": True, "portfolio_id": portfolio.id}


@router.get("/list", summary="List all portfolios")
async def list_portfolios(user_id: int = 1, db: Session = Depends(get_db)):
    """List all portfolios for a user"""
    service = PortfolioService(db)
    portfolios = await service.get_user_portfolios(user_id)

    return {
        "success": True,
        "portfolios": [
            {
                "id": p.id,
                "user_id": p.user_id,
                "name": p.name,
                "initial_capital": p.initial_capital,
                "cash_balance": p.cash_balance,
                "total_value": p.total_value,
                "created_at": p.created_at.isoformat() if p.created_at else None,
            }
            for p in portfolios
        ],
    }


@router.get("/{portfolio_id}", summary="Get portfolio details")
async def get_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    """
    Get detailed portfolio information

    Parameters:
    - **portfolio_id**: Portfolio ID

    Returns portfolio with current metrics
    """
    service = PortfolioService(db)
    portfolio = await service.get_portfolio(portfolio_id)

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    # Get comprehensive metrics
    metrics = await service.calculate_portfolio_metrics(portfolio_id)

    return {
        "success": True,
        "portfolio": {
            "id": portfolio.id,
            "user_id": portfolio.user_id,
            "name": portfolio.name,
            "initial_capital": portfolio.initial_capital,
            "cash_balance": portfolio.cash_balance,
            "total_value": portfolio.total_value,
            "created_at": (
                portfolio.created_at.isoformat() if portfolio.created_at else None
            ),
        },
        "metrics": metrics,
    }


@router.post("/position/add", summary="Add a new position")
async def add_position(request: AddPositionRequest, db: Session = Depends(get_db)):
    """
    Add a new position or add to existing position

    Parameters:
    - **portfolio_id**: Portfolio ID
    - **symbol**: Stock symbol
    - **quantity**: Number of shares
    - **entry_price**: Entry price per share
    - **stop_loss**: Optional stop loss price
    - **target_price**: Optional target price
    - **notes**: Optional position notes

    Returns the created/updated position
    """
    service = PortfolioService(db)

    try:
        position = await service.add_position(
            portfolio_id=request.portfolio_id,
            symbol=request.symbol,
            quantity=request.quantity,
            entry_price=request.entry_price,
            stop_loss=request.stop_loss,
            target_price=request.target_price,
            notes=request.notes,
        )

        return {
            "success": True,
            "position": {
                "id": position.id,
                "symbol": request.symbol,
                "quantity": position.quantity,
                "avg_cost_basis": position.avg_cost_basis,
                "total_cost": position.total_cost,
                "current_price": position.current_price,
                "current_value": position.current_value,
                "unrealized_pnl": position.unrealized_pnl,
                "unrealized_pnl_pct": position.unrealized_pnl_pct,
                "stop_loss": position.stop_loss,
                "target_price": position.target_price,
                "status": position.status,
                "opened_at": (
                    position.opened_at.isoformat() if position.opened_at else None
                ),
            },
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/position/remove", summary="Remove or reduce a position")
async def remove_position(
    request: RemovePositionRequest, db: Session = Depends(get_db)
):
    """
    Remove a position (full or partial exit)

    Parameters:
    - **position_id**: Position ID to close
    - **quantity**: Shares to sell (None = full position)
    - **exit_price**: Exit price (None = current market price)

    Returns the updated position and realized P&L
    """
    service = PortfolioService(db)

    try:
        position, realized_pnl = await service.remove_position(
            position_id=request.position_id,
            quantity=request.quantity,
            exit_price=request.exit_price,
        )

        return {
            "success": True,
            "position": {
                "id": position.id,
                "quantity": position.quantity,
                "status": position.status,
                "closed_at": (
                    position.closed_at.isoformat() if position.closed_at else None
                ),
            },
            "realized_pnl": realized_pnl,
            "message": f"Position {'closed' if position.status == 'closed' else 'reduced'}",
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{portfolio_id}/positions", summary="Get portfolio positions")
async def get_positions(
    portfolio_id: int,
    status: str = Query(
        default="open", description="Position status (open/closed/partial)"
    ),
    db: Session = Depends(get_db),
):
    """
    Get all positions for a portfolio

    Parameters:
    - **portfolio_id**: Portfolio ID
    - **status**: Filter by status (open/closed/partial)

    Returns list of positions
    """
    service = PortfolioService(db)
    positions = await service.get_portfolio_positions(portfolio_id, status)

    # Get ticker symbols
    from app.models import Ticker

    result = []
    for position in positions:
        ticker = db.query(Ticker).filter(Ticker.id == position.ticker_id).first()
        result.append(
            {
                "id": position.id,
                "symbol": ticker.symbol if ticker else "Unknown",
                "quantity": position.quantity,
                "avg_cost_basis": position.avg_cost_basis,
                "current_price": position.current_price,
                "total_cost": position.total_cost,
                "current_value": position.current_value,
                "unrealized_pnl": position.unrealized_pnl,
                "unrealized_pnl_pct": position.unrealized_pnl_pct,
                "stop_loss": position.stop_loss,
                "target_price": position.target_price,
                "position_size_pct": position.position_size_pct,
                "status": position.status,
                "opened_at": (
                    position.opened_at.isoformat() if position.opened_at else None
                ),
                "notes": position.notes,
            }
        )

    return {"success": True, "positions": result, "count": len(result)}


@router.post("/{portfolio_id}/update-prices", summary="Update all position prices")
async def update_positions(portfolio_id: int, db: Session = Depends(get_db)):
    """
    Update all positions with current market prices

    Parameters:
    - **portfolio_id**: Portfolio ID

    Returns updated positions
    """
    service = PortfolioService(db)
    positions = await service.update_all_positions(portfolio_id)

    return {
        "success": True,
        "message": f"Updated {len(positions)} positions",
        "updated_count": len(positions),
    }


@router.get("/{portfolio_id}/metrics", summary="Get portfolio metrics")
async def get_metrics(portfolio_id: int, db: Session = Depends(get_db)):
    """
    Get comprehensive portfolio metrics

    Parameters:
    - **portfolio_id**: Portfolio ID

    Returns:
    - Total value, P&L, allocations, etc.
    """
    service = PortfolioService(db)

    try:
        metrics = await service.calculate_portfolio_metrics(portfolio_id)
        return {"success": True, "metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{portfolio_id}/allocation", summary="Get allocation data for pie chart")
async def get_allocation(portfolio_id: int, db: Session = Depends(get_db)):
    """
    Get portfolio allocation data for visualization

    Parameters:
    - **portfolio_id**: Portfolio ID

    Returns allocation data formatted for pie charts
    """
    service = PortfolioService(db)

    try:
        allocation_data = await service.get_allocation_data(portfolio_id)
        return {"success": True, "allocation": allocation_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
