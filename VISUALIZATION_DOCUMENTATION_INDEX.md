# Legend AI Market Visualization - Documentation Index

## Overview
Complete codebase exploration and documentation for building market visualizations in the Legend AI trading platform.

---

## Documentation Files (Created for You)

### 1. **CODEBASE_STRUCTURE_FOR_VISUALIZATIONS.md** (24KB)
**Most Comprehensive Guide**

This is your go-to reference document. Contains:
- Executive summary of the project
- Complete project structure diagram
- Existing visualization components overview
- Data fetching mechanisms (multi-source fallback)
- API endpoints reference (20+ routers)
- Data models and database schema
- Frontend framework (Vanilla JS + TradingView)
- Pattern detection code locations (8+ patterns + 50+ advanced)
- Market analysis tools and services
- Technology stack summary
- Quick reference table

**Use This For:** Understanding the overall architecture and finding specific components.

---

### 2. **VISUALIZATION_QUICK_REFERENCE.md** (11KB)
**Quick Lookup Guide**

Visual diagram-heavy document with:
- Architecture diagram (Frontend → Backend → Database)
- Key statistics (20+ routers, 8+ detectors, etc.)
- Data flow visualization
- Where visualizations happen (server-side vs client-side)
- Sample API response format
- Database models for visualization
- Performance metrics
- Upcoming features roadmap

**Use This For:** Quick visual understanding without deep details.

---

### 3. **MARKET_VISUALIZATION_ROADMAP.md** (18KB)
**Development Guide for Extending Visualizations**

Step-by-step guide for developers:
- Part 1: Understanding current visualization stack
- Part 2: Key entry points for extensions
- Part 3: Data flow for custom visualizations
- Part 4: Visualization patterns & best practices
- Part 5: Performance optimization tips
- Part 6: Testing strategies (unit, integration, E2E)
- Part 7: Advanced features (multi-timeframe, heatmaps, analytics)
- Part 8: Common visualization tasks
- Part 9: Resources and documentation
- Part 10: Complete worked example

**Use This For:** Building new visualizations or extending existing ones.

---

## Quick Navigation by Use Case

### Understanding the Current System

Start here:
1. `VISUALIZATION_QUICK_REFERENCE.md` - Get the big picture
2. `CODEBASE_STRUCTURE_FOR_VISUALIZATIONS.md` - Deep dive into architecture

### Building New Visualizations

Follow this path:
1. `MARKET_VISUALIZATION_ROADMAP.md` - Part 2-4 (entry points & data flow)
2. `CODEBASE_STRUCTURE_FOR_VISUALIZATIONS.md` - Section 7 (pattern detectors)
3. `MARKET_VISUALIZATION_ROADMAP.md` - Part 10 (worked example)

### Extending Existing Components

Use:
1. `MARKET_VISUALIZATION_ROADMAP.md` - Part 8 (common tasks)
2. `CODEBASE_STRUCTURE_FOR_VISUALIZATIONS.md` - Section 12 (quick reference table)
3. Actual source files referenced in documentation

### Performance Optimization

See:
1. `MARKET_VISUALIZATION_ROADMAP.md` - Part 5
2. `CODEBASE_STRUCTURE_FOR_VISUALIZATIONS.md` - Section 9.2

---

## Key Facts About Legend AI

### Architecture
- **Backend:** FastAPI (Python 3.11) with 20+ API routers
- **Frontend:** Vanilla JavaScript (80KB) + CSS (70KB) + TradingView widgets
- **Database:** PostgreSQL (production) / SQLite (development)
- **Cache:** Redis (multi-tier strategy)
- **Charting:** Chart-IMG API (500 daily calls) + TradingView embed

### Data Sources
1. **TwelveData** (primary, 800 calls/day)
2. **Finnhub** (fallback, 60 calls/day)
3. **Alpha Vantage** (fallback, 500 calls/day)
4. **Yahoo Finance** (last resort, unlimited)

### Pattern Detection
- **8 Core Detectors:** VCP, Cup & Handle, Triangle, Double Top/Bottom, etc.
- **50+ Advanced Patterns:** Harmonic, Candlestick, Gap patterns
- **Scoring:** 0-10 scale based on confidence
- **Entry/Stop/Target:** Automatic calculation with risk/reward ratio

### Dashboard Features
- **Analyze Tab:** Single ticker pattern analysis
- **Scanner Tab:** Bulk universe scanning (S&P 500, NASDAQ 100)
- **Top Setups:** Best patterns ranked by score
- **Market Internals:** Breadth, VIX, sector performance
- **Watchlist:** Portfolio tracking with alerts

### Visualization Components
- **Grid/Table View:** Results display with sorting/filtering
- **Chart Preview:** Annotated charts with indicators
- **TradingView Widget:** Interactive advanced chart
- **Heatmaps:** Sector/market performance
- **Analytics Dashboard:** Pattern win rates, performance metrics

---

## File Organization

```
/home/user/legend-ai-python/
├── CODEBASE_STRUCTURE_FOR_VISUALIZATIONS.md      ← Comprehensive guide
├── VISUALIZATION_QUICK_REFERENCE.md              ← Visual overview
├── MARKET_VISUALIZATION_ROADMAP.md               ← Development guide
├── VISUALIZATION_DOCUMENTATION_INDEX.md          ← This file
│
├── app/
│   ├── core/detectors/                           ← Pattern detectors
│   ├── services/charting.py                      ← Chart generation
│   ├── services/market_data.py                   ← Data fetching
│   ├── api/                                      ← API endpoints
│   └── models.py                                 ← Database models
│
├── templates/
│   ├── dashboard.html                            ← Main UI
│   └── partials/tv_widget_templates.html         ← TradingView templates
│
└── static/
    ├── js/dashboard.js                           ← Frontend logic
    └── css/                                      ← Styling
```

---

## Common Questions Answered

**Q: Where are the pattern detectors?**
A: `/app/core/detectors/` - See CODEBASE guide Section 7.1

**Q: How do I add a new pattern?**
A: Create a detector class, register it, and it auto-integrates. See ROADMAP Part 2.

**Q: Where are the API endpoints?**
A: `/app/api/` - 20+ routers. List in CODEBASE guide Section 4.1

**Q: How is chart generation handled?**
A: `/app/services/charting.py` uses Chart-IMG API. See ROADMAP Part 1.2

**Q: What data sources are used?**
A: Multi-source fallback (TwelveData → Finnhub → Alpha Vantage → Yahoo). See CODEBASE Section 3.1

**Q: How is caching implemented?**
A: Multi-tier (memory → Redis → database). See CODEBASE Section 3.2

**Q: Can I customize the dashboard?**
A: Yes! See ROADMAP Part 3 for data flow and Part 4 for patterns.

**Q: How do I test new visualizations?**
A: Unit, integration, and E2E tests. See ROADMAP Part 6

**Q: What's the tech stack?**
A: FastAPI + Vanilla JS + TradingView + PostgreSQL + Redis. See CODEBASE Section 11.

---

## Performance Metrics

From the codebase analysis:

- **Cache Hit Rate:** 60-80% (reduces API calls by 70%)
- **Pattern Scan Time:** 0.5-2s per ticker
- **Bulk Universe Scan:** 50-100 tickers in <30s
- **Chart Generation:** 0.5-1s per chart
- **Memory Usage:** ~100MB baseline
- **Concurrent Users:** 100+ supported (API-limited)
- **Response Time:** <5s target (usually <2s)

---

## Entry Points for Development

### For Backend Developers
- Add patterns: `/app/core/detectors/`
- Create APIs: `/app/api/`
- Build services: `/app/services/`
- Handle database: `/app/models.py`

### For Frontend Developers
- Modify UI: `/templates/dashboard.html`
- Add interactions: `/static/js/dashboard.js`
- Style components: `/static/css/`
- Embed charts: `/templates/partials/tv_widget_templates.html`

### For Data Scientists
- Improve detectors: `/app/core/detector_base.py`
- Add indicators: `/app/core/indicators.py`
- Enhance analysis: `/app/detectors/advanced/patterns.py`

---

## Related Documentation

Also available in the repository:

- `/docs/TRADINGVIEW_WIDGETS.md` - TradingView integration guide
- `/docs/PATTERN_DETECTION_ANALYSIS.md` - Pattern algorithm details
- `/API_REFERENCE.md` - Complete API documentation
- `/DATA_FLOW_ARCHITECTURE.md` - System architecture
- `/DASHBOARD_IMPROVEMENTS_SUMMARY.md` - Recent UI changes
- `/DEPLOYMENT.md` - Deployment guide
- `/LOCAL_SETUP.md` - Local development setup

---

## Quick Start for Developers

### Understand the System (30 mins)
1. Read `VISUALIZATION_QUICK_REFERENCE.md`
2. Skim `CODEBASE_STRUCTURE_FOR_VISUALIZATIONS.md` Sections 1-4

### Get Hands-On (2 hours)
1. Follow `LOCAL_SETUP.md` to run locally
2. Test a pattern detection: `POST /api/patterns/detect?ticker=AAPL`
3. View dashboard at `http://localhost:8000/dashboard`
4. Inspect frontend in browser DevTools

### Extend the System (4+ hours)
1. Read `MARKET_VISUALIZATION_ROADMAP.md` Part 2-4
2. Choose an extension (new detector, new chart type, etc.)
3. Implement following the patterns in Part 4
4. Test using patterns in Part 6
5. Deploy following `/DEPLOYMENT.md`

---

## Technology Stack Summary

| Component | Technology | Docs Section |
|-----------|-----------|--------------|
| Backend | FastAPI | CODEBASE 1.0 |
| Frontend | Vanilla JS + CSS | CODEBASE 6.0 |
| Charting | Chart-IMG + TradingView | CODEBASE 2.2 |
| Database | PostgreSQL + SQLite | CODEBASE 5.0 |
| Cache | Redis | CODEBASE 3.2 |
| Data Sources | TwelveData, Finnhub, etc. | CODEBASE 3.1 |
| Pattern Detection | Custom detectors | CODEBASE 7.0 |
| Deployment | Railway + Docker | DEPLOYMENT.md |

---

## File Sizes

- **Dashboard HTML:** 38KB
- **Frontend JavaScript:** 80KB
- **Dashboard CSS:** 51KB
- **Design System CSS:** 20KB
- **Charting Service:** 21KB
- **Market Data Service:** 24KB
- **Pattern Detector V1:** 100+ lines
- **Advanced Detectors:** 50+ patterns

**Total Frontend:** ~190KB (minified/gzipped: ~50KB)

---

## Next Steps

1. **Read:** Start with `VISUALIZATION_QUICK_REFERENCE.md` for overview
2. **Explore:** Check `CODEBASE_STRUCTURE_FOR_VISUALIZATIONS.md` for details
3. **Build:** Follow `MARKET_VISUALIZATION_ROADMAP.md` to extend system
4. **Test:** Use the testing patterns in Part 6 of the Roadmap
5. **Deploy:** Follow `/DEPLOYMENT.md` for production

---

## Support & Resources

- **API Documentation:** `/docs` endpoint or `/API_REFERENCE.md`
- **TradingView Help:** `/docs/TRADINGVIEW_WIDGETS.md`
- **Pattern Details:** `/docs/PATTERN_DETECTION_ANALYSIS.md`
- **Troubleshooting:** Check error codes in `/app/core/errors.py`
- **Monitoring:** Prometheus metrics at `/api/metrics/prometheus`

---

**Documentation Generated:** November 18, 2025  
**Codebase Version:** 1.0.0  
**Status:** Production Ready

For questions about specific components, refer to the Section 12 quick reference table in `CODEBASE_STRUCTURE_FOR_VISUALIZATIONS.md`.
