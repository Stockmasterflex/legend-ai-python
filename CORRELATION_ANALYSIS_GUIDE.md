# Legend AI Python - Codebase Structure & Correlation Analysis Implementation Guide

**Project**: Professional Trading Pattern Scanner
**Repository**: /home/user/legend-ai-python
**Framework**: FastAPI + Pandas/NumPy
**Status**: Active development (50+ endpoints, 12K+ LOC)

---

## 1. PROJECT LAYOUT & MAIN DIRECTORIES

### Core Directory Structure

```
legend-ai-python/
├── app/                          # Main application code
│   ├── api/                      # API routers (15 modules, 60+ endpoints)
│   ├── core/                     # Business logic & algorithms
│   ├── services/                 # Service layer (data fetching, caching, analysis)
│   ├── routers/                  # Additional routers (advanced analysis, AI chat)
│   ├── infra/                    # Infrastructure (Chart-IMG, symbols)
│   ├── middleware/               # HTTP middleware (rate limiting, logging)
│   ├── telemetry/                # Prometheus metrics
│   ├── technicals/               # Technical analysis (Fibonacci, trendlines)
│   ├── ai/                       # AI assistant integration
│   ├── detectors/                # Pattern detectors (advanced patterns)
│   └── main.py                   # FastAPI application entry point
│
├── tests/                        # Test suite (10+ test files)
├── templates/                    # HTML templates (Jinja2)
├── static/                       # Static assets (JS, CSS)
├── requirements.txt              # Python dependencies
└── [Documentation files]         # README, deployment guides, etc.
```

### Module Sizes & Function Count

| Module | Lines | Purpose |
|--------|-------|---------|
| app/services/market_data.py | 659 | Multi-source market data fetching with fallback |
| app/services/charting.py | 561 | Chart generation service |
| app/services/multi_tier_cache.py | 627 | Advanced caching layer |
| app/core/pattern_detector.py | ~1000 | Main pattern detection engine |
| app/api/telegram_enhanced.py | 618 | Telegram bot integration |
| app/api/analyze.py | 330 | Single-ticker analysis endpoint |
| **Total API Endpoints** | **139** | Across 24 API files |

---

## 2. DATA FETCHING/API MODULES

### Market Data Service (`app/services/market_data.py`)
**Purpose**: Intelligent multi-source market data fetching with rate limiting

**Data Sources (Priority Order)**:
1. **Redis Cache** (15-minute TTL for recent data, 7-day for historical)
2. **TwelveData** (800 calls/day limit - primary)
3. **Finnhub** (60 calls/day - fallback)
4. **Alpha Vantage** (500 calls/day - fallback)
5. **Yahoo Finance** (unlimited - last resort)

**Key Methods**:
```python
async def get_time_series(ticker, interval, outputsize) -> Dict[str, List]
    # Returns: {c: [], o: [], h: [], l: [], v: [], t: [], source: str, cached: bool}

async def get_price_data(symbol, period, interval) -> pd.DataFrame
    # Returns DataFrame with OHLCV data

async def get_usage_stats() -> Dict[str, Dict]
    # Returns API usage across all sources
```

**Data Format**:
```python
{
    "c": [closes],      # List[float]
    "o": [opens],       # List[float]
    "h": [highs],       # List[float]
    "l": [lows],        # List[float]
    "v": [volumes],     # List[int]
    "t": [timestamps],  # List[int] (Unix)
    "source": "twelvedata|finnhub|alphavantage|yahoo",
    "cached": bool
}
```

### Universe Management (`app/services/universe.py` & `app/api/universe.py`)
**Purpose**: Manages NASDAQ universe of ~3,500 stocks

**Key Endpoints**:
- `GET /api/universe/list` - Get all symbols
- `GET /api/universe/{symbol}` - Symbol details
- `POST /api/universe/scan` - Scan subset by criteria

### Scanning Service (`app/services/scanner.py`)
**Purpose**: Parallel pattern detection across universe

**Key Methods**:
```python
async def scan_universe(tickers: List[str], timeout=None) -> List[ScanResult]
async def scan_single(ticker: str) -> Optional[ScanResult]
```

### Charting Service (`app/services/charting.py`)
**Purpose**: Generate professional TradingView charts via Chart-IMG API

**Endpoints**:
- `GET /api/charts/chart-img/{ticker}` - Single chart
- `POST /api/charts/batch` - Multiple charts

---

## 3. ANALYSIS & VISUALIZATION MODULES

### A. Pattern Detection (`app/core/` & `app/detectors/`)

**Available Patterns**:
- **VCP** (Volatility Contraction Pattern) - `vcp_detector.py`
- **Cup & Handle** - `cup_handle_detector.py`
- **Triangles** (Ascending, Descending, Symmetrical)
- **Head & Shoulders** (Normal & Inverse)
- **Wedges** (Rising, Falling)
- **Double/Triple Tops & Bottoms**
- **Channels** (Up, Down, Sideways)
- **50+ Advanced Patterns** - `app/detectors/advanced/patterns.py`

**Detection API**:
```python
@router.post("/api/patterns/detect")
async def detect_patterns(request: PatternRequest) -> PatternResponse
    # Input: {ticker: str, interval: str, use_yahoo_fallback: bool}
    # Output: PatternResult with confidence, entry, stop, target
```

### B. Technical Analysis Indicators (`app/core/indicators.py`)

**Implemented Indicators**:
- SMA (Simple Moving Average)
- EMA (Exponential Moving Average)
- RSI (Relative Strength Index)
- ATR (Average True Range)
- Divergence detection

**Advanced Technicals** (`app/routers/advanced_analysis.py`):
- **Trendlines**: Auto-detect support/resistance with ML
- **Fibonacci**: Auto-calculate retracement/extension levels
- **Channels**: Detect price channels

**API Endpoints**:
```
POST /api/advanced/patterns/detect
POST /api/advanced/trendlines/detect
POST /api/advanced/fibonacci/auto
POST /api/advanced/fibonacci/manual
POST /api/advanced/comprehensive-analysis
```

### C. Market Analysis (`app/api/market.py`)

**Market Breadth Metrics**:
- Advance/Decline ratio
- % Above 50/200 EMA
- New 52-week highs/lows

**Methods**:
```python
async def _calculate_market_breadth(universe_tickers, max_tickers=50) -> Dict
```

### D. Risk Management (`app/services/risk_calculator.py`)

**Calculations**:
- Position sizing (Kelly Criterion)
- Risk/reward ratios
- Stop loss placement
- Target calculation

**API**:
```
POST /api/risk/calculate
POST /api/risk/kelly-criterion
```

---

## 4. WHERE CORRELATION ANALYSIS WOULD FIT BEST

### Recommended Implementation Strategy

**Primary Location**: Create a dedicated module structure:

```
app/services/correlation_analysis.py    # Core correlation logic
app/api/correlation.py                  # API endpoints
app/core/correlation_stats.py           # Statistical calculations
```

### Integration Points

#### A. Within Advanced Analysis Router (`app/routers/advanced_analysis.py`)
**Location**: `/api/advanced/correlation/*`
**Companion to**: Trendlines, Fibonacci, Pattern detection

#### B. Alongside Market Analysis (`app/api/market.py`)
**Location**: `/api/market/correlation/*`
**Enhancement**: Market breadth + ticker correlation

#### C. Enhanced Pattern Detection
**Location**: Filter pattern results by correlation metrics
**Enhancement**: Identify uncorrelated patterns (lower false signals)

#### D. Watchlist Analysis (`app/api/watchlist.py`)
**Enhancement**: Compute inter-ticker correlations within watchlist

### Data Flow Architecture

```
Market Data Service (timeseries data)
          ↓
    Correlation Service
          ↓
    ┌─────┴─────────┬──────────────┐
    ↓               ↓              ↓
DataFrame     Pandas Corr     Cache Results
(OHLCV)       Matrix/Tests    (Redis)
              
              ↓
          API Endpoints
    
    /api/correlation/matrix
    /api/correlation/pair-analysis
    /api/correlation/cluster-analysis
    /api/correlation/sector-groups
    /api/watchlist/{id}/correlations
```

### Recommended API Endpoints

```python
# Pair-wise correlation
POST /api/correlation/pair-analysis
    Input: {ticker1: str, ticker2: str, period: int, lookback_days: int}
    Output: {correlation: float, p_value: float, r_squared: float, trend: str}

# Correlation matrix
POST /api/correlation/matrix
    Input: {tickers: List[str], period: int}
    Output: {matrix: List[List[float]], tickers: List[str], timestamp: str}

# Sector/group correlations
GET /api/correlation/sector-groups?sector=Technology
    Output: {sector: str, avg_correlation: float, pairs: List[...]}

# Correlation-based clustering
POST /api/correlation/cluster-analysis
    Input: {tickers: List[str], num_clusters: int, method: str}
    Output: {clusters: List[...], silhouette_score: float}

# Watchlist correlations
GET /api/watchlist/{watchlist_id}/correlations?min_threshold=0.7
    Output: {high_corr_pairs: List[...], isolated_tickers: List[...]}

# Correlation-filtered patterns
POST /api/patterns/detect?filter_by_correlation=true&max_correlation=0.6
    Output: PatternResult[] filtered by correlation threshold
```

---

## 5. EXISTING STATISTICAL ANALYSIS CODE

### A. Statistical Helper Functions (`app/core/detector_base.py`)

**Currently Implemented**:
```python
class StatsHelper:
    @staticmethod
    def kendall_tau(series: np.ndarray) -> float
        # Kendall's τ correlation with time index (detects trend)
        # Uses: scipy.stats.kendalltau
    
    @staticmethod
    def volume_z_score(volume: np.ndarray, window: int = 20) -> np.ndarray
        # Z-score normalization of volume
        # Returns: rolling z-scores
    
    @staticmethod
    def atr(high, low, close, period=14) -> np.ndarray
        # Average True Range calculation
    
    @staticmethod
    def curvature_score(prices: np.ndarray) -> float
        # Smoothness score based on second derivative
        # Used for Cup & Handle roundedness detection
    
    @staticmethod
    def zigzag_pivots(high, low, close, atr) -> List[tuple]
        # Pivot detection using adaptive threshold
```

### B. Pattern Detection Logic with Statistics (`app/detectors/advanced/patterns.py`)

**Statistical Methods Used**:
```python
# Standard deviation for peak/trough prominence
peaks_idx, peak_props = find_peaks(highs, distance=5, prominence=highs.std() * 0.5)

# Coefficient of Variation for tightness
tight = seg["close"].std()/max(1e-9, seg["close"].mean()) < 0.015

# Z-score thresholding for volume
volume_z = (volume - rolling_mean) / rolling_std
```

### C. Volatility Analysis

**In Pattern Detectors**:
```python
# VCP Detector
volatility = data["close"].std() / data["close"].mean()

# Volume surge detection
volume_z_score_threshold = 2.0  # std devs above mean
```

### D. Trend Detection (`app/core/detector_base.py`)

```python
def kendall_tau(series: np.ndarray) -> float:
    """Kendall's τ correlation with time index (detects trend)"""
    from scipy.stats import kendalltau
    x = np.arange(len(series))
    tau, p_value = kendalltau(x, series)
    return tau
```

---

## 6. IMPLEMENTATION RECOMMENDATIONS FOR TICKER CORRELATION ANALYSIS

### Quick Win Implementation (Phase 1 - 2 weeks)

**Files to Create**:

1. **`app/services/correlation_analysis.py`** (200-300 LOC)
   ```python
   class CorrelationAnalysisService:
       async def calculate_pair_correlation(ticker1, ticker2, lookback_days=100) -> Dict
       async def calculate_correlation_matrix(tickers: List[str], lookback_days=100) -> Dict
       async def get_sector_correlations(sector: str) -> Dict
   ```

2. **`app/api/correlation.py`** (300-400 LOC)
   ```python
   @router.post("/api/correlation/pair-analysis")
   @router.post("/api/correlation/matrix")
   @router.get("/api/correlation/sector-groups")
   ```

3. **`app/core/correlation_stats.py`** (200-250 LOC)
   ```python
   def calculate_pearson_correlation(series1, series2) -> Tuple[float, float, float]
   def calculate_spearman_correlation(series1, series2) -> Tuple[float, float, float]
   def calculate_rolling_correlation(data1, data2, window=20) -> List[float]
   def detect_correlation_breakpoints(series1, series2, window=20) -> List[Dict]
   ```

### Infrastructure Requirements

**Dependencies Already Available**:
- ✅ pandas (2.2.3) - correlation matrices
- ✅ numpy (1.26.4) - numerical operations
- ✅ scipy (1.14.1) - statistical tests (pearson, spearman, kendall)
- ✅ Redis - caching correlation results

**No Additional Packages Needed!**

### Data Pipeline Integration

**Flow**:
```
1. Client Request → /api/correlation/pair-analysis
2. Fetch both tickers via MarketDataService (cached)
3. Convert to DataFrame with aligned dates
4. Calculate correlation metrics (Pearson, Spearman, Kendall)
5. Perform statistical significance tests
6. Cache results (1-hour TTL)
7. Return comprehensive correlation report
```

### Key Design Decisions

1. **Caching Strategy**:
   - Cache correlation results for 1 hour per pair
   - Cache key: `correlation:{ticker1}:{ticker2}:{period}`
   - Invalidate on market close (4 PM ET)

2. **Date Alignment**:
   - Use pandas `merge(how='inner')` to align different data sources
   - Handle missing data with forward fill

3. **Statistical Methods**:
   - Pearson (linear correlation)
   - Spearman (rank correlation)
   - Kendall's τ (already implemented in detector_base.py)
   - Rolling correlation (dynamic)

4. **Performance Optimization**:
   - Limit matrix size: max 100 tickers per request
   - Use vectorized pandas operations
   - Leverage existing MarketDataService caching

### Testing Strategy

**Test Files to Create**:
- `tests/test_correlation_analysis.py` (150-200 LOC)
- Test cases:
  - Pair correlation calculation
  - Correlation matrix generation
  - Statistical significance
  - Edge cases (NaN values, insufficient data)

---

## 7. ARCHITECTURAL PATTERNS & BEST PRACTICES ALREADY IN USE

### Patterns to Follow for Correlation Analysis

1. **Service Layer Pattern** (like `MarketDataService`)
   ```python
   class CorrelationAnalysisService:
       def __init__(self):
           self.cache = get_cache_service()
           self.market_data = market_data_service
   ```

2. **Caching Pattern** (Redis with TTL)
   ```python
   cache_key = f"correlation:{ticker1}:{ticker2}:{period}"
   await self.cache.set(cache_key, result, ttl=3600)
   ```

3. **API Router Pattern** (Pydantic models)
   ```python
   class CorrelationRequest(BaseModel):
       ticker1: str
       ticker2: str
       lookback_days: int = 100
   
   @router.post("/api/correlation/pair-analysis")
   async def calculate_correlation(request: CorrelationRequest) -> CorrelationResponse
   ```

4. **Error Handling** (HTTPException with status codes)
   ```python
   if not data1 or not data2:
       raise HTTPException(status_code=404, detail="Insufficient data")
   ```

5. **Logging** (structured logging with logger)
   ```python
   logger.info(f"Computing correlation for {ticker1} vs {ticker2}")
   ```

---

## 8. EXISTING CORRELATION/STATISTICAL CODE LOCATIONS

| File | Location | Type | Status |
|------|----------|------|--------|
| `detector_base.py` | `app/core/` | Kendall's τ, Z-score | ✅ Implemented |
| `pattern_detector.py` | `app/core/` | STD dev, variance | ✅ Implemented |
| `triangle_detector.py` | `app/core/detectors/` | STD dev calculations | ✅ Implemented |
| `patterns.py` | `app/detectors/advanced/` | Prominence (STD-based) | ✅ Implemented |
| `market.py` | `app/api/` | Basic breadth metrics | ✅ Implemented |
| `market_data.py` | `app/services/` | Data fetching (no stats) | ✅ Implemented |

**Gap**: No module specifically for multi-ticker correlation analysis yet.

---

## 9. DEPLOYMENT & TESTING CONSIDERATIONS

### Environment Setup
```bash
# Already configured in .env.example:
REDIS_URL=redis://localhost:6379
TWELVEDATA_API_KEY=...
FINNHUB_API_KEY=...
```

### Testing Framework Already in Place
```python
# pytest is already configured
# Use: pytest tests/test_correlation_analysis.py -v
```

### Performance Targets
- Pair correlation: < 500ms (cached)
- Correlation matrix (50 tickers): < 2s
- Caching hit rate: 80%+ for common pairs

---

## 10. SUMMARY & NEXT STEPS

### Current State
✅ **Strong Foundation**:
- Robust market data fetching with multi-source fallback
- Comprehensive pattern detection engine
- Advanced technical analysis (Fibonacci, trendlines)
- Redis caching layer
- FastAPI framework with 60+ endpoints
- Statistical utilities (Kendall's τ, z-scores, std dev)

### Gap
❌ **Missing**:
- Multi-ticker correlation analysis
- Correlation matrices
- Sector/group correlation tracking
- Correlation-based pattern filtering

### Recommended Approach
**Create 3 new modules** (~700-1000 LOC total):
1. `app/services/correlation_analysis.py` - Core logic
2. `app/api/correlation.py` - API endpoints
3. `app/core/correlation_stats.py` - Statistical functions

**Integration Points**:
- Extend `/api/advanced/*` with correlation endpoints
- Enhance `/api/market/*` with sector correlations
- Filter patterns by correlation threshold
- Extend watchlist analysis

**Timeline**: 2-3 weeks for full implementation with tests

---

## Document Information
- **Repository**: /home/user/legend-ai-python
- **Branch**: claude/ticker-correlation-analysis-01Qtox7J8Gb3sGQxh2QoBCWR
- **Date**: 2025-11-18
- **Total Lines of Code (Backend)**: ~12,000
- **Total Endpoints**: 60+
- **API Modules**: 15
- **Service Modules**: 17
- **Test Coverage**: 10+ test files

