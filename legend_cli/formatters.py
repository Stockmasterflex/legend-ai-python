"""Output formatters for Legend CLI."""

import json
import csv
import yaml
from io import StringIO
from typing import Any, List, Dict, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.tree import Tree
from rich import box


class OutputFormatter:
    """Handles output formatting for different formats."""

    def __init__(self, console: Optional[Console] = None):
        """Initialize formatter."""
        self.console = console or Console()

    def format(
        self,
        data: Any,
        format_type: str = "table",
        title: Optional[str] = None
    ) -> str:
        """Format data based on format type."""
        if format_type == "json":
            return self.format_json(data)
        elif format_type == "yaml":
            return self.format_yaml(data)
        elif format_type == "csv":
            return self.format_csv(data)
        elif format_type == "table":
            return self.format_table(data, title)
        else:
            raise ValueError(f"Unknown format type: {format_type}")

    def format_json(self, data: Any, pretty: bool = True) -> str:
        """Format as JSON."""
        if pretty:
            return json.dumps(data, indent=2, default=str)
        return json.dumps(data, default=str)

    def format_yaml(self, data: Any) -> str:
        """Format as YAML."""
        return yaml.dump(data, default_flow_style=False, sort_keys=False)

    def format_csv(self, data: Any) -> str:
        """Format as CSV."""
        if not data:
            return ""

        output = StringIO()

        if isinstance(data, dict):
            # Single record
            writer = csv.DictWriter(output, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)
        elif isinstance(data, list) and data:
            # Multiple records
            if isinstance(data[0], dict):
                writer = csv.DictWriter(output, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            else:
                writer = csv.writer(output)
                for row in data:
                    writer.writerow([row] if not isinstance(row, (list, tuple)) else row)

        return output.getvalue()

    def format_table(self, data: Any, title: Optional[str] = None) -> str:
        """Format as rich table."""
        # This returns empty string as table is printed directly
        if isinstance(data, dict):
            self.print_dict_table(data, title)
        elif isinstance(data, list) and data:
            if isinstance(data[0], dict):
                self.print_list_table(data, title)
            else:
                self.print_simple_list(data, title)
        else:
            self.console.print(data)

        return ""

    def print_dict_table(self, data: Dict[str, Any], title: Optional[str] = None):
        """Print dictionary as table."""
        table = Table(
            title=title,
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )

        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")

        for key, value in data.items():
            # Format value
            if isinstance(value, (dict, list)):
                value_str = json.dumps(value, indent=2, default=str)
            else:
                value_str = str(value)

            table.add_row(key, value_str)

        self.console.print(table)

    def print_list_table(self, data: List[Dict[str, Any]], title: Optional[str] = None):
        """Print list of dictionaries as table."""
        if not data:
            return

        table = Table(
            title=title,
            box=box.ROUNDED,
            show_header=True,
            header_style="bold cyan"
        )

        # Add columns from first record
        columns = list(data[0].keys())
        for col in columns:
            table.add_column(col, style="white")

        # Add rows
        for record in data:
            row = []
            for col in columns:
                value = record.get(col, "")
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, default=str)
                row.append(str(value))
            table.add_row(*row)

        self.console.print(table)

    def print_simple_list(self, data: List[Any], title: Optional[str] = None):
        """Print simple list."""
        if title:
            self.console.print(f"\n[bold cyan]{title}[/bold cyan]")

        for item in data:
            self.console.print(f"  • {item}")

    def print_analysis(self, analysis: Dict[str, Any]):
        """Print analysis results with rich formatting."""
        ticker = analysis.get('ticker', 'N/A')

        # Main panel
        self.console.print(Panel(
            f"[bold cyan]Analysis Results for {ticker}[/bold cyan]",
            box=box.DOUBLE
        ))

        # Price info
        if 'current_price' in analysis:
            price_table = Table(box=box.SIMPLE, show_header=False)
            price_table.add_column("Metric", style="cyan")
            price_table.add_column("Value", style="green")

            price_table.add_row("Current Price", f"${analysis.get('current_price', 0):.2f}")
            if 'change_percent' in analysis:
                change = analysis['change_percent']
                color = "green" if change >= 0 else "red"
                price_table.add_row(
                    "Change",
                    f"[{color}]{change:+.2f}%[/{color}]"
                )

            self.console.print(price_table)

        # Technical indicators
        if 'indicators' in analysis:
            self.console.print("\n[bold]Technical Indicators[/bold]")
            ind = analysis['indicators']

            ind_table = Table(box=box.SIMPLE)
            ind_table.add_column("Indicator", style="cyan")
            ind_table.add_column("Value", style="white")

            for key, value in ind.items():
                if isinstance(value, float):
                    ind_table.add_row(key.upper(), f"{value:.2f}")
                else:
                    ind_table.add_row(key.upper(), str(value))

            self.console.print(ind_table)

        # Patterns
        if 'patterns' in analysis and analysis['patterns']:
            self.console.print("\n[bold]Detected Patterns[/bold]")
            for pattern in analysis['patterns']:
                pattern_name = pattern.get('name', 'Unknown')
                confidence = pattern.get('confidence', 0)
                color = "green" if confidence > 0.7 else "yellow" if confidence > 0.5 else "red"

                self.console.print(
                    f"  • [{color}]{pattern_name}[/{color}] "
                    f"(Confidence: {confidence:.0%})"
                )

        # Trend classification
        if 'trend' in analysis:
            trend = analysis['trend']
            self.console.print(f"\n[bold]Trend:[/bold] {trend}")

    def print_scan_results(self, results: Dict[str, Any]):
        """Print scan results with rich formatting."""
        self.console.print(Panel(
            "[bold cyan]Scan Results[/bold cyan]",
            box=box.DOUBLE
        ))

        summary = results.get('summary', {})
        if summary:
            self.console.print(f"\n[bold]Summary[/bold]")
            self.console.print(f"  Total Scanned: {summary.get('total_scanned', 0)}")
            self.console.print(f"  Patterns Found: {summary.get('patterns_found', 0)}")
            self.console.print(f"  Success Rate: {summary.get('success_rate', 0):.1f}%")

        matches = results.get('matches', [])
        if matches:
            self.console.print(f"\n[bold]Top Matches ({len(matches)})[/bold]\n")

            table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")
            table.add_column("Ticker", style="cyan", no_wrap=True)
            table.add_column("Pattern", style="yellow")
            table.add_column("Confidence", style="green")
            table.add_column("Price", style="white")
            table.add_column("RS Rating", style="magenta")

            for match in matches[:20]:  # Show top 20
                ticker = match.get('ticker', 'N/A')
                pattern = match.get('pattern_type', 'N/A')
                confidence = match.get('confidence', 0)
                price = match.get('price', 0)
                rs_rating = match.get('rs_rating', 0)

                conf_color = "green" if confidence > 0.7 else "yellow"

                table.add_row(
                    ticker,
                    pattern,
                    f"[{conf_color}]{confidence:.0%}[/{conf_color}]",
                    f"${price:.2f}",
                    f"{rs_rating:.0f}"
                )

            self.console.print(table)

    def print_watchlist(self, watchlist: List[Dict[str, Any]]):
        """Print watchlist with rich formatting."""
        if not watchlist:
            self.console.print("[yellow]Watchlist is empty[/yellow]")
            return

        self.console.print(Panel(
            f"[bold cyan]Watchlist ({len(watchlist)} items)[/bold cyan]",
            box=box.DOUBLE
        ))

        table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")
        table.add_column("Ticker", style="cyan", no_wrap=True)
        table.add_column("Status", style="yellow")
        table.add_column("Alert Price", style="white")
        table.add_column("Notes", style="white")
        table.add_column("Added", style="dim")

        for item in watchlist:
            ticker = item.get('ticker', 'N/A')
            status = item.get('status', 'active')
            alert_price = item.get('alert_price')
            notes = item.get('notes', '')
            added = item.get('created_at', '')

            status_color = "green" if status == "active" else "dim"

            table.add_row(
                ticker,
                f"[{status_color}]{status}[/{status_color}]",
                f"${alert_price:.2f}" if alert_price else "-",
                notes[:50] if notes else "-",
                added[:10] if added else "-"
            )

        self.console.print(table)

    def print_error(self, message: str):
        """Print error message."""
        self.console.print(f"[bold red]Error:[/bold red] {message}")

    def print_success(self, message: str):
        """Print success message."""
        self.console.print(f"[bold green]✓[/bold green] {message}")

    def print_info(self, message: str):
        """Print info message."""
        self.console.print(f"[bold cyan]ℹ[/bold cyan] {message}")

    def print_warning(self, message: str):
        """Print warning message."""
        self.console.print(f"[bold yellow]⚠[/bold yellow] {message}")
