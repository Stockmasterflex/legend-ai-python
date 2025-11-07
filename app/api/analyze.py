from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import logging
import asyncio

from app.services.market_data import market_data_service
from app.core.indicators import ema, sma, rsi, detect_rsi_divergences
from app.core.classifiers import minervini_trend_template, weinstein_stage

router = APIRouter(prefix="/api", tags=["analyze"])
logger = logging.getLogger(__name__)


def _as_floats(values: List[Any]) -> List[float]:
    return [float(v) if v is not None else float("nan") for v in values]


@router.get("/analyze")
async def analyze(ticker: str, tf: str = "daily") -> Dict[str, Any]:
    """Analyze a ticker and return OHLCV, indicators, patterns and a simple plan.

    tf: 'daily' | 'weekly'
    """
    try:
        interval = "1day" if tf.lower().startswith("d") else "1week"

        # Fetch price data with a simple retry loop (backoff up to ~4s)
        ohlcv = None
        for attempt in range(4):
            data = await market_data_service.get_time_series(ticker=ticker.upper(), interval=interval, outputsize=500)
            if data and data.get("c"):
                ohlcv = data
                break
            await asyncio.sleep(0.5 * (2 ** attempt))

        if not ohlcv:
            raise HTTPException(status_code=404, detail="No price data available")

        closes = _as_floats(ohlcv["c"])
        opens = _as_floats(ohlcv.get("o", ohlcv["c"]))
        highs = _as_floats(ohlcv.get("h", ohlcv["c"]))
        lows = _as_floats(ohlcv.get("l", ohlcv["c"]))
        vols = [float(v) for v in ohlcv.get("v", [0] * len(closes))]
        times = ohlcv.get("t", [])

        # Indicators (shown on chart)
        ema21 = ema(closes, 21)
        sma50 = sma(closes, 50)
        rsi14 = rsi(closes, 14)
        divergences = detect_rsi_divergences(closes, rsi14)

        # Patterns (daily + weekly)
        mini = minervini_trend_template(closes) if interval == "1day" else {"pass": False, "failed_rules": ["computed on daily only"]}

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

        return {
            "ticker": ticker.upper(),
            "timeframe": "daily" if interval == "1day" else "weekly",
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
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"analyze error for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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

