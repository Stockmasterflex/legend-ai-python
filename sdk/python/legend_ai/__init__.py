"""
Legend AI Python SDK

A professional Python SDK for the Legend AI Trading Pattern Scanner API.

Example:
    >>> from legend_ai import LegendAI
    >>> client = LegendAI(api_key="your-api-key")
    >>> pattern = client.patterns.detect("AAPL", interval="1day")
    >>> print(f"Pattern: {pattern.pattern}, Score: {pattern.score}")
"""

__version__ = "1.0.0"
__author__ = "Legend AI"
__license__ = "MIT"

from .client import LegendAI, AsyncLegendAI
from .exceptions import (
    LegendAIError,
    APIError,
    RateLimitError,
    AuthenticationError,
    ValidationError,
)
from .models import (
    PatternResult,
    ChartResult,
    ScanResult,
    WatchlistItem,
    PositionSize,
    Trade,
)

__all__ = [
    "LegendAI",
    "AsyncLegendAI",
    "LegendAIError",
    "APIError",
    "RateLimitError",
    "AuthenticationError",
    "ValidationError",
    "PatternResult",
    "ChartResult",
    "ScanResult",
    "WatchlistItem",
    "PositionSize",
    "Trade",
]
