# 💰 Cost Optimization Guide

## Goal: Keep Legend AI Running at Minimal Cost

This guide shows you how to minimize costs while maximizing performance.

---

## 📊 Cost Breakdown

### Current Setup (Optimized)

| Service | Provider | Cost | Strategy |
|---------|----------|------|----------|
| **AI** | OpenRouter (Claude 3.5) | **~$3-5/month** | Use Claude instead of GPT-4 |
| **Market Data** | TwelveData + Finnhub + Alpha Vantage | **FREE** | Free tiers + fallback |
| **Charts** | Chart-img.com PRO | **$X/month** | You're paying for this |
| **Database** | Railway PostgreSQL | **$5/month** | Small instance |
| **Redis** | Upstash | **FREE** | 10k commands/day free |
| **Hosting** | Railway | **$5/month** | Starter plan |
| **N8N** | n8n.cloud | **$0-20/month** | Depends on usage |
| **TOTAL** | | **~$13-35/month** | Extremely affordable! |

### Without Optimization

| Service | Cost | Why Expensive |
|---------|------|---------------|
| GPT-4 Direct | **$50-200/month** | 10x more expensive than OpenRouter |
| Premium Data | **$50-500/month** | Real-time professional data |
| Hosted Database | **$25-100/month** | Managed PostgreSQL |
| **TOTAL (Bad)** | **$125-800/month** | 😱 TOO EXPENSIVE! |

---

## 🎯 Optimization Strategies

### 1. AI Costs (BIGGEST Savings!)

#### ✅ Use OpenRouter (Current Setup)
```bash
# .env
OPENROUTER_API_KEY=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
AI_MODEL=anthropic/claude-3.5-sonnet  # ~$3/1M tokens
```

**Cost Comparison:**
- **Direct OpenAI GPT-4:** $30 per 1M tokens (input) + $60 per 1M tokens (output) = **~$45 per 1M tokens**
- **OpenRouter Claude 3.5:** $3 per 1M tokens (input) + $15 per 1M tokens (output) = **~$9 per 1M tokens**
- **Savings: 5x cheaper!** 🎉

**Even Cheaper Options:**
```bash
# Gemini Pro (best price/performance)
AI_MODEL=google/gemini-pro-1.5  # ~$1.25/1M tokens

# GPT-3.5 Turbo (fast & cheap for simple queries)
AI_MODEL=openai/gpt-3.5-turbo  # ~$0.50/1M tokens
```

#### Usage Estimates:
- **Heavy usage:** 10 AI requests/day × 1000 tokens/request = 300k tokens/month
  - Claude 3.5: **$2.70/month** ✅
  - GPT-4: **$13.50/month** ❌

- **Moderate usage:** 3 AI requests/day × 1000 tokens/request = 90k tokens/month
  - Claude 3.5: **$0.81/month** ✅
  - GPT-4: **$4.05/month** ❌

#### Rate Limiting (Prevent Runaway Costs)
```bash
# .env
AI_RATE_LIMIT_PER_MINUTE=20  # Max 20 AI requests/minute
```

**Protects you from:**
- Accidental infinite loops
- Bot spam
- Malicious users
- Budget overruns

#### Response Caching
```bash
# .env
CACHE_TTL_AI_RESPONSES=1800  # Cache for 30 minutes
```

**Savings:**
- Same question within 30 min = **$0 cost** (cached!)
- Reduces API calls by **50-70%**

---

### 2. Market Data Costs (FREE with Smart Fallback)

#### Multi-Source Fallback Strategy

```bash
# .env
DATA_SOURCE_PRIORITY=twelvedata,finnhub,alphavantage
```

**How it works:**
1. Try **TwelveData** first (500 calls/day FREE)
2. If rate limited → try **Finnhub** (60 calls/min FREE)
3. If rate limited → try **Alpha Vantage** (500 calls/day FREE)
4. Cache everything!

**Daily Limits:**
| Source | Free Tier | Our Strategy |
|--------|-----------|--------------|
| TwelveData | 500/day | Primary |
| Finnhub | 60/min (86k/day) | Fallback |
| Alpha Vantage | 500/day | Backup |
| **TOTAL** | **87,000 calls/day** | More than enough! |

#### Aggressive Caching
```bash
# .env
CACHE_TTL_MARKET_DATA=900  # 15 minutes
```

**Impact:**
- Stock price doesn't change every second
- 15-min cache is fine for swing trading
- Reduces API calls by **90%+**

**Example:**
- Without cache: 100 users × 10 requests/day = **1,000 API calls**
- With 15-min cache: **~100 API calls** (90% reduction!)

---

### 3. Database Costs

#### Railway PostgreSQL
```bash
# Current: $5/month for 256MB
# Scales to: $10/month for 1GB
```

**Optimization:**
- Index frequently queried columns
- Clean up old data periodically
- Use Redis for hot data

#### Alternative: Supabase (FREE tier)
```bash
# Up to 500MB database FREE
# 50k monthly active users FREE
```

**Migration if needed:**
```bash
DATABASE_URL=postgresql://postgres:[password]@db.supabase.co:5432/postgres
```

---

### 4. Redis Caching (FREE)

#### Upstash Redis
```bash
REDIS_URL=redis://default:AXsPAAIncDI4MDVmZThlODU1YzU0YjJiYTBmNmU2MjdiNmIwZDA1YXAyMzE1MDM@pleasing-tahr-31503.upstash.io:6379
```

**Free Tier:**
- 10,000 commands/day
- 256MB storage
- Low latency worldwide

**Our Usage (optimized):**
- ~3,000 commands/day
- **Well within free tier!** ✅

**What We Cache:**
- Pattern detection results (1 hour)
- Market data (15 minutes)
- Chart images (2 hours)
- AI responses (30 minutes)

**Savings:**
- Avoid recomputing expensive operations
- Reduce database load
- Faster response times
- **99% cache hit rate possible!**

---

### 5. Hosting Costs

#### Railway (Current)
```bash
# Starter: $5/month
# Hobby: $20/month (if you need more resources)
```

**Optimization:**
- Use smallest instance that works
- Monitor resource usage
- Scale only when needed

#### Alternative: Fly.io (Cheaper for Small Apps)
```bash
# Free tier: 3 shared VMs
# Paid: $1.94/month minimum
```

---

## 🚀 Advanced Cost Optimizations

### 1. Smart API Key Rotation

**Problem:** Rate limits per API key

**Solution:** Rotate between multiple free API keys
```python
# Pseudo-code
api_keys = [key1, key2, key3]
current_key = api_keys[request_count % len(api_keys)]
```

**Result:** 3x capacity!

### 2. Request Batching

**Problem:** Making 100 separate API calls = expensive

**Solution:** Batch requests
```python
# Instead of:
for symbol in symbols:
    get_price(symbol)  # 100 API calls

# Do this:
get_prices(symbols)  # 1 API call (batch)
```

**Savings:** 100x reduction in API calls!

### 3. Lazy Loading

**Problem:** Loading all data upfront = slow + expensive

**Solution:** Load only what's needed
```python
# Don't pre-load 500 stocks
# Load top 10, then load more if user scrolls
```

**Savings:** 50x reduction in initial load!

### 4. Background Jobs

**Problem:** Real-time scanning for 500 stocks = expensive

**Solution:** Run scans in background during off-peak hours
```python
# Schedule at 6 AM daily (low traffic time)
# Cache results for the day
# Users get instant responses (from cache)
```

**Savings:** Optimize resource usage!

### 5. Progressive Enhancement

**Problem:** Full AI analysis for every request = expensive

**Solution:** Tiered approach
```python
# Free users: Cached results only
# Light users: Basic AI (GPT-3.5)
# Premium users: Full AI (Claude 3.5)
```

---

## 📉 Monitoring Costs

### Track Usage Daily

```bash
# Check OpenRouter usage
curl https://openrouter.ai/api/v1/generation \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"

# Check TwelveData usage
curl "https://api.twelvedata.com/usage?apikey=$TWELVEDATA_API_KEY"

# Check Finnhub usage
# (Check dashboard: https://finnhub.io/dashboard)

# Check Railway usage
# (Check dashboard: https://railway.app)
```

### Set Budget Alerts

**OpenRouter:**
- Set monthly budget: $10/month
- Email alert at 80% ($8)
- Hard stop at 100% ($10)

**Railway:**
- Set spending limit in dashboard
- Get notified at thresholds

---

## 🎯 Recommended Settings for Maximum Savings

```bash
# .env - COST OPTIMIZED CONFIGURATION

# AI: Use Claude (3x cheaper than GPT-4)
OPENROUTER_API_KEY=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
AI_MODEL=anthropic/claude-3.5-sonnet
AI_TEMPERATURE=0.7
AI_RATE_LIMIT_PER_MINUTE=20  # Prevent runaway costs

# Market Data: Free tiers + aggressive caching
TWELVEDATA_API_KEY=14b61f5898d1412681a8dfc878f857b4
FINNHUB_API_KEY=cv9n4f1r01qpd9s87710cv9n4f1r01qpd9s877lg
ALPHA_VANTAGE_API_KEY=3WOG24BQLRKC7KOO
DATA_SOURCE_PRIORITY=twelvedata,finnhub,alphavantage

# Caching: Maximize cache TTL
CACHE_TTL_PATTERNS=3600       # 1 hour (patterns don't change often)
CACHE_TTL_MARKET_DATA=900     # 15 min (good enough for swing trading)
CACHE_TTL_CHARTS=7200         # 2 hours (charts don't change much)
CACHE_TTL_AI_RESPONSES=1800   # 30 min (cache AI responses)

# Rate Limiting: Prevent abuse
RATE_LIMIT_PER_MINUTE=60
MARKET_DATA_RATE_LIMIT=30

# Database: Use smallest instance
DATABASE_URL=postgresql://...  # Railway starter

# Redis: FREE tier
REDIS_URL=redis://...  # Upstash free tier
```

---

## 💡 Pro Tips

### 1. Use Chart-img.com (You're Paying for It!)
```bash
CHART_IMG_API_KEY=tGvkXDWnfI5G8WX6VnsIJ3xLvnfLt56x6Q8UaNbU
```
- You have PRO version = **unlimited charts**
- Don't waste it! Generate charts freely
- Cache them for 2 hours to reduce regeneration

### 2. Batch User Requests
```python
# If 10 users request AAPL within 15 minutes:
# - Fetch once
# - Serve cached to all 10
# - 90% savings!
```

### 3. Precompute Popular Stocks
```python
# Daily job: Scan top 100 stocks at 6 AM
# Cache results all day
# 99% of requests = instant (from cache)
```

### 4. Use Telegram for Free Notifications
```bash
TELEGRAM_BOT_TOKEN=8072569977:AAH6ajboc0Tl9LHUp1VUj3eQHy_XF6naGB4
```
- Free push notifications
- Better than SMS or email
- No rate limits

---

## 🎊 Summary: Your Optimized Setup

**Monthly Costs:**
```
AI (Claude via OpenRouter):     $3-5
Market Data:                    $0 (free tiers)
Charts (Chart-img PRO):         $X (you're already paying)
Database (Railway):             $5
Redis (Upstash):                $0 (free tier)
Hosting (Railway):              $5
N8N:                            $0-20
─────────────────────────────────
TOTAL:                          $13-35/month
```

**Compared to alternatives:**
- Direct OpenAI + Premium data: **$125-800/month**
- **You save: $112-765/month** (91-96% savings!)

**With your setup:**
✅ Same quality (Claude 3.5 = GPT-4 quality)
✅ Same speed (cached responses)
✅ Same features (everything works)
✅ **10x cheaper** than naive approach!

---

## 🚨 Warning Signs

**Watch out for these cost traps:**

1. **No caching** = 10x more API calls
2. **No rate limiting** = runaway costs
3. **Using GPT-4 directly** = 5x more expensive
4. **Not using fallback sources** = hitting rate limits
5. **Real-time everything** = unnecessary API calls

**If your costs spike:**
1. Check OpenRouter dashboard (api usage)
2. Check Railway logs (resource usage)
3. Check Redis cache hit rate
4. Review API call patterns
5. Enable more aggressive caching

---

**Your setup is now optimized for maximum performance at minimum cost!** 🎯
