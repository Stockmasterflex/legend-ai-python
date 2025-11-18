#!/bin/bash
#
# Setup automated backups using cron
#
# This script configures a cron job to run database backups automatically
#
# Usage:
#   ./setup_backup_cron.sh [--daily|--hourly|--custom "cron_schedule"]
#

set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Get absolute path to backup script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_SCRIPT="${SCRIPT_DIR}/db_backup.sh"

if [ ! -f "$BACKUP_SCRIPT" ]; then
    log_warn "Backup script not found at: ${BACKUP_SCRIPT}"
    exit 1
fi

# Default: daily at 2 AM
CRON_SCHEDULE="0 2 * * *"

# Parse arguments
case "${1:-daily}" in
    --daily)
        CRON_SCHEDULE="0 2 * * *"  # Daily at 2 AM
        log_info "Setting up daily backups at 2:00 AM"
        ;;
    --hourly)
        CRON_SCHEDULE="0 * * * *"  # Every hour
        log_info "Setting up hourly backups"
        ;;
    --custom)
        if [ -z "${2:-}" ]; then
            log_warn "Custom schedule requires a cron expression"
            exit 1
        fi
        CRON_SCHEDULE="$2"
        log_info "Setting up custom schedule: ${CRON_SCHEDULE}"
        ;;
    *)
        log_info "Using default schedule: daily at 2:00 AM"
        ;;
esac

# Create cron job entry
CRON_JOB="${CRON_SCHEDULE} cd $(dirname "$SCRIPT_DIR")/../.. && ${BACKUP_SCRIPT} >> /var/log/legendai_backup.log 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "db_backup.sh"; then
    log_warn "Backup cron job already exists. Removing old entry..."
    crontab -l 2>/dev/null | grep -v "db_backup.sh" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

log_info "Cron job installed successfully"
log_info "Schedule: ${CRON_SCHEDULE}"
log_info "Log file: /var/log/legendai_backup.log"

echo ""
echo "Current crontab:"
crontab -l

echo ""
log_info "To view backup logs: tail -f /var/log/legendai_backup.log"
log_info "To remove cron job: crontab -e (then delete the line with db_backup.sh)"

exit 0
