# Backup & Disaster Recovery System

## Overview

Comprehensive backup and disaster recovery system for Legend AI with automated backups, monitoring, and restoration procedures.

## Quick Start

### Full System Backup
```bash
# Backup everything (database + universe + Redis)
./backup/backup_all.sh
```

### Individual Backups
```bash
# Database only
./backup/backup_database.sh

# Universe data only
./backup/backup_universe.sh

# Redis cache only
./backup/backup_redis.sh
```

### Restore Database
```bash
# List available backups
ls -lh backup/backups/database/

# Restore from specific backup
./backup/restore_database.sh backup/backups/database/db_backup_20240115_143022.sql.gz
```

### Monitor Backups
```bash
# Check backup status
python backup/monitor_backups.py
```

## What Gets Backed Up

| Data | Frequency | Retention | Location |
|------|-----------|-----------|----------|
| PostgreSQL Database | Daily (automated) | 7 days | `backup/backups/database/` |
| Universe Data | Daily | 30 days | `backup/backups/universe/` |
| Redis Cache | Daily | 7 days | `backup/backups/redis/` |
| Application Logs | Continuous | 30 days | `deploy/logs/` |

## Automated Backup Schedule

### Setup Cron Jobs

```bash
# Edit crontab
crontab -e

# Add:
# Daily full backup at 2 AM
0 2 * * * /path/to/legend-ai-python/backup/backup_all.sh

# Database backup every 6 hours
0 */6 * * * /path/to/legend-ai-python/backup/backup_database.sh

# Monitor backups every hour
0 * * * * /usr/bin/python3 /path/to/legend-ai-python/backup/monitor_backups.py
```

### Railway Deployment

Railway doesn't support cron jobs natively, so use external scheduler:

**Option 1: GitHub Actions**
```yaml
# .github/workflows/backup.yml
name: Scheduled Backup

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Trigger backup
        run: |
          curl -X POST https://your-app.railway.app/api/admin/backup \
            -H "Authorization: Bearer ${{ secrets.ADMIN_TOKEN }}"
```

**Option 2: External Cron Service**
- https://cron-job.org
- https://easycron.com
- Configure to hit backup endpoint

## Backup Scripts

### 1. backup_all.sh
Master backup script that runs all backups sequentially.

**Features:**
- Backs up database, universe data, and Redis
- Creates consolidated log
- Sends Telegram notifications
- Tracks failures

**Usage:**
```bash
./backup/backup_all.sh
```

### 2. backup_database.sh
PostgreSQL database backup with compression.

**Features:**
- Compressed SQL dumps (gzip)
- Metadata tracking
- Automatic cleanup (7-day retention)
- S3 upload (if configured)
- Telegram notifications

**Configuration:**
```bash
export DATABASE_URL="postgresql://..."
export RETENTION_DAYS=7
export BACKUP_S3_BUCKET="your-bucket"  # Optional
```

**Usage:**
```bash
./backup/backup_database.sh
```

**Output:**
- `backup/backups/database/db_backup_YYYYMMDD_HHMMSS.sql.gz`
- `backup/backups/database/db_backup_YYYYMMDD_HHMMSS.sql.gz.meta`

### 3. backup_universe.sh
Universe and watchlist data backup.

**Features:**
- JSON file backups
- Full data directory archive
- Manifest file creation
- 30-day retention

**Usage:**
```bash
./backup/backup_universe.sh
```

**Output:**
- `backup/backups/universe/universe_seed_YYYYMMDD_HHMMSS.json`
- `backup/backups/universe/watchlist_YYYYMMDD_HHMMSS.json`
- `backup/backups/universe/data_full_YYYYMMDD_HHMMSS.tar.gz`

### 4. backup_redis.sh
Redis snapshot and key export.

**Features:**
- BGSAVE snapshot
- JSON key export (fallback)
- Automatic cleanup
- 7-day retention

**Configuration:**
```bash
export REDIS_URL="redis://..."
# Or
export REDIS_HOST="localhost"
export REDIS_PORT="6379"
export REDIS_PASSWORD="..."  # Optional
```

**Usage:**
```bash
./backup/backup_redis.sh
```

**Output:**
- `backup/backups/redis/dump_YYYYMMDD_HHMMSS.rdb`
- `backup/backups/redis/redis_keys_YYYYMMDD_HHMMSS.json`

### 5. restore_database.sh
Safe database restoration with automatic safety backup.

**Features:**
- Creates safety backup before restore
- Confirmation prompt
- Metadata display
- Telegram notifications

**Usage:**
```bash
# Interactive
./backup/restore_database.sh backup/backups/database/db_backup_20240115_143022.sql.gz

# Confirm with 'yes' when prompted
```

**Safety:**
- Creates `pre_restore_backup_*.sql.gz` before restoration
- Requires explicit confirmation
- Retains safety backup after completion

### 6. monitor_backups.py
Backup monitoring and alerting.

**Features:**
- Checks all backup directories
- Validates backup age
- Sends alerts if backups are missing or old
- JSON status output

**Thresholds:**
- Database: 24 hours
- Universe: 7 days
- Redis: 24 hours

**Usage:**
```bash
python backup/monitor_backups.py
```

**Output:**
```json
{
  "database": {
    "status": "ok",
    "latest": "db_backup_20240115_143022.sql.gz",
    "age_hours": 2.5,
    "threshold_hours": 24
  },
  ...
}
```

## Disaster Recovery

See [Disaster Recovery Runbook](disaster_recovery_runbook.md) for detailed recovery procedures.

### Quick Recovery Scenarios

**Database Failure:**
```bash
./backup/restore_database.sh backup/backups/database/db_backup_latest.sql.gz
```

**Universe Data Loss:**
```bash
cp backup/backups/universe/universe_seed_latest.json data/universe_seed.json
docker-compose restart app
```

**Redis Failure:**
```bash
docker-compose stop redis
cp backup/backups/redis/dump_latest.rdb /path/to/redis/dump.rdb
docker-compose start redis
```

**Complete Server Failure:**
1. Deploy new Railway instance
2. Restore database from S3/local backup
3. Deploy application code
4. Update webhooks/DNS

## Cloud Storage Integration

### AWS S3 Setup

```bash
# Install AWS CLI
pip install awscli

# Configure
aws configure

# Set bucket name
export BACKUP_S3_BUCKET="your-backup-bucket"

# Backups will automatically upload to S3
./backup/backup_database.sh
```

### Download from S3

```bash
# List backups
aws s3 ls s3://your-backup-bucket/database/

# Download specific backup
aws s3 cp s3://your-backup-bucket/database/db_backup_20240115_143022.sql.gz .
```

## Monitoring & Alerts

### Telegram Notifications

Configure Telegram to receive backup alerts:

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
```

**Alerts sent for:**
- ✅ Successful backups
- ❌ Backup failures
- ⚠️ Missing backups
- ⚠️ Old backups (past threshold)
- 🔄 Database restorations

### Prometheus Metrics

Add backup metrics to monitoring:

```python
# In app/telemetry/metrics.py
BACKUP_SUCCESS_TOTAL = Counter('backup_success_total', 'Successful backups', ['type'])
BACKUP_FAILURE_TOTAL = Counter('backup_failure_total', 'Failed backups', ['type'])
BACKUP_AGE_HOURS = Gauge('backup_age_hours', 'Age of latest backup', ['type'])
```

## Testing Backups

### Monthly Backup Test

```bash
# 1. Create test database
createdb test_restore_$(date +%s)

# 2. Restore latest backup
export TEST_DATABASE_URL="postgresql://user:pass@localhost:5432/test_restore_..."
./backup/restore_database.sh backup/backups/database/db_backup_latest.sql.gz

# 3. Verify data
psql $TEST_DATABASE_URL -c "SELECT COUNT(*) FROM tickers;"
psql $TEST_DATABASE_URL -c "SELECT COUNT(*) FROM pattern_scans;"

# 4. Cleanup
dropdb test_restore_...
```

### Automated Testing

Add to CI/CD pipeline:

```yaml
# .github/workflows/test_backups.yml
name: Test Backups
on:
  schedule:
    - cron: '0 3 1 * *'  # Monthly

jobs:
  test-restore:
    runs-on: ubuntu-latest
    steps:
      - name: Test database restore
        run: ./backup/test_restore.sh
```

## Troubleshooting

### Backup fails with "pg_dump: command not found"

```bash
# Install PostgreSQL client tools
# Ubuntu/Debian
sudo apt-get install postgresql-client

# macOS
brew install postgresql
```

### Backup fails with "permission denied"

```bash
# Make scripts executable
chmod +x backup/*.sh
```

### S3 upload fails

```bash
# Check AWS credentials
aws sts get-caller-identity

# Check bucket exists
aws s3 ls s3://your-backup-bucket/

# Check permissions
aws s3api get-bucket-acl --bucket your-backup-bucket
```

### Redis backup fails

```bash
# Install Redis tools
# Ubuntu/Debian
sudo apt-get install redis-tools

# macOS
brew install redis

# Test connection
redis-cli -u $REDIS_URL ping
```

### Restore fails with "database is being accessed"

```bash
# Stop application first
docker-compose down

# Then restore
./backup/restore_database.sh backup.sql.gz

# Start application
docker-compose up -d
```

## Best Practices

1. **Test restores regularly** - Monthly verification
2. **Monitor backup age** - Automated alerts
3. **Offsite storage** - Use S3 or similar
4. **Encrypt backups** - For sensitive data
5. **Document procedures** - Keep runbook updated
6. **Automate everything** - Cron jobs
7. **Version backups** - Don't overwrite
8. **Secure credentials** - Use environment variables

## Security

### Backup Encryption

For sensitive data, encrypt backups:

```bash
# Encrypt backup
gpg --symmetric --cipher-algo AES256 backup.sql.gz

# Decrypt backup
gpg --decrypt backup.sql.gz.gpg > backup.sql.gz
```

### Access Control

```bash
# Restrict backup directory permissions
chmod 700 backup/backups/
chmod 600 backup/backups/*/*.sql.gz
```

### Secure Credentials

Never store credentials in scripts:
- Use environment variables
- Use Railway secrets
- Use AWS IAM roles
- Rotate credentials regularly

## Support

For backup issues:
1. Check logs: `backup/logs/`
2. Test individual scripts
3. Verify environment variables
4. Check disk space
5. Review disaster recovery runbook

## Related Documentation

- [Disaster Recovery Runbook](disaster_recovery_runbook.md)
- [Deployment Guide](../deploy/README.md)
- [Railway Documentation](https://docs.railway.app)
