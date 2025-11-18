"""
Interactive Discord UI components (Views, Buttons, Modals, Selects).
"""
import discord
from discord.ui import Button, Select, Modal, TextInput, View
from typing import Optional, List, Dict, Any
import logging

from app.services.discord_service import discord_service

logger = logging.getLogger(__name__)


# ==================== PATTERN ANALYSIS VIEW ====================

class PatternAnalysisView(View):
    """Interactive view for pattern analysis with action buttons."""

    def __init__(self, ticker: str, data: Dict[str, Any], chart_url: Optional[str] = None):
        super().__init__(timeout=300)
        self.ticker = ticker
        self.data = data
        self.chart_url = chart_url

    @discord.ui.button(label="Add to Watchlist", style=discord.ButtonStyle.primary, emoji="📌")
    async def add_watchlist(self, interaction: discord.Interaction, button: Button):
        """Add stock to user's watchlist."""
        discord_id = str(interaction.user.id)

        # Get pattern info
        patterns = self.data.get("patterns", [])
        pattern_name = patterns[0].get("pattern") if patterns else None
        entry = self.data.get("price", 0)

        success = discord_service.add_to_watchlist(
            discord_id=discord_id,
            ticker=self.ticker,
            pattern=pattern_name,
            entry_price=entry,
        )

        if success:
            await interaction.response.send_message(
                f"✅ Added **{self.ticker}** to your watchlist!",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Failed to add to watchlist. Please try again.",
                ephemeral=True
            )

    @discord.ui.button(label="Set Alert", style=discord.ButtonStyle.secondary, emoji="🔔")
    async def set_alert_btn(self, interaction: discord.Interaction, button: Button):
        """Open alert modal."""
        await interaction.response.send_modal(AlertModal(self.ticker))

    @discord.ui.button(label="Make Call", style=discord.ButtonStyle.success, emoji="📈")
    async def make_call(self, interaction: discord.Interaction, button: Button):
        """Make a trading call for leaderboard."""
        await interaction.response.send_modal(TradingCallModal(self.ticker, self.data))

    @discord.ui.button(label="Paper Trade", style=discord.ButtonStyle.secondary, emoji="💰")
    async def paper_trade(self, interaction: discord.Interaction, button: Button):
        """Open paper trade modal."""
        await interaction.response.send_modal(PaperTradeModal(self.ticker, self.data))

    @discord.ui.button(label="Share", style=discord.ButtonStyle.success, emoji="📤")
    async def share(self, interaction: discord.Interaction, button: Button):
        """Share analysis with channel."""
        patterns = self.data.get("patterns", [])
        pattern_str = patterns[0].get("pattern") if patterns else "No pattern"

        message = (
            f"📊 **{interaction.user.display_name}** shared {self.ticker} analysis\n"
            f"Pattern: **{pattern_str}**\n"
            f"Price: ${self.data.get('price', 0):.2f}"
        )

        await interaction.response.send_message(message)


# ==================== WATCHLIST VIEW ====================

class WatchlistView(View):
    """Interactive watchlist with pagination and actions."""

    def __init__(self, items: List[Dict[str, Any]], page: int = 0):
        super().__init__(timeout=300)
        self.items = items
        self.page = page
        self.items_per_page = 5

    def get_page_items(self) -> List[Dict[str, Any]]:
        """Get items for current page."""
        start = self.page * self.items_per_page
        end = start + self.items_per_page
        return self.items[start:end]

    def get_embed(self) -> discord.Embed:
        """Generate watchlist embed."""
        embed = discord.Embed(
            title="📋 Your Watchlist",
            color=discord.Color.blue(),
            description=f"Page {self.page + 1}/{self.total_pages}"
        )

        page_items = self.get_page_items()

        for item in page_items:
            ticker = item["ticker"]
            pattern = item.get("pattern", "N/A")
            entry = item.get("entry_price", 0)

            value = f"Pattern: {pattern}"
            if entry:
                value += f"\nEntry: ${entry:.2f}"

            embed.add_field(
                name=f"📊 {ticker}",
                value=value,
                inline=True
            )

        if not page_items:
            embed.description = "Your watchlist is empty. Use `/add <ticker>` to add stocks."

        return embed

    @property
    def total_pages(self) -> int:
        """Calculate total pages."""
        return max(1, (len(self.items) + self.items_per_page - 1) // self.items_per_page)

    @discord.ui.button(label="◀️ Previous", style=discord.ButtonStyle.secondary)
    async def previous_page(self, interaction: discord.Interaction, button: Button):
        """Go to previous page."""
        if self.page > 0:
            self.page -= 1
            await interaction.response.edit_message(embed=self.get_embed(), view=self)
        else:
            await interaction.response.send_message("Already on first page", ephemeral=True)

    @discord.ui.button(label="Next ▶️", style=discord.ButtonStyle.secondary)
    async def next_page(self, interaction: discord.Interaction, button: Button):
        """Go to next page."""
        if self.page < self.total_pages - 1:
            self.page += 1
            await interaction.response.edit_message(embed=self.get_embed(), view=self)
        else:
            await interaction.response.send_message("Already on last page", ephemeral=True)

    @discord.ui.button(label="Remove Stock", style=discord.ButtonStyle.danger, emoji="🗑️")
    async def remove_stock(self, interaction: discord.Interaction, button: Button):
        """Remove stock from watchlist."""
        await interaction.response.send_modal(RemoveFromWatchlistModal())

    @discord.ui.button(label="Refresh", style=discord.ButtonStyle.primary, emoji="🔄")
    async def refresh(self, interaction: discord.Interaction, button: Button):
        """Refresh watchlist."""
        discord_id = str(interaction.user.id)
        self.items = discord_service.get_watchlist(discord_id)
        self.page = 0

        await interaction.response.edit_message(embed=self.get_embed(), view=self)


# ==================== SCAN RESULTS VIEW ====================

class ScanResultsView(View):
    """Interactive scan results with filtering and actions."""

    def __init__(self, results: List[Dict[str, Any]]):
        super().__init__(timeout=600)
        self.results = results
        self.current_filter = "all"
        self.page = 0

        # Add pattern filter select
        self.add_item(PatternFilterSelect(self))

    def get_filtered_results(self) -> List[Dict[str, Any]]:
        """Get filtered results."""
        if self.current_filter == "all":
            return self.results

        return [
            r for r in self.results
            if r.get("pattern", "").lower() == self.current_filter.lower()
        ]

    def get_embed(self) -> discord.Embed:
        """Generate results embed."""
        filtered = self.get_filtered_results()

        embed = discord.Embed(
            title="🔍 Pattern Scan Results",
            description=f"Found {len(filtered)} patterns",
            color=discord.Color.green()
        )

        # Show top 10
        for i, result in enumerate(filtered[:10], 1):
            ticker = result.get("symbol", "N/A")
            pattern = result.get("pattern", "N/A")
            confidence = result.get("confidence", 0) * 100

            embed.add_field(
                name=f"{i}. {ticker}",
                value=f"{pattern} ({confidence:.0f}%)",
                inline=True
            )

        if self.current_filter != "all":
            embed.set_footer(text=f"Filter: {self.current_filter}")

        return embed

    @discord.ui.button(label="Add All to Watchlist", style=discord.ButtonStyle.primary, emoji="📌")
    async def add_all(self, interaction: discord.Interaction, button: Button):
        """Add all filtered results to watchlist."""
        filtered = self.get_filtered_results()[:10]  # Limit to top 10
        discord_id = str(interaction.user.id)

        count = 0
        for result in filtered:
            ticker = result.get("symbol")
            pattern = result.get("pattern")

            if discord_service.add_to_watchlist(discord_id, ticker, pattern=pattern):
                count += 1

        await interaction.response.send_message(
            f"✅ Added {count} stocks to your watchlist!",
            ephemeral=True
        )


class PatternFilterSelect(Select):
    """Dropdown to filter scan results by pattern."""

    def __init__(self, parent_view: ScanResultsView):
        self.parent_view = parent_view

        # Get unique patterns from results
        patterns = set(r.get("pattern", "Unknown") for r in parent_view.results)

        options = [
            discord.SelectOption(label="All Patterns", value="all", emoji="🔍")
        ]

        for pattern in sorted(patterns):
            options.append(
                discord.SelectOption(label=pattern, value=pattern, emoji="📊")
            )

        super().__init__(
            placeholder="Filter by pattern...",
            options=options[:25],  # Discord limit
            row=0
        )

    async def callback(self, interaction: discord.Interaction):
        """Handle selection."""
        self.parent_view.current_filter = self.values[0]
        await interaction.response.edit_message(
            embed=self.parent_view.get_embed(),
            view=self.parent_view
        )


# ==================== MODALS ====================

class AlertModal(Modal, title="Set Price Alert"):
    """Modal for creating alerts."""

    alert_type = TextInput(
        label="Alert Type",
        placeholder="price_above, price_below, pattern, rsi_oversold",
        required=True,
        max_length=50
    )

    threshold = TextInput(
        label="Price Threshold (if price alert)",
        placeholder="100.00",
        required=False,
        max_length=20
    )

    pattern_name = TextInput(
        label="Pattern Name (if pattern alert)",
        placeholder="VCP, Cup & Handle, etc.",
        required=False,
        max_length=50
    )

    def __init__(self, ticker: str):
        super().__init__()
        self.ticker = ticker

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        discord_id = str(interaction.user.id)

        threshold_val = None
        if self.threshold.value:
            try:
                threshold_val = float(self.threshold.value)
            except ValueError:
                await interaction.response.send_message(
                    "❌ Invalid price threshold",
                    ephemeral=True
                )
                return

        success = discord_service.create_alert(
            discord_id=discord_id,
            ticker=self.ticker,
            alert_type=self.alert_type.value,
            threshold=threshold_val,
            pattern_name=self.pattern_name.value or None,
        )

        if success:
            await interaction.response.send_message(
                f"✅ Alert set for **{self.ticker}**!\nType: {self.alert_type.value}",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Failed to create alert",
                ephemeral=True
            )


class TradingCallModal(Modal, title="Make Trading Call"):
    """Modal for making public trading calls."""

    call_type = TextInput(
        label="Call Type",
        placeholder="bullish, bearish, or neutral",
        required=True,
        max_length=20
    )

    target = TextInput(
        label="Price Target",
        placeholder="Target price",
        required=False,
        max_length=20
    )

    stop = TextInput(
        label="Stop Loss",
        placeholder="Stop loss price",
        required=False,
        max_length=20
    )

    reasoning = TextInput(
        label="Your Reasoning",
        placeholder="Why are you making this call?",
        style=discord.TextStyle.paragraph,
        required=False,
        max_length=500
    )

    def __init__(self, ticker: str, data: Dict[str, Any]):
        super().__init__()
        self.ticker = ticker
        self.data = data

    async def on_submit(self, interaction: discord.Interaction):
        """Handle trading call submission."""
        discord_id = str(interaction.user.id)
        entry_price = self.data.get("price", 0)

        target_val = None
        if self.target.value:
            try:
                target_val = float(self.target.value)
            except ValueError:
                pass

        stop_val = None
        if self.stop.value:
            try:
                stop_val = float(self.stop.value)
            except ValueError:
                pass

        call_id = discord_service.create_trading_call(
            discord_id=discord_id,
            ticker=self.ticker,
            call_type=self.call_type.value,
            entry_price=entry_price,
            target_price=target_val,
            stop_loss=stop_val,
            reasoning=self.reasoning.value or None,
            message_id=str(interaction.message.id) if interaction.message else None,
            channel_id=str(interaction.channel_id),
            guild_id=str(interaction.guild_id) if interaction.guild_id else None,
        )

        if call_id:
            # Public announcement
            embed = discord.Embed(
                title=f"📈 Trading Call: {self.ticker}",
                description=f"{interaction.user.display_name} is {self.call_type.value.upper()}",
                color=discord.Color.green() if self.call_type.value == "bullish" else discord.Color.red()
            )

            embed.add_field(name="Entry", value=f"${entry_price:.2f}", inline=True)

            if target_val:
                embed.add_field(name="Target", value=f"${target_val:.2f}", inline=True)
            if stop_val:
                embed.add_field(name="Stop", value=f"${stop_val:.2f}", inline=True)

            if self.reasoning.value:
                embed.add_field(
                    name="Reasoning",
                    value=self.reasoning.value,
                    inline=False
                )

            embed.set_footer(text=f"Call ID: {call_id} • Track this for leaderboard")

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                "❌ Failed to create trading call",
                ephemeral=True
            )


class PaperTradeModal(Modal, title="Paper Trade"):
    """Modal for paper trading."""

    action = TextInput(
        label="Action",
        placeholder="buy or sell",
        required=True,
        max_length=10
    )

    shares = TextInput(
        label="Number of Shares",
        placeholder="100",
        required=True,
        max_length=10
    )

    def __init__(self, ticker: str, data: Dict[str, Any]):
        super().__init__()
        self.ticker = ticker
        self.data = data

    async def on_submit(self, interaction: discord.Interaction):
        """Handle paper trade submission."""
        discord_id = str(interaction.user.id)

        try:
            shares_val = int(self.shares.value)
            if shares_val <= 0:
                raise ValueError("Shares must be positive")
        except ValueError:
            await interaction.response.send_message(
                "❌ Invalid number of shares",
                ephemeral=True
            )
            return

        action = self.action.value.lower()

        if action == "buy":
            # Create new paper trade
            price = self.data.get("price", 0)

            trade_id = discord_service.create_paper_trade(
                discord_id=discord_id,
                ticker=self.ticker,
                side="long",
                entry_price=price,
                shares=shares_val,
            )

            if trade_id:
                total_cost = price * shares_val

                embed = discord.Embed(
                    title="✅ Paper Trade Executed",
                    description=f"BUY {shares_val} shares of {self.ticker}",
                    color=discord.Color.green()
                )

                embed.add_field(name="Entry Price", value=f"${price:.2f}", inline=True)
                embed.add_field(name="Total Cost", value=f"${total_cost:.2f}", inline=True)
                embed.add_field(name="Trade ID", value=str(trade_id), inline=True)

                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(
                    "❌ Failed to execute trade",
                    ephemeral=True
                )

        elif action == "sell":
            # Close existing trade - would need to select which trade
            await interaction.response.send_message(
                "To close a trade, use `/papertrade sell <trade_id>`",
                ephemeral=True
            )

        else:
            await interaction.response.send_message(
                "❌ Invalid action. Use 'buy' or 'sell'",
                ephemeral=True
            )


class RemoveFromWatchlistModal(Modal, title="Remove from Watchlist"):
    """Modal for removing stocks from watchlist."""

    ticker = TextInput(
        label="Ticker Symbol",
        placeholder="AAPL",
        required=True,
        max_length=10
    )

    async def on_submit(self, interaction: discord.Interaction):
        """Handle removal."""
        discord_id = str(interaction.user.id)

        success = discord_service.remove_from_watchlist(
            discord_id,
            self.ticker.value.upper()
        )

        if success:
            await interaction.response.send_message(
                f"✅ Removed **{self.ticker.value.upper()}** from watchlist",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"❌ Could not find **{self.ticker.value.upper()}** in your watchlist",
                ephemeral=True
            )


# ==================== LEADERBOARD VIEW ====================

class LeaderboardView(View):
    """Interactive leaderboard with pagination."""

    def __init__(self, leaderboard_data: List[Dict[str, Any]], page: int = 0):
        super().__init__(timeout=300)
        self.leaderboard_data = leaderboard_data
        self.page = page
        self.items_per_page = 10

    def get_embed(self) -> discord.Embed:
        """Generate leaderboard embed."""
        embed = discord.Embed(
            title="🏆 Trading Leaderboard",
            description="Top traders by accuracy",
            color=discord.Color.gold()
        )

        start = self.page * self.items_per_page
        end = start + self.items_per_page

        page_data = self.leaderboard_data[start:end]

        for entry in page_data:
            rank = entry["rank"]
            username = entry["username"]
            accuracy = entry["accuracy"]
            total = entry["total_calls"]
            correct = entry["correct_calls"]

            medal = ""
            if rank == 1:
                medal = "🥇"
            elif rank == 2:
                medal = "🥈"
            elif rank == 3:
                medal = "🥉"

            embed.add_field(
                name=f"{medal} #{rank} - {username}",
                value=f"Accuracy: {accuracy:.1f}% ({correct}/{total} calls)",
                inline=False
            )

        return embed

    @discord.ui.button(label="◀️ Previous", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: Button):
        """Previous page."""
        if self.page > 0:
            self.page -= 1
            await interaction.response.edit_message(embed=self.get_embed(), view=self)
        else:
            await interaction.response.send_message("First page", ephemeral=True)

    @discord.ui.button(label="Next ▶️", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: Button):
        """Next page."""
        max_pages = (len(self.leaderboard_data) + self.items_per_page - 1) // self.items_per_page

        if self.page < max_pages - 1:
            self.page += 1
            await interaction.response.edit_message(embed=self.get_embed(), view=self)
        else:
            await interaction.response.send_message("Last page", ephemeral=True)
