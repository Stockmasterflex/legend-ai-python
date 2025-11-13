# Local Development Setup Guide

This guide walks you through getting Legend AI running locally on your machine.

## Prerequisites

- **Python 3.11+** (check: `python3 --version`)
- **Docker & Docker Compose** (for Redis + PostgreSQL)
- **Git** (already have this)

## Step 1: Create Virtual Environment

```bash
cd /Users/kyleholthaus/Projects/legend-ai-python

# Create venv
python3.11 -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Verify it works
which python  # Should show path to venv/bin/python
```

## Step 2: Install Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**Expected time**: 2-3 minutes

## Step 3: Start Local Services (Redis + PostgreSQL)

Make sure Docker is running on your machine, then:

```bash
# In the project root directory
docker compose up -d

# Verify services are running
docker compose ps
```

You should see:
```
NAME                           STATUS
legend-ai-python-postgres-1    Up (healthy)
legend-ai-python-redis-1       Up (healthy)
legend-ai-python-app-1         Up (or might not be running, that's OK)
```

## Step 4: Verify Environment Configuration

The `.env` file has been created with development defaults. Check it:

```bash
cat .env
```

**Key values to verify**:
- `DEBUG=true` (development mode)
- `REDIS_URL=redis://localhost:6379/0`
- `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/legend_ai`
- `TELEGRAM_BOT_TOKEN=dev-token` (won't connect to real bot yet)

## Step 5: Run the FastAPI Server

```bash
# Option A: Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Option B: Using python directly
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output**:
```
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
INFO:     Starting Legend AI Bot...
INFO:     Setting Telegram webhook to: http://localhost:8000/api/webhook/telegram
⚠️ Telegram bot token not configured - webhook not set
INFO:     Bot started successfully!
```

## Step 6: Test the API

In another terminal:

```bash
# Health check
curl http://localhost:8000/health

# Root endpoint
curl http://localhost:8000/

# Check Redis cache
curl http://localhost:8000/api/cache/health

# Test pattern detection (example NVIDIA)
curl -X POST http://localhost:8000/api/patterns/detect \
  -H "Content-Type: application/json" \
  -d '{"ticker": "NVDA"}'
```

**Expected responses**:
- Health: `{"status": "healthy", "telegram": "not_configured", "redis": "unknown"}`
- Root: `{"status": "running", "service": "Legend AI Bot", "version": "1.0.0"}`

## Step 7: Access the Dashboard

The embedded dashboard is available at:
```
http://localhost:8000/dashboard
```

This includes TradingView widgets (ticker tape, charts, heatmaps, screener, etc.)

## Troubleshooting

### "ModuleNotFoundError: No module named 'app'"
- Make sure you're in the project root directory
- Verify venv is activated (`which python` should show the venv path)

### "ConnectionError: Error while trying to write to socket"
- Redis isn't running: `docker compose ps` to check
- Start it: `docker compose up -d`

### "psycopg2 error: could not connect to server"
- PostgreSQL isn't running
- Start it: `docker compose up -d`
- Wait a few seconds for it to initialize

### Telegram webhook not configuring
- This is expected with `TELEGRAM_BOT_TOKEN=dev-token`
- To use the real bot, update `.env` with a real token from BotFather

### Port 8000 already in use
```bash
# Find what's using it
lsof -i :8000

# Kill the process or use a different port
uvicorn app.main:app --reload --port 8001
```

## Next Steps

1. **Update API Keys** in `.env` once you have them from:
   - TwelveData (market data)
   - OpenRouter (AI models)
   - Chart-IMG (chart generation)
   - Telegram BotFather (if testing bot)

2. **Test Individual Endpoints**: Each API router has different endpoints - check `app/api/` directory

3. **Monitor Logs**: Watch the FastAPI terminal for errors and debug messages

4. **Deploy to Railway**: See `RAILWAY_DEPLOYMENT.md` for production setup

## Common Development Tasks

### Restart the server
```bash
# Stop with Ctrl+C, then restart
uvicorn app.main:app --reload
```

### Reset Redis cache
```bash
docker exec legend-ai-python-redis-1 redis-cli FLUSHALL
```

### View PostgreSQL data
```bash
docker exec -it legend-ai-python-postgres-1 psql -U postgres -d legend_ai
```

### Stop all services
```bash
docker compose down
```

### Completely restart everything
```bash
docker compose down -v  # Remove volumes too
docker compose up -d
```

## File Structure Reference

```
legend-ai-python/
├── .env                    # Your local secrets (DON'T commit)
├── .env.example           # Template for others
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Local Redis + PostgreSQL
├── app/
│   ├── main.py           # FastAPI app entry point
│   ├── config.py         # Settings management
│   ├── api/              # 13 API routers
│   ├── core/             # Business logic
│   └── services/         # External service integrations
└── docs/                 # Documentation
```

---

**You're all set! Start with Step 1 above and let me know if you hit any issues. 🚀**
