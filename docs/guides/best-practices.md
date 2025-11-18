# Best Practices

## 🎯 Pattern Detection

### Use Appropriate Timeframes

```python
# Daily for swing trading
pattern = client.patterns.detect("AAPL", interval="1day")

# Weekly for position trading
pattern = client.patterns.detect("AAPL", interval="1week")

# Hourly for day trading
pattern = client.patterns.detect("AAPL", interval="1hour")
```

### Validate Pattern Scores

```python
# Only consider high-quality setups
pattern = client.patterns.detect("AAPL")
if pattern.score >= 7.5:
    # High-quality setup
    print(f"Good setup: {pattern.pattern}")
else:
    # Skip low-quality patterns
    print("Pattern score too low, skipping")
```

### Check Risk/Reward Ratio

```python
# Look for favorable risk/reward
if pattern.risk_reward_ratio >= 2.0:
    print(f"Good R:R of {pattern.risk_reward_ratio:.1f}R")
else:
    print("Risk/reward not favorable")
```

## 📊 Universe Scanning

### Filter Aggressively

```python
# High-quality setups only
results = client.universe.scan(
    universe="SP500",
    min_score=8.0,  # Only top-tier setups
    max_results=10,  # Focus on best opportunities
    pattern_types=["VCP", "Cup and Handle"]  # Specific patterns
)
```

### Scan Regularly

```python
# Daily scan for new setups
import schedule

def daily_scan():
    results = client.universe.scan(min_score=8.0, max_results=20)
    for result in results:
        if result not in watchlist:
            client.watchlist.add(
                ticker=result.ticker,
                reason=f"{result.pattern} - Score: {result.score}"
            )

schedule.every().day.at("16:00").do(daily_scan)  # After market close
```

### Use Caching Wisely

```python
# Results are cached for 1 hour
# Don't spam the same scan
results = client.universe.scan()  # Fresh scan
results = client.universe.scan()  # Cached (instant)

# Wait 1+ hours for fresh data
```

## ⚖️ Risk Management

### Always Use the 2% Rule

```python
# Never risk more than 2% on a single trade
position = client.risk.calculate_position(
    account_size=10000,
    entry_price=175.50,
    stop_loss_price=170.25,
    risk_percentage=2.0  # 2% max
)
```

### Calculate Before Trading

```python
# Full trade workflow
pattern = client.patterns.detect("AAPL")

position = client.risk.calculate_position(
    account_size=10000,
    entry_price=pattern.entry,
    stop_loss_price=pattern.stop,
    target_price=pattern.target
)

# Now you know exactly how many shares to buy
print(f"Buy {position.position_size} shares")
print(f"Risk: ${position.risk_amount:.2f} ({position.risk_amount/10000*100:.1f}%)")
```

### Consider Kelly Criterion

```python
# Use Kelly Criterion for position sizing
position = client.risk.calculate_position(...)
if position.kelly_criterion:
    # Kelly suggests optimal position size
    print(f"Kelly Criterion: {position.kelly_criterion:.2%}")
```

## 🤖 AI Assistant

### Provide Context

```python
# Better: Include symbol for context
response = client.ai.chat(
    "Should I buy now?",
    symbol="AAPL",
    include_market_data=True
)

# Worse: Generic question
response = client.ai.chat("Should I buy stocks?")
```

### Use for Education

```python
# Learn about patterns
response = client.ai.chat("What is a VCP pattern and how do I trade it?")

# Understand indicators
response = client.ai.chat("How does RSI work?")

# Market context
response = client.ai.chat("What's the current market regime?")
```

### Don't Rely Solely on AI

```python
# Good: AI + your analysis
ai_view = client.ai.analyze("AAPL")
pattern = client.patterns.detect("AAPL")
# Make decision based on both + your research

# Bad: Blindly following AI
ai_view = client.ai.analyze("AAPL")
# Buy immediately without verification
```

## 📱 Watchlist Management

### Organize by Status

```python
# Keep watchlist organized
items = client.watchlist.list()

watching = [i for i in items if i.status == "Watching"]
triggered = [i for i in items if i.status == "Triggered"]

# Review triggered setups first
for item in triggered:
    print(f"{item.ticker} has triggered!")
```

### Set Clear Targets

```python
# Always set entry and stop
client.watchlist.add(
    ticker="NVDA",
    reason="VCP - tight contraction",
    target_entry=450.0,  # Clear entry
    target_stop=440.0,   # Clear stop
)
```

### Clean Up Regularly

```python
# Remove completed or failed setups
items = client.watchlist.list()
for item in items:
    if item.status in ["Completed", "Skipped"]:
        client.watchlist.remove(item.ticker)
```

## 🔄 Caching

### Understand Cache TTLs

- **Pattern Detection**: 1 hour
- **Market Data**: 15 minutes
- **Charts**: 2 hours
- **Universe Scans**: 1 hour

```python
# First call: Fresh data (cached for 1 hour)
pattern = client.patterns.detect("AAPL")

# Within 1 hour: Instant from cache
pattern = client.patterns.detect("AAPL")

# After 1+ hour: Fresh data again
```

### Force Fresh Data

```python
# For time-sensitive data, wait for cache to expire
# Or use different parameters to bypass cache
pattern1 = client.patterns.detect("AAPL", interval="1day")
pattern2 = client.patterns.detect("AAPL", interval="1hour")  # Different cache key
```

## 🚨 Error Handling

### Always Handle Errors

```python
from legend_ai import APIError, RateLimitError, ValidationError

try:
    pattern = client.patterns.detect(ticker)
except RateLimitError:
    # Wait and retry
    time.sleep(60)
    pattern = client.patterns.detect(ticker)
except ValidationError as e:
    # Fix input
    print(f"Invalid input: {e}")
except APIError as e:
    # Log and alert
    logger.error(f"API error: {e}")
```

### Implement Retries

```python
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def get_pattern(ticker):
    return client.patterns.detect(ticker)

pattern = get_pattern("AAPL")  # Auto-retries on failure
```

## 📊 Performance

### Batch Operations

```python
# Good: Scan once, get multiple results
results = client.universe.scan(max_results=50)

# Bad: Individual calls for each stock
for ticker in ['AAPL', 'MSFT', 'GOOGL', ...]:
    pattern = client.patterns.detect(ticker)  # Slow!
```

### Use Async for Concurrency

```python
import asyncio
from legend_ai import AsyncLegendAI

async def scan_multiple():
    async with AsyncLegendAI() as client:
        # Run multiple requests concurrently
        tasks = [
            client.patterns.detect("AAPL"),
            client.patterns.detect("MSFT"),
            client.patterns.detect("GOOGL"),
        ]
        results = await asyncio.gather(*tasks)
        return results

patterns = asyncio.run(scan_multiple())
```

## 🔐 Security

### Don't Hardcode API Keys

```python
# Good: Use environment variables
import os
client = LegendAI(api_key=os.getenv("LEGEND_API_KEY"))

# Bad: Hardcoded
client = LegendAI(api_key="sk-...")  # Never do this!
```

### Use HTTPS

```python
# Good: HTTPS (default)
client = LegendAI(base_url="https://...")

# Bad: HTTP (insecure)
client = LegendAI(base_url="http://...")  # Avoid
```

## 📈 Trading Workflow

### Complete Pattern-to-Trade Workflow

```python
# 1. Scan for setups
results = client.universe.scan(min_score=8.0, max_results=10)

# 2. Analyze top candidates
for result in results[:3]:
    # Get detailed pattern
    pattern = client.patterns.detect(result.ticker)

    # Calculate position size
    position = client.risk.calculate_position(
        account_size=10000,
        entry_price=pattern.entry,
        stop_loss_price=pattern.stop,
        target_price=pattern.target
    )

    # Get AI insight
    ai_view = client.ai.analyze(result.ticker)

    # Add to watchlist
    client.watchlist.add(
        ticker=result.ticker,
        reason=f"{pattern.pattern} - Score: {pattern.score}",
        target_entry=pattern.entry,
        target_stop=pattern.stop
    )

    print(f"{result.ticker}: Buy {position.position_size} @ ${pattern.entry}")

# 3. Execute and track
# ... (manual execution in your broker)

# 4. Log the trade
trade = client.trades.create(
    ticker="AAPL",
    entry_price=175.50,
    stop_loss=170.25,
    target_price=185.00,
    position_size=50
)
```

## 🎓 Learning from Data

### Track Your Performance

```python
# Log all trades
for ticker, entry, stop in my_trades:
    client.trades.create(
        ticker=ticker,
        entry_price=entry,
        stop_loss=stop
    )

# Analyze later
performance = client.analytics.performance()
print(f"Win rate: {performance['win_rate']}")
print(f"Average R: {performance['avg_r']}")
```

## ⚠️ Common Pitfalls

### ❌ Don't Over-Trade

```python
# Bad: Trading every pattern
results = client.universe.scan(min_score=5.0)  # Too low!
for result in results:
    execute_trade(result)  # Trading quantity over quality

# Good: Be selective
results = client.universe.scan(min_score=8.5)  # High quality only
# Trade only your best 2-3 setups
```

### ❌ Don't Ignore Stop Losses

```python
# Bad: Ignoring stop loss
pattern = client.patterns.detect("AAPL")
# Buy at entry but don't set stop loss

# Good: Always use stops
pattern = client.patterns.detect("AAPL")
execute_trade(
    entry=pattern.entry,
    stop=pattern.stop,  # Always set stop!
    target=pattern.target
)
```

### ❌ Don't Chase

```python
# Bad: Buying after breakout
pattern = client.patterns.detect("AAPL")
current_price = get_current_price("AAPL")
if current_price > pattern.entry + 5:  # Already broke out
    buy()  # Chasing!

# Good: Buy at entry or skip
if current_price <= pattern.entry:
    set_limit_order(pattern.entry)
else:
    skip()  # Wait for next setup
```

## 📚 Resources

- [API Documentation](/docs)
- [GitHub Examples](https://github.com/Stockmasterflex/legend-ai-python/tree/main/docs/examples)
- [OpenAPI Specification](../api/openapi-full.yaml)
