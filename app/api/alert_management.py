"""
Alert Management API - Comprehensive alert rule management
Provides CRUD operations, snooze, bulk operations, and alert history
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
import logging

from app.models import AlertRule, AlertLog, AlertDelivery, Ticker
from app.services.database import get_db
from app.services.alert_rule_engine import AlertRuleEngine, ConditionBuilder
from app.services.alert_delivery import AlertDeliveryService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/alert-management", tags=["alert-management"])


# Pydantic models for request/response
class AlertConditionModel(BaseModel):
    """Alert condition model"""
    field: str = Field(..., description="Field to monitor (price, volume, rsi, etc.)")
    operator: str = Field(..., description="Comparison operator (>, <, >=, <=, ==, crosses_above, etc.)")
    value: float = Field(..., description="Target value")
    value_type: str = Field(default="absolute", description="Value type (absolute, percentage)")
    time_window: Optional[int] = Field(None, description="Time window in seconds")
    comparison_period: Optional[str] = Field(None, description="Comparison period (1min, 5min, 1hour, 1day)")


class CreateAlertRuleRequest(BaseModel):
    """Request to create an alert rule"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    ticker_symbol: Optional[str] = Field(None, description="Ticker symbol (e.g., AAPL)")
    alert_type: str = Field(..., description="Alert type (price, pattern, volume, indicator, news, options_flow)")

    condition_logic: str = Field(default="AND", description="Logic for multiple conditions (AND/OR)")
    conditions: List[Dict[str, Any]] = Field(..., min_items=1, description="List of conditions")

    delivery_channels: List[str] = Field(..., min_items=1, description="Delivery channels (telegram, email, sms, discord, slack, webhook, push)")
    delivery_config: Optional[Dict[str, Any]] = Field(None, description="Channel-specific configuration")

    is_enabled: bool = Field(default=True)
    check_frequency: int = Field(default=60, ge=10, description="Check frequency in seconds")
    cooldown_period: int = Field(default=3600, ge=0, description="Cooldown period in seconds")
    user_id: str = Field(default="default")


class UpdateAlertRuleRequest(BaseModel):
    """Request to update an alert rule"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    alert_type: Optional[str] = None
    condition_logic: Optional[str] = None
    conditions: Optional[List[Dict[str, Any]]] = None
    delivery_channels: Optional[List[str]] = None
    delivery_config: Optional[Dict[str, Any]] = None
    is_enabled: Optional[bool] = None
    check_frequency: Optional[int] = Field(None, ge=10)
    cooldown_period: Optional[int] = Field(None, ge=0)


class SnoozeAlertRequest(BaseModel):
    """Request to snooze an alert"""
    duration_minutes: int = Field(..., ge=1, le=10080, description="Snooze duration in minutes (max 1 week)")


class BulkOperationRequest(BaseModel):
    """Request for bulk operations"""
    rule_ids: List[int] = Field(..., min_items=1)
    operation: str = Field(..., description="Operation (enable, disable, delete, snooze)")
    snooze_duration_minutes: Optional[int] = Field(None, ge=1, le=10080)


class AlertRuleResponse(BaseModel):
    """Alert rule response"""
    id: int
    name: str
    description: Optional[str]
    ticker_symbol: Optional[str]
    alert_type: str
    condition_logic: str
    conditions: List[Dict[str, Any]]
    delivery_channels: List[str]
    is_enabled: bool
    is_snoozed: bool
    snoozed_until: Optional[datetime]
    check_frequency: int
    cooldown_period: int
    last_triggered_at: Optional[datetime]
    trigger_count: int
    created_at: datetime
    updated_at: Optional[datetime]
    created_by: str

    class Config:
        from_attributes = True


# CRUD Endpoints
@router.post("/rules", response_model=AlertRuleResponse)
async def create_alert_rule(
    request: CreateAlertRuleRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new alert rule

    Creates a comprehensive alert rule with conditions and delivery channels.
    """
    try:
        # Get or create ticker if specified
        ticker_id = None
        if request.ticker_symbol:
            ticker = db.query(Ticker).filter(Ticker.symbol == request.ticker_symbol.upper()).first()
            if not ticker:
                ticker = Ticker(symbol=request.ticker_symbol.upper())
                db.add(ticker)
                db.commit()
                db.refresh(ticker)
            ticker_id = ticker.id

        # Create alert rule
        rule = AlertRule(
            name=request.name,
            description=request.description,
            ticker_id=ticker_id,
            alert_type=request.alert_type,
            condition_logic=request.condition_logic,
            conditions=request.conditions,
            delivery_channels=request.delivery_channels,
            delivery_config=request.delivery_config,
            is_enabled=request.is_enabled,
            check_frequency=request.check_frequency,
            cooldown_period=request.cooldown_period,
            user_id=request.user_id,
            created_by="user"
        )

        db.add(rule)
        db.commit()
        db.refresh(rule)

        logger.info(f"Created alert rule: {rule.name} (ID: {rule.id})")

        # Get ticker symbol for response
        ticker_symbol = None
        if ticker_id:
            ticker = db.query(Ticker).filter(Ticker.id == ticker_id).first()
            ticker_symbol = ticker.symbol if ticker else None

        return AlertRuleResponse(
            id=rule.id,
            name=rule.name,
            description=rule.description,
            ticker_symbol=ticker_symbol,
            alert_type=rule.alert_type,
            condition_logic=rule.condition_logic,
            conditions=rule.conditions,
            delivery_channels=rule.delivery_channels,
            is_enabled=rule.is_enabled,
            is_snoozed=rule.is_snoozed,
            snoozed_until=rule.snoozed_until,
            check_frequency=rule.check_frequency,
            cooldown_period=rule.cooldown_period,
            last_triggered_at=rule.last_triggered_at,
            trigger_count=rule.trigger_count,
            created_at=rule.created_at,
            updated_at=rule.updated_at,
            created_by=rule.created_by
        )

    except Exception as e:
        logger.error(f"Error creating alert rule: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rules", response_model=List[AlertRuleResponse])
async def get_alert_rules(
    user_id: str = "default",
    is_enabled: Optional[bool] = None,
    alert_type: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Get all alert rules

    Returns a list of alert rules with optional filtering.
    """
    try:
        query = db.query(AlertRule).filter(AlertRule.user_id == user_id)

        if is_enabled is not None:
            query = query.filter(AlertRule.is_enabled == is_enabled)

        if alert_type:
            query = query.filter(AlertRule.alert_type == alert_type)

        rules = query.order_by(desc(AlertRule.created_at)).limit(limit).offset(offset).all()

        # Convert to response models
        response_rules = []
        for rule in rules:
            ticker_symbol = None
            if rule.ticker_id:
                ticker = db.query(Ticker).filter(Ticker.id == rule.ticker_id).first()
                ticker_symbol = ticker.symbol if ticker else None

            response_rules.append(AlertRuleResponse(
                id=rule.id,
                name=rule.name,
                description=rule.description,
                ticker_symbol=ticker_symbol,
                alert_type=rule.alert_type,
                condition_logic=rule.condition_logic,
                conditions=rule.conditions,
                delivery_channels=rule.delivery_channels,
                is_enabled=rule.is_enabled,
                is_snoozed=rule.is_snoozed,
                snoozed_until=rule.snoozed_until,
                check_frequency=rule.check_frequency,
                cooldown_period=rule.cooldown_period,
                last_triggered_at=rule.last_triggered_at,
                trigger_count=rule.trigger_count,
                created_at=rule.created_at,
                updated_at=rule.updated_at,
                created_by=rule.created_by
            ))

        return response_rules

    except Exception as e:
        logger.error(f"Error getting alert rules: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rules/{rule_id}", response_model=AlertRuleResponse)
async def get_alert_rule(
    rule_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific alert rule by ID"""
    try:
        rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
        if not rule:
            raise HTTPException(status_code=404, detail="Alert rule not found")

        ticker_symbol = None
        if rule.ticker_id:
            ticker = db.query(Ticker).filter(Ticker.id == rule.ticker_id).first()
            ticker_symbol = ticker.symbol if ticker else None

        return AlertRuleResponse(
            id=rule.id,
            name=rule.name,
            description=rule.description,
            ticker_symbol=ticker_symbol,
            alert_type=rule.alert_type,
            condition_logic=rule.condition_logic,
            conditions=rule.conditions,
            delivery_channels=rule.delivery_channels,
            is_enabled=rule.is_enabled,
            is_snoozed=rule.is_snoozed,
            snoozed_until=rule.snoozed_until,
            check_frequency=rule.check_frequency,
            cooldown_period=rule.cooldown_period,
            last_triggered_at=rule.last_triggered_at,
            trigger_count=rule.trigger_count,
            created_at=rule.created_at,
            updated_at=rule.updated_at,
            created_by=rule.created_by
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting alert rule {rule_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/rules/{rule_id}", response_model=AlertRuleResponse)
async def update_alert_rule(
    rule_id: int,
    request: UpdateAlertRuleRequest,
    db: Session = Depends(get_db)
):
    """Update an existing alert rule"""
    try:
        rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
        if not rule:
            raise HTTPException(status_code=404, detail="Alert rule not found")

        # Update fields
        if request.name is not None:
            rule.name = request.name
        if request.description is not None:
            rule.description = request.description
        if request.alert_type is not None:
            rule.alert_type = request.alert_type
        if request.condition_logic is not None:
            rule.condition_logic = request.condition_logic
        if request.conditions is not None:
            rule.conditions = request.conditions
        if request.delivery_channels is not None:
            rule.delivery_channels = request.delivery_channels
        if request.delivery_config is not None:
            rule.delivery_config = request.delivery_config
        if request.is_enabled is not None:
            rule.is_enabled = request.is_enabled
        if request.check_frequency is not None:
            rule.check_frequency = request.check_frequency
        if request.cooldown_period is not None:
            rule.cooldown_period = request.cooldown_period

        rule.updated_at = datetime.now()

        db.commit()
        db.refresh(rule)

        logger.info(f"Updated alert rule: {rule.name} (ID: {rule.id})")

        ticker_symbol = None
        if rule.ticker_id:
            ticker = db.query(Ticker).filter(Ticker.id == rule.ticker_id).first()
            ticker_symbol = ticker.symbol if ticker else None

        return AlertRuleResponse(
            id=rule.id,
            name=rule.name,
            description=rule.description,
            ticker_symbol=ticker_symbol,
            alert_type=rule.alert_type,
            condition_logic=rule.condition_logic,
            conditions=rule.conditions,
            delivery_channels=rule.delivery_channels,
            is_enabled=rule.is_enabled,
            is_snoozed=rule.is_snoozed,
            snoozed_until=rule.snoozed_until,
            check_frequency=rule.check_frequency,
            cooldown_period=rule.cooldown_period,
            last_triggered_at=rule.last_triggered_at,
            trigger_count=rule.trigger_count,
            created_at=rule.created_at,
            updated_at=rule.updated_at,
            created_by=rule.created_by
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating alert rule {rule_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/rules/{rule_id}")
async def delete_alert_rule(
    rule_id: int,
    db: Session = Depends(get_db)
):
    """Delete an alert rule"""
    try:
        rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
        if not rule:
            raise HTTPException(status_code=404, detail="Alert rule not found")

        db.delete(rule)
        db.commit()

        logger.info(f"Deleted alert rule ID: {rule_id}")

        return {"success": True, "message": f"Alert rule {rule_id} deleted"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting alert rule {rule_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Snooze Operations
@router.post("/rules/{rule_id}/snooze")
async def snooze_alert_rule(
    rule_id: int,
    request: SnoozeAlertRequest,
    db: Session = Depends(get_db)
):
    """Snooze an alert rule for a specified duration"""
    try:
        rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
        if not rule:
            raise HTTPException(status_code=404, detail="Alert rule not found")

        snooze_until = datetime.now() + timedelta(minutes=request.duration_minutes)
        rule.is_snoozed = True
        rule.snoozed_until = snooze_until

        db.commit()

        logger.info(f"Snoozed alert rule {rule_id} until {snooze_until}")

        return {
            "success": True,
            "message": f"Alert snoozed for {request.duration_minutes} minutes",
            "snoozed_until": snooze_until.isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error snoozing alert rule {rule_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rules/{rule_id}/unsnooze")
async def unsnooze_alert_rule(
    rule_id: int,
    db: Session = Depends(get_db)
):
    """Un-snooze an alert rule"""
    try:
        rule = db.query(AlertRule).filter(AlertRule.id == rule_id).first()
        if not rule:
            raise HTTPException(status_code=404, detail="Alert rule not found")

        rule.is_snoozed = False
        rule.snoozed_until = None

        db.commit()

        logger.info(f"Un-snoozed alert rule {rule_id}")

        return {"success": True, "message": "Alert un-snoozed"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error un-snoozing alert rule {rule_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Bulk Operations
@router.post("/rules/bulk")
async def bulk_operations(
    request: BulkOperationRequest,
    db: Session = Depends(get_db)
):
    """Perform bulk operations on multiple alert rules"""
    try:
        rules = db.query(AlertRule).filter(AlertRule.id.in_(request.rule_ids)).all()

        if not rules:
            raise HTTPException(status_code=404, detail="No rules found")

        results = {
            "total": len(request.rule_ids),
            "processed": 0,
            "failed": 0,
            "errors": []
        }

        for rule in rules:
            try:
                if request.operation == "enable":
                    rule.is_enabled = True
                elif request.operation == "disable":
                    rule.is_enabled = False
                elif request.operation == "delete":
                    db.delete(rule)
                elif request.operation == "snooze":
                    if request.snooze_duration_minutes:
                        rule.is_snoozed = True
                        rule.snoozed_until = datetime.now() + timedelta(minutes=request.snooze_duration_minutes)
                    else:
                        results["errors"].append(f"Rule {rule.id}: Snooze duration not provided")
                        results["failed"] += 1
                        continue
                else:
                    results["errors"].append(f"Rule {rule.id}: Unknown operation {request.operation}")
                    results["failed"] += 1
                    continue

                results["processed"] += 1

            except Exception as e:
                results["errors"].append(f"Rule {rule.id}: {str(e)}")
                results["failed"] += 1

        db.commit()

        logger.info(f"Bulk operation '{request.operation}' completed: {results['processed']}/{results['total']} processed")

        return {
            "success": True,
            "operation": request.operation,
            "results": results
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in bulk operation: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# Alert History
@router.get("/history")
async def get_alert_history(
    user_id: str = "default",
    alert_type: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Get alert history with filtering

    Returns a list of triggered alerts with delivery status.
    """
    try:
        query = db.query(AlertLog).filter(AlertLog.user_id == user_id)

        if alert_type:
            query = query.filter(AlertLog.alert_type == alert_type)

        if status:
            query = query.filter(AlertLog.status == status)

        if start_date:
            query = query.filter(AlertLog.created_at >= start_date)

        if end_date:
            query = query.filter(AlertLog.created_at <= end_date)

        total = query.count()
        alerts = query.order_by(desc(AlertLog.created_at)).limit(limit).offset(offset).all()

        # Convert to response
        alert_history = []
        for alert in alerts:
            ticker_symbol = None
            if alert.ticker_id:
                ticker = db.query(Ticker).filter(Ticker.id == alert.ticker_id).first()
                ticker_symbol = ticker.symbol if ticker else None

            alert_history.append({
                "id": alert.id,
                "rule_id": alert.rule_id,
                "ticker_symbol": ticker_symbol,
                "alert_type": alert.alert_type,
                "alert_title": alert.alert_title,
                "alert_message": alert.alert_message,
                "trigger_price": alert.trigger_price,
                "delivery_channels": alert.delivery_channels,
                "delivery_status": alert.delivery_status,
                "status": alert.status,
                "acknowledged_at": alert.acknowledged_at,
                "created_at": alert.created_at
            })

        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "alerts": alert_history
        }

    except Exception as e:
        logger.error(f"Error getting alert history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Alert Performance
@router.get("/performance")
async def get_alert_performance(
    user_id: str = "default",
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Get alert performance metrics

    Returns statistics about alert triggers, delivery success rates, etc.
    """
    try:
        start_date = datetime.now() - timedelta(days=days)

        # Get all alerts in time period
        alerts = db.query(AlertLog).filter(
            AlertLog.user_id == user_id,
            AlertLog.created_at >= start_date
        ).all()

        # Calculate metrics
        total_alerts = len(alerts)
        alerts_by_type = {}
        delivery_success_rate = {}
        alerts_by_channel = {}

        for alert in alerts:
            # Count by type
            alert_type = alert.alert_type
            alerts_by_type[alert_type] = alerts_by_type.get(alert_type, 0) + 1

            # Delivery success
            if alert.delivery_status:
                for channel, status in alert.delivery_status.items():
                    if channel not in delivery_success_rate:
                        delivery_success_rate[channel] = {"sent": 0, "failed": 0}

                    if status == "sent":
                        delivery_success_rate[channel]["sent"] += 1
                    else:
                        delivery_success_rate[channel]["failed"] += 1

                    # Count by channel
                    alerts_by_channel[channel] = alerts_by_channel.get(channel, 0) + 1

        # Calculate success rates
        success_rates = {}
        for channel, stats in delivery_success_rate.items():
            total = stats["sent"] + stats["failed"]
            success_rates[channel] = (stats["sent"] / total * 100) if total > 0 else 0

        return {
            "period_days": days,
            "total_alerts": total_alerts,
            "alerts_by_type": alerts_by_type,
            "alerts_by_channel": alerts_by_channel,
            "delivery_success_rates": success_rates,
            "delivery_stats": delivery_success_rate
        }

    except Exception as e:
        logger.error(f"Error getting alert performance: {e}")
        raise HTTPException(status_code=500, detail=str(e))
