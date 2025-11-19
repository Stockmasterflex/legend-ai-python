# Pattern Validation System

## Overview

Advanced pattern validation system that tracks pattern accuracy, calculates win/loss rates, and provides performance analytics to continuously improve pattern detection.

## Features

- ✅ **Pattern Outcome Tracking** - Record whether patterns hit targets or stops
- 📊 **Performance Metrics** - Win rates, average gains, max drawdown per pattern
- 🏆 **Pattern Leaderboard** - Rank patterns by performance
- ⚠️ **Auto-Disable Poor Performers** - Identify patterns with low accuracy
- 🔄 **Automatic Validation** - Check historical data to validate outcomes
- 📈 **Backtesting Framework** - Test patterns on historical data
- 🎯 **ML-Ready** - Export data for machine learning models

## Quick Start

### View Pattern Performance

```bash
# Get all pattern performance metrics
curl http://localhost:8000/api/validation/performance

# Filter by specific pattern
curl "http://localhost:8000/api/validation/performance?pattern_type=VCP"
```

### Get Pattern Leaderboard

```bash
# Top 10 patterns
curl http://localhost:8000/api/validation/leaderboard

# Top 5 patterns
curl "http://localhost:8000/api/validation/leaderboard?limit=5"
```

### Auto-Validate Patterns

```bash
# Validate patterns from last 30 days
curl -X POST "http://localhost:8000/api/validation/auto-validate?lookback_days=30"

# Or run scheduled task
python app/tasks/auto_validate_patterns.py
```

### Get Validation Dashboard

```bash
# Comprehensive dashboard data
curl http://localhost:8000/api/validation/dashboard
```

## API Endpoints

### GET /api/validation/performance

Get performance metrics for all patterns or specific pattern type.

**Parameters:**
- `pattern_type` (optional): Filter by pattern type
- `min_samples` (default: 5): Minimum number of validated patterns to include

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "pattern_type": "VCP",
      "total_trades": 45,
      "wins": 32,
      "losses": 13,
      "win_rate": 71.11,
      "avg_gain_loss": 8.5,
      "avg_confidence": 0.75,
      "max_gain": 25.3,
      "max_loss": -8.2,
      "status": "excellent"
    }
  ],
  "count": 8
}
```

**Pattern Status:**
- `excellent`: Win rate >= 60%
- `good`: Win rate >= 50%
- `acceptable`: Win rate >= 40%
- `poor`: Win rate < 40%
- `testing`: < 10 samples

### GET /api/validation/leaderboard

Get top performing patterns ranked by win rate.

**Parameters:**
- `limit` (default: 10, max: 50): Number of patterns to return

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "pattern_type": "Cup & Handle",
      "total_trades": 28,
      "wins": 22,
      "losses": 6,
      "win_rate": 78.57,
      "avg_gain_loss": 12.4,
      "status": "excellent"
    }
  ],
  "count": 10
}
```

### GET /api/validation/to-disable

Get list of patterns that should be disabled due to poor performance.

**Parameters:**
- `min_samples` (default: 20): Minimum trades to consider
- `max_win_rate` (default: 35.0): Maximum acceptable win rate

**Response:**
```json
{
  "success": true,
  "patterns_to_disable": [
    "Double Bottom",
    "Symmetrical Triangle"
  ],
  "count": 2,
  "criteria": {
    "min_samples": 20,
    "max_win_rate": 35.0
  }
}
```

### POST /api/validation/record-outcome

Manually record the outcome of a pattern prediction.

**Request Body:**
```json
{
  "scan_id": 123,
  "outcome": "hit_target",
  "outcome_price": 155.50,
  "actual_gain_loss": 8.5,
  "notes": "Breakout on high volume"
}
```

**Outcome Types:**
- `hit_target`: Price reached target
- `hit_stop`: Price hit stop loss
- `expired`: Pattern expired (30+ days)
- `partial`: Partial profit taken

**Response:**
```json
{
  "success": true,
  "message": "Outcome recorded for scan 123"
}
```

### POST /api/validation/auto-validate

Automatically validate patterns by checking historical price data.

**Parameters:**
- `lookback_days` (default: 30, max: 180): How far back to check

**Response:**
```json
{
  "success": true,
  "validated_count": 15,
  "message": "Validated 15 patterns"
}
```

### GET /api/validation/recent-validations

Get recently validated patterns with outcomes.

**Parameters:**
- `days` (default: 7, max: 90): Days to look back
- `limit` (default: 50, max: 200): Number of results

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 123,
      "ticker": "AAPL",
      "pattern_type": "VCP",
      "scanned_at": "2024-01-01T10:00:00",
      "outcome": "hit_target",
      "outcome_date": "2024-01-15T14:30:00",
      "entry_price": 150.00,
      "target_price": 165.00,
      "stop_loss": 145.00,
      "outcome_price": 165.00,
      "gain_loss": 10.0,
      "was_successful": true,
      "confidence": 0.85
    }
  ],
  "count": 15
}
```

### GET /api/validation/summary

Get overall validation statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_patterns": 250,
    "validated_patterns": 120,
    "unvalidated_patterns": 130,
    "validation_rate": 48.0,
    "successful_patterns": 78,
    "failed_patterns": 42,
    "success_rate": 65.0,
    "avg_gain_loss": 6.5
  }
}
```

### GET /api/validation/dashboard

Get comprehensive validation dashboard data.

**Response:**
```json
{
  "success": true,
  "data": {
    "summary": { ... },
    "top_patterns": [ ... ],
    "recent_validations": [ ... ],
    "poor_performers": [ ... ]
  }
}
```

### POST /api/validation/backtest

Backtest a pattern on historical data (coming soon).

**Request Body:**
```json
{
  "pattern_type": "VCP",
  "ticker_symbol": "AAPL",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31"
}
```

## Automated Validation

### Setup Cron Job

```bash
# Add to crontab
crontab -e

# Run daily at 3 AM
0 3 * * * /usr/bin/python3 /path/to/app/tasks/auto_validate_patterns.py
```

### GitHub Actions (Railway)

```yaml
# .github/workflows/auto_validate.yml
name: Auto Validate Patterns

on:
  schedule:
    - cron: '0 3 * * *'  # Daily at 3 AM UTC

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger validation
        run: |
          curl -X POST https://your-app.railway.app/api/validation/auto-validate?lookback_days=30
```

## Performance Metrics

### Key Metrics

| Metric | Description | Good | Acceptable | Poor |
|--------|-------------|------|------------|------|
| **Win Rate** | % of patterns that hit target | > 60% | 50-60% | < 50% |
| **Avg Gain/Loss** | Average % return per trade | > 8% | 5-8% | < 5% |
| **Max Gain** | Largest winning trade | > 20% | 10-20% | < 10% |
| **Max Loss** | Largest losing trade | < -5% | -5% to -8% | > -8% |
| **Profit Factor** | Total wins / Total losses | > 2.0 | 1.5-2.0 | < 1.5 |

### Pattern Status

- **Excellent** (>= 60% win rate): Keep using, high priority
- **Good** (>= 50% win rate): Reliable, use regularly
- **Acceptable** (>= 40% win rate): Monitor closely
- **Poor** (< 40% win rate): Consider disabling
- **Testing** (< 10 samples): Need more data

## Integration with Pattern Detection

### Automatic Recording

When a pattern is detected, it's automatically saved to the database:

```python
# In pattern scanner
await db_service.save_pattern_scan(
    ticker_symbol="AAPL",
    pattern_data={
        "pattern": "VCP",
        "confidence": 0.85,
        "entry": 150.00,
        "target": 165.00,
        "stop": 145.00
    }
)
```

### Manual Outcome Recording

When you take a trade based on a pattern:

```python
import requests

# When target is hit
requests.post("http://localhost:8000/api/validation/record-outcome", json={
    "scan_id": 123,
    "outcome": "hit_target",
    "outcome_price": 165.00,
    "actual_gain_loss": 10.0
})
```

### Auto-Validation Process

The auto-validation task:

1. Finds all patterns from the last N days without outcomes
2. Fetches historical price data for each pattern
3. Checks if target or stop was hit
4. Records the outcome and calculates gain/loss
5. Updates pattern statistics

## Dashboard Integration

### Add to Dashboard

```html
<!-- In your dashboard -->
<div id="pattern-performance">
  <h2>Pattern Performance</h2>
  <div id="leaderboard"></div>
  <div id="recent-validations"></div>
  <div id="poor-performers"></div>
</div>

<script>
// Fetch dashboard data
fetch('/api/validation/dashboard')
  .then(r => r.json())
  .then(data => {
    // Render leaderboard
    // Render recent validations
    // Show poor performers
  });
</script>
```

### Telegram Notifications

Get alerts about pattern performance:

```python
# In your validation task
if poor_performers:
    send_telegram(
        f"⚠️ Poor Performing Patterns:\n" +
        "\n".join([f"- {p}" for p in poor_performers])
    )
```

## Backtesting (Advanced)

### Run Historical Backtest

```python
from app.services.pattern_validation import PatternValidationService

service = PatternValidationService()

# Backtest VCP pattern on AAPL for 2023
results = await service.backtest_pattern(
    pattern_type="VCP",
    ticker_symbol="AAPL",
    start_date=datetime(2023, 1, 1),
    end_date=datetime(2023, 12, 31)
)

print(f"Win Rate: {results['win_rate']}%")
print(f"Profit Factor: {results['profit_factor']}")
```

## Machine Learning Integration

### Export for ML Training

```python
# Get pattern performance data
performance = await validation_service.get_pattern_performance()

# Export to CSV for ML models
import pandas as pd
df = pd.DataFrame(performance)
df.to_csv('pattern_performance.csv', index=False)

# Features for ML:
# - pattern_type
# - confidence
# - entry_price
# - target_price
# - stop_loss
# - risk_reward
# - rs_rating
# - sector
# - outcome (target variable)
```

## Best Practices

1. **Validate Regularly** - Run auto-validation daily
2. **Track All Patterns** - Record outcomes for accuracy
3. **Monitor Performance** - Check dashboard weekly
4. **Disable Poor Performers** - Remove patterns with < 40% win rate and 20+ samples
5. **Backtest Before Using** - Test new patterns on historical data
6. **Use Confidence Scores** - Only trade patterns with > 0.7 confidence
7. **Set Sample Size Threshold** - Need 20+ samples before trusting metrics

## Troubleshooting

### Auto-Validation Not Working

```bash
# Check database connection
psql $DATABASE_URL -c "SELECT COUNT(*) FROM pattern_scans;"

# Check market data service
curl "http://localhost:8000/api/market/quote?ticker=AAPL"

# Run manually with debug
python app/tasks/auto_validate_patterns.py
```

### Low Win Rates

- Check pattern detection logic
- Verify entry/target/stop calculations
- Review market conditions during trades
- Consider tighter filters (higher confidence threshold)

### Missing Outcomes

- Ensure auto-validation is running
- Check that historical data is available
- Verify patterns are old enough (> 7 days)

## Related Documentation

- [Pattern Detection](./pattern_detection.md)
- [Deployment Guide](../deploy/README.md)
- [API Documentation](./api.md)
