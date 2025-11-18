# PDF Report Generation System

Comprehensive PDF report generation for trading analysis with scheduled delivery capabilities.

## Features

### 📊 Report Types

1. **Daily Market Report**
   - Market summary statistics
   - Top movers and shakers
   - Newly detected patterns
   - Sector performance analysis
   - Key support/resistance levels

2. **Weekly Portfolio Review**
   - Performance summary
   - Best and worst trades
   - Pattern success rates
   - Risk metrics analysis
   - Next week outlook

3. **Trade Plan Reports**
   - Entry/exit analysis
   - Risk/reward breakdown
   - Pattern validation
   - Support/resistance levels
   - Multiple timeframe views

4. **Custom Report Builder**
   - Drag-and-drop sections
   - Choose metrics to display
   - Add custom notes
   - Brand with logo
   - Template library

### 📅 Scheduled Delivery

- **Daily/Weekly/Monthly** schedules
- **Custom cron** expressions
- **Email** delivery
- **Google Drive** upload
- **Local file** save
- **Share link** generation
- **Dashboard** archiving

## Quick Start

### 1. Generate a Daily Market Report

```python
from app.reports import DailyMarketReport, ReportConfig
from datetime import datetime

# Configure the report
config = ReportConfig(
    title="Daily Market Report",
    subtitle=f"Market Analysis for {datetime.now().strftime('%B %d, %Y')}",
    author="Legend AI Trading Platform",
    logo_path="/path/to/logo.png",  # Optional
)

# Create and generate report
report = DailyMarketReport(config=config, db=db_session)
await report.fetch_data()

# Generate PDF
pdf_buffer = report.generate()

# Save to file
with open("daily_report.pdf", "wb") as f:
    f.write(pdf_buffer.getvalue())
```

### 2. Generate a Weekly Portfolio Review

```python
from app.reports import WeeklyPortfolioReport, ReportConfig

config = ReportConfig(
    title="Weekly Portfolio Review",
    subtitle="Performance Analysis",
)

report = WeeklyPortfolioReport(config=config, db=db_session)
await report.fetch_data()

pdf_buffer = report.generate()
```

### 3. Generate a Trade Plan Report

```python
from app.reports import TradePlanReport, ReportConfig

config = ReportConfig(
    title="Trade Plan: AAPL",
    subtitle="Detailed Analysis",
)

report = TradePlanReport(
    config=config,
    symbol="AAPL",
    db=db_session
)
await report.fetch_data(scan_id=123)  # Optional: use specific scan

pdf_buffer = report.generate()
```

### 4. Build a Custom Report

```python
from app.reports import (
    CustomReportBuilder,
    ReportConfig,
    CustomSection,
    SectionType,
    MetricType,
)

config = ReportConfig(
    title="My Custom Trading Report",
    theme="professional",
)

builder = CustomReportBuilder(config=config)

# Add metrics section
builder.add_custom_section(CustomSection(
    section_type=SectionType.METRICS,
    title="Performance Metrics",
    order=1,
    config={'metrics': [
        MetricType.WIN_RATE,
        MetricType.TOTAL_RETURN,
        MetricType.SHARPE_RATIO,
    ]},
))

# Add patterns section
builder.add_custom_section(CustomSection(
    section_type=SectionType.PATTERNS,
    title="Top Patterns",
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
        # ... more patterns
    ]},
))

# Add custom notes
builder.add_custom_section(CustomSection(
    section_type=SectionType.CUSTOM_NOTES,
    title="Trade Notes",
    order=3,
    config={'notes': [
        "Excellent market conditions this week",
        "Watch for pullbacks in tech sector",
    ]},
))

pdf_buffer = builder.generate()
```

## API Endpoints

### Generate Reports

```bash
# Daily Market Report
POST /api/reports/daily-market
{
  "date": "2024-01-15T00:00:00Z"  # Optional
}

# Weekly Portfolio Report
POST /api/reports/weekly-portfolio
{
  "week_end": "2024-01-15T00:00:00Z"  # Optional
}

# Trade Plan Report
POST /api/reports/trade-plan/AAPL
{
  "scan_id": 123  # Optional
}

# Custom Report
POST /api/reports/custom
{
  "config": {
    "title": "My Report",
    "theme": "professional"
  },
  "sections": [
    {
      "section_type": "metrics",
      "title": "Performance",
      "order": 1
    }
  ]
}
```

### Schedule Management

```bash
# Create a schedule
POST /api/reports/schedules
{
  "schedule_id": "daily_market_9am",
  "name": "Daily Market Report - 9 AM",
  "report_type": "daily_market",
  "frequency": "daily",
  "time_of_day": "09:00:00",
  "delivery_methods": ["email", "dashboard"],
  "delivery_config": {
    "email": {
      "smtp_host": "smtp.gmail.com",
      "smtp_port": 587,
      "smtp_user": "your-email@gmail.com",
      "smtp_password": "your-app-password",
      "from_email": "reports@tradingplatform.com",
      "to_emails": ["trader@example.com"],
      "subject_template": "Daily Market Report - {date}",
      "body_template": "Please find attached your daily market report."
    }
  }
}

# List all schedules
GET /api/reports/schedules

# Get specific schedule
GET /api/reports/schedules/{schedule_id}

# Update schedule
PUT /api/reports/schedules/{schedule_id}

# Delete schedule
DELETE /api/reports/schedules/{schedule_id}

# Enable/Disable schedule
POST /api/reports/schedules/{schedule_id}/enable
POST /api/reports/schedules/{schedule_id}/disable

# Run schedule immediately
POST /api/reports/schedules/{schedule_id}/run
```

### Template Library

```bash
# List available templates
GET /api/reports/templates

# Get specific template
GET /api/reports/templates/{template_id}

# Generate from template
POST /api/reports/templates/{template_id}/generate
{
  "config_override": {
    "title": "Custom Title"
  }
}
```

## Scheduling Examples

### Daily Report at 9 AM

```python
from app.reports import (
    ScheduleConfig,
    ScheduleFrequency,
    ReportType,
    ReportConfig,
    DeliveryConfig,
    DeliveryMethod,
    EmailConfig,
)
from datetime import time

schedule = ScheduleConfig(
    schedule_id="daily_9am",
    name="Daily Market Report - 9 AM",
    description="Automated daily market report",
    report_type=ReportType.DAILY_MARKET,
    frequency=ScheduleFrequency.DAILY,
    time_of_day=time(9, 0),  # 9:00 AM
    report_config=ReportConfig(
        title="Daily Market Report",
    ),
    delivery_methods=[DeliveryMethod.EMAIL, DeliveryMethod.DASHBOARD],
    delivery_config=DeliveryConfig(
        email=EmailConfig(
            smtp_user="your-email@gmail.com",
            smtp_password="app-password",
            from_email="reports@platform.com",
            to_emails=["trader@example.com"],
        ),
    ),
)

scheduler.add_schedule(schedule)
```

### Weekly Report on Monday

```python
schedule = ScheduleConfig(
    schedule_id="weekly_monday",
    name="Weekly Portfolio Review - Monday 8 AM",
    report_type=ReportType.WEEKLY_PORTFOLIO,
    frequency=ScheduleFrequency.WEEKLY,
    day_of_week=0,  # Monday (0-6)
    time_of_day=time(8, 0),
    # ... other config
)
```

### Monthly Report on 1st of Month

```python
schedule = ScheduleConfig(
    schedule_id="monthly_1st",
    name="Monthly Performance Report",
    report_type=ReportType.WEEKLY_PORTFOLIO,
    frequency=ScheduleFrequency.MONTHLY,
    day_of_month=1,  # 1st of month
    time_of_day=time(10, 0),
    # ... other config
)
```

### Custom Cron Schedule

```python
schedule = ScheduleConfig(
    schedule_id="custom_cron",
    name="Custom Schedule",
    report_type=ReportType.DAILY_MARKET,
    frequency=ScheduleFrequency.CUSTOM_CRON,
    cron_expression="0 9,15 * * 1-5",  # 9 AM and 3 PM, Mon-Fri
    # ... other config
)
```

## Delivery Options

### Email Delivery

```python
from app.reports import EmailConfig, DeliveryConfig

email_config = EmailConfig(
    smtp_host="smtp.gmail.com",
    smtp_port=587,
    smtp_user="your-email@gmail.com",
    smtp_password="your-app-password",
    from_email="reports@platform.com",
    to_emails=["trader1@example.com", "trader2@example.com"],
    cc_emails=["manager@example.com"],
    subject_template="Trading Report - {date}",
    body_template="Please find attached your trading report for {date}.",
)

delivery_config = DeliveryConfig(email=email_config)
```

### Google Drive Upload

```python
from app.reports import GoogleDriveConfig

drive_config = GoogleDriveConfig(
    credentials_path="/path/to/service-account.json",
    folder_id="1234567890abcdef",  # Optional: specific folder
    share_with_emails=["trader@example.com"],
    make_public=False,
)

delivery_config = DeliveryConfig(google_drive=drive_config)
```

### Local File Save

```python
from app.reports import LocalFileConfig

local_config = LocalFileConfig(
    save_path="/home/user/reports",
    filename_template="report_{date}_{type}.pdf",
    create_directories=True,
)

delivery_config = DeliveryConfig(local_file=local_config)
```

### Share Link

```python
from app.reports import ShareLinkConfig

share_config = ShareLinkConfig(
    base_url="https://platform.com/reports",
    expiry_days=7,
    require_auth=True,
)

delivery_config = DeliveryConfig(share_link=share_config)
```

## Customization

### Custom Branding

```python
config = ReportConfig(
    title="My Trading Report",
    author="My Trading Company",
    logo_path="/path/to/logo.png",
    primary_color="#FF6B35",  # Custom primary color
    secondary_color="#004E89",  # Custom secondary color
    accent_color="#F77F00",  # Custom accent color
)
```

### Custom Themes

```python
from app.reports import ReportTheme

config = ReportConfig(
    title="Report",
    theme=ReportTheme.PROFESSIONAL,  # or DARK, MINIMAL, DEFAULT
)
```

### Page Size Options

```python
from app.reports import PageSize

config = ReportConfig(
    title="Report",
    page_size=PageSize.LETTER,  # or A4
)
```

## Template Library

### Pre-built Templates

1. **Daily Summary** - Quick daily market overview
2. **Weekly Performance** - Comprehensive weekly review
3. **Trade Journal** - Detailed trade journal with notes

### Using Templates

```python
from app.reports import TemplateLibrary, CustomReportBuilder

# Get template
template = TemplateLibrary.get_daily_summary_template()

# Load into builder
builder = CustomReportBuilder(config=template.default_config)
builder.load_template(template)

# Generate
pdf_buffer = builder.generate()
```

### Creating Custom Templates

```python
from app.reports import CustomReportBuilder, ReportTemplate

# Build custom report
builder = CustomReportBuilder(config=config)
# ... add sections ...

# Save as template
template = builder.save_template(
    template_id="my_custom_template",
    name="My Custom Template",
    description="Custom report template for daily use",
    tags=["daily", "custom"],
)
```

## Best Practices

1. **Use Scheduling** - Automate regular reports instead of manual generation
2. **Archive Reports** - Enable archiving to maintain historical records
3. **Test Delivery** - Test email/cloud delivery before scheduling
4. **Brand Consistently** - Use consistent logos and colors across reports
5. **Monitor Schedules** - Regularly check schedule execution logs
6. **Cleanup Archives** - Set retention policies to manage storage

## Troubleshooting

### Email Not Sending

- Check SMTP credentials
- Verify SMTP host and port
- Enable "Less secure app access" for Gmail
- Use app-specific passwords

### Google Drive Upload Failing

- Verify service account credentials
- Check folder permissions
- Ensure Drive API is enabled

### Report Generation Errors

- Check database connection
- Verify data availability
- Review error logs
- Test with sample data

## Performance

- **Generation Time**: 2-5 seconds per report
- **PDF Size**: Typically 200-500 KB
- **Concurrent Generation**: Supports multiple simultaneous reports
- **Caching**: Utilizes existing data caching infrastructure

## Security

- **Credentials**: Store SMTP/API credentials securely
- **Access Control**: Implement authentication for report endpoints
- **Data Privacy**: Reports may contain sensitive trading data
- **Encryption**: Use TLS for email delivery
- **Expiration**: Set expiration on share links

## Support

For issues or questions:
- Check the [API Documentation](/docs)
- Review error logs
- Contact support

## License

Copyright © 2024 Legend AI Trading Platform
