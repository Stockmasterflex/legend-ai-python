#!/bin/bash
# Universe Data Backup Script
# Backs up stock universe data and watchlist

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="${BACKUP_DIR:-${SCRIPT_DIR}/backups/universe}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

log_info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

log_success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

log_info "Starting universe data backup..."

# Backup universe seed data
if [[ -f "${PROJECT_ROOT}/data/universe_seed.json" ]]; then
    cp "${PROJECT_ROOT}/data/universe_seed.json" "${BACKUP_DIR}/universe_seed_${TIMESTAMP}.json"
    log_success "✓ Universe seed data backed up"
fi

# Backup watchlist (if exists)
if [[ -f "${PROJECT_ROOT}/data/watchlist.json" ]]; then
    cp "${PROJECT_ROOT}/data/watchlist.json" "${BACKUP_DIR}/watchlist_${TIMESTAMP}.json"
    log_success "✓ Watchlist data backed up"
fi

# Backup any other data files
if [[ -d "${PROJECT_ROOT}/data" ]]; then
    tar -czf "${BACKUP_DIR}/data_full_${TIMESTAMP}.tar.gz" -C "${PROJECT_ROOT}" data/
    log_success "✓ Full data directory backed up"
fi

# Create manifest
cat > "${BACKUP_DIR}/manifest_${TIMESTAMP}.json" <<EOF
{
    "timestamp": "$(date -Iseconds)",
    "files": [
        "universe_seed_${TIMESTAMP}.json",
        "watchlist_${TIMESTAMP}.json",
        "data_full_${TIMESTAMP}.tar.gz"
    ]
}
EOF

# Cleanup old backups (keep 30 days)
find "$BACKUP_DIR" -name "*.json" -mtime +30 -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +30 -delete

log_success "Universe backup completed!"
ls -lh "$BACKUP_DIR" | tail -5
