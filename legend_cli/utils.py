"""Utility functions for Legend CLI."""

import asyncio
from functools import wraps
from typing import Any, Callable, TypeVar, cast
import sys


T = TypeVar('T')


def async_cmd(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to run async functions in sync context."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return asyncio.run(func(*args, **kwargs))
    return wrapper


def handle_api_error(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator to handle API errors gracefully."""
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            from rich.console import Console
            console = Console()
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
            sys.exit(1)
    return cast(Callable[..., T], wrapper)


def validate_ticker(ticker: str) -> str:
    """Validate and normalize ticker symbol."""
    if not ticker:
        raise ValueError("Ticker symbol cannot be empty")

    # Convert to uppercase and strip whitespace
    ticker = ticker.strip().upper()

    # Basic validation
    if not ticker.isalnum():
        raise ValueError(f"Invalid ticker symbol: {ticker}")

    if len(ticker) > 5:
        # Allow longer tickers for some exchanges
        pass

    return ticker


def validate_interval(interval: str) -> str:
    """Validate interval parameter."""
    valid_intervals = [
        '1min', '5min', '15min', '30min', '1hour',
        '1day', '1week', '1month'
    ]

    if interval not in valid_intervals:
        raise ValueError(
            f"Invalid interval: {interval}. "
            f"Must be one of: {', '.join(valid_intervals)}"
        )

    return interval


def parse_ticker_list(ticker_input: str) -> list[str]:
    """Parse comma-separated ticker list."""
    tickers = [t.strip().upper() for t in ticker_input.split(',')]
    return [t for t in tickers if t]


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format value as percentage."""
    return f"{value:.{decimals}f}%"


def format_currency(value: float, decimals: int = 2) -> str:
    """Format value as currency."""
    return f"${value:,.{decimals}f}"


def get_color_for_change(change: float) -> str:
    """Get color based on price change."""
    if change > 0:
        return "green"
    elif change < 0:
        return "red"
    else:
        return "white"
