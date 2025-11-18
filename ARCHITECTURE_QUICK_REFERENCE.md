# Legend AI - Architecture Quick Reference

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                     │
│  ┌──────────────────┐  ┌────────────────┐  ┌──────────────────────┐   │
│  │ Web Dashboard    │  │  Telegram Bot  │  │  TradingView Widgets │   │
│  │ (Vanilla JS)     │  │  (python-tg)   │  │  (embedded)          │   │
│  └────────┬─────────┘  └────────┬───────┘  └──────────┬───────────┘   │
└───────────┼────────────────────┼──────────────────────┼────────────────┘
            │                    │                      │
            ▼                    ▼                      ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                      API LAYER (FastAPI)                                 │
│  22 Route Modules                                                        │
│  ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────────────┐ │
│  │ analyze │ patterns│ universe│ compare │ watchlist│ ... (17 more)   │ │
│  │ charts  │ market  │ scan    │ trades  │ alerts  │                 │ │
│  └─────────┴─────────┴─────────┴─────────┴─────────┴─────────────────┘ │
│                                                                          │
│  Middleware Stack:                                                      │
│  • Prometheus Metrics  • Rate Limiting  • Structured Logging • CORS    │
└─────────────┬──────────────────────────┬──────────────────────────────┘
              │                          │
              ▼                          ▼
┌──────────────────────────┐   ┌────────────────────────────────────────┐
│  SERVICE LAYER           │   │  CORE LAYER (Algorithms)               │
│  (Business Logic)        │   │                                        │
│ ┌──────────────────────┐ │   │ ┌────────────────────────────────────┐│
│ │ market_data.py       │ │   │ │ Pattern Detectors                  ││
│ │  ↓ TwelveData        │ │   │ │ • VCP, Cup&Handle, Wedges         ││
│ │  ↓ Finnhub           │ │   │ │ • Triangles, Head&Shoulders       ││
│ │  ↓ AlphaVantage      │ │   │ │ • Channels, Double Top/Bottom     ││
│ │  ↓ Yahoo (fallback)  │ │   │ │                                    ││
│ ├──────────────────────┤ │   │ ├────────────────────────────────────┤│
│ │ charting.py          │ │   │ │ Indicators                         ││
│ │  ↓ Chart-IMG API     │ │   │ │ • EMA, SMA, RSI, MACD, ATR        ││
│ │  ↓ 500 calls/day     │ │   │ │ • Fibonacci, Trendlines           ││
│ ├──────────────────────┤ │   │ ├────────────────────────────────────┤│
│ │ pattern_scanner.py   │ │   │ │ Classifiers                        ││
│ │  ↓ All detectors     │ │   │ │ • Minervini Trend Template        ││
│ │  ↓ Concurrent scans  │ │   │ │ • Weinstein Stage Analysis        ││
│ ├──────────────────────┤ │   │ └────────────────────────────────────┘│
│ │ cache.py             │ │   └────────────────────────────────────────┘
│ │  ↓ 3-tier (Redis,    │ │
│ │    DB, Memory)       │ │
│ ├──────────────────────┤ │
│ │ universe.py          │ │
│ │  ↓ S&P500 (500)      │ │
│ │  ↓ NASDAQ100 (100)   │ │
│ ├──────────────────────┤ │
│ │ (10+ more services)  │ │
│ └──────────────────────┘ │
└──────────────────────────┴──────────────────────────────────────────────┘
              │                          │
              ▼                          ▼
┌───────────────────────────────────────────────────────────────────────┐
│              STORAGE & CACHING LAYER                                  │
│  ┌──────────────────────┐  ┌──────────────────────────────────────┐  │
│  │ Redis Cache          │  │ PostgreSQL Database                  │  │
│  │ • API responses      │  │ • Ticker metadata                    │  │
│  │ • Rate limits        │  │ • Pattern scans                      │  │
│  │ • Session data       │  │ • Watchlist                          │  │
│  │ • TTL: 5min-24hr     │  │ • Trade journal                      │  │
│  │                      │  │ • Scan history                       │  │
│  └──────────────────────┘  └──────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Example: Analyze Single Ticker

```
1. User Input (Dashboard)
   └─→ GET /api/analyze?ticker=AAPL&tf=daily

2. API Route (app/api/analyze.py)
   └─→ Check Redis cache
       ├─ HIT: Return cached result (< 10ms)
       └─ MISS: Continue to step 3

3. Market Data Service
   └─→ Try TwelveData (primary)
       ├─ HIT: Fetch OHLCV data
       └─ FAIL: Fallback to Finnhub → AlphaVantage → Yahoo

4. Core Calculations (Parallel)
   ├─→ Calculate indicators (EMA, SMA, RSI, MACD, ATR)
   ├─→ Classify trend (Minervini, Weinstein)
   ├─→ Calculate risk metrics
   └─→ Generate chart URL

5. Response Assembly
   └─→ Return JSON:
       {
         indicators: {...},
         trend_analysis: {...},
         risk_profile: {...},
         chart_url: "https://chart-img.com/...",
         cache: {hit: false, ttl: 3600}
       }

6. Cache Storage
   └─→ Store in Redis for 1 hour (24-hour TTL)

7. Client Display (Dashboard)
   └─→ Render chart + metrics table
```

---

## Data Flow Example: Universe Scan (Bulk)

```
1. User Clicks "RUN SCAN"
   └─→ POST /api/universe/scan
       {min_score: 7.0, max_results: 20, pattern_types: ["VCP"]}

2. Universe Service
   └─→ Get ticker list (S&P500 or NASDAQ100)
       ├─ S&P500: 500 stocks
       └─ NASDAQ100: 100 stocks

3. Concurrent Async Scanning
   └─→ Split into 8 concurrent workers
       ├─ Fetch OHLCV for each ticker (market_data service)
       ├─ Run all detectors (VCP, Cup&Handle, etc.)
       ├─ Score patterns (0-10)
       └─ Filter by min_score threshold

4. Results Aggregation
   └─→ Collect all pattern matches
       ├─ Sort by score descending
       ├─ Limit to max_results
       └─ Enrich with current prices

5. Cache Results
   └─→ Store in Redis for next query
       Key: universe:SP500:20240101:000000

6. Return Results
   └─→ [
         {ticker: "AAPL", pattern: "VCP", score: 8.5, ...},
         {ticker: "MSFT", pattern: "Cup & Handle", score: 7.8, ...},
         ...
       ]

Total Time: 2-5 minutes (depending on API speed)
Cached Re-run: < 100ms
```

---

## API Endpoints by Category

### Single-Ticker Analysis
```
GET  /api/analyze?ticker=AAPL&tf=daily       → Full technical profile
POST /api/patterns/detect                    → Pattern detection
POST /api/multitimeframe/analyze             → Multi-TF confluence
GET  /api/charts/generate                    → Single chart
```

### Bulk Universe Scanning
```
POST /api/universe/scan                      → Full scan (custom filters)
GET  /api/scan?limit=50&sector=Tech          → Top VCP setups
GET  /api/top-setups                         → Best patterns (cached)
```

### Comparison (To Be Implemented)
```
POST /api/comparison/analyze                 → Compare 2-5 tickers
GET  /api/comparison/metrics?tickers=...     → Metrics comparison
```

### Market Intelligence
```
GET  /api/market/breadth                     → Market breadth metrics
GET  /api/market/internals                   → Market internals
```

### Watchlist & Portfolio
```
GET  /api/watchlist                          → User watchlist
POST /api/watchlist/add                      → Add to watchlist
GET  /api/trades/journal                     → Trade history
POST /api/trades/log                         → Log a trade
```

### System
```
GET  /api/health                             → Full health check
GET  /api/version                            → Build info
GET  /docs                                   → Swagger UI
GET  /redoc                                  → ReDoc UI
```

---

## File Organization Cheat Sheet

```
Need to add feature?          → Create in app/api/
Need to access data?          → Use app/services/
Need algorithm?               → Add to app/core/
Need external API?            → Wrapper in app/infra/
Need test?                    → Create in tests/
Need database table?          → Add to app/models.py + alembic migration
```

---

## Development Workflow

### 1. Add New Analysis Feature
```
Step 1: Create service logic
  → app/services/my_feature.py
  
Step 2: Create API endpoint
  → app/api/my_feature.py
  
Step 3: Register router in main.py
  → app.include_router(my_feature_router)
  
Step 4: Add tests
  → tests/test_my_feature.py
  
Step 5: Update dashboard (optional)
  → templates/dashboard.html + static/js/dashboard.js
```

### 2. Add New Pattern Detector
```
Step 1: Create detector class
  → app/core/detectors/my_pattern_detector.py
  
Step 2: Inherit from PatternDetectorBase
  → Implement find() method
  
Step 3: Register in detector_registry.py
  → Add to get_all_detectors()
  
Step 4: Write tests
  → tests/test_my_pattern.py
```

### 3. Integrate External Service
```
Step 1: Create service wrapper
  → app/infra/my_api.py or app/services/my_service.py
  
Step 2: Add API key to config.py
  → Add to Settings class
  
Step 3: Add to .env.example
  → Document required variables
  
Step 4: Use in service/API layer
  → Import and call async method
```

---

## Performance Tuning Checklist

- [ ] Is the endpoint cached? Check app/services/cache.py
- [ ] Is the API call counted? Check market_data.py usage tracking
- [ ] Are operations async? Use `async def`, `await`, `asyncio.gather()`
- [ ] Is database query indexed? Check app/models.py indexes
- [ ] Is response size reasonable? < 1MB ideal
- [ ] Can concurrent workers help? Use asyncio semaphore
- [ ] Is Redis TTL optimal? 5min-24hr typical
- [ ] Are there N+1 queries? Batch where possible

---

## Testing Quick Guide

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_analyze.py
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
```

### Run Async Tests
```bash
pytest -m asyncio
```

### Run Integration Tests Only
```bash
pytest -m integration
```

### Debug Single Test
```bash
pytest tests/test_analyze.py::test_analyze_endpoint -vv -s
```

---

## Key Configuration Files

| File | Purpose |
|------|---------|
| `app/config.py` | Settings (APIs, cache, DB, etc.) |
| `.env.example` | Template for all env variables |
| `requirements.txt` | Python dependencies |
| `pytest.ini` | Pytest configuration |
| `alembic.ini` | Database migration config |
| `docker-compose.yml` | Local dev environment |
| `.gitignore` | Git ignore rules |
| `railway.toml` | Railway.app deployment config |

---

## Helpful Commands

```bash
# Start dev server
uvicorn app.main:app --reload

# Check API endpoints
curl http://localhost:8000/docs

# Test single ticker
curl "http://localhost:8000/api/analyze?ticker=AAPL"

# Run full scan
curl -X POST http://localhost:8000/api/universe/scan \
  -H "Content-Type: application/json" \
  -d '{"min_score": 7.0, "max_results": 20}'

# Check cache hit rate
curl http://localhost:8000/api/metrics/cache

# Health check
curl http://localhost:8000/health | jq

# View logs
docker logs legend-ai-python (if deployed)
```

---

## Common Issues & Solutions

### "Chart-IMG API key not configured"
→ Add `CHART_IMG_API_KEY` to .env

### "Redis not configured"
→ Set `REDIS_URL` in .env or use local Redis

### "Database connection failed"
→ Check `DATABASE_URL` in .env

### "TwelveData API limit reached"
→ Check `/api/market/usage` endpoint, will fall back to Finnhub

### "Pattern not detected"
→ Check pattern score threshold in request, increase bars for more history

---

## Next Steps for Multi-Ticker Comparison

**Recommended implementation:**

1. **Create Service**: `app/services/comparison.py`
2. **Create API**: `app/api/comparison.py` with endpoints:
   - `POST /api/comparison/analyze` - Compare metrics
   - `GET /api/comparison/correlation` - Correlation matrix
3. **Add Tests**: `tests/test_comparison.py`
4. **Update Dashboard**: Add "Compare" tab with multi-ticker input
5. **Deploy**: Merge to main branch

**Estimated Effort**: 2-4 hours total

**Files to Modify**:
- `app/main.py` (add router)
- `templates/dashboard.html` (add tab)
- `static/js/dashboard.js` (add controller)

**Files to Create**:
- `app/services/comparison.py`
- `app/api/comparison.py`
- `tests/test_comparison.py`

---

**Status**: Production Ready for Feature Expansion ✅

See `CODEBASE_ARCHITECTURE_COMPREHENSIVE.md` for detailed analysis.
