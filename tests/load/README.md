# Load Testing & Performance Baseline

## Overview

Comprehensive load testing and performance monitoring for Legend AI.

## Quick Start

### Run Performance Baseline
```bash
# Establish baseline metrics
python tests/load/performance_baseline.py

# Against production
BASE_URL=https://your-app.railway.app python tests/load/performance_baseline.py
```

### Run Load Tests
```bash
# Run all load test scenarios
./tests/load/run_load_tests.sh

# Against production
BASE_URL=https://your-app.railway.app ./tests/load/run_load_tests.sh
```

### Run Single Locust Test
```bash
# Interactive mode with web UI
locust -f tests/load/locustfile.py --host=http://localhost:8000

# Then open: http://localhost:8089

# Headless mode
locust -f tests/load/locustfile.py \
    --host=http://localhost:8000 \
    --users=50 \
    --spawn-rate=5 \
    --run-time=2m \
    --headless
```

## Test Scenarios

### 1. Performance Baseline
**Purpose:** Establish baseline metrics for all critical endpoints

**Endpoints Tested:**
- `/health` - Health check (target: <100ms p95)
- `/api/version` - Version info (target: <100ms p95)
- `/api/watchlist` - Watchlist retrieval (target: <500ms p95)
- `/api/analyze` - Pattern analysis (target: <2000ms p95)
- `/api/scan` - Universe scan (target: <5000ms p95)
- `/health/detailed` - Detailed health (target: <500ms p95)
- `/api/market/quote` - Market quote (target: <1000ms p95)

**Metrics Collected:**
- Minimum response time
- Maximum response time
- Mean response time
- Median response time
- Standard deviation
- 95th percentile (P95)
- 99th percentile (P99)
- Success rate
- Error count

**Usage:**
```bash
python tests/load/performance_baseline.py
```

**Output:**
- Console table with results
- JSON file: `tests/load/results/baseline.json`
- Threshold validation report

### 2. Load Test Scenarios

#### Baseline Performance (10 users)
- **Users:** 10 concurrent
- **Spawn Rate:** 2/sec
- **Duration:** 2 minutes
- **Purpose:** Light load baseline

#### Normal Load (50 users)
- **Users:** 50 concurrent
- **Spawn Rate:** 5/sec
- **Duration:** 3 minutes
- **Purpose:** Expected daily traffic

#### Peak Load (100 users)
- **Users:** 100 concurrent
- **Spawn Rate:** 10/sec
- **Duration:** 2 minutes
- **Purpose:** High traffic periods

#### Stress Test (200 users)
- **Users:** 200 concurrent
- **Spawn Rate:** 20/sec
- **Duration:** 2 minutes
- **Purpose:** Find breaking point

#### Spike Test (500 users)
- **Users:** 500 concurrent
- **Spawn Rate:** 50/sec
- **Duration:** 1 minute
- **Purpose:** Sudden traffic spike

## User Behaviors

### LegendAIUser (Regular User)
Simulates typical user behavior with weighted tasks:

| Task | Weight | Description |
|------|--------|-------------|
| Health Check | 10 | Monitoring/polling |
| Analyze Ticker | 8 | Pattern analysis |
| Get Watchlist | 6 | View saved tickers |
| Get Version | 5 | Version check |
| Add to Watchlist | 4 | Save ticker |
| Get Market Quote | 3 | Price check |
| Get Chart | 2 | Chart generation |
| Detailed Health | 1 | Full diagnostics |

Wait time: 1-3 seconds between tasks

### HeavyUser (Power User)
Simulates intensive operations:

| Task | Weight | Description |
|------|--------|-------------|
| Full Universe Scan | 5 | 50+ ticker scan |
| Batch Analysis | 3 | Multiple tickers |

Wait time: 2-5 seconds between tasks

## Performance Thresholds

| Endpoint | P95 Threshold | P99 Threshold |
|----------|---------------|---------------|
| `/health` | 100 ms | 200 ms |
| `/api/version` | 100 ms | 200 ms |
| `/api/watchlist` | 500 ms | 1000 ms |
| `/api/analyze` | 2000 ms | 5000 ms |
| `/api/scan` | 5000 ms | 10000 ms |
| `/health/detailed` | 500 ms | 1000 ms |
| `/api/market/quote` | 1000 ms | 2000 ms |

## Results

### Location
All results saved to: `tests/load/results/`

### Files Generated
- `baseline.json` - Performance baseline metrics
- `{scenario}_{timestamp}.html` - HTML report with graphs
- `{scenario}_{timestamp}_stats.csv` - Request statistics
- `{scenario}_{timestamp}_failures.csv` - Failure log
- `{scenario}_{timestamp}_exceptions.csv` - Exception log
- `load_test_results.txt` - Summary log

### HTML Reports
Interactive HTML reports include:
- Response time charts
- Request rate graphs
- Failure rate visualization
- Percentile breakdown
- Detailed statistics table

## Installation

### Prerequisites
```bash
# Install load testing dependencies
pip install locust aiohttp

# Or from requirements
pip install -r requirements.txt
```

## Usage Examples

### Quick Performance Check
```bash
# Run baseline test
python tests/load/performance_baseline.py
```

### Full Load Test Suite
```bash
# Run all scenarios
./tests/load/run_load_tests.sh
```

### Custom Load Test
```bash
# 100 users, 5-second ramp-up, 5-minute duration
locust -f tests/load/locustfile.py \
    --host=http://localhost:8000 \
    --users=100 \
    --spawn-rate=20 \
    --run-time=5m \
    --headless \
    --html=results/custom_test.html
```

### Interactive Testing
```bash
# Start web UI
locust -f tests/load/locustfile.py --host=http://localhost:8000

# Open browser to http://localhost:8089
# Configure users/spawn rate in UI
# Start test
# Monitor real-time results
```

## Interpreting Results

### Good Performance
- P95 < threshold
- P99 < threshold
- Failure rate < 1%
- Response time stable under load
- No memory leaks

### Performance Issues
- P95 > threshold
- High failure rate
- Response time increases with load
- Timeout errors
- Memory growth over time

### Common Bottlenecks
1. **Database queries** - Check slow query log
2. **External API calls** - Monitor rate limits
3. **CPU-intensive operations** - Profile pattern detection
4. **Memory usage** - Check for leaks
5. **Connection pooling** - Review pool size

## Integration with CI/CD

Add to `.github/workflows/performance.yml`:

```yaml
name: Performance Tests

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
  workflow_dispatch:

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run baseline tests
        run: python tests/load/performance_baseline.py
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: performance-results
          path: tests/load/results/
```

## Monitoring in Production

### Prometheus Metrics
Monitor these metrics during load tests:
- `analyze_request_duration_seconds`
- `scan_request_duration_seconds`
- `detector_runtime_seconds`
- `cache_hits_total`
- `cache_misses_total`

### Grafana Dashboard
Create dashboard with:
- Request rate
- Response time (P50, P95, P99)
- Error rate
- Cache hit rate
- Active connections

## Capacity Planning

Based on load test results:

| Scenario | Max RPS | Avg Response Time | Recommendation |
|----------|---------|-------------------|----------------|
| Baseline | TBD | TBD | Minimum capacity |
| Normal | TBD | TBD | Daily operations |
| Peak | TBD | TBD | Scale trigger |
| Stress | TBD | TBD | Maximum capacity |

## Troubleshooting

### Tests failing immediately
```bash
# Check if app is running
curl http://localhost:8000/health

# Start app
docker-compose up -d
```

### High failure rate
```bash
# Check logs
docker-compose logs -f app

# Review errors
cat tests/load/results/*_failures.csv
```

### Slow performance
```bash
# Profile the app
py-spy record -o profile.svg -- python -m uvicorn app.main:app

# Check database
# Check external API rate limits
# Review cache hit rate
```

## Best Practices

1. **Establish baseline first** - Run baseline tests before code changes
2. **Test locally** - Validate before production testing
3. **Gradual ramp-up** - Increase load gradually
4. **Monitor resources** - Watch CPU, memory, disk I/O
5. **Save results** - Track performance over time
6. **Set thresholds** - Define acceptable performance
7. **Test regularly** - Weekly or before major releases

## Support

For performance issues:
1. Review HTML reports in `tests/load/results/`
2. Check Prometheus metrics
3. Analyze slow query logs
4. Profile application code
5. Review external API usage
