# Chart-IMG API Setup Guide

This guide will help you configure the Chart-IMG API key for your Legend AI trading dashboard.

## Prerequisites

- Chart-IMG Pro account (you have this already!)
- Your API key: `YOUR_CHART_IMG_API_KEY`
- Railway deployment access

## Why Chart-IMG is Critical

Chart-IMG powers ALL chart previews across your dashboard:
- ✅ **Analysis Tab** - Multi-timeframe charts with entry/stop/target annotations
- ✅ **Watchlist** - Auto-loading preview charts for first 20 items
- ✅ **Pattern Scanner** - Manual preview charts on demand
- ✅ **Top Setups** - Auto-loading charts for all setups

**Without the API key configured, all charts will show placeholders.**

## Setup Instructions for Railway

### Method 1: Railway Dashboard (Recommended)

1. **Log in to Railway** at https://railway.app
2. **Navigate to your project**: `legend-ai-python-production`
3. **Click on your service** (the FastAPI app)
4. **Go to "Variables" tab**
5. **Click "New Variable"**
6. **Add the following:**
   - **Variable name:** `CHARTIMG_API_KEY`
  - **Value:** `YOUR_CHART_IMG_API_KEY`
7. **Click "Add"**
8. **Railway will automatically redeploy** your application

### Method 2: Railway CLI

```bash
# Install Railway CLI if you haven't
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Set the environment variable
railway variables set CHARTIMG_API_KEY=YOUR_CHART_IMG_API_KEY

# Your app will automatically redeploy
```

### Method 3: Local Development (.env file)

For local testing, create/update `.env` in the project root:

```bash
CHARTIMG_API_KEY=YOUR_CHART_IMG_API_KEY
```

**Note:** Never commit the `.env` file to git! It's already in `.gitignore`.

## Verification

After setting the variable, verify it's working:

### 1. Check Health Endpoint

Visit: `https://your-app.railway.app/health`

Look for:
```json
{
  "status": "healthy",  // Should be "healthy", not "degraded"
  "keys": {
    "chartimg": true     // Should be true, not false
  },
  "warnings": []         // Should be empty if Chart-IMG is configured
}
```

### 2. Test Chart Generation

1. Go to the **Analysis tab**
2. Enter a ticker (e.g., `AAPL`)
3. Click **Scan**
4. You should see a chart with indicators and annotations

### 3. Check Browser Console

Open DevTools (F12) and check for these logs:
```
✅ Chart generated for AAPL (1day): https://chart-img.com/...
```

If you see errors like:
```
❌ Chart-IMG API key not configured for AAPL
⚠️ Using placeholder chart for AAPL
```

Then the API key is not set correctly.

## Troubleshooting

### Issue: Charts still showing placeholders

**Possible causes:**
1. Environment variable not set in Railway
2. App hasn't redeployed after setting variable
3. Typo in variable name (must be exactly `CHARTIMG_API_KEY`)

**Solutions:**
- Double-check the variable name in Railway dashboard
- Trigger a manual redeploy in Railway
- Check the `/health` endpoint to verify `keys.chartimg: true`

### Issue: API rate limit exceeded

You're on the **Pro plan** with these limits:
- **500 charts per day**
- **10 charts per second**

The app uses smart caching:
- **24-hour cache** for all chart previews
- **Redis-backed rate limiting** to prevent API abuse
- **Automatic fallback** to placeholder when quota exceeded

Check current usage:
```bash
curl https://your-app.railway.app/api/charts/usage
```

### Issue: Wrong chart symbol

The app tries multiple exchange formats automatically:
1. `NASDAQ:AAPL`
2. `NYSE:AAPL`
3. Mapped format from common stocks

If a ticker isn't showing correctly, it might be on a different exchange. You can override this in the symbol mapping in `app/services/charting.py:346-357`.

## Chart-IMG Pro Features

Your Pro account includes:
- ✅ No watermarks
- ✅ 500 daily API calls
- ✅ 10 requests/second rate limit
- ✅ Custom indicators (EMA, SMA, RSI, Volume)
- ✅ Drawing tools (Long Position with entry/stop/target)
- ✅ Dark theme support
- ✅ Multiple timeframes (1D, 1W, 1H, etc.)

## Support

- Chart-IMG Documentation: https://chart-img.com/documentation
- Chart-IMG Dashboard: https://chart-img.com/dashboard
- Legend AI Issues: Check the `/health` endpoint or browser console for detailed error messages

## Next Steps

Once configured, you can:
1. **Run pattern scans** and see annotated charts immediately
2. **Build your watchlist** with auto-loading preview charts
3. **Use Top Setups** to identify high-probability setups with visual confirmation
4. **Analyze any ticker** with multi-timeframe charts and trade plans

Your trading dashboard is now fully operational! 🚀
