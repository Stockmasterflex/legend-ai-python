"""
Real-time alerts API endpoints
Provides endpoints for monitoring patterns and sending alerts
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
import logging

from app.services.alerts import get_alert_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


class AlertConfigRequest(BaseModel):
    """Alert configuration request"""
    enable_telegram: bool = True
    enable_email: bool = True
    min_confidence: float = 0.75  # Only alert on patterns with this confidence or higher
    check_interval: int = 60  # Check every N seconds


class MonitoringRequest(BaseModel):
    """Request to start/stop monitoring"""
    action: str = "start"  # "start" or "stop"
    min_confidence: Optional[float] = None


class AlertResponse(BaseModel):
    """Response from alert operations"""
    success: bool
    message: str
    details: Optional[dict] = None


@router.get("/health")
async def alerts_health():
    """Health check for alerts service"""
    return {
        "status": "healthy",
        "service": "pattern alerts",
        "features": ["telegram", "email", "watchlist_monitoring"]
    }


@router.post("/monitor", response_model=AlertResponse)
async def start_monitoring(
    request: MonitoringRequest,
    background_tasks: BackgroundTasks
):
    """
    Start real-time monitoring of watchlist patterns

    Monitors watchlist stocks and sends alerts when patterns form.

    Args:
        request: Monitoring configuration

    Returns:
        Status of monitoring operation
    """
    try:
        alert_service = get_alert_service()

        if request.action == "start":
            # Run monitoring in background
            background_tasks.add_task(alert_service.monitor_watchlist)

            return AlertResponse(
                success=True,
                message="✅ Watchlist monitoring started",
                details={
                    "message": "Monitoring watchlist for patterns. Alerts will be sent to Telegram and Email.",
                    "min_confidence": request.min_confidence or alert_service.min_confidence_threshold,
                    "channels": ["Telegram", "Email"],
                    "check_interval": "Continuous"
                }
            )
        else:
            return AlertResponse(
                success=True,
                message="⏹️ Monitoring stopped (coming soon)",
                details={"note": "Monitoring stop functionality will be implemented soon"}
            )

    except Exception as e:
        logger.error(f"Error starting monitoring: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/check-now", response_model=AlertResponse)
async def check_patterns_now():
    """
    Manually trigger pattern check for all watchlist stocks

    Immediately scans all watchlist stocks for patterns and sends any alerts.

    Returns:
        Results of the pattern check
    """
    try:
        alert_service = get_alert_service()

        # Run monitoring
        result = await alert_service.monitor_watchlist()

        if result.get("success"):
            return AlertResponse(
                success=True,
                message=f"✅ Monitoring complete: {result.get('alerts_sent')} alerts sent",
                details=result
            )
        else:
            return AlertResponse(
                success=False,
                message=f"❌ Monitoring failed: {result.get('error')}",
                details=result
            )

    except Exception as e:
        logger.error(f"Error checking patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recent")
async def get_recent_alerts():
    """
    Get recent alerts from this session

    Returns:
        List of recent pattern alerts
    """
    try:
        # This would come from database in production
        # For now, return empty list
        return {
            "success": True,
            "alerts": [],
            "message": "No alerts sent yet. Alerts will appear here when patterns are detected."
        }

    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/config")
async def get_alert_config():
    """
    Get current alert configuration

    Returns:
        Current alert settings
    """
    try:
        alert_service = get_alert_service()

        return {
            "success": True,
            "config": {
                "min_confidence_threshold": alert_service.min_confidence_threshold,
                "telegram_enabled": bool(alert_service.telegram_api_key and alert_service.telegram_chat_id),
                "email_enabled": bool(alert_service.sendgrid_api_key and alert_service.alert_email),
                "alert_channels": ["Telegram", "Email"],
                "cooldown_period": "6 hours (prevents alert spam)"
            }
        }

    except Exception as e:
        logger.error(f"Error getting config: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test")
async def test_alert():
    """
    Send a test alert to configured channels

    Useful for testing that Telegram and Email are properly configured.

    Returns:
        Result of test alert
    """
    try:
        alert_service = get_alert_service()

        # Create test alert data
        test_alert = {
            "ticker": "AAPL",
            "pattern": "Cup & Handle (Test)",
            "confidence": 0.85,
            "entry": 178.50,
            "stop": 175.00,
            "target": 185.00,
            "risk_reward": 2.33,
            "current_price": 177.25,
            "reason": "Test alert - Pattern detection working correctly"
        }

        # Send test alert
        await alert_service._send_alerts(test_alert)

        return {
            "success": True,
            "message": "✅ Test alert sent to Telegram and Email",
            "details": {
                "telegram_sent": bool(alert_service.telegram_api_key and alert_service.telegram_chat_id),
                "email_sent": bool(alert_service.sendgrid_api_key and alert_service.alert_email),
                "test_data": test_alert
            }
        }

    except Exception as e:
        logger.error(f"Error sending test alert: {e}")
        return {
            "success": False,
            "message": f"❌ Test alert failed: {str(e)}",
            "details": {"error": str(e)}
        }
