# 🚀 How to Use Legend AI Dashboard

## Quick Start

### Option 1: Web Dashboard (Recommended)

1. **Navigate to project directory:**
```bash
cd "/Users/kyleholthaus/Projects/Stock Legend AI/legend-ai-python"
```

2. **Start the dashboard:**
```bash
python dashboard_ultimate.py
```

3. **Open in browser:**
```
http://localhost:7860
```

### Option 2: API Endpoints

Access directly via: `https://legend-ai-python-production.up.railway.app`

**Interactive API Docs:** https://legend-ai-python-production.up.railway.app/docs

### Option 3: Telegram Bot

Send messages to your Telegram bot:
- `/start` - Welcome
- `/pattern NVDA` - Analyze NVDA
- `/chart TSLA` - Get chart
- `/scan` - Quick universe scan

---

## Dashboard Features

### 📊 Pattern Scanner Tab
- Enter any ticker (AAPL, NVDA, TSLA, etc.)
- Get instant pattern analysis
- See entry/stop/target levels
- View pattern score (1-10)

### 🌐 Universe Scanner Tab
- Scan S&P 500 + NASDAQ 100
- Find top setups automatically
- Ranked by pattern strength
- Updated daily

### 📋 Watchlist Tab
- Add tickers you're watching
- Track reasons and notes
- Monitor status
- Quick reference

### 💼 Trade Planner Tab
- Calculate position size
- Set entry and stop
- Determine shares to buy
- See risk/reward

### 📈 Market Internals Tab
- Current S&P 500 price
- VIX level
- Market regime
- Trading conditions

### 📊 Performance Tab
- Win rate tracking
- P&L analysis
- Best/worst trades
- Average R:R

---

## API Usage Examples

### Analyze Pattern
```bash
curl -X POST https://legend-ai-python-production.up.railway.app/api/patterns/detect \
  -H "Content-Type: application/json" \
  -d '{"ticker": "NVDA"}'
```

### Quick Universe Scan
```bash
curl -X POST https://legend-ai-python-production.up.railway.app/api/universe/scan/quick
```

### Add to Watchlist
```bash
curl -X POST https://legend-ai-python-production.up.railway.app/api/watchlist/add \
  -H "Content-Type: application/json" \
  -d '{"ticker": "TSLA", "reason": "VCP setup"}'
```

### Create Trade Plan
```bash
curl -X POST https://legend-ai-python-production.up.railway.app/api/trade/plan \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "NVDA",
    "entry": 145.50,
    "stop": 140.00,
    "account_size": 10000,
    "risk_percent": 2
  }'
```

---

## Tips & Best Practices

1. **Run universe scans during off-hours** - Results are cached for 24 hours
2. **Use quick scan** for fast insights on liquid stocks
3. **Add promising setups to watchlist** - Track them over time
4. **Create trade plans before entering** - Know your risk
5. **Log trades for performance tracking** - Improve your edge

---

## Troubleshooting

**Dashboard won't start?**
- Make sure FastAPI is running first: `uvicorn app.main:app --reload`
- Install requirements: `pip install -r requirements.txt`

**API errors?**
- Check health: `curl https://legend-ai-python-production.up.railway.app/health`
- View logs: `railway logs`

**Empty scan results?**
- Results are cached - may need fresh data
- Try `/api/universe/tickers` to see available stocks

---

## Demo Flow (Tomorrow)

1. **Open Dashboard** → Show professional UI
2. **Pattern Scanner** → Analyze NVDA (Cup & Handle 3.7/10)
3. **Universe Scanner** → Show top 10 setups from scan
4. **Add to Watchlist** → Add NVDA with reason
5. **Trade Planner** → Calculate position for $10K account
6. **Market Internals** → Show current regime
7. **Telegram Bot** → Send `/pattern TSLA` command

---

**You're ready to go! 🎉**

