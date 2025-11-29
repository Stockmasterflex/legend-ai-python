"""Scan endpoints with telemetry and Top Setups.

Provides both POST/GET `/api/scan` endpoints plus `/api/top-setups` for the dashboard.
Combines universe scanning with flag-gated VCP scanner and comprehensive telemetry.
"""
from __future__ import annotations

import asyncio
import json
import time
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from collections import defaultdict

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
from app.services.pattern_scanner import pattern_scanner_service
from app.telemetry.metrics import (
    SCAN_ERRORS_TOTAL,
    SCAN_REQUEST_DURATION_SECONDS,
)
from app.utils.build_info import resolve_build_sha
from app.services.cache import get_cache_service
from app.utils.pattern_groups import bucket_name

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["scan"])
cache_service = get_cache_service()
SCAN_LATEST_KEY = "scan:latest"
SCAN_HISTORY_TEMPLATE = "scan:results:{date}"


def _bucketize_entries(entries: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    buckets: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for entry in entries:
        bucket = bucket_name(entry.get("pattern", ""))
        if bucket:
            buckets[bucket].append(entry)
    return dict(buckets)


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
    min_score: float = Query(6.0, ge=0.0, le=10.0),  # Temporarily lowered to debug
):
    """Return the latest top setups for the dashboard tab with timeout protection."""

    try:
        # Add timeout protection (max 15 seconds)
        async with asyncio.timeout(15.0):
            results, cached = await _load_top_setups(min_score, limit)

        return TopSetupsResponse(
            success=True,
            count=len(results),
            min_score=min_score,
            cached=cached,
            generated_at=datetime.utcnow(),
            results=results,
        )
    except asyncio.TimeoutError:
        logger.warning(f"⏱️ Top setups request timed out after 15s - returning empty results")
        # Return empty results instead of failing
        return TopSetupsResponse(
            success=True,
            count=0,
            min_score=min_score,
            cached=False,
            generated_at=datetime.utcnow(),
            results=[],
        )
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive guard
        logger.error(f"❌ Failed to load top setups: {exc}", exc_info=True)
        # Return empty results on error instead of raising 500
        return TopSetupsResponse(
            success=True,
            count=0,
            min_score=min_score,
            cached=False,
            generated_at=datetime.utcnow(),
            results=[],
        )


@router.get("/scan/latest")
async def get_latest_scan_result() -> Dict[str, Any]:
    """Return the latest cached EOD scan payload."""
    payload = await cache_service.get(SCAN_LATEST_KEY)
    if not payload:
        raise HTTPException(status_code=404, detail="No scan results yet")
    return payload


@router.get("/scan/date/{scan_date}")
async def get_scan_by_date(scan_date: str) -> Dict[str, Any]:
    """Return cached scan results for a specific date (YYYYMMDD)."""
    key = SCAN_HISTORY_TEMPLATE.format(date=scan_date)
    payload = await cache_service.get(key)
    if not payload:
        raise HTTPException(status_code=404, detail=f"No scan data for {scan_date}")
    return payload


@router.get("/scan/sector/{sector}")
async def get_scan_by_sector(sector: str) -> Dict[str, Any]:
    """Return latest scan data filtered by sector name."""
    payload = await cache_service.get(SCAN_LATEST_KEY)
    if not payload:
        raise HTTPException(status_code=404, detail="No scan results yet")

    sector_normalized = sector.strip().lower()
    filtered = [
        entry for entry in payload.get("results", [])
        if (entry.get("sector") or "").strip().lower() == sector_normalized
    ]
    summary = {
        "scan_date": payload.get("scan_date"),
        "total_symbols": payload.get("total_symbols"),
        "patterns_found": len(filtered),
        "buckets": _bucketize_entries(filtered),
        "top_setups": sorted(filtered, key=lambda item: item.get("score", 0), reverse=True)[:10],
        "results": filtered,
        "generated_at": payload.get("generated_at"),
    }
    return summary


async def _load_top_setups(min_score: float, limit: int) -> tuple[list[ScanResult], bool]:
    """Fetch cached universe scan results or trigger a fresh run using multi-pattern scanner."""

    logger.info(f"Loading top setups: min_score={min_score}, limit={limit}")
    cached = False
    results = []

    cache_key = f"top_setups:multi:min{min_score}"
    latest_payload = await cache_service.get(SCAN_LATEST_KEY)
    if latest_payload:
        cached = True
        results = [
            {
                "ticker": item.get("symbol") or item.get("ticker"),
                "pattern": item.get("pattern"),
                "score": item.get("score"),
                "entry": item.get("entry"),
                "stop": item.get("stop"),
                "target": item.get("target"),
                "risk_reward": item.get("risk_reward"),
                "current_price": item.get("current_price"),
                "source": item.get("sector") or "Legend AI",
            }
            for item in latest_payload.get("top_setups", [])
            if item.get("score", 0) >= min_score
        ]
        logger.info("Using nightly scan data for top setups (%s entries)", len(results))
        if results:
            normalized = [_coerce_scan_result(item) for item in results[:limit]]
            logger.info(f"Returning {len(normalized)} normalized top setups (cached={cached})")
            return normalized, cached

    # Try Redis cache first to keep responses fast.
    try:
        redis = await universe_service.cache._get_redis()
        cached_payload = await redis.get(cache_key)
        if cached_payload:
            cached = True
            results = json.loads(cached_payload)
            logger.info(f"✅ Top setups cache hit: {len(results)} results")
        else:
            logger.info("Top setups cache miss")
    except Exception as exc:
        logger.warning(f"Top setups cache lookup failed: {exc}")

    # Run a fresh scan using the old VCP scanner as fallback
    if not results:
        logger.info(f"Running fallback VCP scan for top setups (min_score={min_score})")
        try:
            # Use the old scanner temporarily
            from app.services.scanner import scan_service
            scan_result = await scan_service.run_daily_vcp_scan(limit=max(limit, 20))

            logger.info(f"VCP scan result: results_count={len(scan_result.get('results', []))}")

            if scan_result.get("results"):
                # Convert old format to new format
                converted_results = []
                for item in scan_result["results"]:
                    converted_results.append({
                        "ticker": item.get("ticker", item.get("symbol", "???")),
                        "pattern": item.get("pattern", "VCP"),
                        "score": float(item.get("score", 0)),
                        "entry": item.get("entry", 0),
                        "stop": item.get("stop", 0),
                        "target": item.get("target", 0),
                        "risk_reward": item.get("risk_reward", 0),
                        "current_price": item.get("current_price"),
                        "source": "VCP_Scanner"
                    })
                results = converted_results
                logger.info(f"Using {len(results)} results from VCP scan")

                # Cache the results for 1 hour
                try:
                    redis = await universe_service.cache._get_redis()
                    await redis.setex(cache_key, 3600, json.dumps(results))
                    logger.info(f"✅ Cached {len(results)} top setups")
                except Exception as exc:
                    logger.warning(f"Failed to cache top setups: {exc}")
            else:
                logger.warning("VCP scan returned no results")
        except Exception as exc:
            logger.error(f"VCP scan failed: {exc}")

    # Fall back to quick scan if we still don't have data.
    if not results:
        logger.info("Top setups falling back to quick scan")
        try:
            # Create a default QuickScanRequest for fallback
            from app.api.universe import QuickScanRequest
            default_request = QuickScanRequest(
                universe="nasdaq100",
                limit=max(limit * 2, 20),  # Scan more for better results
                min_score=min_score,
                min_rs=60.0,
                timeframe="1day"
            )
            fallback = await quick_scan(default_request)
            raw_results = fallback.get("data", [])
            results = _normalize_quick_scan(raw_results)
            logger.info(f"Quick scan fallback: {len(raw_results)} raw results, {len(results)} normalized")
        except Exception as exc:
            logger.error(f"Quick scan fallback failed: {exc}")

    normalized = [_coerce_scan_result(item) for item in results[:limit]]
    logger.info(f"Returning {len(normalized)} normalized top setups (cached={cached})")
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

    # Handle both "symbol" (from pattern_scanner) and "ticker" (from old scanner)
    ticker = item.get("ticker") or item.get("symbol", "???")

    return {
        "ticker": ticker,
        "pattern": item.get("pattern", "Unknown"),
        "score": float(item.get("score") or 0.0),
        "entry": _to_float(item.get("entry")),
        "stop": _to_float(item.get("stop")),
        "target": _to_float(item.get("target")),
        "risk_reward": float(item.get("risk_reward") or 0.0),
        "current_price": item.get("current_price"),
        "source": item.get("source", "Multi-Pattern"),
    }


def _to_float(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


@router.get("/scan/patterns")
async def scan_patterns(
    request: Request,
    limit: int = Query(50, ge=1, le=200),
    min_score: float = Query(7.0, ge=0.0, le=10.0),
    patterns: Optional[str] = Query(None, description="Comma-separated pattern names to filter by"),
) -> Dict[str, Any]:
    """
    Multi-pattern scanner endpoint - scans universe with all available detectors

    This endpoint uses the new modular detector system to find patterns across
    all 17+ available pattern types (VCP, Cup & Handle, Triangles, Wedges, etc.)

    Query Parameters:
        limit: Maximum number of results to return (1-200)
        min_score: Minimum pattern score to include (0-10 scale)
        patterns: Optional comma-separated list of specific patterns to scan for
                 Example: "VCP,Cup & Handle,Ascending Triangle"

    Returns:
        Scan results with detected patterns sorted by score
    """
    started = time.perf_counter()

    telemetry: Dict[str, Any] = {
        "event": "scan_patterns",
        "status": "pending",
        "limit": limit,
        "min_score": min_score,
    }
    request.state.telemetry = telemetry

    try:
        # Parse pattern filter if provided
        pattern_filter = None
        if patterns:
            pattern_filter = [p.strip() for p in patterns.split(",") if p.strip()]
            telemetry["pattern_filter"] = pattern_filter

        telemetry["status"] = "running"

        # Run multi-pattern scan
        payload = await pattern_scanner_service.scan_universe(
            universe=None,  # Use default universe
            limit=limit,
            pattern_filter=pattern_filter,
            min_score=min_score
        )

        telemetry.update({
            "status": "ok",
            "scan_universe": payload.get("universe_size"),
            "scan_results": len(payload.get("results", [])),
            "total_hits": payload.get("meta", {}).get("total_hits", 0),
        })

        return payload

    except Exception as exc:
        telemetry["status"] = "error"
        SCAN_ERRORS_TOTAL.inc()
        logger.exception("Multi-pattern scan failed: %s", exc)
        raise HTTPException(status_code=500, detail="Multi-pattern scan failed") from exc
    finally:
        duration = time.perf_counter() - started
        telemetry["duration_ms"] = round(duration * 1000, 2)
        SCAN_REQUEST_DURATION_SECONDS.labels(
            status=telemetry.get("status", "unknown"),
            universe_size=str(telemetry.get("scan_universe", 0)),
        ).observe(duration)
