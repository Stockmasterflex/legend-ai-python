# TradingView Integration Guide

## Overview

Legend AI now integrates seamlessly with TradingView, providing:

- **Webhook Receiver**: Receive real-time alerts from TradingView
- **Alert Processing**: Process price, indicator, pattern, breakout, and stop-loss alerts
- **Two-Way Sync**: Share patterns and watchlists between Legend AI and TradingView
- **Strategy Integration**: Import and backtest TradingView strategies

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Webhook Setup](#webhook-setup)
3. [Alert Types](#alert-types)
4. [Two-Way Sync](#two-way-sync)
5. [Strategy Integration](#strategy-integration)
6. [API Reference](#api-reference)
7. [Examples](#examples)
8. [Security](#security)
9. [Troubleshooting](#troubleshooting)

---

## Quick Start

### 1. Environment Configuration

Add these variables to your `.env` file:

```bash
# TradingView Integration (Optional)
TRADINGVIEW_WEBHOOK_SECRET=your_secret_key_here
TRADINGVIEW_API_KEY=your_api_key_here
TRADINGVIEW_RATE_LIMIT_PER_MINUTE=100
```

### 2. Database Migration

Create the TradingView tables:

```bash
# Create migration
alembic revision --autogenerate -m "Add TradingView integration tables"

# Apply migration
alembic upgrade head
```

### 3. Verify Installation

Test the health endpoint:

```bash
curl https://your-domain.com/api/tradingview/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "tradingview_integration",
  "version": "1.0.0"
}
```

---

## Webhook Setup

### Step 1: Get Your Webhook URL

Your webhook URL is:

```
https://your-domain.com/api/tradingview/webhooks/tradingview
```

### Step 2: Create Alert in TradingView

1. Open a chart in TradingView
2. Click the **Alert** button (clock icon) or press `Alt + A`
3. Configure your alert conditions
4. In the **Notifications** tab, enable **Webhook URL**
5. Paste your webhook URL
6. Configure the alert message (see formats below)

### Step 3: Alert Message Formats

#### Basic Alert

```json
{
  "ticker": "{{ticker}}",
  "close": {{close}},
  "time": "{{time}}",
  "interval": "{{interval}}",
  "alert_name": "My Alert Name",
  "message": "Custom message here"
}
```

#### Price Alert

```json
{
  "ticker": "{{ticker}}",
  "close": {{close}},
  "time": "{{time}}",
  "interval": "{{interval}}",
  "alert_name": "Price Alert",
  "message": "{{ticker}} crossed above {{close}}"
}
```

#### Indicator Alert (with RSI, MACD)

```json
{
  "ticker": "{{ticker}}",
  "close": {{close}},
  "time": "{{time}}",
  "interval": "{{interval}}",
  "alert_name": "RSI Oversold",
  "message": "RSI below 30",
  "rsi": 28.5,
  "macd": -1.2
}
```

#### Pattern Alert

```json
{
  "ticker": "{{ticker}}",
  "close": {{close}},
  "time": "{{time}}",
  "interval": "{{interval}}",
  "alert_name": "VCP Pattern",
  "message": "VCP pattern detected on {{ticker}}"
}
```

#### Breakout Alert

```json
{
  "ticker": "{{ticker}}",
  "close": {{close}},
  "time": "{{time}}",
  "interval": "{{interval}}",
  "alert_name": "Breakout",
  "message": "{{ticker}} broke resistance at {{close}}"
}
```

#### Stop-Loss Alert

```json
{
  "ticker": "{{ticker}}",
  "close": {{close}},
  "time": "{{time}}",
  "interval": "{{interval}}",
  "alert_name": "Stop Loss",
  "message": "Stop-loss hit at {{close}}"
}
```

#### Strategy Alert (with Action)

```json
{
  "ticker": "{{ticker}}",
  "close": {{close}},
  "time": "{{time}}",
  "interval": "{{interval}}",
  "strategy_name": "My Trading Strategy",
  "message": "Buy {{ticker}} at {{close}}",
  "action": "buy"
}
```

---

## Alert Types

Legend AI automatically classifies incoming alerts into these types:

### 1. **Price Alerts**

Triggered when price crosses a threshold.

**Keywords**: `price`, `crossed`, `above`, `below`, `target`

**Processing**:
- Updates watchlist items if configured
- Logs alert to database
- Sends notifications via Telegram/Email

### 2. **Indicator Alerts**

Triggered by technical indicators (RSI, MACD, EMA, etc.).

**Keywords**: `rsi`, `macd`, `ema`, `sma`, `bollinger`, `stochastic`, `indicator`

**Processing**:
- Logs indicator values
- Can cross-reference with Legend AI indicators
- Sends notifications

### 3. **Pattern Alerts**

Triggered when chart patterns are detected.

**Keywords**: `vcp`, `cup`, `handle`, `triangle`, `wedge`, `head`, `shoulders`

**Processing**:
- **Pattern Confirmation**: Runs Legend AI pattern detector
- **Scores Pattern**: Assigns Legend AI confidence score (0-10)
- **Creates Alert**: Only if confirmed by Legend AI (score ≥ 7)
- **Updates Watchlist**: Adds to watchlist if high-scoring

**Example Flow**:
```
TradingView Alert → Legend AI Confirms → Score 8.5 → Alert Sent → Added to Watchlist
```

### 4. **Breakout Alerts**

Triggered when price breaks through support/resistance.

**Keywords**: `breakout`, `break out`, `broke`, `resistance`

**Processing**:
- Updates watchlist status to "Breaking Out"
- Records trigger time
- Sends immediate notification

### 5. **Stop-Loss Alerts**

Triggered when stop-loss is hit.

**Keywords**: `stop`, `stop-loss`, `stoploss`, `sl hit`

**Processing**:
- Logs stop-loss trigger
- Can auto-close positions (if trades module enabled)
- Sends urgent notification

---

## Two-Way Sync

### Sync Legend AI Patterns to TradingView

Push detected patterns from Legend AI to TradingView for alert creation:

```bash
POST /api/tradingview/sync/pattern
```

**Request**:

```json
{
  "pattern_scan_id": 123
}
```

**Response**:

```json
{
  "success": true,
  "sync_id": 456,
  "message": "Pattern ready for TradingView alert creation"
}
```

**Use Case**: After Legend AI detects a VCP pattern on AAPL, you can create a TradingView alert to monitor the entry point visually on your charts.

### Sync Watchlist to TradingView

Share your Legend AI watchlist with TradingView:

```bash
POST /api/tradingview/sync/watchlist
```

**Request**:

```json
{
  "watchlist_ids": [1, 2, 3, 4, 5]
}
```

**Response**:

```json
{
  "success": true,
  "synced_count": 5,
  "message": "5 watchlist items synced to TradingView"
}
```

**Use Case**: Create TradingView alerts for all stocks on your Legend AI watchlist automatically.

---

## Strategy Integration

### Import TradingView Strategy

Import a TradingView strategy for backtesting:

```bash
POST /api/tradingview/strategies/import
```

**Request**:

```json
{
  "name": "RSI Reversal Strategy",
  "description": "Buy when RSI < 30, sell when RSI > 70",
  "strategy_config": {
    "timeframe": "1D",
    "indicators": ["RSI", "EMA"],
    "entry_conditions": {
      "rsi": {"operator": "<", "value": 30},
      "price": {"operator": ">", "indicator": "ema_20"}
    },
    "exit_conditions": {
      "rsi": {"operator": ">", "value": 70}
    },
    "risk_reward_ratio": 2.0,
    "win_rate": 0.65,
    "profit_factor": 1.8,
    "max_drawdown": 0.15,
    "total_trades": 150
  },
  "pine_script_code": "// Optional Pine Script code here"
}
```

**Response**:

```json
{
  "success": true,
  "strategy_id": 789,
  "name": "RSI Reversal Strategy"
}
```

### Backtest Strategy

Run backtests against Legend AI data:

```bash
POST /api/tradingview/strategies/backtest
```

**Request**:

```json
{
  "strategy_id": 789,
  "symbols": ["AAPL", "MSFT", "GOOGL", "NVDA"],
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```

**Response**:

```json
{
  "success": true,
  "strategy_id": 789,
  "results": {
    "total_trades": 42,
    "winning_trades": 28,
    "losing_trades": 14,
    "win_rate": 0.67,
    "profit_factor": 2.1,
    "max_drawdown": 0.12,
    "total_return": 0.45,
    "sharpe_ratio": 1.8
  }
}
```

### List Imported Strategies

```bash
GET /api/tradingview/strategies
```

**Response**:

```json
{
  "success": true,
  "count": 3,
  "strategies": [
    {
      "id": 789,
      "name": "RSI Reversal Strategy",
      "description": "Buy when RSI < 30, sell when RSI > 70",
      "timeframe": "1D",
      "win_rate": 0.65,
      "profit_factor": 1.8,
      "max_drawdown": 0.15,
      "legend_optimized": false,
      "created_at": "2025-01-15T10:00:00Z"
    }
  ]
}
```

---

## API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/tradingview/webhooks/tradingview` | Receive TradingView webhooks |
| `GET` | `/api/tradingview/alerts` | Query received alerts |
| `POST` | `/api/tradingview/sync/pattern` | Sync pattern to TradingView |
| `POST` | `/api/tradingview/sync/watchlist` | Sync watchlist to TradingView |
| `POST` | `/api/tradingview/strategies/import` | Import TradingView strategy |
| `POST` | `/api/tradingview/strategies/backtest` | Backtest strategy |
| `GET` | `/api/tradingview/strategies` | List imported strategies |
| `GET` | `/api/tradingview/health` | Health check |

### Query Alerts

```bash
GET /api/tradingview/alerts?symbol=AAPL&alert_type=pattern&limit=50
```

**Query Parameters**:
- `symbol` (optional): Filter by ticker symbol
- `alert_type` (optional): Filter by type (price, indicator, pattern, breakout, stop_loss)
- `limit` (optional): Max results (default 50)

**Response**:

```json
{
  "success": true,
  "count": 5,
  "alerts": [
    {
      "id": 123,
      "symbol": "AAPL",
      "alert_type": "pattern",
      "alert_name": "AAPL VCP Pattern",
      "trigger_price": 150.50,
      "action": null,
      "processed": true,
      "confirmed": true,
      "legend_score": 8.5,
      "received_at": "2025-01-15T10:30:00Z"
    }
  ]
}
```

---

## Examples

### Example 1: TradingView Sends Price Alert

**TradingView Alert Message**:

```json
{
  "ticker": "NVDA",
  "close": 500.00,
  "time": "2025-01-15 14:30:00",
  "interval": "1D",
  "alert_name": "NVDA Above $500",
  "message": "NVDA crossed above $500"
}
```

**Legend AI Processing**:

1. Receives webhook
2. Identifies as "price" alert
3. Checks watchlist for NVDA
4. Logs alert to database
5. Sends Telegram notification

### Example 2: TradingView Detects VCP Pattern

**TradingView Alert Message**:

```json
{
  "ticker": "AAPL",
  "close": 175.50,
  "time": "2025-01-15 15:00:00",
  "interval": "1D",
  "alert_name": "AAPL VCP",
  "message": "VCP pattern detected on AAPL"
}
```

**Legend AI Processing**:

1. Receives webhook
2. Identifies as "pattern" alert
3. **Runs Legend AI pattern detector on AAPL**
4. **Confirms VCP pattern with score 8.2/10**
5. Marks alert as "confirmed"
6. Adds to watchlist with entry/stop/target
7. Sends Telegram notification with chart

### Example 3: TradingView Strategy Sends Buy Signal

**TradingView Alert Message**:

```json
{
  "ticker": "TSLA",
  "close": 250.00,
  "time": "2025-01-15 16:00:00",
  "interval": "4H",
  "strategy_name": "MACD Crossover",
  "message": "Buy TSLA at 250",
  "action": "buy"
}
```

**Legend AI Processing**:

1. Receives webhook
2. Identifies action as "buy"
3. Confirms signal against Legend AI data
4. Calculates position size (risk management)
5. Sends Telegram notification
6. Optionally: Creates trade entry

---

## Security

### Signature Validation

Enable webhook signature validation for production:

1. Set `TRADINGVIEW_WEBHOOK_SECRET` in `.env`
2. TradingView should send signature in `X-TradingView-Signature` header
3. Legend AI validates using HMAC-SHA256

**How it works**:

```python
# Legend AI validates:
expected_signature = HMAC-SHA256(payload, TRADINGVIEW_WEBHOOK_SECRET)
if expected_signature == X-TradingView-Signature:
    # Process webhook
else:
    # Reject (401 Unauthorized)
```

### Rate Limiting

- **Default**: 100 requests per minute per IP
- **Configurable**: Set `TRADINGVIEW_RATE_LIMIT_PER_MINUTE`
- **Response**: `429 Too Many Requests` when exceeded

### IP Logging

All webhook requests log the sender's IP address for audit trails.

---

## Troubleshooting

### Webhook Not Receiving

**Issue**: TradingView alerts aren't reaching Legend AI

**Solutions**:
1. Verify webhook URL is correct
2. Check TradingView alert is enabled and active
3. Check Legend AI logs for errors
4. Verify firewall/proxy settings
5. Test with curl:

```bash
curl -X POST https://your-domain.com/api/tradingview/webhooks/tradingview \
  -H "Content-Type: application/json" \
  -d '{"ticker":"TEST","close":100,"message":"test"}'
```

### Alerts Not Confirmed

**Issue**: Pattern alerts not being confirmed by Legend AI

**Solutions**:
1. Check pattern detection is working: `POST /api/patterns/detect`
2. Verify symbol is valid and has data
3. Check Legend AI score threshold (default ≥ 7)
4. Review alert logs: `GET /api/tradingview/alerts?symbol=AAPL`

### Rate Limit Errors

**Issue**: Getting `429 Too Many Requests`

**Solutions**:
1. Increase `TRADINGVIEW_RATE_LIMIT_PER_MINUTE`
2. Reduce alert frequency in TradingView
3. Use batch processing for multiple symbols

### Database Errors

**Issue**: Errors saving alerts to database

**Solutions**:
1. Run database migration: `alembic upgrade head`
2. Verify database connection: Check `DATABASE_URL`
3. Check database logs for errors

---

## Database Schema

### `tradingview_alerts`

Stores all received TradingView alerts.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key |
| `ticker_id` | Integer | Foreign key to tickers |
| `symbol` | String | Ticker symbol |
| `alert_type` | String | price, indicator, pattern, breakout, stop_loss |
| `alert_name` | String | Name of alert in TradingView |
| `message` | Text | Full alert message |
| `trigger_price` | Float | Price at trigger |
| `trigger_time` | String | TradingView timestamp |
| `interval` | String | Timeframe (1m, 5m, 1h, 1D, etc.) |
| `indicator_values` | Text | JSON of indicator values |
| `strategy_name` | String | Strategy that triggered alert |
| `action` | String | buy, sell, long, short, exit |
| `processed` | Boolean | Whether alert has been processed |
| `confirmed` | Boolean | Whether confirmed by Legend AI |
| `legend_score` | Float | Legend AI confirmation score |
| `webhook_ip` | String | Sender IP address |
| `received_at` | DateTime | When alert was received |
| `processed_at` | DateTime | When alert was processed |

### `tradingview_strategies`

Stores imported TradingView strategies.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key |
| `name` | String | Strategy name |
| `description` | Text | Strategy description |
| `pine_script_code` | Text | Optional Pine Script code |
| `strategy_config` | Text | JSON of strategy parameters |
| `timeframe` | String | Default timeframe |
| `indicators_used` | Text | JSON array of indicators |
| `entry_conditions` | Text | JSON of entry rules |
| `exit_conditions` | Text | JSON of exit rules |
| `risk_reward_ratio` | Float | R:R ratio |
| `win_rate` | Float | Historical win rate |
| `profit_factor` | Float | Profit factor |
| `max_drawdown` | Float | Max drawdown |
| `total_trades` | Integer | Total trades |
| `backtest_results` | Text | JSON of Legend AI backtest results |
| `legend_optimized` | Boolean | Whether optimized by Legend AI |
| `created_at` | DateTime | Import timestamp |
| `updated_at` | DateTime | Last update |

### `tradingview_sync`

Tracks bidirectional sync between systems.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key |
| `sync_type` | String | watchlist, pattern, alert, chart |
| `legend_id` | Integer | ID in Legend AI system |
| `tradingview_alert_id` | String | TradingView alert ID |
| `symbol` | String | Ticker symbol |
| `direction` | String | legend_to_tv, tv_to_legend, bidirectional |
| `status` | String | pending, synced, failed |
| `sync_data` | Text | JSON of sync payload |
| `error_message` | Text | Error if sync failed |
| `last_synced_at` | DateTime | Last sync timestamp |
| `created_at` | DateTime | Creation timestamp |

---

## Advanced Features

### Custom Alert Routing

You can customize alert processing by editing `app/services/tradingview.py`:

```python
async def _process_pattern_alert(self, db: Session, tv_alert: TradingViewAlert):
    # Custom logic here
    # Example: Only process alerts with score > 8.5
    if tv_alert.legend_score and tv_alert.legend_score > 8.5:
        # Send to premium Telegram channel
        pass
```

### Multi-Account Support

Track alerts per user by setting `user_id` in the alert payload:

```json
{
  "ticker": "AAPL",
  "user_id": "telegram_123456",
  "message": "Custom alert"
}
```

### Custom Indicators

Pass custom indicator values in the webhook:

```json
{
  "ticker": "NVDA",
  "custom_indicator_1": 75.5,
  "custom_indicator_2": -10.2
}
```

Access in processing:

```python
# app/services/tradingview.py
indicator_values = json.loads(tv_alert.indicator_values or "{}")
custom_1 = indicator_values.get("custom_indicator_1")
```

---

## Performance Tips

1. **Use Rate Limiting**: Prevent webhook spam
2. **Batch Alerts**: For universe scans, batch alerts instead of individual webhooks
3. **Optimize Database**: Index frequently queried fields (symbol, alert_type, received_at)
4. **Cache Pattern Results**: Cache Legend AI pattern detection results
5. **Async Processing**: Process alerts asynchronously for high volume

---

## Support

For issues or questions:

1. Check [Troubleshooting](#troubleshooting) section
2. Review API logs
3. Check database for alert records
4. Test endpoints with curl/Postman
5. Open issue on GitHub

---

## Changelog

### v1.0.0 (2025-01-15)

- Initial TradingView integration
- Webhook receiver with signature validation
- 5 alert types: price, indicator, pattern, breakout, stop-loss
- Pattern confirmation with Legend AI
- Two-way sync for patterns and watchlists
- Strategy import and backtesting
- Rate limiting and security features
- Comprehensive API documentation

---

## License

This integration is part of Legend AI and follows the same license.
