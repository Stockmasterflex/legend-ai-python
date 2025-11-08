# 🧠 Legend AI — Product Requirements Document (Full System PRD v2.0)

---

## 1️⃣ Mission Statement
**Legend AI** is a professional-grade, AI-assisted trading intelligence system built for **technical analysts, swing traders, and FinTech developers**.  
It fuses **pattern recognition, AI-driven insights, and automated trade planning** into a single cohesive ecosystem — designed to match the performance and logic of elite traders like Minervini, O’Neil, and Livermore.

**Core goals:**
- Deliver real-time, data-backed pattern analysis and trade plans.
- Provide automated scanning and ranking of stocks by setup quality.
- Create a clean, intuitive web app deployable on Railway or any FastAPI backend.
- Integrate AI copilots (GPT, Claude, Gemini) for commentary, scoring, and forecasting.
- Support modular expansion into Telegram, Google Sheets, and automation workflows.

---

## 2️⃣ Core User Profiles

| Profile | Description | Primary Goals |
|----------|--------------|----------------|
| **Active Swing Trader** | Trades 2–10 positions using daily/weekly charts. | Identify high-probability setups and manage risk. |
| **Quant/Analyst** | Runs systematic scans or data research. | Use API endpoints for pattern or signal extraction. |
| **FinTech Developer** | Builds apps or dashboards using Legend AI’s data or APIs. | Integrate backend analytics, charts, and AI layers into products. |
| **Content Creator / Mentor** | Uses Legend AI to publish trade insights, watchlists, and pattern studies. | Automate visual chart reports and analysis outputs. |

---

## 3️⃣ Primary Features Overview

| Feature | Description |
|----------|-------------|
| **Analyze** | Input ticker → fetch OHLCV → calculate indicators → detect patterns → return trade plan + Chart-IMG snapshot. |
| **Pattern Scanner** | Batch scans a list of tickers, detecting VCPs, bases, breakouts, pullbacks, and grouping results into buckets. |
| **Top Setups (Daily Picks)** | Automatically highlights top-ranked setups each day across all pattern classes. |
| **Market Internals Dashboard** | Displays sector strength, index trends, breadth, and volatility metrics. |
| **Watchlist Manager** | Allows saving, removing, and analyzing favorite tickers via CRUD interface. |
| **Telegram Alerts** *(future)* | Sends AI-ranked setups or alerts for breakout events via bot notifications. |
| **AI Commentary** *(future)* | Uses GPT or Claude to summarize market conditions, setups, and confidence levels. |
| **Trade Journal Export** *(future)* | Syncs executed trades to Google Sheets or Notion for journaling and review. |

---

## 4️⃣ System Architecture

### ⚙️ Backend (FastAPI)
- Python 3.11+ with FastAPI and async support
- Core routes:
  - `/api/analyze`
  - `/api/scan`
  - `/api/scan_buckets` *(planned for upgrade)*
  - `/api/watchlist`
  - `/api/version` (returns build SHA)
- Services:
  - `market_data`: handles OHLCV via TwelveData/Finnhub/AlphaVantage fallback chain.
  - `chartimg`: interfaces with Chart-IMG API for server-side chart rendering.
  - `patterns`: runs Minervini, Weinstein, and VCP classification logic.
  - `cache`: Redis caching for data reuse and rate-limit mitigation.

### 🎨 Frontend (Web)
- Built with **Jinja2 templates** + **vanilla JavaScript** (`static/js/dashboard.js`).
- SPA-like tab navigation:
  - Analyze
  - Pattern Scanner
  - Top Setups
  - Market Internals
  - Watchlist
- Chart-IMG rendering: triggered only after successful /api/analyze request.
- Dynamic intel panels show:
  - Pattern grades
  - Rule failures
  - Stage and RS rank
  - Distances to key MAs
  - R-multiple and plan summary
- Cache-busted JS (`?v={{ build_sha }}`) and header build tag (`BUILD <sha>`).

### 🗄️ Infrastructure
- **Deployment:** GitHub → Railway (auto CI/CD)
- **Databases:**
  - PostgreSQL (for future trade logs & watchlists)
  - Redis (for caching pattern data & scan results)
- **Secrets (Railway Variables):**
  - `CHARTIMG_API_KEY`
  - `TWELVEDATA_API_KEY`
  - `FINNHUB_API_KEY`
  - `ALPHA_VANTAGE_API_KEY`
  - `OPENROUTER_API_KEY`
  - `TELEGRAM_BOT_TOKEN`
  - `GOOGLE_SHEETS_ID`
- **Storage:** Google Sheets or Redis JSON for logs/reports
- **CI/CD:** GitHub Actions with pytest + lint checks

---

## 5️⃣ Key Technical Components

### A. **Chart Generation**
- Uses [Chart-IMG v2 API](https://chart-img.com/docs)
- Config:
  - `theme`: dark
  - `studies`: EMA(21), SMA(50), RSI(14), Volume
  - `drawings`: Long Position (entry, stop, target)
- Exponential backoff (max 4 tries) on errors
- Returns pre-signed `chart_url` → embedded in dashboard

### B. **Pattern Detection Algorithms**
- **Minervini Trend Template (TT):**
  - 10MA > 20MA > 50MA > 200MA
  - Price > 50MA and 200MA
  - RS line trending up
- **VCP (Volatility Contraction Pattern):**
  - Series of narrowing contractions
  - Decreasing volume sequence
  - Dry-up at base end
- **Weinstein Stage Analysis:**
  - Stage 1–4 classification based on MA slope and price relative position
- **Breakouts:**
  - Price above pivot +40% avg volume
- **Flat Bases:**
  - Tight consolidation within 15% range over ≥ 5 weeks

### C. **AI Modules (Planned Integration)**
- **AI Commentary Engine:**
  - Summarizes setups and assigns “Conviction Score”
  - Uses GPT-5 via OpenRouter
- **AI Trade Advisor:**
  - Generates alternate plan suggestions (entry/stop/target)
- **AI Journal Coach:**
  - Reviews user trades and generates insights for consistency improvement

---

## 6️⃣ UX / UI Requirements

- Design:
  - Dark, gradient-themed UI (trader aesthetic)
  - Cards, gradients, and emoji indicators (🔥 A+, 🟩 Inside Up, etc.)
  - Responsive for desktop and tablet (mobile minimal)
- Tabs always visible; switching tabs unloads charts.
- Analyze → Image render, plan output, intel panel.
- Pattern Scanner → Grid of cards with patterns grouped by bucket.
- Market Internals → Embedded TradingView widgets (indices, VIX, sector heatmap).
- Watchlist → Table view with “Analyze Again” quick action.
- Include “BUILD <sha>” header tag for version traceability.

---

## 7️⃣ Data Flow Summary

1. User enters ticker + timeframe → frontend sends `/api/analyze?ticker=NVDA&tf=daily`
2. Backend fetches OHLCV (TwelveData → fallback)
3. Runs indicators + pattern detection logic
4. Generates chart snapshot (Chart-IMG)
5. Stores temporary data in Redis cache
6. Returns JSON with `chart_url`, `patterns`, and `plan`
7. Frontend displays chart + intel + action buttons

---

## 8️⃣ Logging, Testing, and Telemetry

### Logging
- Log startup config (booleans for key presence)
- Log Chart-IMG POST request attempts with:
  - symbol
  - interval
  - status code
  - truncated response body
- Log all pattern detections and scan durations.

### Testing
- `pytest -q tests`
  - `test_analyze_contract.py`: verifies JSON schema
  - `test_smoke.py`: startup/healthcheck
  - Future: `test_scan_buckets.py`: verifies bucket assignment logic
- CI: fail on pytest errors (no `|| true`)

---

## 9️⃣ Performance Targets

| Metric | Target |
|---------|--------|
| Analyze Response | < 2 sec |
| Scan 100 Tickers | < 15 sec |
| Chart-IMG Render | < 1.5 sec |
| UI Load | < 1 sec |
| Error Rate | < 1% 500s/day |

---

## 🔟 Future Expansion & Integrations

| Feature | Description | Status |
|----------|--------------|---------|
| **AI Council Mode** | Uses multiple AI models (GPT, Claude, Gemini) to vote on best trade direction. | In concept |
| **Telegram Notifications** | Daily top setups pushed to Telegram. | Planned |
| **Portfolio Tracker** | Track performance, R-multiple, and hit rate. | Planned |
| **Trade Journal Export** | Syncs to Sheets or Notion. | Planned |
| **Macro & Sentiment Layer** | Integrates AAII, VIX, and put/call ratios. | Future |
| **Legend Score System** | Composite score from technical + volume + AI confidence. | In design |
| **Auto Setup Reports** | Scheduled summary emails or Telegram snapshots. | Planned |

---

## 11️⃣ Architecture Diagram (Simplified)

Frontend (Dashboard.js)
↓
FastAPI (Analyze, Scan, Watchlist)
↓
Services:
├── market_data.py  → TwelveData / Finnhub / AlphaVantage
├── chartimg.py     → Chart-IMG v2
├── patterns.py     → Minervini, Weinstein, VCP logic
├── cache.py        → Redis (1h TTL)
↓
Storage / Outputs:
├── PostgreSQL (future trades)
├── Redis (cache)
├── Google Sheets (reports)
└── Telegram Bot (alerts)

---

## 12️⃣ Release Phases

| Phase | Objective | Deliverables |
|--------|------------|---------------|
| **Phase 1 (MVP)** | Core backend + Analyze tab | /api/analyze, ChartIMG integration, working dashboard |
| **Phase 2 (Scanner)** | Add /api/scan + buckets | Group setups into VCP, Bases, Breakouts, Pullbacks |
| **Phase 3 (Top Setups)** | Rank and publish best tickers | Daily cache and Telegram alert |
| **Phase 4 (AI Insights)** | Integrate GPT/Claude commentary | AI confidence layer + trade plan commentary |
| **Phase 5 (User Tools)** | Watchlist + Trade Journal | CRUD + export to Sheets or Notion |

---

## ✅ Acceptance Criteria Summary

| Category | Requirement |
|-----------|-------------|
| **Backend Health** | /health and /version return 200 |
| **Analyze Output** | Valid JSON with populated `chart_url` |
| **Scanner Buckets** | Deterministic grouping works on live data |
| **Performance** | Analyze < 2s, Scan < 15s |
| **Frontend UX** | Tabs working, no chart on load |
| **Security** | No keys exposed client-side |
| **CI/CD** | All tests green before merge |
| **Deployment** | Railway auto-deploy on base branch |
| **Telemetry** | ChartIMG + Analyze logs visible in dashboard |
| **AI Readiness** | PRD + MVP_SPEC sync completed for automation agents |

---

_This PRD defines the full Legend AI system scope, covering architecture, UX, data flow, and development phases. It serves as the master reference for engineering, AI coding agents, and roadmap planning._
