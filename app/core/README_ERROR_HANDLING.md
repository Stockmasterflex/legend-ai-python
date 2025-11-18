# Error Handling System

**Structured, Actionable Error Handling for Legend AI**

## Overview

This error handling system provides:
- ✅ Custom exception hierarchy with context
- ✅ Sentry-style error aggregation
- ✅ Automatic retry with exponential backoff
- ✅ Circuit breaker pattern for external services
- ✅ Structured logging with full context
- ✅ User-friendly error messages
- ✅ Recovery hints for debugging

## Quick Start

### Using Custom Exceptions

```python
from app.core.errors import MarketDataError, InsufficientDataError

# Raise with context
raise MarketDataError(
    "Failed to fetch price data",
    user_message="Market data temporarily unavailable",
    technical_details={"ticker": "AAPL", "source": "TwelveData"},
    recovery_hint="Try again in a few moments"
)
```

### Using Error Context Manager

```python
from app.core.errors import error_context, MarketDataError

# Automatic error handling
with error_context("fetch_market_data", ticker="AAPL", source="TwelveData"):
    data = await fetch_data()
    # Errors are automatically:
    # - Logged with full context
    # - Aggregated for monitoring
    # - Wrapped in MarketDataError
```

### Using Decorators

```python
from app.core.errors import handle_errors
from app.core.error_recovery import with_retry, with_circuit_breaker

# Automatic error handling
@handle_errors(error_class=MarketDataError)
async def fetch_prices(ticker: str):
    return await api_call(ticker)

# Automatic retry on failure
@with_retry(config=RetryConfig(max_attempts=5))
async def fetch_with_retry(ticker: str):
    return await api_call(ticker)

# Circuit breaker protection
@with_circuit_breaker("twelvedata_api")
async def fetch_from_twelvedata(ticker: str):
    return await api_call(ticker)
```

## Exception Hierarchy

```
LegendAIError (base)
├── ValidationError
│   ├── InvalidTickerError
│   ├── InvalidIntervalError
│   └── InvalidParameterError
├── ExternalServiceError
│   ├── MarketDataError
│   ├── RateLimitError
│   ├── APIQuotaExceededError
│   ├── NetworkError
│   └── TimeoutError
├── DataError
│   ├── InsufficientDataError
│   ├── DataTransformError
│   └── MalformedDataError
├── PatternDetectionError
│   ├── DetectorNotFoundError
│   └── DetectorExecutionError
├── ConfigurationError
│   ├── MissingAPIKeyError
│   └── InvalidConfigurationError
└── CacheError
```

## Error Aggregation

Errors are automatically grouped by fingerprint (exception type + stack trace):

```python
from app.core.errors import error_aggregator

# Get statistics
stats = error_aggregator.get_stats()
# {
#   "total_groups": 5,
#   "total_errors": 127,
#   "top_errors": [
#     {"type": "MarketDataError", "occurrences": 45, ...}
#   ]
# }

# Get error groups
groups = error_aggregator.get_groups()
```

## Retry Logic

```python
from app.core.error_recovery import with_retry, RetryConfig

# Configure retry behavior
config = RetryConfig(
    max_attempts=5,
    initial_delay=1.0,  # seconds
    max_delay=60.0,
    exponential_base=2.0,
    jitter=True,
    retryable_errors=(ExternalServiceError, NetworkError)
)

@with_retry(config=config)
async def fetch_data():
    return await risky_operation()
```

## Circuit Breaker

Prevents cascade failures by temporarily stopping calls to failing services:

```python
from app.core.error_recovery import with_circuit_breaker, CircuitBreakerConfig

config = CircuitBreakerConfig(
    failure_threshold=5,  # Open after 5 failures
    success_threshold=2,  # Close after 2 successes in half-open
    timeout=60.0,  # Wait 60s before half-open
    half_open_max_calls=3
)

@with_circuit_breaker("my_service", config=config)
async def call_external_service():
    return await api_call()
```

**States**:
- **CLOSED**: Normal operation
- **OPEN**: Service failing, rejecting all calls
- **HALF_OPEN**: Testing if service recovered

## API Endpoints

### Get Error Statistics
```bash
GET /api/errors/stats
```

### Get Error Groups
```bash
GET /api/errors/groups
```

### Get Circuit Breaker States
```bash
GET /api/errors/circuits
```

### Get Service Health
```bash
GET /api/errors/health
```

## Best Practices

### 1. Use Specific Exception Types

```python
# ❌ Bad
raise Exception("Failed")

# ✅ Good
raise MarketDataError(
    "Failed to fetch data",
    technical_details={"ticker": ticker},
    recovery_hint="Check API status"
)
```

### 2. Always Add Context

```python
# ❌ Bad
try:
    data = fetch()
except Exception as e:
    logger.error("Failed")

# ✅ Good
with error_context("fetch_data", ticker="AAPL"):
    data = fetch()
```

### 3. Use logger.exception()

```python
# ❌ Bad
except Exception as e:
    logger.error(f"Error: {e}")

# ✅ Good
except Exception as e:
    logger.exception("Operation failed", extra={"ticker": ticker})
```

### 4. Provide Recovery Hints

```python
# ✅ Good
raise RateLimitError(
    "API rate limit exceeded",
    recovery_hint="Wait 60s for quota reset or upgrade your plan"
)
```

## Files

- `app/core/errors.py` - Exception classes, error context, aggregation
- `app/core/error_recovery.py` - Retry logic, circuit breakers, health monitoring
- `app/api/errors.py` - Error monitoring API endpoints
- `docs/ERROR_PLAYBOOK.md` - Comprehensive debugging guide

## Examples

See `docs/ERROR_PLAYBOOK.md` for:
- Common error scenarios
- Debugging workflows
- Recovery procedures
- Troubleshooting checklist

## Testing

```bash
# Run syntax check
python -m py_compile app/core/errors.py app/core/error_recovery.py

# Test application startup
uvicorn app.main:app --reload

# Check error endpoints
curl http://localhost:8000/api/errors/stats
```

---

**Debug issues 10x faster with structured, actionable errors!**
