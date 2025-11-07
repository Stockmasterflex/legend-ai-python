from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/watchlist", tags=["watchlist"])


class WatchlistItem(BaseModel):
    ticker: str
    reason: Optional[str] = None
    target_entry: Optional[float] = None
    target_stop: Optional[float] = None
    target_price: Optional[float] = None
    notes: Optional[str] = None
    alerts_enabled: bool = True
    alert_threshold: Optional[float] = None


class WatchlistUpdate(BaseModel):
    status: Optional[str] = None  # "Watching", "Breaking Out", "Triggered", "Completed", "Skipped"
    notes: Optional[str] = None
    target_entry: Optional[float] = None
    target_stop: Optional[float] = None
    target_price: Optional[float] = None
    alerts_enabled: Optional[bool] = None


class WatchlistResponse(BaseModel):
    id: int
    ticker: str
    status: str
    target_entry: Optional[float]
    target_stop: Optional[float]
    target_price: Optional[float]
    reason: Optional[str]
    notes: Optional[str]
    alerts_enabled: bool
    added_at: str
    updated_at: str


@router.post("/add")
async def add_to_watchlist(item: WatchlistItem):
    """
    Add a ticker to the watchlist
    
    Stores in PostgreSQL with status tracking and alert configuration
    """
    try:
        from app.services.database import get_database_service
        
        db_service = get_database_service()
        ticker = item.ticker.upper().strip()
        
        # Get or create ticker in database
        ticker_obj = db_service.get_or_create_ticker(ticker)
        
        # Check if already in watchlist
        watchlist_item = db_service.get_watchlist_item(ticker)
        
        if watchlist_item:
            logger.warning(f"⚠️ {ticker} already in watchlist, updating instead")
            # Update existing
            db_service.update_watchlist_item(
                ticker_id=ticker_obj.id,
                data={
                    "status": "Watching",
                    "reason": item.reason,
                    "target_entry": item.target_entry,
                    "target_stop": item.target_stop,
                    "target_price": item.target_price,
                    "notes": item.notes,
                    "alerts_enabled": item.alerts_enabled,
                    "alert_threshold": item.alert_threshold
                }
            )
            return {
                "success": True,
                "ticker": ticker,
                "message": f"{ticker} updated in watchlist",
                "action": "updated"
            }
        
        # Add new item
        watchlist_item = db_service.add_to_watchlist(
            ticker_id=ticker_obj.id,
            reason=item.reason,
            target_entry=item.target_entry,
            target_stop=item.target_stop,
            target_price=item.target_price,
            notes=item.notes,
            alerts_enabled=item.alerts_enabled,
            alert_threshold=item.alert_threshold
        )
        
        logger.info(f"✅ Added {ticker} to watchlist (ID: {watchlist_item.id})")
        
        return {
            "success": True,
            "ticker": ticker,
            "watchlist_id": watchlist_item.id,
            "message": f"{ticker} added to watchlist",
            "action": "added"
        }
        
    except Exception as e:
        logger.error(f"Error adding to watchlist: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add to watchlist: {str(e)}")


@router.delete("/remove/{ticker}")
async def remove_from_watchlist(ticker: str):
    """Remove a ticker from the watchlist"""
    try:
        from app.services.database import get_database_service
        
        db_service = get_database_service()
        ticker = ticker.upper().strip()
        
        # Find and delete
        watchlist_item = db_service.get_watchlist_item(ticker)
        if not watchlist_item:
            raise HTTPException(status_code=404, detail=f"{ticker} not found in watchlist")
        
        db_service.delete_from_watchlist(ticker_id=watchlist_item.ticker_id)
        
        logger.info(f"❌ Removed {ticker} from watchlist")
        
        return {
            "success": True,
            "ticker": ticker,
            "message": f"{ticker} removed from watchlist"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing from watchlist: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to remove from watchlist: {str(e)}")


@router.get("")
async def get_watchlist(
    status: Optional[str] = Query(None, description="Filter by status: Watching, Breaking Out, Triggered, etc.")
):
    """
    Get all items from the watchlist
    
    Returns: List of watched tickers with status and metadata
    """
    try:
        from app.services.database import get_database_service
        
        db_service = get_database_service()
        
        # Fetch from database
        items = db_service.get_watchlist_items(status_filter=status)
        
        results = []
        for item in items:
            results.append({
                "id": item.id,
                "ticker": item.symbol if hasattr(item, 'symbol') else "UNKNOWN",
                "status": item.status,
                "target_entry": item.target_entry,
                "target_stop": item.target_stop,
                "target_price": item.target_price,
                "reason": item.reason,
                "notes": item.notes,
                "alerts_enabled": item.alerts_enabled,
                "added_at": item.added_at.isoformat() if item.added_at else None,
                "updated_at": item.updated_at.isoformat() if item.updated_at else None,
                "triggered_at": item.triggered_at.isoformat() if item.triggered_at else None
            })
        
        logger.info(f"📋 Fetched watchlist: {len(results)} items")
        
        return {
            "success": True,
            "items": results,
            "total": len(results),
            "filtered_by_status": status
        }
        
    except Exception as e:
        logger.error(f"Error fetching watchlist: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch watchlist: {str(e)}")


@router.get("/status/{ticker}")
async def get_ticker_status(ticker: str):
    """Get status of a specific ticker on the watchlist"""
    try:
        from app.services.database import get_database_service
        
        db_service = get_database_service()
        ticker = ticker.upper().strip()
        
        item = db_service.get_watchlist_item(ticker)
        
        if not item:
            raise HTTPException(status_code=404, detail=f"{ticker} not found in watchlist")
        
        return {
            "success": True,
            "ticker": ticker,
            "data": {
                "id": item.id,
                "status": item.status,
                "target_entry": item.target_entry,
                "target_stop": item.target_stop,
                "target_price": item.target_price,
                "reason": item.reason,
                "notes": item.notes,
                "alerts_enabled": item.alerts_enabled,
                "alert_threshold": item.alert_threshold,
                "added_at": item.added_at.isoformat() if item.added_at else None,
                "updated_at": item.updated_at.isoformat() if item.updated_at else None,
                "triggered_at": item.triggered_at.isoformat() if item.triggered_at else None
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching ticker status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch ticker status: {str(e)}")


@router.patch("/{ticker}")
async def update_watchlist_item(ticker: str, update: WatchlistUpdate):
    """
    Update a watchlist item (status, notes, targets, alerts)
    
    PATCH /api/watchlist/NVDA
    {
        "status": "Triggered",
        "notes": "Breakout confirmed with volume surge",
        "target_entry": 150.50,
        "alerts_enabled": false
    }
    """
    try:
        from app.services.database import get_database_service
        
        db_service = get_database_service()
        ticker = ticker.upper().strip()
        
        # Find item
        watchlist_item = db_service.get_watchlist_item(ticker)
        if not watchlist_item:
            raise HTTPException(status_code=404, detail=f"{ticker} not found in watchlist")
        
        # Build update dict (only include provided fields)
        update_data = {}
        if update.status is not None:
            update_data["status"] = update.status
            if update.status == "Triggered":
                update_data["triggered_at"] = datetime.utcnow()
        if update.notes is not None:
            update_data["notes"] = update.notes
        if update.target_entry is not None:
            update_data["target_entry"] = update.target_entry
        if update.target_stop is not None:
            update_data["target_stop"] = update.target_stop
        if update.target_price is not None:
            update_data["target_price"] = update.target_price
        if update.alerts_enabled is not None:
            update_data["alerts_enabled"] = update.alerts_enabled
        
        # Update database
        updated_item = db_service.update_watchlist_item(
            ticker_id=watchlist_item.ticker_id,
            data=update_data
        )
        
        logger.info(f"📝 Updated watchlist item for {ticker}: {update_data}")
        
        return {
            "success": True,
            "ticker": ticker,
            "updated_fields": list(update_data.keys()),
            "new_status": update_data.get("status", watchlist_item.status),
            "message": f"{ticker} watchlist item updated"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating watchlist item: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update watchlist item: {str(e)}")


@router.get("/activity/recent")
async def get_watchlist_activity(limit: int = Query(20, le=100)):
    """
    Get recent watchlist activity (updates, triggers)
    
    Returns: Most recent N changes to watchlist items
    """
    try:
        from app.services.database import get_database_service
        
        db_service = get_database_service()
        
        # Fetch recent updates (sorting by updated_at desc)
        items = db_service.get_watchlist_activity(limit=limit)
        
        activity = []
        for item in items:
            activity.append({
                "ticker": item.symbol if hasattr(item, 'symbol') else "UNKNOWN",
                "status": item.status,
                "triggered_at": item.triggered_at.isoformat() if item.triggered_at else None,
                "updated_at": item.updated_at.isoformat() if item.updated_at else None,
                "reason": item.reason,
                "target_entry": item.target_entry,
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
