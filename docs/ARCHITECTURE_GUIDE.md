# Architecture Guide

## Stack
- Backend: FastAPI (Python 3.11+), httpx, pydantic; async I/O with jitter backoff; Redis cache via `redis.asyncio`.
- Frontend: server‑rendered templates (`templates/`) + static JS/CSS (`static/`), dark theme.
- Deploy: Railway (auto from GitHub) using `railway.toml`.
- Data: TwelveData primary; optional Finnhub and Alpha Vantage; Yahoo fallback; caching via Redis.
- Secrets: Railway variables only; never exposed to the frontend.

## Directory Layout
app/
  api/ (routers for analyze, universe scan, charts, watchlist, alerts, etc.)
  core/ (indicators, classifiers, pattern detectors)
  services/ (market_data, cache, database, universe, charting)
  main.py (FastAPI app wiring, CORS, router includes)
static/
templates/
tests/
docs/

## Responsibilities
- api/: request/response handling and contract enforcement; no provider logic.
- core/: pure functions (calculations/detections) — easy to test and reuse.
- services/: side effects (HTTP calls, caching, DB, retries/backoff, file I/O).
- templates/static: minimal UI hydration; no secrets or heavy logic.

## API Contracts (don’t break without updating tests)
- `/api/analyze` schema per MVP: ohlcv[], indicators { ema21, sma50, rsi14, divs[] }, patterns { minervini, weinstein, vcp }, plan { entry, stop, target, risk_r }.
- `/api/scan` (stable alias of current `/api/universe/scan`).
- `/api/top-setups` (near‑term), `/api/watchlist` CRUD.

## Reliability
- Exponential backoff with jitter (max ~4 tries) and strict timeouts on external calls.
- Return `400` with `{ "insufficient": "data" }` when inputs aren’t adequate; avoid 500s for expected conditions.
- Use Redis cache for price/pattern data to control provider usage.
- No client‑side secrets; all third‑party requests originate server‑side.

## Frontend Rules
- Don’t mount charts until data is returned.
- Destroy chart on tab change; re‑mount on Analyze action.
- Indicators: 21EMA, 50SMA, Volume, RSI(14) with divergence markers.

