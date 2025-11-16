"""
Simple Redis-based rate limiting middleware for FastAPI
Protects public endpoints from abuse
"""
import time
import logging
from typing import Optional, Callable
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from redis.asyncio import Redis

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware using Redis with sliding window algorithm.

    Rate limits:
    - Public endpoints: 60 requests per minute per IP
    - No limit on health checks or static files
    """

    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.window_seconds = 60
        self.redis: Optional[Redis] = None

    async def dispatch(self, request: Request, call_next: Callable):
        # Skip rate limiting for certain paths
        if self._should_skip_rate_limit(request):
            return await call_next(request)

        # Get client identifier (IP address)
        client_ip = self._get_client_ip(request)

        # Check rate limit
        try:
            is_allowed = await self._check_rate_limit(client_ip, request.url.path)
            if not is_allowed:
                logger.warning(f"Rate limit exceeded for {client_ip} on {request.url.path}")
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": "Rate limit exceeded. Please try again later.",
                        "limit": f"{self.requests_per_minute} requests per minute"
                    }
                )
        except Exception as e:
            # If rate limiting fails, allow the request but log the error
            logger.error(f"Rate limit check failed: {e}")

        return await call_next(request)

    def _should_skip_rate_limit(self, request: Request) -> bool:
        """Check if this request should skip rate limiting"""
        path = request.url.path

        # Skip for health checks
        if path in ["/health", "/", "/docs", "/openapi.json"]:
            return True

        # Skip for static files
        if path.startswith("/static/"):
            return True

        # Skip for dashboard HTML (rate limit the API calls instead)
        if path == "/dashboard":
            return True

        return False

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address, handling proxies"""
        # Check X-Forwarded-For header (set by Railway/proxies)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # X-Forwarded-For can be a comma-separated list
            return forwarded_for.split(",")[0].strip()

        # Check X-Real-IP header
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fall back to direct connection IP
        if request.client and request.client.host:
            return request.client.host

        return "unknown"

    async def _check_rate_limit(self, client_ip: str, path: str) -> bool:
        """
        Check if request is within rate limit using Redis sliding window.
        Returns True if allowed, False if rate limit exceeded.
        """
        # Lazy initialize Redis connection
        if self.redis is None:
            try:
                self.redis = Redis.from_url(settings.redis_url, decode_responses=True)
            except Exception as e:
                logger.error(f"Failed to connect to Redis for rate limiting: {e}")
                # Allow request if Redis is unavailable
                return True

        # Create rate limit key
        key = f"ratelimit:{client_ip}:{path}"
        now = int(time.time())
        window_start = now - self.window_seconds

        try:
            # Use Redis sorted set with timestamps
            pipe = self.redis.pipeline()

            # Remove old entries outside the window
            pipe.zremrangebyscore(key, 0, window_start)

            # Count requests in current window
            pipe.zcard(key)

            # Add current request
            pipe.zadd(key, {str(now): now})

            # Set expiry
            pipe.expire(key, self.window_seconds)

            # Execute pipeline
            results = await pipe.execute()

            # results[1] is the count before adding current request
            request_count = results[1]

            # Check if under limit
            return request_count < self.requests_per_minute

        except Exception as e:
            logger.error(f"Rate limit check error: {e}")
            # Allow request if rate limiting fails
            return True


def get_rate_limit_middleware(requests_per_minute: int = 60) -> RateLimitMiddleware:
    """Factory function to create rate limit middleware"""
    return lambda app: RateLimitMiddleware(app, requests_per_minute)
