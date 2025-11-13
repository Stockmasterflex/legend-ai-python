# RUNBOOK — Observability & Local Telemetry

**Audience:** Engineers spinning up Legend AI locally who need to inspect logs, metrics, and Grafana dashboards in under five minutes.

---

## 1. Structured JSON Logs

1. Start the API (any `uvicorn`/Railway entry point). Logs are now JSON objects emitted by `StructuredLoggingMiddleware`.
2. Each request log contains:
   ```json
   { "ts": "...", "event": "GET /api/analyze", "symbol": "TSLA", "interval": "1day", "status": 200, "duration_ms": 512.4, "cache_hit": false, "build_sha": "abc1234" }
   ```
3. Logs now include `route` and `flag_scanner_enabled`, so downstream parsers can break metrics by flag state + endpoint.
4. To pretty-print locally:
   ```bash
   uvicorn app.main:app --reload | jq -r 'select(.event != null)'
   ```
   (`jq` is optional; without it you still get raw JSON per line.)

> Never mutate response payloads—the middleware hooks in before/after requests so behavior stays identical.

---

## 2. Prometheus Metrics

1. With the API running, hit `http://localhost:8000/metrics`.
2. Confirm the required series exist:
   - `analyze_request_duration_seconds_bucket` / `_sum` / `_count`
   - `chartimg_post_status_total{status="success|error"}`
   - `cache_hits_total`, `cache_misses_total`
   - `scan_request_duration_seconds_bucket{status,universe_size}` plus `_sum`/`_count` so latency panels can be broken out by universe size.
   - `detector_runtime_seconds{pattern="VCP"}` (summary count/sum) for tracking detector runtimes.
   - `cache_hits_total{name="scan"}` / `cache_misses_total{name="scan"}` (and `name="analyze"`) so Grafana can calculate cache hit ratios for each flow.
3. Trigger traffic to populate metrics (e.g., `curl 'http://localhost:8000/api/analyze?ticker=TSLA&tf=daily'`).

---

## 3. Local Prometheus + Grafana Stack

1. Build/run the observability stack (Grafana + Prometheus only; it scrapes the API running on your host):
   ```bash
   docker compose -f ops/observability.yml up
   ```
2. Prometheus is available at `http://localhost:9090` and already scrapes `host.docker.internal:8000/metrics`.
3. Grafana is at `http://localhost:3000` (admin/admin by default). Add Prometheus (`http://prometheus:9090`) as a data source and import any dashboard:
   - Fast check: create a new panel with `analyze_request_duration_seconds_count`.
4. Stop the stack with `Ctrl+C` or `docker compose -f ops/observability.yml down`.

---

## 4. Quick Health Checklist

| Item | Command | Expected |
| --- | --- | --- |
| API health | `curl http://localhost:8000/health` | `"status": "healthy"` and JSON response unchanged |
| Metrics | `curl http://localhost:8000/metrics \| head` | Text exposition format with required series |
| Logs | observe server output | JSON lines including `build_sha` field |
| Grafana | visit `http://localhost:3000` | Login succeeds, Prom datasource reachable |

If any check fails, restart the API, then the observability stack, and re-test. Review `ops/bin/check_env.py` to confirm required secrets exist for upstream APIs when running against real services.

## 5. Grafana — Phase 2 telemetry

Import `ops/grafana/legend_phase2.json` into Grafana to unlock the Phase-2 telemetry dashboard. The JSON already wires `Prometheus` as the data source and shows panels for:

- p50/p95 latency for `/api/analyze` (`interval="1day"`) and `/api/scan` (`status="ok"`) using the new histograms.
- Detector runtime for `pattern="VCP"` via `detector_runtime_seconds`.
- Cache hit ratios by service (`name="analyze"` / `name="scan"`) computed from the cache hit/miss counters.
- Daily error budget (`increase(analyze_errors_total[1d]) + increase(scan_errors_total[1d])` vs the request counts).

Use Grafana’s import dialog, point it to `ops/grafana/legend_phase2.json`, and share the resulting dashboard with the rest of the team.
