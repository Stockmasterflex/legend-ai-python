#!/bin/bash

# Setup script for CI/CD secrets
# This script helps configure GitHub secrets for the testing pipeline

set -e

echo "🔐 Legend AI - CI/CD Secrets Setup"
echo "==================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ GitHub CLI (gh) is not installed${NC}"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check if logged in to GitHub
if ! gh auth status &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in to GitHub CLI${NC}"
    echo "Please run: gh auth login"
    exit 1
fi

echo -e "${GREEN}✓${NC} GitHub CLI is installed and authenticated"
echo ""

# Get repository info
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo "Repository: $REPO"
echo ""

# Function to set a secret
set_secret() {
    local secret_name=$1
    local secret_description=$2
    local secret_value

    echo -e "${YELLOW}Setting up: $secret_name${NC}"
    echo "$secret_description"
    echo ""

    read -p "Enter value (or press Enter to skip): " secret_value

    if [ -z "$secret_value" ]; then
        echo -e "${YELLOW}⏭️  Skipped $secret_name${NC}"
        echo ""
        return
    fi

    if gh secret set "$secret_name" --body "$secret_value"; then
        echo -e "${GREEN}✓${NC} $secret_name set successfully"
    else
        echo -e "${RED}❌${NC} Failed to set $secret_name"
    fi
    echo ""
}

# Railway Token
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1️⃣  RAILWAY TOKEN"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "To get your Railway token:"
echo "  1. Install Railway CLI: curl -fsSL https://railway.app/install.sh | sh"
echo "  2. Login: railway login"
echo "  3. Get token from: https://railway.app/account/tokens"
echo ""
set_secret "RAILWAY_TOKEN" "Railway API Token for deployment"

# Slack Webhook
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2️⃣  SLACK WEBHOOK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "To get your Slack webhook URL:"
echo "  1. Go to: https://api.slack.com/apps"
echo "  2. Create a new app or select existing"
echo "  3. Enable 'Incoming Webhooks'"
echo "  4. Add webhook to workspace"
echo "  5. Copy the webhook URL"
echo ""
set_secret "SLACK_WEBHOOK_URL" "Slack Webhook URL for notifications (starts with https://hooks.slack.com/...)"

# Telegram Bot Token
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3️⃣  TELEGRAM BOT TOKEN"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "To get your Telegram bot token:"
echo "  1. Open Telegram and search for @BotFather"
echo "  2. Send: /newbot"
echo "  3. Follow prompts to create bot"
echo "  4. Copy the token (format: 123456:ABC-DEF...)"
echo ""
set_secret "TELEGRAM_BOT_TOKEN" "Telegram Bot Token (from @BotFather)"

# Telegram Chat ID
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4️⃣  TELEGRAM CHAT ID"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "To get your Telegram chat ID:"
echo "  1. Send a message to your bot"
echo "  2. Visit: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates"
echo "  3. Look for 'chat':{'id': YOUR_CHAT_ID}"
echo "  Or use @userinfobot to get your chat ID"
echo ""
set_secret "TELEGRAM_CHAT_ID" "Telegram Chat ID (your user ID or channel ID)"

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 SETUP COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "View configured secrets:"
echo "  gh secret list"
echo ""
echo "To test your workflow:"
echo "  git push origin main"
echo ""
echo "View workflow runs:"
echo "  gh run list --workflow=test-and-deploy.yml"
echo ""
echo -e "${GREEN}✅ All done! Your CI/CD pipeline is ready.${NC}"
echo ""
echo "📚 For more information, see: .github/TESTING_SETUP.md"
