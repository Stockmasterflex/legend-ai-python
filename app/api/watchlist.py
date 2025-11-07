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
                "target_price": item.target_price
            })
        
        logger.info(f"📊 Fetched {len(activity)} recent watchlist updates")
        
        return {
            "success": True,
            "activity": activity,
            "count": len(activity)
        }
        
    except Exception as e:
        logger.error(f"Error fetching watchlist activity: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch activity: {str(e)}")
