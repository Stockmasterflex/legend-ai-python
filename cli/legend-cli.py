#!/usr/bin/env python3
"""
Legend AI CLI Tool

Command-line interface for the Legend AI Trading Pattern Scanner API

Usage:
    legend-cli detect AAPL
    legend-cli scan --min-score 8.0
    legend-cli chat "What are the best tech stocks?"
    legend-cli watchlist add NVDA --reason "VCP forming"
"""

import sys
import argparse
import json
from typing import Optional
import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

console = Console()


class LegendCLI:
    """Legend AI CLI Client"""

    def __init__(self, base_url: str = "https://legend-ai-python-production.up.railway.app"):
        self.base_url = base_url
        self.client = httpx.Client(base_url=base_url, timeout=30.0)

    def detect_pattern(self, ticker: str, interval: str = "1day") -> None:
        """Detect pattern for a ticker"""
        console.print(f"[bold blue]Detecting pattern for {ticker}...[/bold blue]")

        try:
            response = self.client.post(
                "/api/patterns/detect",
                json={"ticker": ticker, "interval": interval},
            )
            response.raise_for_status()
            data = response.json()

            if data.get("success"):
                result = data["data"]

                # Create result panel
                panel = Panel.fit(
                    f"""[bold green]{result['pattern']}[/bold green]

[yellow]Score:[/yellow] {result['score']}/10
[yellow]Entry:[/yellow] ${result['entry']:.2f}
[yellow]Stop:[/yellow] ${result['stop']:.2f}
[yellow]Target:[/yellow] ${result['target']:.2f}
[yellow]Risk/Reward:[/yellow] {result['risk_reward_ratio']:.2f}R
[yellow]RS Rating:[/yellow] {result.get('rs_rating', 'N/A')}

[dim]Cached: {data.get('cached', False)} | Processing Time: {data.get('processing_time', 0):.2f}s[/dim]
""",
                    title=f"Pattern for {ticker}",
                    border_style="green",
                )
                console.print(panel)

                if result.get("chart_url"):
                    console.print(f"[blue]Chart:[/blue] {result['chart_url']}")
            else:
                console.print(f"[red]Error:[/red] {data.get('error')}")

        except httpx.HTTPStatusError as e:
            console.print(f"[red]HTTP Error {e.response.status_code}:[/red] {e.response.text}")
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")

    def scan_universe(
        self,
        universe: str = "SP500",
        min_score: float = 7.0,
        max_results: int = 20,
    ) -> None:
        """Scan universe for patterns"""
        console.print(f"[bold blue]Scanning {universe} (min score: {min_score})...[/bold blue]")

        try:
            response = self.client.post(
                "/api/universe/scan",
                json={
                    "universe": universe,
                    "min_score": min_score,
                    "max_results": max_results,
                },
            )
            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])
            if not results:
                console.print("[yellow]No patterns found matching criteria[/yellow]")
                return

            # Create table
            table = Table(title=f"Top Setups from {universe}")
            table.add_column("Ticker", style="cyan", no_wrap=True)
            table.add_column("Pattern", style="magenta")
            table.add_column("Score", justify="right", style="green")
            table.add_column("Entry", justify="right")
            table.add_column("Target", justify="right")
            table.add_column("R:R", justify="right", style="yellow")

            for result in results[:max_results]:
                table.add_row(
                    result["ticker"],
                    result["pattern"],
                    f"{result['score']:.1f}",
                    f"${result['entry']:.2f}",
                    f"${result['target']:.2f}",
                    f"{result.get('risk_reward_ratio', 0):.1f}R",
                )

            console.print(table)
            console.print(
                f"\n[dim]Found {data.get('total_found', 0)} patterns from {data.get('total_scanned', 0)} stocks[/dim]"
            )

        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")

    def chat(self, message: str, symbol: Optional[str] = None) -> None:
        """Chat with AI assistant"""
        console.print(f"[bold blue]Asking AI...[/bold blue]")

        try:
            payload = {"message": message}
            if symbol:
                payload["symbol"] = symbol
                payload["include_market_data"] = True

            response = self.client.post("/api/ai/chat", json=payload)
            response.raise_for_status()
            data = response.json()

            panel = Panel.fit(
                data["response"],
                title="AI Assistant",
                border_style="blue",
            )
            console.print(panel)

        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")

    def watchlist_list(self) -> None:
        """List watchlist items"""
        try:
            response = self.client.get("/api/watchlist")
            response.raise_for_status()
            data = response.json()

            items = data.get("items", [])
            if not items:
                console.print("[yellow]Watchlist is empty[/yellow]")
                return

            table = Table(title="Watchlist")
            table.add_column("Ticker", style="cyan")
            table.add_column("Status", style="magenta")
            table.add_column("Entry", justify="right")
            table.add_column("Stop", justify="right")
            table.add_column("Reason")

            for item in items:
                table.add_row(
                    item["ticker"],
                    item["status"],
                    f"${item.get('target_entry', 0):.2f}" if item.get("target_entry") else "-",
                    f"${item.get('target_stop', 0):.2f}" if item.get("target_stop") else "-",
                    item.get("reason", ""),
                )

            console.print(table)

        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")

    def watchlist_add(self, ticker: str, reason: Optional[str] = None) -> None:
        """Add ticker to watchlist"""
        try:
            payload = {"ticker": ticker}
            if reason:
                payload["reason"] = reason

            response = self.client.post("/api/watchlist/add", json=payload)
            response.raise_for_status()

            console.print(f"[green]✓[/green] Added {ticker} to watchlist")

        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")

    def health(self) -> None:
        """Check API health"""
        try:
            response = self.client.get("/health")
            response.raise_for_status()
            data = response.json()

            status_color = {"healthy": "green", "degraded": "yellow", "unhealthy": "red"}.get(
                data["status"], "white"
            )

            console.print(
                f"\n[bold]API Health:[/bold] [{status_color}]{data['status'].upper()}[/{status_color}]"
            )
            console.print(f"Version: {data.get('version', 'unknown')}")
            console.print(f"Redis: {data.get('redis', 'unknown')}")
            console.print(f"Telegram: {data.get('telegram', 'unknown')}")

            if data.get("warnings"):
                console.print("\n[yellow]Warnings:[/yellow]")
                for warning in data["warnings"]:
                    console.print(f"  • {warning}")

        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Legend AI CLI - Trading Pattern Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--url", default="https://legend-ai-python-production.up.railway.app", help="API base URL")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Detect command
    detect_parser = subparsers.add_parser("detect", help="Detect pattern for a ticker")
    detect_parser.add_argument("ticker", help="Stock ticker symbol")
    detect_parser.add_argument("--interval", default="1day", choices=["1day", "1week", "1hour", "4hour"])

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan universe for patterns")
    scan_parser.add_argument("--universe", default="SP500", choices=["SP500", "NASDAQ100"])
    scan_parser.add_argument("--min-score", type=float, default=7.0, help="Minimum pattern score")
    scan_parser.add_argument("--max-results", type=int, default=20, help="Maximum results")

    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Chat with AI assistant")
    chat_parser.add_argument("message", help="Your message")
    chat_parser.add_argument("--symbol", help="Stock symbol for context")

    # Watchlist commands
    watchlist_parser = subparsers.add_parser("watchlist", help="Manage watchlist")
    watchlist_subparsers = watchlist_parser.add_subparsers(dest="watchlist_command")

    watchlist_list_parser = watchlist_subparsers.add_parser("list", help="List watchlist items")
    watchlist_add_parser = watchlist_subparsers.add_parser("add", help="Add to watchlist")
    watchlist_add_parser.add_argument("ticker", help="Stock ticker")
    watchlist_add_parser.add_argument("--reason", help="Reason for adding")

    # Health command
    health_parser = subparsers.add_parser("health", help="Check API health")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cli = LegendCLI(base_url=args.url)

    if args.command == "detect":
        cli.detect_pattern(args.ticker, args.interval)
    elif args.command == "scan":
        cli.scan_universe(args.universe, args.min_score, args.max_results)
    elif args.command == "chat":
        cli.chat(args.message, args.symbol)
    elif args.command == "watchlist":
        if args.watchlist_command == "list":
            cli.watchlist_list()
        elif args.watchlist_command == "add":
            cli.watchlist_add(args.ticker, args.reason)
        else:
            watchlist_parser.print_help()
    elif args.command == "health":
        cli.health()


if __name__ == "__main__":
    main()
