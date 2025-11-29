# Legend AI Deployment Guide

## Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Railway account (optional, for managed deployment)

## Local Development

### 1. Clone Repository

```bash
git clone https://github.com/your-org/legend-ai-python.git
cd legend-ai-python
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL

```bash
# Create database
createdb legend_ai

# Run migrations
alembic upgrade head
```

### 5. Setup Redis

```bash
# Start Redis
redis-server

# Verify
redis-cli ping  # Should return PONG
```

### 6. Configure Environment

Create `.env`:

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/legend_ai

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# API Keys
TWELVEDATA_API_KEY=your_key
FINNHUB_API_KEY=your_key
ALPHA_VANTAGE_KEY=your_key
CHART_IMG_API_KEY=your_key

# Telegram (Optional)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# App Settings
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### 7. Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit: http://localhost:8000/docs

## Railway Deployment

### 1. Install Railway CLI

```bash
npm install -g @railway/cli
```

### 2. Login to Railway

```bash
railway login
```

### 3. Initialize Project

```bash
railway init
```

### 4. Add PostgreSQL

```bash
railway add postgresql
```

### 5. Add Redis

```bash
railway add redis
```

### 6. Set Environment Variables

```bash
railway variables set TWELVEDATA_API_KEY=your_key
railway variables set FINNHUB_API_KEY=your_key
railway variables set CHART_IMG_API_KEY=your_key
railway variables set TELEGRAM_BOT_TOKEN=your_token
railway variables set TELEGRAM_CHAT_ID=your_id
```

### 7. Deploy

```bash
railway up
```

### 8. Run Migrations

```bash
railway run alembic upgrade head
```

### 9. Check Status

```bash
railway status
railway logs
```

## Docker Deployment

### 1. Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://legend:legend@db:5432/legend_ai
      REDIS_HOST: redis
      REDIS_PORT: 6379
    depends_on:
      - db
      - redis
    volumes:
      - ./data:/app/data

  db:
    image: postgres:14
    environment:
      POSTGRES_USER: legend
      POSTGRES_PASSWORD: legend
      POSTGRES_DB: legend_ai
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 3. Build and Run

```bash
docker-compose up -d
```

### 4. Run Migrations

```bash
docker-compose exec app alembic upgrade head
```

## Production Checklist

### Security
- [ ] Change default database passwords
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS properly
- [ ] Rate limit API endpoints
- [ ] Setup firewall rules

### Monitoring
- [ ] Configure logging (Sentry, LogDNA)
- [ ] Setup health checks (`/health`)
- [ ] Monitor error rates
- [ ] Track API response times
- [ ] Alert on high CPU/memory usage

### Performance
- [ ] Enable Redis caching
- [ ] Configure connection pooling
- [ ] Optimize database queries
- [ ] Add database indices
- [ ] Use CDN for static assets

### Reliability
- [ ] Setup database backups (daily)
- [ ] Configure auto-scaling
- [ ] Test disaster recovery
- [ ] Document rollback procedure
- [ ] Setup CI/CD pipeline

### Scheduled Jobs
- [ ] Verify EOD scanner runs (4:05 PM ET)
- [ ] Verify watchlist monitor (5-min intervals)
- [ ] Verify universe refresh (Sunday 8 PM)
- [ ] Monitor job failures

## Maintenance

### Database Backups

```bash
# Backup
pg_dump legend_ai > backup_$(date +%Y%m%d).sql

# Restore
psql legend_ai < backup_20251129.sql
```

### Log Rotation

Configure in `/etc/logrotate.d/legend-ai`:

```
/var/log/legend-ai/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
}
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Health Checks

```bash
# Check API
curl http://localhost:8000/health

# Check database
psql -c "SELECT 1"

# Check Redis
redis-cli ping

# Check scheduler
curl http://localhost:8000/api/scan/latest
```

## Troubleshooting

### App Won't Start
```bash
# Check logs
railway logs
# or
docker-compose logs app

# Verify environment variables
railway variables
```

### Database Connection Errors
```bash
# Test connection
psql $DATABASE_URL

# Check credentials in .env
cat .env | grep DATABASE_URL
```

### Redis Connection Errors
```bash
# Test Redis
redis-cli -h $REDIS_HOST -p $REDIS_PORT ping

# Check if Redis is running
ps aux | grep redis
```

### Scheduler Not Running
```bash
# Check logs for scheduler errors
grep "scheduler" logs/app.log

# Verify timezone
TZ=America/New_York date
```

### High Memory Usage
```bash
# Check memory
free -h

# Restart app
railway restart
# or
docker-compose restart app
```

## Support

- **Documentation:** `/docs`
- **Health:** `/health`
- **Version:** `/version`
- **Logs:** `railway logs` or `docker-compose logs`

---

**Deploy with confidence! 🚀**
