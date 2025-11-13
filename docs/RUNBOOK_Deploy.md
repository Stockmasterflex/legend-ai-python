# RUNBOOK — Deploying to Railway

**References**: `docs/Legend_AI_Roadmap.md:9` (Phase 1 exit criteria) + `docs/Legend_AI_Roadmap.md:18-21` (backend/data/ops scope), `docs/Legend_AI_MVP.md:41-47` (Launch readiness + Redis/Postgres verification), `DEPLOYMENT_STATUS.md:347-374` (logs & troubleshooting).

Use this checklist each time you push a Phase 1 build so Redis, Postgres, and Chart-IMG stay aligned across local + Railway environments.

## 1. Prep & Tooling
1. Install the Railway CLI: `npm i -g @railway/cli`.
2. Authenticate once: `railway login`.
3. Link the repo to the project: `railway link --project legend-ai`.

## 2. Provision Services (one-time per project)
1. **Postgres**: `railway service add postgres`. Record the generated `DATABASE_URL`.
2. **Redis**: `railway service add redis`. Record the `REDIS_URL`.
3. **FastAPI service**: `railway up` creates/builds the app container.
4. Confirm both data stores are reachable (mirrors MVP line 47):  
   ```bash
   railway run python - <<'PY'
   import redis, os
   redis.Redis.from_url(os.environ["REDIS_URL"]).ping()
   print("Redis OK")
   import psycopg2
   psycopg2.connect(os.environ["DATABASE_URL"]).close()
   print("Postgres OK")
   PY
   ```

## 3. Configure Environment Variables
Set the mandatory keys before every deploy (see `README.md:59` and MVP guardrails):
```bash
railway variables set \
  BUILD_SHA=$(git rev-parse HEAD) \
  CHARTIMG_API_KEY=... \
  TWELVEDATA_API_KEY=... \
  OPENROUTER_API_KEY=... \
  TELEGRAM_BOT_TOKEN=... \
  SECRET_KEY=... \
  REDIS_URL=${REDIS_URL} \
  DATABASE_URL=${DATABASE_URL}
```
Add any feature flags or temporary diagnostics here as well, and mirror them in `.env` so CI + local runs are consistent.

## 4. Deploy Workflow
1. **Run tests locally** (per `docs/RUNBOOK_CI_Smoke.md`) and update `CHANGELOG.md`.
2. **Tag the release** with the build SHA for traceability in headers:  
   ```bash
   export BUILD_SHA=$(git rev-parse --short HEAD)
   ```
3. **Deploy**: `railway up --service legend-ai-api`.
4. **Verify**:
   - `railway logs --service legend-ai-api --follow` (watch for Chart-IMG retries per roadmap data/ops line 20).
   - Hit `/version` to confirm `BUILD <sha>` is visible (`curl https://$RAILWAY_PUBLIC_DOMAIN/version`).
   - Run `railway run pytest tests/test_smoke.py -q` if the service allows ad-hoc jobs.

## 5. Common Pitfalls
- **Missing env vars** → `/health` returns 500 because Redis/Postgres secrets are absent; cross-check `docs/Legend_AI_MVP.md:47`.
- **Chart-IMG quota** → Deploy introduces higher traffic and hits the 10 rps cap; follow `docs/RUNBOOK_ChartIMG.md`.
- **Stale build SHA** → UI header still shows previous SHA; ensure `BUILD_SHA` env var updated before deploy.
- **CI skipped** → GitHub Actions bypass means the roadmap exit criterion (`test_analyze_contract.py` green) isn’t satisfied—block release.

## 6. Rollback Steps
1. Identify the last known good deployment: `railway status --service legend-ai-api`.
2. Roll back: `railway rollback --service legend-ai-api <deployment_id>`.
3. Re-run smoke tests against the rolled-back instance (`curl https://$RAILWAY_PUBLIC_DOMAIN/health` and `pytest tests/test_smoke.py -q` locally with the corresponding commit).
4. Add a `Fixed` entry to `CHANGELOG.md` and annotate `docs/Release_Templates/Sprint_Tracker.csv` so the team knows which sprint absorbed the rollback.

## 7. Post-Deploy Verification (Phase 1 exit proof)
- Analyzer responses <2 s (`/api/analyze?ticker=AAPL&tf=daily | jq '.timings'` if instrumented).
- `chart_url` populated (ensures Chart-IMG scope from `docs/Legend_AI_MVP.md:15`).
- Seeded universe tables accessible (`redis-cli -u "$REDIS_URL" HLEN universe:SP500` should return >0).
- `/health`, `/version`, and `/api/analyze` smoke suite green (ties to `docs/Legend_AI_MVP.md:41-46`).

Document completion in the sprint tracker row and link to the relevant runbook sections for quick auditing.

## From phone

1. Grab the build URL (e.g., `https://{RAILWAY_PUBLIC_DOMAIN}`) and run the emergency health gate script:
   ```bash
   API_BASE=https://{RAILWAY_PUBLIC_DOMAIN} ops/bin/health_gate.sh
   ```
   The script fires `/health`, `/version`, and `/api/scan?limit=1` so you get instant confidence that the scan route is responsive even on a mobile network.
2. Review the output for HTTP 200 responses; failing requests are a strong signal to block the release and inspect the log stream before touching anything else.
