"""
Security API Endpoints
Monitoring, alerting, and security management
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional, List, Dict
from datetime import datetime
import logging

from app.security import (
    security_monitor,
    api_key_manager,
    secrets_manager,
    InputValidator
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/security", tags=["security"])


async def verify_admin_access(x_admin_key: Optional[str] = Header(None)):
    """
    Verify admin access for security endpoints.
    In production, this should check against a secure admin key.
    """
    # TODO: Implement proper admin authentication
    # For now, this is a placeholder
    if not x_admin_key:
        raise HTTPException(
            status_code=401,
            detail="Admin authentication required"
        )
    return True


@router.get("/health")
async def security_health():
    """
    Get security system health status.
    Public endpoint for basic security health check.
    """
    return {
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "ddos_protection": "active",
            "security_headers": "active",
            "input_validation": "active",
            "monitoring": "active"
        }
    }


@router.get("/summary")
async def get_security_summary(
    hours: int = 24,
    _: bool = Depends(verify_admin_access)
):
    """
    Get security summary for the last N hours.
    Requires admin authentication.

    Args:
        hours: Number of hours to summarize (default: 24)
    """
    try:
        hours = InputValidator.validate_integer(hours, min_value=1, max_value=168, name="hours")
        summary = await security_monitor.get_security_summary(hours=hours)
        return summary
    except Exception as e:
        logger.error(f"Failed to get security summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate security summary")


@router.get("/events/recent")
async def get_recent_security_events(
    limit: int = 100,
    _: bool = Depends(verify_admin_access)
):
    """
    Get recent security events.
    Requires admin authentication.

    Args:
        limit: Maximum number of events to return
    """
    try:
        limit = InputValidator.validate_integer(limit, min_value=1, max_value=1000, name="limit")

        # This would return recent events from the security monitor
        # For now, return a placeholder
        return {
            "events": [],
            "count": 0,
            "limit": limit,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get security events: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve security events")


@router.post("/test-alert")
async def test_security_alert(_: bool = Depends(verify_admin_access)):
    """
    Send a test security alert to verify notification system.
    Requires admin authentication.
    """
    try:
        await security_monitor.log_security_event(
            event_type="test_alert",
            severity=security_monitor.SEVERITY_LOW,
            details={"message": "This is a test alert"},
            ip_address="127.0.0.1"
        )

        return {
            "status": "success",
            "message": "Test alert sent successfully"
        }
    except Exception as e:
        logger.error(f"Failed to send test alert: {e}")
        raise HTTPException(status_code=500, detail="Failed to send test alert")


@router.get("/secrets/rotation-status")
async def get_secrets_rotation_status(_: bool = Depends(verify_admin_access)):
    """
    Check which secrets need rotation.
    Requires admin authentication.
    """
    try:
        needs_rotation = await secrets_manager.check_rotation_needed()

        return {
            "needs_rotation": needs_rotation,
            "count": len(needs_rotation),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to check rotation status: {e}")
        raise HTTPException(status_code=500, detail="Failed to check rotation status")


@router.post("/secrets/scan")
async def scan_text_for_secrets(
    text: str,
    _: bool = Depends(verify_admin_access)
):
    """
    Scan text for potential secrets.
    Requires admin authentication.

    Useful for checking commits, configuration files, etc.
    """
    try:
        text = InputValidator.sanitize_string(text, max_length=100000)
        detected = secrets_manager.scan_for_secrets(text)

        if detected:
            logger.warning(f"🚨 Secrets detected in scanned text: {len(detected)} findings")

        return {
            "secrets_detected": len(detected),
            "findings": detected,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to scan for secrets: {e}")
        raise HTTPException(status_code=500, detail="Failed to scan text")


@router.get("/api-keys/audit")
async def get_api_keys_audit(_: bool = Depends(verify_admin_access)):
    """
    Get API keys audit report.
    Requires admin authentication.
    """
    try:
        audit = await api_key_manager.audit_api_keys()
        return audit
    except Exception as e:
        logger.error(f"Failed to get API keys audit: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate audit report")


@router.post("/report/daily")
async def trigger_daily_report(_: bool = Depends(verify_admin_access)):
    """
    Manually trigger daily security report.
    Requires admin authentication.
    """
    try:
        await security_monitor.generate_daily_security_report()

        return {
            "status": "success",
            "message": "Daily security report generated and sent"
        }
    except Exception as e:
        logger.error(f"Failed to generate daily report: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate report")


@router.get("/blocked-ips")
async def get_blocked_ips(_: bool = Depends(verify_admin_access)):
    """
    Get list of currently blocked IP addresses.
    Requires admin authentication.
    """
    try:
        # This would query Redis for blocked IPs
        # Placeholder for now
        return {
            "blocked_ips": [],
            "count": 0,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get blocked IPs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve blocked IPs")


@router.post("/ip/unblock/{ip_address}")
async def unblock_ip(
    ip_address: str,
    _: bool = Depends(verify_admin_access)
):
    """
    Manually unblock an IP address.
    Requires admin authentication.
    """
    try:
        # Validate IP address format
        ip_address = InputValidator.sanitize_string(ip_address, max_length=45)

        # This would remove the IP from Redis blocklist
        # Placeholder for now
        logger.info(f"🔓 IP unblocked manually: {ip_address}")

        return {
            "status": "success",
            "message": f"IP {ip_address} has been unblocked"
        }
    except Exception as e:
        logger.error(f"Failed to unblock IP: {e}")
        raise HTTPException(status_code=500, detail="Failed to unblock IP")


@router.get("/metrics")
async def get_security_metrics(_: bool = Depends(verify_admin_access)):
    """
    Get comprehensive security metrics.
    Requires admin authentication.
    """
    try:
        summary_24h = await security_monitor.get_security_summary(hours=24)
        summary_1h = await security_monitor.get_security_summary(hours=1)
        api_keys_audit = await api_key_manager.audit_api_keys()
        rotation_status = await secrets_manager.check_rotation_needed()

        return {
            "last_24_hours": summary_24h,
            "last_hour": summary_1h,
            "api_keys": api_keys_audit,
            "secrets_rotation": {
                "needs_rotation": len(rotation_status),
                "items": rotation_status
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get security metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve security metrics")
