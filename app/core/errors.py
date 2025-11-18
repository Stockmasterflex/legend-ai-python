"""
Custom exception hierarchy and error handling utilities for Legend AI.

This module provides:
- Custom exception classes with context
- Error categorization (transient, permanent, retryable)
- Error aggregation and reporting
- Structured error logging utilities
"""

import functools
import logging
import time
import traceback
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar
from collections import defaultdict
from threading import Lock

logger = logging.getLogger(__name__)

# Type variable for decorators
F = TypeVar("F", bound=Callable[..., Any])


class ErrorCategory(str, Enum):
    """Error categories for classification and handling strategies."""

    TRANSIENT = "transient"  # Temporary, retry might succeed
    PERMANENT = "permanent"  # Permanent, retry won't help
    VALIDATION = "validation"  # User input validation error
    EXTERNAL = "external"  # External service/API error
    DATA = "data"  # Data processing error
    CONFIGURATION = "configuration"  # Configuration/setup error
    INTERNAL = "internal"  # Internal programming error


class ErrorSeverity(str, Enum):
    """Error severity levels for prioritization."""

    LOW = "low"  # Minor issue, no user impact
    MEDIUM = "medium"  # Some degradation, partial functionality
    HIGH = "high"  # Significant impact, major functionality broken
    CRITICAL = "critical"  # System down or data loss risk


@dataclass
class ErrorContext:
    """Context information for errors."""

    timestamp: datetime = field(default_factory=datetime.utcnow)
    category: ErrorCategory = ErrorCategory.INTERNAL
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    retryable: bool = False
    user_message: Optional[str] = None
    technical_details: Dict[str, Any] = field(default_factory=dict)
    stack_trace: Optional[str] = None
    recovery_hint: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "category": self.category.value,
            "severity": self.severity.value,
            "retryable": self.retryable,
            "user_message": self.user_message,
            "technical_details": self.technical_details,
            "stack_trace": self.stack_trace,
            "recovery_hint": self.recovery_hint,
        }


# ============================================================================
# CUSTOM EXCEPTION HIERARCHY
# ============================================================================


class LegendAIError(Exception):
    """
    Base exception for all Legend AI errors.

    Provides:
    - Error categorization
    - Severity levels
    - Retry guidance
    - User-friendly messages
    - Technical context
    """

    category: ErrorCategory = ErrorCategory.INTERNAL
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    retryable: bool = False
    default_user_message: str = "An error occurred while processing your request"
    recovery_hint: Optional[str] = None

    def __init__(
        self,
        message: str,
        *,
        user_message: Optional[str] = None,
        technical_details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
        recovery_hint: Optional[str] = None,
    ):
        super().__init__(message)
        self.message = message
        self.user_message = user_message or self.default_user_message
        self.technical_details = technical_details or {}
        self.cause = cause
        self.recovery_hint = recovery_hint or self.recovery_hint
        self.timestamp = datetime.utcnow()

    def get_context(self) -> ErrorContext:
        """Get structured error context."""
        return ErrorContext(
            timestamp=self.timestamp,
            category=self.category,
            severity=self.severity,
            retryable=self.retryable,
            user_message=self.user_message,
            technical_details=self.technical_details,
            stack_trace=traceback.format_exc() if self.cause else None,
            recovery_hint=self.recovery_hint,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            "error": self.__class__.__name__,
            "message": self.user_message,
            "category": self.category.value,
            "severity": self.severity.value,
            "retryable": self.retryable,
            "details": self.technical_details,
            "recovery_hint": self.recovery_hint,
            "timestamp": self.timestamp.isoformat(),
        }


# ============================================================================
# VALIDATION ERRORS
# ============================================================================


class ValidationError(LegendAIError):
    """Input validation error - user provided invalid data."""

    category = ErrorCategory.VALIDATION
    severity = ErrorSeverity.LOW
    retryable = False
    default_user_message = "Invalid input provided"
    recovery_hint = "Check your input and try again"


class InvalidTickerError(ValidationError):
    """Invalid stock ticker symbol."""

    default_user_message = "Invalid ticker symbol"
    recovery_hint = "Provide a valid stock ticker (e.g., AAPL, TSLA)"


class InvalidIntervalError(ValidationError):
    """Invalid time interval."""

    default_user_message = "Invalid time interval"
    recovery_hint = "Use valid intervals: 1min, 5min, 15min, 30min, 1h, 4h, 1day, 1week, 1month"


class InvalidParameterError(ValidationError):
    """Invalid parameter value."""

    default_user_message = "Invalid parameter value"


# ============================================================================
# EXTERNAL SERVICE ERRORS
# ============================================================================


class ExternalServiceError(LegendAIError):
    """External service/API error."""

    category = ErrorCategory.EXTERNAL
    severity = ErrorSeverity.HIGH
    retryable = True
    default_user_message = "External service unavailable"
    recovery_hint = "Please try again in a few moments"


class MarketDataError(ExternalServiceError):
    """Market data API error."""

    default_user_message = "Unable to fetch market data"
    recovery_hint = "Market data service may be temporarily unavailable. Try again in a moment."


class RateLimitError(ExternalServiceError):
    """API rate limit exceeded."""

    severity = ErrorSeverity.MEDIUM
    retryable = True
    default_user_message = "Rate limit exceeded"
    recovery_hint = "Too many requests. Please wait a moment and try again."


class APIQuotaExceededError(ExternalServiceError):
    """API quota exceeded."""

    severity = ErrorSeverity.HIGH
    retryable = False
    default_user_message = "API quota exceeded"
    recovery_hint = "Daily API quota reached. Please try again tomorrow or upgrade your plan."


class NetworkError(ExternalServiceError):
    """Network connectivity error."""

    severity = ErrorSeverity.MEDIUM
    retryable = True
    default_user_message = "Network error"
    recovery_hint = "Check your internet connection and try again"


class TimeoutError(ExternalServiceError):
    """Operation timeout."""

    severity = ErrorSeverity.MEDIUM
    retryable = True
    default_user_message = "Request timed out"
    recovery_hint = "The operation took too long. Please try again."


# ============================================================================
# DATA PROCESSING ERRORS
# ============================================================================


class DataError(LegendAIError):
    """Data processing error."""

    category = ErrorCategory.DATA
    severity = ErrorSeverity.MEDIUM
    retryable = False
    default_user_message = "Data processing error"


class InsufficientDataError(DataError):
    """Insufficient data for analysis."""

    severity = ErrorSeverity.LOW
    default_user_message = "Not enough data for analysis"
    recovery_hint = "The stock may be newly listed or data is unavailable for the selected period"


class DataTransformError(DataError):
    """Data transformation error."""

    default_user_message = "Unable to process data"
    recovery_hint = "Data format may be invalid or corrupted"


class MalformedDataError(DataError):
    """Malformed or corrupted data."""

    default_user_message = "Data format error"
    recovery_hint = "Received malformed data from source"


# ============================================================================
# PATTERN DETECTION ERRORS
# ============================================================================


class PatternDetectionError(LegendAIError):
    """Pattern detection error."""

    category = ErrorCategory.DATA
    severity = ErrorSeverity.MEDIUM
    retryable = False
    default_user_message = "Pattern analysis failed"


class DetectorNotFoundError(PatternDetectionError):
    """Pattern detector not found in registry."""

    severity = ErrorSeverity.LOW
    default_user_message = "Pattern detector not available"


class DetectorExecutionError(PatternDetectionError):
    """Error during pattern detector execution."""

    severity = ErrorSeverity.MEDIUM
    default_user_message = "Pattern detection failed"
    recovery_hint = "Try analyzing a different stock or time period"


# ============================================================================
# CONFIGURATION ERRORS
# ============================================================================


class ConfigurationError(LegendAIError):
    """Configuration or setup error."""

    category = ErrorCategory.CONFIGURATION
    severity = ErrorSeverity.CRITICAL
    retryable = False
    default_user_message = "System configuration error"
    recovery_hint = "Contact support if this persists"


class MissingAPIKeyError(ConfigurationError):
    """Required API key missing."""

    default_user_message = "Service configuration incomplete"
    recovery_hint = "API credentials not configured. Contact administrator."


class InvalidConfigurationError(ConfigurationError):
    """Invalid configuration value."""

    default_user_message = "Invalid system configuration"


# ============================================================================
# CACHE ERRORS
# ============================================================================


class CacheError(LegendAIError):
    """Cache operation error."""

    category = ErrorCategory.TRANSIENT
    severity = ErrorSeverity.LOW
    retryable = True
    default_user_message = "Cache error"
    recovery_hint = "Operation will proceed without cache"


# ============================================================================
# ERROR AGGREGATION (Sentry-style)
# ============================================================================


@dataclass
class ErrorOccurrence:
    """Single error occurrence."""

    timestamp: datetime
    exception_type: str
    message: str
    context: ErrorContext
    fingerprint: str


@dataclass
class ErrorGroup:
    """Aggregated group of similar errors."""

    fingerprint: str
    exception_type: str
    first_seen: datetime
    last_seen: datetime
    occurrences: int = 0
    samples: List[ErrorOccurrence] = field(default_factory=list)

    def update(self, occurrence: ErrorOccurrence):
        """Update group with new occurrence."""
        self.last_seen = occurrence.timestamp
        self.occurrences += 1
        if len(self.samples) < 10:  # Keep up to 10 samples
            self.samples.append(occurrence)


class ErrorAggregator:
    """
    Sentry-style error aggregation.

    Groups similar errors together for better debugging and monitoring.
    """

    def __init__(self, max_groups: int = 1000):
        self.max_groups = max_groups
        self._groups: Dict[str, ErrorGroup] = {}
        self._lock = Lock()

    def capture_exception(
        self,
        exc: Exception,
        *,
        context: Optional[ErrorContext] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Capture and aggregate an exception.

        Returns:
            Fingerprint of the error group
        """
        # Generate fingerprint for grouping
        fingerprint = self._generate_fingerprint(exc)

        # Create occurrence
        occurrence = ErrorOccurrence(
            timestamp=datetime.utcnow(),
            exception_type=type(exc).__name__,
            message=str(exc),
            context=context or ErrorContext(),
            fingerprint=fingerprint,
        )

        # Update or create group
        with self._lock:
            if fingerprint not in self._groups:
                if len(self._groups) >= self.max_groups:
                    # Remove oldest group
                    oldest = min(self._groups.values(), key=lambda g: g.last_seen)
                    del self._groups[oldest.fingerprint]

                self._groups[fingerprint] = ErrorGroup(
                    fingerprint=fingerprint,
                    exception_type=type(exc).__name__,
                    first_seen=occurrence.timestamp,
                    last_seen=occurrence.timestamp,
                )

            self._groups[fingerprint].update(occurrence)

        # Log the error
        logger.error(
            "error_captured exception_type=%s fingerprint=%s occurrences=%d",
            type(exc).__name__,
            fingerprint[:8],
            self._groups[fingerprint].occurrences,
            extra={"error_context": context.to_dict() if context else {}, **(extra or {})},
            exc_info=exc,
        )

        return fingerprint

    def _generate_fingerprint(self, exc: Exception) -> str:
        """Generate fingerprint for error grouping."""
        # Use exception type and first 2 stack frames
        tb = traceback.extract_tb(exc.__traceback__) if exc.__traceback__ else []

        parts = [type(exc).__name__]
        for frame in tb[:2]:
            parts.append(f"{frame.filename}:{frame.name}:{frame.lineno}")

        fingerprint = "|".join(parts)
        return fingerprint

    def get_groups(self) -> List[ErrorGroup]:
        """Get all error groups sorted by last seen."""
        with self._lock:
            return sorted(
                self._groups.values(),
                key=lambda g: g.last_seen,
                reverse=True,
            )

    def get_stats(self) -> Dict[str, Any]:
        """Get error statistics."""
        with self._lock:
            total_errors = sum(g.occurrences for g in self._groups.values())
            return {
                "total_groups": len(self._groups),
                "total_errors": total_errors,
                "top_errors": [
                    {
                        "type": g.exception_type,
                        "occurrences": g.occurrences,
                        "fingerprint": g.fingerprint[:8],
                        "last_seen": g.last_seen.isoformat(),
                    }
                    for g in sorted(
                        self._groups.values(),
                        key=lambda g: g.occurrences,
                        reverse=True,
                    )[:10]
                ],
            }

    def clear(self):
        """Clear all error groups."""
        with self._lock:
            self._groups.clear()


# Global error aggregator instance
error_aggregator = ErrorAggregator()


# ============================================================================
# ERROR HANDLING UTILITIES
# ============================================================================


@contextmanager
def error_context(
    operation: str,
    *,
    error_class: Type[LegendAIError] = LegendAIError,
    log_errors: bool = True,
    capture: bool = True,
    reraise: bool = True,
    **context_kwargs,
):
    """
    Context manager for structured error handling.

    Usage:
        with error_context("fetch_market_data", ticker="AAPL"):
            # Your code here
            data = fetch_data()

    Args:
        operation: Name of the operation for logging
        error_class: Exception class to wrap errors in
        log_errors: Whether to log errors
        capture: Whether to capture in error aggregator
        reraise: Whether to reraise the error
        **context_kwargs: Additional context for error logging
    """
    start_time = time.perf_counter()

    try:
        yield
    except error_class:
        # Already a LegendAI error, just reraise
        raise
    except Exception as exc:
        duration_ms = (time.perf_counter() - start_time) * 1000

        # Create error context
        ctx = ErrorContext(
            technical_details={
                "operation": operation,
                "duration_ms": duration_ms,
                **context_kwargs,
            }
        )

        # Capture in aggregator
        if capture:
            error_aggregator.capture_exception(exc, context=ctx)

        # Log error
        if log_errors:
            logger.exception(
                "operation_failed operation=%s duration_ms=%.1f",
                operation,
                duration_ms,
                extra={"context": context_kwargs},
            )

        # Wrap and reraise
        if reraise:
            wrapped = error_class(
                f"{operation} failed: {str(exc)}",
                technical_details=ctx.technical_details,
                cause=exc,
            )
            raise wrapped from exc


def handle_errors(
    *,
    error_class: Type[LegendAIError] = LegendAIError,
    log_errors: bool = True,
    capture: bool = True,
    reraise: bool = True,
):
    """
    Decorator for error handling.

    Usage:
        @handle_errors(error_class=MarketDataError)
        async def fetch_prices(ticker: str):
            # Your code here
            return data
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            operation = f"{func.__module__}.{func.__name__}"
            with error_context(
                operation,
                error_class=error_class,
                log_errors=log_errors,
                capture=capture,
                reraise=reraise,
                function=func.__name__,
            ):
                return await func(*args, **kwargs)

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            operation = f"{func.__module__}.{func.__name__}"
            with error_context(
                operation,
                error_class=error_class,
                log_errors=log_errors,
                capture=capture,
                reraise=reraise,
                function=func.__name__,
            ):
                return func(*args, **kwargs)

        # Return appropriate wrapper based on whether function is async
        import inspect
        if inspect.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        else:
            return sync_wrapper  # type: ignore

    return decorator


def log_error_context(
    logger_instance: logging.Logger,
    error: Exception,
    operation: str,
    **context,
):
    """
    Log error with full context.

    Usage:
        try:
            result = risky_operation()
        except Exception as e:
            log_error_context(logger, e, "risky_operation", ticker="AAPL")
            raise
    """
    if isinstance(error, LegendAIError):
        ctx = error.get_context()
        logger_instance.error(
            "error_occurred operation=%s error_type=%s category=%s severity=%s retryable=%s",
            operation,
            type(error).__name__,
            ctx.category.value,
            ctx.severity.value,
            ctx.retryable,
            extra={
                "error_context": ctx.to_dict(),
                "operation_context": context,
            },
            exc_info=error,
        )
    else:
        logger_instance.exception(
            "unexpected_error operation=%s error_type=%s",
            operation,
            type(error).__name__,
            extra={"operation_context": context},
        )
