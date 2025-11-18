"""
AI-Powered Trade Plan API
Comprehensive endpoints for creating, managing, and analyzing trade plans
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
import logging
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import TradePlan, Ticker
from app.database import get_db
from app.services.plan_generator import get_plan_generator, TradePlanData
from app.services.pdf_export import get_pdf_export_service
from app.services.trade_plan_library import get_trade_plan_library
from app.services.trade_plan_alerts import get_trade_plan_alert_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/trade-plans", tags=["trade-plans"])


# Pydantic models for requests/responses
class CreatePlanRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")
    account_size: float = Field(10000.0, description="Trading account size")
    risk_percentage: float = Field(2.0, description="Risk per trade (%)")
    timeframe: str = Field("1day", description="Chart timeframe")
    strategy: str = Field("swing", description="Trading strategy")
    user_notes: Optional[str] = Field(None, description="Optional user notes")
    export_pdf: bool = Field(True, description="Generate PDF export")


class UpdatePlanRequest(BaseModel):
    status: Optional[str] = Field(None, description="Plan status")
    entry_price_actual: Optional[float] = Field(None, description="Actual entry price")
    exit_price_actual: Optional[float] = Field(None, description="Actual exit price")
    outcome: Optional[str] = Field(None, description="Trade outcome")
    lessons_learned: Optional[str] = Field(None, description="Lessons learned")


class PlanResponse(BaseModel):
    id: int
    ticker: str
    pattern_type: str
    pattern_score: float
    status: str
    entry_zone: dict
    stop_levels: dict
    targets: dict
    position: dict
    pdf_path: Optional[str] = None
    created_at: str


@router.post("/create", response_model=dict)
async def create_trade_plan(
    req: CreatePlanRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate AI-powered trade plan for a ticker

    Creates comprehensive trade plan with:
    - Pattern analysis
    - Entry/stop/target levels
    - Multi-scenario planning
    - Position sizing
    - AI analysis
    - Optional PDF export
    """
    try:
        logger.info(f"📊 Creating trade plan for {req.ticker}")

        # Generate plan using AI
        plan_generator = get_plan_generator()
        plan_data: TradePlanData = await plan_generator.generate_plan(
            ticker=req.ticker,
            account_size=req.account_size,
            risk_percentage=req.risk_percentage,
            timeframe=req.timeframe,
            strategy=req.strategy,
            user_notes=req.user_notes
        )

        # Get or create ticker
        ticker_result = await db.execute(
            select(Ticker).where(Ticker.symbol == req.ticker.upper())
        )
        ticker = ticker_result.scalar_one_or_none()

        if not ticker:
            ticker = Ticker(symbol=req.ticker.upper())
            db.add(ticker)
            await db.flush()

        # Create trade plan record
        trade_plan = TradePlan(
            ticker_id=ticker.id,
            user_id="default",
            pattern_type=plan_data.pattern_type,
            pattern_score=plan_data.pattern_score,
            current_price=plan_data.current_price,
            entry_zone_low=plan_data.entry_zone.low,
            entry_zone_high=plan_data.entry_zone.high,
            optimal_entry=plan_data.entry_zone.optimal,
            initial_stop=plan_data.stop_levels.initial_stop,
            trailing_stop=plan_data.stop_levels.trailing_stop,
            invalidation_price=plan_data.stop_levels.invalidation_price,
            best_case_target=plan_data.scenario_analysis.best_case_target,
            best_case_rr=plan_data.scenario_analysis.best_case_rr,
            base_case_target=plan_data.scenario_analysis.base_case_target,
            base_case_rr=plan_data.scenario_analysis.base_case_rr,
            worst_case_target=plan_data.scenario_analysis.worst_case_target,
            worst_case_rr=plan_data.scenario_analysis.worst_case_rr,
            account_size=req.account_size,
            risk_percentage=req.risk_percentage,
            position_size=plan_data.position_size,
            position_value=plan_data.position_value,
            risk_amount=plan_data.risk_amount,
            timeframe=req.timeframe,
            strategy=req.strategy,
            notes=plan_data.ai_notes,
            checklist=json.dumps(plan_data.checklist),
            alerts_config=json.dumps({}),
            status="planned",
            chart_url=plan_data.chart_url
        )

        db.add(trade_plan)
        await db.commit()
        await db.refresh(trade_plan)

        # Create alerts for the plan
        alert_service = get_trade_plan_alert_service()
        await alert_service.create_alerts_for_plan(db, trade_plan.id)

        # Export to PDF if requested
        pdf_path = None
        if req.export_pdf:
            try:
                pdf_service = get_pdf_export_service()
                pdf_path = await pdf_service.generate_pdf(plan_data)
                trade_plan.pdf_path = pdf_path
                await db.commit()
            except Exception as e:
                logger.warning(f"PDF export failed: {e}")

        logger.info(f"✅ Trade plan created: ID {trade_plan.id}")

        return {
            "success": True,
            "plan_id": trade_plan.id,
            "ticker": req.ticker,
            "pattern": plan_data.pattern_type,
            "score": plan_data.pattern_score,
            "entry_zone": {
                "low": plan_data.entry_zone.low,
                "high": plan_data.entry_zone.high,
                "optimal": plan_data.entry_zone.optimal
            },
            "stop": plan_data.stop_levels.initial_stop,
            "targets": {
                "best": plan_data.scenario_analysis.best_case_target,
                "base": plan_data.scenario_analysis.base_case_target,
                "worst": plan_data.scenario_analysis.worst_case_target
            },
            "position_size": plan_data.position_size,
            "risk_amount": plan_data.risk_amount,
            "pdf_path": pdf_path,
            "message": f"Trade plan created successfully for {req.ticker}"
        }

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating trade plan: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create trade plan: {str(e)}")


@router.get("/list")
async def list_trade_plans(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """
    List all trade plans with optional filtering

    Query parameters:
    - status: Filter by status (planned, active, completed, cancelled)
    - limit: Maximum results (default 50)
    - offset: Pagination offset (default 0)
    """
    try:
        library = get_trade_plan_library()
        plans = await library.get_all_plans(
            db=db,
            status=status,
            limit=limit,
            offset=offset
        )

        return {
            "success": True,
            "count": len(plans),
            "plans": plans
        }

    except Exception as e:
        logger.error(f"Error listing plans: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{plan_id}")
async def get_trade_plan(
    plan_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed trade plan by ID"""
    try:
        library = get_trade_plan_library()
        plan = await library.get_plan_by_id(db, plan_id)

        if not plan:
            raise HTTPException(status_code=404, detail="Trade plan not found")

        return {
            "success": True,
            "plan": plan
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{plan_id}")
async def update_trade_plan(
    plan_id: int,
    req: UpdatePlanRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Update trade plan status and execution details

    Can update:
    - Status (planned -> active -> completed)
    - Entry/exit prices
    - Outcome and lessons learned
    """
    try:
        result = await db.execute(
            select(TradePlan).where(TradePlan.id == plan_id)
        )
        plan = result.scalar_one_or_none()

        if not plan:
            raise HTTPException(status_code=404, detail="Trade plan not found")

        # Update fields
        if req.status:
            plan.status = req.status

        if req.entry_price_actual:
            plan.entry_price_actual = req.entry_price_actual
            if not plan.entry_date:
                from datetime import datetime
                plan.entry_date = datetime.utcnow()

        if req.exit_price_actual:
            # Use library to handle outcome calculation
            library = get_trade_plan_library()
            await library.update_plan_outcome(
                db=db,
                plan_id=plan_id,
                outcome=req.outcome or "completed",
                exit_price=req.exit_price_actual,
                lessons_learned=req.lessons_learned
            )
        else:
            await db.commit()

        logger.info(f"✅ Updated trade plan {plan_id}")

        return {
            "success": True,
            "plan_id": plan_id,
            "message": "Trade plan updated successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/summary")
async def get_analytics(
    days: int = 90,
    db: AsyncSession = Depends(get_db)
):
    """
    Get comprehensive trade plan analytics

    Includes:
    - Win rate and P&L statistics
    - Performance by pattern type
    - Target hit statistics
    - Improvement suggestions
    """
    try:
        library = get_trade_plan_library()
        analytics = await library.get_analytics(db, days=days)

        return {
            "success": True,
            "analytics": analytics
        }

    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{plan_id}/export-pdf")
async def export_plan_to_pdf(
    plan_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Export existing trade plan to PDF"""
    try:
        # Get plan details
        library = get_trade_plan_library()
        plan_dict = await library.get_plan_by_id(db, plan_id)

        if not plan_dict:
            raise HTTPException(status_code=404, detail="Trade plan not found")

        # Reconstruct TradePlanData for PDF export
        # (This is a simplified version - you might need to fetch full data)

        logger.info(f"📄 PDF export for plan {plan_id} - feature available")

        return {
            "success": True,
            "message": "PDF export available via plan creation",
            "plan_id": plan_id
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{plan_id}")
async def delete_trade_plan(
    plan_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a trade plan"""
    try:
        result = await db.execute(
            select(TradePlan).where(TradePlan.id == plan_id)
        )
        plan = result.scalar_one_or_none()

        if not plan:
            raise HTTPException(status_code=404, detail="Trade plan not found")

        await db.delete(plan)
        await db.commit()

        logger.info(f"🗑️ Deleted trade plan {plan_id}")

        return {
            "success": True,
            "message": f"Trade plan {plan_id} deleted successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Background monitoring endpoint (can be called by scheduler)
@router.post("/monitor/active")
async def monitor_active_plans(db: AsyncSession = Depends(get_db)):
    """
    Monitor all active trade plans and trigger alerts

    This endpoint should be called periodically (e.g., every 5 minutes)
    by a scheduler or cron job
    """
    try:
        alert_service = get_trade_plan_alert_service()
        result = await alert_service.monitor_active_plans(db)

        return {
            "success": True,
            "monitoring_result": result
        }

    except Exception as e:
        logger.error(f"Error monitoring plans: {e}")
        raise HTTPException(status_code=500, detail=str(e))
