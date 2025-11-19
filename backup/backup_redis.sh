#!/bin/bash
# Redis Backup Script
# Creates Redis snapshot backups

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="${BACKUP_DIR:-${SCRIPT_DIR}/backups/redis}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

log_info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

log_success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

log_info "Starting Redis backup..."

# Parse REDIS_URL if available
if [[ -n "$REDIS_URL" ]]; then
    if [[ $REDIS_URL =~ redis://([^:@]+:)?([^@]+)@([^:]+):([0-9]+) ]]; then
        REDIS_PASSWORD="${BASH_REMATCH[2]}"
        REDIS_HOST="${BASH_REMATCH[3]}"
        REDIS_PORT="${BASH_REMATCH[4]}"
    elif [[ $REDIS_URL =~ redis://([^:]+):([0-9]+) ]]; then
        REDIS_HOST="${BASH_REMATCH[1]}"
        REDIS_PORT="${BASH_REMATCH[2]}"
    else
        REDIS_HOST="localhost"
        REDIS_PORT="6379"
    fi
else
    REDIS_HOST="${REDIS_HOST:-localhost}"
    REDIS_PORT="${REDIS_PORT:-6379}"
fi

log_info "Redis: $REDIS_HOST:$REDIS_PORT"

# Trigger BGSAVE
if command -v redis-cli &> /dev/null; then
    REDIS_CMD="redis-cli -h $REDIS_HOST -p $REDIS_PORT"

    if [[ -n "$REDIS_PASSWORD" ]]; then
        REDIS_CMD="$REDIS_CMD -a $REDIS_PASSWORD"
    fi

    # Trigger background save
    $REDIS_CMD BGSAVE > /dev/null 2>&1 || {
        log_error "Failed to trigger BGSAVE"
        exit 1
    }

    log_info "BGSAVE triggered, waiting for completion..."

    # Wait for BGSAVE to complete
    while true; do
        STATUS=$($REDIS_CMD LASTSAVE 2>/dev/null || echo "0")
        sleep 1
        NEW_STATUS=$($REDIS_CMD LASTSAVE 2>/dev/null || echo "0")

        if [[ "$NEW_STATUS" != "$STATUS" ]]; then
            break
        fi
    done

    log_success "✓ Redis snapshot created"

    # Get dump.rdb location
    RDB_FILE=$($REDIS_CMD CONFIG GET dir | tail -n 1)/dump.rdb

    if [[ -f "$RDB_FILE" ]]; then
        cp "$RDB_FILE" "${BACKUP_DIR}/dump_${TIMESTAMP}.rdb"
        log_success "✓ Snapshot backed up: ${BACKUP_DIR}/dump_${TIMESTAMP}.rdb"
    else
        log_error "Could not find Redis dump file at: $RDB_FILE"
    fi
else
    log_error "redis-cli not found. Install redis-tools or redis package."
    exit 1
fi

# Export all keys to JSON (fallback method)
log_info "Exporting keys to JSON..."

cat > /tmp/redis_export.py <<'PYTHON'
import redis
import json
import os
import sys

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
r = redis.from_url(redis_url)

data = {}
keys = r.keys('*')

for key in keys:
    key_str = key.decode('utf-8')
    key_type = r.type(key).decode('utf-8')

    try:
        if key_type == 'string':
            data[key_str] = r.get(key).decode('utf-8')
        elif key_type == 'hash':
            data[key_str] = {k.decode('utf-8'): v.decode('utf-8') for k, v in r.hgetall(key).items()}
        elif key_type == 'list':
            data[key_str] = [v.decode('utf-8') for v in r.lrange(key, 0, -1)]
        elif key_type == 'set':
            data[key_str] = [v.decode('utf-8') for v in r.smembers(key)]
        elif key_type == 'zset':
            data[key_str] = [(v.decode('utf-8'), score) for v, score in r.zrange(key, 0, -1, withscores=True)]
    except Exception as e:
        print(f"Error exporting key {key_str}: {e}", file=sys.stderr)

print(json.dumps(data, indent=2))
PYTHON

if command -v python3 &> /dev/null; then
    python3 /tmp/redis_export.py > "${BACKUP_DIR}/redis_keys_${TIMESTAMP}.json" 2>/dev/null || {
        log_error "Failed to export Redis keys"
    }

    if [[ -f "${BACKUP_DIR}/redis_keys_${TIMESTAMP}.json" ]]; then
        log_success "✓ Keys exported to JSON"
    fi
fi

# Cleanup old backups (keep 7 days)
find "$BACKUP_DIR" -name "dump_*.rdb" -mtime +7 -delete
find "$BACKUP_DIR" -name "redis_keys_*.json" -mtime +7 -delete

log_success "Redis backup completed!"
ls -lh "$BACKUP_DIR" | tail -5
