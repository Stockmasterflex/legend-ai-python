# Legend AI Roadmap

This living roadmap extracts the planned phases from the MVP PRD and maps them to discrete deliverables. Each phase builds on the previous one, keeping the product cohesive while allowing incremental releases.

## Phase 1 – Core Analyze Stack
- Implement `/api/analyze` with OHLCV, indicators, pattern detection (Minervini, Weinstein, VCP), plan, and `chart_url`.
- Build the Analyze tab UI: form, async fetch, intel panel, and chart snapshot rendering.
- Log key presence and Chart-IMG diagnostics; add `/version` and `build_sha` visibility.
- Tighten tests (`test_analyze_contract.py`, smoke suite) and enforce CI.

## Phase 2 – Scanners & Top Setups
- Deliver `/api/scan` and `/api/top-setups` with bucketed results and caching.
- Launch Pattern Scanner tab with ranked cards and direct Analyze links.
- Surface Top Setups as a daily curated list, including quick intel and chart snapshot access.
- Persist scan metadata and integrate with quick alerts (e.g., Telegram stubs).

## Phase 3 – Watchlist & Market Internals
- Provide full watchlist CRUD (server + frontend) with notes, statuses, and re-analyze actions.
- Populate Market Internals tab with breadth metrics, indices, heatmap, and VIX sections.
- Lazy-load tab data and ensure tabs unload charts for performance.
- Improve watchlist persistence via Redis/Postgres bridging.

## Phase 4 – AI Commentary & Guidance
- Introduce AI Commentary module (GPT/Claude via OpenRouter) for convictions and summaries.
- Ship AI Trade Advisor with alternate plans, risk suggestions, and R-multiple coaching.
- Add AI Journal Coach exporting insights to Google Sheets, Notion, or Telegram digests.

## Phase 5 – Platform Expansion & Hardening
- Build Legend Score composites, macro/sentiment overlays, and portfolio dashboards.
- Extend CI/CD: smoke tests, linting, deployment tagging with `build_sha`.
- Document AI Council mode, automated reports, and future automation workflows.

## Swing Trader Critical Features (from MASTER_IMPROVEMENT_PLAN, SWING_TRADER_FEATURE_ROADMAP)
- **Real-Time Pattern Alerts**: Monitor watchlist every minute during market hours, send Telegram/email/SMS alerts when strong patterns appear, log R:R, entry, and stop. Toast notifications and alert history on the dashboard.
- **Multi-Timeframe Confirmation**: Confirm setups across weekly, daily, 4H, and 1H charts; boost confidence when timeframes align. New “Multi-TF Analysis” tab or overlay displays pattern heatmap per timeframe.
- **Entry/Exit Management**: Trade journal, position sizing, ATR-based stops, partial exits; endpoints like `/api/trades/create`, `/api/trades/open`, `/api/trades/{id}/close` track PnL and R multiple over time.
- **Universe Scanner & Scheduled Jobs**: Weekly refresh of S&P 500 + NASDAQ 100 universes, scheduled scan at market close, rate-limiting + caching, deliver top 10–20 setups plus sector scanning endpoints.
- **Watchlist & Alerts**: Full CRUD with states (Watching/Breaking Out/Triggered) and real-time monitoring; integrate with the universe scanner, watchlist-based alerts, and Telegram bot commands (`/watchlist`, `/plan`, `/scan`).

Track progress by aligning each sprint/PR to a roadmap phase while keeping docs updated.
