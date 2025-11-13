# Legend AI - API Reference

Complete reference of all available endpoints in the Legend AI FastAPI backend.

## Quick Stats
- **Total Routers**: 14
- **Total Endpoints**: 44+
- **Base URL (Local)**: `http://localhost:8000`
- **Base URL (Production)**: `https://your-railway-domain.railway.app`

---

## Health & Status Endpoints

### System Health
```
GET /health
GET /
```
Returns overall service health including Telegram, Redis, and database status.

---

## Pattern Detection (13 endpoints)

**Module**: `app/api/patterns.py`

### Detect Pattern
```
POST /api/patterns/detect
Content-Type: application/json

{
  "ticker": "NVDA",
  "interval": "1day",
  "use_yahoo_fallback": true
}
```
Detects pattern setups (VCP, Cup & Handle, Flat Base, Breakout) with:
- Entry price
- Stop loss
- Target price
- Risk/reward ratio
- RS (Relative Strength) rating

### Cache Statistics
```
GET /api/patterns/cache/stats
```
View cache hit rates and performance metrics.

### Service Health
```
GET /api/patterns/health
```

---

## Market Data & Analysis (5 endpoints)

**Module**: `app/api/market.py`

### Market Internals
```
GET /api/market/internals
```
Analyzes market regime (uptrend, downtrend, consolidation) based on:
- SPY price
- 50-day SMA
- 200-day SMA
- Market breadth

---

## Chart Generation (2 endpoints)

**Module**: `app/api/charts.py`

### Generate Chart
```
POST /api/charts/generate
Content-Type: application/json

{
  "ticker": "NVDA",
  "interval": "daily",
  "studies": ["RSI", "MACD", "Volume"],
  "theme": "dark"
}
```
Generates TradingView-powered chart images with technical studies.

### Health
```
GET /api/charts/health
```

---

## Universe Scanning (6 endpoints)

**Module**: `app/api/universe.py`

### Get Universe Tickers
```
GET /api/universe/tickers
GET /api/universe/sp500
GET /api/universe/nasdaq100
```
Returns list of tickers to scan.

### Full Scan
```
POST /api/universe/scan
Content-Type: application/json

{
  "universe": "nasdaq100",
  "interval": "1day"
}
```
Scans entire universe for pattern setups (can take 2-5 minutes).

### Quick Scan
```
POST /api/universe/scan/quick
Content-Type: application/json

{
  "universe": "sp500",
  "limit": 20
}
```
Scans top tickers for speed.

### Health
```
GET /api/universe/health
```

---

## Multi-Timeframe Analysis (3 endpoints)

**Module**: `app/api/multitimeframe.py`

### Analyze Multiple Timeframes
```
POST /api/multitimeframe/analyze
Content-Type: application/json

{
  "ticker": "NVDA",
  "timeframes": ["1day", "4hour", "1hour"]
}
```
Analyzes pattern confluence across multiple timeframes (confluence = strength).

### Quick Multi-TF Analysis
```
POST /api/multitimeframe/quick/{ticker}
```
Fast analysis for a single ticker across standard timeframes.

### Health
```
GET /api/multitimeframe/health
```

---

## Risk Management (5 endpoints)

**Module**: `app/api/risk.py`

### Calculate Position Size
```
POST /api/risk/calculate-position
Content-Type: application/json

{
  "account_size": 10000,
  "risk_percent": 2,
  "entry": 150.00,
  "stop": 145.00
}
```
Calculates position size using:
- 2% risk rule
- Kelly Criterion
- ATR-based stops
- Variance analysis

### Breakeven Analysis
```
POST /api/risk/breakeven
Content-Type: application/json

{
  "entry": 150.00,
  "commission": 0.5
}
```
Calculates price needed to break even.

### Recovery Analysis
```
POST /api/risk/recovery
Content-Type: application/json

{
  "current_price": 145.00,
  "loss": 500
}
```
Calculates required gains to recover from loss.

### Risk Rules
```
GET /api/risk/rules
```
Returns configured risk management rules.

### Health
```
GET /api/risk/health
```

---

## Watchlist Management (4 endpoints)

**Module**: `app/api/watchlist.py`

### Get Watchlist
```
GET /api/watchlist?user_id={chat_id}
```
Returns all symbols in the specified user's watchlist. `user_id` defaults to `default` when omitted.

### Add to Watchlist
```
POST /api/watchlist/add
Content-Type: application/json

{
  "ticker": "NVDA",
  "reason": "Strong uptrend pattern",
  "tags": "VCP, Earnings",
  "user_id": "123456789"
}
```

### Remove from Watchlist
```
DELETE /api/watchlist/remove/{ticker}?user_id={chat_id}
```

### Check Watchlist Status
```
GET /api/watchlist/status/{ticker}
```

---

## Trade Management (5 endpoints)

**Module**: `app/api/trades.py`

### Create Trade
```
POST /api/trades/create
Content-Type: application/json

{
  "ticker": "NVDA",
  "entry": 150.00,
  "stop": 145.00,
  "target": 160.00,
  "quantity": 10,
  "notes": "VCP pattern breakout"
}
```
Logs a new trade in the journal.

### Close Trade
```
POST /api/trades/close
Content-Type: application/json

{
  "trade_id": "uuid-here",
  "exit_price": 158.50,
  "notes": "Partial exit on resistance"
}
```

### Get Open Trades
```
GET /api/trades/open
```

### Get Closed Trades
```
GET /api/trades/closed
```

### Trade Statistics
```
GET /api/trades/statistics
```
Returns P&L, win rate, risk/reward ratio.

### Health
```
GET /api/trades/health
```

---

## Trade Planning (1 endpoint)

**Module**: `app/api/trade_plan.py`

### Create Trade Plan
```
POST /api/trade/plan
Content-Type: application/json

{
  "ticker": "NVDA",
  "pattern": "VCP",
  "setup_date": "2025-11-06",
  "reason": "4-month base with improving trend template"
}
```
Creates detailed trade plan with:
- Entry criteria
- Stop loss levels
- Target prices
- Risk/reward analysis
- Plan review checklist

---

## Analytics & Performance (3 endpoints)

**Module**: `app/api/analytics.py`

### Trade Analytics
```
POST /api/analytics/trade
Content-Type: application/json

{
  "trade_id": "uuid-here"
}
```
Deep analysis of a specific trade.

### Performance Metrics
```
GET /api/analytics/performance
```
Overall portfolio and trading performance.

### Trade Journal
```
GET /api/analytics/journal
```
Complete trading journal with all entries.

---

## Alerts & Monitoring (6 endpoints)

**Module**: `app/api/alerts.py`

### Monitor Pattern
```
POST /api/alerts/monitor
Content-Type: application/json

{
  "ticker": "NVDA",
  "pattern_type": "VCP",
  "alert_on": "breakout"
}
```
Sets up real-time alert for pattern events.

### Check Alerts Now
```
POST /api/alerts/check-now
```
Force immediate check of all monitored patterns.

### Recent Alerts
```
GET /api/alerts/recent
```
Last 20 alerts triggered.

### Alert Config
```
GET /api/alerts/config
```
Currently configured alerts.

### Test Alert
```
POST /api/alerts/test
Content-Type: application/json

{
  "channel": "telegram"
}
```
Send test alert to verify Telegram integration.

### Health
```
GET /api/alerts/health
```

---

## Telegram Bot (1 endpoint)

**Module**: `app/api/telegram_enhanced.py`

### Webhook
```
POST /api/webhook/telegram
```
Telegram bot webhook (auto-configured on startup).

**Commands**:
- `/start` - Begin using the bot
- `/scan` - Scan NASDAQ for patterns
- `/pattern NVDA` - Analyze specific ticker
- `/chart NVDA` - Generate chart
- `/watchlist` - View watchlist
- `/help` - Show all commands

---

## Dashboard (2 endpoints)

**Module**: `app/api/dashboard.py`

### Dashboard Page
```
GET /dashboard
```
Full HTML dashboard with embedded TradingView widgets:
- Live ticker tape (SPX, NDX, DJI, BTC, EUR/USD)
- Market overview
- Stock heatmap (sector rotation)
- Stock screener
- Advanced charts with studies
- Economic calendar
- Top market stories
- Symbol performance info

### Dashboard Test
```
GET /dashboard/test
```

---

## Example Usage

### Complete Pattern Detection Flow

```bash
# 1. Detect pattern for ticker
curl -X POST http://localhost:8000/api/patterns/detect \
  -H "Content-Type: application/json" \
  -d '{"ticker": "NVDA", "interval": "1day"}'

# 2. Get market regime
curl http://localhost:8000/api/market/internals

# 3. Analyze across timeframes
curl -X POST http://localhost:8000/api/multitimeframe/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "NVDA", "timeframes": ["1day", "4hour", "1hour"]}'

# 4. Calculate position size
curl -X POST http://localhost:8000/api/risk/calculate-position \
  -H "Content-Type: application/json" \
  -d '{"account_size": 10000, "risk_percent": 2, "entry": 150, "stop": 145}'

# 5. Create trade plan
curl -X POST http://localhost:8000/api/trade/plan \
  -H "Content-Type: application/json" \
  -d '{"ticker": "NVDA", "pattern": "VCP", "reason": "breakout setup"}'

# 6. Set up alert
curl -X POST http://localhost:8000/api/alerts/monitor \
  -H "Content-Type: application/json" \
  -d '{"ticker": "NVDA", "pattern_type": "VCP", "alert_on": "breakout"}'

# 7. View dashboard with TradingView widgets
open http://localhost:8000/dashboard
```

---

## Response Format

All endpoints return JSON in standardized format:

**Success**:
```json
{
  "success": true,
  "data": { /* endpoint-specific data */ },
  "cached": false,
  "processing_time": 1.23
}
```

**Error**:
```json
{
  "success": false,
  "error": "Human-readable error message",
  "detail": "Technical error details"
}
```

---

## Rate Limits

**Per API Service** (managed by cache):
- TwelveData: 800 calls/day
- Finnhub: 60 calls/day
- AlphaVantage: 500 calls/day
- OpenRouter: ~100 calls/day (depends on plan)

**Caching Strategy**:
- Market data: 1-hour TTL
- Pattern results: 4-hour TTL
- Chart images: 24-hour TTL
- Cache hit rate: ~80% after warmup

---

## Next Steps

1. **Test Endpoints**: Use the complete flow example above
2. **Monitor Logs**: Watch for errors in the FastAPI terminal
3. **Check Dashboard**: Visit `/dashboard` to see embedded TradingView widgets
4. **Configure Telegram**: Update TELEGRAM_BOT_TOKEN to test bot commands
5. **Deploy to Railway**: See RAILWAY_DEPLOYMENT.md for production setup

---

**Happy trading! 📈**
