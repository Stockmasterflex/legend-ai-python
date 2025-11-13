# RUNBOOK — Chart-IMG Integration

**References**: `docs/Legend_AI_MVP.md:15` (Chart-IMG acceptance), `docs/Legend_AI_MVP.md:31-33` (guardrails on retries/logging/CI), `docs/Legend_AI_Roadmap.md:9` and `docs/Legend_AI_Roadmap.md:18-21` (Phase 1 backend + ops expectations).

This runbook keeps the Chart-IMG overlay pipeline healthy so `/api/analyze` responses always return the annotated `chart_url` promised in the MVP. Follow these steps whenever rotating keys, debugging image output, or responding to throttling incidents.

## 1. Pre-flight Checks
1. **Confirm credentials**  
   ```bash
   railway variables get CHARTIMG_API_KEY
   grep CHARTIMG_API_KEY .env
   ```
   Values must match; per `README.md:59` the key name is `CHARTIMG_API_KEY`.
2. **Validate Redis reachability** (rate limiting + usage counters live there): `redis-cli -u "$REDIS_URL" PING`.
3. **Open logs** to watch retries/backoff, as required by `docs/Legend_AI_MVP.md:31-33`:  
   ```bash
   tail -f logs/app.log | rg chart-img
   railway logs --service legend-ai-api --follow
   ```

## 2. Rotate the Chart-IMG Key
1. Generate/retrieve the new key in the Chart-IMG dashboard.
2. **Update Railway** (production):  
   ```bash
   railway variables set CHARTIMG_API_KEY=sk_live_newvalue
   railway redeploy
   ```
3. **Update local dev**: edit `.env`, restart `uvicorn`, and run `source .env && export $(cut -d= -f1 .env)`.
4. **Invalidate cached secrets**:  
   ```bash
   redis-cli -u "$REDIS_URL" DEL chartimg:burst chartimg:usage:$(date -u +%Y%m%d)
   ```
   This ensures the new key starts clean and the rate-limiter counters match the fresh quota.
5. **Document the rotation** in `CHANGELOG.md` (Added/Telemetry) and in the current sprint row of `docs/Release_Templates/Sprint_Tracker.csv`.

## 3. Test Image Output End-to-End
1. **Direct API probe** (confirms key works before touching Legend AI):  
   ```bash
   curl -s https://api.chart-img.com/v2/tradingview/advanced-chart \
     -H "x-api-key: $CHARTIMG_API_KEY" \
     -H "content-type: application/json" \
     -d '{"symbol":"NASDAQ:AAPL","interval":"1D","width":800,"height":500,"studies":[{"name":"Moving Average Exponential","input":{"length":21,"source":"close"}}]}'
   ```
   Expect `{"url": "...png", "etag": "...", "expire": "..."}`.
2. **Legend AI smoke**: with FastAPI running, hit `/api/analyze` and assert `chart_url` is populated (ties back to the contract in `tests/test_analyze_contract.py`):  
   ```bash
   curl -s "http://localhost:8000/api/analyze?ticker=AAPL&tf=daily" | jq '.chart_url'
   ```
   Empty result indicates fallback mode or missing annotations.
3. **CI confirmation**: run `pytest tests/test_analyze_contract.py -k chart_url -q` to guard the acceptance in `docs/Legend_AI_MVP.md:15`.

## 4. Retry/Backoff Behavior
- `app/services/charting.py` enforces **10 req/sec** bursts plus **500 calls/day** via Redis counters (`chartimg:burst`, `chartimg:usage:YYYYMMDD`). When counters overflow, `fallback_mode` becomes `True` and `_get_fallback_url` returns a TradingView link—acceptable only temporarily per `docs/Legend_AI_Roadmap.md:18-20`.
- **Backoff tuning**: if you see `⚠️ Chart-IMG daily quota exhausted` in logs, pause automation, increase cache hit rate (see `cache.set_chart` in `app/api/charts.py`), and communicate in the sprint tracker.
- **Manual reset**: clearing `chartimg:burst`/`chartimg:usage:*` releases stuck tokens once you verify Chart-IMG has reset its counters.

## 5. Incident Recovery
1. **Symptoms**: `/api/analyze` lacks `chart_url`, logs show HTTP 4xx/429, or latency exceeds the 1.5 s limit noted in `docs/Legend_AI_MVP.md:29-31`.
2. **Immediate actions**:
   - Verify key status (Section 2).
   - Check Redis quota keys (`redis-cli ... GET chartimg:usage:$(date -u +%Y%m%d)`).
   - Review Railway logs for upstream HTTP status.
3. **Fallback messaging**: Ensure the UI displays the fallback notice promised in `docs/Legend_AI_MVP.md:43`. If not, create a ticket and annotate `CHANGELOG.md`.
4. **Post-incident**: Record cause, duration, and mitigation in `CHANGELOG.md` (Telemetry + Fixed) and update `docs/RUNBOOK_Deploy.md` if deployment steps changed.

By following the steps above, the Chart-IMG overlay remains compliant with the MVP contract and the Phase 1 backend/ops scope outlined in the roadmap.
