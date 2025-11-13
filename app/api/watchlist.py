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
STORE_VERSION = 2


def _load() -> dict:
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text())
        except Exception:
            return {"version": STORE_VERSION, "users": {}}
    else:
        data = {}

    if not isinstance(data, dict):
        return {"version": STORE_VERSION, "users": {}}

    # Legacy format: {"AAPL": {...}}
    if "users" not in data:
        legacy_items = {}
        for ticker, payload in data.items():
            if isinstance(payload, dict):
                legacy_items[ticker] = payload
        return {"version": STORE_VERSION, "users": {"default": legacy_items}}

    users = data.get("users")
    if not isinstance(users, dict):
        users = {}

    return {"version": STORE_VERSION, "users": users}


def _save(data: dict) -> None:
    payload = {"version": STORE_VERSION, "users": data.get("users", {})}
    DATA_FILE.write_text(json.dumps(payload, indent=2))


def _get_user_bucket(data: dict, user_id: str) -> dict:
    users = data.setdefault("users", {})
    bucket = users.setdefault(user_id, {})
    return bucket


class WatchlistItem(BaseModel):
    ticker: str
    reason: Optional[str] = None
    tags: Optional[str] = None
    target_entry: Optional[float] = None
    status: str = "Watching"
    user_id: str = "default"


@router.post("/add")
async def add_to_watchlist(item: WatchlistItem):
    """Prefer Postgres, fallback to file store."""
    try:
        from app.services.database import get_database_service
        dbs = get_database_service()
        inserted = dbs.add_watchlist_symbol(
            item.ticker,
            item.reason,
            item.tags,
            item.status,
            item.user_id,
        )
        if inserted:
            return {"success": True, "ticker": item.ticker.upper()}
    except Exception:
        pass

    db = _load()
    ticker = item.ticker.upper().strip()
    user_bucket = _get_user_bucket(db, item.user_id)
    timestamp = datetime.utcnow().isoformat()
    user_bucket[ticker] = {
        "ticker": ticker,
        "reason": item.reason,
        "tags": item.tags,
        "target_entry": item.target_entry,
        "status": item.status,
        "added_date": timestamp,
        "added_at": timestamp,
    }
    _save(db)
    return {"success": True, "ticker": ticker}


@router.get("")
async def get_watchlist(user_id: str = "default"):
    try:
        from app.services.database import get_database_service
        dbs = get_database_service()
        items = dbs.get_watchlist_items(user_id=user_id)
        if items:
            return {"success": True, "items": items, "total": len(items)}
    except Exception:
        pass
    db = _load()
    user_bucket = _get_user_bucket(db, user_id)
    sorted_items = sorted(
        user_bucket.values(),
        key=lambda x: x.get("added_at") or x.get("added_date", ""),
        reverse=True,
    )
    normalized = []
    for entry in sorted_items:
        normalized.append({
            **entry,
            "added_at": entry.get("added_at") or entry.get("added_date"),
        })
    return {"success": True, "items": normalized, "total": len(normalized)}


@router.delete("/remove/{ticker}")
async def remove_from_watchlist(ticker: str, user_id: str = "default"):
    t = ticker.upper().strip()
    try:
        from app.services.database import get_database_service
        dbs = get_database_service()
        removed = dbs.remove_watchlist_symbol(t, user_id=user_id)
        if removed:
            return {"success": True, "message": f"{t} removed"}
    except Exception:
        pass

    db = _load()
    user_bucket = _get_user_bucket(db, user_id)
    if t in user_bucket:
        user_bucket.pop(t)
        _save(db)
        return {"success": True, "message": f"{t} removed"}
    raise HTTPException(status_code=404, detail=f"{t} not in watchlist")
