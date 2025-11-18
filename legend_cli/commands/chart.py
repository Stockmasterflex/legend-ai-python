"""Chart command for Legend CLI."""

import typer
from typing import Optional
from rich.console import Console
import webbrowser

from ..client import LegendAPIClient
from ..config_manager import get_config
from ..formatters import OutputFormatter
from ..utils import async_cmd, validate_ticker, validate_interval

app = typer.Typer(help="Generate and view charts")
console = Console()
formatter = OutputFormatter(console)


@app.command()
@async_cmd
async def show(
    ticker: str = typer.Argument(..., help="Ticker symbol"),
    interval: str = typer.Option("1day", "--interval", "-i", help="Time interval"),
    bars: int = typer.Option(120, "--bars", "-b", help="Number of bars"),
    open_browser: bool = typer.Option(True, "--open/--no-open", help="Open chart in browser"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format")
):
    """Generate and display a chart for a ticker."""
    try:
        ticker = validate_ticker(ticker)
        interval = validate_interval(interval)

        config = get_config()
        output_format = output or config.output_format

        async with LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        ) as client:
            console.print(f"[cyan]Generating chart for {ticker}...[/cyan]")

            result = await client.generate_chart(ticker, interval, bars)

            chart_url = result.get('chart_url')

            if output_format == "json":
                console.print(formatter.format_json(result))
            else:
                if chart_url:
                    formatter.print_success(f"Chart generated: {chart_url}")

                    if open_browser:
                        console.print("[cyan]Opening chart in browser...[/cyan]")
                        webbrowser.open(chart_url)
                else:
                    formatter.print_error("No chart URL returned")

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)


@app.command()
@async_cmd
async def batch(
    tickers: str = typer.Argument(..., help="Comma-separated ticker symbols"),
    interval: str = typer.Option("1day", "--interval", "-i", help="Time interval"),
    bars: int = typer.Option(120, "--bars", "-b", help="Number of bars"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format")
):
    """Generate charts for multiple tickers."""
    try:
        from ..utils import parse_ticker_list
        import asyncio

        ticker_list = parse_ticker_list(tickers)
        if not ticker_list:
            formatter.print_error("No valid tickers provided")
            raise typer.Exit(1)

        config = get_config()
        output_format = output or config.output_format

        console.print(f"[cyan]Generating charts for {len(ticker_list)} tickers...[/cyan]")

        async with LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        ) as client:
            # Generate charts concurrently
            async def gen_chart(ticker: str):
                try:
                    return await client.generate_chart(ticker, interval, bars)
                except Exception as e:
                    return {'ticker': ticker, 'error': str(e)}

            results = await asyncio.gather(*[gen_chart(t) for t in ticker_list])

            # Format output
            if output_format == "json":
                console.print(formatter.format_json(results))
            else:
                for result in results:
                    ticker = result.get('ticker', 'N/A')
                    if 'error' in result:
                        console.print(f"[red]{ticker}: Error - {result['error']}[/red]")
                    else:
                        chart_url = result.get('chart_url')
                        if chart_url:
                            console.print(f"[green]{ticker}:[/green] {chart_url}")

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)
