# Legend AI Trading System - Architecture Diagrams

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Telegram Bot │ Gradio Dashboard │ HTML Templates       │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/WebSocket
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              FASTAPI APPLICATION (app/main.py)              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         MIDDLEWARE LAYER (3 layers)                 │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌────────────┐  │   │
│  │  │ MetricsM'ware│ │ StructuredLog│ │ RateLimit  │  │   │
│  │  │(Prometheus)  │ │(Structured)  │ │(60 req/min)│  │   │
│  │  └──────────────┘ └──────────────┘ └────────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                  │
│                           ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    API ROUTER LAYER (24 Routers, 60+ Endpoints)    │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │ PATTERN DETECTION ROUTERS                    │  │   │
│  │  │ • /api/patterns/detect                       │  │   │
│  │  │ • /api/scan (universe scanning)              │  │   │
│  │  │ • /api/charts (chart generation)             │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │ TRADING ROUTERS (NEW EXECUTION WILL GO HERE) │  │   │
│  │  │ • /api/trades (trade management)             │  │   │
│  │  │ • /api/trade/plan (position planning)        │  │   │
│  │  │ • /api/risk (risk calculator)                │  │   │
│  │  │ • /api/execution/* (NEW - order execution)   │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │ MONITORING ROUTERS                           │  │   │
│  │  │ • /api/alerts (alert management)             │  │   │
│  │  │ • /api/watchlist (watchlist CRUD)            │  │   │
│  │  │ • /api/metrics (system metrics)              │  │   │
│  │  │ • /api/telegram (telegram webhook)           │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                  │
│                           ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │    SERVICE LAYER (Business Logic)                  │   │
│  │  ┌──────────────┬──────────────┬────────────────┐  │   │
│  │  │ TradeManager │RiskCalculator│MarketDataSvc  │  │   │
│  │  │(manual)      │(2%, Kelly)   │(multi-source) │  │   │
│  │  └──────────────┴──────────────┴────────────────┘  │   │
│  │  ┌──────────────┬──────────────┬────────────────┐  │   │
│  │  │ AlertService │ScannerService│ChartingService │  │   │
│  │  │(Telegram,EM) │(VCP pattern) │(Chart-IMG)    │  │   │
│  │  └──────────────┴──────────────┴────────────────┘  │   │
│  │  ┌──────────────┬──────────────┐                   │   │
│  │  │MonitoringSvc │CacheWarmer   │                   │   │
│  │  │(Prometheus)  │(Redis warm)  │                   │   │
│  │  └──────────────┴──────────────┘                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                  │
│                           ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │   PATTERN DETECTION LAYER (7 Detectors)            │   │
│  │  VCP │ Cup&Handle │ Triangle │ Wedge │ Dual TB      │   │
│  │  HeadShoulders │ Channel                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                  │
└───────────┬──────────────┬┴──────────────┬─────────────────┘
            │              │               │
            ▼              ▼               ▼
      ┌─────────────┐ ┌──────────────┐ ┌──────────────┐
      │ CACHE LAYER │ │DATABASE LAYER│ │ API CLIENTS  │
      │  (Redis)    │ │(PostgreSQL)  │ │(Market Data) │
      └─────────────┘ └──────────────┘ └──────────────┘
```

## Data Flow: Pattern → Order → Execution

```
┌──────────────────────────────────────────────────────────────┐
│ 1. PATTERN DETECTION                                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  TwelveData API    Finnhub    AlphaVantage    Yahoo Finance  │
│       │               │             │              │         │
│       └───────────────┴─────────────┴──────────────┘         │
│                       │                                      │
│                       ▼                                      │
│              ┌─────────────────┐                            │
│              │ MarketDataService│ (Redis cache 15min)       │
│              └────────┬────────┘                            │
│                       │                                      │
│                       ▼                                      │
│        ┌──────────────────────────────┐                     │
│        │ 7 Pattern Detectors (parallel)│                    │
│        │ ├─ VCPDetector               │                    │
│        │ ├─ CupHandleDetector         │                    │
│        │ ├─ TriangleDetector          │                    │
│        │ └─ ... (4 more)              │                    │
│        └────────┬─────────────────────┘                    │
│                 │                                          │
│    ┌────────────┴────────────┐                            │
│    │                         │                            │
│    ▼ Pattern Detected        ▼ No Pattern                │
│  (score ≥ 0.75)                                          │
│    │                                                      │
│    └────→ Update Watchlist                               │
│           Send Telegram Alert                            │
│           Log to Database                                │
│                                                          │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 2. USER APPROVES → EXECUTION (NEW SYSTEM)                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Telegram: "Execute AAPL VCP pattern"                       │
│       │                                                     │
│       ▼                                                     │
│  ┌──────────────────────────────────────────┐             │
│  │ ExecutionService.submit_order()          │             │
│  │                                          │             │
│  │ ├─ Validate order vs RiskCalculator ✓    │             │
│  │ ├─ Check position limits                │             │
│  │ ├─ Verify account balance               │             │
│  │ └─ Create Order record in DB            │             │
│  └──────────────────────────────────────────┘             │
│       │                                                    │
│       ▼                                                    │
│  ┌──────────────────────────────────────────┐            │
│  │ BrokerConnector (NEW)                    │            │
│  │ ├─ AlpacaConnector (first)              │            │
│  │ ├─ TDAmeritradeConnector (future)       │            │
│  │ └─ Generic REST Connector               │            │
│  └──────────────────────────────────────────┘            │
│       │                                                   │
│       ├─→ Alpaca API: /orders (POST)                     │
│       │   Returns: { order_id, status, ... }            │
│       │                                                  │
│       ▼                                                  │
│  ┌──────────────────────────────────────────┐           │
│  │ ExecutionService.track_order()           │           │
│  │ ├─ Poll broker for order status          │           │
│  │ ├─ Create Position record                │           │
│  │ ├─ Link to Trade record                  │           │
│  │ └─ Notify user (Telegram)                │           │
│  └──────────────────────────────────────────┘           │
│       │                                                  │
└───────┼──────────────────────────────────────────────────┘
        │
┌───────┴──────────────────────────────────────────────────────┐
│ 3. BROKER EXECUTION & FILL                                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Broker Fills Order                                          │
│  Alpaca API: /orders/{order_id}                             │
│  Response: { status: "filled", fills: [...] }              │
│       │                                                     │
│       ▼                                                     │
│  ExecutionService.process_fill()                            │
│  │                                                          │
│  ├─ Create Fill record (quantity, price, time)             │
│  ├─ Update Order status to "filled"                        │
│  ├─ Update Position record                                 │
│  │   ├─ quantity, avg_cost, market_value                   │
│  │   └─ unrealized P&L                                     │
│  │                                                          │
│  ├─ Update Trade record                                    │
│  │   ├─ Link to Order/Fill                                │
│  │   ├─ Populate with actual fills                         │
│  │   └─ Track execution P&L                               │
│  │                                                          │
│  └─ Notify user                                            │
│     ├─ Telegram: "AAPL filled 100@156.23"                 │
│     ├─ Log to MonitoringService                           │
│     └─ Update TradeManager statistics                     │
│                                                            │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ 4. POSITION MANAGEMENT & CLOSING                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  User closes half position at profit:                       │
│  POST /api/execution/close?symbol=AAPL&qty=50&price=160    │
│       │                                                     │
│       ▼                                                     │
│  ExecutionService.submit_close_order()                      │
│  └─> BrokerConnector.submit_sell_order()                   │
│      └─> Alpaca API closes position                        │
│          └─> process_fill() again                          │
│              ├─ Update Position (qty: 100→50)             │
│              ├─ Calculate realized P&L                     │
│              └─ Update Trade (partial exit)               │
│                                                            │
└──────────────────────────────────────────────────────────────┘
```

## Database Schema: Current vs. New

```
CURRENT (Existing)
═════════════════════════════════════════

Ticker
├── id, symbol, name
├── sector, industry, exchange
└── created_at, updated_at

PatternScan
├── id, ticker_id, pattern_type
├── score, entry_price, stop_price, target_price
├── risk_reward_ratio, chart_url
└── scanned_at

Watchlist
├── id, user_id, ticker_id
├── status, target_entry, target_stop, target_price
├── alerts_enabled, alert_threshold
└── added_at, triggered_at


NEW (Execution System)
═════════════════════════════════════════

BrokerAccount (NEW)
├── id, user_id
├── broker_name (alpaca, td_ameritrade, etc.)
├── account_id, account_number
├── api_key_hash, refresh_token_hash
├── account_type (CASH, MARGIN, etc.)
├── buying_power, available_balance, equity
├── webhook_url, webhook_secret
└── enabled, last_synced_at

Order (NEW)
├── id, order_id (external)
├── ticker_id, trade_id (FK)
├── order_type (BUY, SELL, SHORT, COVER)
├── quantity, filled_quantity
├── limit_price, stop_price
├── status (PENDING, SUBMITTED, FILLED, PARTIAL, CANCELLED)
├── execution_strategy (MARKET, LIMIT, SMART)
├── broker_id, broker_order_id
├── commission, fees, actual_slippage
├── created_at, submitted_at, filled_at
└── audit_trail (JSON)

Position (NEW)
├── id, ticker_id, broker_account_id
├── symbol, quantity, avg_cost
├── current_price, market_value
├── unrealized_pnl, unrealized_pnl_pct
├── stop_loss_price, target_price
├── related_order_ids (JSON)
└── opened_at, updated_at

Fill (NEW)
├── id, order_id, ticker_id
├── fill_id (external)
├── quantity, fill_price, fill_time
├── commission, fees
├── exchange, execution_venue
└── broker_transaction_id

ExecutionLog (NEW)
├── id, order_id
├── event_type (CREATED, SUBMITTED, FILLED, REJECTED, etc.)
├── previous_status, new_status
├── event_details (JSON)
├── error_message, timestamp
└── event_source
```

## Service Layer Architecture

```
SERVICE LAYER (Business Logic)
═══════════════════════════════════════════════════════════

TRADING SERVICES
┌─────────────────────────────────────────────────┐
│ TradeManager                                    │
│ └─ create_trade()      (manual entry)           │
│ └─ close_trade(id, exit_price)                  │
│ └─ get_statistics()    (win rate, profit factor)│
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ RiskCalculator                                  │
│ └─ calculate_position_size()    (2% rule)       │
│ └─ _kelly_criterion()            (kelly sizing)│
│ └─ calculate_break_even_points() (commission)   │
│ └─ calculate_account_recovery()                 │
└─────────────────────────────────────────────────┘

NEW EXECUTION SERVICES (To Implement)
┌─────────────────────────────────────────────────┐
│ ExecutionService                                │
│ └─ submit_order()                               │
│ └─ cancel_order(order_id)                       │
│ └─ process_fill()                               │
│ └─ track_position()                             │
│ └─ close_position()                             │
│ └─ validate_order()                             │
│ └─ pre_flight_checks()                          │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ BrokerConnector (Abstract)                      │
│ └─ submit_order()                               │
│ └─ cancel_order()                               │
│ └─ get_order_status()                           │
│ └─ get_positions()                              │
│ └─ get_account()                                │
│ └─ _handle_auth()                               │
│                                                 │
│ Implementations:                                │
│ ├─ AlpacaConnector                             │
│ ├─ TDAmeritradeConnector                       │
│ ├─ InteractiveBrokersConnector                 │
│ └─ SchwabConnector                             │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ IntelligentExecutor                             │
│ └─ execute_vwap()           (volume weighted)   │
│ └─ execute_twap()           (time weighted)     │
│ └─ execute_iceberg()        (hidden orders)     │
│ └─ adjust_limit_price()     (dynamic pricing)   │
│ └─ minimize_slippage()                          │
│ └─ detect_market_regime()                       │
└─────────────────────────────────────────────────┘


DATA SERVICES (Existing)
┌─────────────────────────────────────────────────┐
│ MarketDataService                               │
│ └─ get_time_series()       (TwelveData→...)    │
│ └─ get_usage_stats()                            │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ ScannerService                                  │
│ └─ run_daily_vcp_scan()    (pattern detection)  │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ ChartingService                                 │
│ └─ generate_chart()        (Chart-IMG API)      │
└─────────────────────────────────────────────────┘


MONITORING SERVICES (Existing)
┌─────────────────────────────────────────────────┐
│ AlertService                                    │
│ └─ monitor_watchlist()     (Telegram, Email)    │
│ └─ _send_alerts()                               │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ MonitoringService                               │
│ └─ collect_metrics()       (Prometheus)         │
│ └─ send_telegram_alert()                        │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ DatabaseService                                 │
│ └─ All CRUD operations                          │
│ └─ Connection pooling                           │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Cache (Multi-tier)                              │
│ └─ get_cache_service()                          │
│    ├─ Redis (hot, 5-15min)                     │
│    ├─ Database (warm, 1hr)                     │
│    └─ CDN (static, 24hr)                       │
└─────────────────────────────────────────────────┘
```

## Integration Points

```
Pattern Detection System         Order Execution System
═════════════════════════════════════════════════════════

                        ↓
                  
              Pattern Score ≥ 0.75
         (VCP, Cup&Handle, Triangle, etc.)
                        │
                        ▼
              Alert User via Telegram
         (show entry, stop, target, risk:reward)
                        │
                        ▼ User clicks "Execute"
                        │
    ┌───────────────────┴───────────────────┐
    │                                       │
    ▼                                       ▼
Use RiskCalculator               Use ExecutionService
(validate position size)         (place order)
    │                                       │
    ├─ Account size check          ├─ Order validation
    ├─ Max position % check        ├─ Risk pre-check
    ├─ 2% rule enforcement         ├─ Broker submission
    │                              │
    └───────────────┬──────────────┘
                    │
                    ▼
        Use MonitoringService
        (track execution metrics)
            │
            ├─ Execution time
            ├─ Slippage
            ├─ Fill price vs entry
            │
            ▼
        Use AlertService
        (notify on fills)
            │
            ├─ Telegram: "AAPL filled 100@156.23"
            └─ Email: detailed fill report
                    │
                    ▼
        Use TradeManager
        (log for statistics)
            │
            ├─ Link Order→Trade
            ├─ Calculate P&L
            └─ Update statistics
```

## Deployment Architecture

```
PRODUCTION (Railway)
════════════════════════════════════════════

                    Internet
                        │
                        ▼
            Railway Public Domain
       (auto-detected for Telegram webhook)
                        │
            ┌───────────┴───────────┐
            │                       │
            ▼                       ▼
    ┌──────────────┐        ┌──────────────┐
    │ FastAPI App  │        │ Telegram     │
    │(Uvicorn)     │        │ Webhook      │
    └──────────────┘        └──────────────┘
            │
    ┌───────┴────────┬──────────────┐
    │                │              │
    ▼                ▼              ▼
 PostgreSQL      Redis          Broker APIs
 (database)    (cache)      (Alpaca, TD, etc.)
    │             │              │
    └─────────────┴──────────────┘
            │
            ▼
    Monitoring & Logging
    ├─ Prometheus metrics
    ├─ Structured logs
    ├─ Error alerts
    └─ Performance tracking
```

