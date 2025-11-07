from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/watchlist", tags=["watchlist"])

DATA_FILE = Path("data/watchlist.json")
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)


def _load() -> dict:
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text())
        except Exception:
            return {}
    return {}


def _save(data: dict) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2))


class WatchlistItem(BaseModel):
    ticker: str
    reason: Optional[str] = None
    target_entry: Optional[float] = None
    status: str = "Watching"


@router.post("/add")
async def add_to_watchlist(item: WatchlistItem):
    """Prefer Postgres, fallback to file store."""
    try:
        from app.services.database import get_database_service
        dbs = get_database_service()
        dbs.add_watchlist_symbol(item.ticker, item.reason, None, item.status)
        return {"success": True, "ticker": item.ticker.upper()}
    except Exception:
        db = _load()
        ticker = item.ticker.upper().strip()
        db[ticker] = {
            "ticker": ticker,
            "reason": item.reason,
            "target_entry": item.target_entry,
            "status": item.status,
            "added_date": datetime.utcnow().isoformat(),
        }
        _save(db)
        return {"success": True, "ticker": ticker}


@router.get("")
async def get_watchlist():
    try:
        from app.services.database import get_database_service
        dbs = get_database_service()
        items = dbs.get_watchlist_items()
        if items:
            return {"success": True, "items": items, "total": len(items)}
    except Exception:
        pass
    db = _load()
    items = list(db.values())
    return {"success": True, "items": items, "total": len(items)}


@router.delete("/remove/{ticker}")
async def remove_from_watchlist(ticker: str):
    db = _load()
    t = ticker.upper().strip()
    if t in db:
        db.pop(t)
        _save(db)
        return {"success": True, "message": f"{t} removed"}
    raise HTTPException(status_code=404, detail=f"{t} not in watchlist")
