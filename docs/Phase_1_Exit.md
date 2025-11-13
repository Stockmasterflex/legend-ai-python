# Phase 1 Exit Checklist

Direct snapshot of `docs/Legend_AI_Roadmap.md:5-21`. QA should tick every box before declaring Phase 1 complete.

## Release Table Items (`docs/Legend_AI_Roadmap.md:9-13`)
- [ ] Objective satisfied: end-to-end analyze workflow shipped plus seeded universe data.
- [ ] Key modules live: `/api/analyze`, Chart-IMG integration, Analyze tab, `/version` + `/health`, S&P 500 + NASDAQ 100 ingestion (PRD §§3,5A,5D,12).
- [ ] Exit metrics met: analyze response <2 s, build SHA visible in UI, seeded universe tables available, `tests/test_analyze_contract.py` + smoke suite green.

## Backend Scope (`docs/Legend_AI_Roadmap.md:18`)
- [ ] `/api/analyze`, `/health`, `/version` deployed with Chart-IMG retries/backoff.
- [ ] Redis cache wired for analyzer payloads (1 h TTL) and actively serving hits.
- [ ] Universe ingestion job running on schedule with latest ticker set.

## Frontend Scope (`docs/Legend_AI_Roadmap.md:19`)
- [ ] Analyze tab implements async fetch, loading states, intel panel, and Chart-IMG render gated on request success.
- [ ] Header displays `BUILD <sha>` with cache-busted assets (`dashboard.js?v={{ build_sha }}`) to unblock deployments.

## Data & Ops Scope (`docs/Legend_AI_Roadmap.md:20`)
- [ ] TwelveData→Finnhub→AlphaVantage fallback verified in logs.
- [ ] Key presence logged at startup (TwelveData, Finnhub, AlphaVantage, Chart-IMG).
- [ ] Chart-IMG diagnostics captured (status, duration, retry count).
- [ ] CI runs smoke + contract tests on every merge.

## Definition of Done (`docs/Legend_AI_Roadmap.md:21`)
- [ ] Analyzer responses under 2 s on high-volume tickers (spot-check AAPL, TSLA, NVDA).
- [ ] CI (`pytest -q tests` + smoke) green in GitHub Actions/Railway.
- [ ] Universe tables populated with sector metadata and queried successfully by the analyzer.
