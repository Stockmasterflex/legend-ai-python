# Comprehensive Alerting Infrastructure

## Overview

The Legend AI platform now includes a comprehensive, production-ready alerting infrastructure that provides real-time monitoring, multi-channel notifications, and AI-powered alert suggestions for trading activities.

## Features

### 1. Alert Types

The system supports 6 major alert types:

- **Price Alerts**: Monitor price levels, percentage changes, and price targets
- **Pattern Detected Alerts**: Get notified when chart patterns form (VCP, Cup & Handle, etc.)
- **Volume Spike Alerts**: Track unusual volume activity
- **Technical Indicator Crosses**: Monitor RSI, MACD, moving average crosses
- **News Sentiment Alerts**: Alert on sentiment changes (when integrated)
- **Options Flow Alerts**: Track unusual options activity

### 2. Alert Conditions Builder

Build complex alert conditions with a flexible, visual condition builder:

- **Multiple Conditions**: Add multiple conditions per alert
- **AND/OR Logic**: Combine conditions with AND or OR logic
- **Operators**: Support for `>`, `<`, `>=`, `<=`, `==`, `crosses_above`, `crosses_below`, `percentage_change`
- **Time-based Conditions**: Set time windows for condition evaluation
- **Complex Expressions**: Build sophisticated alert logic

Example:
```python
from app.services.alert_rule_engine import ConditionBuilder

# Build an alert for price breakout with volume confirmation
builder = ConditionBuilder()
alert_conditions = (builder
    .price("greater_than", 150.00)
    .volume("greater_than", 50, value_type="percentage")  # 50% above average
    .rsi("greater_than", 60)
    .and_logic()
    .build()
)
```

### 3. Multi-Channel Delivery

Deliver alerts across 7 different channels:

- **Telegram Bot**: Rich formatted messages with inline actions
- **Email Notifications**: Professional HTML emails via SendGrid
- **SMS**: Text message alerts via Twilio integration
- **Discord Webhooks**: Send alerts to Discord channels
- **Slack Integration**: Post alerts to Slack channels
- **Custom Webhooks**: Send to any HTTP endpoint (N8N, Zapier, etc.)
- **Push Notifications**: Web push notifications (requires web push setup)

### 4. Alert Management

Complete CRUD operations for managing alerts:

- **Create**: Define new alert rules
- **Read**: View all alerts or specific alerts
- **Update**: Modify alert conditions and settings
- **Delete**: Remove alert rules
- **Snooze**: Temporarily disable alerts (1 min - 1 week)
- **Bulk Operations**: Enable, disable, delete, or snooze multiple alerts at once
- **Alert History**: View complete alert trigger history
- **Performance Tracking**: Analyze alert effectiveness and delivery rates

### 5. Smart Alerts

AI-powered alert suggestions:

- **AI-Suggested Alerts**: Claude analyzes market conditions and suggests relevant alerts
- **Pattern-Based Auto-Alerts**: Automatically suggest alerts based on detected patterns
- **Risk-Based Alerts**: Suggest stop losses, take profits, and trailing stops
- **Correlation Alerts**: Monitor SPY, VIX, and correlated instruments

## API Endpoints

### Alert Management

#### Create Alert Rule
```http
POST /api/alert-management/rules
Content-Type: application/json

{
  "name": "AAPL Price Breakout",
  "description": "Alert when AAPL breaks above $180 with volume",
  "ticker_symbol": "AAPL",
  "alert_type": "price",
  "condition_logic": "AND",
  "conditions": [
    {
      "field": "price",
      "operator": "greater_than",
      "value": 180,
      "value_type": "absolute"
    },
    {
      "field": "volume",
      "operator": "greater_than",
      "value": 50,
      "value_type": "percentage"
    }
  ],
  "delivery_channels": ["telegram", "email"],
  "is_enabled": true,
  "check_frequency": 60,
  "cooldown_period": 3600
}
```

#### Get All Alert Rules
```http
GET /api/alert-management/rules?is_enabled=true&limit=100
```

#### Update Alert Rule
```http
PUT /api/alert-management/rules/{rule_id}
Content-Type: application/json

{
  "is_enabled": false
}
```

#### Snooze Alert
```http
POST /api/alert-management/rules/{rule_id}/snooze
Content-Type: application/json

{
  "duration_minutes": 60
}
```

#### Bulk Operations
```http
POST /api/alert-management/rules/bulk
Content-Type: application/json

{
  "rule_ids": [1, 2, 3],
  "operation": "disable"
}
```

#### Get Alert History
```http
GET /api/alert-management/history?alert_type=price&limit=100
```

#### Get Alert Performance
```http
GET /api/alert-management/performance?days=30
```

### Smart Alerts

#### Get AI Suggestions
```http
POST /api/smart-alerts/suggest
Content-Type: application/json

{
  "ticker_symbol": "AAPL",
  "suggestion_types": ["ai", "pattern", "risk", "correlation"]
}
```

#### Auto-Create Alert from Suggestion
```http
POST /api/smart-alerts/auto-create
Content-Type: application/json

{
  "suggestion": {
    "ticker_symbol": "AAPL",
    "name": "AAPL Stop Loss",
    "alert_type": "price",
    "conditions": [...],
    "delivery_channels": ["telegram", "email"]
  }
}
```

#### Discover Alert Opportunities
```http
GET /api/smart-alerts/discover?limit=10
```

## Database Schema

### AlertRule Table
```sql
CREATE TABLE alert_rules (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    ticker_id INTEGER REFERENCES tickers(id),
    alert_type VARCHAR(50) NOT NULL,
    condition_logic VARCHAR(10) DEFAULT 'AND',
    conditions JSON NOT NULL,
    delivery_channels JSON NOT NULL,
    delivery_config JSON,
    is_enabled BOOLEAN DEFAULT TRUE,
    is_snoozed BOOLEAN DEFAULT FALSE,
    snoozed_until TIMESTAMP WITH TIME ZONE,
    check_frequency INTEGER DEFAULT 60,
    cooldown_period INTEGER DEFAULT 3600,
    last_triggered_at TIMESTAMP WITH TIME ZONE,
    trigger_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    created_by VARCHAR(50) DEFAULT 'user'
);
```

### AlertLog Table (Enhanced)
```sql
CREATE TABLE alert_logs (
    id SERIAL PRIMARY KEY,
    rule_id INTEGER REFERENCES alert_rules(id) ON DELETE SET NULL,
    ticker_id INTEGER REFERENCES tickers(id),
    user_id VARCHAR(100),
    alert_type VARCHAR(50),
    alert_title VARCHAR(200),
    alert_message TEXT,
    trigger_price FLOAT,
    trigger_value FLOAT,
    trigger_data JSON,
    conditions_met JSON,
    delivery_channels JSON,
    delivery_status JSON,
    sent_via VARCHAR(200),
    status VARCHAR(20) DEFAULT 'sent',
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    dismissed_at TIMESTAMP WITH TIME ZONE,
    response_time_ms INTEGER,
    alert_sent_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### AlertDelivery Table
```sql
CREATE TABLE alert_deliveries (
    id SERIAL PRIMARY KEY,
    alert_log_id INTEGER REFERENCES alert_logs(id) ON DELETE CASCADE,
    channel VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending',
    attempts INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 3,
    last_attempt_at TIMESTAMP WITH TIME ZONE,
    next_retry_at TIMESTAMP WITH TIME ZONE,
    delivered_at TIMESTAMP WITH TIME ZONE,
    failed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    external_id VARCHAR(200),
    channel_metadata JSON,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Architecture

### Components

1. **Alert Rule Engine** (`app/services/alert_rule_engine.py`)
   - Evaluates alert conditions against market data
   - Supports complex logic (AND/OR)
   - Handles time-based conditions
   - Manages cooldown periods

2. **Alert Delivery Service** (`app/services/alert_delivery.py`)
   - Multi-channel delivery system
   - Retry logic with exponential backoff
   - Delivery status tracking
   - Channel-specific formatting

3. **Alert Scheduler** (`app/services/alert_scheduler.py`)
   - Background monitoring using APScheduler
   - Checks all active rules every minute
   - Auto-scaling based on rule count
   - Non-blocking, asynchronous execution

4. **Smart Alert Service** (`app/services/smart_alerts.py`)
   - AI-powered alert suggestions
   - Pattern-based auto-alerts
   - Risk management alerts
   - Correlation monitoring

## Configuration

### Environment Variables

Add these to your `.env` file:

```bash
# Existing configurations
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
SENDGRID_API_KEY=your_sendgrid_key
ALERT_EMAIL=your@email.com

# New configurations for comprehensive alerting
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=+1234567890
ALERT_PHONE_NUMBER=+1234567890

DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...

OPENROUTER_API_KEY=your_openrouter_key  # For AI suggestions
```

### Database Migration

Run the database migration to create the new tables:

```bash
alembic upgrade head
```

Or manually run:

```bash
alembic upgrade 001
```

## Usage Examples

### Example 1: Price Alert with Volume Confirmation

```python
import httpx

# Create a price breakout alert
alert = {
    "name": "NVDA Breakout Alert",
    "description": "Alert when NVDA breaks above $500 with high volume",
    "ticker_symbol": "NVDA",
    "alert_type": "price",
    "condition_logic": "AND",
    "conditions": [
        {"field": "price", "operator": ">", "value": 500, "value_type": "absolute"},
        {"field": "volume", "operator": ">", "value": 50, "value_type": "percentage"}
    ],
    "delivery_channels": ["telegram", "email", "sms"],
    "check_frequency": 60,
    "cooldown_period": 3600
}

async with httpx.AsyncClient() as client:
    response = await client.post("http://localhost:8000/api/alert-management/rules", json=alert)
    print(response.json())
```

### Example 2: RSI Oversold Alert

```python
alert = {
    "name": "SPY Oversold Alert",
    "description": "Alert when SPY RSI drops below 30",
    "ticker_symbol": "SPY",
    "alert_type": "indicator",
    "condition_logic": "AND",
    "conditions": [
        {"field": "rsi", "operator": "<", "value": 30, "value_type": "absolute"}
    ],
    "delivery_channels": ["telegram"],
    "check_frequency": 300,  # Check every 5 minutes
    "cooldown_period": 7200   # Don't re-alert for 2 hours
}
```

### Example 3: Pattern Detection Alert

```python
alert = {
    "name": "VCP Pattern Alert - AAPL",
    "description": "Alert when VCP pattern is detected on AAPL",
    "ticker_symbol": "AAPL",
    "alert_type": "pattern",
    "condition_logic": "AND",
    "conditions": [
        {"field": "pattern_score", "operator": ">=", "value": 0.75, "value_type": "absolute"}
    ],
    "delivery_channels": ["telegram", "email", "discord"],
    "check_frequency": 3600,  # Check every hour
    "cooldown_period": 86400  # Don't re-alert for 24 hours
}
```

### Example 4: Get AI Suggestions

```python
async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/api/smart-alerts/suggest",
        json={
            "ticker_symbol": "TSLA",
            "suggestion_types": ["ai", "risk"]
        }
    )
    suggestions = response.json()["suggestions"]

    # Auto-create the first suggestion
    if suggestions:
        await client.post(
            "http://localhost:8000/api/smart-alerts/auto-create",
            json={"suggestion": suggestions[0]}
        )
```

## Alert Scheduler

The alert scheduler runs automatically on application startup and monitors all active alert rules:

- **Check Frequency**: Every 60 seconds (configurable)
- **Parallel Processing**: Monitors multiple tickers simultaneously
- **Auto-scaling**: Adjusts based on number of active rules
- **Market Hours Aware**: Can be configured to only check during market hours

### Scheduler Status

Check scheduler status:

```http
GET /api/alerts/health
```

## Performance Tracking

Track alert performance and delivery rates:

```http
GET /api/alert-management/performance?days=30
```

Response:
```json
{
  "period_days": 30,
  "total_alerts": 156,
  "alerts_by_type": {
    "price": 89,
    "pattern": 45,
    "indicator": 22
  },
  "alerts_by_channel": {
    "telegram": 156,
    "email": 120,
    "sms": 45
  },
  "delivery_success_rates": {
    "telegram": 98.7,
    "email": 95.8,
    "sms": 92.3
  }
}
```

## Best Practices

1. **Cooldown Periods**: Set appropriate cooldown periods to avoid alert spam
2. **Condition Logic**: Use AND for stricter alerts, OR for broader coverage
3. **Multi-Channel Delivery**: Use SMS for critical alerts, Telegram for regular updates
4. **Smart Alerts**: Regularly review AI suggestions for new opportunities
5. **Alert History**: Analyze performance to refine alert conditions
6. **Snooze Feature**: Use snooze during news events or volatile periods
7. **Bulk Operations**: Manage multiple alerts efficiently during different market conditions

## Troubleshooting

### Alert Not Triggering

1. Check if rule is enabled: `GET /api/alert-management/rules/{rule_id}`
2. Verify conditions are correctly formatted
3. Check cooldown period hasn't been triggered recently
4. Ensure market data is available for the ticker

### Delivery Failures

1. Check delivery status: `GET /api/alert-management/history`
2. Verify API keys are configured correctly
3. Check external service status (Telegram, SendGrid, Twilio)
4. Review error messages in `alert_deliveries` table

### Scheduler Not Running

1. Check logs for scheduler startup errors
2. Verify APScheduler is installed: `pip list | grep apscheduler`
3. Check database connectivity
4. Review scheduler status: `GET /api/alerts/health`

## Future Enhancements

- [ ] Machine learning-based alert optimization
- [ ] Alert templates library
- [ ] Mobile app integration
- [ ] Voice alerts (Twilio voice calls)
- [ ] Alert sharing and social features
- [ ] Advanced backtesting for alert conditions
- [ ] Market hours awareness (only alert during trading hours)
- [ ] Multi-user support with permissions

## Support

For issues or questions:
- GitHub Issues: https://github.com/Stockmasterflex/legend-ai-python/issues
- Documentation: `/docs` endpoint
- API Documentation: `/api/docs/getting-started`

---

**Built with ❤️ for swing traders by Legend AI**
