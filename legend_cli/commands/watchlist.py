"""Watchlist command for Legend CLI."""

import typer
from typing import Optional
from rich.console import Console

from ..client import LegendAPIClient
from ..config_manager import get_config
from ..formatters import OutputFormatter
from ..utils import async_cmd, validate_ticker

app = typer.Typer(help="Manage your watchlist")
console = Console()
formatter = OutputFormatter(console)


@app.command()
@async_cmd
async def add(
    ticker: str = typer.Argument(..., help="Ticker symbol to add"),
    notes: Optional[str] = typer.Option(None, "--notes", "-n", help="Notes about the ticker"),
    alert_price: Optional[float] = typer.Option(None, "--alert-price", "-a", help="Alert price")
):
    """Add a ticker to your watchlist."""
    try:
        ticker = validate_ticker(ticker)
        config = get_config()

        async with LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        ) as client:
            result = await client.watchlist_add(
                ticker=ticker,
                notes=notes,
                alert_price=alert_price
            )

            formatter.print_success(f"Added {ticker} to watchlist")

            if config.verbose:
                console.print(formatter.format_json(result))

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)


@app.command()
@async_cmd
async def remove(
    ticker: str = typer.Argument(..., help="Ticker symbol to remove"),
):
    """Remove a ticker from your watchlist."""
    try:
        ticker = validate_ticker(ticker)
        config = get_config()

        # Confirm removal
        if not typer.confirm(f"Remove {ticker} from watchlist?"):
            formatter.print_info("Cancelled")
            return

        async with LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        ) as client:
            await client.watchlist_remove(ticker)
            formatter.print_success(f"Removed {ticker} from watchlist")

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)


@app.command("list")
@async_cmd
async def list_watchlist(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format")
):
    """List watchlist items."""
    try:
        config = get_config()
        output_format = output or config.output_format

        async with LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        ) as client:
            result = await client.watchlist_list(status=status)
            items = result.get('items', [])

            if not items:
                formatter.print_info("Watchlist is empty")
                return

            if output_format == "table":
                formatter.print_watchlist(items)
            elif output_format == "json":
                console.print(formatter.format_json(items))
            elif output_format == "csv":
                console.print(formatter.format_csv(items))
            else:
                console.print(formatter.format(items, output_format))

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)


@app.command()
@async_cmd
async def update(
    ticker: str = typer.Argument(..., help="Ticker symbol"),
    status: str = typer.Argument(..., help="New status (active, watching, triggered, closed)")
):
    """Update watchlist item status."""
    try:
        ticker = validate_ticker(ticker)
        config = get_config()

        valid_statuses = ['active', 'watching', 'triggered', 'closed']
        if status not in valid_statuses:
            formatter.print_error(
                f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
            raise typer.Exit(1)

        async with LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        ) as client:
            await client.watchlist_update_status(ticker, status)
            formatter.print_success(f"Updated {ticker} status to '{status}'")

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)


@app.command()
@async_cmd
async def clear(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Clear only items with this status"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation")
):
    """Clear watchlist items."""
    try:
        config = get_config()

        if not force:
            msg = "Clear entire watchlist?"
            if status:
                msg = f"Clear all '{status}' items from watchlist?"

            if not typer.confirm(msg):
                formatter.print_info("Cancelled")
                return

        async with LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        ) as client:
            # Get items to clear
            result = await client.watchlist_list(status=status)
            items = result.get('items', [])

            if not items:
                formatter.print_info("No items to clear")
                return

            # Remove each item
            for item in items:
                ticker = item.get('ticker')
                if ticker:
                    await client.watchlist_remove(ticker)

            formatter.print_success(f"Cleared {len(items)} items from watchlist")

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)
