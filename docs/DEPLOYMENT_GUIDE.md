# 🚀 Railway Deployment Guide

## Quick Fix for Current Deployment Failure

Your Railway deployment is failing on healthcheck. Here's how to fix it:

### Issue
```
Attempt #13 failed with service unavailable
1/1 replicas never became healthy!
```

### Root Cause
1. Healthcheck endpoint taking too long
2. Redis connection timeout
3. App not starting fast enough

### Solution

✅ **Already Fixed in Code:**
1. Added `/healthz` endpoint (super fast, always returns 200 OK)
2. Made Redis connection non-blocking (2-second timeout)
3. Redis failure now only marks service as "degraded", not "unhealthy"

---

## Railway Configuration

### Environment Variables (Set in Railway Dashboard)

**Required:**
```bash
# Core
SECRET_KEY=af10148245a5421e4df19595b6d530434ed6b4c1266636371814bad48a0b775d
DEBUG=false

# AI (OpenRouter - CHEAPER than OpenAI!)
OPENROUTER_API_KEY=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
AI_MODEL=anthropic/claude-3.5-sonnet

# Market Data
TWELVEDATA_API_KEY=14b61f5898d1412681a8dfc878f857b4
FINNHUB_API_KEY=cv9n4f1r01qpd9s87710cv9n4f1r01qpd9s877lg
ALPHA_VANTAGE_API_KEY=3WOG24BQLRKC7KOO

# Charts
CHART_IMG_API_KEY=tGvkXDWnfI5G8WX6VnsIJ3xLvnfLt56x6Q8UaNbU

# Telegram
TELEGRAM_BOT_TOKEN=8072569977:AAH6ajboc0Tl9LHUp1VUj3eQHy_XF6naGB4
TELEGRAM_CHAT_ID=7815143490
TELEGRAM_WEBHOOK_URL=https://legend-ai-python-production.up.railway.app

# Database (Railway provides this automatically)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Redis (use your Upstash URL)
REDIS_URL=redis://default:AXsPAAIncDI4MDVmZThlODU1YzU0YjJiYTBmNmU2MjdiNmIwZDA1YXAyMzE1MDM@pleasing-tahr-31503.upstash.io:6379

# Google Sheets (optional)
GOOGLE_SHEETS_ID=1g6vBpp3-d9C-fMYFz4P7BU_Vq5FNDd-VBzxDjw2kDLk

# N8N (optional)
N8N_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
N8N_API_URL=https://kylethomas.app.n8n.cloud
```

---

## Deployment Steps

### 1. Push Code to GitHub
```bash
git add -A
git commit -m "fix: Railway deployment with optimized healthcheck and OpenRouter AI"
git push origin claude/trading-platform-analysis-01Ur5MBEEUAk3JaPc7nEYhFj
```

### 2. Railway Will Auto-Deploy
- Railway detects the push
- Builds Docker image
- Deploys to production
- Runs healthcheck on `/healthz`

### 3. Verify Deployment
```bash
# Check health
curl https://legend-ai-python-production.up.railway.app/healthz

# Should return:
{"status": "ok"}

# Check detailed health
curl https://legend-ai-python-production.up.railway.app/health

# Should return full status with Redis, DB, etc.
```

### 4. Test API
```bash
# Test advanced pattern detection
curl -X POST "https://legend-ai-python-production.up.railway.app/api/advanced/patterns/detect" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "min_confidence": 70}'

# Test AI chat
curl -X POST "https://legend-ai-python-production.up.railway.app/api/ai/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Analyze TSLA", "symbol": "TSLA"}'
```

---

## Troubleshooting

### If Deployment Still Fails

#### 1. Check Railway Logs
```bash
# In Railway dashboard, click on your service
# Go to "Deployments" tab
# Click on failed deployment
# View logs
```

#### 2. Common Issues

**Issue: "service unavailable"**
```
Solution: Healthcheck timeout too short
Fix: railway.json now sets timeout to 100 seconds
```

**Issue: "Redis connection failed"**
```
Solution: Redis URL incorrect or Upstash down
Fix: App now continues without Redis (degraded mode)
Check: Verify REDIS_URL in Railway env vars
```

**Issue: "Database connection failed"**
```
Solution: DATABASE_URL not set
Fix: Railway should auto-provide this
Check: Make sure PostgreSQL plugin is added to your service
```

**Issue: "Module not found"**
```
Solution: Missing dependency
Fix: Verify requirements.txt has all dependencies
Run: pip install -r requirements.txt (locally to test)
```

#### 3. Manual Health Check Configuration

If Railway still uses wrong healthcheck path:

```bash
# In Railway dashboard
# Settings → Healthcheck
# Set path to: /healthz
# Set interval to: 10 seconds
# Set timeout to: 100 seconds
```

---

## Performance Optimization

### Railway Instance Size

**Current: Hobby Plan ($5/month)**
- 512MB RAM
- 0.5 vCPU
- Suitable for:
  - 100-1000 requests/day
  - Light AI usage
  - Development/testing

**If You Need More:**
```
Hobby ($5/mo)     → Pro ($20/mo)
512MB RAM         → 8GB RAM
0.5 vCPU         → 8 vCPU
Good for: 1k/day  → Good for: 100k/day
```

### Scaling Tips

**Horizontal Scaling (Multiple Instances):**
```bash
# railway.json
{
  "deploy": {
    "numReplicas": 2  # Run 2 instances
  }
}
```

**Vertical Scaling (Bigger Instance):**
```bash
# In Railway dashboard
# Settings → Resources
# Increase RAM/CPU
```

**Auto-Scaling:**
- Railway Pro plan supports auto-scaling
- Scales based on CPU/memory usage
- Costs scale with usage

---

## Monitoring

### Railway Dashboard
- **Metrics**: CPU, Memory, Network usage
- **Logs**: Real-time application logs
- **Deployments**: Build history and status

### Application Metrics
```bash
# Check health endpoint
curl https://your-app.railway.app/health

# Response includes:
{
  "status": "healthy",
  "redis": {"status": "connected", "latency_ms": 15},
  "telegram": "configured",
  "keys": {
    "chartimg": true,
    "twelvedata": true,
    "finnhub": true,
    "alpha_vantage": true
  },
  "universe": {"seeded": true, "cached_symbols": 500}
}
```

### Cost Monitoring
```bash
# Railway dashboard shows:
- Current month spend
- Projected month spend
- Resource usage graphs

# Set budget alerts:
- Settings → Billing
- Set monthly budget
- Get email alerts at 80%, 100%
```

---

## Rollback if Needed

### Quick Rollback
```bash
# In Railway dashboard
# Deployments tab
# Click on previous successful deployment
# Click "Redeploy"
```

### Git Rollback
```bash
# Revert to previous commit
git revert HEAD
git push

# Or reset to specific commit
git reset --hard <commit-hash>
git push --force
```

---

## Success Checklist

After deployment, verify:

- [ ] `/healthz` returns `{"status": "ok"}`
- [ ] `/health` shows detailed status
- [ ] `/docs` shows API documentation
- [ ] AI chat works (test via `/api/ai/chat`)
- [ ] Pattern detection works (test via `/api/advanced/patterns/detect`)
- [ ] Telegram webhook is set (check logs)
- [ ] Redis is connected (check `/health`)
- [ ] Database is connected (check `/health`)
- [ ] No errors in Railway logs
- [ ] Resource usage is normal (<50% CPU, <300MB RAM)

---

## Next Steps After Successful Deployment

1. **Test All Features**
   - Try AI chat
   - Detect patterns
   - Generate charts
   - Test Telegram bot

2. **Set Up Monitoring**
   - Configure Railway alerts
   - Set budget limits
   - Watch for errors

3. **Optimize Costs**
   - Review API usage
   - Tune cache TTLs
   - Monitor OpenRouter usage

4. **Add Custom Domain** (Optional)
   ```bash
   # Railway dashboard
   # Settings → Domains
   # Add: trading.yourdomain.com
   ```

5. **Enable SSL** (Automatic on Railway)
   - HTTPS enabled by default
   - Certificate auto-renewed

---

## Support

**Railway Issues:**
- Dashboard: https://railway.app
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway

**Legend AI Issues:**
- GitHub: Your repository
- Logs: `/health` endpoint
- Docs: `/docs` endpoint

---

**Your app should now deploy successfully!** 🎉

If you still have issues, check Railway logs and the `/health` endpoint for detailed diagnostics.
