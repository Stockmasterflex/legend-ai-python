# MTF Trading System - Quick Reference Guide

## KEY FINDINGS AT A GLANCE

### Existing MTF Support: ✓ FOUNDATION ALREADY EXISTS
- **Basic MTF Service**: `app/services/multitimeframe.py` (327 lines)
- **MTF API Endpoints**: `app/api/multitimeframe.py` (168 lines)
- **Timeframes**: 1D (50%), 1W (25%), 4H (15%), 1H (10%)
- **Confluence Scoring**: Simple average with weighting

### What's Ready to Build On

| Component | Location | Status | Quality |
|---|---|---|---|
| **Pattern Detectors** | `app/core/detectors/` | ✓ 8 detectors | Production-ready |
| **Indicators** | `app/core/indicators.py` | ✓ SMA, EMA, RSI | Basic |
| **Market Data Service** | `app/services/market_data.py` | ✓ Multi-source | Robust |
| **Trendline Detection** | `app/technicals/trendlines.py` | ✓ RANSAC-based | Advanced |
| **Fibonacci Levels** | `app/technicals/fibonacci.py` | ✓ Full support | Complete |
| **Scanner Service** | `app/services/pattern_scanner.py` | ✓ Concurrent | Fast |
| **Charting** | `app/services/charting.py` | ✓ Chart-IMG | Good |
| **Database Models** | `app/models.py` | ✓ 6 tables | Extensible |
| **Caching** | `app/services/cache.py` | ✓ Redis + DB | Multi-tier |

---

## WHERE TO BUILD NEW MTF FEATURES

### 1. NEW: MTF Indicator Module
```
📁 app/core/mtf_indicators/
├── __init__.py
├── mtf_divergence.py        # RSI/MACD divergence across TF
├── mtf_confluence.py        # Enhanced confluence scoring
├── mtf_alignment.py         # Price action alignment
└── mtf_volatility.py        # ATR volatility analysis
```
**Purpose**: Advanced MTF indicator calculations beyond basic confluence

### 2. NEW: MTF Pattern Detectors
```
📁 app/core/detectors/mtf/
├── __init__.py
├── mtf_vcp_detector.py      # VCP with multiple TF validation
├── mtf_breakout_detector.py # Breakout confluence
└── mtf_support_detector.py  # Support/resistance alignment
```
**Purpose**: Pattern detection with explicit MTF logic

### 3. EXTEND: MTF Service
```
📄 app/services/multitimeframe.py (currently 327 lines)
+ Advanced analysis methods
+ Divergence detection
+ Alignment scoring
+ Risk assessment across TF
```
**Purpose**: Business logic for MTF analysis

### 4. EXTEND: MTF API
```
📄 app/api/multitimeframe.py (currently 168 lines)
+ /analyze-divergences/{ticker}
+ /alignment-detail/{ticker}
+ /confluence-breakdown/{ticker}
+ /multi-pattern/{ticker}
```
**Purpose**: Expose MTF features as REST endpoints

### 5. EXTEND: Database Models
```
📄 app/models.py
+ MTFConfluence table
+ MTFDivergence table
+ MTFAlignment table
```
**Purpose**: Persist MTF analysis results

---

## ARCHITECTURAL INTEGRATION POINTS

```
┌─────────────────────────────────────────────┐
│        REST API Endpoints                   │
│  (app/api/multitimeframe.py - EXTEND)      │
└────────────────────┬────────────────────────┘
                     │
┌────────────────────▼────────────────────────┐
│     MTF Service Layer                       │
│  (app/services/multitimeframe.py - EXTEND)  │
└────────────────────┬────────────────────────┘
                     │
        ┌────────────┼────────────┬─────────┐
        │            │            │         │
        ▼            ▼            ▼         ▼
┌──────────────┐ ┌─────────┐ ┌──────────┐ ┌──────────┐
│MTF Indicators│ │MTF      │ │Scanner   │ │Market    │
│(NEW MODULE)  │ │Detectors│ │Service   │ │Data Svc  │
│              │ │(NEW)    │ │(EXTEND)  │ │(REUSE)   │
└──────┬───────┘ └────┬────┘ └──────────┘ └──────────┘
       │              │              
       └──────┬───────┘              
              │
        ┌─────▼─────┐
        │  Models   │
        │ (EXTEND)  │
        └───────────┘
              │
        ┌─────▼──────────┐
        │  Database      │
        │  Cache         │
        │  Files         │
        └────────────────┘
```

---

## REUSABLE UTILITIES (Don't Reinvent!)

### From `app/core/detector_base.py`
```python
StatsHelper:
  - atr()                    # Average True Range
  - volume_z_score()         # Volume analysis
  - zigzag_pivots()          # Pivot detection
  - kendall_tau()            # Trend detection

GeometryHelper:
  - fit_line_ransac()        # Line fitting
  - distance_point_to_line() # Geometry
  - convergence_percent()    # Pattern convergence
```

### From `app/technicals/`
```python
FibonacciCalculator:
  - calculate_auto_fibonacci()
  - calculate_fibonacci_for_swing()
  - Fib levels, arcs, fans, time zones

AutoTrendlineDetector:
  - detect_all_trendlines()
  - detect_channels()
  - Horizontal S/R detection
```

### From `app/core/indicators.py`
```python
- sma()
- ema()
- rsi()
- detect_rsi_divergences()
```

---

## DATA FLOW FOR NEW MTF FEATURES

### Typical MTF Analysis Request
```
1. API Request
   GET /api/multitimeframe/analyze?ticker=NVDA

2. Service Layer
   - Fetch 1D, 1W, 4H, 1H data via MarketDataService
   - Run analysis on each timeframe
   - Calculate confluence scores
   - Detect divergences (NEW)
   - Score alignment (NEW)

3. Pattern Detectors
   - Run existing 8 detectors
   - Run new MTF-aware detectors
   - Return PatternResult objects

4. Technical Analysis
   - Calculate moving averages
   - Detect trendlines
   - Calculate Fibonacci levels
   - Detect divergences

5. Response
   - Return MultiTimeframeResult
   - Include divergence details
   - Include alignment scores
   - Include recommendations
```

---

## CODE QUALITY STANDARDS TO FOLLOW

### Detector Pattern (all detectors follow this)
```python
class MyDetector(Detector):
    def __init__(self, **kwargs):
        super().__init__("my_detector", **kwargs)
        self.config = MyConfig()
        # Apply overrides
        
    def find(self, ohlcv: pd.DataFrame, 
             timeframe: str, symbol: str) -> List[PatternResult]:
        # Return list of PatternResult objects
        pass
```

### Register in `detector_registry.py`
```python
self.register("my_detector", MyDetector, 
              ["Pattern Name 1", "Pattern Name 2"])
```

### API Endpoint Pattern
```python
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/feature", tags=["feature"])

class RequestModel(BaseModel):
    ticker: str
    
class ResponseModel(BaseModel):
    success: bool
    data: dict
    
@router.post("/endpoint", response_model=ResponseModel)
async def my_endpoint(request: RequestModel):
    # Implementation
    return ResponseModel(success=True, data={})
```

### Service Pattern
```python
class MyService:
    def __init__(self):
        self.market_data = market_data_service
        
    async def analyze(self, ticker: str) -> dict:
        # Implementation
        pass

# Singleton pattern
_service: Optional[MyService] = None

def get_my_service() -> MyService:
    global _service
    if _service is None:
        _service = MyService()
    return _service
```

---

## FILE SIZE REFERENCE

| File | Lines | Purpose |
|---|---|---|
| `app/core/detectors/vcp_detector.py` | 400+ | Template for detector |
| `app/services/multitimeframe.py` | 327 | Template for service |
| `app/api/multitimeframe.py` | 168 | Template for API |
| `app/core/indicators.py` | 96 | Minimal indicator module |
| `app/technicals/fibonacci.py` | 397 | Complex technical tool |
| `app/technicals/trendlines.py` | 522 | Complex technical tool |

---

## TESTING APPROACH

### Unit Tests
- `tests/test_mtf_indicators.py` - Test new indicators
- `tests/test_mtf_detectors.py` - Test new detectors
- Follow pattern from `tests/test_all_detectors_unit.py`

### Integration Tests
- `tests/test_mtf_api.py` - Test API endpoints
- Follow pattern from `tests/test_api_integration.py`

### Performance Tests
- `tests/test_mtf_performance.py` - Benchmark MTF analysis
- Follow pattern from `tests/test_performance_benchmarks.py`

### Test Data
```python
# Use real market data from test fixtures
# See tests/conftest.py for fixtures
# Or use test_pattern_detection.py for examples
```

---

## DEPLOYMENT NOTES

- Database migrations: Use Alembic for new models
- Environment vars: Check `app/config.py` for required vars
- Caching: Automatically handled by `get_cache_service()`
- Rate limiting: Handled by middleware (60 req/min)
- CORS: Configured in `main.py`

