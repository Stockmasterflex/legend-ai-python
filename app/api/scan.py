"""Scan endpoints with telemetry and Top Setups.

Provides both POST/GET `/api/scan` endpoints plus `/api/top-setups` for the dashboard.
Combines universe scanning with flag-gated VCP scanner and comprehensive telemetry.
"""
from __future__ import annotations

import json
import time
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel

from app.api.universe import (
    ScanRequest,
    ScanResponse,
    ScanResult,
    scan_universe as universe_scan_handler,
    quick_scan,
)
from app.services.universe import universe_service
from app.core.flags import get_legend_flags
from app.services.scanner import scan_service
from app.telemetry.metrics import (
    SCAN_ERRORS_TOTAL,
    SCAN_REQUEST_DURATION_SECONDS,
)
from app.utils.build_info import resolve_build_sha

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["scan"])


def _disabled_payload() -> Dict[str, Any]:
    return {
        "as_of": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "universe_size": 0,
        "results": [],
        "meta": {
            "build_sha": resolve_build_sha(),
            "duration_ms": 0.0,
            "result_count": 0,
            "total_hits": 0,
            "reason": "scanner_disabled",
        },
    }


@router.post("/scan", response_model=ScanResponse)
async def scan_alias(request: ScanRequest):
    """Stable alias for the existing universe scan endpoint."""
    return await universe_scan_handler(request)


@router.get("/scan")
async def scan_endpoint(
    request: Request,
    limit: int = Query(50, ge=1, le=200),
    sector: Optional[str] = Query(None),
) -> Dict[str, Any]:
    """GET endpoint for flag-gated VCP scanner with telemetry."""
    started = time.perf_counter()
    sector_filter = sector.strip() if sector and sector.strip() else None
    telemetry: Dict[str, Any] = {
        "event": "scan",
        "status": "pending",
        "limit": limit,
        "sector": sector_filter,
    }
    request.state.telemetry = telemetry
    flags = get_legend_flags()
    payload: Optional[Dict[str, Any]] = None

    if not flags.enable_scanner:
        telemetry.update({"status": "disabled", "scan_universe": 0, "scan_results": 0})
        payload = _disabled_payload()
        return payload

    try:
        telemetry["status"] = "running"
        payload = await scan_service.run_daily_vcp_scan(limit=limit, sector=sector_filter)
        telemetry.update(
            {
                "status": "ok",
                "scan_universe": payload.get("universe_size"),
                "scan_results": len(payload.get("results", [])),
            }
        )
        return payload
    except Exception as exc:
        telemetry["status"] = "error"
        SCAN_ERRORS_TOTAL.inc()
        logger.exception("scan_failed: %s", exc)
        raise HTTPException(status_code=500, detail="scan_failed") from exc
    finally:
        duration = time.perf_counter() - started
        telemetry["duration_ms"] = round(duration * 1000, 2)
        universe_size = payload.get("universe_size", 0) if payload else 0
        status_label = telemetry.get("status", "unknown")
        SCAN_REQUEST_DURATION_SECONDS.labels(
            status=status_label,
            universe_size=str(universe_size),
        ).observe(duration)


class TopSetupsResponse(BaseModel):
    """Response payload for GET /api/top-setups."""

    success: bool
    count: int
    min_score: float
    cached: bool
    generated_at: datetime
    results: List[ScanResult]


@router.get("/top-setups", response_model=TopSetupsResponse)
async def get_top_setups(
    limit: int = Query(10, ge=1, le=50),
    min_score: float = Query(7.0, ge=0.0, le=10.0),
):
    """Return the latest top setups for the dashboard tab."""

    try:
        results, cached = await _load_top_setups(min_score, limit)

        return TopSetupsResponse(
            success=True,
            count=len(results),
            min_score=min_score,
            cached=cached,
            generated_at=datetime.utcnow(),
            results=results,
        )
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive guard
        logger.error("Failed to load top setups: %s", exc)
        raise HTTPException(status_code=500, detail="Unable to load top setups")


async def _load_top_setups(min_score: float, limit: int) -> tuple[list[ScanResult], bool]:
    """Fetch cached universe scan results or trigger a fresh run."""

    cached = False
    results = []

    cache_key = f"universe:scan:min{min_score}"

    # Try Redis cache first to keep responses fast.
    try:
        redis = await universe_service.cache._get_redis()
        cached_payload = await redis.get(cache_key)
        if cached_payload:
            cached = True
            results = json.loads(cached_payload)
    except Exception as exc:
        logger.debug("Top setups cache lookup failed: %s", exc)

    # Run a fresh universe scan (it will populate cache) if needed.
    if not results:
        results = await universe_service.scan_universe(
            min_score=min_score,
            max_results=max(limit, 20),
            pattern_types=None,
        )

    # Fall back to quick scan cache if we still don't have data.
    if not results:
        logger.info("Top setups falling back to quick scan cache")
        fallback = await quick_scan()
        results = _normalize_quick_scan(fallback.get("results", []))

    normalized = [_coerce_scan_result(item) for item in results[:limit]]
    return normalized, cached


def _normalize_quick_scan(results: list[dict]) -> list[dict]:
    """Convert quick scan payloads into ScanResult-compatible dicts."""

    normalized = []
    for item in results:
        entry = _to_float(item.get("entry"))
        stop = _to_float(item.get("stop"))
        target = _to_float(item.get("target"))
        risk = max(entry - stop, 0.01)
        reward = max(target - entry, 0.0)
        risk_reward = round(reward / risk, 2) if risk else 0.0
        normalized.append(
            {
                "ticker": item.get("ticker", "???"),
                "pattern": item.get("pattern", "Unknown"),
                "score": float(item.get("score") or 0.0),
                "entry": entry,
                "stop": stop,
                "target": target,
                "risk_reward": risk_reward,
                "current_price": None,
                "source": item.get("source", "Top50"),
            }
        )
    return normalized


def _coerce_scan_result(item: dict) -> dict:
    """Ensure dict matches ScanResult schema (floats required)."""

    return {
        "ticker": item.get("ticker", "???"),
        "pattern": item.get("pattern", "Unknown"),
        "score": float(item.get("score") or 0.0),
        "entry": _to_float(item.get("entry")),
        "stop": _to_float(item.get("stop")),
        "target": _to_float(item.get("target")),
        "risk_reward": float(item.get("risk_reward") or 0.0),
        "current_price": item.get("current_price"),
        "source": item.get("source", "Universe"),
    }


def _to_float(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0
