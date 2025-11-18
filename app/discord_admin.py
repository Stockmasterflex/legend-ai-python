"""
Admin commands for Discord bot server configuration.
"""
import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional
import logging

from app.services.discord_service import discord_service

logger = logging.getLogger(__name__)


async def is_admin(interaction: discord.Interaction) -> bool:
    """Check if user has admin permissions."""
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "❌ You need administrator permissions to use this command.",
            ephemeral=True
        )
        return False
    return True


@app_commands.command(name="setup", description="[ADMIN] Configure bot for this server")
@app_commands.describe(
    market_updates_channel="Channel for daily market briefs",
    signals_channel="Channel for pattern alerts",
    daily_picks_channel="Channel for daily top picks"
)
async def setup_command(
    interaction: discord.Interaction,
    market_updates_channel: Optional[discord.TextChannel] = None,
    signals_channel: Optional[discord.TextChannel] = None,
    daily_picks_channel: Optional[discord.TextChannel] = None
):
    """Set up bot channels."""
    if not await is_admin(interaction):
        return

    await interaction.response.defer(thinking=True, ephemeral=True)

    try:
        guild_id = str(interaction.guild_id)

        config_updates = {
            "guild_name": interaction.guild.name,
        }

        if market_updates_channel:
            config_updates["channel_market_updates"] = str(market_updates_channel.id)

        if signals_channel:
            config_updates["channel_signals"] = str(signals_channel.id)

        if daily_picks_channel:
            config_updates["channel_daily_picks"] = str(daily_picks_channel.id)

        success = discord_service.update_server_config(guild_id, **config_updates)

        if success:
            embed = discord.Embed(
                title="✅ Server Configuration Updated",
                description="Bot channels have been configured",
                color=discord.Color.green()
            )

            if market_updates_channel:
                embed.add_field(
                    name="📊 Market Updates",
                    value=market_updates_channel.mention,
                    inline=False
                )

            if signals_channel:
                embed.add_field(
                    name="🔔 Signals",
                    value=signals_channel.mention,
                    inline=False
                )

            if daily_picks_channel:
                embed.add_field(
                    name="🎯 Daily Picks",
                    value=daily_picks_channel.mention,
                    inline=False
                )

            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.followup.send(
                "❌ Failed to update configuration",
                ephemeral=True
            )

    except Exception as e:
        logger.error(f"Error in setup command: {e}")
        await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)


@app_commands.command(name="configure", description="[ADMIN] Configure bot features")
@app_commands.describe(
    daily_brief="Enable daily market brief",
    pattern_alerts="Enable pattern alerts",
    top_picks="Enable top picks",
    brief_time="Time for daily brief (HH:MM UTC)",
    picks_time="Time for daily picks (HH:MM UTC)"
)
async def configure_command(
    interaction: discord.Interaction,
    daily_brief: Optional[bool] = None,
    pattern_alerts: Optional[bool] = None,
    top_picks: Optional[bool] = None,
    brief_time: Optional[str] = None,
    picks_time: Optional[str] = None
):
    """Configure bot features."""
    if not await is_admin(interaction):
        return

    await interaction.response.defer(thinking=True, ephemeral=True)

    try:
        guild_id = str(interaction.guild_id)

        config_updates = {}

        if daily_brief is not None:
            config_updates["enable_daily_brief"] = daily_brief

        if pattern_alerts is not None:
            config_updates["enable_pattern_alerts"] = pattern_alerts

        if top_picks is not None:
            config_updates["enable_top_picks"] = top_picks

        if brief_time:
            config_updates["daily_brief_time"] = brief_time

        if picks_time:
            config_updates["daily_picks_time"] = picks_time

        if not config_updates:
            await interaction.followup.send(
                "❌ No configuration options provided",
                ephemeral=True
            )
            return

        success = discord_service.update_server_config(guild_id, **config_updates)

        if success:
            embed = discord.Embed(
                title="✅ Features Configured",
                description="Bot features have been updated",
                color=discord.Color.green()
            )

            for key, value in config_updates.items():
                embed.add_field(
                    name=key.replace("_", " ").title(),
                    value=str(value),
                    inline=True
                )

            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.followup.send(
                "❌ Failed to update configuration",
                ephemeral=True
            )

    except Exception as e:
        logger.error(f"Error in configure command: {e}")
        await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)


@app_commands.command(name="status", description="[ADMIN] View bot configuration")
async def status_command(interaction: discord.Interaction):
    """View bot configuration."""
    if not await is_admin(interaction):
        return

    await interaction.response.defer(thinking=True, ephemeral=True)

    try:
        guild_id = str(interaction.guild_id)
        config = discord_service.get_server_config(guild_id)

        embed = discord.Embed(
            title="⚙️ Bot Configuration",
            description=f"Settings for {interaction.guild.name}",
            color=discord.Color.blue()
        )

        if not config:
            embed.description = "No configuration found. Use `/setup` to configure."
            await interaction.followup.send(embed=embed, ephemeral=True)
            return

        # Channels
        if config.get("channel_market_updates"):
            channel = interaction.guild.get_channel(int(config["channel_market_updates"]))
            embed.add_field(
                name="📊 Market Updates",
                value=channel.mention if channel else "Channel not found",
                inline=False
            )

        if config.get("channel_signals"):
            channel = interaction.guild.get_channel(int(config["channel_signals"]))
            embed.add_field(
                name="🔔 Signals",
                value=channel.mention if channel else "Channel not found",
                inline=False
            )

        if config.get("channel_daily_picks"):
            channel = interaction.guild.get_channel(int(config["channel_daily_picks"]))
            embed.add_field(
                name="🎯 Daily Picks",
                value=channel.mention if channel else "Channel not found",
                inline=False
            )

        # Features
        embed.add_field(
            name="Features",
            value=(
                f"Daily Brief: {'✅' if config.get('enable_daily_brief') else '❌'}\n"
                f"Pattern Alerts: {'✅' if config.get('enable_pattern_alerts') else '❌'}\n"
                f"Top Picks: {'✅' if config.get('enable_top_picks') else '❌'}"
            ),
            inline=False
        )

        # Times
        embed.add_field(
            name="Schedule",
            value=(
                f"Daily Brief: {config.get('daily_brief_time', 'Not set')} UTC\n"
                f"Daily Picks: {config.get('daily_picks_time', 'Not set')} UTC"
            ),
            inline=False
        )

        await interaction.followup.send(embed=embed, ephemeral=True)

    except Exception as e:
        logger.error(f"Error in status command: {e}")
        await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)


@app_commands.command(name="test_brief", description="[ADMIN] Send test market brief")
async def test_brief_command(interaction: discord.Interaction):
    """Send a test market brief."""
    if not await is_admin(interaction):
        return

    await interaction.response.defer(thinking=True)

    try:
        # Import here to avoid circular dependency
        from app.discord_tasks import DiscordTasksManager

        # Get bot from interaction
        bot = interaction.client

        # Create task manager temporarily
        task_manager = DiscordTasksManager(bot)

        # Generate and send brief
        embed = await task_manager._generate_market_brief()

        await interaction.followup.send(
            content="📊 **Test Market Brief**",
            embed=embed
        )

    except Exception as e:
        logger.error(f"Error in test_brief command: {e}")
        await interaction.followup.send(f"❌ Error: {str(e)}")


def setup_admin_commands(bot: commands.Bot):
    """Add admin commands to the bot."""
    bot.tree.add_command(setup_command)
    bot.tree.add_command(configure_command)
    bot.tree.add_command(status_command)
    bot.tree.add_command(test_brief_command)

    logger.info("Admin commands registered")
