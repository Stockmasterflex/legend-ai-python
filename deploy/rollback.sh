#!/bin/bash
# Rollback Script
# Reverts to a previous deployment state

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get rollback tag (default to latest pre-deploy tag)
ROLLBACK_TAG="${1:-}"

if [ -z "$ROLLBACK_TAG" ]; then
    echo -e "${YELLOW}No rollback tag specified. Finding latest pre-deploy tag...${NC}"
    ROLLBACK_TAG=$(git tag -l "pre-deploy-*" | sort -r | head -n 1)

    if [ -z "$ROLLBACK_TAG" ]; then
        echo -e "${RED}❌ No rollback tags found!${NC}"
        exit 1
    fi

    echo -e "${BLUE}Found tag: $ROLLBACK_TAG${NC}"
fi

echo -e "${YELLOW}⚠ WARNING: This will rollback to $ROLLBACK_TAG${NC}"
echo -e "${YELLOW}Current branch will be reset to this tag.${NC}"
echo ""
read -p "Continue? (yes/no): " -r
if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "Rollback cancelled."
    exit 0
fi

echo -e "${BLUE}Starting rollback to $ROLLBACK_TAG...${NC}"

# Verify tag exists
if ! git rev-parse "$ROLLBACK_TAG" >/dev/null 2>&1; then
    echo -e "${RED}❌ Tag $ROLLBACK_TAG not found!${NC}"
    exit 1
fi

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# Create backup of current state
BACKUP_TAG="rollback-backup-$(date +%Y%m%d-%H%M%S)"
git tag -f "$BACKUP_TAG"
echo -e "${GREEN}✓ Current state backed up as: $BACKUP_TAG${NC}"

# Reset to rollback tag
echo "Resetting to $ROLLBACK_TAG..."
git reset --hard "$ROLLBACK_TAG"

echo -e "${GREEN}✓ Code rolled back to $ROLLBACK_TAG${NC}"

# Restart services
echo "Restarting services..."
if command -v docker-compose &> /dev/null; then
    docker-compose down
    docker-compose up -d --build
    echo -e "${GREEN}✓ Docker services restarted${NC}"
elif [ -n "$RAILWAY_ENVIRONMENT" ]; then
    echo -e "${BLUE}Railway will automatically redeploy${NC}"
else
    echo -e "${YELLOW}⚠ Manual service restart may be required${NC}"
fi

# Notify
echo ""
echo -e "${GREEN}✓ Rollback completed!${NC}"
echo -e "${BLUE}Rolled back to: $ROLLBACK_TAG${NC}"
echo -e "${BLUE}Current state backed up as: $BACKUP_TAG${NC}"

# Send Telegram notification
if [[ -n "${TELEGRAM_BOT_TOKEN}" && -n "${TELEGRAM_CHAT_ID}" ]]; then
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d "chat_id=${TELEGRAM_CHAT_ID}" \
        -d "text=🔄 *Rollback Completed*%0A%0ATag: \`${ROLLBACK_TAG}\`%0ABackup: \`${BACKUP_TAG}\`%0ATime: $(date)" \
        -d "parse_mode=Markdown" > /dev/null 2>&1 || true
fi

exit 0
