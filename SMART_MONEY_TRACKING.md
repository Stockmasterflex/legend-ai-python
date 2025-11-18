# Smart Money Tracking System

A comprehensive system for tracking institutional and smart money flows in the market.

## Overview

The Smart Money Tracking system monitors and analyzes four key areas:

1. **Dark Pool Prints** - Real-time dark pool transactions
2. **Institutional Ownership** - 13F filings and ownership changes
3. **Block Trade Alerts** - Large volume spikes and unusual options activity
4. **Analytics Dashboard** - Comprehensive smart money indicators

## Features

### 1. Dark Pool Tracking

Monitor off-exchange dark pool transactions to identify institutional positioning:

- **Real-time Prints**: Track dark pool transactions as they occur
- **Size & Price Analysis**: Analyze transaction sizes and price levels
- **Premium/Discount Calculations**: Identify trades at premium or discount to market
- **Historical Patterns**: Analyze dark pool volume trends over time
- **Unusual Activity Detection**: Alert on volume spikes above historical averages

**Key Metrics:**
- Dark Pool Ratio (dark pool volume / total volume)
- Premium/Discount percentage
- Bullish/Bearish sentiment distribution
- Large block analysis (>$1M transactions)

### 2. Institutional Ownership

Track institutional investors and their position changes:

- **13F Filings Analysis**: Process quarterly institutional holdings reports
- **Ownership Changes**: Track increases, decreases, new positions, and exits
- **Top Holders**: Monitor largest institutional stakeholders
- **Insider Transactions**: Track insider buying and selling activity

**Key Metrics:**
- Institutional ownership percentage
- Net institutional flow (buying vs selling)
- Number of new positions vs sold out positions
- Conviction score based on holder changes

### 3. Block Trade Alerts

Monitor large block trades and unusual options activity:

- **Large Volume Spikes**: Detect volume significantly above average
- **Unusual Sweeps**: Identify aggressive sweep orders across exchanges
- **Options Positioning**: Analyze call/put ratios and unusual options flow
- **Smart Money Divergence**: Detect divergence between price and smart money flow

**Alert Types:**
- Large block trades (>$10M)
- Unusual options sweeps (>3x normal volume)
- Volume spikes (>2x average)
- Price/flow divergence

### 4. Analytics Dashboard

Comprehensive dashboard combining all smart money data:

- **Smart Money Index**: Composite score (0-100) of overall smart money strength
- **Flow Analysis**: Net institutional and insider flows
- **Accumulation/Distribution**: Overall market sentiment
- **Divergence Detection**: Identify price/flow disconnects
- **Confidence Score**: Reliability of smart money signals

## API Endpoints

### Dark Pool Endpoints

```
GET /smart-money/dark-pool/{symbol}/prints
GET /smart-money/dark-pool/{symbol}/summary
GET /smart-money/dark-pool/{symbol}/patterns
GET /smart-money/dark-pool/{symbol}/unusual
```

### Institutional Endpoints

```
GET /smart-money/institutional/{symbol}/holders
GET /smart-money/institutional/{symbol}/changes
GET /smart-money/institutional/{symbol}/flow
GET /smart-money/institutional/{symbol}/insiders
GET /smart-money/institutional/{symbol}/insider-sentiment
```

### Block Trade Endpoints

```
GET /smart-money/blocks/{symbol}/recent
GET /smart-money/blocks/{symbol}/options
GET /smart-money/blocks/{symbol}/options-positioning
GET /smart-money/blocks/{symbol}/volume-spike
GET /smart-money/blocks/{symbol}/divergence
```

### Analytics Endpoints

```
GET /smart-money/analytics/{symbol}/flow
GET /smart-money/analytics/{symbol}/indicators
GET /smart-money/analytics/{symbol}/dashboard
GET /smart-money/alerts/{symbol}
```

### Dashboard UI

```
GET /smart-money/dashboard
```

## Usage Examples

### 1. Get Dark Pool Summary

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get(
        "http://localhost:8000/smart-money/dark-pool/AAPL/summary"
    )
    data = response.json()
    print(f"Dark Pool Volume: {data['total_volume']}")
    print(f"Premium Percentage: {data['premium_percentage']}%")
```

### 2. Check Institutional Flow

```python
response = await client.get(
    "http://localhost:8000/smart-money/institutional/AAPL/flow"
)
flow = response.json()
print(f"Flow Direction: {flow['flow_direction']}")
print(f"Net Change: {flow['net_change_percentage']}%")
```

### 3. Get Smart Money Indicators

```python
response = await client.get(
    "http://localhost:8000/smart-money/analytics/AAPL/indicators",
    params={"price_change": 2.5}
)
indicators = response.json()
print(f"Smart Money Index: {indicators['smart_money_index']}")
print(f"Accumulation Score: {indicators['accumulation_score']}")
```

### 4. Get Complete Dashboard Data

```python
response = await client.get(
    "http://localhost:8000/smart-money/analytics/AAPL/dashboard",
    params={
        "price_change": 1.5,
        "total_volume": 50000000
    }
)
dashboard = response.json()
```

### 5. Generate Demo Data (Testing)

```python
response = await client.post(
    "http://localhost:8000/smart-money/demo/AAPL/generate-data",
    params={"days": 7}
)
print(response.json())
```

## Dashboard UI

Access the interactive dashboard at:

```
http://localhost:8000/smart-money/dashboard
```

### Features:
- Real-time data visualization
- Interactive charts and tables
- Alert notifications
- Dark pool print feed
- Institutional holder rankings
- Block trade monitoring
- Options flow analysis

### Dashboard Sections:

1. **Key Metrics Cards**
   - Smart Money Index
   - Dark Pool Ratio
   - Institutional Ownership
   - Accumulation Score

2. **Alerts Panel**
   - Recent high-severity alerts
   - Large block notifications
   - Unusual options activity

3. **Dark Pool Activity**
   - Recent prints table
   - Daily summary statistics
   - Premium/discount analysis

4. **Institutional Holdings**
   - Top 10 holders
   - Position changes
   - Flow direction indicators

5. **Block Trades**
   - Recent large blocks
   - Trade type classification
   - Sentiment indicators

6. **Options Positioning**
   - Call/Put premium comparison
   - Call/Put ratio
   - Sentiment analysis

7. **Flow Analysis**
   - Institutional vs Insider flows
   - Net buying/selling
   - Overall accumulation/distribution

## Data Models

### Dark Pool Print

```python
{
    "symbol": "AAPL",
    "timestamp": "2025-11-18T10:30:00",
    "price": 178.50,
    "size": 500000,
    "value": 89250000.0,
    "premium_discount": 0.5,
    "market_price": 178.00,
    "is_premium": true,
    "sentiment": "bullish"
}
```

### Block Trade

```python
{
    "symbol": "AAPL",
    "timestamp": "2025-11-18T10:30:00",
    "trade_type": "sweep",
    "price": 178.50,
    "size": 250000,
    "value": 44625000.0,
    "is_options": false,
    "sentiment": "bullish",
    "volume_ratio": 3.5
}
```

### Smart Money Indicators

```python
{
    "symbol": "AAPL",
    "smart_money_index": 75.0,
    "dark_pool_ratio": 0.35,
    "dark_pool_sentiment": "bullish",
    "institutional_ownership": 62.5,
    "institutional_momentum": "strong_buying",
    "accumulation_score": 65.0,
    "unusual_activity_score": 78.5,
    "divergence_score": 12.5
}
```

## Interpretation Guide

### Smart Money Index (0-100)
- **75-100**: Strong institutional buying, high confidence
- **50-75**: Moderate bullish sentiment
- **25-50**: Moderate bearish sentiment
- **0-25**: Strong institutional selling, high risk

### Accumulation Score (-100 to 100)
- **> 50**: Strong accumulation phase
- **20-50**: Moderate accumulation
- **-20-20**: Neutral/sideways
- **-50 - -20**: Moderate distribution
- **< -50**: Strong distribution phase

### Dark Pool Ratio
- **> 40%**: Very high institutional interest
- **30-40%**: High institutional interest
- **20-30%**: Moderate institutional interest
- **< 20%**: Low institutional interest

### Flow Direction
- **strong_inflow**: Heavy institutional buying (>2% increase)
- **inflow**: Institutional buying
- **neutral**: Balanced activity
- **outflow**: Institutional selling
- **strong_outflow**: Heavy institutional selling (>2% decrease)

## Testing

Run the test suite:

```bash
pytest tests/test_smart_money.py -v
```

Test coverage includes:
- Dark pool service operations
- Institutional tracking
- Block trade detection
- Analytics calculations
- Integration workflows

## Architecture

### Service Layer

```
app/services/smart_money/
├── __init__.py
├── models.py              # Data models
├── dark_pool.py          # Dark pool tracking
├── institutional.py      # Institutional ownership
├── block_trades.py       # Block trade alerts
└── analytics.py          # Aggregated analytics
```

### API Layer

```
app/api/smart_money.py    # REST API endpoints
```

### UI Layer

```
templates/smart_money_dashboard.html
```

## Performance Considerations

- In-memory storage for demo (replace with database for production)
- Data retention: 30 days for prints/trades, 7 days for alerts
- Caching recommended for frequently accessed analytics
- Rate limiting on API endpoints

## Future Enhancements

1. **Real-time Data Integration**
   - Connect to real dark pool data feeds
   - Live SEC filing monitoring
   - Real-time options flow data

2. **Machine Learning**
   - Predictive models for smart money movements
   - Anomaly detection for unusual patterns
   - Sentiment analysis on institutional activity

3. **Extended Analytics**
   - Multi-timeframe analysis
   - Correlation with price movements
   - Historical backtesting capabilities

4. **Notifications**
   - Email/SMS alerts
   - Telegram integration
   - Webhook support

5. **Data Sources**
   - SEC EDGAR API integration
   - Options data providers
   - Enhanced dark pool feeds

## Support

For issues or questions:
- Review API documentation at `/docs`
- Check test examples in `tests/test_smart_money.py`
- Refer to code documentation in service files

## License

Part of Legend AI Trading Platform
