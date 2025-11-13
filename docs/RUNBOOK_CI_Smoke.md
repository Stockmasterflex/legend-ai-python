# RUNBOOK — CI + Smoke Validation

**References**: `docs/Legend_AI_MVP.md:20` (Logging + CI row), `docs/Legend_AI_MVP.md:33` (pytest + smoke requirement), `docs/Legend_AI_Roadmap.md:9` and `docs/Legend_AI_Roadmap.md:20-21` (Phase 1 exit criteria + Definition of Done), `DEPLOYMENT_STATUS.md:365-374` (log locations).

Goal: give any engineer a 10-minute path to prove Phase 1 is still green before or after a deploy.

## 1. Test Matrix (run in this order)
1. **Unit + contract suite** (full gate from MVP line 33):  
   ```bash
   pytest -q tests
   ```
2. **Focused contract verification** (quick re-run when only analyzer payloads changed):  
   ```bash
   pytest tests/test_analyze_contract.py -q
   ```
3. **Smoke suite** (`tests/test_smoke.py`) to verify `/health`, `/version`, `/api/analyze` happy-path without Redis/Postgres:  
   ```bash
   pytest tests/test_smoke.py -q
   ```
4. **Optional targeted files**: `pytest tests/test_patterns.py -q` when touching detectors, `pytest tests/test_indicators.py -q` when messing with ATR/MA math.

## 2. Interpreting Failures
- **Schema drift** (most common): `tests/test_analyze_contract.py` asserts all top-level keys (`ticker`, `timeframe`, `ohlcv`, `indicators`, `patterns`, `plan`, `relative_strength`, `intel`, `universe`, `chart_url`). If one disappears, document the intentional change in `CHANGELOG.md` and update both the PRD and contract tests before merging.
- **Chart URL missing**: signals Chart-IMG fallback. Cross-check `docs/RUNBOOK_ChartIMG.md` before retrying; MVP line 15 requires `chart_url` exist even if value is `null`.
- **Performance regressions**: If tests stall, profile the analyzer path locally (`pytest -vv tests/test_smoke.py::test_analyze_endpoint_smoke --durations=10`) and compare to the `<2s` SLA spelled out in `docs/Legend_AI_MVP.md:29` and `docs/Legend_AI_Roadmap.md:9`.

## 3. CI “Green” Definition
CI is considered green only when all bullets below pass:
- `pytest -q tests` exits 0 with no `xfail` surprises.
- Contract + smoke suites run in CI (GitHub Actions / Railway) without `|| true` or retry hacks.
- Logs captured during the run include Chart-IMG POST telemetry with `symbol`, `interval`, `status`, and `duration` fields (explicitly required by `docs/Legend_AI_MVP.md:20`).
- Exit criteria from `docs/Legend_AI_Roadmap.md:9` remain true: analyzer responses <2s, `BUILD <sha>` visible, seeded universe tables intact, `test_analyze_contract.py` + smoke suite green.

## 4. Log Collection & Artifacts
- **Local**: `tail -f logs/*.log` (per `DEPLOYMENT_STATUS.md:367-374`) while tests run to capture retries/backoff context.
- **Railway**: `railway logs --service legend-ai-api --follow` for hosted builds. Save the relevant lines in the PR description when telemetry is involved.
- **Pytest logs**: rerun with `pytest -q tests --log-cli-level=INFO` if you need structured messages in CI artifacts.

## 5. When to Block a Deploy
Block and investigate immediately if:
- Any analyzer contract test fails twice in a row (indicator, pattern, or plan key removal can break downstream clients).
- `/health` or `/version` fails (UI caches `BUILD <sha>` per `docs/Legend_AI_Roadmap.md:19`; stale values mean the deploy did not pick up the latest code).
- Chart-IMG logs lose `status` or `duration` fields, violating the MVP telemetry spec.

Always capture the failing command output, link it in the sprint tracker row, and document remediation steps in `CHANGELOG.md` under Fixed/Telemetry once resolved.
