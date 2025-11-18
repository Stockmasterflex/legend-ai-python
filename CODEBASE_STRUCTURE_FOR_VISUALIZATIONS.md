# Legend AI Trading Platform - Comprehensive Codebase Overview

## Executive Summary
Legend AI is a **FastAPI-based trading pattern scanner** that detects chart patterns, analyzes market data, and provides actionable trade setups. The project features:
- FastAPI backend with 20+ API routers
- HTML/CSS/JavaScript frontend with TradingView widget integration
- Multi-pattern detector system (8+ pattern types)
- Market data from multiple sources with intelligent fallback
- Redis-based caching and rate limiting
- PostgreSQL database for historical data
- Telegram bot integration

**Version:** 1.0.0 | **Stack:** Python 3.11 + FastAPI | **UI:** Vanilla JS + CSS + TradingView

---

## 1. PROJECT STRUCTURE & ORGANIZATION

```
legend-ai-python/
├── app/                          # Main FastAPI application
│   ├── main.py                   # FastAPI app initialization (20+ routers)
│   ├── config.py                 # Settings/environment configuration
│   ├── models.py                 # SQLAlchemy database models
│   │
│   ├── api/                      # API route handlers (20+ routers)
│   │   ├── patterns.py           # Pattern detection API
│   │   ├── charts.py             # Chart generation API
│   │   ├── dashboard.py          # Dashboard HTML serving
│   │   ├── scan.py               # Universe scanning
│   │   ├── universe.py           # Stock universe management
│   │   ├── market.py             # Market data/internals
│   │   ├── watchlist.py          # Watchlist management
│   │   ├── trades.py             # Trade tracking
│   │   ├── alerts.py             # Alert system
│   │   ├── analytics.py          # Analytics endpoints
│   │   └── ... (12 more routers)
│   │
│   ├── core/                     # Core business logic
│   │   ├── pattern_detector.py   # Pattern detection (Mark Minervini template)
│   │   ├── pattern_detector_v2.py # V2 pattern detection
│   │   ├── chart_generator.py    # Chart-IMG API wrapper
│   │   ├── indicators.py         # Technical indicators (RSI, EMA, SMA, etc.)
│   │   ├── detector_base.py      # Base detector class
│   │   ├── detector_registry.py  # Pattern detector registry
│   │   ├── detector_config.py    # Detector configuration
│   │   │
│   │   └── detectors/            # Specific pattern detectors
│   │       ├── vcp_detector.py          # Vertical Consolidation Pattern
│   │       ├── cup_handle_detector.py   # Cup & Handle pattern
│   │       ├── double_top_bottom_detector.py
│   │       ├── triangle_detector.py
│   │       ├── head_shoulders_detector.py
│   │       ├── wedge_detector.py
│   │       ├── channel_detector.py
│   │       └── sma50_pullback_detector.py
│   │
│   ├── services/                 # Service layer
│   │   ├── market_data.py        # Multi-source market data fetching
│   │   ├── charting.py           # Chart-IMG service wrapper
│   │   ├── cache.py              # Redis cache service
│   │   ├── multi_tier_cache.py   # Advanced cache strategy
│   │   ├── pattern_scanner.py    # Pattern scanning service
│   │   ├── database.py           # Database operations
│   │   ├── universe.py           # Stock universe service
│   │   ├── universe_store.py     # Universe in-memory store
│   │   └── ... (more services)
│   │
│   ├── routers/                  # Advanced routers
│   │   ├── ai_chat.py            # AI chat assistant
│   │   └── advanced_analysis.py  # Advanced technical analysis
│   │
│   ├── middleware/               # Middleware
│   │   ├── metrics_middleware.py # Prometheus metrics
│   │   ├── rate_limit.py         # Rate limiting
│   │   └── structured_logging.py # Logging
│   │
│   ├── infra/                    # Infrastructure
│   │   └── chartimg.py           # Chart-IMG API client
│   │
│   ├── telemetry/                # Monitoring/observability
│   │   └── monitoring.py
│   │
│   ├── utils/                    # Utilities
│   │   └── build_info.py
│   │
│   └── detectors/advanced/       # Advanced pattern detectors
│       └── patterns.py           # 50+ chart patterns
│
├── templates/                    # Frontend HTML
│   ├── dashboard.html            # Main dashboard (38KB)
│   ├── tv_symbol_lab.html        # TradingView widget lab
│   └── partials/
│       └── tv_widget_templates.html # Reusable TradingView templates
│
├── static/                       # Frontend assets
│   ├── css/
│   │   ├── cyberpunk-design-system.css  # Design system (20KB)
│   │   └── dashboard.css         # Dashboard styles (51KB)
│   ├── js/
│   │   ├── dashboard.js          # Main dashboard controller (80KB)
│   │   └── tv-widgets.js         # TradingView widget helpers
│   └── images/
│
├── tests/                        # Test suite
│   └── ... (test files)
│
├── docs/                         # Documentation
│   ├── API/
│   │   └── SCAN.md
│   ├── TRADINGVIEW_WIDGETS.md    # TradingView integration guide
│   ├── PATTERN_DETECTION_ANALYSIS.md
│   └── ... (20+ docs)
│
├── alembic/                      # Database migrations
│
├── monitoring/                   # Monitoring infrastructure
│
├── requirements.txt              # Python dependencies
├── docker-compose.yml            # Docker setup
├── pytest.ini                    # Testing configuration
├── alembic.ini                   # Database migration config
└── .env.example                  # Environment template
```

---

## 2. EXISTING VISUALIZATION & DASHBOARD COMPONENTS

### 2.1 Dashboard Infrastructure

**Main Dashboard:** `/templates/dashboard.html` (38KB)
- **Framework:** Vanilla JavaScript + Alpine.js (lightweight)
- **Styling:** CSS Grid + Flexbox (custom cyberpunk design system)
- **Architecture:** HTMX-style (no heavy frameworks like React/Vue)

**Key Dashboard Features:**
1. **Analyze Tab** - Single ticker pattern analysis
   - Pattern form with ticker input
   - Real-time results grid
   - Synchronized chart preview
   - TradingView embedded advanced chart

2. **Pattern Scanner Tab** - Universe bulk scanning
   - Multi-ticker analysis
   - Results table with sorting/filtering
   - Top setups extraction

3. **Market Internals Tab** - Market regime display
   - Breadth indicators
   - Market health metrics
   - Internals visualization

4. **Watchlist Tab** - Portfolio tracking
   - Add/remove tickers
   - Status tracking
   - Price alerts

5. **TradingView Integration**
   - Advanced chart widget (embedded in Analyze tab)
   - Daily/Weekly toggle
   - Symbol Lab (full TradingView interface)
   - Ticker tape and heatmaps (available via `/tv` endpoint)

### 2.2 Charting System

**Chart Generation:** `/app/services/charting.py` (200+ lines)
- **Provider:** Chart-IMG API (Professional plan: 500 daily calls)
- **Indicators Support:**
  - EMA21, EMA50, EMA200
  - SMA50, SMA200
  - RSI
  - Volume
  - Custom support/resistance lines
  
**Features:**
- Entry/stop/target annotations
- Multi-timeframe preset support
- Rate-limited with graceful degradation
- Cached chart URLs in Redis

**Chart Presets:**
- `breakout` - EMA21 + SMA50
- `swing` - Moving averages focus
- `momentum` - Indicator-heavy
- `support` - Support/resistance focus
- `minimal` - Ultra-minimal (single EMA21)

**API Endpoints:**
```
POST /api/charts/generate              # Generate single chart
POST /api/charts/multi-timeframe       # Multiple timeframe charts
POST /api/charts/preview-batch         # Bulk preview generation
GET  /api/charts/usage                 # Check Chart-IMG quota
```

### 2.3 Frontend Architecture

**Frontend Stack:**
- **HTML:** Semantic HTML5 templates
- **CSS:** 70KB custom stylesheet (Grid-based layout)
- **JavaScript:** 80KB vanilla JS (no framework dependencies)
- **TradingView:** Embedded widgets via TV Charting Library

**Frontend Features:**
- Real-time form validation
- Async API calls with loading states
- Error handling with toast notifications
- Tab-based navigation
- Responsive design (mobile-friendly)
- WebSocket support (for live updates, not yet implemented)

---

## 3. DATA FETCHING MECHANISMS

### 3.1 Market Data Service

**File:** `/app/services/market_data.py` (24KB)

**Architecture:** Multi-source fallback with intelligent routing

```
Priority Order:
1. Redis Cache (instant)
2. TwelveData (primary, 800 calls/day free tier)
3. Finnhub (60 calls/day free tier)
4. Alpha Vantage (500 calls/day free tier)
5. Yahoo Finance (unlimited, last resort)
```

**Key Methods:**
```python
async def get_time_series(ticker, interval, outputsize)
async def get_intraday(ticker, interval)
async def get_daily(ticker)
async def get_quote(ticker)
async def get_usage_stats()
```

**Supported Intervals:**
- Intraday: 1min, 5min, 15min, 30min, 1h, 4h
- Daily: 1day (daily bars)
- Weekly: 1week

**Response Format:**
```json
{
  "t": [1700000000, ...],  // Unix timestamps
  "o": [150.5, ...],        // Open prices
  "h": [151.2, ...],        // High prices
  "l": [149.8, ...],        // Low prices
  "c": [150.9, ...],        // Close prices
  "v": [1000000, ...]       // Volumes
}
```

### 3.2 Caching Strategy

**File:** `/app/services/cache.py` (15KB)

**Multi-tier Cache:**
1. **L1 Cache:** In-memory (Python dict)
2. **L2 Cache:** Redis (distributed, TTL-based)
3. **L3 Cache:** Database (historical)

**Cache TTL:**
- Market data: 1 hour
- Pattern scans: 24 hours
- Charts: 7 days
- Universe list: 1 day

**Cache Keys Pattern:**
```
market_data:{symbol}:{interval}
pattern_scan:{symbol}:{interval}
chart:{symbol}:{interval}:{entry}:{stop}:{target}
```

### 3.3 Universe Management

**Files:** 
- `/app/services/universe_store.py` - In-memory store
- `/app/services/universe_data.py` - Data loading
- `/app/api/universe.py` - API endpoints

**Available Universes:**
- **S&P 500** - 500 largest US companies
- **NASDAQ 100** - 100 largest NASDAQ stocks
- **Custom lists** - User-defined watchlists

**Universe Data:**
- Symbol
- Company name
- Sector
- Industry
- Market cap
- Exchange

---

## 4. API ENDPOINTS & DATA MODELS

### 4.1 Core API Endpoints

#### Pattern Detection
```
POST /api/patterns/detect
  Request: {ticker, interval, use_yahoo_fallback}
  Response: {success, data: PatternResult, cached, processing_time}
  
GET  /api/patterns/scan-universe
  Params: ?universe=SP500&limit=50&min_score=7.0
  Response: {results: [PatternResult, ...], meta}
```

#### Chart Generation
```
POST /api/charts/generate
  Request: {ticker, interval, entry, stop, target, preset}
  Response: {chart_url, cached, processing_time}
  
POST /api/charts/multi-timeframe
  Request: {ticker, timeframes: [1day, 1week, ...]}
  Response: {charts: {timeframe -> url}}
  
POST /api/charts/preview-batch
  Request: {context, items: [{symbol, interval}, ...]}
  Response: {results: [PreviewItem, ...]}
```

#### Market Data
```
GET  /api/market/quote/{ticker}
  Response: {symbol, price, change, volume, ...}
  
GET  /api/market/bars/{ticker}
  Params: ?interval=1day&limit=100
  Response: {t, o, h, l, c, v}
  
GET  /api/market/internals
  Response: {breadth, advance_decline_ratio, put_call_ratio, ...}
```

#### Scanner & Analysis
```
POST /api/scan/universe
  Request: {symbols: [AAPL, ...], min_score: 7.0}
  Response: {results: [PatternResult, ...]}
  
GET  /api/advanced/patterns/detect
  Params: ?symbol=AAPL&min_confidence=60
  Response: {patterns: [AdvancedPattern, ...]}
  
POST /api/advanced/trendlines/detect
  Request: {symbol, lookback_period}
  Response: {trendlines: [Trendline, ...]}
```

#### Watchlist Management
```
GET  /api/watchlist
  Response: [{symbol, status, entry, stop, target, ...}, ...]
  
POST /api/watchlist
  Request: {symbol, status, entry, stop, target}
  Response: {id, symbol, ...}
  
PUT  /api/watchlist/{id}
  Request: {status, notes}
  Response: Updated watchlist item
  
DELETE /api/watchlist/{id}
  Response: {success}
```

#### Analytics & Performance
```
GET  /api/analytics/performance
  Response: {win_rate, avg_profit, sharpe_ratio, ...}
  
GET  /api/analytics/pattern-stats
  Response: {pattern_name: {win_rate, avg_rr, ...}, ...}
  
GET  /api/metrics/prometheus
  Response: Prometheus metrics for monitoring
```

### 4.2 Data Models

**PatternResult** - Pattern detection output
```python
{
  ticker: str
  pattern: str  # VCP, Cup & Handle, etc.
  score: float  # 0-10 scale
  entry: float
  stop: float
  target: float
  risk_reward: float
  criteria_met: List[str]
  analysis: str
  current_price: float
  support_start: float
  support_end: float
  volume_increasing: bool
  consolidation_days: int
  chart_url: str (optional)
  rs_rating: float (optional)
  timestamp: datetime
}
```

**ChartConfig** - Chart generation request
```python
{
  ticker: str
  interval: str  # 1D, 1W, 4H, etc.
  entry: Optional[float]
  stop: Optional[float]
  target: Optional[float]
  show_volume: bool
  show_ema10: bool
  show_ema21: bool
  show_sma50: bool
  show_sma150: bool
  show_sma200: bool
}
```

**MarketInternals** - Market regime data
```python
{
  breadth_advance: int
  breadth_decline: int
  breadth_unchanged: int
  advance_decline_ratio: float
  put_call_ratio: float
  vix: float
  market_cap_breadth: float
  new_highs: int
  new_lows: int
}
```

---

## 5. DATABASE MODELS & PERSISTENCE

**File:** `/app/models.py` (105 lines)

**SQLAlchemy Models:**

1. **Ticker** - Stock metadata
   - symbol, name, sector, industry, exchange
   - Indexed for fast lookups

2. **PatternScan** - Pattern detection results
   - ticker_id, pattern_type, score, entry, stop, target
   - criteria_met (JSON), analysis, chart_url
   - scanned_at (timestamp index)

3. **Watchlist** - User portfolio tracking
   - ticker_id, status, entry/stop/target prices
   - alerts_enabled, alert_threshold
   - triggered_at, added_at

4. **ScanLog** - Bulk scan history
   - scan_type, tickers_scanned, patterns_found
   - start_time, end_time, status, error_message

5. **UniverseScan** - Universe-level scan results
   - universe (SP500, NASDAQ100, CUSTOM)
   - total_scanned, patterns_found, top_score
   - duration_seconds

6. **AlertLog** - Alert trigger history
   - ticker_id, alert_type, trigger_price
   - alert_sent_at, sent_via, status

**Database Connection:**
- PostgreSQL (production on Railway)
- SQLite (development local)
- Migrations via Alembic (`/alembic`)

---

## 6. FRONTEND FRAMEWORK & VISUALIZATION LIBRARIES

### 6.1 Current Frontend Stack

**No Heavy JavaScript Framework**
- Pure vanilla JavaScript
- No React, Vue, or Angular
- Lightweight Alpine.js for reactive UI
- Minimal dependencies (intentional design choice)

**Visualization Libraries Used:**
- **TradingView Charting Library** (embedded widget)
- **Chart-IMG API** (server-side chart generation)
- **CSS Grid/Flexbox** (custom layouts)

### 6.2 TradingView Integration

**Template Files:**
- `/templates/dashboard.html` - Main dashboard with embedded charts
- `/templates/tv_symbol_lab.html` - Full TradingView interface
- `/templates/partials/tv_widget_templates.html` - Reusable widget templates

**Available TradingView Widgets:**
1. **Advanced Chart Widget**
   - Interactive candlestick charts
   - Drawing tools
   - Technical indicators
   - Multiple timeframes

2. **Ticker Tape Widget**
   - Real-time stock tickers
   - Price movements
   - Customizable symbols

3. **Market Heatmap Widget**
   - Sector-based heatmap
   - Real-time updates
   - Color-coded performance

4. **Symbol Info Widget**
   - Company details
   - Trading stats
   - Dividend/earnings info

**TradingView API Reference:**
- Widget initialization via `new TradingView.widget(...)`
- Full docs in `/docs/TRADINGVIEW_WIDGETS.md`

### 6.3 Custom UI Components

**Design System:** `/static/css/cyberpunk-design-system.css` (20KB)
- Color palette (neon blues, greens, reds on dark)
- Typography system
- Button styles
- Form controls
- Badge/tag system
- Animation utilities

**Layout Components:**
- Tabs (tab navigation)
- Forms (input validation)
- Grids (data tables)
- Cards (information panels)
- Modals (dialogs)
- Toasts (notifications)

---

## 7. PATTERN DETECTION CODE LOCATION

### 7.1 Pattern Detectors

**Base Class:** `/app/core/detector_base.py`
```python
class Detector:
    def find(df: DataFrame, timeframe: str, symbol: str) -> List[PatternResult]
```

**Specific Pattern Implementations:**

1. **VCP Detector** - `/app/core/detectors/vcp_detector.py`
   - Vertical Consolidation Pattern (Mark Minervini)
   - Most popular pattern in trend template

2. **Cup & Handle** - `/app/core/detectors/cup_handle_detector.py`
   - Classic reversal pattern
   - High win rate setup

3. **Double Top/Bottom** - `/app/core/detectors/double_top_bottom_detector.py`
   - Reversal patterns at key levels

4. **Triangle** - `/app/core/detectors/triangle_detector.py`
   - Continuation consolidation

5. **Head & Shoulders** - `/app/core/detectors/head_shoulders_detector.py`
   - Classic reversal pattern

6. **Wedge** - `/app/core/detectors/wedge_detector.py`
   - Falling/Rising wedges

7. **Channel** - `/app/core/detectors/channel_detector.py`
   - Parallel support/resistance

8. **SMA50 Pullback** - `/app/core/detectors/sma50_pullback_detector.py`
   - Moving average mean reversion

### 7.2 Advanced Pattern Detector

**File:** `/app/detectors/advanced/patterns.py`

Implements 50+ patterns:
- **Continuation:** Flags, Pennants, Triangles, Wedges, Rectangles
- **Reversal:** Head & Shoulders, Double/Triple Tops/Bottoms, Cup & Handle
- **Candlestick:** Hammers, Engulfing, Harami, Stars, Soldiers/Crows
- **Gaps:** Breakaway, Runaway, Exhaustion, Island Reversals
- **Harmonic:** Gartley, Bat, Butterfly, Crab patterns

### 7.3 Pattern Detector Registry

**File:** `/app/core/detector_registry.py`

```python
def get_all_detectors() -> List[Detector]
  Returns: All registered pattern detectors

def register_detector(detector: Detector)
  Registers custom detector
```

**Pattern Detection Flow:**
```
1. Fetch market data (OHLCV)
2. Convert to DataFrame
3. Run through all detectors
4. Filter by confidence score
5. Sort by score
6. Return results
```

### 7.4 Technical Indicators

**File:** `/app/core/indicators.py`

**Indicators Implemented:**
- Moving Averages (SMA, EMA, DEMA)
- Momentum (RSI, MACD, Stochastic)
- Volatility (ATR, Bollinger Bands)
- Trend (ADX, Trendlines)
- Volume (OBV, CMF)
- Support/Resistance (pivots, levels)

---

## 8. MARKET DATA ANALYSIS TOOLS

### 8.1 Technical Analysis Services

**Risk Calculator:** `/app/services/risk_calculator.py`
```python
def calculate_position_size(capital, entry, stop)
def calculate_risk_reward_ratio(entry, stop, target)
def calculate_kelly_criterion(win_rate, avg_win, avg_loss)
```

**Alerts Service:** `/app/services/alerts.py`
- Price alerts (when stock reaches level)
- Pattern alerts (when pattern detected)
- Volume alerts (unusual volume)
- Breakout alerts

**Scanner Service:** `/app/services/scanner.py`
- Bulk universe scanning
- Multi-pattern detection
- Results aggregation and ranking
- Performance tracking

### 8.2 Market Internals Analysis

**Endpoints:**
```
GET /api/market/internals
GET /api/market/breadth/{symbol}
GET /api/market/sector-performance
GET /api/market/volatility-index
```

**Metrics Tracked:**
- Advance/Decline ratio
- New highs/lows
- Put/Call ratio
- VIX (volatility index)
- Market cap breadth
- Sector rotation

### 8.3 AI-Powered Analysis

**File:** `/app/routers/ai_chat.py` (10KB)

**Features:**
- Natural language pattern analysis
- Trade setup explanations
- Risk management suggestions
- Market sentiment analysis

**Models Used:**
- Anthropic Claude 3.5 Sonnet (default)
- OpenAI GPT-4o-mini (fallback)
- Custom OpenRouter routing

### 8.4 Advanced Technical Analysis

**File:** `/app/routers/advanced_analysis.py` (14KB)

**Capabilities:**
1. **Trendline Detection**
   - Automatic trendline drawing
   - Support/resistance levels
   - Channel identification

2. **Fibonacci Analysis**
   - Auto-swing detection
   - Fibonacci retracements
   - Extension levels
   - Confluence zones

3. **Multi-Pattern Detection**
   - 50+ pattern types
   - Confidence scoring
   - Historical win rates

4. **Support/Resistance**
   - Pivot points
   - Horizontal levels
   - Dynamic S/R zones

---

## 9. KEY FEATURES FOR MARKET VISUALIZATION

### 9.1 Real-time Updates
- WebSocket support (infrastructure in place)
- Redis pub/sub ready
- Async/await throughout codebase

### 9.2 Performance Optimization
- **Caching:** Multi-tier (memory → Redis → DB)
- **API Routing:** Intelligent fallback for API limits
- **Rate Limiting:** Per-IP and per-endpoint
- **Database Indexes:** On commonly queried fields

### 9.3 Error Handling
- Graceful degradation (fallback data sources)
- Detailed error codes and messages
- Structured logging
- Prometheus metrics

### 9.4 Deployment Ready
- Docker support (`Dockerfile`)
- Railway deployment configured
- PostgreSQL + Redis setup
- GitHub Actions CI/CD ready
- Environment variable configuration

---

## 10. RELEVANT DOCUMENTATION

**Key Files:**
- `/docs/TRADINGVIEW_WIDGETS.md` - Embedding TradingView widgets
- `/docs/PATTERN_DETECTION_ANALYSIS.md` - Pattern algorithm details
- `/API_REFERENCE.md` - Complete API documentation
- `/DASHBOARD_IMPROVEMENTS_SUMMARY.md` - Recent UI changes
- `/DATA_FLOW_ARCHITECTURE.md` - System architecture diagram

**Configuration:**
- `.env.example` - All required environment variables
- `requirements.txt` - Python dependencies
- `docker-compose.yml` - Docker setup
- `alembic.ini` - Database migrations

---

## 11. TECHNOLOGY STACK SUMMARY

| Category | Technology | Details |
|----------|-----------|---------|
| **Backend** | FastAPI | Modern async Python web framework |
| **Database** | PostgreSQL + SQLite | Production + Development |
| **Cache** | Redis | Multi-tier caching strategy |
| **Frontend** | Vanilla JS + CSS | No heavy frameworks |
| **Charting** | TradingView + Chart-IMG | Professional charting libraries |
| **Data Sources** | TwelveData, Finnhub, Yahoo | Multi-source fallback |
| **AI** | OpenRouter/Claude | Pattern analysis & explanations |
| **Deployment** | Railway + Docker | One-click deployment |
| **Monitoring** | Prometheus + Structured Logs | Observability |
| **Testing** | Pytest + Playwright | E2E and unit tests |

---

## 12. QUICK REFERENCE: WHERE TO FIND THINGS

| Functionality | Location |
|---------------|----------|
| Pattern detection | `/app/core/detectors/` + `/app/detectors/advanced/` |
| Market data fetching | `/app/services/market_data.py` |
| Chart generation | `/app/services/charting.py` + `/app/api/charts.py` |
| Dashboard UI | `/templates/dashboard.html` |
| Frontend JavaScript | `/static/js/dashboard.js` (80KB) |
| Frontend CSS | `/static/css/` (cyberpunk theme) |
| TradingView widgets | `/templates/partials/tv_widget_templates.html` |
| Database models | `/app/models.py` |
| API endpoints | `/app/api/` (20+ routers) |
| Caching logic | `/app/services/cache.py` + `/app/services/multi_tier_cache.py` |
| Configuration | `/app/config.py` |
| Error handling | `/app/core/errors.py` |
| Risk calculations | `/app/services/risk_calculator.py` |
| AI analysis | `/app/routers/ai_chat.py` |
| Advanced analysis | `/app/routers/advanced_analysis.py` |
| Telegram bot | `/app/api/telegram_enhanced.py` |

