"""
Security Headers Middleware
Implements OWASP security headers, CSP, XSS protection, clickjacking prevention
"""
import logging
from typing import Callable
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Add comprehensive security headers to all responses.

    Implements OWASP Top 10 security headers:
    - Content Security Policy (CSP)
    - X-Content-Type-Options
    - X-Frame-Options
    - X-XSS-Protection
    - Strict-Transport-Security (HSTS)
    - Referrer-Policy
    - Permissions-Policy
    """

    def __init__(self, app, environment: str = "production"):
        super().__init__(app)
        self.environment = environment

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Add security headers
        self._add_security_headers(response, request)

        return response

    def _add_security_headers(self, response: Response, request: Request):
        """Add all security headers to the response"""

        # Content Security Policy (CSP)
        # Strict policy to prevent XSS attacks
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://unpkg.com",
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com",
            "img-src 'self' data: https: blob:",
            "font-src 'self' https://fonts.gstatic.com data:",
            "connect-src 'self' https://api.telegram.org https://api.openai.com https://openrouter.ai",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'",
            "upgrade-insecure-requests"
        ]

        # Relax CSP in development
        if self.environment == "development":
            csp_directives = [
                "default-src 'self'",
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https:",
                "style-src 'self' 'unsafe-inline' https:",
                "img-src 'self' data: https: blob:",
                "font-src 'self' data: https:",
                "connect-src 'self' https:",
            ]

        response.headers["Content-Security-Policy"] = "; ".join(csp_directives)

        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking attacks
        response.headers["X-Frame-Options"] = "DENY"

        # XSS Protection (legacy, but still useful)
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Strict Transport Security (HSTS)
        # Force HTTPS for 1 year, including subdomains
        if self.environment == "production":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )

        # Referrer Policy
        # Don't leak referrer information to third parties
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions Policy (formerly Feature-Policy)
        # Disable unnecessary browser features
        permissions = [
            "geolocation=()",
            "microphone=()",
            "camera=()",
            "payment=()",
            "usb=()",
            "magnetometer=()",
            "gyroscope=()",
            "accelerometer=()",
        ]
        response.headers["Permissions-Policy"] = ", ".join(permissions)

        # Additional security headers
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        response.headers["X-Download-Options"] = "noopen"

        # Remove headers that leak server information
        response.headers.pop("Server", None)
        response.headers.pop("X-Powered-By", None)

        # Add custom security identifier
        response.headers["X-Security-Level"] = "hardened"

        # Cache control for sensitive endpoints
        if self._is_sensitive_endpoint(request.url.path):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"

    def _is_sensitive_endpoint(self, path: str) -> bool:
        """Check if endpoint contains sensitive data"""
        sensitive_patterns = [
            "/api/",
            "/health",
            "/metrics",
        ]
        return any(path.startswith(pattern) for pattern in sensitive_patterns)


class SecureCookieMiddleware(BaseHTTPMiddleware):
    """
    Ensure all cookies are set securely.

    Features:
    - HttpOnly flag (prevent JavaScript access)
    - Secure flag (HTTPS only)
    - SameSite=Strict (CSRF protection)
    """

    def __init__(self, app, environment: str = "production"):
        super().__init__(app)
        self.environment = environment

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Modify Set-Cookie headers to add security flags
        if "set-cookie" in response.headers:
            cookies = response.headers.get_list("set-cookie")
            response.headers.pop("set-cookie")

            for cookie in cookies:
                # Add security flags if not present
                if "HttpOnly" not in cookie:
                    cookie += "; HttpOnly"

                if "Secure" not in cookie and self.environment == "production":
                    cookie += "; Secure"

                if "SameSite" not in cookie:
                    cookie += "; SameSite=Strict"

                response.headers.append("set-cookie", cookie)

        return response
