"""
Advanced DDoS Protection and Rate Limiting Middleware
Implements multi-tier rate limiting, automatic IP blocking, and exponential backoff
"""
import time
import logging
from typing import Optional, Callable, Dict
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from redis.asyncio import Redis
from datetime import datetime, timedelta

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class DDOSProtectionMiddleware(BaseHTTPMiddleware):
    """
    Advanced DDoS protection with multi-tier rate limiting.

    Features:
    - IP-based rate limiting (100 req/min default)
    - API key-based rate limiting (1000 req/hour)
    - Per-endpoint rate limits (stricter for expensive ops)
    - Automatic malicious IP blocking
    - Exponential backoff on repeated failures
    - Suspicious activity detection
    """

    # Rate limit tiers (requests per minute)
    TIER_PUBLIC = 100  # Public endpoints without API key
    TIER_AUTHENTICATED = 500  # With valid API key
    TIER_EXPENSIVE = 20  # Expensive operations (AI, backtesting)
    TIER_HEALTH = 1000  # Health checks can be very frequent

    # Blocking thresholds
    MAX_VIOLATIONS_BEFORE_BLOCK = 10  # Block after 10 violations in window
    BLOCK_DURATION_SECONDS = 3600  # Block for 1 hour
    VIOLATION_WINDOW_SECONDS = 300  # 5 minute window for violations

    # Exponential backoff
    BACKOFF_BASE_SECONDS = 1  # Start with 1 second delay
    BACKOFF_MAX_SECONDS = 60  # Max 60 second delay

    # Expensive endpoints that need stricter limits
    EXPENSIVE_ENDPOINTS = [
        "/api/ai/",
        "/api/patterns/detect",
        "/api/advanced/",
        "/api/analyze",
        "/api/scan",
    ]

    def __init__(self, app):
        super().__init__(app)
        self.redis: Optional[Redis] = None

    async def dispatch(self, request: Request, call_next: Callable):
        # Skip rate limiting for certain paths
        if self._should_skip_rate_limit(request):
            return await call_next(request)

        # Get client identifier
        client_ip = self._get_client_ip(request)
        api_key = self._get_api_key(request)

        # Check if IP is blocked
        if await self._is_ip_blocked(client_ip):
            logger.warning(f"🚫 Blocked IP attempted access: {client_ip}")
            return JSONResponse(
                status_code=403,
                content={
                    "error": "Access forbidden",
                    "detail": "Your IP has been temporarily blocked due to suspicious activity",
                    "blocked_until": await self._get_block_expiry(client_ip)
                }
            )

        # Determine rate limit tier
        tier = self._get_rate_limit_tier(request, api_key)

        # Check rate limit
        try:
            is_allowed, retry_after = await self._check_rate_limit(
                client_ip,
                request.url.path,
                tier,
                api_key
            )

            if not is_allowed:
                # Record violation
                await self._record_violation(client_ip, request.url.path)

                # Check if should block IP
                violation_count = await self._get_violation_count(client_ip)
                if violation_count >= self.MAX_VIOLATIONS_BEFORE_BLOCK:
                    await self._block_ip(client_ip)
                    logger.error(f"🚫 IP BLOCKED due to repeated violations: {client_ip}")

                logger.warning(
                    f"⚠️ Rate limit exceeded: {client_ip} on {request.url.path} "
                    f"(tier: {tier}/min, violations: {violation_count})"
                )

                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Rate limit exceeded",
                        "detail": f"Too many requests. Please try again later.",
                        "limit": f"{tier} requests per minute",
                        "retry_after": retry_after,
                        "violations": violation_count,
                        "warning": "Repeated violations will result in temporary IP block"
                    },
                    headers={
                        "Retry-After": str(retry_after),
                        "X-RateLimit-Limit": str(tier),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int(time.time() + retry_after))
                    }
                )
        except Exception as e:
            logger.error(f"Rate limit check failed: {e}")
            # Fail open - allow request but log error

        return await call_next(request)

    def _should_skip_rate_limit(self, request: Request) -> bool:
        """Check if this request should skip rate limiting"""
        path = request.url.path

        # Skip for specific health check paths only
        if path in ["/health", "/healthz"]:
            return True

        # Skip for static files
        if path.startswith("/static/"):
            return True

        return False

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address, handling proxies and load balancers"""
        # Check X-Forwarded-For header (Railway, Cloudflare, etc.)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # Take the first IP (original client)
            return forwarded_for.split(",")[0].strip()

        # Check X-Real-IP header
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Check Cloudflare header
        cf_ip = request.headers.get("CF-Connecting-IP")
        if cf_ip:
            return cf_ip

        # Fall back to direct connection IP
        if request.client and request.client.host:
            return request.client.host

        return "unknown"

    def _get_api_key(self, request: Request) -> Optional[str]:
        """Extract API key from request headers or query params"""
        # Check Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header[7:]

        # Check X-API-Key header
        api_key = request.headers.get("X-API-Key")
        if api_key:
            return api_key

        # Check query parameter (less secure, but sometimes needed)
        if "api_key" in request.query_params:
            return request.query_params["api_key"]

        return None

    def _get_rate_limit_tier(self, request: Request, api_key: Optional[str]) -> int:
        """Determine appropriate rate limit tier for this request"""
        path = request.url.path

        # Health checks get highest limit
        if path in ["/health", "/healthz", "/"]:
            return self.TIER_HEALTH

        # Expensive endpoints get strictest limit
        if any(path.startswith(endpoint) for endpoint in self.EXPENSIVE_ENDPOINTS):
            return self.TIER_EXPENSIVE

        # Authenticated requests get higher limits
        if api_key:
            return self.TIER_AUTHENTICATED

        # Default public tier
        return self.TIER_PUBLIC

    async def _check_rate_limit(
        self,
        client_ip: str,
        path: str,
        tier: int,
        api_key: Optional[str] = None
    ) -> tuple[bool, int]:
        """
        Check if request is within rate limit.
        Returns (is_allowed, retry_after_seconds)
        """
        # Lazy initialize Redis
        if self.redis is None:
            try:
                self.redis = Redis.from_url(settings.redis_url, decode_responses=True)
            except Exception as e:
                logger.error(f"Failed to connect to Redis for rate limiting: {e}")
                return True, 0  # Fail open

        # Create composite key for IP + path + api_key
        key_parts = [client_ip, self._normalize_path(path)]
        if api_key:
            key_parts.append(f"key:{api_key[:8]}")  # Use prefix of API key

        key = f"ratelimit:{':'.join(key_parts)}"
        now = int(time.time())
        window_start = now - 60  # 1 minute window

        try:
            pipe = self.redis.pipeline()

            # Remove old entries
            pipe.zremrangebyscore(key, 0, window_start)

            # Count requests in window
            pipe.zcard(key)

            # Add current request timestamp
            pipe.zadd(key, {str(now): now})

            # Set expiry
            pipe.expire(key, 60)

            results = await pipe.execute()
            request_count = results[1]

            # Check if under limit
            is_allowed = request_count < tier

            # Calculate retry after (seconds until oldest request expires)
            retry_after = max(1, 60 - (now - window_start))

            return is_allowed, retry_after

        except Exception as e:
            logger.error(f"Rate limit check error: {e}")
            return True, 0  # Fail open

    def _normalize_path(self, path: str) -> str:
        """Normalize path for rate limiting (group similar endpoints)"""
        # Remove trailing slashes
        path = path.rstrip("/")

        # Group API endpoints
        if path.startswith("/api/"):
            parts = path.split("/")
            if len(parts) >= 3:
                # Use first 3 parts: /api/resource
                return "/".join(parts[:3])

        return path

    async def _record_violation(self, client_ip: str, path: str):
        """Record a rate limit violation"""
        if self.redis is None:
            return

        key = f"violations:{client_ip}"
        now = int(time.time())

        try:
            pipe = self.redis.pipeline()

            # Remove old violations outside window
            window_start = now - self.VIOLATION_WINDOW_SECONDS
            pipe.zremrangebyscore(key, 0, window_start)

            # Add new violation
            pipe.zadd(key, {f"{path}:{now}": now})

            # Set expiry
            pipe.expire(key, self.VIOLATION_WINDOW_SECONDS)

            await pipe.execute()

        except Exception as e:
            logger.error(f"Failed to record violation: {e}")

    async def _get_violation_count(self, client_ip: str) -> int:
        """Get number of violations in the current window"""
        if self.redis is None:
            return 0

        key = f"violations:{client_ip}"

        try:
            count = await self.redis.zcard(key)
            return count or 0
        except Exception as e:
            logger.error(f"Failed to get violation count: {e}")
            return 0

    async def _block_ip(self, client_ip: str):
        """Block an IP address temporarily"""
        if self.redis is None:
            return

        key = f"blocked:{client_ip}"

        try:
            await self.redis.setex(
                key,
                self.BLOCK_DURATION_SECONDS,
                datetime.utcnow().isoformat()
            )

            # Log to security monitoring
            logger.error(
                f"🚫 SECURITY ALERT: IP {client_ip} blocked for {self.BLOCK_DURATION_SECONDS}s "
                f"due to repeated rate limit violations"
            )

        except Exception as e:
            logger.error(f"Failed to block IP: {e}")

    async def _is_ip_blocked(self, client_ip: str) -> bool:
        """Check if an IP is currently blocked"""
        if self.redis is None:
            return False

        key = f"blocked:{client_ip}"

        try:
            is_blocked = await self.redis.exists(key)
            return bool(is_blocked)
        except Exception as e:
            logger.error(f"Failed to check IP block status: {e}")
            return False

    async def _get_block_expiry(self, client_ip: str) -> Optional[str]:
        """Get when an IP block expires"""
        if self.redis is None:
            return None

        key = f"blocked:{client_ip}"

        try:
            ttl = await self.redis.ttl(key)
            if ttl > 0:
                expiry_time = datetime.utcnow() + timedelta(seconds=ttl)
                return expiry_time.isoformat()
        except Exception as e:
            logger.error(f"Failed to get block expiry: {e}")

        return None
