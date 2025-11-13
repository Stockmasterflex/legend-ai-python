# Legend AI Changelog Template

Legend AI follows the [Keep a Changelog](https://keepachangelog.com/) style so every release calls out what shipped, how it was verified, and where to look for supporting evidence. Copy the scaffold below to log each deployment and always keep the most recent release at the top of the file.

## How to Use This Template
- **Version tag**: Use `v{{build_sha}} – YYYY-MM-DD` exactly (per release build + date). Example: `v3ab12f1 – 2024-05-13`.
- **Source of truth**: Cross-link the MVP scope (`docs/Legend_AI_MVP.md`) and the corresponding roadmap phase (`docs/Legend_AI_Roadmap.md`) inside each entry so readers know which acceptance criteria moved.
- **Verification**: For every section, call out the test, log snippet, or dashboard URL that proves the change met the guardrails in `docs/RUNBOOK_CI_Smoke.md` and `docs/RUNBOOK_Deploy.md`.

## Release Entry Scaffold

```
## v{{build_sha}} – YYYY-MM-DD

### Added
- ...

### Changed
- ...

### Fixed
- ...

### Performance
- ...

### Telemetry
- ...

### Verification
- `pytest -q tests`
- `Railway logs --service legend-ai-api --follow`
- Links to sprint tracker rows / PRs / dashboards
```

> Tip: mirror the order of the columns in `docs/Release_Templates/Sprint_Tracker.csv` so contributors can jump between the changelog, sprint artifacts, and roadmap exit criteria without re-parsing context.

## Unreleased

### Added
- Flag-gated `/api/scan` with sector filtering, missing-OHLC placeholders, rule-failure tracing, and per-request telemetry (duration labels, cache-aware counters, detector summaries).
- `slo_report.py` that reads `artifacts/metrics.prom` and prints the p95 latency for analyze/scan plus the combined error rate so CI job summaries call out the SLO.
- `ops/grafana/legend_phase2.json` plus `ops/bin/health_gate.sh` to give operators turnkey dashboards + mobile-ready sanity checks.

### Changed
- Centralized ATR/RS/MA helpers, unified logging metadata (route/build SHA/flag), and rounded up scan/analyze telemetry (histograms/counters/summaries).
- Added docs for the scanner API contract, VCP grading, CI telemetry, observability playbooks, and the new Grafana/SLO workflows.

### Telemetry
- Scan latency histograms now expose `{status,universe_size}`, detector runtimes are summarized per pattern, and cache hits/misses can be sliced by `name` so Grafana panels can report hit ratio + error-budget in `ops/grafana/legend_phase2.json`.

### Verification
- `pytest -q tests/test_scan_contract.py tests/test_vcp_detector.py tests/test_scanner_service.py`
