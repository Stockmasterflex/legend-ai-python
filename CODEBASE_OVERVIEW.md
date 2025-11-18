# Legend AI Trading Pattern Scanner - Codebase Architecture Overview

## Project Summary

**Legend AI** is a FastAPI-based trading pattern scanner and AI-powered financial assistant. It provides:
- Real-time pattern detection (VCP, Cup & Handle, Triangles, etc.)
- AI-powered stock analysis via Claude/GPT-4
- Multi-source market data integration (TwelveData, Finnhub, Alpha Vantage, Yahoo)
- Telegram bot integration with webhook support
- Intelligent caching (Redis multi-tier)
- Database persistence (PostgreSQL/SQLite)

---

## 1. Project Structure & Organization

```
legend-ai-python/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management (Pydantic Settings)
│   ├── models.py               # SQLAlchemy database models
│   ├── lifecycle.py            # Startup/shutdown events
│   │
│   ├── ai/
│   │   └── assistant.py        # AIFinancialAssistant (GPT-4/Claude via OpenRouter)
│   │
│   ├── api/                    # API endpoint routers (25+ endpoints)
│   │   ├── patterns.py         # Pattern detection endpoint
│   │   ├── analyze.py          # Multi-ticker analysis
│   │   ├── charts.py           # Chart generation
│   │   ├── market.py           # Market data queries
│   │   ├── scan.py             # Universe scanning
│   │   ├── alerts.py           # Alert management
│   │   ├── trades.py           # Trade tracking
│   │   ├── telegram.py         # Telegram webhook handler
│   │   ├── telegram_enhanced.py # Enhanced Telegram features
│   │   └── ... (15 more endpoints)
│   │
│   ├── routers/
│   │   ├── ai_chat.py          # AI chat endpoints (/api/ai/*)
│   │   └── advanced_analysis.py # Advanced analysis endpoints
│   │
│   ├── services/               # Business logic layer
│   │   ├── market_data.py      # Multi-source data fetching with fallback
│   │   ├── database.py         # SQLAlchemy database service
│   │   ├── cache.py            # Redis caching service
│   │   ├── cache_warmer.py     # Pre-warming cache on startup
│   │   ├── multi_tier_cache.py # Hot/warm tier caching strategy
│   │   ├── charting.py         # Chart generation service
│   │   ├── scanner.py          # Pattern scanner service
│   │   ├── universe.py         # Symbol universe management
│   │   ├── pattern_scanner.py  # Pattern detection orchestration
│   │   ├── trades.py           # Trade management
│   │   ├── alerts.py           # Alert system
│   │   ├── risk_calculator.py  # Risk metrics
│   │   └── ... (more services)
│   │
│   ├── core/                   # Core pattern detection logic
│   │   ├── detector_base.py    # Base Detector interface & PatternResult
│   │   ├── detector_registry.py # Detector registry (8 detector types)
│   │   ├── pattern_detector.py # Main pattern detector orchestrator
│   │   ├── indicators.py       # Technical indicators
│   │   ├── detectors/          # Specific detector implementations
│   │   │   ├── vcp_detector.py
│   │   │   ├── cup_handle_detector.py
│   │   │   ├── triangle_detector.py
│   │   │   ├── wedge_detector.py
│   │   │   ├── head_shoulders_detector.py
│   │   │   ├── double_top_bottom_detector.py
│   │   │   ├── channel_detector.py
│   │   │   └── sma50_pullback_detector.py
│   │   └── detector_config.py  # Detector configurations
│   │
│   ├── technicals/             # Technical analysis tools
│   │   ├── trendlines.py       # Trendline detection
│   │   └── fibonacci.py        # Fibonacci retracements
│   │
│   ├── telemetry/
│   │   ├── metrics.py          # Prometheus metrics
│   │   ├── monitoring.py       # System monitoring
│   │   └── alerter.py          # Alert management
│   │
│   ├── middleware/             # HTTP middleware
│   │   ├── metrics_middleware.py # Request/response metrics
│   │   ├── rate_limit.py       # Rate limiting
│   │   └── structured_logging.py # Request logging
│   │
│   ├── infra/                  # Infrastructure integrations
│   │   ├── chartimg.py         # Chart-img.com API
│   │   └── symbols.py          # Symbol utilities
│   │
│   └── utils/
│       └── build_info.py       # Build/version info
│
├── data/
│   └── universe_seed.json      # Initial symbol universe (SP500, NASDAQ100)
│
├── ops/
│   ├── prometheus/             # Prometheus configuration
│   ├── grafana/                # Grafana dashboard config
│   └── monitoring/             # Monitoring setup
│
├── requirements.txt            # Python dependencies
├── .env.example                # Configuration template
├── config.py                   # Settings object
└── main.py                     # Entry point
```

### Directory Organization Patterns

1. **API Endpoints** (`/app/api/`) - 25+ routers handling HTTP requests
2. **Services** (`/app/services/`) - Reusable business logic (singletons/DI)
3. **Core Logic** (`/app/core/`) - Core pattern detection algorithms
4. **Models** (`/app/models.py`) - SQLAlchemy ORM models
5. **Configuration** - Environment-driven via Pydantic Settings

---

## 2. Existing API Integrations

### Market Data Service (Multi-Source Fallback)

**File:** `/app/services/market_data.py`

Uses intelligent fallback strategy:
1. **Redis Cache** (instant, 0 API calls)
2. **TwelveData** (primary, 800 calls/day free)
3. **Finnhub** (fallback 1, 60 calls/day free)
4. **Alpha Vantage** (fallback 2, 500 calls/day free)
5. **Yahoo Finance** (unlimited, no API key needed)

```python
# Usage example:
market_data = MarketDataService()
data = await market_data.get_time_series(
    ticker="AAPL",
    interval="1day",
    outputsize=500
)
# Returns: {"c": [...], "o": [...], "h": [...], "l": [...], "v": [...], "t": [...]}
```

### AI Service (OpenRouter + OpenAI)

**File:** `/app/ai/assistant.py`

Supports multiple LLM providers:
- **OpenRouter** (recommended, 3-10x cheaper)
  - Claude 3.5 Sonnet (~$3/1M tokens) - default
  - Gemini Pro (~$1.25/1M tokens)
  - GPT-4 Turbo (~$10/1M tokens)
- **Direct OpenAI** (fallback)

```python
assistant = AIFinancialAssistant()
response = await assistant.chat(
    user_message="What patterns does AAPL show?",
    symbol="AAPL",
    include_market_data=True
)
```

### Chart Generation

**File:** `/app/services/charting.py` and `/app/infra/chartimg.py`

Uses Chart-img.com API for professional OHLC charts.

### Telegram Bot Integration

**File:** `/app/api/telegram_enhanced.py`

Webhook-based integration with auto-configuration from Railway environment.

---

## 3. Data Models & Database Setup

### SQLAlchemy ORM Models

**File:** `/app/models.py`

#### Core Tables:

```python
# Ticker tracking
class Ticker(Base):
    symbol: str (unique, indexed)
    name: str
    sector: str
    industry: str
    exchange: str
    created_at, updated_at

# Pattern scan results
class PatternScan(Base):
    ticker_id: ForeignKey
    pattern_type: str
    score: float
    entry_price, stop_price, target_price: float
    risk_reward_ratio: float
    criteria_met: JSON string
    chart_url: str
    scanned_at: DateTime (indexed)

# User watchlists
class Watchlist(Base):
    user_id: str (indexed)
    ticker_id: ForeignKey
    status: str (Watching, Breaking Out, Triggered, etc)
    target_entry, target_stop, target_price: float
    alerts_enabled: bool
    added_at, triggered_at: DateTime

# Scanning history
class ScanLog(Base):
    scan_type: str (daily, weekly, custom)
    tickers_scanned: int
    patterns_found: int
    duration_seconds: float
    status: str
    error_message: str

# Universe results
class UniverseScan(Base):
    scan_date: DateTime (indexed)
    universe: str (SP500, NASDAQ100, CUSTOM)
    total_scanned: int
    patterns_found: int
    top_score: float
    status: str

# Alert history
class AlertLog(Base):
    ticker_id: ForeignKey
    alert_type: str (price, pattern, breakout, volume)
    trigger_price, trigger_value: float
    alert_sent_at: DateTime (indexed)
    sent_via: str (telegram, email, push)
    status: str (sent, failed, acknowledged)
```

### Database Service

**File:** `/app/services/database.py`

```python
db_service = get_database_service()

# Operations
ticker = db_service.get_or_create_ticker("AAPL")
db_service.save_pattern_scan(ticker_symbol, pattern_data)
db_service.save_pattern_scans_batch(scans_list)  # Optimized bulk insert
db_service.get_recent_scans(limit=50, pattern_type="VCP", min_score=0.7)
db_service.add_to_watchlist(user_id, ticker_symbol, notes)
db_service.get_watchlist(user_id)
db_service.log_scan(scan_type, tickers_scanned, patterns_found)
```

### Connection Configuration

- **Development:** SQLite with StaticPool
- **Production:** PostgreSQL with QueuePool
- Connection pooling optimized for Railway (5 connections, 30s timeout)
- Query timeout: 30 seconds

---

## 4. Existing AI/LLM Integrations

### AIFinancialAssistant Class

**File:** `/app/ai/assistant.py`

Core capabilities:

1. **Conversational Chat**
   ```python
   response = await assistant.chat(
       user_message="What are the best tech stocks?",
       symbol=None,
       include_market_data=True
   )
   ```

2. **Stock Analysis**
   ```python
   analysis = await assistant.analyze_stock("AAPL")
   # Returns: structured analysis with technical setup, key levels, patterns, risks
   ```

3. **Stock Comparison**
   ```python
   comparison = await assistant.compare_stocks(["AAPL", "MSFT", "GOOGL"])
   # Compares for day/swing/long-term trading
   ```

4. **Pattern Education**
   ```python
   explanation = await assistant.explain_pattern("Cup and Handle")
   ```

### RAG (Retrieval Augmented Generation)

Market context built from:
- Current price & change
- Moving averages (20/50/200 SMA)
- Technical indicators (RSI)
- Detected patterns (top 5)
- Support/resistance trendlines
- Fibonacci retracements
- Volume analysis
- Volatility (20-day annualized)

System prompt emphasizes:
- Technical & fundamental analysis
- Risk warnings & disclaimers
- Educational (not financial advice)
- Data-driven responses

### API Endpoints

**File:** `/app/routers/ai_chat.py`

```
POST /api/ai/chat          - Conversational chat
POST /api/ai/analyze       - Comprehensive stock analysis
POST /api/ai/compare       - Multi-stock comparison
POST /api/ai/explain-pattern - Pattern explanation
POST /api/ai/clear-history - Clear conversation history
GET  /api/ai/status        - Check AI availability
```

---

## 5. Configuration Management

### Settings Architecture

**File:** `/app/config.py`

Uses **Pydantic v2 BaseSettings** with:
- Environment file loading (`.env`)
- Automatic type validation
- Default values with production overrides

```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )
```

### Configuration Categories

#### Core Application
```python
app_name: str = "Legend AI"
debug: bool = False
secret_key: str = "dev-secret-key-change-in-production"
cors_origins: str = "*"  # Auto-detects Railway domain in production
```

#### AI Services
```python
openrouter_api_key: Optional[str]  # Recommended (cheaper)
openai_api_key: Optional[str]      # Fallback
ai_model: str = "anthropic/claude-3.5-sonnet"
ai_temperature: float = 0.7
```

#### Market Data APIs
```python
twelvedata_api_key: Optional[str]
finnhub_api_key: Optional[str]
alpha_vantage_api_key: Optional[str]
data_source_priority: str = "twelvedata,finnhub,alphavantage"

# Daily limits
twelvedata_daily_limit: int = 800
finnhub_daily_limit: int = 60
alpha_vantage_daily_limit: int = 500
```

#### Chart Generation
```python
chart_img_api_key: Optional[str]  # Chart-img.com PRO
chartimg_daily_limit: int = 500
```

#### Caching Strategy
```python
cache_ttl_patterns: int = 3600      # 1 hour
cache_ttl_market_data: int = 900    # 15 minutes
cache_ttl_charts: int = 7200        # 2 hours
cache_ttl_ai_responses: int = 1800  # 30 minutes
```

#### Multi-Tier Cache Settings
```python
cache_hot_ttl_min: int = 300        # 5 minutes (Redis hot tier)
cache_hot_ttl_max: int = 900        # 15 minutes
cache_warm_ttl: int = 3600          # 1 hour (Database warm tier)
cache_cdn_ttl: int = 86400          # 24 hours (CDN/static)
cache_promotion_threshold: int = 3  # Access count to promote
cache_hot_max_size: int = 10000     # Max keys in hot tier
cache_enable_warming: bool = True   # Pre-warm on startup
```

#### Rate Limiting
```python
rate_limit_per_minute: int = 60
ai_rate_limit_per_minute: int = 20
market_data_rate_limit: int = 30
```

#### Database & Redis
```python
database_url: Optional[str]         # PostgreSQL or SQLite
redis_url: str = "redis://localhost:6379"
```

#### Telegram Integration
```python
telegram_bot_token: str = "dev-token"
telegram_chat_id: Optional[str]
telegram_webhook_url: Optional[str]  # Auto-detected from Railway
```

### Auto-Detection Features

Railway environment variable detection:
```python
@property
def allowed_origins(self) -> list[str]:
    """Auto-detects Railway domain, restricts CORS in production"""
    railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    if railway_domain:
        return [f"https://{railway_domain}", f"http://{railway_domain}"]
    return ["*"]  # Development fallback

@property
def auto_webhook_url(self) -> str:
    """Auto-generates Telegram webhook from Railway domain"""
    railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    if railway_domain:
        return f"https://{railway_domain}"
    return "http://localhost:8000"
```

---

## 6. Main Entry Points & Services

### FastAPI Application Entry Point

**File:** `/app/main.py`

#### Core Setup
```python
app = FastAPI(
    title="Legend AI - Trading Pattern Scanner",
    docs_url="/docs",           # Swagger UI
    redoc_url="/redoc",         # ReDoc
    openapi_url="/openapi.json"
)

# Middleware stack (top-down):
1. MetricsMiddleware          # Prometheus metrics collection
2. StructuredLoggingMiddleware # Request/response logging
3. RateLimitMiddleware         # Rate limiting (60 req/min)
4. CORSMiddleware              # Cross-origin requests
```

#### Routes Registered (25+ routers)
```python
/api/patterns          - Pattern detection
/api/analyze           - Multi-ticker analysis
/api/charts            - Chart generation
/api/market            - Market data queries
/api/scan              - Universe scanning
/api/alerts            - Alert management
/api/trades            - Trade tracking
/api/watchlist         - Watchlist management
/api/universe          - Universe management
/api/risk              - Risk calculations
/api/analytics         - Analytics
/api/ai/chat           - AI chat
/api/ai/analyze        - AI stock analysis
/api/telegram          - Telegram webhooks
/api/metrics           - Prometheus metrics
/api/cache-mgmt        - Cache management
/api/api-usage         - API usage stats
/dashboard             - Dashboard
/health                - Health check
/docs                  - API documentation
```

#### Health Checks
```python
GET /healthz           - Simple K8s health check
GET /health            - Detailed health status
GET /health/detailed   - Full diagnostics
```

### Lifecycle Management

**File:** `/app/lifecycle.py`

#### Startup Events
1. Universe seeding (load S&P 500, NASDAQ 100)
2. Telegram webhook configuration
3. Multi-tier cache warming
4. Monitoring service startup
5. Alerting service startup

#### Shutdown Events
1. Monitoring service stop
2. Alerting service stop
3. Clean resource cleanup

### Service Initialization

**Singleton Services:**
```python
from app.services.market_data import market_data_service
from app.services.cache import get_cache_service
from app.services.database import get_database_service
from app.routers.ai_chat import get_ai_assistant

# All initialized lazily on first access
market_data = market_data_service
cache = await get_cache_service()
db = get_database_service()
ai = get_ai_assistant()
```

### Pattern Detection Service

**File:** `/app/services/pattern_scanner.py`

```python
scanner = PatternScanner()
results = await scanner.scan_ticker("AAPL", interval="1day")
batch_results = await scanner.scan_universe(
    symbols=["AAPL", "MSFT", "GOOGL"],
    min_score=0.7
)
```

### Core Pattern Detectors

**File:** `/app/core/detector_registry.py`

8 registered detector types:
1. VCP (Volatility Contraction Pattern)
2. Cup & Handle
3. Triangles (Ascending/Descending/Symmetrical)
4. Wedges (Rising/Falling)
5. Head & Shoulders (Normal & Inverse)
6. Double Top/Bottom
7. Channels (Up/Down/Sideways)
8. SMA 50 Pullback

```python
from app.core.detector_registry import get_detector_registry

registry = get_detector_registry()
detector = registry.get_detector("vcp")  # Get specific detector
all_detectors = registry.get_all_detectors()  # Get all
```

---

## 7. Key Dependencies

### Core Framework
- **FastAPI** 0.115.6 - Web framework
- **Uvicorn** 0.32.1 - ASGI server
- **Pydantic** 2.10.6 - Data validation

### Database & Caching
- **SQLAlchemy** 2.0.36 - ORM
- **psycopg2** 2.9.10 - PostgreSQL driver
- **Redis** 5.2.1 - Async Redis client
- **Alembic** 1.14.0 - Database migrations

### Data Processing
- **Pandas** 2.2.3 - DataFrames
- **NumPy** 1.26.4 - Numerical computing
- **SciPy** 1.14.1 - Scientific computing

### AI/LLM
- **OpenAI** 1.59.7 - GPT-4/Claude client (OpenRouter + direct)

### Integration
- **python-telegram-bot** 21.9 - Telegram bot
- **httpx** 0.28.1 - Async HTTP client

### Monitoring
- **prometheus-client** 0.20.0 - Metrics collection

### Testing
- **pytest** 8.4.2
- **pytest-asyncio** 1.3.0
- **mypy** 1.13.0

---

## 8. Caching Architecture

### Multi-Tier Cache Strategy

```
┌─────────────────────────────────────────┐
│ Request Comes In                        │
└──────────────┬──────────────────────────┘
               │
        ┌──────▼──────────┐
        │ Redis Hot Tier  │ (5-15 min TTL)
        │ In-memory, fast │
        │ 10k max keys    │
        └──────┬──────────┘
               │ Miss?
        ┌──────▼────────────────┐
        │ Database Warm Tier    │ (1 hour TTL)
        │ Persistent cache      │
        │ Promoted after 3 hits │
        └──────┬────────────────┘
               │ Miss?
        ┌──────▼────────────────┐
        │ Fetch from API        │
        │ TwelveData, Finnhub   │
        │ Alpha Vantage, Yahoo  │
        └──────┬────────────────┘
               │
        ┌──────▼────────────────┐
        │ Cache Result          │
        │ Store in both tiers   │
        └──────────────────────┘
```

### Cache Keys (Consistent Format)

```
pattern:ticker=AAPL:interval=1day
timeseries:AAPL:1day
ohlcv:TSLA:1d:5y
chart:AAPL:1day
ai_response:MSFT:<hash>
```

### Cache Service Usage

**File:** `/app/services/cache.py`

```python
cache = get_cache_service()

# Generic operations
await cache.set(key, value, ttl=3600)
value = await cache.get(key)

# Pattern cache
await cache.set_pattern(ticker, interval, result)
result = await cache.get_pattern(ticker, interval)

# Batch operations
results = await cache.get_batch(keys)
await cache.set_batch(items, ttl=3600)
```

---

## 9. Request/Response Flow Example

### Pattern Detection Endpoint

```
1. HTTP POST /api/patterns/detect
   Request: { "ticker": "AAPL", "interval": "1day" }

2. API Router (patterns.py)
   ├─ Validate ticker format
   └─ Call scanner service

3. Pattern Scanner Service
   ├─ Check cache (Redis)
   │  └─ Cache hit? Return immediately
   └─ Fetch market data
      ├─ Check cache (Redis)
      ├─ Call MarketDataService
      │  ├─ TwelveData (primary)
      │  ├─ Finnhub (fallback)
      │  ├─ Alpha Vantage (fallback)
      │  └─ Yahoo Finance (fallback)
      └─ Parse OHLCV data

4. Pattern Detection (DetectorRegistry)
   ├─ Run VCP Detector
   ├─ Run Cup & Handle Detector
   ├─ Run Triangle Detector
   ├─ ... (8 detectors total)
   └─ Collect results

5. Technical Analysis Tools
   ├─ Calculate indicators
   ├─ Detect trendlines
   ├─ Calculate Fibonacci levels
   └─ Identify support/resistance

6. Chart Generation (Chart-img.com)
   └─ Generate professional OHLC chart

7. Database Storage
   └─ Save to PatternScan table (optional)

8. Cache Results
   ├─ Store in Redis (hot tier)
   └─ Store in database (warm tier)

9. Return Response
   Response: {
     "success": true,
     "data": {
       "ticker": "AAPL",
       "patterns": [...],
       "chart_url": "...",
       "timestamp": "..."
     },
     "cached": false,
     "api_used": "twelvedata",
     "processing_time": 1.23
   }
```

---

## 10. Integration Points for AI Market Analysis

### Recommended Extension Points

1. **New Analysis Service** (`/app/services/market_analysis.py`)
   - Build on existing `MarketDataService`
   - Use detector registry for pattern detection
   - Integrate with AIFinancialAssistant

2. **New API Router** (`/app/api/market_analysis.py`)
   - POST /api/analysis/market-overview
   - POST /api/analysis/sector-analysis
   - POST /api/analysis/watch-list-summary
   - GET /api/analysis/trend-report

3. **New Database Model** (`/app/models.py`)
   - Add `MarketAnalysisReport` table
   - Add `SectorAnalysis` table
   - Add `TrendReport` table

4. **Cache Keys for Analysis**
   - market_analysis:sector=tech:date=2024-01-15
   - trend_report:universe=sp500:period=1mo
   - watch_list_summary:user_id=123:date=2024-01-15

5. **Leverage Existing Infrastructure**
   - AI context building (_build_market_context) already gathers comprehensive data
   - Detector registry already identifies patterns
   - Market data service already handles multi-source fallback
   - Caching strategy already optimized
   - Database models already in place

### Example: Adding Market Analysis Endpoint

```python
# 1. Service layer: /app/services/market_analysis.py
class MarketAnalysisService:
    def __init__(self):
        self.market_data = MarketDataService()
        self.ai = AIFinancialAssistant()
        self.db = get_database_service()
        self.cache = get_cache_service()
    
    async def analyze_market_overview(self, universe: str = "SP500"):
        # Fetch symbols from universe
        # Analyze each with AI
        # Aggregate results
        # Cache for 24 hours
        # Return comprehensive overview

# 2. API Router: /app/api/market_analysis.py
@router.post("/market-overview")
async def analyze_market_overview(request: MarketOverviewRequest):
    service = MarketAnalysisService()
    analysis = await service.analyze_market_overview(
        universe=request.universe
    )
    return analysis

# 3. Add to main.py routers
from app.api.market_analysis import router as analysis_router
app.include_router(analysis_router)
```

---

## 11. Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Web** | FastAPI + Uvicorn | REST API framework |
| **Async** | asyncio | Async/concurrent operations |
| **Validation** | Pydantic v2 | Data validation & settings |
| **Database** | SQLAlchemy + PostgreSQL | Persistence & ORM |
| **Caching** | Redis | High-speed caching |
| **Data Processing** | Pandas, NumPy, SciPy | Analysis & calculations |
| **AI/LLM** | OpenAI client (OpenRouter) | Claude 3.5 Sonnet, GPT-4 |
| **Charting** | Chart-img.com API | Professional OHLC charts |
| **Bot** | python-telegram-bot | Telegram integration |
| **HTTP** | httpx | Async HTTP requests |
| **Monitoring** | Prometheus | Metrics collection |
| **Testing** | pytest, mypy | Testing & type checking |
| **Deployment** | Railway | Cloud hosting |

---

## 12. Architecture Principles

1. **Layered Architecture**
   - API routers → Services → Core logic
   - Clear separation of concerns

2. **Singleton Pattern**
   - Shared service instances (market data, cache, DB)
   - Initialized once, reused globally

3. **Dependency Injection**
   - Services injected where needed
   - Easy to test and mock

4. **Caching Strategy**
   - Multi-tier (hot/warm/cold)
   - Automatic invalidation (TTL-based)

5. **Fault Tolerance**
   - Multi-source fallback (4 market data sources)
   - Graceful degradation (warnings instead of failures)
   - Non-blocking startup (cache warming optional)

6. **Configuration Management**
   - Environment-driven
   - Auto-detection (Railway, webhook URLs)
   - Feature flags support

7. **Monitoring & Observability**
   - Prometheus metrics
   - Structured logging
   - Health check endpoints

---

## Conclusion

The Legend AI codebase is well-architected for adding new AI-powered analysis features. The existing infrastructure provides:

- Robust market data fetching with intelligent fallback
- AI integration pattern established and tested
- Database and caching layers ready for new data
- Extensible detector registry for pattern analysis
- Clean API endpoint structure for new features

You can leverage the existing `AIFinancialAssistant`, `MarketDataService`, and detector infrastructure to build your market analysis system while following the established patterns and conventions.

