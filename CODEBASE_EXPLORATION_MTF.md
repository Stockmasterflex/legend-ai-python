# Legend AI Python Codebase Exploration

## Project Overview
- **Type**: Trading Pattern Detection System with Multi-Timeframe Analysis
- **Total Code**: ~19,717 lines of Python
- **Framework**: FastAPI for API layer
- **Data Sources**: TwelveData, Finnhub, Alpha Vantage, Yahoo Finance
- **Database**: SQLAlchemy ORM (migrations via Alembic)
- **Caching**: Redis-backed multi-tier caching system

---

## 1. CURRENT DIRECTORY STRUCTURE

### Main Application (`/home/user/legend-ai-python/app/`)

```
app/
├── api/                      # FastAPI Route Handlers
│   ├── multitimeframe.py     # ✓ MTF Analysis endpoints
│   ├── patterns.py           # Pattern detection endpoints
│   ├── charts.py             # Chart generation via Chart-IMG API
│   ├── scan.py               # Universe scanning
│   ├── market.py             # Market data endpoints
│   ├── analyze.py            # Single ticker analysis
│   ├── alerts.py             # Alert monitoring
│   ├── trades.py             # Trade management
│   ├── trade_plan.py         # Trade planning
│   ├── telegram*.py          # Telegram bot integration
│   └── [other APIs]          # Risk, watchlist, analytics, etc.
│
├── core/                      # Core Analysis Engine
│   ├── detector_base.py      # Base Detector class + helpers
│   ├── detector_config.py    # Configuration thresholds
│   ├── detector_registry.py  # Central detector registry
│   ├── indicators.py         # ✓ Basic indicators (SMA, EMA, RSI)
│   ├── pattern_detector.py   # Main pattern analysis engine
│   ├── pattern_detector_v2.py
│   ├── detectors/            # Individual Pattern Detectors
│   │   ├── vcp_detector.py              # VCP (Volatility Contraction)
│   │   ├── cup_handle_detector.py       # Cup & Handle
│   │   ├── triangle_detector.py         # Triangles (all types)
│   │   ├── wedge_detector.py            # Wedges
│   │   ├── head_shoulders_detector.py   # H&S patterns
│   │   ├── double_top_bottom_detector.py# Doubles
│   │   ├── channel_detector.py          # Channel patterns
│   │   └── sma50_pullback_detector.py   # SMA-based pullbacks
│   └── [other utilities]
│
├── services/                  # Business Logic Layer
│   ├── market_data.py        # ✓ Multi-source data fetching + API fallback
│   ├── multitimeframe.py     # ✓ MTF Analysis service
│   ├── pattern_scanner.py    # ✓ Multi-detector scanning service
│   ├── charting.py           # ✓ Chart generation (Chart-IMG integration)
│   ├── cache.py              # Redis caching
│   ├── multi_tier_cache.py   # Advanced caching strategy
│   ├── cache_warmer.py       # Cache pre-warming
│   ├── database.py           # Database operations
│   ├── scanner.py            # Pattern scanning workflows
│   ├── universe.py           # Universe management
│   ├── alerts.py             # Alert service
│   ├── trades.py             # Trade tracking
│   └── risk_calculator.py    # Risk/reward calculations
│
├── technicals/                # Technical Analysis Tools
│   ├── fibonacci.py          # ✓ Fibonacci retracements/extensions
│   ├── trendlines.py         # ✓ Automated trendline detection
│   └── [other technical tools]
│
├── infra/                     # Infrastructure Services
│   ├── chartimg.py           # Chart-IMG API wrapper
│   ├── symbols.py            # Symbol management
│   └── [API clients]
│
└── models.py                  # ✓ SQLAlchemy Data Models
    ├── Ticker
    ├── PatternScan
    ├── Watchlist
    ├── ScanLog
    ├── UniverseScan
    ├── AlertLog
```

---

## 2. EXISTING PATTERN DETECTION & TECHNICAL ANALYSIS

### A. Implemented Pattern Detectors (8 Total)

**Registered in `detector_registry.py`:**

| Pattern Type | Detector Class | Key Features |
|---|---|---|
| VCP | `VCPDetector` | Volatility contraction detection, swing analysis, breakout validation |
| Cup & Handle | `CupHandleDetector` | Cup formation, handle pullback, breakout confirmation |
| Triangles | `TriangleDetector` | Ascending, Descending, Symmetrical - convergence scoring |
| Wedges | `WedgeDetector` | Rising/Falling wedges - breakout detection |
| Head & Shoulders | `HeadShouldersDetector` | Regular + Inverse patterns |
| Double Tops/Bottoms | `DoubleTopBottomDetector` | Double patterns |
| Channels | `ChannelDetector` | Up/Down/Sideways channels - parallel line detection |
| SMA 50 Pullback | `SMA50PullbackDetector` | MA-based pullback patterns |

**All detectors inherit from `Detector` base class with:**
- Standard `find(ohlcv, timeframe, symbol)` method
- Configurable thresholds via `DetectorConfig`
- `PatternResult` output format
- RANSAC line fitting
- Volume/ATR analysis

### B. Existing Indicators (in `app/core/indicators.py`)

```python
sma()              # Simple Moving Average
ema()              # Exponential Moving Average
rsi()              # Relative Strength Index (14-period default)
detect_rsi_divergences()  # Bullish/Bearish RSI divergence detection
```

### C. Existing Technical Tools (in `app/technicals/`)

**Fibonacci Levels** (`fibonacci.py`):
- Auto-detect significant swings
- Calculate retracement levels (0.236, 0.382, 0.5, 0.618, 0.786)
- Calculate extension levels (1.272, 1.414, 1.618, 2.0, 2.618)
- Fibonacci time zones, arcs, and fan lines

**Trendline Detection** (`trendlines.py`):
- RANSAC-based trendline fitting
- Support and resistance detection
- Channel detection (parallel trendlines)
- Horizontal support/resistance levels (clustering)
- Strength scoring based on touches, R², and breaks

---

## 3. EXISTING MULTI-TIMEFRAME SUPPORT

### Current MTF Implementation (in `app/services/multitimeframe.py`)

**Supported Timeframes:**
- `1day` (Daily) - 50% weight in confluence score
- `1week` (Weekly) - 25% weight
- `4hour` (4-Hour) - 15% weight
- `1hour` (1-Hour) - 10% weight

**MultiTimeframeResult Data Structure:**
```python
@dataclass
class MultiTimeframeResult:
    ticker: str
    overall_confluence: float     # 0-1 scale
    strong_signal: bool
    signal_quality: str           # "Excellent", "Good", "Fair", "Poor"
    
    daily_1d: TimeframeAnalysis
    weekly_1w: TimeframeAnalysis
    four_hour_4h: TimeframeAnalysis
    one_hour_1h: TimeframeAnalysis
    
    alignment_details: Dict
    recommendations: List[str]
```

**TimeframeAnalysis contains:**
- Pattern type and confidence
- Trend direction (up/down/sideways)
- Trend strength (strong/medium/weak)
- Volume trend (increasing/decreasing/neutral)
- Entry, Stop, Target prices

**API Endpoints:**
- `POST /api/multitimeframe/analyze` - Full MTF analysis
- `POST /api/multitimeframe/quick/{ticker}` - Quick check

---

## 4. DATA STRUCTURES FOR MARKET DATA

### Core Market Data Model (`models.py`)

```python
class Ticker(Base):
    symbol: str              # Primary key
    name, sector, industry   # Company info
    exchange, created_at     # Metadata

class PatternScan(Base):
    ticker_id, pattern_type
    score: float             # Confidence 0-10
    entry, stop, target      # Trade levels
    risk_reward_ratio: float
    criteria_met: List[str]  # JSON array
    volume_dry_up: bool
    consolidation_days: int
    chart_url: str           # Generated chart link
    rs_rating: float         # Relative strength
    scanned_at: datetime

class Watchlist(Base):
    ticker_id, user_id
    status: str              # "Watching", "Breaking Out", "Triggered", etc.
    target_entry, target_stop, target_price
    notes: str
    alerts_enabled: bool
    triggered_at: datetime
```

### Pattern Detection Output (`core/detector_base.py`)

```python
@dataclass
class PatternResult:
    symbol: str
    timeframe: str
    asof: str (ISO8601)
    pattern_type: PatternType    # Enum
    strong: bool                 # confidence >= 0.75
    confidence: float            # [0, 1]
    
    window_start, window_end: str
    lines: Dict                  # Pattern geometry
    touches: Dict[str, int]      # Touch counts
    breakout: Optional[Dict]     # Breakout details
    evidence: Optional[Dict]     # Supporting data
```

### TimeframeAnalysis (`multitimeframe.py`)

```python
@dataclass
class TimeframeAnalysis:
    timeframe: str
    pattern_detected: bool
    pattern_type: Optional[str]
    confidence: float
    trend_direction: str         # "up", "down", "sideways"
    trend_strength: str          # "strong", "medium", "weak"
    volume_trend: str            # "increasing", "decreasing", "neutral"
    entry, stop, target: float
```

---

## 5. MARKET DATA SERVICES

### MarketDataService (`services/market_data.py`)

**Multi-Source Fallback Priority:**
1. Redis Cache (instant)
2. TwelveData (primary, 800 calls/day)
3. Finnhub (60 calls/day)
4. Alpha Vantage (500 calls/day)
5. Yahoo Finance (unlimited, may be blocked)

**Methods:**
- `get_time_series(ticker, interval, outputsize)` - Fetch OHLCV data
- `get_usage_stats()` - API rate limit tracking
- `_check_rate_limit()` - Rate limit validation
- `_increment_usage()` - Track API consumption

**Data Format (OHLCV from APIs):**
```python
{
    "c": [closes],        # Close prices
    "o": [opens],         # Open prices
    "h": [highs],         # High prices
    "l": [lows],          # Low prices
    "v": [volumes],       # Volumes
    "t": [timestamps]     # Unix timestamps
}
```

---

## 6. CHARTING FUNCTIONALITY

### ChartingService (`services/charting.py`)

**Chart-IMG API Integration:**
- Endpoint: `https://api.chart-img.com/v2/tradingview/advanced-chart/storage`
- Rate limit: 10 calls/sec (100ms delay)
- Pro plan: 500 daily calls, no watermark

**Available Indicators:**
- EMA21, EMA50, EMA200 (Exponential MAs)
- SMA50, SMA200 (Simple MAs)
- RSI (Relative Strength Index)
- Volume bars
- Custom support/resistance drawings

**Chart Presets:**
- `breakout`: EMA21 + SMA50
- `swing`: EMA21 + SMA50
- `momentum`: EMA21 + SMA50
- `support`: EMA21 + SMA50
- `minimal`: EMA21 only

---

## 7. SCANNER SERVICE

### PatternScannerService (`services/pattern_scanner.py`)

**Scanning Workflow:**
1. Fetch price data for symbol(s)
2. Convert to DataFrame
3. Run all registered detectors
4. Filter by confidence threshold
5. Sort by score
6. Return results

**Methods:**
- `scan_symbol(symbol, timeframe, pattern_filter)` - Single symbol scan
- `scan_universe(universe, limit, pattern_filter, min_score)` - Bulk scan
- Concurrent scanning with semaphore (8 concurrent by default)

**Output Format:**
```python
{
    "symbol": str,
    "timeframe": str,
    "pattern": str,
    "score": float (0-10),
    "confidence": float (0-1),
    "entry", "stop", "target": float,
    "risk_reward": float,
    "window_start", "window_end": str,
    "strong": bool,
    "evidence": Dict,
    "detected_at": ISO8601
}
```

---

## 8. CONFIGURATION & THRESHOLDS

### VCP Configuration Example (`detector_config.py`)

```python
class VCPConfig:
    MIN_BASE_LENGTH = 30        # Minimum consolidation bars
    MAX_BASE_LENGTH = 200       # Maximum consolidation bars
    MIN_CONTRACTIONS = 3        # Minimum contraction count
    CONTRACTION_THRESHOLD = 0.3 # 30% declines shrinking
    VOLUME_THRESHOLD = 0.75     # Volume dry-up requirement
```

**All configurable via environment variables or CLI flags**

---

## 9. API STRUCTURE

### Main Router Registrations (`main.py`)

```python
app.include_router(multitf_router)          # MTF analysis
app.include_router(patterns_router)         # Pattern detection
app.include_router(charts_router)           # Chart generation
app.include_router(universe_router)         # Universe management
app.include_router(watchlist_router)        # Watchlist management
app.include_router(scan_router)             # Scanning
app.include_router(market_router)           # Market data
app.include_router(alerts_router)           # Alerts
app.include_router(trades_router)           # Trade tracking
app.include_router(analytics_router)        # Analytics
```

### Middleware Stack:
- MetricsMiddleware (top) - HTTP metrics capture
- StructuredLoggingMiddleware - Structured logging
- RateLimitMiddleware - 60 req/min per IP
- CORSMiddleware - Cross-origin control

---

## 10. CACHING STRATEGY

### Multi-Tier Cache (`services/multi_tier_cache.py` and `cache.py`)

**Tier 1 (Redis):**
- Fast access (~1ms)
- TTL-based expiration
- Market data cache (24h)
- Pattern results (1h)

**Tier 2 (Database):**
- Persistent storage
- Historical pattern scans
- Watchlist data

**Tier 3 (Warmer):**
- Pre-warm cache for popular symbols
- Scheduled universe scans

---

## RECOMMENDATIONS FOR MTF TRADING SYSTEM

### Best Directory Placement

1. **For MTF Indicator Calculation Engine:**
   ```
   app/core/mtf_indicators/     (NEW)
   ├── __init__.py
   ├── mtf_divergence.py        # Multi-TF divergence detection
   ├── mtf_confluence.py        # Enhanced confluence scoring
   ├── mtf_alignment.py         # Higher TF alignment
   └── mtf_volatility.py        # Cross-TF volatility metrics
   ```

2. **For MTF Pattern Detectors:**
   ```
   app/core/detectors/mtf/      (NEW)
   ├── __init__.py
   ├── mtf_vcp_detector.py      # MTF VCP patterns
   ├── mtf_breakout_detector.py # MTF breakout confluence
   ├── mtf_support_detector.py  # Support/resistance confluence
   ```

3. **For MTF Services:**
   - Extend `app/services/multitimeframe.py` with advanced MTF logic
   - OR create `app/services/mtf_advanced.py` for new functionality

4. **For API Endpoints:**
   - Extend `app/api/multitimeframe.py` with new endpoints
   - Examples:
     - `/api/multitimeframe/divergences/{ticker}`
     - `/api/multitimeframe/confluence-detail/{ticker}`
     - `/api/multitimeframe/alignment-score/{ticker}`

5. **For Database Models:**
   - Extend `app/models.py` with:
     ```python
     class MTFConfluence(Base):
         ticker_id, timeframe
         divergence_score, alignment_score
         confluence_breakdown: Dict  # By TF
         detected_at: datetime
     ```

### Integration Points

1. **With Existing Services:**
   - Hook into `PatternScannerService` for multi-TF pattern detection
   - Extend `ChartingService` for multi-TF chart generation
   - Use `MarketDataService` for data fetching

2. **With Detector Registry:**
   - Register MTF detectors in `detector_registry.py`
   - Follow `Detector` protocol (find method)
   - Return `PatternResult` objects

3. **With Database:**
   - Add MTF results to `PatternScan` model
   - Store in new `MTFConfluence` table
   - Track via `ScanLog` with `scan_type="mtf"`

### Key Reusable Components

- `StatsHelper` - ATR, volume z-score, pivots
- `GeometryHelper` - Line fitting, convergence
- `FibonacciCalculator` - Retracement/extension levels
- `AutoTrendlineDetector` - Trendline support/resistance
- Existing indicators (SMA, EMA, RSI)

---

## Testing Infrastructure

- **Test Framework**: pytest
- **Test Directory**: `/home/user/legend-ai-python/tests/`
- **Key Test Files:**
  - `test_pattern_detection.py` - Pattern detection tests
  - `test_all_detectors_unit.py` - Individual detector tests
  - `test_api_integration.py` - API endpoint tests
  - `test_performance_benchmarks.py` - Performance tests

---

## Database Migrations

- **Tool**: Alembic
- **Config**: `/home/user/legend-ai-python/alembic.ini`
- **Migrations**: `/home/user/legend-ai-python/alembic/versions/`

