# GraphQL Query Examples

Complete collection of query, mutation, and subscription examples for the Legend AI GraphQL API.

## 🔍 Queries

### Get Ticker Information

```graphql
query GetTicker {
  ticker(symbol: "AAPL") {
    id
    symbol
    name
    sector
    industry
    exchange
    createdAt
  }
}
```

### Search Tickers

```graphql
query SearchTickers {
  searchTickers(query: "tech", limit: 10) {
    id
    symbol
    name
    sector
  }
}
```

### Get Tickers by Sector

```graphql
query TechStocks {
  tickersBySector(sector: "Technology", limit: 50) {
    symbol
    name
    industry
  }
}
```

### Real-time Pattern Detection

```graphql
query DetectPattern {
  detectPattern(ticker: "TSLA", interval: "1d") {
    ticker
    pattern
    score
    entry
    stop
    target
    riskReward
    criteriaMet
    analysis
    timestamp
    rsRating
    currentPrice
    chartUrl
  }
}
```

### Get Pattern Scans for a Ticker

```graphql
query PatternHistory {
  patternScans(ticker: "NVDA", limit: 10) {
    id
    patternType
    score
    entryPrice
    stopPrice
    targetPrice
    riskRewardRatio
    scannedAt
    ticker {
      symbol
      name
      sector
    }
  }
}
```

### Top Pattern Setups

```graphql
query TopSetups {
  topSetups(minScore: 7.5, limit: 20, patternType: "VCP") {
    id
    patternType
    score
    entryPrice
    stopPrice
    targetPrice
    riskRewardRatio
    consolidationDays
    rsRating
    scannedAt
    ticker {
      symbol
      name
      sector
      industry
    }
  }
}
```

### Watchlist

```graphql
query MyWatchlist {
  watchlist(userId: "default", status: "Watching") {
    id
    status
    targetEntry
    targetStop
    targetPrice
    reason
    notes
    alertsEnabled
    addedAt
    ticker {
      symbol
      name
      sector
    }
  }
}
```

### Scan History

```graphql
query ScanHistory {
  scanHistory(limit: 10) {
    id
    scanDate
    universe
    totalScanned
    patternsFound
    topScore
    durationSeconds
    status
  }
}
```

### Recent Alerts

```graphql
query RecentAlerts {
  recentAlerts(ticker: "AAPL", limit: 20) {
    id
    alertType
    triggerPrice
    alertSentAt
    status
    ticker {
      symbol
      name
    }
  }
}
```

### Advanced Pattern Search

```graphql
query SearchPatterns {
  searchPatterns(
    patternType: "Cup & Handle"
    minScore: 8.0
    sector: "Technology"
    limit: 30
    offset: 0
  ) {
    id
    patternType
    score
    entryPrice
    stopPrice
    targetPrice
    consolidationDays
    ticker {
      symbol
      name
      sector
    }
  }
}
```

### Platform Statistics

```graphql
query Stats {
  stats
}
```

Response:
```json
{
  "total_tickers": 5000,
  "total_scans": 125000,
  "total_watchlist_items": 250,
  "scans_last_24h": 1500,
  "timestamp": "2025-01-15T10:30:00Z"
}
```

---

## ✏️ Mutations

### Add to Watchlist

```graphql
mutation AddToWatchlist {
  addToWatchlist(
    input: {
      ticker: "AAPL"
      userId: "default"
      reason: "Cup & Handle forming, score 8.5"
      alertsEnabled: true
      alertThreshold: 2.0
    }
  ) {
    id
    status
    ticker {
      symbol
      name
    }
  }
}
```

### Update Watchlist Item

```graphql
mutation UpdateWatchlist {
  updateWatchlist(
    input: {
      id: 123
      status: TRIGGERED
      targetEntry: 185.50
      targetStop: 180.00
      targetPrice: 200.00
      notes: "Breakout confirmed with volume"
      alertsEnabled: true
    }
  ) {
    id
    status
    targetEntry
    targetStop
    targetPrice
    triggeredAt
  }
}
```

### Remove from Watchlist

```graphql
mutation RemoveFromWatchlist {
  removeFromWatchlist(ticker: "AAPL", userId: "default")
}
```

### Scan Pattern (Detect and Save)

```graphql
mutation ScanPattern {
  scanPattern(input: { ticker: "TSLA", interval: "1d", useYahooFallback: false }) {
    ticker
    pattern
    score
    entry
    stop
    target
    riskReward
    criteriaMet
    analysis
    chartUrl
  }
}
```

### Calculate Position Size

```graphql
mutation CalculatePosition {
  calculatePositionSize(
    input: {
      entry: 185.50
      stop: 180.00
      accountSize: 100000
      riskPercent: 1.0
      target: 200.00
    }
  ) {
    shares
    dollarAmount
    riskPerShare
    totalRisk
    positionPercent
  }
}
```

Example response:
```json
{
  "calculatePositionSize": {
    "shares": 181,
    "dollarAmount": 33575.50,
    "riskPerShare": 5.50,
    "totalRisk": 995.50,
    "positionPercent": 33.58
  }
}
```

### Generate Chart

```graphql
mutation GenerateChart {
  generateChart(
    input: {
      ticker: "NVDA"
      interval: "1d"
      timeframe: "6mo"
      indicators: ["SMA_50", "SMA_200", "VOLUME"]
    }
  )
}
```

Returns chart URL as string.

### Bulk Add to Watchlist

```graphql
mutation BulkAddToWatchlist {
  bulkAddToWatchlist(
    tickers: ["AAPL", "TSLA", "NVDA", "MSFT"]
    userId: "default"
    reason: "High RS stocks in breakout zone"
  )
}
```

Returns count of items added.

### Clear Cache

```graphql
mutation ClearCache {
  clearCache(pattern: "pattern:*")
}
```

### Cleanup Old Scans

```graphql
mutation CleanupScans {
  cleanupOldScans(daysOld: 30)
}
```

Returns count of deleted records.

---

## 🔴 Subscriptions (Real-time)

### Pattern Detection Events

```graphql
subscription PatternDetected {
  patternDetected(tickers: ["AAPL", "TSLA", "NVDA"], minScore: 7.5) {
    ticker
    pattern
    score
    entry
    timestamp
  }
}
```

Real-time events when patterns are detected on watched tickers.

### Price Alerts

```graphql
subscription PriceAlerts {
  priceAlerts(userId: "default") {
    ticker
    price
    alertType
    message
    timestamp
  }
}
```

Get notified when price alerts trigger.

### Scan Progress

```graphql
subscription ScanProgress {
  scanProgress(scanId: 12345) {
    scanId
    progress
    tickersScanned
    patternsFound
    currentTicker
  }
}
```

Monitor universe scan progress in real-time.

### Watchlist Updates

```graphql
subscription WatchlistUpdates {
  watchlistUpdates(userId: "default")
}
```

Get notified when watchlist items are added/removed/updated.

### Market Updates

```graphql
subscription MarketUpdates {
  marketUpdates
}
```

Real-time market breadth and internals data.

---

## 🔗 Complex Queries (Using Fragments)

### Full Ticker Profile

```graphql
fragment TickerDetails on Ticker {
  id
  symbol
  name
  sector
  industry
  exchange
}

fragment PatternDetails on PatternScan {
  id
  patternType
  score
  entryPrice
  stopPrice
  targetPrice
  riskRewardRatio
  consolidationDays
  rsRating
  scannedAt
}

query TickerProfile {
  ticker(symbol: "AAPL") {
    ...TickerDetails
  }

  patternScans(ticker: "AAPL", limit: 5) {
    ...PatternDetails
    ticker {
      ...TickerDetails
    }
  }

  watchlist(userId: "default") {
    id
    status
    ticker {
      ...TickerDetails
    }
  }
}
```

### Dashboard Query (Single Request)

```graphql
query Dashboard {
  # Top setups
  topSetups(minScore: 7.5, limit: 10) {
    id
    patternType
    score
    ticker {
      symbol
      name
      sector
    }
  }

  # User watchlist
  watchlist(userId: "default") {
    id
    status
    ticker {
      symbol
    }
  }

  # Recent scan history
  scanHistory(limit: 5) {
    id
    scanDate
    universe
    patternsFound
  }

  # Platform stats
  stats
}
```

---

## 📊 Performance Tips

### 1. Request Only What You Need

❌ **Bad** (Over-fetching):
```graphql
query {
  topSetups(minScore: 7.0, limit: 20) {
    id
    patternType
    score
    entryPrice
    stopPrice
    targetPrice
    riskRewardRatio
    criteriaMet
    analysis
    currentPrice
    volumeDryUp
    consolidationDays
    chartUrl
    rsRating
    scannedAt
    ticker {
      id
      symbol
      name
      sector
      industry
      exchange
      createdAt
      updatedAt
    }
  }
}
```

✅ **Good** (Only what's needed):
```graphql
query {
  topSetups(minScore: 7.0, limit: 20) {
    id
    patternType
    score
    entryPrice
    ticker {
      symbol
      name
    }
  }
}
```

### 2. Use Variables

❌ **Bad**:
```graphql
query {
  ticker(symbol: "AAPL") { ... }
}
```

✅ **Good**:
```graphql
query GetTicker($symbol: String!) {
  ticker(symbol: $symbol) { ... }
}

# Variables:
{ "symbol": "AAPL" }
```

### 3. Leverage Caching

Queries are automatically cached on the server side. Identical queries within the cache TTL window will return cached results.

### 4. Batch Related Queries

Instead of multiple requests:
```graphql
# Request 1
query { ticker(symbol: "AAPL") { ... } }

# Request 2
query { patternScans(ticker: "AAPL") { ... } }
```

Do this:
```graphql
# Single request
query {
  ticker(symbol: "AAPL") { ... }
  patternScans(ticker: "AAPL") { ... }
}
```

---

## 🎯 Use Cases

### Use Case 1: Build a Pattern Scanner Dashboard

1. Get top setups: `topSetups`
2. Subscribe to new patterns: `patternDetected` subscription
3. Add interesting patterns to watchlist: `addToWatchlist` mutation
4. Get detailed pattern info: `patternScans` query

### Use Case 2: Track Your Watchlist

1. Load watchlist: `watchlist` query
2. Subscribe to updates: `watchlistUpdates` subscription
3. Update status when triggered: `updateWatchlist` mutation
4. Remove completed trades: `removeFromWatchlist` mutation

### Use Case 3: Real-time Pattern Alerts

1. Subscribe to patterns on specific tickers: `patternDetected` subscription
2. Filter by minimum score
3. Get desktop notifications
4. Automatically add high-scoring patterns to watchlist

### Use Case 4: Portfolio Analysis

1. Search patterns in specific sector: `searchPatterns` with sector filter
2. Get ticker details: `ticker` query
3. Calculate position sizes: `calculatePositionSize` mutation
4. Generate charts: `generateChart` mutation

---

## 🐛 Debugging

Enable GraphQL debugging in Apollo Client DevTools:

1. Install [Apollo Client DevTools](https://www.apollographql.com/docs/react/development-testing/developer-tooling/)
2. Open browser DevTools → Apollo tab
3. Inspect queries, mutations, and cache

Test queries in GraphQL Playground:
- Visit: `https://your-api-domain.com/graphql`
- Use the built-in documentation explorer
- Test queries with variables
- View schema documentation

---

## 📚 Additional Resources

- [GraphQL Spec](https://spec.graphql.org/)
- [Strawberry GraphQL Docs](https://strawberry.rocks/)
- [Apollo Client Docs](https://www.apollographql.com/docs/react/)
