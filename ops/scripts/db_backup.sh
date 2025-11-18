#!/bin/bash
#
# Database Backup Script for Legend AI (PostgreSQL)
#
# This script creates compressed backups of the PostgreSQL database
# and optionally uploads them to cloud storage.
#
# Usage:
#   ./db_backup.sh [options]
#
# Options:
#   --keep-days N    Keep backups for N days (default: 7)
#   --s3-bucket      S3 bucket for remote backup (optional)
#   --local-only     Skip remote upload
#
# Requirements:
#   - pg_dump installed
#   - DATABASE_URL environment variable set
#   - aws CLI configured (for S3 upload)
#

set -euo pipefail

# Configuration
BACKUP_DIR="${BACKUP_DIR:-./backups}"
KEEP_DAYS="${KEEP_DAYS:-7}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
S3_BUCKET="${S3_BUCKET:-}"
LOCAL_ONLY=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --keep-days)
            KEEP_DAYS="$2"
            shift 2
            ;;
        --s3-bucket)
            S3_BUCKET="$2"
            shift 2
            ;;
        --local-only)
            LOCAL_ONLY=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

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

# Check if DATABASE_URL is set
if [ -z "${DATABASE_URL:-}" ]; then
    log_error "DATABASE_URL environment variable is not set"
    exit 1
fi

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Extract database connection details from DATABASE_URL
# Format: postgresql://user:password@host:port/dbname
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

# Backup filename
BACKUP_FILE="${BACKUP_DIR}/legendai_${DB_NAME}_${TIMESTAMP}.sql.gz"

log_info "Starting database backup..."
log_info "Database: ${DB_NAME}"
log_info "Host: ${DB_HOST}"
log_info "Backup file: ${BACKUP_FILE}"

# Create backup
export PGPASSWORD="$DB_PASS"

if pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
    --verbose \
    --format=plain \
    --no-owner \
    --no-acl \
    --clean \
    --if-exists \
    | gzip > "$BACKUP_FILE"; then

    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    log_info "Backup completed successfully (size: ${BACKUP_SIZE})"
else
    log_error "Backup failed"
    exit 1
fi

# Upload to S3 if configured
if [ "$LOCAL_ONLY" = false ] && [ -n "$S3_BUCKET" ]; then
    log_info "Uploading to S3: s3://${S3_BUCKET}/backups/$(basename "$BACKUP_FILE")"

    if command -v aws &> /dev/null; then
        if aws s3 cp "$BACKUP_FILE" "s3://${S3_BUCKET}/backups/" --storage-class STANDARD_IA; then
            log_info "S3 upload completed successfully"
        else
            log_warn "S3 upload failed, but local backup is available"
        fi
    else
        log_warn "AWS CLI not found, skipping S3 upload"
    fi
fi

# Clean up old backups
log_info "Cleaning up backups older than ${KEEP_DAYS} days..."
find "$BACKUP_DIR" -name "legendai_*.sql.gz" -type f -mtime +${KEEP_DAYS} -delete
REMAINING=$(find "$BACKUP_DIR" -name "legendai_*.sql.gz" -type f | wc -l)
log_info "Cleanup complete. ${REMAINING} backups remaining."

# Create a "latest" symlink
ln -sf "$(basename "$BACKUP_FILE")" "${BACKUP_DIR}/latest.sql.gz"

log_info "Backup process completed successfully"
log_info "Backup location: ${BACKUP_FILE}"

# Print backup information
cat <<EOF

Backup Summary:
--------------
Timestamp:     $TIMESTAMP
Database:      $DB_NAME
File:          $BACKUP_FILE
Size:          $BACKUP_SIZE
Retention:     $KEEP_DAYS days
EOF

if [ "$LOCAL_ONLY" = false ] && [ -n "$S3_BUCKET" ]; then
    echo "S3 Location:   s3://${S3_BUCKET}/backups/$(basename "$BACKUP_FILE")"
fi

exit 0
