# Legend AI MVP

This is the consolidated MVP definition drawn from `Legend_AI_PRD.md`, the master improvement plan, and the prior MVP specs. It lists the core capabilities that must be in place before we graduate past Phase 1.

## Core Services

| Capability | Description | Status |
|------------|-------------|--------|
| `/api/analyze` | Analyze a ticker (OHLCV, indicators, Minervini/Weinstein/VCP, ATR plan) and emit a Chart-IMG snapshot. | ✅ contract in place; tests exist |
| `/api/scan` & `/api/scan/universe` | Batch scan SP500/NASDAQ100 with filters, caching, and ranking. | 🚧 Server has endpoints; UI stubbed |
| Chart-IMG rendering | Server-side Chart-IMG request with EMA/SMA/RSI studies plus plan drawings. | 🛠️ Diagnostics + fallback improved |
| Watchlist CRUD | Save/remove tickers with reason/status and feature in dashboard & Telegram. | 🟡 File fallback exists; needs persistence |
| `/version` + build SHA | Expose short commit/build value and include in UI for cache busting. | ✅ Implemented |
| `/health` + startup logs | Report service health and key presence (Chart-IMG/TwelveData). | ✅ Logging + endpoint ready |

## Dashboard Experience

- **Analyze Tab**: form, async fetch, loading state, chart image, intel panel with pattern grades, Plan, RS distances, R-multiple.
- **Tabbed Layout**: accessible tab controls, unsubscribed chart canvas when leaving Analyze.
- **Pattern Scanner**: placeholder for scanned setups with quick Analyze links.
- **Top Setups**: daily ranked list to highlight best setup(s).
- **Market Internals**: includes ticker tape + optional embedded widgets (ticker tape, heatmap, sector overview).
- **Watchlist**: list + filter + add/remove + re-analyze actions.
- **Build Info**: header shows `BUILD <sha>` and JS is cache-busted.

## Key Non-Functional Targets

- Analyze response time < 2s for common tickers.
- Chart-IMG requests use exponential backoff (max 4 tries), log statuses, and handle missing keys gracefully.
- CI runs `pytest -q tests` with no `|| true`.
- Smoke tests cover `/health`, `/version`, `/api/analyze`, `chart_url` presence.
- Logging includes Chart-IMG symbol/status, Be aggressive about not exposing secrets.

## Next Milestones (from Master Plan)

1. Universe data ingestion, scheduled scans, and caching (24h TTL, per-sector scanning).
2. Watchlist monitor + Telegram alert workflow (every 5 min), plus market internals metrics.
3. Trade plan generator (ATR sizing, risk/reward) + journal/export.
4. AI commentary/responses, Legend score, and automation (Sheets/Notion exports).

Once these are in place, we can mark the MVP complete and plan Phase 2+ expansions.
