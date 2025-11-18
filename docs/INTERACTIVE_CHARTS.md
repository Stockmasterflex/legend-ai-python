# Interactive Charts System

## Overview

Legend AI now features a professional, interactive charting system built with Lightweight Charts (by TradingView). This replaces the static Chart-IMG API with a rich, client-side charting solution.

## Features

### 1. **Interactive Candlestick Charts**
- Real-time zoom and pan
- Crosshair with price/date display
- Volume bars below price action
- Multiple timeframe support (1D, 1W, 1M)
- Responsive and mobile-friendly

### 2. **Technical Indicators**
- **EMA 21** - Fast exponential moving average
- **SMA 50** - Medium-term simple moving average
- **SMA 200** - Long-term simple moving average
- **Bollinger Bands** - Volatility bands (20-period, 2 std dev)
- **VWAP** - Volume weighted average price
- **Volume Profile** - Price-based volume distribution

Toggle indicators on/off via the toolbar dropdown menu.

### 3. **Drawing Tools**
- **Horizontal Lines** - Support/resistance levels
- **Trend Lines** - Connect swing points
- **Fibonacci Retracements** - Automatic fib levels (0, 23.6%, 38.2%, 50%, 61.8%, 78.6%, 100%)
- **Rectangle Zones** - Highlight consolidation areas

Drawings are automatically saved per ticker to localStorage.

### 4. **Pattern Annotations**
- Automatically highlight detected patterns
- Entry/stop/target markers with price labels
- Pattern labels with confidence scores
- Risk zone shading between entry and stop
- Divergence annotations
- Support/resistance level annotations
- Volume spike markers

### 5. **Chart Presets**
- **Clean** - Price action only
- **Technical** - All indicators (EMA 21, SMA 50, SMA 200, Bollinger Bands, VWAP)
- **Minervini** - Mark Minervini setup (EMA 21, SMA 50)
- **Custom** - Manually select your own indicators

### 6. **Export & Share**
- **Download PNG** - Save chart as image file
- **Copy to Clipboard** - Copy chart image directly
- **Share URL** - Generate shareable link with chart state (symbol, timeframe, indicators, preset)
- **Print** - Print-friendly format

## Architecture

### Components

```
/static/js/
├── interactive-chart.js       # Main chart component
├── chart-indicators.js        # Technical indicators calculations
├── chart-drawings.js          # Drawing tools
├── chart-annotations.js       # Pattern annotations
└── chart-integration.js       # Dashboard integration helper

/static/css/
└── interactive-chart.css      # Chart UI styling (cyberpunk theme)
```

### Backend API

**Endpoint:** `GET /api/charts/data`

**Parameters:**
- `symbol` (required) - Stock ticker symbol
- `timeframe` (optional) - Chart timeframe (1D, 1W, 1M) - default: 1D

**Response:**
```json
{
  "success": true,
  "symbol": "AAPL",
  "timeframe": "1D",
  "candles": [
    {
      "time": 1234567890,
      "open": 150.25,
      "high": 152.50,
      "low": 149.75,
      "close": 151.80
    }
  ],
  "volume": [
    {
      "time": 1234567890,
      "value": 50000000,
      "color": "#26a69a"
    }
  ],
  "meta": {
    "currency": "USD",
    "exchange": "NASDAQ",
    "instrument_type": "EQUITY"
  }
}
```

**Data Source:** Yahoo Finance API
**Caching:** 15 minutes (900 seconds)

## Usage

### Basic Usage

```javascript
// Create a new interactive chart
const chart = new InteractiveChart('chart-container', {
    symbol: 'AAPL',
    timeframe: '1D'
});

// Load data
await chart.loadData('AAPL', '1D');
```

### Dashboard Integration

The `ChartIntegration` helper provides a simple interface for the dashboard:

```javascript
// Initialize chart
await ChartIntegration.initChart('analyze-chart', 'AAPL', '1D', {
    preset: 'technical',
    patterns: [
        {
            id: 'pattern1',
            pattern_type: 'bull_flag',
            confidence: 0.85,
            entry_price: 150.00,
            stop_loss: 145.00,
            target_price: 160.00,
            timestamp: 1234567890
        }
    ]
});

// Update existing chart
await ChartIntegration.updateChart('analyze-chart', 'TSLA', '1W');

// Apply preset
ChartIntegration.applyPreset('analyze-chart', 'minervini');

// Add indicator
ChartIntegration.addIndicator('analyze-chart', 'ema21');

// Activate drawing tool
ChartIntegration.activateDrawing('analyze-chart', 'trendline');

// Export chart
await ChartIntegration.exportPNG('analyze-chart');
```

### Replacing Static Chart Images

```javascript
// Replace a static Chart-IMG URL with interactive chart
await ChartIntegration.replaceStaticChart(
    'analyze-chart',
    'https://chart-img.com/static/chart.png',
    'AAPL',
    '1D'
);
```

### Pattern Annotations

```javascript
// Add pattern annotation
chart.addPatternAnnotation({
    id: 'pattern1',
    pattern_type: 'bull_flag',
    confidence: 0.85,
    entry_price: 150.00,
    stop_loss: 145.00,
    target_price: 160.00,
    timestamp: 1234567890,
    zone_start: 1234560000,
    zone_end: 1234567890
});
```

## Technical Details

### Lightweight Charts

- **Version:** 4.1.3
- **CDN:** https://unpkg.com/lightweight-charts@4.1.3/dist/lightweight-charts.standalone.production.js
- **Docs:** https://tradingview.github.io/lightweight-charts/

### Indicator Calculations

All technical indicators are calculated client-side using standard formulas:

- **EMA:** Exponential moving average with 2/(period+1) multiplier
- **SMA:** Simple moving average
- **Bollinger Bands:** 20-period SMA ± 2 standard deviations
- **VWAP:** Cumulative (Typical Price × Volume) / Cumulative Volume
- **Volume Profile:** Price-level volume distribution

### Data Storage

- **Drawings:** Saved to `localStorage` with key `chart_drawings_{symbol}`
- **Chart Preferences:** Saved to `localStorage` with key `legend_ai_interactive_charts`
- **URL State:** Encoded as base64 JSON in query parameter `?chart=...`

## Styling

The chart UI uses the existing cyberpunk design system with:

- **Background:** `#0a0e1a` (dark blue-black)
- **Borders:** `#1a1f2e` (subtle gray-blue)
- **Primary Accent:** `#00ffff` (cyan/aqua)
- **Up Color:** `#00ff88` (neon green)
- **Down Color:** `#ff0066` (magenta/pink)
- **Font:** Inter (UI), JetBrains Mono (numbers)

## Browser Compatibility

- **Chrome/Edge:** ✅ Full support
- **Firefox:** ✅ Full support
- **Safari:** ✅ Full support
- **Mobile:** ✅ Touch gestures supported (pinch to zoom, drag to pan)

## Performance

- **Rendering:** Canvas-based (hardware accelerated)
- **Data Points:** Optimized for 200-500 candles
- **Indicators:** Client-side calculation (no backend load)
- **Caching:** 15-minute cache for market data

## Migration from Chart-IMG

The interactive charts system is designed as a drop-in replacement for Chart-IMG:

1. **Same container IDs** - Works with existing `#analyze-chart` etc.
2. **Graceful fallback** - Falls back to static images if JavaScript fails
3. **Toggle feature** - Can be disabled via `ChartIntegration.toggleInteractive(false)`
4. **API parity** - Similar timeframe naming (1D, 1W, 1M)

## Future Enhancements

Potential additions:
- [ ] More indicators (RSI, MACD, Stochastic)
- [ ] Custom indicator builder
- [ ] Alert creation on price levels
- [ ] Replay mode (time machine)
- [ ] Compare symbols overlay
- [ ] Custom color themes
- [ ] Indicator templates/strategies
- [ ] Chart layouts (save/restore entire setup)

## Troubleshooting

### Charts not loading
- Check browser console for errors
- Verify `/api/charts/data` endpoint is accessible
- Ensure Yahoo Finance API is reachable
- Check Redis cache connection

### Indicators not showing
- Verify indicator calculations have sufficient data points
- Check if timeframe has enough historical data
- Ensure indicator checkbox is checked

### Drawings not saving
- Check localStorage is enabled in browser
- Verify browser has storage quota available
- Check browser console for storage errors

### Performance issues
- Reduce number of active indicators
- Clear old drawings
- Use longer timeframes (less data points)
- Close other tabs/applications

## Support

For issues or questions:
- Check browser console for error messages
- Review network tab for API failures
- Verify data format from `/api/charts/data`
- Check Lightweight Charts documentation

## License

This interactive charts implementation uses:
- **Lightweight Charts** - Apache License 2.0
- **Yahoo Finance API** - Public API (subject to rate limits)
