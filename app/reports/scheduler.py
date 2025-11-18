"""
Report Scheduling System

Provides scheduled report generation and delivery:
- Daily/Weekly/Monthly schedules
- Cron-like scheduling
- Automatic delivery via email/cloud
- Archive management
"""

from datetime import datetime, time, timedelta
from typing import Dict, List, Optional, Any, Callable
from enum import Enum

from pydantic import BaseModel, Field
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.job import Job
import asyncio
import logging

from .base import ReportConfig
from .daily_market import DailyMarketReport
from .weekly_portfolio import WeeklyPortfolioReport
from .trade_plan import TradePlanReport
from .custom_builder import CustomReportBuilder, ReportTemplate
from .delivery import ReportDelivery, DeliveryConfig, DeliveryMethod

logger = logging.getLogger(__name__)


class ScheduleFrequency(str, Enum):
    """Schedule frequency options"""
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM_CRON = "custom_cron"


class ReportType(str, Enum):
    """Types of reports that can be scheduled"""
    DAILY_MARKET = "daily_market"
    WEEKLY_PORTFOLIO = "weekly_portfolio"
    TRADE_PLAN = "trade_plan"
    CUSTOM = "custom"


class ScheduleConfig(BaseModel):
    """Configuration for scheduled reports"""
    schedule_id: str
    name: str
    description: Optional[str] = None
    report_type: ReportType
    frequency: ScheduleFrequency

    # Report configuration
    report_config: ReportConfig
    report_params: Dict[str, Any] = Field(default_factory=dict)

    # Scheduling details
    time_of_day: Optional[time] = None  # For daily/weekly/monthly
    day_of_week: Optional[int] = None  # 0-6 for Monday-Sunday (weekly)
    day_of_month: Optional[int] = None  # 1-31 (monthly)
    cron_expression: Optional[str] = None  # For custom schedules

    # Delivery configuration
    delivery_methods: List[DeliveryMethod] = Field(default_factory=list)
    delivery_config: DeliveryConfig

    # Archive settings
    archive_enabled: bool = True
    archive_path: str = "/tmp/report_archive"
    retention_days: int = 30

    # Metadata
    enabled: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    run_count: int = 0


class ReportScheduler:
    """Manages scheduled report generation and delivery"""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.schedules: Dict[str, ScheduleConfig] = {}
        self.jobs: Dict[str, Job] = {}
        self.delivery = ReportDelivery()

    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Report scheduler started")

    def shutdown(self):
        """Shutdown the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Report scheduler shutdown")

    def add_schedule(self, schedule: ScheduleConfig) -> str:
        """Add a new scheduled report"""
        # Store the schedule
        self.schedules[schedule.schedule_id] = schedule

        # Create the job
        if schedule.enabled:
            self._create_job(schedule)

        logger.info(f"Added schedule: {schedule.name} ({schedule.schedule_id})")
        return schedule.schedule_id

    def remove_schedule(self, schedule_id: str):
        """Remove a scheduled report"""
        if schedule_id in self.schedules:
            # Remove the job
            if schedule_id in self.jobs:
                self.jobs[schedule_id].remove()
                del self.jobs[schedule_id]

            # Remove the schedule
            del self.schedules[schedule_id]
            logger.info(f"Removed schedule: {schedule_id}")

    def update_schedule(self, schedule_id: str, schedule: ScheduleConfig):
        """Update an existing schedule"""
        if schedule_id in self.schedules:
            # Remove old job
            if schedule_id in self.jobs:
                self.jobs[schedule_id].remove()
                del self.jobs[schedule_id]

            # Update schedule
            self.schedules[schedule_id] = schedule

            # Create new job if enabled
            if schedule.enabled:
                self._create_job(schedule)

            logger.info(f"Updated schedule: {schedule.name} ({schedule_id})")

    def enable_schedule(self, schedule_id: str):
        """Enable a schedule"""
        if schedule_id in self.schedules:
            schedule = self.schedules[schedule_id]
            schedule.enabled = True

            if schedule_id not in self.jobs:
                self._create_job(schedule)

            logger.info(f"Enabled schedule: {schedule_id}")

    def disable_schedule(self, schedule_id: str):
        """Disable a schedule"""
        if schedule_id in self.schedules:
            schedule = self.schedules[schedule_id]
            schedule.enabled = False

            if schedule_id in self.jobs:
                self.jobs[schedule_id].remove()
                del self.jobs[schedule_id]

            logger.info(f"Disabled schedule: {schedule_id}")

    def get_schedule(self, schedule_id: str) -> Optional[ScheduleConfig]:
        """Get a schedule by ID"""
        return self.schedules.get(schedule_id)

    def list_schedules(self, enabled_only: bool = False) -> List[ScheduleConfig]:
        """List all schedules"""
        schedules = list(self.schedules.values())
        if enabled_only:
            schedules = [s for s in schedules if s.enabled]
        return schedules

    def run_now(self, schedule_id: str) -> bool:
        """Run a scheduled report immediately"""
        if schedule_id in self.schedules:
            schedule = self.schedules[schedule_id]
            asyncio.create_task(self._generate_and_deliver(schedule))
            logger.info(f"Manually triggered schedule: {schedule_id}")
            return True
        return False

    def _create_job(self, schedule: ScheduleConfig):
        """Create a scheduler job for the schedule"""
        trigger = self._create_trigger(schedule)

        job = self.scheduler.add_job(
            func=self._generate_and_deliver,
            trigger=trigger,
            args=[schedule],
            id=schedule.schedule_id,
            name=schedule.name,
            replace_existing=True,
        )

        self.jobs[schedule.schedule_id] = job

        # Update next run time
        if job.next_run_time:
            schedule.next_run = job.next_run_time

        logger.info(f"Created job for schedule: {schedule.name}, next run: {job.next_run_time}")

    def _create_trigger(self, schedule: ScheduleConfig):
        """Create appropriate trigger based on schedule frequency"""
        if schedule.frequency == ScheduleFrequency.ONCE:
            # One-time execution
            run_date = schedule.report_params.get('run_date', datetime.now())
            return DateTrigger(run_date=run_date)

        elif schedule.frequency == ScheduleFrequency.DAILY:
            # Daily at specified time
            hour = schedule.time_of_day.hour if schedule.time_of_day else 9
            minute = schedule.time_of_day.minute if schedule.time_of_day else 0

            return CronTrigger(
                hour=hour,
                minute=minute,
            )

        elif schedule.frequency == ScheduleFrequency.WEEKLY:
            # Weekly on specified day
            hour = schedule.time_of_day.hour if schedule.time_of_day else 9
            minute = schedule.time_of_day.minute if schedule.time_of_day else 0
            day_of_week = schedule.day_of_week or 0  # Monday by default

            return CronTrigger(
                day_of_week=day_of_week,
                hour=hour,
                minute=minute,
            )

        elif schedule.frequency == ScheduleFrequency.MONTHLY:
            # Monthly on specified day
            hour = schedule.time_of_day.hour if schedule.time_of_day else 9
            minute = schedule.time_of_day.minute if schedule.time_of_day else 0
            day = schedule.day_of_month or 1

            return CronTrigger(
                day=day,
                hour=hour,
                minute=minute,
            )

        elif schedule.frequency == ScheduleFrequency.CUSTOM_CRON:
            # Custom cron expression
            if not schedule.cron_expression:
                raise ValueError("cron_expression required for CUSTOM_CRON frequency")

            # Parse cron expression
            parts = schedule.cron_expression.split()
            if len(parts) != 5:
                raise ValueError("Invalid cron expression")

            minute, hour, day, month, day_of_week = parts

            return CronTrigger(
                minute=minute,
                hour=hour,
                day=day,
                month=month,
                day_of_week=day_of_week,
            )

        else:
            raise ValueError(f"Unsupported frequency: {schedule.frequency}")

    async def _generate_and_deliver(self, schedule: ScheduleConfig):
        """Generate report and deliver it"""
        try:
            logger.info(f"Generating scheduled report: {schedule.name}")

            # Generate the report
            report_buffer = await self._generate_report(schedule)

            if not report_buffer:
                logger.error(f"Failed to generate report: {schedule.name}")
                return

            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{schedule.report_type.value}_{timestamp}.pdf"

            # Archive if enabled
            if schedule.archive_enabled:
                archive_path = f"{schedule.archive_path}/{filename}"
                with open(archive_path, 'wb') as f:
                    f.write(report_buffer.getvalue())
                logger.info(f"Archived report: {archive_path}")

            # Deliver via configured methods
            for method in schedule.delivery_methods:
                success = await self.delivery.deliver(
                    report_buffer=report_buffer,
                    filename=filename,
                    method=method,
                    config=schedule.delivery_config,
                )

                if success:
                    logger.info(f"Delivered report via {method}: {filename}")
                else:
                    logger.error(f"Failed to deliver report via {method}: {filename}")

            # Update schedule metadata
            schedule.last_run = datetime.now()
            schedule.run_count += 1

            # Update next run time
            if schedule.schedule_id in self.jobs:
                job = self.jobs[schedule.schedule_id]
                if job.next_run_time:
                    schedule.next_run = job.next_run_time

            logger.info(f"Successfully completed scheduled report: {schedule.name}")

        except Exception as e:
            logger.error(f"Error generating scheduled report {schedule.name}: {e}", exc_info=True)

    async def _generate_report(self, schedule: ScheduleConfig):
        """Generate the report based on type"""
        try:
            if schedule.report_type == ReportType.DAILY_MARKET:
                report = DailyMarketReport(
                    config=schedule.report_config,
                    db=schedule.report_params.get('db'),
                )
                await report.fetch_data()
                return report.generate()

            elif schedule.report_type == ReportType.WEEKLY_PORTFOLIO:
                report = WeeklyPortfolioReport(
                    config=schedule.report_config,
                    db=schedule.report_params.get('db'),
                )
                await report.fetch_data()
                return report.generate()

            elif schedule.report_type == ReportType.TRADE_PLAN:
                report = TradePlanReport(
                    config=schedule.report_config,
                    symbol=schedule.report_params.get('symbol', ''),
                    db=schedule.report_params.get('db'),
                )
                await report.fetch_data(
                    scan_id=schedule.report_params.get('scan_id')
                )
                return report.generate()

            elif schedule.report_type == ReportType.CUSTOM:
                report = CustomReportBuilder(config=schedule.report_config)

                # Load template if specified
                template = schedule.report_params.get('template')
                if template:
                    report.load_template(template)

                # Add custom sections
                sections = schedule.report_params.get('sections', [])
                for section in sections:
                    report.add_custom_section(section)

                return report.generate()

            else:
                logger.error(f"Unknown report type: {schedule.report_type}")
                return None

        except Exception as e:
            logger.error(f"Error generating report: {e}", exc_info=True)
            return None

    def cleanup_archives(self, schedule_id: str):
        """Clean up old archived reports based on retention policy"""
        if schedule_id not in self.schedules:
            return

        schedule = self.schedules[schedule_id]

        if not schedule.archive_enabled:
            return

        import os
        from pathlib import Path

        archive_dir = Path(schedule.archive_path)
        if not archive_dir.exists():
            return

        # Calculate cutoff date
        cutoff_date = datetime.now() - timedelta(days=schedule.retention_days)

        # Clean up old files
        deleted_count = 0
        for file_path in archive_dir.glob(f"{schedule.report_type.value}_*.pdf"):
            if file_path.stat().st_mtime < cutoff_date.timestamp():
                file_path.unlink()
                deleted_count += 1

        if deleted_count > 0:
            logger.info(f"Cleaned up {deleted_count} archived reports for {schedule_id}")
