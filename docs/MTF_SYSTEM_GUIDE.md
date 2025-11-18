# Comprehensive Multi-Timeframe (MTF) Trading System

## Overview

The Comprehensive MTF Trading System is an advanced multi-timeframe analysis framework that provides traders with a complete view of market conditions across multiple timeframes, from Monthly down to 1-Hour charts.

## Features

### 1. **Timeframe Alignment Analysis**
- Analyzes 5 timeframes: Monthly (1M), Weekly (1W), Daily (1D), 4-Hour (4H), 1-Hour (1H)
- Detects when all timeframes align (bullish or bearish)
- Identifies conflicts between higher and lower timeframes
- Weighted scoring (Monthly: 30%, Weekly: 25%, Daily: 20%, 4H: 15%, 1H: 10%)

### 2. **MTF Dashboard**
- **Side-by-side charts** with all timeframes
- **Indicator table** showing SMA50, SMA200, RSI, MACD across all timeframes
- **Pattern summary** displaying detected patterns on each timeframe
- **Recommendation engine** providing actionable trading advice

### 3. **MTF Scoring System (0-10 scale)**
- **10/10**: All timeframes bullish with strong trends
- **8-9/10**: Strong alignment, minor conflicts
- **6-7/10**: Good alignment, some mixed signals
- **4-5/10**: Mixed signals, neutral
- **2-3/10**: Poor alignment, conflicting signals
- **0-1/10**: All timeframes bearish

**Score Components**:
- Trend Alignment (40% weight)
- Momentum Indicators (25% weight)
- Volume Confirmation (20% weight)
- Pattern Quality (15% weight)

### 4. **Entry Timing Optimization**
- **Higher timeframes (Daily, Weekly, Monthly)** determine DIRECTION
- **Lower timeframes (4H, 1H)** determine ENTRY TIMING
- Optimizes entry on pullbacks to support (in uptrends) or rallies to resistance (in downtrends)
- Risk:Reward ratio calculation
- Confidence scoring based on alignment

### 5. **Divergence Detection**
- Detects bullish and bearish divergences (price vs RSI)
- Cross-timeframe divergence analysis
- Severity classification (Strong, Moderate, Weak)
- Regular and hidden divergences

### 6. **Alignment Alerts**
- **All Timeframes Bullish** → Strong Buy signal
- **All Timeframes Bearish** → Strong Sell signal
- **Higher/Lower TF Agreement** → Confluence confirmation
- **Divergence Alerts** → Potential reversal warnings
- **Entry Signal Alerts** → High-confidence entry opportunities

## Architecture

### Core Modules

```
app/core/
├── mtf_analyzer.py          # Timeframe analysis and divergence detection
├── mtf_scoring.py           # Scoring engine (0-10 scale)
├── mtf_entry_timing.py      # Entry timing optimization
├── mtf_dashboard.py         # Dashboard generation
└── mtf_alerts.py            # Alert system

app/services/
└── mtf_comprehensive.py     # Comprehensive MTF service (integrates all modules)

app/api/
├── multitimeframe.py        # Basic MTF API (legacy)
└── mtf_comprehensive.py     # Comprehensive MTF API
```

### Data Flow

```
1. Fetch OHLCV data for all timeframes
   ↓
2. Analyze each timeframe individually
   (Trend, RSI, MACD, Volume, S/R levels)
   ↓
3. Calculate alignment across timeframes
   ↓
4. Detect divergences
   ↓
5. Calculate MTF score (0-10)
   ↓
6. Optimize entry timing
   ↓
7. Generate dashboard
   ↓
8. Generate alerts
   ↓
9. Return comprehensive result
```

## API Endpoints

### Primary Endpoint

**POST /api/mtf/analyze**

Comprehensive MTF analysis with full dashboard, scoring, and alerts.

```json
{
  "ticker": "NVDA",
  "previous_score": null,
  "include_dashboard": true
}
```

**Response:**
```json
{
  "success": true,
  "ticker": "NVDA",
  "mtf_score": 8.5,
  "score_category": "Excellent",
  "trade_recommendation": "Strong Buy",
  "alignment_type": "All Bullish",
  "is_aligned": true,
  "bullish_timeframes": ["1M", "1W", "1D", "4H", "1H"],
  "bearish_timeframes": [],
  "entry_signal": "buy",
  "entry_confidence": 0.85,
  "optimal_entry_tf": "1H",
  "total_alerts": 3,
  "high_priority_alerts": 2,
  "alerts": [...],
  "dashboard": "...",
  "full_report": "..."
}
```

### Quick Analysis

**GET /api/mtf/analyze/{ticker}**

Quick MTF analysis (shorthand for POST endpoint).

```bash
curl http://localhost:8000/api/mtf/analyze/NVDA
```

### Dashboard Only

**POST /api/mtf/dashboard**

Returns formatted dashboard text only.

### Alerts Only

**POST /api/mtf/alerts**

Returns alerts only.

### Score Only

**POST /api/mtf/score**

Returns MTF score and breakdown only.

### Entry Timing Only

**POST /api/mtf/entry-timing**

Returns entry timing analysis only.

### Full Report

**GET /api/mtf/report/{ticker}?format=text**

Returns complete text report.

## Usage Examples

### Example 1: Basic Analysis

```python
from app.services.mtf_comprehensive import get_comprehensive_mtf_service

service = get_comprehensive_mtf_service()
result = await service.analyze_comprehensive("NVDA")

print(f"MTF Score: {result.mtf_score.overall_score}/10")
print(f"Recommendation: {result.trade_recommendation}")
print(f"Alignment: {result.alignment.alignment_type}")
```

### Example 2: Entry Timing

```python
result = await service.analyze_comprehensive("AAPL")
signal = result.entry_timing.current_signal

if signal.signal_type == "buy":
    print(f"LONG Entry: ${signal.entry_price:.2f}")
    print(f"Stop Loss: ${signal.stop_loss:.2f}")
    print(f"Take Profit: ${signal.take_profit:.2f}")
    print(f"R:R = {signal.risk_reward_ratio:.2f}")
```

### Example 3: Scan Multiple Stocks

```python
watchlist = ["NVDA", "AAPL", "MSFT", "TSLA"]
results = []

for ticker in watchlist:
    result = await service.analyze_comprehensive(ticker)
    results.append({
        "ticker": ticker,
        "score": result.mtf_score.overall_score,
        "signal": result.entry_timing.current_signal.signal_type
    })

# Sort by score
results.sort(key=lambda x: x["score"], reverse=True)

# Best setup
best = results[0]
print(f"Best setup: {best['ticker']} ({best['score']}/10)")
```

### Example 4: Dashboard Display

```python
result = await service.analyze_comprehensive("TSLA")
dashboard = service.dashboard_generator.format_dashboard_text(result.dashboard)
print(dashboard)
```

### Example 5: Alert Monitoring

```python
result = await service.analyze_comprehensive("SPY")

# Filter critical alerts
critical_alerts = [
    a for a in result.alerts
    if a.severity.value in ["critical", "high"]
]

for alert in critical_alerts:
    print(f"{alert.title}")
    print(f"{alert.message}")
    print(f"Action: {alert.suggested_action}")
```

## Scoring Logic

### Component Scores

**Trend Alignment (0-10)**
- All timeframes up: 10
- Most timeframes up: 7-9
- Mixed: 4-6
- Most timeframes down: 1-3
- All timeframes down: 0

**Momentum (0-10)**
- RSI 50-70 + MACD positive: 8-10
- RSI 40-50 + MACD positive: 6-8
- RSI < 40 or > 70: 3-6
- Bearish momentum: 0-3

**Volume (0-10)**
- Increasing volume on uptrend: 8-10
- Decreasing volume on uptrend: 4-6
- Increasing volume on downtrend: 0-3

**Pattern Quality (0-10)**
- High-confidence pattern detected: 8-10
- Moderate-confidence pattern: 5-7
- No pattern or low confidence: 3-5

### Overall Score Calculation

```
Overall = (
    Trend Alignment × 0.40 +
    Momentum × 0.25 +
    Volume × 0.20 +
    Pattern Quality × 0.15
) + Divergence Adjustment (-3 to +3)
```

## Alert System

### Alert Types

1. **Alignment Alerts**
   - All timeframes bullish
   - All timeframes bearish
   - Higher/Lower TF agreement

2. **Divergence Alerts**
   - Bullish divergence detected
   - Bearish divergence detected
   - Cross-timeframe divergences

3. **Entry Signal Alerts**
   - High-confidence long entry
   - High-confidence short entry

4. **Score Alerts**
   - Score reaches "Excellent" (≥ 8.5)
   - Score drops to "Poor" (< 4.0)
   - Significant score change (± 2.0)

### Alert Severity

- **Critical**: All timeframes aligned, high-confidence entries
- **High**: Strong alignment, significant divergences
- **Medium**: Partial alignment, moderate signals
- **Low**: Minor signals, weak divergences
- **Info**: General information

## Interpretation Guide

### Score Interpretation

| Score | Category | Interpretation | Action |
|-------|----------|----------------|--------|
| 9.0-10.0 | Excellent | All timeframes bullish, strong setup | Strong Buy |
| 7.5-8.9 | Good | Most timeframes aligned, quality setup | Buy |
| 5.5-7.4 | Fair | Some alignment, mixed signals | Hold/Wait |
| 3.0-5.4 | Poor | Conflicting signals, low confidence | Avoid |
| 0.0-2.9 | Very Poor | Bearish alignment, avoid longs | Sell/Short |

### Alignment Interpretation

- **All Bullish**: All 5 timeframes trending up → Strong buy signal
- **Mostly Bullish**: 4/5 timeframes up → Buy signal, watch the outlier
- **Mixed Bullish**: 3/5 timeframes up → Cautious buy, wait for confirmation
- **Mixed Bearish**: 3/5 timeframes down → Cautious sell
- **Mostly Bearish**: 4/5 timeframes down → Sell signal
- **All Bearish**: All 5 timeframes down → Strong sell signal

### Entry Timing Strategy

1. **Determine Direction** from higher timeframes (Daily, Weekly, Monthly)
2. **Wait for Pullback** on lower timeframes (4H, 1H)
3. **Enter on Support** (for longs) or **Resistance** (for shorts)
4. **Confirm with Volume** and pattern signals
5. **Set Stops** based on S/R levels
6. **Target** next resistance (longs) or support (shorts)

## Best Practices

### 1. Multi-Timeframe Confluence
- Always check higher timeframe trend before entering
- Don't fight the higher timeframe trend
- Use lower timeframes for precision entries only

### 2. Risk Management
- Only take trades with R:R ≥ 1.5
- Position size based on stop distance
- Honor stops - don't move them wider

### 3. Entry Timing
- Wait for alignment (score ≥ 7.0 preferred)
- Enter on pullbacks in direction of trend
- Confirm with volume and patterns

### 4. Alert Usage
- Monitor critical/high alerts
- Act on alignment alerts (all timeframes)
- Watch divergence alerts for reversals
- Use entry signal alerts for timing

### 5. Scanning Workflow
- Scan watchlist for scores ≥ 7.0
- Check alignment type (prefer "All Bullish")
- Review entry timing and R:R
- Confirm with dashboard indicators
- Execute on high-confidence setups

## Performance Considerations

- First analysis may take 5-10 seconds (data fetching)
- Subsequent analyses are faster (cached data)
- Use `/score` or `/alerts` endpoints for quick checks
- Full dashboard generation adds 1-2 seconds

## Troubleshooting

**Issue**: "No data available for timeframe"
- Solution: Some stocks don't have intraday data (4H, 1H). Use `/analyze` endpoint which handles this gracefully.

**Issue**: "MTF score is always 5.0"
- Solution: All timeframes are sideways/neutral. Wait for trend development.

**Issue**: "Entry signal is always 'wait'"
- Solution: No clear entry setup. Stock may be mid-move or no pullback yet.

## Future Enhancements

- [ ] Support for additional timeframes (15min, 30min)
- [ ] Custom timeframe weights
- [ ] Backtesting integration
- [ ] Alert delivery (email, SMS, Telegram)
- [ ] Chart image generation
- [ ] Historical score tracking
- [ ] Machine learning score optimization

## References

- Original MTF Service: `app/services/multitimeframe.py`
- Basic MTF API: `app/api/multitimeframe.py`
- Example Usage: `examples/mtf_comprehensive_example.py`
- API Documentation: `/docs` (when server is running)

---

**Last Updated**: 2025-01-18
**Version**: 2.0
**Author**: Legend AI Trading System
