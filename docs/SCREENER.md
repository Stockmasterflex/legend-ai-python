# Advanced Stock Screener

A comprehensive stock screening system with proven trading strategies and custom filters.

## Features

### 1. Filter Criteria

Screen stocks using multiple criteria:

#### Price Filters
- **Min/Max Price**: Filter stocks by price range
- **Price Change**: Filter by percentage price change over period

#### Volume Filters
- **Min Volume**: Minimum daily volume
- **Min Average Volume**: Minimum average volume over period

#### Relative Strength
- **RS Rating**: Relative strength vs SPY (0-100 scale)
- Higher RS indicates outperformance vs market

#### Pattern Detection
- **Supported Patterns**: VCP, Cup & Handle, Ascending Triangle, and more
- **Min Confidence**: Minimum pattern confidence threshold (0-1)

#### Technical Indicators
- **Above SMA 50/200**: Price above moving averages
- **Above EMA 21**: Price above 21-day exponential moving average
- **SMA 50 > SMA 200**: Golden cross condition
- **% Above SMA 50**: Price position relative to 50-day MA

#### Momentum Filters
- **Price Change %**: Percentage change over specified period
- **Price Change Period**: Number of days for momentum calculation

#### Volatility
- **ATR (Average True Range)**: Filter by volatility range

#### Fundamental
- **Sectors**: Include specific sectors
- **Exclude Sectors**: Exclude specific sectors

#### Advanced Criteria
- **Minervini Trend Template**: Mark Minervini's trend template
- **Gap Up Today**: Stocks gapping up with minimum gap percentage
- **In Consolidation**: Stocks in consolidation pattern

---

## 2. Pre-built Screen Templates

### Minervini SEPA
**Mark Minervini's Specific Entry Point Analysis**

Criteria:
- Price > $5
- RS Rating > 70
- Price within 0-15% of SMA50
- Above EMA21 and SMA50
- SMA50 > SMA200 (uptrend)
- Passes Minervini Trend Template
- VCP pattern
- Average volume > 500K

**Use Case**: Finding high-quality growth stocks at ideal entry points

---

### O'Neil CAN SLIM
**William O'Neil's Growth Stock Methodology**

Criteria:
- Price > $10
- RS Rating > 80 (Leaders only)
- Average volume > 1M
- Above SMA50 and SMA200
- SMA50 > SMA200
- Price -5% to +20% from SMA50
- Patterns: Cup & Handle, VCP, Ascending Triangle

**Use Case**: Identifying institutional-quality growth leaders

---

### Momentum Leaders
**High Momentum Stocks with Strong Relative Strength**

Criteria:
- Price > $10
- RS Rating > 85
- 15%+ gain in last 20 days
- Above all major moving averages
- Average volume > 1M

**Use Case**: Finding stocks with strong ongoing momentum

---

### Breakout Candidates
**Stocks Setting Up for Potential Breakouts**

Criteria:
- Price > $5
- RS Rating > 75
- Minervini Trend Template
- Price 0-10% above SMA50
- In consolidation (max 60 days)
- Patterns: VCP, Cup & Handle, Ascending Triangle

**Use Case**: Finding stocks building bases before breakouts

---

### Gap-Up Today
**Stocks Gapping Up with Volume**

Criteria:
- Price > $5
- Gap up > 2%
- Volume > 500K
- Above SMA50
- RS Rating > 60

**Use Case**: Finding stocks with significant buying pressure

---

### High Tight Flag
**O'Neil's Strongest Pattern**

Criteria:
- Price > $10
- 50%+ gain in ~8 weeks
- RS Rating > 90
- In tight consolidation (3-5 weeks)
- Above all moving averages

**Use Case**: Finding explosive growth stocks

---

### Pullback to Support
**Quality Pullbacks to SMA50**

Criteria:
- Price > $5
- Price -5% to +2% from SMA50
- SMA50 > SMA200
- RS Rating > 70
- Average volume > 500K

**Use Case**: Finding bounce opportunities at support

---

### Pocket Pivot
**Volume Spikes on Up Days**

Criteria:
- Price > $5
- RS Rating > 75
- Above SMA50 and EMA21
- Volume > 1M
- Positive day

**Use Case**: Identifying accumulation days

---

### Strong Foundation
**Stocks with Aligned Moving Averages**

Criteria:
- Price > $5
- All MAs aligned (EMA21 > SMA50 > SMA200)
- RS Rating > 70
- Average volume > 500K

**Use Case**: Finding technically strong stocks

---

### Post-IPO Base
**Recent IPOs Building First Base**

Criteria:
- Price > $15
- RS Rating > 80
- Above SMA50
- Price 0-15% above SMA50
- Patterns: VCP, Cup & Handle
- Average volume > 1M

**Use Case**: Finding IPOs with institutional backing

---

## 3. Save & Schedule

### Save Custom Screens
```bash
POST /api/screener/saved
{
  "name": "My Custom Screen",
  "description": "High momentum tech stocks",
  "filter_criteria": { ... },
  "user_id": "default"
}
```

### Schedule Screens
```bash
POST /api/screener/saved/{screen_id}/schedule
{
  "frequency": "daily",
  "time": "09:30",
  "email_results": true,
  "alert_on_match": true
}
```

**Frequency Options**:
- `daily`: Run every day at specified time
- `weekly`: Run every Monday at specified time
- `hourly`: Run every hour at specified time

**Notifications**:
- **Email Results**: Receive full screen results via email
- **Alert on Match**: Get instant alerts when matches are found

---

## 4. Results Display

### API Response Format
```json
{
  "as_of": "2025-11-18T10:30:00Z",
  "universe_size": 600,
  "results": [
    {
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "sector": "Technology",
      "industry": "Consumer Electronics",
      "price": 195.50,
      "volume": 52000000,
      "avg_volume": 48000000,
      "rs_rating": 85.3,
      "score": 87.5,
      "patterns": [
        {
          "type": "VCP",
          "confidence": 0.85,
          "entry_price": 196.00,
          "stop_price": 189.50,
          "target_price": 210.00
        }
      ],
      "match_data": {
        "price": 195.50,
        "volume": 52000000,
        "rs_rating": 85.3,
        "sma_50": 185.20,
        "sma_200": 175.80,
        "ema_21": 192.10
      }
    }
  ],
  "meta": {
    "build_sha": "abc123",
    "duration_ms": 15234,
    "result_count": 25,
    "total_scanned": 600
  }
}
```

### Export to CSV
```bash
GET /api/screener/saved/{screen_id}/export/csv
```

Downloads results as CSV file with columns:
- Symbol, Name, Sector, Industry
- Price, Volume, Avg Volume
- RS Rating, Score

---

## API Endpoints

### Run Custom Screen
```bash
POST /api/screener/run
{
  "filter_criteria": {
    "min_price": 10.0,
    "min_rs_rating": 70.0,
    "above_sma_50": true,
    "minervini_template": true
  },
  "limit": 50
}
```

### Run Template Screen
```bash
POST /api/screener/templates/MINERVINI_SEPA/run?limit=50
```

### List Templates
```bash
GET /api/screener/templates
```

### Create Saved Screen
```bash
POST /api/screener/saved
{
  "name": "My Screen",
  "filter_criteria": { ... }
}
```

### List Saved Screens
```bash
GET /api/screener/saved?user_id=default
```

### Run Saved Screen
```bash
POST /api/screener/saved/{screen_id}/run?limit=50
```

### Schedule Screen
```bash
POST /api/screener/saved/{screen_id}/schedule
{
  "frequency": "daily",
  "time": "09:30",
  "email_results": true
}
```

### Get Screen Results History
```bash
GET /api/screener/saved/{screen_id}/results?limit=100
```

### Export Results to CSV
```bash
GET /api/screener/saved/{screen_id}/export/csv
```

---

## Usage Examples

### Example 1: Find High RS Momentum Stocks
```python
import requests

response = requests.post(
    "http://localhost:8000/api/screener/run",
    json={
        "filter_criteria": {
            "min_price": 10.0,
            "min_rs_rating": 85.0,
            "above_sma_50": True,
            "above_sma_200": True,
            "min_avg_volume": 1000000
        },
        "limit": 50
    }
)

results = response.json()
for stock in results["results"]:
    print(f"{stock['symbol']}: RS {stock['rs_rating']}, Score {stock['score']}")
```

### Example 2: Run Minervini SEPA Template
```python
response = requests.post(
    "http://localhost:8000/api/screener/templates/MINERVINI_SEPA/run",
    params={"limit": 30}
)

results = response.json()
```

### Example 3: Save and Schedule a Screen
```python
# Create saved screen
create_response = requests.post(
    "http://localhost:8000/api/screener/saved",
    json={
        "name": "Daily Tech Leaders",
        "description": "High RS tech stocks",
        "filter_criteria": {
            "min_rs_rating": 80.0,
            "sectors": ["Technology"],
            "above_sma_50": True
        }
    }
)

screen_id = create_response.json()["id"]

# Schedule it
schedule_response = requests.post(
    f"http://localhost:8000/api/screener/saved/{screen_id}/schedule",
    json={
        "frequency": "daily",
        "time": "09:30",
        "email_results": True,
        "alert_on_match": True
    }
)
```

---

## Database Schema

### saved_screens
```sql
CREATE TABLE saved_screens (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    filter_criteria TEXT NOT NULL,
    is_template BOOLEAN DEFAULT FALSE,
    template_type VARCHAR(50),
    is_scheduled BOOLEAN DEFAULT FALSE,
    schedule_frequency VARCHAR(20),
    schedule_time VARCHAR(10),
    email_results BOOLEAN DEFAULT FALSE,
    alert_on_match BOOLEAN DEFAULT FALSE,
    last_run_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

### screen_results
```sql
CREATE TABLE screen_results (
    id SERIAL PRIMARY KEY,
    screen_id INTEGER REFERENCES saved_screens(id),
    ticker_id INTEGER REFERENCES tickers(id),
    score FLOAT NOT NULL,
    match_data TEXT,
    price FLOAT,
    volume FLOAT,
    rs_rating FLOAT,
    executed_at TIMESTAMP DEFAULT NOW()
);
```

### scheduled_scans
```sql
CREATE TABLE scheduled_scans (
    id SERIAL PRIMARY KEY,
    screen_id INTEGER REFERENCES saved_screens(id),
    scheduled_time TIMESTAMP,
    executed_at TIMESTAMP,
    status VARCHAR(20),
    results_count INTEGER DEFAULT 0,
    error_message TEXT,
    email_sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Setup Instructions

### 1. Run Database Migration
```bash
cd /home/user/legend-ai-python
python migrations/add_screener_tables.py
```

### 2. Initialize Template Screens
```bash
curl -X POST http://localhost:8000/api/screener/initialize-templates
```

### 3. Configure Email (Optional)
Set environment variables for email notifications:
```bash
export SENDGRID_API_KEY="your_sendgrid_api_key"
export ALERT_EMAIL="your@email.com"
```

### 4. Configure Telegram (Optional)
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
```

---

## Gradio UI

Launch the web interface:
```bash
python app/ui/screener_interface.py
```

Features:
- **Pre-built Templates Tab**: Select and run proven strategies
- **Custom Screen Tab**: Build custom screens with interactive filters
- **Documentation Tab**: In-app documentation

---

## Performance

- **Universe Size**: Scans up to 600 stocks (S&P 500 + NASDAQ 100)
- **Concurrency**: 8 concurrent scans for fast execution
- **Caching**: Redis caching for market data
- **Typical Scan Time**: 15-30 seconds for full universe

---

## Tips & Best Practices

1. **Start with Templates**: Learn from proven strategies before building custom screens
2. **Use High RS Threshold**: RS > 80 for leaders, RS > 70 for quality stocks
3. **Combine Filters**: Multiple criteria improve result quality
4. **Monitor Volume**: Ensure adequate liquidity (500K+ avg volume)
5. **Schedule Wisely**: Run screens after market open (09:45+) for accurate data
6. **Review Historical Results**: Analyze past matches to refine criteria
7. **Export and Analyze**: Download CSV for deeper analysis in Excel/Python

---

## Troubleshooting

### No Results Found
- Try relaxing some filters
- Check if criteria are too restrictive
- Verify market conditions support your strategy

### Slow Performance
- Reduce universe size by filtering sectors
- Lower limit parameter
- Check Redis cache is working

### Email Not Sending
- Verify SendGrid API key is set
- Check alert_email is configured
- Review logs for errors

---

## Future Enhancements

- [ ] Fundamental data integration (P/E, EPS growth)
- [ ] Backtest screen performance
- [ ] Portfolio integration
- [ ] Mobile app
- [ ] Real-time alerts
- [ ] Social sharing of screens
- [ ] Screen performance analytics

---

## Support

For issues or questions:
- API Documentation: `/docs`
- GitHub Issues: [Create an issue](https://github.com/your-repo/issues)
- Email: support@legendai.com

---

**Built with Legend AI | Powered by proven trading strategies**
