"""Analyze command for Legend CLI."""

import typer
from typing import Optional
from rich.console import Console

from ..client import LegendAPIClient
from ..config_manager import get_config
from ..formatters import OutputFormatter
from ..utils import async_cmd, validate_ticker, validate_interval

app = typer.Typer(help="Analyze stocks and patterns")
console = Console()
formatter = OutputFormatter(console)


@app.command()
@async_cmd
async def ticker(
    symbol: str = typer.Argument(..., help="Ticker symbol (e.g., AAPL)"),
    interval: str = typer.Option("1day", "--interval", "-i", help="Time interval"),
    bars: int = typer.Option(400, "--bars", "-b", help="Number of bars to analyze"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format (table/json/yaml/csv)"),
    pattern: bool = typer.Option(False, "--pattern", "-p", help="Include pattern detection")
):
    """Analyze a ticker symbol."""
    try:
        # Validate inputs
        symbol = validate_ticker(symbol)
        interval = validate_interval(interval)

        config = get_config()
        output_format = output or config.output_format

        # Create API client
        async with LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        ) as client:
            # Get analysis
            console.print(f"[cyan]Analyzing {symbol}...[/cyan]")

            if pattern:
                # Get pattern analysis
                result = await client.analyze_pattern(symbol, interval)
            else:
                # Get standard analysis
                result = await client.analyze(symbol, interval, bars)

            # Format and print output
            if output_format == "table":
                formatter.print_analysis(result)
            else:
                output_str = formatter.format(result, output_format)
                console.print(output_str)

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)


@app.command()
@async_cmd
async def pattern(
    symbol: str = typer.Argument(..., help="Ticker symbol"),
    interval: str = typer.Option("1day", "--interval", "-i", help="Time interval"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format")
):
    """Detect patterns for a ticker."""
    try:
        symbol = validate_ticker(symbol)
        interval = validate_interval(interval)

        config = get_config()
        output_format = output or config.output_format

        async with LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        ) as client:
            console.print(f"[cyan]Detecting patterns for {symbol}...[/cyan]")
            result = await client.analyze_pattern(symbol, interval)

            if output_format == "table":
                formatter.print_analysis(result)
            else:
                output_str = formatter.format(result, output_format)
                console.print(output_str)

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)


@app.command()
@async_cmd
async def market(
    universe: str = typer.Option("SP500", "--universe", "-u", help="Universe to analyze"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format")
):
    """Analyze market internals and breadth."""
    try:
        config = get_config()
        output_format = output or config.output_format

        async with LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        ) as client:
            console.print(f"[cyan]Analyzing {universe} market internals...[/cyan]")
            result = await client.market_internals(universe)

            if output_format == "table":
                formatter.print_dict_table(result, f"{universe} Market Internals")
            else:
                output_str = formatter.format(result, output_format)
                console.print(output_str)

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)


@app.command()
@async_cmd
async def batch(
    tickers: str = typer.Argument(..., help="Comma-separated ticker symbols"),
    interval: str = typer.Option("1day", "--interval", "-i", help="Time interval"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format"),
    concurrent: int = typer.Option(5, "--concurrent", "-c", help="Number of concurrent requests")
):
    """Analyze multiple tickers in batch."""
    try:
        from ..utils import parse_ticker_list
        import asyncio

        ticker_list = parse_ticker_list(tickers)
        if not ticker_list:
            formatter.print_error("No valid tickers provided")
            raise typer.Exit(1)

        config = get_config()
        output_format = output or config.output_format

        console.print(f"[cyan]Analyzing {len(ticker_list)} tickers...[/cyan]")

        async with LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        ) as client:
            # Create semaphore to limit concurrent requests
            semaphore = asyncio.Semaphore(concurrent)

            async def analyze_one(ticker: str):
                async with semaphore:
                    try:
                        return await client.analyze(ticker, interval)
                    except Exception as e:
                        return {'ticker': ticker, 'error': str(e)}

            # Analyze all tickers
            results = await asyncio.gather(*[analyze_one(t) for t in ticker_list])

            # Format output
            if output_format == "json":
                console.print(formatter.format_json(results))
            elif output_format == "csv":
                console.print(formatter.format_csv(results))
            else:
                # Print summary table
                for i, result in enumerate(results, 1):
                    ticker = result.get('ticker', ticker_list[i-1])
                    if 'error' in result:
                        console.print(f"[red]{ticker}: Error - {result['error']}[/red]")
                    else:
                        console.print(f"\n[bold cyan]{'='*60}[/bold cyan]")
                        formatter.print_analysis(result)

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)
