# Market Visualization Development Roadmap

## Overview
This guide helps developers understand how to extend, enhance, or build new market visualization components for Legend AI.

---

## Part 1: Understanding Current Visualization Stack

### What Exists Today

1. **Dashboard Interface** (`/templates/dashboard.html`)
   - 5 main tabs with distinct visualizations
   - TradingView Advanced Chart widget (interactive)
   - Results grid/table views
   - Form inputs for user control

2. **Chart Generation** (`/app/services/charting.py`)
   - Server-side chart rendering via Chart-IMG API
   - Professional annotations (entry/stop/target)
   - Multiple indicator overlays
   - Rate-limited with graceful fallbacks

3. **Data Models** (`/app/core/pattern_detector.py`)
   - PatternResult dataclass with 20+ fields
   - Includes score, entry/stop/target, analysis, metadata

4. **Frontend JavaScript** (`/static/js/dashboard.js`, 80KB)
   - Handles form submission and async API calls
   - Grid rendering and tab navigation
   - Error handling and loading states
   - TradingView widget initialization

---

## Part 2: Key Entry Points for Extensions

### Pattern Detection Visualization

**Location:** `/app/core/detectors/` and `/app/detectors/advanced/`

**Extension Path:**
```python
# 1. Create new detector
class MyPatternDetector(Detector):
    def find(df: DataFrame, timeframe: str, symbol: str) -> List[PatternResult]:
        # Your pattern logic here
        return [PatternResult(...)]

# 2. Register in detector_registry.py
register_detector(MyPatternDetector())

# 3. Automatically appears in:
#    - /api/patterns/detect endpoint
#    - Dashboard results
#    - Universe scanner
```

**Example: Add a New Pattern Type**
```python
# File: /app/core/detectors/my_pattern.py
from app.core.detector_base import Detector, PatternResult

class MyPatternDetector(Detector):
    name = "My Pattern"
    
    def find(self, df, timeframe, symbol):
        # Calculate pattern logic
        if pattern_found:
            return [PatternResult(
                ticker=symbol,
                pattern="My Pattern",
                score=8.5,
                entry=entry_price,
                stop=stop_price,
                target=target_price,
                criteria_met=["criterion1", "criterion2"],
                analysis="Detailed description...",
            )]
        return []
```

### Chart Customization

**Location:** `/app/services/charting.py`

**Key Methods to Extend:**
```python
class ChartingService:
    # Modify chart presets
    CHART_PRESETS = {
        "custom_preset": ["EMA21", "SMA50", "RSI"],  # Add new preset
    }
    
    # Customize studies
    STUDIES_CONFIG = {
        "MyIndicator": {
            "name": "My Custom Indicator",
            "input": {...},
            "override": {...}
        }
    }
    
    # Customize drawings
    def _build_drawings(self, config):
        # Add custom drawing logic
        pass
```

### Frontend Widget Creation

**Location:** `/templates/dashboard.html` and `/static/js/dashboard.js`

**Process:**
1. Add new tab to dashboard HTML
2. Create API handler in `/app/api/`
3. Add JavaScript event listener in `dashboard.js`
4. Style with CSS from `/static/css/dashboard.css`

**Example: Add Chart Comparison Tab**
```html
<!-- In dashboard.html -->
<button class="tab-button" data-tab-target="compare">Compare Charts</button>

<section id="tab-compare" class="tab-pane" data-tab-panel="compare">
    <!-- Comparison UI here -->
</section>
```

```javascript
// In dashboard.js
const compareForm = document.getElementById('compare-form');
compareForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = new FormData(compareForm);
    const response = await fetch('/api/compare-charts', {
        method: 'POST',
        body: JSON.stringify(Object.fromEntries(data))
    });
    // Handle response and render
});
```

---

## Part 3: Data Flow for Custom Visualizations

### Step-by-Step Flow

```
1. USER ACTION (Dashboard)
   └─ Form submission / Button click
   
2. FRONTEND (JavaScript)
   └─ Validate input
   └─ Show loading spinner
   └─ Make async API call
   
3. API ENDPOINT (/app/api/...)
   └─ Validate request
   └─ Check cache first
   └─ Call service layer if needed
   └─ Return structured response
   
4. SERVICE LAYER (/app/services/...)
   └─ Fetch market data (cache or API)
   └─ Process/analyze data
   └─ Generate visualizations
   └─ Cache results
   
5. BACKEND RESPONSE
   └─ Return JSON with:
      - success: bool
      - data: analysis results
      - chart_url: (optional) generated chart
      - metadata: timing, source, etc.
   
6. FRONTEND RENDERING
   └─ Hide loading spinner
   └─ Render results grid/chart
   └─ Update TradingView widget if needed
   └─ Show success/error toast
```

### Adding Custom Visualization Type

**Create New API Endpoint:**
```python
# File: /app/api/custom_visualization.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/custom", tags=["custom"])

class CustomRequest(BaseModel):
    ticker: str
    timeframe: str

@router.post("/analyze")
async def analyze_custom(request: CustomRequest):
    # Fetch data
    market_data = await market_data_service.get_time_series(
        request.ticker, request.timeframe
    )
    
    # Your analysis logic
    results = await my_analysis_service.analyze(market_data)
    
    # Generate visualization if needed
    chart_url = await charting_service.generate_chart(...)
    
    return {
        "success": True,
        "data": results,
        "chart_url": chart_url,
        "timestamp": datetime.now()
    }
```

---

## Part 4: Visualization Patterns & Best Practices

### Pattern 1: Real-Time Results Grid

**Use Case:** Display tabular data (scan results, watchlist, etc.)

**Files Involved:**
- Template: `/templates/dashboard.html`
- JavaScript: `/static/js/dashboard.js`
- API: `/app/api/*.py`

**Example:**
```javascript
const displayResults = (results) => {
    const grid = document.getElementById('results-grid');
    grid.innerHTML = results.map(r => `
        <tr class="result-row">
            <td>${r.ticker}</td>
            <td>${r.pattern}</td>
            <td class="score-badge">${r.score.toFixed(1)}</td>
            <td>${r.entry.toFixed(2)}</td>
            <td>${r.target.toFixed(2)}</td>
        </tr>
    `).join('');
};
```

### Pattern 2: Synchronized Chart Updates

**Use Case:** Keep TradingView chart synced with analysis

**Files Involved:**
- Template: `/templates/partials/tv_widget_templates.html`
- JavaScript: `/static/js/tv-widgets.js`
- API: `/app/api/charts.py`

**Example:**
```javascript
const updateTradingViewChart = (symbol, timeframe) => {
    window.tvWidget?.setSymbol(`NASDAQ:${symbol}`, timeframe);
};

// Call after pattern detection
updateTradingViewChart(patternResult.ticker, 'D');
```

### Pattern 3: Server-Side Chart Caching

**Use Case:** Generate once, serve many times

**Implementation:**
```python
# In /app/services/charting.py
cache_key = f"chart:{ticker}:{interval}:{entry}:{stop}:{target}"

# Check cache
cached_url = await cache_service.get(cache_key)
if cached_url:
    return {"url": cached_url, "cached": True}

# Generate new
chart = await chart_img_api.generate(...)
url = chart['url']

# Cache for 7 days
await cache_service.set(cache_key, url, ttl=7*24*3600)

return {"url": url, "cached": False}
```

### Pattern 4: Progressive Loading

**Use Case:** Show results as they become available

**Implementation:**
```javascript
const scanWithProgress = async (symbols) => {
    for (const symbol of symbols) {
        const result = await fetch(`/api/patterns/detect`, {
            method: 'POST',
            body: JSON.stringify({ticker: symbol})
        }).then(r => r.json());
        
        // Add to results immediately
        addToResultsGrid(result);
        
        // Update count
        updateProgress(symbols.indexOf(symbol) + 1, symbols.length);
    }
};
```

---

## Part 5: Performance Optimization for Visualizations

### 1. Caching Strategy

**Implement Multi-tier Caching:**
```python
# L1: Memory cache (fast, limited)
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_calculation(symbol: str):
    return ...

# L2: Redis cache (shared, medium TTL)
await cache_service.set(key, value, ttl=3600)

# L3: Database (persistent, no TTL)
db_session.add(PatternScan(...))
db_session.commit()
```

### 2. Lazy Loading

**Load data on demand:**
```javascript
// Only fetch when tab is clicked
document.addEventListener('click', async (e) => {
    if (e.target.dataset.tabTarget === 'scanner') {
        if (!state.universeDataLoaded) {
            state.universeDataLoaded = true;
            const results = await fetch('/api/scan/universe').then(r => r.json());
            renderResults(results);
        }
    }
});
```

### 3. Result Pagination

**Limit initial results:**
```python
# API endpoint
@router.get("/patterns/scan")
async def scan(limit: int = 50, offset: int = 0):
    results = await scanner.scan_universe()
    return {
        "data": results[offset:offset+limit],
        "total": len(results),
        "has_more": offset + limit < len(results)
    }
```

---

## Part 6: Testing Visualizations

### Unit Tests

**File:** `/tests/test_pattern_detection.py`

```python
from app.core.detectors.vcp_detector import VCPDetector
import pandas as pd

def test_vcp_pattern():
    detector = VCPDetector()
    df = load_test_data()  # Test OHLCV data
    
    patterns = detector.find(df, "1day", "AAPL")
    
    assert len(patterns) > 0
    assert patterns[0].score > 6.0
    assert patterns[0].pattern == "VCP"
```

### Integration Tests

```python
async def test_pattern_detection_api():
    response = await client.post("/api/patterns/detect", json={
        "ticker": "AAPL",
        "interval": "1day"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
```

### E2E Tests (Playwright)

**File:** `/tests/test_dashboard_ui.js`

```javascript
test('should detect pattern and update chart', async ({ page }) => {
    await page.goto('http://localhost:8000/dashboard');
    
    // Enter ticker
    await page.fill('#pattern-ticker', 'AAPL');
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Wait for results
    await page.waitForSelector('.result-row');
    
    // Verify chart updated
    const chart = await page.locator('#analyze-chart');
    expect(await chart.isVisible()).toBeTruthy();
});
```

---

## Part 7: Advanced Visualization Features

### 1. Multi-Timeframe Comparison

**Location:** `/app/api/charts.py` -> `multi_timeframe_charts` endpoint

**Enhancement:**
```python
async def compare_timeframes(ticker: str, timeframes: List[str]):
    charts = {}
    for tf in timeframes:
        chart = await charting_service.generate_chart(
            ChartConfig(ticker=ticker, interval=tf)
        )
        charts[tf] = chart['url']
    
    return {
        "ticker": ticker,
        "charts": charts,
        "layout": "grid"  # or "carousel"
    }
```

### 2. Pattern Heatmaps

**Create sector/industry performance heatmap:**
```python
@router.get("/market/sector-heatmap")
async def sector_heatmap():
    sectors = await market_data.get_sector_performance()
    
    return {
        "heatmap_data": sectors,
        "html": render_heatmap_html(sectors)  # SVG or HTML
    }
```

### 3. Pattern Statistics Dashboard

**Track win rates and performance:**
```python
@router.get("/analytics/pattern-performance")
async def pattern_performance():
    stats = await database.query("""
        SELECT 
            pattern_type,
            COUNT(*) as count,
            AVG(risk_reward_ratio) as avg_rr,
            SUM(CASE WHEN triggered THEN 1 ELSE 0 END) / COUNT(*) as win_rate
        FROM pattern_scans
        GROUP BY pattern_type
        ORDER BY win_rate DESC
    """)
    
    return {"patterns": stats}
```

---

## Part 8: Common Visualization Tasks

### Task: Add New Market Indicator

1. **Implement in indicators.py:**
```python
def calculate_my_indicator(prices: List[float]) -> List[float]:
    # Your calculation
    return results
```

2. **Add to PatternResult:**
```python
@dataclass
class PatternResult:
    # ... existing fields ...
    my_indicator_value: Optional[float] = None
```

3. **Use in detectors:**
```python
my_value = indicators.calculate_my_indicator(closes)
if my_value > threshold:
    # Pattern detected
```

4. **Display in frontend:**
```javascript
const displayIndicator = (value) => {
    document.getElementById('indicator-display').textContent = 
        `My Indicator: ${value.toFixed(2)}`;
};
```

### Task: Add Real-Time Updates

1. **Use WebSocket (FastAPI):**
```python
from fastapi import WebSocket

@app.websocket("/ws/pattern-updates")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        result = await analyze(data)
        await websocket.send_json(result)
```

2. **Connect from frontend:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/pattern-updates');

ws.onmessage = (event) => {
    const result = JSON.parse(event.data);
    updateDashboard(result);
};
```

---

## Part 9: Resources & Documentation

### Key Files to Reference

| Task | File | Purpose |
|------|------|---------|
| Add pattern | `/app/core/detectors/` | Pattern detection logic |
| Create chart | `/app/services/charting.py` | Chart generation |
| New API | `/app/api/` | REST endpoints |
| Frontend | `/static/js/dashboard.js` | UI logic |
| Styling | `/static/css/` | Visual design |
| Database | `/app/models.py` | Data persistence |
| Indicators | `/app/core/indicators.py` | Technical analysis |

### Configuration

- **Chart-IMG API**: Get key from `.env` -> `CHART_IMG_API_KEY`
- **TradingView**: Docs at `/docs/TRADINGVIEW_WIDGETS.md`
- **Cache TTL**: Set in `/app/services/cache.py`
- **API Limits**: Track in `/app/services/market_data.py`

### Testing

```bash
# Unit tests
pytest tests/

# With coverage
pytest --cov=app tests/

# Integration tests
pytest tests/test_api/

# E2E tests
pytest --headed tests/e2e/
```

### Deployment

- **Local**: `uvicorn app.main:app --reload`
- **Docker**: `docker-compose up`
- **Railway**: See `/DEPLOYMENT.md`

---

## Part 10: Example: Building a New Visualization

### Scenario: Create a "Volatility Heat Map" Dashboard

**Step 1: Design the data model**
```python
@dataclass
class VolatilityPoint:
    ticker: str
    sector: str
    atr_percent: float
    bb_width: float
    volatility_score: float
```

**Step 2: Implement detector**
```python
# /app/routers/volatility.py
@router.get("/volatility/heatmap")
async def volatility_heatmap(universe: str = "SP500"):
    universe_symbols = await universe_service.get_symbols(universe)
    
    volatility_data = []
    for symbol in universe_symbols:
        ohlcv = await market_data.get_daily(symbol)
        atr = calculate_atr(ohlcv)
        bb = calculate_bollinger_bands(ohlcv)
        
        volatility_data.append(VolatilityPoint(
            ticker=symbol,
            sector=get_sector(symbol),
            atr_percent=atr / ohlcv['c'][-1] * 100,
            bb_width=bb['upper'] - bb['lower'],
            volatility_score=calculate_score(atr, bb)
        ))
    
    return {"data": volatility_data, "timestamp": datetime.now()}
```

**Step 3: Create frontend tab**
```html
<button class="tab-button" data-tab-target="volatility">
    Volatility Heat Map
</button>

<section id="tab-volatility" class="tab-pane">
    <div id="volatility-heatmap" class="heatmap-container"></div>
</section>
```

**Step 4: Add JavaScript handler**
```javascript
const loadVolatilityHeatmap = async () => {
    const response = await fetch('/api/volatility/heatmap?universe=SP500');
    const data = await response.json();
    
    renderHeatmap(data.data);
};

document.addEventListener('click', e => {
    if (e.target.dataset.tabTarget === 'volatility') {
        loadVolatilityHeatmap();
    }
});
```

**Step 5: Render heatmap**
```javascript
const renderHeatmap = (data) => {
    const container = document.getElementById('volatility-heatmap');
    
    const html = data.map(point => `
        <div class="heatmap-cell" 
             style="background: ${getColorForScore(point.volatility_score)}">
            <span>${point.ticker}</span>
            <span class="value">${point.atr_percent.toFixed(1)}%</span>
        </div>
    `).join('');
    
    container.innerHTML = html;
};

const getColorForScore = (score) => {
    // Green: low volatility, Red: high volatility
    const hue = 120 - (score * 120); // Green to Red
    return `hsl(${hue}, 100%, 50%)`;
};
```

---

## Summary

Legend AI's visualization stack is:
- **Modular**: Each component can be extended independently
- **Scalable**: Caching and database support large datasets
- **Responsive**: CSS Grid/Flexbox + TradingView
- **Well-tested**: Unit, integration, and E2E tests included
- **Production-ready**: Deployed on Railway with monitoring

To build new visualizations:
1. Create data model or detector
2. Add API endpoint
3. Build frontend UI
4. Style with CSS
5. Test thoroughly
6. Deploy

All pieces work together through REST APIs and the multi-tier caching system.

---

**For detailed implementation examples, see:**
- `/CODEBASE_STRUCTURE_FOR_VISUALIZATIONS.md` - Full architecture
- `/VISUALIZATION_QUICK_REFERENCE.md` - Quick reference guide
- `/docs/TRADINGVIEW_WIDGETS.md` - TradingView integration
- `/API_REFERENCE.md` - Complete API documentation
