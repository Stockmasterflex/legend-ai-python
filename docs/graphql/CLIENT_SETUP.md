# GraphQL Client Setup

This guide shows how to integrate the Legend AI GraphQL API into your client applications.

## Table of Contents

- [Apollo Client Setup](#apollo-client-setup)
- [React Integration](#react-integration)
- [TypeScript Types](#typescript-types)
- [Example Queries](#example-queries)
- [Example Mutations](#example-mutations)
- [Real-time Subscriptions](#real-time-subscriptions)

---

## Apollo Client Setup

### Installation

```bash
npm install @apollo/client graphql
# or
yarn add @apollo/client graphql
```

### Basic Configuration

```typescript
// src/lib/apollo-client.ts
import { ApolloClient, InMemoryCache, HttpLink, split } from '@apollo/client';
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { getMainDefinition } from '@apollo/client/utilities';
import { createClient } from 'graphql-ws';

const httpLink = new HttpLink({
  uri: 'https://your-api-domain.com/graphql',
  headers: {
    // Add authorization header if needed
    // authorization: `Bearer ${token}`,
  },
});

// WebSocket link for subscriptions
const wsLink = new GraphQLWsLink(
  createClient({
    url: 'wss://your-api-domain.com/graphql',
    connectionParams: {
      // Add auth token if needed
      // authToken: token,
    },
  })
);

// Split links based on operation type
const splitLink = split(
  ({ query }) => {
    const definition = getMainDefinition(query);
    return (
      definition.kind === 'OperationDefinition' &&
      definition.operation === 'subscription'
    );
  },
  wsLink,
  httpLink
);

export const apolloClient = new ApolloClient({
  link: splitLink,
  cache: new InMemoryCache({
    typePolicies: {
      Query: {
        fields: {
          // Cache policy for pattern scans
          patternScans: {
            keyArgs: ['ticker'],
            merge(existing = [], incoming) {
              return [...existing, ...incoming];
            },
          },
        },
      },
    },
  }),
  defaultOptions: {
    watchQuery: {
      fetchPolicy: 'cache-and-network',
    },
  },
});
```

### Next.js App Router Setup

```typescript
// src/app/providers.tsx
'use client';

import { ApolloProvider } from '@apollo/client';
import { apolloClient } from '@/lib/apollo-client';

export function Providers({ children }: { children: React.ReactNode }) {
  return <ApolloProvider client={apolloClient}>{children}</ApolloProvider>;
}
```

```typescript
// src/app/layout.tsx
import { Providers } from './providers';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

---

## React Integration

### Example: Pattern Scanner Component

```typescript
// src/components/PatternScanner.tsx
'use client';

import { useQuery, gql } from '@apollo/client';

const TOP_SETUPS_QUERY = gql`
  query TopSetups($minScore: Float!, $limit: Int!) {
    topSetups(minScore: $minScore, limit: $limit) {
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
`;

export function PatternScanner() {
  const { loading, error, data, refetch } = useQuery(TOP_SETUPS_QUERY, {
    variables: { minScore: 7.0, limit: 20 },
    pollInterval: 60000, // Refresh every minute
  });

  if (loading) return <div>Loading top setups...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="pattern-scanner">
      <h2>Top Pattern Setups</h2>
      <button onClick={() => refetch()}>Refresh</button>

      <div className="setups-grid">
        {data.topSetups.map((setup) => (
          <div key={setup.id} className="setup-card">
            <h3>{setup.ticker.symbol}</h3>
            <p>{setup.ticker.name}</p>
            <div className="pattern-info">
              <span className="pattern-type">{setup.patternType}</span>
              <span className="score">Score: {setup.score.toFixed(1)}</span>
            </div>
            <div className="trade-levels">
              <p>Entry: ${setup.entryPrice.toFixed(2)}</p>
              <p>Stop: ${setup.stopPrice.toFixed(2)}</p>
              <p>Target: ${setup.targetPrice.toFixed(2)}</p>
              <p>R:R = {setup.riskRewardRatio.toFixed(2)}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### Example: Watchlist Manager

```typescript
// src/components/WatchlistManager.tsx
'use client';

import { useQuery, useMutation, gql } from '@apollo/client';
import { useState } from 'react';

const WATCHLIST_QUERY = gql`
  query Watchlist($userId: String!) {
    watchlist(userId: $userId) {
      id
      status
      reason
      alertsEnabled
      addedAt
      ticker {
        symbol
        name
        sector
      }
    }
  }
`;

const ADD_TO_WATCHLIST = gql`
  mutation AddToWatchlist($input: WatchlistAddInput!) {
    addToWatchlist(input: $input) {
      id
      ticker {
        symbol
      }
    }
  }
`;

const REMOVE_FROM_WATCHLIST = gql`
  mutation RemoveFromWatchlist($ticker: String!, $userId: String!) {
    removeFromWatchlist(ticker: $ticker, userId: $userId)
  }
`;

export function WatchlistManager({ userId = 'default' }) {
  const [ticker, setTicker] = useState('');
  const [reason, setReason] = useState('');

  const { data, loading, refetch } = useQuery(WATCHLIST_QUERY, {
    variables: { userId },
  });

  const [addToWatchlist] = useMutation(ADD_TO_WATCHLIST, {
    onCompleted: () => {
      setTicker('');
      setReason('');
      refetch();
    },
  });

  const [removeFromWatchlist] = useMutation(REMOVE_FROM_WATCHLIST, {
    onCompleted: () => refetch(),
  });

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    await addToWatchlist({
      variables: {
        input: {
          ticker,
          userId,
          reason,
          alertsEnabled: true,
        },
      },
    });
  };

  return (
    <div className="watchlist-manager">
      <h2>My Watchlist</h2>

      <form onSubmit={handleAdd}>
        <input
          type="text"
          placeholder="Ticker (e.g., AAPL)"
          value={ticker}
          onChange={(e) => setTicker(e.target.value.toUpperCase())}
          required
        />
        <input
          type="text"
          placeholder="Reason"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
        />
        <button type="submit">Add to Watchlist</button>
      </form>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {data?.watchlist.map((item) => (
            <li key={item.id}>
              <strong>{item.ticker.symbol}</strong> - {item.ticker.name}
              <br />
              <small>Status: {item.status}</small>
              <br />
              <small>Reason: {item.reason}</small>
              <button
                onClick={() =>
                  removeFromWatchlist({
                    variables: { ticker: item.ticker.symbol, userId },
                  })
                }
              >
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

---

## Real-time Subscriptions

### Pattern Detection Events

```typescript
// src/hooks/usePatternDetection.ts
import { useSubscription, gql } from '@apollo/client';

const PATTERN_DETECTED = gql`
  subscription PatternDetected($tickers: [String!]!, $minScore: Float!) {
    patternDetected(tickers: $tickers, minScore: $minScore) {
      ticker
      pattern
      score
      entry
      timestamp
    }
  }
`;

export function usePatternDetection(tickers: string[], minScore = 7.0) {
  const { data, loading } = useSubscription(PATTERN_DETECTED, {
    variables: { tickers, minScore },
  });

  return { event: data?.patternDetected, loading };
}
```

### Usage in Component

```typescript
// src/components/LivePatternFeed.tsx
'use client';

import { usePatternDetection } from '@/hooks/usePatternDetection';
import { useState, useEffect } from 'react';

export function LivePatternFeed() {
  const watchlist = ['AAPL', 'TSLA', 'NVDA', 'MSFT'];
  const { event } = usePatternDetection(watchlist, 7.5);
  const [events, setEvents] = useState([]);

  useEffect(() => {
    if (event) {
      setEvents((prev) => [event, ...prev].slice(0, 50)); // Keep last 50 events

      // Show notification
      if (Notification.permission === 'granted') {
        new Notification(`${event.pattern} detected on ${event.ticker}`, {
          body: `Score: ${event.score} | Entry: $${event.entry}`,
        });
      }
    }
  }, [event]);

  return (
    <div className="live-feed">
      <h2>🔴 Live Pattern Detection</h2>
      <div className="events">
        {events.map((evt, idx) => (
          <div key={idx} className="event">
            <strong>{evt.ticker}</strong> - {evt.pattern}
            <br />
            Score: {evt.score} | Entry: ${evt.entry}
            <br />
            <small>{new Date(evt.timestamp).toLocaleString()}</small>
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## TypeScript Types

### Generate Types from Schema

Install code generator:

```bash
npm install -D @graphql-codegen/cli @graphql-codegen/typescript
npm install -D @graphql-codegen/typescript-operations
npm install -D @graphql-codegen/typescript-react-apollo
```

Create `codegen.yml`:

```yaml
# codegen.yml
schema: 'https://your-api-domain.com/graphql'
documents: 'src/**/*.{ts,tsx}'
generates:
  src/generated/graphql.ts:
    plugins:
      - 'typescript'
      - 'typescript-operations'
      - 'typescript-react-apollo'
    config:
      withHooks: true
      withComponent: false
      withHOC: false
```

Add script to `package.json`:

```json
{
  "scripts": {
    "codegen": "graphql-codegen --config codegen.yml"
  }
}
```

Run code generation:

```bash
npm run codegen
```

### Use Generated Types

```typescript
import { useTopSetupsQuery } from '@/generated/graphql';

function MyComponent() {
  const { data, loading } = useTopSetupsQuery({
    variables: { minScore: 7.0, limit: 20 },
  });

  // Types are automatically inferred!
  // data.topSetups is fully typed
}
```

---

## Optimistic Updates

```typescript
const UPDATE_WATCHLIST = gql`
  mutation UpdateWatchlist($input: WatchlistUpdateInput!) {
    updateWatchlist(input: $input) {
      id
      status
      notes
    }
  }
`;

const [updateWatchlist] = useMutation(UPDATE_WATCHLIST, {
  optimisticResponse: ({ input }) => ({
    updateWatchlist: {
      __typename: 'WatchlistItem',
      id: input.id,
      status: input.status || 'Watching',
      notes: input.notes || '',
    },
  }),
  update(cache, { data }) {
    // Update cache after mutation
    cache.modify({
      fields: {
        watchlist(existingItems = []) {
          return existingItems.map((item) =>
            item.id === data.updateWatchlist.id
              ? { ...item, ...data.updateWatchlist }
              : item
          );
        },
      },
    });
  },
});
```

---

## Error Handling

```typescript
import { ApolloError } from '@apollo/client';

function handleGraphQLError(error: ApolloError) {
  if (error.networkError) {
    console.error('Network error:', error.networkError);
    return 'Network error. Please check your connection.';
  }

  if (error.graphQLErrors) {
    error.graphQLErrors.forEach((err) => {
      console.error('GraphQL error:', err.message);
    });
    return 'Something went wrong. Please try again.';
  }

  return 'An unexpected error occurred.';
}
```

---

## Best Practices

1. **Use Fragments** for reusable field selections:

```typescript
const TICKER_FRAGMENT = gql`
  fragment TickerFields on Ticker {
    id
    symbol
    name
    sector
    industry
  }
`;

const QUERY = gql`
  ${TICKER_FRAGMENT}
  query GetTicker($symbol: String!) {
    ticker(symbol: $symbol) {
      ...TickerFields
    }
  }
`;
```

2. **Implement Pagination** for large datasets:

```typescript
const { data, fetchMore } = useQuery(PATTERN_SCANS_QUERY, {
  variables: { limit: 20, offset: 0 },
});

const loadMore = () => {
  fetchMore({
    variables: { offset: data.patternScans.length },
  });
};
```

3. **Cache Management**:

```typescript
// Clear cache on logout
apolloClient.clearStore();

// Evict specific items
apolloClient.cache.evict({ id: 'Ticker:1' });
apolloClient.cache.gc();
```

4. **Batch Queries**:

```typescript
const { data } = useQuery(gql`
  query GetAllData($ticker: String!) {
    ticker(symbol: $ticker) {
      symbol
      name
    }
    patternScans(ticker: $ticker, limit: 10) {
      id
      patternType
      score
    }
    watchlist(userId: "default") {
      id
      status
    }
  }
`);
```

---

## Additional Resources

- [Apollo Client Documentation](https://www.apollographql.com/docs/react/)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [Strawberry GraphQL](https://strawberry.rocks/)
