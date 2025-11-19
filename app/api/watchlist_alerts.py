"""
Watchlist Alerts API Endpoints
Configure and manage real-time watchlist alerts
"""

from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from typing import Optional
from pydantic import BaseModel

from app.services.watchlist_alerts import WatchlistAlertsService


router = APIRouter()
alerts_service = WatchlistAlertsService()


class AlertPreferencesRequest(BaseModel):
    """Request to update alert preferences"""
    ticker_symbol: str
    alert_on_pattern: bool = True
    alert_on_price_target: bool = True
    alert_on_stop_loss: bool = True
    alert_frequency: str = "once"  # 'once', 'hourly', 'daily', 'always', 'disabled'


class MuteAlertsRequest(BaseModel):
    """Request to mute alerts"""
    ticker_symbol: str
    duration_hours: Optional[int] = None  # None = permanent until unmuted


@router.get("/history")
async def get_alert_history(
    user_id: str = Query("default", description="User ID"),
    limit: int = Query(50, ge=1, le=200),
    days: int = Query(30, ge=1, le=180)
):
    """
    Get alert history for a user

    Shows all alerts sent in the specified time period
    """
    try:
        history = await alerts_service.get_alert_history(
            user_id=user_id,
            limit=limit,
            days=days
        )

        return {
            "success": True,
            "data": history,
            "count": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mute")
async def mute_ticker_alerts(request: MuteAlertsRequest, user_id: str = Query("default")):
    """
    Mute alerts for a specific ticker

    Can be temporary (with duration) or permanent (until unmuted)
    """
    try:
        await alerts_service.mute_ticker_alerts(
            user_id=user_id,
            ticker_symbol=request.ticker_symbol,
            duration_hours=request.duration_hours
        )

        message = f"Alerts muted for {request.ticker_symbol}"
        if request.duration_hours:
            message += f" for {request.duration_hours} hours"

        return {
            "success": True,
            "message": message
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/unmute")
async def unmute_ticker_alerts(ticker_symbol: str, user_id: str = Query("default")):
    """
    Unmute alerts for a specific ticker

    Re-enables alerts that were previously muted
    """
    try:
        await alerts_service.unmute_ticker_alerts(
            user_id=user_id,
            ticker_symbol=ticker_symbol
        )

        return {
            "success": True,
            "message": f"Alerts unmuted for {ticker_symbol}"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/check-now")
async def check_watchlist_now(background_tasks: BackgroundTasks):
    """
    Manually trigger a watchlist check

    Useful for testing or immediate checks
    """
    try:
        background_tasks.add_task(alerts_service.check_watchlist)

        return {
            "success": True,
            "message": "Watchlist check triggered"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_monitoring_status():
    """
    Get monitoring service status

    Shows if the watchlist monitoring is running
    """
    return {
        "success": True,
        "is_running": alerts_service.is_running,
        "message": "Monitoring active" if alerts_service.is_running else "Monitoring stopped"
    }
