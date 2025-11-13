# Launch Readiness Checklist

Mirrors `docs/Legend_AI_MVP.md:41-47` so Phase 1 sign-off stays anchored to the MVP definition. Re-check every item before promoting a build.

- [ ] `/api/analyze`, `/health`, `/version` passing smoke suite locally and in CI.
- [ ] Chart-IMG key verified, retries/backoff observed in logs, fallback messaging shown if key missing.
- [ ] Analyze tab renders full intel panel + chart, Build SHA header displayed, JS cache busting confirmed.
- [ ] Universe ingestion job populated with current tickers/sector tags; analyzer queries the dataset.
- [ ] Watchlist CRUD accessible from UI + API with persistence outside process memory.
- [ ] Redis + PostgreSQL connections validated, secrets stored in Railway variables, no keys exposed client-side.
