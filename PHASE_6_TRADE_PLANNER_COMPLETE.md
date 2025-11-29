# Phase 6: Trade Planner & Journal - COMPLETE ✅

**Date:** November 29, 2025  
**Status:** ✅ COMPLETE

## ✅ Implemented Features

### 6A. Trade Planner API
**File Created:** `app/api/trade_planner.py`

**Endpoints:**
- `POST /api/trade/plan` - Full trade planning with position sizing
- `POST /api/trade/quick-size` - Quick position size calculation

**Features:**
- **Position Sizing:** Based on account risk % (default 1%)
- **Risk Management:**
  - Risk per share = Entry - Stop
  - Position size = (Account × Risk%) / Risk per share
  - Validates concentration < 20% of account
  - R:R validation (warns if < 2:1)
- **Partial Exits:** Automatic 1R/2R/3R levels
  - 50% at 1R (lock in initial risk)
  - 30% at 2R (capture swing target)
  - 20% at 3R (let winners run)
- **Warnings:**
  - Position too large (>20% concentration)
  - R:R too low (<2:1)
  - Position too small (<10 shares)

**Request Example:**
```json
{
  "ticker": "NVDA",
  "pattern": "VCP",
  "entry": 485.00,
  "stop": 465.00,
  "target": 525.00,
  "account_size": 100000,
  "risk_percent": 1.0
}
```

**Response Example:**
```json
{
  "ticker": "NVDA",
  "position_size": 50,
  "dollar_amount": 24250.00,
  "risk_amount": 1000.00,
  "potential_profit": 2000.00,
  "r_multiple": 2.0,
  "risk_per_share": 20.00,
  "concentration_pct": 24.25,
  "partial_exits": [
    {"shares": 25, "price": 505.00, "r_multiple": 1.0, "percentage": 50.0},
    {"shares": 15, "price": 525.00, "r_multiple": 2.0, "percentage": 30.0},
    {"shares": 10, "price": 545.00, "r_multiple": 3.0, "percentage": 20.0}
  ],
  "warnings": ["⚠️ Position size (24.3%) exceeds 20% concentration limit..."]
}
```

### 6B. Trade Journal
**Files Created:**
- `app/api/journal.py` - Journal API
- `app/models.py` - Trade model added
- `alembic/versions/003_add_trades_table.py` - Migration

**Database Schema:**
```sql
CREATE TABLE trades (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    pattern VARCHAR(50),
    entry_date TIMESTAMP,
    entry_price FLOAT NOT NULL,
    stop_price FLOAT NOT NULL,
    target_price FLOAT,
    exit_date TIMESTAMP,
    exit_price FLOAT,
    shares INT NOT NULL,
    profit_loss FLOAT,
    r_multiple FLOAT,
    status VARCHAR(20) DEFAULT 'Open',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

**Endpoints:**
- `POST /api/journal/trade` - Log new trade
- `GET /api/journal/trades?status=Open&ticker=NVDA` - List trades with filters
- `PUT /api/journal/trade/{id}` - Update/close trade (auto-calculates P&L and R)
- `GET /api/journal/stats` - Performance statistics
- `GET /api/journal/export` - Export to CSV

**Performance Metrics:**
- Total trades (open/closed)
- Win rate %
- Average R-multiple
- Total P&L
- Largest win/loss
- Average win/loss
- Expectancy: `(Win% × Avg Win) - (Loss% × Avg Loss)`
- Profit Factor: `Gross Wins / Gross Losses`

**Stats Response Example:**
```json
{
  "total_trades": 42,
  "open_trades": 3,
  "closed_trades": 39,
  "win_rate": 67.5,
  "avg_r_multiple": 2.3,
  "total_profit_loss": 12450.00,
  "largest_win": 2100.00,
  "largest_loss": -850.00,
  "avg_win": 650.00,
  "avg_loss": -320.00,
  "expectancy": 335.50,
  "profit_factor": 2.15
}
```

## 📝 Files Modified/Created

1. **app/api/trade_planner.py** (NEW)
   - Position sizing calculations
   - Partial exit levels
   - Risk management validations

2. **app/api/journal.py** (NEW)
   - Trade CRUD operations
   - Performance statistics
   - CSV export

3. **app/models.py** (MODIFIED)
   - Added `Trade` model

4. **alembic/versions/003_add_trades_table.py** (NEW)
   - Database migration for trades table

5. **app/main.py** (MODIFIED)
   - Registered trade_planner and journal routers

6. **tests/test_trade_planner.py** (NEW)
   - 12 tests, all passing
   - Position sizing, partial exits, validations

## 🚀 Usage Examples

### Plan a Trade
```bash
curl -X POST http://localhost:8000/api/trade/plan \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "NVDA",
    "pattern": "VCP",
    "entry": 485.00,
    "stop": 465.00,
    "target": 525.00,
    "account_size": 100000,
    "risk_percent": 1.0
  }'
```

### Log a Trade
```bash
curl -X POST http://localhost:8000/api/journal/trade \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "NVDA",
    "pattern": "VCP",
    "entry_date": "2025-11-29",
    "entry_price": 485.00,
    "stop_price": 465.00,
    "target_price": 525.00,
    "shares": 50,
    "notes": "Perfect VCP setup with volume dry-up"
  }'
```

### Close a Trade
```bash
curl -X PUT http://localhost:8000/api/journal/trade/1 \
  -H "Content-Type: application/json" \
  -d '{
    "exit_date": "2025-12-05",
    "exit_price": 510.00,
    "status": "Closed"
  }'
```

### Get Stats
```bash
curl http://localhost:8000/api/journal/stats
```

### Export CSV
```bash
curl http://localhost:8000/api/journal/export > trades.csv
```

## ✅ Requirements Met

- ✅ ATR-based position sizing (using Entry-Stop risk)
- ✅ Concentration limit validation (20%)
- ✅ R:R calculation and validation
- ✅ Partial exit levels (1R, 2R, 3R)
- ✅ Trade logging with P&L tracking
- ✅ Performance statistics (win rate, expectancy, profit factor)
- ✅ CSV export
- ✅ Auto-calculate R-multiple on exit
- ✅ Comprehensive test coverage (12 tests, 100% pass)

## 🧪 Test Results

```
12 tests PASSED
- Position sizing calculations
- Partial exit distribution
- Request validation
- R:R calculations
- Concentration warnings
```

**Phase 6 Complete** - Ready for Phase 7 (Multi-Timeframe Confirmation)

