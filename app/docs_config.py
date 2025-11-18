"""
OpenAPI Documentation Configuration
Beautiful, comprehensive API documentation setup
"""

# Tags metadata for better organization
tags_metadata = [
    {
        "name": "patterns",
        "description": "🎯 **Pattern Detection & Analysis** - Detect and analyze chart patterns with AI-powered insights",
        "externalDocs": {
            "description": "Pattern Detection Guide",
            "url": "https://github.com/Stockmasterflex/legend-ai-python/blob/main/API_REFERENCE.md#patterns"
        }
    },
    {
        "name": "AI Assistant",
        "description": "🤖 **AI-Powered Trading Assistant** - Chat with AI, get stock analysis, and learn trading concepts",
    },
    {
        "name": "charts",
        "description": "📊 **Chart Generation** - Generate professional TradingView-style charts with indicators",
    },
    {
        "name": "universe",
        "description": "🌌 **Market Universe** - Scan and filter thousands of stocks across exchanges",
    },
    {
        "name": "watchlist",
        "description": "👁️ **Watchlist Management** - Track your favorite stocks and portfolios",
    },
    {
        "name": "analytics",
        "description": "📈 **Market Analytics** - Advanced market analysis and statistics",
    },
    {
        "name": "market",
        "description": "💹 **Market Data** - Real-time and historical market data",
    },
    {
        "name": "alerts",
        "description": "🔔 **Price Alerts** - Set up price alerts and notifications",
    },
    {
        "name": "risk",
        "description": "⚖️ **Risk Analysis** - Position sizing and risk management tools",
    },
    {
        "name": "trades",
        "description": "💼 **Trade Tracking** - Track and analyze your trades",
    },
    {
        "name": "telegram",
        "description": "📱 **Telegram Integration** - Telegram bot for mobile alerts and analysis",
    },
    {
        "name": "dashboard",
        "description": "🎛️ **Dashboard** - Main application dashboard",
    },
    {
        "name": "scan",
        "description": "🔍 **Market Scanner** - Scan markets for trading opportunities",
    },
    {
        "name": "advanced_analysis",
        "description": "🧪 **Advanced Analysis** - Multi-timeframe and advanced technical analysis",
    },
    {
        "name": "Google Sheets",
        "description": "📊 **Google Sheets Integration** - Bidirectional sync with Google Sheets for watchlist, patterns, trades, portfolio, and dashboards",
    },
]

# Custom OpenAPI schema
openapi_custom_info = {
    "title": "Legend AI - Trading Pattern Scanner API",
    "description": """
# 🚀 Legend AI Trading API

**Professional-grade trading pattern detection and market analysis platform**

## 🎯 Key Features

- **AI-Powered Pattern Detection**: Automatically detect chart patterns with confidence scores
- **Real-Time Market Data**: Multi-source data aggregation (TwelveData, Finnhub, Alpha Vantage)
- **Interactive Charts**: Professional TradingView-style charts with indicators
- **AI Trading Assistant**: Chat with AI for stock analysis and trading insights
- **Smart Caching**: Redis-backed caching for lightning-fast responses
- **Rate Limiting**: Built-in protection (60 requests/minute)

## 🔥 Popular Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/patterns/detect` | Detect chart patterns for any ticker |
| `POST /api/ai/chat` | Chat with AI trading assistant |
| `POST /api/ai/analyze` | Get comprehensive AI stock analysis |
| `POST /api/universe/scan` | Scan market universe for setups |
| `GET /api/charts/generate` | Generate chart images |

## 🛠️ Quick Start

### 1. Detect a Pattern

```bash
curl -X POST "https://your-api.com/api/patterns/detect" \\
  -H "Content-Type: application/json" \\
  -d '{"ticker": "AAPL", "interval": "1day"}'
```

### 2. Chat with AI

```bash
curl -X POST "https://your-api.com/api/ai/chat" \\
  -H "Content-Type: application/json" \\
  -d '{"message": "What are the best tech stocks right now?"}'
```

## 📚 Response Format

All endpoints return JSON with consistent structure:

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

Currently, the API is open for testing. Production deployments should implement API key authentication.

## ⚡ Rate Limits

- **60 requests per minute** per IP address
- Rate limit headers included in responses
- Upgrade available for higher limits

## 🐛 Error Handling

The API uses standard HTTP status codes:

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

## 💡 Support

- **Documentation**: [API Reference](https://github.com/Stockmasterflex/legend-ai-python)
- **Issues**: [GitHub Issues](https://github.com/Stockmasterflex/legend-ai-python/issues)

---

**⚠️ Disclaimer**: This is an educational tool. Not financial advice. Always do your own research.
    """,
    "version": "1.0.0",
    "contact": {
        "name": "Legend AI Support",
        "url": "https://github.com/Stockmasterflex/legend-ai-python",
        "email": "support@legend-ai.com"
    },
    "license_info": {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
}

# Example responses for common error scenarios
error_responses = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "error": "Invalid ticker symbol format",
                    "detail": "Ticker must be alphanumeric"
                }
            }
        }
    },
    404: {
        "description": "Not Found",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "error": "No price data available for INVALID",
                    "detail": "Symbol not found in any data source"
                }
            }
        }
    },
    429: {
        "description": "Too Many Requests",
        "content": {
            "application/json": {
                "example": {
                    "error": "Rate limit exceeded",
                    "detail": "Maximum 60 requests per minute. Try again in 30 seconds."
                }
            }
        }
    },
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "error": "Pattern analysis failed",
                    "detail": "Internal processing error"
                }
            }
        }
    },
    503: {
        "description": "Service Unavailable",
        "content": {
            "application/json": {
                "example": {
                    "error": "Service temporarily unavailable",
                    "detail": "External data provider is down. Please try again later."
                }
            }
        }
    }
}

# Code examples for different languages
code_examples = {
    "python": {
        "pattern_detect": """
# Python Example - Detect Pattern
import requests

response = requests.post(
    'https://your-api.com/api/patterns/detect',
    json={
        'ticker': 'AAPL',
        'interval': '1day'
    }
)

result = response.json()
if result['success']:
    pattern = result['data']
    print(f"Pattern: {pattern['pattern']}")
    print(f"Score: {pattern['score']}/10")
    print(f"Entry: ${pattern['entry']:.2f}")
    print(f"Target: ${pattern['target']:.2f}")
else:
    print(f"Error: {result['error']}")
        """,
        "ai_chat": """
# Python Example - AI Chat
import requests

response = requests.post(
    'https://your-api.com/api/ai/chat',
    json={
        'message': 'Analyze TSLA for me',
        'symbol': 'TSLA',
        'include_market_data': True
    }
)

result = response.json()
print(result['response'])
        """
    },
    "javascript": {
        "pattern_detect": """
// JavaScript Example - Detect Pattern
const response = await fetch('https://your-api.com/api/patterns/detect', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    ticker: 'AAPL',
    interval: '1day'
  })
});

const result = await response.json();
if (result.success) {
  const pattern = result.data;
  console.log(`Pattern: ${pattern.pattern}`);
  console.log(`Score: ${pattern.score}/10`);
  console.log(`Entry: $${pattern.entry.toFixed(2)}`);
} else {
  console.error(`Error: ${result.error}`);
}
        """,
        "ai_chat": """
// JavaScript Example - AI Chat
const response = await fetch('https://your-api.com/api/ai/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: 'Analyze TSLA for me',
    symbol: 'TSLA',
    include_market_data: true
  })
});

const result = await response.json();
console.log(result.response);
        """
    },
    "curl": {
        "pattern_detect": """
# cURL Example - Detect Pattern
curl -X POST "https://your-api.com/api/patterns/detect" \\
  -H "Content-Type: application/json" \\
  -d '{
    "ticker": "AAPL",
    "interval": "1day"
  }'
        """,
        "ai_chat": """
# cURL Example - AI Chat
curl -X POST "https://your-api.com/api/ai/chat" \\
  -H "Content-Type: application/json" \\
  -d '{
    "message": "Analyze TSLA for me",
    "symbol": "TSLA",
    "include_market_data": true
  }'
        """
    }
}
