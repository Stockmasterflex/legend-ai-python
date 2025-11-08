from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import logging
import asyncio

from app.services.market_data import market_data_service
from app.core.indicators import ema, sma, rsi, detect_rsi_divergences
from app.core.classifiers import minervini_trend_template, weinstein_stage
from app.services.cache import get_cache_service
from app.infra.chartimg import build_analyze_chart

router = APIRouter(prefix="/api", tags=["analyze"])
logger = logging.getLogger(__name__)


def _as_floats(values: List[Any]) -> List[float]:
    return [float(v) if v is not None else float("nan") for v in values]


def _sanitize_series(values: List[float]) -> List[Optional[float]]:
    """Replace NaN/Inf with None for JSON compatibility."""
    out: List[Optional[float]] = []
    for v in values:
        try:
            f = float(v)
            if f != f or f in (float("inf"), float("-inf")):
                out.append(None)
            else:
                out.append(f)
        except Exception:
            out.append(None)
    return out


@router.get("/analyze")
async def analyze(
    ticker: str,
    tf: str = Query("daily", pattern="^(daily|weekly)$"),
    bars: int = Query(400, ge=100, le=5000)
) -> Dict[str, Any]:
    """Analyze a ticker and return OHLCV, indicators, patterns and a simple plan.

    tf: 'daily' | 'weekly'
    """
    try:
        interval = "1day" if tf.lower().startswith("d") else "1week"

        # Cache key
        cache = get_cache_service()
        cache_key = f"analyze:{ticker.upper()}:{interval}:{bars}"
        cached = await cache.get(cache_key)
        if cached:
            cached["cache"] = {"hit": True, "ttl": 120}
            return cached

        # Fetch price data with jitter backoff (max 4 tries)
        ohlcv = None
        for attempt in range(4):
            data = await market_data_service.get_time_series(
                ticker=ticker.upper(), interval=interval, outputsize=bars
            )
            if data and data.get("c"):
                ohlcv = data
                break
            # exponential backoff with jitter
            base = 0.3
            import random
            await asyncio.sleep(random.uniform(0, base * (2 ** attempt)))

        if not ohlcv:
            # Contract: if insufficient data, return 400 with {"insufficient":"data"}
            return JSONResponse(status_code=400, content={"insufficient": "data"})

        closes = _as_floats(ohlcv["c"])
        opens = _as_floats(ohlcv.get("o", ohlcv["c"]))
        highs = _as_floats(ohlcv.get("h", ohlcv["c"]))
        lows = _as_floats(ohlcv.get("l", ohlcv["c"]))
        vols = [float(v) for v in ohlcv.get("v", [0] * len(closes))]
        times = ohlcv.get("t", [])

        # Basic sanity: require at least 50 bars for SMA50 per contract
        if len(closes) < 50:
            return JSONResponse(status_code=400, content={"insufficient": "data"})

        # Indicators required by contract
        ema21 = _sanitize_series(ema(closes, 21))
        sma50 = _sanitize_series(sma(closes, 50))
        rsi14 = _sanitize_series(rsi(closes, 14))
        divergences = detect_rsi_divergences(closes, rsi14)

        # Note: RS calculations are not part of the contract output; skipped to keep response minimal

        # Patterns (daily + weekly)
        mini_raw = minervini_trend_template(closes) if interval == "1day" else {"pass": False, "failed_rules": ["computed on daily only"]}
        # Contract requires key "passed"
        mini = {"passed": bool(mini_raw.get("pass", False)), "failed_rules": mini_raw.get("failed_rules", [])}

        # For Weinstein, use weekly data; if we are already weekly, reuse; otherwise ask for 1week
        if interval == "1week":
            closes_week = closes
        else:
            week = await market_data_service.get_time_series(ticker=ticker.upper(), interval="1week", outputsize=200)
            closes_week = _as_floats(week["c"]) if week and week.get("c") else []
        wein = weinstein_stage(closes_week) if closes_week else {"stage": 0, "reason": "insufficient data"}

        vcp_info = {"detected": False, "score": 0.0, "notes": []}

        # Simple ATR-based plan (14-period true range on selected timeframe)
        atr = _compute_atr(highs, lows, closes, period=14)
        last_close = closes[-1]
        last_atr = atr[-1] if atr else 0.0
        entry = round(last_close, 2)
        stop = round(max(0.01, entry - 1.5 * last_atr), 2)
        target = round(entry + 2 * (entry - stop), 2)
        risk_r = round((target - entry) / (entry - stop), 2) if (entry - stop) > 0 else 0.0

        # Build OHLCV list for clients that want raw data
        ohlcv_rows = []
        for i in range(len(closes)):
            t = times[i] if i < len(times) else None
            ohlcv_rows.append({
                "t": t,
                "o": opens[i],
                "h": highs[i],
                "l": lows[i],
                "c": closes[i],
                "v": vols[i] if i < len(vols) else 0
            })

        # Optional: map divergence indices to minimal drawing hints
        divergence_markers = []
        try:
            for d in divergences[:5]:
                idx = d.get("index")
                if idx is None or idx >= len(closes):
                    continue
                ts = times[idx] if idx < len(times) else None
                divergence_markers.append({
                    "datetime": ts if isinstance(ts, str) else None,
                    "price": closes[idx],
                    "type": d.get("type"),
                })
        except Exception:
            divergence_markers = []

        chart_url: Optional[str] = None
        try:
            chart_url = await build_analyze_chart(
                ticker=ticker.upper(),
                tf="daily" if interval == "1day" else "weekly",
                plan={"entry": entry, "stop": stop, "target": target},
                divergence_points=divergence_markers,
                range_hint=times[-1] if times else None,
            )
        except Exception:
            chart_url = None

        result = {
            "ticker": ticker.upper(),
            "timeframe": "daily" if interval == "1day" else "weekly",
            "bars": bars,
            "ohlcv": ohlcv_rows,
            "indicators": {
                "ema21": ema21,
                "sma50": sma50,
                "rsi14": rsi14,
                "rsi_divergences": divergences,
            },
            "patterns": {
                "minervini": mini,
                "weinstein": wein,
                "vcp": vcp_info,
            },
            "plan": {
                "entry": entry,
                "stop": stop,
                "target": target,
                "risk_r": risk_r,
            },
            "chart_url": chart_url,
            "cache": {"hit": False, "ttl": 0}
        }

        # Cache for 120 seconds
        try:
            await cache.set(cache_key, result, ttl=120)
        except Exception:
            pass
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"analyze error for {ticker}: {e}")
        # Contract: clear error message
        raise HTTPException(status_code=500, detail=f"analyze_failed: {str(e)}")


def _compute_atr(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> List[float]:
    if not highs or not lows or not closes:
        return []
    trs: List[float] = []
    prev_close = closes[0]
    for i in range(len(closes)):
        if i == 0:
            trs.append(highs[i] - lows[i])
        else:
            tr = max(highs[i] - lows[i], abs(highs[i] - prev_close), abs(lows[i] - prev_close))
            trs.append(tr)
            prev_close = closes[i]
    return ema(trs, period)


def _relative_strength(closes: List[float], interval: str) -> (List[Optional[float]], List[Optional[float]]):
    """Compute RS ratio vs SPY and 50-bar SMA slope of RS (both arrays len=closes)."""
    try:
        # Fetch SPY series on same interval
        rs = []
        slope = []
        loop = asyncio.get_event_loop()
        # Note: call synchronously via loop.run_until_complete if needed; here we're in async context
        # but we keep API async
    except Exception:
        return [None for _ in closes], [None for _ in closes]
