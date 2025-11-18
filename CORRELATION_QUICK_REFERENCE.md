# Quick Reference: Correlation Analysis Implementation

## Files to Create (3 new modules, ~1000 LOC total)

### 1. app/services/correlation_analysis.py (250-300 LOC)
```python
class CorrelationAnalysisService:
    """Service for multi-ticker correlation analysis"""
    
    async def calculate_pair_correlation(ticker1, ticker2, lookback_days=100)
    async def calculate_correlation_matrix(tickers, lookback_days=100) 
    async def get_sector_correlations(sector)
    async def detect_correlation_clusters(tickers, num_clusters=5)
```

### 2. app/api/correlation.py (300-350 LOC)
**Endpoints:**
- `POST /api/correlation/pair-analysis` - Analyze two tickers
- `POST /api/correlation/matrix` - Calculate correlation matrix
- `GET /api/correlation/sector-groups?sector=Technology` - Sector analysis
- `POST /api/correlation/cluster-analysis` - Find similar tickers
- `GET /api/watchlist/{id}/correlations` - Analyze watchlist

### 3. app/core/correlation_stats.py (200-250 LOC)
```python
def calculate_pearson_correlation(series1, series2)
def calculate_spearman_correlation(series1, series2)
def calculate_rolling_correlation(data1, data2, window=20)
def detect_correlation_breakpoints(series1, series2, threshold=2.0)
def filter_patterns_by_correlation(patterns, threshold=0.7)
```

## Integration Points

| Current Module | Enhancement | Location |
|---|---|---|
| `app/api/market.py` | Add sector correlation heatmap | Market analysis endpoints |
| `app/api/patterns.py` | Filter patterns by correlation | Pattern detection with query param |
| `app/api/watchlist.py` | Add watchlist correlation analysis | New endpoint in watchlist router |
| `app/routers/advanced_analysis.py` | Add correlation endpoints | `/api/advanced/correlation/*` |

## Existing Code to Leverage

1. **Market Data Service** (`app/services/market_data.py`)
   - Use for fetching price data
   - Already handles caching & fallback

2. **StatsHelper Class** (`app/core/detector_base.py`)
   - Kendall's τ implementation already exists
   - Can reuse volume_z_score, atr methods

3. **Caching Pattern** 
   - Follow existing Redis caching pattern
   - TTL: 1 hour for correlation results

4. **API Router Pattern**
   - Follow Pydantic request/response models
   - Use existing error handling (HTTPException)

## Implementation Checklist

### Phase 1: Core Implementation (Week 1-2)
- [ ] Create `app/core/correlation_stats.py` with base functions
- [ ] Create `app/services/correlation_analysis.py` service layer
- [ ] Implement Pearson correlation calculation
- [ ] Implement Spearman correlation calculation
- [ ] Add Redis caching for results
- [ ] Add comprehensive logging

### Phase 2: API Endpoints (Week 2-3)
- [ ] Create `app/api/correlation.py` router
- [ ] Implement `POST /api/correlation/pair-analysis` endpoint
- [ ] Implement `POST /api/correlation/matrix` endpoint
- [ ] Implement `GET /api/correlation/sector-groups` endpoint
- [ ] Add Pydantic request/response models
- [ ] Add endpoint documentation

### Phase 3: Advanced Features (Week 3)
- [ ] Implement rolling correlation
- [ ] Implement correlation breakpoint detection
- [ ] Implement clustering analysis
- [ ] Add pattern filtering by correlation
- [ ] Enhance watchlist API

### Phase 4: Testing & Documentation
- [ ] Create `tests/test_correlation_analysis.py`
- [ ] Add unit tests for all stat functions
- [ ] Add integration tests for endpoints
- [ ] Create API documentation
- [ ] Performance testing (optimize if needed)

## Key Performance Targets

| Metric | Target |
|--------|--------|
| Pair correlation (cached) | <500ms |
| Pair correlation (first calc) | <2s |
| Matrix (50 tickers) | <3s |
| Matrix (100 tickers) | <5s |
| Cache hit rate | >80% |

## Example API Requests

### Pair Analysis
```bash
curl -X POST http://localhost:8000/api/correlation/pair-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "ticker1": "AAPL",
    "ticker2": "MSFT",
    "lookback_days": 100
  }'
```

### Correlation Matrix
```bash
curl -X POST http://localhost:8000/api/correlation/matrix \
  -H "Content-Type: application/json" \
  -d '{
    "tickers": ["AAPL", "MSFT", "GOOGL", "META"],
    "lookback_days": 100
  }'
```

### Sector Groups
```bash
curl -X GET "http://localhost:8000/api/correlation/sector-groups?sector=Technology"
```

## Technology Stack (Already Available)

- pandas (2.2.3) - DataFrame operations
- numpy (1.26.4) - Numerical operations
- scipy (1.14.1) - Statistical tests
- redis (5.2.1) - Caching
- fastapi (0.115.6) - API framework
- pydantic (2.10.6) - Data validation

**NO NEW DEPENDENCIES NEEDED!**

## Testing Framework

```bash
# Run tests
pytest tests/test_correlation_analysis.py -v

# With coverage
pytest tests/test_correlation_analysis.py --cov=app.services.correlation_analysis
```

## Development Tips

1. **Use existing patterns:**
   - Copy service layer pattern from `MarketDataService`
   - Copy router pattern from `advanced_analysis.py`
   - Copy error handling from other API modules

2. **Leverage existing utilities:**
   - Use `market_data_service.get_time_series()` for data fetch
   - Use `get_cache_service()` for caching
   - Use `StatsHelper` methods from detector_base.py

3. **Performance optimization:**
   - Cache frequently requested correlations (1 hour)
   - Limit matrix size to 100 tickers max
   - Use pandas vectorized operations
   - Implement lazy evaluation where possible

4. **Error handling:**
   - Validate ticker symbols exist
   - Handle insufficient data (< 20 data points)
   - Return meaningful error messages
   - Log all failures for debugging

## Next Steps

1. Review this guide with team
2. Get approval on proposed API endpoints
3. Start Phase 1 implementation
4. Set up branch for correlation feature
5. Begin development of core modules

---

**Repository:** /home/user/legend-ai-python
**Branch:** claude/ticker-correlation-analysis-01Qtox7J8Gb3sGQxh2QoBCWR
**Created:** 2025-11-18
