---

# 🧠 Legend AI — Product Requirements Document (Full System PRD v2.0)

Legend AI is an AI-assisted trading intelligence platform for swing traders, analysts, and FinTech builders. This PRD merges the ambitions of the master improvement plan, the swinging feature roadmap, and the MVP spec into one cohesive long-term strategy.

## 1️⃣ Mission & Outcomes
**Legend AI** aims to deliver real-time, technical pattern intelligence with AI commentary, automated trade planning, and deployable dashboards. We focus on:

- Professional-grade trade setups (Minervini, Weinstein, VCP).
- Automated universe scanning + ranked top setups.
- Chart-IMG snapshots + Plan generation.
- Expandable pipelines (watchlist, Telegram, Sheets, AI Commentary).

## 1.5 📚 Source Alignment

| Source doc | Key commitments pulled in | Reflected in |
|-------------|---------------------------|--------------|
| `docs/Legend_AI_Roadmap.md` | Phase-by-phase trajectory from analyze → scanners → watchlist → AI. | Section 12 release phases + Section 5 module ordering. |
| `docs/Legend_AI_MVP.md` | MVP contract for `/api/analyze`, scan endpoints, dashboard tabs, logging/testing. | Sections 3–8 (functional modules, UX, telemetry). |
| `docs/MVP_SPEC.md` | Stable API contracts, in/out-of-scope guardrails, performance bars. | Mission/Scope section, API expectations in Sections 4–9. |
| `MASTER_IMPROVEMENT_PLAN.md` | Universe scanner backlog, scheduled jobs, trade planner, caching, rate-limit observability. | Section 5 (D–F), release phases, performance/telemetry targets. |
| `SWING_TRADER_FEATURE_ROADMAP.md` | Real-time alerts, multi-timeframe confirmation, entry/exit management, Telegram workflows. | Section 5E, UX Section 6, release phases + acceptance criteria. |

## 2️⃣ Core Audiences

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
| **Scheduled Universe Scans** | Nightly + EOD scan of S&P 500 / NASDAQ 100 with caching, rate-limit aware batching, and Telegram/Sheets digests. |
| **Market Internals Dashboard** | Displays sector strength, index trends, breadth, and volatility metrics. |
| **Watchlist Manager** | Allows saving, removing, and analyzing favorite tickers via CRUD interface. |
| **Multi-Timeframe Confirmation** | Shows weekly/daily/4H/1H pattern alignment, confidence boosts, and heatmap visual. |
| **Trade Planner & Journal** | Builds ATR-based plans, position sizing, and logs executions for expectancy stats + exports. |
| **Telegram Alerts & Commands** | Sends breakout alerts (Watching → Triggered) and exposes `/scan`, `/plan`, `/watchlist` bot commands. |
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
  - `/api/trade/plan/{ticker}`
  - `/api/version` (returns build SHA)
- Services:
  - `market_data`: handles OHLCV via TwelveData/Finnhub/AlphaVantage fallback chain.
  - `chartimg`: interfaces with Chart-IMG API for server-side chart rendering.
  - `patterns`: runs Minervini, Weinstein, and VCP classification logic.
  - `cache`: Redis caching for data reuse and rate-limit mitigation.
  - `universe`: ingests S&P 500 / NASDAQ 100 lists, annotates sectors, and schedules nightly scans + sector filters.
  - `alerts`: monitors watchlist states, dispatches Telegram/email/web toasts, and persists alert history.
  - `trade_planner`: calculates ATR/R-multiple plans, journaling payloads, and export formatting.
  - `scheduler`: orchestrates cron-style jobs (EOD scan, 5-min watchlist monitor, market briefings).

### 🎨 Frontend (Web)
- Built with **Jinja2 templates** + **vanilla JavaScript** (`static/js/dashboard.js`).
- SPA-like tab navigation:
  - Analyze
  - Pattern Scanner
  - Top Setups
  - Market Internals
  - Watchlist
  - Multi-TF Analysis
  - Trade Planner
  - Alert Center
- Chart-IMG rendering: triggered only after successful /api/analyze request.
- Dynamic intel panels show:
  - Pattern grades
  - Rule failures
  - Stage and RS rank
  - Distances to key MAs
  - R-multiple and plan summary
  - Multi-timeframe heatmap + confidence boosts
  - Watchlist status + alert feed pills
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
- Multi-timeframe rendering: `/api/charts/multi` accepts `["1W","1D","4H","1H"]` to power the Multi-TF tab.
- Entry/stop/target overlays re-enabled with trimmed annotations (max 2 drawings) per master plan 1.2.
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
- **Multi-Timeframe Confirmation:**
  - Runs detectors on 1W/1D/4H/1H
  - Applies weighted boosts when higher + lower timeframes align
  - Outputs heatmap + confidence deltas for UI + alerting

### C. **AI Modules (Planned Integration)**
- **AI Commentary Engine:**
  - Summarizes setups and assigns “Conviction Score”
  - Uses GPT-5 via OpenRouter
- **AI Trade Advisor:**
  - Generates alternate plan suggestions (entry/stop/target)
- **AI Journal Coach:**
  - Reviews user trades and generates insights for consistency improvement

### D. **Universe Scanning & Scheduling**
- **Data Backbone:**
  - Weekly ingestion of S&P 500 + NASDAQ 100 with sector/industry tags (PostgreSQL + Redis cache).
- **Endpoints:**
  - `POST /api/scan/universe`, `POST /api/scan/sector/{sector}`, `GET /api/top-setups?limit=10`.
  - Rate-limit aware batching (chunks of 25) with exponential backoff + jitter.
- **Scheduling:**
  - Cron job at 4:05 PM ET (post-close) and Sunday refresh.
  - Stores snapshot JSON for dashboard tabs + Telegram digest.
- **Outputs:**
  - Bucketed cards (VCP, Flat Base, Breakout, Pullback), Legend Score, RS rank, `chart_url`.

### E. **Watchlist, Alerts & Telegram Automations**
- **Watchlist States:** `Watching`, `Breaking Out`, `Triggered` with timestamp + note per ticker.
- **Monitoring Loop:** Every 5 minutes during market hours, re-runs pattern + price/volume thresholds (>=1.5x avg vol, MA distances).
- **Alert Channels:** Dashboard toast/history, Telegram bot (photos + Markdown), optional email/SMS stubs.
- **Bot Commands:** `/scan`, `/scan sector TECH`, `/plan NVDA`, `/watchlist`, `/add TICKER reason`, `/triggered`.
- **Audit Trail:** Redis list + Sheets tab logging ticker, pattern, confidence, R:R, and response latency.

### F. **Trade Planner, Journal & Risk Engine**
- **Endpoint:** `POST /api/trade/plan/{ticker}` returns entry, stop, R targets (2R/3R), ATR-based position sizing.
- **Position Sizing:** Account-size aware, supports fixed % risk and Kelly-lite multiplier.
- **Partial Exits & Notes:** Allows up to 3 targets, adds journal prompts (“why setup”, “lessons”).
- **Storage:** PostgreSQL `trades` + `journal_entries`, optional Sheets export for manual review.
- **Reporting:** Weekly performance summaries (win rate, expectancy, drawdown) feeding dashboard + Telegram `/stats`.

---

## 6️⃣ UX / UI Requirements

- Design:
  - Dark, gradient-themed UI (trader aesthetic)
  - Cards, gradients, and emoji indicators (🔥 A+, 🟩 Inside Up, etc.)
  - Responsive for desktop and tablet (mobile minimal)
- Tabs always visible; switching tabs unloads charts.
- Analyze → Image render, plan output, intel panel.
- Pattern Scanner → Grid of cards with patterns grouped by bucket.
- Top Setups → Daily list with Telegram share + “Analyze again” CTA.
- Market Internals → Embedded TradingView widgets (indices, VIX, sector heatmap).
- Watchlist → Table view with “Analyze Again” quick action.
- Multi-TF Analysis → Heatmap of timeframe agreement + confidence boost badges.
- Trade Planner → Form for account size/risk %, AI suggestions, and journal notes.
- Alert Center → Toast feed with filters (channel, status) + retry/ack controls.
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

**Background Jobs**
- **EOD Universe Scan:** Scheduler → `universe` service → chunked `/api/scan/universe` → cache (Redis) + persist (PostgreSQL) → Top Setups tab + Telegram digest.
- **Watchlist Monitor:** Scheduler → `alerts` service → pull watchlist states → re-run analyzer → emit alerts (Telegram/API/dashboard) → log to Sheets + Redis queue.
- **Market Briefing:** Post-close job aggregates internals, risk metrics, and legend scores, then posts to Telegram `/market` and optional Sheets tab.

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
- Log universe scan job metadata (batch size, runtime, cache hits) and watchlist alert emissions (channel, status).
- Emit rate-limit gauges + cache hit rates for Grafana/Prometheus hooks.

### Testing
- `pytest -q tests`
  - `test_analyze_contract.py`: verifies JSON schema
  - `test_smoke.py`: startup/healthcheck
  - Future: `test_scan_buckets.py`: verifies bucket assignment logic
  - Future: `test_trade_plan.py`: validates ATR sizing & R targets
  - Future: `test_alert_scheduler.py`: simulates watchlist transitions + Telegram payloads
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
| Alert Latency | < 60 sec from trigger to Telegram toast |
| EOD Universe Scan | < 20 min for 600 symbols with caching |

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
├── universe.py     → Universe ingestion + scheduled scans
├── alerts.py       → Watchlist monitors + Telegram bot
├── trade_planner.py→ ATR sizing + journaling payloads
├── scheduler.py    → Orchestrates cron + workers
↓
Storage / Outputs:
├── PostgreSQL (future trades)
├── Redis (cache)
├── Google Sheets (reports/journal)
├── Telegram Bot (alerts)
└── Notion / Sheets exports (trade plans)

---

## 12️⃣ Release Phases

| Phase | Objective | Deliverables |
|--------|------------|---------------|
| **Phase 1 – Analyze + Universe Baseline** | Lock in MVP spec + roadmap phase 1 deliverables. | `/api/analyze`, Chart-IMG with entry/stop overlays, Analyze tab, `/health` + `/version`, watchlist CRUD MVP, `build_sha`, and seeded S&P 500 / NASDAQ 100 tables with sector metadata. |
| **Phase 2 – Scanners, Top Setups & Scheduling** | Execute the master plan 1.1 backlog. | `/api/scan`, `/api/scan/universe`, `/api/scan/sector/{sector}`, scheduled EOD scans + caching (24h TTL), Telegram/Sheets digests, Pattern Scanner + Top Setups tabs pulling from cached data. |
| **Phase 3 – Watchlist Intelligence & Market Internals** | Merge roadmap phase 3 with swing-trader alert requirements. | Watchlist states (Watching / Breaking Out / Triggered), five-minute monitoring job, toast + Telegram/email alerts, Market Internals tab (breadth, VIX, heatmap), alert history log, multi-timeframe confirmation overlays. |
| **Phase 4 – Trade Plans, Journal & Risk Engine** | Cover master plan 1.3 plus entry/exit management backlog. | `/api/trade/plan/{ticker}`, ATR/Kelly sizing, R-multiple insights, trade journal schema + CRUD/export, Trade Planner UI, partial exit templates, Sheets/Notion sync jobs. |
| **Phase 5 – AI Guidance & Platform Hardening** | Incorporate roadmap phases 4–5 and master plan phase 2/3. | GPT/Claude commentary + AI Council, multi-timeframe confidence boosts, Legend Score, market briefings, telemetry dashboards, rate-limit monitoring, CI/CD hardening, portfolio + performance analytics dashboards. |

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
| **Watchlist Alerts** | States transition correctly and alerts propagate to dashboard + Telegram |
| **Trade Planner** | `/api/trade/plan` returns ATR sizing + 2R/3R targets |
| **Multi-TF Tab** | Heatmap reflects weekly/daily/4H/1H detector outputs |

---

_This PRD defines the full Legend AI system scope, covering architecture, UX, data flow, and development phases. It serves as the master reference for engineering, AI coding agents, and roadmap planning._
