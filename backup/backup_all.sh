#!/bin/bash
# Master Backup Script
# Backs up all critical data: database, universe data, Redis

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/logs/backup_$(date +%Y%m%d_%H%M%S).log"

mkdir -p "${SCRIPT_DIR}/logs"

log() {
    echo -e "${2:-$NC}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
}

log_success() { log "$1" "$GREEN"; }
log_error() { log "$1" "$RED"; }
log_info() { log "$1" "$BLUE"; }

send_telegram() {
    local message="$1"
    if [[ -n "${TELEGRAM_BOT_TOKEN}" && -n "${TELEGRAM_CHAT_ID}" ]]; then
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d "chat_id=${TELEGRAM_CHAT_ID}" \
            -d "text=${message}" \
            -d "parse_mode=Markdown" > /dev/null 2>&1 || true
    fi
}

log_info "========================================="
log_info "Starting Full System Backup"
log_info "========================================="

FAILED=0

# 1. Backup Database
log_info "1/3: Backing up PostgreSQL database..."
if bash "${SCRIPT_DIR}/backup_database.sh" >> "$LOG_FILE" 2>&1; then
    log_success "✓ Database backup completed"
else
    log_error "✗ Database backup failed"
    ((FAILED++))
fi

# 2. Backup Universe Data
log_info "2/3: Backing up universe data..."
if bash "${SCRIPT_DIR}/backup_universe.sh" >> "$LOG_FILE" 2>&1; then
    log_success "✓ Universe data backup completed"
else
    log_error "✗ Universe data backup failed"
    ((FAILED++))
fi

# 3. Backup Redis
log_info "3/3: Backing up Redis cache..."
if bash "${SCRIPT_DIR}/backup_redis.sh" >> "$LOG_FILE" 2>&1; then
    log_success "✓ Redis backup completed"
else
    log_error "✗ Redis backup failed"
    ((FAILED++))
fi

# Summary
log_info "========================================="
if [[ $FAILED -eq 0 ]]; then
    log_success "✅ All backups completed successfully!"
    send_telegram "✅ *Full System Backup Complete*%0A%0ATime: $(date)%0ALog: \`$(basename "$LOG_FILE")\`"
else
    log_error "⚠️ $FAILED backup(s) failed!"
    send_telegram "⚠️ *Backup Completed with Errors*%0A%0AFailed: ${FAILED}%0ALog: \`$(basename "$LOG_FILE")\`"
fi
log_info "========================================="
log_info "Log file: $LOG_FILE"

exit $FAILED
