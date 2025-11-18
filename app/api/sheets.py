"""
Google Sheets API Router
Endpoints for bidirectional synchronization with Google Sheets
"""

import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field

from app.services.google_sheets import get_sheets_service
from app.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/sheets", tags=["Google Sheets"])

settings = get_settings()


# ==========================================
# REQUEST MODELS
# ==========================================

class SyncRequest(BaseModel):
    """Request to sync data with Google Sheets"""
    sheet_id: Optional[str] = Field(None, description="Google Sheet ID (uses default if not provided)")
    direction: str = Field("to_sheet", description="Sync direction: 'to_sheet', 'from_sheet', or 'bidirectional'")


class PatternExportRequest(BaseModel):
    """Request to export pattern results"""
    sheet_id: Optional[str] = None
    days: int = Field(7, description="Number of days of pattern history to export")


class DashboardRequest(BaseModel):
    """Request to create/update dashboard"""
    sheet_id: Optional[str] = None


# ==========================================
# WATCHLIST ENDPOINTS
# ==========================================

@router.post("/watchlist/sync")
async def sync_watchlist(request: SyncRequest, background_tasks: BackgroundTasks):
    """
    Sync watchlist with Google Sheets

    Supports:
    - to_sheet: Export watchlist to Google Sheet
    - from_sheet: Import watchlist from Google Sheet
    - bidirectional: Two-way sync
    """
    try:
        sheets_service = get_sheets_service()

        if not settings.google_sheets_enabled:
            raise HTTPException(status_code=400, detail="Google Sheets integration is not enabled")

        await sheets_service.initialize()

        if request.direction in ["to_sheet", "bidirectional"]:
            result = await sheets_service.sync_watchlist_to_sheet(request.sheet_id)
            if result["status"] == "error":
                raise HTTPException(status_code=500, detail=result["error"])

        if request.direction in ["from_sheet", "bidirectional"]:
            result = await sheets_service.sync_watchlist_from_sheet(request.sheet_id)
            if result["status"] == "error":
                raise HTTPException(status_code=500, detail=result["error"])

        return {
            "status": "success",
            "message": f"Watchlist synced ({request.direction})",
            "direction": request.direction,
            "sheet_id": request.sheet_id or settings.google_sheets_watchlist_id
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to sync watchlist: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/watchlist/export")
async def export_watchlist(sheet_id: Optional[str] = None):
    """Export watchlist to Google Sheet (one-way)"""
    try:
        sheets_service = get_sheets_service()
        await sheets_service.initialize()

        result = await sheets_service.sync_watchlist_to_sheet(sheet_id)

        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to export watchlist: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/watchlist/import")
async def import_watchlist(sheet_id: Optional[str] = None):
    """Import watchlist from Google Sheet (one-way)"""
    try:
        sheets_service = get_sheets_service()
        await sheets_service.initialize()

        result = await sheets_service.sync_watchlist_from_sheet(sheet_id)

        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to import watchlist: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# PATTERN RESULTS ENDPOINTS
# ==========================================

@router.post("/patterns/export")
async def export_patterns(request: PatternExportRequest):
    """
    Export pattern scan results to Google Sheet

    Includes:
    - Recent pattern detections
    - Scores and entry/exit points
    - Chart URLs
    - Performance metrics
    """
    try:
        sheets_service = get_sheets_service()
        await sheets_service.initialize()

        result = await sheets_service.export_pattern_results(request.sheet_id, request.days)

        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to export patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# TRADE JOURNAL ENDPOINTS
# ==========================================

@router.post("/trades/export")
async def export_trades(sheet_id: Optional[str] = None):
    """
    Export trade journal to Google Sheet

    Includes:
    - All trades (open and closed)
    - P&L calculations
    - Performance statistics
    - Win rate and R-multiples
    """
    try:
        sheets_service = get_sheets_service()
        await sheets_service.initialize()

        result = await sheets_service.sync_trades_to_sheet(sheet_id)

        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to export trades: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# PORTFOLIO ENDPOINTS
# ==========================================

@router.post("/portfolio/export")
async def export_portfolio(sheet_id: Optional[str] = None):
    """
    Export portfolio holdings to Google Sheet

    Includes:
    - Current positions
    - P&L calculations
    - Risk metrics
    - Position sizing
    """
    try:
        sheets_service = get_sheets_service()
        await sheets_service.initialize()

        result = await sheets_service.sync_portfolio_to_sheet(sheet_id)

        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to export portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/portfolio/import")
async def import_portfolio(sheet_id: Optional[str] = None):
    """
    Import portfolio holdings from Google Sheet

    Allows manual entry of positions in Google Sheets
    and syncs them back to the database
    """
    try:
        sheets_service = get_sheets_service()
        await sheets_service.initialize()

        result = await sheets_service.import_portfolio_from_sheet(sheet_id)

        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to import portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/portfolio/sync")
async def sync_portfolio(request: SyncRequest):
    """
    Bidirectional portfolio sync

    Syncs portfolio data in both directions:
    - Export current holdings to Sheet
    - Import any manual updates from Sheet
    """
    try:
        sheets_service = get_sheets_service()
        await sheets_service.initialize()

        if request.direction in ["to_sheet", "bidirectional"]:
            result = await sheets_service.sync_portfolio_to_sheet(request.sheet_id)
            if result["status"] == "error":
                raise HTTPException(status_code=500, detail=result["error"])

        if request.direction in ["from_sheet", "bidirectional"]:
            result = await sheets_service.import_portfolio_from_sheet(request.sheet_id)
            if result["status"] == "error":
                raise HTTPException(status_code=500, detail=result["error"])

        return {
            "status": "success",
            "message": f"Portfolio synced ({request.direction})",
            "direction": request.direction,
            "sheet_id": request.sheet_id or settings.google_sheets_portfolio_id
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to sync portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# DASHBOARD ENDPOINTS
# ==========================================

@router.post("/dashboard/create")
async def create_dashboard(request: DashboardRequest):
    """
    Create custom trading dashboard in Google Sheets

    Creates multiple worksheets with:
    - Overview with key metrics
    - Top pattern detections
    - Active trades
    - Performance statistics

    Includes formulas for real-time calculations
    """
    try:
        sheets_service = get_sheets_service()
        await sheets_service.initialize()

        result = await sheets_service.create_dashboard(request.sheet_id)

        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["error"])

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/dashboard/refresh")
async def refresh_dashboard(sheet_id: Optional[str] = None):
    """
    Refresh dashboard with latest data

    Updates all dashboard worksheets with current data
    """
    try:
        sheets_service = get_sheets_service()
        await sheets_service.initialize()

        result = await sheets_service.create_dashboard(sheet_id)

        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["error"])

        return {
            "status": "success",
            "message": "Dashboard refreshed",
            "sheet_id": sheet_id or settings.google_sheets_dashboard_id
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to refresh dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# SYNC ALL ENDPOINT
# ==========================================

@router.post("/sync-all")
async def sync_all(background_tasks: BackgroundTasks):
    """
    Sync all data to Google Sheets

    Exports:
    - Watchlist
    - Pattern results (last 7 days)
    - Trade journal
    - Portfolio holdings
    - Dashboard

    Runs as background task for non-blocking operation
    """
    try:
        sheets_service = get_sheets_service()

        if not settings.google_sheets_enabled:
            raise HTTPException(status_code=400, detail="Google Sheets integration is not enabled")

        # Run sync in background
        background_tasks.add_task(_sync_all_background, sheets_service)

        return {
            "status": "queued",
            "message": "Full sync started in background",
            "note": "Check /api/sheets/status for sync progress"
        }

    except Exception as e:
        logger.error(f"Failed to queue sync: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def _sync_all_background(sheets_service):
    """Background task to sync all sheets"""
    try:
        await sheets_service.initialize()

        # Sync watchlist
        if settings.google_sheets_watchlist_id:
            await sheets_service.sync_watchlist_to_sheet()
            logger.info("✅ Background sync: Watchlist complete")

        # Export patterns
        if settings.google_sheets_patterns_id:
            await sheets_service.export_pattern_results(days=7)
            logger.info("✅ Background sync: Patterns complete")

        # Export trades
        if settings.google_sheets_trades_id:
            await sheets_service.sync_trades_to_sheet()
            logger.info("✅ Background sync: Trades complete")

        # Export portfolio
        if settings.google_sheets_portfolio_id:
            await sheets_service.sync_portfolio_to_sheet()
            logger.info("✅ Background sync: Portfolio complete")

        # Refresh dashboard
        if settings.google_sheets_dashboard_id:
            await sheets_service.create_dashboard()
            logger.info("✅ Background sync: Dashboard complete")

        logger.info("✅ Full background sync completed")

    except Exception as e:
        logger.error(f"❌ Background sync failed: {e}")


# ==========================================
# STATUS ENDPOINT
# ==========================================

@router.get("/status")
async def get_sync_status():
    """
    Get status of all Google Sheets syncs

    Returns:
    - Last sync time for each sheet type
    - Number of records synced
    - Sync status and any errors
    """
    try:
        sheets_service = get_sheets_service()

        if not settings.google_sheets_enabled:
            return {
                "enabled": False,
                "message": "Google Sheets integration is disabled"
            }

        status = await sheets_service.get_sync_status()

        return {
            "enabled": True,
            "syncs": status,
            "configuration": {
                "watchlist_id": settings.google_sheets_watchlist_id,
                "patterns_id": settings.google_sheets_patterns_id,
                "trades_id": settings.google_sheets_trades_id,
                "portfolio_id": settings.google_sheets_portfolio_id,
                "dashboard_id": settings.google_sheets_dashboard_id,
                "sync_interval": settings.google_sheets_sync_interval
            }
        }

    except Exception as e:
        logger.error(f"Failed to get sync status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# HEALTH CHECK
# ==========================================

@router.get("/health")
async def health_check():
    """Check Google Sheets integration health"""
    try:
        sheets_service = get_sheets_service()

        if not settings.google_sheets_enabled:
            return {
                "status": "disabled",
                "message": "Google Sheets integration is disabled in settings"
            }

        # Try to initialize
        initialized = await sheets_service.initialize()

        if initialized:
            return {
                "status": "healthy",
                "message": "Google Sheets integration is working",
                "configured_sheets": {
                    "watchlist": bool(settings.google_sheets_watchlist_id),
                    "patterns": bool(settings.google_sheets_patterns_id),
                    "trades": bool(settings.google_sheets_trades_id),
                    "portfolio": bool(settings.google_sheets_portfolio_id),
                    "dashboard": bool(settings.google_sheets_dashboard_id)
                }
            }
        else:
            return {
                "status": "unhealthy",
                "message": "Failed to initialize Google Sheets service"
            }

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
