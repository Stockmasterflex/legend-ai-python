"""
Smart Alerts API - AI-powered alert suggestions
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import logging

from app.models import AlertRule
from app.services.database import get_db
from app.services.smart_alerts import SmartAlertService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/smart-alerts", tags=["smart-alerts"])


class SuggestAlertsRequest(BaseModel):
    """Request for alert suggestions"""
    ticker_symbol: str = Field(..., min_length=1, max_length=10)
    suggestion_types: Optional[List[str]] = Field(
        default=["ai", "pattern", "risk", "correlation"],
        description="Types of suggestions to generate"
    )


class AutoCreateAlertRequest(BaseModel):
    """Request to auto-create alert from suggestion"""
    suggestion: Dict[str, Any]
    user_id: str = Field(default="default")


@router.post("/suggest")
async def suggest_alerts(
    request: SuggestAlertsRequest,
    db: Session = Depends(get_db)
):
    """
    Get AI-powered alert suggestions for a ticker

    Analyzes market conditions and suggests relevant alerts.
    """
    try:
        smart_alert_service = SmartAlertService(db)
        all_suggestions = []

        # AI-based suggestions
        if "ai" in request.suggestion_types:
            ai_suggestions = await smart_alert_service.suggest_alerts_for_ticker(request.ticker_symbol)
            all_suggestions.extend(ai_suggestions)

        # Pattern-based suggestions
        if "pattern" in request.suggestion_types:
            pattern_suggestions = await smart_alert_service.suggest_pattern_based_alerts()
            # Filter for this ticker
            pattern_suggestions = [s for s in pattern_suggestions if s.get("ticker_symbol") == request.ticker_symbol.upper()]
            all_suggestions.extend(pattern_suggestions)

        # Risk-based suggestions
        if "risk" in request.suggestion_types:
            risk_suggestions = await smart_alert_service.suggest_risk_based_alerts(request.ticker_symbol)
            all_suggestions.extend(risk_suggestions)

        # Correlation-based suggestions
        if "correlation" in request.suggestion_types:
            correlation_suggestions = await smart_alert_service.suggest_correlation_alerts(request.ticker_symbol)
            all_suggestions.extend(correlation_suggestions)

        return {
            "success": True,
            "ticker": request.ticker_symbol.upper(),
            "total_suggestions": len(all_suggestions),
            "suggestions": all_suggestions
        }

    except Exception as e:
        logger.error(f"Error suggesting alerts for {request.ticker_symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/suggest-pattern-based")
async def suggest_pattern_based_alerts(
    user_id: str = "default",
    db: Session = Depends(get_db)
):
    """
    Get pattern-based alert suggestions

    Analyzes recent pattern scans and suggests alerts.
    """
    try:
        smart_alert_service = SmartAlertService(db)
        suggestions = await smart_alert_service.suggest_pattern_based_alerts(user_id)

        return {
            "success": True,
            "total_suggestions": len(suggestions),
            "suggestions": suggestions
        }

    except Exception as e:
        logger.error(f"Error suggesting pattern-based alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/auto-create")
async def auto_create_alert(
    request: AutoCreateAlertRequest,
    db: Session = Depends(get_db)
):
    """
    Automatically create an alert from a suggestion

    Takes a suggestion and creates an active alert rule.
    """
    try:
        smart_alert_service = SmartAlertService(db)
        alert_rule = await smart_alert_service.auto_create_alert(request.suggestion, request.user_id)

        if not alert_rule:
            raise HTTPException(status_code=400, detail="Failed to create alert from suggestion")

        return {
            "success": True,
            "message": f"Alert created: {alert_rule.name}",
            "alert_rule_id": alert_rule.id,
            "alert_rule": {
                "id": alert_rule.id,
                "name": alert_rule.name,
                "description": alert_rule.description,
                "alert_type": alert_rule.alert_type,
                "is_enabled": alert_rule.is_enabled,
                "created_by": alert_rule.created_by
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error auto-creating alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bulk-auto-create")
async def bulk_auto_create_alerts(
    suggestions: List[Dict[str, Any]],
    user_id: str = "default",
    db: Session = Depends(get_db)
):
    """
    Bulk create multiple alerts from suggestions

    Takes multiple suggestions and creates alert rules.
    """
    try:
        smart_alert_service = SmartAlertService(db)

        results = {
            "total": len(suggestions),
            "created": 0,
            "failed": 0,
            "alert_rules": [],
            "errors": []
        }

        for suggestion in suggestions:
            try:
                alert_rule = await smart_alert_service.auto_create_alert(suggestion, user_id)

                if alert_rule:
                    results["created"] += 1
                    results["alert_rules"].append({
                        "id": alert_rule.id,
                        "name": alert_rule.name,
                        "alert_type": alert_rule.alert_type
                    })
                else:
                    results["failed"] += 1
                    results["errors"].append(f"Failed to create alert: {suggestion.get('name', 'Unknown')}")

            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Error creating alert: {str(e)}")

        return {
            "success": True,
            "message": f"Created {results['created']}/{results['total']} alerts",
            "results": results
        }

    except Exception as e:
        logger.error(f"Error bulk creating alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/discover")
async def discover_alert_opportunities(
    user_id: str = "default",
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Discover alert opportunities from watchlist and recent scans

    Analyzes user's watchlist and recent pattern scans to find alert opportunities.
    """
    try:
        smart_alert_service = SmartAlertService(db)

        # Get pattern-based suggestions
        pattern_suggestions = await smart_alert_service.suggest_pattern_based_alerts(user_id)

        # Limit results
        suggestions = pattern_suggestions[:limit]

        return {
            "success": True,
            "message": f"Found {len(suggestions)} alert opportunities",
            "total_opportunities": len(pattern_suggestions),
            "showing": len(suggestions),
            "opportunities": suggestions
        }

    except Exception as e:
        logger.error(f"Error discovering alert opportunities: {e}")
        raise HTTPException(status_code=500, detail=str(e))
