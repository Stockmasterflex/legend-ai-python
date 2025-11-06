from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/analytics", tags=["analytics"])

trade_journal = []

class Trade(BaseModel):
    ticker: str
    entry: float
    exit: float
    shares: int
    pnl: float
    r_multiple: float
    date: str = datetime.utcnow().isoformat()

@router.post("/trade")
async def log_trade(trade: Trade):
    trade_journal.append(trade.dict())
    logger.info(f"📊 Trade logged: {trade.ticker} - ${trade.pnl:.2f} ({trade.r_multiple}R)")
    return {"success": True, "message": "Trade logged"}

@router.get("/performance")
async def get_performance():
    if not trade_journal:
        return {"total_trades": 0, "win_rate": 0, "avg_rr": 0, "total_pnl": 0}
    
    wins = [t for t in trade_journal if t["pnl"] > 0]
    total_pnl = sum(t["pnl"] for t in trade_journal)
    avg_rr = sum(t["r_multiple"] for t in trade_journal) / len(trade_journal)
    
    return {
        "total_trades": len(trade_journal),
        "wins": len(wins),
        "losses": len(trade_journal) - len(wins),
        "win_rate": round(len(wins) / len(trade_journal) * 100, 1),
        "avg_rr": round(avg_rr, 2),
        "total_pnl": round(total_pnl, 2),
        "best_trade": max((t["pnl"] for t in trade_journal), default=0),
        "worst_trade": min((t["pnl"] for t in trade_journal), default=0)
    }

@router.get("/journal")
async def get_journal():
    return {"trades": trade_journal[-20:], "total": len(trade_journal)}

