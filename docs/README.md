# Legend AI API Documentation

Complete documentation for the Legend AI Trading Pattern Scanner API.

## 📚 Table of Contents

### Getting Started
- [Getting Started Guide](./guides/getting-started.md) - Quick start and basics
- [Best Practices](./guides/best-practices.md) - Recommended patterns and workflows
- [Rate Limiting Guide](./guides/rate-limiting.md) - Understanding rate limits

### API Reference
- [OpenAPI Specification](./api/openapi-full.yaml) - Complete OpenAPI 3.0 spec
- [Interactive Docs](https://legend-ai-python-production.up.railway.app/docs) - Swagger UI
- [Postman Collection](./postman_collection.json) - Import into Postman

### SDKs & Tools
- [Python SDK](../sdk/python/) - Official Python SDK
- [JavaScript/TypeScript SDK](../sdk/javascript/) - Official JS/TS SDK
- [CLI Tool](../cli/) - Command-line interface

### Integration Guides
- [Python Integration](./guides/python-sdk.md) - Using the Python SDK
- [JavaScript Integration](./guides/javascript-sdk.md) - Using the JS/TS SDK
- [REST API Integration](./guides/rest-api.md) - Direct HTTP integration
- [Authentication](./guides/authentication.md) - API authentication

### Features
- [Pattern Detection](./guides/pattern-detection.md) - 15+ chart patterns
- [Universe Scanning](./guides/universe-scanning.md) - Scan S&P 500 / NASDAQ
- [AI Assistant](./guides/ai-assistant.md) - AI-powered insights
- [Risk Management](./guides/risk-management.md) - Position sizing
- [Chart Generation](./guides/chart-generation.md) - Professional charts

### Tools
- [API Playground](../playground/index.html) - Interactive testing
- [Code Examples](./examples/) - Working code samples

## 🚀 Quick Start

### 1. Choose Your SDK

**Python:**
```bash
pip install legend-ai
```

**JavaScript:**
```bash
npm install @legend-ai/sdk
```

**CLI:**
```bash
pip install legend-cli
```

### 2. Basic Usage

**Python:**
```python
from legend_ai import LegendAI

client = LegendAI()
pattern = client.patterns.detect("AAPL")
print(f"{pattern.pattern}: {pattern.score}/10")
```

**JavaScript:**
```javascript
import { LegendAI } from '@legend-ai/sdk';

const client = new LegendAI();
const pattern = await client.patterns.detect('AAPL');
console.log(`${pattern.pattern}: ${pattern.score}/10`);
```

**CLI:**
```bash
legend-cli detect AAPL
legend-cli scan --min-score 8.0
legend-cli chat "What are the best tech stocks?"
```

**cURL:**
```bash
curl -X POST "https://legend-ai-python-production.up.railway.app/api/patterns/detect" \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL", "interval": "1day"}'
```

## 📖 Core Concepts

### Pattern Detection
Detect 15+ chart patterns with AI-powered confidence scores:
- VCP (Volatility Contraction Pattern)
- Cup and Handle
- Ascending/Descending Triangles
- Head and Shoulders
- Double Top/Bottom
- And more...

### Universe Scanning
Scan entire market universes:
- **SP500**: All S&P 500 stocks (500 tickers)
- **NASDAQ100**: All NASDAQ 100 stocks (100 tickers)
- **CUSTOM**: Your custom universe

### AI Assistant
Chat with AI for:
- Stock analysis
- Pattern explanations
- Market insights
- Trading education

### Risk Management
Professional risk tools:
- 2% risk rule
- Position sizing
- Kelly Criterion
- R-multiple calculations

## 🔗 Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/patterns/detect` | Detect patterns for a ticker |
| `POST /api/universe/scan` | Scan universe for setups |
| `POST /api/ai/chat` | Chat with AI assistant |
| `POST /api/charts/generate` | Generate professional charts |
| `POST /api/risk/calculate-position` | Calculate position size |
| `GET /api/watchlist` | Get watchlist items |
| `GET /health` | API health check |

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

## 🔐 Authentication

Currently **open for testing**. No API key required.

For production deployments:
```python
client = LegendAI(api_key="your-api-key")
```

## ⚡ Rate Limits

- **60 requests per minute** per IP address
- Rate limit headers included in responses
- HTTP 429 returned when exceeded

## 🛠️ Tools & Resources

### Interactive Tools
- [API Playground](../playground/index.html) - Test APIs in browser
- [Swagger UI](/docs) - Interactive API documentation
- [ReDoc](/redoc) - Alternative API documentation

### Development Tools
- [Postman Collection](./postman_collection.json) - Import into Postman
- [OpenAPI Spec](./api/openapi-full.yaml) - Use with OpenAPI tools

### Code Generators
The OpenAPI spec can generate SDKs for:
- Java
- Go
- Ruby
- PHP
- And 50+ more languages

Use [OpenAPI Generator](https://openapi-generator.tech/):
```bash
openapi-generator-cli generate -i docs/api/openapi-full.yaml -g java -o ./java-sdk
```

## 📦 Package Publishing

### Python SDK (PyPI)

```bash
cd sdk/python
python -m build
twine upload dist/*
```

Or use GitHub Actions workflow: `.github/workflows/publish-python.yml`

### JavaScript SDK (npm)

```bash
cd sdk/javascript
npm run build
npm publish --access public
```

Or use GitHub Actions workflow: `.github/workflows/publish-javascript.yml`

## 🎓 Examples

### Pattern Detection
```python
# Basic detection
pattern = client.patterns.detect("AAPL")

# Custom interval
pattern = client.patterns.detect("NVDA", interval="1week")

# With fallback
pattern = client.patterns.detect("MSFT", use_yahoo_fallback=True)
```

### Universe Scanning
```python
# Scan S&P 500
results = client.universe.scan(
    universe="SP500",
    min_score=8.0,
    max_results=10
)

for result in results:
    print(f"{result.ticker}: {result.pattern} ({result.score})")
```

### Risk Management
```python
# Calculate position size
position = client.risk.calculate_position(
    account_size=10000,
    entry_price=175.50,
    stop_loss_price=170.25,
    risk_percentage=2.0
)

print(f"Buy {position.position_size} shares")
print(f"Risk: ${position.risk_amount:.2f}")
```

### AI Chat
```python
# Chat with context
response = client.ai.chat(
    "Should I buy TSLA now?",
    symbol="TSLA",
    include_market_data=True
)
print(response.response)
```

## 🐛 Error Handling

### Python
```python
from legend_ai import APIError, RateLimitError

try:
    pattern = client.patterns.detect("AAPL")
except RateLimitError:
    print("Rate limit exceeded, wait 60 seconds")
except APIError as e:
    print(f"API error: {e}")
```

### JavaScript
```javascript
import { APIError, RateLimitError } from '@legend-ai/sdk';

try {
  const pattern = await client.patterns.detect('AAPL');
} catch (error) {
  if (error instanceof RateLimitError) {
    console.error('Rate limit exceeded');
  }
}
```

## 📈 Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

## 🔗 Links

- **Production API**: https://legend-ai-python-production.up.railway.app
- **Interactive Docs**: https://legend-ai-python-production.up.railway.app/docs
- **GitHub**: https://github.com/Stockmasterflex/legend-ai-python
- **Playground**: [playground/index.html](../playground/index.html)

## 📄 License

MIT License - see [LICENSE](../LICENSE) for details.

## ⚠️ Disclaimer

This is an educational tool. **Not financial advice.** Always do your own research before making investment decisions.

## 🆘 Support

- **Documentation**: This directory
- **Issues**: [GitHub Issues](https://github.com/Stockmasterflex/legend-ai-python/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Stockmasterflex/legend-ai-python/discussions)

## 🎉 Contributing

We welcome contributions! See our contributing guidelines for:
- Bug reports
- Feature requests
- Documentation improvements
- Code contributions

---

**Built with ❤️ by the Legend AI team**
