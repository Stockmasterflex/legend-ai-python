"""Alerts command for Legend CLI."""

import typer
from typing import Optional
from rich.console import Console

from ..client import LegendAPIClient
from ..config_manager import get_config
from ..formatters import OutputFormatter
from ..utils import async_cmd, validate_ticker

app = typer.Typer(help="Manage alerts")
console = Console()
formatter = OutputFormatter(console)


@app.command("list")
@async_cmd
async def list_alerts(
    ticker: Optional[str] = typer.Option(None, "--ticker", "-t", help="Filter by ticker"),
    active_only: bool = typer.Option(True, "--active/--all", help="Show active alerts only"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format")
):
    """List alerts."""
    try:
        config = get_config()
        output_format = output or config.output_format

        async with LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        ) as client:
            result = await client.alerts_list(ticker=ticker, active_only=active_only)
            alerts = result.get('alerts', [])

            if not alerts:
                formatter.print_info("No alerts found")
                return

            if output_format == "table":
                from rich.table import Table
                from rich import box

                table = Table(
                    title=f"Alerts ({len(alerts)} items)",
                    box=box.ROUNDED,
                    show_header=True,
                    header_style="bold cyan"
                )

                table.add_column("ID", style="dim", no_wrap=True)
                table.add_column("Ticker", style="cyan", no_wrap=True)
                table.add_column("Type", style="yellow")
                table.add_column("Condition", style="white")
                table.add_column("Target", style="green")
                table.add_column("Status", style="white")

                for alert in alerts:
                    alert_id = str(alert.get('id', ''))
                    ticker = alert.get('ticker', 'N/A')
                    alert_type = alert.get('alert_type', 'N/A')
                    condition = alert.get('condition', '-')
                    target = alert.get('target_price')
                    status = alert.get('status', 'active')

                    status_color = "green" if status == "active" else "dim"

                    table.add_row(
                        alert_id,
                        ticker,
                        alert_type,
                        condition,
                        f"${target:.2f}" if target else "-",
                        f"[{status_color}]{status}[/{status_color}]"
                    )

                console.print(table)
            else:
                console.print(formatter.format(alerts, output_format))

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)


@app.command()
@async_cmd
async def create(
    ticker: str = typer.Argument(..., help="Ticker symbol"),
    alert_type: str = typer.Option(..., "--type", "-t", help="Alert type (price, pattern, breakout)"),
    target_price: Optional[float] = typer.Option(None, "--price", "-p", help="Target price"),
    condition: Optional[str] = typer.Option(None, "--condition", "-c", help="Condition (above, below, crosses)")
):
    """Create a new alert."""
    try:
        ticker = validate_ticker(ticker)
        config = get_config()

        valid_types = ['price', 'pattern', 'breakout', 'volume']
        if alert_type not in valid_types:
            formatter.print_error(
                f"Invalid alert type. Must be one of: {', '.join(valid_types)}"
            )
            raise typer.Exit(1)

        async with LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        ) as client:
            result = await client.alerts_create(
                ticker=ticker,
                alert_type=alert_type,
                target_price=target_price,
                condition=condition
            )

            alert_id = result.get('id')
            formatter.print_success(f"Created alert #{alert_id} for {ticker}")

            if config.verbose:
                console.print(formatter.format_json(result))

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)


@app.command()
@async_cmd
async def delete(
    alert_id: int = typer.Argument(..., help="Alert ID to delete"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation")
):
    """Delete an alert."""
    try:
        config = get_config()

        if not force and not typer.confirm(f"Delete alert #{alert_id}?"):
            formatter.print_info("Cancelled")
            return

        async with LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        ) as client:
            await client.alerts_delete(alert_id)
            formatter.print_success(f"Deleted alert #{alert_id}")

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)
