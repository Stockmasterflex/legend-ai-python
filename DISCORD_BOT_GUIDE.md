# Discord Stock Bot - Complete Guide

## 🤖 Overview

Full-featured Discord bot for stock analysis, pattern detection, and trading community features. Built on top of the Legend AI platform.

## ✨ Features

### 1. Bot Commands

#### Stock Analysis
- `/pattern <ticker>` - Comprehensive pattern analysis with interactive buttons
- `/chart <ticker> [timeframe]` - Get stock charts (daily, 4h, 1h)
- `/scan [sector]` - Run universe pattern scan with filtering
- `/watchlist` - View your personal watchlist with pagination
- `/add <ticker>` - Add stock to your watchlist
- `/alert <ticker> <type> <value>` - Set price or pattern alerts

#### Community Features
- `/leaderboard` - View top traders by accuracy
- `/papertrade <action> [ticker] [shares]` - Paper trading commands

#### Admin Commands (Requires Administrator)
- `/setup` - Configure bot channels
- `/configure` - Enable/disable features and set schedules
- `/status` - View current bot configuration
- `/test_brief` - Send test market brief

### 2. Server Features

#### Automated Posting
- **Daily Market Brief** - Pre-market overview of major indices (9 AM ET)
- **Daily Top Picks** - Top 5 pattern setups from overnight scan (8:30 AM ET)
- **Pattern Alerts** - Real-time pattern detection alerts
- **Price Alerts** - User-specific price alerts (checked every 5 minutes)

#### Channels
Configure these channels for automated posts:
- `#market-updates` - Daily briefs and market news
- `#signals` - Pattern alerts and signals
- `#daily-picks` - Top setups

### 3. Interactive Embeds

All commands use rich embeds with:
- **Charts** - Integrated Chart-IMG charts
- **Action Buttons** - Quick actions (add to watchlist, set alerts, share)
- **Pagination** - Navigate through long lists
- **Filters** - Filter scan results by pattern type
- **Modals** - User-friendly forms for alerts and calls

### 4. Community Features

#### Leaderboard
- Track trading call accuracy
- Rank users by correct calls
- Historical performance tracking

#### Paper Trading
- Virtual $100,000 starting balance
- Track P&L and performance
- Compete with other traders

#### Shared Watchlists
- Create public watchlists
- Follow other traders
- Collaborative analysis

#### Trading Calls
- Make public bullish/bearish calls
- Track accuracy for leaderboard
- Include reasoning and targets

## 🚀 Setup

### 1. Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and create a bot
4. Copy the bot token
5. Enable these Privileged Gateway Intents:
   - Server Members Intent
   - Message Content Intent

### 3. Invite Bot to Server

Use this URL (replace `YOUR_CLIENT_ID`):
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=277025770496&scope=bot%20applications.commands
```

Required Permissions:
- Read Messages/View Channels
- Send Messages
- Embed Links
- Attach Files
- Read Message History
- Use Slash Commands
- Mention Everyone (optional, for alerts)

### 4. Environment Configuration

Add to your `.env` file:

```env
# Discord Bot
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_GUILD_ID=your_server_id  # Optional, for single-server bots
DISCORD_CHANNEL_MARKET_UPDATES=channel_id  # Optional
DISCORD_CHANNEL_SIGNALS=channel_id  # Optional
DISCORD_CHANNEL_DAILY_PICKS=channel_id  # Optional

# Existing Legend AI config
CHARTIMG_API_KEY=your_key
TWELVEDATA_API_KEY=your_key
DATABASE_URL=postgresql://...  # Required for Discord features
```

### 5. Database Setup

The Discord bot requires a PostgreSQL database for:
- User profiles and stats
- Watchlists
- Alerts
- Paper trades
- Trading calls
- Server configuration

Tables will be auto-created on first run.

### 6. Run the Bot

#### Option 1: Standalone Bot
```bash
python run_discord_bot.py
```

#### Option 2: Alongside FastAPI
```python
# In your main.py or startup script
from app.discord_bot import start_bot
import asyncio

# Start in background
asyncio.create_task(start_bot())
```

#### Option 3: Separate Process (Production)
```bash
# Terminal 1: FastAPI
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Discord Bot
python run_discord_bot.py
```

## 📖 Usage Guide

### For Server Admins

#### Initial Setup
1. Invite bot to your server
2. Create channels: `#market-updates`, `#signals`, `#daily-picks`
3. Run `/setup` command:
   ```
   /setup market_updates_channel:#market-updates signals_channel:#signals daily_picks_channel:#daily-picks
   ```
4. Configure features with `/configure`:
   ```
   /configure daily_brief:true pattern_alerts:true top_picks:true
   ```
5. Check status with `/status`

#### Test Configuration
- Use `/test_brief` to send a test market brief
- Verify channels are receiving posts

### For Users

#### Getting Started
1. Use `/watchlist` to see your empty watchlist
2. Add stocks with `/add AAPL` or `/add TSLA`
3. Analyze patterns with `/pattern AAPL`
4. Set alerts with `/alert AAPL price_above 200`

#### Making Trading Calls
1. Run `/pattern TICKER` to analyze
2. Click "Make Call" button
3. Fill in the modal with your analysis
4. Call is posted publicly and tracked for leaderboard

#### Paper Trading
1. Check balance: `/papertrade balance`
2. Buy stocks: Click "Paper Trade" on any analysis
3. Track positions in your profile

#### Viewing Leaderboard
- `/leaderboard` - See top traders
- Rankings based on call accuracy
- Minimum calls required for ranking

## 🎨 Interactive Features

### Pattern Analysis View
When you run `/pattern TICKER`, you get interactive buttons:
- **📌 Add to Watchlist** - Quick add
- **🔔 Set Alert** - Opens alert modal
- **📈 Make Call** - Make public trading call
- **💰 Paper Trade** - Quick paper trade
- **📤 Share** - Share analysis with channel

### Scan Results View
After `/scan`, you can:
- Filter by pattern type (dropdown)
- Add all results to watchlist
- Navigate through results

### Watchlist View
Your `/watchlist` includes:
- ◀️ ▶️ Pagination
- 🗑️ Remove stocks
- 🔄 Refresh

## 🔧 Configuration

### Scheduled Tasks

Edit times in `discord_tasks.py`:

```python
@tasks.loop(time=time(hour=14, minute=0))  # 9 AM ET = 14:00 UTC
async def daily_market_brief(self):
    # ...

@tasks.loop(time=time(hour=13, minute=30))  # 8:30 AM ET
async def daily_top_picks(self):
    # ...
```

### Alert Check Intervals

```python
@tasks.loop(minutes=5)  # Price alerts every 5 minutes
async def check_price_alerts(self):
    # ...
```

### Customization

**Embed Colors:**
- Blue: Info/Analysis
- Green: Success/Buy signals
- Red: Errors/Sell signals
- Gold: Leaderboard/Top picks

**Response Styles:**
- Ephemeral: Private messages (watchlist management)
- Public: Shared analysis and calls

## 📊 Database Schema

### Key Tables

**discord_users**
- User profiles and stats
- Paper trading balance
- Call accuracy tracking

**discord_watchlist**
- User watchlists
- Entry prices and targets
- Pattern context

**discord_alerts**
- Price and pattern alerts
- Trigger tracking

**discord_paper_trades**
- Open and closed positions
- P&L tracking

**discord_trading_calls**
- Public calls
- Validation and accuracy

**discord_server_config**
- Per-server configuration
- Channel mappings
- Feature flags

## 🚨 Troubleshooting

### Bot Not Responding
1. Check bot is online (green dot in Discord)
2. Verify bot has proper permissions
3. Check logs: `tail -f discord_bot.log`
4. Ensure slash commands are synced (happens on startup)

### Slash Commands Not Showing
1. Wait 5-10 minutes after bot joins server
2. Try restarting Discord client
3. Check bot has `applications.commands` scope

### Database Errors
1. Verify `DATABASE_URL` is set correctly
2. Check PostgreSQL is running
3. Ensure database exists
4. Tables auto-create on first run

### Missing Market Data
1. Verify API keys are set (`TWELVEDATA_API_KEY`, etc.)
2. Check API rate limits
3. Review logs for specific errors

### Charts Not Showing
1. Verify `CHARTIMG_API_KEY` is set
2. Check Chart-IMG service status
3. Ensure bot has embed permissions

## 🔐 Security

### Permissions
- Admin commands check `administrator` permission
- User data is per-user (can't access others' watchlists)
- Trading calls are public by design

### Rate Limiting
- Discord has built-in rate limits
- Bot respects Discord API limits
- Consider implementing additional rate limiting for heavy users

### Data Privacy
- User IDs are stored as Discord IDs
- No personal information stored
- Paper trades are virtual only

## 📈 Performance

### Optimization Tips
1. Use database indexing (already configured)
2. Cache frequent queries
3. Limit scan results (top 50)
4. Paginate long lists

### Scaling
- Bot handles multiple servers simultaneously
- Each server has independent configuration
- Database connection pooling enabled
- Background tasks run once per bot instance

## 🤝 Integration with Legend AI

The Discord bot integrates with:
- **Pattern Detection** - Uses `scanner.py` and detector system
- **Market Data** - `market_data_service` for prices
- **Charts** - Chart-IMG API via `chartimg.py`
- **Analysis** - Full analysis endpoint at `/api/analyze`

All bot commands leverage existing Legend AI infrastructure!

## 📝 Future Enhancements

Planned features:
- [ ] Webhook integration for external alerts
- [ ] Multi-timeframe analysis in embeds
- [ ] Backtesting integration
- [ ] AI-powered trade ideas
- [ ] Competition mode with prizes
- [ ] Advanced filtering options
- [ ] Portfolio tracking
- [ ] Risk management tools

## 🆘 Support

For issues:
1. Check logs: `discord_bot.log`
2. Review configuration: `/status` command
3. Test with `/test_brief`
4. Check Legend AI API is running

## 📚 References

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/docs)
- [Legend AI Documentation](./README.md)
- [Chart-IMG API](./CHART_IMG_API.md)

---

**Built with ❤️ using Legend AI Platform**
