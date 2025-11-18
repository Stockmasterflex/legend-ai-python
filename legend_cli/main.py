"""Main CLI entry point for Legend AI."""

import typer
from typing import Optional
from rich.console import Console

from . import __version__
from .commands import analyze, scan, watchlist, chart, alerts, config as config_cmd
from .formatters import OutputFormatter
from .utils import async_cmd
from .client import LegendAPIClient
from .config_manager import get_config

# Create main app
app = typer.Typer(
    name="legend",
    help="Legend AI - Professional trading pattern scanner and analysis CLI",
    add_completion=True,
    rich_markup_mode="rich"
)

# Add command groups
app.add_typer(analyze.app, name="analyze", help="Analyze stocks and patterns")
app.add_typer(scan.app, name="scan", help="Scan for trading patterns")
app.add_typer(watchlist.app, name="watchlist", help="Manage watchlist")
app.add_typer(chart.app, name="chart", help="Generate and view charts")
app.add_typer(alerts.app, name="alerts", help="Manage alerts")
app.add_typer(config_cmd.app, name="config", help="Manage configuration")

console = Console()
formatter = OutputFormatter(console)


def version_callback(value: bool):
    """Show version information."""
    if value:
        console.print(f"[bold cyan]Legend AI CLI[/bold cyan] v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit"
    ),
):
    """
    Legend AI CLI - Professional trading pattern scanner and analysis.

    \b
    Quick Start:
      legend analyze AAPL                  # Analyze a stock
      legend scan --sector tech            # Scan tech sector
      legend watchlist add TSLA            # Add to watchlist
      legend chart NVDA --interval weekly  # Generate chart
      legend tui                           # Launch interactive mode

    \b
    Configuration:
      legend config init                   # Initialize config
      legend config show                   # Show current config

    \b
    Documentation:
      https://github.com/your-org/legend-ai-python
    """
    pass


@app.command()
@async_cmd
async def health(
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format")
):
    """Check API health status."""
    try:
        config = get_config()
        output_format = output or config.output_format

        async with LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        ) as client:
            result = await client.health_check()

            if output_format == "json":
                console.print(formatter.format_json(result))
            else:
                status = result.get('status', 'unknown')
                color = "green" if status == "healthy" else "red"

                console.print(f"[{color}]API Status: {status}[/{color}]")
                console.print(f"API URL: {config.api_url}")

                if config.verbose:
                    console.print(formatter.format_json(result))

    except Exception as e:
        formatter.print_error(f"Health check failed: {str(e)}")
        raise typer.Exit(1)


@app.command()
def tui(
    universe: str = typer.Option("SP500", "--universe", "-u", help="Default universe"),
    refresh: int = typer.Option(5, "--refresh", "-r", help="Refresh interval (seconds)")
):
    """Launch interactive TUI mode."""
    try:
        from .tui.app import LegendTUI

        console.print("[cyan]Launching Legend AI TUI...[/cyan]")

        # Create and run TUI app
        tui_app = LegendTUI(universe=universe, refresh_interval=refresh)
        tui_app.run()

    except ImportError as e:
        formatter.print_error(
            "TUI mode requires additional dependencies. "
            "Install with: pip install legend-ai[tui]"
        )
        raise typer.Exit(1)
    except Exception as e:
        formatter.print_error(f"TUI error: {str(e)}")
        raise typer.Exit(1)


@app.command()
@async_cmd
async def quick(
    ticker: str = typer.Argument(..., help="Ticker symbol"),
):
    """Quick analysis (shorthand for analyze)."""
    try:
        from .utils import validate_ticker

        ticker = validate_ticker(ticker)
        config = get_config()

        async with LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        ) as client:
            console.print(f"[cyan]Quick analysis of {ticker}...[/cyan]")

            result = await client.analyze(ticker)
            formatter.print_analysis(result)

    except Exception as e:
        formatter.print_error(str(e))
        raise typer.Exit(1)


@app.command()
def doctor():
    """Run diagnostics and check configuration."""
    import sys
    from pathlib import Path

    console.print("[bold cyan]Legend AI CLI Doctor[/bold cyan]\n")

    # Check Python version
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    console.print(f"[cyan]Python version:[/cyan] {py_version}")

    if sys.version_info < (3, 11):
        formatter.print_warning("Python 3.11+ recommended")
    else:
        formatter.print_success("Python version OK")

    # Check config
    try:
        config = get_config()
        formatter.print_success("Configuration loaded")
        console.print(f"  API URL: {config.api_url}")

        if config.api_key:
            formatter.print_success("API key configured")
        else:
            formatter.print_warning("No API key set")

    except Exception as e:
        formatter.print_error(f"Configuration error: {e}")

    # Check API connectivity
    console.print("\n[cyan]Checking API connectivity...[/cyan]")
    try:
        import asyncio

        async def check_health():
            config = get_config()
            async with LegendAPIClient(
                base_url=config.api_url,
                api_key=config.api_key,
                timeout=5
            ) as client:
                return await client.health_check()

        result = asyncio.run(check_health())
        formatter.print_success("API is reachable")

    except Exception as e:
        formatter.print_error(f"Cannot reach API: {e}")
        formatter.print_info(
            f"Make sure the API is running at {config.api_url}\n"
            "  Start with: uvicorn app.main:app --reload"
        )

    # Check dependencies
    console.print("\n[cyan]Checking dependencies...[/cyan]")

    deps = [
        ('typer', 'CLI framework'),
        ('rich', 'Terminal formatting'),
        ('httpx', 'HTTP client'),
        ('pydantic', 'Data validation'),
        ('yaml', 'Config files'),
    ]

    for module, desc in deps:
        try:
            __import__(module)
            formatter.print_success(f"{module}: {desc}")
        except ImportError:
            formatter.print_error(f"{module} not installed ({desc})")

    # Check optional dependencies
    console.print("\n[cyan]Optional dependencies:[/cyan]")

    try:
        __import__('textual')
        formatter.print_success("textual: TUI mode available")
    except ImportError:
        formatter.print_info("textual: Install for TUI mode (pip install textual)")

    console.print("\n[bold green]Diagnostics complete![/bold green]")


if __name__ == "__main__":
    app()
