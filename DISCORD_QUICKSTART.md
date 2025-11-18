# Discord Bot - Quick Start Guide

Get your Discord stock bot running in 5 minutes!

## ⚡ Quick Setup

### 1. Create Discord Bot (2 minutes)

1. Go to https://discord.com/developers/applications
2. Click "New Application" → Name it "Stock Bot"
3. Go to "Bot" tab → Click "Add Bot"
4. Copy your bot token (keep it secret!)
5. Enable these under "Privileged Gateway Intents":
   - ✅ Server Members Intent
   - ✅ Message Content Intent

### 2. Invite Bot to Your Server (1 minute)

Replace `YOUR_CLIENT_ID` with your Application ID (from "General Information" tab):

```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=277025770496&scope=bot%20applications.commands
```

### 3. Configure Environment (1 minute)

Add to your `.env` file:

```env
# Required
DISCORD_BOT_TOKEN=your_bot_token_here
DATABASE_URL=postgresql://...  # Required for Discord features

# Recommended (for full features)
CHARTIMG_API_KEY=your_key
TWELVEDATA_API_KEY=your_key
```

### 4. Run the Bot (1 minute)

```bash
# Install dependencies (if not done)
pip install discord.py

# Run standalone
python run_discord_bot.py
```

That's it! 🎉

## 🎯 First Commands

### As Admin

1. Create these channels in your Discord:
   - `#market-updates`
   - `#signals`
   - `#daily-picks`

2. Run setup command:
   ```
   /setup market_updates_channel:#market-updates signals_channel:#signals daily_picks_channel:#daily-picks
   ```

3. Enable features:
   ```
   /configure daily_brief:true pattern_alerts:true top_picks:true
   ```

4. Test it:
   ```
   /test_brief
   ```

### As User

```
/pattern AAPL          # Analyze Apple
/scan                  # Scan for patterns
/watchlist             # View your watchlist
/add TSLA              # Add Tesla to watchlist
/chart SPY             # Get SPY chart
/leaderboard           # See top traders
```

## 📊 What You Get

### Automated Daily Posts
- 🌅 **8:30 AM ET** - Top 5 pattern setups
- 📈 **9:00 AM ET** - Market brief (SPY, QQQ, IWM, DIA)

### Interactive Commands
- Pattern analysis with charts
- Watchlist management
- Price alerts
- Paper trading
- Leaderboard

### Community Features
- Trading calls tracking
- Accuracy leaderboard
- Shared watchlists
- Paper trading competitions

## 🔧 Troubleshooting

### Bot shows offline?
```bash
# Check logs
tail -f discord_bot.log

# Verify token is correct in .env
```

### Commands not showing?
- Wait 5-10 minutes after inviting bot
- Try restarting Discord
- Check bot has proper permissions

### Database errors?
```bash
# Ensure PostgreSQL is running
# Tables auto-create on first run
```

### Need help?
See full guide: [DISCORD_BOT_GUIDE.md](./DISCORD_BOT_GUIDE.md)

## 🚀 Production Deployment

### Option 1: Railway

```bash
# Already running FastAPI on Railway?
# Just add Discord bot token to environment variables
# Bot runs in background automatically
```

### Option 2: Separate Process

```bash
# Terminal 1: API
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Discord Bot
python run_discord_bot.py
```

### Option 3: Docker

```dockerfile
# Add to your Dockerfile
CMD python run_discord_bot.py & uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 Next Steps

1. ✅ Complete initial setup
2. 📖 Read full guide: [DISCORD_BOT_GUIDE.md](./DISCORD_BOT_GUIDE.md)
3. 🎨 Customize embed colors and messages
4. 📊 Configure alert intervals
5. 🏆 Enable paper trading competitions

---

**Questions?** Check the full documentation or open an issue!
