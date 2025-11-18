"""
Example: PDF Report Generation

This script demonstrates how to use the PDF report generation system
to create various types of trading reports.
"""

import asyncio
from datetime import datetime, time
from pathlib import Path

# Import report classes
from app.reports import (
    ReportConfig,
    DailyMarketReport,
    WeeklyPortfolioReport,
    TradePlanReport,
    CustomReportBuilder,
    CustomSection,
    SectionType,
    MetricType,
    ReportTemplate,
    TemplateLibrary,
    ReportScheduler,
    ScheduleConfig,
    ScheduleFrequency,
    ReportType,
    DeliveryConfig,
    DeliveryMethod,
    EmailConfig,
    LocalFileConfig,
)


async def example_daily_market_report():
    """Example: Generate a daily market report"""
    print("📊 Generating Daily Market Report...")

    config = ReportConfig(
        title="Daily Market Report",
        subtitle=f"Market Analysis for {datetime.now().strftime('%B %d, %Y')}",
        author="Legend AI Trading Platform",
        theme="professional",
        include_timestamp=True,
    )

    report = DailyMarketReport(config=config)
    await report.fetch_data()

    # Generate PDF
    pdf_buffer = report.generate()

    # Save to file
    output_path = "/tmp/daily_market_report.pdf"
    with open(output_path, "wb") as f:
        f.write(pdf_buffer.getvalue())

    print(f"✅ Daily market report saved to: {output_path}")
    return output_path


async def example_weekly_portfolio_report():
    """Example: Generate a weekly portfolio review"""
    print("📈 Generating Weekly Portfolio Review...")

    config = ReportConfig(
        title="Weekly Portfolio Review",
        subtitle=f"Performance Analysis - Week Ending {datetime.now().strftime('%B %d, %Y')}",
        author="Legend AI Trading Platform",
        theme="professional",
    )

    report = WeeklyPortfolioReport(config=config)
    await report.fetch_data()

    # Generate PDF
    pdf_buffer = report.generate()

    # Save to file
    output_path = "/tmp/weekly_portfolio_report.pdf"
    with open(output_path, "wb") as f:
        f.write(pdf_buffer.getvalue())

    print(f"✅ Weekly portfolio report saved to: {output_path}")
    return output_path


async def example_trade_plan_report():
    """Example: Generate a trade plan report"""
    print("📋 Generating Trade Plan Report...")

    symbol = "AAPL"

    config = ReportConfig(
        title=f"Trade Plan: {symbol}",
        subtitle=f"Detailed Analysis - {datetime.now().strftime('%B %d, %Y')}",
        author="Legend AI Trading Platform",
        theme="professional",
    )

    report = TradePlanReport(
        config=config,
        symbol=symbol,
    )

    # Provide sample data for demonstration
    report.scan_data = {
        'symbol': symbol,
        'pattern_type': 'VCP',
        'score': 8.5,
        'entry_price': 150.00,
        'stop_loss': 145.00,
        'target_price': 165.00,
        'risk_reward_ratio': 3.0,
        'rs_rating': 92.0,
        'criteria_met': ['Price above 21/50/200 EMA', 'RS Rating > 85', 'Volume confirmation'],
    }

    await report.fetch_data()

    # Generate PDF
    pdf_buffer = report.generate()

    # Save to file
    output_path = f"/tmp/trade_plan_{symbol}.pdf"
    with open(output_path, "wb") as f:
        f.write(pdf_buffer.getvalue())

    print(f"✅ Trade plan report saved to: {output_path}")
    return output_path


async def example_custom_report():
    """Example: Build a custom report"""
    print("🎨 Building Custom Report...")

    config = ReportConfig(
        title="My Custom Trading Report",
        subtitle="Personalized Market Analysis",
        author="Legend AI Trading Platform",
        theme="professional",
        primary_color="#1f77b4",
        secondary_color="#2ca02c",
    )

    builder = CustomReportBuilder(config=config)

    # Add metrics section
    builder.add_metric(MetricType.WIN_RATE, 68.5)
    builder.add_metric(MetricType.TOTAL_RETURN, 15.3)
    builder.add_metric(MetricType.SHARPE_RATIO, 1.8)
    builder.add_metric(MetricType.PATTERN_COUNT, 42)

    builder.add_custom_section(CustomSection(
        section_type=SectionType.METRICS,
        title="Performance Metrics",
        order=1,
        config={'metrics': [
            MetricType.WIN_RATE,
            MetricType.TOTAL_RETURN,
            MetricType.SHARPE_RATIO,
            MetricType.PATTERN_COUNT,
        ]},
    ))

    # Add patterns table
    builder.add_custom_section(CustomSection(
        section_type=SectionType.PATTERNS,
        title="Top Patterns This Week",
        order=2,
        data={'patterns': [
            {
                'symbol': 'AAPL',
                'pattern_type': 'VCP',
                'score': 8.5,
                'entry_price': 150.00,
                'target_price': 165.00,
                'stop_loss': 145.00,
            },
            {
                'symbol': 'MSFT',
                'pattern_type': 'Cup & Handle',
                'score': 8.2,
                'entry_price': 380.00,
                'target_price': 410.00,
                'stop_loss': 370.00,
            },
            {
                'symbol': 'NVDA',
                'pattern_type': 'Flat Base',
                'score': 7.8,
                'entry_price': 450.00,
                'target_price': 490.00,
                'stop_loss': 435.00,
            },
        ]},
    ))

    # Add custom notes
    builder.add_custom_section(CustomSection(
        section_type=SectionType.CUSTOM_NOTES,
        title="Market Observations",
        order=3,
        config={'notes': [
            "Strong momentum in technology sector",
            "Several high-quality VCP patterns forming",
            "Market breadth improving week over week",
            "Watch for pullbacks to key support levels",
        ]},
    ))

    # Add watchlist
    builder.add_custom_section(CustomSection(
        section_type=SectionType.WATCHLIST,
        title="Current Watchlist",
        order=4,
        data={'watchlist': [
            {
                'symbol': 'TSLA',
                'name': 'Tesla Inc',
                'price': 250.00,
                'change_pct': 2.5,
                'status': 'Watching',
            },
            {
                'symbol': 'AMD',
                'name': 'Advanced Micro Devices',
                'price': 145.00,
                'change_pct': 1.8,
                'status': 'Breaking Out',
            },
        ]},
    ))

    # Generate PDF
    pdf_buffer = builder.generate()

    # Save to file
    output_path = "/tmp/custom_report.pdf"
    with open(output_path, "wb") as f:
        f.write(pdf_buffer.getvalue())

    print(f"✅ Custom report saved to: {output_path}")
    return output_path


async def example_template_usage():
    """Example: Use a pre-built template"""
    print("📑 Using Pre-built Template...")

    # Get daily summary template
    template = TemplateLibrary.get_daily_summary_template()

    # Create builder and load template
    builder = CustomReportBuilder(config=template.default_config)
    builder.load_template(template)

    # Add some metrics data
    builder.add_metric(MetricType.PATTERN_COUNT, 28)
    builder.add_metric(MetricType.RS_RATING_AVG, 87.5)

    # Generate PDF
    pdf_buffer = builder.generate()

    # Save to file
    output_path = f"/tmp/template_report.pdf"
    with open(output_path, "wb") as f:
        f.write(pdf_buffer.getvalue())

    print(f"✅ Template report saved to: {output_path}")
    return output_path


def example_scheduling():
    """Example: Schedule automated reports"""
    print("⏰ Setting up Report Schedules...")

    scheduler = ReportScheduler()
    scheduler.start()

    # Schedule 1: Daily market report at 9 AM
    daily_schedule = ScheduleConfig(
        schedule_id="daily_market_9am",
        name="Daily Market Report - 9 AM",
        description="Automated daily market report",
        report_type=ReportType.DAILY_MARKET,
        frequency=ScheduleFrequency.DAILY,
        time_of_day=time(9, 0),
        report_config=ReportConfig(
            title="Daily Market Report",
            subtitle="Automated Daily Analysis",
        ),
        delivery_methods=[DeliveryMethod.LOCAL_FILE],
        delivery_config=DeliveryConfig(
            local_file=LocalFileConfig(
                save_path="/tmp/scheduled_reports",
                filename_template="daily_market_{date}.pdf",
            ),
        ),
        archive_enabled=True,
        archive_path="/tmp/report_archive",
    )

    schedule_id = scheduler.add_schedule(daily_schedule)
    print(f"✅ Created daily schedule: {schedule_id}")
    print(f"   Next run: {daily_schedule.next_run}")

    # Schedule 2: Weekly portfolio review on Monday at 8 AM
    weekly_schedule = ScheduleConfig(
        schedule_id="weekly_portfolio_monday",
        name="Weekly Portfolio Review - Monday",
        description="Weekly performance review every Monday",
        report_type=ReportType.WEEKLY_PORTFOLIO,
        frequency=ScheduleFrequency.WEEKLY,
        day_of_week=0,  # Monday
        time_of_day=time(8, 0),
        report_config=ReportConfig(
            title="Weekly Portfolio Review",
        ),
        delivery_methods=[DeliveryMethod.LOCAL_FILE],
        delivery_config=DeliveryConfig(
            local_file=LocalFileConfig(
                save_path="/tmp/scheduled_reports",
                filename_template="weekly_portfolio_{date}.pdf",
            ),
        ),
    )

    schedule_id = scheduler.add_schedule(weekly_schedule)
    print(f"✅ Created weekly schedule: {schedule_id}")
    print(f"   Next run: {weekly_schedule.next_run}")

    # List all schedules
    schedules = scheduler.list_schedules()
    print(f"\n📋 Total schedules: {len(schedules)}")

    return scheduler


async def main():
    """Run all examples"""
    print("=" * 60)
    print("PDF Report Generation Examples")
    print("=" * 60)
    print()

    # Run examples
    await example_daily_market_report()
    print()

    await example_weekly_portfolio_report()
    print()

    await example_trade_plan_report()
    print()

    await example_custom_report()
    print()

    await example_template_usage()
    print()

    # Note: Scheduling example doesn't use async
    scheduler = example_scheduling()
    print()

    print("=" * 60)
    print("✨ All examples completed successfully!")
    print("=" * 60)
    print()
    print("Generated reports are saved in /tmp/")
    print("Check the files:")
    print("  - /tmp/daily_market_report.pdf")
    print("  - /tmp/weekly_portfolio_report.pdf")
    print("  - /tmp/trade_plan_AAPL.pdf")
    print("  - /tmp/custom_report.pdf")
    print("  - /tmp/template_report.pdf")
    print()

    # Cleanup: shutdown scheduler
    scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
