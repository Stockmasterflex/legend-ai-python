# Trading Strategy Best Practices & Optimization Guide

This guide provides advanced tips, best practices, and optimization techniques for implementing the Minervini, O'Neil, and Weinstein trading strategies.

## Table of Contents

1. [Backtesting Guidelines](#backtesting-guidelines)
2. [Parameter Optimization](#parameter-optimization)
3. [Risk Management Advanced](#risk-management-advanced)
4. [Performance Metrics](#performance-metrics)
5. [Common Mistakes](#common-mistakes)
6. [Strategy Combinations](#strategy-combinations)
7. [Market Conditions Adaptation](#market-conditions-adaptation)
8. [Automation & Scanning](#automation--scanning)

---

## Backtesting Guidelines

### Essential Principles

#### 1. Survivorship Bias

**Problem**: Only testing on stocks that still exist today
**Solution**: Include delisted stocks in your dataset

```python
# Bad: Only current S&P 500 members
stocks = get_current_sp500()

# Good: All stocks that were ever in S&P 500
stocks = get_historical_sp500(include_delisted=True)
```

#### 2. Look-Ahead Bias

**Problem**: Using future information not available at trade time
**Solution**: Strict time-based data access

```python
# Bad: Using final close for entry decision
entry_price = df['close'].iloc[i]  # Knows final close

# Good: Use high/low range or next bar open
entry_price = df['open'].iloc[i+1]  # Next bar entry
```

#### 3. Realistic Slippage & Commissions

**Commission**: $0-1 per trade (zero for most brokers)
**Slippage**: 0.1-0.5% depending on liquidity

```python
# Example position entry with slippage
theoretical_entry = 50.00
slippage = 0.002  # 0.2%
actual_entry = theoretical_entry * (1 + slippage)  # $50.10

# Commission impact (legacy)
commission = 1.00  # $1 per trade
shares = 100
total_cost = actual_entry * shares + commission
```

#### 4. Position Sizing Constraints

**Account for:**
- Maximum position size (e.g., 10% of account)
- Minimum lot sizes (100 shares, or fractional?)
- Available capital constraints
- Margin requirements (if applicable)

```python
def calculate_realistic_position(account_value, entry_price,
                                 stop_loss, risk_pct=0.01):
    """Calculate position size with real-world constraints"""

    # Max shares based on risk
    risk_amount = account_value * risk_pct
    risk_per_share = entry_price - stop_loss
    max_shares_risk = int(risk_amount / risk_per_share)

    # Max shares based on position size (e.g., 20% max)
    max_position_value = account_value * 0.20
    max_shares_position = int(max_position_value / entry_price)

    # Take minimum
    shares = min(max_shares_risk, max_shares_position)

    # Round to lot size (e.g., 100 shares)
    shares = (shares // 100) * 100

    return max(shares, 0)  # At least 0
```

### Backtesting Checklist

- [ ] Use clean, adjusted OHLCV data (splits, dividends)
- [ ] Include all corporate actions
- [ ] Account for survivorship bias
- [ ] Avoid look-ahead bias
- [ ] Apply realistic slippage (0.1-0.5%)
- [ ] Include commissions (if any)
- [ ] Respect position sizing limits
- [ ] Test across multiple market conditions
- [ ] Use out-of-sample testing (walk-forward)
- [ ] Track all metrics (not just returns)

### Sample Backtest Framework

```python
class StrategyBacktest:
    def __init__(self, initial_capital=100000,
                 commission=0, slippage=0.002):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.positions = {}
        self.trades = []
        self.equity_curve = []

    def enter_trade(self, symbol, date, entry_price,
                   stop_loss, shares):
        """Enter a position"""
        # Apply slippage
        actual_entry = entry_price * (1 + self.slippage)

        # Calculate cost
        cost = actual_entry * shares + self.commission

        # Check if enough capital
        if cost > self.capital:
            return False  # Can't afford trade

        # Update capital
        self.capital -= cost

        # Record position
        self.positions[symbol] = {
            'entry_date': date,
            'entry_price': actual_entry,
            'stop_loss': stop_loss,
            'shares': shares,
            'cost_basis': cost
        }

        return True

    def exit_trade(self, symbol, date, exit_price, reason):
        """Exit a position"""
        if symbol not in self.positions:
            return False

        pos = self.positions[symbol]

        # Apply slippage (negative for sells)
        actual_exit = exit_price * (1 - self.slippage)

        # Calculate proceeds
        proceeds = actual_exit * pos['shares'] - self.commission

        # Update capital
        self.capital += proceeds

        # Calculate P&L
        pnl = proceeds - pos['cost_basis']
        pnl_pct = (pnl / pos['cost_basis']) * 100

        # Record trade
        self.trades.append({
            'symbol': symbol,
            'entry_date': pos['entry_date'],
            'exit_date': date,
            'entry_price': pos['entry_price'],
            'exit_price': actual_exit,
            'shares': pos['shares'],
            'pnl': pnl,
            'pnl_pct': pnl_pct,
            'exit_reason': reason
        })

        # Remove position
        del self.positions[symbol]

        return True

    def update_equity(self, date, current_prices):
        """Update equity curve"""
        # Cash + position values
        position_value = sum(
            current_prices.get(sym, pos['entry_price']) * pos['shares']
            for sym, pos in self.positions.items()
        )

        total_equity = self.capital + position_value

        self.equity_curve.append({
            'date': date,
            'equity': total_equity,
            'cash': self.capital,
            'positions_value': position_value,
            'num_positions': len(self.positions)
        })

        return total_equity
```

---

## Parameter Optimization

### Dangerous Practices to Avoid

#### 1. Over-Optimization (Curve Fitting)

**Problem**: Parameters that work perfectly on historical data but fail in live trading

**Signs of over-fitting:**
- Too many parameters (>5-7)
- Very specific values (MA = 47.3 days instead of 50)
- Perfect results on in-sample data
- Poor performance on out-of-sample data

**Solutions:**
- Use simple, round numbers (50, 100, 200)
- Limit number of parameters
- Test on out-of-sample data
- Use walk-forward optimization
- Check parameter stability

#### 2. Walk-Forward Analysis

Best practice for optimization:

```
Year 1-3: Optimize parameters → Find MA = 50, Stop = 7%
Year 4: Test with those parameters → Record results
Year 2-4: Re-optimize → Find MA = 50, Stop = 7% (stable!)
Year 5: Test with new parameters → Record results
...continue rolling window
```

**Implementation:**
```python
def walk_forward_optimization(data, window=252*3, step=252):
    """
    Walk-forward parameter optimization

    Args:
        data: Full dataset
        window: Optimization window (3 years)
        step: Step forward (1 year)
    """
    results = []

    for start in range(0, len(data) - window - step, step):
        # Optimization period
        opt_data = data[start:start + window]

        # Find best parameters on optimization period
        best_params = optimize_parameters(opt_data)

        # Test period (next year)
        test_data = data[start + window:start + window + step]

        # Test with optimized parameters
        test_result = backtest(test_data, best_params)

        results.append({
            'opt_period': (start, start + window),
            'test_period': (start + window, start + window + step),
            'params': best_params,
            'test_return': test_result['return'],
            'test_sharpe': test_result['sharpe']
        })

    return results
```

### Recommended Parameter Ranges

#### Minervini Strategy

| Parameter | Default | Range | Notes |
|-----------|---------|-------|-------|
| Risk per trade | 1% | 0.5-2% | Don't exceed 2% |
| Stop loss | 7-10% | 5-12% | Volatile stocks = wider |
| RS rating min | 70 | 60-85 | Higher = more selective |
| VCP contractions | 3+ | 3-6 | Quality over quantity |

#### O'Neil Strategy

| Parameter | Default | Range | Notes |
|-----------|---------|-------|-------|
| Volume surge | 40-50% | 30-100% | Higher = stronger |
| Stop loss | 7-8% | 6-10% | Strict! |
| RS rating min | 80 | 70-90 | Top 20% minimum |
| CAN SLIM min | 5/7 | 4-6/7 | 6+ is ideal |

#### Weinstein Strategy

| Parameter | Default | Range | Notes |
|-----------|---------|-------|-------|
| MA period (weekly) | 30 | 25-40 | 30 is standard |
| MA period (daily) | 150 | 130-200 | 150 ≈ 30 weeks |
| Volume surge | 2x | 1.5-3x | 2x minimum |
| Stop loss | 10-15% | 8-20% | Below MA or base |

### Parameter Stability Test

Check if parameters are stable across time:

```python
def test_parameter_stability(data, param_name, param_range):
    """Test how sensitive results are to parameter changes"""

    results = {}

    for param_value in param_range:
        # Run backtest with this parameter
        result = backtest(data, **{param_name: param_value})

        results[param_value] = {
            'total_return': result['total_return'],
            'sharpe': result['sharpe'],
            'max_drawdown': result['max_drawdown']
        }

    # Good parameter: stable across range
    # Bad parameter: huge variance in results

    return results

# Example
stop_loss_range = [0.05, 0.06, 0.07, 0.08, 0.09, 0.10]
stability = test_parameter_stability(data, 'stop_loss', stop_loss_range)

# If 7% stop = 50% return and 8% stop = 10% return → unstable!
# If 7% stop = 50% return and 8% stop = 48% return → stable ✓
```

---

## Risk Management Advanced

### Position Sizing Methods

#### 1. Fixed Fractional (Minervini's 1% Rule)

```python
def fixed_fractional(account_value, risk_pct, entry, stop):
    """Risk fixed % of account per trade"""
    risk_amount = account_value * risk_pct
    risk_per_share = entry - stop
    shares = int(risk_amount / risk_per_share)
    return shares

# Example
shares = fixed_fractional(100000, 0.01, 50, 46.50)
# Risks exactly $1,000 (1% of $100k)
```

#### 2. Percent Volatility (Normalize by ATR)

```python
def percent_volatility(account_value, atr, target_volatility=0.02):
    """Position size based on stock's volatility (ATR)"""
    # Target: position volatility = 2% of account
    target_risk = account_value * target_volatility
    shares = int(target_risk / atr)
    return shares

# Example: Stock A with ATR=$2 gets same risk as Stock B with ATR=$4
# by adjusting share count
```

#### 3. Kelly Criterion (Advanced)

```python
def kelly_criterion(win_rate, avg_win, avg_loss):
    """Optimal position size based on edge"""
    # Kelly % = (Win% × AvgWin - Loss% × AvgLoss) / AvgWin
    loss_rate = 1 - win_rate
    kelly_pct = (win_rate * avg_win - loss_rate * avg_loss) / avg_win

    # Use fractional Kelly (e.g., 25-50% of full Kelly)
    # Full Kelly is too aggressive
    safe_kelly = kelly_pct * 0.25

    return max(0, min(safe_kelly, 0.10))  # Cap at 10%

# Example
win_rate = 0.55  # 55% win rate
avg_win = 0.25   # Average win: 25%
avg_loss = 0.07  # Average loss: 7%

kelly = kelly_criterion(win_rate, avg_win, avg_loss)
# Returns position size as % of account
```

### Portfolio Heat Management

**Portfolio Heat** = Total risk across all open positions

```python
def calculate_portfolio_heat(positions, account_value):
    """Calculate total risk exposure"""
    total_risk = 0

    for pos in positions:
        risk_per_share = pos['entry'] - pos['stop']
        position_risk = risk_per_share * pos['shares']
        total_risk += position_risk

    heat_pct = (total_risk / account_value) * 100

    return heat_pct

# Example
positions = [
    {'entry': 50, 'stop': 46.50, 'shares': 285},  # $1k risk
    {'entry': 100, 'stop': 93, 'shares': 142},    # $1k risk
    {'entry': 25, 'stop': 23.25, 'shares': 571},  # $1k risk
]

heat = calculate_portfolio_heat(positions, 100000)
# heat = 3% (3 positions × 1% each)

# Rules:
# - Keep heat < 6-8% in normal markets
# - Reduce heat to < 3% in volatile markets
# - Stop taking new positions if heat > 6%
```

### Correlation Management

**Diversification**: Don't buy 5 stocks in same industry!

```python
def check_correlation(positions, correlation_matrix, max_corr=0.7):
    """Check if new position is too correlated with existing"""

    symbols = [p['symbol'] for p in positions]

    for existing_sym in symbols:
        for new_sym in symbols:
            if existing_sym != new_sym:
                corr = correlation_matrix.loc[existing_sym, new_sym]

                if corr > max_corr:
                    return False  # Too correlated

    return True  # OK to add

# Example: Don't buy NVDA, AMD, AVGO all together (all semiconductors)
# Better: NVDA (semiconductors), MSFT (software), TSLA (automotive)
```

---

## Performance Metrics

### Essential Metrics to Track

#### 1. Win Rate

```python
win_rate = winning_trades / total_trades
```

**Benchmarks:**
- Minervini/O'Neil: 50-60% (trend following)
- Weinstein: 45-55% (longer holding periods)

#### 2. Average Win / Average Loss Ratio

```python
avg_win_pct = mean([t['pnl_pct'] for t in trades if t['pnl'] > 0])
avg_loss_pct = mean([abs(t['pnl_pct']) for t in trades if t['pnl'] < 0])
win_loss_ratio = avg_win_pct / avg_loss_pct
```

**Benchmarks:**
- Minimum: 2:1 (win 2x what you lose)
- Good: 3:1 or higher
- Minervini: 4:1+ (let winners run, cut losers fast)

#### 3. Expectancy

```python
expectancy = (win_rate * avg_win) - (loss_rate * avg_loss)
```

**Interpretation:**
- Positive expectancy = profitable system
- Higher is better
- Example: (0.55 × 0.25) - (0.45 × 0.07) = 0.106 = 10.6% per trade

#### 4. Sharpe Ratio

```python
def calculate_sharpe(returns, risk_free_rate=0.02):
    """Risk-adjusted returns"""
    excess_returns = returns - (risk_free_rate / 252)  # Daily
    sharpe = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
    return sharpe
```

**Benchmarks:**
- < 1: Poor
- 1-2: Good
- 2-3: Very good
- 3+: Excellent

#### 5. Maximum Drawdown

```python
def calculate_max_drawdown(equity_curve):
    """Largest peak-to-trough decline"""
    peak = equity_curve[0]
    max_dd = 0

    for equity in equity_curve:
        if equity > peak:
            peak = equity

        drawdown = (peak - equity) / peak
        max_dd = max(max_dd, drawdown)

    return max_dd

# Example
max_dd = calculate_max_drawdown(equity_curve)
# max_dd = 0.15 = 15% maximum drawdown
```

**Benchmarks:**
- < 10%: Exceptional
- 10-20%: Good
- 20-30%: Acceptable
- > 30%: High risk

#### 6. Profit Factor

```python
gross_profit = sum([t['pnl'] for t in trades if t['pnl'] > 0])
gross_loss = abs(sum([t['pnl'] for t in trades if t['pnl'] < 0]))
profit_factor = gross_profit / gross_loss
```

**Benchmarks:**
- < 1.0: Losing system
- 1.0-1.5: Breakeven to marginal
- 1.5-2.0: Good
- 2.0+: Excellent

### Complete Performance Report

```python
def generate_performance_report(trades, equity_curve):
    """Comprehensive performance analysis"""

    winning_trades = [t for t in trades if t['pnl'] > 0]
    losing_trades = [t for t in trades if t['pnl'] < 0]

    report = {
        'Total Trades': len(trades),
        'Winning Trades': len(winning_trades),
        'Losing Trades': len(losing_trades),
        'Win Rate': len(winning_trades) / len(trades) * 100,

        'Avg Win': np.mean([t['pnl_pct'] for t in winning_trades]),
        'Avg Loss': np.mean([t['pnl_pct'] for t in losing_trades]),
        'Win/Loss Ratio': np.mean([t['pnl_pct'] for t in winning_trades]) /
                         abs(np.mean([t['pnl_pct'] for t in losing_trades])),

        'Expectancy': calculate_expectancy(trades),
        'Profit Factor': calculate_profit_factor(trades),

        'Total Return': (equity_curve[-1] - equity_curve[0]) / equity_curve[0] * 100,
        'Sharpe Ratio': calculate_sharpe(equity_curve),
        'Max Drawdown': calculate_max_drawdown(equity_curve) * 100,

        'Best Trade': max([t['pnl_pct'] for t in trades]),
        'Worst Trade': min([t['pnl_pct'] for t in trades]),

        'Avg Hold Time': np.mean([(t['exit_date'] - t['entry_date']).days
                                  for t in trades])
    }

    return report
```

---

## Common Mistakes

### 1. Not Following Your Stop Loss

**Mistake**: "I'll give it one more day..."
**Result**: 7% loss becomes 20% loss

**Solution**: Set stop orders immediately after entry

### 2. Chasing Stocks

**Mistake**: Buying stock 10% above buy point
**Result**: Poor risk/reward, often leads to loss

**Solution**: Only buy within 5% of buy point, otherwise wait for pullback

### 3. Buying Stage 4 "Bargains"

**Mistake**: "It's down 50%, must be cheap!"
**Result**: Catches falling knife, continues to fall

**Solution**: Never buy stocks in Stage 4 downtrend

### 4. Overtrading

**Mistake**: 20+ trades per week
**Result**: Commissions, slippage, emotional exhaustion

**Solution**: Quality over quantity. 2-5 high-quality setups per week

### 5. Ignoring Market Conditions

**Mistake**: Aggressively buying during market correction
**Result**: All positions stop out

**Solution**: Reduce positions during Stage 4 markets, wait for FTD

### 6. Position Size Too Large

**Mistake**: 50% of account in one stock
**Result**: Single loss destroys account

**Solution**: Max 10-20% per position, max 6-8% portfolio heat

### 7. Not Taking Partial Profits

**Mistake**: Holding for "maximum" gain, gives it all back
**Result**: 40% gain becomes 5% gain

**Solution**: Take 25-50% off at 20-25% gain, let rest run

### 8. Analysis Paralysis

**Mistake**: Studying charts forever, never pulling trigger
**Result**: Missed opportunities

**Solution**: Have a checklist, when criteria met → execute

---

## Strategy Combinations

### The "Triple Confirmation" System

Use all three strategies as filters:

**Step 1: Weinstein Stage Filter** (Universe Reduction)
```python
# Filter 1: Only Stage 2 stocks
stage_2_stocks = [s for s in universe if weinstein.analyze_stage(s).stage == Stage.STAGE_2]
# Reduces 5000 stocks → 500 stocks
```

**Step 2: O'Neil CAN SLIM Filter** (Fundamental Quality)
```python
# Filter 2: CAN SLIM score >= 5
quality_stocks = [s for s in stage_2_stocks
                 if oneil.evaluate_canslim(s).total_score >= 5]
# Reduces 500 stocks → 50 stocks
```

**Step 3: Minervini VCP Filter** (Precise Entry)
```python
# Filter 3: VCP pattern forming
vcp_stocks = [s for s in quality_stocks
             if minervini.analyze_vcp(s).is_vcp]
# Reduces 50 stocks → 5-10 stocks
```

**Result**: 5-10 highest-probability setups from universe of 5000!

### Scoring System

Assign points to create composite score:

```python
def calculate_composite_score(ohlcv, fundamentals):
    """Combine all three strategies into single score"""

    score = 0
    max_score = 100

    # Weinstein Stage Analysis (30 points)
    stage_result = weinstein.analyze_stage(ohlcv)
    if stage_result.stage == Stage.STAGE_2:
        score += 20
        if stage_result.sub_stage == '2A':
            score += 10  # Bonus for early Stage 2

    # O'Neil CAN SLIM (30 points)
    canslim = oneil.evaluate_canslim(ohlcv, fundamentals)
    score += (canslim.total_score / 7) * 30

    # Minervini VCP & Trend Template (40 points)
    trend = minervini.check_trend_template(ohlcv)
    score += (trend.score / 8) * 20

    vcp = minervini.analyze_vcp(ohlcv)
    if vcp.is_vcp:
        score += 20

    # Normalize to 0-100
    composite_score = (score / max_score) * 100

    return composite_score

# Only buy stocks with composite score > 70
```

---

## Market Conditions Adaptation

### Bull Market (Stage 2)
- **Aggressiveness**: 80-100% invested
- **Position Size**: Full size (10-20% per position)
- **Risk per Trade**: 1% standard
- **Stop Loss**: Standard (7-10%)
- **Strategy Mix**: All three strategies active

### Bull Market Under Pressure (Stage 2→3 Transition)
- **Aggressiveness**: 50-80% invested
- **Position Size**: Reduce to 5-15% per position
- **Risk per Trade**: 0.5-1%
- **Stop Loss**: Tighter (5-7%)
- **Strategy Mix**: More selective, higher scores only

### Market Correction (Stage 4)
- **Aggressiveness**: 0-30% invested (mostly cash)
- **Position Size**: Very small (5-10%)
- **Risk per Trade**: 0.25-0.5%
- **Stop Loss**: Very tight (3-5%)
- **Strategy Mix**: Wait for Follow-Through Day

### Bear Market (Stage 4 Extended)
- **Aggressiveness**: 0% invested (100% cash)
- **Position Size**: N/A
- **Risk per Trade**: N/A
- **Stop Loss**: N/A
- **Strategy Mix**: Watch, wait, and learn

### Dynamic Allocation

```python
def adjust_for_market(market_stage):
    """Adjust strategy parameters based on market stage"""

    if market_stage == 'BULL':
        return {
            'max_positions': 10,
            'position_size': 0.15,  # 15% per position
            'risk_per_trade': 0.01,
            'min_score': 60
        }

    elif market_stage == 'BULL_UNDER_PRESSURE':
        return {
            'max_positions': 5,
            'position_size': 0.10,
            'risk_per_trade': 0.0075,
            'min_score': 70
        }

    elif market_stage == 'CORRECTION':
        return {
            'max_positions': 2,
            'position_size': 0.05,
            'risk_per_trade': 0.005,
            'min_score': 80
        }

    else:  # BEAR MARKET
        return {
            'max_positions': 0,
            'position_size': 0,
            'risk_per_trade': 0,
            'min_score': 100  # Essentially no trades
        }
```

---

## Automation & Scanning

### Daily Scan Workflow

**Morning (Before Market Open):**
1. Update all stock data
2. Run Weinstein stage analysis on universe
3. Filter for Stage 2A and 2B stocks only
4. Check overnight news for existing positions

**Midday (Market Hours):**
1. Monitor existing positions for stop hits
2. Scan for breakouts (volume + price)
3. Check watchlist for entry signals

**Evening (After Market Close):**
1. Update positions with today's close
2. Run full strategy scans
3. Generate watchlist for tomorrow
4. Review trades and update journal

### Automated Scanner Example

```python
class StrategyScanner:
    """Automated stock scanner using all three strategies"""

    def __init__(self, universe):
        self.universe = universe
        self.minervini = MinerviniStrategy()
        self.oneil = ONeilStrategy()
        self.weinstein = WeinsteinStrategy()

    def scan_daily(self):
        """Daily scan for new opportunities"""

        results = []

        for symbol in self.universe:
            try:
                # Get data
                ohlcv = get_ohlcv(symbol)
                fundamentals = get_fundamentals(symbol)

                # Quick filters
                if len(ohlcv) < 252:
                    continue  # Need 1 year minimum

                if ohlcv['close'].iloc[-1] < 10:
                    continue  # Skip penny stocks

                if ohlcv['volume'].iloc[-1] < 500000:
                    continue  # Need minimum liquidity

                # Strategy analysis
                stage = self.weinstein.analyze_stage(ohlcv)

                # Only Stage 2
                if stage.stage.name != 'STAGE_2_ADVANCING':
                    continue

                # Check other criteria
                trend = self.minervini.check_trend_template(ohlcv)
                canslim = self.oneil.evaluate_canslim(ohlcv, fundamentals)
                vcp = self.minervini.analyze_vcp(ohlcv)

                # Calculate score
                score = self.calculate_score(trend, canslim, vcp, stage)

                if score >= 70:  # Threshold
                    results.append({
                        'symbol': symbol,
                        'score': score,
                        'stage': stage.sub_stage,
                        'trend_score': trend.score,
                        'canslim_score': canslim.total_score,
                        'has_vcp': vcp.is_vcp,
                        'price': ohlcv['close'].iloc[-1]
                    })

            except Exception as e:
                print(f"Error scanning {symbol}: {e}")
                continue

        # Sort by score
        results = sorted(results, key=lambda x: x['score'], reverse=True)

        return results[:20]  # Top 20 ideas

    def calculate_score(self, trend, canslim, vcp, stage):
        """Composite scoring"""
        score = 0

        # Weinstein (30 pts)
        if stage.stage.name == 'STAGE_2_ADVANCING':
            score += 20
            if stage.sub_stage == '2A':
                score += 10

        # O'Neil (30 pts)
        score += (canslim.total_score / 7) * 30

        # Minervini (40 pts)
        score += (trend.score / 8) * 25
        if vcp.is_vcp:
            score += 15

        return min(100, score)
```

---

## Final Checklist

Before going live with any strategy:

- [ ] Backtest on at least 5 years of data
- [ ] Test across different market conditions
- [ ] Verify positive expectancy
- [ ] Confirm Sharpe ratio > 1
- [ ] Check max drawdown is acceptable
- [ ] Test with realistic slippage/commissions
- [ ] Validate on out-of-sample data
- [ ] Paper trade for 2-3 months
- [ ] Start with small position sizes
- [ ] Have clear written rules
- [ ] Set up risk management systems
- [ ] Prepare for drawdown periods
- [ ] Keep a trading journal
- [ ] Review and adapt regularly

---

*Remember: Perfect execution of an average strategy beats poor execution of a perfect strategy.*

**Good luck and trade safely!**
