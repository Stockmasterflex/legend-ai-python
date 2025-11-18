"""Main TUI application for Legend AI."""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, DataTable, Button, Input, TabbedContent, TabPane
from textual.binding import Binding
from textual import events
from textual.reactive import reactive
from datetime import datetime
import asyncio

from ..client import LegendAPIClient
from ..config_manager import get_config


class StatusBar(Static):
    """Status bar showing API connection and last update time."""

    status = reactive("Initializing...")
    last_update = reactive("")

    def render(self) -> str:
        """Render status bar."""
        return f"Status: {self.status} | Last Update: {self.last_update}"


class MarketOverview(Static):
    """Market overview panel."""

    market_data = reactive({})

    def render(self) -> str:
        """Render market overview."""
        if not self.market_data:
            return "[cyan]Loading market data...[/cyan]"

        lines = ["[bold cyan]Market Overview[/bold cyan]\n"]

        breadth = self.market_data.get('breadth', {})
        if breadth:
            lines.append(f"Advance/Decline: {breadth.get('advance_decline_ratio', 0):.2f}")
            lines.append(f"New Highs: {breadth.get('new_highs', 0)}")
            lines.append(f"New Lows: {breadth.get('new_lows', 0)}")

        return "\n".join(lines)


class WatchlistPanel(Static):
    """Watchlist panel showing tracked stocks."""

    watchlist = reactive([])

    def render(self) -> str:
        """Render watchlist."""
        if not self.watchlist:
            return "[yellow]Watchlist is empty[/yellow]"

        lines = ["[bold cyan]Watchlist[/bold cyan]\n"]

        for item in self.watchlist[:10]:  # Show top 10
            ticker = item.get('ticker', 'N/A')
            status = item.get('status', 'active')
            lines.append(f"  • {ticker} [{status}]")

        if len(self.watchlist) > 10:
            lines.append(f"\n  ... and {len(self.watchlist) - 10} more")

        return "\n".join(lines)


class ScanResults(DataTable):
    """Data table for scan results."""

    def __init__(self, *args, **kwargs):
        """Initialize scan results table."""
        super().__init__(*args, **kwargs)
        self.cursor_type = "row"
        self.zebra_stripes = True

    def on_mount(self) -> None:
        """Set up table columns when mounted."""
        self.add_column("Ticker", key="ticker")
        self.add_column("Pattern", key="pattern")
        self.add_column("Confidence", key="confidence")
        self.add_column("Price", key="price")
        self.add_column("RS Rating", key="rs_rating")

    def update_results(self, results: list):
        """Update table with scan results."""
        self.clear()

        for result in results:
            ticker = result.get('ticker', 'N/A')
            pattern = result.get('pattern_type', 'N/A')
            confidence = result.get('confidence', 0)
            price = result.get('price', 0)
            rs_rating = result.get('rs_rating', 0)

            self.add_row(
                ticker,
                pattern,
                f"{confidence:.0%}",
                f"${price:.2f}",
                f"{rs_rating:.0f}"
            )


class AnalysisPanel(Static):
    """Analysis details panel."""

    analysis = reactive({})

    def render(self) -> str:
        """Render analysis."""
        if not self.analysis:
            return "[dim]Select a ticker to analyze[/dim]"

        lines = []

        ticker = self.analysis.get('ticker', 'N/A')
        lines.append(f"[bold cyan]{ticker} Analysis[/bold cyan]\n")

        # Price info
        if 'current_price' in self.analysis:
            price = self.analysis['current_price']
            lines.append(f"Price: ${price:.2f}")

        if 'change_percent' in self.analysis:
            change = self.analysis['change_percent']
            color = "green" if change >= 0 else "red"
            lines.append(f"Change: [{color}]{change:+.2f}%[/{color}]")

        # Indicators
        if 'indicators' in self.analysis:
            lines.append("\n[bold]Indicators[/bold]")
            for key, value in self.analysis['indicators'].items():
                if isinstance(value, float):
                    lines.append(f"  {key}: {value:.2f}")
                else:
                    lines.append(f"  {key}: {value}")

        # Patterns
        if 'patterns' in self.analysis and self.analysis['patterns']:
            lines.append("\n[bold]Patterns[/bold]")
            for pattern in self.analysis['patterns']:
                name = pattern.get('name', 'Unknown')
                conf = pattern.get('confidence', 0)
                lines.append(f"  • {name} ({conf:.0%})")

        return "\n".join(lines)


class LegendTUI(App):
    """Legend AI Terminal User Interface."""

    CSS = """
    Screen {
        layout: grid;
        grid-size: 3 3;
        grid-rows: 3 1fr 1;
    }

    Header {
        column-span: 3;
    }

    #market-overview {
        row-span: 2;
        border: solid cyan;
        padding: 1;
    }

    #scan-results {
        row-span: 2;
        column-span: 2;
        border: solid cyan;
        padding: 1;
    }

    #watchlist {
        border: solid cyan;
        padding: 1;
    }

    #analysis {
        column-span: 2;
        border: solid cyan;
        padding: 1;
    }

    StatusBar {
        column-span: 3;
        background: $boost;
        color: $text;
        padding: 0 1;
    }

    Footer {
        column-span: 3;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("s", "scan", "Scan"),
        Binding("w", "watchlist", "Watchlist"),
        Binding("a", "analyze", "Analyze"),
        Binding("?", "help", "Help"),
    ]

    def __init__(self, universe: str = "SP500", refresh_interval: int = 5):
        """Initialize TUI."""
        super().__init__()
        self.universe = universe
        self.refresh_interval = refresh_interval
        self.title = "Legend AI - Trading Pattern Scanner"
        self.sub_title = f"Universe: {universe}"

        # Components
        self.status_bar = None
        self.market_overview = None
        self.scan_results = None
        self.watchlist_panel = None
        self.analysis_panel = None

        # API client
        self.client = None
        self.auto_refresh_task = None

    def compose(self) -> ComposeResult:
        """Compose TUI layout."""
        yield Header(show_clock=True)

        self.market_overview = MarketOverview(id="market-overview")
        yield self.market_overview

        self.scan_results = ScanResults(id="scan-results")
        yield self.scan_results

        self.watchlist_panel = WatchlistPanel(id="watchlist")
        yield self.watchlist_panel

        self.analysis_panel = AnalysisPanel(id="analysis")
        yield self.analysis_panel

        self.status_bar = StatusBar()
        yield self.status_bar

        yield Footer()

    async def on_mount(self) -> None:
        """Handle mount event."""
        # Initialize API client
        config = get_config()
        self.client = LegendAPIClient(
            base_url=config.api_url,
            api_key=config.api_key,
            timeout=config.timeout
        )

        # Initial data load
        await self.refresh_all()

        # Start auto-refresh
        self.auto_refresh_task = asyncio.create_task(self.auto_refresh())

    async def on_unmount(self) -> None:
        """Handle unmount event."""
        # Cancel auto-refresh
        if self.auto_refresh_task:
            self.auto_refresh_task.cancel()

        # Close API client
        if self.client:
            await self.client.close()

    async def auto_refresh(self):
        """Auto-refresh data periodically."""
        while True:
            try:
                await asyncio.sleep(self.refresh_interval)
                await self.refresh_all()
            except asyncio.CancelledError:
                break
            except Exception:
                pass

    async def refresh_all(self):
        """Refresh all data."""
        try:
            self.status_bar.status = "Refreshing..."

            # Fetch data concurrently
            market_task = self.client.market_internals(self.universe)
            scan_task = self.client.quick_scan(self.universe)
            watchlist_task = self.client.watchlist_list()

            market_data, scan_data, watchlist_data = await asyncio.gather(
                market_task,
                scan_task,
                watchlist_task,
                return_exceptions=True
            )

            # Update panels
            if isinstance(market_data, dict):
                self.market_overview.market_data = market_data

            if isinstance(scan_data, dict):
                matches = scan_data.get('matches', [])
                self.scan_results.update_results(matches[:50])

            if isinstance(watchlist_data, dict):
                items = watchlist_data.get('items', [])
                self.watchlist_panel.watchlist = items

            # Update status
            self.status_bar.status = "Connected"
            self.status_bar.last_update = datetime.now().strftime("%H:%M:%S")

        except Exception as e:
            self.status_bar.status = f"Error: {str(e)}"

    async def action_refresh(self) -> None:
        """Refresh action."""
        await self.refresh_all()

    async def action_scan(self) -> None:
        """Trigger a new scan."""
        try:
            self.status_bar.status = "Scanning..."
            result = await self.client.scan(universe=self.universe)

            matches = result.get('matches', [])
            self.scan_results.update_results(matches[:50])

            self.status_bar.status = f"Scan complete: {len(matches)} matches"

        except Exception as e:
            self.status_bar.status = f"Scan error: {str(e)}"

    async def action_analyze(self) -> None:
        """Analyze selected ticker."""
        try:
            # Get selected row
            row_key = self.scan_results.cursor_row

            if row_key is None or row_key < 0:
                self.status_bar.status = "No ticker selected"
                return

            # Get ticker from table
            row = self.scan_results.get_row_at(row_key)
            ticker = str(row[0])  # First column is ticker

            self.status_bar.status = f"Analyzing {ticker}..."

            # Fetch analysis
            result = await self.client.analyze(ticker)
            self.analysis_panel.analysis = result

            self.status_bar.status = f"Analysis complete: {ticker}"

        except Exception as e:
            self.status_bar.status = f"Analysis error: {str(e)}"

    async def action_watchlist(self) -> None:
        """Refresh watchlist."""
        try:
            self.status_bar.status = "Refreshing watchlist..."
            result = await self.client.watchlist_list()

            items = result.get('items', [])
            self.watchlist_panel.watchlist = items

            self.status_bar.status = f"Watchlist: {len(items)} items"

        except Exception as e:
            self.status_bar.status = f"Watchlist error: {str(e)}"

    def action_help(self) -> None:
        """Show help."""
        self.status_bar.status = "Press: [r]efresh [s]can [a]nalyze [w]atchlist [q]uit"


def run_tui(universe: str = "SP500", refresh_interval: int = 5):
    """Run the TUI application."""
    app = LegendTUI(universe=universe, refresh_interval=refresh_interval)
    app.run()
