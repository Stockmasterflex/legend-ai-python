# Legend AI - Deployment Guide

## Quick Start (Railway)

### 1. Fork & Connect Repository
```bash
# Railway will automatically detect this as a Python/FastAPI app
# Railway will use: python3 -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 2. Add PostgreSQL Plugin
- In Railway dashboard, click "Add Plugin"
- Select "PostgreSQL"
- Railway will automatically set DATABASE_URL

### 3. Add Redis Plugin
- Click "Add Plugin"
- Select "Redis"
- Railway will automatically set REDIS_URL

### 4. Configure Environment Variables
Copy variables from `.env.production.template` and set in Railway:

**Required Variables:**
```
ENVIRONMENT=production
TWELVEDATA_API_KEY=<get from twelvedata.com>
FINNHUB_API_KEY=<get from finnhub.io>
ALPHA_VANTAGE_API_KEY=<get from alphavantage.co>
CHART_IMG_API_KEY=<get from chart-img.com>
OPENROUTER_API_KEY=<get from openrouter.ai>
LOG_LEVEL=INFO
DEBUG=false
ALLOWED_ORIGINS=https://yourdomain.com
```

**Optional:**
```
TELEGRAM_BOT_TOKEN=<your-bot-token>
```

### 5. Deploy
```bash
git push origin integration/ai-features
# Railway will auto-deploy
```

### 6. Verify Deployment
```bash
curl https://your-app.up.railway.app/health
# Should return: {"status": "healthy", ...}

curl https://your-app.up.railway.app/api/universe/tickers
# Should return: {"success": true, "total": 518, ...}
```

---

## Manual Deployment (Docker)

### Build Image
```bash
docker build -t legend-ai:latest .
```

### Run Container
```bash
docker run -d \
  --name legend-ai \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  -e REDIS_URL="redis://..." \
  -e TWELVEDATA_API_KEY="..." \
  -e FINNHUB_API_KEY="..." \
  -e ALPHA_VANTAGE_API_KEY="..." \
  -e CHART_IMG_API_KEY="..." \
  -e OPENROUTER_API_KEY="..." \
  -e ENVIRONMENT="production" \
  legend-ai:latest
```

---

## Local Development

### 1. Setup
```bash
# Clone repository
git clone https://github.com/Stockmasterflex/legend-ai-python.git
cd legend-ai-python

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy template
cp .env.production.template .env

# Edit .env with your API keys
nano .env
```

### 3. Run Application
```bash
# Start Redis (if testing locally)
redis-server --daemonize yes

# Start application
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access Dashboard
```
http://localhost:8000/dashboard
http://localhost:8000/docs  # API documentation
```

---

## Post-Deployment Checklist

### ✅ Verify Services
- [ ] `/health` endpoint returns "healthy" (not "degraded")
- [ ] `/api/universe/tickers` returns 518 symbols
- [ ] `/api/universe/seed` successfully seeds universe
- [ ] `/dashboard` loads correctly
- [ ] Pattern detection works with real ticker

### ✅ Test Pattern Detection
```bash
curl -X POST https://your-app.railway.app/api/patterns/detect \
  -H "Content-Type: application/json" \
  -d '{"ticker": "NVDA", "interval": "1day"}'
```

### ✅ Verify API Usage
```bash
curl https://your-app.railway.app/api/usage
# Should show API call counts
```

### ✅ Monitor Logs
```bash
# Railway Dashboard -> Logs
# Watch for errors during startup
```

---

## Troubleshooting

### Health Check Shows "degraded"
**Symptoms:**
```json
{"status": "degraded", "issues": ["Telegram bot not configured"]}
```

**Causes:**
1. Missing API keys → Add all required keys
2. Redis not connected → Verify REDIS_URL
3. Database not accessible → Check DATABASE_URL
4. Telegram not configured → Optional, can ignore

**Fix:**
```bash
# Check environment variables are set
railway vars

# Verify PostgreSQL plugin is attached
railway plugins

# Check Redis connection in logs
railway logs
```

### Pattern Detection Returns "No data available"
**Cause:** API keys not working or rate limit exceeded

**Fix:**
```bash
# Test API keys directly
curl "https://api.twelvedata.com/time_series?symbol=AAPL&interval=1day&apikey=YOUR_KEY"

# Check API usage
curl https://your-app.railway.app/api/usage
```

### Universe Not Seeding
**Symptoms:** `/api/universe/tickers` returns 0 symbols

**Fix:**
```bash
# Manually trigger seed
curl -X POST https://your-app.railway.app/api/universe/seed

# Check logs for errors
railway logs | grep "universe"
```

### Out of API Calls
**Symptoms:** All market data requests fail with 429 errors

**Solution:**
- Check usage: `GET /api/usage`
- Wait for daily reset (midnight UTC)
- Upgrade API plan
- Enable Redis caching to reduce calls

---

## Performance Tips

### 1. Enable Redis Caching
Redis dramatically reduces API calls:
```
Without Redis: ~100-200 API calls/day for active users
With Redis: ~10-20 API calls/day for active users
```

### 2. Cache Warming
On startup, app warms cache with popular tickers (SPY, QQQ, etc.)
- Reduces initial load time
- Prevents API rate limit issues

### 3. API Rate Limits
Monitor usage to stay within free tier limits:
```bash
curl https://your-app.railway.app/api/usage
```

**Daily Limits (Free Tier):**
- TwelveData: 800 calls/day
- Finnhub: 60 calls/minute
- Alpha Vantage: 500 calls/day
- Chart-IMG: Depends on plan

---

## Security Best Practices

### 1. Never Commit API Keys
```bash
# Always use environment variables
# Add to .gitignore:
.env
.env.local
.env.production
```

### 2. Use HTTPS Only
```bash
# In production, enforce HTTPS
ALLOWED_ORIGINS=https://yourdomain.com
```

### 3. Rate Limiting
Built-in rate limiting:
- 60 requests/minute per IP
- Configure in `app/middleware/rate_limit.py`

### 4. CORS Configuration
```bash
# Restrict to your domains only
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

---

## Monitoring & Alerts

### Setup Telegram Alerts
```bash
1. Talk to @BotFather on Telegram
2. Create new bot: /newbot
3. Copy token
4. Set in Railway: TELEGRAM_BOT_TOKEN=<token>
5. Restart app
```

### Health Monitoring
```bash
# Set up external monitoring (UptimeRobot, etc.)
# Ping: https://your-app.railway.app/health every 5 minutes
```

### Error Tracking (Optional)
```bash
# Add Sentry for error tracking
pip install sentry-sdk
# Configure in app/main.py
```

---

## Scaling

### Horizontal Scaling
Railway supports automatic scaling:
```bash
# In Railway dashboard:
Settings -> Replicas -> Auto-scale
```

### Database Connection Pooling
Already configured in `app/services/database.py`:
```python
pool_size=10
max_overflow=20
```

### Redis Connection Pooling
Built into redis-py client

---

## Backup & Disaster Recovery

### Database Backups
```bash
# Railway PostgreSQL automatic backups
# Manual backup:
railway run pg_dump $DATABASE_URL > backup.sql
```

### Environment Variables Backup
```bash
# Export from Railway
railway vars > railway-env-backup.txt
# Keep this file secure!
```

---

## Support

### Documentation
- API Docs: `https://your-app.railway.app/docs`
- Redoc: `https://your-app.railway.app/redoc`
- Error Codes: `https://your-app.railway.app/api/docs/errors`

### Logs
```bash
# Railway
railway logs --tail 100

# Local
tail -f app.log
```

### Issues
Report issues: https://github.com/Stockmasterflex/legend-ai-python/issues

---

**Last Updated**: 2025-11-19  
**Version**: 1.0.0  
**Build**: 76bfbd9
