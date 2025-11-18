# Legend AI - Comprehensive Codebase Architecture & Tax Optimization Integration Plan

## Executive Summary

Legend AI is a professional trading pattern scanner and analysis platform built with **FastAPI (Python)** backend. The system currently supports:
- Pattern detection (VCP, Cup & Handle, Head & Shoulders, etc.)
- Real-time market data aggregation from multiple sources
- Position sizing and risk management
- Trade tracking and performance statistics
- Professional charting capabilities
- Telegram bot integration

**Current Scale**: ~75+ API files in total | 15+ API routers | 50+ endpoints | 20+ services

---

## PART 1: CURRENT PROJECT ORGANIZATION & FILE STRUCTURE

### 1.1 Root Directory Structure

```
legend-ai-python/
├── app/                           # Main application code
├── tests/                         # Test suite (19 test files)
├── alembic/                       # Database migrations setup
├── docs/                          # Documentation
├── monitoring/                    # Monitoring and metrics
├── static/                        # Frontend assets (CSS, JS)
├── templates/                     # HTML templates
├── scripts/                       # Utility scripts
├── requirements.txt               # Python dependencies
├── pytest.ini                     # Pytest configuration
├── docker-compose.yml             # Docker setup
├── Dockerfile                     # Container definition
└── README.md                      # Project documentation
```

### 1.2 Main Application Structure (`app/`)

```
app/
├── main.py                        # FastAPI entry point (160+ lines)
├── config.py                      # Pydantic settings management
├── models.py                      # SQLAlchemy database models (105 lines)
├── lifecycle.py                   # App startup/shutdown events
├── docs_config.py                 # OpenAPI documentation config
│
├── api/                           # 25+ API route files
│   ├── analyze.py                 # Single-ticker analysis
│   ├── charts.py                  # Chart-IMG generation
│   ├── trades.py                  # Trade management (226 lines)
│   ├── risk.py                    # Risk/position sizing (268 lines)
│   ├── patterns.py                # Pattern detection
│   ├── scan.py                    # Universe scanning
│   ├── market.py                  # Market breadth/internals
│   ├── watchlist.py               # Watchlist management
│   ├── alerts.py                  # Alert system
│   ├── universe.py                # Universe management
│   ├── telegram_enhanced.py       # Telegram bot (618 lines)
│   ├── multitimeframe.py          # Multi-timeframe analysis
│   ├── dashboard.py               # Dashboard backend
│   ├── analytics.py               # Analytics endpoints
│   ├── cache_mgmt.py              # Cache management
│   ├── api_usage.py               # API usage tracking
│   ├── docs.py                    # Documentation endpoints
│   └── [other API files]          # Version, errors, metrics, etc.
│
├── services/                      # 16 service layer files
│   ├── trades.py                  # Trade management service (233 lines)
│   ├── risk_calculator.py         # Position sizing (322 lines)
│   ├── market_data.py             # Multi-source data fetching (23k lines)
│   ├── cache.py                   # Redis caching service (14.5k lines)
│   ├── multi_tier_cache.py        # Advanced caching strategy (21k lines)
│   ├── charting.py                # Chart-IMG integration (20k lines)
│   ├── database.py                # Database operations (18k lines)
│   ├── scanner.py                 # Universe scanning service
│   ├── pattern_scanner.py         # Pattern scanning logic
│   ├── alerts.py                  # Alert monitoring
│   ├── api_clients.py             # External API clients
│   ├── universe.py                # Universe management
│   ├── universe_store.py          # In-memory cache for universe
│   └── [other services]           # Multitimeframe, universe_data
│
├── core/                          # Business logic & algorithms
│   ├── pattern_detector.py        # Minervini pattern detection
│   ├── pattern_detector_v2.py     # V2 pattern detector
│   ├── classifiers.py             # Trend classification
│   ├── indicators.py              # Technical indicators (SMA, EMA, RSI, ATR, etc.)
│   ├── metrics.py                 # Technical metrics
│   ├── detector_base.py           # Base detector class
│   ├── detector_registry.py       # Detector plugin system
│   ├── detector_config.py         # Detector configuration
│   ├── chart_generator.py         # Chart rendering
│   ├── error_recovery.py          # Error handling
│   ├── flags.py                   # Feature flags
│   └── detectors/                 # Pattern detector implementations
│       ├── vcp_detector.py        # VCP pattern
│       ├── cup_handle_detector.py # Cup & Handle pattern
│       ├── channel_detector.py    # Channel pattern
│       ├── triangle_detector.py   # Triangle pattern
│       ├── wedge_detector.py      # Wedge pattern
│       ├── double_top_bottom_detector.py
│       ├── head_shoulders_detector.py
│       └── sma50_pullback_detector.py
│
├── infra/                         # Infrastructure layer
│   ├── chartimg.py                # Chart-IMG API wrapper
│   └── symbols.py                 # Symbol formatting utilities
│
├── middleware/                    # HTTP middleware
│   ├── metrics_middleware.py      # Prometheus metrics collection
│   ├── rate_limit.py              # Rate limiting (60 req/min)
│   └── structured_logging.py      # Telemetry/structured logging
│
├── routers/                       # Additional routers
│   ├── ai_chat.py                 # AI chat endpoint
│   └── advanced_analysis.py       # Advanced analysis endpoints
│
├── technicals/                    # Technical analysis utilities
│   ├── fibonacci.py               # Fibonacci analysis
│   └── trendlines.py              # Trendline drawing
│
└── telemetry/                     # Monitoring & metrics
    ├── metrics.py                 # Prometheus metrics definitions
    ├── monitoring.py              # Health monitoring
    └── alerter.py                 # Alert system
```

---

## PART 2: EXISTING PORTFOLIO/TRADING RELATED CODE

### 2.1 Trade Management System (`app/services/trades.py`)

**Trade Dataclass** (lines 17-36):
```python
@dataclass
class Trade:
    trade_id: str                  # Unique ID (UUID prefix)
    ticker: str                    # Stock symbol
    entry_price: float             # Entry price per share
    stop_loss: float               # Stop loss price
    target_price: float            # Take profit target
    position_size: int             # Number of shares
    risk_amount: float             # $ risk on trade
    reward_amount: float           # $ reward potential
    status: str                    # "open" or "closed"
    entry_date: str                # ISO format datetime
    
    # Exit information (populated on close)
    exit_date: Optional[str]       # When trade exited
    exit_price: Optional[float]    # Exit price per share
    profit_loss: Optional[float]   # $ P&L
    profit_loss_pct: Optional[float] # % return
    win: Optional[bool]            # Profitable or not
    r_multiple: Optional[float]    # Reward/risk multiple
    notes: Optional[str]           # Trade notes
```

**TradeManager Service** (lines 40-232):
- `create_trade()` - Create new trade entry, store in Redis
- `close_trade()` - Close trade, calculate P&L metrics
- `get_open_trades()` - Retrieve all open positions
- `get_closed_trades(limit)` - Get closed trades history
- `get_statistics()` - Calculate performance metrics:
  - Win rate, profit factor, expectancy
  - Average win/loss
  - Total P&L
  - Risk/reward analysis

**Storage**: Redis with 30-day TTL per trade

### 2.2 Trade API Endpoints (`app/api/trades.py`)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/trades/create` | POST | Create new trade |
| `/api/trades/close` | POST | Close trade with exit price |
| `/api/trades/open` | GET | List all open trades |
| `/api/trades/closed` | GET | List closed trades (paginated) |
| `/api/trades/statistics` | GET | Trading performance stats |
| `/api/trades/health` | GET | Service health check |

### 2.3 Position Sizing & Risk Management

**RiskCalculator Service** (`app/services/risk_calculator.py`):

```python
class PositionSize:
    account_size: float
    risk_per_trade: float          # 2% of account
    entry_price: float
    stop_loss_price: float
    target_price: float
    
    # Calculated
    risk_distance: float           # Entry to stop
    reward_distance: float         # Entry to target
    position_size: int             # Shares to trade
    position_size_dollars: float   # Dollar amount
    risk_reward_ratio: float       # Reward/Risk ratio
    
    # Advanced calculations
    kelly_position_size: Optional[int]      # Kelly Criterion
    conservative_position_size: Optional[int]
    aggressive_position_size: Optional[int]
```

**Methods**:
- `calculate_position_size()` - 2% rule, Kelly Criterion sizing
- `_kelly_criterion()` - Optimal position sizing based on win rate
- `calculate_break_even_points()` - Account for commissions
- `calculate_account_recovery()` - Recovery from losses analysis

**Risk API** (`app/api/risk.py`):
- `/api/risk/calculate-position` - POST position sizing
- `/api/risk/calculate-breakeven` - POST breakeven analysis
- `/api/risk/calculate-recovery` - POST recovery analysis
- `/api/risk/health` - GET health check

---

## PART 3: DATA MODELS FOR TRADES, POSITIONS, AND SECURITIES

### 3.1 SQLAlchemy Database Models (`app/models.py`)

**Ticker Model**:
```python
class Ticker(Base):
    __tablename__ = "tickers"
    id: Integer (PK)
    symbol: String(10, unique, indexed)
    name: String(255)
    sector: String(100)
    industry: String(100)
    exchange: String(20)
    created_at, updated_at: DateTime
```

**PatternScan Model**:
```python
class PatternScan(Base):
    __tablename__ = "pattern_scans"
    id: Integer (PK)
    ticker_id: Integer (FK -> Ticker)
    pattern_type: String(50)      # VCP, Cup & Handle, etc.
    score: Float                  # 0-10 confidence
    entry_price, stop_price, target_price: Float
    risk_reward_ratio: Float
    criteria_met: Text (JSON)
    analysis: Text
    current_price: Float
    volume_dry_up: Boolean
    consolidation_days: Integer
    chart_url: Text
    rs_rating: Float
    scanned_at: DateTime (indexed)
```

**Watchlist Model**:
```python
class Watchlist(Base):
    __tablename__ = "watchlists"
    id: Integer (PK)
    user_id: String(100, indexed)
    ticker_id: Integer (FK -> Ticker)
    status: String(50, indexed)  # Watching, Breaking Out, Triggered, etc.
    target_entry, target_stop, target_price: Float
    reason, notes: Text
    alerts_enabled: Boolean
    alert_threshold: Float
    added_at, triggered_at, updated_at: DateTime
```

**AlertLog Model**:
```python
class AlertLog(Base):
    __tablename__ = "alert_logs"
    id: Integer (PK)
    ticker_id: Integer (FK -> Ticker)
    alert_type: String(50, indexed)  # price, pattern, breakout, volume
    trigger_price, trigger_value: Float
    alert_sent_at: DateTime (indexed)
    sent_via: String(50)          # telegram, email, push
    user_id: String(100, indexed)
    status: String(20)            # sent, failed, acknowledged
```

**ScanLog & UniverseScan Models**:
- Track scanning operations and results
- Useful for audit trails and performance monitoring

### 3.2 In-Memory Cache Structures

**Redis Storage** (`app/services/trades.py`):
- `trade:{trade_id}` - Individual trade JSON
- `trades:open` - List of open trade IDs
- `trades:closed` - List of closed trade IDs
- TTL: 30 days per trade

**Universe Store** (`app/services/universe_store.py`):
- Maintains in-memory S&P 500, NASDAQ 100 listings
- Keys: ticker symbols
- Values: Symbol metadata (name, sector, industry, exchange)

---

## PART 4: EXISTING TAX-RELATED FUNCTIONALITY

### 4.1 Current Tax-Related Code
**Result**: NO existing tax-related code found in the codebase.

**Search Results**:
- No `cost_basis` tracking
- No `holding_period` calculations (short-term vs long-term)
- No `capital_gains` computation
- No `tax_lot` management
- No wash sale detection
- No tax harvesting logic
- No tax reports or exports

### 4.2 Documentation References
- ENHANCEMENT_ROADMAP.md mentions "Tax optimization" as a future goal
- No dedicated tax optimization module or documentation
- Tax system is a greenfield opportunity

---

## PART 5: TESTING STRUCTURE & PATTERNS

### 5.1 Test Files Organization

```
tests/
├── test_smoke.py                 # Basic health checks
├── test_api_integration.py       # API endpoint tests
├── test_pattern_detection.py     # Pattern detector tests
├── test_pattern_detectors.py     # Individual detector tests
├── test_scanner_service.py       # Scanner service tests
├── test_market_data.py           # Market data fetching tests
├── test_analyze_contract.py      # Analysis endpoint tests
├── test_charting.py              # Chart generation tests
├── test_indicators.py            # Technical indicators tests
├── test_all_detectors_unit.py    # All detector unit tests
├── test_performance_benchmarks.py # Performance tests
├── test_scan_endpoints.py        # Scan API endpoint tests
├── test_universe_api.py          # Universe API tests
├── test_watchlist_api.py         # Watchlist API tests
├── test_market_internals.py      # Market internals tests
├── test_vcp_detector.py          # VCP-specific tests
├── test_patterns.py              # Pattern tests
├── test_scan_contract.py         # Scan contract tests
└── test_production.py            # Production integration tests
```

### 5.2 Testing Patterns

**Pytest Configuration** (`pytest.ini`):
```ini
[pytest]
testpaths = tests
addopts =
    --basetemp .pytest_tmp
    --cov=app                      # Coverage on app module
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-report=json:coverage.json
    --strict-markers
    -v

markers =
    asyncio                        # Async tests
    benchmark                      # Performance tests
    slow                           # Long-running tests
    integration                    # Integration tests
    unit                           # Unit tests
```

**Common Testing Patterns**:

1. **Fixture-Based Testing** (`test_smoke.py`):
```python
@pytest.fixture
def client():
    # Setup test client with stubbed cache
    import app.services.universe_store as uni_mod
    uni_mod.universe_store.cache = _StubCache()
    
    with TestClient(main.app) as test_client:
        yield test_client

def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
```

2. **Mocking & Monkeypatching** (`test_api_integration.py`):
```python
@patch("app.api.patterns.market_data_service")
@patch("app.api.patterns.detector_registry")
def test_detect_patterns_endpoint(mock_registry, mock_market_service, client):
    mock_market_service.fetch_data = AsyncMock(return_value=mock_data)
    mock_detector = MagicMock()
    mock_detector.find.return_value = []
    # Test assertions...
```

3. **Async Testing** (`test_scanner_service.py`):
```python
@pytest.mark.asyncio
async def test_scanner_service_preserves_missing_data(monkeypatch):
    async def fake_get_all():
        return {"AAA": {...}, "MISS": {...}}
    
    monkeypatch.setattr(universe_store, "get_all", fake_get_all)
    # Test assertions...
```

4. **Data Fixtures**:
```python
@pytest.fixture
def mock_market_data():
    dates = pd.date_range("2024-01-01", periods=100, freq="D")
    return pd.DataFrame({
        "datetime": dates,
        "open": np.linspace(100, 150, 100),
        "high": np.linspace(101, 151, 100),
        "low": np.linspace(99, 149, 100),
        "close": np.linspace(100, 150, 100),
        "volume": np.full(100, 1_000_000),
    })
```

---

## PART 6: COMPREHENSIVE INTEGRATION ARCHITECTURE

### 6.1 Recommended Tax Optimization System Structure

```
app/
├── api/
│   └── tax_optimization.py       # NEW: Tax API endpoints
│       ├── POST /api/tax/calculate-gains
│       ├── POST /api/tax/detect-wash-sales
│       ├── POST /api/tax/harvest-losses
│       ├── POST /api/tax/estimate-impact
│       ├── POST /api/tax/rebalance-efficiently
│       └── GET /api/tax/report
│
├── services/
│   └── tax_optimizer.py          # NEW: Tax optimization service
│       ├── TaxOptimizer class
│       ├── CapitalGainsCalculator
│       ├── WashSaleDetector
│       ├── TaxHarvester
│       ├── PortfolioRebalancer
│       └── TaxReportGenerator
│
├── core/
│   └── tax_models.py             # NEW: Tax calculation logic
│       ├── CapitalGainType enum (ST/LT)
│       ├── TaxLotResult dataclass
│       ├── WashSaleMatch dataclass
│       ├── TaxStrategy enum
│       └── Tax calculation methods
│
└── models.py                     # EXTEND: Database models
    ├── Add Position table
    ├── Add TaxLot table
    ├── Add CapitalGain table
    └── Add TaxHarvestLog table
```

### 6.2 Required Data Models (to extend `app/models.py`)

**Position Model** (NEW):
```python
class Position(Base):
    __tablename__ = "positions"
    id: Integer (PK)
    user_id: String(100, indexed)
    ticker_id: Integer (FK -> Ticker)
    quantity: Integer              # Current shares held
    current_price: Float           # Latest market price
    current_value: Float           # quantity * current_price
    opened_at: DateTime (indexed)  # When first purchased
    updated_at: DateTime
    metadata: Text (JSON)          # Additional info
```

**TaxLot Model** (NEW):
```python
class TaxLot(Base):
    __tablename__ = "tax_lots"
    id: Integer (PK)
    position_id: Integer (FK -> Position)
    acquisition_date: Date (indexed)
    quantity: Integer              # Shares in this lot
    cost_basis_per_share: Float
    total_cost_basis: Float
    long_term: Boolean (computed)  # 365+ days
    status: String(50)             # active, partial_sold, closed
    sold_on: Date
    capital_gain: Float (computed)
    tax_impact: Float (computed)
    created_at: DateTime
```

**CapitalGain Model** (NEW):
```python
class CapitalGain(Base):
    __tablename__ = "capital_gains"
    id: Integer (PK)
    tax_lot_id: Integer (FK -> TaxLot)
    ticker: String(10, indexed)
    quantity: Integer
    acquisition_date: Date
    disposition_date: Date
    cost_basis: Float
    sale_proceeds: Float
    gain_loss: Float              # sale_proceeds - cost_basis
    holding_days: Integer
    is_long_term: Boolean
    gain_type: String(20)         # "long_term", "short_term"
    strategy: String(50)          # "harvest", "rebalance", etc.
    notes: Text
    created_at: DateTime (indexed)
```

**TaxHarvestLog Model** (NEW):
```python
class TaxHarvestLog(Base):
    __tablename__ = "tax_harvest_logs"
    id: Integer (PK)
    user_id: String(100, indexed)
    strategy: String(50)          # Strategy applied
    original_holding: String(10)  # Original position (ticker)
    replacement_holding: String(10) # Replacement position (ticker)
    loss_harvested: Float         # Tax loss realized ($)
    estimated_tax_savings: Float  # At estimated tax rate
    execution_date: DateTime
    notes: Text
```

### 6.3 Service Layer Architecture

**TaxOptimizer Service** Structure:

```python
class TaxOptimizer:
    """Main tax optimization service"""
    
    def __init__(self):
        self.capital_gains_calc = CapitalGainsCalculator()
        self.wash_sale_detector = WashSaleDetector()
        self.tax_harvester = TaxHarvester()
        self.rebalancer = PortfolioRebalancer()
        self.report_gen = TaxReportGenerator()
    
    # Core Methods
    async def calculate_capital_gains(trades: List[Trade]) -> Dict
    async def detect_wash_sales(trades: List[Trade]) -> List[WashSaleMatch]
    async def identify_harvest_opportunities(portfolio: Dict) -> List[HarvestOption]
    async def estimate_tax_impact(transaction: Trade, tax_rate: float) -> TaxImpact
    async def rebalance_efficiently(portfolio: Dict, target_allocation: Dict) -> RebalanceResult
    async def generate_tax_report(date_range: Tuple[Date, Date]) -> TaxReport
```

### 6.4 API Endpoint Design

```
Tax Optimization API Routes:

POST /api/tax/calculate-gains
├── Body: list of closed trades
├── Response: capital gains broken down by type (ST/LT)

POST /api/tax/detect-wash-sales
├── Body: list of trades and current date
├── Response: wash sale violations with replacement requirements

POST /api/tax/harvest-losses
├── Body: portfolio snapshot + tax rate + strategy
├── Response: harvest recommendations with tax savings estimate

POST /api/tax/estimate-impact
├── Body: proposed trade + current holdings
├── Response: tax impact analysis before execution

POST /api/tax/rebalance-efficiently
├── Body: current portfolio + target allocation
├── Response: rebalancing trades with tax optimization

GET /api/tax/report
├── Query: date_range, format (PDF/JSON/CSV)
├── Response: comprehensive tax report

GET /api/tax/positions
├── Response: all tracked positions with cost basis and tax status

GET /api/tax/summary
├── Response: YTD gains/losses, estimated tax liability
```

---

## PART 7: INTEGRATION POINTS & DATA FLOW

### 7.1 Integration with Existing Trade System

**Current Trade Flow**:
```
User Creates Trade (API)
    ↓
TradeManager.create_trade()
    ↓
Trade stored in Redis
    ↓
User Closes Trade (API)
    ↓
TradeManager.close_trade()
    ↓
P&L calculated
    ↓
Statistics updated
```

**Enhanced Tax-Aware Flow**:
```
User Creates Trade (API)
    ↓
TradeManager.create_trade()
    ↓
Trade stored in Redis
    ↓
[NEW] TaxOptimizer monitors trade
    ↓
[NEW] Wash sale check (if short position)
    ↓
[NEW] Create TaxLot record in DB
    ↓
User Closes Trade (API)
    ↓
TradeManager.close_trade()
    ↓
P&L calculated
    ↓
[NEW] TaxOptimizer.process_sale()
    ↓
[NEW] Calculate capital gain/loss
    ↓
[NEW] Record in CapitalGain table
    ↓
[NEW] Check harvest opportunities
    ↓
Statistics updated (including tax impact)
```

### 7.2 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    User/Frontend                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
  /api/trades      /api/risk      /api/tax (NEW)
   (create,        (position      (harvest,
    close,         sizing,        wash-sale,
    stats)         kelly)         gains, etc.)
        │              │              │
        └──────────────┼──────────────┘
                       ▼
          ┌────────────────────────┐
          │   Services Layer       │
          ├────────────────────────┤
          │ TradeManager           │
          │ RiskCalculator         │
          │ TaxOptimizer (NEW)     │◄── New Service
          │ MarketDataService      │
          │ CacheService           │
          └────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    ┌────────┐   ┌──────────┐   ┌──────────┐
    │ Redis  │   │Database  │   │Market    │
    │ Cache  │   │(Models)  │   │Data API  │
    └────────┘   └──────────┘   └──────────┘
                       │
                ┌──────┴──────┐
                │             │
                ▼             ▼
            ┌────────┐   ┌────────┐
            │Trades  │   │Tax Lots│ (NEW)
            │Watchl. │   │Gains   │ (NEW)
            │Tickers │   │Harvest │ (NEW)
            └────────┘   └────────┘
```

### 7.3 Integration Dependencies

**Required Extensions**:
1. **app/models.py**: Add Position, TaxLot, CapitalGain, TaxHarvestLog tables
2. **app/services/trades.py**: Extend Trade class with tax fields
3. **app/main.py**: Register new tax_optimization router
4. **app/config.py**: Add tax-related settings (tax rates, wash sale rules)
5. **app/middleware/structured_logging.py**: Log tax decisions for audit

**New Dependencies** (if not in requirements.txt):
- `python-dateutil` (for holding period calculations)
- `numpy` (already included) - for gain/loss calculations
- `pandas` (already included) - for portfolio analysis

---

## PART 8: KEY CODE EXAMPLES & PATTERNS

### 8.1 Service Singleton Pattern (used throughout)

```python
# Pattern used in trades.py, risk_calculator.py
_service_instance: Optional[ServiceClass] = None

def get_service() -> ServiceClass:
    global _service_instance
    if _service_instance is None:
        _service_instance = ServiceClass()
    return _service_instance

# Usage in API endpoints
service = get_service()
result = await service.some_method()
```

### 8.2 Dataclass + Async Pattern

```python
@dataclass
class Trade:
    # Fields...
    pass

class TradeManager:
    async def create_trade(...) -> Trade:
        # Create and store
        return trade
    
    async def close_trade(trade_id: str) -> Trade:
        # Retrieve, update, return
        return updated_trade
    
    async def get_statistics() -> Dict[str, Any]:
        # Calculate from multiple closed trades
        return stats_dict
```

### 8.3 Testing Pattern for Services

```python
@pytest.fixture
def client():
    with TestClient(main.app) as test_client:
        yield test_client

@patch("app.services.market_data_service")
def test_endpoint(mock_service, client):
    mock_service.fetch_data = AsyncMock(return_value=data)
    response = client.post("/api/endpoint", json={...})
    assert response.status_code == 200
```

---

## PART 9: DEPENDENCIES & TECHNOLOGY

### 9.1 Current Dependencies

```
fastapi==0.115.6                  # Web framework
uvicorn[standard]==0.32.1         # ASGI server
redis==5.2.1                      # Caching
sqlalchemy==2.0.36                # ORM
psycopg2-binary==2.9.10           # PostgreSQL adapter
alembic==1.14.0                   # Database migrations
pandas==2.2.3                     # Data processing
numpy==1.26.4                     # Numerical computing
pydantic==2.10.6                  # Data validation
pytest==8.4.2                     # Testing framework
pytest-asyncio==1.3.0             # Async test support
```

### 9.2 Additional Dependencies Recommended for Tax Module

- `python-dateutil` - Holding period calculations
- `pytz` - Timezone handling for accurate dates
- `reportlab` or `fpdf2` - PDF tax report generation (optional)

---

## PART 10: RECOMMENDED INTEGRATION ROADMAP

### Phase 1: Foundation (Week 1-2)
1. [ ] Extend `models.py` with Position, TaxLot, CapitalGain models
2. [ ] Create database migrations with Alembic
3. [ ] Implement core tax calculation classes in `core/tax_models.py`
4. [ ] Add TaxOptimizer service (`services/tax_optimizer.py`)

### Phase 2: Core Features (Week 2-3)
1. [ ] Implement capital gains calculation engine
2. [ ] Add wash sale detection logic
3. [ ] Build tax harvesting opportunity identifier
4. [ ] Implement portfolio rebalancing with tax awareness

### Phase 3: API & Integration (Week 3-4)
1. [ ] Create `/api/tax/` endpoints
2. [ ] Integrate with existing trade management
3. [ ] Add tax impact to trade creation/closing
4. [ ] Update statistics endpoints with tax data

### Phase 4: Testing & Reports (Week 4-5)
1. [ ] Write comprehensive unit tests
2. [ ] Add integration tests
3. [ ] Implement tax report generation
4. [ ] Create documentation

### Phase 5: Optimization & Deployment
1. [ ] Performance tuning
2. [ ] Add tax strategy recommendations
3. [ ] Dashboard integration
4. [ ] Production deployment

---

## CONCLUSION

The Legend AI codebase is well-structured with:
- **Clear separation of concerns** (API → Services → Core → Models)
- **Async/await throughout** for performance
- **Redis caching** for speed
- **PostgreSQL database** for persistence
- **Comprehensive testing** with pytest
- **Monitoring and telemetry** built-in

The tax optimization system should follow these same patterns and integrate cleanly with the existing trade management infrastructure, extending the Trade dataclass with tax fields and adding new services and database models to handle the complex tax calculations without disrupting current functionality.

