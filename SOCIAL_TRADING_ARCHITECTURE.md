# Legend AI Trading Platform - Architecture & Social Trading Implementation Guide

## Executive Summary

The Legend AI platform is a FastAPI-based trading pattern detection and analysis system with:
- **Backend**: Python FastAPI microservice architecture
- **Database**: PostgreSQL with SQLAlchemy ORM (with Alembic migrations)
- **Cache**: Redis for performance optimization
- **Frontend**: HTML/JavaScript dashboard with TradingView widgets
- **Integration**: Telegram bot, AI assistant (Claude/OpenAI), multiple market data APIs

**Current State**: The platform has **foundational user tracking** (via Telegram user IDs) but NO proper user authentication, profiles, or social features yet.

---

## 1. PROJECT STRUCTURE

### Directory Layout

```
/home/user/legend-ai-python/
├── app/                          # Main FastAPI application
│   ├── main.py                   # FastAPI app initialization + routers
│   ├── config.py                 # Environment settings & configuration
│   ├── models.py                 # SQLAlchemy ORM models (6 tables)
│   ├── lifecycle.py              # App startup/shutdown hooks
│   ├── api/                      # 23 API route modules (60+ endpoints)
│   │   ├── patterns.py           # Pattern detection endpoints
│   │   ├── charts.py             # Chart generation
│   │   ├── trades.py             # Trade management
│   │   ├── watchlist.py          # Watchlist CRUD
│   │   ├── scan.py               # Universe scanning
│   │   ├── market.py             # Market data/metrics
│   │   ├── universe.py           # Universe management
│   │   ├── alerts.py             # Alert management
│   │   ├── telegram_enhanced.py  # Telegram integration
│   │   ├── ai_chat.py            # AI assistant endpoints
│   │   └── ... (14 more routers)
│   ├── routers/                  # Custom routers
│   │   ├── ai_chat.py            # Chat & analysis endpoints
│   │   └── advanced_analysis.py  # Advanced analysis features
│   ├── services/                 # Business logic
│   │   ├── database.py           # PostgreSQL service
│   │   ├── trades.py             # Trade management service
│   │   ├── cache.py              # Redis cache service
│   │   ├── market_data.py        # Market data fetching
│   │   ├── pattern_scanner.py    # Pattern detection service
│   │   ├── charting.py           # Chart generation
│   │   ├── multitimeframe.py     # Multi-timeframe analysis
│   │   └── ... (8 more services)
│   ├── core/                     # Core pattern detection
│   │   ├── detectors/            # Pattern detectors (9 types)
│   │   │   ├── vcp_detector.py
│   │   │   ├── cup_handle_detector.py
│   │   │   ├── triangle_detector.py
│   │   │   ├── channel_detector.py
│   │   │   ├── wedge_detector.py
│   │   │   ├── head_shoulders_detector.py
│   │   │   ├── double_top_bottom_detector.py
│   │   │   ├── sma50_pullback_detector.py
│   │   │   └── ... (more)
│   │   ├── indicators.py         # Technical indicators
│   │   ├── pattern_detector_v2.py
│   │   └── detector_registry.py
│   ├── middleware/               # Request/response middleware
│   │   ├── structured_logging.py
│   │   ├── rate_limit.py
│   │   └── metrics_middleware.py
│   ├── ai/                       # AI/ML features
│   │   └── assistant.py          # Claude/OpenAI integration
│   ├── telemetry/                # Monitoring & observability
│   │   ├── metrics.py
│   │   ├── monitoring.py
│   │   └── alerter.py
│   └── utils/                    # Utilities
├── static/                       # Frontend assets
│   ├── css/
│   │   ├── dashboard.css
│   │   └── cyberpunk-design-system.css
│   ├── js/
│   │   ├── dashboard.js
│   │   └── tv-widgets.js
│   └── images/
├── templates/                    # HTML templates
│   ├── dashboard.html            # Main dashboard
│   └── tv_symbol_lab.html        # TradingView lab
├── tests/                        # Test suite (35+ test files)
├── alembic/                      # Database migrations (Alembic)
├── monitoring/                   # Monitoring configs (Prometheus, Grafana, AlertManager)
└── docs/                         # Documentation

```

### Key Technologies
- **Backend**: FastAPI 0.100+ (async-first)
- **Database**: PostgreSQL with SQLAlchemy 2.0 + Alembic
- **Cache**: Redis (multi-tier caching strategy)
- **API Clients**: httpx (async HTTP client)
- **Market Data**: TwelveData, Finnhub, Alpha Vantage, Yahoo Finance
- **Charting**: Chart-IMG API
- **AI**: OpenRouter/Claude API
- **Frontend**: HTML5 + Vanilla JavaScript + TradingView Lightweight Charts
- **Deployment**: Railway (Docker + GitHub)

---

## 2. DATABASE & MODELS SETUP

### Current Database Schema (6 Tables in PostgreSQL)

```python
# app/models.py (SQLAlchemy ORM)

1. Ticker
   - id (PK)
   - symbol (unique, indexed)
   - name
   - sector
   - industry
   - exchange
   - created_at / updated_at

2. PatternScan (Pattern Detection Results)
   - id (PK)
   - ticker_id (FK) → Ticker
   - pattern_type (VCP, Cup & Handle, etc.)
   - score
   - entry_price / stop_price / target_price
   - risk_reward_ratio
   - criteria_met (JSON string)
   - analysis
   - current_price
   - volume_dry_up (boolean)
   - consolidation_days
   - chart_url
   - rs_rating
   - scanned_at (indexed, for queries)

3. Watchlist (User Watchlist with Status Tracking)
   - id (PK)
   - user_id (String[100], indexed) ← Currently just Telegram ID or "default"
   - ticker_id (FK) → Ticker
   - status ("Watching", "Breaking Out", "Triggered", "Completed", "Skipped")
   - target_entry / target_stop / target_price
   - reason (text)
   - notes (text)
   - alerts_enabled (boolean)
   - alert_threshold (%)
   - added_at / triggered_at / updated_at

4. ScanLog (Scanning History)
   - id (PK)
   - scan_type ("daily", "weekly", "custom")
   - tickers_scanned
   - patterns_found
   - start_time / end_time
   - status ("completed", "failed", "partial")
   - error_message

5. UniverseScan (Market Scanning Results)
   - id (PK)
   - scan_date (indexed)
   - universe ("SP500", "NASDAQ100", "CUSTOM")
   - total_scanned
   - patterns_found
   - top_score
   - duration_seconds
   - status / error_message

6. AlertLog (Alert Trigger History)
   - id (PK)
   - ticker_id (FK) → Ticker
   - alert_type ("price", "pattern", "breakout", "volume")
   - trigger_price / trigger_value
   - alert_sent_at (indexed)
   - sent_via ("telegram", "email", "push")
   - user_id (indexed) ← String identifier
   - status ("sent", "failed", "acknowledged")
```

### Database Service Architecture

```
DatabaseService (app/services/database.py)
├── Connection Management
│   ├── SQLAlchemy engine with connection pooling
│   ├── PostgreSQL optimized (pool_size=5, max_overflow=10)
│   ├── Connection recycling (3600s)
│   └── Pool pre-ping (health checks)
├── Query Methods
│   ├── get_or_create_ticker()
│   ├── get_tickers()
│   ├── save_pattern_scan()
│   ├── save_pattern_scans_batch() ← Optimized bulk insert
│   ├── get_recent_scans()
│   ├── add_watchlist_symbol()
│   ├── get_watchlist_items()
│   └── ... (20+ methods)
└── Query Caching
    └── @cache_query decorator for automatic Redis caching
```

### Migrations Setup
- **Alembic** is configured for database schema versioning
- Located in `/home/user/legend-ai-python/alembic/`
- Auto-creates tables on `database.init_db()` call

---

## 3. API ROUTING PATTERNS

### Main Application Setup (app/main.py)

```python
FastAPI app with:
├── Middleware Stack (bottom-to-top)
│   ├── MetricsMiddleware          (HTTP metrics collection)
│   ├── StructuredLoggingMiddleware (Telemetry tracking)
│   ├── RateLimitMiddleware         (60 req/min per IP)
│   └── CORSMiddleware              (Environment-aware origins)
│
├── 19 Registered Routers (prefix=/api)
│   ├── patterns_router         → POST /api/patterns/detect
│   ├── charts_router           → GET /api/charts/*
│   ├── universe_router         → GET /api/universe/*
│   ├── watchlist_router        → CRUD /api/watchlist/*
│   ├── trade_router            → CRUD /api/trades/*
│   ├── analytics_router        → GET /api/analytics/*
│   ├── market_router           → GET /api/market/*
│   ├── alerts_router           → CRUD /api/alerts/*
│   ├── multitf_router          → GET /api/multitimeframe/*
│   ├── risk_router             → POST /api/risk/*
│   ├── trades_router           → GET /api/trades/*
│   ├── scan_router             → POST /api/scan/*
│   ├── telegram_router         → Webhook /api/telegram/*
│   ├── tv_router               → TradingView /api/tv/*
│   ├── ai_chat_router          → /api/ai/chat, /api/ai/analyze
│   ├── advanced_analysis_router → Advanced features
│   ├── cache_mgmt_router       → Cache management
│   ├── api_usage_router        → API usage tracking
│   └── ... (more)
│
└── Static Files & Templates
    ├── /dashboard               → dashboard.html
    └── /static/*                → CSS, JS, images
```

### Router Pattern Example (Standardized Across Codebase)

```python
# Pattern: Each router follows this structure
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

router = APIRouter(prefix="/api/patterns", tags=["patterns"])
logger = logging.getLogger(__name__)

# 1. Pydantic Models for request/response validation
class PatternRequest(BaseModel):
    ticker: str
    interval: str  # "1day", "1week", etc.
    ...

# 2. Endpoint with full documentation
@router.post("/detect", response_model=Dict[str, Any])
async def detect_pattern(request: PatternRequest):
    """
    Detect trading patterns for a given ticker
    
    Args:
        ticker: Stock symbol (e.g., AAPL)
        interval: Timeframe (1day, 1week, etc.)
    
    Returns:
        Pattern detection results with scores & charts
    """
    try:
        # Service layer call
        result = await pattern_service.detect(request.ticker, request.interval)
        return {"success": True, "data": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Pattern detection failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# 3. Health check endpoint
@router.get("/health")
async def health():
    return {"status": "healthy", "service": "patterns"}
```

### API Endpoints Summary (60+ total)

| Router | Endpoints | Purpose |
|--------|-----------|---------|
| patterns | /detect, /cache/stats | Pattern detection |
| charts | /image, /cache, /burst | Chart generation |
| trades | /create, /close, /open, /closed, /statistics | Trade tracking |
| watchlist | /add, /get, /remove | Watchlist management |
| scan | /universe, /status | Scanning operations |
| market | /metrics, /sentiment, /internals | Market data |
| universe | /list, /update, /scan | Universe management |
| alerts | /create, /list, /update | Alert management |
| telegram | /webhook, /commands | Telegram bot |
| ai_chat | /chat, /analyze, /compare | AI assistant |
| ... (9 more routers) | ... | ... |

---

## 4. EXISTING USER/PROFILE FUNCTIONALITY

### Current User Model
**Status**: MINIMAL - Basic user tracking via Telegram IDs only

### Existing User References
```python
# In Models:
Watchlist.user_id = Column(String(100), default="default")
AlertLog.user_id = Column(String(100), nullable=True)

# In Services:
# app/services/trades.py
# Trades are stored in Redis by trade_id (no user isolation)
# app/services/database.py
# No user-specific queries exist
```

### What's Missing
1. **No User Account System** - No signup/login/authentication
2. **No User Profiles** - No user profile data, preferences, or stats
3. **No User Isolation** - No access control (everyone sees same data)
4. **No User-Specific Data** - Trades not tied to users, watchlists are global
5. **No Social Features** - No followers, following, leaderboards, or trade sharing
6. **No API Keys/Tokens** - No JWT or authentication tokens
7. **No User Preferences** - No settings, notification preferences, or trading preferences

### Current Authentication
- **Telegram Bot**: Uses Telegram user_id for identification (not secure for web)
- **No Web Auth**: Dashboard is public, no login required
- **No API Auth**: All API endpoints are public

---

## 5. TRADING-RELATED COMPONENTS ALREADY IN PLACE

### A. Pattern Detection System (Most Developed Feature)

#### 9 Pattern Detectors Implemented
```
app/core/detectors/
├── vcp_detector.py              → Volatility Contraction Pattern
├── cup_handle_detector.py       → Cup & Handle formations
├── triangle_detector.py          → Ascending/Descending triangles
├── channel_detector.py           → Parallel channel patterns
├── wedge_detector.py             → Rising/Falling wedges
├── head_shoulders_detector.py   → Head & Shoulders reversals
├── double_top_bottom_detector.py → Double tops/bottoms
├── sma50_pullback_detector.py   → SMA50 pullback patterns
└── (More in detector_registry.py)
```

**Detector Output Format**:
```python
PatternResult:
  - pattern: str                  # Pattern name (VCP, Cup & Handle, etc.)
  - score: float (0-100)         # Confidence score
  - entry: float                  # Suggested entry price
  - stop: float                   # Stop loss price
  - target: float                 # Take profit target
  - risk_reward: float            # Risk-to-reward ratio
  - criteria_met: List[str]      # Pattern criteria matched
  - analysis: str                 # Detailed analysis text
```

#### Pattern Detection Pipeline
```
1. Market Data Fetch
   ├── Cache (15 min TTL)
   ├── TwelveData API (primary)
   ├── Finnhub API (fallback)
   ├── Alpha Vantage (fallback)
   └── Yahoo Finance (fallback)
   
2. Technical Indicators (Calculated)
   ├── Moving Averages (SMA, EMA)
   ├── Volume Analysis
   ├── Support/Resistance
   ├── Trend Lines
   ├── Momentum (RSI, MACD, Stochastic)
   └── Volatility (ATR, Bollinger Bands)
   
3. Pattern Detectors (Parallel)
   ├── Run all 9 detectors simultaneously
   ├── Cache results (1 hour TTL)
   └── Return matches with scores
   
4. Chart Generation
   ├── Chart-IMG API
   ├── Generate pattern visualization
   └── Cache charts (2 hour TTL)
```

### B. Trade Management System

#### Trade Model & Service
```python
Trade (in-memory via Redis):
  - trade_id: UUID
  - ticker: str
  - entry_price: float
  - stop_loss: float
  - target_price: float
  - position_size: int
  - risk_amount: float
  - reward_amount: float
  - status: "open" | "closed"
  - entry_date: datetime
  - exit_date: datetime (if closed)
  - profit_loss: float
  - profit_loss_pct: float
  - win: bool
  - r_multiple: float (profit / risk)
  - notes: str
```

#### Trade Endpoints
```python
POST /api/trades/create          → Create trade
POST /api/trades/close           → Close trade with exit price
GET /api/trades/open             → Get open trades
GET /api/trades/closed           → Get closed trades (paginated)
GET /api/trades/statistics       → Get trading statistics
```

#### Trading Statistics Calculated
```python
Statistics:
  - total_trades
  - winning_trades / losing_trades
  - win_rate (%)
  - total_profit_loss
  - profit_factor
  - average_win / average_loss
  - average_r_multiple
  - expectancy_per_trade
```

### C. Risk Management

#### Risk Calculation Endpoints
```python
POST /api/risk/position-size     → Calculate shares for risk amount
POST /api/risk/risk-reward       → Calculate R:R ratio
POST /api/risk/kelly-criterion   → Kelly formula calculation
```

**Risk Inputs**:
- Entry price, stop loss, target price
- Account risk % or fixed dollar amount
- Commission per share (optional)

### D. Universe Scanning

#### Scanner Features
```python
POST /api/scan/universe          → Scan selected universe
POST /api/scan/custom            → Custom symbol list scan
GET /api/scan/status             → Scan progress/status
```

**Universes Supported**:
- SP500
- NASDAQ100
- Custom lists

### E. Watchlist Management

#### Watchlist Features
```python
POST /api/watchlist/add          → Add ticker + reason + tags
GET /api/watchlist               → Get all watched tickers
DELETE /api/watchlist/remove/:ticker  → Remove from watchlist
```

**Watchlist Statuses**:
- Watching (initial)
- Breaking Out (pattern detected)
- Triggered (price target met)
- Completed (trade closed)
- Skipped (passed on trade)

### F. Alerts System

#### Alert Types Supported
```python
AlertTypes:
  - "price"     → Price level alerts
  - "pattern"   → New pattern detected
  - "breakout"  → Breakout alerts
  - "volume"    → Volume spike alerts
```

#### Alert Delivery
- Telegram (primary)
- Email (optional, SendGrid)
- Push notifications (future)

### G. Technical Indicators

```python
# app/core/indicators.py

Available Indicators:
  - Simple Moving Average (SMA)
  - Exponential Moving Average (EMA)
  - Relative Strength Index (RSI)
  - Moving Average Convergence Divergence (MACD)
  - Average True Range (ATR)
  - Bollinger Bands
  - Stochastic Oscillator
  - Volume-weighted metrics
  - Trend line detection
  - Support/Resistance zones
```

### H. Chart Generation

#### Chart Service
```python
ChartingService:
  - Chart-IMG API integration
  - Pattern visualization
  - Technical indicator overlays
  - Burst limit handling (graceful degradation)
  - Caching strategy (2 hour TTL)
```

---

## ARCHITECTURE RECOMMENDATIONS FOR SOCIAL TRADING FEATURES

### Current Gaps to Address

| Feature | Current State | Needed |
|---------|---------------|--------|
| User Authentication | ❌ None | JWT-based auth |
| User Profiles | ❌ None | User table + profile data |
| User Isolation | ❌ Global data | Per-user data isolation |
| Trade Attribution | ⚠️ In-memory cache | Database persistence |
| Follower System | ❌ None | User relationships table |
| Trade Sharing | ❌ None | Trade sharing + visibility API |
| Leaderboards | ❌ None | Stats aggregation queries |
| Performance Tracking | ⚠️ Limited | Comprehensive stats table |
| API Authorization | ❌ None | Per-user API key system |

### Recommended Implementation Locations

#### 1. Database Schema Additions
```
New Tables to Create (via Alembic migration):
app/models.py
├── User (accounts, profiles)
├── UserProfile (preferences, stats)
├── Follow (user relationships)
├── SharedTrade (social trading)
├── TradePerformance (aggregated stats)
└── UserRole (for future admins/mods)
```

#### 2. Authentication System
```
New Modules:
app/services/auth.py
  ├── JWT token generation/validation
  ├── Password hashing (bcrypt)
  ├── Session management
  └── API key generation

app/api/auth.py (Router)
  ├── POST /api/auth/register
  ├── POST /api/auth/login
  ├── POST /api/auth/logout
  ├── POST /api/auth/refresh-token
  └── POST /api/auth/request-password-reset
```

#### 3. User/Profile Endpoints
```
New Router: app/api/users.py
├── GET /api/users/me                    # Current user profile
├── PUT /api/users/me                    # Update profile
├── GET /api/users/:user_id              # Public profile
├── POST /api/users/me/settings          # User preferences
├── GET /api/users/:user_id/stats        # Trading statistics
└── DELETE /api/users/me                 # Account deletion
```

#### 4. Social Features - Follow System
```
New Router: app/api/follows.py
├── POST /api/follows/:user_id           # Follow user
├── DELETE /api/follows/:user_id         # Unfollow
├── GET /api/follows/followers           # Get my followers
├── GET /api/follows/following           # Who I follow
├── GET /api/users/:user_id/followers    # User's followers
└── GET /api/users/:user_id/following    # User's following
```

#### 5. Social Trading Features
```
New Router: app/api/social-trades.py
├── POST /api/social-trades/create       # Share/publish trade
├── GET /api/social-trades/feed          # Social trading feed
├── GET /api/social-trades/:trade_id     # View shared trade
├── POST /api/social-trades/:trade_id/copy  # Copy trade
├── GET /api/social-trades/:trade_id/reactions  # Likes/comments
├── POST /api/social-trades/:trade_id/like     # Like trade
├── POST /api/social-trades/:trade_id/comment  # Comment on trade
└── DELETE /api/social-trades/:trade_id  # Delete shared trade
```

#### 6. Leaderboards
```
New Router: app/api/leaderboards.py
├── GET /api/leaderboards/winrate
├── GET /api/leaderboards/profitability
├── GET /api/leaderboards/consistency
├── GET /api/leaderboards/roi
├── GET /api/leaderboards/followers
└── GET /api/leaderboards/period (daily, weekly, monthly, all-time)
```

#### 7. Update Existing Services
```
Modifications Needed:
├── app/services/trades.py
│   └── Add user_id parameter to all methods (BREAKING CHANGE)
├── app/services/database.py
│   └── Add user relationship to all trade queries
├── app/api/trades.py
│   └── Add user authentication check to all endpoints
└── middleware
    └── Add per-user rate limiting (not global)
```

#### 8. Frontend Changes
```
Template Updates:
├── templates/dashboard.html
│   ├── Add login/registration UI
│   ├── Add user profile dropdown
│   ├── Add social feed section
│   └── Add leaderboard view
└── static/js/
    ├── new: auth.js (login/token management)
    ├── new: social.js (follow, share, like features)
    └── update: dashboard.js (add user context)
```

---

## IMPLEMENTATION ROADMAP FOR SOCIAL TRADING

### Phase 1: Foundation (Week 1-2)
1. Create `User` and `UserProfile` tables (Alembic migration)
2. Implement authentication service (JWT, bcrypt)
3. Add `/api/auth/register`, `/api/auth/login` endpoints
4. Update middleware to check authentication tokens
5. Create user profile API (`/api/users/me`)

### Phase 2: Data Migration (Week 2-3)
1. Update `trades.py` service to use `user_id` parameter
2. Migrate existing trade data to new schema
3. Update all trade endpoints to require authentication
4. Implement per-user trade isolation

### Phase 3: Social Core (Week 3-4)
1. Create `Follow` table (user relationships)
2. Implement follow/unfollow API
3. Create `SharedTrade` table
4. Add social trading endpoints

### Phase 4: Engagement (Week 4-5)
1. Implement likes/comments on trades
2. Add leaderboard calculations
3. Create performance aggregation queries
4. Build leaderboard endpoints

### Phase 5: Polish (Week 5-6)
1. Update frontend with social UI
2. Add notifications (WebSocket or polling)
3. Implement API key system for users
4. Add social feed aggregation

---

## CACHING STRATEGY FOR SOCIAL FEATURES

```
Redis Key Patterns (to Add):

# User Data (Hot tier)
user:{user_id}               → User profile (TTL: 1h)
user:{user_id}:stats        → User stats (TTL: 30min)
user:{user_id}:trades       → User trades (TTL: 5min)

# Social Data (Warm tier)
follows:{user_id}           → Following list (TTL: 1h)
followers:{user_id}         → Follower list (TTL: 1h)
leaderboard:{period}        → Leaderboard (TTL: 30min)

# Feed Data (Hot tier)
feed:{user_id}              → User's social feed (TTL: 5min)
shared_trades:{user_id}     → Shared trades by user (TTL: 10min)

# Search/Discovery (Warm tier)
top_traders:week            → Weekly top performers (TTL: 1h)
trending_trades             → Trending trades (TTL: 15min)
```

---

## KEY METRICS TO TRACK

```python
# User Metrics
- Total users created
- Active monthly users (MAU)
- Authentication success/failure rate
- API key usage per user

# Social Metrics
- Total follows/followers
- Social feed engagement (views, likes, comments)
- Trade copies (copy popularity)
- User retention (% returning weekly)

# Trading Metrics (Per-user)
- Win rate
- Profitability
- Consistency (std dev of returns)
- Follower growth rate
- Leaderboard position changes
```

---

## SECURITY CONSIDERATIONS

### For Social Features
1. **Rate Limiting**: Per-user limits (not just IP-based)
2. **Authorization**: Check user ownership before updates/deletes
3. **Validation**: Input validation on all social data
4. **Privacy**: Hide sensitive data (actual P&L, account balance)
5. **Spam Prevention**: Limits on trade sharing, comments, follows
6. **Data Integrity**: Transactions for follow/unfollow, trade copies

### Token Security
1. JWT with short expiry (15 min) + refresh tokens (7 days)
2. Secure HttpOnly cookies for web
3. Rate limit login attempts
4. Password requirements (min 8 chars, complexity)

---

## TESTING STRATEGY

```
New Test Files Needed:
├── tests/test_auth.py
│   └── Registration, login, token refresh, password reset
├── tests/test_users.py
│   └── Profile CRUD, settings, stats calculation
├── tests/test_follows.py
│   └── Follow/unfollow, follower lists, privacy
├── tests/test_social_trades.py
│   └── Share, copy, reactions (likes/comments)
├── tests/test_leaderboards.py
│   └── Leaderboard calculation, ranking, periods
└── tests/test_social_integration.py
    └── End-to-end social trading workflows
```

---

## DEPLOYMENT CHANGES

### Environment Variables to Add
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/legend_social

# Authentication
JWT_SECRET_KEY=<random-secret>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Social Features
ENABLE_SOCIAL_TRADING=true
MAX_TRADE_SHARES_PER_DAY=10
MAX_FOLLOWS_PER_USER=1000
```

### Migration Strategy
1. Deploy authentication system first (non-breaking)
2. Create new tables in parallel
3. Gradually migrate trade data (background job)
4. Enable per-user isolation via feature flag
5. Launch social features once data fully migrated

