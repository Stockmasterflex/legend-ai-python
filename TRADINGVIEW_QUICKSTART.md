# TradingView Integration - Quick Start

## 🚀 Get Started in 5 Minutes

### 1. Environment Setup

Add to your `.env` file:

```bash
# Optional: For webhook signature validation
TRADINGVIEW_WEBHOOK_SECRET=your_secret_key_here

# Optional: TradingView API key (future use)
TRADINGVIEW_API_KEY=your_api_key_here

# Optional: Adjust rate limiting (default: 100)
TRADINGVIEW_RATE_LIMIT_PER_MINUTE=100
```

### 2. Run Database Migration

```bash
# Create migration for new tables
alembic revision --autogenerate -m "Add TradingView integration"

# Apply migration
alembic upgrade head
```

### 3. Get Your Webhook URL

Your webhook URL is:

```
https://your-domain.com/api/tradingview/webhooks/tradingview
```

### 4. Create TradingView Alert

1. Open a chart in TradingView
2. Click **Alert** (clock icon) or press `Alt + A`
3. Set your alert conditions
4. In **Notifications**, enable **Webhook URL**
5. Paste your webhook URL
6. Set alert message:

```json
{
  "ticker": "{{ticker}}",
  "close": {{close}},
  "time": "{{time}}",
  "interval": "{{interval}}",
  "alert_name": "My First Alert",
  "message": "Price alert triggered"
}
```

### 5. Test It!

Send a test webhook:

```bash
curl -X POST https://your-domain.com/api/tradingview/webhooks/tradingview \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "close": 150.00,
    "time": "2025-01-15 10:00:00",
    "interval": "1D",
    "alert_name": "AAPL Test",
    "message": "Test alert from TradingView"
  }'
```

Expected response:

```json
{
  "success": true,
  "alert_id": 1,
  "symbol": "AAPL",
  "alert_type": "price",
  "action": null
}
```

### 6. View Received Alerts

```bash
curl https://your-domain.com/api/tradingview/alerts
```

## 🎯 Alert Types

### Price Alert

```json
{
  "ticker": "{{ticker}}",
  "close": {{close}},
  "message": "Price crossed ${{close}}"
}
```

### Pattern Alert (with Legend AI confirmation)

```json
{
  "ticker": "{{ticker}}",
  "close": {{close}},
  "message": "VCP pattern detected on {{ticker}}"
}
```

Legend AI will automatically:
- Detect patterns on the symbol
- Assign a confidence score (0-10)
- Confirm or reject the alert
- Add to watchlist if score ≥ 7

### Indicator Alert

```json
{
  "ticker": "{{ticker}}",
  "close": {{close}},
  "message": "RSI oversold",
  "rsi": 28.5,
  "macd": -1.2
}
```

### Breakout Alert

```json
{
  "ticker": "{{ticker}}",
  "close": {{close}},
  "message": "{{ticker}} broke resistance at {{close}}"
}
```

### Stop-Loss Alert

```json
{
  "ticker": "{{ticker}}",
  "close": {{close}},
  "message": "Stop-loss hit at {{close}}"
}
```

### Strategy Alert (with action)

```json
{
  "ticker": "{{ticker}}",
  "close": {{close}},
  "strategy_name": "My Strategy",
  "message": "Buy {{ticker}} at {{close}}"
}
```

Legend AI will extract the action: `buy`, `sell`, `exit`

## 📊 API Endpoints

### Query Alerts

```bash
# All alerts
GET /api/tradingview/alerts

# Filter by symbol
GET /api/tradingview/alerts?symbol=AAPL

# Filter by type
GET /api/tradingview/alerts?alert_type=pattern

# Limit results
GET /api/tradingview/alerts?limit=10
```

### Sync Pattern to TradingView

```bash
POST /api/tradingview/sync/pattern
{
  "pattern_scan_id": 123
}
```

### Sync Watchlist to TradingView

```bash
POST /api/tradingview/sync/watchlist
{
  "watchlist_ids": [1, 2, 3]
}
```

### Import Strategy

```bash
POST /api/tradingview/strategies/import
{
  "name": "RSI Reversal",
  "description": "Buy RSI < 30, Sell RSI > 70",
  "strategy_config": {
    "timeframe": "1D",
    "indicators": ["RSI"],
    "entry_conditions": {"rsi": {"operator": "<", "value": 30}},
    "exit_conditions": {"rsi": {"operator": ">", "value": 70}}
  }
}
```

### Backtest Strategy

```bash
POST /api/tradingview/strategies/backtest
{
  "strategy_id": 1,
  "symbols": ["AAPL", "MSFT"],
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```

## 🔐 Security

### Enable Signature Validation

1. Set `TRADINGVIEW_WEBHOOK_SECRET` in `.env`
2. TradingView will sign webhooks with HMAC-SHA256
3. Legend AI validates the signature
4. Invalid signatures are rejected (401 Unauthorized)

### Rate Limiting

- Default: 100 requests/minute per IP
- Configurable via `TRADINGVIEW_RATE_LIMIT_PER_MINUTE`
- Exceeded requests return `429 Too Many Requests`

## 📚 Full Documentation

For complete documentation, see:
- [Full TradingView Integration Guide](docs/TRADINGVIEW_INTEGRATION.md)
- [API Documentation](https://your-domain.com/docs#tradingview)

## ❓ Troubleshooting

### Webhook Not Working?

1. Check webhook URL is correct
2. Verify TradingView alert is active
3. Test with curl (see step 5 above)
4. Check logs for errors

### Pattern Not Confirmed?

1. Verify pattern detection works: `POST /api/patterns/detect`
2. Check Legend AI score threshold (≥ 7)
3. Review alert: `GET /api/tradingview/alerts?symbol=AAPL`

### Rate Limit Errors?

1. Increase `TRADINGVIEW_RATE_LIMIT_PER_MINUTE`
2. Reduce alert frequency in TradingView

## 🎉 You're Ready!

Your TradingView integration is live! Start creating alerts and let Legend AI confirm your patterns automatically.

For advanced features, check the [full documentation](docs/TRADINGVIEW_INTEGRATION.md).
