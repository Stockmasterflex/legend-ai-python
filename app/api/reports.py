"""
Reports API Router

FastAPI endpoints for PDF report generation and management:
- Generate daily/weekly/trade plan reports
- Custom report builder
- Schedule management
- Delivery configuration
- Template library
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Response
from fastapi.responses import StreamingResponse
from typing import List, Optional
from datetime import datetime, time
from io import BytesIO

from ..reports import (
    ReportConfig,
    DailyMarketReport,
    WeeklyPortfolioReport,
    TradePlanReport,
    CustomReportBuilder,
    CustomSection,
    ReportTemplate,
    TemplateLibrary,
    ReportScheduler,
    ScheduleConfig,
    ScheduleFrequency,
    ReportType,
    ReportDelivery,
    DeliveryConfig,
    DeliveryMethod,
)
from ..services.database import get_db
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/reports", tags=["reports"])

# Global scheduler instance
report_scheduler = ReportScheduler()


@router.on_event("startup")
async def start_scheduler():
    """Start the report scheduler on app startup"""
    report_scheduler.start()
    logger.info("Report scheduler started")


@router.on_event("shutdown")
async def shutdown_scheduler():
    """Shutdown the report scheduler on app shutdown"""
    report_scheduler.shutdown()
    logger.info("Report scheduler shutdown")


# ============================================================================
# Daily Market Reports
# ============================================================================

@router.post("/daily-market", response_class=StreamingResponse)
async def generate_daily_market_report(
    date: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    """
    Generate a daily market report

    Returns PDF file with:
    - Market summary
    - Top movers
    - New patterns detected
    - Sector performance
    - Key levels to watch
    """
    try:
        config = ReportConfig(
            title="Daily Market Report",
            subtitle=f"Market Analysis for {(date or datetime.now()).strftime('%B %d, %Y')}",
        )

        report = DailyMarketReport(config=config, db=db, date=date)
        await report.fetch_data()

        pdf_buffer = report.generate()

        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=daily_market_report_{datetime.now().strftime('%Y%m%d')}.pdf"
            }
        )

    except Exception as e:
        logger.error(f"Error generating daily market report: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Weekly Portfolio Reports
# ============================================================================

@router.post("/weekly-portfolio", response_class=StreamingResponse)
async def generate_weekly_portfolio_report(
    week_end: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    """
    Generate a weekly portfolio review report

    Returns PDF file with:
    - Performance summary
    - Best/worst trades
    - Pattern success rates
    - Risk metrics
    - Next week outlook
    """
    try:
        config = ReportConfig(
            title="Weekly Portfolio Review",
            subtitle=f"Performance Analysis - Week Ending {(week_end or datetime.now()).strftime('%B %d, %Y')}",
        )

        report = WeeklyPortfolioReport(config=config, db=db, week_end=week_end)
        await report.fetch_data()

        pdf_buffer = report.generate()

        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=weekly_portfolio_report_{datetime.now().strftime('%Y%m%d')}.pdf"
            }
        )

    except Exception as e:
        logger.error(f"Error generating weekly portfolio report: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Trade Plan Reports
# ============================================================================

@router.post("/trade-plan/{symbol}", response_class=StreamingResponse)
async def generate_trade_plan_report(
    symbol: str,
    scan_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
    Generate a detailed trade plan report for a specific symbol

    Returns PDF file with:
    - Entry/exit analysis
    - Risk/reward breakdown
    - Pattern validation
    - Support/resistance levels
    - Multiple timeframe views
    """
    try:
        config = ReportConfig(
            title=f"Trade Plan: {symbol}",
            subtitle=f"Detailed Analysis - {datetime.now().strftime('%B %d, %Y')}",
        )

        report = TradePlanReport(config=config, symbol=symbol, db=db)
        await report.fetch_data(scan_id=scan_id)

        pdf_buffer = report.generate()

        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=trade_plan_{symbol}_{datetime.now().strftime('%Y%m%d')}.pdf"
            }
        )

    except Exception as e:
        logger.error(f"Error generating trade plan report: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Custom Report Builder
# ============================================================================

@router.post("/custom", response_class=StreamingResponse)
async def generate_custom_report(
    config: ReportConfig,
    sections: List[CustomSection],
):
    """
    Generate a custom report with user-defined sections

    Allows flexible report creation with:
    - Drag-and-drop section ordering
    - Multiple section types (text, table, chart, metrics, etc.)
    - Custom styling and branding
    """
    try:
        report = CustomReportBuilder(config=config)

        for section in sections:
            report.add_custom_section(section)

        pdf_buffer = report.generate()

        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=custom_report_{datetime.now().strftime('%Y%m%d')}.pdf"
            }
        )

    except Exception as e:
        logger.error(f"Error generating custom report: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Template Library
# ============================================================================

@router.get("/templates", response_model=List[ReportTemplate])
async def list_templates():
    """List all available report templates"""
    try:
        templates = TemplateLibrary.list_templates()
        return templates

    except Exception as e:
        logger.error(f"Error listing templates: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates/{template_id}", response_model=ReportTemplate)
async def get_template(template_id: str):
    """Get a specific template by ID"""
    try:
        templates = TemplateLibrary.list_templates()
        template = next((t for t in templates if t.template_id == template_id), None)

        if not template:
            raise HTTPException(status_code=404, detail="Template not found")

        return template

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting template: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/templates/{template_id}/generate", response_class=StreamingResponse)
async def generate_from_template(
    template_id: str,
    config_override: Optional[ReportConfig] = None,
):
    """Generate a report from a saved template"""
    try:
        templates = TemplateLibrary.list_templates()
        template = next((t for t in templates if t.template_id == template_id), None)

        if not template:
            raise HTTPException(status_code=404, detail="Template not found")

        # Use override config or template default
        config = config_override or template.default_config

        report = CustomReportBuilder(config=config)
        report.load_template(template)

        pdf_buffer = report.generate()

        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={template_id}_{datetime.now().strftime('%Y%m%d')}.pdf"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating report from template: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Schedule Management
# ============================================================================

@router.post("/schedules", response_model=dict)
async def create_schedule(schedule: ScheduleConfig):
    """Create a new scheduled report"""
    try:
        schedule_id = report_scheduler.add_schedule(schedule)
        return {
            "schedule_id": schedule_id,
            "message": "Schedule created successfully",
            "next_run": schedule.next_run,
        }

    except Exception as e:
        logger.error(f"Error creating schedule: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/schedules", response_model=List[ScheduleConfig])
async def list_schedules(enabled_only: bool = False):
    """List all scheduled reports"""
    try:
        schedules = report_scheduler.list_schedules(enabled_only=enabled_only)
        return schedules

    except Exception as e:
        logger.error(f"Error listing schedules: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/schedules/{schedule_id}", response_model=ScheduleConfig)
async def get_schedule(schedule_id: str):
    """Get a specific schedule"""
    try:
        schedule = report_scheduler.get_schedule(schedule_id)

        if not schedule:
            raise HTTPException(status_code=404, detail="Schedule not found")

        return schedule

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting schedule: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/schedules/{schedule_id}", response_model=dict)
async def update_schedule(schedule_id: str, schedule: ScheduleConfig):
    """Update an existing schedule"""
    try:
        existing = report_scheduler.get_schedule(schedule_id)

        if not existing:
            raise HTTPException(status_code=404, detail="Schedule not found")

        report_scheduler.update_schedule(schedule_id, schedule)

        return {
            "schedule_id": schedule_id,
            "message": "Schedule updated successfully",
            "next_run": schedule.next_run,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating schedule: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/schedules/{schedule_id}", response_model=dict)
async def delete_schedule(schedule_id: str):
    """Delete a schedule"""
    try:
        existing = report_scheduler.get_schedule(schedule_id)

        if not existing:
            raise HTTPException(status_code=404, detail="Schedule not found")

        report_scheduler.remove_schedule(schedule_id)

        return {
            "schedule_id": schedule_id,
            "message": "Schedule deleted successfully",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting schedule: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/schedules/{schedule_id}/enable", response_model=dict)
async def enable_schedule(schedule_id: str):
    """Enable a schedule"""
    try:
        existing = report_scheduler.get_schedule(schedule_id)

        if not existing:
            raise HTTPException(status_code=404, detail="Schedule not found")

        report_scheduler.enable_schedule(schedule_id)

        return {
            "schedule_id": schedule_id,
            "message": "Schedule enabled successfully",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enabling schedule: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/schedules/{schedule_id}/disable", response_model=dict)
async def disable_schedule(schedule_id: str):
    """Disable a schedule"""
    try:
        existing = report_scheduler.get_schedule(schedule_id)

        if not existing:
            raise HTTPException(status_code=404, detail="Schedule not found")

        report_scheduler.disable_schedule(schedule_id)

        return {
            "schedule_id": schedule_id,
            "message": "Schedule disabled successfully",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error disabling schedule: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/schedules/{schedule_id}/run", response_model=dict)
async def run_schedule_now(schedule_id: str):
    """Run a scheduled report immediately"""
    try:
        success = report_scheduler.run_now(schedule_id)

        if not success:
            raise HTTPException(status_code=404, detail="Schedule not found")

        return {
            "schedule_id": schedule_id,
            "message": "Schedule triggered successfully",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error running schedule: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Report Delivery
# ============================================================================

@router.post("/deliver", response_model=dict)
async def deliver_report(
    report_type: ReportType,
    delivery_methods: List[DeliveryMethod],
    delivery_config: DeliveryConfig,
    background_tasks: BackgroundTasks,
    symbol: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Generate and deliver a report via specified methods

    Supports:
    - Email delivery
    - Google Drive upload
    - Local file save
    - Share link generation
    - Dashboard archiving
    """
    try:
        # Generate the report
        config = ReportConfig(title=f"{report_type.value} Report")

        if report_type == ReportType.DAILY_MARKET:
            report = DailyMarketReport(config=config, db=db)
            await report.fetch_data()
            pdf_buffer = report.generate()
            filename = f"daily_market_{datetime.now().strftime('%Y%m%d')}.pdf"

        elif report_type == ReportType.WEEKLY_PORTFOLIO:
            report = WeeklyPortfolioReport(config=config, db=db)
            await report.fetch_data()
            pdf_buffer = report.generate()
            filename = f"weekly_portfolio_{datetime.now().strftime('%Y%m%d')}.pdf"

        elif report_type == ReportType.TRADE_PLAN:
            if not symbol:
                raise HTTPException(status_code=400, detail="Symbol required for trade plan report")

            report = TradePlanReport(config=config, symbol=symbol, db=db)
            await report.fetch_data()
            pdf_buffer = report.generate()
            filename = f"trade_plan_{symbol}_{datetime.now().strftime('%Y%m%d')}.pdf"

        else:
            raise HTTPException(status_code=400, detail="Invalid report type")

        # Deliver via specified methods
        delivery = ReportDelivery()
        results = []

        for method in delivery_methods:
            success = await delivery.deliver(
                report_buffer=pdf_buffer,
                filename=filename,
                method=method,
                config=delivery_config,
            )
            results.append({
                "method": method,
                "success": success,
            })

        return {
            "message": "Report delivered",
            "results": results,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error delivering report: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
