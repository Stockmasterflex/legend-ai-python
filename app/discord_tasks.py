"""
Background tasks for Discord bot (alerts, scheduled posts, etc).
"""
import asyncio
import logging
from datetime import datetime, time
from typing import List, Dict, Any, Optional
import discord
from discord.ext import tasks

from app.services.discord_service import discord_service
from app.services.market_data import market_data_service
from app.services.scanner import ScannerService

logger = logging.getLogger(__name__)


class DiscordTasksManager:
    """Manages all Discord bot background tasks."""

    def __init__(self, bot):
        self.bot = bot
        self.scanner = ScannerService()

    def start_all_tasks(self):
        """Start all background tasks."""
        self.daily_market_brief.start()
        self.daily_top_picks.start()
        self.check_price_alerts.start()
        self.check_pattern_alerts.start()
        self.validate_trading_calls.start()

        logger.info("✅ All Discord background tasks started")

    def stop_all_tasks(self):
        """Stop all background tasks."""
        self.daily_market_brief.cancel()
        self.daily_top_picks.cancel()
        self.check_price_alerts.cancel()
        self.check_pattern_alerts.cancel()
        self.validate_trading_calls.cancel()

        logger.info("🛑 All Discord background tasks stopped")

    # ==================== DAILY MARKET BRIEF ====================

    @tasks.loop(time=time(hour=14, minute=0))  # 9 AM ET (14:00 UTC)
    async def daily_market_brief(self):
        """Post daily market brief to configured channels."""
        await self.bot.wait_until_ready()

        logger.info("📊 Generating daily market brief...")

        try:
            for guild in self.bot.guilds:
                guild_id = str(guild.id)
                config = discord_service.get_server_config(guild_id)

                if not config or not config.get("enable_daily_brief"):
                    continue

                channel_id = config.get("channel_market_updates")
                if not channel_id:
                    continue

                channel = guild.get_channel(int(channel_id))
                if not channel:
                    logger.warning(f"Channel {channel_id} not found in guild {guild.name}")
                    continue

                # Generate brief
                embed = await self._generate_market_brief()

                await channel.send(embed=embed)
                logger.info(f"✅ Sent market brief to {guild.name}")

        except Exception as e:
            logger.error(f"Error sending daily market brief: {e}", exc_info=True)

    async def _generate_market_brief(self) -> discord.Embed:
        """Generate comprehensive market brief."""
        embed = discord.Embed(
            title="📊 Daily Market Brief",
            description="Pre-market overview and key levels",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )

        # Major indices
        indices = {
            "SPY": "S&P 500",
            "QQQ": "Nasdaq 100",
            "IWM": "Russell 2000",
            "DIA": "Dow Jones"
        }

        for ticker, name in indices.items():
            try:
                data = await market_data_service.get_prices(ticker, interval="1d", limit=5)

                if data and "c" in data and len(data["c"]) >= 2:
                    close = data["c"][-1]
                    prev_close = data["c"][-2]
                    change = ((close - prev_close) / prev_close) * 100

                    emoji = "🟢" if change >= 0 else "🔴"

                    embed.add_field(
                        name=f"{emoji} {name}",
                        value=f"${close:.2f} ({change:+.2f}%)",
                        inline=True
                    )
            except Exception as e:
                logger.error(f"Error fetching {ticker}: {e}")

        # Add market internals if available
        try:
            # VIX
            vix_data = await market_data_service.get_prices("VIX", interval="1d", limit=2)
            if vix_data and "c" in vix_data:
                vix = vix_data["c"][-1]
                embed.add_field(
                    name="💨 Volatility (VIX)",
                    value=f"{vix:.2f}",
                    inline=True
                )
        except:
            pass

        embed.add_field(
            name="📅 Date",
            value=datetime.utcnow().strftime("%B %d, %Y"),
            inline=False
        )

        embed.set_footer(text="Legend AI • Market Data • Updates daily at 9 AM ET")

        return embed

    # ==================== DAILY TOP PICKS ====================

    @tasks.loop(time=time(hour=13, minute=30))  # 8:30 AM ET
    async def daily_top_picks(self):
        """Post top pattern setups of the day."""
        await self.bot.wait_until_ready()

        logger.info("🎯 Generating daily top picks...")

        try:
            # Run scanner
            results = await self.scanner.scan_universe()

            if not results or not results.get("patterns"):
                logger.info("No patterns found in scan")
                return

            patterns = results["patterns"]

            # Sort by confidence
            top_picks = sorted(
                patterns,
                key=lambda x: x.get("confidence", 0),
                reverse=True
            )[:5]

            # Send to all configured servers
            for guild in self.bot.guilds:
                guild_id = str(guild.id)
                config = discord_service.get_server_config(guild_id)

                if not config or not config.get("enable_top_picks"):
                    continue

                channel_id = config.get("channel_daily_picks")
                if not channel_id:
                    continue

                channel = guild.get_channel(int(channel_id))
                if not channel:
                    continue

                embed = self._create_top_picks_embed(top_picks)
                await channel.send(embed=embed)

                logger.info(f"✅ Sent top picks to {guild.name}")

        except Exception as e:
            logger.error(f"Error sending daily top picks: {e}", exc_info=True)

    def _create_top_picks_embed(self, picks: List[Dict[str, Any]]) -> discord.Embed:
        """Create embed for top daily picks."""
        embed = discord.Embed(
            title="🎯 Top Setups Today",
            description="Highest confidence pattern setups from overnight scan",
            color=discord.Color.gold(),
            timestamp=datetime.utcnow()
        )

        for i, pick in enumerate(picks, 1):
            ticker = pick.get("symbol", "N/A")
            pattern = pick.get("pattern", "N/A")
            confidence = pick.get("confidence", 0) * 100
            price = pick.get("price", 0)

            embed.add_field(
                name=f"{i}. **{ticker}** - {pattern}",
                value=f"Confidence: {confidence:.0f}% | Price: ${price:.2f}",
                inline=False
            )

        embed.set_footer(text=f"Legend AI • Scanned {len(picks)} stocks • Daily at 8:30 AM ET")

        return embed

    # ==================== PRICE ALERTS ====================

    @tasks.loop(minutes=5)
    async def check_price_alerts(self):
        """Check and trigger price alerts."""
        await self.bot.wait_until_ready()

        try:
            # Get all active alerts
            alerts = discord_service.get_active_alerts()

            for alert in alerts:
                if alert["alert_type"] not in ["price_above", "price_below"]:
                    continue

                ticker = alert["ticker"]
                threshold = alert["threshold"]

                # Get current price
                data = await market_data_service.get_prices(ticker, interval="1d", limit=1)

                if not data or "c" not in data:
                    continue

                current_price = data["c"][-1]

                # Check if alert triggered
                triggered = False

                if alert["alert_type"] == "price_above" and current_price >= threshold:
                    triggered = True
                elif alert["alert_type"] == "price_below" and current_price <= threshold:
                    triggered = True

                if triggered:
                    await self._send_alert_notification(alert, current_price)
                    discord_service.trigger_alert(alert["id"])

        except Exception as e:
            logger.error(f"Error checking price alerts: {e}", exc_info=True)

    async def _send_alert_notification(self, alert: Dict[str, Any], current_price: float):
        """Send alert notification to user."""
        try:
            discord_id = alert["discord_id"]
            user = await self.bot.fetch_user(int(discord_id))

            if not user:
                return

            embed = discord.Embed(
                title="🔔 Price Alert Triggered!",
                description=f"Your alert for **{alert['ticker']}** has been triggered",
                color=discord.Color.gold()
            )

            embed.add_field(
                name="Alert Type",
                value=alert["alert_type"].replace("_", " ").title(),
                inline=True
            )

            embed.add_field(
                name="Threshold",
                value=f"${alert['threshold']:.2f}",
                inline=True
            )

            embed.add_field(
                name="Current Price",
                value=f"${current_price:.2f}",
                inline=True
            )

            embed.set_footer(text="Legend AI • Price Alerts")

            await user.send(embed=embed)

        except Exception as e:
            logger.error(f"Error sending alert notification: {e}")

    # ==================== PATTERN ALERTS ====================

    @tasks.loop(hours=4)
    async def check_pattern_alerts(self):
        """Check for new patterns and send alerts."""
        await self.bot.wait_until_ready()

        try:
            # Get active pattern alerts
            alerts = discord_service.get_active_alerts()
            pattern_alerts = [a for a in alerts if a["alert_type"] == "pattern"]

            for alert in pattern_alerts:
                ticker = alert["ticker"]
                pattern_name = alert.get("pattern_name")

                # Run analysis
                # TODO: Implement pattern check
                # For now, skip
                pass

        except Exception as e:
            logger.error(f"Error checking pattern alerts: {e}", exc_info=True)

    # ==================== TRADING CALL VALIDATION ====================

    @tasks.loop(hours=24)
    async def validate_trading_calls(self):
        """Validate trading calls after time has passed."""
        await self.bot.wait_until_ready()

        # TODO: Implement call validation logic
        # - Check if target or stop was hit
        # - Update call record
        # - Update user stats
        # - Notify user

        pass
