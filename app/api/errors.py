"""
Error monitoring and statistics API endpoints.
"""

import logging
from typing import Any, Dict, List

from fastapi import APIRouter

from app.core.error_recovery import _circuit_breakers, health_monitor
from app.core.errors import error_aggregator

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/errors", tags=["errors"])


@router.get("/stats")
async def get_error_stats() -> Dict[str, Any]:
    """
    Get error aggregation statistics.

    Returns summary of error groups, total errors, and top error types.
    """
    return error_aggregator.get_stats()


@router.get("/groups")
async def get_error_groups() -> List[Dict[str, Any]]:
    """
    Get all error groups with details.

    Returns detailed information about each error group including samples.
    """
    groups = error_aggregator.get_groups()
    return [
        {
            "fingerprint": g.fingerprint,
            "exception_type": g.exception_type,
            "first_seen": g.first_seen.isoformat(),
            "last_seen": g.last_seen.isoformat(),
            "occurrences": g.occurrences,
            "samples": [
                {
                    "timestamp": s.timestamp.isoformat(),
                    "message": s.message,
                    "context": s.context.to_dict(),
                }
                for s in g.samples[:3]  # First 3 samples
            ],
        }
        for g in groups[:50]  # Top 50 groups
    ]


@router.get("/circuits")
async def get_circuit_breakers() -> Dict[str, Any]:
    """
    Get circuit breaker states for all services.

    Shows which external services are healthy, degraded, or unavailable.
    """
    return {name: breaker.get_state() for name, breaker in _circuit_breakers.items()}


@router.get("/health")
async def get_service_health() -> Dict[str, Any]:
    """
    Get health metrics for all monitored services.

    Returns success rates, average durations, and recent errors.
    """
    return health_monitor.get_all_health()


@router.post("/clear")
async def clear_error_stats() -> Dict[str, str]:
    """
    Clear all error statistics (admin only).

    Use with caution - clears error aggregation data.
    """
    error_aggregator.clear()
    logger.warning("Error statistics cleared via API")
    return {"status": "cleared", "message": "All error statistics have been cleared"}
