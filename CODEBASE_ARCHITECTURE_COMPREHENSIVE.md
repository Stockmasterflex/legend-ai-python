# Legend AI Python FastAPI - Codebase Architecture Analysis

## Executive Summary

Legend AI is a **professional trading pattern scanner** built with **FastAPI** that converts n8n workflows to a Python backend. The platform analyzes stock tickers for technical patterns, provides real-time data, generates charts, and delivers insights through a modern web dashboard, Telegram bot, and REST API.

**Status:** Phase 1.1+ - Production Ready (Core Features Operational)

---

## 1. PROJECT STRUCTURE & MAIN DIRECTORIES

### Root Level Architecture
```
legend-ai-python/
├── app/                          # Main FastAPI application
├── static/                       # Frontend assets (CSS, JS, images)
├── templates/                    # HTML templates (dashboard, widgets)
├── tests/                        # Pytest test suite (19+ test files)
├── docs/                         # Documentation (roadmaps, guides, checklists)
├── alembic/                      # Database migrations
├── monitoring/                   # Prometheus metrics and monitoring
├── ops/                          # DevOps scripts
├── scripts/                      # Utility scripts
└── data/                         # Local data storage
```

### App Directory Structure (Core Application)
```
app/
├── main.py                       # FastAPI app initialization & routing
├── config.py                     # Settings/environment management (Pydantic)
├── models.py                     # SQLAlchemy database models
├── lifecycle.py                  # App startup/shutdown handlers
├── docs_config.py               # OpenAPI documentation metadata
│
├── api/                          # API endpoint routers (22 modules)
│   ├── analyze.py              # Single-ticker technical analysis
│   ├── charts.py               # Chart generation endpoints
│   ├── patterns.py             # Pattern detection endpoints
│   ├── universe.py             # Bulk universe scanning (S&P500, NASDAQ)
│   ├── scan.py                 # VCP scanner & top setups
│   ├── multitimeframe.py       # Multi-timeframe confluence analysis
│   ├── market.py               # Market internals & breadth metrics
│   ├── watchlist.py            # Watchlist management
│   ├── trades.py               # Trade journal & history
│   ├── analytics.py            # Trade performance analytics
│   ├── risk.py                 # Risk calculation APIs
│   ├── alerts.py               # Alert management
│   ├── dashboard.py            # Dashboard HTML serving
│   ├── telegram*.py            # Telegram bot webhooks
│   ├── cache_mgmt.py           # Cache statistics & management
│   └── ... (16 more APIs)
│
├── core/                        # Business logic & algorithms
│   ├── pattern_detector.py     # Base pattern detection engine
│   ├── pattern_detector_v2.py  # Improved pattern detection
│   ├── indicators.py           # TA indicators (EMA, SMA, RSI, etc.)
│   ├── classifiers.py          # Trend classification (Minervini, Weinstein)
│   ├── metrics.py              # Risk metrics (ATR, R-multiples, etc.)
│   ├── chart_generator.py      # Chart rendering logic
│   ├── error_recovery.py       # Error handling strategies
│   ├── detector_base.py        # Base detector class
│   ├── detector_registry.py    # Pattern detector registration
│   ├── detector_config.py      # Detector configuration
│   ├── flags.py                # Feature flags
│   └── detectors/              # Individual pattern detectors
│       ├── vcp_detector.py
│       ├── cup_handle_detector.py
│       ├── channel_detector.py
│       ├── triangle_detector.py
│       ├── wedge_detector.py
│       ├── head_shoulders_detector.py
│       ├── double_top_bottom_detector.py
│       └── sma50_pullback_detector.py
│
├── services/                    # External service integrations
│   ├── market_data.py          # Multi-source market data (TwelveData, Finnhub, AlphaVantage)
│   ├── charting.py             # Chart-IMG service integration (500 daily calls)
│   ├── cache.py                # Redis caching layer
│   ├── multi_tier_cache.py     # Advanced caching strategy
│   ├── cache_warmer.py         # Pre-cache warming service
│   ├── pattern_scanner.py      # Multi-pattern scanning service
│   ├── scanner.py              # VCP scanner service
│   ├── trades.py               # Trade tracking service
│   ├── universe.py             # Universe/watchlist scanning
│   ├── universe_store.py       # In-memory ticker universe store
│   ├── universe_data.py        # Universe data providers
│   ├── database.py             # Database connection management
│   ├── alerts.py               # Price & pattern alerting
│   ├── api_clients.py          # HTTP client configuration
│   ├── multitimeframe.py       # Multi-timeframe analysis service
│   └── risk_calculator.py      # Risk metrics calculations
│
├── infra/                       # Infrastructure & external APIs
│   ├── chartimg.py             # Chart-IMG API wrapper
│   └── symbols.py              # Symbol validation & lookup
│
├── telemetry/                   # Monitoring & metrics
│   ├── metrics.py              # Prometheus metric definitions
│   ├── monitoring.py           # Monitoring service
│   ├── alerter.py              # Alert triggering
│   └── (metrics collection)
│
├── middleware/                  # HTTP middleware
│   ├── metrics_middleware.py   # Request metrics collection
│   ├── rate_limit.py           # Rate limiting (60 req/min/IP)
│   └── structured_logging.py   # JSON structured logging
│
├── routers/                     # Additional routers
│   ├── ai_chat.py              # AI chatbot for trading
│   └── advanced_analysis.py    # Advanced analysis features
│
├── technicals/                  # Technical analysis helpers
│   ├── fibonacci.py            # Fibonacci retracement/extension
│   └── trendlines.py           # Trendline support/resistance
│
└── utils/                       # Utility functions
    └── build_info.py           # Build metadata (SHA, branch)
```

---

## 2. EXISTING CHARTING/VISUALIZATION CAPABILITIES

### Chart Generation Service
**Module:** `app/services/charting.py` & `app/infra/chartimg.py`

#### Capabilities:
- **Provider:** Chart-IMG API (Pro Plan: 500 daily calls, 10/sec rate limit)
- **Chart Types:** Trading view advanced charts with professional indicators
- **Supported Indicators/Overlays:**
  - Moving Averages: EMA21, EMA50, EMA200, SMA50, SMA200
  - Oscillators: RSI, MACD
  - Custom Support/Resistance drawings
  - Long position entry/stop/target annotations
  - Volume analysis

#### Chart Presets:
```python
"breakout": ["EMA21", "SMA50"]
"swing": ["EMA21", "SMA50"]
"momentum": ["EMA21", "SMA50"]
"support": ["EMA21", "SMA50"]
"minimal": ["EMA21"]
```

#### API Endpoints:
- **POST /api/charts/generate** - Single chart with entry/stop/target
- **POST /api/charts/multi** - Multi-timeframe charts (1D, 1W, 4H)
- **POST /api/charts/preview-batch** - Bulk preview generation

#### Caching:
- Redis-backed rate limiting
- Graceful degradation if rate limit exceeded
- 24-hour cache TTL for generated URLs

### Dashboard Visualization
**Module:** `templates/dashboard.html` + `static/js/dashboard.js`

#### Features:
- Modern cyberpunk design system
- Real-time data refresh
- TradingView embedded widgets (via Chart-IMG integration)
- Responsive layout (mobile/tablet/desktop)
- Interactive tabs: Analyze, Universe Scan, Watchlist, Market Internals

#### Technologies:
- **Vanilla JavaScript** (no framework dependencies)
- **CSS Grid/Flexbox** layouts
- **HTML5** semantic markup
- **Chart-IMG** for chart rendering

---

## 3. DATA FETCHING & STORAGE MECHANISMS

### Market Data Service
**Module:** `app/services/market_data.py`

#### Multi-Source Fallback (Intelligent Priority)
1. **Redis Cache** (instant, 24-hour TTL)
2. **TwelveData** (primary, 800 calls/day) - High quality, fastest
3. **Finnhub** (fallback, 60 calls/day) - Good for market internals
4. **Alpha Vantage** (fallback, 500 calls/day) - Reliable but slower
5. **Yahoo Finance** (last resort, unlimited) - May be blocked

#### Rate Limiting
- **API Usage Tracking:** Redis-backed daily counters
- **Smart Fallback:** Automatically switches to next API when limit reached
- **Usage Statistics:** `/api/market/usage` endpoint for monitoring

#### Data Structures
```python
{
    "c": [closes],      # Closing prices
    "o": [opens],       # Opening prices
    "h": [highs],       # High prices
    "l": [lows],        # Low prices
    "v": [volumes],     # Trading volumes
    "t": [timestamps]   # Timestamps
}
```

### Database Models
**Module:** `app/models.py`

#### SQLAlchemy Tables:
- **Ticker:** Stock metadata (symbol, name, sector, industry)
- **PatternScan:** Detection results (pattern type, score, entry/stop/target)
- **Watchlist:** User-tracked symbols with alerts
- **ScanLog:** Universe scanning history
- **UniverseScan:** Bulk scan results
- **AlertLog:** Alert trigger history
- **Trade:** Trade journal entries

#### Database Setup
- **ORM:** SQLAlchemy 2.0
- **Migrations:** Alembic (in `alembic/` directory)
- **Connection:** PostgreSQL (configurable, Railway supported)
- **Optional:** Can run without database (in-memory cache mode)

### Caching Strategy
**Modules:** `app/services/cache.py`, `app/services/multi_tier_cache.py`

#### Three-Tier Cache:
1. **L1 - Redis (Hot Cache):** 5-60 minute TTL
2. **L2 - Database:** Persistent long-term storage
3. **L3 - Memory:** In-process fallback

#### Cache Keys (Semantic):
- `analyze:{ticker}:{interval}:{bars}`
- `pattern:{ticker}:{interval}`
- `chart:{ticker}:{interval}:{checksum}`
- `universe:{universe_name}:{timestamp}`

#### Cache Management:
- **Warmup Service:** `cache_warmer.py` pre-loads common queries
- **Invalidation:** Automatic on market hours, manual via `/api/cache` endpoint
- **Monitoring:** `/api/metrics/cache` tracks hit rates

---

## 4. EXISTING COMPARISON & ANALYSIS FEATURES

### A. Multi-Timeframe Confluence Analysis
**Module:** `app/api/multitimeframe.py` & `app/services/multitimeframe.py`

#### Features:
- Single ticker analyzed across multiple timeframes (1D, 1W, 4H, 1H)
- Confluence scoring (0-100%) based on signal alignment
- Signal quality classification ("Weak", "Good", "Strong")
- Returns combined analysis for all timeframes

#### Endpoint:
```
POST /api/multitimeframe/analyze
{
    "ticker": "NVDA"
}
→ confluence: 82%, signal_quality: "Good"
```

### B. Market Internals & Breadth Analysis
**Module:** `app/api/market.py`

#### Features:
- Advance/Decline ratios (sample of 50 tickers)
- % of stocks above EMA50 and EMA200
- New 52-week highs/lows counts
- Market breadth indices

#### Endpoints:
- `GET /api/market/breadth` - Market-wide metrics
- `GET /api/market/internals` - Detailed breadth analysis

### C. Single-Ticker Technical Analysis
**Module:** `app/api/analyze.py`

#### Features:
- Comprehensive technical analysis for one ticker
- Indicators: EMA, SMA, RSI, MACD, ATR
- Minervini trend template classification
- Weinstein stage analysis
- MA distances from price
- Relative strength metrics
- Risk/reward calculations (ATR-based)

#### Endpoint:
```
GET /api/analyze?ticker=AAPL&tf=daily&bars=400
→ Full technical profile + chart
```

### D. Pattern Detection
**Module:** `app/api/patterns.py` & `app/core/detectors/`

#### Patterns Detected:
1. **VCP** (Volatility Contraction Pattern)
2. **Cup & Handle**
3. **Flat Base**
4. **Channels**
5. **Triangles** (ascending, descending, symmetrical)
6. **Wedges** (rising, falling)
7. **Head & Shoulders** (normal & inverse)
8. **Double Top/Bottom**
9. **SMA50 Pullback**
10. **Breakout**

#### Endpoint:
```
POST /api/patterns/detect
{
    "ticker": "AAPL",
    "interval": "1day"
}
→ Detected patterns with scores, entry/stop/target
```

### E. Universe Scanning (Bulk Multi-Ticker)
**Module:** `app/api/universe.py` & `app/services/universe.py`

#### Features:
- Scans S&P 500 (500 stocks) or NASDAQ 100 (100 stocks)
- Pattern filtering available
- Min confidence threshold (0.6-1.0)
- Concurrent async scanning
- Results ranked by score

#### Endpoints:
```
POST /api/universe/scan
{
    "min_score": 7.0,
    "max_results": 20,
    "pattern_types": ["VCP", "Cup & Handle"]
}
→ List of matching tickers with scores

GET /api/scan
→ Daily VCP scan with top setups
```

#### Performance:
- Scans up to 600 tickers concurrently
- Max concurrency: 8 (configurable)
- Typical duration: 2-5 minutes for full S&P500

### F. VCP (Volatility Contraction) Specialization
**Module:** `app/core/detectors/vcp_detector.py` & `app/services/scanner.py`

#### Features:
- Dedicated VCP pattern scanner
- Volume dry-up detection
- Consolidation period analysis
- Breakout prediction
- RS (Relative Strength) rating integration

#### Endpoint:
```
GET /api/scan?limit=50&sector=Technology
→ Top 50 VCP setups filtered by sector
```

---

## 5. UI FRAMEWORK

### Frontend Stack
**No Heavy Framework** - Intentionally lightweight

#### Technologies:
- **HTML5:** Semantic markup
- **Vanilla JavaScript:** No jQuery, Vue, React, or Angular
- **CSS3:** Custom design system (no Tailwind, Bootstrap)
- **Alpine.js:** Minimal for reactive state (optional, compatible)

#### Design System
**Module:** `static/css/cyberpunk-design-system.css`

- **Theme:** Dark mode (cyberpunk aesthetic)
- **Typography:** Inter font, JetBrains Mono for code
- **Colors:** Neon accents (electric blue, red, green)
- **Components:** Buttons, cards, tabs, modals, forms

#### Dashboard Architecture
**Main File:** `static/js/dashboard.js` (80KB)

#### Tab Structure:
1. **Analyze** - Single ticker analysis form
2. **Universe Scan** - Bulk S&P500/NASDAQ scanning
3. **Top Setups** - Best patterns found (cached)
4. **Watchlist** - User-tracked symbols
5. **Market Internals** - Breadth metrics & heat maps

#### Key UI Components:
- Form handlers for ticker input
- Real-time loading states & spinners
- Toast notifications for user feedback
- Table rendering with sorting
- Chart embedding (Chart-IMG URLs)
- TradingView widget integration

#### TradingView Integration
**Module:** `static/js/tv-widgets.js` & `templates/tv_symbol_lab.html`

- Embedded TradingView advanced charts
- Symbol Lab for comparative analysis
- Ticker tape widget
- Stock screener widget

---

## 6. TESTING FRAMEWORK & PATTERNS

### Test Setup
**Location:** `tests/` directory (19+ test files)
**Framework:** **Pytest** with async support

#### Test Configuration
**File:** `pytest.ini`
```ini
[pytest]
testpaths = tests
addopts = --cov=app --cov-report=term-missing --strict-markers -v
markers = asyncio, benchmark, slow, integration, unit
```

#### Coverage:
- **Target:** Line coverage with HTML reports
- **Reports:** Generated to `htmlcov/` directory
- **Coverage file:** `coverage.json` (CI/CD friendly)

### Test Files Overview
1. **test_smoke.py** - Basic endpoint health checks
2. **test_analyze_contract.py** - Analyze API contract tests
3. **test_charting.py** - Chart generation tests
4. **test_patterns.py** - Pattern detection unit tests
5. **test_indicators.py** - TA indicator calculation tests
6. **test_scanner_service.py** - Universe scanning tests
7. **test_market_data.py** - Data fetching with fallback tests
8. **test_universe_api.py** - Universe API integration tests
9. **test_vcp_detector.py** - VCP-specific pattern tests
10. ... (9 more test files)

### Testing Patterns

#### Fixtures (Standard Pytest)
```python
@pytest.fixture
def client():
    # FastAPI TestClient with stubbed services
    with TestClient(main.app) as test_client:
        yield test_client
```

#### Async Testing
```python
@pytest.mark.asyncio
async def test_market_data_fetch():
    data = await market_data_service.get_time_series("AAPL")
    assert data["c"] is not None
```

#### Mocking Strategy
- **Monkeypatch:** For service method mocking
- **Stubs:** Simple in-memory cache stubs
- **Fixtures:** Seeded test data (OHLCV series)

#### Test Data Generation
```python
def _make_series(n=260):
    closes = [100 + i * 0.4 for i in range(n)]
    # Create synthetic OHLCV data
    return {"c": closes, "o": opens, ...}
```

### CI/CD Integration
**GitHub Actions:** `.github/workflows/` (configured)

- Pytest runs on every PR
- Coverage reports generated
- Smoke tests validate key endpoints

---

## 7. CODEBASE ARCHITECTURE PATTERNS

### Architecture Overview

#### Layered Architecture:
```
┌─────────────────────────────────┐
│  API Layer (22 routers)         │ ← FastAPI endpoints
├─────────────────────────────────┤
│  Service Layer (15+ services)   │ ← Business logic
├─────────────────────────────────┤
│  Core Layer (algorithms)        │ ← Pattern detection, indicators
├─────────────────────────────────┤
│  Infrastructure Layer           │ ← External APIs, DB
├─────────────────────────────────┤
│  Caching & Storage              │ ← Redis, PostgreSQL
└─────────────────────────────────┘
```

#### Key Patterns:

1. **Service Locator Pattern**
   - `get_cache_service()` - Singleton cache
   - `market_data_service` - Global market data instance
   - `universe_service` - Global universe scanning

2. **Async/Await Throughout**
   - All I/O operations are async
   - Concurrent ticker processing
   - Non-blocking database queries

3. **Dependency Injection** (Light)
   - Config injected via settings
   - Services passed to API routes
   - Monkeypatchable for testing

4. **Middleware Pipeline**
   - Metrics collection
   - Structured logging
   - Rate limiting
   - CORS handling

5. **Error Recovery**
   - Multi-source data fallback
   - Graceful API degradation
   - Comprehensive error responses

### Configuration Management
**Module:** `app/config.py`

- **Tool:** Pydantic Settings with `.env` file
- **Environment-Aware:** Different settings for Dev/Prod
- **Railway Integration:** Auto-detects domain and CORS
- **API Key Management:** Multiple key sources (env vars, `.env`)

### Logging Strategy
**Middleware:** `app/middleware/structured_logging.py`

- **Format:** JSON structured logging
- **Fields:** timestamp, event, ticker, interval, status
- **Levels:** DEBUG, INFO, WARNING, ERROR
- **Async-Safe:** Non-blocking log writes

---

## 8. KEY ARCHITECTURAL DECISIONS

### Why This Stack?
1. **FastAPI** - Modern async, auto OpenAPI docs, excellent performance
2. **PostgreSQL** - Robust, scales well, ideal for trading data
3. **Redis** - Fast caching, rate limiting, session storage
4. **Vanilla JS** - No frontend build step, lightweight, fast loading
5. **Chart-IMG** - Professional charts without client-side rendering
6. **TwelveData** - Best API for stock data with unlimited flexibility

### Trade-offs Made
- **No ORM for caching:** Direct Redis keys for speed
- **No job queue (Celery):** Async/await instead, simpler ops
- **No WebSockets:** REST polling sufficient for current UX
- **Single database:** PostgreSQL only (no MongoDB, no DynamoDB)
- **No microservices:** Monolithic for easier deployment

### Performance Optimizations
1. **Three-tier caching** (Redis → DB → Memory)
2. **Concurrent async scanning** (8 max concurrent)
3. **Rate limiting** (60 req/min per IP to prevent abuse)
4. **Database indexing** (on ticker, pattern, date)
5. **API response caching** (24-hour TTL)

---

## 9. DEPENDENCIES & TECH STACK

### Core Dependencies
```
Framework:          FastAPI 0.115.6
Server:             Uvicorn 0.32.1
Database:           SQLAlchemy 2.0.36, PostgreSQL, Alembic
Async:              Asyncio (Python stdlib)
HTTP Client:        httpx 0.28.1
Caching:            Redis 5.2.1
Config:             Pydantic 2.10.6, Pydantic-Settings 2.7.1
Auth:               python-jose, passlib
Telegram:           python-telegram-bot 21.9
Testing:            pytest 8.4.2, pytest-asyncio 1.3.0
Data Processing:    pandas 2.2.3, numpy 1.26.4, scipy 1.14.1
AI/LLM:             openai 1.59.7
Monitoring:         prometheus-client 0.20.0+
Dashboard:          Gradio 5.9.1 (Phase 2)
```

### External Services
- **Market Data:** TwelveData, Finnhub, Alpha Vantage
- **Charts:** Chart-IMG API (Pro: 500 calls/day)
- **AI:** OpenRouter (Claude 3.5 Sonnet)
- **Messaging:** Telegram Bot API
- **Deployment:** Railway (integrated PostgreSQL + Redis)

---

## 10. RECOMMENDATION: WHERE TO INTEGRATE MULTI-TICKER COMPARISON

### Current State Analysis
**Single-ticker operations are primary:**
- `/api/analyze` - One ticker at a time
- `/api/patterns/detect` - One ticker at a time
- `/api/multitimeframe/analyze` - One ticker across timeframes

**Bulk operations exist but lack comparison:**
- `/api/universe/scan` - Returns list, no comparison
- `/api/scan` - Returns ranked list, no side-by-side analysis

**Gap:** No "compare these 2-5 tickers" feature

### Proposed Integration Points

#### **Option 1: New Comparison API Module (Recommended)**
**Location:** Create `app/api/comparison.py`

```python
POST /api/comparison/analyze
{
    "tickers": ["AAPL", "MSFT", "NVDA"],
    "metrics": ["rsi", "ma_distances", "trend_stage", "risk_reward"],
    "interval": "1day"
}
→ Comparative metrics table, visual heatmap, correlation matrix
```

**Advantages:**
- Clean separation of concerns
- Reusable comparison logic
- Easy to extend with new metrics

**Implementation:**
1. Create `app/services/comparison.py` - Core logic
2. Create `app/api/comparison.py` - FastAPI router
3. Add comparison tests in `tests/test_comparison.py`
4. Dashboard tab: "Compare Tickers"

#### **Option 2: Extend Universe Scanner**
**Location:** Extend `app/api/universe.py`

```python
POST /api/universe/compare
{
    "tickers": ["AAPL", "MSFT"],
    "include_metrics": true
}
→ Detailed comparison of patterns, technicals, fundamentals
```

**Advantages:**
- Leverages existing scanner infrastructure
- Natural progression from bulk scanning
- Uses existing universe caching

#### **Option 3: Dashboard Widget**
**Location:** Enhance `templates/dashboard.html` + `static/js/dashboard.js`

- Add "Comparison" tab
- Multi-select ticker input
- Real-time table with metrics
- No new backend required (use existing endpoints)

### Recommended Implementation Path

#### **Phase 1: API Foundation**
```
New files:
  app/services/comparison.py      # Core comparison logic
  app/api/comparison.py           # API endpoints
  tests/test_comparison.py        # Tests

Modified files:
  app/main.py                     # Include comparison router
```

#### **Phase 2: Dashboard UI**
```
Modified files:
  templates/dashboard.html        # Add comparison tab
  static/js/dashboard.js          # Comparison tab controller
  static/css/dashboard.css        # Styling
```

#### **Phase 3: Advanced Features**
```
Optional enhancements:
  - Correlation matrix visualization
  - Sector-wide comparison
  - Historical comparison (pattern frequency by ticker)
  - "Find similar patterns" feature
```

### Suggested Comparison Metrics

#### Technical Metrics (Already Available):
1. **Trend & Momentum**
   - RSI (over/under bought)
   - MACD (trend direction)
   - Trend stage (Minervini classification)
   - Price position vs MA (EMA21, SMA50, SMA200)

2. **Risk Metrics**
   - ATR (volatility)
   - Risk/Reward ratio
   - Support/Resistance distance

3. **Pattern Metrics**
   - Detected patterns
   - Pattern score (0-10)
   - Pattern confidence

4. **Volume Metrics**
   - Volume trend
   - Volume MA ratio
   - Volume dry-up status

#### Visualization Options:
1. **Comparison Table** - Side-by-side metrics (easiest)
2. **Heatmap** - Color-coded metric strength
3. **Radar Chart** - Pattern/metric profile comparison
4. **Correlation Matrix** - Ticker inter-correlation

### Integration with Existing Features

#### Uses Existing Services:
- ✅ `market_data_service` - Fetch OHLCV
- ✅ `charting_service` - Generate charts
- ✅ `cache_service` - Cache results
- ✅ Pattern detectors - Run detection on multiple tickers

#### Extends Existing Patterns:
- ✅ Async concurrent processing (like universe scanner)
- ✅ Rate limiting (respects API quotas)
- ✅ Caching strategy (3-tier cache)
- ✅ Error recovery (multi-source fallback)

### Database Schema Additions (Optional)
```sql
CREATE TABLE comparison_sessions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100),
    tickers TEXT[],        -- Array of ticker symbols
    metrics TEXT[],        -- Array of metric names
    interval VARCHAR(20),
    result_json JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_comparison_user ON comparison_sessions(user_id);
CREATE INDEX idx_comparison_created ON comparison_sessions(created_at);
```

---

## 11. PROJECT STATISTICS

### Codebase Size
- **Python files:** 100+ in `app/` directory
- **Test files:** 19 test modules
- **Lines of code:** ~20,000+ (app logic)
- **Test coverage:** Tracks HTML coverage reports

### API Endpoints
- **Total routes:** 22+ API modules
- **Documented endpoints:** 100+ (Swagger-compliant)
- **Async operations:** 100% of I/O

### Performance Metrics
- **Response time:** <5 seconds typical
- **Cache hit rate:** 60-80% (production)
- **API rate limit:** 60 requests/min per IP
- **Max concurrent scans:** 8 tickers
- **Universe scan time:** 2-5 minutes (full S&P500)

### Supported Patterns
- **10 pattern types** recognized
- **8+ detectors** implemented
- **100+ aliases** for pattern names (UI normalization)

---

## 12. DEPLOYMENT & INFRASTRUCTURE

### Container & Deployment
- **Docker:** Containerized (Dockerfile in root)
- **Orchestration:** Railway.app (integrated PostgreSQL + Redis)
- **Health checks:** `/health`, `/healthz` endpoints
- **CI/CD:** GitHub Actions configured

### Environment
- **Railway domain:** Auto-detected
- **CORS:** Environment-aware (prod: self-domain only)
- **Secrets:** Managed via Railway environment variables

### Monitoring
- **Metrics:** Prometheus format (`/metrics` endpoint)
- **Logging:** JSON structured logs (for log aggregation)
- **Alerts:** Configured in `monitoring/` directory

---

## 13. QUICK START FOR MULTI-TICKER FEATURE

### Step 1: Analyze Requirements
- What metrics to compare?
- How many tickers (2, 5, unlimited)?
- UI: Table, heatmap, radar chart, or combination?
- Real-time or cached results acceptable?

### Step 2: Create Core Service
```python
# app/services/comparison.py
class ComparisonService:
    async def compare_tickers(
        self, 
        tickers: List[str],
        metrics: List[str],
        interval: str
    ) -> Dict[str, Any]:
        """Fetch and compare metrics across multiple tickers"""
        # Fetch OHLCV for each ticker concurrently
        # Calculate indicators for each
        # Build comparison matrix
        # Return structured results
```

### Step 3: Create API Endpoint
```python
# app/api/comparison.py
@router.post("/compare")
async def compare_tickers(request: ComparisonRequest):
    """Compare multiple tickers on key metrics"""
    service = get_comparison_service()
    results = await service.compare_tickers(
        request.tickers,
        request.metrics,
        request.interval
    )
    return results
```

### Step 4: Add Dashboard Tab
```javascript
// static/js/dashboard.js
switchTab('comparison', async () => {
    const tickers = ['AAPL', 'MSFT', 'NVDA'];
    const result = await fetch('/api/comparison/compare', {
        method: 'POST',
        body: JSON.stringify({
            tickers,
            metrics: ['rsi', 'ma_distance', 'trend_stage'],
            interval: '1day'
        })
    });
    renderComparisonTable(result);
});
```

### Step 5: Write Tests
```python
# tests/test_comparison.py
@pytest.mark.asyncio
async def test_compare_tickers(monkeypatch, client):
    response = client.post('/api/comparison/compare', json={
        'tickers': ['AAPL', 'MSFT'],
        'metrics': ['rsi'],
        'interval': '1day'
    })
    assert response.status_code == 200
    data = response.json()
    assert 'AAPL' in data['results']
    assert 'MSFT' in data['results']
```

---

## CONCLUSION

Legend AI is a **well-architected, production-ready trading analysis platform** with:
- ✅ Modular service architecture
- ✅ Comprehensive testing framework
- ✅ Modern async/await patterns
- ✅ Professional UI with dark mode design
- ✅ Multi-source data fetching with fallbacks
- ✅ Intelligent 3-tier caching
- ✅ 10+ pattern detection algorithms
- ✅ 100+ documented API endpoints

**Multi-ticker comparison** should be integrated as a new service layer (`app/services/comparison.py`) with corresponding API module (`app/api/comparison.py`), following the existing architectural patterns.

The project is **ready for immediate feature expansion** with clear patterns to follow.
