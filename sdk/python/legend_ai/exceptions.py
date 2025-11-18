"""
Exception classes for Legend AI SDK
"""


class LegendAIError(Exception):
    """Base exception for all Legend AI errors"""
    pass


class APIError(LegendAIError):
    """General API error"""
    pass


class RateLimitError(LegendAIError):
    """Rate limit exceeded"""
    pass


class AuthenticationError(LegendAIError):
    """Authentication failed"""
    pass


class ValidationError(LegendAIError):
    """Request validation failed"""
    pass


class ResourceNotFoundError(LegendAIError):
    """Requested resource not found"""
    pass
