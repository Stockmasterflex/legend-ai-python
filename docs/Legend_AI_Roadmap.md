# Legend AI Roadmap

This living roadmap mirrors the priorities in `docs/Legend_AI_PRD.md` and keeps the team anchored on which capabilities land in each release. Every phase builds on the previous one while honoring the swing-trader feature set, the master improvement plan, and the MVP guardrails.

## Release Phase Overview

| Phase | Objective | Key Modules (PRD refs) | Exit Criteria |
|-------|-----------|------------------------|---------------|
| **Phase 1 – Analyze + Universe Baseline** | Ship the end-to-end analyze workflow and seed our universe data. | `/api/analyze`, Chart-IMG integration, Analyze tab, `/version` + `/health`, S&P 500 + NASDAQ 100 ingestion (PRD §§3,5A,5D,12). | Analyze response <2s, build SHA visible, seeded universe tables, `test_analyze_contract.py` + smoke suite green. |
| **Phase 2 – Scanners & Top Setups** | Turn the analyzer into nightly scanners with cached outputs and curated picks. | `/api/scan`, `/api/scan/universe`, `/api/top-setups`, scheduler, Pattern Scanner + Top Setups tabs (PRD §§3–5D,12). | 600-symbol EOD scan <20 min, cached buckets feeding UI + Telegram/Sheets digests, scan telemetry logged. |
| **Phase 3 – Watchlist Intelligence & Market Internals** | Operationalize the watchlist, alerts, and macro dashboards. | Watchlist CRUD/states, 5-min monitor, alert center, Market Internals tab, multi-timeframe overlays (PRD §§3,5E,6,8,12). | Alerts flow to dashboard + Telegram in <60s, market internals widgets live, multi-TF heatmap rendered. |
| **Phase 4 – Trade Planner, Journal & Risk Engine** | Complete the risk workflow and journaling experience. | `/api/trade/plan/{ticker}`, ATR/Kelly sizing, trade/journal storage + exports, Trade Planner UI, partial exit templates (PRD §§3,5F,6). | Trade plan endpoint returns ATR + 2R/3R targets, journaling persistence enabled, weekly performance summaries generated. |
| **Phase 5 – AI Guidance & Platform Hardening** | Layer on AI copilots, scoring, and telemetry hardening. | AI Commentary, AI Trade Advisor, AI Journal Coach, Legend Score, AI Council concept, macro/sentiment overlays, CI/CD + observability upgrades (PRD §§5C,5F,8–10,12). | GPT/Claude commentary in app, Legend Score surfaced, telemetry dashboards + rate-limit monitoring online. |

## Phase Details

### Phase 1 – Analyze + Universe Baseline
- **Backend**: `/api/analyze`, `/health`, `/version`, Chart-IMG retries/backoff, Redis cache, seeded universe ingestion job.
- **Frontend**: Analyze tab with async fetch, loading states, intel panel, Chart-IMG render gated on request success, header `BUILD <sha>`.
- **Data & Ops**: TwelveData→Finnhub→AlphaVantage fallback, log key presence, capture Chart-IMG diagnostics, CI running smoke + contract tests.
- **Definition of Done**: Analyze responses under 2s on common tickers, tests green in CI, universe tables populated with sector metadata.

### Phase 2 – Scanners & Top Setups
- **APIs**: `/api/scan`, `/api/scan/universe`, `/api/scan/sector/{sector}`, `/api/top-setups?limit=10` with Redis caching (24h TTL) and bucketed payloads.
- **Scheduling**: Cron at 4:05 PM ET + Sunday refresh. Rate-limit aware batching (chunks of 25) with exponential backoff + jitter.
- **UI & Distribution**: Pattern Scanner and Top Setups tabs consume cached data, Telegram/Sheets digests pull the same payloads, cards include quick Analyze & chart links.
- **Status Update (Nov 2025)**: Advanced detectors for wedges, triangles, and head & shoulders patterns now power both scanners and Top Setups, closing the roadmap item for “non-VCP” structures.
- **Definition of Done**: 600-symbol scans finish in <20 minutes, cached JSON drives both UI tabs, telemetry logs batch size/runtime/cache hits.

### Phase 3 – Watchlist Intelligence & Market Internals
- **Watchlist**: CRUD UI + API, states (Watching/Breaking Out/Triggered), re-analyze actions, Redis/Postgres persistence bridge.
- **Alerting**: Five-minute monitoring loop during market hours, toast feed, Telegram/email/SMS hooks, `/scan`, `/plan`, `/watchlist` bot commands, alert history log per ticker.
- **Market Internals**: Breadth metrics, sector heatmap, VIX, indices, multi-timeframe confirmation heatmap + confidence boosts. _Status (Nov 2025): TradingView ticker tape, market overview, SPX + ETF heatmaps, screener, economic calendar, and SPY/QQQ/IWM/VIX minis are live on the dashboard, with Playwright coverage capturing each widget._
- **Definition of Done**: Alerts flow to dashboard + Telegram in <60 seconds with audit trail, Market Internals tab lazy-loads widgets, multi-TF overlay live in Analyze + dedicated tab.

### Phase 4 – Trade Plans, Journal & Risk Engine
- **Endpoints**: `/api/trade/plan/{ticker}` with ATR sizing, fixed % risk, Kelly-lite multiplier, partial exits (2R/3R) and journal prompts.
- **Data**: PostgreSQL `trades`, `journal_entries`, Sheets/Notion export jobs, weekly stats summarizer powering dashboards + `/stats` command.
- **UX**: Trade Planner tab for account inputs, AI plan suggestions, journaling notes, and export controls.
- **Definition of Done**: Trade plan endpoint exercised in CI, planner UI persists entries, weekly performance digest automatically posted.

### Phase 5 – AI Guidance & Platform Hardening
- **AI Modules**: GPT/Claude commentary + conviction score, AI Trade Advisor for alternates, AI Journal Coach insights, AI Council concept for ensemble voting.
- **Analytics**: Legend Score composite, macro & sentiment overlays (AAII, VIX, put/call), portfolio dashboards, market briefings.
- **Platform**: Expanded CI (lint + pytest), telemetry dashboards, rate-limit monitoring, automation of auto setup reports.
- **Definition of Done**: AI commentary + Legend Score visible in UI, macro overlays shipping, CI/CD adds linting + deployment tagging, observability dashboards live.

## Swing Trader Critical Features

Pulling from the master improvement plan and swing-trader feature roadmap, these initiatives span multiple phases and should always have active owners:
- **Real-Time Pattern Alerts (Phases 3–4)**: 5-minute watchlist polling, R:R logging, Telegram/email/SMS routing, dashboard toast feed, alert history with retries.
- **Multi-Timeframe Confirmation (Phases 3–5)**: Weekly/Daily/4H/1H detectors, confidence boosts, Analyze + Multi-TF tabs kept in sync, heatmap visual plus boost badges.
- **Entry/Exit Management (Phase 4)**: Trade journal CRUD, ATR-based sizing, partial exits, endpoints `/api/trades/create|open|close`, expectancy reporting.
- **Universe Scanner & Scheduled Jobs (Phases 1–2)**: Weekly symbol refresh, post-close scan, rate-limit + caching discipline, sector-level scans, top setups digest.
- **Watchlist & Bot Commands (Phase 3)**: CRUD with statuses, Telegram `/watchlist`, `/plan`, `/scan` orchestration, triggered alerts piped into Sheets + Redis audit logs.
- **TradingView Symbol Lab (Phase 3)**: `/tv?tvwidgetsymbol=` route exposes ticker tape, symbol info, advanced chart with EMA21/SMA50/RSI, fundamentals, technicals, news, and Chart-IMG snapshots; Analyze/Scanner/Watchlist/Top Setups provide `TV` actions that open the lab in a new tab.

## Cross-Cutting Workstreams
- **Observability & Telemetry (PRD §8)**: Structured logs for Chart-IMG, scan durations, alert emissions; metrics exported to Grafana/Prometheus; error budget reviews every phase.
- **Data Backbone & Scheduling (PRD §5D)**: Universe ingestion, sector tagging, Redis/Postgres synchronization, scheduler health checks, retry/jitter strategy documented.
- **Security & Secrets Hygiene**: Railway env audit, no keys client-side, smoke tests ensure missing key warnings are surfaced.
- **Docs & Alignment**: Keep `Legend_AI_PRD.md`, MVP spec, and roadmap annotated per release; every sprint ties to a row in the phase overview table.

## Tracking & Reporting
- **Sprint Rituals**: Each PR/Sprint references its phase + acceptance criteria, and updates the “exit criteria” column when completed.
- **KPIs**: Monitor Analyze <2s, Scan 100 tickers <15s, Alert latency <60s, Universe scan <20 min, Error rate <1% per day.
- **Change Log**: Append notable milestones (feature flags, AI upgrades, tooling) at the top of the doc as they ship to maintain historical context.

Track progress by aligning every deliverable to its phase row while continuously investing in the cross-cutting workstreams.
