"""
Background job to refresh the quick scan cache.
"""
import logging

from app.api.patterns import scan_quick_patterns

logger = logging.getLogger("quick_scan_warmup")


async def run_quick_scan_warmup():
    """
    Force a quick scan so cached results stay warm for the LiveScanner frontend.
    """
    try:
        result = await scan_quick_patterns(force_refresh=True)
        cache_status = result.meta or {}
        logger.info(
            "Quick scan warmup completed: %s results · cache=%s",
            result.count,
            cache_status.get("cached"),
        )
        return result
    except Exception as exc:
        logger.error("Quick scan warmup failed: %s", exc)
        return None
