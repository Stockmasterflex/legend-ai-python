# Ticker Correlation Analysis

A comprehensive correlation analysis system for trading analysis with four main features:

## Features

### 1. Correlation Heatmap
Generate real-time correlation matrices with interactive visualization data.

**Endpoint:** `POST /api/correlation/heatmap`

**Example Request:**
```json
{
  "tickers": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"],
  "period": "3month",
  "interval": "1day",
  "method": "pearson"
}
```

**Features:**
- Real-time correlations between all ticker pairs
- Sector groupings and analysis
- Interactive hover data with color-coded strength
- Multiple correlation methods (Pearson, Spearman, Kendall)

---

### 2. Pair Trading Opportunities
Identify correlated pairs suitable for mean reversion trading.

**Endpoint:** `POST /api/correlation/pair-trading`

**Example Request:**
```json
{
  "tickers": ["XLE", "XLF", "XLK", "XLV", "XLI", "XLP", "XLY"],
  "period": "3month",
  "min_correlation": 0.7,
  "max_correlation": 0.95,
  "top_n": 10
}
```

**Features:**
- Find highly correlated stock pairs
- Divergence detection from mean spread
- Mean reversion trading signals
- Historical spread patterns
- Lead-lag relationship analysis

**Trading Signals:**
- `long_spread`: Spread too low → Buy ticker1, Short ticker2
- `short_spread`: Spread too high → Short ticker1, Buy ticker2
- `null`: No signal (spread within normal range)

---

### 3. Portfolio Diversification Analysis
Analyze correlation structure and identify redundant holdings.

**Endpoint:** `POST /api/correlation/portfolio-diversification`

**Example Request:**
```json
{
  "portfolio": {
    "AAPL": 0.20,
    "MSFT": 0.15,
    "GOOGL": 0.15,
    "AMZN": 0.10,
    "TSLA": 0.10,
    "JPM": 0.15,
    "XOM": 0.15
  },
  "period": "3month"
}
```

**Features:**
- Correlation with current holdings
- Reduce portfolio redundancy
- Optimal allocation suggestions
- Risk clustering analysis
- Diversification score (0-1, higher = better)

---

### 4. Market Leadership Analysis
Identify which tickers lead or lag the market.

**Endpoint:** `POST /api/correlation/market-leadership`

**Example Request:**
```json
{
  "tickers": ["AAPL", "MSFT", "TSLA", "JPM", "XOM"],
  "benchmark": "SPY",
  "period": "3month"
}
```

**Features:**
- Beta analysis (market sensitivity)
- Lead-lag detection
- Sector rotation identification
- Correlation strength with benchmark

**Leadership Types:**
- `leader`: Moves before the benchmark
- `laggard`: Follows benchmark movements
- `simultaneous`: Moves with the benchmark

**Beta Interpretation:**
- Beta > 1.0: More volatile than market
- Beta ≈ 1.0: Similar volatility
- Beta < 1.0: Less volatile
- Beta < 0: Inverse relationship

---

## Quick Correlation Check

For a simple correlation between two tickers:

**Endpoint:** `GET /api/correlation/quick-correlation`

**Example:**
```
GET /api/correlation/quick-correlation?ticker1=AAPL&ticker2=MSFT&period=3month
```

---

## Response Format

All endpoints return JSON with this structure:

```json
{
  "success": true,
  "data": {
    // Endpoint-specific data
  }
}
```

---

## Implementation Details

### Core Modules

1. **`app/core/correlation_stats.py`** - Statistical calculations
   - Correlation matrix computation (Pearson, Spearman, Kendall)
   - Rolling correlations
   - Pair analysis and spread calculations
   - Beta and lead-lag analysis
   - Portfolio metrics

2. **`app/services/correlation_analysis.py`** - Business logic
   - Market data integration
   - Caching layer (Redis)
   - High-level analysis functions
   - Result formatting

3. **`app/api/correlation.py`** - API endpoints
   - Request validation
   - Error handling
   - Comprehensive documentation

---

## Caching

All correlation analysis results are cached in Redis:

- **Heatmaps**: 1 hour TTL
- **Pair Trading**: 30 minutes TTL
- **Portfolio Analysis**: 1 hour TTL
- **Market Leadership**: 1 hour TTL

---

## Performance

- Optimized for multiple tickers
- Asynchronous data fetching
- Intelligent caching
- Parallel processing where possible

---

## Use Cases

### 1. Pair Trading Strategy
```python
import requests

# Find correlated pairs
response = requests.post('http://localhost:8000/api/correlation/pair-trading', json={
    'tickers': ['XLF', 'JPM', 'BAC', 'WFC', 'C'],
    'period': '3month',
    'min_correlation': 0.75,
    'top_n': 5
})

pairs = response.json()['data']['pairs']

# Look for trading signals
for pair in pairs:
    if pair['signal'] == 'long_spread':
        print(f"Long {pair['ticker1']}, Short {pair['ticker2']}")
        print(f"Z-score: {pair['z_score']:.2f}")
```

### 2. Portfolio Diversification Check
```python
# Analyze portfolio correlation
portfolio = {
    'AAPL': 0.25,
    'MSFT': 0.20,
    'GOOGL': 0.15,
    'AMZN': 0.15,
    'TSLA': 0.15,
    'NVDA': 0.10
}

response = requests.post('http://localhost:8000/api/correlation/portfolio-diversification',
    json={'portfolio': portfolio, 'period': '6month'})

result = response.json()['data']
print(f"Diversification Score: {result['portfolio_metrics']['diversification_score']:.2f}")
print(f"Average Correlation: {result['portfolio_metrics']['average_correlation']:.2f}")

# Check for redundant holdings
for pair in result['redundant_holdings']:
    print(f"Consider reducing: {pair['suggested_reduce']} (corr: {pair['correlation']:.2f})")
```

### 3. Market Leadership Monitoring
```python
# Identify market leaders
tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA', 'TSLA']

response = requests.post('http://localhost:8000/api/correlation/market-leadership', json={
    'tickers': tech_stocks,
    'benchmark': 'QQQ',
    'period': '3month'
})

result = response.json()['data']

print("Market Leaders:")
for stock in result['leaders']:
    print(f"  {stock['ticker']}: Beta={stock['beta']:.2f}, Leads by {stock['lead_lag_periods']} periods")

print("\nMarket Laggards:")
for stock in result['laggards']:
    print(f"  {stock['ticker']}: Beta={stock['beta']:.2f}")
```

---

## API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Look for the **Correlation** section with 🔗 icon.

---

## Dependencies

All required packages are already in `requirements.txt`:
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `scipy` - Statistical functions
- `redis` - Caching

---

## Notes

- Correlation does not imply causation
- Past correlations may not predict future relationships
- Use correlation analysis as one tool among many
- Always validate signals with fundamental analysis
- Consider transaction costs in pair trading strategies

---

## Support

For issues or questions:
- Check the API documentation at `/docs`
- Review example code in this document
- File an issue on GitHub
