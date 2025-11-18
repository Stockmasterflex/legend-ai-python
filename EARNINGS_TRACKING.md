# Earnings Tracking & Alerts

Comprehensive earnings tracking system integrated into Legend AI.

## Features

### 1. Earnings Calendar
- **Upcoming Earnings Dates**: View earnings reports for the next 7-90 days
- **Historical Beat/Miss Data**: Track historical earnings performance
- **Consensus Estimates**: EPS and revenue estimates
- **Surprise Percentage**: Historical beat/miss percentages
- **Sector Filtering**: Filter earnings by sector
- **Watchlist Integration**: See which watchlist stocks are reporting

### 2. Pre/Post-Earnings Analysis
- **Historical Price Reaction**: Average gap percentage on earnings
- **Volume Patterns**: Typical volume increase on earnings days
- **Volatility Analysis**: Intraday and multi-day price movements
- **Gap Analysis**: Pre-close to post-open gap statistics
- **Multi-day Tracking**: 1-week and 1-month post-earnings movements

### 3. Earnings Alerts
- **Upcoming Earnings**: Alerts 7 days before earnings
- **Surprise Alerts**: Alerts on significant beat/miss (>5% threshold)
- **Gap Alerts**: Alerts on significant price gaps (>3% threshold)
- **Volume Alerts**: Alerts on unusual volume (>2x average)
- **Pattern Alerts**: Post-earnings pattern formation alerts
- **Delivery**: Via Telegram and Email

### 4. Calendar Visualization
- **Monthly View**: Visual calendar with all upcoming earnings
- **Color-Coded**: Beat rate color coding (green=high, yellow=medium, red=low)
- **Sector Filters**: Filter by Technology, Healthcare, Financial, etc.
- **Watchlist Badges**: Stars on watchlist stocks
- **Export Options**:
  - JSON format
  - CSV for spreadsheets
  - iCal for Google Calendar/Apple Calendar

## API Endpoints

### Earnings Calendar
```
GET /api/earnings/calendar?days_ahead=30&ticker=AAPL
```
Returns upcoming earnings for specified period.

### Historical Beat/Miss
```
GET /api/earnings/ticker/{ticker}/history?limit=8
```
Returns historical earnings performance.

### Earnings Reaction Analysis
```
GET /api/earnings/ticker/{ticker}/reaction?earnings_date=2024-01-15
```
Analyzes price reaction to specific earnings event.

### Historical Reactions
```
GET /api/earnings/ticker/{ticker}/reactions/historical?limit=8
```
Returns historical earnings reaction patterns.

### Upcoming Earnings
```
GET /api/earnings/upcoming?days=7
```
Quick view of earnings in next N days.

### Watchlist Earnings
```
GET /api/earnings/watchlist
```
Returns earnings for all watchlist stocks.

### Calendar Export
```
GET /api/earnings/export/calendar?format=ical&days_ahead=30
```
Export calendar in JSON, CSV, or iCal format.

## Database Schema

### EarningsCalendar
- Stores earnings dates, estimates, and actual results
- Tracks beat/miss metrics
- Links to ticker information

### EarningsReaction
- Pre/post earnings price data
- Gap and move percentages
- Volume and volatility metrics
- Multi-day reaction tracking

### EarningsAlert
- Alert configuration per ticker
- Alert type settings
- Threshold configurations
- Last alert tracking

## Usage

### Dashboard
1. Navigate to "Earnings Calendar" tab
2. Select date range (7-90 days)
3. Filter by sector if desired
4. Click on any earnings event for detailed analysis
5. Export calendar to your preferred format

### API Integration
```python
import requests

# Get upcoming earnings
response = requests.get('http://localhost:8000/api/earnings/calendar?days_ahead=30')
earnings = response.json()

# Analyze specific ticker
response = requests.get('http://localhost:8000/api/earnings/ticker/AAPL/history')
history = response.json()
```

### Setting Up Alerts
Earnings alerts are automatically monitored for watchlist stocks:
- Add stock to watchlist
- Alerts will trigger based on default thresholds
- Customize thresholds via API if needed

## Data Sources

The earnings service uses multiple data sources with intelligent fallback:
1. **Finnhub**: Primary source for earnings calendar
2. **Alpha Vantage**: Fallback for historical earnings data
3. **Market Data Service**: Price data for reaction analysis

## Configuration

Set these environment variables for full functionality:
- `FINNHUB_API_KEY`: Finnhub API key
- `ALPHA_VANTAGE_API_KEY`: Alpha Vantage API key
- `TELEGRAM_BOT_TOKEN`: Telegram bot token for alerts
- `TELEGRAM_CHAT_ID`: Telegram chat ID for alerts
- `SENDGRID_API_KEY`: SendGrid API key for email alerts
- `ALERT_EMAIL`: Email address for alerts

## Performance

- **Caching**: 6-hour cache for earnings calendar
- **Rate Limiting**: Respects API limits for data sources
- **Cooldowns**: 24-hour cooldown between duplicate alerts
- **Lazy Loading**: Dashboard loads data on tab activation

## Future Enhancements

- [ ] Options flow changes around earnings
- [ ] Analyst upgrades/downgrades tracking
- [ ] Conference call sentiment analysis
- [ ] Earnings surprise prediction using ML
- [ ] Real-time earnings updates
- [ ] Customizable alert thresholds per ticker
- [ ] Earnings season statistics
- [ ] Sector comparison views
