# Market Patterns & Seasonality Analysis Guide

## Overview

The Market Seasonality Analysis module provides comprehensive analysis of historical patterns and seasonality effects in financial markets. This powerful tool helps traders and analysts identify:

- **Seasonal Patterns**: Best/worst months, quarters, weeks, and days for trading
- **Election Cycles**: Presidential election cycle effects on market performance
- **Options Expiration**: OPEX week patterns and triple witching effects
- **Earnings Season**: Quarterly earnings patterns and drift analysis
- **Market Cycles**: Bull/bear regime detection and transition analysis

## Features

### 1. Seasonal Patterns Analysis

Analyzes historical performance across different time periods:

#### Monthly Analysis
- Identifies best and worst performing months
- Calculates average returns, volatility, and win rates for each month
- Ranks current month against historical performance
- Example: "April is historically the strongest month with 1.5% average return"

#### Quarterly Analysis
- Q1, Q2, Q3, Q4 performance comparison
- Seasonal strength indicators
- Current quarter ranking

#### Week of Month Analysis
- Analyzes performance by week (1st week, 2nd week, etc.)
- Identifies patterns like "first week of month" strength

#### Day of Week Analysis
- Monday through Friday performance patterns
- Example: "Monday shows below-average returns, Friday shows above-average"

### 2. Election Cycle Analysis

Presidential election cycles have historically influenced market performance:

#### Cycle Phases
- **Year 1 (Post-Election)**: Typically weakest year, market adjusts to new policies
- **Year 2 (Mid-Term)**: Below-average performance, mid-term election uncertainty
- **Year 3 (Pre-Election)**: Historically strongest year, policy stimulus
- **Year 4 (Election Year)**: Above-average, market optimism

#### Features
- Current phase detection
- Historical performance by phase
- Policy impact scoring
- Pre/post election pattern detection

### 3. Options Expiration Effects

Analysis of options expiration (OPEX) impact on markets:

#### Features
- Next OPEX date calculation (3rd Friday)
- Triple witching detection (March, June, September, December)
- Pre-OPEX drift analysis
- Post-OPEX performance patterns
- Pin risk calculation at strike levels
- Max pain price estimation
- Gamma exposure analysis

#### Patterns
- **Bullish Pre-OPEX**: Market tends to drift higher before expiration
- **Bearish Post-OPEX**: Weakness after expiration
- **Elevated Volatility**: Increased volatility during OPEX week

### 4. Earnings Season Analysis

Quarterly earnings season effects:

#### Seasons
- **Q4 Earnings**: January-February reporting
- **Q1 Earnings**: April-May reporting
- **Q2 Earnings**: July-August reporting
- **Q3 Earnings**: October-November reporting

#### Features
- Peak earnings week detection (typically 3-5 weeks into season)
- Pre-announcement drift analysis
- Post-earnings price action
- Sector rotation signals
- Earnings volatility premium calculation

### 5. Market Cycle Detection

Advanced regime classification and trend analysis:

#### Regime Types
- **Bull Strong**: Strong uptrend, price above MAs, high momentum
- **Bull Weak**: Uptrend but showing signs of weakness
- **Bear Strong**: Strong downtrend, distribution
- **Bear Weak**: Downtrend but showing signs of recovery
- **Accumulation**: Smart money buying, building positions
- **Distribution**: Smart money selling, reducing exposure
- **Sideways**: Range-bound, no clear trend

#### Indicators
- Bull/Bear score (-100 to +100)
- Accumulation/Distribution score (-100 to +100)
- Trend strength (0-100)
- Volatility regime (low, normal, high, extreme)
- Support and resistance levels
- Regime transition probabilities

## API Endpoints

### Complete Seasonality Analysis

**Endpoint**: `POST /api/advanced/seasonality/analyze`

**Request**:
```json
{
  "symbol": "SPY",
  "include_options_data": true,
  "include_earnings_data": true
}
```

**Response**:
```json
{
  "ticker": "SPY",
  "analysis_date": "2024-11-18T00:00:00",
  "composite_score": 67.5,
  "seasonal_patterns": {
    "best_months": [
      ["April", 1.5],
      ["July", 1.2],
      ["December", 1.1]
    ],
    "worst_months": [
      ["September", -0.5],
      ["August", -0.1],
      ["June", 0.1]
    ],
    "current_rankings": {
      "month": 4,
      "quarter": 2,
      "week": 3,
      "day": 2
    }
  },
  "election_cycle": {
    "current_phase": "year_1",
    "years_until_election": 3,
    "current_phase_performance": {
      "avg_return": 0.75,
      "volatility": 1.2
    }
  },
  "options_expiration": {
    "is_opex_week": false,
    "days_to_opex": 12,
    "is_triple_witching": false,
    "drift_pattern": "bullish_pre_bearish_post"
  },
  "market_cycle": {
    "current_regime": "bull_weak",
    "confidence": 72.5,
    "scores": {
      "bull_bear": 35.0,
      "accumulation_distribution": 15.0,
      "trend_strength": 45.0
    },
    "volatility_regime": "normal",
    "support_levels": [420.50, 415.25, 410.00],
    "resistance_levels": [430.75, 435.50, 440.00]
  },
  "insights": [
    "Historically strong month (ranked #4)",
    "Strong bull market regime (72% confidence)"
  ],
  "warnings": [
    "Post-election year - historically weakest year"
  ],
  "recommendation": {
    "overall_favorability": "bullish",
    "score": 67.5,
    "confidence": "medium"
  }
}
```

### Election Cycle Information

**Endpoint**: `GET /api/advanced/seasonality/election-cycle`

Returns current election cycle phase and historical patterns.

### Monthly Patterns

**Endpoint**: `GET /api/advanced/seasonality/monthly-patterns`

Returns historical monthly performance patterns with insights.

## Python Usage

### Basic Usage

```python
from app.core.market_seasonality import MarketSeasonalityAnalyzer
from datetime import datetime

# Initialize analyzer
analyzer = MarketSeasonalityAnalyzer()

# Prepare data
price_data = {
    "c": closes,  # List of closing prices
    "h": highs,   # List of high prices
    "l": lows,    # List of low prices
    "v": volumes  # List of volumes
}

dates = [...]  # List of datetime objects

# Run complete analysis
report = await analyzer.analyze_complete_seasonality(
    ticker="SPY",
    price_data=price_data,
    dates=dates,
    current_date=datetime.now()
)

# Access results
print(f"Composite Score: {report.composite_score}")
print(f"Current Regime: {report.market_cycle.current_regime}")
print(f"Best Months: {report.seasonal_patterns.best_months}")
print(f"Insights: {report.key_insights}")
print(f"Warnings: {report.warnings}")
```

### Individual Analyses

```python
# Seasonal patterns only
seasonal = analyzer.analyze_seasonal_patterns(closes, dates, datetime.now())
print(f"Best performing month: {seasonal.best_months[0]}")

# Election cycle only
election = analyzer.analyze_election_cycle(closes, dates, datetime.now())
print(f"Current phase: {election.current_phase}")

# Options expiration only
options = analyzer.analyze_options_expiration(closes, dates, datetime.now())
print(f"Days to OPEX: {options.days_to_opex}")

# Market cycle only
cycle = analyzer.detect_market_cycle(closes, highs, lows, volumes, dates, datetime.now())
print(f"Regime: {cycle.current_regime}")
```

## Use Cases

### 1. Timing Market Entry/Exit

Use seasonal patterns to identify optimal entry points:

```python
# Check if current month is historically strong
if seasonal.current_month_rank <= 4:
    print("Favorable seasonal period - consider increasing exposure")
elif seasonal.current_month_rank >= 9:
    print("Weak seasonal period - consider reducing exposure")
```

### 2. Risk Management

Adjust position sizing based on volatility regime:

```python
if cycle.volatility_regime == "extreme":
    position_size *= 0.5  # Reduce size in high volatility
elif cycle.volatility_regime == "low":
    position_size *= 1.2  # Increase size in low volatility
```

### 3. Election Cycle Trading

Align strategy with presidential cycle:

```python
if election.current_phase == ElectionCyclePhase.YEAR_3:
    print("Year 3 - historically strongest, increase equity exposure")
elif election.current_phase == ElectionCyclePhase.YEAR_1:
    print("Year 1 - historically weakest, be defensive")
```

### 4. OPEX Week Positioning

Navigate options expiration:

```python
if options.is_opex_week:
    if options.opex_drift_pattern == "bullish_pre_bearish_post":
        print("Consider taking profits before expiration")
    if options.is_triple_witching:
        print("Triple witching - expect elevated volatility")
```

### 5. Regime-Based Strategy Selection

Choose strategy based on market regime:

```python
if cycle.current_regime == MarketRegime.BULL_STRONG:
    strategy = "trend_following"
elif cycle.current_regime == MarketRegime.SIDEWAYS:
    strategy = "mean_reversion"
elif cycle.current_regime == MarketRegime.DISTRIBUTION:
    strategy = "defensive"
```

## Interpretation Guide

### Composite Score (0-100)

- **80-100**: Very Bullish - Multiple favorable patterns aligned
- **60-80**: Bullish - Generally favorable conditions
- **40-60**: Neutral - Mixed signals
- **20-40**: Bearish - Generally unfavorable conditions
- **0-20**: Very Bearish - Multiple negative patterns

### Bull/Bear Score (-100 to +100)

- **+60 to +100**: Strong Bull - Aggressive long positioning
- **+20 to +60**: Weak Bull - Cautious long positioning
- **-20 to +20**: Neutral - Wait for clarity
- **-60 to -20**: Weak Bear - Cautious short/defensive
- **-100 to -60**: Strong Bear - Aggressive defensive positioning

### Regime Confidence

- **>80%**: High confidence - strong regime signals
- **60-80%**: Medium confidence - some mixed signals
- **<60%**: Low confidence - regime uncertain

## Historical Performance

Based on S&P 500 data (1950-2024):

### Monthly Performance Ranking
1. April: +1.5% average
2. July: +1.2% average
3. March: +1.1% average
4. January: +1.0% average
5. November: +1.0% average
...
12. September: -0.5% average

### Election Cycle Performance
- Year 1 (Post-Election): +4.0% average
- Year 2 (Mid-Term): +5.5% average
- Year 3 (Pre-Election): +16.3% average
- Year 4 (Election): +7.5% average

### OPEX Effects
- Pre-OPEX Week: +0.3% average
- Post-OPEX Week: -0.1% average
- Triple Witching Volatility: +25% vs normal

## Limitations and Considerations

1. **Past Performance**: Historical patterns don't guarantee future results
2. **Changing Markets**: Market structure evolves over time
3. **External Events**: Black swan events can override seasonal patterns
4. **Multiple Timeframes**: Consider multiple timeframes for confirmation
5. **Risk Management**: Always use proper position sizing and stops

## Best Practices

1. **Combine Multiple Signals**: Don't rely on single pattern
2. **Use Composite Score**: Consider overall favorability
3. **Monitor Regime Changes**: Watch for regime transitions
4. **Respect Volatility**: Adjust sizing based on volatility regime
5. **Stay Flexible**: Be ready to adapt when patterns break

## Support and Documentation

For more information:
- API Documentation: `/docs` (FastAPI Swagger UI)
- Code: `app/core/market_seasonality.py`
- Tests: `tests/test_market_seasonality.py`
- Examples: See API endpoint documentation

## Contributing

To add new patterns or improve analysis:
1. Update `MarketSeasonalityAnalyzer` class
2. Add corresponding tests
3. Update this documentation
4. Submit PR for review
