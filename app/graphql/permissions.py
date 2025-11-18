"""
GraphQL Authorization and Permissions
Rate limiting, auth checks, and field-level permissions
"""

from typing import Any
from functools import wraps
import strawberry
from strawberry.permission import BasePermission
from strawberry.types import Info
from .context import GraphQLContext


class IsAuthenticated(BasePermission):
    """Check if user is authenticated"""
    message = "User is not authenticated"

    def has_permission(self, source: Any, info: Info[GraphQLContext], **kwargs) -> bool:
        context = info.context
        # For now, we accept all requests (no auth implemented in REST either)
        # In production, check JWT token or API key
        return True


class RateLimited(BasePermission):
    """Rate limit expensive operations"""
    message = "Rate limit exceeded"

    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    def has_permission(self, source: Any, info: Info[GraphQLContext], **kwargs) -> bool:
        context = info.context

        # Get client identifier (IP or user_id)
        client_id = context.user_id or "anonymous"
        cache_key = f"ratelimit:{client_id}"

        # This is a simplified version - in production use a sliding window
        # or token bucket algorithm with Redis
        return True  # Disabled for now


class IsPremium(BasePermission):
    """Check if user has premium access"""
    message = "Premium subscription required"

    def has_permission(self, source: Any, info: Info[GraphQLContext], **kwargs) -> bool:
        # Placeholder - implement based on your subscription model
        return True


def cached(ttl: int = 300):
    """
    Cache decorator for resolver results

    Args:
        ttl: Time to live in seconds (default 5 minutes)
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract info from kwargs
            info = kwargs.get('info')
            if not info or not hasattr(info, 'context'):
                return await func(*args, **kwargs)

            context = info.context

            # Generate cache key from function name and arguments
            # Simplified - in production, use a more robust key generation
            cache_key = f"graphql:{func.__name__}:{hash(frozenset(kwargs.items()))}"

            # Check cache
            cached_result = await context.cache.get(cache_key)
            if cached_result:
                import json
                return json.loads(cached_result)

            # Execute function
            result = await func(*args, **kwargs)

            # Cache result
            if result is not None:
                import json
                try:
                    # Convert result to JSON-serializable format
                    # This is simplified - may need custom serialization
                    await context.cache.setex(cache_key, ttl, json.dumps(result))
                except (TypeError, ValueError):
                    pass  # Skip caching if not serializable

            return result

        return wrapper
    return decorator


# Field-level permissions
class FieldPermission:
    """Apply permissions to specific fields"""

    @staticmethod
    def admin_only(field_name: str):
        """Restrict field to admin users only"""
        # Placeholder for admin-only fields
        return strawberry.field(permission_classes=[IsAuthenticated])

    @staticmethod
    def premium_only(field_name: str):
        """Restrict field to premium users"""
        return strawberry.field(permission_classes=[IsPremium])
