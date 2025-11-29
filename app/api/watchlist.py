from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
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
    tags: Optional[List[str]] = None

    @field_validator("ticker")
    @classmethod
    def uppercase_ticker(cls, value: str) -> str:
        ticker = (value or "").strip().upper()
        if not ticker:
            raise ValueError("ticker_required")
        return ticker

    @field_validator("tags", mode="before")
    @classmethod
    def split_tags(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            tags = [tag.strip() for tag in value.split(",") if tag.strip()]
            return tags or None
        if isinstance(value, list):
            cleaned = [str(tag).strip() for tag in value if str(tag).strip()]
            return cleaned or None
        return None


class WatchlistUpdate(BaseModel):
    reason: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[List[str]] = None

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, value):
        if value is None:
            return None
        if isinstance(value, str):
            tags = [tag.strip() for tag in value.split(",") if tag.strip()]
            return tags or None
        if isinstance(value, list):
            cleaned = [str(tag).strip() for tag in value if str(tag).strip()]
            return cleaned or None
        return None


@router.post("/add")
async def add_to_watchlist(item: WatchlistItem):
    """Prefer Postgres, fallback to file store."""
    try:
        from app.services.database import get_database_service
        dbs = get_database_service()
        tags_str = ",".join(item.tags) if item.tags else None
        dbs.add_watchlist_symbol(item.ticker, item.reason, tags_str, item.status)
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
            "tags": item.tags or [],
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
            for item in items:
                raw_tags = item.get("tags")
                if isinstance(raw_tags, str):
                    tags = [tag.strip() for tag in raw_tags.split(",") if tag.strip()]
                    item["tags"] = tags
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
    t = ticker.upper().strip()
    try:
        from app.services.database import get_database_service
        dbs = get_database_service()
        if dbs.remove_watchlist_symbol(t):
            items = dbs.get_watchlist_items()
            await _sync_cache(items)
            return {"success": True, "message": f"{t} removed"}
    except Exception:
        pass
    db = _load()
    if t in db:
        db.pop(t)
        _save(db)
        await _sync_cache(list(db.values()))
        return {"success": True, "message": f"{t} removed"}
    raise HTTPException(status_code=404, detail=f"{t} not in watchlist")


@router.put("/{ticker}")
async def update_watchlist_item(ticker: str, payload: WatchlistUpdate):
    t = ticker.upper().strip()
    updated = False
    try:
        from app.services.database import get_database_service
        dbs = get_database_service()
        tags_str = ",".join(payload.tags) if payload.tags else None
        updated = dbs.update_watchlist_symbol(
            t,
            reason=payload.reason,
            tags=tags_str,
            status=payload.status,
        )
        if updated:
            items = dbs.get_watchlist_items()
            await _sync_cache(items)
            return {"success": True}
    except Exception:
        updated = False

    db = _load()
    entry = db.get(t)
    if not entry:
        raise HTTPException(status_code=404, detail=f"{t} not in watchlist")
    if payload.reason is not None:
        entry["reason"] = payload.reason
    if payload.status is not None:
        entry["status"] = payload.status
    if payload.tags is not None:
        entry["tags"] = payload.tags
    db[t] = entry
    _save(db)
    await _sync_cache(list(db.values()))
    return {"success": True}


@router.post("/check")
async def manual_watchlist_check():
    """Manually trigger watchlist monitoring check"""
    try:
        from app.jobs.watchlist_monitor import run_watchlist_check
        from app.services.telegram_bot import get_telegram_bot
        
        logger.info("Manual watchlist check triggered")
        alerts = await run_watchlist_check()
        
        # Send Telegram alerts if any
        if alerts:
            bot = get_telegram_bot()
            for alert in alerts:
                await bot.send_alert(alert)
        
        return {
            "success": True,
            "alerts_triggered": len(alerts),
            "alerts": alerts
        }
    except Exception as e:
        logger.error(f"Manual watchlist check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Watchlist check failed: {str(e)}")
