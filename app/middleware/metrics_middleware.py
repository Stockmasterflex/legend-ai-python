"""
Enhanced metrics middleware for comprehensive monitoring
Tracks all HTTP requests, response times, error rates, and more
"""

import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.telemetry.metrics import (ERROR_RATE_TOTAL,
                                   HTTP_REQUEST_DURATION_SECONDS,
                                   HTTP_REQUEST_SIZE_BYTES,
                                   HTTP_REQUESTS_TOTAL,
                                   HTTP_RESPONSE_SIZE_BYTES)

logger = logging.getLogger(__name__)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to track comprehensive HTTP metrics"""

    async def dispatch(self, request: Request, call_next):
        # Skip metrics for the metrics endpoint itself
        if request.url.path == "/metrics":
            return await call_next(request)

        # Normalize endpoint path (replace IDs with placeholders)
        endpoint = self._normalize_path(request.url.path)
        method = request.method

        # Track request size
        request_size = int(request.headers.get("content-length", 0))
        if request_size > 0:
            HTTP_REQUEST_SIZE_BYTES.labels(method=method, endpoint=endpoint).observe(
                request_size
            )

        # Time the request
        start_time = time.perf_counter()

        # Process request and handle errors
        status_code = 500
        response = None

        try:
            response = await call_next(request)
            status_code = response.status_code

            # Track error rates
            if status_code >= 400:
                error_type = "client_error" if status_code < 500 else "server_error"
                severity = "warning" if status_code < 500 else "error"
                ERROR_RATE_TOTAL.labels(
                    error_type=error_type, severity=severity, endpoint=endpoint
                ).inc()

            return response

        except Exception as e:
            # Track unhandled exceptions
            ERROR_RATE_TOTAL.labels(
                error_type="exception", severity="critical", endpoint=endpoint
            ).inc()
            logger.error(f"Unhandled exception in {endpoint}: {e}")
            raise

        finally:
            # Track request duration
            duration = time.perf_counter() - start_time

            HTTP_REQUESTS_TOTAL.labels(
                method=method, endpoint=endpoint, status_code=status_code
            ).inc()

            HTTP_REQUEST_DURATION_SECONDS.labels(
                method=method, endpoint=endpoint, status_code=status_code
            ).observe(duration)

            # Track response size
            if response:
                response_size = int(response.headers.get("content-length", 0))
                if response_size > 0:
                    HTTP_RESPONSE_SIZE_BYTES.labels(
                        method=method, endpoint=endpoint
                    ).observe(response_size)

    def _normalize_path(self, path: str) -> str:
        """Normalize path by replacing variable segments"""
        # Skip normalization for root and static paths
        if path in ["/", "/health", "/healthz", "/metrics", "/docs", "/openapi.json"]:
            return path

        parts = path.split("/")
        normalized_parts = []

        for i, part in enumerate(parts):
            # Replace ticker symbols (uppercase, 1-5 chars)
            if part.isupper() and 1 <= len(part) <= 5:
                normalized_parts.append("{ticker}")
            # Replace numeric IDs
            elif part.isdigit():
                normalized_parts.append("{id}")
            # Replace UUIDs
            elif "-" in part and len(part) == 36:
                normalized_parts.append("{uuid}")
            else:
                normalized_parts.append(part)

        return "/".join(normalized_parts)
