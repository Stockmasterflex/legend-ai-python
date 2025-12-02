# Legend AI Daily Pattern Scanner System

## Overview

Automated daily batch scanner that detects Mark Minervini-style chart patterns at market close (6 PM EST). Scans S&P 500 + NASDAQ 100 (~200 tickers) for VCP, Cup & Handle, and Flat Base patterns.

**Performance:**
- ✅ Scans complete in < 15 minutes
- ✅ Top 20 results per pattern (score ≥ 7/10)
- ✅ Professional TradingView-style charts with entry/stop/target levels
- ✅ Redis caching (24hr TTL) + PostgreSQL history
- ✅ Telegram notifications on completion
- ✅ Production-ready error handling

## Architecture

```
Daily Cron Jobs (Railway) → Pattern Scanner Service → Redis Cache + PostgreSQL
                                                    → Chart Generation (Chart-img API)
                                                    → Telegram Notifications
```

### Components

1. **Scanner Service** (`app/services/daily_pattern_scanner.py`)
   - Core scanning logic with retry handling
   - Chart generation integration
   - Redis + PostgreSQL storage

2. **Job Scripts** (`app/jobs/`)
   - `scan_vcp.py` - VCP scanner (6:00 PM EST)
   - `scan_cup_handle.py` - Cup & Handle scanner (6:15 PM EST)
   - `scan_flat_base.py` - Flat Base scanner (6:30 PM EST)

3. **API Endpoints** (`app/api/patterns.py`)
   - `GET /api/patterns/{pattern_type}/daily` - Today's scan results
   - `GET /api/patterns/{pattern_type}/history?days=7` - Historical results
   - `GET /api/patterns/scanner/health` - Scanner health check

4. **Database** (`alembic/versions/005_add_pattern_results_table.py`)
   - `pattern_results` table for persistent storage

5. **Cron Configuration** (`railway.json`)
   - Railway-native cron jobs (no APScheduler)

## API Usage

### Get Today's VCP Scan Results

```bash
curl https://legend-ai-python-production.up.railway.app/api/patterns/vcp/daily
```

**Response:**
```json
{
  "success": true,
  "pattern_type": "VCP",
  "scan_date": "2025-12-02",
  "count": 15,
  "results": [
    {
      "ticker": "NVDA",
      "score": 9.2,
      "entry": 145.50,
      "stop": 140.00,
      "target": 158.00,
      "chart_url": "https://api.chart-img.com/v2/...",
      "reasons": [
        "✓ 3 contractions detected",
        "✓ Volume drying up",
        "✓ RSI healthy at 62"
      ],
      "indicators": {
        "ema50": 142.30,
        "ema200": 135.80,
        "rsi": 62,
        "volume_vs_avg": 0.65,
        "current_price": 145.20
      }
    }
  ]
}
```

### Get Historical Scan Results

```bash
curl https://legend-ai-python-production.up.railway.app/api/patterns/vcp/history?days=7
```

### Check Scanner Health

```bash
curl https://legend-ai-python-production.up.railway.app/api/patterns/scanner/health
```

**Response:**
```json
{
  "status": "healthy",
  "redis_cache": "connected",
  "postgresql": "connected",
  "last_scans": {
    "VCP": {
      "last_scan_date": "2025-12-02",
      "total_results_7d": 42
    },
    "Cup & Handle": {
      "last_scan_date": "2025-12-02",
      "total_results_7d": 28
    }
  },
  "next_scheduled_runs": {
    "VCP": "18:00 EST (Mon-Fri)",
    "Cup & Handle": "18:15 EST (Mon-Fri)",
    "Flat Base": "18:30 EST (Mon-Fri)"
  },
  "current_time_est": "2025-12-02 15:30:00 EST"
}
```

## Supported Patterns

| Pattern Type | URL Slug | Description |
|-------------|----------|-------------|
| VCP | `vcp` | Volatility Contraction Pattern (Minervini) |
| Cup & Handle | `cup_handle` | Classic cup formation with handle |
| Flat Base | `flat_base` | Tight consolidation near highs |
| Triangle | `triangle` | Ascending/Descending/Symmetrical triangles |
| Power Play | `power_play` | Strong momentum breakouts |

## Manual Testing

### Run VCP Scanner Manually

```bash
python -m app.jobs.scan_vcp
```

**Expected Output:**
```
============================================================
🚀 VCP PATTERN SCANNER JOB STARTED
⏰ Time: 2025-12-02T18:00:00
============================================================
🔍 Starting VCP scan for 200 tickers (min_score=7.0)
✅ NVDA: VCP score=9.2
✅ AAPL: VCP score=8.5
...
============================================================
✅ VCP SCAN COMPLETED SUCCESSFULLY
📊 Scanned: 200 tickers
🎯 Found: 15 setups
🏆 Top results: 15
⏱ Duration: 245.3s
============================================================

🏆 TOP 5 VCP SETUPS:
  1. NVDA: 9.2/10 @ $145.50 (target: $158.00)
  2. AAPL: 8.5/10 @ $178.20 (target: $195.00)
  3. META: 8.3/10 @ $525.00 (target: $575.00)
  4. AMD: 7.9/10 @ $152.30 (target: $168.00)
  5. CRM: 7.5/10 @ $285.00 (target: $312.00)
```

## Environment Variables

Required in Railway environment:

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Redis (Upstash)
REDIS_URL=redis://default:password@host:port

# Market Data APIs
TWELVEDATA_API_KEY=your_key
FINNHUB_API_KEY=your_key
ALPHA_VANTAGE_API_KEY=your_key

# Chart Generation
CHART_IMG_API_KEY=YOUR_CHART_IMG_API_KEY

# Telegram Notifications
TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID=7815143490
```

## Railway Cron Jobs

Defined in `railway.json`:

```json
{
  "cron": [
    {
      "name": "scan-vcp",
      "schedule": "0 23 * * 1-5",
      "command": "python -m app.jobs.scan_vcp"
    },
    {
      "name": "scan-cup-handle",
      "schedule": "15 23 * * 1-5",
      "command": "python -m app.jobs.scan_cup_handle"
    },
    {
      "name": "scan-flat-base",
      "schedule": "30 23 * * 1-5",
      "command": "python -m app.jobs.scan_flat_base"
    }
  ]
}
```

**Schedule:** Monday-Friday (1-5) at:
- 23:00 UTC = 6:00 PM EST (VCP)
- 23:15 UTC = 6:15 PM EST (Cup & Handle)
- 23:30 UTC = 6:30 PM EST (Flat Base)

## Database Schema

```sql
CREATE TABLE pattern_results (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    pattern_type VARCHAR(50) NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    score NUMERIC(3,1) NOT NULL,
    entry_price NUMERIC(10,2),
    stop_price NUMERIC(10,2),
    target_price NUMERIC(10,2),
    chart_url TEXT,
    reasons JSONB,
    indicators JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(date, pattern_type, ticker)
);

CREATE INDEX idx_pattern_date ON pattern_results(date, pattern_type);
CREATE INDEX idx_pattern_score_desc ON pattern_results(score DESC);
```

## Redis Cache Structure

**Key Format:**
```
patterns:{pattern_type}:{YYYY-MM-DD}
```

**Example:**
```
patterns:vcp:2025-12-02
```

**Value:** JSON array of top 20 results

**TTL:** 86400 seconds (24 hours)

## Telegram Notifications

Scanner sends notifications on scan completion:

```
🎯 VCP Scan Complete

✅ Scanned: 200 tickers
📈 Found: 15 setups (score ≥ 7)
⏱ Duration: 245s

🏆 Top 5 Setups:
1. NVDA: 9.2/10 @ $145.50
2. AAPL: 8.5/10 @ $178.20
3. META: 8.3/10 @ $525.00
4. AMD: 7.9/10 @ $152.30
5. CRM: 7.5/10 @ $285.00
```

## Error Handling

### Retry Logic
- Market data API failures: 3x exponential backoff
- Chart generation failures: Graceful degradation (stores without chart)
- Database failures: Logged, Telegram alert sent

### Monitoring
- Comprehensive logging to stdout (Railway logs)
- Telegram alerts on failures
- Health check endpoint: `/api/patterns/scanner/health`

## Pattern Detection Algorithms

### VCP (Volatility Contraction Pattern)

**Criteria:**
- ✅ 3+ contractions with shrinking % declines
- ✅ Volume drying up during base (< 70% avg)
- ✅ Price > EMA50 > EMA200
- ✅ Clean pivot with volume surge on breakout
- ✅ Proximity to 52-week high (within 25%)

**Scoring:** 0-10 scale based on Minervini template

### Cup & Handle

**Criteria:**
- ✅ Rounded cup formation (U-shape)
- ✅ Shallow handle (< 15% of cup depth)
- ✅ Volume declining in handle
- ✅ Breakout above rim with volume

### Flat Base

**Criteria:**
- ✅ Tight consolidation (< 10% range)
- ✅ Duration 5-15 weeks
- ✅ Price within 15% of highs
- ✅ Low volatility

## Deployment Checklist

- [x] Database migration applied (`alembic upgrade head`)
- [x] Environment variables set in Railway
- [x] Cron jobs configured in `railway.json`
- [x] Telegram bot configured
- [x] Redis cache connected
- [x] PostgreSQL connected
- [x] Chart-img API key valid
- [x] Market data APIs configured

## Monitoring & Observability

### Logs
```bash
# View Railway logs
railway logs --service legend-ai-python

# Filter for scanner jobs
railway logs | grep "SCAN"
```

### Metrics
- Scan duration (seconds)
- Tickers scanned
- Patterns found
- Error rate
- Cache hit rate

### Alerts
- Telegram notifications on scan completion/failure
- Health check endpoint for external monitoring

## Troubleshooting

### Scanner Not Running

**Check cron jobs:**
```bash
# View Railway cron status
railway status
```

**Check logs:**
```bash
railway logs | grep "scan-vcp"
```

### No Results

**Check Redis:**
```bash
# Test cache connection
curl https://your-app.railway.app/api/patterns/scanner/health
```

**Check database:**
```sql
SELECT COUNT(*) FROM pattern_results WHERE date = CURRENT_DATE;
```

### Chart Generation Failed

Charts are optional. If Chart-img API fails, scanner continues and stores results without charts.

**Check Chart-img API key:**
```bash
echo $CHART_IMG_API_KEY
```

## Future Enhancements

- [ ] Additional patterns (Triangle, Power Play)
- [ ] Email notifications
- [ ] Slack integration
- [ ] Pattern backtest results in charts
- [ ] Mobile push notifications
- [ ] Custom watchlist scanning

## Support

- **GitHub Issues:** https://github.com/kyleanicholson/legend-ai/issues
- **Documentation:** https://github.com/kyleanicholson/legend-ai/docs
- **Production URL:** https://legend-ai-python-production.up.railway.app
