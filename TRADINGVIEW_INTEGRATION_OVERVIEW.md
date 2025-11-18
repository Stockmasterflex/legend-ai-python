# Legend AI Codebase - Comprehensive Overview

## Executive Summary

**Legend AI** is a professional trading pattern scanner and analysis platform built with **FastAPI (Python)** backend and HTML/JavaScript frontend. The system provides real-time pattern detection (VCP, Cup & Handle, Triangles, etc.), market analysis, watchlist management, risk calculations, and Telegram bot integration for swing traders.

**Current Scale**: ~12,000 lines of backend Python code | 15+ API routers | 50+ endpoints | 8 pattern detectors

---

## 1. PROJECT STRUCTURE & ARCHITECTURE

### 1.1 Directory Layout

```
legend-ai-python/
├── app/                                 # Main application (FastAPI)
│   ├── main.py                         # FastAPI entry point & router registration
│   ├── config.py                       # Pydantic settings & environment config
│   ├── models.py                       # SQLAlchemy database models
│   ├── lifecycle.py                    # App startup/shutdown handlers
│   ├── docs_config.py                  # OpenAPI documentation config
│   │
│   ├── api/                            # API Route Handlers (15+ routers)
│   │   ├── patterns.py                 # Pattern detection endpoint (/api/patterns/detect)
│   │   ├── scan.py                     # Universe scanning with telemetry & top-setups
│   │   ├── universe.py                 # Universe management & tickers
│   │   ├── charts.py                   # Chart-IMG chart generation
│   │   ├── market.py                   # Market breadth & internals analysis
│   │   ├── telegram.py                 # Telegram webhook handler (/api/webhook/telegram)
│   │   ├── telegram_enhanced.py        # Enhanced bot with NLP & AI intent
│   │   ├── watchlist.py                # Watchlist CRUD operations
│   │   ├── alerts.py                   # Alert monitoring & testing
│   │   ├── trades.py                   # Trade tracking & management
│   │   ├── risk.py                     # Position sizing & Kelly Criterion
│   │   ├── trade_plan.py               # Trading plan generation
│   │   ├── multitimeframe.py           # Multi-timeframe confluence analysis
│   │   ├── analyze.py                  # Single-ticker deep analysis
│   │   ├── analytics.py                # Dashboard analytics
│   │   ├── dashboard.py                # Dashboard backend
│   │   ├── metrics.py                  # Prometheus metrics endpoints
│   │   ├── version.py                  # Version/build info
│   │   ├── tv.py                       # TradingView symbol lab page
│   │   ├── cache_mgmt.py               # Cache management endpoints
│   │   ├── api_usage.py                # API usage tracking
│   │   ├── docs.py                     # Documentation endpoints
│   │   └── errors.py                   # Error documentation
│   │
│   ├── core/                           # Business Logic & Algorithms
│   │   ├── pattern_detector.py         # Legacy Minervini 8-point pattern detector
│   │   ├── pattern_detector_v2.py      # V2 pattern detector
│   │   ├── detector_base.py            # Base class for all detectors
│   │   ├── detector_registry.py        # Central registry for all detectors
│   │   ├── detector_config.py          # Detector configuration
│   │   ├── classifiers.py              # Trend classification (Minervini, Weinstein)
│   │   ├── indicators.py               # Technical indicators (SMA, EMA, RSI, MACD, ATR, etc.)
│   │   ├── metrics.py                  # Technical metrics (support/resistance, contractions)
│   │   ├── flags.py                    # Feature flags (A/B testing)
│   │   ├── error_recovery.py           # Error handling & recovery
│   │   ├── errors.py                   # Custom error classes
│   │   ├── chart_generator.py          # Chart rendering logic
│   │   ├── detectors/                  # Pattern Detector Implementations
│   │   │   ├── vcp_detector.py         # VCP (Volatility Contraction Pattern)
│   │   │   ├── cup_handle_detector.py  # Cup & Handle pattern
│   │   │   ├── triangle_detector.py    # Ascending/Descending/Symmetrical Triangles
│   │   │   ├── wedge_detector.py       # Rising/Falling Wedges
│   │   │   ├── head_shoulders_detector.py  # Head & Shoulders patterns
│   │   │   ├── double_top_bottom_detector.py # Double Top/Bottom patterns
│   │   │   ├── channel_detector.py     # Channel patterns (Up/Down/Sideways)
│   │   │   └── sma50_pullback_detector.py # 50 SMA Pullback pattern
│   │   └── detectors/advanced/patterns.py # Advanced pattern analysis
│   │
│   ├── services/                       # Service Layer (Business Logic)
│   │   ├── market_data.py              # Multi-source market data with fallback
│   │   ├── cache.py                    # Redis caching service
│   │   ├── cache_warmer.py             # Cache warming on startup
│   │   ├── multi_tier_cache.py         # Multi-tier cache (hot/warm/cold)
│   │   ├── database.py                 # SQLAlchemy database operations
│   │   ├── scanner.py                  # Universe scanning service
│   │   ├── pattern_scanner.py          # Multi-pattern scanner service
│   │   ├── universe.py                 # Universe management
│   │   ├── universe_data.py            # Universe data fetching (S&P 500, NASDAQ 100)
│   │   ├── universe_store.py           # In-memory universe cache
│   │   ├── alerts.py                   # Alert monitoring & sending
│   │   ├── charting.py                 # Chart generation service
│   │   ├── trades.py                   # Trade tracking service
│   │   ├── risk_calculator.py          # Position sizing calculator
│   │   ├── multitimeframe.py           # Multi-timeframe analysis
│   │   ├── api_clients.py              # External API client wrappers
│   │   └── __init__.py                 # Service initialization
│   │
│   ├── routers/                        # Additional routers
│   │   ├── ai_chat.py                  # AI chat endpoint
│   │   └── advanced_analysis.py        # Advanced analysis router
│   │
│   ├── infra/                          # Infrastructure/Utilities
│   │   ├── chartimg.py                 # Chart-IMG API wrapper
│   │   ├── symbols.py                  # Symbol formatting utilities
│   │   └── __init__.py
│   │
│   ├── middleware/                     # HTTP Middleware
│   │   ├── rate_limit.py               # Rate limiting (60 req/min per IP)
│   │   ├── structured_logging.py       # Telemetry & structured logging
│   │   ├── metrics_middleware.py       # Prometheus metrics collection
│   │   └── __init__.py
│   │
│   ├── telemetry/                      # Monitoring & Telemetry
│   │   ├── metrics.py                  # Prometheus metric definitions
│   │   ├── monitoring.py               # Monitoring utilities
│   │   ├── alerter.py                  # Alert service
│   │   └── __init__.py
│   │
│   ├── technicals/                     # Technical Analysis
│   │   ├── fibonacci.py                # Fibonacci retracement levels
│   │   ├── trendlines.py               # Trendline analysis
│   │   └── __init__.py
│   │
│   ├── utils/                          # Utility Functions
│   │   ├── build_info.py               # Build/version info
│   │   └── __init__.py
│   │
│   └── ai/                             # AI Integration
│       └── assistant.py                # AI assistant (future)
│
├── templates/                          # HTML Templates
│   ├── dashboard.html                  # Main dashboard UI
│   ├── tv_symbol_lab.html              # TradingView symbol picker
│   └── partials/
│       └── tv_widget_templates.html    # TradingView widget templates
│
├── static/                             # Static Assets
│   ├── js/
│   │   ├── dashboard.js                # Dashboard controller (vanilla JS)
│   │   ├── tv-widgets.js               # TradingView widget manager
│   │   └── ...
│   └── css/
│       ├── cyberpunk-design-system.css # Design system
│       ├── dashboard.css               # Dashboard styling
│       └── ...
│
├── tests/                              # Test Suite
│   ├── test_smoke.py                   # Smoke tests
│   ├── test_analyze_contract.py        # Analyze endpoint tests
│   ├── test_scanner_service.py         # Scanner service tests
│   └── ... (9+ more test files)
│
├── monitoring/                         # Monitoring Infrastructure
│   ├── dashboards/                     # Grafana dashboards
│   └── ...
│
├── alembic/                            # Database migrations
├── alembic.ini                         # Alembic config
├── requirements.txt                    # Python dependencies
├── Dockerfile                          # Container definition
├── docker-compose.yml                  # Docker compose for local dev
├── .env.example                        # Environment template
├── pytest.ini                          # Pytest configuration
└── README.md & docs/                   # Documentation

```

### 1.2 Technology Stack

#### Backend
- **Framework**: FastAPI 0.115.6 (async Python web framework)
- **Server**: Uvicorn 0.32.1 (ASGI server)
- **Language**: Python 3.11+
- **Data Processing**: Pandas 2.2.3, NumPy 1.26.4
- **Database ORM**: SQLAlchemy 2.0.36
- **Caching**: Redis 5.2.1 (async support)
- **Testing**: Pytest 8.4.2, Pytest-AsyncIO 1.3.0
- **Monitoring**: Prometheus-client 0.20.0+

#### Frontend
- **Framework**: Vanilla JavaScript (Gradio 5.9.1 for dashboard)
- **Charting**: TradingView widgets (embedded)
- **UI Components**: Custom cyberpunk design system (CSS)

#### Deployment
- **Containerization**: Docker
- **Infrastructure**: Railway (auto-configured with PostgreSQL + Redis)
- **Database**: PostgreSQL (production) | SQLite (local dev)

#### External Services
| Service | Purpose | Limit | Status |
|---------|---------|-------|--------|
| TwelveData | Market data (OHLCV) | 800 calls/day | Primary |
| Finnhub | Market data fallback | 60 calls/day | Fallback |
| Alpha Vantage | Market data fallback | 500 calls/day | Fallback |
| Yahoo Finance | Market data fallback | Unlimited | Last resort |
| Chart-IMG | Chart generation | 500 calls/day | Active |
| Telegram Bot API | Bot interface | Unlimited | Active |
| OpenRouter | AI models | Variable | Optional |

---

## 2. API ENDPOINTS & WEBHOOK HANDLERS

### 2.1 Complete Endpoint Listing

#### Health & Status
- `GET /` - Root health check
- `GET /health` - Detailed health check (includes Telegram, Redis, database status)
- `GET /healthz` - Simple health check for Railway/K8s

#### Pattern Detection (13+ endpoints)
- `POST /api/patterns/detect` - Detect chart patterns for a ticker
- `GET /api/patterns/cache/stats` - View cache hit rates
- `GET /api/patterns/health` - Pattern service health
- `GET /api/patterns/health/detailed` - Detailed pattern service status

#### Universe Scanning (6+ endpoints)
- `POST /api/scan` - Full universe scan (alias for universe/scan)
- `GET /api/scan` - Flag-gated VCP scanner with telemetry
- `GET /api/scan/patterns` - Multi-pattern scanner with filtering
- `POST /api/universe/scan` - Full universe scan (S&P 500 or NASDAQ 100)
- `POST /api/universe/scan/quick` - Quick scan for responsive dashboard
- `GET /api/universe/tickers` - Get universe tickers
- `GET /api/universe/{universe}` - Get specific universe (sp500, nasdaq100)
- `GET /api/universe/health` - Universe service health
- `GET /api/top-setups` - Get latest top setups for dashboard

#### Chart Generation (2+ endpoints)
- `POST /api/charts/generate` - Generate TradingView-powered chart image
- `GET /api/charts/health` - Chart service health

#### Market Data & Analysis (5+ endpoints)
- `GET /api/market/internals` - Market regime analysis (uptrend, downtrend, consolidation)
- `GET /api/market/health` - Market service health
- `GET /api/analyze/{ticker}` - Deep analysis for single ticker

#### Multi-Timeframe Analysis (3+ endpoints)
- `POST /api/multitimeframe/analyze` - Analyze across multiple timeframes
- `POST /api/multitimeframe/quick/{ticker}` - Fast multi-TF analysis
- `GET /api/multitimeframe/health` - Multi-TF service health

#### Watchlist Management (4+ endpoints)
- `GET /api/watchlist` - Get user's watchlist
- `POST /api/watchlist/add` - Add ticker to watchlist
- `DELETE /api/watchlist/remove/{ticker}` - Remove from watchlist
- `GET /api/watchlist/status/{ticker}` - Check if ticker in watchlist

#### Alert System (4+ endpoints)
- `POST /api/alerts/monitor` - Start monitoring for patterns
- `POST /api/alerts/check-now` - Manually trigger pattern check
- `GET /api/alerts/recent` - Get recent alerts
- `GET /api/alerts/config` - Get alert configuration
- `POST /api/alerts/test` - Send test alert

#### Risk Management (5+ endpoints)
- `POST /api/risk/calculate-position` - Calculate optimal position size
- `POST /api/risk/kelly` - Calculate Kelly Criterion position
- `POST /api/risk/breakeven` - Calculate breakeven points
- `POST /api/risk/recovery` - Calculate recovery scenarios
- `GET /api/risk/health` - Risk service health

#### Trading Plan & Trades (5+ endpoints)
- `POST /api/plan` - Generate trading plan for ticker
- `POST /api/trades/create` - Create new trade record
- `GET /api/trades/{trade_id}` - Get trade details
- `GET /api/trades` - Get all trades
- `POST /api/trades/{trade_id}/close` - Close trade

#### **Telegram Integration (Webhook Handler)**
- `POST /api/webhook/telegram` - **Telegram webhook endpoint** (CRITICAL)
  - Receives Telegram updates via webhook
  - Parses commands: /pattern, /chart, /scan, /help, etc.
  - Supports natural language queries (AI intent classification)
  - Routes to appropriate handlers
  - Returns Telegram-formatted responses

#### Dashboard & Analytics
- `GET /dashboard` - Main dashboard HTML
- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/analytics/performance` - Portfolio analytics

#### TradingView Integration
- `GET /tv` - TradingView Symbol Lab page
- `GET /tv/{symbol}` - TradingView page for specific symbol

#### Utilities
- `GET /api/version` - Get build version/SHA
- `GET /api/metrics` - Prometheus metrics endpoint
- `GET /api/usage` - API usage statistics
- `GET /api/cache/clear` - Clear cache (admin only)
- `GET /api/docs/errors` - Error code documentation
- `GET /api/docs/getting-started` - Getting started guide

### 2.2 Telegram Webhook Handler Deep Dive

**File**: `/app/api/telegram.py` & `/app/api/telegram_enhanced.py`

```python
# Webhook endpoint receives Telegram updates
POST /api/webhook/telegram
{
  "update_id": 12345,
  "message": {
    "message_id": 1,
    "chat": {"id": "YOUR_CHAT_ID"},
    "text": "/pattern NVDA"
  }
}
```

**Handler Flow**:
1. Receives Telegram update via webhook
2. Parses message text and chat ID
3. Classifies command type (slash command or natural language)
4. Routes to appropriate handler:
   - `/pattern {ticker}` → PatternDetector → Format response
   - `/chart {ticker}` → ChartingService → Send photo
   - `/scan` → UniverseScanner → Top results
   - `/help` or `/start` → Return command list
   - Natural language → AI intent classifier → Route to handler

**Supported Commands**:
- `/start` - Welcome message with available commands
- `/help` - Show help menu
- `/pattern TICKER` - Analyze pattern setup
- `/chart TICKER` - Generate chart image
- `/scan` - Quick universe scan
- `/watchlist` - View watchlist
- `/add TICKER` - Add to watchlist
- `/remove TICKER` - Remove from watchlist
- `/plan TICKER` - Get trading plan
- `/market` - Market internals
- `/usage` - API usage stats
- Natural language: "Find VCP patterns", "Show me NVDA chart", etc.

---

## 3. DATA MODELS & DATABASE SCHEMAS

### 3.1 Database Models (SQLAlchemy)

**File**: `/app/models.py`

```python
class Ticker(Base):
    """Stock ticker information"""
    __tablename__ = "tickers"
    - id: Integer (PK)
    - symbol: String(10) - Unique ticker symbol (indexed)
    - name: String(255)
    - sector: String(100)
    - industry: String(100)
    - exchange: String(20)
    - created_at: DateTime
    - updated_at: DateTime

class PatternScan(Base):
    """Pattern scanning results"""
    __tablename__ = "pattern_scans"
    - id: Integer (PK)
    - ticker_id: Integer (FK to tickers)
    - pattern_type: String(50) - VCP, Cup & Handle, etc. (indexed)
    - score: Float - Pattern confidence (0-10)
    - entry_price: Float
    - stop_price: Float
    - target_price: Float
    - risk_reward_ratio: Float
    - criteria_met: Text - JSON array of satisfied criteria
    - analysis: Text - Detailed analysis
    - current_price: Float
    - volume_dry_up: Boolean
    - consolidation_days: Integer
    - chart_url: Text - Generated chart URL
    - rs_rating: Float - Relative Strength rating
    - scanned_at: DateTime (indexed)

class Watchlist(Base):
    """User watchlist with alert tracking"""
    __tablename__ = "watchlists"
    - id: Integer (PK)
    - user_id: String(100) - Telegram user ID or "default" (indexed)
    - ticker_id: Integer (FK to tickers)
    - status: String(50) - "Watching", "Breaking Out", "Triggered", "Completed", "Skipped"
    - target_entry: Float
    - target_stop: Float
    - target_price: Float
    - reason: Text - Why on watchlist
    - notes: Text
    - alerts_enabled: Boolean
    - alert_threshold: Float - % move to trigger alert
    - added_at: DateTime (indexed)
    - triggered_at: DateTime (indexed)
    - updated_at: DateTime

class ScanLog(Base):
    """Universe scanning audit trail"""
    __tablename__ = "scan_logs"
    - id: Integer (PK)
    - scan_type: String(50) - daily, weekly, custom (indexed)
    - tickers_scanned: Integer
    - patterns_found: Integer
    - start_time: DateTime (indexed)
    - end_time: DateTime
    - status: String(20) - completed, failed, partial
    - error_message: Text

class UniverseScan(Base):
    """Universe scanning results by date"""
    __tablename__ = "universe_scans"
    - id: Integer (PK)
    - scan_date: DateTime (indexed)
    - universe: String(50) - "SP500", "NASDAQ100", "CUSTOM" (indexed)
    - total_scanned: Integer
    - patterns_found: Integer
    - top_score: Float
    - duration_seconds: Float
    - status: String(20)
    - error_message: Text

class AlertLog(Base):
    """Alert trigger history"""
    __tablename__ = "alert_logs"
    - id: Integer (PK)
    - ticker_id: Integer (FK to tickers)
    - alert_type: String(50) - price, pattern, breakout, volume (indexed)
    - trigger_price: Float
    - trigger_value: Float
    - alert_sent_at: DateTime (indexed)
    - sent_via: String(50) - telegram, email, push
    - user_id: String(100) (indexed)
    - status: String(20) - sent, failed, acknowledged
```

### 3.2 Pydantic Response Models

**Key Response Models** (used in API endpoints):

```python
# Pattern Detection
class PatternResult:
    ticker: str
    pattern: str  # "VCP", "Cup & Handle", "NONE", etc.
    score: float  # 0-10 scale
    entry: float
    stop: float
    target: float
    risk_reward: float
    criteria_met: List[str]
    analysis: str
    timestamp: datetime
    rs_rating: Optional[float]
    current_price: Optional[float]
    support_start: Optional[float]
    support_end: Optional[float]
    volume_increasing: Optional[bool]
    consolidation_days: Optional[int]
    chart_url: Optional[str]

# Scan Results
class ScanResult:
    ticker: str
    pattern: str
    score: float
    entry: float
    stop: float
    target: float
    risk_reward: float
    current_price: Optional[float]
    source: str  # "SP500", "NASDAQ100"
    chart_url: Optional[str]

class ScanResponse:
    success: bool
    results: List[ScanResult]
    total_scanned: int
    total_found: int
    cached: bool
    scan_time: Optional[float]

# Risk Management
class PositionRequest:
    account_size: float
    entry_price: float
    stop_loss_price: float
    target_price: float
    risk_percentage: Optional[float] = 0.02
    win_rate: Optional[float] = None

# Alert & Watchlist
class WatchlistItem:
    ticker: str
    reason: str
    status: str = "Watching"
    alerts_enabled: bool = True

class AlertResponse:
    success: bool
    message: str
    details: Optional[dict]
```

---

## 4. PATTERN ANALYSIS & ALERT SYSTEMS

### 4.1 Pattern Detection Architecture

#### Detector Registry
**File**: `/app/core/detector_registry.py`

Centralized registry for all 8 pattern detectors:

```python
REGISTERED DETECTORS:
├── VCP Detector (Volatility Contraction Pattern)
├── Cup & Handle Detector
├── Triangle Detector (Ascending, Descending, Symmetrical)
├── Wedge Detector (Rising, Falling)
├── Head & Shoulders Detector (including Inverse H&S)
├── Double Top/Bottom Detector
├── Channel Detector (Up, Down, Sideways)
└── 50 SMA Pullback Detector
```

#### Base Detector Class
**File**: `/app/core/detector_base.py`

```python
class Detector:
    """Base class for all pattern detectors"""
    name: str
    patterns: List[str]
    
    def find(self, df: DataFrame, timeframe: str, symbol: str) -> List[PatternResult]:
        """Analyze OHLCV data and return detected patterns"""
```

#### Pattern Detector (Legacy)
**File**: `/app/core/pattern_detector.py`

Implements Mark Minervini's 8-Point Trend Template:
1. Price above 150 SMA
2. Price above 200 SMA  
3. 150 SMA above 200 SMA
4. 200 SMA trending up for 1+ months
5. 50 SMA above 150 SMA
6. 50 SMA above 200 SMA
7. Price above 50 SMA
8. Close price above 50 SMA

**Pattern Detection Logic**:
- VCP (Volatility Contraction Pattern)
- Cup & Handle Formation
- Flat Base
- Breakout Detection
- RS Rating (Relative Strength vs SPY)

### 4.2 Alert System

**Files**: 
- `/app/services/alerts.py` - Alert monitoring service
- `/app/api/alerts.py` - Alert API endpoints
- `/app/telemetry/alerter.py` - Alert sender

**Alert Flow**:

```
┌─────────────────────────────────────────────┐
│ 1. Start Monitoring                         │
│ POST /api/alerts/monitor                    │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│ 2. Get Watchlist Items                      │
│ Fetch all monitored tickers from database   │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│ 3. Fetch Market Data                        │
│ Get 500-bar daily OHLCV for each ticker     │
│ (Cache: 15 min TTL)                         │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│ 4. Run Pattern Detectors                    │
│ Analyze for patterns (VCP, Cup & Handle)    │
│ Calculate confidence scores                 │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│ 5. Filter by Confidence                     │
│ Only alert if score >= 0.75 (75%)           │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│ 6. Anti-Spam Check                          │
│ Don't alert same ticker twice in 6 hours    │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│ 7. Send Multi-Channel Alerts                │
│ ├─ Telegram (if configured)                 │
│ ├─ Email (SendGrid, if configured)          │
│ └─ Log to database (AlertLog table)         │
└─────────────────────────────────────────────┘
```

**Alert Configuration** (from `/app/services/alerts.py`):

```python
class AlertService:
    min_confidence_threshold = 0.75      # 75% confidence minimum
    last_alerted = {}                    # Track last alert per ticker
    COOLDOWN_PERIOD = 6 * 3600           # 6 hours between alerts
    
    Channels:
    - Telegram: Uses settings.telegram_bot_token & chat_id
    - Email: Uses SendGrid API (settings.sendgrid_api_key)
    - Database: Always logs to alert_logs table
```

**Alert Message Format**:
```
🚨 PATTERN ALERT
================
📊 Stock: NVDA
🎯 Pattern: Cup & Handle
⭐ Score: 8.5/10
💰 Entry: $120.50
🛑 Stop: $115.20
🎯 Target: $135.80
📈 Risk/Reward: 2.15
```

---

## 5. STRATEGY/BACKTESTING INFRASTRUCTURE

### 5.1 Risk Management System

**File**: `/app/services/risk_calculator.py`

```python
class RiskCalculator:
    
    def calculate_position_size(
        account_size: float,
        entry_price: float,
        stop_loss_price: float,
        target_price: float,
        risk_percentage: float = 0.02,  # 2% per trade
        win_rate: Optional[float] = None
    ):
        """Calculate optimal position size using multiple strategies"""
        
        # Strategy 1: 2% Risk Rule (Standard)
        risk_per_share = abs(entry_price - stop_loss_price)
        max_loss = account_size * risk_percentage
        shares = int(max_loss / risk_per_share)
        
        # Strategy 2: Kelly Criterion (if win_rate provided)
        if win_rate:
            risk_reward = (target_price - entry_price) / (entry_price - stop_loss_price)
            kelly_fraction = (win_rate * risk_reward - (1 - win_rate)) / risk_reward
            kelly_shares = int((account_size * kelly_fraction) / entry_price)
        
        # Strategy 3: Conservative (0.5% per trade)
        conservative_shares = int((account_size * 0.005) / risk_per_share)
        
        # Strategy 4: Aggressive (3% per trade)
        aggressive_shares = int((account_size * 0.03) / risk_per_share)
        
        return {
            "recommended": shares,           # 2% rule
            "kelly_criterion": kelly_shares, # Kelly (if available)
            "conservative": conservative_shares,
            "aggressive": aggressive_shares,
            "risk_per_trade": max_loss,
            "potential_profit": (target_price - entry_price) * shares,
            "risk_reward_ratio": (target_price - entry_price) / risk_per_share
        }
```

### 5.2 Trade Tracking

**File**: `/app/services/trades.py`

**Trade Lifecycle**:
```
CREATE ──→ ACTIVE ──→ CLOSED
  │        ├─ Entry confirmed
  │        ├─ Stop loss set
  │        └─ Target tracked
  │
  └─ Track:
    - Entry price
    - Exit price
    - P&L
    - Win rate
    - Risk/reward achieved
```

### 5.3 Multi-Timeframe Analysis

**File**: `/app/services/multitimeframe.py`

Analyzes pattern confluence across timeframes:
```
Timeframes:
├─ 1day (primary)
├─ 4hour (confirmation)
├─ 1hour (entry signal)
├─ 15min (micro-trend)
└─ 5min (scalp opportunity)

Confluence Score:
- All timeframes aligned = +40 points
- 3/5 aligned = +25 points  
- 2/5 aligned = +10 points
```

---

## 6. CONFIGURATION & DEPENDENCIES

### 6.1 Configuration Management

**File**: `/app/config.py` (Pydantic Settings)

```python
class Settings(BaseSettings):
    # Core
    app_name: str = "Legend AI"
    debug: bool = False
    secret_key: str
    cors_origins: str = "*"
    
    # Telegram Bot
    telegram_bot_token: str
    telegram_chat_id: Optional[str]
    telegram_webhook_url: Optional[str]
    
    # AI Services
    openrouter_api_key: Optional[str]
    openai_api_key: Optional[str]
    ai_model: str = "anthropic/claude-3.5-sonnet"
    
    # Market Data APIs
    twelvedata_api_key: Optional[str]
    finnhub_api_key: Optional[str]
    alpha_vantage_api_key: Optional[str]
    
    # Chart Generation
    chartimg_api_key: Optional[str]
    
    # API Rate Limits (daily)
    twelvedata_daily_limit: int = 800
    finnhub_daily_limit: int = 60
    alpha_vantage_daily_limit: int = 500
    chartimg_daily_limit: int = 500
    
    # Caching
    redis_url: str = "redis://localhost:6379"
    cache_ttl_patterns: int = 3600         # 1 hour
    cache_ttl_market_data: int = 900       # 15 minutes
    cache_ttl_charts: int = 7200           # 2 hours
    cache_ttl_ai_responses: int = 1800     # 30 minutes
    
    # Multi-Tier Cache
    cache_hot_ttl_min: int = 300           # 5 minutes
    cache_hot_ttl_max: int = 900           # 15 minutes
    cache_warm_ttl: int = 3600             # 1 hour
    cache_cdn_ttl: int = 86400             # 24 hours
    cache_hot_max_size: int = 10000
    cache_enable_warming: bool = True
    
    # Rate Limits
    rate_limit_per_minute: int = 60
    ai_rate_limit_per_minute: int = 20
    market_data_rate_limit: int = 30
    
    # Database
    database_url: Optional[str]
    
    # Email Alerts
    sendgrid_api_key: Optional[str]
    alert_email: Optional[str]
    
    # Feature Flags
    legend_flags_enable_scanner: int = 1
```

**Environment Variables** (from `.env.example`):
```bash
# Core
TELEGRAM_BOT_TOKEN=your-token
TELEGRAM_CHAT_ID=your-chat-id
TELEGRAM_WEBHOOK_URL=https://your-domain.railway.app

# Market Data
TWELVEDATA_API_KEY=your-key
FINNHUB_API_KEY=your-key
ALPHA_VANTAGE_API_KEY=your-key

# Charts
CHARTIMG_API_KEY=your-key

# AI
OPENROUTER_API_KEY=your-key

# Database
DATABASE_URL=postgresql://user:pass@localhost/dbname

# Redis
REDIS_URL=redis://localhost:6379

# Email
SENDGRID_API_KEY=your-key
ALERT_EMAIL=your-email@example.com

# Feature Flags
LEGEND_FLAGS_ENABLE_SCANNER=1
```

### 6.2 Dependencies

**File**: `/requirements.txt`

```
# Web Framework
fastapi==0.115.6
uvicorn[standard]==0.32.1

# Telegram
python-telegram-bot==21.9

# HTTP Client
httpx==0.28.1

# Cache & Database
redis==5.2.1
sqlalchemy==2.0.36
psycopg2-binary==2.9.10
alembic==1.14.0

# Configuration
pydantic==2.10.6
pydantic-settings==2.7.1
python-dotenv==1.0.0

# Data Processing
pandas==2.2.3
numpy==1.26.4
scipy==1.14.1

# AI
openai==1.59.7

# Dashboard
gradio==5.9.1

# Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# Monitoring
prometheus-client>=0.20.0

# Testing
pytest==8.4.2
pytest-asyncio==1.3.0
pytest-cov==6.0.0

# Type Checking
mypy==1.13.0
```

### 6.3 Market Data Sources (Fallback Chain)

**File**: `/app/services/market_data.py`

```python
class DataSource(str, Enum):
    CACHE = "cache"              # 1st: Check Redis (instant)
    TWELVE_DATA = "twelvedata"   # 2nd: Primary (800/day)
    FINNHUB = "finnhub"          # 3rd: Fallback (60/day)
    ALPHA_VANTAGE = "alphavantage"  # 4th: Fallback (500/day)
    YAHOO = "yahoo"              # 5th: Last resort (unlimited)
```

**Fallback Logic**:
1. Try cache first (15 min TTL)
2. If cache miss, try TwelveData (if quota available)
3. If TwelveData fails, try Finnhub
4. If Finnhub fails, try Alpha Vantage
5. If all fail, try Yahoo Finance
6. Return best available data or error

---

## 7. CACHING STRATEGY

### 7.1 Cache Keys & TTL

```python
# Pattern Results (1 hour)
pattern:ticker=AAPL:interval=1day  (3600s)

# Market Data / OHLCV (15 minutes)
ohlcv:AAPL:1day                    (900s)

# Chart URLs (2 hours)
chart:AAPL:1D                       (7200s)

# API Usage Tracking (24 hours)
api_usage:twelvedata               (86400s)
api_usage:finnhub                  (86400s)
api_usage:alphavantage             (86400s)

# Universe Scan Results
top_setups:multi:min7.0            (3600s)
quick_scan_cache:nasdaq100         (600s)

# Chart-IMG Cache
chartimg:AAPL:1D:600x400           (900s)
```

### 7.2 Multi-Tier Cache

**File**: `/app/services/multi_tier_cache.py`

```
Tier 1: HOT (Redis)
├─ TTL: 5-15 minutes
├─ Use: Frequently accessed data
└─ Promotion threshold: 3 accesses

Tier 2: WARM (Database)
├─ TTL: 1 hour
├─ Use: Medium-frequency data
└─ After demotion from hot tier

Tier 3: COLD (CDN/Static)
├─ TTL: 24 hours
├─ Use: Stable/reference data
└─ Path: /tmp/legend-ai-cdn

Cache Warming:
├─ On startup, pre-populate hot tier
├─ S&P 500 top 50 stocks
└─ Reduces cold-start latency
```

---

## 8. INTEGRATION POINTS FOR TRADINGVIEW

### 8.1 Existing TradingView Integration

**File**: `/app/api/tv.py`

Current TradingView integration:
- Symbol Lab page (`/tv` and `/tv/{symbol}`)
- TradingView widget templates
- Chart display using TradingView widgets

### 8.2 Recommended TradingView Webhook Integration Points

Based on codebase architecture, here are the ideal integration points:

**1. Webhook Receiver** (New Endpoint)
```
POST /api/webhook/tradingview
{
  "ticker": "AAPL",
  "signal": "BUY" or "SELL",
  "price": 178.50,
  "timestamp": "2024-11-18T10:30:00Z",
  "alert_message": "Custom message from TradingView"
}
```

**2. Signal Processing**
- Route through existing pattern detector for validation
- Check alert configuration
- Log to AlertLog table
- Send via Telegram/Email if configured

**3. Trade Automation** (Optional)
- Create trade record if auto-trade enabled
- Send to watchlist if monitoring enabled
- Trigger additional analysis

### 8.3 Data Flow for TradingView Integration

```
TradingView Alert
       │
       ▼
/api/webhook/tradingview (NEW)
       │
       ├─ Parse webhook payload
       ├─ Validate signature (if enabled)
       │
       ▼
AlertService (existing)
       ├─ Check if ticker in watchlist
       ├─ Validate against min_confidence
       ├─ Apply rate limiting
       │
       ▼
Send Alerts (existing)
       ├─ Telegram
       ├─ Email
       └─ Database log
```

---

## 9. SCANNER & UNIVERSE INFRASTRUCTURE

### 9.1 Universe Definition

**File**: `/app/services/universe_data.py`

Supported universes:
- **S&P 500** - 500 largest US companies
- **NASDAQ 100** - 100 largest NASDAQ companies
- **Custom** - User-defined list

Universe data is:
- Fetched from external sources
- Cached in-memory (UniverseStore)
- Updated daily

### 9.2 Scanning Process

**File**: `/app/services/pattern_scanner.py`

```python
class PatternScannerService:
    
    async def scan_universe(
        universe: Optional[str] = None,  # sp500, nasdaq100, custom
        limit: int = 50,                  # Max results
        pattern_filter: Optional[List[str]] = None,  # VCP, Cup & Handle
        min_score: float = 7.0            # Min confidence
    ):
        """
        Scan entire universe for patterns
        """
        
        # 1. Get universe tickers
        tickers = get_universe_tickers(universe)
        
        # 2. Run parallel scans (max 8 concurrent)
        results = await asyncio.gather(
            *[scan_symbol(ticker) for ticker in tickers[:limit]],
            return_exceptions=True
        )
        
        # 3. Filter by pattern type & confidence
        filtered = [
            r for r in results 
            if r.score >= min_score
            and (not pattern_filter or r.pattern in pattern_filter)
        ]
        
        # 4. Sort by score
        sorted_results = sorted(filtered, key=lambda x: x.score, reverse=True)
        
        # 5. Return top results with metadata
        return {
            "success": True,
            "universe_size": len(tickers),
            "scanned": len(results),
            "results": sorted_results[:limit],
            "meta": {
                "duration_ms": time_elapsed,
                "total_hits": len(filtered),
                "build_sha": resolve_build_sha()
            }
        }
```

**Scan Concurrency**: Max 8 concurrent scans to avoid API rate limits

**Performance**: ~500 tickers in 2-5 minutes depending on data source availability

---

## 10. KEY SERVICE FLOWS

### 10.1 Pattern Detection Flow

```
GET /api/patterns/detect?ticker=NVDA
    │
    ├─ 1. Check Redis cache
    │   key: pattern:NVDA:1day
    │   │
    │   ├─ HIT: Return cached result
    │   │
    │   └─ MISS: Continue
    │
    ├─ 2. Fetch Market Data
    │   ├─ Check cache: ohlcv:NVDA:1day (900s)
    │   ├─ Try APIs: TwelveData → Finnhub → Alpha Vantage → Yahoo
    │   └─ Cache result for 15 minutes
    │
    ├─ 3. Run Detectors (Parallel)
    │   ├─ VCP Detector
    │   ├─ Cup & Handle Detector
    │   ├─ Triangle Detector
    │   └─ ... (8 total detectors)
    │
    ├─ 4. Select Best Pattern
    │   └─ Return highest scoring result
    │
    ├─ 5. Generate Chart (Optional)
    │   └─ Call Chart-IMG API with TradingView symbol
    │
    ├─ 6. Cache Pattern Result
    │   └─ Store for 1 hour
    │
    └─ 7. Return PatternResponse
```

### 10.2 Universe Scan Flow

```
POST /api/scan
    │
    ├─ Check feature flag: legend_flags_enable_scanner
    │   │
    │   └─ If disabled: Return empty results
    │
    ├─ Get universe tickers (SP500 or NASDAQ100)
    │
    ├─ Run VCP scan with concurrency control (max 8)
    │   ├─ Fetch price data for each ticker
    │   ├─ Run VCP detector
    │   ├─ Calculate RS rating vs SPY
    │   └─ Return patterns with score >= min_score
    │
    ├─ Filter by min_score (default 7.0)
    │
    ├─ Sort by score descending
    │
    ├─ Cache results for 10 minutes
    │   key: quick_scan_cache:{universe}
    │
    └─ Return ScanResponse
```

### 10.3 Alert Monitoring Flow

```
POST /api/alerts/monitor
    │
    ├─ Get watchlist from database
    │
    ├─ For each ticker:
    │   ├─ Fetch 500-bar daily data
    │   ├─ Run pattern detectors
    │   ├─ Check confidence >= 0.75
    │   ├─ Check 6-hour cooldown
    │   │
    │   └─ If all pass:
    │       ├─ Format alert message
    │       ├─ Send to Telegram
    │       ├─ Send to Email
    │       └─ Log to database
    │
    └─ Return monitoring result
```

---

## 11. DEPLOYMENT & ENVIRONMENT

### 11.1 Docker Deployment

**Dockerfile**:
- Base: `python:3.11-slim`
- Exposes: Port 8000
- Health check: `/health` endpoint
- Environment: Auto-detects Railway domain

**docker-compose.yml**:
```yaml
services:
  app:
    build: .
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgresql://...
      - REDIS_URL=redis://redis:6379
  postgres:
    image: postgres:15
  redis:
    image: redis:7
```

### 11.2 Railway Deployment

Auto-configured with:
- PostgreSQL database
- Redis cache
- Public domain (RAILWAY_PUBLIC_DOMAIN env var)
- Auto CORS configuration
- Auto webhook URL generation

---

## 12. MONITORING & OBSERVABILITY

### 12.1 Prometheus Metrics

**File**: `/app/telemetry/metrics.py`

Key metrics:
- `scan_request_duration_seconds` - Scan latency
- `scan_errors_total` - Failed scans
- `pattern_detection_duration_seconds` - Detection latency
- `cache_hits_total` - Cache performance
- `api_requests_total` - Request count

Metrics endpoint: `GET /api/metrics`

### 12.2 Structured Logging

**File**: `/app/middleware/structured_logging.py`

Logs include:
- Request metadata (path, method, status)
- Processing time
- Cache hit/miss
- API source used
- Errors with stack traces

### 12.3 Rate Limiting

**File**: `/app/middleware/rate_limit.py`

- 60 requests/minute per IP (configurable)
- Redis-based tracking
- Returns 429 when exceeded

---

## 13. SUMMARY TABLE: COMPONENTS & RESPONSIBILITIES

| Component | File | Purpose | Key Methods |
|-----------|------|---------|-------------|
| **Telegram Webhook** | `/app/api/telegram.py` | Handle Telegram messages | `telegram_webhook()` |
| **Pattern Detector** | `/app/core/pattern_detector.py` | Detect patterns | `analyze_ticker()` |
| **Pattern Scanner** | `/app/services/pattern_scanner.py` | Scan universes | `scan_symbol()`, `scan_universe()` |
| **Market Data** | `/app/services/market_data.py` | Multi-source data | `get_time_series()` |
| **Alert Service** | `/app/services/alerts.py` | Monitor & alert | `monitor_watchlist()` |
| **Risk Calculator** | `/app/services/risk_calculator.py` | Position sizing | `calculate_position_size()` |
| **Cache Service** | `/app/services/cache.py` | Redis caching | `get()`, `set()` |
| **Database Service** | `/app/services/database.py` | SQLAlchemy ORM | CRUD operations |
| **Detector Registry** | `/app/core/detector_registry.py` | Detector lookup | `get_all_detectors()` |

---

## CONCLUSION

The Legend AI codebase is a **well-architected, production-ready trading platform** with:

✅ **Modular design** - Easy to extend with new patterns/integrations
✅ **Multi-source data** - Fallback chain prevents failures  
✅ **Smart caching** - Redis + multi-tier strategy minimizes API calls
✅ **Real-time alerts** - Telegram + Email + Database logging
✅ **Professional tools** - Risk management, multi-timeframe analysis, trading plans
✅ **Webhook ready** - Telegram webhook handler + extensible architecture
✅ **Documented APIs** - 50+ endpoints with detailed OpenAPI specs

**For TradingView Integration**, the system is ready to accept webhooks at a new `/api/webhook/tradingview` endpoint, process signals through existing pattern detectors, and route to alert channels. The foundational work is complete; integration would be straightforward.

