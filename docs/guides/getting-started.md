# Getting Started with Legend AI API

Welcome to the Legend AI Trading Pattern Scanner API! This guide will help you get started quickly.

## 🚀 Quick Start

### 1. Choose Your Interface

Legend AI provides multiple ways to interact with the API:

- **Python SDK**: `pip install legend-ai`
- **JavaScript SDK**: `npm install @legend-ai/sdk`
- **CLI Tool**: `pip install legend-cli`
- **Direct HTTP**: Use curl, Postman, or any HTTP client
- **Interactive Docs**: Visit `/docs` on the API

### 2. Make Your First Request

#### Using Python SDK

```python
from legend_ai import LegendAI

# Initialize client
client = LegendAI()

# Detect a pattern
pattern = client.patterns.detect("AAPL")
print(f"Pattern: {pattern.pattern}")
print(f"Score: {pattern.score}/10")
print(f"Entry: ${pattern.entry:.2f}")
```

#### Using JavaScript SDK

```javascript
import { LegendAI } from '@legend-ai/sdk';

const client = new LegendAI();

const pattern = await client.patterns.detect('AAPL');
console.log(`Pattern: ${pattern.pattern}, Score: ${pattern.score}`);
```

#### Using curl

```bash
curl -X POST "https://legend-ai-python-production.up.railway.app/api/patterns/detect" \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL", "interval": "1day"}'
```

#### Using CLI

```bash
legend-cli detect AAPL
```

## 📚 Core Concepts

### Patterns

Legend AI detects 15+ chart patterns including:
- **VCP (Volatility Contraction Pattern)**
- **Cup and Handle**
- **Ascending/Descending Triangles**
- **Head and Shoulders**
- **Double Top/Bottom**
- And more...

Each pattern comes with:
- **Score** (0-10): Confidence score
- **Entry**: Suggested entry price
- **Stop**: Stop loss price
- **Target**: Target price
- **Risk/Reward Ratio**: Expected R multiple

### Timeframes

Supported intervals:
- `1day` - Daily charts (default)
- `1week` - Weekly charts
- `1hour` - Hourly charts
- `4hour` - 4-hour charts

### Universe Scanning

Scan entire market universes:
- **SP500**: All S&P 500 stocks
- **NASDAQ100**: All NASDAQ 100 stocks
- **CUSTOM**: Your custom universe

## 🎯 Common Use Cases

### 1. Find Trading Setups

```python
# Scan S&P 500 for high-quality setups
results = client.universe.scan(
    universe="SP500",
    min_score=8.0,
    max_results=10
)

for result in results:
    print(f"{result.ticker}: {result.pattern} ({result.score})")
```

### 2. Analyze a Specific Stock

```python
# Get pattern analysis
pattern = client.patterns.detect("TSLA", interval="1day")

# Generate chart
chart = client.charts.generate(
    "TSLA",
    entry=pattern.entry,
    stop=pattern.stop,
    target=pattern.target
)

# Get AI analysis
analysis = client.ai.analyze("TSLA")
```

### 3. Calculate Position Size

```python
# Calculate how many shares to buy
position = client.risk.calculate_position(
    account_size=10000,
    entry_price=175.50,
    stop_loss_price=170.25,
    risk_percentage=2.0  # 2% risk rule
)

print(f"Buy {position.position_size} shares")
print(f"Risk: ${position.risk_amount:.2f}")
```

### 4. Track Your Watchlist

```python
# Add stocks to watchlist
client.watchlist.add(
    ticker="NVDA",
    reason="VCP forming",
    target_entry=450.0,
    target_stop=440.0
)

# Get watchlist
items = client.watchlist.list()
for item in items:
    print(f"{item.ticker}: {item.status}")
```

## 🔐 Authentication

Currently, the API is **open for testing** and doesn't require authentication.

For production deployments, API key authentication will be required:

```python
# Future: API key authentication
client = LegendAI(api_key="your-api-key")
```

## ⚡ Rate Limits

Current limits:
- **60 requests per minute** per IP address
- Rate limit headers included in responses

Exceeding limits returns HTTP 429 with retry information.

## 📊 Response Format

All endpoints return consistent JSON:

```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "cached": false,
  "processing_time": 1.23
}
```

## 🐛 Error Handling

### Python SDK

```python
from legend_ai import LegendAI, APIError, RateLimitError

try:
    pattern = client.patterns.detect("INVALID")
except RateLimitError as e:
    print("Rate limit exceeded, wait before retrying")
except APIError as e:
    print(f"API error: {e}")
```

### JavaScript SDK

```javascript
try {
  const pattern = await client.patterns.detect('INVALID');
} catch (error) {
  if (error instanceof RateLimitError) {
    console.error('Rate limit exceeded');
  }
}
```

## 🔗 Next Steps

- [API Reference](../api/openapi-full.yaml)
- [Python SDK Guide](./python-sdk.md)
- [JavaScript SDK Guide](./javascript-sdk.md)
- [Authentication Guide](./authentication.md)
- [Best Practices](./best-practices.md)
- [Rate Limiting Guide](./rate-limiting.md)

## 💡 Examples

Check out the [examples directory](../examples/) for complete working examples:
- Pattern detection
- Universe scanning
- AI chat integration
- Risk management
- Trade tracking

## 🆘 Support

- **Documentation**: [GitHub](https://github.com/Stockmasterflex/legend-ai-python)
- **Issues**: [GitHub Issues](https://github.com/Stockmasterflex/legend-ai-python/issues)
- **API Reference**: [OpenAPI Spec](../api/openapi-full.yaml)

## ⚠️ Disclaimer

This is an educational tool. Not financial advice. Always do your own research before making investment decisions.
