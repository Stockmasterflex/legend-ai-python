# Chart-IMG Pro API Documentation

## Overview
Chart-IMG provides REST API endpoints for generating TradingView chart images. This document covers our Pro Plan configuration.

## Plan Details
- **Plan**: Pro
- **Daily Limit**: 500 requests/day
- **Rate Limit**: 10 requests/sec
- **Max Resolution**: 1920 x 1080
- **Watermark**: No
- **Max Parameters**: 5 (studies + drawings combined)
- **Storage Duration**: 30 days

## Authentication

### Method 1: Header Authentication (Recommended)
```
x-api-key: YOUR_API_KEY
```

### Method 2: Query Parameter
```
?key=YOUR_API_KEY
```

## Base Endpoint
```
https://api.chart-img.com/v2/tradingview/advanced-chart
```

## Chart Generation (v2 Advanced Chart)

### POST Request Example
```bash
curl -X POST https://api.chart-img.com/v2/tradingview/advanced-chart \
  -H "x-api-key: YOUR_API_KEY" \
  -H "content-type: application/json" \
  -d '{
    "symbol": "NASDAQ:AAPL",
    "interval": "1D",
    "width": 1200,
    "height": 600,
    "theme": "dark",
    "studies": [...],
    "drawings": [...]
  }'
```

### Request Parameters

#### Required/Common
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| symbol | String | BINANCE:BTCUSDT | TradingView symbol (EXCHANGE:SYMBOL) |
| interval | String | 1D | Chart interval [1m, 5m, 15m, 30m, 1h, 4h, 1D, 1W, 1M] |
| width | Integer | 800 | Image width in pixels (Min: 400, Max: 1920) |
| height | Integer | 600 | Image height in pixels (Min: 300, Max: 1080) |

#### Optional
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| theme | String | light | Chart theme [light, dark] |
| style | String | candle | Chart style [candle, bar, line, area, heikinAshi, hollowCandle, baseline, hiLo, column] |
| format | String | png | Image format [png, jpeg] |
| range | Object | - | Set custom date range {from, to} in ISO8601 |
| studies | Array | [] | Indicator studies (max 5 including drawings) |
| drawings | Array | [] | Chart annotations (max 5 including studies) |
| override | Object | {} | Override chart settings |

## Key Indicators for Legend AI

### 1. Relative Strength Index (RSI)
```json
{
  "name": "Relative Strength Index",
  "input": {
    "length": 14,
    "smoothingLine": "SMA",
    "smoothingLength": 14
  },
  "override": {
    "Plot.linewidth": 2,
    "Plot.plottype": "line",
    "Plot.color": "rgb(126,87,194)",
    "UpperLimit.visible": true,
    "UpperLimit.value": 70,
    "LowerLimit.visible": true,
    "LowerLimit.value": 30
  }
}
```

### 2. Moving Averages (EMA 21 & SMA 50)
```json
{
  "name": "Moving Average Exponential",
  "input": {
    "length": 21,
    "source": "close"
  },
  "override": {
    "Plot.linewidth": 2,
    "Plot.color": "rgb(255,109,0)"
  }
},
{
  "name": "Moving Average",
  "input": {
    "length": 50,
    "source": "close",
    "smoothingLine": "SMA"
  },
  "override": {
    "Plot.linewidth": 2,
    "Plot.color": "rgb(67,160,71)"
  }
}
```

### 3. Volume
```json
{
  "name": "Volume",
  "forceOverlay": false,
  "override": {
    "Volume.plottype": "columns",
    "Volume.color.0": "rgba(247,82,95,0.5)",
    "Volume.color.1": "rgba(34,171,148,0.5)"
  }
}
```

## Key Drawings for Legend AI

### 1. Long Position (Entry, Stop, Target)
```json
{
  "name": "Long Position",
  "input": {
    "startDatetime": "2025-01-01T00:00:00.000Z",
    "entryPrice": 150.00,
    "targetPrice": 160.00,
    "stopPrice": 145.00
  },
  "override": {
    "fillBackground": true,
    "showPrice": true,
    "showStats": true
  }
}
```

### 2. Support & Resistance (Horizontal Lines)
```json
{
  "name": "Horizontal Line",
  "input": {
    "price": 155.00,
    "text": "Resistance"
  },
  "override": {
    "lineColor": "rgb(255,82,82)",
    "textColor": "rgb(255,82,82)",
    "lineStyle": 1
  }
},
{
  "name": "Horizontal Line",
  "input": {
    "price": 145.00,
    "text": "Support"
  },
  "override": {
    "lineColor": "rgb(67,160,71)",
    "textColor": "rgb(67,160,71)",
    "lineStyle": 1
  }
}
```

## Response Format

### Success Response (200 OK)
```json
{
  "url": "https://r2.chart-img.com/tradingview/advanced-chart/snapshot/ABC123.png",
  "etag": "abc123def456",
  "expire": "2025-02-06T23:19:30.786Z"
}
```

### Storage Endpoint
Also available: `/v2/tradingview/advanced-chart/storage` for storing charts in Cloud Storage.

## Error Codes

| Status | Error | Meaning |
|--------|-------|---------|
| 400 | Bad Request | Invalid JSON format |
| 401 | Invalid Request | Missing/invalid API key |
| 403 | Forbidden | API key invalid or inactive |
| 422 | Invalid Symbol/Interval | Invalid symbol or unsupported interval |
| 429 | Too Many Requests | Rate limit exceeded (10/sec) or daily limit exceeded (500/day) |
| 500 | Server Error | API server error |
| 504 | Timeout | Request took too long |

## Rate Limiting Strategy
- **Per Second**: 10 requests max
- **Per Day**: 500 requests max
- **Queue Strategy**: Use delays between requests to stay under rate limit
- **Retry Strategy**: Exponential backoff for 429/504 errors

## Testing Symbols
- `NASDAQ:AAPL` - Apple
- `NASDAQ:NVDA` - Nvidia
- `NYSE:JPM` - JP Morgan
- `BINANCE:BTCUSDT` - Bitcoin
- `COINBASE:BTCUSD` - Bitcoin (Coinbase)

## Supported Exchanges
See `/v3/tradingview/exchange/list` for complete list. Common ones:
- NASDAQ, NYSE, AMEX - US Stocks
- BINANCE, COINBASE, KRAKEN - Crypto
- FOREX.com, OANDA - Forex
- CME, CBOT, NYMEX - Futures

## Implementation Notes

1. **Always use v2 API** for advanced charts with indicators and drawings
2. **Icon/Display**: Chart URL can be embedded as `<img>` tag or `<iframe>` for interactive embed
3. **Caching**: Cache chart URLs for 24 hours to reduce API calls
4. **Error Handling**: Implement retry logic with exponential backoff
5. **Daily Tracking**: Monitor daily API usage to stay under 500 calls/day limit

## Feature Matrix

| Feature | Available | Pro Plan Limit |
|---------|-----------|-----------------|
| Custom indicators | Yes | 5 total (studies + drawings) |
| Chart styles | Yes | All 9 styles |
| Resolutions | Yes | Up to 1920x1080 |
| Watermark | No | Removed |
| Export formats | Yes | PNG, JPEG |
| Storage duration | Yes | 30 days |
| Rate limit | 10/sec | Per second |
| Daily quota | 500 | Per day |

## Next Steps
- Integrate into `app/services/charting.py`
- Add indicator calculations to pattern detection
- Implement support/resistance level drawing
- Add long position visualization to charts
