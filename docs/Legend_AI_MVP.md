# Legend AI MVP

This is the consolidated MVP definition drawn from `docs/Legend_AI_PRD.md`, the master improvement plan, and prior MVP specs. It lists the non-negotiable capabilities that must be in place before we exit Phase 1 and unlock the Phase 2 scanner work.

## MVP Outcomes
- Deliver professional-grade `/api/analyze` responses with deterministic pattern grading, ATR-based plans, and Chart-IMG overlays.
- Stand up the Analyze-first dashboard experience (tab framework, intel panel, build info) so traders can self-serve insights.
- Prove operational readiness: health/version endpoints, key diagnostics, CI + telemetry, and seeded universe data for follow-on scanners.

## Functional Scope & Acceptance

| Capability | Description | Status | Acceptance Criteria (PRD refs) |
|------------|-------------|--------|--------------------------------|
| `/api/analyze` | OHLCV ingestion (TwelveData→Finnhub→AlphaVantage), indicators, Minervini/Weinstein/VCP classifiers, ATR plan payload. | ✅ contract + tests exist | JSON matches schema, analyze <2s, returns `chart_url`, RS metrics, rule failures (PRD §§3,5A,9). |
| Chart-IMG rendering | Server-side Chart-IMG v2 request with EMA(21)/SMA(50)/RSI(14)/Volume + entry/stop/target drawings, exponential backoff. | ✅ retries/logging wired | Errors logged with symbol/interval/status, trimmed annotations (≤2) present, `chart_url` embedded in UI (PRD §5A). |
| `/health` + `/version` | Report runtime health, key presence, build SHA for UI cache busting. | ✅ live | Smoke tests for `/health`, `/version`, build tag shown in header (PRD §§4,6). |
| Universe ingestion | Seed S&P 500 + NASDAQ 100 with sector tags, stage data for later scans. | ✅ seeded snapshot live | Nightly job populates Redis/Postgres snapshot, metadata accessible to analyzer (PRD §5D). |
| Watchlist CRUD (file → Redis bridge) | Basic add/remove/list with reason + status used by Analyze tab + Telegram stubs. | ✅ Redis bridge live | CRUD endpoints exist, data persisted outside process memory, re-analyze action wired (PRD §§3,5E). |
| Dashboard Analyze tab | Form, async fetch, loading state, intel cards (patterns, rule fails, RS rank, MA distances, plan summary). | ✅ UI shipped | Chart renders only after successful API call, tabs unload charts, `BUILD <sha>` header + cache-busted JS (PRD §6). |
| Logging + CI | Startup logs of key presence, Chart-IMG POST telemetry, pytest + smoke suite in CI. | ✅ base logging | CI blocks on failures, logs capture symbol/interval/status/duration, no secrets leak (PRD §8). |

## Dashboard & UX Commitments (Phase 1 scope)
- **Analyze Tab**: canonical entry point; includes ticker/timeframe inputs, loading skeleton, Chart-IMG snapshot, Plan + intel panel with pattern grades, rule failures, RS rank, MA distances, and R-multiple summary.
- **Tabbed Layout**: Jinja2 + vanilla JS tabs for Analyze, Pattern Scanner (stub), Top Setups (stub), Market Internals (stub), Watchlist; non-active tabs release Chart-IMG resources.
- **Watchlist Panel**: Minimal CRUD plus “Analyze Again” CTA using the MVP watchlist service.
- **Build Info & Versioning**: Header `BUILD <sha>` tag + `?v={{ build_sha }}` cache busting for `dashboard.js` as required in PRD §6.

## Operational Guardrails
- Analyze SLA <2s, Chart-IMG render <1.5s, error rate <1% 500s/day (PRD §9).
- Redis caching on analyzer outputs (1h TTL) to manage rate limits; fallback chain metrics logged.
- Chart-IMG, TwelveData, Finnhub, AlphaVantage, OpenRouter keys sourced from Railway variables; CI ensures absence is surfaced.
- Logging captures analyze duration, pattern detections, Chart-IMG POST attempts, and key scheduler events; ready for export to Grafana/Prometheus hooks.
- CI: `pytest -q tests` + smoke tests covering `/health`, `/version`, `/api/analyze` (no `|| true`).

## Data, Scheduling & Integrations
- **Universe Backbone**: Weekly ingestion job with sector tagging, stored in Redis + Postgres for downstream scanners (PRD §5D).
- **Scheduler**: Even at MVP, cron scaffolding exists for nightly ingestion and future scans; logs runtime + retries.
- **Cache Strategy**: Redis for Analyze/scan payloads (1h TTL) and watchlist snapshots; ensures Chart-IMG + data provider rate limits stay green.
- **External Integrations**: Chart-IMG, Telegram bot stubs, Google Sheets export placeholders—wires are in place even if not yet surfaced in UI.

## Launch Readiness Checklist
- [x] `/api/analyze`, `/health`, `/version` passing smoke suite locally and in CI.
- [x] Chart-IMG key verified, retries/backoff observed in logs, fallback messaging shown if key missing.
- [x] Analyze tab renders full intel panel + chart, Build SHA header displayed, JS cache busting confirmed.
- [x] Universe ingestion job populated with current tickers/sector tags; analyzer queries the dataset.
- [x] Watchlist CRUD accessible from UI + API with persistence outside process memory.
- [x] Redis + PostgreSQL connections validated, secrets stored in Railway variables, no keys exposed client-side.

## Next Milestones (Phase 2+ preview)
1. **Scanners & Top Setups**: `/api/scan*` endpoints, cached bucket outputs, Pattern Scanner + Top Setups tabs consuming real data, Telegram/Sheets digests (PRD §12 Phase 2).
2. **Watchlist Monitor & Market Internals**: 5-min alert loop, toast feed, Telegram notifications, breadth metrics, multi-timeframe heatmap (PRD §12 Phase 3).
3. **Trade Planner & Journal**: `/api/trade/plan`, ATR/Kelly sizing, journal storage + exports, Trade Planner UI (PRD §12 Phase 4).
4. **AI Guidance & Legend Score**: GPT/Claude commentary, Legend Score composites, AI council + macro overlays, telemetry dashboards + CI/CD hardening (PRD §12 Phase 5).

MVP completion = every capability in the Functional Scope table meets its acceptance criteria, the launch checklist is satisfied, and the backlog is ready to progress into Phase 2 scanners without rework.
