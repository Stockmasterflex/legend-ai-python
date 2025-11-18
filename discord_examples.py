"""
Discord Bot Usage Examples
Run this to test Discord service functions independently
"""
from app.services.discord_service import discord_service
from app.config import get_settings

# Ensure database is configured
settings = get_settings()
if not settings.database_url:
    print("⚠️  DATABASE_URL not configured")
    print("Discord bot requires PostgreSQL for user data, watchlists, etc.")
    exit(1)


def example_user_creation():
    """Example: Create/get user"""
    user = discord_service.get_or_create_user(
        discord_id="123456789",
        username="TestUser",
        discriminator="1234"
    )
    print(f"✅ User created/retrieved: {user.username}")


def example_watchlist():
    """Example: Manage watchlist"""
    discord_id = "123456789"

    # Add to watchlist
    success = discord_service.add_to_watchlist(
        discord_id=discord_id,
        ticker="AAPL",
        pattern="VCP",
        entry_price=180.50,
        stop_loss=175.00,
        target=195.00,
        notes="Strong pattern after pullback"
    )
    print(f"✅ Added to watchlist: {success}")

    # Get watchlist
    items = discord_service.get_watchlist(discord_id)
    print(f"📋 Watchlist items: {len(items)}")
    for item in items:
        print(f"   - {item['ticker']}: {item['pattern']}")

    # Remove from watchlist
    success = discord_service.remove_from_watchlist(discord_id, "AAPL")
    print(f"✅ Removed from watchlist: {success}")


def example_alerts():
    """Example: Create alerts"""
    discord_id = "123456789"

    # Price alert
    success = discord_service.create_alert(
        discord_id=discord_id,
        ticker="TSLA",
        alert_type="price_above",
        threshold=250.00
    )
    print(f"🔔 Price alert created: {success}")

    # Pattern alert
    success = discord_service.create_alert(
        discord_id=discord_id,
        ticker="NVDA",
        alert_type="pattern",
        pattern_name="Cup & Handle"
    )
    print(f"🔔 Pattern alert created: {success}")

    # Get active alerts
    alerts = discord_service.get_active_alerts()
    print(f"📢 Active alerts: {len(alerts)}")


def example_paper_trading():
    """Example: Paper trading"""
    discord_id = "123456789"

    # Open trade
    trade_id = discord_service.create_paper_trade(
        discord_id=discord_id,
        ticker="SPY",
        side="long",
        entry_price=450.00,
        shares=10
    )
    print(f"💰 Paper trade opened: ID {trade_id}")

    # Get open trades
    trades = discord_service.get_open_trades(discord_id)
    print(f"📊 Open trades: {len(trades)}")

    # Close trade
    if trade_id:
        result = discord_service.close_paper_trade(trade_id, exit_price=455.00)
        if result:
            print(f"✅ Trade closed: P&L ${result['pnl']:.2f} ({result['pnl_pct']:.2f}%)")


def example_trading_calls():
    """Example: Trading calls for leaderboard"""
    discord_id = "123456789"

    # Create call
    call_id = discord_service.create_trading_call(
        discord_id=discord_id,
        ticker="AAPL",
        call_type="bullish",
        entry_price=180.00,
        target_price=195.00,
        stop_loss=175.00,
        reasoning="Strong VCP pattern with high RS"
    )
    print(f"📈 Trading call created: ID {call_id}")

    # Validate call (after time passes)
    if call_id:
        success = discord_service.validate_trading_call(
            call_id=call_id,
            was_correct=True,
            actual_move_pct=8.3
        )
        print(f"✅ Call validated: {success}")


def example_leaderboard():
    """Example: Get leaderboard"""
    leaderboard = discord_service.get_leaderboard(limit=10)

    print(f"\n🏆 LEADERBOARD")
    print("=" * 50)

    for entry in leaderboard:
        print(
            f"{entry['rank']:2d}. {entry['username']:20s} "
            f"| Accuracy: {entry['accuracy']:5.1f}% "
            f"({entry['correct_calls']}/{entry['total_calls']})"
        )


def example_server_config():
    """Example: Server configuration"""
    guild_id = "987654321"

    # Update config
    success = discord_service.update_server_config(
        guild_id=guild_id,
        guild_name="Test Server",
        channel_market_updates="123456789",
        channel_signals="123456790",
        channel_daily_picks="123456791",
        enable_daily_brief=True,
        enable_pattern_alerts=True,
        enable_top_picks=True,
        daily_brief_time="09:00",
        daily_picks_time="08:30"
    )
    print(f"⚙️  Server config updated: {success}")

    # Get config
    config = discord_service.get_server_config(guild_id)
    if config:
        print(f"📋 Server config retrieved")
        print(f"   - Daily Brief: {config['enable_daily_brief']} at {config['daily_brief_time']}")
        print(f"   - Pattern Alerts: {config['enable_pattern_alerts']}")
        print(f"   - Top Picks: {config['enable_top_picks']} at {config['daily_picks_time']}")


if __name__ == "__main__":
    print("🤖 Discord Bot Service Examples")
    print("=" * 50)

    try:
        print("\n1. User Creation")
        example_user_creation()

        print("\n2. Watchlist Management")
        example_watchlist()

        print("\n3. Alerts")
        example_alerts()

        print("\n4. Paper Trading")
        example_paper_trading()

        print("\n5. Trading Calls")
        example_trading_calls()

        print("\n6. Leaderboard")
        example_leaderboard()

        print("\n7. Server Configuration")
        example_server_config()

        print("\n✅ All examples completed!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure DATABASE_URL is configured in .env")
