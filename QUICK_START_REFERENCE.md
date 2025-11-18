# Legend AI Codebase - Quick Start Reference

## Key Findings Summary

This document provides a quick reference to understand the Legend AI architecture for implementing AI price forecasting features.

---

## At a Glance

| Aspect | Details |
|--------|---------|
| **Language** | Python 3.11+ |
| **Framework** | FastAPI (async) |
| **Database** | PostgreSQL + SQLAlchemy ORM |
| **Caching** | Redis (3-tier multi-tier cache) |
| **Code Size** | 119 Python files, ~30K lines |
| **API Endpoints** | 60+ endpoints across 23 routers |
| **ML Components** | 50+ pattern detectors, AI assistant |
| **Data Sources** | TwelveData, Finnhub, Alpha Vantage, Yahoo Finance |
| **Deployment** | Docker, Railway, Kubernetes-ready |

---

## Architecture in 60 Seconds

```
CLIENT (Gradio/HTML/Telegram)
    ↓
FASTAPI APP (23 routers, 60+ endpoints)
    ├→ Middleware (metrics, logging, rate limiting)
    └→ Services (Market Data, Pattern Scanner, Charting, AI)
        ├→ Core Logic (Detectors, Technical Analysis)
        ├→ Cache (Redis 5-15min, DB 1hr, CDN 24hr)
        └→ External APIs (TwelveData, Finnhub, Chart-IMG, etc.)
```

---

## Most Important Files for Forecasting

### 1. Data Pipeline
- **`app/services/market_data.py`** - Fetch OHLCV from 4 sources with fallback
- **`app/services/cache.py`** - Redis caching with TTL management
- **`app/services/multi_tier_cache.py`** - 3-tier cache (hot/warm/cdn)

### 2. Technical Indicators (Ready to Use)
- **`app/core/indicators.py`** - SMA, EMA, RSI, MACD, Bollinger Bands
- **`app/technicals/fibonacci.py`** - Fibonacci levels
- **`app/technicals/trendlines.py`** - Automated trendline detection

### 3. Pattern Detection (ML Foundation)
- **`app/core/pattern_detector.py`** - Main detector orchestrator (36KB)
- **`app/detectors/advanced/patterns.py`** - 50+ pattern library (63KB)
- **`app/core/detectors/`** - 8 specialized detectors

### 4. Database Models (Extend These)
- **`app/models.py`** - SQLAlchemy models
  - `Ticker` - Stock metadata
  - `PatternScan` - Pattern results
  - `Watchlist` - User tracking
  - → **Add `PricePrediction` model here**

### 5. API Routes (Follow This Pattern)
- **`app/api/patterns.py`** - Pattern detection endpoints (follow for forecasting)
- **`app/api/market.py`** - Market data endpoints
- **`app/api/analyze.py`** - Analysis endpoints

### 6. AI Services
- **`app/ai/assistant.py`** - Claude/GPT-4 integration via OpenRouter
- **`app/routers/ai_chat.py`** - Conversational AI endpoints

---

## Data Models Already in Place

### Database Schema (PostgreSQL)

```sql
-- Existing tables relevant for forecasting:

Tickers (symbol, name, sector, industry, exchange, created_at, updated_at)
  ↓ 
PatternScans (ticker_id, pattern_type, score, entry, stop, target, analysis)
  ↓
UniverseScans (scan_date, universe, total_scanned, patterns_found, status)
```

### API Data Structures

**Request/Response Pattern** (used throughout):
```python
class PredictionRequest(BaseModel):
    ticker: str
    timeframe: str
    model_type: str  # e.g., "lstm", "ensemble"

class PredictionResponse(BaseModel):
    success: bool
    data: PredictionResult
    confidence: float
    cached: bool
    processing_time: float
```

---

## Key Integration Points for Forecasting

### 1. Fetch Data (Already Implemented)
```python
from app.services.market_data import MarketDataService

market_data = MarketDataService()
ohlcv = await market_data.get_time_series("AAPL", "1day", 500)
# Returns: {c: [...], o: [...], h: [...], l: [...], v: [...], t: [...]}
```

### 2. Compute Features (Already Implemented)
```python
from app.core.indicators import calculate_indicators

indicators = calculate_indicators(closes, highs, lows, volumes)
# Returns: {sma_50: [], ema_21: [], rsi: [], macd: [], ...}
```

### 3. Cache Results
```python
from app.services.cache import get_cache_service

cache = get_cache_service()
await cache.set(f"forecast:{ticker}:{timeframe}", prediction, ttl=1800)
```

### 4. Store in Database
```python
from app.models import PricePrediction
from app.services.database import database_service

# Add to database after creating PricePrediction model
db = database_service.SessionLocal()
prediction_record = PricePrediction(
    ticker_id=ticker_id,
    prediction_type="LSTM",
    target_price=175.50,
    confidence=0.85,
    horizon_days=30
)
db.add(prediction_record)
db.commit()
```

### 5. Expose via API
```python
from fastapi import APIRouter
from app.services.market_data import MarketDataService

router = APIRouter(prefix="/api/forecast", tags=["forecast"])

@router.post("/predict")
async def predict_price(request: PredictionRequest):
    # Use MarketDataService, indicators, models
    # Return PredictionResponse
```

---

## Technical Stack for ML

### Already Available
- **pandas, numpy, scipy** - Data manipulation and calculations
- **scikit-learn** (via scipy) - Statistical functions
- **asyncio** - Async/await for background processing

### Recommended to Add
```python
# In requirements.txt, add:
tensorflow==2.x          # For LSTM models
xgboost==2.x             # For tree ensembles
joblib==1.x              # Model serialization
scikit-learn==1.x        # ML algorithms
```

---

## Testing Framework Ready

```bash
# Run tests
pytest tests/

# Run specific test
pytest tests/test_market_data.py -v

# With coverage
pytest --cov=app tests/
```

**Test files to review**:
- `tests/test_market_data.py` - Data pipeline tests
- `tests/test_pattern_detection.py` - Detector tests
- `tests/test_api_integration.py` - API endpoint tests

---

## API Endpoint Patterns

### Pattern Detection (Follow This)
```
POST /api/patterns/detect
{
    "ticker": "AAPL",
    "interval": "1day",
    "use_yahoo_fallback": true
}

Response:
{
    "success": true,
    "data": {
        "ticker": "AAPL",
        "pattern": "Cup & Handle",
        "score": 8.5,
        ...
    },
    "cached": false,
    "api_used": "twelvedata",
    "processing_time": 1.23
}
```

### Recommended Forecast Pattern
```
POST /api/forecast/predict
{
    "ticker": "AAPL",
    "timeframe": "daily",
    "model_type": "lstm",
    "horizon_days": 30
}

Response:
{
    "success": true,
    "data": {
        "ticker": "AAPL",
        "current_price": 175.00,
        "predicted_price": 185.50,
        "confidence": 0.82,
        "horizon_days": 30,
        "model_type": "lstm"
    },
    "cached": false,
    "processing_time": 2.45
}
```

---

## Directory Structure for New Features

```
app/
├── ml/                    # ← ADD THIS
│   ├── __init__.py
│   ├── price_forecaster.py      # Main forecasting logic
│   ├── feature_engineering.py   # Feature computation
│   ├── models/                  # Trained model storage
│   │   ├── lstm_model.h5
│   │   ├── ensemble_model.pkl
│   │   └── scaler.pkl
│   └── training/               # Training scripts
│       ├── train_lstm.py
│       ├── train_ensemble.py
│       └── backtest.py
│
├── api/forecast.py              # ← ADD THIS (forecasting endpoints)
│
└── models.py                    # ← EXTEND THIS
    ├── Existing models...
    └── + PricePrediction      # ← ADD THIS TABLE
```

---

## Deployment Readiness

### Environment Variables Needed
```bash
# In .env file (already has template):
OPENROUTER_API_KEY=...      # AI models
TWELVEDATA_API_KEY=...      # Market data
REDIS_URL=redis://...       # Caching
DATABASE_URL=postgresql://... # Storage
TELEGRAM_BOT_TOKEN=...      # Notifications
```

### Docker Support
- ✅ Dockerfile exists
- ✅ docker-compose.yml configured
- ✅ GitHub Actions CI/CD ready
- ✅ Railway deployment-ready

---

## Performance Characteristics

### Current Performance
| Component | Latency | Cache TTL | Notes |
|-----------|---------|-----------|-------|
| Pattern Detection | ~1-2s | 1 hour | 8+ parallel detectors |
| Market Data Fetch | ~500ms | 15 min | Multi-source fallback |
| Chart Generation | ~2-3s | 2 hours | Chart-IMG API |
| AI Analysis | ~3-5s | 30 min | Claude via OpenRouter |

### Caching Strategy
```
Hot Cache (Redis):      5-15min   → Frequently accessed data
Warm Cache (Database):  1 hour    → Pattern results
CDN Cache (Static):     24 hours  → Chart images
```

---

## Best Practices to Follow

### 1. Use Async/Await
```python
# ✅ Good
async def get_prediction(ticker: str):
    data = await market_data.get_time_series(ticker)
    
# ❌ Avoid
def get_prediction(ticker: str):
    data = market_data.get_time_series(ticker)  # Blocking!
```

### 2. Cache Results
```python
# ✅ Cache expensive computations
cache_key = f"forecast:{ticker}:{timeframe}"
cached = await cache.get(cache_key)
if not cached:
    result = compute_forecast(...)
    await cache.set(cache_key, result, ttl=1800)
```

### 3. Handle Errors Gracefully
```python
# ✅ Use existing error handling
from app.core.error_recovery import handle_api_error

try:
    data = await api_call()
except Exception as e:
    error = handle_api_error(e)
    return ErrorResponse(error)
```

### 4. Log Telemetry
```python
# ✅ Track metrics
logger.info(f"🤖 Prediction for {ticker} completed in {elapsed:.2f}s")
request.state.telemetry = {
    "event": "price_forecast",
    "symbol": ticker,
    "confidence": 0.82
}
```

---

## Implementation Checklist for Forecasting

- [ ] Create `app/ml/` directory
- [ ] Add `PricePrediction` table to `app/models.py`
- [ ] Create feature engineering module
- [ ] Train and save ML models
- [ ] Create `app/api/forecast.py` with endpoints
- [ ] Add `/api/forecast/predict` endpoint
- [ ] Add `/api/forecast/backtest` endpoint
- [ ] Implement caching for predictions
- [ ] Add database storage for predictions
- [ ] Create tests in `tests/test_forecasting.py`
- [ ] Update documentation
- [ ] Deploy and monitor

---

## Documentation Files

For deeper understanding, review:
- **`CODEBASE_ARCHITECTURE.md`** - Comprehensive architecture overview
- **`ARCHITECTURE_DIAGRAMS.txt`** - Visual architecture diagrams
- **`DATA_FLOW_ARCHITECTURE.md`** - Detailed data flow
- **`ENHANCEMENT_ROADMAP.md`** - Planned ML features
- **`docs/` folder** - 35+ documentation files

---

## Support Resources

### Key Contacts
- **Pattern Detection**: See `app/core/pattern_detector.py`
- **Market Data**: See `app/services/market_data.py`
- **Database**: See `app/services/database.py`
- **API Routes**: See `app/api/` folder

### Testing
```bash
# Run all tests
pytest tests/ -v

# Test coverage
pytest --cov=app tests/

# Specific test file
pytest tests/test_market_data.py -v -s
```

### Local Development
```bash
# Start Redis
redis-server

# Start app
uvicorn app.main:app --reload

# In another terminal, test API
curl http://localhost:8000/health
```

---

## Quick Links

| File | Purpose |
|------|---------|
| `/app/main.py` | FastAPI app entry point |
| `/app/config.py` | Settings management |
| `/app/models.py` | Database schema |
| `/requirements.txt` | Python dependencies |
| `/tests/` | Test suite |
| `/docs/` | Documentation |
| `/.env.example` | Environment template |

---

## Summary

The Legend AI codebase is **production-ready** with:
- ✅ Complete data pipeline infrastructure
- ✅ Technical indicators already computed
- ✅ Caching framework in place
- ✅ Database schema for storing results
- ✅ API routing patterns established
- ✅ Testing framework ready
- ✅ Deployment infrastructure configured

**You have all the building blocks needed to implement AI price forecasting!**

