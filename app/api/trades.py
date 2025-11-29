"""
Trade Management API endpoints
Track open/closed trades and performance statistics
"""

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.trades import get_trade_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/trades", tags=["trades"])


class CreateTradeRequest(BaseModel):
    """Create trade request"""

    ticker: str
    entry_price: float
    stop_loss: float
    target_price: float
    position_size: int
    risk_amount: float
    notes: Optional[str] = None


class CloseTradeRequest(BaseModel):
    """Close trade request"""

    trade_id: str
    exit_price: float


@router.get("/health")
async def trades_health():
    """Health check for trade management service"""
    return {
        "status": "healthy",
        "service": "trade management",
        "features": ["create", "close", "stats", "history"],
    }


@router.post("/create")
async def create_trade(request: CreateTradeRequest):
    """
    Create a new trade entry

    Args:
        request: Trade creation parameters

    Returns:
        Created trade with ID
    """
    try:
        manager = get_trade_manager()

        trade = await manager.create_trade(
            ticker=request.ticker,
            entry_price=request.entry_price,
            stop_loss=request.stop_loss,
            target_price=request.target_price,
            position_size=request.position_size,
            risk_amount=request.risk_amount,
            notes=request.notes,
        )

        rr = (
            abs(request.target_price - request.entry_price)
            / abs(request.entry_price - request.stop_loss)
            if request.entry_price != request.stop_loss
            else 0
        )

        return {
            "success": True,
            "trade": {
                "trade_id": trade.trade_id,
                "ticker": trade.ticker,
                "entry_price": f"${trade.entry_price:.2f}",
                "stop_loss": f"${trade.stop_loss:.2f}",
                "target_price": f"${trade.target_price:.2f}",
                "position_size": trade.position_size,
                "risk_reward_ratio": f"{rr:.2f}:1",
                "risk_amount": f"${trade.risk_amount:,.2f}",
                "reward_amount": f"${trade.reward_amount:,.2f}",
                "status": trade.status,
                "entry_date": trade.entry_date,
            },
        }

    except Exception as e:
        logger.error(f"Error creating trade: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/close")
async def close_trade(request: CloseTradeRequest):
    """
    Close a trade and calculate P&L

    Args:
        request: Trade ID and exit price

    Returns:
        Closed trade with P&L
    """
    try:
        manager = get_trade_manager()

        trade = await manager.close_trade(
            trade_id=request.trade_id, exit_price=request.exit_price
        )

        return {
            "success": True,
            "trade": {
                "trade_id": trade.trade_id,
                "ticker": trade.ticker,
                "entry_price": f"${trade.entry_price:.2f}",
                "exit_price": f"${trade.exit_price:.2f}",
                "position_size": trade.position_size,
                "profit_loss": f"${trade.profit_loss:,.2f}",
                "profit_loss_pct": f"{trade.profit_loss_pct:.2f}%",
                "win": "✅" if trade.win else "❌",
                "r_multiple": f"{trade.r_multiple:.2f}R",
                "status": trade.status,
                "exit_date": trade.exit_date,
            },
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error closing trade: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/open")
async def get_open_trades():
    """Get all open trades"""
    try:
        manager = get_trade_manager()
        trades = await manager.get_open_trades()

        trade_list = []
        for trade in trades:
            trade_list.append(
                {
                    "trade_id": trade.trade_id,
                    "ticker": trade.ticker,
                    "entry_price": f"${trade.entry_price:.2f}",
                    "stop_loss": f"${trade.stop_loss:.2f}",
                    "target_price": f"${trade.target_price:.2f}",
                    "position_size": trade.position_size,
                    "risk": f"${trade.risk_amount:,.2f}",
                    "reward": f"${trade.reward_amount:,.2f}",
                    "entry_date": trade.entry_date,
                }
            )

        return {"success": True, "open_trades": len(trade_list), "trades": trade_list}

    except Exception as e:
        logger.error(f"Error fetching open trades: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/closed")
async def get_closed_trades(limit: int = 20):
    """Get closed trades"""
    try:
        manager = get_trade_manager()
        trades = await manager.get_closed_trades(limit=limit)

        trade_list = []
        for trade in trades:
            trade_list.append(
                {
                    "trade_id": trade.trade_id,
                    "ticker": trade.ticker,
                    "entry_price": f"${trade.entry_price:.2f}",
                    "exit_price": f"${trade.exit_price:.2f}",
                    "profit_loss": f"${trade.profit_loss:,.2f}",
                    "profit_loss_pct": f"{trade.profit_loss_pct:.2f}%",
                    "win": "✅" if trade.win else "❌",
                    "r_multiple": f"{trade.r_multiple:.2f}R",
                    "entry_date": trade.entry_date,
                    "exit_date": trade.exit_date,
                }
            )

        return {"success": True, "closed_trades": len(trade_list), "trades": trade_list}

    except Exception as e:
        logger.error(f"Error fetching closed trades: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics")
async def get_trading_statistics():
    """Get trading performance statistics"""
    try:
        manager = get_trade_manager()
        stats = await manager.get_statistics()

        return {
            "success": True,
            "statistics": {
                "total_trades": stats.get("total_trades"),
                "winning_trades": stats.get("winning_trades"),
                "losing_trades": stats.get("losing_trades"),
                "win_rate": f"{stats.get('win_rate_pct', 0):.1f}%",
                "total_profit_loss": f"${stats.get('total_profit_loss', 0):,.2f}",
                "average_win": f"${stats.get('average_win', 0):,.2f}",
                "average_loss": f"${stats.get('average_loss', 0):,.2f}",
                "profit_factor": stats.get("profit_factor", 0),
                "average_r_multiple": f"{stats.get('average_r_multiple', 0):.2f}R",
                "expectancy_per_trade": f"${stats.get('expectancy_per_trade', 0):,.2f}",
                "expectancy_quality": stats.get("expectancy_description"),
            },
        }

    except Exception as e:
        logger.error(f"Error calculating statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))
