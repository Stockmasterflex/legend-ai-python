import json
import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.flags import LEGEND_FLAGS
from app.utils.build_info import resolve_build_sha


class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    """Emit JSON logs for every request without touching handlers."""

    def __init__(self, app):
        super().__init__(app)
        self.logger = logging.getLogger("legend.telemetry")
        self.build_sha = resolve_build_sha()

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response: Optional[Response] = None
        status_code = 500
        exc: Optional[Exception] = None
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        except Exception as err:  # pragma: no cover - bubbled to FastAPI
            exc = err
            status_code = 500
            raise
        finally:
            duration_ms = round((time.perf_counter() - start) * 1000, 3)
            metadata = self._extract_metadata(request)
            cache_hit = metadata.get("cache_hit")
            if cache_hit is None and response is not None:
                cache_header = response.headers.get("x-cache-hit")
                if cache_header is not None:
                    cache_hit = cache_header.lower() == "true"

            level_name = metadata.get("level") or self._level_from_status(status_code)
            payload: Dict[str, Any] = {
                "ts": datetime.now(timezone.utc).isoformat(),
                "level": level_name,
                "event": metadata.get("event") or f"{request.method} {request.url.path}",
                "symbol": metadata.get("symbol"),
                "interval": metadata.get("interval"),
                "status": metadata.get("status") or status_code,
                "duration_ms": duration_ms,
                "cache_hit": cache_hit,
                "build_sha": self.build_sha,
                "route": metadata.get("route") or self._lookup_route(request),
                "flag_scanner_enabled": LEGEND_FLAGS.enable_scanner,
            }
            logger_method = getattr(self.logger, level_name.lower(), self.logger.info)
            logger_method(json.dumps(payload))

    def _extract_metadata(self, request: Request) -> Dict[str, Any]:
        metadata: Dict[str, Any] = {}
        if hasattr(request.state, "telemetry"):
            metadata.update(getattr(request.state, "telemetry") or {})
        metadata.setdefault("symbol", self._lookup_symbol(request))
        metadata.setdefault("interval", self._lookup_interval(request))
        metadata.setdefault("route", self._lookup_route(request))
        return metadata

    @staticmethod
    def _lookup_symbol(request: Request) -> Optional[str]:
        for key in ("ticker", "symbol"):
            if key in request.query_params:
                return request.query_params[key].upper()
            if key in request.path_params:
                value = request.path_params[key]
                if isinstance(value, str):
                    return value.upper()
        return None

    @staticmethod
    def _lookup_interval(request: Request) -> Optional[str]:
        for key in ("tf", "interval", "timeframe"):
            if key in request.query_params:
                return request.query_params[key]
            if key in request.path_params:
                return request.path_params[key]
        return None

    @staticmethod
    def _lookup_route(request: Request) -> Optional[str]:
        route = request.scope.get("route")
        if route and hasattr(route, "path"):
            return getattr(route, "path", None)
        return request.url.path

    @staticmethod
    def _level_from_status(status_code: int) -> str:
        if status_code >= 500:
            return "ERROR"
        if status_code >= 400:
            return "WARNING"
        return "INFO"
