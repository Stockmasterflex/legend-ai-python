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

