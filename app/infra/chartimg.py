import os
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import asyncio
import httpx

from app.config import get_settings
from app.infra.symbols import to_chartimg_symbol

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
    api_key = settings.chartimg_api_key
    if not api_key or api_key.lower().startswith("dev"):
        # Skip in dev/test without a real key
        return None

    interval = "1D" if tf.lower().startswith("d") else "1W"
    # Try common US exchanges then fallback to simple uppercase ticker
    t = (ticker or "").upper()
    symbol_candidates: List[str] = [f"NASDAQ:{t}", f"NYSE:{t}", to_chartimg_symbol(ticker)]

    drawings: List[Dict[str, Any]] = []
    try:
        entry = float(plan.get("entry"))
        stop = float(plan.get("stop"))
        target = float(plan.get("target"))
        start_dt = range_hint or _iso_now()
        drawings.append({
            "name": "Long Position",
            "input": {
                "startDatetime": start_dt,
                "entryPrice": entry,
                "stopPrice": stop,
                "targetPrice": target,
            },
        })
    except Exception as e:
        logger.debug(f"Chart drawing plan skipped: {e}")

    # Optional: annotate a few divergence markers
    if divergence_points:
        for d in divergence_points[:5]:  # limit markers
            dt = d.get("datetime") or _iso_now()
            price = d.get("price")
            if price is None:
                continue
            drawings.append({
                "name": "Arrow Marker",
                "input": {"datetime": dt, "price": float(price)},
            })

    base_payload: Dict[str, Any] = {
        "theme": "dark",
        "interval": interval,
        "studies": [
            {"name": "Volume", "forceOverlay": True},
            {"name": "Relative Strength Index", "input": {"length": 14}},
            {"name": "Moving Average Exponential", "input": {"length": 21}},
            {"name": "Moving Average", "input": {"length": 50}},
        ],
        "drawings": drawings,
    }

    url = "https://api.chart-img.com/v2/tradingview/advanced-chart"
    headers = {"x-api-key": api_key}

    # Backoff with jitter up to 4 tries
    last_err: Optional[Exception] = None
    for attempt in range(4):
        try:
            timeout = httpx.Timeout(15.0)
            async with httpx.AsyncClient(timeout=timeout) as client:
                for sym in symbol_candidates:
                    payload: Dict[str, Any] = {**base_payload, "symbol": sym}
                    logger.info(f"Chart-IMG request: symbol={sym} interval={interval}")
                    resp = await client.post(url, json=payload, headers=headers)
                    logger.info(f"Chart-IMG status: {resp.status_code} symbol={sym} interval={interval}")
                    if resp.status_code in (200, 201):
                        try:
                            data = resp.json()
                            # Chart-IMG returns one of these keys depending on endpoint
                            return data.get("url") or data.get("imageUrl") or data.get("image_url")
                        except Exception:
                            return None
                    # Non-200
                    body_head = (resp.text or "")[:150]
                    if resp.status_code in (429, 500, 502, 503, 504):
                        logger.warning(f"Chart-IMG retryable status={resp.status_code} body={body_head}")
                        # try next candidate this attempt; if all fail we'll backoff
                        continue
                    else:
                        logger.warning(f"Chart-IMG non-200 status={resp.status_code} body={body_head}")
                        # Try next candidate; if none succeed, return None (no point backoff on 4xx other than 429)
                        continue
                # If we exhausted candidates without success, raise to trigger backoff
                raise RuntimeError("all_symbol_candidates_failed")
        except Exception as e:
            last_err = e
            base = 0.4
            import random
            await asyncio.sleep(random.uniform(0, base * (2 ** attempt)))
    logger.error(f"Chart-IMG render failed after retries: {last_err}")
    return None
