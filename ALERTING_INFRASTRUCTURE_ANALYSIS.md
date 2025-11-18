# Legend AI - Comprehensive Codebase Exploration Report

## Executive Summary

**Legend AI** is a professional trading pattern scanner built with **FastAPI (Python 3.11)** that analyzes stock charts for high-probability trading patterns (VCP, Cup & Handle, Breakouts). The system spans:
- **~12,000 lines** of backend Python code
- **15+ API routers** with 50+ REST endpoints
- **3 integration layers**: Market Data, Caching, Database
- **Multiple external service integrations**: Telegram, TwelveData, Chart-IMG, OpenRouter AI

---

## 1. PROJECT STRUCTURE & ARCHITECTURE

### High-Level Architecture

```
FastAPI Application (app/main.py)
├── API Layer (15 routers, 50+ endpoints)
├── Service Layer (Business logic)
├── Core Layer (Pattern detection, indicators)
├── Infrastructure (Cache, Database, External APIs)
└── Middleware (Rate limiting, Structured logging, Metrics)
```

### Directory Organization

```
legend-ai-python/
├── app/
│   ├── main.py                    # FastAPI app setup, middleware, router registration
│   ├── config.py                  # Pydantic settings (env vars)
│   ├── models.py                  # SQLAlchemy database models (Ticker, PatternScan, Watchlist, AlertLog)
│   ├── lifecycle.py               # Startup/shutdown events (Telegram webhook setup)
│   │
│   ├── api/                       # API Routers (REST endpoints)
│   │   ├── patterns.py            # POST /api/patterns/detect → Pattern detection
│   │   ├── scan.py                # GET /api/scan/* → Universe scanning
│   │   ├── charts.py              # POST /api/charts/generate → Chart generation
│   │   ├── watchlist.py           # /api/watchlist/* → Watchlist CRUD
│   │   ├── alerts.py              # /api/alerts/* → Alert management (EXISTS)
│   │   ├── trades.py              # /api/trades/* → Trade tracking
│   │   ├── telegram_enhanced.py   # /api/webhook/telegram → Telegram bot
│   │   ├── market.py              # /api/market/* → Market metrics
│   │   ├── analyze.py             # /api/analyze/* → Single-ticker analysis
│   │   ├── universe.py            # /api/universe/* → Universe management
│   │   ├── risk.py                # /api/risk/* → Risk calculator
│   │   ├── multitimeframe.py      # /api/multitimeframe/* → Multi-TF analysis
│   │   ├── analytics.py           # /api/analytics/* → Analytics
│   │   ├── dashboard.py           # /api/dashboard/* → Dashboard backend
│   │   └── ... (9 other routers)
│   │
│   ├── services/                  # Business logic layer
│   │   ├── alerts.py              # AlertService - Pattern monitoring + Telegram/Email alerts
│   │   ├── market_data.py         # MarketDataService - Multi-source data fetching
│   │   ├── cache.py               # CacheService - Redis operations
│   │   ├── database.py            # DatabaseService - SQLAlchemy operations
│   │   ├── charting.py            # ChartingService - Chart-IMG integration
│   │   ├── scanner.py             # ScannerService - Universe scanning
│   │   ├── trades.py              # TradeService - Trade tracking
│   │   ├── risk_calculator.py     # RiskCalculatorService - Position sizing
│   │   ├── universe.py            # UniverseService - Universe management
│   │   └── ... (8 other services)
│   │
│   ├── core/                      # Core algorithms & detectors
│   │   ├── pattern_detector.py    # PatternDetector - VCP, Cup & Handle detection
│   │   ├── pattern_detector_v2.py # Enhanced pattern detection
│   │   ├── indicators.py          # SMA, EMA, RSI, Bollinger Bands, MACD
│   │   ├── classifiers.py         # Trend classification (Minervini, Weinstein)
│   │   ├── metrics.py             # Technical metrics (ATR, support/resistance)
│   │   ├── detectors/
│   │   │   ├── vcp_detector.py
│   │   │   ├── cup_handle_detector.py
│   │   │   ├── channel_detector.py
│   │   │   └── ... (7 other detectors)
│   │   └── chart_generator.py     # Chart rendering
│   │
│   ├── middleware/                # HTTP middleware
│   │   ├── structured_logging.py  # Logging middleware
│   │   ├── rate_limit.py          # Rate limiting (60 req/min)
│   │   └── metrics_middleware.py  # Prometheus metrics collection
│   │
│   ├── telemetry/                 # Monitoring & alerting
│   │   ├── alerter.py             # MonitoringAlerter - Threshold-based alerts
│   │   ├── monitoring.py          # MonitoringService - Metrics collection
│   │   └── metrics.py             # Prometheus metric definitions
│   │
│   ├── routers/                   # Additional routers
│   │   ├── ai_chat.py             # AI chat endpoint
│   │   └── advanced_analysis.py   # Advanced analysis endpoints
│   │
│   └── utils/, technicals/, infra/, ai/
│
├── tests/                         # Test suite
├── alembic/                       # Database migrations
├── requirements.txt               # Python dependencies
└── .env.example                   # Environment variables template
```

---

## 2. EXISTING ALERT/NOTIFICATION SYSTEMS

### Current Alert Infrastructure (Foundation Already Exists!)

#### **Service Layer: `app/services/alerts.py`**
**Status**: ✅ PARTIALLY IMPLEMENTED

```python
class AlertService:
    - Monitors watchlist for pattern formations
    - Sends alerts via Telegram + Email (SendGrid)
    - Pattern confidence threshold-based triggering (default 0.75)
    - Cooldown mechanism: 6-hour cooldown between same-ticker alerts
    - Methods:
        * monitor_watchlist()      # Main monitoring loop
        * _send_alerts()           # Routes to all channels
        * _send_telegram_alert()   # Telegram via Telegram Bot API
        * _send_email_alert()      # Email via SendGrid API
```

**Capabilities**:
- ✅ Telegram message formatting with inline keyboards
- ✅ Email HTML formatting with styled alert cards
- ✅ Pattern extraction (ticker, type, confidence, entry, stop, target, R:R)
- ✅ User alert tracking to prevent spam
- ❌ Database persistence (doesn't log to DB)
- ❌ Alert routing/rules engine
- ❌ Webhook/custom integrations
- ❌ Alert scheduling or time-based triggers

#### **API Layer: `app/api/alerts.py`**
**Status**: ✅ BASIC ENDPOINTS IMPLEMENTED

```
POST /api/alerts/monitor           # Start watching watchlist
POST /api/alerts/check-now         # Manual trigger
GET /api/alerts/recent             # View recent alerts
GET /api/alerts/config             # Get alert config
POST /api/alerts/test              # Send test alert
```

**Limitations**:
- No persistent alert history (returns empty list)
- No configurable thresholds
- No alert frequency rules
- Background tasks don't persist results

#### **Database Model: `app/models.py`**
**Status**: ✅ SCHEMA EXISTS (BUT UNUSED)

```python
class AlertLog(Base):
    __tablename__ = "alert_logs"
    
    id = Column(Integer, primary_key=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True)
    alert_type = Column(String(50), index=True)        # "price", "pattern", "breakout", "volume"
    trigger_price = Column(Float, nullable=True)
    trigger_value = Column(Float, nullable=True)
    alert_sent_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    sent_via = Column(String(50))                      # "telegram", "email", "push"
    user_id = Column(String(100), nullable=True, index=True)
    status = Column(String(20), default="sent")        # "sent", "failed", "acknowledged"
```

**Status**: Defined but **NEVER WRITTEN TO** - alerts not being logged to database

#### **Telemetry Layer: `app/telemetry/alerter.py`**
**Status**: ✅ MONITORING ALERTER EXISTS

```python
class MonitoringAlerter:
    - Monitors system metrics (error rates, response times, DB connections)
    - Sends Telegram alerts on threshold breach
    - Alert thresholds configured:
        * 10+ 5xx errors/minute
        * 50+ 4xx errors/minute
        * 95th percentile response time > 5s
        * 80% DB pool utilization
    - 5-minute cooldown between alerts of same type
```

**Purpose**: Infrastructure/operational alerting, not trading alerts

---

## 3. DATABASE MODELS & STRUCTURE

### Data Model Relationships

```
┌──────────────────┐
│    Ticker        │ (id, symbol, name, sector, industry, exchange)
└────────┬─────────┘
         │ 1:N
         ├─→ PatternScan    (pattern_type, score, entry, stop, target)
         ├─→ Watchlist      (status, target_entry, alerts_enabled)
         ├─→ AlertLog       (alert_type, sent_via, status)
         └─→ ScanLog        (scan results tracking)

UniverseScan    (universe-wide scan results)
```

### Database Configuration

**Location**: `app/services/database.py`

**Features**:
- ✅ SQLAlchemy 2.0 support
- ✅ Connection pooling (QueuePool for PostgreSQL)
- ✅ Pool management: size=5, max_overflow=10, pre_ping=true
- ✅ Railway-optimized settings (30s query timeout)
- ✅ Batch operations (bulk_save_objects)
- ✅ Query caching decorator
- ✅ Health check endpoint

**Initialization**:
```python
db_service = get_database_service()
db_service.init_db()  # Creates all tables
```

---

## 4. API ENDPOINT PATTERNS

### Standard Endpoint Pattern

All endpoints follow this structure:

```python
# app/api/patterns.py
@router.post("/detect",
             response_model=PatternResponse,
             summary="Detect Chart Pattern")
async def detect_pattern(
    request: PatternRequest,
    background_tasks: BackgroundTasks = None
) -> PatternResponse:
    try:
        # Validation
        # Cache check
        # Service call
        # Response with metadata (cached, api_used, processing_time)
    except HTTPException as e:
        # Structured error response
```

### Response Metadata Pattern

```python
class PatternResponse(BaseModel):
    success: bool
    data: Optional[Dict]
    error: Optional[str]
    cached: bool              # Was it from cache?
    api_used: str            # Which data source?
    processing_time: float   # How long?
```

### Key API Groupings

| Group | Routers | Count | Purpose |
|-------|---------|-------|---------|
| **Pattern Detection** | patterns.py | 13 endpoints | Analyze charts for setups |
| **Scanning** | scan.py | 8 endpoints | Universe scanning |
| **Charts** | charts.py | 2 endpoints | Generate chart images |
| **Watchlist** | watchlist.py | 6 endpoints | Manage tracked stocks |
| **Market Data** | market.py | 5 endpoints | Market metrics/internals |
| **Alerts** | alerts.py | 5 endpoints | Alert management |
| **Telegram** | telegram_enhanced.py | 8+ endpoints | Bot commands |
| **Trades** | trades.py | 5+ endpoints | Trade tracking |
| **Analytics** | analytics.py | 3 endpoints | Reporting |

---

## 5. EXTERNAL SERVICE INTEGRATIONS

### Market Data (Multi-Source Fallback)

**Service**: `app/services/market_data.py`

```
Priority Chain:
1. Redis Cache (CacheService)
2. TwelveData API (primary, 800/day free)
3. Finnhub API (fallback, 60/day free)
4. Alpha Vantage API (backup, 500/day free)
5. Yahoo Finance (final fallback, rate limited)
```

**Configuration** (`.env.example`):
```
TWELVEDATA_API_KEY=...
FINNHUB_API_KEY=...
ALPHA_VANTAGE_API_KEY=...
DATA_SOURCE_PRIORITY=twelvedata,finnhub,alphavantage
```

### Telegram Bot Integration

**Service**: `app/api/telegram_enhanced.py` + `app/services/alerts.py`

**Features**:
- ✅ Webhook-based (sets via `/setWebhook` in lifecycle)
- ✅ Command parsing: /pattern, /scan, /watchlist, /add, /remove, /plan
- ✅ Message formatting with Markdown
- ✅ Inline keyboards with callback buttons
- ✅ Photo/chart sending capability

**Configuration**:
```
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_CHAT_ID=your-chat-id
TELEGRAM_WEBHOOK_URL=auto-detected from Railway
```

**Auto-Webhook Setup**: `app/lifecycle.py`
- Runs at startup
- Auto-detects Railway public domain
- Sets webhook to `/api/webhook/telegram`

### Chart Generation (Chart-IMG)

**Service**: `app/services/charting.py`

**Features**:
- TradingView-powered chart rendering
- Support for technical studies (RSI, MACD, Volume)
- Light/dark themes
- Burst limiting (prevents overload)

**Configuration**:
```
CHART_IMG_API_KEY=...
CHARTIMG_DAILY_LIMIT=500
CACHE_TTL_CHARTS=7200  # 2 hours
```

### Email Alerts (SendGrid)

**Service**: `app/services/alerts.py`

**Features**:
- HTML email formatting
- Professional styling
- Configured via `app/config.py`

**Configuration**:
```
SENDGRID_API_KEY=...
ALERT_EMAIL=your-email@example.com
```

### AI Integration (OpenRouter)

**Service**: `app/routers/ai_chat.py`

**Models Supported**:
- Claude 3.5 Sonnet (recommended, cheapest per token)
- GPT-4, Gemini Pro, GPT-3.5

**Configuration**:
```
OPENROUTER_API_KEY=...
AI_MODEL=anthropic/claude-3.5-sonnet
AI_TEMPERATURE=0.7
```

---

## 6. CONFIGURATION PATTERNS

### Settings Management

**File**: `app/config.py`

**Using Pydantic BaseSettings**:
```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
    
    # Telegram
    telegram_bot_token: str = "dev-token"
    telegram_chat_id: Optional[str] = None
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # Database
    database_url: Optional[str] = None
    
    # Cache TTLs
    cache_ttl_patterns: int = 3600      # 1 hour
    cache_ttl_market_data: int = 900    # 15 min
    cache_ttl_charts: int = 7200        # 2 hours
    
    # Rate limits
    rate_limit_per_minute: int = 60
    ai_rate_limit_per_minute: int = 20
    
    # Feature flags
    legend_flags_enable_scanner: int = 1

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

### Environment Variables

**Key Categories**:

1. **Core App**
   - DEBUG, SECRET_KEY, APP_NAME, LOG_LEVEL

2. **External APIs**
   - TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
   - TWELVEDATA_API_KEY, FINNHUB_API_KEY
   - CHART_IMG_API_KEY, OPENROUTER_API_KEY

3. **Infrastructure**
   - DATABASE_URL (Railway-provided)
   - REDIS_URL (Upstash)
   - CORS_ORIGINS (auto-detected)

4. **Caching Strategy**
   - CACHE_TTL_PATTERNS, CACHE_TTL_MARKET_DATA
   - CACHE_TTL_CHARTS, CACHE_TTL_AI_RESPONSES

5. **Rate Limiting**
   - RATE_LIMIT_PER_MINUTE (global)
   - AI_RATE_LIMIT_PER_MINUTE
   - MARKET_DATA_RATE_LIMIT

---

## 7. FRONTEND STRUCTURE

### Dashboard Components

**Location**: `app/api/dashboard.py` + Static files

**Features**:
- ✅ Responsive design (Tailwind-inspired)
- ✅ TradingView embedded widgets
- ✅ Real-time metric updates
- ✅ Watchlist management UI
- ✅ Pattern detection results display
- ❌ No interactive chart editor
- ❌ Limited real-time push (polling-based)

### Static Files

**Location**: `/home/user/legend-ai-python/static/`

**Mounting**: 
```python
static_path = Path(__file__).parent.parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
```

### Swagger/OpenAPI Documentation

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`
- **OpenAPI JSON**: `/openapi.json`
- **Custom tags**: Grouped by feature (patterns, market, alerts)

---

## 8. MIDDLEWARE & INFRASTRUCTURE

### Middleware Stack

```
↓ Request
│
├─ MetricsMiddleware          # Prometheus metrics collection
├─ StructuredLoggingMiddleware # Structured JSON logging
├─ RateLimitMiddleware        # 60 req/min per IP
└─ CORSMiddleware             # Environment-aware CORS

↓ Response
```

### Rate Limiting

**Service**: `app/middleware/rate_limit.py`

```python
class RateLimitMiddleware:
    - 60 requests/minute per IP
    - Tracked via Redis
    - Returns 429 when exceeded
    - Exempts health checks
```

### Structured Logging

**Service**: `app/middleware/structured_logging.py`

```python
class StructuredLoggingMiddleware:
    - Logs all requests as JSON
    - Includes: method, path, status, duration, user_agent
    - Integration with telemetry service
```

### Metrics Collection

**Service**: `app/middleware/metrics_middleware.py`

**Metrics Exposed**:
- Request count (by endpoint, method, status)
- Response time (histogram)
- Active connections
- Error rates

**Format**: Prometheus-compatible at `/metrics`

---

## 9. CACHE STRATEGY

### Cache Service

**File**: `app/services/cache.py`

**Key Features**:
- ✅ Redis async client
- ✅ Smart TTL based on market hours
- ✅ Pattern caching (1-2 hours)
- ✅ Price data caching (15 min to 7 days depending on age)
- ✅ Chart caching (1-2 hours)
- ✅ Cache invalidation methods
- ✅ Cache statistics endpoint

**Cache Key Patterns**:
```
pattern:ticker={ticker}:interval={interval}      → Pattern results
ohlcv:{ticker}:1d:5y                            → OHLCV price data
chart:ticker={ticker}:interval={interval}       → Chart URLs
api_usage:{service}:date={date}                 → API quota tracking
```

### Multi-Tier Cache (Advanced)

**File**: `app/services/multi_tier_cache.py`

```
Hot Tier:     Redis         (5-15 min TTL, max 10k keys)
  ↓
Warm Tier:    Database      (1 hour TTL)
  ↓
Cold Tier:    CDN/S3        (24+ hours TTL)
```

---

## COMPREHENSIVE RECOMMENDATIONS FOR ALERTING INFRASTRUCTURE

### Current State Assessment

**Strengths ✅**:
1. Database schema already defined (AlertLog table exists)
2. Service layer partially implemented (AlertService exists)
3. API endpoints defined (5 alert endpoints)
4. Telegram integration working
5. Email integration ready (SendGrid)
6. Middleware/monitoring foundation present
7. Configuration system in place

**Gaps ❌**:
1. **Alerts not persisted** - AlertLog table created but never written to
2. **No alert rules engine** - hardcoded 75% confidence threshold
3. **No scheduling** - only manual triggers or background tasks without persistence
4. **No webhook support** - only Telegram and email
5. **No alert acknowledgment** - status field exists but not used
6. **No filtering/routing** - all alerts go to same channel
7. **No real-time subscriptions** - polling-based only
8. **Limited monitoring** - system alerts exist but trading alerts incomplete

### Recommended Implementation Roadmap

#### Phase 1: Stabilize Existing (Week 1)

**Priority 1a: Enable Alert Persistence**
```
File: app/services/alerts.py
Action: Modify _send_alerts() to log to database
  - Call db_service.save_alert_log() after each send
  - Track alert_type, trigger_price, status
  - Store in AlertLog table
  - Enables /api/alerts/recent to return real data
```

**Priority 1b: Fix Recent Alerts Endpoint**
```
File: app/api/alerts.py
GET /api/alerts/recent
  - Query AlertLog from DB
  - Filter by user_id, date range
  - Return with status history
```

#### Phase 2: Alert Rules Engine (Week 2-3)

**Priority 2a: Create AlertRule Model**
```python
class AlertRule(Base):
    __tablename__ = "alert_rules"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), index=True)
    
    # What to alert on
    trigger_type = Column(String(50))  # "pattern", "price", "volume", "breakout"
    pattern_type = Column(String(50), nullable=True)  # "VCP", "Cup & Handle", etc.
    min_confidence = Column(Float, default=0.75)
    
    # Alert channel routing
    send_telegram = Column(Boolean, default=True)
    send_email = Column(Boolean, default=False)
    send_webhook = Column(String(500), nullable=True)
    
    # Filtering
    symbols_only = Column(String(500), nullable=True)  # Comma-separated whitelist
    exclude_symbols = Column(String(500), nullable=True)  # Blacklist
    time_start = Column(Time, nullable=True)  # Only alert 9:30 AM - 4:00 PM?
    time_end = Column(Time, nullable=True)
    
    # Frequency control
    cooldown_minutes = Column(Integer, default=360)  # Min 6 hours between alerts
    max_alerts_per_day = Column(Integer, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    enabled = Column(Boolean, default=True)
```

**Priority 2b: Create AlertRuleEngine Service**
```python
class AlertRuleEngine:
    def __init__(self):
        self.db = get_database_service()
        self.cache = get_cache_service()
    
    async def evaluate_alert(self, 
                             pattern_result: PatternResult,
                             user_id: str = "default") -> List[Alert]:
        """
        Check if alert should be sent based on rules
        Returns list of Alert objects to send
        """
        rules = await self.db.get_alert_rules_for_user(user_id)
        matching_rules = []
        
        for rule in rules:
            if not rule.enabled:
                continue
            if pattern_result.score < rule.min_confidence:
                continue
            if rule.symbols_only and pattern_result.ticker not in rule.symbols_only.split(','):
                continue
            if pattern_result.ticker in rule.exclude_symbols.split(','):
                continue
            if not await self._can_alert_now(rule):  # Cooldown check
                continue
            matching_rules.append(rule)
        
        return matching_rules
```

#### Phase 3: Enhanced Routing & Webhooks (Week 3-4)

**Priority 3a: Add Webhook Support**
```python
class AlertDeliveryChannel(BaseModel):
    type: str  # "telegram", "email", "webhook", "discord", "slack"
    config: Dict[str, str]  # token, url, etc.

# Modify AlertService._send_alerts()
async def _send_alerts(self, alert_data: Dict, channels: List[AlertDeliveryChannel]):
    for channel in channels:
        if channel.type == "telegram":
            await self._send_telegram_alert(alert_data)
        elif channel.type == "email":
            await self._send_email_alert(alert_data)
        elif channel.type == "webhook":
            await self._send_webhook_alert(alert_data, channel.config)
        elif channel.type == "discord":
            await self._send_discord_alert(alert_data, channel.config)
        # ... etc
```

**Priority 3b: Add Webhook Destination Model**
```python
class AlertWebhook(Base):
    __tablename__ = "alert_webhooks"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), index=True)
    
    name = Column(String(100))  # "My N8N workflow"
    url = Column(String(500))  # https://webhook.site/...
    
    # Webhook payload customization
    payload_template = Column(Text)  # JSON template with {ticker}, {pattern}, etc.
    headers = Column(Text)  # JSON of custom headers
    
    # Retry policy
    max_retries = Column(Integer, default=3)
    retry_delay_seconds = Column(Integer, default=60)
    
    # Testing
    last_sent_at = Column(DateTime(timezone=True), nullable=True)
    last_status = Column(Integer, nullable=True)  # HTTP status code
    
    enabled = Column(Boolean, default=True)
```

#### Phase 4: Real-Time Subscriptions (Week 4-5)

**Priority 4a: WebSocket Support**
```python
# app/api/websocket.py
from fastapi import WebSocket

@router.websocket("/ws/alerts/{user_id}")
async def websocket_alerts(websocket: WebSocket, user_id: str):
    await websocket.accept()
    
    # Subscribe to alert stream
    async for alert in alert_service.subscribe_alerts(user_id):
        await websocket.send_json(alert.dict())
```

**Priority 4b: Server-Sent Events (SSE) Alternative**
```python
# Simpler than WebSocket
@router.get("/api/alerts/stream/{user_id}")
async def stream_alerts(user_id: str):
    return StreamingResponse(
        alert_service.stream_alerts(user_id),
        media_type="text/event-stream"
    )
```

#### Phase 5: Monitoring & Analytics (Week 5-6)

**Priority 5a: Alert Metrics**
```python
# app/telemetry/alerting_metrics.py
ALERTS_SENT_TOTAL = Counter('alerts_sent_total', 'Total alerts sent', ['type', 'channel'])
ALERT_RULES_EVALUATED = Counter('alert_rules_evaluated_total', 'Rules evaluated')
ALERT_SEND_DURATION = Histogram('alert_send_duration_seconds', 'Time to send alert')
ALERTS_FAILED = Counter('alerts_failed_total', 'Failed alerts', ['channel', 'error'])
```

**Priority 5b: Alert Dashboard**
```
GET /api/alerts/stats
  - Alerts sent (by type, by channel, by day)
  - Alert delivery success rate
  - Most common patterns alerted
  - Top symbols alerted
  - Alerts by time of day
```

### File Structure for New Alerting System

```
app/
├── api/
│   ├── alerts.py  (EXPAND)
│   └── alert_webhooks.py  (NEW)
│
├── models.py  (ADD)
│   └── AlertRule
│   └── AlertWebhook
│   └── AlertDeliveryLog  (more detailed than AlertLog)
│
├── services/
│   ├── alerts.py  (ENHANCE)
│   ├── alert_rules.py  (NEW)
│   ├── alert_delivery.py  (NEW)
│   └── alert_scheduler.py  (NEW)
│
├── core/
│   ├── alert_processor.py  (NEW)
│   └── webhook_dispatcher.py  (NEW)
│
├── telemetry/
│   ├── alerting_metrics.py  (NEW)
│   └── alerter.py  (ENHANCE)
│
└── routers/
    └── websocket.py  (NEW - optional)
```

### Database Migration Strategy

```python
# alembic/versions/001_add_alerting_tables.py

def upgrade():
    op.create_table('alert_rules',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.String(100), index=True),
        sa.Column('trigger_type', sa.String(50)),
        # ... rest of columns
    )
    
    op.create_table('alert_webhooks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.String(100), index=True),
        # ... rest of columns
    )
    
    op.create_table('alert_delivery_logs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('alert_rule_id', sa.Integer, sa.ForeignKey('alert_rules.id')),
        # ... rest of columns
    )

def downgrade():
    op.drop_table('alert_delivery_logs')
    op.drop_table('alert_webhooks')
    op.drop_table('alert_rules')
```

---

## QUICK REFERENCE: WHERE TO IMPLEMENT FEATURES

| Feature | Primary File | Support Files | Priority |
|---------|-------------|----------------|----------|
| **Enable DB Persistence** | `app/services/alerts.py` | `app/models.py` | 🔴 P0 |
| **Rules Engine** | `app/services/alert_rules.py` (new) | `app/models.py` | 🟠 P1 |
| **Webhook Support** | `app/services/alert_delivery.py` (new) | `app/models.py` | 🟠 P1 |
| **Alert Scheduling** | `app/services/alert_scheduler.py` (new) | `app/lifecycle.py` | 🟠 P1 |
| **Metrics & Analytics** | `app/telemetry/alerting_metrics.py` (new) | `app/api/alerts.py` | 🟡 P2 |
| **WebSocket/Real-time** | `app/routers/websocket.py` (new) | `app/services/alerts.py` | 🟡 P2 |
| **Alert Testing Tools** | `app/api/alerts.py` | `app/services/alerts.py` | 🟡 P2 |

---

## DEPENDENCIES & TECH STACK

### Current Dependencies (from requirements.txt)
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- Pydantic 2.5.0
- Redis 5.0.1
- httpx (async HTTP client)
- Prometheus-client (metrics)
- Pandas, NumPy (data processing)

### New Dependencies for Enhanced Alerting
```
python-dateutil      # For time-based scheduling
APScheduler          # For alert scheduling
pydantic-extra-types # For Email validation
tenacity            # For retry logic
fastapi-events      # For event streaming (optional)
```

---

## DEPLOYMENT CONSIDERATIONS

### Railway-Specific Configuration

```env
# Auto-configured by Railway
DATABASE_URL=postgresql://user:password@host/db  # PostgreSQL provided
RAILWAY_PUBLIC_DOMAIN=your-app.railway.app       # Auto-detected
RAILWAY_GIT_COMMIT_SHA=...                       # For versioning

# Manual configuration needed
TELEGRAM_BOT_TOKEN=...
CHART_IMG_API_KEY=...
OPENROUTER_API_KEY=...
```

### Health Check Endpoints

```
GET /health       # Fast check (config only, no network calls)
GET /healthz      # K8s/Railway liveness probe
GET /health/detailed  # Full diagnostics
GET /metrics      # Prometheus metrics
```

---

## TESTING STRATEGY

```
tests/
├── test_alert_rules.py      # Rules engine logic
├── test_alert_delivery.py   # Channel delivery
├── test_alert_webhooks.py   # Webhook integration
├── test_alert_scheduler.py  # Scheduling logic
└── test_alerts_integration.py  # E2E alert flow
```

### Key Test Cases

1. **Rule Evaluation**
   - Confidence threshold filtering
   - Symbol whitelist/blacklist
   - Cooldown period enforcement
   - Time-of-day filtering

2. **Delivery**
   - Telegram delivery success/failure
   - Email formatting
   - Webhook retries
   - Channel routing

3. **Persistence**
   - Alert logged to database
   - Status tracking (sent, failed, acknowledged)
   - Query recent alerts by user

---

## IMPLEMENTATION PRIORITY MATRIX

```
Priority    Effort    Impact    Timeline    Must-Do?
────────────────────────────────────────────────────────
P0  DB Persist    Low       High       Immediate   YES
P1  Rules Engine  Medium    High       Week 1-2    YES
P1  Webhook       Medium    Medium     Week 2-3    MAYBE
P2  Scheduling    High      Medium     Week 3-4    MAYBE
P2  WebSocket     High      Low        Week 4-5    MAYBE
P3  Analytics     Medium    Low        Week 5-6    MAYBE
```

---

## SUMMARY

**Legend AI has a solid foundation for alerting infrastructure with:**
- Pre-built database schema (AlertLog)
- Service layer structure (AlertService)
- API endpoints (5 alert endpoints)
- Telegram integration (working)
- Email integration (ready)

**Quick Wins (First 2 Days):**
1. Enable AlertLog database persistence
2. Fix /api/alerts/recent endpoint
3. Verify Telegram delivery
4. Add test endpoint

**Strategic Priorities (Following Weeks):**
1. Rules engine for flexible alert conditions
2. Webhook support for integrations
3. Real-time monitoring metrics
4. Alert scheduling capabilities

This positions Legend AI to support sophisticated trading alert workflows with professional-grade reliability and flexibility.

