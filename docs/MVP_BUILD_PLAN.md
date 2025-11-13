# Legend AI MVP Build Plan

This document tracks the remaining work items needed to realize the MVP outlined in `docs/Legend_AI_PRD.md`. The goal is to incrementally implement backend contracts, Chart-IMG rendering, frontend tabs, and supporting tooling. Each section below highlights the current status and next steps.

## 1. Analyze API + Chart Rendering (Core contract)

- **Status**: `/api/analyze` already returns OHLCV, indicators, patterns, plan, and optional `chart_url`. It sanitizes NaN/Inf values and caches results. Tests cover the contract via `tests/test_analyze_contract.py`.
- **Next steps**:
  - Ensure Chart-IMG calls use robust symbol detection and logging (already improved).
  - Confirm `chart_url` populates when the API key is configured and fallback gracefully when missing.
  - Expand unit tests to cover divergence detection, plan generation, and failure modes (e.g., insufficient data).

## 2. Dashboard Frontend (Analyze experience)

- **Status**: The Analyze tab uses vanilla JS to fetch `/api/analyze`, render the intel panel, and display a chart snapshot. Tabs switch without mounting TradingView by default. The UI already includes build/version info.
- **Next steps**:
  - Wire Pattern Scanner, Top Setups, Market Internals, and Watchlist tabs to real data endpoints (or guarded placeholders).
  - Improve styling, spacing, and responsive behavior based on the PRD.
  - Add accessible tab controls with keyboard interactions and history persistence.

## 3. Scanning + Top Setups (Batch workflows)

- **Status**: `app/api/universe.py` exposes scan endpoints; there are services for Universe scanning and caching. However, the UI integration is still placeholder text.
- **Next steps**:
  - Build UI cards displaying scanned setups, linking to Analyze for each ticker.
  - Add scheduled job or button to refresh Top Setups daily.
  - Store scan metadata (timestamps, score) for later review.

## 4. Market Internals + Watchlist

- **Status**: Templates include market internals and watchlist sections, but many rely on stubbed or non-existent data.
- **Next steps**:
  - Connect watchlist CRUD routes to persistent storage (file fallback already exists; consider Redis/Postgres later).
  - Populate Market Internals via existing services or embed TradingView widgets (ticker tape, heatmap, etc.).
  - Ensure each tab fetches data only when visible (lazy loading).

## 5. Observability, Logging, and CI

- **Status**: Startup logs report key presence; Chart-IMG logs now include symbol/interval/status. CI runs pytest via GitHub Actions.
- **Next steps**:
  - Capture Chart-IMG responses (especially failures) in a structured log or telemetry service.
  - Add smoke tests for `/health`, `/version`, and `/api/analyze`.
  - Ensure instrumentation for deployment verification (e.g., `build_sha` in headers, cache-busted scripts).

## 6. Documentation and Roadmap

- **Status**: PRD and build plan exist under `docs/`. MVP spec and architecture docs are also in place.
- **Next steps**:
  - Keep this plan updated as features are built or deferred.
  - Document any additional APIs or admin commands introduced along the way.

---

### Implementation Approach

1. **Backend first**: finalize `/api/analyze`, `chartimg`, `/version`, and watchlist persistence. Include tests for each contract.
2. **Dashboard polish**: get each tab wired, ensure the Analyze image only appears after success, and maintain accessible tabs.
3. **Testing & DevOps**: run pytest, CI, and deployment verification. Add smoke tests or scripts if needed.

Each set of changes will target a dedicated branch/PR so we can review incrementally while working toward the full MVP.
