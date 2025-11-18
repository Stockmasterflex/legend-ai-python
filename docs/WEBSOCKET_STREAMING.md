# WebSocket Real-Time Streaming

## Overview

The Legend AI trading platform now supports real-time streaming of market data, pattern alerts, and notifications via WebSockets. This feature enables live updates without page refreshes, providing traders with instant information about price movements, pattern detections, and alert triggers.

## Architecture

### Backend Components

#### 1. WebSocket Connection Manager (`app/services/websocket_manager.py`)

The connection manager handles all WebSocket connections and provides:

- **Connection Pooling**: Manages multiple concurrent WebSocket connections
- **Subscription Management**: Tracks which clients are subscribed to which data streams
- **Redis Pub/Sub Integration**: Enables horizontal scaling across multiple server instances
- **Message Broadcasting**: Efficiently broadcasts messages to subscribed clients
- **Heartbeat Mechanism**: Monitors connection health with ping/pong
- **Message History**: Stores recent messages for replay to new subscribers
- **Throttling**: Prevents message flooding (max 10 messages/second per connection)
- **Stale Connection Cleanup**: Automatically removes dead connections

**Key Methods:**
```python
manager = get_manager()

# Connection management
await manager.connect(websocket, connection_id, user_id)
manager.disconnect(connection_id)

# Subscriptions
await manager.subscribe_ticker(connection_id, "AAPL")
await manager.subscribe_patterns(connection_id)
await manager.subscribe_alerts(connection_id)
await manager.subscribe_market_status(connection_id)

# Broadcasting
await manager.publish_price_update(ticker, price_data)
await manager.publish_pattern_alert(pattern_data)
await manager.publish_alert_trigger(alert_data)
await manager.publish_market_status(status_data)
```

#### 2. WebSocket Router (`app/routers/websocket.py`)

FastAPI WebSocket endpoint that handles:

- WebSocket connections at `/api/ws`
- Message routing based on message type
- Subscription/unsubscription requests
- Heartbeat ping/pong
- Error handling

**Endpoints:**
- `WebSocket /api/ws` - Main WebSocket endpoint
- `GET /api/ws/stats` - Connection statistics
- `POST /api/ws/broadcast/price` - Broadcast price update (internal)
- `POST /api/ws/broadcast/pattern` - Broadcast pattern alert (internal)
- `POST /api/ws/broadcast/alert` - Broadcast alert trigger (internal)
- `POST /api/ws/broadcast/market_status` - Broadcast market status (internal)

#### 3. Real-Time Streamer Service (`app/services/realtime_streamer.py`)

Background service that:

- Fetches live price data for subscribed tickers
- Monitors watchlist for alert conditions
- Tracks market status (open/closed)
- Cleans up stale connections
- Adjusts update frequency based on market hours

**Configuration:**
```python
streamer = get_streamer()
await streamer.start()  # Starts background tasks
await streamer.stop()   # Stops all tasks
```

### Frontend Components

#### 1. WebSocket Client (`static/js/websocket-client.js`)

Core WebSocket client with advanced features:

**Features:**
- ✅ Automatic reconnection with exponential backoff
- ✅ Message queue management for high-frequency updates
- ✅ Throttled DOM updates (max 10/sec)
- ✅ Batch DOM updates for performance
- ✅ Memory leak prevention
- ✅ Heartbeat/ping-pong mechanism
- ✅ Connection health monitoring
- ✅ Change detection (only update changed elements)

**Usage:**
```javascript
// Create client
const ws = new WebSocketClient({
    userId: 'user123',
    maxMessagesPerSecond: 10,
    batchUpdateDelay: 100
});

// Connect
ws.connect();

// Subscribe to data streams
ws.subscribe('ticker', 'AAPL');
ws.subscribe('patterns');
ws.subscribe('alerts');
ws.subscribe('market_status');

// Register event handlers
ws.on('price_update', (data) => {
    console.log('Price update:', data);
});

ws.on('pattern_alert', (data) => {
    console.log('Pattern detected:', data);
});

// Efficient DOM updates
const priceElement = document.getElementById('aapl-price');
ws.updateElementIfChanged(priceElement, 150.25, val => `$${val.toFixed(2)}`);

// Get statistics
const stats = ws.getStats();
console.log('WebSocket stats:', stats);

// Disconnect
ws.disconnect();
```

#### 2. Real-Time Dashboard Integration (`static/js/realtime-dashboard.js`)

Dashboard integration that:

- Auto-connects to WebSocket on page load
- Subscribes to all watchlist tickers
- Updates price displays in real-time
- Shows notifications for significant events
- Displays connection status
- Plays sound alerts (configurable)

**Auto-initialization:**
```javascript
// Automatically initializes on page load
// Access via global: window.realtimeDashboard

// Manual subscription
realtimeDashboard.subscribeTicker('TSLA');
realtimeDashboard.unsubscribeTicker('TSLA');

// Toggle stats display
realtimeDashboard.toggleStats();
```

#### 3. Real-Time Styles (`static/css/realtime.css`)

Professional UI components:

- Connection status indicator
- Animated notifications
- Price change animations
- Pattern detection highlights
- Alert trigger effects
- Market status badges
- Loading skeletons

## Message Protocol

### Client → Server Messages

#### 1. Subscribe to Ticker
```json
{
    "type": "subscribe",
    "channel": "ticker",
    "ticker": "AAPL"
}
```

#### 2. Subscribe to Patterns
```json
{
    "type": "subscribe",
    "channel": "patterns"
}
```

#### 3. Subscribe to Alerts
```json
{
    "type": "subscribe",
    "channel": "alerts"
}
```

#### 4. Subscribe to Market Status
```json
{
    "type": "subscribe",
    "channel": "market_status"
}
```

#### 5. Heartbeat Ping
```json
{
    "type": "ping"
}
```

#### 6. Unsubscribe
```json
{
    "type": "unsubscribe",
    "channel": "ticker",
    "ticker": "AAPL"
}
```

### Server → Client Messages

#### 1. Connection Acknowledgment
```json
{
    "type": "connection",
    "status": "connected",
    "connection_id": "user123_abc123",
    "timestamp": "2025-11-18T10:30:00Z"
}
```

#### 2. Price Update
```json
{
    "type": "price_update",
    "ticker": "AAPL",
    "price": 150.25,
    "change": 2.50,
    "change_percent": 1.69,
    "volume": 75000000,
    "high": 151.00,
    "low": 148.50,
    "open": 149.00,
    "timestamp": "2025-11-18T10:30:00Z"
}
```

#### 3. Pattern Alert
```json
{
    "type": "pattern_alert",
    "ticker": "AAPL",
    "pattern_type": "VCP",
    "score": 8.5,
    "entry_price": 150.50,
    "stop_price": 145.00,
    "target_price": 165.00,
    "risk_reward_ratio": 2.64,
    "message": "VCP pattern detected with high score",
    "timestamp": "2025-11-18T10:30:00Z"
}
```

#### 4. Alert Trigger
```json
{
    "type": "alert_trigger",
    "ticker": "AAPL",
    "alert_type": "breakout",
    "trigger_price": 150.00,
    "current_price": 150.25,
    "message": "AAPL breaking out at $150.25 (target: $150.00)",
    "timestamp": "2025-11-18T10:30:00Z"
}
```

#### 5. Market Status
```json
{
    "type": "market_status",
    "status": "open",
    "next_open": null,
    "next_close": "2025-11-18T21:00:00Z",
    "timestamp": "2025-11-18T14:30:00Z"
}
```

#### 6. Subscription Confirmation
```json
{
    "type": "subscription",
    "action": "subscribed",
    "ticker": "AAPL",
    "timestamp": "2025-11-18T10:30:00Z"
}
```

#### 7. Historical Data
```json
{
    "type": "history",
    "ticker": "AAPL",
    "messages": [
        {
            "type": "price_update",
            "ticker": "AAPL",
            "price": 149.50,
            "...": "..."
        }
    ],
    "timestamp": "2025-11-18T10:30:00Z"
}
```

#### 8. Pong Response
```json
{
    "type": "pong",
    "timestamp": "2025-11-18T10:30:00Z"
}
```

#### 9. Error
```json
{
    "type": "error",
    "message": "Unknown message type: invalid",
    "timestamp": "2025-11-18T10:30:00Z"
}
```

## Redis Pub/Sub Channels

For horizontal scaling across multiple server instances:

### Channels
- `price_updates` - Price update broadcasts
- `pattern_alerts` - Pattern detection alerts
- `alert_triggers` - Alert trigger notifications
- `market_status` - Market status changes

### Message Format
All Redis messages are JSON-encoded with the same structure as WebSocket messages.

## Performance Optimizations

### Backend

1. **Connection Pooling**: Efficient management of WebSocket connections
2. **Message Throttling**: Max 10 messages/sec per connection to prevent flooding
3. **Batch Processing**: Process multiple subscriptions in batches
4. **Lazy Data Fetching**: Only fetch data for subscribed tickers
5. **Redis Pub/Sub**: Enable horizontal scaling without N×N connections
6. **Message History**: Cache last 100 messages per ticker for instant replay
7. **Stale Connection Cleanup**: Remove inactive connections automatically

### Frontend

1. **Throttling**: Max 10 messages/sec processing to prevent UI lag
2. **Message Queue**: Queue high-frequency updates for smooth processing
3. **Batch DOM Updates**: Group DOM changes and apply once per frame (100ms)
4. **Change Detection**: Only update DOM elements when values actually change
5. **requestAnimationFrame**: Use browser's rendering cycle for updates
6. **Memory Management**: Automatic cache clearing to prevent memory leaks
7. **Exponential Backoff**: Smart reconnection strategy (1s → 30s max)

## Configuration

### Environment Variables

```bash
# Redis URL for pub/sub (required for scaling)
REDIS_URL=redis://localhost:6379

# Optional: Configure update intervals
REALTIME_UPDATE_INTERVAL=5  # seconds (market hours)
REALTIME_AFTER_HOURS_INTERVAL=60  # seconds (after hours)
```

### JavaScript Configuration

```javascript
const ws = new WebSocketClient({
    url: 'ws://localhost:8000/api/ws',  // Auto-detected by default
    userId: 'user123',
    reconnectDelay: 1000,  // Initial reconnect delay (ms)
    maxReconnectDelay: 30000,  // Max reconnect delay (ms)
    reconnectBackoffMultiplier: 1.5,
    heartbeatInterval: 30000,  // Heartbeat every 30s
    maxMessagesPerSecond: 10,  // Throttle limit
    batchUpdateDelay: 100,  // DOM update batching (ms)
    maxQueueSize: 1000  // Max queued messages
});
```

## Deployment

### Single Server (No Redis)

WebSocket will work on a single server without Redis. Messages are broadcasted directly to connected clients.

### Multiple Servers (With Redis)

For horizontal scaling:

1. **Setup Redis**: Ensure Redis is running and accessible
2. **Configure REDIS_URL**: Set environment variable
3. **Deploy Multiple Instances**: Each instance connects to the same Redis
4. **Load Balancer**: Configure sticky sessions or use Redis for session storage

```yaml
# docker-compose.yml
services:
  app1:
    environment:
      - REDIS_URL=redis://redis:6379
  app2:
    environment:
      - REDIS_URL=redis://redis:6379
  redis:
    image: redis:7-alpine
```

## Testing

### Manual Testing

1. **Open Dashboard**: Navigate to `/dashboard`
2. **Check Connection**: Look for green "Live" indicator in header
3. **Open Browser Console**: Check for WebSocket logs
4. **Add Tickers to Watchlist**: They should auto-subscribe
5. **Wait for Updates**: Price updates should appear every 5 seconds (market hours)

### API Testing

```bash
# Get WebSocket stats
curl http://localhost:8000/api/ws/stats

# Broadcast test price update
curl -X POST "http://localhost:8000/api/ws/broadcast/price" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "price": 150.25,
    "change": 2.50,
    "change_percent": 1.69,
    "volume": 75000000,
    "high": 151.00,
    "low": 148.50,
    "open_price": 149.00
  }'
```

### WebSocket Client Testing

```javascript
// Open browser console on dashboard
const stats = realtimeDashboard.ws.getStats();
console.log('Connection stats:', stats);

// Toggle stats display
realtimeDashboard.toggleStats();

// Manually subscribe to a ticker
realtimeDashboard.subscribeTicker('TSLA');

// Check subscriptions
console.log('Subscriptions:', stats.subscriptions);
```

## Monitoring

### Connection Statistics

```bash
GET /api/ws/stats
```

Returns:
```json
{
    "active_connections": 15,
    "ticker_subscriptions": {
        "AAPL": 10,
        "TSLA": 5,
        "MSFT": 8
    },
    "pattern_subscribers": 12,
    "alert_subscribers": 15,
    "market_status_subscribers": 15,
    "total_connections": 150,
    "messages_sent": 45000,
    "messages_received": 3000,
    "errors": 2,
    "uptime": 3600
}
```

### Frontend Statistics

Access via browser console:
```javascript
realtimeDashboard.ws.getStats()
```

Returns:
```json
{
    "connected": true,
    "reconnecting": false,
    "reconnectAttempts": 0,
    "messagesReceived": 1250,
    "messagesSent": 45,
    "updatesApplied": 3800,
    "reconnects": 1,
    "errors": 0,
    "lastMessageTime": "2025-11-18T10:30:00Z",
    "subscriptions": ["ticker:AAPL", "ticker:TSLA", "patterns", "alerts"],
    "queueSize": 0,
    "pendingUpdates": 0,
    "cacheSize": 50
}
```

## Troubleshooting

### Connection Issues

**Problem**: WebSocket won't connect

**Solutions**:
1. Check if server is running: `GET /health`
2. Verify WebSocket endpoint: `ws://localhost:8000/api/ws`
3. Check browser console for errors
4. Ensure no firewall blocking WebSocket connections
5. Try disabling browser extensions

### Performance Issues

**Problem**: UI lagging with high-frequency updates

**Solutions**:
1. Reduce `maxMessagesPerSecond` in client config
2. Increase `batchUpdateDelay` for less frequent DOM updates
3. Unsubscribe from unused tickers
4. Clear cache: `ws.clearCache()`
5. Check browser performance in DevTools

### Memory Leaks

**Problem**: Memory usage growing over time

**Solutions**:
1. Disconnect and reconnect periodically
2. Clear data cache: `ws.clearCache()`
3. Ensure event handlers are properly removed
4. Check for orphaned DOM elements

### Redis Connection Issues

**Problem**: Redis pub/sub not working

**Solutions**:
1. Verify Redis is running: `redis-cli ping`
2. Check REDIS_URL environment variable
3. Test Redis connection: `redis-cli -u $REDIS_URL ping`
4. Check firewall rules
5. Verify Redis version (7+ recommended)

## Security Considerations

1. **Authentication**: Consider adding JWT token authentication to WebSocket connections
2. **Rate Limiting**: Already implemented (10 msg/sec per connection)
3. **Input Validation**: All messages are validated before processing
4. **CORS**: WebSocket respects CORS settings from FastAPI
5. **Heartbeat**: Prevents zombie connections (stale after 60s)

## Future Enhancements

- [ ] User authentication for WebSocket connections
- [ ] Per-user message filtering
- [ ] Advanced pattern alerts with custom criteria
- [ ] Order execution notifications
- [ ] Portfolio value updates
- [ ] News alerts
- [ ] Social sentiment updates
- [ ] Multi-user chat/collaboration
- [ ] Screen sharing for education
- [ ] Voice alerts

## API Documentation

Full WebSocket API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Look for the "websocket" tag in the API documentation.
