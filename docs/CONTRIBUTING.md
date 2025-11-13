## Contributing

## Branch & PR Flow
- Feature PRs: smallest viable change, DIFF ONLY.
- Commit style: chore/docs/feat/fix/refactor/test
- PR template: What, Why, Risks, Rollback

## Testing Policy
- Unit: indicators, patterns, planner logic (core functions stay pure).
- Contract: `/api/analyze` keys/types — fail if shape changes.

## AI Guardrails
- Stay within MVP_SPEC + ARCHITECTURE_GUIDE.
- No secrets in repo or frontend; use Railway env.
- No infra/redis/cache panels in UI.
- Ask one yes/no question when ambiguous; then pause.
- Don’t alter public JSON schemas without updating tests.

## Code Quality
- Python: Ruff/Black; JS: Prettier/ESLint (if present).
- Keep core pure and services side‑effectful; isolate I/O.

## Docs & Release Hygiene
1. **Update the changelog**: add a new `v{{build_sha}} – YYYY-MM-DD` section in `CHANGELOG.md` with Added/Changed/Fixed/Performance/Telemetry notes plus links to the matching roadmap rows.
2. **Refresh runbooks**: if a release touched Chart-IMG, CI, or deployment flow, add the new steps + log locations to `docs/RUNBOOK_ChartIMG.md`, `docs/RUNBOOK_CI_Smoke.md`, and/or `docs/RUNBOOK_Deploy.md` before merging.
3. **Sync checklists**: tick/untick `docs/Launch_Readiness_Checklist.md` and `docs/Phase_1_Exit.md` so QA can see what’s still open for Phase 1.
4. **Archive sprint context**: append rows to `docs/Release_Templates/Sprint_Tracker.csv` (Task, Owner, Status, PR Link, Notes) so every shipped change maps back to a checklist item.
