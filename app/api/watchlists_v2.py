"""
Professional Watchlist API v2
Multiple watchlists, smart organization, analytics, and import/export
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.services.watchlist_service import get_watchlist_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v2/watchlists", tags=["watchlists-v2"])


# ==================== Request/Response Models ====================

class CreateGroupRequest(BaseModel):
    name: str = Field(..., description="Watchlist group name")
    description: Optional[str] = Field(None, description="Group description")
    color: str = Field("#3B82F6", description="Hex color code")
    strategy: Optional[str] = Field(None, description="Trading strategy")


class UpdateGroupRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    strategy: Optional[str] = None


class AddItemRequest(BaseModel):
    ticker: str = Field(..., description="Stock symbol")
    group_id: Optional[int] = Field(None, description="Watchlist group ID")
    status: str = Field("Watching", description="Status")
    color: Optional[str] = Field(None, description="Ticker color")
    category: Optional[str] = Field(None, description="Category")
    pattern_type: Optional[str] = Field(None, description="Pattern type")
    strength_score: Optional[float] = Field(None, ge=0, le=100, description="Strength score 0-100")
    target_entry: Optional[float] = Field(None, description="Target entry price")
    target_stop: Optional[float] = Field(None, description="Stop loss price")
    target_price: Optional[float] = Field(None, description="Target price")
    reason: Optional[str] = Field(None, description="Reason for adding")
    notes: Optional[str] = Field(None, description="Additional notes")
    tags: Optional[List[str]] = Field(None, description="Tags")
    alerts_enabled: bool = Field(True, description="Enable alerts")
    alert_threshold: Optional[float] = Field(None, description="Alert threshold %")


class UpdateItemRequest(BaseModel):
    status: Optional[str] = None
    color: Optional[str] = None
    category: Optional[str] = None
    pattern_type: Optional[str] = None
    strength_score: Optional[float] = Field(None, ge=0, le=100)
    target_entry: Optional[float] = None
    target_stop: Optional[float] = None
    target_price: Optional[float] = None
    reason: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    alerts_enabled: Optional[bool] = None
    alert_threshold: Optional[float] = None
    entry_price: Optional[float] = None
    exit_price: Optional[float] = None
    profit_loss_pct: Optional[float] = None


class ReorderRequest(BaseModel):
    ids: List[int] = Field(..., description="Ordered list of IDs")


class ImportSymbolsRequest(BaseModel):
    symbols: List[str] = Field(..., description="List of ticker symbols")
    group_id: Optional[int] = Field(None, description="Target group ID")


class ImportTradingViewRequest(BaseModel):
    symbols_string: str = Field(..., description="Comma or newline separated symbols")
    group_id: Optional[int] = Field(None, description="Target group ID")


# ==================== Watchlist Group Endpoints ====================

@router.post("/groups")
async def create_watchlist_group(
    request: CreateGroupRequest,
    user_id: str = "default"
):
    """Create a new watchlist group"""
    try:
        service = get_watchlist_service()
        group = service.create_group(
            user_id=user_id,
            name=request.name,
            description=request.description,
            color=request.color,
            strategy=request.strategy
        )
        return {"success": True, "group": group}
    except Exception as e:
        logger.error(f"Error creating group: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/groups")
async def get_watchlist_groups(user_id: str = "default"):
    """Get all watchlist groups for a user"""
    try:
        service = get_watchlist_service()
        groups = service.get_groups(user_id)
        return {"success": True, "groups": groups, "total": len(groups)}
    except Exception as e:
        logger.error(f"Error getting groups: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/groups/{group_id}")
async def update_watchlist_group(
    group_id: int,
    request: UpdateGroupRequest
):
    """Update watchlist group properties"""
    try:
        service = get_watchlist_service()
        updates = {k: v for k, v in request.dict().items() if v is not None}
        group = service.update_group(group_id, **updates)
        return {"success": True, "group": group}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating group: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/groups/{group_id}")
async def delete_watchlist_group(
    group_id: int,
    move_items_to: Optional[int] = Query(None, description="Move items to this group ID")
):
    """Delete a watchlist group"""
    try:
        service = get_watchlist_service()
        success = service.delete_group(group_id, move_items_to)
        if not success:
            raise HTTPException(status_code=404, detail="Group not found")
        return {"success": True, "message": "Group deleted"}
    except Exception as e:
        logger.error(f"Error deleting group: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/groups/reorder")
async def reorder_watchlist_groups(
    request: ReorderRequest,
    user_id: str = "default"
):
    """Reorder watchlist groups (drag-and-drop)"""
    try:
        service = get_watchlist_service()
        service.reorder_groups(user_id, request.ids)
        return {"success": True, "message": "Groups reordered"}
    except Exception as e:
        logger.error(f"Error reordering groups: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Watchlist Item Endpoints ====================

@router.post("/items")
async def add_watchlist_item(
    request: AddItemRequest,
    user_id: str = "default"
):
    """Add item to watchlist"""
    try:
        service = get_watchlist_service()
        kwargs = {k: v for k, v in request.dict().items() if k != 'ticker' and k != 'group_id' and v is not None}
        item = service.add_item(
            user_id=user_id,
            symbol=request.ticker,
            group_id=request.group_id,
            **kwargs
        )
        return {"success": True, "item": item}
    except Exception as e:
        logger.error(f"Error adding item: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/items")
async def get_watchlist_items(
    user_id: str = "default",
    group_id: Optional[int] = Query(None, description="Filter by group ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    pattern_type: Optional[str] = Query(None, description="Filter by pattern"),
    category: Optional[str] = Query(None, description="Filter by category"),
    min_strength: Optional[float] = Query(None, description="Minimum strength score")
):
    """Get watchlist items with optional filtering"""
    try:
        service = get_watchlist_service()
        filters = {}
        if status:
            filters['status'] = status
        if pattern_type:
            filters['pattern_type'] = pattern_type
        if category:
            filters['category'] = category
        if min_strength is not None:
            filters['min_strength'] = min_strength

        items = service.get_items(user_id, group_id, filters if filters else None)
        return {"success": True, "items": items, "total": len(items)}
    except Exception as e:
        logger.error(f"Error getting items: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/items/{item_id}")
async def update_watchlist_item(
    item_id: int,
    request: UpdateItemRequest
):
    """Update watchlist item properties"""
    try:
        service = get_watchlist_service()
        updates = {k: v for k, v in request.dict().items() if v is not None}
        item = service.update_item(item_id, **updates)
        return {"success": True, "item": item}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating item: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/items/{item_id}")
async def delete_watchlist_item(item_id: int):
    """Remove item from watchlist"""
    try:
        service = get_watchlist_service()
        success = service.delete_item(item_id)
        if not success:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"success": True, "message": "Item removed"}
    except Exception as e:
        logger.error(f"Error deleting item: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/items/reorder")
async def reorder_watchlist_items(
    request: ReorderRequest,
    user_id: str = "default",
    group_id: Optional[int] = Query(None, description="Group ID")
):
    """Reorder items within a group (drag-and-drop)"""
    try:
        service = get_watchlist_service()
        service.reorder_items(user_id, group_id, request.ids)
        return {"success": True, "message": "Items reordered"}
    except Exception as e:
        logger.error(f"Error reordering items: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/items/{item_id}/color")
async def set_item_color(item_id: int, color: str):
    """Set color for a specific ticker"""
    try:
        service = get_watchlist_service()
        item = service.color_code_item(item_id, color)
        return {"success": True, "item": item}
    except Exception as e:
        logger.error(f"Error setting color: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Smart Organization Endpoints ====================

@router.post("/organize/auto-categorize")
async def auto_categorize_items(
    user_id: str = "default",
    group_id: Optional[int] = Query(None, description="Group ID")
):
    """Auto-categorize items by sector"""
    try:
        service = get_watchlist_service()
        count = service.auto_categorize(user_id, group_id)
        return {
            "success": True,
            "message": f"Auto-categorized {count} items",
            "items_updated": count
        }
    except Exception as e:
        logger.error(f"Error auto-categorizing: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/organize/by-pattern")
async def group_by_pattern(user_id: str = "default"):
    """Group items by pattern type"""
    try:
        service = get_watchlist_service()
        grouped = service.group_by_pattern(user_id)
        return {"success": True, "grouped": grouped}
    except Exception as e:
        logger.error(f"Error grouping by pattern: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/organize/by-strength")
async def sort_by_strength(
    user_id: str = "default",
    group_id: Optional[int] = Query(None, description="Group ID")
):
    """Get items sorted by strength score"""
    try:
        service = get_watchlist_service()
        items = service.sort_by_strength(user_id, group_id)
        return {"success": True, "items": items, "total": len(items)}
    except Exception as e:
        logger.error(f"Error sorting by strength: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Analytics Endpoints ====================

@router.get("/analytics")
async def get_watchlist_analytics(
    user_id: str = "default",
    group_id: Optional[int] = Query(None, description="Group ID for analytics")
):
    """Get comprehensive watchlist analytics"""
    try:
        service = get_watchlist_service()
        analytics = service.get_analytics(user_id, group_id)
        return {"success": True, "analytics": analytics}
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Import/Export Endpoints ====================

@router.get("/export/csv")
async def export_to_csv(
    user_id: str = "default",
    group_id: Optional[int] = Query(None, description="Group ID to export")
):
    """Export watchlist to CSV"""
    try:
        service = get_watchlist_service()
        csv_content = service.export_to_csv(user_id, group_id)
        return {
            "success": True,
            "csv": csv_content,
            "filename": f"watchlist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    except Exception as e:
        logger.error(f"Error exporting to CSV: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import/csv")
async def import_from_csv(
    csv_file: UploadFile = File(...),
    user_id: str = "default",
    group_id: Optional[int] = Query(None, description="Target group ID")
):
    """Import watchlist from CSV file"""
    try:
        csv_content = await csv_file.read()
        csv_text = csv_content.decode('utf-8')

        service = get_watchlist_service()
        result = service.import_from_csv(user_id, csv_text, group_id)
        return result
    except Exception as e:
        logger.error(f"Error importing from CSV: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import/symbols")
async def import_symbols(
    request: ImportSymbolsRequest,
    user_id: str = "default"
):
    """Import from simple list of symbols (copy/paste)"""
    try:
        service = get_watchlist_service()
        result = service.import_symbols_list(user_id, request.symbols, request.group_id)
        return result
    except Exception as e:
        logger.error(f"Error importing symbols: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export/tradingview")
async def export_to_tradingview(
    user_id: str = "default",
    group_id: Optional[int] = Query(None, description="Group ID to export")
):
    """Export to TradingView format (comma-separated symbols)"""
    try:
        service = get_watchlist_service()
        symbols_string = service.export_to_tradingview(user_id, group_id)
        return {
            "success": True,
            "symbols": symbols_string,
            "count": len(symbols_string.split(','))
        }
    except Exception as e:
        logger.error(f"Error exporting to TradingView: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import/tradingview")
async def import_from_tradingview(
    request: ImportTradingViewRequest,
    user_id: str = "default"
):
    """Import from TradingView format (comma or newline separated)"""
    try:
        service = get_watchlist_service()
        result = service.import_from_tradingview(user_id, request.symbols_string, request.group_id)
        return result
    except Exception as e:
        logger.error(f"Error importing from TradingView: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Utility Endpoints ====================

@router.get("/summary")
async def get_watchlist_summary(user_id: str = "default"):
    """Get quick summary of all watchlists"""
    try:
        service = get_watchlist_service()
        groups = service.get_groups(user_id)

        summary = []
        for group in groups:
            items = service.get_items(user_id, group['id'])
            analytics = service.get_analytics(user_id, group['id'])

            summary.append({
                "group": group,
                "item_count": len(items),
                "average_strength": analytics.get('average_strength', 0),
                "status_breakdown": analytics.get('status_breakdown', {})
            })

        # Include ungrouped items
        ungrouped_items = service.get_items(user_id, group_id=None)
        if ungrouped_items:
            ungrouped_analytics = service.get_analytics(user_id, group_id=None)
            summary.append({
                "group": {"id": None, "name": "Ungrouped", "color": "#6B7280"},
                "item_count": len(ungrouped_items),
                "average_strength": ungrouped_analytics.get('average_strength', 0),
                "status_breakdown": ungrouped_analytics.get('status_breakdown', {})
            })

        return {"success": True, "summary": summary}
    except Exception as e:
        logger.error(f"Error getting summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))
