from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import logging
import asyncio
import random
import time
from contextlib import suppress

from app.services.market_data import market_data_service
from app.core.indicators import ema, sma, rsi, detect_rsi_divergences
from app.core.classifiers import minervini_trend_template, weinstein_stage
from app.core.metrics import (
    compute_atr,
    last_valid,
    ma_distances,
    relative_strength_metrics,
    sanitize_series,
)
from app.services.cache import get_cache_service
from app.infra.chartimg import build_analyze_chart
from app.services.universe_store import universe_store
from app.services.multitimeframe import MultiTimeframeConfirmation
from app.telemetry.metrics import (
    ANALYZE_REQUEST_DURATION_SECONDS,
    CACHE_HITS_TOTAL,
    CACHE_MISSES_TOTAL,
    CHARTIMG_POST_STATUS_TOTAL,
    ANALYZE_ERRORS_TOTAL,
)

router = APIRouter(prefix="/api", tags=["analyze"])
logger = logging.getLogger(__name__)


def _as_floats(values: List[Any]) -> List[float]:
    return [float(v) if v is not None else float("nan") for v in values]


def _update_request_state(
    request: Request,
    ticker: str,
    interval: str,
    status: str,
    cache_hit: Optional[bool] = None,
) -> None:
    state = getattr(request.state, "telemetry", {}) or {}
    state.update(
        {
            "event": "analyze",
            "symbol": ticker,
            "interval": interval,
            "status": status,
        }
    )
    if cache_hit is not None:
        state["cache_hit"] = cache_hit
    request.state.telemetry = state


@router.get("/analyze")
async def analyze(
    request: Request,
    ticker: str,
    tf: str = Query("daily", pattern="^(daily|weekly)$"),
    bars: int = Query(400, ge=100, le=5000),
    multi_timeframe: bool = Query(False, description="Include multi-timeframe analysis"),
) -> Dict[str, Any]:
    """Analyze a ticker and return indicators, patterns, RS intel, and an ATR plan."""
    ticker_clean = ticker.upper().strip()
    if not ticker_clean:
        raise HTTPException(status_code=400, detail="ticker_required")

    interval = "1day" if tf.lower().startswith("d") else "1week"
    timeframe_label = "daily" if interval == "1day" else "weekly"
    cache = get_cache_service()
    cache_key = f"analyze:{ticker_clean}:{interval}:{bars}"
    started = time.perf_counter()

    def _observe_duration() -> float:
        duration_sec = max(time.perf_counter() - started, 0.0)
        ANALYZE_REQUEST_DURATION_SECONDS.labels(interval=interval).observe(duration_sec)
        return duration_sec

    _update_request_state(request, ticker_clean, interval, "received")

    cached = await cache.get(cache_key)
    if cached:
        response = {**cached, "cache": {"hit": True, "ttl": cached.get("cache", {}).get("ttl", 0)}}
        CACHE_HITS_TOTAL.labels(name="analyze").inc()
        _observe_duration()
        _update_request_state(request, ticker_clean, interval, "ok", cache_hit=True)
        logger.info(
            "analyze_duration ticker=%s interval=%s duration_ms=%.1f cache_hit=True",
            ticker_clean,
            interval,
            (time.perf_counter() - started) * 1000,
        )
        return response
    CACHE_MISSES_TOTAL.labels(name="analyze").inc()

    price_task = asyncio.create_task(
        _fetch_series_with_backoff(ticker_clean, interval, bars)
    )
    spy_task = asyncio.create_task(
        _fetch_series_with_backoff("SPY", interval, min(600, max(200, bars)))
    )
    weekly_task = None
    if interval == "1day":
        weekly_task = asyncio.create_task(
            _fetch_series_with_backoff(ticker_clean, "1week", max(260, bars // 5))
        )

    try:
        ohlcv = await price_task
        if not _has_prices(ohlcv):
            logger.warning("analyze_insufficient_data ticker=%s interval=%s", ticker_clean, interval)
            spy_task.cancel()
            with suppress(asyncio.CancelledError):
                await spy_task
            if weekly_task:
                weekly_task.cancel()
                with suppress(asyncio.CancelledError):
                    await weekly_task
            _observe_duration()
            _update_request_state(request, ticker_clean, interval, "insufficient", cache_hit=False)
            logger.info(
                "analyze_duration ticker=%s interval=%s duration_ms=%.1f cache_hit=False status=insufficient",
                ticker_clean,
                interval,
                (time.perf_counter() - started) * 1000,
            )
            # Use 422 to signal the request was well-formed but could not be
            # processed due to missing upstream data. This keeps the endpoint
            # contract consistent for clients and avoids false 400s when
            # external data providers are unavailable during tests.
            return JSONResponse(status_code=422, content={"insufficient": "data"})

        spy_data = await spy_task if spy_task else None
        weekly_data = ohlcv if interval == "1week" else (await weekly_task if weekly_task else None)

        closes = _as_floats(ohlcv["c"])
        opens = _as_floats(ohlcv.get("o", ohlcv["c"]))
        highs = _as_floats(ohlcv.get("h", ohlcv["c"]))
        lows = _as_floats(ohlcv.get("l", ohlcv["c"]))
        vols = [float(v) for v in ohlcv.get("v", [0] * len(closes))]
        times = ohlcv.get("t", [])

        if len(closes) < 50:
            logger.info(
                "analyze_duration ticker=%s interval=%s duration_ms=%.1f cache_hit=False status=insufficient",
                ticker_clean,
                interval,
                (time.perf_counter() - started) * 1000,
            )
            _observe_duration()
            _update_request_state(request, ticker_clean, interval, "insufficient", cache_hit=False)
            return JSONResponse(status_code=400, content={"insufficient": "data"})

        ema21_raw = ema(closes, 21)
        ema21 = sanitize_series(ema21_raw)
        sma50_raw = sma(closes, 50)
        sma50 = sanitize_series(sma50_raw)
        rsi_raw = rsi(closes, 14)
        rsi14 = sanitize_series(rsi_raw)
        divergences = detect_rsi_divergences(closes, rsi_raw)

        mini_raw = (
            minervini_trend_template(closes)
            if interval == "1day"
            else {"pass": False, "failed_rules": ["computed on daily only"]}
        )
        mini = {"passed": bool(mini_raw.get("pass", False)), "failed_rules": mini_raw.get("failed_rules", [])}

        weekly_closes = closes if interval == "1week" else _as_floats(weekly_data["c"]) if _has_prices(weekly_data) else []
        wein = weinstein_stage(weekly_closes) if weekly_closes else {"stage": 0, "reason": "insufficient data"}

        vcp_info = {"detected": False, "score": 0.0, "notes": []}

        atr = compute_atr(highs, lows, closes, period=14)
        last_close = closes[-1]
        last_atr = atr[-1] if atr else 0.0
        entry = round(last_close, 2)
        stop = round(max(0.01, entry - 1.5 * last_atr), 2)
        target = round(entry + 2 * (entry - stop), 2)
        risk_r = round((target - entry) / (entry - stop), 2) if (entry - stop) > 0 else 0.0
        atr_pct = round((last_atr / entry) * 100, 2) if entry else None

        ohlcv_rows = []
        for i in range(len(closes)):
            t = times[i] if i < len(times) else None
            ohlcv_rows.append(
                {
                    "t": t,
                    "o": opens[i],
                    "h": highs[i],
                    "l": lows[i],
                    "c": closes[i],
                    "v": vols[i] if i < len(vols) else 0,
                }
            )

        divergence_markers = []
        for d in divergences[:5]:
            idx = d.get("index")
            if idx is None or idx >= len(closes):
                continue
            ts = times[idx] if idx < len(times) else None
            divergence_markers.append(
                {
                    "datetime": ts if isinstance(ts, str) else None,
                    "price": closes[idx],
                    "type": d.get("type"),
                }
            )

        rs_metrics = relative_strength_metrics(closes, spy_data.get("c") if _has_prices(spy_data) else [])
        ma_spread = ma_distances(
            last_close,
            last_valid(ema21_raw),
            last_valid(sma50_raw),
        )

        chart_url: Optional[str]
        try:
            chart_url = await build_analyze_chart(
                ticker=ticker_clean,
                tf=timeframe_label,
                plan={"entry": entry, "stop": stop, "target": target},
                divergence_points=divergence_markers,
                range_hint=times[-1] if times else None,
            )
            CHARTIMG_POST_STATUS_TOTAL.labels(status="success").inc()
        except Exception as e:
            logger.error(f"Chart generation failed for {ticker_clean}: {e}", exc_info=True)
            CHARTIMG_POST_STATUS_TOTAL.labels(status="error").inc()
            chart_url = None

        universe_meta = await universe_store.get_metadata(ticker_clean)

        result = {
            "ticker": ticker_clean,
            "timeframe": timeframe_label,
            "bars": len(ohlcv_rows),
            "universe": universe_meta,
            "ohlcv": ohlcv_rows,
            "indicators": {
                "ema21": ema21,
                "sma50": sma50,
                "rsi14": rsi14,
                "rsi_divergences": divergences,
                "rsi_markers": divergence_markers,
                "ma_distances": ma_spread,
            },
            "patterns": {
                "minervini": mini,
                "weinstein": wein,
                "vcp": vcp_info,
            },
            "relative_strength": rs_metrics,
            "plan": {
                "entry": entry,
                "stop": stop,
                "target": target,
                "risk_r": risk_r,
                "atr14": round(last_atr, 2),
                "atr_percent": atr_pct,
            },
            "intel": {
                "rule_failures": mini["failed_rules"],
                "rs_rank": rs_metrics.get("rank"),
                "ma_distances": ma_spread,
                "r_multiple": risk_r,
            },
            "chart_url": chart_url,
            "sources": {
                "price": ohlcv.get("source"),
                "spy": spy_data.get("source") if spy_data else None,
            },
            "cache": {"hit": False, "ttl": 3600},
        }
        
        # Add multi-timeframe analysis if requested
        if multi_timeframe:
            try:
                mtf_service = MultiTimeframeConfirmation()
                mtf_result = await mtf_service.analyze_multi_timeframe(ticker_clean)
                result["multi_timeframe"] = {
                    "overall_confluence": round(mtf_result.overall_confluence, 2),
                    "signal_quality": mtf_result.signal_quality,
                    "strong_signal": mtf_result.strong_signal,
                    "timeframes": {
                        "weekly": {
                            "pattern": mtf_result.weekly_1w.pattern_type,
                            "confidence": round(mtf_result.weekly_1w.confidence, 2),
                            "detected": mtf_result.weekly_1w.pattern_detected
                        },
                        "daily": {
                            "pattern": mtf_result.daily_1d.pattern_type,
                            "confidence": round(mtf_result.daily_1d.confidence, 2),
                            "detected": mtf_result.daily_1d.pattern_detected
                        },
                        "4h": {
                            "pattern": mtf_result.four_hour_4h.pattern_type,
                            "confidence": round(mtf_result.four_hour_4h.confidence, 2),
                            "detected": mtf_result.four_hour_4h.pattern_detected
                        },
                        "1h": {
                            "pattern": mtf_result.one_hour_1h.pattern_type,
                            "confidence": round(mtf_result.one_hour_1h.confidence, 2),
                            "detected": mtf_result.one_hour_1h.pattern_detected
                        }
                    },
                    "alignment": mtf_result.alignment_details,
                    "recommendations": mtf_result.recommendations
                }
                logger.info(f"✅ Multi-timeframe analysis added for {ticker_clean}: {mtf_result.signal_quality}")
            except Exception as e:
                logger.warning(f"Multi-timeframe analysis failed for {ticker_clean}: {e}")
                result["multi_timeframe"] = None

        try:
            await cache.set(cache_key, result, ttl=3600)
        except Exception:
            logger.debug("analyze cache set failed for %s", ticker_clean)

        _observe_duration()
        _update_request_state(request, ticker_clean, interval, "ok", cache_hit=False)
        logger.info(
            "analyze_duration ticker=%s interval=%s duration_ms=%.1f cache_hit=False",
            ticker_clean,
            interval,
            (time.perf_counter() - started) * 1000,
        )
        return result
    except HTTPException:
        ANALYZE_ERRORS_TOTAL.inc()
        _observe_duration()
        _update_request_state(request, ticker_clean, interval, "http_error", cache_hit=False)
        logger.info(
            "analyze_duration ticker=%s interval=%s duration_ms=%.1f cache_hit=False status=error",
            ticker_clean,
            interval,
            (time.perf_counter() - started) * 1000,
        )
        raise
    except Exception as exc:
        ANALYZE_ERRORS_TOTAL.inc()
        logger.exception("analyze error for %s: %s", ticker_clean, exc)
        _observe_duration()
        _update_request_state(request, ticker_clean, interval, "exception", cache_hit=False)
        logger.info(
            "analyze_duration ticker=%s interval=%s duration_ms=%.1f cache_hit=False status=exception",
            ticker_clean,
            interval,
            (time.perf_counter() - started) * 1000,
        )
        raise HTTPException(status_code=500, detail=f"analyze_failed: {str(exc)}")


def _has_prices(data: Optional[Dict[str, Any]]) -> bool:
    return bool(data and data.get("c"))


async def _fetch_series_with_backoff(ticker: str, interval: str, outputsize: int) -> Dict[str, Any]:
    for attempt in range(4):
        data = await market_data_service.get_time_series(
            ticker=ticker,
            interval=interval,
            outputsize=outputsize,
        )
        if _has_prices(data):
            return data
        await asyncio.sleep(random.uniform(0.1, 0.3 * (2 ** attempt)))
    return {}
