# Legend AI JavaScript/TypeScript SDK

Professional JavaScript/TypeScript SDK for the Legend AI Trading Pattern Scanner API.

[![npm version](https://badge.fury.io/js/%40legend-ai%2Fsdk.svg)](https://www.npmjs.com/package/@legend-ai/sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🎯 **Pattern Detection**: Detect 15+ chart patterns with AI
- 📊 **Chart Generation**: Create professional TradingView-style charts
- 🌌 **Universe Scanning**: Scan S&P 500, NASDAQ for setups
- 🤖 **AI Assistant**: Chat with AI for stock analysis
- ⚖️ **Risk Management**: Position sizing and risk calculations
- 💼 **Trade Tracking**: Manage your trade journal
- 🔒 **Type Safe**: Full TypeScript support with type definitions
- 📦 **Tree Shakeable**: ESM and CommonJS support

## 📦 Installation

```bash
npm install @legend-ai/sdk
# or
yarn add @legend-ai/sdk
# or
pnpm add @legend-ai/sdk
```

## 🚀 Quick Start

### TypeScript

```typescript
import { LegendAI } from '@legend-ai/sdk';

// Initialize client
const client = new LegendAI();

// Detect pattern
const pattern = await client.patterns.detect('AAPL', {
  interval: '1day'
});
console.log(`Pattern: ${pattern.pattern}`);
console.log(`Score: ${pattern.score}/10`);
console.log(`Entry: $${pattern.entry.toFixed(2)}`);
console.log(`R:R: ${pattern.risk_reward_ratio.toFixed(2)}R`);

// Generate chart
const chart = await client.charts.generate('AAPL', {
  entry: pattern.entry,
  stop: pattern.stop,
  target: pattern.target,
  indicators: ['SMA50', 'SMA200', 'EMA21']
});
console.log(`Chart: ${chart.chart_url}`);

// Chat with AI
const response = await client.ai.chat('What are the best tech stocks right now?', {
  include_market_data: true
});
console.log(response.response);
```

### JavaScript

```javascript
const { LegendAI } = require('@legend-ai/sdk');

const client = new LegendAI();

async function main() {
  // Detect pattern
  const pattern = await client.patterns.detect('TSLA');
  console.log(`Pattern: ${pattern.pattern}, Score: ${pattern.score}`);

  // Scan universe
  const results = await client.universe.scan({
    universe: 'SP500',
    min_score: 8.0,
    max_results: 10
  });

  results.forEach(result => {
    console.log(`${result.ticker}: ${result.pattern} (${result.score})`);
  });
}

main();
```

## 📚 Usage Examples

### Pattern Detection

```typescript
// Basic pattern detection
const pattern = await client.patterns.detect('AAPL');

// With custom interval
const pattern = await client.patterns.detect('NVDA', {
  interval: '1week'
});

// With Yahoo fallback
const pattern = await client.patterns.detect('MSFT', {
  use_yahoo_fallback: true
});
```

### Universe Scanning

```typescript
// Scan S&P 500
const results = await client.universe.scan({
  universe: 'SP500',
  min_score: 7.5,
  max_results: 20
});

// Filter by pattern types
const vcpSetups = await client.universe.scan({
  universe: 'NASDAQ100',
  pattern_types: ['VCP', 'Cup and Handle'],
  min_score: 8.0
});

// Get universe tickers
const tickers = await client.universe.getTickers('SP500');
console.log(`S&P 500 has ${tickers.length} stocks`);
```

### AI Assistant

```typescript
// Chat with context
const response = await client.ai.chat('Should I buy TSLA now?', {
  symbol: 'TSLA',
  include_market_data: true
});
console.log(response.response);

// Get stock analysis
const analysis = await client.ai.analyze('AAPL');
console.log(analysis);

// Multi-turn conversation
const conv1 = await client.ai.chat('Analyze NVDA for me');
const conv2 = await client.ai.chat('What about AMD?', {
  conversation_id: conv1.conversation_id
});
```

### Watchlist Management

```typescript
// Add to watchlist
await client.watchlist.add('NVDA', {
  reason: 'VCP setup forming',
  target_entry: 450.0,
  target_stop: 440.0
});

// Get watchlist
const items = await client.watchlist.list();
items.forEach(item => {
  console.log(`${item.ticker}: ${item.status} - ${item.reason}`);
});

// Remove from watchlist
await client.watchlist.remove('NVDA');
```

### Risk Management

```typescript
// Calculate position size
const position = await client.risk.calculatePosition({
  account_size: 10000,
  entry_price: 175.50,
  stop_loss_price: 170.25,
  target_price: 185.00,
  risk_percentage: 2.0
});

console.log(`Position Size: ${position.position_size} shares`);
console.log(`Risk Amount: $${position.risk_amount.toFixed(2)}`);
console.log(`Kelly Criterion: ${(position.kelly_criterion * 100).toFixed(2)}%`);
```

### Trade Management

```typescript
// Create trade entry
const trade = await client.trades.create({
  ticker: 'AAPL',
  entry_price: 175.50,
  stop_loss: 170.25,
  target_price: 185.00,
  position_size: 50,
  risk_amount: 200.00
});
console.log(`Trade ID: ${trade.trade_id}`);
```

### Market Data

```typescript
// Get market internals
const internals = await client.market.internals();
console.log(`Market Regime: ${internals.regime}`);

// Get market breadth
const breadth = await client.market.breadth();
console.log(breadth);
```

## 🔧 Configuration

### Custom Base URL

```typescript
const client = new LegendAI({
  baseURL: 'http://localhost:8000'
});
```

### API Key (Future)

```typescript
const client = new LegendAI({
  apiKey: 'your-api-key'
});
```

### Custom Timeout

```typescript
const client = new LegendAI({
  timeout: 60000 // 60 seconds
});
```

## 🛡️ Error Handling

```typescript
import { LegendAI, APIError, RateLimitError, ValidationError } from '@legend-ai/sdk';

const client = new LegendAI();

try {
  const pattern = await client.patterns.detect('INVALID');
} catch (error) {
  if (error instanceof ValidationError) {
    console.error('Validation error:', error.message);
  } else if (error instanceof RateLimitError) {
    console.error('Rate limit exceeded:', error.message);
  } else if (error instanceof APIError) {
    console.error('API error:', error.message);
  }
}
```

## 📖 API Reference

### Client Methods

- `client.patterns.detect(ticker, options)` - Detect patterns
- `client.charts.generate(ticker, options)` - Generate charts
- `client.universe.scan(options)` - Scan universe
- `client.ai.chat(message, options)` - Chat with AI
- `client.ai.analyze(symbol)` - Get AI analysis
- `client.watchlist.list(userId)` - Get watchlist
- `client.watchlist.add(ticker, options)` - Add to watchlist
- `client.risk.calculatePosition(request)` - Calculate position size
- `client.trades.create(request)` - Create trade entry
- `client.market.internals()` - Get market internals

### TypeScript Types

All request/response types are fully typed:

```typescript
import type {
  PatternResult,
  ChartResult,
  ScanResult,
  WatchlistItem,
  PositionSize,
  AIResponse,
} from '@legend-ai/sdk';
```

## 🔗 Links

- [Documentation](https://github.com/Stockmasterflex/legend-ai-python/blob/main/docs/)
- [API Reference](https://github.com/Stockmasterflex/legend-ai-python/blob/main/API_ENDPOINTS.md)
- [Examples](https://github.com/Stockmasterflex/legend-ai-python/tree/main/docs/examples)
- [GitHub](https://github.com/Stockmasterflex/legend-ai-python)
- [npm](https://www.npmjs.com/package/@legend-ai/sdk)

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## ⚠️ Disclaimer

This is an educational tool. Not financial advice. Always do your own research before making investment decisions.
