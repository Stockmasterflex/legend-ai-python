"""Scan command for Legend CLI."""

import typer
from typing import Optional, List
from rich.console import Console

from ..client import LegendAPIClient
from ..config_manager import get_config
from ..formatters import OutputFormatter
from ..utils import async_cmd

app = typer.Typer(help="Scan stocks for patterns")
console = Console()
formatter = OutputFormatter(console)


@app.command()
@async_cmd
async def universe(
    name: str = typer.Option("SP500", "--universe", "-u", help="Universe name (SP500, NASDAQ100)"),
    sector: Optional[str] = typer.Option(None, "--sector", "-s", help="Filter by sector"),
    min_price: Optional[float] = typer.Option(None, "--min-price", help="Minimum price"),
    max_price: Optional[float] = typer.Option(None, "--max-price", help="Maximum price"),
    min_volume: Optional[int] = typer.Option(None, "--min-volume", help="Minimum volume"),
    patterns: Optional[str] = typer.Option(None, "--patterns", "-p", help="Comma-separated pattern types"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format"),
    limit: int = typer.Option(20, "--limit", "-l", help="Max results to show")
):
    """Scan a universe for trading patterns."""
    try:
        config = get_config()
        output_format = output or config.output_format

        # Parse pattern types
        pattern_types = None
        if patterns:
            pattern_types = [p.strip() for p in patterns.split(',')]

        async with LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        ) as client:
            console.print(f"[cyan]Scanning {name} universe...[/cyan]")

            result = await client.scan(
                universe=name,
                sector=sector,
                min_price=min_price,
                max_price=max_price,
                min_volume=min_volume,
                pattern_types=pattern_types
            )

            # Limit results if needed
            if 'matches' in result and len(result['matches']) > limit:
                result['matches'] = result['matches'][:limit]

            # Format output
            if output_format == "table":
                formatter.print_scan_results(result)
            elif output_format == "json":
                console.print(formatter.format_json(result))
            elif output_format == "csv":
                matches = result.get('matches', [])
                console.print(formatter.format_csv(matches))
            else:
                console.print(formatter.format(result, output_format))

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)


@app.command()
@async_cmd
async def quick(
    universe: str = typer.Option("SP500", "--universe", "-u", help="Universe name"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format")
):
    """Quick scan of a universe."""
    try:
        config = get_config()
        output_format = output or config.output_format

        async with LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        ) as client:
            console.print(f"[cyan]Quick scanning {universe}...[/cyan]")
            result = await client.quick_scan(universe)

            if output_format == "table":
                formatter.print_scan_results(result)
            else:
                console.print(formatter.format(result, output_format))

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)


@app.command()
@async_cmd
async def sector(
    sector_name: str = typer.Argument(..., help="Sector name (e.g., Technology)"),
    universe: str = typer.Option("SP500", "--universe", "-u", help="Universe name"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format")
):
    """Scan a specific sector."""
    try:
        config = get_config()
        output_format = output or config.output_format

        async with LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        ) as client:
            console.print(f"[cyan]Scanning {sector_name} sector in {universe}...[/cyan]")

            result = await client.scan(universe=universe, sector=sector_name)

            if output_format == "table":
                formatter.print_scan_results(result)
            else:
                console.print(formatter.format(result, output_format))

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)
