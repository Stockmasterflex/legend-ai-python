# Legend AI - Railway Deployment Guide

## 🚀 Quick Railway Deployment

### Prerequisites
- Railway account (https://railway.app)
- GitHub repository with this code

### Step 1: Connect to Railway
```bash
# Install Railway CLI (optional)
npm install -g @railway/cli

# Login
railway login

# Or use Railway web dashboard
```

### Step 2: Deploy from GitHub
1. Go to Railway dashboard
2. Click "New Project" → "Deploy from GitHub"
3. Select your `legend-ai-python` repository
4. Railway will auto-detect the configuration

### Step 3: Configure Environment Variables
In Railway dashboard, go to your project → Variables, and set:

```bash
# Required API Keys
TELEGRAM_BOT_TOKEN=8072569977:AAH6ajboc0Tl9LHUp1VUj3eQHy_XF6naGB4
OPENROUTER_API_KEY=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
TWELVEDATA_API_KEY=14b61f5898d1412681a8dfc878f857b4
CHARTIMG_API_KEY=tGvkXDWnfI5G8WX6VnsIJ3xLvnfLt56x6Q8UaNbU

# App Settings
DEBUG=false
SECRET_KEY=your-production-secret-key

# Database (Railway provides PostgreSQL)
DATABASE_URL=${{ PostgreSQL.DATABASE_URL }}

# Redis (Railway provides Redis)
REDIS_URL=${{ Redis.REDIS_URL }}
```

### Step 4: Add PostgreSQL Database
1. In Railway project, click "Add Plugin" → PostgreSQL
2. Railway will auto-configure DATABASE_URL

### Step 5: Add Redis Cache
1. In Railway project, click "Add Plugin" → Redis
2. Railway will auto-configure REDIS_URL

### Step 6: Deploy
```bash
railway deploy
```

### Step 7: Set Telegram Webhook
After deployment, get your Railway URL and set the webhook:

```bash
curl -X POST "https://api.telegram.org/bot8072569977:AAH6ajboc0Tl9LHUp1VUj3eQHy_XF6naGB4/setWebhook" \
-H "Content-Type: application/json" \
-d '{"url": "https://your-railway-app.railway.app/api/webhook/telegram"}'
```

### Step 8: Verify Deployment
Test the bot:
```bash
curl -X POST "https://api.telegram.org/bot8072569977:AAH6ajboc0Tl9LHUp1VUj3eQHy_XF6naGB4/sendMessage" \
-H "Content-Type: application/json" \
-d '{"chat_id": "7815143490", "text": "🤖 Legend AI deployed successfully!"}'
```

## 🔧 Local Development

### Using Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start Redis (if not using Docker)
redis-server

# Start PostgreSQL (if not using Docker)
# Install and start PostgreSQL

# Run the app
uvicorn app.main:app --reload
```

## 📊 Health Checks

### Application Health
- **URL**: `https://your-app.railway.app/health`
- **Expected**: `{"status":"healthy","telegram":"connected","redis":"healthy","database":"healthy"}`

### API Endpoints
- **Pattern Detection**: `POST /api/patterns/detect`
- **Chart Generation**: `POST /api/charts/generate`
- **Cache Stats**: `GET /api/patterns/health`
- **Telegram Webhook**: `POST /api/webhook/telegram`

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check DATABASE_URL format
   - Verify PostgreSQL plugin is active

2. **Redis Connection Failed**
   - Check REDIS_URL format
   - Verify Redis plugin is active

3. **API Key Errors**
   - Verify all required environment variables are set
   - Check API key formats

4. **Telegram Webhook Issues**
   - Verify webhook URL is accessible
   - Check Railway app is not sleeping

### Logs
```bash
# Railway logs
railway logs

# Local logs
docker-compose logs app
```

## 🎯 Performance Monitoring

### Key Metrics
- Response time: <3s for pattern detection
- Cache hit rate: >70%
- API usage: Monitor TwelveData limits (800/day)
- Error rate: <1%

### Scaling
Railway automatically scales based on usage. Monitor costs and upgrade plan if needed.

## 🔄 Updates & Maintenance

### Deploying Updates
```bash
# Push to GitHub main branch
git add .
git commit -m "Update Legend AI"
git push origin main

# Railway auto-deploys
```

### Database Migrations
```bash
# For future schema changes
alembic revision --autogenerate -m "Add new table"
alembic upgrade head
```

## 📞 Support

If issues persist:
1. Check Railway dashboard for errors
2. Review application logs
3. Verify all environment variables
4. Test API keys independently
