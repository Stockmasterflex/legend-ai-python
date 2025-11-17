from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
from pathlib import Path
import logging

from app.services.cache import get_cache_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/watchlist", tags=["watchlist"])

DATA_FILE = Path("data/watchlist.json")
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
WATCHLIST_CACHE_KEY = "watchlist:items"


def _load() -> dict:
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text())
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning(f"Failed to load watchlist from {DATA_FILE}: {exc}")
            return {}
    return {}


def _save(data: dict) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2))


async def _sync_cache(items: List[Dict[str, Any]]) -> None:
    try:
        cache = get_cache_service()
        await cache.set(WATCHLIST_CACHE_KEY, items, ttl=3600)
    except (ConnectionError, TimeoutError) as exc:
        logger.debug("watchlist cache sync skipped (connection issue): %s", exc)
    except Exception as exc:
        logger.warning("watchlist cache sync failed unexpectedly: %s", exc)


async def _cache_items() -> Optional[List[Dict[str, Any]]]:
    try:
        cache = get_cache_service()
        cached = await cache.get(WATCHLIST_CACHE_KEY)
        if isinstance(cached, list):
            return cached
    except Exception:
        return None
    return None


class WatchlistItem(BaseModel):
    ticker: str
    reason: Optional[str] = None
    target_entry: Optional[float] = None
    status: str = "Watching"
    tags: Optional[str] = None


@router.post("/add")
async def add_to_watchlist(item: WatchlistItem):
    """Prefer Postgres, fallback to file store."""
    try:
        from app.services.database import get_database_service
        dbs = get_database_service()
        dbs.add_watchlist_symbol(item.ticker, item.reason, item.tags, item.status)
        all_items = dbs.get_watchlist_items()
        await _sync_cache(all_items)
        return {"success": True, "ticker": item.ticker.upper()}
    except Exception:
        db = _load()
        ticker = item.ticker.upper().strip()
        db[ticker] = {
            "ticker": ticker,
            "reason": item.reason,
            "target_entry": item.target_entry,
            "status": item.status,
            "tags": item.tags,
            "added_date": datetime.utcnow().isoformat(),
        }
        _save(db)
        await _sync_cache(list(db.values()))
        return {"success": True, "ticker": ticker}


@router.get("")
async def get_watchlist():
    try:
        from app.services.database import get_database_service
        dbs = get_database_service()
        items = dbs.get_watchlist_items()
        if items:
            await _sync_cache(items)
            return {"success": True, "items": items, "total": len(items)}
    except Exception:
        pass
    cached = await _cache_items()
    if cached is not None:
        return {"success": True, "items": cached, "total": len(cached)}
    db = _load()
    items = list(db.values())
    await _sync_cache(items)
    return {"success": True, "items": items, "total": len(items)}


@router.delete("/remove/{ticker}")
async def remove_from_watchlist(ticker: str):
    db = _load()
    t = ticker.upper().strip()
    if t in db:
        db.pop(t)
        _save(db)
        await _sync_cache(list(db.values()))
        return {"success": True, "message": f"{t} removed"}
    raise HTTPException(status_code=404, detail=f"{t} not in watchlist")
