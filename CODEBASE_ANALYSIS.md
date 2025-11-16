# Legend AI - Comprehensive Codebase Overview

## Executive Summary

Legend AI is a professional trading pattern scanner and analysis platform built with **FastAPI (Python)** backend and **HTML/JavaScript** frontend. It provides real-time pattern detection (VCP, Cup & Handle), market analysis, watchlist management, and risk management tools for swing traders. The system integrates multiple market data sources, AI-powered analysis, and professional charting capabilities.

**Current Scale**: ~12,000 lines of backend Python code | 15+ API routers | 50+ endpoints

---

## 1. TECHNOLOGY STACK

### Backend
- **Framework**: FastAPI 0.104.1 (async Python web framework)
- **Server**: Uvicorn 0.24.0 (ASGI server)
- **Language**: Python 3.11
- **Data Processing**: Pandas 2.1.4, NumPy 1.26.2
- **Database ORM**: SQLAlchemy 2.0.23
- **Caching**: Redis 5.0.1 (async support)

### Frontend
- **Framework**: Vanilla JavaScript (no heavy frameworks)
- **Templating**: Jinja2 (via FastAPI)
- **Charting**: TradingView widgets (embedded)
- **UI Components**: Custom cyberpunk design system (CSS)
- **Real-time Updates**: HTMX-ready (not fully implemented)

### External Services
| Service | Purpose | API Limit | Usage |
|---------|---------|-----------|-------|
| **TwelveData** | Market data (OHLCV) | 800 calls/day | Primary data source |
| **Finnhub** | Market data fallback | 60 calls/day | Fallback when TwelveData depleted |
| **Alpha Vantage** | Market data fallback | 500 calls/day | Secondary fallback |
| **Chart-IMG** | Chart generation | 500 calls/day | TradingView chart rendering |
| **OpenRouter** | AI models | Variable | AI analysis (future) |
| **Telegram Bot API** | Bot interface | Unlimited | Webhook integration |

### Infrastructure
- **Containerization**: Docker (Python 3.11-slim base)
- **Deployment**: Railway (auto-configured, PostgreSQL + Redis included)
- **Database**: PostgreSQL (production) or SQLite (local dev)
- **Monitoring**: Prometheus metrics, structured logging

---

## 2. CURRENT ARCHITECTURE

### Directory Structure

```
legend-ai-python/
├── app/
│   ├── main.py                          # FastAPI entry point
│   ├── config.py                        # Pydantic settings management
│   ├── models.py                        # SQLAlchemy database models
│   │
│   ├── api/                             # 15+ API routers (4,354 lines)
│   │   ├── analyze.py         (330 ln)  # Single-ticker analysis with indicators
│   │   ├── scan.py            (228 ln)  # Universe scanner endpoint
│   │   ├── universe.py         (436 ln)  # Universe management
│   │   ├── charts.py          (415 ln)  # Chart-IMG chart generation
│   │   ├── patterns.py        (247 ln)  # Pattern detection endpoint
│   │   ├── market.py          (347 ln)  # Market breadth/internals
│   │   ├── telegram_enhanced.py (618 ln) # Telegram bot (command handling)
│   │   ├── watchlist.py       (114 ln)  # Watchlist management
│   │   ├── alerts.py          (221 ln)  # Alert system
│   │   ├── trades.py          (226 ln)  # Trade tracking
│   │   ├── risk.py            (268 ln)  # Risk management/position sizing
│   │   ├── trade_plan.py      (50 ln)   # Trade planning
│   │   ├── multitimeframe.py  (167 ln)  # Multi-timeframe analysis
│   │   ├── analytics.py       (50 ln)   # Analytics endpoints
│   │   ├── dashboard.py       (156 ln)  # Dashboard backend
│   │   ├── metrics.py         (11 ln)   # Prometheus metrics
│   │   ├── version.py         (20 ln)   # Version info
│   │   └── tv.py              (52 ln)   # TradingView integration
│   │
│   ├── core/                            # Business logic & algorithms
│   │   ├── pattern_detector.py          # Legacy Minervini pattern detector
│   │   ├── pattern_detector_v2.py       # V2 pattern detector
│   │   ├── classifiers.py               # Trend classification (Minervini, Weinstein)
│   │   ├── indicators.py                # Technical indicators (SMA, EMA, RSI)
│   │   ├── metrics.py                   # Technical metrics (ATR, support/resistance)
│   │   ├── flags.py                     # Feature flags for A/B testing
│   │   ├── detector_base.py             # Base detector class
│   │   ├── detector_config.py           # Configuration for detectors
│   │   ├── detectors/
│   │   │   ├── vcp_detector.py          # VCP (Volatility Contraction Pattern)
│   │   │   └── cup_handle_detector.py   # Cup & Handle pattern
│   │   └── chart_generator.py           # Chart rendering
│   │
│   ├── services/                        # Service layer
│   │   ├── market_data.py               # Multi-source market data fetching
│   │   ├── scanner.py                   # Universe scanning service
│   │   ├── charting.py                  # Chart-IMG integration
│   │   ├── cache.py                     # Redis caching service
│   │   ├── database.py                  # Database operations
│   │   ├── universe.py                  # Universe management
│   │   ├── universe_data.py             # Universe data source
│   │   ├── universe_store.py            # In-memory universe cache
│   │   ├── alerts.py                    # Alert monitoring service
│   │   ├── api_clients.py               # External API clients
│   │   ├── trades.py                    # Trade management
│   │   ├── risk_calculator.py           # Position sizing & Kelly Criterion
│   │   └── multitimeframe.py            # Multi-timeframe analysis
│   │
│   ├── infra/                           # Infrastructure
│   │   ├── chartimg.py                  # Chart-IMG API wrapper
│   │   └── symbols.py                   # Symbol formatting utilities
│   │
│   ├── middleware/                      # HTTP middleware
│   │   ├── rate_limit.py                # Redis-based rate limiting (60 req/min)
│   │   └── structured_logging.py        # Telemetry/logging middleware
│   │
│   └── telemetry/
│       └── metrics.py                   # Prometheus metrics definitions
│
├── templates/                           # HTML templates
│   ├── dashboard.html                   # Main dashboard UI
│   ├── tv_symbol_lab.html               # TradingView symbol picker
│   └── partials/tv_widget_templates.html # TradingView widget templates
│
├── static/                              # Static assets
│   ├── js/
│   │   ├── dashboard.js                 # Dashboard controller (vanilla JS)
│   │   └── tv-widgets.js                # TradingView widget manager
│   └── css/
│       ├── cyberpunk-design-system.css  # Design system
│       └── dashboard.css                # Dashboard styling
│
├── tests/                               # Test suite (1,051 lines)
│   ├── test_analyze_contract.py   (155 ln)
│   ├── test_scanner_service.py    (92 ln)
│   ├── test_market_internals.py   (98 ln)
│   ├── test_charting.py           (98 ln)
│   ├── test_smoke.py              (91 ln)
│   └── ... (9 more test files)
│
├── requirements.txt                     # Python dependencies
├── Dockerfile                           # Container definition
└── .env.example                         # Environment template
```

---

## 3. EXISTING FEATURES & FUNCTIONALITY

### A. Pattern Detection & Analysis

#### 1. **Minervini Trend Template** (app/core/classifiers.py)
- 8-point trend classification system
- Checks:
  - Price above SMA(50) and SMA(200)
  - SMA(50) > SMA(150) > SMA(200)
  - SMA(200) rising (slope check)
  - SMA(50) rising (slope check)
- Returns: `pass: bool`, `failed_rules: [str]`

#### 2. **VCP Detector** (app/core/detectors/vcp_detector.py)
- **Volatility Contraction Pattern** detection
- Key features:
  - Identifies N≥3 contractions (shrinking % declines)
  - Volume dries up during consolidation
  - Strong breakout with volume surge
  - Requires ≥3 clean contractions, last ≤5-8%
  - Minimum 100 bars of data
- Output: PatternResult with confidence score

#### 3. **Cup & Handle Detector** (app/core/detectors/cup_handle_detector.py)
- Classic chart pattern recognition
- Identifies cup formation + handle pullback
- Volume confirmation analysis

#### 4. **Pattern Scoring System** (app/core/pattern_detector.py)
- Score range: 0-10
- Considers:
  - Volume characteristics
  - Consolidation quality
  - Support/resistance levels
  - Relative strength (RS) rating
  - Trend template compliance

### B. Market Data Services

#### **Multi-Source Market Data** (app/services/market_data.py)
```python
Priority order:
1. Redis Cache (instant, 15-min TTL)
2. TwelveData (primary, 800/day)
3. Finnhub (fallback, 60/day)
4. Alpha Vantage (fallback, 500/day)
5. Yahoo Finance (last resort, unlimited)
```
- Returns: OHLCV data (opens, highs, lows, closes, volumes)
- Timeframes: 1-minute, 5-minute, 15-minute, hourly, daily, weekly, monthly
- Usage tracking: Redis-based daily counters with 24-hour reset
- Backoff strategy: Exponential retry on rate limits

### C. Technical Indicators

#### **Implemented Indicators** (app/core/indicators.py)
1. **SMA** (Simple Moving Average) - 20, 50, 150, 200 period
2. **EMA** (Exponential Moving Average) - 21, 50 period
3. **RSI** (Relative Strength Index) - 14 period with smoothing
4. **ATR** (Average True Range) - 14 period volatility
5. **Divergence Detection** - RSI swing divergences

#### **Metrics Calculated** (app/core/metrics.py)
- 52-week highs/lows
- Support/resistance levels
- Volume dry-up detection
- Volatility contractions
- Moving average distances
- Relative strength ratings
- Risk/reward ratios

### D. Universe Scanning

#### **Scanner Service** (app/services/scanner.py)
- Scans up to 600 symbols (configurable)
- Multi-concurrency: 8 concurrent requests
- Supports sector filtering
- Minimum confidence threshold: 0.45 (configurable)
- Returns top N results sorted by score
- Features:
  - SPY relative strength calculation
  - Symbol metadata caching
  - Missing data tracking
  - Duration metrics

#### **Universe Definitions**
- **NASDAQ-100**: ~100 most active tech stocks (hardcoded list in code)
- **S&P 500**: Fetch from Wikipedia (cached 7 days)
- **Custom**: Upload own universe

### E. Charting & Visualization

#### **Chart-IMG Integration** (app/infra/chartimg.py, app/services/charting.py)
- **Endpoint**: `https://api.chart-img.com/v2/tradingview/advanced-chart/storage`
- **Studies** (Simplified for performance):
  - EMA 21 (blue line)
  - SMA 50 (red line)
  - Volume overlay
  - RSI (optional)
- **Drawings**:
  - Long Position (entry, stop, target)
  - Arrow markers for divergences
- **Rate Limit Handling**:
  - 0.1s delay between requests (10/sec)
  - Max 5 total parameters (studies + drawings combined)
  - Graceful degradation if limit exceeded
- **Caching**: 15-minute TTL

#### **TradingView Widget Integration** (static/js/tv-widgets.js, templates/)
- Advanced Chart widget (live price data)
- Ticker tape
- Market heatmaps
- Symbol search
- Daily/Weekly toggle
- Symbol-aware (NASDAQ:TICKER, NYSE:TICKER)

### F. Analysis Endpoints

#### **GET /api/analyze** (app/api/analyze.py)
```python
Parameters:
  ticker: str          # Stock symbol
  tf: str             # "daily" or "weekly"
  bars: int           # Number of bars (100-5000, default 400)

Returns:
  - closes/opens/highs/lows/volumes
  - Minervini trend template analysis
  - Weinstein stage classification
  - Technical indicators (EMA, SMA, RSI)
  - Support/resistance levels
  - Relative strength metrics
  - ATR-based risk plan
  - Moving average crossover analysis
  - RSI divergences
  - Cache metadata
  - Auto-generated chart URL
```
- **Cache**: 1-hour TTL
- **Telemetry**: Duration tracking, cache hits/misses

#### **POST /api/scan** (app/api/scan.py)
- Universal scanner endpoint
- Feature-flagged (enable_scanner flag)
- Returns top setups with scores
- Metadata: build SHA, duration, universe size

### G. Risk Management

#### **Position Sizing** (app/services/risk_calculator.py, app/api/risk.py)
- **2% Rule**: Never risk >2% of account on single trade
  - Allows survival of 50 consecutive losses
- **Kelly Criterion**: Optional position sizing based on win rate
- **Features**:
  - Conservative/Aggressive position variants
  - Break-even calculations
  - Recovery calculations
  - Expected value estimation

### H. Watchlist Management

#### **Watchlist Service** (app/api/watchlist.py)
- Storage: PostgreSQL (primary) or JSON file (fallback)
- Fields:
  - Ticker, reason, target_entry, status
  - Tags (custom labels like "Breakout", "VCP", "Leader")
  - Added date, triggered date
  - Alerts enabled/disabled
- **Cache**: 1-hour Redis TTL for performance

#### **Alert Tags Library** (17 predefined tags)
- Breakout, Momentum, VCP, Pullback
- Earnings, Post-earnings drift
- Leader, Laggard
- Reclaim of 21 EMA, Reclaim of 50 SMA
- First pullback, Late-stage base
- Extended, Gap up, Base-on-base
- Short squeeze, Power trend

### I. Market Internals

#### **Market Breadth** (app/api/market.py)
- Advance/Decline ratio
- % above 50 EMA / 200 EMA
- New 52-week highs/lows
- Samples up to 50 tickers to avoid rate limits

### J. Telegram Bot Integration

#### **Bot Commands** (app/api/telegram_enhanced.py)
- `/start` - Welcome and command menu
- `/pattern TICKER` - Detailed pattern analysis
- `/scan` - Quick scan for top 30 setups
- `/chart TICKER` - Annotated chart
- `/watchlist` - View user watchlist
- `/add TICKER` - Add to watchlist
- `/remove TICKER` - Remove from watchlist
- `/plan TICKER` - Generate trade plan
- `/market` - Market internals
- `/usage` - API usage statistics
- Natural language queries (future)

#### **Features**:
- Webhook-based (auto-configures from Railway)
- Typing indicators
- Markdown formatting with emoji
- Photo responses with captions
- Message formatting
- Error handling with fallbacks

### K. Trade Management

#### **Trade Tracking** (app/api/trades.py, app/services/trades.py)
- Trade entry/exit logging
- Win/loss tracking
- Performance metrics
- Trade journal

---

## 4. DATA SOURCES & REAL-TIME CAPABILITIES

### Market Data Flow
```
Client Request
    ↓
Redis Cache (1) [Hit → 15ms response]
    ↓
TwelveData API (2) [800/day limit]
    ↓
Finnhub Fallback (3) [60/day limit]
    ↓
Alpha Vantage (4) [500/day limit]
    ↓
Yahoo Finance (5) [Unlimited but unreliable]
```

### Real-Time Features
1. **Live Quotes**: TradingView widgets (3-second delayed)
2. **Analysis Caching**: 1-hour for stability, 15-min for market data
3. **Universe Caching**: 
   - In-memory store (app/services/universe_store.py)
   - Seeded on startup from `data/universe_seed.json`
   - ~600 symbols cached
4. **Alert Monitoring**: Background watchlist monitoring (future)

### Data Limitations
- Daily/Weekly only (intraday coming later per dashboard)
- No pre-market/after-hours
- 15-20 min delay on market data (API limitation)
- Rate-limited by multiple sources

---

## 5. AI/ML IMPLEMENTATIONS

### Current AI Usage
1. **OpenRouter Integration** (configured but minimal use)
   - Available in config
   - Not heavily integrated in current version
   - Designed for future intent classification

### Pattern Detection Algorithms (Math-Based, Not ML)
1. **Trend Template Classification** - Rule-based (Minervini)
2. **Stage Analysis** - Rule-based (Weinstein)
3. **Volatility Contraction Detection** - Statistical (ATR-based)
4. **Divergence Detection** - Rule-based (RSI swings)

### Scoring System
- Composite score (0-10) based on:
  - Pattern strength
  - Volume confirmation
  - Trend template compliance
  - Support/resistance quality
  - RS rating

---

## 6. API STRUCTURE

### API Routers Organization
```
15 Routers | 50+ Endpoints | ~4,354 lines

/api/analyze              → Single-ticker analysis
/api/scan                 → Universe scanner
/api/universe/*           → Universe management
/api/charts/*             → Chart generation
/api/patterns             → Pattern detection
/api/market/*             → Market internals
/api/webhook/telegram     → Telegram bot
/api/watchlist/*          → Watchlist CRUD
/api/alerts/*             → Alert management
/api/trades/*             → Trade tracking
/api/risk/*               → Position sizing
/api/trade-plan/*         → Trade planning
/api/multitimeframe/*     → Multi-TF analysis
/api/version              → Build info
/api/metrics              → Prometheus metrics
/api/tv                   → TradingView integration
```

### Response Format
- JSON (except charts which return image URLs)
- Consistent error codes (400, 429, 500)
- Telemetry metadata in responses
- Cache information in analyze responses

---

## 7. AUTHENTICATION & USER MANAGEMENT

### Current Implementation
- **No Authentication Yet** (Phase 1)
- Telegram integration provides user context via chat_id
- Watchlist keyed to "default" user or Telegram chat_id
- Database models support user_id field (future)

### Security Measures Implemented
1. **Rate Limiting** (app/middleware/rate_limit.py)
   - 60 requests/minute per IP
   - Redis-based sliding window
   - Exempts health checks, static files, docs

2. **CORS Middleware**
   - Railway: Restricted to app domain only
   - Local dev: Allow all origins
   - Auto-detects RAILWAY_PUBLIC_DOMAIN

3. **Telegram Webhook Security**
   - Auto-configured from Railway
   - Signature verification (future)

---

## 8. PATTERN RECOGNITION & ALGORITHMIC TRADING

### Implemented Patterns
1. **VCP** (Volatility Contraction Pattern)
   - Minervini methodology
   - High success rate per Minervini research

2. **Cup & Handle**
   - Classic chart pattern
   - Volume confirmation required

3. **Trend Template**
   - 8-point Minervini checks
   - Moving average alignment

4. **Flags & Pennants** (implemented in detectors)

5. **Support/Resistance** (calculated, not detected)

### Trade Setup Features
- Entry price (from pattern bottom)
- Stop loss price (consolidation low)
- Target price (% of pattern size)
- Risk/reward ratio (auto-calculated)
- Position sizing (2% rule, Kelly Criterion)

---

## 9. PERFORMANCE OPTIMIZATIONS

### 1. **Caching Strategy**
| Resource | TTL | Strategy |
|----------|-----|----------|
| Pattern results | 1 hour | Market hours only |
| Market data | 15 min | Per symbol |
| Universe data | 24 hours | Seeded on startup |
| Chart URLs | 15 min | Per symbol+settings |
| Watchlist | 1 hour | Redis + file backup |
| Universe store | In-memory | Refreshed hourly |

### 2. **API Rate Limit Management**
- Daily usage tracking (Redis counters)
- Automatic fallback to next source
- Exponential backoff on errors
- Usage stats endpoint for monitoring

### 3. **Concurrency Control**
- Asyncio with Semaphore (max 8 concurrent)
- Background tasks for monitoring
- Timeout handling (5s per request)

### 4. **Code Organization**
- Service layer (business logic)
- Router layer (HTTP interface)
- Core layer (algorithms)
- Infrastructure layer (external APIs)

### 5. **Middleware Stack**
1. StructuredLoggingMiddleware (telemetry)
2. RateLimitMiddleware (protection)
3. CORSMiddleware (cross-origin)

### 6. **Database Design**
- Indexed queries:
  - ticker_id, symbol, user_id, scan_date
  - Status fields for filtering
- Connection pooling (SQLAlchemy)

---

## 10. TESTING INFRASTRUCTURE

### Test Suite (1,051 lines)
```
tests/
├── test_analyze_contract.py       (155 ln) - Analyze endpoint contracts
├── test_scanner_service.py        (92 ln)  - Scanner logic
├── test_market_internals.py       (98 ln)  - Market breadth calculations
├── test_charting.py               (98 ln)  - Chart-IMG integration
├── test_smoke.py                  (91 ln)  - Health checks
├── test_vcp_detector.py           (77 ln)  - VCP pattern detection
├── test_scan_endpoints.py         (77 ln)  - Scan API endpoints
├── test_pattern_detectors.py      (72 ln)  - Pattern logic
├── test_scan_contract.py          (71 ln)  - Scan request/response
├── test_universe_api.py           (62 ln)  - Universe endpoints
├── test_watchlist_api.py          (47 ln)  - Watchlist CRUD
├── test_market_data.py            (47 ln)  - Market data fetching
├── test_indicators.py             (34 ln)  - Technical indicators
└── test_patterns.py               (30 ln)  - Pattern detection
```

### Testing Tools
- **pytest** 8.4.2
- **pytest-asyncio** 1.3.0
- Unit tests, integration tests
- Async test support

### Test Coverage Areas
- ✅ API endpoint contracts
- ✅ Data validation
- ✅ Pattern detection logic
- ✅ Indicator calculations
- ✅ Market data fetching
- ✅ Caching behavior
- ⏳ E2E tests (Playwright in progress)

---

## DEPLOYMENT & MONITORING

### Deployment
- **Docker**: Python 3.11-slim base image
- **Platform**: Railway (auto-scaling, PostgreSQL, Redis included)
- **Health Checks**: 30s interval, 10s timeout, 5s start period
- **Port**: 8000 (configurable via PORT env variable)

### Monitoring
- **Prometheus Metrics**:
  - analyze_request_duration_seconds
  - scan_request_duration_seconds
  - detector_runtime_seconds
  - chartimg_post_status_total
  - cache_hits_total / cache_misses_total
  - analyze_errors_total / scan_errors_total

- **Structured Logging**:
  - Telemetry middleware logs all requests
  - Event tracking per API call
  - Symbol, interval, status tracking

- **Health Endpoints**:
  - `/health` - Full system status
  - `/api/version` - Build information
  - Redis connectivity tests
  - Database health checks
  - API key presence verification

---

## CONFIGURATION MANAGEMENT

### Environment Variables (app/config.py)
```python
# App
APP_NAME, DEBUG, SECRET_KEY

# Telegram
TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_WEBHOOK_URL

# Market Data APIs
TWELVEDATA_API_KEY, FINNHUB_API_KEY, ALPHA_VANTAGE_API_KEY
TWELVEDATA_DAILY_LIMIT=800, FINNHUB_DAILY_LIMIT=60, etc.

# AI & Charts
OPENROUTER_API_KEY, CHART_IMG_API_KEY

# Infrastructure
REDIS_URL, DATABASE_URL

# CORS
CORS_ORIGINS (auto-detects Railway domain)

# Optional
SENDGRID_API_KEY, ALERT_EMAIL, SMTP_*
```

---

## KNOWN LIMITATIONS

1. **Intraday Analysis**: Daily/Weekly only (per dashboard note)
2. **Authentication**: No user auth system yet (Phase 2)
3. **AI Integration**: Minimal (OpenRouter configured but not used)
4. **Real-time Updates**: 15-20min data delay (API limitation)
5. **Pattern Database**: Patterns not persisted (stateless)
6. **Backtesting**: No historical validation
7. **Order Integration**: No broker connectivity
8. **Mobile**: No mobile app (web-only)

---

## NEXT PHASES (Per ROADMAP.md)

### Phase 1.2: Telegram & Pattern Refinement
- Telegram command enhancements
- Pattern confidence scoring
- RS Rank filtering (>70 minimum)
- Additional pattern types
- Cache warming strategies

### Phase 2: Gradio Dashboard
- Web interface improvements
- Bulk analysis UI
- Trade journal features

### Phase 3: Professional UI
- HTMX for real-time updates
- User authentication
- Advanced reporting

### Phase 4: Launch
- Comprehensive testing
- Documentation
- 24/7 monitoring
- Railway deployment

---

## KEY STATISTICS

| Metric | Value |
|--------|-------|
| **Total Backend Lines** | ~12,000 |
| **API Routers** | 15 |
| **Endpoints** | 50+ |
| **Database Models** | 5 (Ticker, PatternScan, Watchlist, ScanLog, AlertLog) |
| **Test Files** | 14 |
| **Test Coverage** | 1,051 lines |
| **Core Detectors** | 4 (VCP, Cup & Handle, Pattern v1/v2) |
| **Technical Indicators** | 5+ |
| **External APIs** | 5 sources |
| **Middleware** | 3 layers |
| **Cache TTLs** | 5 different strategies |

---

## CONCLUSIONS

**Legend AI is a production-ready trading analysis platform** with:
- ✅ Robust backend architecture (FastAPI, async, multi-source data)
- ✅ Professional pattern detection (math-based, not ML)
- ✅ Intelligent caching and rate limit management
- ✅ Real-time charting integration (TradingView)
- ✅ Comprehensive risk management tools
- ✅ Telegram bot interface
- ✅ Docker & Railway deployment ready
- ✅ Structured logging and Prometheus metrics
- ✅ Solid test foundation

**Ready for enhancement in**:
- User authentication & multi-user support
- AI-powered intent classification
- Advanced pattern persistence & analytics
- Mobile application
- Broker integration for live trading
