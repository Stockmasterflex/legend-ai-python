import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import httpx

from app.config import get_settings
from app.infra.symbols import to_chartimg_symbol
from app.services.cache import get_cache_service

logger = logging.getLogger(__name__)


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def build_analyze_chart(
    ticker: str,
    tf: str,
    plan: Dict[str, Any],
    divergence_points: Optional[List[Dict[str, Any]]] = None,
    range_hint: Optional[str] = None,
) -> Optional[str]:
    """Render a TradingView advanced chart via Chart-IMG and return the image URL.

    - Never exposes API key to clients; server-side only.
    - Uses exponential backoff (max 4 tries) on transient errors.
    - tf: "daily" | "weekly"
    - divergence_points: optional list of {"datetime": ISO8601, "price": float} or
      {"index": int, "datetime": ..., "price": ...}. Only a few markers should be sent.
    """
    settings = get_settings()
    api_key = settings.chart_img_api_key
    if not api_key or api_key.lower().startswith("dev"):
        # Skip in dev/test without a real key
        return None

    interval = "1D" if tf.lower().startswith("d") else "1W"
    # Try common US exchanges then fallback to simple uppercase ticker
    t = (ticker or "").upper()
    symbol_candidates: List[str] = [
        f"NASDAQ:{t}",
        f"NYSE:{t}",
        to_chartimg_symbol(ticker),
    ]

    drawings: List[Dict[str, Any]] = []
    try:
        entry = float(plan.get("entry"))
        stop = float(plan.get("stop"))
        target = float(plan.get("target"))
        start_dt = range_hint or _iso_now()
        drawings.append(
            {
                "name": "Long Position",
                "input": {
                    "startDatetime": start_dt,
                    "entryPrice": entry,
                    "stopPrice": stop,
                    "targetPrice": target,
                },
            }
        )
    except Exception as e:
        logger.debug(f"Chart drawing plan skipped: {e}")

    # Optional: annotate a few divergence markers
    if divergence_points:
        for d in divergence_points[:5]:  # limit markers
            dt = d.get("datetime") or _iso_now()
            price = d.get("price")
            if price is None:
                continue
            drawings.append(
                {
                    "name": "Arrow Marker",
                    "input": {"datetime": dt, "price": float(price)},
                }
            )

    # Chart-IMG Pro has a limit of 5 parameters total (studies + drawings combined)
    # Prioritize: Volume, EMA 21, SMA 50, then Long Position drawing if available
    studies = [
        {"name": "Volume", "forceOverlay": True},
        {
            "name": "Moving Average Exponential",
            "input": {"length": 21, "source": "close"},
        },
        {"name": "Moving Average", "input": {"length": 50, "source": "close"}},
    ]

    # Calculate remaining parameter budget (max 5 total, 3 studies used so far)
    params_used = len(studies) + len(drawings)
    if params_used > 5:
        # Prioritize Long Position over divergence markers
        # Keep only Long Position if we have it, drop divergence markers
        drawings = [d for d in drawings if d.get("name") == "Long Position"][:1]
        logger.warning(
            f"Chart-IMG parameter limit: reduced from {params_used} to {len(studies) + len(drawings)} params"
        )

    base_payload: Dict[str, Any] = {
        "theme": "dark",
        "interval": interval,
        "studies": studies,
        "drawings": drawings,
    }

    # Use /storage endpoint to get a URL (not raw PNG)
    url = "https://api.chart-img.com/v2/tradingview/advanced-chart/storage"
    headers = {"x-api-key": api_key}

    # Cache hit short-circuits expensive renders
    cache = get_cache_service()
    try:
        cached = await cache.get_chart(t, interval)
        if cached:
            logger.info("chartimg_cache_hit symbol=%s interval=%s", t, interval)
            return cached
    except Exception as exc:
        logger.debug("chartimg cache get failed: %s", exc)

    # Get smart TTL from config (respects market hours)
    settings = get_settings()

    # Backoff with jitter up to 4 tries
    last_err: Optional[Exception] = None
    for attempt in range(4):
        try:
            timeout = httpx.Timeout(8.0)
            async with httpx.AsyncClient(timeout=timeout) as client:
                for sym in symbol_candidates:
                    payload: Dict[str, Any] = {**base_payload, "symbol": sym}
                    start = time.perf_counter()
                    logger.info(
                        "chartimg_attempt_start symbol=%s interval=%s attempt=%s",
                        sym,
                        interval,
                        attempt + 1,
                    )
                    resp = await client.post(url, json=payload, headers=headers)
                    duration_ms = (time.perf_counter() - start) * 1000
                    logger.info(
                        "chartimg_attempt_complete symbol=%s interval=%s status=%s duration_ms=%.1f attempt=%s",
                        sym,
                        interval,
                        resp.status_code,
                        duration_ms,
                        attempt + 1,
                    )
                    if resp.status_code in (200, 201):
                        try:
                            data = resp.json()
                            # Chart-IMG returns one of these keys depending on endpoint
                            chart_url = (
                                data.get("url")
                                or data.get("imageUrl")
                                or data.get("image_url")
                            )
                            if chart_url:
                                try:
                                    # Use smart caching with config TTL (market hours aware)
                                    await cache.set_chart(t, interval, chart_url)
                                except Exception as exc:
                                    logger.debug("chartimg cache set failed: %s", exc)
                            else:
                                logger.warning(
                                    f"Chart-IMG 200 OK but no url in response for {sym}: {data}"
                                )
                            return chart_url
                        except Exception as e:
                            logger.error(
                                f"Chart-IMG response parsing failed for {sym}: {e}",
                                exc_info=True,
                            )
                            return None
                    # Non-200
                    body_head = (resp.text or "")[:150]
                    if resp.status_code in (429, 500, 502, 503, 504):
                        logger.info(
                            "chartimg_retryable status=%s body=%s",
                            resp.status_code,
                            body_head,
                        )
                        # try next candidate this attempt; if all fail we'll backoff
                        continue
                    else:
                        logger.info(
                            "chartimg_non200 status=%s body=%s",
                            resp.status_code,
                            body_head,
                        )
                        # Try next candidate; if none succeed, return None (no point backoff on 4xx other than 429)
                        continue
                # If we exhausted candidates without success, raise to trigger backoff
                raise RuntimeError("all_symbol_candidates_failed")
        except Exception as e:
            last_err = e
            base = 0.4
            import random

            await asyncio.sleep(random.uniform(0, base * (2**attempt)))
    logger.error(f"Chart-IMG render failed after retries: {last_err}")
    return None
