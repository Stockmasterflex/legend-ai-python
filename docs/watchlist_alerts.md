# Real-Time Watchlist Alerts

## Overview

Real-time monitoring system that watches your watchlist tickers and sends Telegram alerts when patterns form or price targets are hit.

## Features

- 🔔 **Pattern Formation Alerts** - Notified when new patterns are detected
- 💰 **Price Target Alerts** - Alert when entry or stop prices are reached
- ⏰ **Scheduled Monitoring** - Checks watchlist every 5 minutes
- 📜 **Alert History** - Track all sent alerts
- 🔕 **Mute Controls** - Temporarily disable alerts
- ⚙️ **Alert Preferences** - Customize alert frequency and types

## Quick Start

### Start Monitoring Service

```bash
# Run as background service
python app/tasks/watchlist_monitor.py

# Or with custom interval (in minutes)
WATCHLIST_CHECK_INTERVAL_MINUTES=10 python app/tasks/watchlist_monitor.py

# Run as systemd service (recommended for production)
sudo systemctl start watchlist-monitor
```

### Add Ticker with Alerts

```bash
# Add to watchlist with alert preferences
curl -X POST http://localhost:8000/api/watchlist/add \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "reason": "VCP pattern forming",
    "target_entry": 150.00,
    "target_stop": 145.00,
    "alerts_enabled": true,
    "alert_on_pattern": true,
    "alert_on_price_target": true
  }'
```

### Check Watchlist Manually

```bash
# Trigger immediate check
curl -X POST http://localhost:8000/api/alerts/watchlist/check-now
```

## API Endpoints

### GET /api/alerts/watchlist/history

Get alert history for a user.

**Parameters:**
- `user_id` (default: "default"): User ID
- `limit` (default: 50, max: 200): Number of alerts
- `days` (default: 30, max: 180): Days to look back

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 123,
      "ticker": "AAPL",
      "alert_type": "Pattern Detected",
      "trigger_price": 150.00,
      "sent_at": "2024-01-15T10:30:00",
      "sent_via": "telegram",
      "status": "sent",
      "message": "📊 Pattern Detected..."
    }
  ],
  "count": 15
}
```

### POST /api/alerts/watchlist/mute

Mute alerts for a specific ticker.

**Request Body:**
```json
{
  "ticker_symbol": "AAPL",
  "duration_hours": 24
}
```

**Response:**
```json
{
  "success": true,
  "message": "Alerts muted for AAPL for 24 hours"
}
```

### POST /api/alerts/watchlist/unmute

Unmute alerts for a ticker.

**Parameters:**
- `ticker_symbol`: Ticker to unmute
- `user_id` (optional): User ID

**Response:**
```json
{
  "success": true,
  "message": "Alerts unmuted for AAPL"
}
```

### POST /api/alerts/watchlist/check-now

Manually trigger a watchlist check.

**Response:**
```json
{
  "success": true,
  "message": "Watchlist check triggered"
}
```

### GET /api/alerts/watchlist/status

Get monitoring service status.

**Response:**
```json
{
  "success": true,
  "is_running": true,
  "message": "Monitoring active"
}
```

## Alert Types

### 1. Pattern Formation Alert

Sent when a new pattern is detected on a watchlist ticker.

**Example:**
```
📊 Pattern Detected

Ticker: AAPL
Pattern: VCP
Confidence: 85.0%

Entry: $150.00
Target: $165.00 (+10.0%)
Stop: $145.00 (-3.3%)
Risk/Reward: 3.00

Detected at 2024-01-15 10:30:00
```

### 2. Price Target Alert

Sent when entry or stop price is reached.

**Example:**
```
🚨 Target Entry Price Reached

Ticker: AAPL
Current Price: $150.00
Target Entry: $150.00
Stop Loss: $145.00

Alert triggered at 2024-01-15 14:30:00
```

### 3. Stop Loss Alert

Sent when price drops to stop loss level.

**Example:**
```
🚨 Stop Loss Triggered

Ticker: AAPL
Current Price: $145.00
Target Entry: $150.00
Stop Loss: $145.00

Alert triggered at 2024-01-15 16:45:00
```

## Alert Frequency Settings

Control how often alerts are sent:

| Frequency | Behavior |
|-----------|----------|
| `once` | Alert only once per event |
| `hourly` | Alert maximum once per hour |
| `daily` | Alert maximum once per day |
| `always` | Alert every time (can be spammy) |
| `disabled` | No alerts |

**Update Frequency:**
```bash
# Via database
UPDATE watchlists
SET alert_frequency = 'daily'
WHERE ticker_id = (SELECT id FROM tickers WHERE symbol = 'AAPL');
```

## Watchlist Preferences

Each watchlist item has these alert settings:

```python
{
    "alerts_enabled": True,           # Master switch
    "alert_on_pattern": True,         # Alert on pattern formation
    "alert_on_price_target": True,    # Alert on target price
    "alert_on_stop_loss": True,       # Alert on stop loss
    "alert_frequency": "once"         # How often to alert
}
```

## Setup as Background Service

### Systemd Service (Linux)

Create `/etc/systemd/system/watchlist-monitor.service`:

```ini
[Unit]
Description=Legend AI Watchlist Monitor
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/legend-ai-python
Environment="DATABASE_URL=postgresql://..."
Environment="REDIS_URL=redis://..."
Environment="TELEGRAM_BOT_TOKEN=..."
Environment="WATCHLIST_CHECK_INTERVAL_MINUTES=5"
ExecStart=/usr/bin/python3 app/tasks/watchlist_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Start service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable watchlist-monitor
sudo systemctl start watchlist-monitor

# Check status
sudo systemctl status watchlist-monitor

# View logs
sudo journalctl -u watchlist-monitor -f
```

### Docker Compose

Add to `docker-compose.yml`:

```yaml
services:
  watchlist-monitor:
    build: .
    command: python app/tasks/watchlist_monitor.py
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - WATCHLIST_CHECK_INTERVAL_MINUTES=5
    restart: unless-stopped
    depends_on:
      - postgres
      - redis
```

**Start:**
```bash
docker-compose up -d watchlist-monitor
docker-compose logs -f watchlist-monitor
```

### Railway Deployment

Railway doesn't support long-running background tasks natively. Use external scheduler:

**Option 1: Cron Job Service**
```bash
# Use cron-job.org or similar to hit endpoint
# Schedule: */5 * * * * (every 5 minutes)
# URL: POST https://your-app.railway.app/api/alerts/watchlist/check-now
```

**Option 2: GitHub Actions**
```yaml
# .github/workflows/watchlist_monitor.yml
name: Watchlist Monitor

on:
  schedule:
    - cron: '*/5 * * * *'  # Every 5 minutes

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger watchlist check
        run: |
          curl -X POST https://your-app.railway.app/api/alerts/watchlist/check-now
```

## Monitoring Workflow

### How It Works

1. **Monitoring Loop** - Runs every N minutes (default: 5)
2. **Fetch Watchlist** - Gets all active watchlist items with alerts enabled
3. **Check Each Ticker:**
   - Fetch current price
   - Check if price targets reached
   - Check for new pattern formation
   - Run pattern detection if needed
4. **Send Alerts:**
   - Check alert frequency settings
   - Verify not muted
   - Send Telegram notification
   - Log alert to database
5. **Repeat**

### Flowchart

```
┌─────────────────────┐
│ Start Monitor Loop  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Get Watchlist Items │
│ (alerts_enabled=true)│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ For Each Ticker:    │
│  - Get current price│
│  - Check targets    │
│  - Check patterns   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Should Send Alert?  │
│  - Check frequency  │
│  - Check mute       │
└──────────┬──────────┘
           │
       ┌───┴───┐
       │  Yes  │
       └───┬───┘
           │
           ▼
┌─────────────────────┐
│ Send Telegram Alert │
│ Log to Database     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Wait N Minutes      │
└──────────┬──────────┘
           │
           └──────────────┐
                          │
                          ▼
                    (Loop back)
```

## Example Use Cases

### Use Case 1: Pattern Formation Alerts

Monitor watchlist for new pattern formations:

```python
# Add tickers with pattern alerts
tickers = ["AAPL", "MSFT", "GOOGL", "TSLA"]

for ticker in tickers:
    add_to_watchlist(
        symbol=ticker,
        alerts_enabled=True,
        alert_on_pattern=True,
        alert_frequency="once"  # Alert once when pattern forms
    )

# Start monitoring
python app/tasks/watchlist_monitor.py
```

### Use Case 2: Entry Price Alerts

Get notified when stocks reach your target entry:

```python
# Add with specific entry prices
add_to_watchlist(
    symbol="AAPL",
    target_entry=150.00,
    alert_on_price_target=True,
    alert_frequency="once"
)

# When price reaches $150, you'll get:
# "🚨 Target Entry Price Reached - AAPL at $150.00"
```

### Use Case 3: Breakout Monitoring

Monitor for breakouts with alerts:

```python
# Add stocks near breakout
add_to_watchlist(
    symbol="NVDA",
    target_entry=500.00,  # Breakout level
    target_stop=480.00,   # Invalidation
    alert_on_pattern=True,
    alert_on_price_target=True,
    alert_frequency="hourly"  # Can alert multiple times
)
```

## Alert History

View all alerts sent:

```bash
# Last 50 alerts
curl http://localhost:8000/api/alerts/watchlist/history

# Last 7 days
curl "http://localhost:8000/api/alerts/watchlist/history?days=7"

# Specific user
curl "http://localhost:8000/api/alerts/watchlist/history?user_id=123456789"
```

## Mute Controls

### Temporary Mute

```bash
# Mute for 24 hours
curl -X POST http://localhost:8000/api/alerts/watchlist/mute \
  -H "Content-Type: application/json" \
  -d '{"ticker_symbol": "AAPL", "duration_hours": 24}'
```

### Permanent Mute

```bash
# Mute until manually unmuted
curl -X POST http://localhost:8000/api/alerts/watchlist/mute \
  -H "Content-Type: application/json" \
  -d '{"ticker_symbol": "AAPL"}'
```

### Unmute

```bash
curl -X POST "http://localhost:8000/api/alerts/watchlist/unmute?ticker_symbol=AAPL"
```

## Performance Considerations

### Rate Limiting

- **Market Data API**: Respect rate limits (500/day for free tier)
- **Pattern Detection**: Can be CPU-intensive
- **Telegram API**: Max 30 messages/second

### Optimization Tips

1. **Adjust Check Interval** - 5-15 minutes is usually sufficient
2. **Limit Watchlist Size** - Keep under 50 tickers for fast checks
3. **Use Confidence Threshold** - Only alert on high-confidence patterns (>= 0.7)
4. **Cache Market Data** - Reduce API calls
5. **Batch Processing** - Check multiple tickers in parallel

## Troubleshooting

### Alerts Not Sending

```bash
# Check service status
curl http://localhost:8000/api/alerts/watchlist/status

# Check Telegram bot
curl http://localhost:8000/health/detailed | jq '.telegram'

# View logs
sudo journalctl -u watchlist-monitor -f

# Or Docker logs
docker-compose logs -f watchlist-monitor
```

### Missing Alerts

- Verify `alerts_enabled = true` on watchlist item
- Check `alert_frequency` setting
- Ensure not muted (`muted_until` is null)
- Verify pattern detection is working

### Too Many Alerts

- Change `alert_frequency` to 'daily' or 'once'
- Increase confidence threshold
- Mute specific tickers temporarily

## Best Practices

1. **Start Small** - Add 10-20 tickers initially
2. **Use 'Once' Frequency** - Avoid alert spam
3. **Set Realistic Targets** - Don't set too many price alerts
4. **Monitor Regularly** - Check alert history weekly
5. **Mute When Needed** - Temporarily mute during high volatility
6. **Review Performance** - Disable alerts for low-accuracy patterns

## Related Documentation

- [Watchlist API](../api/watchlist.md)
- [Pattern Detection](./pattern_detection.md)
- [Telegram Bot](./telegram_bot.md)
- [Deployment Guide](../deploy/README.md)
