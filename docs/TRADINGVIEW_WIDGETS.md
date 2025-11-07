# TradingView Widgets Documentation

This document contains all TradingView widget code used in Legend AI. Each widget is documented with its HTML/JavaScript implementation for easy reference, editing, and reuse.

---

## 1. Advanced Chart Widget

**Purpose**: Professional trading charts with technical studies (RSI, MACD, Volume, SMA, EMA)

**Files**: `app/api/dashboard.py` - `createTradingViewWidget()` function

### HTML Implementation

```html
<div class="tradingview-widget-container" style="height:100%;width:100%">
  <div class="tradingview-widget-container__widget" style="height:calc(100% - 32px);width:100%"></div>
  <div class="tradingview-widget-copyright">
    <a href="https://www.tradingview.com/symbols/{SYMBOL}/" rel="noopener nofollow" target="_blank">
      <span class="blue-text">{SYMBOL} chart</span>
    </a>
    <span class="trademark"> by TradingView</span>
  </div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
  {
    "allow_symbol_change": true,
    "calendar": false,
    "details": false,
    "hide_side_toolbar": true,
    "hide_top_toolbar": false,
    "hide_legend": false,
    "hide_volume": false,
    "hotlist": false,
    "interval": "D",
    "locale": "en",
    "save_image": true,
    "style": "1",
    "symbol": "{SYMBOL}",
    "theme": "dark",
    "timezone": "Etc/UTC",
    "backgroundColor": "#0F0F0F",
    "gridColor": "rgba(242, 242, 242, 0.06)",
    "withdateranges": false,
    "studies": [
      "STD;RSI",
      "STD;MACD",
      "Volume@tv-basicstudies",
      "STD;SMA",
      "STD;EMA"
    ],
    "autosize": true
  }
  </script>
</div>
```

### JavaScript Function (Vanilla JS)

```javascript
function createTradingViewWidget(symbol, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const tvSymbol = symbol.includes(':') ? symbol : 'NASDAQ:' + symbol;

    const widgetHTML = `
        <div class="tradingview-widget-container" style="height:100%;width:100%">
          <div class="tradingview-widget-container__widget" style="height:calc(100% - 32px);width:100%"></div>
          <div class="tradingview-widget-copyright">
            <a href="https://www.tradingview.com/symbols/${tvSymbol}/" rel="noopener nofollow" target="_blank">
              <span class="blue-text">${symbol} chart</span>
            </a>
            <span class="trademark"> by TradingView</span>
          </div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
          {
            "allow_symbol_change": true,
            "calendar": false,
            "details": false,
            "hide_side_toolbar": true,
            "hide_top_toolbar": false,
            "hide_legend": false,
            "hide_volume": false,
            "hotlist": false,
            "interval": "D",
            "locale": "en",
            "save_image": true,
            "style": "1",
            "symbol": "${tvSymbol}",
            "theme": "dark",
            "timezone": "Etc/UTC",
            "backgroundColor": "#0F0F0F",
            "gridColor": "rgba(242, 242, 242, 0.06)",
            "withdateranges": false,
            "studies": [
              "STD;RSI",
              "STD;MACD",
              "Volume@tv-basicstudies",
              "STD;SMA",
              "STD;EMA"
            ],
            "autosize": true
          }
          <\/script>
        </div>
    `;

    container.innerHTML = widgetHTML;

    // Reload the TradingView script
    const script = document.createElement('script');
    script.src = 'https://s3.tradingview.com/tv.js';
    script.async = true;
    document.body.appendChild(script);
}
```

### Usage

```javascript
// In your HTML
<div id="chart_NVDA_0"></div>

// Call the function
createTradingViewWidget('NVDA', 'chart_NVDA_0');
```

**Key Settings**:
- `interval`: "D" (daily), change to "W" (weekly), "4H", "1H" as needed
- `studies`: Array of technical studies - can add/remove as needed
- `backgroundColor`: Dark theme color (#0F0F0F)
- `theme`: "dark" or "light"

---

## 2. Ticker Tape Widget

**Purpose**: Real-time ticker showing prices and changes for major indices and assets

**Use Case**: Market header/overview section

### HTML Implementation

```html
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright">
    <a href="https://www.tradingview.com/markets/" rel="noopener nofollow" target="_blank">
      <span class="blue-text">Ticker tape</span>
    </a>
    <span class="trademark"> by TradingView</span>
  </div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
  {
    "symbols": [
      {
        "proName": "FOREXCOM:SPXUSD",
        "title": "S&P 500 Index"
      },
      {
        "proName": "FOREXCOM:NSXUSD",
        "title": "US 100 Cash CFD"
      },
      {
        "proName": "FX_IDC:EURUSD",
        "title": "EUR to USD"
      },
      {
        "proName": "BITSTAMP:BTCUSD",
        "title": "Bitcoin"
      },
      {
        "proName": "BITSTAMP:ETHUSD",
        "title": "Ethereum"
      }
    ],
    "colorTheme": "dark",
    "locale": "en",
    "largeChartUrl": "",
    "isTransparent": false,
    "showSymbolLogo": true,
    "displayMode": "adaptive"
  }
  </script>
</div>
```

### JavaScript Function (Vanilla JS)

```javascript
function createTickerTapeWidget(containerId, symbols) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const widgetHTML = `
        <div class="tradingview-widget-container">
          <div class="tradingview-widget-container__widget"></div>
          <div class="tradingview-widget-copyright">
            <a href="https://www.tradingview.com/markets/" rel="noopener nofollow" target="_blank">
              <span class="blue-text">Ticker tape</span>
            </a>
            <span class="trademark"> by TradingView</span>
          </div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
          {
            "symbols": ${JSON.stringify(symbols)},
            "colorTheme": "dark",
            "locale": "en",
            "largeChartUrl": "",
            "isTransparent": false,
            "showSymbolLogo": true,
            "displayMode": "adaptive"
          }
          <\/script>
        </div>
    `;

    container.innerHTML = widgetHTML;

    const script = document.createElement('script');
    script.src = 'https://s3.tradingview.com/tv.js';
    script.async = true;
    document.body.appendChild(script);
}
```

### Usage

```javascript
const symbols = [
  { "proName": "FOREXCOM:SPXUSD", "title": "S&P 500" },
  { "proName": "FOREXCOM:NSXUSD", "title": "NASDAQ 100" },
  { "proName": "BITSTAMP:BTCUSD", "title": "Bitcoin" }
];

createTickerTapeWidget('ticker_container', symbols);
```

**Key Settings**:
- `symbols`: Array of ticker objects (proName + title)
- `displayMode`: "adaptive", "compact", or "full"
- `showSymbolLogo`: true/false
- `colorTheme`: "dark" or "light"

---

## 3. Stock Heatmap Widget

**Purpose**: Visual heatmap of S&P 500 stocks grouped by sector, colored by price change

**Use Case**: Quick market overview, sector analysis

### HTML Implementation

```html
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright">
    <a href="https://www.tradingview.com/heatmap/stock/" rel="noopener nofollow" target="_blank">
      <span class="blue-text">Stock Heatmap</span>
    </a>
    <span class="trademark"> by TradingView</span>
  </div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-stock-heatmap.js" async>
  {
    "dataSource": "SPX500",
    "blockSize": "market_cap_basic",
    "blockColor": "change",
    "grouping": "sector",
    "locale": "en",
    "symbolUrl": "",
    "colorTheme": "dark",
    "exchanges": [],
    "hasTopBar": false,
    "isDataSetEnabled": false,
    "isZoomEnabled": true,
    "hasSymbolTooltip": true,
    "isMonoSize": false,
    "width": "100%",
    "height": "100%"
  }
  </script>
</div>
```

### JavaScript Function (Vanilla JS)

```javascript
function createStockHeatmapWidget(containerId, options = {}) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const defaultOptions = {
        "dataSource": "SPX500",
        "blockSize": "market_cap_basic",
        "blockColor": "change",
        "grouping": "sector",
        "locale": "en",
        "colorTheme": "dark",
        "isZoomEnabled": true,
        "hasSymbolTooltip": true
    };

    const config = { ...defaultOptions, ...options };

    const widgetHTML = `
        <div class="tradingview-widget-container">
          <div class="tradingview-widget-container__widget"></div>
          <div class="tradingview-widget-copyright">
            <a href="https://www.tradingview.com/heatmap/stock/" rel="noopener nofollow" target="_blank">
              <span class="blue-text">Stock Heatmap</span>
            </a>
            <span class="trademark"> by TradingView</span>
          </div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-stock-heatmap.js" async>
          ${JSON.stringify(config)}
          <\/script>
        </div>
    `;

    container.innerHTML = widgetHTML;

    const script = document.createElement('script');
    script.src = 'https://s3.tradingview.com/tv.js';
    script.async = true;
    document.body.appendChild(script);
}
```

### Usage

```javascript
// Basic usage
createStockHeatmapWidget('heatmap_container');

// With custom options
createStockHeatmapWidget('heatmap_container', {
    "grouping": "industry",  // or "sector"
    "blockSize": "market_cap_basic"  // or "price_scale"
});
```

**Key Settings**:
- `dataSource`: "SPX500", "NASDAQ100", "AllUSStocks"
- `grouping`: "sector", "industry", "country"
- `blockSize`: "market_cap_basic", "price_scale"
- `blockColor`: "change" (red/green), "volume", "range"

---

## 4. ETF Heatmap Widget

**Purpose**: Visual heatmap of ETFs, useful for sector/asset class rotation analysis

**Use Case**: Asset allocation, ETF comparison, sector rotation

### HTML Implementation

```html
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright">
    <a href="https://www.tradingview.com/heatmap/etf/" rel="noopener nofollow" target="_blank">
      <span class="blue-text">ETF Heatmap</span>
    </a>
    <span class="trademark"> by TradingView</span>
  </div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-etf-heatmap.js" async>
  {
    "dataSource": "AllUSEtf",
    "blockSize": "volume",
    "blockColor": "change",
    "grouping": "asset_class",
    "locale": "en",
    "symbolUrl": "",
    "colorTheme": "dark",
    "hasTopBar": false,
    "isDataSetEnabled": false,
    "isZoomEnabled": true,
    "hasSymbolTooltip": true,
    "isMonoSize": false,
    "width": "100%",
    "height": "100%"
  }
  </script>
</div>
```

### JavaScript Function (Vanilla JS)

```javascript
function createETFHeatmapWidget(containerId, options = {}) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const defaultOptions = {
        "dataSource": "AllUSEtf",
        "blockSize": "volume",
        "blockColor": "change",
        "grouping": "asset_class",
        "locale": "en",
        "colorTheme": "dark",
        "isZoomEnabled": true,
        "hasSymbolTooltip": true
    };

    const config = { ...defaultOptions, ...options };

    const widgetHTML = `
        <div class="tradingview-widget-container">
          <div class="tradingview-widget-container__widget"></div>
          <div class="tradingview-widget-copyright">
            <a href="https://www.tradingview.com/heatmap/etf/" rel="noopener nofollow" target="_blank">
              <span class="blue-text">ETF Heatmap</span>
            </a>
            <span class="trademark"> by TradingView</span>
          </div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-etf-heatmap.js" async>
          ${JSON.stringify(config)}
          <\/script>
        </div>
    `;

    container.innerHTML = widgetHTML;

    const script = document.createElement('script');
    script.src = 'https://s3.tradingview.com/tv.js';
    script.async = true;
    document.body.appendChild(script);
}
```

### Usage

```javascript
// Basic usage
createETFHeatmapWidget('etf_heatmap_container');

// With custom options
createETFHeatmapWidget('etf_heatmap_container', {
    "grouping": "asset_class",  // or "country", "currency"
    "blockSize": "volume"  // or "market_cap_basic"
});
```

**Key Settings**:
- `dataSource`: "AllUSEtf", "AllWorldEtf"
- `grouping`: "asset_class", "country", "currency", "issuer"
- `blockSize`: "volume", "market_cap_basic", "price_scale"
- `blockColor`: "change", "volume", "range"

---

## 5. Stock Screener Widget

**Purpose**: Full-featured stock screener with filtering, sorting, and analysis capabilities

**Use Case**: Alternative to native universe scan, stock discovery

### HTML Implementation

```html
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright">
    <a href="https://www.tradingview.com/screener/" rel="noopener nofollow" target="_blank">
      <span class="blue-text">Stock Screener</span>
    </a>
    <span class="trademark"> by TradingView</span>
  </div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-screener.js" async>
  {
    "market": "america",
    "showToolbar": true,
    "defaultColumn": "overview",
    "defaultScreen": "top_gainers",
    "isTransparent": false,
    "locale": "en",
    "colorTheme": "dark",
    "width": "100%",
    "height": 550
  }
  </script>
</div>
```

### JavaScript Function (Vanilla JS)

```javascript
function createStockScreenerWidget(containerId, options = {}) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const defaultOptions = {
        "market": "america",
        "showToolbar": true,
        "defaultColumn": "overview",
        "defaultScreen": "top_gainers",
        "isTransparent": false,
        "locale": "en",
        "colorTheme": "dark",
        "width": "100%",
        "height": 550
    };

    const config = { ...defaultOptions, ...options };

    const widgetHTML = `
        <div class="tradingview-widget-container">
          <div class="tradingview-widget-container__widget"></div>
          <div class="tradingview-widget-copyright">
            <a href="https://www.tradingview.com/screener/" rel="noopener nofollow" target="_blank">
              <span class="blue-text">Stock Screener</span>
            </a>
            <span class="trademark"> by TradingView</span>
          </div>
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-screener.js" async>
          ${JSON.stringify(config)}
          <\/script>
        </div>
    `;

    container.innerHTML = widgetHTML;

    const script = document.createElement('script');
    script.src = 'https://s3.tradingview.com/tv.js';
    script.async = true;
    document.body.appendChild(script);
}
```

### Usage

```javascript
// Basic usage
createStockScreenerWidget('screener_container');

// With custom options
createStockScreenerWidget('screener_container', {
    "market": "america",
    "defaultScreen": "top_losers",
    "height": 700
});
```

**Key Settings**:
- `market`: "america", "europe", "asia", etc.
- `defaultScreen`: "top_gainers", "top_losers", "most_active", "earnings", etc.
- `defaultColumn`: "overview", "performance", "technicals", "fundamentals"
- `showToolbar`: true/false (enable filters)

---

## Integration Guide

### Adding to Dashboard

```javascript
// 1. Create container divs in HTML
<div id="ticker_container" style="height: 60px; margin-bottom: 20px;"></div>
<div id="stock_heatmap" style="height: 600px; margin-bottom: 20px;"></div>
<div id="etf_heatmap" style="height: 600px; margin-bottom: 20px;"></div>
<div id="screener_container" style="height: 700px;"></div>

// 2. Call widget functions on page load
window.addEventListener('DOMContentLoaded', function() {
    createTickerTapeWidget('ticker_container', symbols);
    createStockHeatmapWidget('stock_heatmap');
    createETFHeatmapWidget('etf_heatmap');
    createStockScreenerWidget('screener_container');
});
```

### Responsive Design

All widgets automatically resize to container dimensions:

```css
.widget-container {
    width: 100%;
    height: 600px;
    margin-bottom: 20px;
}

@media (max-width: 768px) {
    .widget-container {
        height: 400px;
    }
}
```

---

## Performance Notes

- **Lazy Loading**: Load widgets only when needed (tabs, modals)
- **Script Caching**: TradingView's script (`tv.js`) is cached by browser
- **Multiple Instances**: Each container creates a new widget instance
- **Reload**: Call the function again to replace widget with updated config

---

## References

- [TradingView Advanced Chart Docs](https://www.tradingview.com/pine-script-docs/)
- [TradingView Embedding Docs](https://www.tradingview.com/widget-docs/)
- [TradingView API Reference](https://www.tradingview.com/charting_library_docs/)

---

**Last Updated**: 2025-11-07
**Status**: Production Ready
