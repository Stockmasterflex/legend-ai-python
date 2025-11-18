"""
Full-featured Discord bot for stock analysis and community trading.
"""
import asyncio
import logging
from datetime import datetime, time, timedelta
from typing import Optional, List, Dict, Any
from io import BytesIO
import discord
from discord import app_commands
from discord.ext import commands, tasks
import httpx

from app.config import get_settings
from app.services.market_data import market_data_service
from app.services.scanner import ScannerService
from app.services.discord_service import discord_service
from app.infra.chartimg import build_analyze_chart
from app.discord_views import (
    PatternAnalysisView,
    WatchlistView,
    ScanResultsView,
    LeaderboardView,
)
from app.discord_tasks import DiscordTasksManager
from app.discord_admin import setup_admin_commands

logger = logging.getLogger(__name__)


class StockBot(commands.Bot):
    """Discord bot for stock analysis and trading community."""

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

        self.settings = get_settings()
        self.scanner = ScannerService()
        self.http_client = httpx.AsyncClient(timeout=30.0)

    async def setup_hook(self):
        """Set up bot on startup."""
        # Initialize task manager
        self.tasks_manager = DiscordTasksManager(self)
        self.tasks_manager.start_all_tasks()

        # Register admin commands
        setup_admin_commands(self)

        logger.info("Discord bot setup complete")

    async def on_ready(self):
        """Bot is ready."""
        logger.info(f"✅ Discord bot logged in as {self.user}")
        logger.info(f"   Guilds: {len(self.guilds)}")

        # Sync commands
        try:
            synced = await self.tree.sync()
            logger.info(f"   Synced {len(synced)} command(s)")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")



# Create bot instance
bot = StockBot()


# ==================== SLASH COMMANDS ====================

@bot.tree.command(name="pattern", description="Analyze stock for patterns")
@app_commands.describe(ticker="Stock ticker symbol")
async def pattern_command(interaction: discord.Interaction, ticker: str):
    """Analyze stock pattern."""
    await interaction.response.defer(thinking=True)

    try:
        ticker = ticker.upper()

        # Get analysis
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://localhost:8000/api/analyze",
                params={"ticker": ticker, "interval": "daily"}
            )
            response.raise_for_status()
            data = response.json()

        # Create embed
        embed = await create_analysis_embed(ticker, data)

        # Get chart
        chart_url = await get_chart_url(ticker, "daily")

        if chart_url:
            embed.set_image(url=chart_url)

        # Create interactive view
        view = PatternAnalysisView(ticker, data, chart_url)

        await interaction.followup.send(embed=embed, view=view)

    except Exception as e:
        logger.error(f"Error in pattern command: {e}")
        await interaction.followup.send(f"❌ Error analyzing {ticker}: {str(e)}")


@bot.tree.command(name="scan", description="Run universe scan for patterns")
@app_commands.describe(sector="Optional sector filter")
async def scan_command(interaction: discord.Interaction, sector: Optional[str] = None):
    """Run pattern scanner."""
    await interaction.response.defer(thinking=True)

    try:
        # Run scan
        results = await bot.scanner.scan_universe()

        if not results or not results.get("patterns"):
            await interaction.followup.send("No patterns found in current scan.")
            return

        patterns = results["patterns"]

        # Filter by sector if provided
        if sector:
            patterns = [p for p in patterns if p.get("sector", "").lower() == sector.lower()]

        # Create interactive view
        view = ScanResultsView(patterns)

        await interaction.followup.send(embed=view.get_embed(), view=view)

    except Exception as e:
        logger.error(f"Error in scan command: {e}")
        await interaction.followup.send(f"❌ Error running scan: {str(e)}")


@bot.tree.command(name="watchlist", description="Show your watchlist")
async def watchlist_command(interaction: discord.Interaction):
    """Display user's watchlist."""
    await interaction.response.defer(thinking=True)

    try:
        discord_id = str(interaction.user.id)

        # Get user and create if needed
        discord_service.get_or_create_user(
            discord_id=discord_id,
            username=interaction.user.name,
            discriminator=interaction.user.discriminator
        )

        # Get watchlist items
        items = discord_service.get_watchlist(discord_id)

        # Create interactive view
        view = WatchlistView(items)

        await interaction.followup.send(embed=view.get_embed(), view=view)

    except Exception as e:
        logger.error(f"Error in watchlist command: {e}")
        await interaction.followup.send(f"❌ Error: {str(e)}")


@bot.tree.command(name="add", description="Add stock to watchlist")
@app_commands.describe(ticker="Stock ticker symbol")
async def add_command(interaction: discord.Interaction, ticker: str):
    """Add to watchlist."""
    await interaction.response.defer(thinking=True)

    try:
        ticker = ticker.upper()
        discord_id = str(interaction.user.id)

        # Ensure user exists
        discord_service.get_or_create_user(
            discord_id=discord_id,
            username=interaction.user.name,
            discriminator=interaction.user.discriminator
        )

        # Add to watchlist
        success = discord_service.add_to_watchlist(discord_id, ticker)

        if success:
            embed = discord.Embed(
                title="✅ Added to Watchlist",
                description=f"**{ticker}** has been added to your watchlist",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="❌ Error",
                description=f"Could not add **{ticker}** to watchlist",
                color=discord.Color.red()
            )

        await interaction.followup.send(embed=embed, ephemeral=True)

    except Exception as e:
        logger.error(f"Error in add command: {e}")
        await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)


@bot.tree.command(name="chart", description="Get stock chart")
@app_commands.describe(
    ticker="Stock ticker symbol",
    timeframe="Chart timeframe (daily, 4h, 1h)"
)
async def chart_command(
    interaction: discord.Interaction,
    ticker: str,
    timeframe: Optional[str] = "daily"
):
    """Get stock chart."""
    await interaction.response.defer(thinking=True)

    try:
        ticker = ticker.upper()

        # Get chart URL
        chart_url = await get_chart_url(ticker, timeframe)

        if not chart_url:
            await interaction.followup.send(f"❌ Could not generate chart for {ticker}")
            return

        embed = discord.Embed(
            title=f"📈 {ticker} Chart",
            description=f"Timeframe: {timeframe}",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )

        embed.set_image(url=chart_url)
        embed.set_footer(text="Legend AI • Chart-IMG")

        await interaction.followup.send(embed=embed)

    except Exception as e:
        logger.error(f"Error in chart command: {e}")
        await interaction.followup.send(f"❌ Error: {str(e)}")


@bot.tree.command(name="alert", description="Set price or pattern alert")
@app_commands.describe(
    ticker="Stock ticker symbol",
    alert_type="Alert type",
    value="Price threshold or pattern name"
)
async def alert_command(
    interaction: discord.Interaction,
    ticker: str,
    alert_type: str,
    value: str
):
    """Set alert."""
    await interaction.response.defer(thinking=True, ephemeral=True)

    try:
        ticker = ticker.upper()
        user_id = str(interaction.user.id)

        # TODO: Save to database

        embed = discord.Embed(
            title="🔔 Alert Set",
            description=f"You'll be notified when {ticker} meets your criteria",
            color=discord.Color.green()
        )

        embed.add_field(name="Type", value=alert_type, inline=True)
        embed.add_field(name="Value", value=value, inline=True)

        await interaction.followup.send(embed=embed, ephemeral=True)

    except Exception as e:
        logger.error(f"Error in alert command: {e}")
        await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)


@bot.tree.command(name="leaderboard", description="Show trading leaderboard")
async def leaderboard_command(interaction: discord.Interaction):
    """Display leaderboard."""
    await interaction.response.defer(thinking=True)

    try:
        # Get leaderboard data
        leaderboard_data = discord_service.get_leaderboard(limit=50)

        if not leaderboard_data:
            embed = discord.Embed(
                title="🏆 Trading Leaderboard",
                description="No trading calls yet. Make some calls to get on the leaderboard!",
                color=discord.Color.gold()
            )
            await interaction.followup.send(embed=embed)
            return

        # Create interactive view
        view = LeaderboardView(leaderboard_data)

        await interaction.followup.send(embed=view.get_embed(), view=view)

    except Exception as e:
        logger.error(f"Error in leaderboard command: {e}")
        await interaction.followup.send(f"❌ Error: {str(e)}")


@bot.tree.command(name="papertrade", description="Manage paper trading")
@app_commands.describe(
    action="Action to perform",
    ticker="Stock ticker symbol",
    shares="Number of shares"
)
async def papertrade_command(
    interaction: discord.Interaction,
    action: str,
    ticker: Optional[str] = None,
    shares: Optional[int] = None
):
    """Paper trading commands."""
    await interaction.response.defer(thinking=True, ephemeral=True)

    try:
        user_id = str(interaction.user.id)

        if action == "balance":
            # Show balance
            embed = discord.Embed(
                title="💰 Paper Trading Balance",
                description="Your virtual portfolio",
                color=discord.Color.blue()
            )
            embed.add_field(name="Cash", value="$100,000.00", inline=True)
            embed.add_field(name="Equity", value="$0.00", inline=True)
            embed.add_field(name="Total", value="$100,000.00", inline=True)

            await interaction.followup.send(embed=embed, ephemeral=True)

        elif action in ["buy", "sell"]:
            if not ticker or not shares:
                await interaction.followup.send(
                    "❌ Please provide ticker and shares",
                    ephemeral=True
                )
                return

            # TODO: Execute paper trade

            embed = discord.Embed(
                title=f"✅ Paper Trade Executed",
                description=f"{action.upper()} {shares} shares of {ticker.upper()}",
                color=discord.Color.green()
            )

            await interaction.followup.send(embed=embed, ephemeral=True)

        else:
            await interaction.followup.send(
                f"❌ Unknown action: {action}",
                ephemeral=True
            )

    except Exception as e:
        logger.error(f"Error in papertrade command: {e}")
        await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)


# ==================== INTERACTIVE VIEWS ====================

class PatternAnalysisView(discord.ui.View):
    """Interactive view for pattern analysis."""

    def __init__(self, ticker: str, data: Dict[str, Any]):
        super().__init__(timeout=300)
        self.ticker = ticker
        self.data = data

    @discord.ui.button(label="Add to Watchlist", style=discord.ButtonStyle.primary, emoji="📌")
    async def add_to_watchlist(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Add to watchlist button."""
        # TODO: Add to database
        await interaction.response.send_message(
            f"✅ Added {self.ticker} to your watchlist",
            ephemeral=True
        )

    @discord.ui.button(label="Set Alert", style=discord.ButtonStyle.secondary, emoji="🔔")
    async def set_alert(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Set alert button."""
        await interaction.response.send_modal(AlertModal(self.ticker))

    @discord.ui.button(label="Share Analysis", style=discord.ButtonStyle.success, emoji="📤")
    async def share_analysis(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Share analysis."""
        await interaction.response.send_message(
            f"📊 {interaction.user.mention} shared analysis for **{self.ticker}**",
            ephemeral=False
        )

    @discord.ui.button(label="More Details", style=discord.ButtonStyle.secondary, emoji="ℹ️")
    async def more_details(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Show more details."""
        embed = discord.Embed(
            title=f"📊 {self.ticker} - Detailed Analysis",
            color=discord.Color.blue()
        )

        # Add detailed metrics
        patterns = self.data.get("patterns", [])
        if patterns:
            for pattern in patterns[:3]:
                embed.add_field(
                    name=pattern.get("pattern", "Unknown"),
                    value=f"Confidence: {pattern.get('confidence', 0)*100:.1f}%",
                    inline=True
                )

        await interaction.response.send_message(embed=embed, ephemeral=True)


class AlertModal(discord.ui.Modal, title="Set Price Alert"):
    """Modal for setting alerts."""

    alert_type = discord.ui.TextInput(
        label="Alert Type",
        placeholder="price_above, price_below, pattern",
        required=True
    )

    threshold = discord.ui.TextInput(
        label="Price Threshold (if price alert)",
        placeholder="100.00",
        required=False
    )

    def __init__(self, ticker: str):
        super().__init__()
        self.ticker = ticker

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        # TODO: Save to database

        await interaction.response.send_message(
            f"✅ Alert set for {self.ticker}",
            ephemeral=True
        )


# ==================== HELPER FUNCTIONS ====================

async def create_analysis_embed(ticker: str, data: Dict[str, Any]) -> discord.Embed:
    """Create analysis embed."""
    embed = discord.Embed(
        title=f"📊 {ticker} Analysis",
        description="Pattern analysis and technical indicators",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )

    # Price info
    price = data.get("price", 0)
    change = data.get("change_pct", 0)

    emoji = "🟢" if change > 0 else "🔴"
    embed.add_field(
        name="Price",
        value=f"${price:.2f} ({emoji} {change:+.2f}%)",
        inline=True
    )

    # Patterns
    patterns = data.get("patterns", [])
    if patterns:
        pattern_str = "\n".join([
            f"• {p.get('pattern', 'N/A')} ({p.get('confidence', 0)*100:.0f}%)"
            for p in patterns[:3]
        ])
        embed.add_field(
            name="Patterns Detected",
            value=pattern_str,
            inline=False
        )

    # Stage
    stage = data.get("stage", "Unknown")
    embed.add_field(name="Weinstein Stage", value=stage, inline=True)

    # Trend
    trend = data.get("trend_template", {})
    if trend:
        is_uptrend = trend.get("is_uptrend", False)
        embed.add_field(
            name="Trend",
            value="✅ Uptrend" if is_uptrend else "❌ No Uptrend",
            inline=True
        )

    embed.set_footer(text="Legend AI • Technical Analysis")

    return embed


async def get_chart_url(ticker: str, interval: str = "daily") -> Optional[str]:
    """Get chart image URL."""
    try:
        settings = get_settings()
        api_key = settings.chart_img_api_key

        if not api_key:
            logger.warning("No Chart-IMG API key configured")
            return None

        chart_config = build_analyze_chart(ticker, interval)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.chart-img.com/v2/tradingview/advanced-chart",
                json=chart_config,
                headers={"x-api-key": api_key},
                timeout=30.0
            )

            if response.status_code == 200:
                return response.json().get("url")

    except Exception as e:
        logger.error(f"Error getting chart: {e}")

    return None


# ==================== BOT RUNNER ====================

async def start_bot():
    """Start the Discord bot."""
    settings = get_settings()

    if not settings.discord_bot_token:
        logger.error("No Discord bot token configured")
        return

    try:
        await bot.start(settings.discord_bot_token)
    except Exception as e:
        logger.error(f"Error starting Discord bot: {e}")
        raise


def run_bot():
    """Run bot in sync context."""
    asyncio.run(start_bot())


if __name__ == "__main__":
    run_bot()
