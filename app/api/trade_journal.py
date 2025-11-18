"""
Trade Journal API endpoints
Professional trade journaling with pre-trade planning, execution tracking, and analytics
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.services.trade_journal import get_trade_journal_service
from app.services.trade_reporting import get_reporting_service
from app.services.database import get_db
from app.models import TradeStatus, EmotionalState, MarketCondition
from fastapi.responses import Response

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/journal", tags=["trade-journal"])


# ==================== REQUEST MODELS ====================

class CreateTradePlanRequest(BaseModel):
    """Create a pre-trade plan"""
    ticker: str
    pattern_identified: str
    thesis: str
    planned_entry: float
    planned_stop: float
    planned_target: float
    planned_position_size: int
    checklist_data: Optional[Dict] = None
    screenshot_url: Optional[str] = None
    user_id: str = "default"


class CompleteChecklistRequest(BaseModel):
    """Complete pre-trade checklist"""
    trade_id: str
    checklist_data: Dict


class ExecuteEntryRequest(BaseModel):
    """Execute trade entry"""
    trade_id: str
    actual_entry_price: float
    actual_position_size: int
    actual_stop_price: Optional[float] = None
    emotional_state: Optional[str] = None
    market_condition: Optional[str] = None
    market_context: Optional[str] = None


class PartialExitRequest(BaseModel):
    """Record partial exit"""
    trade_id: str
    exit_price: float
    shares_sold: int
    reason: str


class ExecuteExitRequest(BaseModel):
    """Execute trade exit"""
    trade_id: str
    exit_price: float
    exit_reason: str
    emotional_state: Optional[str] = None
    fees_paid: float = 0.0
    follow_through_notes: Optional[str] = None


class AddNotesRequest(BaseModel):
    """Add post-trade review notes"""
    trade_id: str
    what_went_well: Optional[str] = None
    what_went_wrong: Optional[str] = None
    lessons_learned: Optional[str] = None


class AddTagRequest(BaseModel):
    """Add tag to trade"""
    trade_id: str
    tag: str


class AddMistakeRequest(BaseModel):
    """Record trading mistake"""
    trade_id: str
    category: str = Field(..., description="entry, exit, sizing, emotional, planning")
    mistake_type: str
    description: str
    impact: str = Field(..., description="minor, moderate, major")


class CreatePlaybookRequest(BaseModel):
    """Create trading playbook"""
    name: str
    description: str
    pattern_type: str
    entry_criteria: List[str]
    exit_criteria: List[str]
    risk_management: Dict
    user_id: str = "default"


class AddLessonRequest(BaseModel):
    """Record trading lesson"""
    title: str
    lesson: str
    pattern_type: Optional[str] = None
    importance: str = "medium"
    user_id: str = "default"


# ==================== PRE-TRADE PLANNING ENDPOINTS ====================

@router.get("/health")
async def journal_health():
    """Health check for trade journal service"""
    return {
        "status": "healthy",
        "service": "trade journal",
        "features": [
            "pre-trade planning",
            "execution tracking",
            "performance analytics",
            "learning system",
            "pattern analysis"
        ]
    }


@router.post("/plan/create")
async def create_trade_plan(
    request: CreateTradePlanRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a pre-trade plan with checklist

    This is step 1: Document your trade idea before execution
    Includes pattern identification, thesis, and risk/reward calculation
    """
    try:
        service = get_trade_journal_service(db)

        trade = await service.create_trade_plan(
            ticker=request.ticker,
            pattern_identified=request.pattern_identified,
            thesis=request.thesis,
            planned_entry=request.planned_entry,
            planned_stop=request.planned_stop,
            planned_target=request.planned_target,
            planned_position_size=request.planned_position_size,
            checklist_data=request.checklist_data,
            screenshot_url=request.screenshot_url,
            user_id=request.user_id
        )

        return {
            "success": True,
            "trade_id": trade.trade_id,
            "ticker": request.ticker,
            "pattern": request.pattern_identified,
            "risk_reward_ratio": f"{trade.planned_risk_reward:.2f}:1",
            "risk_amount": f"${trade.planned_risk_amount:,.2f}",
            "status": "planned",
            "checklist_completed": trade.checklist_completed,
            "message": "Trade plan created. Complete checklist before entry."
        }

    except Exception as e:
        logger.error(f"Error creating trade plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/plan/checklist")
async def complete_checklist(
    request: CompleteChecklistRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Complete pre-trade checklist

    Verify all entry criteria are met before execution
    """
    try:
        service = get_trade_journal_service(db)
        trade = await service.complete_checklist(
            trade_id=request.trade_id,
            checklist_data=request.checklist_data
        )

        return {
            "success": True,
            "trade_id": trade.trade_id,
            "checklist_completed": trade.checklist_completed,
            "items_checked": len([k for k, v in request.checklist_data.items() if v]),
            "total_items": len(request.checklist_data),
            "ready_to_trade": trade.checklist_completed
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error completing checklist: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== TRADE EXECUTION ENDPOINTS ====================

@router.post("/execute/entry")
async def execute_entry(
    request: ExecuteEntryRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Execute trade entry and track slippage

    This is step 2: Record actual entry details vs planned
    """
    try:
        service = get_trade_journal_service(db)

        # Convert string enums if provided
        emotional_state = None
        if request.emotional_state:
            emotional_state = EmotionalState[request.emotional_state.upper()]

        market_condition = None
        if request.market_condition:
            market_condition = MarketCondition[request.market_condition.upper()]

        trade = await service.execute_entry(
            trade_id=request.trade_id,
            actual_entry_price=request.actual_entry_price,
            actual_position_size=request.actual_position_size,
            actual_stop_price=request.actual_stop_price,
            emotional_state=emotional_state,
            market_condition=market_condition,
            market_context=request.market_context
        )

        return {
            "success": True,
            "trade_id": trade.trade_id,
            "status": "open",
            "entry_price": f"${trade.actual_entry_price:.2f}",
            "planned_entry": f"${trade.planned_entry:.2f}",
            "slippage": f"${trade.entry_slippage:.4f}",
            "slippage_cost": f"${trade.slippage_cost:.2f}",
            "position_size": trade.actual_position_size,
            "emotional_state": request.emotional_state,
            "market_condition": request.market_condition,
            "entry_time": trade.entry_timestamp.isoformat()
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error executing entry: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute/partial-exit")
async def partial_exit(
    request: PartialExitRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Record a partial exit

    Scale out of positions while tracking each exit
    """
    try:
        service = get_trade_journal_service(db)
        trade = await service.add_partial_exit(
            trade_id=request.trade_id,
            exit_price=request.exit_price,
            shares_sold=request.shares_sold,
            reason=request.reason
        )

        return {
            "success": True,
            "trade_id": trade.trade_id,
            "partial_exit_recorded": True,
            "total_partial_exits": len(trade.partial_exits) if trade.partial_exits else 0
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error recording partial exit: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/execute/exit")
async def execute_exit(
    request: ExecuteExitRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Execute trade exit and calculate final P&L

    This is step 3: Close the trade and record all metrics
    """
    try:
        service = get_trade_journal_service(db)

        # Convert emotional state if provided
        emotional_state = None
        if request.emotional_state:
            emotional_state = EmotionalState[request.emotional_state.upper()]

        trade = await service.execute_exit(
            trade_id=request.trade_id,
            exit_price=request.exit_price,
            exit_reason=request.exit_reason,
            emotional_state=emotional_state,
            fees_paid=request.fees_paid,
            follow_through_notes=request.follow_through_notes
        )

        return {
            "success": True,
            "trade_id": trade.trade_id,
            "status": "closed",
            "exit_price": f"${trade.exit_price:.2f}",
            "exit_reason": trade.exit_reason,
            "gross_pnl": f"${trade.gross_pnl:,.2f}",
            "net_pnl": f"${trade.net_pnl:,.2f}",
            "r_multiple": f"{trade.r_multiple:.2f}R",
            "holding_period_hours": f"{trade.holding_period_hours:.1f}h",
            "fees_paid": f"${trade.fees_paid:.2f}",
            "win": trade.net_pnl > 0,
            "exit_time": trade.exit_timestamp.isoformat()
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error executing exit: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== POST-TRADE REVIEW ENDPOINTS ====================

@router.post("/review/notes")
async def add_trade_notes(
    request: AddNotesRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Add post-trade review notes

    This is step 4: Review what went well and what to improve
    """
    try:
        service = get_trade_journal_service(db)
        trade = await service.add_trade_notes(
            trade_id=request.trade_id,
            what_went_well=request.what_went_well,
            what_went_wrong=request.what_went_wrong,
            lessons_learned=request.lessons_learned
        )

        return {
            "success": True,
            "trade_id": trade.trade_id,
            "review_completed": True
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error adding trade notes: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/review/tag")
async def add_tag(
    request: AddTagRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Add tag to trade for organization

    Examples: 'lesson', 'perfect_execution', 'revenge_trade', 'emotional'
    """
    try:
        service = get_trade_journal_service(db)
        tag = await service.add_trade_tag(
            trade_id=request.trade_id,
            tag=request.tag
        )

        return {
            "success": True,
            "trade_id": request.trade_id,
            "tag_added": tag.tag
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error adding tag: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/review/mistake")
async def add_mistake(
    request: AddMistakeRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Categorize a trading mistake

    Track patterns in mistakes to improve over time
    """
    try:
        service = get_trade_journal_service(db)
        mistake = await service.add_mistake(
            trade_id=request.trade_id,
            category=request.category,
            mistake_type=request.mistake_type,
            description=request.description,
            impact=request.impact
        )

        return {
            "success": True,
            "trade_id": request.trade_id,
            "mistake_category": mistake.category,
            "mistake_type": mistake.mistake_type,
            "impact": mistake.impact
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error adding mistake: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== LEARNING SYSTEM ENDPOINTS ====================

@router.post("/playbook/create")
async def create_playbook(
    request: CreatePlaybookRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a trading playbook/strategy

    Document your repeatable trading setups
    """
    try:
        service = get_trade_journal_service(db)
        playbook = await service.create_playbook(
            name=request.name,
            description=request.description,
            pattern_type=request.pattern_type,
            entry_criteria=request.entry_criteria,
            exit_criteria=request.exit_criteria,
            risk_management=request.risk_management,
            user_id=request.user_id
        )

        return {
            "success": True,
            "playbook_id": playbook.id,
            "name": playbook.name,
            "pattern_type": playbook.pattern_type,
            "created": playbook.created_at.isoformat()
        }

    except Exception as e:
        logger.error(f"Error creating playbook: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/lesson/add")
async def add_lesson(
    request: AddLessonRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Record a trading lesson learned

    Build your knowledge base over time
    """
    try:
        service = get_trade_journal_service(db)
        lesson = await service.add_lesson(
            title=request.title,
            lesson=request.lesson,
            pattern_type=request.pattern_type,
            importance=request.importance,
            user_id=request.user_id
        )

        return {
            "success": True,
            "lesson_id": lesson.id,
            "title": lesson.title,
            "importance": lesson.importance
        }

    except Exception as e:
        logger.error(f"Error adding lesson: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== ANALYTICS ENDPOINTS ====================

@router.get("/trades")
async def get_trades(
    user_id: str = "default",
    status: Optional[str] = None,
    pattern: Optional[str] = None,
    tags: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """
    Get trades with filters

    Query params:
    - status: planned, open, closed, cancelled
    - pattern: VCP, Cup and Handle, etc.
    - tags: comma-separated tags
    - start_date: ISO format
    - end_date: ISO format
    - limit: max results (default 50)
    """
    try:
        service = get_trade_journal_service(db)

        # Parse filters
        status_enum = TradeStatus[status.upper()] if status else None
        tags_list = tags.split(',') if tags else None
        start_dt = datetime.fromisoformat(start_date) if start_date else None
        end_dt = datetime.fromisoformat(end_date) if end_date else None

        trades = await service.get_trades(
            user_id=user_id,
            status=status_enum,
            pattern=pattern,
            tags=tags_list,
            start_date=start_dt,
            end_date=end_dt,
            limit=limit
        )

        trade_list = []
        for trade in trades:
            trade_dict = {
                "trade_id": trade.trade_id,
                "ticker": trade.ticker_id,  # Will need to join with Ticker
                "pattern": trade.pattern_identified,
                "status": trade.status.value,
                "planned_entry": trade.planned_entry,
                "planned_stop": trade.planned_stop,
                "planned_target": trade.planned_target,
                "created_at": trade.created_at.isoformat()
            }

            if trade.status == TradeStatus.CLOSED:
                trade_dict.update({
                    "net_pnl": trade.net_pnl,
                    "r_multiple": trade.r_multiple,
                    "holding_hours": trade.holding_period_hours
                })

            trade_list.append(trade_dict)

        return {
            "success": True,
            "count": len(trade_list),
            "trades": trade_list
        }

    except Exception as e:
        logger.error(f"Error fetching trades: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/performance")
async def get_performance_analytics(
    user_id: str = "default",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get comprehensive performance analytics

    Includes win rate, R-multiple distribution, best/worst trades, etc.
    """
    try:
        service = get_trade_journal_service(db)

        start_dt = datetime.fromisoformat(start_date) if start_date else None
        end_dt = datetime.fromisoformat(end_date) if end_date else None

        analytics = await service.get_performance_analytics(
            user_id=user_id,
            start_date=start_dt,
            end_date=end_dt
        )

        return {
            "success": True,
            "analytics": analytics
        }

    except Exception as e:
        logger.error(f"Error calculating analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/patterns")
async def get_pattern_performance(
    user_id: str = "default",
    db: AsyncSession = Depends(get_db)
):
    """
    Get performance breakdown by pattern type

    See which patterns work best for you
    """
    try:
        service = get_trade_journal_service(db)
        patterns = await service.get_pattern_performance(user_id=user_id)

        return {
            "success": True,
            "patterns": patterns
        }

    except Exception as e:
        logger.error(f"Error analyzing patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/mistakes")
async def get_mistake_analysis(
    user_id: str = "default",
    db: AsyncSession = Depends(get_db)
):
    """
    Analyze common trading mistakes

    Identify patterns in your mistakes to avoid them
    """
    try:
        service = get_trade_journal_service(db)
        mistakes = await service.get_mistake_analysis(user_id=user_id)

        return {
            "success": True,
            "mistakes": mistakes,
            "total_categories": len(set(m['category'] for m in mistakes))
        }

    except Exception as e:
        logger.error(f"Error analyzing mistakes: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== UTILITY ENDPOINTS ====================

@router.get("/checklist/template")
async def get_checklist_template(pattern: str = "general"):
    """
    Get pre-trade checklist template

    Customize based on pattern type
    """
    templates = {
        "general": {
            "trend_aligned": False,
            "volume_confirmation": False,
            "risk_defined": False,
            "position_sized": False,
            "chart_screenshot": False,
            "thesis_documented": False,
            "stop_set": False,
            "target_set": False
        },
        "VCP": {
            "trend_aligned": False,
            "volume_dry_up": False,
            "contraction_visible": False,
            "tight_consolidation": False,
            "above_21ema": False,
            "rs_strong": False,
            "risk_defined": False,
            "breakout_alert_set": False
        },
        "Cup and Handle": {
            "cup_depth_ok": False,
            "handle_forming": False,
            "volume_pattern_correct": False,
            "pivot_identified": False,
            "trend_aligned": False,
            "rs_strong": False,
            "risk_reward_acceptable": False,
            "breakout_alert_set": False
        }
    }

    template = templates.get(pattern, templates["general"])

    return {
        "success": True,
        "pattern": pattern,
        "checklist": template,
        "items_count": len(template)
    }


@router.get("/emotions")
async def get_emotional_states():
    """Get available emotional states for tracking"""
    return {
        "success": True,
        "emotional_states": [state.value for state in EmotionalState]
    }


@router.get("/market-conditions")
async def get_market_conditions():
    """Get available market conditions for tracking"""
    return {
        "success": True,
        "market_conditions": [condition.value for condition in MarketCondition]
    }


# ==================== EXPORT & REPORTING ENDPOINTS ====================

@router.get("/export/csv")
async def export_trades_csv(
    user_id: str = "default",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Export trades to CSV format

    Download your trade history for Excel/Sheets analysis
    """
    try:
        service = get_reporting_service(db)

        start_dt = datetime.fromisoformat(start_date) if start_date else None
        end_dt = datetime.fromisoformat(end_date) if end_date else None

        csv_content = await service.export_trades_csv(
            user_id=user_id,
            start_date=start_dt,
            end_date=end_dt
        )

        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=trades_export_{datetime.now().strftime('%Y%m%d')}.csv"
            }
        )

    except Exception as e:
        logger.error(f"Error exporting CSV: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export/tax-report")
async def export_tax_report(
    user_id: str = "default",
    year: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Export tax report (IRS Form 8949 compatible)

    Get your trades formatted for tax filing
    """
    try:
        service = get_reporting_service(db)

        csv_content = await service.export_tax_report_csv(
            user_id=user_id,
            year=year
        )

        report_year = year or datetime.now().year

        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=tax_report_{report_year}.csv"
            }
        )

    except Exception as e:
        logger.error(f"Error generating tax report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export/json")
async def export_trades_json(
    user_id: str = "default",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Export trades to JSON format

    Complete trade data with all details
    """
    try:
        service = get_reporting_service(db)

        start_dt = datetime.fromisoformat(start_date) if start_date else None
        end_dt = datetime.fromisoformat(end_date) if end_date else None

        json_data = await service.export_trades_json(
            user_id=user_id,
            start_date=start_dt,
            end_date=end_dt
        )

        return {
            "success": True,
            "export": json_data
        }

    except Exception as e:
        logger.error(f"Error exporting JSON: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reports/performance-letter")
async def get_performance_letter(
    user_id: str = "default",
    period: str = "monthly",
    db: AsyncSession = Depends(get_db)
):
    """
    Generate performance letter

    Professional trading report like a fund manager's monthly letter

    Periods: daily, weekly, monthly, quarterly, yearly
    """
    try:
        service = get_reporting_service(db)

        letter = await service.generate_performance_letter(
            user_id=user_id,
            period=period
        )

        return Response(
            content=letter,
            media_type="text/plain",
            headers={
                "Content-Disposition": f"attachment; filename=performance_letter_{period}_{datetime.now().strftime('%Y%m%d')}.txt"
            }
        )

    except Exception as e:
        logger.error(f"Error generating performance letter: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reports/accountability")
async def get_accountability_report(
    user_id: str = "default",
    db: AsyncSession = Depends(get_db)
):
    """
    Generate accountability report

    Track your discipline, planning, and rule adherence
    """
    try:
        service = get_reporting_service(db)

        report = await service.generate_accountability_report(user_id=user_id)

        return {
            "success": True,
            "accountability_report": report
        }

    except Exception as e:
        logger.error(f"Error generating accountability report: {e}")
        raise HTTPException(status_code=500, detail=str(e))
