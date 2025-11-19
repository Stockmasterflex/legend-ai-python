#!/bin/bash
# Database Backup Script
# Automated PostgreSQL database backups with retention policy

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="${BACKUP_DIR:-${SCRIPT_DIR}/backups/database}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/db_backup_${TIMESTAMP}.sql.gz"

# Create backup directory
mkdir -p "$BACKUP_DIR"

log() {
    echo -e "${2:-$NC}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

log_success() { log "$1" "$GREEN"; }
log_error() { log "$1" "$RED"; }
log_info() { log "$1" "$BLUE"; }

# Send Telegram notification
send_telegram() {
    local message="$1"
    if [[ -n "${TELEGRAM_BOT_TOKEN}" && -n "${TELEGRAM_CHAT_ID}" ]]; then
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d "chat_id=${TELEGRAM_CHAT_ID}" \
            -d "text=${message}" \
            -d "parse_mode=Markdown" > /dev/null 2>&1 || true
    fi
}

log_info "Starting database backup..."

# Check if DATABASE_URL is set
if [[ -z "$DATABASE_URL" ]]; then
    log_error "DATABASE_URL not set!"
    send_telegram "❌ *Database Backup Failed*%0A%0AError: DATABASE_URL not set"
    exit 1
fi

# Parse DATABASE_URL (format: postgresql://user:password@host:port/database)
DB_URL="$DATABASE_URL"

# Extract components
if [[ $DB_URL =~ postgres(ql)?://([^:]+):([^@]+)@([^:]+):([^/]+)/(.+) ]]; then
    DB_USER="${BASH_REMATCH[2]}"
    DB_PASS="${BASH_REMATCH[3]}"
    DB_HOST="${BASH_REMATCH[4]}"
    DB_PORT="${BASH_REMATCH[5]}"
    DB_NAME="${BASH_REMATCH[6]}"
else
    log_error "Invalid DATABASE_URL format"
    send_telegram "❌ *Database Backup Failed*%0A%0AError: Invalid DATABASE_URL format"
    exit 1
fi

log_info "Database: $DB_NAME @ $DB_HOST:$DB_PORT"

# Create backup
log_info "Creating backup: $BACKUP_FILE"

export PGPASSWORD="$DB_PASS"

if pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
    --no-owner --no-acl --clean --if-exists | gzip > "$BACKUP_FILE"; then

    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    log_success "✓ Backup created: $BACKUP_FILE ($BACKUP_SIZE)"

    # Create metadata file
    cat > "${BACKUP_FILE}.meta" <<EOF
{
    "timestamp": "$(date -Iseconds)",
    "database": "$DB_NAME",
    "host": "$DB_HOST",
    "size": "$BACKUP_SIZE",
    "file": "$(basename "$BACKUP_FILE")"
}
EOF

    send_telegram "✅ *Database Backup Successful*%0A%0ADatabase: \`${DB_NAME}\`%0ASize: ${BACKUP_SIZE}%0AFile: \`$(basename "$BACKUP_FILE")\`"
else
    log_error "Backup failed!"
    send_telegram "❌ *Database Backup Failed*%0A%0ACheck logs for details"
    exit 1
fi

# Clean up old backups
log_info "Cleaning up backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "db_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "db_backup_*.sql.gz.meta" -mtime +$RETENTION_DAYS -delete

REMAINING=$(find "$BACKUP_DIR" -name "db_backup_*.sql.gz" | wc -l)
log_success "✓ Cleanup complete. $REMAINING backups retained."

# Upload to cloud storage (if configured)
if [[ -n "$BACKUP_S3_BUCKET" ]]; then
    log_info "Uploading to S3..."
    if command -v aws &> /dev/null; then
        aws s3 cp "$BACKUP_FILE" "s3://${BACKUP_S3_BUCKET}/database/" || log_error "S3 upload failed"
        aws s3 cp "${BACKUP_FILE}.meta" "s3://${BACKUP_S3_BUCKET}/database/" || log_error "S3 metadata upload failed"
    else
        log_error "AWS CLI not installed, skipping S3 upload"
    fi
fi

log_success "Database backup completed successfully!"

# List recent backups
log_info "Recent backups:"
ls -lh "$BACKUP_DIR"/db_backup_*.sql.gz | tail -5
