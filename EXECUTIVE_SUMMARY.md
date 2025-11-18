# Legend AI - Ticker Correlation Analysis: Codebase Exploration Summary

**Date:** November 18, 2025
**Repository:** /home/user/legend-ai-python  
**Branch:** claude/ticker-correlation-analysis-01Qtox7J8Gb3sGQxh2QoBCWR

---

## Executive Summary

The Legend AI codebase is a **well-architected trading pattern scanner** built with FastAPI, comprising ~12,000 lines of Python code across 24 API files and 17 service modules. The project has a **solid foundation for correlation analysis implementation** with all necessary dependencies already in place and established patterns to follow.

**Good News:** No additional packages are needed! The codebase already includes pandas, numpy, and scipy with all required statistical functions.

---

## 1. PROJECT OVERVIEW

### Key Statistics
- **Total Lines of Code:** ~12,000 (backend)
- **API Endpoints:** 60+ across 24 API files
- **Service Modules:** 17 with specialized business logic
- **Core Modules:** Pattern detection, indicators, statistics helpers
- **Database:** PostgreSQL + Redis caching
- **Framework:** FastAPI + Uvicorn (async)

### Current Functionality
✅ Multi-ticker pattern detection (50+ patterns)  
✅ Real-time market data fetching (5 data sources with fallback)  
✅ Professional chart generation (TradingView integration)  
✅ Technical analysis indicators (SMA, EMA, RSI, ATR)  
✅ Advanced analysis (Fibonacci, Trendlines, Channels)  
✅ Risk management (Kelly Criterion, position sizing)  
✅ Market breadth tracking  
✅ Telegram bot integration  
✅ Comprehensive caching layer (Redis)  

---

## 2. PROJECT STRUCTURE

### Directory Layout
```
app/
├── api/                    (15 routers, 60+ endpoints)
├── services/               (17 modules - business logic)
├── core/                   (algorithms & calculations)
├── routers/                (advanced analysis, AI chat)
├── detectors/              (50+ pattern detectors)
├── technicals/             (Fibonacci, Trendlines)
├── middleware/             (logging, rate limiting)
├── infra/                  (Chart-IMG, symbols)
├── ai/                     (AI assistant)
├── telemetry/              (Prometheus metrics)
└── main.py                 (FastAPI app)
```

### Key Modules by Size
| Module | Lines | Purpose |
|--------|-------|---------|
| market_data.py | 659 | Multi-source data fetching |
| charting.py | 561 | Chart generation |
| multi_tier_cache.py | 627 | Advanced caching |
| pattern_detector.py | ~1000 | Main pattern engine |

---

## 3. DATA FETCHING & MARKET DATA LAYER

### Market Data Service (`app/services/market_data.py`)
**Purpose:** Intelligent multi-source market data fetching with rate limiting and fallback

**Data Sources (Priority Order):**
1. Redis Cache (15 min - 7 day TTL)
2. TwelveData API (800 calls/day)
3. Finnhub API (60 calls/day)
4. Alpha Vantage (500 calls/day)
5. Yahoo Finance (unlimited)

**Data Format:**
```python
{
    "c": [closes],      # List[float]
    "o": [opens],       # List[float]  
    "h": [highs],       # List[float]
    "l": [lows],        # List[float]
    "v": [volumes],     # List[int]
    "t": [timestamps],  # List[int] (Unix)
    "source": str,      # "twelvedata" | "finnhub" | "yahoo" | etc
    "cached": bool
}
```

**Key Methods:**
- `async get_time_series(ticker, interval, outputsize)` - OHLCV data
- `async get_price_data(symbol, period, interval)` - DataFrame
- `async get_usage_stats()` - API usage tracking

### Universe Management
- ~3,500 NASDAQ stocks managed in-memory
- Sector/industry classification
- Screening capabilities

---

## 4. EXISTING ANALYSIS & VISUALIZATION MODULES

### A. Pattern Detection (50+ Patterns)
**Implemented in:** `app/core/`, `app/detectors/`, `app/core/detectors/`

**Main Patterns:**
- VCP (Volatility Contraction Pattern)
- Cup & Handle
- Triangles (Ascending, Descending, Symmetrical)
- Head & Shoulders (Normal & Inverse)
- Wedges, Double Tops/Bottoms
- Channels, 50+ Advanced Patterns

**API:** `POST /api/patterns/detect`

### B. Technical Indicators
- SMA, EMA, RSI, ATR, Divergence Detection
- **Advanced:** Trendlines, Fibonacci, Support/Resistance

**API Endpoints:**
- `POST /api/advanced/patterns/detect`
- `POST /api/advanced/trendlines/detect`
- `POST /api/advanced/fibonacci/auto`
- `POST /api/advanced/comprehensive-analysis`

### C. Market Analysis
**Metrics:** Advance/Decline ratio, % Above 50/200 EMA, New 52-week highs/lows
**Location:** `app/api/market.py`

### D. Risk Management
**Features:** Position sizing (Kelly), Risk/reward ratios, Stop placement
**Location:** `app/services/risk_calculator.py`

---

## 5. EXISTING STATISTICAL ANALYSIS CODE

### Already Implemented Statistical Functions

**In `app/core/detector_base.py` (StatsHelper class):**
- `kendall_tau()` - Kendall's τ correlation with time index (trend detection)
- `volume_z_score()` - Z-score normalization of volume
- `atr()` - Average True Range calculation
- `curvature_score()` - Smoothness scoring (second derivative)
- `zigzag_pivots()` - Pivot detection with adaptive thresholding

**In Pattern Detectors:**
- Standard deviation calculations
- Coefficient of variation (tightness ratio)
- Z-score thresholding
- Volatility analysis

**Existing Usage:**
- Kendall's τ for trend detection
- Std dev for volume surge detection (z-score >= 2.0)
- Standard deviation for peak prominence
- Coefficient of variation for consolidation tightness

### Statistical Methods Already in Use
✅ Kendall's τ (scipy.stats.kendalltau)  
✅ Z-score normalization  
✅ Standard deviation  
✅ Variance calculations  
✅ Rolling window statistics  

**Gap:** No module for **multi-ticker correlation analysis** yet.

---

## 6. WHERE CORRELATION ANALYSIS FITS BEST

### Recommended Implementation Strategy

**Primary Location:** Create dedicated module structure:

```
app/services/correlation_analysis.py    # Core logic (250-300 LOC)
app/api/correlation.py                  # API endpoints (300-350 LOC)
app/core/correlation_stats.py           # Statistical functions (200-250 LOC)
```

### Integration Points

#### 1. Advanced Analysis Router (`app/routers/advanced_analysis.py`)
**Location:** `/api/advanced/correlation/*`
**Rationale:** Natural companion to Trendlines, Fibonacci, Pattern detection

#### 2. Market Analysis (`app/api/market.py`)
**Enhancement:** Add sector correlation heatmaps to market breadth
**Location:** `/api/market/correlation/*`

#### 3. Pattern Detection (`app/api/patterns.py`)
**Enhancement:** Filter patterns by correlation (avoid redundant signals)
**Query Param:** `filter_by_correlation=true&max_correlation=0.6`

#### 4. Watchlist Enhancement (`app/api/watchlist.py`)
**New Endpoint:** `GET /api/watchlist/{id}/correlations`
**Purpose:** Analyze inter-ticker correlations within watchlists

### Data Flow Architecture
```
Market Data Service (OHLCV)
        ↓
Correlation Service
        ↓
┌───────┴────────┬──────────┐
↓                ↓          ↓
DataFrame    Pandas Corr  Cache
(OHLCV)      Matrix/Tests (Redis)
        
              ↓
        API Endpoints
```

---

## 7. RECOMMENDED API ENDPOINTS

### Core Endpoints to Implement

```python
# Pair-wise correlation
POST /api/correlation/pair-analysis
    Input: {ticker1, ticker2, period, lookback_days}
    Output: {correlation, p_value, r_squared, trend}

# Correlation matrix
POST /api/correlation/matrix
    Input: {tickers: List[str], period, lookback_days}
    Output: {matrix: List[List[float]], tickers}

# Sector correlations
GET /api/correlation/sector-groups?sector=Technology
    Output: {sector, avg_correlation, pairs}

# Clustering analysis
POST /api/correlation/cluster-analysis
    Input: {tickers, num_clusters, method}
    Output: {clusters, silhouette_score}

# Watchlist correlations
GET /api/watchlist/{id}/correlations?min_threshold=0.7
    Output: {high_corr_pairs, isolated_tickers}

# Pattern filtering
POST /api/patterns/detect?filter_by_correlation=true&max_corr=0.6
    Output: PatternResult[] filtered by correlation
```

---

## 8. IMPLEMENTATION RECOMMENDATIONS

### Quick Win Approach: 3 New Modules (~1000 LOC Total)

#### Module 1: `app/core/correlation_stats.py` (200-250 LOC)
```python
def calculate_pearson_correlation(series1, series2) -> Tuple[float, float, float]
def calculate_spearman_correlation(series1, series2) -> Tuple[float, float, float]
def calculate_rolling_correlation(data1, data2, window=20) -> List[float]
def detect_correlation_breakpoints(series1, series2, threshold=2.0) -> List[Dict]
def filter_patterns_by_correlation(patterns, threshold=0.7) -> List[Pattern]
```

#### Module 2: `app/services/correlation_analysis.py` (250-300 LOC)
```python
class CorrelationAnalysisService:
    async def calculate_pair_correlation(ticker1, ticker2, lookback_days=100)
    async def calculate_correlation_matrix(tickers: List[str], lookback_days=100)
    async def get_sector_correlations(sector: str)
    async def detect_correlation_clusters(tickers, num_clusters=5)
```

#### Module 3: `app/api/correlation.py` (300-350 LOC)
```python
@router.post("/api/correlation/pair-analysis")
@router.post("/api/correlation/matrix")
@router.get("/api/correlation/sector-groups")
@router.post("/api/correlation/cluster-analysis")
# ... with proper Pydantic models and documentation
```

### Dependencies Required
✅ pandas (2.2.3) - already included  
✅ numpy (1.26.4) - already included  
✅ scipy (1.14.1) - already included  
✅ redis (5.2.1) - already included  

**NO NEW PACKAGES NEEDED!**

### Key Design Decisions

1. **Caching:** 1-hour TTL per pair using Redis (key: `correlation:{ticker1}:{ticker2}:{period}`)
2. **Date Alignment:** Use pandas `merge(how='inner')` for different data sources
3. **Statistical Methods:** Pearson, Spearman, Kendall's τ, Rolling correlation
4. **Performance:** Limit matrix size to 100 tickers, use vectorized operations

### Timeline & Effort

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| Phase 1: Core Stats | Week 1 | Correlation calculations, tests |
| Phase 2: Service Layer | Week 2 | Service implementation, caching |
| Phase 3: API Endpoints | Week 2-3 | 5 endpoints, documentation |
| Phase 4: Advanced Features | Week 3-4 | Clustering, breakpoints, filtering |
| Phase 5: Testing & Docs | Week 4 | Full test coverage, API docs |

**Total Effort:** 3-4 weeks for full implementation

---

## 9. ARCHITECTURAL PATTERNS TO FOLLOW

### 1. Service Layer Pattern (like `MarketDataService`)
```python
class CorrelationAnalysisService:
    def __init__(self):
        self.cache = get_cache_service()
        self.market_data = market_data_service
```

### 2. Caching Pattern (Redis with TTL)
```python
cache_key = f"correlation:{ticker1}:{ticker2}:{period}"
await self.cache.set(cache_key, result, ttl=3600)
```

### 3. API Router Pattern (Pydantic models)
```python
class CorrelationRequest(BaseModel):
    ticker1: str
    ticker2: str
    lookback_days: int = 100

@router.post("/api/correlation/pair-analysis")
async def calculate_correlation(request: CorrelationRequest) -> CorrelationResponse
```

### 4. Error Handling (HTTPException)
```python
if not data1 or not data2:
    raise HTTPException(status_code=404, detail="Insufficient data")
```

### 5. Structured Logging
```python
logger.info(f"Computing correlation for {ticker1} vs {ticker2}")
logger.error(f"Correlation calculation failed: {e}")
```

---

## 10. PERFORMANCE TARGETS

| Metric | Target | Notes |
|--------|--------|-------|
| Pair correlation (cached) | <500ms | Redis hit |
| Pair correlation (first calc) | <2s | Full calculation |
| Correlation matrix (50 tickers) | <3s | Vectorized ops |
| Correlation matrix (100 tickers) | <5s | Max recommended |
| Cache hit rate | >80% | For common pairs |

---

## 11. TESTING STRATEGY

### Create: `tests/test_correlation_analysis.py`

**Test Coverage:**
- Unit tests for all statistical functions
- Integration tests for service layer
- Integration tests for API endpoints
- Edge case handling (NaN, insufficient data)
- Performance benchmarking

```bash
# Run tests
pytest tests/test_correlation_analysis.py -v

# With coverage
pytest tests/test_correlation_analysis.py --cov=app
```

---

## 12. SUMMARY: STRENGTHS & GAPS

### Current Strengths ✅
- Robust market data fetching with multi-source fallback
- Comprehensive pattern detection (50+ patterns)
- Advanced technical analysis (Fibonacci, Trendlines)
- Redis caching layer with smart TTL strategy
- FastAPI framework with 60+ well-designed endpoints
- Statistical utilities (Kendall's τ, z-scores, std dev)
- Excellent error handling and logging
- Professional test infrastructure

### Identified Gaps ❌
- No multi-ticker correlation analysis module
- No correlation matrices for sector analysis
- No correlation-based clustering
- No pattern filtering by correlation thresholds
- No correlation breakpoint detection
- No watchlist correlation analysis

### Solution ✅
**Create 3 new, focused modules** that integrate seamlessly with existing architecture:
1. `app/core/correlation_stats.py` - Statistical calculations
2. `app/services/correlation_analysis.py` - Service layer
3. `app/api/correlation.py` - API endpoints

---

## 13. NEXT STEPS & RECOMMENDATIONS

### Immediate Actions

1. **Review Generated Documentation**
   - [ ] Read `CORRELATION_ANALYSIS_GUIDE.md` (comprehensive)
   - [ ] Read `CORRELATION_ARCHITECTURE.txt` (visual)
   - [ ] Read `CORRELATION_QUICK_REFERENCE.md` (quick start)

2. **Validate Approach**
   - [ ] Review with team
   - [ ] Approve proposed endpoints
   - [ ] Confirm implementation timeline

3. **Begin Implementation**
   - [ ] Start with `app/core/correlation_stats.py`
   - [ ] Follow existing patterns from codebase
   - [ ] Leverage existing utilities (MarketDataService, cache, logging)
   - [ ] Write tests as you go

4. **Development Workflow**
   - [ ] Create branch: `claude/correlation-analysis`
   - [ ] Commit frequently (small, focused commits)
   - [ ] Run tests before each push
   - [ ] Document API endpoints in docstrings

---

## FILES GENERATED

✅ **CORRELATION_ANALYSIS_GUIDE.md** (17 KB)
- Comprehensive 10-section guide
- Detailed API endpoint specifications
- Full implementation recommendations
- Architecture diagrams

✅ **CORRELATION_ARCHITECTURE.txt** (23 KB)
- Visual architecture diagrams
- Data flow illustrations
- Integration points
- Feature breakdown

✅ **CORRELATION_QUICK_REFERENCE.md** (5.8 KB)
- Quick implementation checklist
- File structure template
- Example API requests
- Performance targets

All files saved to: `/home/user/legend-ai-python/`

---

## Conclusion

The Legend AI codebase is **well-positioned for ticker correlation analysis implementation**. With all necessary dependencies already in place, established architectural patterns to follow, and a clear understanding of where the new modules should integrate, implementation can begin immediately. The recommended 3-module approach (~1000 LOC total) will provide comprehensive correlation analysis capabilities while maintaining consistency with the existing architecture.

**Estimated Timeline:** 3-4 weeks for full implementation with tests and documentation
**Effort Level:** Medium (clear requirements, existing patterns, no new dependencies)
**Complexity:** Low-Medium (standard statistical calculations, leveraging existing services)

---

**Prepared by:** Claude Code Analysis
**Date:** November 18, 2025
**Repository:** /home/user/legend-ai-python
**Branch:** claude/ticker-correlation-analysis-01Qtox7J8Gb3sGQxh2QoBCWR
