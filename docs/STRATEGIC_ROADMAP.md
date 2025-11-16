# Legend AI - Strategic Roadmap
## Based on GPT-4 & Gemini AI Comprehensive Audits

This document outlines the strategic roadmap for taking Legend AI from MVP to production-grade trading platform.

---

## 📋 **Issues Prioritization Matrix**

### 🔴 **Critical (Fix Immediately)**

| # | Issue | Impact | Status | ETA |
|---|-------|--------|--------|-----|
| 1 | **Rate Limiting** | Prevents API abuse, protects quota | ✅ FIXED | Complete |
| 2 | **CORS Security** | Production security risk | ✅ FIXED | Complete |
| 3 | **Chart-IMG Response Parsing** | Charts not loading | ✅ FIXED | Complete |
| 4 | **Chart Indicator Clutter** | Reduces visual clarity | ✅ FIXED | Complete |
| 5 | **Health Check Diagnostics** | Better observability | ✅ FIXED | Complete |

### 🟡 **High Priority (Next 7 Days)**

| # | Issue | Impact | Status | ETA |
|---|-------|--------|--------|-----|
| 1 | **Data Persistence Layer** | Watchlist/scans lost on reload | 🟡 PLANNED | 3 days |
| 2 | **Concurrent API Calls** | Scanning is too slow (10-15s) | 🟡 PLANNED | 2 days |
| 3 | **Cache Optimization** | Reduce API costs, improve speed | 🟡 PLANNED | 2 days |
| 4 | **Loading States** | Better UX feedback | ✅ FIXED | Complete |

### 🟢 **Medium Priority (Next 30 Days)**

| # | Feature | Impact | Status | ETA |
|---|---------|--------|--------|-----|
| 1 | **Multi-Timeframe Analysis** | Better trade confluence | 🟢 PLANNED | 14 days |
| 2 | **RS Ranking System** | IBD-style relative strength | 🟢 PLANNED | 7 days |
| 3 | **Alert Engine** | Real-time breakout notifications | 🟢 PLANNED | 14 days |
| 4 | **Pattern Testing** | 95%+ test coverage goal | 🟢 IN PROGRESS | 21 days |
| 5 | **Code Refactoring** | Break large functions | 🟢 ONGOING | 30 days |

### 🔵 **Future Enhancements (Phase 2-4)**

| # | Feature | Impact | Status | ETA |
|---|---------|--------|--------|-----|
| 1 | **Trade Journal** | Track performance, analytics | 🔵 ROADMAP | Phase 3 |
| 2 | **Backtesting Module** | Validate pattern performance | 🔵 ROADMAP | Phase 3 |
| 3 | **Multi-User Support** | User authentication & isolation | 🔵 ROADMAP | Phase 3 |
| 4 | **Interactive Charts** | Plotly/D3.js drill-down | 🔵 ROADMAP | Phase 4 |
| 5 | **Sector Rotation Views** | Market-wide analysis | 🔵 ROADMAP | Phase 4 |

---

## 🛠 **Technical Implementation Plan**

### **Week 1: Persistence & Performance**

#### 1. Data Persistence Layer
**Goal:** Watchlist and scans persist across sessions

**Implementation:**
- **Option A:** Redis-based persistence (quick win)
  ```python
  # Use existing Redis for watchlist storage
  # Key: user:watchlist:{user_id}
  # Value: JSON serialized watchlist items
  ```
- **Option B:** PostgreSQL (full solution)
  ```python
  # SQLAlchemy models for:
  # - Watchlist items
  # - Scan results
  # - User settings
  # - Trade journal (future)
  ```

**Recommendation:** Start with Redis (1 day), migrate to PostgreSQL later (Phase 3)

**Files to modify:**
- `app/api/watchlist.py` - Add Redis persistence
- `app/services/cache.py` - Extend for watchlist storage
- Create: `app/models/watchlist.py` - Data models

#### 2. Concurrent API Scanning
**Goal:** Reduce scan time from 10-15s to <3s

**Current Problem:**
```python
# app/api/scan.py - Serial execution
for ticker in tickers:
    result = await scan_single_ticker(ticker)  # Slow!
```

**Solution:**
```python
# Concurrent execution with asyncio.gather
tasks = [scan_single_ticker(ticker) for ticker in tickers]
results = await asyncio.gather(*tasks, return_exceptions=True)
```

**Additional Optimizations:**
- Batch API calls where possible
- Use connection pooling for market data APIs
- Add progress tracking via Server-Sent Events (SSE)

**Files to modify:**
- `app/api/scan.py` - Implement concurrent scanning
- `app/services/market_data.py` - Add connection pooling
- Create: `app/api/scan_progress.py` - SSE endpoint

#### 3. Cache Instrumentation & Optimization
**Goal:** 80%+ cache hit rate, reduce API costs

**Implementation:**
```python
# New endpoint: /api/cache/stats
{
  "cache_hit_rate": 0.85,
  "total_requests": 1000,
  "cache_hits": 850,
  "cache_misses": 150,
  "by_provider": {
    "twelvedata": {"hits": 300, "misses": 50},
    "finnhub": {"hits": 250, "misses": 50},
    "chartimg": {"hits": 300, "misses": 50}
  }
}
```

**TTL Optimization:**
```python
# Current: Generic TTL
# Problem: Intraday data cached too long, EOD data expired too soon

# Solution: Smart TTLs
TTL_CONFIG = {
    "price_intraday": 60,      # 1 minute
    "price_eod": 3600,          # 1 hour
    "pattern_result": 3600,     # 1 hour
    "chart_image": 86400,       # 24 hours
    "company_profile": 604800,  # 7 days
}
```

**Files to create:**
- `app/api/cache_stats.py` - Cache metrics endpoint
- `app/services/cache_metrics.py` - Instrumentation

**Files to modify:**
- `app/services/cache.py` - Smart TTL system

---

### **Week 2-4: Features & Quality**

#### 4. Multi-Timeframe Confirmation
**Goal:** Detect patterns across multiple timeframes for higher confidence

**Implementation:**
```python
# New: Multi-TF pattern scoring
{
  "ticker": "AAPL",
  "pattern": "VCP",
  "daily": {"detected": true, "confidence": 0.85},
  "weekly": {"detected": true, "confidence": 0.90},
  "hourly": {"detected": false},
  "confluence_score": 0.88  # (0.85 + 0.90) / 2
}
```

**Files to create:**
- `app/core/multi_timeframe.py` - Confluence logic

**Files to modify:**
- `app/api/analyze.py` - Add multi-TF analysis option

#### 5. Relative Strength (RS) Ranking
**Goal:** IBD-style RS rating (1-99)

**Implementation:**
```python
def calculate_rs_rating(ticker_returns: list, spy_returns: list) -> int:
    """
    Calculate 12-month RS with 3-month weight (IBD methodology)
    Returns: 1-99 rating (99 = strongest)
    """
    # Weight recent performance more heavily
    # Compare to S&P 500 (SPY)
    # Percentile rank against universe
```

**Files to create:**
- `app/core/relative_strength.py` - RS calculation
- `app/api/rs_ranking.py` - RS endpoint

#### 6. Alert Engine
**Goal:** Real-time notifications for breakouts/patterns

**Implementation:**
```python
# Alert triggers:
# - Price breaks above pivot
# - Volume surge (>1.5x avg)
# - Pattern detection (VCP, Flat Base)

# Delivery:
# - Telegram (already configured)
# - Email (SendGrid)
# - Web push notifications
```

**Files to create:**
- `app/services/alert_engine.py` - Alert logic
- `app/api/alerts.py` - Alert management
- `app/jobs/alert_monitor.py` - Background task

#### 7. Test Coverage Expansion
**Goal:** 95% coverage on core modules

**Priority Tests:**
1. **Pattern Detection** - Edge cases for VCP, Cup & Handle
2. **Market Data Fallback** - Sequential provider testing
3. **Trade Planner** - Risk calculation validation
4. **Cache Service** - TTL and eviction logic

**Files to create:**
- `tests/core/test_pattern_detector_v2.py`
- `tests/services/test_market_data_fallback.py`
- `tests/core/test_trade_planner.py`
- `tests/services/test_cache_service.py`

---

## 📊 **Success Metrics**

### Performance Targets

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Scan time (50 tickers) | 10-15s | <3s | 🟡 |
| Cache hit rate | Unknown | >80% | 🟡 |
| API cost per scan | Unknown | <$0.01 | 🟡 |
| Dashboard load time | <2s | <1s | ✅ |

### Quality Targets

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Test coverage | ~20% | >95% | 🟡 |
| Code complexity (avg) | High | Medium | 🟡 |
| Security score | B | A+ | 🟢 |
| API response time (p95) | Unknown | <500ms | 🟡 |

---

## 🚀 **Deployment Strategy**

### Phase 1 (Week 1): Quick Wins ✅
- [x] Rate limiting
- [x] CORS security
- [x] Chart indicator simplification
- [x] Enhanced health checks
- [x] Chart-IMG response parsing fix

### Phase 2 (Week 2): Performance
- [ ] Redis persistence for watchlist
- [ ] Concurrent API scanning
- [ ] Cache instrumentation
- [ ] Loading states improvements

### Phase 3 (Weeks 3-4): Features
- [ ] Multi-timeframe analysis
- [ ] RS ranking system
- [ ] Alert engine MVP
- [ ] Pattern test coverage >70%

### Phase 4 (Month 2+): Scale
- [ ] PostgreSQL migration
- [ ] Multi-user support
- [ ] Trade journal
- [ ] Backtesting module
- [ ] Load testing & monitoring

---

## 🎯 **Next Actions (Priority Order)**

1. **Set Chart-IMG API Key** (5 min) - Already provided in setup guide
2. **Implement Redis Persistence** (1 day) - Watchlist storage
3. **Add Concurrent Scanning** (2 days) - Speed up pattern detection
4. **Cache Metrics Endpoint** (1 day) - Track hit rate and costs
5. **Multi-TF Analysis** (3 days) - Better pattern confirmation
6. **RS Ranking System** (2 days) - IBD-style filtering
7. **Alert Engine MVP** (3 days) - Telegram breakout alerts

---

## 📚 **Resources & References**

### Architecture Decisions
- **Persistence:** Start with Redis (fast), migrate to PostgreSQL (scalable)
- **Concurrency:** asyncio.gather for I/O-bound operations
- **Caching:** Smart TTLs based on data type, not blanket TTL
- **Testing:** pytest with async support, aim for edge cases

### Dependencies to Add
```txt
# requirements.txt additions
slowapi==0.1.9           # Rate limiting (alternative to custom)
sse-starlette==1.8.2     # Server-sent events for progress
plotly==5.18.0           # Interactive charts (Phase 4)
```

### Key References
- [IBD RS Rating Methodology](https://www.investors.com/how-to-invest/investors-corner/relative-strength-rating-stock-chart-analysis-helps-pick-outstanding-growth-stocks/)
- [FastAPI Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- [Redis Sorted Sets for Rate Limiting](https://redis.io/docs/data-types/sorted-sets/)

---

**Last Updated:** 2025-01-16
**Status:** Active Development
**Next Review:** 2025-01-23
