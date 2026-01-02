# Railway Environment Variables Setup Guide

## 🚨 CRITICAL: Add These Environment Variables to Railway

Go to Railway Dashboard → Legend-Ai-Python project → legend-ai-python service → Variables tab

## Required Variables (Copy-Paste Ready)

### CORS Configuration (CRITICAL for Vercel integration)
```
CORS_ORIGINS=https://kyle-career-site.vercel.app
```

### Market Data APIs
```
TWELVEDATA_API_KEY=14b61f5898d1412681a8dfc878f857b4
FINNHUB_API_KEY=cv9n4f1r01qpd9s87710cv9n4f1r01qpd9s877lg
ALPHA_VANTAGE_API_KEY=3WOG24BQLRKC7KOO
```

### Chart Generation
```
CHART_IMG_API_KEY=tGvkXDWnfI5G8WX6VnsIJ3xLvnfLt56x6Q8UaNbU
```

### AI Services  
```
OPENROUTER_API_KEY=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
AI_MODEL=anthropic/claude-3.5-sonnet
```

## ✅ Verification
After adding, test: `curl https://legend-ai-python-production.up.railway.app/health`
