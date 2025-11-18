# 🚀 Legend AI GraphQL API

Modern GraphQL API for the Legend AI Trading Pattern Scanner, providing a flexible and efficient alternative to REST.

## Overview

The GraphQL API provides:

- ✅ **Flexible queries** - Request exactly the data you need
- ✅ **Real-time subscriptions** - WebSocket-based live updates
- ✅ **Efficient data loading** - DataLoader batching prevents N+1 queries
- ✅ **Strong typing** - Full TypeScript support with code generation
- ✅ **Built-in caching** - Redis-backed query result caching
- ✅ **Interactive playground** - GraphiQL interface for exploration
- ✅ **Comprehensive documentation** - Self-documenting schema

## Getting Started

### GraphQL Endpoint

```
https://your-domain.com/graphql
```

### GraphQL Playground (GraphiQL)

Visit the endpoint in your browser to access the interactive GraphQL playground:

```
https://your-domain.com/graphql
```

Features:
- Interactive query builder
- Auto-completion
- Schema documentation
- Real-time query execution
- Query history

## Quick Start

### Example Query

```graphql
query {
  topSetups(minScore: 7.5, limit: 10) {
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

### Example Mutation

```graphql
mutation {
  addToWatchlist(
    input: {
      ticker: "AAPL"
      reason: "VCP pattern forming"
    }
  ) {
    id
    ticker {
      symbol
    }
  }
}
```

### Example Subscription

```graphql
subscription {
  patternDetected(minScore: 8.0) {
    ticker
    pattern
    score
    entry
  }
}
```

## Architecture

### Schema Design

```
┌─────────────────────────────────────┐
│         GraphQL Schema              │
├─────────────────────────────────────┤
│  Queries (Read Operations)          │
│  - ticker                           │
│  - patternScans                     │
│  - topSetups                        │
│  - watchlist                        │
│  - searchPatterns                   │
│                                     │
│  Mutations (Write Operations)       │
│  - addToWatchlist                   │
│  - updateWatchlist                  │
│  - scanPattern                      │
│  - calculatePositionSize            │
│                                     │
│  Subscriptions (Real-time)          │
│  - patternDetected                  │
│  - priceAlerts                      │
│  - scanProgress                     │
└─────────────────────────────────────┘
```

### Data Flow

```
Client Request
     ↓
FastAPI + Strawberry GraphQL
     ↓
GraphQL Context (DB + Cache + DataLoaders)
     ↓
Resolvers (with caching & batching)
     ↓
Business Logic Services
     ↓
Database / External APIs
     ↓
Response
```

### Performance Optimizations

1. **DataLoader Batching**
   - Batches multiple database queries into single requests
   - Prevents N+1 query problem
   - Automatic per-request caching

2. **Redis Caching**
   - Query result caching (5-60 min TTL)
   - Pattern detection results cached
   - Market data cached

3. **Efficient Database Queries**
   - Async database operations
   - Connection pooling
   - Optimized indexes

4. **Field-level Resolution**
   - Only requested fields are fetched
   - Nested resolvers are lazy-loaded

## Schema Documentation

### Types

#### Ticker
```graphql
type Ticker {
  id: Int!
  symbol: String!
  name: String
  sector: String
  industry: String
  exchange: String
  createdAt: DateTime!
  updatedAt: DateTime
}
```

#### PatternScan
```graphql
type PatternScan {
  id: Int!
  tickerId: Int!
  patternType: String!
  score: Float!
  entryPrice: Float
  stopPrice: Float
  targetPrice: Float
  riskRewardRatio: Float
  analysis: String
  scannedAt: DateTime!
  ticker: Ticker
}
```

#### WatchlistItem
```graphql
type WatchlistItem {
  id: Int!
  userId: String!
  tickerId: Int!
  status: String!
  targetEntry: Float
  targetStop: Float
  targetPrice: Float
  reason: String
  notes: String
  alertsEnabled: Boolean!
  addedAt: DateTime!
  ticker: Ticker
}
```

### Queries

| Query | Description | Arguments |
|-------|-------------|-----------|
| `ticker` | Get ticker by symbol | `symbol: String!` |
| `searchTickers` | Search tickers | `query: String!`, `limit: Int` |
| `tickersBySector` | Get tickers in sector | `sector: String!`, `limit: Int` |
| `detectPattern` | Real-time pattern detection | `ticker: String!`, `interval: String` |
| `patternScans` | Historical scans | `ticker: String!`, `limit: Int` |
| `topSetups` | Top scoring patterns | `minScore: Float`, `limit: Int`, `patternType: String` |
| `watchlist` | User watchlist | `userId: String`, `status: String` |
| `scanHistory` | Scan execution logs | `limit: Int` |
| `recentAlerts` | Recent alert history | `ticker: String`, `userId: String`, `limit: Int` |
| `searchPatterns` | Advanced pattern search | `patternType: String`, `minScore: Float`, `sector: String`, `limit: Int` |
| `stats` | Platform statistics | - |

### Mutations

| Mutation | Description | Input |
|----------|-------------|-------|
| `addToWatchlist` | Add ticker to watchlist | `WatchlistAddInput!` |
| `updateWatchlist` | Update watchlist item | `WatchlistUpdateInput!` |
| `removeFromWatchlist` | Remove from watchlist | `ticker: String!`, `userId: String` |
| `scanPattern` | Detect and save pattern | `PatternDetectInput!` |
| `calculatePositionSize` | Calculate position sizing | `PositionSizeInput!` |
| `generateChart` | Generate chart image | `ChartGenerateInput!` |
| `bulkAddToWatchlist` | Add multiple tickers | `tickers: [String!]!`, `userId: String`, `reason: String` |
| `clearCache` | Clear cache entries | `pattern: String!` |
| `cleanupOldScans` | Delete old scans | `daysOld: Int` |

### Subscriptions

| Subscription | Description | Arguments |
|--------------|-------------|-----------|
| `patternDetected` | Real-time pattern events | `tickers: [String!]`, `minScore: Float` |
| `priceAlerts` | Price alert notifications | `userId: String` |
| `scanProgress` | Universe scan progress | `scanId: Int!` |
| `watchlistUpdates` | Watchlist changes | `userId: String` |
| `marketUpdates` | Market breadth updates | - |

## Client Integration

### Supported Clients

- ✅ Apollo Client (JavaScript/TypeScript)
- ✅ Relay (React)
- ✅ URQL (React/Vue/Svelte)
- ✅ GraphQL Request (lightweight)
- ✅ Any GraphQL client library

### Quick Setup

**Apollo Client (React):**

```bash
npm install @apollo/client graphql
```

```typescript
import { ApolloClient, InMemoryCache } from '@apollo/client';

const client = new ApolloClient({
  uri: 'https://your-domain.com/graphql',
  cache: new InMemoryCache(),
});
```

See [CLIENT_SETUP.md](./CLIENT_SETUP.md) for detailed integration guides.

## Authentication

Currently, the API accepts all requests (matching the REST API behavior). To add authentication:

1. Include `Authorization` header:
   ```
   Authorization: Bearer YOUR_JWT_TOKEN
   ```

2. The token will be validated in the GraphQL context
3. User ID will be extracted and used for user-specific queries

## Rate Limiting

- Inherits FastAPI rate limiting (60 requests/minute per IP)
- Expensive operations may have additional limits
- Premium users (when implemented) will have higher limits

## Error Handling

GraphQL errors follow the standard format:

```json
{
  "errors": [
    {
      "message": "Ticker not found",
      "locations": [{ "line": 2, "column": 3 }],
      "path": ["ticker"]
    }
  ],
  "data": null
}
```

Error types:
- **Validation errors** - Invalid input
- **Not found errors** - Resource doesn't exist
- **Authorization errors** - Permission denied
- **Internal errors** - Server-side issues

## Monitoring & Performance

### Metrics

All GraphQL operations are tracked with Prometheus metrics:

- `graphql_query_duration_seconds` - Query execution time
- `graphql_query_total` - Total queries executed
- `graphql_errors_total` - Error count
- `graphql_cache_hits_total` - Cache hit rate

### Logging

Structured logs for all operations:

```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "level": "INFO",
  "operation": "topSetups",
  "duration_ms": 45.2,
  "cached": false,
  "user_id": "default"
}
```

## Best Practices

### 1. Request Only What You Need

❌ Over-fetching:
```graphql
query {
  topSetups(minScore: 7.0, limit: 20) {
    # All fields even if not needed
  }
}
```

✅ Optimal:
```graphql
query {
  topSetups(minScore: 7.0, limit: 20) {
    patternType
    score
    ticker { symbol }
  }
}
```

### 2. Use Query Variables

```graphql
query GetTicker($symbol: String!) {
  ticker(symbol: $symbol) {
    name
  }
}
```

### 3. Leverage Fragments

```graphql
fragment TickerInfo on Ticker {
  symbol
  name
  sector
}

query {
  topSetups(minScore: 7.0) {
    ticker { ...TickerInfo }
  }
}
```

### 4. Batch Queries

Instead of multiple requests, combine into one:

```graphql
query Dashboard {
  topSetups(minScore: 7.5) { ... }
  watchlist(userId: "default") { ... }
  scanHistory(limit: 5) { ... }
}
```

## Comparison: GraphQL vs REST

| Feature | GraphQL | REST |
|---------|---------|------|
| Data fetching | Request exactly what you need | Fixed endpoints |
| Over/Under fetching | No | Common issue |
| Real-time | Native subscriptions | Polling or SSE |
| Versioning | Not needed | Required (v1, v2) |
| Documentation | Self-documenting | Separate docs |
| Tooling | Rich ecosystem | Standard HTTP tools |
| Caching | Field-level | URL-based |
| Learning curve | Steeper | Gentler |

## Migration from REST

The GraphQL API complements the existing REST API. Both can be used simultaneously:

| REST Endpoint | GraphQL Equivalent |
|--------------|-------------------|
| `GET /api/patterns/detect` | `query { detectPattern }` |
| `POST /api/watchlist/add` | `mutation { addToWatchlist }` |
| `GET /api/scan/top-setups` | `query { topSetups }` |

## Troubleshooting

### Common Issues

**1. "Cannot query field X on type Y"**
- Field doesn't exist in schema
- Check schema documentation in playground

**2. "Variable $X of type Y was provided invalid value"**
- Type mismatch in variables
- Ensure variable types match schema

**3. "Subscription connection failed"**
- WebSocket connection issue
- Check if WSS is enabled
- Verify WebSocket URL (wss:// not https://)

**4. Slow queries**
- Requesting too many nested fields
- Reduce query complexity
- Use pagination for large datasets

## Contributing

To extend the GraphQL schema:

1. Add types in `app/graphql/types.py`
2. Add resolvers in `app/graphql/queries.py` or `mutations.py`
3. Update schema in `app/graphql/schema.py`
4. Add tests
5. Update documentation

## Resources

- 📖 [Query Examples](./QUERY_EXAMPLES.md) - Comprehensive query examples
- 💻 [Client Setup](./CLIENT_SETUP.md) - Integration guides for clients
- 🎮 [GraphQL Playground](https://your-domain.com/graphql) - Interactive explorer
- 📚 [GraphQL Docs](https://graphql.org/learn/) - Learn GraphQL basics
- 🍓 [Strawberry Docs](https://strawberry.rocks/) - Framework documentation

## Support

- 🐛 Report issues: [GitHub Issues](https://github.com/your-repo/issues)
- 💬 Questions: [Discussions](https://github.com/your-repo/discussions)
- 📧 Email: support@legend-ai.com

## License

Same license as the main Legend AI project.

---

**Built with ❤️ using Strawberry GraphQL + FastAPI**
