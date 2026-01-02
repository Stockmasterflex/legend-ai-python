# Railway Environment Variables Setup Guide

## 🚨 CRITICAL: Add These Environment Variables to Railway

Go to Railway Dashboard → Legend-Ai-Python project → legend-ai-python service → Variables tab

## Required Variables

⚠️ **SECURITY NOTE**: Real API keys have been removed from this public documentation. Retrieve your actual keys from your secure credential storage.

### CORS Configuration (CRITICAL for Vercel integration)
```bash
CORS_ORIGINS=https://kyle-career-site.vercel.app
```

### Market Data APIs
```bash
TWELVEDATA_API_KEY=your-twelvedata-api-key-here
FINNHUB_API_KEY=your-finnhub-api-key-here
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-api-key-here
```

### Chart Generation
```bash
CHART_IMG_API_KEY=your-chart-img-api-key-here
```

### AI Services
```bash
OPENROUTER_API_KEY=your-openrouter-api-key-here
AI_MODEL=anthropic/claude-3.5-sonnet
```

### Redis Cache (if not using Railway Redis)
```bash
REDIS_URL=your-redis-connection-url-here
```

## ✅ Verification
After adding, test:
```bash
curl https://legend-ai-python-production.up.railway.app/health
```

## 🔒 Security Best Practices
- Never commit real API keys to Git
- Store credentials in Railway environment variables only
- Rotate keys immediately if exposed
- Use `.env` files locally (ensure they're in `.gitignore`)
