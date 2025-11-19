#!/bin/bash
# Database Restore Script
# Restores PostgreSQL database from backup

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="${BACKUP_DIR:-${SCRIPT_DIR}/backups/database}"

log() {
    echo -e "${2:-$NC}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

log_success() { log "$1" "$GREEN"; }
log_error() { log "$1" "$RED"; }
log_warning() { log "$1" "$YELLOW"; }
log_info() { log "$1" "$BLUE"; }

# Check if backup file provided
BACKUP_FILE="$1"

if [[ -z "$BACKUP_FILE" ]]; then
    log_info "Available backups:"
    ls -lh "$BACKUP_DIR"/db_backup_*.sql.gz 2>/dev/null || true
    echo ""
    log_error "Usage: $0 <backup_file>"
    log_error "Example: $0 $BACKUP_DIR/db_backup_20240115_143022.sql.gz"
    exit 1
fi

# Check if file exists
if [[ ! -f "$BACKUP_FILE" ]]; then
    log_error "Backup file not found: $BACKUP_FILE"
    exit 1
fi

log_warning "⚠️  WARNING: This will REPLACE the current database!"
log_warning "⚠️  Current data will be LOST!"
echo ""
log_info "Backup file: $BACKUP_FILE"
log_info "File size: $(du -h "$BACKUP_FILE" | cut -f1)"

if [[ -f "${BACKUP_FILE}.meta" ]]; then
    log_info "Backup metadata:"
    cat "${BACKUP_FILE}.meta"
fi

echo ""
read -p "Are you sure you want to restore? (type 'yes' to confirm): " -r
if [[ ! $REPLY =~ ^yes$ ]]; then
    log_info "Restore cancelled."
    exit 0
fi

# Check DATABASE_URL
if [[ -z "$DATABASE_URL" ]]; then
    log_error "DATABASE_URL not set!"
    exit 1
fi

# Parse DATABASE_URL
DB_URL="$DATABASE_URL"

if [[ $DB_URL =~ postgres(ql)?://([^:]+):([^@]+)@([^:]+):([^/]+)/(.+) ]]; then
    DB_USER="${BASH_REMATCH[2]}"
    DB_PASS="${BASH_REMATCH[3]}"
    DB_HOST="${BASH_REMATCH[4]}"
    DB_PORT="${BASH_REMATCH[5]}"
    DB_NAME="${BASH_REMATCH[6]}"
else
    log_error "Invalid DATABASE_URL format"
    exit 1
fi

log_info "Target database: $DB_NAME @ $DB_HOST:$DB_PORT"

# Create a safety backup first
SAFETY_BACKUP="${BACKUP_DIR}/pre_restore_backup_$(date +%Y%m%d_%H%M%S).sql.gz"
log_info "Creating safety backup first: $SAFETY_BACKUP"

export PGPASSWORD="$DB_PASS"

pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
    --no-owner --no-acl --clean --if-exists | gzip > "$SAFETY_BACKUP" || {
    log_error "Failed to create safety backup!"
    exit 1
}

log_success "✓ Safety backup created"

# Restore database
log_info "Restoring database from: $BACKUP_FILE"

if gunzip -c "$BACKUP_FILE" | psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" 2>&1 | tee /tmp/restore.log; then
    log_success "✓ Database restored successfully!"

    # Send Telegram notification
    if [[ -n "${TELEGRAM_BOT_TOKEN}" && -n "${TELEGRAM_CHAT_ID}" ]]; then
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d "chat_id=${TELEGRAM_CHAT_ID}" \
            -d "text=✅ *Database Restored*%0A%0AFrom: \`$(basename "$BACKUP_FILE")\`%0ADatabase: \`${DB_NAME}\`%0ASafety backup: \`$(basename "$SAFETY_BACKUP")\`" \
            -d "parse_mode=Markdown" > /dev/null 2>&1 || true
    fi

    log_info "Safety backup retained at: $SAFETY_BACKUP"
else
    log_error "Restore failed! Check /tmp/restore.log for details"
    log_info "Safety backup available at: $SAFETY_BACKUP"
    exit 1
fi

log_success "Restore completed!"
