# Legend AI Python SDK

Professional Python SDK for the Legend AI Trading Pattern Scanner API.

[![PyPI version](https://badge.fury.io/py/legend-ai.svg)](https://badge.fury.io/py/legend-ai)
[![Python Support](https://img.shields.io/pypi/pyversions/legend-ai.svg)](https://pypi.org/project/legend-ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🎯 **Pattern Detection**: Detect 15+ chart patterns with AI
- 📊 **Chart Generation**: Create professional TradingView-style charts
- 🌌 **Universe Scanning**: Scan S&P 500, NASDAQ for setups
- 🤖 **AI Assistant**: Chat with AI for stock analysis
- ⚖️ **Risk Management**: Position sizing and risk calculations
- 💼 **Trade Tracking**: Manage your trade journal
- ⚡ **Async Support**: Full async/await support
- 🔒 **Type Safe**: Complete type hints for IDE support

## 📦 Installation

```bash
pip install legend-ai
```

## 🚀 Quick Start

### Synchronous Client

```python
from legend_ai import LegendAI

# Initialize client
client = LegendAI()

# Detect pattern
pattern = client.patterns.detect("AAPL", interval="1day")
print(f"Pattern: {pattern.pattern}")
print(f"Score: {pattern.score}/10")
print(f"Entry: ${pattern.entry:.2f}")
print(f"Target: ${pattern.target:.2f}")
print(f"Risk/Reward: {pattern.risk_reward_ratio:.2f}R")

# Generate chart
chart = client.charts.generate(
    ticker="AAPL",
    entry=pattern.entry,
    stop=pattern.stop,
    target=pattern.target,
    indicators=["SMA50", "SMA200", "EMA21"]
)
print(f"Chart URL: {chart.chart_url}")

# Chat with AI
response = client.ai.chat(
    message="What are the best tech stocks right now?",
    include_market_data=True
)
print(response.response)
```

### Asynchronous Client

```python
import asyncio
from legend_ai import AsyncLegendAI

async def main():
    async with AsyncLegendAI() as client:
        # Detect pattern
        pattern = await client.patterns.detect("TSLA")
        print(f"Pattern: {pattern.pattern}, Score: {pattern.score}")

        # Scan universe
        results = await client.universe.scan(
            universe="SP500",
            min_score=8.0,
            max_results=10
        )

        for result in results:
            print(f"{result.ticker}: {result.pattern} ({result.score})")

asyncio.run(main())
```

## 📚 Usage Examples

### Pattern Detection

```python
# Basic pattern detection
pattern = client.patterns.detect("AAPL")

# With custom interval
pattern = client.patterns.detect("NVDA", interval="1week")

# With Yahoo fallback
pattern = client.patterns.detect("MSFT", use_yahoo_fallback=True)
```

### Universe Scanning

```python
# Scan S&P 500
results = client.universe.scan(
    universe="SP500",
    min_score=7.5,
    max_results=20
)

# Filter by pattern types
results = client.universe.scan(
    universe="NASDAQ100",
    pattern_types=["VCP", "Cup and Handle"],
    min_score=8.0
)

# Get universe tickers
tickers = client.universe.get_tickers("SP500")
print(f"S&P 500 has {len(tickers)} stocks")
```

### AI Assistant

```python
# Chat with context
response = client.ai.chat(
    message="Should I buy TSLA now?",
    symbol="TSLA",
    include_market_data=True
)
print(response.response)

# Get stock analysis
analysis = client.ai.analyze("AAPL")
print(analysis)
```

### Watchlist Management

```python
# Add to watchlist
client.watchlist.add(
    ticker="NVDA",
    reason="VCP setup forming",
    target_entry=450.0,
    target_stop=440.0
)

# Get watchlist
items = client.watchlist.list()
for item in items:
    print(f"{item.ticker}: {item.status} - {item.reason}")

# Remove from watchlist
client.watchlist.remove("NVDA")
```

### Risk Management

```python
# Calculate position size
position = client.risk.calculate_position(
    account_size=10000,
    entry_price=175.50,
    stop_loss_price=170.25,
    target_price=185.00,
    risk_percentage=2.0
)

print(f"Position Size: {position.position_size} shares")
print(f"Risk Amount: ${position.risk_amount:.2f}")
print(f"Kelly Criterion: {position.kelly_criterion:.2%}")
```

### Trade Management

```python
# Create trade entry
trade = client.trades.create(
    ticker="AAPL",
    entry_price=175.50,
    stop_loss=170.25,
    target_price=185.00,
    position_size=50,
    risk_amount=200.00
)
print(f"Trade ID: {trade['trade_id']}")
```

### Market Data

```python
# Get market internals
internals = client.market.internals()
print(f"Market Regime: {internals['regime']}")

# Get market breadth
breadth = client.market.breadth()
print(f"Advance/Decline: {breadth}")
```

## 🔧 Configuration

### Custom Base URL

```python
# Use custom API endpoint
client = LegendAI(base_url="http://localhost:8000")
```

### API Key (Future)

```python
# When API keys are enabled
client = LegendAI(api_key="your-api-key")
```

### Custom Timeout

```python
# Set custom timeout
client = LegendAI(timeout=60.0)
```

## 🛡️ Error Handling

```python
from legend_ai import (
    LegendAI,
    APIError,
    RateLimitError,
    ValidationError,
)

client = LegendAI()

try:
    pattern = client.patterns.detect("INVALID")
except ValidationError as e:
    print(f"Validation error: {e}")
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except APIError as e:
    print(f"API error: {e}")
```

## 📖 API Reference

### Client Methods

- `client.patterns.detect(ticker, interval, use_yahoo_fallback)` - Detect patterns
- `client.charts.generate(ticker, interval, entry, stop, target, indicators)` - Generate charts
- `client.universe.scan(universe, min_score, max_results, pattern_types)` - Scan universe
- `client.ai.chat(message, symbol, include_market_data, conversation_id)` - Chat with AI
- `client.ai.analyze(symbol)` - Get AI analysis
- `client.watchlist.list(user_id)` - Get watchlist
- `client.watchlist.add(ticker, reason, target_entry, target_stop)` - Add to watchlist
- `client.risk.calculate_position(...)` - Calculate position size
- `client.trades.create(...)` - Create trade entry
- `client.market.internals()` - Get market internals

### Models

All responses are returned as typed dataclass objects:

- `PatternResult` - Pattern detection result
- `ChartResult` - Chart generation result
- `ScanResult` - Universe scan result
- `WatchlistItem` - Watchlist item
- `PositionSize` - Position sizing calculation
- `Trade` - Trade record
- `AIResponse` - AI chat/analysis response

## 🔗 Links

- [Documentation](https://github.com/Stockmasterflex/legend-ai-python/blob/main/docs/)
- [API Reference](https://github.com/Stockmasterflex/legend-ai-python/blob/main/API_ENDPOINTS.md)
- [Examples](https://github.com/Stockmasterflex/legend-ai-python/tree/main/docs/examples)
- [GitHub](https://github.com/Stockmasterflex/legend-ai-python)

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## ⚠️ Disclaimer

This is an educational tool. Not financial advice. Always do your own research before making investment decisions.
