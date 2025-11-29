"""
Error recovery utilities including retry logic and circuit breaker pattern.

This module provides:
- Retry with exponential backoff
- Circuit breaker pattern for external services
- Fallback strategies
- Timeout wrappers
"""

import asyncio
import functools
import logging
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional, TypeVar

from app.core.errors import ExternalServiceError, RateLimitError
from app.core.errors import TimeoutError as LegendTimeoutError

logger = logging.getLogger(__name__)

T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])


class CircuitState(str, Enum):
    """Circuit breaker states."""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, rejecting requests
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class RetryConfig:
    """Configuration for retry logic."""

    max_attempts: int = 3
    initial_delay: float = 1.0  # seconds
    max_delay: float = 60.0  # seconds
    exponential_base: float = 2.0
    jitter: bool = True
    retryable_errors: tuple = (
        ExternalServiceError,
        RateLimitError,
        ConnectionError,
        asyncio.TimeoutError,
    )


@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker."""

    failure_threshold: int = 5  # Failures before opening
    success_threshold: int = 2  # Successes to close from half-open
    timeout: float = 60.0  # Seconds to wait before half-open
    half_open_max_calls: int = 3  # Max calls in half-open state


class CircuitBreaker:
    """
    Circuit breaker pattern implementation for external services.

    Prevents cascading failures by temporarily stopping calls to failing services.
    """

    def __init__(self, name: str, config: Optional[CircuitBreakerConfig] = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.half_open_calls = 0

    def can_execute(self) -> bool:
        """Check if operation can be executed."""
        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:
            # Check if timeout has elapsed
            if self.last_failure_time:
                elapsed = (datetime.utcnow() - self.last_failure_time).total_seconds()
                if elapsed >= self.config.timeout:
                    logger.info(
                        "circuit_breaker_half_open name=%s timeout_elapsed=%.1fs",
                        self.name,
                        elapsed,
                    )
                    self.state = CircuitState.HALF_OPEN
                    self.half_open_calls = 0
                    return True
            return False

        if self.state == CircuitState.HALF_OPEN:
            # Allow limited calls in half-open state
            return self.half_open_calls < self.config.half_open_max_calls

        return False

    def record_success(self):
        """Record successful operation."""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            logger.info(
                "circuit_breaker_success name=%s state=%s successes=%d/%d",
                self.name,
                self.state.value,
                self.success_count,
                self.config.success_threshold,
            )

            if self.success_count >= self.config.success_threshold:
                self._close()
        elif self.state == CircuitState.CLOSED:
            # Reset failure count on success
            self.failure_count = 0

    def record_failure(self):
        """Record failed operation."""
        self.last_failure_time = datetime.utcnow()

        if self.state == CircuitState.HALF_OPEN:
            # Go back to open on any failure in half-open
            self._open()
        elif self.state == CircuitState.CLOSED:
            self.failure_count += 1
            logger.warning(
                "circuit_breaker_failure name=%s failures=%d/%d",
                self.name,
                self.failure_count,
                self.config.failure_threshold,
            )

            if self.failure_count >= self.config.failure_threshold:
                self._open()

    def _open(self):
        """Open the circuit (stop allowing calls)."""
        self.state = CircuitState.OPEN
        self.failure_count = 0
        self.success_count = 0
        logger.error(
            "circuit_breaker_opened name=%s timeout=%.1fs",
            self.name,
            self.config.timeout,
        )

    def _close(self):
        """Close the circuit (resume normal operation)."""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        logger.info("circuit_breaker_closed name=%s", self.name)

    def get_state(self) -> dict:
        """Get current circuit breaker state."""
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure": (
                self.last_failure_time.isoformat() if self.last_failure_time else None
            ),
        }


# Global circuit breaker registry
_circuit_breakers: dict[str, CircuitBreaker] = {}


def get_circuit_breaker(
    name: str, config: Optional[CircuitBreakerConfig] = None
) -> CircuitBreaker:
    """Get or create a circuit breaker."""
    if name not in _circuit_breakers:
        _circuit_breakers[name] = CircuitBreaker(name, config)
    return _circuit_breakers[name]


def with_circuit_breaker(
    name: str,
    config: Optional[CircuitBreakerConfig] = None,
    fallback: Optional[Callable] = None,
):
    """
    Decorator to add circuit breaker protection.

    Usage:
        @with_circuit_breaker("twelvedata_api")
        async def fetch_prices(ticker: str):
            return await api_call(ticker)
    """

    def decorator(func: F) -> F:
        circuit = get_circuit_breaker(name, config)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            if not circuit.can_execute():
                logger.warning(
                    "circuit_breaker_rejected operation=%s state=%s",
                    func.__name__,
                    circuit.state.value,
                )
                if fallback:
                    return (
                        await fallback(*args, **kwargs)
                        if asyncio.iscoroutinefunction(fallback)
                        else fallback(*args, **kwargs)
                    )
                raise ExternalServiceError(
                    f"Service '{name}' is temporarily unavailable",
                    user_message="Service temporarily unavailable, please try again later",
                    recovery_hint=f"The service is experiencing issues. It will be retried automatically in {circuit.config.timeout}s",
                )

            if circuit.state == CircuitState.HALF_OPEN:
                circuit.half_open_calls += 1

            try:
                result = await func(*args, **kwargs)
                circuit.record_success()
                return result
            except Exception:
                circuit.record_failure()
                raise

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            if not circuit.can_execute():
                logger.warning(
                    "circuit_breaker_rejected operation=%s state=%s",
                    func.__name__,
                    circuit.state.value,
                )
                if fallback:
                    return fallback(*args, **kwargs)
                raise ExternalServiceError(
                    f"Service '{name}' is temporarily unavailable",
                    user_message="Service temporarily unavailable, please try again later",
                )

            if circuit.state == CircuitState.HALF_OPEN:
                circuit.half_open_calls += 1

            try:
                result = func(*args, **kwargs)
                circuit.record_success()
                return result
            except Exception:
                circuit.record_failure()
                raise

        import inspect

        if inspect.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        else:
            return sync_wrapper  # type: ignore

    return decorator


def with_retry(
    config: Optional[RetryConfig] = None,
    operation_name: Optional[str] = None,
):
    """
    Decorator to add retry logic with exponential backoff.

    Usage:
        @with_retry(config=RetryConfig(max_attempts=5))
        async def fetch_data():
            return await api_call()
    """
    retry_config = config or RetryConfig()

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            op_name = operation_name or f"{func.__module__}.{func.__name__}"
            last_exception = None

            for attempt in range(1, retry_config.max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except retry_config.retryable_errors as e:
                    last_exception = e
                    if attempt == retry_config.max_attempts:
                        logger.error(
                            "retry_exhausted operation=%s attempts=%d error=%s",
                            op_name,
                            attempt,
                            type(e).__name__,
                        )
                        raise

                    # Calculate delay with exponential backoff
                    delay = min(
                        retry_config.initial_delay
                        * (retry_config.exponential_base ** (attempt - 1)),
                        retry_config.max_delay,
                    )

                    # Add jitter to prevent thundering herd
                    if retry_config.jitter:
                        import random

                        delay = delay * (0.5 + random.random() * 0.5)

                    logger.warning(
                        "retry_attempt operation=%s attempt=%d/%d delay=%.2fs error=%s",
                        op_name,
                        attempt,
                        retry_config.max_attempts,
                        delay,
                        str(e)[:100],
                    )

                    await asyncio.sleep(delay)

            # Should not reach here, but just in case
            if last_exception:
                raise last_exception

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            op_name = operation_name or f"{func.__module__}.{func.__name__}"
            last_exception = None

            for attempt in range(1, retry_config.max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except retry_config.retryable_errors as e:
                    last_exception = e
                    if attempt == retry_config.max_attempts:
                        logger.error(
                            "retry_exhausted operation=%s attempts=%d error=%s",
                            op_name,
                            attempt,
                            type(e).__name__,
                        )
                        raise

                    # Calculate delay
                    delay = min(
                        retry_config.initial_delay
                        * (retry_config.exponential_base ** (attempt - 1)),
                        retry_config.max_delay,
                    )

                    if retry_config.jitter:
                        import random

                        delay = delay * (0.5 + random.random() * 0.5)

                    logger.warning(
                        "retry_attempt operation=%s attempt=%d/%d delay=%.2fs error=%s",
                        op_name,
                        attempt,
                        retry_config.max_attempts,
                        delay,
                        str(e)[:100],
                    )

                    time.sleep(delay)

            if last_exception:
                raise last_exception

        import inspect

        if inspect.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        else:
            return sync_wrapper  # type: ignore

    return decorator


async def with_timeout(
    coro: Callable[..., T],
    timeout_seconds: float,
    *args,
    operation_name: Optional[str] = None,
    **kwargs,
) -> T:
    """
    Execute coroutine with timeout.

    Usage:
        result = await with_timeout(
            fetch_data,
            timeout_seconds=10.0,
            ticker="AAPL"
        )
    """
    op_name = operation_name or "operation"

    try:
        async with asyncio.timeout(timeout_seconds):
            return await coro(*args, **kwargs)
    except asyncio.TimeoutError as e:
        logger.warning(
            "operation_timeout operation=%s timeout=%.1fs",
            op_name,
            timeout_seconds,
        )
        raise LegendTimeoutError(
            f"{op_name} timed out after {timeout_seconds}s",
            user_message="Operation timed out",
            recovery_hint=f"The operation took longer than {timeout_seconds}s. Try again or contact support.",
        ) from e


def with_fallback(*fallback_funcs: Callable):
    """
    Decorator to add fallback functions.

    Usage:
        @with_fallback(fallback_source_1, fallback_source_2)
        async def fetch_data():
            return await primary_source()
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Try primary function
            try:
                return await func(*args, **kwargs)
            except Exception as primary_error:
                logger.warning(
                    "primary_failed function=%s error=%s attempting_fallbacks=%d",
                    func.__name__,
                    type(primary_error).__name__,
                    len(fallback_funcs),
                )

                # Try fallbacks in order
                for i, fallback in enumerate(fallback_funcs, 1):
                    try:
                        logger.info(
                            "trying_fallback function=%s fallback=%d/%d",
                            func.__name__,
                            i,
                            len(fallback_funcs),
                        )
                        result = (
                            await fallback(*args, **kwargs)
                            if asyncio.iscoroutinefunction(fallback)
                            else fallback(*args, **kwargs)
                        )
                        logger.info(
                            "fallback_success function=%s fallback=%d",
                            func.__name__,
                            i,
                        )
                        return result
                    except Exception as fallback_error:
                        logger.warning(
                            "fallback_failed function=%s fallback=%d error=%s",
                            func.__name__,
                            i,
                            type(fallback_error).__name__,
                        )
                        continue

                # All fallbacks failed
                logger.error(
                    "all_fallbacks_failed function=%s",
                    func.__name__,
                )
                raise primary_error

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as primary_error:
                logger.warning(
                    "primary_failed function=%s error=%s",
                    func.__name__,
                    type(primary_error).__name__,
                )

                for i, fallback in enumerate(fallback_funcs, 1):
                    try:
                        result = fallback(*args, **kwargs)
                        logger.info(
                            "fallback_success function=%s fallback=%d", func.__name__, i
                        )
                        return result
                    except Exception:
                        continue

                raise primary_error

        import inspect

        if inspect.iscoroutinefunction(func):
            return async_wrapper  # type: ignore
        else:
            return sync_wrapper  # type: ignore

    return decorator


@dataclass
class HealthMetrics:
    """Health metrics for a service."""

    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_duration_ms: float = 0.0
    recent_errors: deque = field(default_factory=lambda: deque(maxlen=10))

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_requests == 0:
            return 1.0
        return self.successful_requests / self.total_requests

    @property
    def avg_duration_ms(self) -> float:
        """Calculate average duration."""
        if self.total_requests == 0:
            return 0.0
        return self.total_duration_ms / self.total_requests

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": round(self.success_rate, 3),
            "avg_duration_ms": round(self.avg_duration_ms, 2),
            "recent_errors": [
                {"timestamp": e["timestamp"].isoformat(), "error": e["error"]}
                for e in self.recent_errors
            ],
        }


class HealthMonitor:
    """Monitor health of operations and services."""

    def __init__(self):
        self._metrics: dict[str, HealthMetrics] = {}

    def record_request(
        self,
        service: str,
        success: bool,
        duration_ms: float,
        error: Optional[Exception] = None,
    ):
        """Record request metrics."""
        if service not in self._metrics:
            self._metrics[service] = HealthMetrics()

        metrics = self._metrics[service]
        metrics.total_requests += 1
        metrics.total_duration_ms += duration_ms

        if success:
            metrics.successful_requests += 1
        else:
            metrics.failed_requests += 1
            if error:
                metrics.recent_errors.append(
                    {"timestamp": datetime.utcnow(), "error": str(error)}
                )

    def get_health(self, service: str) -> dict:
        """Get health metrics for a service."""
        if service not in self._metrics:
            return {"status": "unknown", "metrics": {}}

        metrics = self._metrics[service]
        status = "healthy"

        if metrics.success_rate < 0.5:
            status = "critical"
        elif metrics.success_rate < 0.8:
            status = "degraded"

        return {"status": status, "metrics": metrics.to_dict()}

    def get_all_health(self) -> dict:
        """Get health for all services."""
        return {service: self.get_health(service) for service in self._metrics}


# Global health monitor
health_monitor = HealthMonitor()
