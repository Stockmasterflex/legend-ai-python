# Legend AI — MVP Spec

## 1) Mission
Legend AI is for active swing traders who need to quickly scan for high‑quality technical setups, analyze individual tickers, and build clear trade plans fast. The experience is focused and professional: dark, clean UI with charts first, no clutter, and actionable right‑panel intel.

## 2) In‑Scope (MVP)
- Analyze: input ticker/timeframe → chart (candles + 21EMA, 50SMA, Volume, RSI w/ divergences), right‑panel intel (Minervini pass/fail + failed rules, Weinstein stage + reason, VCP flag/score, entry/stop/target + R).
- Pattern Scanner: batch scan with filters, ranked cards → open Analyze.
- Top Setups: daily top 10 with chart + plan.
- Market Internals: TradingView widgets (ticker strip, heatmaps, SPY/QQQ/IWM/VIX + sectors).
- Watchlist: simple CRUD, persisted.

## 3) Out of Scope (MVP)
- Telegram/alerts, broker execution, auth/multi‑tenant, advanced ML models beyond VCP.

## 4) API Contracts (stable)
- GET `/health` → `{ "ok": true }` or healthy summary
- GET `/api/analyze?ticker=TSLA&tf=daily` → JSON with `{ ohlcv[], indicators{ema21,sma50,rsi14,divs[]}, patterns{minervini,weinstein,vcp}, plan{entry,stop,target,risk_r} }`
- POST `/api/scan` → ranked setups (alias of current `/api/universe/scan`)
- GET `/api/top-setups?limit=10`
- CRUD `/api/watchlist`

Notes:
- Current implementation provides `/api/universe/scan` and `/api/universe/scan/quick`; `/api/scan` will be a stable alias maintained by the API layer.

## 5) Success Criteria
- `/api/analyze` returns in < 2s for common tickers; UI mounts chart only after data.
- Dark theme, uncluttered; no infra metrics in UI; tests pass on PR.

## 6) Risks / Assumptions
- Data provider limits; chart rendering costs; keep keys server‑side; exponential backoff on HTTP with jitter; cache safely; never expose secrets client‑side.

