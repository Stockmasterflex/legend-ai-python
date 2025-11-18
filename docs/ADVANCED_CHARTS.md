# Advanced Charting Components Documentation

## Overview

The Legend AI Advanced Charting system provides professional-grade technical analysis tools with custom chart types, interactive annotations, indicators, and backtesting capabilities.

## Features

### 1. Custom Chart Types

#### Renko Charts
- **Description**: Price movement charts that filter out time and focus on significant price changes
- **Use Case**: Identify trends and filter market noise
- **Configuration**:
  - `brickSize`: Fixed size or 'ATR' for automatic sizing
  - `atrPeriod`: Period for ATR calculation (default: 14)

**Example**:
```javascript
const renkoChart = new RenkoChart('container-id', {
    brickSize: 'ATR',
    atrPeriod: 14,
    upColor: '#00ff41',
    downColor: '#ff0050'
});
renkoChart.setData(ohlcvData);
```

#### Kagi Charts
- **Description**: Japanese charting technique emphasizing trend reversals
- **Use Case**: Identify trend changes and support/resistance levels
- **Configuration**:
  - `reversalAmount`: Fixed percentage or 'ATR'
  - `reversalPercentage`: Percentage for reversals (default: 4%)

**Example**:
```javascript
const kagiChart = new KagiChart('container-id', {
    reversalAmount: 'ATR',
    reversalPercentage: 4.0,
    thickColor: '#00ff41',
    thinColor: '#ff0050'
});
```

#### Point & Figure Charts
- **Description**: X and O charts filtering minor price movements
- **Use Case**: Long-term trend analysis and pattern recognition
- **Configuration**:
  - `boxSize`: Fixed size or 'ATR'
  - `reversalBoxes`: Number of boxes for reversal (default: 3)

**Example**:
```javascript
const pfChart = new PointFigureChart('container-id', {
    boxSize: 'ATR',
    reversalBoxes: 3,
    xColor: '#00ff41',
    oColor: '#ff0050'
});
```

#### Market Profile Charts
- **Description**: Shows price distribution over time using TPO (Time Price Opportunity)
- **Use Case**: Identify value areas and trading ranges
- **Configuration**:
  - `tickSize`: Price increment (default: 0.5)
  - `timePerLetter`: Minutes per TPO letter (default: 30)
  - `valueAreaPercent`: Percentage for value area (default: 70%)

**Example**:
```javascript
const mpChart = new MarketProfileChart('container-id', {
    tickSize: 0.5,
    timePerLetter: 30,
    valueAreaPercent: 70,
    showValueArea: true
});
```

#### Footprint Charts
- **Description**: Shows bid/ask volume at each price level within candles
- **Use Case**: Order flow analysis and volume profiling
- **Configuration**:
  - `tickSize`: Price level increment (default: 0.1)
  - `showDelta`: Display delta (buy - sell volume)
  - `showImbalance`: Highlight volume imbalances

**Example**:
```javascript
const footprintChart = new FootprintChart('container-id', {
    tickSize: 0.1,
    showDelta: true,
    showImbalance: true,
    imbalanceRatio: 1.5
});
```

### 2. Interactive Annotations

#### Trend Lines
```javascript
const annotationManager = new AnnotationManager(chart);

// Draw trend line
annotationManager.setTool('trendline');
// User clicks start and end points

// Programmatically add trend line
annotationManager.addTrendLine(
    { price: 100, time: timestamp1 },
    { price: 120, time: timestamp2 },
    { color: '#00ff41', width: 2, style: 'solid', extend: false }
);
```

#### Fibonacci Tools
```javascript
// Add Fibonacci retracement
annotationManager.addFibonacci(
    { price: 100, time: timestamp1 },
    { price: 150, time: timestamp2 },
    {
        levels: [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0],
        showLabels: true,
        colors: {
            0.618: '#00ff00',
            0.5: '#ffff00',
            0.382: '#ff8000'
        }
    }
);
```

#### Harmonic Patterns
```javascript
const patternDetector = new HarmonicPatternDetector();

// Auto-detect patterns
const patterns = patternDetector.detectPatterns(priceData);

// Draw detected patterns
const harmonicAnnotation = new HarmonicPatternAnnotation(annotationManager);
patterns.forEach(pattern => harmonicAnnotation.drawPattern(pattern));
```

Supported patterns:
- Gartley
- Butterfly
- Bat
- Crab
- Shark
- Cypher

### 3. Custom Indicator Builder

#### Built-in Indicators
- SMA (Simple Moving Average)
- EMA (Exponential Moving Average)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- ATR (Average True Range)
- Stochastic Oscillator
- ADX (Average Directional Index)
- OBV (On Balance Volume)

#### Using Built-in Indicators
```javascript
const indicatorBuilder = new IndicatorBuilder();

// Calculate SMA
const sma = indicatorBuilder.builtInIndicators.SMA.calculate(data, 20);

// Calculate RSI
const rsi = indicatorBuilder.builtInIndicators.RSI.calculate(data, 14);

// Calculate MACD
const macd = indicatorBuilder.builtInIndicators.MACD.calculate(data, 12, 26, 9);
// Returns: { macd, signal, histogram }
```

#### Creating Custom Indicators
```javascript
// Create custom indicator with formula
const customIndicator = indicatorBuilder.createCustomIndicator(
    'MyCustomIndicator',
    'SMA(close, 20) > SMA(close, 50)',  // Formula
    { period1: 20, period2: 50 }         // Parameters
);

// Evaluate formula
const result = indicatorBuilder.evaluateFormula(
    'RSI(close, 14) > 70',
    data,
    { period: 14 }
);
```

#### Combining Indicators
```javascript
const combined = indicatorBuilder.combineIndicators(
    [
        { values: rsi },
        { values: macd.histogram }
    ],
    'AND'  // 'AND', 'OR', or custom function
);
```

### 4. Alert System

#### Creating Alerts
```javascript
const alertSystem = new AlertSystem();

// Price cross alert
alertSystem.createPriceCrossAlert('AAPL', 150, 'above');

// RSI alert
alertSystem.createRSIAlert(70, 'above');

// Indicator cross alert
alertSystem.createIndicatorCrossAlert(
    'MA Crossover',
    'SMA-20',
    'SMA-50',
    'above'
);

// Custom alert with formula
alertSystem.createFormulaAlert(
    'Custom Alert',
    'RSI(data, 14) > 70 && close > SMA(data, 20)',
    'RSI overbought and price above SMA'
);
```

#### Managing Alerts
```javascript
// Start automatic checking
alertSystem.startAutoCheck(dataProvider, 5000);  // Check every 5 seconds

// Set notification callback
alertSystem.setNotificationCallback((alertEvent) => {
    console.log('Alert triggered:', alertEvent.message);
    // Custom notification handling
});

// Get all alerts
const alerts = alertSystem.getAllAlerts();

// Delete alert
alertSystem.deleteAlert(alertId);
```

### 5. Strategy Backtesting

#### Creating a Strategy
```javascript
const backtestEngine = new BacktestingEngine();

// Define strategy
const strategy = backtestEngine.createStrategy({
    name: 'MA Crossover',

    // Entry condition
    entryCondition: (context) => {
        const sma20 = context.indicators.SMA_20;
        const sma50 = context.indicators.SMA_50;

        if (!sma20 || !sma50) return false;

        const current20 = sma20[sma20.length - 1];
        const current50 = sma50[sma50.length - 1];
        const prev20 = sma20[sma20.length - 2];
        const prev50 = sma50[sma50.length - 2];

        // Bullish crossover
        return prev20 <= prev50 && current20 > current50;
    },

    // Exit condition
    exitCondition: (context) => {
        const sma20 = context.indicators.SMA_20;
        const sma50 = context.indicators.SMA_50;

        const current20 = sma20[sma20.length - 1];
        const current50 = sma50[sma50.length - 1];

        // Exit on bearish crossover
        return current20 < current50;
    },

    stopLoss: 2,      // 2% stop loss
    takeProfit: 5,    // 5% take profit
    positionSize: 100, // 100% of capital
    maxPositions: 1
});
```

#### Running Backtest
```javascript
const results = backtestEngine.runBacktest(
    'MA Crossover',
    historicalData,
    10000,  // Initial capital
    {
        commission: 0.001,  // 0.1% commission
        indicators: {
            SMA_20: indicatorBuilder.calculateSMA(historicalData, 20),
            SMA_50: indicatorBuilder.calculateSMA(historicalData, 50)
        }
    }
);

// Generate report
const report = backtestEngine.generateReport('MA Crossover');

console.log('Total Return:', report.summary.totalReturnPercent);
console.log('Win Rate:', report.summary.winRate);
console.log('Profit Factor:', report.summary.profitFactor);
console.log('Max Drawdown:', report.summary.maxDrawdown);
```

### 6. Performance Optimization

#### WebGL Rendering
```javascript
// For large datasets (1M+ points)
const webglRenderer = new WebGLRenderer(canvas);

// Render line chart
webglRenderer.renderLine(dataPoints, viewport, [0, 1, 0.25, 1]);

// Render candlesticks
webglRenderer.renderCandles(candles, viewport);
```

#### Data Decimation
```javascript
// Largest Triangle Three Buckets algorithm
const decimated = DataDecimator.decimate(largeDataset, 1000);

// Min-Max downsampling (preserves extremes)
const downsampled = DataDecimator.minMaxDownsample(data, 10);
```

#### Lazy Loading
```javascript
const lazyLoader = new LazyDataLoader(dataProvider, 500);

// Load data for viewport
const viewportData = await lazyLoader.getViewportData(0, 100);

// Prefetch next range
await lazyLoader.prefetch(100, 200, 'forward');
```

### 7. Export Capabilities

#### High-Resolution Images
```javascript
const exporter = new ChartExportManager(chart);

// Export as PNG
await exporter.downloadPNG('chart.png', 2);  // 2x scale

// Export as JPG
await exporter.downloadJPG('chart.jpg', 2, 0.95);  // 2x scale, 95% quality

// Export as SVG
await exporter.downloadSVG('chart.svg');
```

#### PDF Export
```javascript
// Export as PDF (requires jsPDF library)
await exporter.exportPDF('chart.pdf', {
    orientation: 'landscape',
    format: 'a4',
    title: 'Trading Chart Analysis',
    metadata: {
        'Symbol': 'AAPL',
        'Timeframe': '1H',
        'Date': new Date().toLocaleDateString()
    }
});
```

#### Video Recording
```javascript
// Start recording
const recording = exporter.startRecording({
    fps: 30,
    bitrate: 2500000
});

// ... user interacts with chart ...

// Stop recording
recording.stop();  // Automatically downloads video
```

## API Endpoints

### Chart Data Endpoints

#### Get OHLCV Data
```
POST /api/charts/data/ohlcv
```

Request:
```json
{
  "symbol": "AAPL",
  "timeframe": "1h",
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "limit": 500
}
```

#### Get Renko Chart Data
```
POST /api/charts/data/renko
```

Request:
```json
{
  "symbol": "AAPL",
  "timeframe": "1h",
  "brick_size": null,
  "atr_period": 14,
  "limit": 500
}
```

#### Calculate Indicator
```
POST /api/charts/indicators/calculate
```

Request:
```json
{
  "symbol": "AAPL",
  "timeframe": "1h",
  "indicator": "RSI",
  "parameters": {
    "period": 14
  },
  "limit": 500
}
```

#### Run Backtest
```
POST /api/charts/backtest/run
```

Request:
```json
{
  "symbol": "AAPL",
  "timeframe": "1h",
  "strategy_config": {
    "name": "MA Cross",
    "entry": "SMA(20) > SMA(50)",
    "exit": "SMA(20) < SMA(50)",
    "stop_loss": 2,
    "take_profit": 5
  },
  "start_date": "2023-01-01",
  "end_date": "2024-01-01",
  "initial_capital": 10000
}
```

## Complete Example

```javascript
// Initialize chart UI
const chartUI = new ChartUIController('chart-container');

// Load data
await chartUI.loadChart('AAPL', '1h');

// Switch to Renko chart
chartUI.currentChartType = 'renko';
chartUI.updateChart();

// Add indicators
const indicatorBuilder = new IndicatorBuilder();
const sma = indicatorBuilder.builtInIndicators.SMA.calculate(chartUI.data, 20);
chartUI.currentChart.addIndicator({ name: 'SMA-20', values: sma });

// Create alert
const alertSystem = new AlertSystem();
alertSystem.createPriceCrossAlert('AAPL', 150, 'above');

// Draw annotations
const annotationManager = new AnnotationManager(chartUI.currentChart);
annotationManager.setTool('trendline');

// Detect harmonic patterns
const patternDetector = new HarmonicPatternAnnotation(annotationManager);
const patterns = patternDetector.autoDetect(chartUI.data);

// Run backtest
const backtestEngine = new BacktestingEngine();
backtestEngine.createStrategy({
    name: 'Test Strategy',
    entryCondition: (ctx) => true,
    exitCondition: (ctx) => false
});
const results = backtestEngine.runBacktest('Test Strategy', chartUI.data, 10000);

// Export chart
const exporter = new ChartExportManager(chartUI.currentChart);
await exporter.downloadPNG('aapl_chart.png', 2);
```

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Dependencies

### Required
- None (pure vanilla JavaScript)

### Optional (for enhanced features)
- **jsPDF**: PDF export functionality
- **SheetJS**: Excel export functionality

## Performance Tips

1. **Use WebGL for large datasets**: Switch to WebGL rendering for 100k+ data points
2. **Enable data decimation**: Automatically reduce data based on zoom level
3. **Lazy load historical data**: Load data on-demand as user pans
4. **Limit concurrent indicators**: Each indicator adds processing overhead
5. **Optimize annotation rendering**: Use Canvas instead of SVG for many annotations

## Troubleshooting

### Chart not rendering
- Check browser console for errors
- Ensure container element exists
- Verify data format matches expected OHLCV structure

### Performance issues
- Enable data decimation
- Reduce number of visible candles
- Switch to WebGL rendering
- Disable real-time updates during heavy interactions

### Export failures
- Check browser permissions for downloads
- Ensure required libraries (jsPDF) are loaded
- Verify sufficient memory for large exports

## License

MIT License - See LICENSE file for details

## Support

For issues and feature requests, please visit:
https://github.com/Stockmasterflex/legend-ai-python/issues
