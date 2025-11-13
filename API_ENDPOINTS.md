# Complete API Endpoints Reference

**Base URL:** `https://legend-ai-python-production.up.railway.app`

---

## Health & Status Endpoints

### 1. Root Health Check
```
GET /
```
**Response:**
```json
{
  "status": "running",
  "service": "Legend AI Bot",
  "version": "1.0.0"
}
```

### 2. Detailed Health Check
```
GET /health
```
**Response:**
```json
{
  "status": "ok",
  "telegram_status": "configured",
  "cache_status": "healthy",
  "redis_status": "connected"
}
```

---

## Pattern Detection Endpoints

### 1. Detect Pattern
```
POST /api/patterns/detect
Content-Type: application/json

{
  "ticker": "NVDA",
  "interval": "1day"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "ticker": "NVDA",
    "pattern": "VCP",
    "score": 8.5,
    "entry": 120.50,
    "stop": 115.20,
    "target": 135.80,
    "risk_reward": 2.15,
    "current_price": 119.30,
    "rs_rating": 92,
    "source": "TwelveData"
  }
}
```

### 2. Cache Statistics
```
GET /api/patterns/cache/stats
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_keys": 150,
    "pattern_keys": 45,
    "price_keys": 78,
    "hit_rate": 87.5,
    "memory": "2.3 MB"
  }
}
```

---

## Chart Generation Endpoints

### 1. Generate Chart
```
POST /api/charts/generate
Content-Type: application/json

{
  "ticker": "NVDA",
  "interval": "1D",
  "timeframe": "6M",
  "indicators": ["SMA(50)", "SMA(200)"]
}
```

**Response:**
```json
{
  "success": true,
  "url": "https://.../chart.png"
}
```

---

## Universe Scanning Endpoints

### 1. Scan Universe
```
POST /api/universe/scan
Content-Type: application/json

{
  "min_score": 7.0,
  "limit": 20
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "ticker": "NVDA",
      "pattern": "VCP",
      "score": 8.5,
      "entry": 120.50,
      "stop": 115.20,
      "target": 135.80,
      "risk_reward": 2.15
    }
  ],
  "count": 15,
  "scanned": 100
}
```

### 2. Get Universe Tickers
```
GET /api/universe/tickers
```

**Response:**
```json
{
  "sp500_count": 500,
  "nasdaq100_count": 100,
  "total": 600
}
```

---

## Watchlist Endpoints

### 1. Get Watchlist
```
GET /api/watchlist?user_id={chat_id}
```

**Response:**
```json
{
  "success": true,
  "items": [
    {
      "ticker": "NVDA",
      "reason": "VCP Setup",
      "added_date": "2024-11-06",
      "status": "Monitoring"
    }
  ]
}
```

### 2. Add to Watchlist
```
POST /api/watchlist/add
Content-Type: application/json

{
  "ticker": "NVDA",
  "reason": "VCP Breakout Setup",
  "tags": "Momentum, Earnings",
  "user_id": "123456789"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Added NVDA to watchlist"
}
```

### 3. Remove from Watchlist
```
DELETE /api/watchlist/remove/{ticker}?user_id={chat_id}
```

**Response:**
```json
{
  "success": true,
  "message": "Removed NVDA from watchlist"
}
```

### 4. Get Watchlist Status
```
GET /api/watchlist/status/{ticker}
```

**Response:**
```json
{
  "success": true,
  "ticker": "NVDA",
  "in_watchlist": true,
  "added_date": "2024-11-06"
}
```

---

## Market Data Endpoints

### 1. Market Internals
```
GET /api/market/internals
```

**Response:**
```json
{
  "success": true,
  "data": {
    "spy_price": 589.45,
    "sma_50": 587.20,
    "sma_200": 580.15,
    "regime": "UPTREND",
    "status": "Bullish"
  }
}
```

---

## Trading Plan Endpoints

### 1. Generate Trading Plan
```
POST /api/plan
Content-Type: application/json

{
  "ticker": "NVDA",
  "account_size": 10000,
  "risk_percent": 2.0
}
```

**Response:**
```json
{
  "success": true,
  "plan": {
    "ticker": "NVDA",
    "pattern": "VCP",
    "entry": 120.50,
    "stop": 115.20,
    "target": 135.80,
    "shares": 38,
    "position_value": 4579.00,
    "risk_amount": 200.00,
    "potential_profit": 585.40,
    "account_size": 10000
  }
}
```

---

## Telegram Endpoints

### 1. Telegram Webhook (CRITICAL - Now Fixed!)
```
POST /api/webhook/telegram
Content-Type: application/json

{
  "update_id": 12345,
  "message": {
    "message_id": 1,
    "chat": {
      "id": "YOUR_CHAT_ID"
    },
    "text": "/start"
  }
}
```

**Response:**
```json
{
  "ok": true
}
```

---

## Testing with curl

### Test Pattern Detection
```bash
curl -X POST https://legend-ai-python-production.up.railway.app/api/patterns/detect \
  -H "Content-Type: application/json" \
  -d '{"ticker":"NVDA","interval":"1day"}'
```

### Test Telegram Webhook
```bash
curl -X POST https://legend-ai-python-production.up.railway.app/api/webhook/telegram \
  -H "Content-Type: application/json" \
  -d '{
    "update_id": 1,
    "message": {
      "message_id": 1,
      "chat": {"id": "999999"},
      "text": "/help"
    }
  }'
```

### Test Watchlist
```bash
curl -X GET https://legend-ai-python-production.up.railway.app/api/watchlist

curl -X POST https://legend-ai-python-production.up.railway.app/api/watchlist/add \
  -H "Content-Type: application/json" \
  -d '{"ticker":"TSLA","reason":"Test"}'
```

---

## Error Response Format

All endpoints return this format on error:

```json
{
  "success": false,
  "detail": "Error description here"
}
```

HTTP Status Codes:
- `200` - Success
- `400` - Bad Request (invalid params)
- `404` - Not Found
- `500` - Server Error
- `503` - Service Unavailable

---

## Rate Limits

- Pattern Detection: 5 per minute per ticker (api limits apply)
- Universe Scan: 1 per 2 minutes (limited by data source)
- Watchlist: Unlimited
- Telegram: As set by Telegram API

---

## Notes

- All times are in UTC
- Prices are in USD
- Timeouts vary by endpoint (see dashboard_pro.py for specifics)
- Dates are in YYYY-MM-DD format

