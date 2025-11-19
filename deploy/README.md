# Legend AI - Deployment Scripts

## 🚀 One-Click Deployment

Automated deployment system with pre-flight checks, validation, smoke tests, and automatic rollback on failure.

## Quick Start

```bash
# Deploy with one command
./deploy/deploy.sh
```

## What It Does

The deployment script automatically:

1. ✅ **Pre-Deploy Validation** - Checks code, dependencies, and system requirements
2. 🏷️ **Creates Rollback Point** - Git tag for instant rollback if needed
3. 🔐 **Validates Environment** - Ensures all required API keys and configs are set
4. 🗄️ **Runs Migrations** - Updates database schema safely
5. 🏗️ **Builds & Deploys** - Docker or Railway deployment
6. ✓ **Smoke Tests** - Validates all critical endpoints are working
7. 📱 **Telegram Alerts** - Sends deployment status notifications

If **any step fails**, it automatically rolls back to the previous working state.

## Individual Scripts

### Pre-Deploy Validation
```bash
./deploy/pre-deploy-check.sh
```
Checks:
- Python version (3.11+)
- Git status
- Disk space
- Critical files exist
- Python syntax
- Test suite (optional)

### Environment Validation
```bash
python ./deploy/check_env_vars.py
```
Validates:
- Required env vars (SECRET_KEY, DATABASE_URL)
- Recommended vars (REDIS_URL, API keys)
- Railway environment detection
- Database and Redis configuration

### Database Migrations
```bash
python ./deploy/run_migrations.py
```
Performs:
- Creates missing tables
- Adds database indexes
- Runs schema updates
- Adds pattern validation columns
- Adds alert preference columns

### Smoke Tests
```bash
./deploy/smoke-tests.sh
```
Tests:
- `/health` - Health check endpoint
- `/healthz` - Kubernetes health
- `/api/version` - Version info
- `/metrics` - Prometheus metrics
- `/api/analyze` - Pattern analysis
- `/api/scan` - Universe scanner
- `/api/watchlist` - Watchlist API
- Redis and Telegram status

### Rollback
```bash
# Rollback to latest pre-deploy tag
./deploy/rollback.sh

# Rollback to specific tag
./deploy/rollback.sh pre-deploy-20240115-143022
```

## Environment Variables

### Required for Telegram Notifications
```bash
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### Required for Deployment
```bash
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://...
```

### Optional (for full functionality)
```bash
REDIS_URL=redis://...
TWELVEDATA_API_KEY=...
CHART_IMG_API_KEY=...
OPENROUTER_API_KEY=...
```

## Railway Deployment

For Railway, the script auto-detects the environment:

```bash
# Railway will use railway.toml configuration
# Just run the deployment script
./deploy/deploy.sh
```

The script detects:
- `RAILWAY_ENVIRONMENT` - Auto-detected
- `RAILWAY_PUBLIC_DOMAIN` - Used for smoke tests

## Docker Deployment

For local Docker deployment:

```bash
# Script automatically uses docker-compose
./deploy/deploy.sh
```

## Manual Deployment

If you prefer manual control:

```bash
# 1. Validate
./deploy/pre-deploy-check.sh

# 2. Check environment
python ./deploy/check_env_vars.py

# 3. Run migrations
python ./deploy/run_migrations.py

# 4. Deploy (choose one)
docker-compose up -d --build    # Docker
railway up                       # Railway

# 5. Test
./deploy/smoke-tests.sh
```

## Rollback Tags

Every deployment creates a rollback tag:
```
pre-deploy-YYYYMMDD-HHMMSS
```

View all rollback points:
```bash
git tag -l "pre-deploy-*"
```

Rollback to a specific point:
```bash
./deploy/rollback.sh pre-deploy-20240115-143022
```

## Logs

All deployment logs are saved in:
```
deploy/logs/deploy_YYYYMMDD_HHMMSS.log
```

## Telegram Notifications

If configured, you'll receive:
- ✅ Deployment success notification
- 🚨 Deployment failure alert
- 🔄 Rollback completion notice

## Troubleshooting

### Deployment fails at pre-checks
```bash
# Review the specific check that failed
./deploy/pre-deploy-check.sh
```

### Environment validation fails
```bash
# Check missing variables
python ./deploy/check_env_vars.py

# Set missing variables
export SECRET_KEY="your_secret_key"
export DATABASE_URL="postgresql://..."
```

### Smoke tests fail
```bash
# Run tests manually to see detailed output
./deploy/smoke-tests.sh

# Check specific endpoint
curl http://localhost:8000/health/detailed
```

### Need to rollback
```bash
# List available rollback points
git tag -l "pre-deploy-*"

# Rollback to specific tag
./deploy/rollback.sh pre-deploy-20240115-143022
```

## Best Practices

1. **Always test locally first**
   ```bash
   docker-compose up -d
   ./deploy/smoke-tests.sh
   ```

2. **Review pre-deploy checks**
   ```bash
   ./deploy/pre-deploy-check.sh
   ```

3. **Keep rollback tags for at least 7 days**
   ```bash
   # Clean old tags (older than 7 days)
   git tag -l "pre-deploy-*" | while read tag; do
       # Review and delete manually
   done
   ```

4. **Monitor logs during deployment**
   ```bash
   tail -f deploy/logs/deploy_*.log
   ```

## Safety Features

- ✅ Automatic rollback on any failure
- ✅ Pre-flight validation prevents bad deploys
- ✅ Smoke tests catch runtime issues
- ✅ Git tags enable instant rollback
- ✅ Comprehensive logging
- ✅ Telegram alerts keep you informed

## Support

If deployment fails:
1. Check the log file in `deploy/logs/`
2. Review the failed step
3. Fix the issue
4. Run deployment again

The system will automatically rollback on failure, so your production environment stays safe.
