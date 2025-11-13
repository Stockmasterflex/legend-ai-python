# RUNBOOK — CI Telemetry & Artifacts

**Audience:** Contributors monitoring GitHub Actions CI for Legend AI. Follow these steps whenever a build fails or you need proof of runtime/test health. Total read time: <5 minutes.

---

## 1. Pipeline Overview

1. **Install** dependencies via `pip`.
2. **Env Sanity (`ops/bin/check_env.py`)** — validates required API keys (booleans only). Missing vars fail the job before tests start.
3. **Tests with Telemetry** — executes `pytest --durations=25 tests`, recording:
   - wall-clock duration (`artifacts/test-summary.json`)
   - raw pytest output (`artifacts/pytest.log`)
   - Prometheus snapshot of in-process metrics (`artifacts/metrics.prom`)
4. **Artifact Upload** — `legend-ci-telemetry` artifact is retained even if tests fail.

---

## 2. Inspecting Artifacts

1. Open the CI run → **Artifacts** → download `legend-ci-telemetry`.
2. Files inside:
   - `pytest.log`: search for stack traces or failed tests; includes built-in pytest duration table.
   - `test-summary.json`: quick JSON payload with start/end epoch seconds and total duration.
   - `metrics.prom`: scrapeable text exposing `analyze_request_duration_seconds`, `chartimg_post_status_total`, `cache_hits_total`, and `cache_misses_total` as they existed during tests. Useful for spotting regressions (e.g., rising error counts).

---

## 3. SLO Report

1. After the `Test with telemetry artifacts` step finishes, run:
   ```bash
   python slo_report.py --metrics-file artifacts/metrics.prom
   ```
   The script prints p95 latency for `/api/analyze`, p95 for `/api/scan`, and the overall error rate so CI logs can call out whether the new telemetry gate passed.
2. Add the printed p95 and error-rate lines to the job summary or release notes for easy auditing.

## 4. Common Tasks
| Goal | Action |
| --- | --- |
| Env failure | Check the `Verify telemetry env` step output to see which boolean flipped to `false`; add the missing secret to repo/org settings. |
| Slow tests | Compare `duration_seconds` across runs (a diff of >20% warrants investigation). |
| Analyze/chartimg regressions | Parse `metrics.prom` (or import into Prometheus) to view histogram/counter values captured during CI. |

---

## 5. Handy Commands

Locally reproducing CI telemetry:

```bash
python ops/bin/check_env.py           # ensure secrets exist
pytest --durations=25 tests | tee artifacts/pytest.log
python - <<'PY'
from prometheus_client import generate_latest
import pathlib
import app.telemetry.metrics  # ensures collectors are loaded
pathlib.Path("artifacts/metrics.prom").write_bytes(generate_latest())
PY
python slo_report.py --metrics-file artifacts/metrics.prom
```

Upload the artifacts with `gh run upload-artifact legend-ci-telemetry artifacts` if you need to preserve the local repro in GitHub.
