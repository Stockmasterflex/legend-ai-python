from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/watchlist", tags=["watchlist"])

watchlist_db = {}

class WatchlistItem(BaseModel):
    ticker: str
    reason: Optional[str] = None
    target_entry: Optional[float] = None
    status: str = "Watching"

class WatchlistResponse(BaseModel):
    success: bool
    items: List[dict]
    total: int

@router.post("/add")
async def add_to_watchlist(item: WatchlistItem):
    ticker = item.ticker.upper()
    watchlist_db[ticker] = {
        "ticker": ticker,
        "reason": item.reason,
        "target_entry": item.target_entry,
        "status": item.status,
        "added_date": datetime.utcnow().isoformat()
    }
    logger.info(f"✅ Added {ticker} to watchlist")
    return {"success": True, "ticker": ticker, "message": f"{ticker} added to watchlist"}

@router.delete("/remove/{ticker}")
async def remove_from_watchlist(ticker: str):
    ticker = ticker.upper()
    if ticker in watchlist_db:
        del watchlist_db[ticker]
        logger.info(f"❌ Removed {ticker} from watchlist")
        return {"success": True, "message": f"{ticker} removed from watchlist"}
    raise HTTPException(status_code=404, detail=f"{ticker} not found in watchlist")

@router.get("")
async def get_watchlist():
    items = list(watchlist_db.values())
    return WatchlistResponse(success=True, items=items, total=len(items))

@router.get("/status/{ticker}")
async def get_ticker_status(ticker: str):
    ticker = ticker.upper()
    if ticker in watchlist_db:
        return {"success": True, "ticker": ticker, "data": watchlist_db[ticker]}
    raise HTTPException(status_code=404, detail=f"{ticker} not in watchlist")

