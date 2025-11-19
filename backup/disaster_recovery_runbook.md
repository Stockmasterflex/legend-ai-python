# Disaster Recovery Runbook

## 🚨 Emergency Response Guide

This document provides step-by-step instructions for recovering Legend AI from various disaster scenarios.

## Quick Reference

| Scenario | Recovery Time | Data Loss | Script |
|----------|---------------|-----------|--------|
| Database corruption | 5-10 min | None (last backup) | `restore_database.sh` |
| Complete server failure | 15-30 min | Minimal | Full DR process |
| Redis failure | 1-2 min | Cache only | `backup_redis.sh` restore |
| Universe data loss | 1 min | None | Git restore |
| Code corruption | 2-5 min | None | Git rollback |

## Emergency Contacts

- **System Owner**: [Your contact info]
- **Railway Support**: https://railway.app/support
- **Telegram Bot**: @YourBotName

## Disaster Scenarios

### Scenario 1: Database Corruption or Loss

**Symptoms:**
- Application can't connect to database
- Data inconsistencies
- Database errors in logs

**Recovery Steps:**

1. **Assess the damage**
   ```bash
   # Check database status
   psql $DATABASE_URL -c "SELECT version();"
   ```

2. **Stop the application**
   ```bash
   docker-compose down
   # Or on Railway: temporarily disable service
   ```

3. **Find latest backup**
   ```bash
   ls -lh backup/backups/database/
   ```

4. **Restore from backup**
   ```bash
   ./backup/restore_database.sh backup/backups/database/db_backup_YYYYMMDD_HHMMSS.sql.gz
   ```

5. **Verify restoration**
   ```bash
   psql $DATABASE_URL -c "SELECT COUNT(*) FROM tickers;"
   psql $DATABASE_URL -c "SELECT COUNT(*) FROM pattern_scans;"
   ```

6. **Restart application**
   ```bash
   docker-compose up -d
   # Or on Railway: re-enable service
   ```

7. **Run smoke tests**
   ```bash
   ./deploy/smoke-tests.sh
   ```

**Expected Recovery Time**: 5-10 minutes
**Data Loss**: Up to last backup interval (default: daily)

---

### Scenario 2: Complete Server Failure

**Symptoms:**
- Server unreachable
- Railway service down
- Complete infrastructure loss

**Recovery Steps:**

1. **Deploy new Railway instance**
   ```bash
   # From local machine with working copy
   git clone https://github.com/yourusername/legend-ai-python.git
   cd legend-ai-python
   railway login
   railway init
   railway up
   ```

2. **Set environment variables**
   ```bash
   # Copy from .env.example and fill in values
   railway variables set SECRET_KEY=xxx
   railway variables set DATABASE_URL=xxx
   railway variables set REDIS_URL=xxx
   railway variables set TELEGRAM_BOT_TOKEN=xxx
   railway variables set TWELVEDATA_API_KEY=xxx
   railway variables set CHART_IMG_API_KEY=xxx
   railway variables set OPENROUTER_API_KEY=xxx
   ```

3. **Provision new database**
   ```bash
   # Railway automatically provisions PostgreSQL
   # Get DATABASE_URL from Railway dashboard
   ```

4. **Restore database from backup**
   ```bash
   # Download latest backup from S3 (if configured)
   aws s3 cp s3://your-bucket/database/db_backup_latest.sql.gz .

   # Or use local backup
   ./backup/restore_database.sh backup/backups/database/db_backup_YYYYMMDD_HHMMSS.sql.gz
   ```

5. **Deploy application**
   ```bash
   ./deploy/deploy.sh
   ```

6. **Verify all services**
   ```bash
   curl https://your-new-app.railway.app/health/detailed
   ```

7. **Update DNS/webhooks**
   ```bash
   # Update Telegram webhook
   curl -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook?url=https://your-new-app.railway.app/api/webhook/telegram"
   ```

**Expected Recovery Time**: 15-30 minutes
**Data Loss**: Up to last backup

---

### Scenario 3: Redis Cache Failure

**Symptoms:**
- Slow performance
- Cache misses
- Redis connection errors

**Recovery Steps:**

1. **Check Redis status**
   ```bash
   redis-cli -u $REDIS_URL ping
   ```

2. **Restart Redis**
   ```bash
   # Docker
   docker-compose restart redis

   # Railway
   # Restart Redis service from dashboard
   ```

3. **Restore from backup (optional)**
   ```bash
   # If data recovery needed
   # Stop Redis
   docker-compose stop redis

   # Replace dump.rdb
   cp backup/backups/redis/dump_YYYYMMDD_HHMMSS.rdb /path/to/redis/dump.rdb

   # Start Redis
   docker-compose start redis
   ```

4. **Warm up cache**
   ```bash
   # Application will rebuild cache on first requests
   # Or manually trigger popular queries
   curl "http://localhost:8000/api/analyze?ticker=AAPL&interval=1d"
   ```

**Expected Recovery Time**: 1-2 minutes
**Data Loss**: Cache only (acceptable)

---

### Scenario 4: Universe Data Corruption

**Symptoms:**
- Invalid ticker symbols
- Missing universe data
- Scan errors

**Recovery Steps:**

1. **Restore from Git**
   ```bash
   git checkout data/universe_seed.json
   ```

2. **Or restore from backup**
   ```bash
   cp backup/backups/universe/universe_seed_YYYYMMDD_HHMMSS.json data/universe_seed.json
   ```

3. **Restart application**
   ```bash
   docker-compose restart app
   ```

4. **Verify**
   ```bash
   curl http://localhost:8000/health/detailed | jq '.universe'
   ```

**Expected Recovery Time**: 1 minute
**Data Loss**: None

---

### Scenario 5: Code Deployment Failure

**Symptoms:**
- Application won't start
- Deployment errors
- Breaking changes

**Recovery Steps:**

1. **Automatic rollback (if using deploy.sh)**
   ```bash
   # Rollback happens automatically on deployment failure
   # Check logs: deploy/logs/deploy_*.log
   ```

2. **Manual rollback**
   ```bash
   # Find rollback point
   git tag -l "pre-deploy-*"

   # Rollback
   ./deploy/rollback.sh pre-deploy-YYYYMMDD-HHMMSS
   ```

3. **Or rollback to last known good commit**
   ```bash
   git log --oneline
   git reset --hard <commit-hash>
   git push -f origin main
   ```

4. **Redeploy**
   ```bash
   ./deploy/deploy.sh
   ```

**Expected Recovery Time**: 2-5 minutes
**Data Loss**: None

---

### Scenario 6: API Key Compromise

**Symptoms:**
- Unusual API usage
- Unauthorized access
- API rate limit exceeded

**Recovery Steps:**

1. **Immediately rotate compromised keys**
   ```bash
   # Generate new keys from provider dashboards
   # TwelveData: https://twelvedata.com/account
   # ChartIMG: https://chartimg.com/account
   # OpenRouter: https://openrouter.ai/keys
   # Telegram: @BotFather - /revoke, /newbot
   ```

2. **Update environment variables**
   ```bash
   # Railway
   railway variables set TWELVEDATA_API_KEY=new_key
   railway variables set CHART_IMG_API_KEY=new_key
   railway variables set OPENROUTER_API_KEY=new_key
   railway variables set TELEGRAM_BOT_TOKEN=new_token

   # Or update .env file
   ```

3. **Restart application**
   ```bash
   railway restart
   # Or
   docker-compose restart app
   ```

4. **Verify new keys work**
   ```bash
   ./deploy/smoke-tests.sh
   ```

5. **Review access logs**
   ```bash
   # Check for unauthorized access
   railway logs
   ```

**Expected Recovery Time**: 10-15 minutes
**Data Loss**: None

---

## Backup Verification

### Weekly Backup Test

Run monthly to ensure backups work:

```bash
# 1. Create test database
createdb test_restore

# 2. Restore latest backup
export DATABASE_URL="postgresql://user:pass@localhost:5432/test_restore"
./backup/restore_database.sh backup/backups/database/db_backup_latest.sql.gz

# 3. Verify data
psql $DATABASE_URL -c "SELECT COUNT(*) FROM tickers;"

# 4. Cleanup
dropdb test_restore
```

---

## Automated Backup Schedule

### Setup Cron Jobs

```bash
# Edit crontab
crontab -e

# Add these lines:

# Daily full backup at 2 AM
0 2 * * * /path/to/legend-ai-python/backup/backup_all.sh

# Database backup every 6 hours
0 */6 * * * /path/to/legend-ai-python/backup/backup_database.sh

# Redis backup every 12 hours
0 */12 * * * /path/to/legend-ai-python/backup/backup_redis.sh

# Weekly verification test (Sundays at 3 AM)
0 3 * * 0 /path/to/legend-ai-python/backup/verify_backups.sh
```

### Railway Scheduled Jobs

In `railway.toml`:

```toml
[deploy]
healthcheckPath = "/health"

[[deploy.cron]]
schedule = "0 2 * * *"
command = "./backup/backup_all.sh"

[[deploy.cron]]
schedule = "0 */6 * * *"
command = "./backup/backup_database.sh"
```

---

## Data Retention Policy

| Data Type | Retention | Location |
|-----------|-----------|----------|
| Database backups | 7 days | Local + S3 |
| Redis snapshots | 7 days | Local |
| Universe data | 30 days | Local + Git |
| Application logs | 14 days | Railway |
| Deployment logs | 30 days | Local |

---

## Monitoring & Alerts

### Setup Alerts

1. **Backup failure alerts** - Already integrated via Telegram
2. **Disk space alerts** - Monitor backup directory size
3. **Database health** - `/health/detailed` endpoint
4. **Application uptime** - Railway health checks

### Health Check Endpoints

```bash
# Basic health
curl https://your-app.railway.app/health

# Detailed health (shows all dependencies)
curl https://your-app.railway.app/health/detailed

# Metrics
curl https://your-app.railway.app/metrics
```

---

## Post-Incident Checklist

After resolving any disaster:

- [ ] Document what happened
- [ ] Document what was done
- [ ] Update runbook if needed
- [ ] Review backup strategy
- [ ] Test backup restoration
- [ ] Notify stakeholders
- [ ] Schedule post-mortem
- [ ] Implement preventive measures

---

## Prevention Best Practices

1. **Regular backups** - Automated daily
2. **Test restores** - Monthly verification
3. **Monitor health** - Continuous monitoring
4. **Version control** - All code in Git
5. **Infrastructure as Code** - Document all configs
6. **Redundancy** - Multiple API providers
7. **Rate limiting** - Prevent abuse
8. **Secrets management** - Rotate keys regularly

---

## Support & Escalation

### If This Runbook Doesn't Help:

1. Check Railway status: https://railway.app/status
2. Review application logs: `railway logs`
3. Check database logs: `railway logs -s postgres`
4. Contact Railway support: https://railway.app/support
5. Review GitHub issues: https://github.com/your-repo/issues

### Emergency Rollback

If all else fails:

```bash
# Nuclear option: complete rollback
git checkout main
git reset --hard origin/main
./deploy/deploy.sh
```

---

## Document History

- 2024-01-15: Initial version
- Last Updated: 2024-01-15
- Next Review: 2024-02-15

---

**Remember**: In a disaster, stay calm and follow the steps methodically. Most disasters are recoverable with proper backups!
