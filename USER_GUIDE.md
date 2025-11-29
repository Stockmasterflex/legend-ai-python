# Legend AI User Guide

## Introduction

Legend AI is a professional-grade pattern recognition and trading analysis platform built for Minervini-style VCP (Volatility Contraction Pattern) traders. It combines 140+ pattern detectors, relative strength analysis, and automated scanning to identify high-probability setups.

## Quick Start

### 1. Analyze a Single Stock

```bash
curl "http://localhost:8000/api/analyze?ticker=NVDA&multi_timeframe=true"
```

Returns:
- Pattern detection (VCP, Cup & Handle, Flags, etc.)
- Entry/Stop/Target levels
- Risk/Reward ratio
- Minervini Trend Template score
- Relative Strength rating
- Multi-timeframe confirmation

### 2. Scan the Universe

Get today's top setups from S&P 500 + NASDAQ 100:

```bash
curl "http://localhost:8000/api/scan/latest?min_score=7.0"
```

### 3. Plan a Trade

Calculate position size and partial exits:

```bash
curl -X POST "http://localhost:8000/api/trade/plan" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "NVDA",
    "entry": 485.00,
    "stop": 465.00,
    "target": 525.00,
    "account_size": 100000,
    "risk_percent": 1.0
  }'
```

Returns:
- Position size (shares)
- Dollar amount
- Risk amount
- Partial exit levels (1R, 2R, 3R)
- Concentration warnings

### 4. Add to Watchlist

```bash
curl -X POST "http://localhost:8000/api/watchlist/add" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "NVDA",
    "reason": "VCP setup forming",
    "target_entry": 485.00,
    "target_stop": 465.00,
    "target_price": 525.00
  }'
```

Watchlist monitors price every 5 minutes during market hours and sends Telegram alerts when:
- Price breaks above entry + 1.5x volume → "Breaking Out"
- Price hits stop or target → "Triggered"

### 5. Log Trades

```bash
curl -X POST "http://localhost:8000/api/journal/trade" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "NVDA",
    "entry_date": "2025-11-29",
    "entry_price": 485.00,
    "stop_price": 465.00,
    "target_price": 525.00,
    "shares": 50,
    "notes": "Perfect VCP setup"
  }'
```

Close trade:

```bash
curl -X PUT "http://localhost:8000/api/journal/trade/1" \
  -H "Content-Type: application/json" \
  -d '{
    "exit_date": "2025-12-05",
    "exit_price": 510.00,
    "status": "Closed"
  }'
```

Get performance stats:

```bash
curl "http://localhost:8000/api/journal/stats"
```

## Key Features

### Pattern Detection
- **VCP (Volatility Contraction Pattern)** - Minervini's signature setup
- **High Tight Flag** - Explosive breakout pattern
- **Cup & Handle** - Classic continuation pattern
- **Flat Base** - Tight consolidation
- **Bull/Bear Flags** - Momentum continuations
- **Double Bottoms** - Reversal setups
- **Head & Shoulders** - Top/bottom reversals
- **Wedges** - Rising/falling patterns
- **Pennants** - Triangular consolidations

### SEPA Methodology
**S**tage: Weinstein stage analysis (1-4)
**E**ntry: Precise breakout levels
**P**ivot: Support/resistance pivots
**A**nalysis: Multi-timeframe confirmation

### Relative Strength Rating
Minervini's RS rating (0-99 scale):
- **90-99:** 🔥 Strongest stocks (top 10%)
- **70-89:** 🟢 Strong (top 30%)
- **50-69:** 🟡 Average
- **<50:** ⚪ Weak

### Risk Management
- ATR-based position sizing
- 1% account risk per trade (configurable)
- 20% concentration limit
- R:R validation (minimum 2:1)
- Partial exits: 50% @ 1R, 30% @ 2R, 20% @ 3R

### Watchlist & Alerts
- 5-minute monitoring (9:30 AM - 4:00 PM ET)
- Telegram alerts on breakouts
- State management (Watching/Breaking Out/Triggered)
- Volume confirmation (1.5x average)

### Trade Journal
- Log all trades with P&L tracking
- Performance statistics:
  - Win rate %
  - Average R-multiple
  - Expectancy
  - Profit factor
- CSV export

## API Endpoints

### Analysis
- `GET /api/analyze` - Analyze single ticker
- `GET /api/patterns/detect` - Pattern detection
- `POST /api/patterns/scan` - Batch scan

### Scanner
- `GET /api/scan/latest` - Latest EOD scan
- `GET /api/scan/date/{YYYYMMDD}` - Historical scans
- `GET /api/scan/sector/{sector}` - Sector filter
- `GET /api/top-setups` - Top 10 setups

### Watchlist
- `POST /api/watchlist/add` - Add ticker
- `GET /api/watchlist` - List all
- `DELETE /api/watchlist/remove/{ticker}` - Remove
- `PUT /api/watchlist/{ticker}` - Update
- `POST /api/watchlist/check` - Manual check

### Trade Planner
- `POST /api/trade/plan` - Full trade plan
- `POST /api/trade/quick-size` - Quick calculator

### Journal
- `POST /api/journal/trade` - Log trade
- `GET /api/journal/trades` - List trades
- `PUT /api/journal/trade/{id}` - Close trade
- `GET /api/journal/stats` - Performance stats
- `GET /api/journal/export` - CSV export

### Dashboard
- `GET /dashboard` - Market internals dashboard

## Configuration

### Environment Variables

```bash
# Required
DATABASE_URL=postgresql://user:pass@host:5432/legend_ai
REDIS_HOST=localhost
REDIS_PORT=6379

# API Keys
TWELVEDATA_API_KEY=your_key
FINNHUB_API_KEY=your_key
ALPHA_VANTAGE_KEY=your_key
CHART_IMG_API_KEY=your_key

# Telegram (Optional)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Risk Settings
DEFAULT_RISK_PERCENT=1.0
MAX_CONCENTRATION_PERCENT=20.0
MIN_RISK_REWARD=2.0
```

### Scheduled Jobs

- **EOD Scanner:** 4:05 PM ET Mon-Fri (after market close)
- **Universe Refresh:** 8:00 PM ET Sunday
- **Watchlist Monitor:** Every 5 min, 9:30 AM - 4:00 PM ET Mon-Fri

## Best Practices

### 1. Always Check Multi-Timeframe
```bash
curl "http://localhost:8000/api/analyze?ticker=NVDA&multi_timeframe=true"
```

Look for:
- ✅ Weekly + Daily pattern alignment
- ✅ Overall confluence ≥ 70%
- ✅ Signal quality: "Good" or "Excellent"

### 2. Filter by RS Rating
Only trade stocks with RS ≥ 70:

```bash
curl "http://localhost:8000/api/scan/latest?min_rs=70"
```

### 3. Use Position Sizing
Never skip the trade planner:

```bash
curl -X POST "http://localhost:8000/api/trade/plan" -d '{...}'
```

Warnings to heed:
- ⚠️ Position >20% concentration
- ⚠️ R:R <2:1
- ⚠️ Position size <10 shares

### 4. Scale Out at Partial Exits
Follow the plan:
- **50% @ 1R** - Lock in initial risk
- **30% @ 2R** - Capture swing target
- **20% @ 3R** - Let winners run

### 5. Journal Every Trade
```bash
# Entry
POST /api/journal/trade

# Exit
PUT /api/journal/trade/1

# Review stats weekly
GET /api/journal/stats
```

Target metrics:
- Win rate: ≥60%
- Avg R-multiple: ≥2.0
- Profit factor: ≥1.5

## Troubleshooting

### No Patterns Found
- Check if data exists: `GET /api/analyze?ticker=NVDA`
- Verify market data API keys are set
- Try different timeframes: `&interval=1week`

### Watchlist Not Alerting
- Check if market hours: 9:30 AM - 4:00 PM ET Mon-Fri
- Verify Telegram bot is configured
- Run manual check: `POST /api/watchlist/check`

### Scanner Returns Empty
- Wait for EOD scan to complete (4:05 PM ET)
- Check scan logs: `GET /api/scan/latest`
- Lower score threshold: `?min_score=6.0`

## Support

- **Documentation:** `/docs` (FastAPI Swagger UI)
- **API Reference:** `/redoc` (ReDoc)
- **Health Check:** `/health`
- **Version:** `/version`

---

**Happy Trading! 🚀📊**

