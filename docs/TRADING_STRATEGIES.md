# Trading Strategies Documentation

This document provides comprehensive documentation for the proven trading strategies implemented in this platform, based on methodologies from legendary traders:

- **Mark Minervini** - SEPA, VCP, Stage Analysis
- **William O'Neil** - CAN SLIM, Cup & Handle, Breakouts
- **Stan Weinstein** - 4-Stage Cycle Analysis

## Table of Contents

1. [Overview](#overview)
2. [Mark Minervini Strategy](#mark-minervini-strategy)
3. [William O'Neil Strategy](#william-oneil-strategy)
4. [Stan Weinstein Strategy](#stan-weinstein-strategy)
5. [Comparison & Best Practices](#comparison--best-practices)
6. [Implementation Guide](#implementation-guide)

---

## Overview

### Why These Strategies?

These three trading methodologies share common principles:
- **Trend Following**: Buy stocks in confirmed uptrends
- **Volume Confirmation**: Institutional buying drives big moves
- **Risk Management**: Defined stop losses, position sizing
- **Pattern Recognition**: Specific chart setups signal high-probability trades
- **Market Timing**: Only trade when market conditions are favorable

### Key Differences

| Strategy | Best For | Time Frame | Key Metric | Risk/Trade |
|----------|----------|------------|------------|------------|
| **Minervini** | Growth stocks, momentum | Swing (weeks-months) | VCP pattern, RS rating | 1% |
| **O'Neil** | IPOs, growth leaders | Swing (weeks-months) | CAN SLIM score | 7-8% |
| **Weinstein** | All stocks, trend following | Position (months) | Stage analysis | Stage-based |

---

## Mark Minervini Strategy

### Overview

Mark Minervini is a U.S. stock trading champion (1997) with a verified 5-year return of 33,554%. His SEPA (Specific Entry Point Analysis) methodology combines technical and fundamental analysis for precision entries.

### Core Components

#### 1. Trend Template (8-Point Checklist)

Every stock must pass this checklist to be in a confirmed Stage 2 uptrend:

1. **Current price > 150-day & 200-day MA**
2. **150-day MA > 200-day MA**
3. **200-day MA trending up** (at least 1 month)
4. **50-day MA > 150-day MA > 200-day MA**
5. **Current price > 50-day MA**
6. **Price at least 30% above 52-week low**
7. **Price within 25% of 52-week high**
8. **Relative Strength (RS) rating ≥ 70**

**Scoring**: Must meet at least 7 of 8 criteria.

#### 2. VCP (Volatility Contraction Pattern)

The VCP is Minervini's signature pattern:

**Characteristics:**
- Series of 3-6 price contractions (pullbacks)
- Each contraction is **smaller** than the previous (e.g., 20%, 12%, 8%, 4%)
- Volume **decreases** during each contraction
- Final contraction typically ≤ 8%
- Creates "tight" price action before explosive breakout

**Example:**
```
Contraction 1: -18% decline from high
Contraction 2: -12% decline from high
Contraction 3: -7% decline from high
Contraction 4: -4% decline from high  ← Breakout ready
```

**Entry**: Buy when price breaks above the pivot (resistance) on **volume surge**

#### 3. Stage Analysis

Minervini uses a 4-stage model (similar to Weinstein):

- **Stage 1**: Basing - Consolidation, price flat
- **Stage 2**: Uptrend - Buy zone! Strong momentum
- **Stage 3**: Topping - Distribution, exit
- **Stage 4**: Downtrend - Avoid completely

**Only buy in Stage 2.**

#### 4. Position Sizing (1% Risk Rule)

**Never risk more than 1% of your total capital on a single trade.**

**Formula:**
```
Risk per share = Entry Price - Stop Loss Price
Shares to buy = (Account Size × 0.01) / Risk per share
```

**Example:**
- Account: $100,000
- Entry: $50
- Stop Loss: $46.50 (7% below entry)
- Risk per share: $3.50
- Shares: ($100,000 × 0.01) / $3.50 = 285 shares
- Total position: $14,250 (14.25% of account)
- Max loss if stopped out: $1,000 (1% of account)

#### 5. Entry/Exit Rules

**Entry Types:**
1. **Breakout Entry**: Buy as price breaks above VCP pivot on volume
2. **Pullback Entry**: Buy on pullback to 50-day MA in confirmed uptrend

**Stop Loss:**
- 7% for less volatile stocks
- 10% for more volatile stocks
- Place below recent swing low or key support

**Profit Taking:**
- Let winners run (trailing stop)
- Take partial profits at 20-25%
- Full exit if breaks below 50-day MA on volume

**Risk/Reward:**
- Minimum 4:1 risk/reward ratio
- Example: Risk $1 to make $4+

---

## William O'Neil Strategy

### Overview

William O'Neil founded Investor's Business Daily (IBD) and developed the CAN SLIM system by studying the biggest stock market winners from 1953-1993. His methodology focuses on buying leading stocks in leading industries at the right time.

### Core Components

#### 1. CAN SLIM Criteria

Each letter represents a key characteristic:

##### C - Current Quarterly Earnings
- **Requirement**: EPS up **25%+ YoY** (year-over-year)
- Look for acceleration: 25% → 50% → 100%
- Both sales and earnings should be up

##### A - Annual Earnings Growth
- **Requirement**: EPS growth **25%+ per year** over last 3 years
- ROE (Return on Equity) > 17%
- Stable or expanding profit margins

##### N - New (Something New)
- **New products or services** driving growth
- **New management** turning company around
- **New highs** - stock within 15% of 52-week high
- New industry leadership

##### S - Supply & Demand
- **Reasonable float**: Prefer < 25M shares for small-cap growth
- **Volume**: Accumulation days > Distribution days
- Buybacks reducing share count is bullish

##### L - Leader or Laggard
- **Requirement**: RS Rating **80+** (top 20% of market)
- Buy #1 or #2 stock in industry group
- Avoid sympathy plays - buy the leader

##### I - Institutional Sponsorship
- **Requirement**: 10-50% institutional ownership
- Increasing number of funds owning (recent quarters)
- Quality institutions (Fidelity, T. Rowe Price, etc.)
- Not excessive (>70% can lead to heavy selling)

##### M - Market Direction
- **Requirement**: Market in **confirmed uptrend**
- 75% of stocks follow the market
- Use Follow-Through Day to confirm bottom
- Reduce/stop buying in corrections

**Scoring**: Need 5-6 out of 7 criteria met.

#### 2. Cup & Handle Pattern

O'Neil's most profitable pattern:

**Cup Formation:**
- **Prior uptrend**: At least 30% gain before cup
- **Depth**: 12-33% (max 50% in bear market)
- **Shape**: Rounded bottom (U-shape, not V)
- **Duration**: 7-65 weeks (prefer 3-6 months)
- **Left/Right peaks**: Similar heights (within 5%)

**Handle Formation:**
- **Location**: Upper half of cup
- **Depth**: 8-12% (max 15%)
- **Duration**: 1-4+ weeks
- **Shape**: Downward drift or sideways
- **Volume**: Should dry up (decreasing)

**Buy Point:**
- Just above right peak (pivot point)
- Buy within 5% of buy point
- Requires **volume surge**: 40-50%+ above average

**Example:**
```
    Right Peak ($50) ← BUY POINT
    /‾‾‾‾‾\  Handle
   /       \___/
  /             \
Left Peak        Cup Bottom
($50)             ($35, -30% depth)
```

#### 3. Breakout Rules

**Valid Breakout Checklist:**
- [ ] Price breaks above pivot/resistance
- [ ] Volume **50%+ above 50-day average**
- [ ] Close in upper 25% of day's range
- [ ] Buy within 5% of buy point
- [ ] Market in confirmed uptrend (ideally)
- [ ] Stock meets CAN SLIM criteria

**Volume is Critical:**
- 40-50% surge: Minimum acceptable
- 100%+ surge: Very strong
- 200%+ surge: Explosive (institutions piling in)

#### 4. Follow-Through Day (FTD)

FTD signals market bottom and confirms new uptrend:

**Criteria:**
1. Occurs on **day 4-7** of rally attempt (can be up to day 12)
2. Major index (S&P 500, NASDAQ) gains **1.25%+** (ideally 1.7%+)
3. **Volume higher** than previous day
4. Volume above 50-day average (preferred)

**How to Use:**
- FTD = green light to start buying
- No FTD = stay cautious, light positions
- Failed FTD (market drops below FTD day) = red flag

#### 5. Risk Management

**Stop Loss:**
- **7-8% maximum** below buy point
- No exceptions - cut losses quickly
- "Sell at 7-8% loss, or you'll be selling at 50% loss later"

**Position Sizing:**
- Start with 1/2 position
- Add 1/2 more if stock proves itself (+3-5%)
- Max 20-25% of portfolio in single stock

**When to Sell:**
- Stock drops 7-8% from buy point
- Breaks below buy point after poor action
- Volume dries up at resistance
- Market enters correction

---

## Stan Weinstein Strategy

### Overview

Stan Weinstein's "Secrets for Profiting in Bull and Bear Markets" (1988) introduced Stage Analysis, a powerful trend-following system. Weinstein uses **weekly charts** and the **30-week moving average** as the primary tools.

### Core Components

#### 1. The 4-Stage Cycle

Every stock goes through 4 repeating stages:

##### Stage 1: Basing (Accumulation)
**Characteristics:**
- Price oscillates above/below **flat** 30-week MA
- Narrow trading range (low volatility)
- Low volume
- MA is horizontal (neither rising nor falling)

**Action:** Watch and wait. Accumulate small positions late in stage.

**Duration:** Weeks to months

##### Stage 2: Advancing (Markup)
**Characteristics:**
- Price breaks **above resistance** on **heavy volume** (2-3x average)
- Price stays **above rising** 30-week MA
- Makes higher highs and higher lows
- Volume expands on rallies, contracts on dips
- MA slopes upward

**Action:** **BUY AGGRESSIVELY** early in Stage 2 (Stage 2A)

**Duration:** Months to years

**Sub-stages:**
- **2A (Early)**: Just broke out, MA just turned up - BEST buying zone
- **2B (Late)**: Extended move, MA steep - Be cautious, take profits

##### Stage 3: Topping (Distribution)
**Characteristics:**
- Price churns sideways, MA **flattens**
- Price crosses above/below MA frequently (whipsaws)
- High volume but no progress (churning)
- Leading stocks start to break down

**Action:** Sell holdings, take profits. Reduce positions.

**Duration:** Weeks to months

##### Stage 4: Declining (Markdown)
**Characteristics:**
- Price breaks **below** 30-week MA on volume
- Makes lower highs and lower lows
- MA slopes **downward**
- Rallies are brief and weak
- Volume spikes on declines

**Action:** **AVOID**. Do not buy. Short if experienced.

**Duration:** Months to years

**The Cycle:**
```
Stage 1 → Stage 2 → Stage 3 → Stage 4 → (repeat)
Basing    Advancing  Topping    Declining
  🔄         ⬆️          ➡️          ⬇️
```

#### 2. The 30-Week Moving Average

The **30-week simple moving average** (SMA) is Weinstein's primary indicator:

**On Daily Charts:** Use **150-day MA** (equivalent to 30-week)

**Rules:**
- **Above MA** + **MA rising** = Bullish (Stage 2)
- **Below MA** + **MA falling** = Bearish (Stage 4)
- **At MA** + **MA flat** = Neutral (Stage 1 or 3)

**Entry Signal:**
- Buy when price closes **above 30-week MA** for first time
- MA must be **turning up** (or already rising)
- Volume must be **2x 4-week average**

**Exit Signal:**
- Sell when price closes **below 30-week MA**
- MA turning down confirms Stage 4

#### 3. Stage 2 Breakout Strategy

**Setup Checklist:**
- [ ] Stock in Stage 1 base (flat MA, tight range)
- [ ] Base duration: 4+ weeks minimum
- [ ] Resistance level clearly defined
- [ ] Volume contracting during base

**Breakout Triggers:**
- [ ] Price breaks above resistance
- [ ] Close above 30-week MA
- [ ] Volume **2-3x 4-week average**
- [ ] 30-week MA turning up
- [ ] Mansfield RS crossing above zero (confirming)

**Entry:**
- Buy on breakout day or next day if volume confirmed
- Buy within **5-10%** of breakout price

**Stop Loss:**
- Below recent base low
- Or below 30-week MA
- Max risk: 10-15%

#### 4. Mansfield Relative Strength

Measures stock performance vs. market:

**Formula:**
```
MRS = ((Stock Price / Market Price) / 52-week MA of ratio) - 1) × 100
```

**Interpretation:**
- **MRS > 0**: Stock outperforming market ✅
- **MRS < 0**: Stock underperforming market ❌
- **Crossing above 0**: Bullish signal (buy)
- **Crossing below 0**: Bearish signal (sell)
- **Rising MRS**: Strengthening momentum
- **Falling MRS**: Weakening momentum

**Best Stocks:**
- MRS > 0 and rising
- In top 20% of all stocks by MRS
- Leading their industry group

#### 5. Volume Analysis

**Volume Patterns:**

**Stage 1 (Base):**
- Volume low and contracting
- No climactic spikes

**Stage 2 (Uptrend):**
- Volume **expands on rallies** (up days)
- Volume **contracts on dips** (down days)
- "Up on volume, down on light volume" = healthy

**Stage 3 (Top):**
- High volume but no progress
- Volume on down days increasing
- Distribution occurring

**Stage 4 (Downtrend):**
- Volume spikes on panic selling
- Rallies on light volume (weak)

**Breakout Volume:**
- **Minimum**: 2x 4-week average
- **Ideal**: 3x+ 4-week average
- More volume = stronger institutional buying

#### 6. Risk Management

**Position Sizing:**
- Allocate based on stage:
  - Stage 2A (early): 100% allocation
  - Stage 2B (late): 50% allocation or less
  - Stage 3: 0% - exit
  - Stage 4: 0% - avoid

**Stop Losses:**
- **Initial stop**: Below base low or 30-week MA
- **Trailing stop**: Raise to 30-week MA as it rises
- Exit if closes below 30-week MA

**Portfolio Management:**
- **Bull Market**: 80-100% invested (Stage 2 stocks)
- **Bear Market**: 0-20% invested (mostly cash)
- Diversify across 10-15 stocks minimum

---

## Comparison & Best Practices

### Strategy Comparison Matrix

| Aspect | Minervini | O'Neil | Weinstein |
|--------|-----------|--------|-----------|
| **Timeframe** | Daily charts | Daily charts | Weekly charts (30-week MA) |
| **Key Indicator** | 50/150/200-day MA, VCP | Cup & Handle, RS rating | 30-week MA, Stage |
| **Entry Signal** | VCP breakout, pullback to 50-day MA | Cup & Handle breakout above pivot | Stage 2 breakout above resistance |
| **Volume Requirement** | Surge on breakout | 40-50%+ above average | 2-3x 4-week average |
| **Stop Loss** | 7-10% | 7-8% | Below 30-week MA or base |
| **Risk per Trade** | 1% | Varies | Stage-based |
| **Best for Beginners** | Intermediate | Advanced | Beginner-Intermediate |
| **Pattern Complexity** | High (VCP nuanced) | High (Cup & Handle quality) | Medium (Stage visual) |
| **Fundamental Weight** | 30% | 50% (CAN SLIM) | 10% |
| **Market Timing** | Important (Stage 2) | Critical (Follow-Through Day) | Essential (Bull/Bear) |

### When to Use Each Strategy

**Use Minervini When:**
- ✅ Looking for momentum growth stocks
- ✅ Want precision entries (SEPA)
- ✅ Comfortable with tight stops (7-10%)
- ✅ Focus on small-cap to mid-cap growth
- ✅ Can monitor daily for VCP patterns

**Use O'Neil When:**
- ✅ Want complete system (fundamental + technical)
- ✅ Buying established leaders (large-cap)
- ✅ Following IPOs and new issues
- ✅ Have access to IBD data (RS ratings, etc.)
- ✅ Want clear buy/sell rules (Cup & Handle)

**Use Weinstein When:**
- ✅ Prefer longer-term trend following
- ✅ Want simplicity (just 30-week MA + stage)
- ✅ Trading any size stock or ETF
- ✅ Checking weekly (not daily)
- ✅ Need clear market timing signals (stages)

### Combining Strategies (Best Approach!)

The most powerful approach is to **combine elements** from all three:

**Screening:**
1. Use **Weinstein Stage Analysis** to identify Stage 2 stocks
2. Filter for **O'Neil CAN SLIM criteria** (fundamentals)
3. Look for **Minervini VCP patterns** for precise entry

**Entry:**
1. Buy **Stage 2A stocks** (Weinstein - early uptrend)
2. With **CAN SLIM score 5+** (O'Neil - strong fundamentals)
3. On **VCP breakout or pullback to 50-day MA** (Minervini - precise entry)
4. Confirm with **volume surge** (all three agree)

**Risk Management:**
1. Use **Minervini 1% risk rule** for position sizing
2. Set **O'Neil 7-8% stop loss** below entry
3. Exit if **Weinstein Stage changes** to Stage 3 or 4

**Position Management:**
1. Take **partial profits at 20-25%** (Minervini/O'Neil)
2. Use **trailing stop at 50-day MA** (Minervini)
3. Exit completely if **breaks below 30-week MA** (Weinstein)

**Example Combined Workflow:**
```
1. Screen: All stocks in Weinstein Stage 2A
2. Filter: CAN SLIM score ≥ 5, RS rating ≥ 80
3. Pattern: VCP with 3+ contractions forming
4. Entry: Buy on breakout above VCP pivot
5. Volume: Confirm 2x+ average volume
6. Position: Risk 1% of account (Minervini rule)
7. Stop: 7% below entry (O'Neil rule)
8. Exit: If breaks 50-day MA or Stage changes
```

---

## Implementation Guide

### Getting Started

#### 1. Setup Your Environment

```python
from app.strategies import MinerviniStrategy, ONeilStrategy, WeinsteinStrategy
import pandas as pd

# Load your OHLCV data
ohlcv = pd.read_csv('stock_data.csv')
# Ensure columns: ['open', 'high', 'low', 'close', 'volume']
```

#### 2. Basic Usage Examples

See `examples/strategy_examples.py` for detailed code examples.

**Minervini Example:**
```python
# Initialize strategy
minervini = MinerviniStrategy(
    risk_per_trade=0.01,  # 1% risk
    max_stop_loss=0.10,   # 10% max stop
    account_size=100000
)

# Check Trend Template
trend_result = minervini.check_trend_template(ohlcv)
print(f"Stage: {trend_result.stage}")
print(f"Score: {trend_result.score}/8")
print(f"Passes: {trend_result.passes}")

# Analyze for VCP
vcp = minervini.analyze_vcp(ohlcv)
print(f"Is VCP: {vcp.is_vcp}")
print(f"Contractions: {vcp.contraction_sequence}")

# Generate SEPA signal
signal = minervini.generate_sepa_signal(ohlcv, symbol='AAPL')
if signal:
    print(f"Entry: ${signal.entry_price:.2f}")
    print(f"Stop: ${signal.stop_loss:.2f}")
    print(f"Position Size: {signal.position_size_pct:.1f}%")
```

**O'Neil Example:**
```python
# Initialize strategy
oneil = ONeilStrategy(
    min_volume_surge=0.40,  # 40% volume increase
    max_stop_loss=0.08,     # 8% max stop
)

# Evaluate CAN SLIM
fundamentals = {
    'eps_growth_qoq': 50,  # 50% quarterly growth
    'eps_growth_3yr': 30,  # 30% annual growth
    'institutional_ownership_pct': 35,
    'shares_outstanding': 50_000_000
}

canslim = oneil.evaluate_canslim(ohlcv, fundamentals)
print(f"Score: {canslim.total_score}/7")
print(f"Recommendation: {canslim.recommendation}")

# Detect Cup & Handle
cup_handle = oneil.detect_cup_and_handle(ohlcv)
if cup_handle.found:
    print(f"Buy Point: ${cup_handle.buy_point:.2f}")
    print(f"Quality: {cup_handle.quality_score:.0f}/100")

# Identify Breakout
breakout = oneil.identify_breakout(ohlcv, symbol='TSLA')
if breakout:
    print(f"Breakout: ${breakout.buy_point:.2f}")
    print(f"Volume Surge: +{breakout.volume_surge_pct:.0f}%")
```

**Weinstein Example:**
```python
# Initialize strategy
weinstein = WeinsteinStrategy(
    use_weekly=True,        # Use weekly charts
    min_volume_surge=2.0,   # 2x volume
    ma_period=30            # 30-week MA
)

# Analyze Stage
stage_result = weinstein.analyze_stage(ohlcv)
print(f"Stage: {stage_result.stage.name}")
print(f"Sub-stage: {stage_result.sub_stage}")
print(f"MA Slope: {stage_result.ma_slope}")

# Calculate Mansfield RS
market_ohlcv = pd.read_csv('sp500_data.csv')
mansfield = weinstein.calculate_mansfield_rs(ohlcv, market_ohlcv)
print(f"Mansfield RS: {mansfield.current_value:.2f}")
print(f"Is Strong: {mansfield.is_strong}")

# Identify Stage 2 Breakout
breakout = weinstein.identify_stage2_breakout(
    ohlcv,
    symbol='NVDA',
    market_ohlcv=market_ohlcv
)
if breakout:
    print(f"Entry: ${breakout.entry_price:.2f}")
    print(f"Stop: ${breakout.stop_loss:.2f}")
    print(f"Volume: {breakout.volume_vs_avg:.1f}x average")
```

### Best Practices

#### 1. Data Quality
- Use clean, adjusted OHLCV data
- Include at least 252 trading days (1 year)
- Verify volume is actual volume (not 0 or NaN)

#### 2. Backtesting
- Test strategies on historical data first
- Account for slippage and commissions
- Use realistic position sizing
- Don't over-optimize parameters

#### 3. Risk Management
- Never risk more than 1-2% per trade
- Diversify across 10-15 positions minimum
- Keep 10-20% cash for opportunities
- Honor your stop losses (no exceptions!)

#### 4. Market Conditions
- These are bull market strategies
- Reduce positions in corrections (Stage 4 markets)
- Wait for Follow-Through Day before aggressive buying
- Cash is a position during bear markets

#### 5. Psychology
- Follow your rules mechanically
- Don't chase stocks > 5% above buy point
- Cut losses quickly, let winners run
- Take partial profits to lock in gains
- Don't buy "bargains" in Stage 4!

### Performance Metrics

Track these metrics to evaluate strategy performance:

- **Win Rate**: % of profitable trades (target: 50-60%)
- **Avg Win / Avg Loss**: Ratio (target: >2:1)
- **Expectancy**: (Win% × Avg Win) - (Loss% × Avg Loss)
- **Max Drawdown**: Largest peak-to-trough decline
- **Sharpe Ratio**: Risk-adjusted returns

### Further Resources

**Books:**
- Mark Minervini: "Trade Like a Stock Market Wizard" (2013)
- Mark Minervini: "Think & Trade Like a Champion" (2017)
- William O'Neil: "How to Make Money in Stocks" (2009)
- Stan Weinstein: "Secrets for Profiting in Bull and Bear Markets" (1988)

**Tools:**
- Investor's Business Daily (IBD): RS ratings, CAN SLIM data
- MarketSmith: O'Neil's charting platform
- TradingView: Chart patterns, indicators
- FinViz: Stock screeners

**Practice:**
- Paper trade first (no real money)
- Start with small positions
- Keep a trading journal
- Review trades weekly

---

## Disclaimer

**This is educational material only. Not financial advice.**

- Past performance does not guarantee future results
- Trading stocks involves substantial risk of loss
- Only trade with capital you can afford to lose
- Consult a licensed financial advisor before investing
- The strategies described require discipline and practice
- No strategy wins 100% of the time

**Key Risks:**
- Market risk (overall market declines)
- Individual stock risk (company-specific issues)
- Gap risk (overnight price gaps through stop loss)
- Slippage and commission costs
- Psychological challenges (fear, greed, FOMO)

**Remember:**
> "The goal is not to be right. The goal is to make money." - Mark Minervini

Focus on consistent execution of your rules, proper risk management, and continuous learning.

---

*Last Updated: 2025*
*Version: 1.0*
