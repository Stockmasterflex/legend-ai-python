#!/bin/bash
#
# Database Restore Script for Legend AI (PostgreSQL)
#
# This script restores a PostgreSQL database from a backup file
#
# Usage:
#   ./db_restore.sh <backup_file>
#   ./db_restore.sh --latest
#   ./db_restore.sh --from-s3 s3://bucket/path/to/backup.sql.gz
#
# Requirements:
#   - psql installed
#   - DATABASE_URL environment variable set
#   - aws CLI configured (for S3 download)
#

set -euo pipefail

# Configuration
BACKUP_DIR="${BACKUP_DIR:-./backups}"
BACKUP_FILE=""
FROM_S3=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Parse arguments
if [ $# -eq 0 ]; then
    log_error "No backup file specified"
    echo "Usage: $0 <backup_file> | --latest | --from-s3 <s3_url>"
    exit 1
fi

case "$1" in
    --latest)
        BACKUP_FILE="${BACKUP_DIR}/latest.sql.gz"
        if [ ! -f "$BACKUP_FILE" ]; then
            log_error "No latest backup found at ${BACKUP_FILE}"
            exit 1
        fi
        ;;
    --from-s3)
        if [ -z "${2:-}" ]; then
            log_error "--from-s3 requires an S3 URL"
            exit 1
        fi
        FROM_S3="$2"
        TEMP_FILE=$(mktemp)
        BACKUP_FILE="${TEMP_FILE}.sql.gz"

        log_info "Downloading from S3: ${FROM_S3}"
        if aws s3 cp "$FROM_S3" "$BACKUP_FILE"; then
            log_info "Download completed"
        else
            log_error "Failed to download from S3"
            exit 1
        fi
        ;;
    *)
        BACKUP_FILE="$1"
        if [ ! -f "$BACKUP_FILE" ]; then
            log_error "Backup file not found: ${BACKUP_FILE}"
            exit 1
        fi
        ;;
esac

# Check if DATABASE_URL is set
if [ -z "${DATABASE_URL:-}" ]; then
    log_error "DATABASE_URL environment variable is not set"
    exit 1
fi

# Extract database connection details
if [[ $DATABASE_URL =~ postgresql://([^:]+):([^@]+)@([^:]+):([0-9]+)/(.+) ]]; then
    DB_USER="${BASH_REMATCH[1]}"
    DB_PASS="${BASH_REMATCH[2]}"
    DB_HOST="${BASH_REMATCH[3]}"
    DB_PORT="${BASH_REMATCH[4]}"
    DB_NAME="${BASH_REMATCH[5]}"
else
    log_error "Invalid DATABASE_URL format"
    exit 1
fi

log_warn "==================== WARNING ===================="
log_warn "This will REPLACE the database: ${DB_NAME}"
log_warn "Host: ${DB_HOST}"
log_warn "Backup file: ${BACKUP_FILE}"
log_warn "==============================================="
echo ""
read -p "Are you sure you want to continue? (type 'yes' to confirm): " -r
echo

if [[ ! $REPLY =~ ^yes$ ]]; then
    log_info "Restore cancelled"
    exit 0
fi

log_info "Starting database restore..."

# Set password for psql
export PGPASSWORD="$DB_PASS"

# Restore database
if gunzip < "$BACKUP_FILE" | psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" --quiet; then
    log_info "Database restore completed successfully"
else
    log_error "Database restore failed"
    exit 1
fi

# Clean up temporary file if downloaded from S3
if [ -n "$FROM_S3" ]; then
    rm -f "$BACKUP_FILE"
fi

log_info "Restore process completed successfully"

exit 0
