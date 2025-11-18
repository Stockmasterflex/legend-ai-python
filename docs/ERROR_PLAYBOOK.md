# Error Handling Playbook

**Legend AI Error Handling and Debugging Guide**

This playbook helps you debug issues 10x faster by providing structured approaches to common errors, monitoring strategies, and recovery procedures.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Error Categories](#error-categories)
3. [Common Errors & Solutions](#common-errors--solutions)
4. [Debugging Workflows](#debugging-workflows)
5. [Error Monitoring](#error-monitoring)
6. [Recovery Strategies](#recovery-strategies)
7. [API Reference](#api-reference)

---

## Quick Start

### Understanding an Error

When you encounter an error in Legend AI, it will contain:

```json
{
  "error": "MarketDataError",
  "message": "Unable to fetch market data",
  "category": "external",
  "severity": "high",
  "retryable": true,
  "details": {...},
  "recovery_hint": "Market data service may be temporarily unavailable...",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

**Key Fields:**
- **category**: Type of error (validation, external, data, etc.)
- **severity**: Impact level (low, medium, high, critical)
- **retryable**: Whether retrying might succeed
- **recovery_hint**: Actionable next steps

### Finding Error Logs

```bash
# View all errors in the last hour
grep "ERROR" logs/app.log | tail -100

# View specific error type
grep "MarketDataError" logs/app.log

# View error aggregation stats
curl http://localhost:8000/api/errors/stats
```

---

## Error Categories

### 1. **Validation Errors** (Category: `validation`)

**What**: Invalid user input or parameters
**Severity**: Low
**Retryable**: No (fix input first)

Common examples:
- Invalid ticker symbol
- Invalid time interval
- Missing required parameters
- Out-of-range values

**Recovery**:
1. Check error `details` field for specific validation failure
2. Correct input and retry
3. No need to wait or retry with same input

---

### 2. **External Service Errors** (Category: `external`)

**What**: Third-party API or service failures
**Severity**: High
**Retryable**: Yes (usually)

#### 2.1 Market Data Errors

```python
MarketDataError: Unable to fetch market data
```

**Possible Causes**:
- API rate limit exceeded
- API service down
- Network connectivity issue
- Invalid API key

**Debug Steps**:
1. Check API usage stats:
   ```bash
   curl http://localhost:8000/api/market/internals
   # Look at "api_usage" section
   ```

2. Check which data source failed:
   ```bash
   grep "TwelveData\|Finnhub\|Yahoo" logs/app.log | tail -20
   ```

3. Verify API keys configured:
   ```bash
   env | grep -i "api_key\|twelve\|finnhub"
   ```

**Recovery**:
- If rate limited: Wait for quota reset (shown in logs)
- If network error: Retry in 30-60 seconds
- If API key invalid: Update configuration
- System automatically falls back to alternate data sources

#### 2.2 Rate Limit Errors

```python
RateLimitError: Rate limit exceeded
```

**Debug Steps**:
1. Check current usage:
   ```bash
   redis-cli GET api_usage:twelvedata
   redis-cli GET api_usage:finnhub
   ```

2. Check when quota resets:
   ```bash
   grep "rate_limit\|quota" logs/app.log | tail -10
   ```

**Recovery**:
- Wait for automatic quota reset (midnight UTC for daily limits)
- Use different data source if available
- Upgrade API plan if hitting limits frequently

#### 2.3 Timeout Errors

```python
TimeoutError: Request timed out
```

**Possible Causes**:
- External API slow response
- Large data request
- Network latency

**Recovery**:
- Automatic retry with exponential backoff (up to 3 attempts)
- Reduce data request size
- Check network connectivity

---

### 3. **Data Processing Errors** (Category: `data`)

#### 3.1 Insufficient Data

```python
InsufficientDataError: Not enough data for analysis
```

**Causes**:
- Stock newly listed
- Limited historical data available
- Data gaps in source

**Debug Steps**:
```bash
# Check how much data we got
grep "Insufficient data\|data points" logs/app.log | grep TICKER_SYMBOL
```

**Recovery**:
- Try shorter time period
- Use different interval (daily instead of intraday)
- Accept that some newly listed stocks can't be analyzed

#### 3.2 Malformed Data

```python
DataTransformError: Unable to process data
MalformedDataError: Data format error
```

**Causes**:
- API returned unexpected format
- Missing required fields
- Data type mismatch

**Debug Steps**:
```bash
# Check raw API responses
grep "API response\|raw_data" logs/app.log | tail -5

# Check data transformation errors
grep "DataTransformError\|MalformedDataError" logs/app.log
```

**Recovery**:
- Automatic fallback to alternative data source
- Report issue if persistent with specific ticker

---

### 4. **Pattern Detection Errors** (Category: `data`)

```python
PatternDetectionError: Pattern analysis failed
DetectorExecutionError: Error during pattern detector execution
```

**Causes**:
- Insufficient data points for pattern
- Numerical instability (RANSAC, statistics)
- Invalid parameters

**Debug Steps**:
```bash
# Check which detector failed
grep "detector.*failed\|PatternDetectionError" logs/app.log

# Check data quality
curl http://localhost:8000/api/analyze?ticker=AAPL | jq '.ohlcv | length'
```

**Recovery**:
- Errors are logged but don't stop analysis
- System continues with other patterns
- Check logs for pattern: `detector_.*_failed`

---

### 5. **Configuration Errors** (Category: `configuration`)

```python
ConfigurationError: System configuration error
MissingAPIKeyError: API credentials not configured
```

**Severity**: Critical
**Retryable**: No (fix config first)

**Debug Steps**:
```bash
# Check environment variables
env | grep -i "redis\|api_key\|telegram"

# Check config loading
grep "config\|settings\|environment" logs/app.log | head -20
```

**Recovery**:
1. Verify all required environment variables set:
   - `REDIS_URL`
   - `TWELVEDATA_API_KEY` (optional but recommended)
   - `FINNHUB_API_KEY` (optional fallback)
   - `TELEGRAM_BOT_TOKEN` (if using Telegram)

2. Restart application after config changes

---

### 6. **Cache Errors** (Category: `transient`)

```python
CacheError: Cache operation error
```

**Severity**: Low
**Retryable**: Yes

**Causes**:
- Redis connection failure
- Redis out of memory
- Network issue

**Debug Steps**:
```bash
# Check Redis connection
redis-cli PING

# Check Redis memory
redis-cli INFO memory

# Check cache service health
curl http://localhost:8000/health | jq '.cache'
```

**Recovery**:
- System operates without cache (degraded performance)
- Check Redis service status
- Clear cache if corrupted: `redis-cli FLUSHDB`

---

## Debugging Workflows

### Workflow 1: API Endpoint Returns 500 Error

```
Error: HTTP 500 Internal Server Error
```

**Steps**:

1. **Get Request ID** (if using structured logging):
   ```bash
   grep "request_id=abc123" logs/app.log
   ```

2. **Find the error**:
   ```bash
   grep "ERROR\|EXCEPTION" logs/app.log | tail -50
   ```

3. **Check error aggregation**:
   ```bash
   curl http://localhost:8000/api/errors/stats | jq '.top_errors'
   ```

4. **Identify category**:
   - External? → Check API status
   - Data? → Check data quality
   - Internal? → Check stack trace

5. **Review error context**:
   ```bash
   grep "error_context" logs/app.log | tail -10 | jq
   ```

### Workflow 2: Scan Returns No Results

```
Scan completed but found 0 stocks
```

**Steps**:

1. **Check universe size**:
   ```bash
   curl http://localhost:8000/api/universe/stats
   ```

2. **Check pattern detector status**:
   ```bash
   grep "detector.*registered" logs/app.log
   ```

3. **Run single ticker test**:
   ```bash
   curl "http://localhost:8000/api/analyze?ticker=AAPL" | jq
   ```

4. **Check data availability**:
   ```bash
   grep "market_data.*AAPL" logs/app.log
   ```

5. **Review scan parameters**:
   - Score threshold too high?
   - Universe filtered too aggressively?

### Workflow 3: Slow Response Times

```
Requests taking >10 seconds
```

**Steps**:

1. **Check operation duration**:
   ```bash
   grep "duration_ms" logs/app.log | awk '{print $NF}' | sort -n | tail -20
   ```

2. **Identify slow operations**:
   ```bash
   grep "duration_ms.*[0-9]{4,}" logs/app.log  # >1000ms
   ```

3. **Check cache hit rate**:
   ```bash
   curl http://localhost:8000/health | jq '.cache.stats.redis_hit_rate'
   ```

4. **Check external API latency**:
   ```bash
   grep "API.*duration\|external.*time" logs/app.log
   ```

5. **Optimize**:
   - Increase cache TTL
   - Enable request timeout
   - Use circuit breaker for failing services

---

## Error Monitoring

### Real-Time Monitoring

```bash
# Watch error rate
watch -n 5 'grep "ERROR" logs/app.log | tail -20'

# Monitor specific error types
watch -n 5 'curl -s http://localhost:8000/api/errors/stats | jq ".top_errors"'

# Monitor API health
watch -n 10 'curl -s http://localhost:8000/health | jq ".status"'
```

### Error Aggregation API

**Get Error Statistics**:
```bash
GET /api/errors/stats
```

Response:
```json
{
  "total_groups": 5,
  "total_errors": 127,
  "top_errors": [
    {
      "type": "MarketDataError",
      "occurrences": 45,
      "fingerprint": "a3b2c1d4",
      "last_seen": "2025-01-15T10:30:00Z"
    }
  ]
}
```

**Get Error Groups**:
```bash
GET /api/errors/groups
```

Returns all error groups with samples for investigation.

### Metrics (Prometheus)

```bash
# Error counters
curl http://localhost:8000/metrics | grep error_total

# Example output:
# scan_errors_total 12
# analyze_errors_total 8
```

---

## Recovery Strategies

### Automatic Recovery

The system includes built-in recovery mechanisms:

1. **Retry with Exponential Backoff**
   - Automatically retries transient failures
   - Up to 3 attempts by default
   - Delays: 1s, 2s, 4s

2. **Circuit Breaker**
   - Stops calling failing services
   - Prevents cascade failures
   - Auto-recovers after timeout

3. **Multi-Source Fallback**
   - Market data: TwelveData → Finnhub → Yahoo
   - Automatic failover on errors

4. **Graceful Degradation**
   - Cache errors: Continue without cache
   - Single detector failure: Continue with other detectors
   - Missing optional data: Proceed with available data

### Manual Recovery

**Clear All Caches**:
```bash
redis-cli FLUSHDB
```

**Reset API Usage Counters**:
```bash
redis-cli DEL api_usage:twelvedata
redis-cli DEL api_usage:finnhub
```

**Restart Services**:
```bash
# Application
systemctl restart legend-ai

# Redis
systemctl restart redis
```

**Force Universe Reseed**:
```bash
curl -X POST http://localhost:8000/api/universe/reseed
```

---

## API Reference

### Custom Exception Classes

```python
from app.core.errors import (
    MarketDataError,
    RateLimitError,
    InsufficientDataError,
    PatternDetectionError,
    ValidationError,
)

# Usage
try:
    data = await fetch_market_data(ticker)
except MarketDataError as e:
    # Error already logged and aggregated
    # e.user_message - User-friendly message
    # e.recovery_hint - Actionable guidance
    # e.to_dict() - Full error details
```

### Error Context Manager

```python
from app.core.errors import error_context

# Automatic error handling with context
with error_context("fetch_market_data", ticker="AAPL"):
    data = await fetch_data()
    # Errors automatically:
    # - Logged with context
    # - Aggregated
    # - Wrapped in appropriate exception
```

### Decorators

```python
from app.core.errors import handle_errors
from app.core.error_recovery import with_retry, with_circuit_breaker

# Error handling
@handle_errors(error_class=MarketDataError)
async def fetch_prices(ticker: str):
    return await api_call(ticker)

# Retry logic
@with_retry(max_attempts=5)
async def fetch_with_retry(ticker: str):
    return await api_call(ticker)

# Circuit breaker
@with_circuit_breaker("twelvedata_api")
async def fetch_from_twelvedata(ticker: str):
    return await api_call(ticker)
```

### Error Aggregator

```python
from app.core.errors import error_aggregator

# Capture exception
try:
    risky_operation()
except Exception as exc:
    fingerprint = error_aggregator.capture_exception(
        exc,
        context=ErrorContext(category=ErrorCategory.EXTERNAL),
        extra={"ticker": "AAPL"}
    )

# Get statistics
stats = error_aggregator.get_stats()
# {
#   "total_groups": 5,
#   "total_errors": 127,
#   "top_errors": [...]
# }

# Get all groups
groups = error_aggregator.get_groups()
```

---

## Best Practices

### 1. Always Use Specific Exception Types

❌ **Bad**:
```python
except Exception:
    pass
```

✅ **Good**:
```python
except (MarketDataError, TimeoutError) as e:
    logger.exception("Market data fetch failed", extra={"ticker": ticker})
    raise
```

### 2. Add Context to Errors

❌ **Bad**:
```python
raise Exception("Failed")
```

✅ **Good**:
```python
raise MarketDataError(
    "Failed to fetch market data",
    technical_details={"ticker": ticker, "source": source},
    recovery_hint="Try again in a few moments or check API status"
)
```

### 3. Use logger.exception() for Errors

❌ **Bad**:
```python
except Exception as e:
    logger.error(f"Error: {e}")
```

✅ **Good**:
```python
except Exception as e:
    logger.exception("Operation failed with error", extra={"context": "value"})
    # Automatically includes stack trace
```

### 4. Implement Graceful Degradation

✅ **Good**:
```python
try:
    spy_data = await fetch_spy_data()
except MarketDataError:
    logger.warning("SPY data unavailable, continuing without it")
    spy_data = None  # Continue with degraded functionality
```

### 5. Use Error Aggregation

✅ **Good**:
```python
from app.core.errors import error_aggregator, error_context

with error_context("pattern_detection", ticker=ticker):
    patterns = detector.detect(data)
    # Errors automatically aggregated for monitoring
```

---

## Troubleshooting Checklist

### Service Won't Start

- [ ] Check environment variables configured
- [ ] Check Redis running: `redis-cli PING`
- [ ] Check port 8000 not in use: `lsof -i :8000`
- [ ] Check logs: `tail -100 logs/app.log`
- [ ] Verify Python dependencies: `pip list | grep -i "fastapi\|redis"`

### No Data Returned

- [ ] Check API keys configured
- [ ] Check API usage not exceeded: `/api/market/internals`
- [ ] Test single ticker: `/api/analyze?ticker=AAPL`
- [ ] Check cache status: `redis-cli INFO`
- [ ] Verify universe loaded: `/api/universe/stats`

### High Error Rate

- [ ] Check error aggregation: `/api/errors/stats`
- [ ] Review top errors in logs
- [ ] Check external service status
- [ ] Verify rate limits not exceeded
- [ ] Check Redis memory: `redis-cli INFO memory`

### Performance Issues

- [ ] Check cache hit rate: `/health`
- [ ] Monitor operation durations in logs
- [ ] Check external API latency
- [ ] Review timeout settings
- [ ] Consider scaling Redis

---

## Support Resources

- **Logs**: `/var/log/legend-ai/` or `logs/app.log`
- **Health Check**: `http://localhost:8000/health`
- **Error Stats**: `http://localhost:8000/api/errors/stats`
- **Metrics**: `http://localhost:8000/metrics` (Prometheus)
- **Documentation**: `docs/`

---

**Last Updated**: 2025-01-15
**Version**: 1.0
**Maintained By**: Legend AI Team
