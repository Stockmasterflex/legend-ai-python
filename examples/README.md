# Examples

This directory contains example scripts demonstrating how to use various features of the Legend AI Trading Platform.

## PDF Report Generation

### generate_reports.py

Comprehensive example demonstrating all PDF report generation features:

- **Daily Market Reports** - Generate automated market analysis reports
- **Weekly Portfolio Reviews** - Create performance review reports
- **Trade Plan Reports** - Build detailed trade analysis reports
- **Custom Reports** - Use the report builder to create personalized reports
- **Template Usage** - Leverage pre-built report templates
- **Scheduling** - Set up automated report generation and delivery

**Run the examples:**

```bash
python examples/generate_reports.py
```

**Output:**

The script will generate several PDF reports in `/tmp/`:
- `daily_market_report.pdf`
- `weekly_portfolio_report.pdf`
- `trade_plan_AAPL.pdf`
- `custom_report.pdf`
- `template_report.pdf`

## API Usage Examples

### Using curl

Generate a daily market report:
```bash
curl -X POST http://localhost:8000/api/reports/daily-market \
  -o daily_report.pdf
```

Generate a trade plan:
```bash
curl -X POST http://localhost:8000/api/reports/trade-plan/AAPL \
  -o trade_plan_AAPL.pdf
```

List available templates:
```bash
curl http://localhost:8000/api/reports/templates
```

### Using Python requests

```python
import requests

# Generate daily market report
response = requests.post('http://localhost:8000/api/reports/daily-market')
with open('daily_report.pdf', 'wb') as f:
    f.write(response.content)

# Create a schedule
schedule_data = {
    "schedule_id": "daily_9am",
    "name": "Daily Report - 9 AM",
    "report_type": "daily_market",
    "frequency": "daily",
    "time_of_day": "09:00:00",
    "delivery_methods": ["local_file"],
    "delivery_config": {
        "local_file": {
            "save_path": "/tmp/reports",
            "filename_template": "daily_{date}.pdf"
        }
    }
}

response = requests.post(
    'http://localhost:8000/api/reports/schedules',
    json=schedule_data
)
print(response.json())
```

## More Examples

Check the documentation at `/docs/PDF_REPORTS.md` for more detailed examples and usage patterns.
