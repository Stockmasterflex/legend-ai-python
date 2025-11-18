# Google Sheets Integration Guide

## Overview

Legend AI now includes comprehensive bidirectional Google Sheets integration, enabling real-time synchronization of:

1. **Watchlist** - Track stocks with two-way sync
2. **Pattern Results** - Export daily pattern scans
3. **Trade Journal** - Log trades with P&L tracking
4. **Portfolio** - Import/export holdings with risk metrics
5. **Custom Dashboards** - Real-time data with formulas

## Features

### ✅ Bidirectional Sync
- Export data from app → Google Sheets
- Import data from Google Sheets → app
- Automatic conflict resolution
- Background sync tasks

### ✅ Real-Time Updates
- Configurable sync intervals (default: 5 minutes)
- Manual sync on-demand via API
- Batch processing for efficiency

### ✅ Multiple Sheet Support
- Each feature can use a separate Google Sheet
- Or combine all in one sheet with multiple tabs
- Flexible configuration

### ✅ Rich Formatting
- Color-coded headers
- Conditional formatting for scores
- Professional styling
- Auto-sized columns

## Setup Instructions

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable **Google Sheets API**
4. Enable **Google Drive API**

### 2. Create Service Account

1. Navigate to **IAM & Admin > Service Accounts**
2. Click **Create Service Account**
3. Name it `legend-ai-sheets` and create
4. Click on the service account
5. Go to **Keys** tab
6. Click **Add Key > Create New Key**
7. Select **JSON** format
8. Download the JSON file

### 3. Share Google Sheets

1. Create Google Sheets for each feature (or use one sheet with multiple tabs)
2. Share each sheet with the service account email (found in JSON file)
   - Example: `legend-ai-sheets@your-project.iam.gserviceaccount.com`
3. Give **Editor** permissions
4. Copy the Sheet ID from the URL:
   - URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`

### 4. Configure Environment Variables

Add to your `.env` file:

```bash
# Enable Google Sheets integration
GOOGLE_SHEETS_ENABLED=true

# Service account credentials (JSON string or file path)
GOOGLE_SHEETS_CREDENTIALS_JSON=/path/to/service-account.json
# OR as JSON string (for Railway/Heroku):
# GOOGLE_SHEETS_CREDENTIALS_JSON='{"type":"service_account","project_id":"...","private_key":"..."}'

# Sheet IDs for each feature
GOOGLE_SHEETS_WATCHLIST_ID=your-watchlist-sheet-id
GOOGLE_SHEETS_PATTERNS_ID=your-patterns-sheet-id
GOOGLE_SHEETS_TRADES_ID=your-trades-sheet-id
GOOGLE_SHEETS_PORTFOLIO_ID=your-portfolio-sheet-id
GOOGLE_SHEETS_DASHBOARD_ID=your-dashboard-sheet-id

# Optional: Sync configuration
GOOGLE_SHEETS_SYNC_INTERVAL=300  # seconds (default: 5 minutes)
GOOGLE_SHEETS_BATCH_SIZE=100     # rows per batch
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

The following packages are now included:
- `google-auth==2.35.0`
- `google-auth-oauthlib==1.2.1`
- `google-api-python-client==2.149.0`
- `gspread==6.1.3`
- `gspread-asyncio==1.9.2`

### 6. Run Database Migration

```bash
# Create migration
alembic revision --autogenerate -m "Add Google Sheets integration models"

# Apply migration
alembic upgrade head
```

This adds the following tables:
- `trades` - Trade journal entries
- `portfolios` - Portfolio holdings
- `sheet_syncs` - Sync tracking/audit log

## API Endpoints

### Health Check

```bash
GET /api/sheets/health
```

Check if Google Sheets integration is configured and working.

**Response:**
```json
{
  "status": "healthy",
  "message": "Google Sheets integration is working",
  "configured_sheets": {
    "watchlist": true,
    "patterns": true,
    "trades": true,
    "portfolio": true,
    "dashboard": true
  }
}
```

### Watchlist Sync

#### Export Watchlist
```bash
POST /api/sheets/watchlist/export
```

Exports current watchlist to Google Sheet.

#### Import Watchlist
```bash
POST /api/sheets/watchlist/import
```

Imports watchlist from Google Sheet.

#### Bidirectional Sync
```bash
POST /api/sheets/watchlist/sync
Content-Type: application/json

{
  "direction": "bidirectional"
}
```

**Directions:**
- `to_sheet` - Export only
- `from_sheet` - Import only
- `bidirectional` - Both ways

### Pattern Results

```bash
POST /api/sheets/patterns/export
Content-Type: application/json

{
  "days": 7
}
```

Exports pattern scan results from the last N days.

**Sheet Columns:**
- Date, Ticker, Pattern Type, Score
- Current Price, Entry, Stop, Target
- Risk/Reward Ratio
- Volume Dry Up, Consolidation Days
- RS Rating, Analysis, Chart URL

### Trade Journal

```bash
POST /api/sheets/trades/export
```

Exports all trades with performance statistics.

**Sheet Sections:**
1. **Trade Log** - All entries and exits
2. **Statistics Summary** - Win rate, P&L, R-multiples

**Columns:**
- Trade ID, Ticker, Entry/Exit Dates
- Entry/Exit Prices, Stop Loss, Target
- Position Size, Risk Amount
- P&L ($), P&L (%), R-Multiple
- Win/Loss, Notes

### Portfolio Tracking

#### Export Portfolio
```bash
POST /api/sheets/portfolio/export
```

Exports current holdings with risk metrics.

**Columns:**
- Ticker, Shares, Avg Cost
- Current Price, Market Value
- Cost Basis, Unrealized P&L ($), Unrealized P&L (%)
- Position Size %, Risk Amount
- Stop Loss, Target Price
- Acquired Date, Notes

#### Import Portfolio
```bash
POST /api/sheets/portfolio/import
```

Imports holdings from Google Sheet (for manual entry).

#### Bidirectional Sync
```bash
POST /api/sheets/portfolio/sync
Content-Type: application/json

{
  "direction": "bidirectional"
}
```

### Custom Dashboard

```bash
POST /api/sheets/dashboard/create
```

Creates a multi-tab dashboard with:

**Tab 1: Overview**
- Quick stats (watchlist count, patterns, active trades)
- Market status
- Last updated timestamp

**Tab 2: Top Patterns**
- 20 highest-scoring patterns from last 7 days
- Ticker, pattern type, score, entry, target, R/R ratio

**Tab 3: Active Trades**
- All open positions
- Ticker, entry, stop, target, size, risk, days open

**Tab 4: Performance**
- Total trades, win rate
- Total P&L, average win/loss
- Profit factor

#### Refresh Dashboard
```bash
POST /api/sheets/dashboard/refresh
```

Updates all dashboard tabs with latest data.

### Sync All

```bash
POST /api/sheets/sync-all
```

Syncs all configured sheets in one call (runs in background).

**Response:**
```json
{
  "status": "queued",
  "message": "Full sync started in background",
  "note": "Check /api/sheets/status for sync progress"
}
```

### Sync Status

```bash
GET /api/sheets/status
```

Get status of all sheet syncs.

**Response:**
```json
{
  "enabled": true,
  "syncs": [
    {
      "sheet_type": "watchlist",
      "sheet_id": "abc123...",
      "last_sync": "2025-01-15T10:30:00Z",
      "direction": "to_sheet",
      "records": 25,
      "status": "success",
      "error": null
    }
  ],
  "configuration": {
    "watchlist_id": "abc123...",
    "patterns_id": "def456...",
    "sync_interval": 300
  }
}
```

## Usage Examples

### Python

```python
import requests

# Base URL
base_url = "https://your-api.com"

# Export watchlist
response = requests.post(f"{base_url}/api/sheets/watchlist/export")
print(response.json())
# {"status": "success", "records": 25, "sheet_id": "..."}

# Bidirectional portfolio sync
response = requests.post(
    f"{base_url}/api/sheets/portfolio/sync",
    json={"direction": "bidirectional"}
)
print(response.json())

# Export last 30 days of patterns
response = requests.post(
    f"{base_url}/api/sheets/patterns/export",
    json={"days": 30}
)
print(response.json())

# Create dashboard
response = requests.post(f"{base_url}/api/sheets/dashboard/create")
print(response.json())

# Sync everything
response = requests.post(f"{base_url}/api/sheets/sync-all")
print(response.json())
```

### cURL

```bash
# Export watchlist
curl -X POST https://your-api.com/api/sheets/watchlist/export

# Bidirectional sync
curl -X POST https://your-api.com/api/sheets/watchlist/sync \
  -H "Content-Type: application/json" \
  -d '{"direction": "bidirectional"}'

# Export patterns
curl -X POST https://your-api.com/api/sheets/patterns/export \
  -H "Content-Type: application/json" \
  -d '{"days": 7}'

# Sync all
curl -X POST https://your-api.com/api/sheets/sync-all

# Check status
curl https://your-api.com/api/sheets/status
```

### JavaScript/Node.js

```javascript
// Export watchlist
const response = await fetch('https://your-api.com/api/sheets/watchlist/export', {
  method: 'POST'
});
const result = await response.json();
console.log(result);

// Bidirectional portfolio sync
const syncResponse = await fetch('https://your-api.com/api/sheets/portfolio/sync', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ direction: 'bidirectional' })
});

// Create dashboard
const dashboardResponse = await fetch('https://your-api.com/api/sheets/dashboard/create', {
  method: 'POST'
});
```

## Automation with Cron/Scheduler

### Option 1: External Cron Job

```bash
# Add to crontab (every 5 minutes)
*/5 * * * * curl -X POST https://your-api.com/api/sheets/sync-all
```

### Option 2: GitHub Actions

```yaml
name: Sync Google Sheets
on:
  schedule:
    - cron: '*/5 * * * *'  # Every 5 minutes
  workflow_dispatch:  # Manual trigger

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Sync All Sheets
        run: |
          curl -X POST https://your-api.com/api/sheets/sync-all
```

### Option 3: n8n Workflow

1. Create new workflow in n8n
2. Add **Schedule Trigger** (every 5 minutes)
3. Add **HTTP Request** node:
   - Method: POST
   - URL: `https://your-api.com/api/sheets/sync-all`
4. Activate workflow

## Google Sheets Formulas

You can add custom formulas to your sheets for advanced calculations:

### Calculate Total Portfolio Value

```
=SUM(E2:E100)  # Sum of Market Value column
```

### Calculate Win Rate

```
=COUNTIF(O2:O100,"WIN")/COUNTA(O2:O100)*100
```

### Conditional Formatting

**Highlight High-Score Patterns (8-10):**
1. Select score column (D2:D100)
2. Format > Conditional formatting
3. Format cells if: `Greater than or equal to` 8
4. Green background

**Highlight Losing Trades:**
1. Select P&L column
2. Format cells if: `Less than` 0
3. Red background

## Troubleshooting

### "Google Sheets integration is disabled"
- Set `GOOGLE_SHEETS_ENABLED=true` in `.env`
- Restart the application

### "Failed to initialize Google Sheets service"
- Check service account JSON is valid
- Verify JSON path or ensure JSON string is properly escaped
- Check logs for detailed error message

### "Permission denied" errors
- Verify sheet is shared with service account email
- Ensure service account has **Editor** permissions
- Check Sheet ID is correct

### "Sheet not found"
- Verify Sheet ID in environment variables
- Ensure sheet wasn't deleted
- Check you're using the right Sheet ID (from URL)

### Slow sync performance
- Reduce `GOOGLE_SHEETS_BATCH_SIZE` if hitting rate limits
- Increase `GOOGLE_SHEETS_SYNC_INTERVAL` for less frequent syncs
- Consider using separate sheets instead of one large sheet

### Data not updating
- Check `/api/sheets/status` for last sync time
- Look for errors in sync status
- Verify manual sync works: `POST /api/sheets/watchlist/export`
- Check application logs for errors

## Architecture

### Service Layer
**`app/services/google_sheets.py`**
- Handles all Google Sheets API interactions
- Singleton pattern for efficiency
- Async/await for non-blocking operations
- Error handling and retry logic

### API Layer
**`app/api/sheets.py`**
- RESTful endpoints for all operations
- Request validation with Pydantic
- Background task support
- Comprehensive error responses

### Database Models
**`app/models.py`**
- `Trade` - Trade journal entries
- `Portfolio` - Holdings and positions
- `SheetSync` - Sync tracking and audit log

### Configuration
**`app/config.py`**
- All settings in one place
- Environment variable support
- Validation and defaults

## Performance

### Caching
- Service instance cached (singleton)
- Sheet metadata cached
- Minimal API calls

### Batch Processing
- Configurable batch size (default: 100 rows)
- Efficient bulk updates
- Rate limit compliance

### Background Tasks
- Non-blocking sync operations
- FastAPI BackgroundTasks
- Async processing

### Rate Limits
- Google Sheets API: 100 requests/100 seconds/user
- Our default config stays well under limits
- Automatic retry on rate limit errors

## Security

### Service Account Best Practices
- Never commit service account JSON to git
- Use environment variables or secret managers
- Rotate keys periodically
- Minimum required permissions (Sheets + Drive)

### Sheet Permissions
- Only share with service account email
- Use "Editor" not "Owner" permissions
- Don't make sheets publicly accessible
- Consider using separate sheets per user

### Data Privacy
- Service account can only access shared sheets
- No access to user's other Google Drive files
- All API calls use HTTPS
- Credentials encrypted in memory

## Limitations

- Google Sheets has a 10 million cell limit per sheet
- Maximum 200 sheets per spreadsheet
- API quota: 100 requests per 100 seconds per user
- Cell character limit: 50,000 characters

## Roadmap

Future enhancements:
- [ ] Real-time sync via WebSockets
- [ ] Chart images embedded in sheets
- [ ] Custom template sheets
- [ ] Multi-user support with separate sheets
- [ ] Automated report generation
- [ ] Integration with Google Data Studio
- [ ] Email notifications on sync errors
- [ ] Backup/restore from sheets

## Support

For issues or questions:
- Check logs: Application logs contain detailed error messages
- API status: `GET /api/sheets/status`
- Health check: `GET /api/sheets/health`
- GitHub Issues: [Report a bug](https://github.com/Stockmasterflex/legend-ai-python/issues)

## License

MIT License - See LICENSE file for details.
