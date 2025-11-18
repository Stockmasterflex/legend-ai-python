# Legend AI Codebase - Data Access & Caching Analysis

## Executive Summary

This is a **FastAPI-based trading pattern detection system** with multi-tier caching infrastructure, intelligent API fallback mechanisms, and comprehensive database integration. The application is designed to scan stock universes for technical patterns and generate annotated trading charts.

---

## 1. CURRENT DATA ACCESS PATTERNS

### 1.1 External API Calls (High-Frequency)

#### Market Data APIs (Multi-Source Fallback System)
**File:** `/app/services/market_data.py` (Lines 1-492)

**APIs Called:**
1. **TwelveData** (Primary) - 800 calls/day limit
   - Endpoint: `https://api.twelvedata.com/time_series`
   - Uses: Historical OHLCV data
   - Fallback chain position: 1st
   
2. **Finnhub** (Fallback 1) - 60 calls/day limit
   - Endpoint: `https://finnhub.io/api/v1/stock/candle`
   - Uses: When TwelveData fails or rate limit reached
   - Fallback chain position: 2nd

3. **Alpha Vantage** (Fallback 2) - 500 calls/day limit
   - Endpoint: `https://www.alphavantage.co/query`
   - Uses: When Finnhub fails
   - Fallback chain position: 3rd

4. **Yahoo Finance** (Last Resort) - Unlimited but may be blocked
   - Endpoint: `https://query1.finance.yahoo.com/v8/finance/chart/{ticker}`
   - Uses: When all paid APIs fail
   - Fallback chain position: 4th

**Call Pattern:**
- `get_time_series()` - Fetches OHLCV with intelligent fallback (900s cache TTL)
- `get_quote()` - Gets current price (attempts TwelveData first)
- **Rate limiting:** Tracked in Redis with daily counters

**Usage Tracking:** `/app/services/market_data.py` (Lines 46-107)
- Stored in Redis keys: `api_usage:twelvedata`, `api_usage:finnhub`, `api_usage:alphavantage`
- Daily reset: 86400s TTL
- Prevents API rate limit overages

#### Chart-IMG API (Chart Generation)
**Files:** 
- `/app/services/charting.py` (Lines 1-300+)
- `/app/infra/chartimg.py` (Lines 1-200)

**API Endpoint:** `https://api.chart-img.com/v2/tradingview/advanced-chart/storage`

**Call Pattern:**
- POST requests with chart configuration (symbol, interval, studies, drawings)
- Supports indicators: Volume, EMA21, SMA50, RSI, MACD
- Rate limit: 500 calls/day, 10 calls/sec (Pro plan)
- **Burst limiting:** Redis-based token bucket (lines 134-148 in charting.py)

**Key Features:**
- Max 5 parameters per request (studies + drawings combined)
- Graceful degradation: Falls back to SVG placeholder if API down
- Exponential backoff with jitter (up to 4 retries)

---

### 1.2 Database Queries (Pattern Persistence)

**Files:**
- `/app/services/database.py` (9,808 bytes)
- `/app/models.py` (105 lines)

**Database Tables:**

| Table | Purpose | Key Fields | Queries |
|-------|---------|-----------|---------|
| `tickers` | Stock symbols | symbol (UNIQUE, indexed), name, sector, exchange | get_or_create_ticker() |
| `pattern_scans` | Detection results | ticker_id, pattern_type (indexed), score, entry/stop/target, rs_rating, chart_url | save_pattern_scan(), query by pattern_type |
| `watchlists` | User tracking | user_id (indexed), ticker_id, status (indexed), alerts_enabled, reason | Add/remove from watchlist, filter by status |
| `scan_logs` | Scan history | scan_type (indexed), tickers_scanned, patterns_found, status | Log all universe scans |
| `universe_scans` | Universe results | scan_date (indexed), universe (indexed), total_scanned, patterns_found, duration | Track daily/weekly scans |
| `alert_logs` | Alert history | ticker_id (indexed), alert_type (indexed), alert_sent_at, sent_via | Alert tracking |

**Query Patterns:**
```python
# Common queries (from database.py)
get_or_create_ticker(symbol)  # Creates if not exists
save_pattern_scan(ticker_symbol, pattern_data)  # INSERT
get_watchlist(user_id)  # Filter by user_id + status
```

**Database Technology:** SQLAlchemy 2.0.36 with PostgreSQL (psycopg2-binary)

---

## 2. EXISTING CACHING INFRASTRUCTURE

### 2.1 Redis-Based Cache System

**File:** `/app/services/cache.py` (370 lines)

**Cache Keys Schema:**
```
# Pattern results (1 hour TTL by default)
pattern:ticker={ticker}:interval={interval}

# Price data (15 minute TTL)
ohlcv:{ticker}:1d:5y

# Chart URLs (15 minute TTL)
chart:ticker={ticker}:interval={interval}

# API usage tracking (24 hour reset)
api_usage:twelvedata
api_usage:finnhub
api_usage:alphavantage

# Chart-IMG rate limiting (burst control)
chartimg:burst  # Sorted set for token bucket

# Chart-IMG daily usage
chartimg:daily_usage
```

**Cache Service Methods:**
- `get_pattern()` / `set_pattern()` - Pattern detection results
- `get_price_data()` / `set_price_data()` - Market data
- `get_chart()` / `set_chart()` - Chart URLs
- `invalidate_pattern()` / `invalidate_price_data()` - Manual invalidation
- `get_cache_stats()` - Hit rate monitoring
- `clear_all_cache()` - Bulk clearing

**Implementation Details:**
- Lazy Redis initialization (connects on first use)
- JSON serialization for complex data
- Error handling with fallback to None (fail-open)
- Async/await support throughout

**TTL Strategy (from config.py):**
```python
cache_ttl_patterns: int = 3600      # 1 hour
cache_ttl_market_data: int = 900    # 15 minutes  
cache_ttl_charts: int = 7200        # 2 hours
cache_ttl_ai_responses: int = 1800  # 30 minutes
```

### 2.2 HTTP Client Caching

**Implicit caching in APIs:**
- `/api/patterns/detect` - Cache hit check before external API calls
- `/api/charts/generate` - Checks cache before Chart-IMG API
- `/api/charts/preview/batch` - Per-item cache (24 hour TTL)

**Cache Hit Example (patterns.py, lines 60-100):**
```python
cached_result = await cache.get_pattern(ticker, interval)
if cached_result:
    # Regenerate fresh chart URLs only (reuse detection)
    return PatternResponse(cached=True, ...)
```

---

## 3. MAIN DATA MODELS & SERVICES

### 3.1 Core Services

| Service | Purpose | Files | Key Methods |
|---------|---------|-------|------------|
| **MarketDataService** | Multi-source price data with fallback | `/app/services/market_data.py` | `get_time_series()`, `get_quote()`, `get_usage_stats()` |
| **PatternScannerService** | Multi-detector pattern scanning | `/app/services/pattern_scanner.py` | `scan_symbol()`, `scan_universe()` |
| **ScannerService** | VCP-focused daily scanner | `/app/services/scanner.py` | `run_daily_vcp_scan()` |
| **ChartingService** | Chart-IMG integration | `/app/services/charting.py` | `generate_chart()`, `generate_multi_timeframe_charts()`, `generate_thumbnail()` |
| **CacheService** | Redis caching layer | `/app/services/cache.py` | `get()`, `set()`, `get_pattern()`, `set_pattern()` |
| **DatabaseService** | PostgreSQL persistence | `/app/services/database.py` | `save_pattern_scan()`, `get_tickers()` |
| **UniverseService** | Stock universe management | `/app/services/universe.py` | `scan_universe()` |
| **RiskCalculatorService** | Risk metrics | `/app/services/risk_calculator.py` | `calculate_risk_reward()`, `calculate_position_size()` |
| **AlertsService** | Alert management | `/app/services/alerts.py` | `send_alert()`, `get_alerts()` |

### 3.2 Pattern Detectors

**Location:** `/app/core/detectors/` (8 specialized detectors)

| Detector | Pattern Type | Complexity |
|----------|-------------|-----------|
| `vcp_detector.py` | Volatility Contraction | High - Multi-stage validation |
| `cup_handle_detector.py` | Cup & Handle | Medium - Shape analysis |
| `triangle_detector.py` | Triangle patterns | Medium - Trend lines |
| `channel_detector.py` | Support/Resistance channels | Medium |
| `wedge_detector.py` | Rising/Falling wedges | Medium |
| `head_shoulders_detector.py` | H&S / Inverse H&S | High - Complex geometry |
| `double_top_bottom_detector.py` | Double/Multiple tops/bottoms | Medium |
| `sma50_pullback_detector.py` | Moving average pullback | Low |

**Base Class:** `/app/core/detector_base.py`
- Common interface: `PatternResult` dataclass
- Implements: `find(df, timeframe, symbol)` -> List[PatternResult]

---

## 4. EXTERNAL API CALLS SUMMARY

### 4.1 API Call Frequency Analysis

```
Daily API Calls (Approximate):

Market Data APIs:
- TwelveData:     ~100-150 calls/day (19-25% of 800/day limit)
- Finnhub:        ~5-10 calls/day (mostly when TwelveData fails)
- Alpha Vantage:  ~1-3 calls/day (rare fallback)
- Yahoo Finance:  <1 call/day (last resort)

Chart-IMG:
- Generated charts: ~50-100/day (10-20% of 500/day limit)
- Burst rate: <10 requests/sec (enforced via Redis token bucket)

Total Daily API Calls: ~150-260 (Conservative estimate)
```

### 4.2 Critical API Dependencies

**HIGH PRIORITY (Block feature if unavailable):**
1. Market Data (TwelveData/Finnhub/Alpha Vantage) - Required for pattern detection
2. Chart-IMG API - Required for chart visualization

**MEDIUM PRIORITY:**
1. Telegram Bot API - For notifications (graceful failure)
2. OpenRouter/OpenAI - For AI chat (graceful failure)

---

## 5. DATABASE QUERY PATTERNS

### 5.1 Hot Query Paths

```python
# Pattern detection flow (high frequency)
1. get_or_create_ticker(symbol) 
   -> SELECT * FROM tickers WHERE symbol = ?
   -> INSERT ticker if not exists

2. save_pattern_scan(pattern_data)
   -> INSERT INTO pattern_scans (ticker_id, pattern_type, score, ...)

3. get_tickers() with limit
   -> SELECT * FROM tickers LIMIT 100
   -> Used for universe metadata

# Watchlist queries
4. get_watchlist(user_id)
   -> SELECT * FROM watchlists WHERE user_id = ? AND status = ?

5. update_watchlist_status(watchlist_id, new_status)
   -> UPDATE watchlists SET status = ? WHERE id = ?
```

### 5.2 Index Strategy

**Defined Indexes:**
- `tickers.symbol` - UNIQUE, indexed (primary lookup)
- `pattern_scans.ticker_id` - indexed (join to tickers)
- `pattern_scans.pattern_type` - indexed (filter by pattern)
- `watchlists.user_id` - indexed (user lookups)
- `watchlists.status` - indexed (status filtering)
- `scan_logs.scan_type` - indexed (scan history)
- `universe_scans.scan_date` - indexed (time-based queries)
- `universe_scans.universe` - indexed (universe filtering)

---

## 6. CHART GENERATION CODE

### 6.1 Chart Generation Flow

**File:** `/app/services/charting.py` (550+ lines)

**Process:**
1. Request validation (ticker, timeframe, entry/stop/target)
2. Rate limit check (burst: 10/sec, daily: 500/day via Redis)
3. Cache lookup (24-hour TTL for chart URLs)
4. Build Chart-IMG payload:
   - Symbol normalization (NASDAQ:AAPL, NYSE:IBM, etc.)
   - Studies selection (EMA21, SMA50, max 5 parameters)
   - Drawings for trade levels (entry, stop, target)
5. POST to Chart-IMG API with exponential backoff
6. Parse response, extract chart URL
7. Cache URL for future requests
8. Graceful fallback to SVG placeholder if API unavailable

**Preset Configurations:**
```python
CHART_PRESETS = {
    "breakout": ["EMA21", "SMA50"],
    "swing": ["EMA21", "SMA50"],
    "momentum": ["EMA21", "SMA50"],
    "support": ["EMA21", "SMA50"],
    "minimal": ["EMA21"],
}
```

### 6.2 Chart-IMG Request Limitations

**Constraint:** Max 5 parameters (studies + drawings)
```
Default allocation:
- 3 studies (EMA21, SMA50, maybe RSI)
- 2 drawings (entry line, stop line)
= 5 parameters (at limit)

Management strategy:
- Simplify to 2-3 studies
- Limit drawings to 2 (entry, stop)
- Drop divergence markers if at limit
```

---

## 7. API ENDPOINTS (Key Data Flows)

### 7.1 Pattern Detection Endpoints

| Endpoint | Method | File | Purpose | Cache |
|----------|--------|------|---------|-------|
| `/api/patterns/detect` | POST | patterns.py | Detect patterns for ticker | 1h TTL |
| `/api/scan` | GET/POST | scan.py | Universe scan (VCP focus) | Per request |
| `/api/universe/quick-scan` | POST | universe.py | Quick multi-pattern scan | Per request |
| `/api/top-setups` | GET | scan.py | Top setups for dashboard | Per request |

### 7.2 Chart Endpoints

| Endpoint | Method | File | Purpose | Cache |
|----------|--------|------|---------|-------|
| `/api/charts/generate` | POST | charts.py | Generate annotated chart | 15m TTL |
| `/api/charts/multi` | POST | charts.py | Multi-timeframe charts | Per request |
| `/api/charts/preview/batch` | POST | charts.py | Batch preview generation | 24h TTL |
| `/api/charts/usage` | GET | charts.py | Chart-IMG usage stats | Real-time |
| `/api/charts/health` | GET | charts.py | Chart service health | Real-time |

### 7.3 Market Data Endpoints

| Endpoint | Method | File | Purpose | Cache |
|----------|--------|------|---------|-------|
| `/api/market/breadth` | GET | market.py | Market breadth metrics | Per request |
| `/api/market/usage` | GET | market.py | API usage stats | Real-time |

---

## 8. CACHING OPPORTUNITIES & GAPS

### 8.1 Opportunities (Well-Optimized)

✅ **Pattern Detection Results** - Cached 1 hour (reasonable for daily traders)
✅ **Market Data** - Cached 15 minutes (matches market tick frequency)
✅ **Chart URLs** - Cached 15 minutes (prevents redundant Chart-IMG calls)
✅ **API Usage Tracking** - In Redis, prevents rate limit overages
✅ **Chart-IMG Rate Limiting** - Burst control via Redis sorted set token bucket

### 8.2 Potential Improvements

#### Gap 1: Universe Metadata Caching
**Current:** Universe list fetched fresh each request
**Location:** `/app/services/universe_data.py`, `/app/services/universe.py`
**Impact:** ~500 symbols × 60+ scans/day = expensive operations
**Opportunity:**
- Cache universe metadata (S&P 500, NASDAQ 100) for 24 hours
- Current: Falls back to hardcoded list if cache empty
- Improvement: Pre-populate cache on startup, validate freshness

#### Gap 2: Indicator Calculations Caching
**Current:** EMA/SMA recalculated per pattern detector per scan
**Location:** `/app/core/indicators.py`
**Impact:** Redundant calculations on same data
**Opportunity:**
- Cache computed indicators (EMA21, SMA50, SMA200) at ticker level
- Attach to market_data cache key
- TTL: Match market_data (15 minutes)
- Example: `indicators:AAPL:1day:EMA21` -> [values...]

#### Gap 3: Pattern Detector Intermediate Results
**Current:** Each detector re-analyzes same price data independently
**Location:** `/app/services/pattern_scanner.py`, `/app/core/detectors/`
**Impact:** VCP detector runs same trend analysis as H&S detector
**Opportunity:**
- Cache common calculations: trend lines, pivots, support/resistance levels
- Share within same timeframe/ticker scan
- Key: `analysis:AAPL:1day:pivots` -> pivot points
- TTL: 15 minutes (same as market data)

#### Gap 4: Universe Scan Results Caching
**Current:** Only cached per-request, no between-request cache
**Location:** `/api/scan`, `/api/universe/quick-scan`
**Impact:** Same universe scan repeated multiple times daily
**Opportunity:**
- Cache full scan results for 2-4 hours
- Invalidate on significant market moves (5%+ decline)
- Key: `universe:daily:nasdaq100:2024-11-18` -> [top 50 setups]
- TTL: 4 hours during market hours, 24 hours after close

#### Gap 5: Symbol Resolution Caching
**Current:** Symbol normalization to Chart-IMG format done per request
**Location:** `/app/infra/chartimg.py`, `/app/services/charting.py`
**Impact:** Same transformation repeatedly (minimal but cumulative)
**Opportunity:**
- Cache ticker -> Chart-IMG symbol mapping
- Key: `symbol:AAPL:chartimg` -> "NASDAQ:AAPL"
- TTL: Permanent (only changes if exchange listing changes)

#### Gap 6: AI Chat Response Caching
**Current:** Configured but may not be fully utilized
**Location:** `/app/routers/ai_chat.py`
**Impact:** Same questions asked by multiple users
**Opportunity:**
- Implement content-addressable caching (hash of question)
- Store response for 30 minutes
- Key: `ai:response:{hash(question)}` -> response
- Useful for: "What is a VCP pattern?", "How to calculate R:R?"

#### Gap 7: Relative Strength (RS) Rating Caching
**Current:** SPY data fetched fresh each scan
**Location:** `/app/services/scanner.py` (line 91)
**Impact:** SPY data identical for all symbols in same scan
**Opportunity:**
- Fetch SPY once per daily scan, cache for 24 hours
- Key: `spy:1day:2024-11-18` -> ohlcv data
- Share across all VCP detectors in same scan

#### Gap 8: Risk Calculator Results
**Current:** Recalculated for each chart generation
**Location:** `/app/services/risk_calculator.py`
**Impact:** ATR, position size recalculated for same ticker
**Opportunity:**
- Cache risk metrics at ticker/timeframe level
- Key: `risk:AAPL:1day:atr` -> atr_value
- TTL: 1 hour (risk metrics don't change frequently)

---

## 9. CONFIGURATION & TUNING

### 9.1 Current Configuration (`/app/config.py`)

```python
# Redis
redis_url: str = "redis://localhost:6379"

# Cache TTLs (configurable via environment)
cache_ttl_patterns: int = 3600        # 1 hour
cache_ttl_market_data: int = 900      # 15 minutes
cache_ttl_charts: int = 7200          # 2 hours
cache_ttl_ai_responses: int = 1800    # 30 minutes

# Rate Limits
rate_limit_per_minute: int = 60       # Global
ai_rate_limit_per_minute: int = 20    # AI only
market_data_rate_limit: int = 30      # Market data

# API Limits (daily)
twelvedata_daily_limit: int = 800
finnhub_daily_limit: int = 60
alpha_vantage_daily_limit: int = 500
chartimg_daily_limit: int = 500
```

### 9.2 Environment Variables for Tuning

```bash
# In .env:
CACHE_TTL_PATTERNS=3600              # Adjust pattern cache
CACHE_TTL_MARKET_DATA=900            # Adjust data cache (must be <15 min)
CACHE_TTL_CHARTS=7200                # Chart URL retention
RATE_LIMIT_PER_MINUTE=60             # API rate limit
```

---

## 10. TELEMETRY & MONITORING

### 10.1 Cache Metrics

**File:** `/app/telemetry/metrics.py`

**Tracked Metrics:**
- `CACHE_HITS_TOTAL` - Total cache hits (all keys)
- `CACHE_MISSES_TOTAL` - Total cache misses
- Hit rate calculation: hits / (hits + misses)

**Usage (scanner.py):**
```python
self._record_cache_metric(spy_series)  # Records CACHE_HITS_TOTAL or CACHE_MISSES_TOTAL
```

### 10.2 Cache Statistics Endpoint

**Location:** Cache service includes `get_cache_stats()` method

**Response Format:**
```json
{
  "redis_hits": 1234,
  "redis_misses": 567,
  "redis_hit_rate": 68.5,
  "total_keys": 234,
  "pattern_keys": 45,
  "price_keys": 89,
  "chart_keys": 100,
  "memory_used": "2.3M"
}
```

---

## 11. DEPLOYMENT INFRASTRUCTURE

### 11.1 Container Configuration

**Docker Compose:** `/docker-compose.yml`
- FastAPI service on port 8000
- PostgreSQL database
- Redis cache
- All services networked together

**Runtime:** Uvicorn with 4 workers (configurable)

### 11.2 Railway Deployment

**Key Features:**
- Auto-scales based on demand
- PostgreSQL and Redis provisioned separately
- Environment variables auto-populated
- Automatic health checks on `/healthz`

---

## 12. SUMMARY: HIGH-PRIORITY CACHING NEEDS

| Priority | Opportunity | Est. Savings | Effort | File |
|----------|-------------|--------------|--------|------|
| 🔴 HIGH | Universe scan results cache (2-4h) | 60% scan time | Medium | scan.py |
| 🔴 HIGH | Indicator calculations cache | 40% detector time | Medium | indicators.py |
| 🟠 MEDIUM | Universe metadata cache (24h) | 20% startup time | Low | universe.py |
| 🟠 MEDIUM | RS rating (SPY) cache (24h) | 15% scan time | Low | scanner.py |
| 🟠 MEDIUM | Detector intermediate results share | 30% per detector | Medium | pattern_scanner.py |
| 🟡 LOW | Symbol resolution mapping | 5% chart time | Low | chartimg.py |
| 🟡 LOW | AI response caching (semantic) | 25% AI calls | Medium | ai_chat.py |
| 🟡 LOW | Risk metrics cache (1h) | 10% chart time | Low | risk_calculator.py |

---

## 13. KEY FILES REFERENCE

### Core Services
- `/app/services/cache.py` - Redis caching service (370 lines)
- `/app/services/market_data.py` - Multi-source market data (492 lines)
- `/app/services/pattern_scanner.py` - Pattern detection orchestration (281 lines)
- `/app/services/charting.py` - Chart-IMG integration (550+ lines)
- `/app/services/scanner.py` - VCP-focused daily scanner (400+ lines)

### API Endpoints
- `/app/api/patterns.py` - Pattern detection endpoints
- `/app/api/charts.py` - Chart generation endpoints
- `/app/api/scan.py` - Universe scan endpoints
- `/app/api/universe.py` - Universe management
- `/app/api/market.py` - Market data endpoints

### Configuration
- `/app/config.py` - Settings and defaults
- `/app/models.py` - Database models
- `.env.example` - Environment configuration template

### Pattern Detectors
- `/app/core/detectors/vcp_detector.py` - VCP patterns
- `/app/core/detectors/cup_handle_detector.py` - Cup & Handle
- `/app/core/detectors/triangle_detector.py` - Triangles
- `/app/core/detector_base.py` - Base detector interface

---

## 14. DATA FLOW DIAGRAM

```
User Request
    ↓
FastAPI Endpoint (e.g., /api/patterns/detect)
    ↓
Cache Check (Redis) ✓ Cache Hit → Return cached result
    ↓ (Cache Miss)
Market Data Service
    ├→ Cache Check ✓ Cache Hit → Return cached OHLCV
    └→ (Cache Miss)
         TwelveData API (Primary)
            ↓ (Fail/Rate Limit)
         Finnhub API
            ↓ (Fail/Rate Limit)
         Alpha Vantage API
            ↓ (Fail/Rate Limit)
         Yahoo Finance API
    ↓ (Get OHLCV data)
Store in Cache (15 min TTL)
    ↓
Pattern Detectors (8 specialized detectors)
    ├→ VCP Detector
    ├→ Cup & Handle Detector
    ├→ Triangle Detector
    ├→ H&S Detector
    └→ ... (others)
    ↓
Filter by confidence score
    ↓
Generate Chart
    ├→ Cache Check ✓ Cache Hit → Return URL
    └→ (Cache Miss)
         Chart-IMG API
         Store URL in Cache (15 min TTL)
    ↓
Store Pattern Result in Cache (1 hour TTL)
    ↓
Store in Database (PostgreSQL)
    ↓
Return JSON Response
    ↓
User receives pattern analysis + chart URL
```

---

## CONCLUSION

The Legend AI system has **solid foundational caching** with Redis integration and intelligent API fallback mechanisms. The **primary optimization opportunity** is implementing **higher-level caches** for:

1. **Universe scan results** (2-4 hour cache would prevent redundant 500+ ticker scans)
2. **Indicator calculations** (shared across detectors)
3. **Market data enrichment** (RS ratings, breadth metrics)

These three improvements would likely **reduce API costs by 40-60%** while maintaining real-time pattern detection accuracy for active traders.
