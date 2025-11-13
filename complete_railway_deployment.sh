#!/bin/bash
# Complete Railway deployment script
# Run this AFTER railway login is complete

set -e

echo "🚀 Completing Legend AI Railway Deployment"
echo "=========================================="

# Verify authentication
echo "Checking Railway authentication..."
railway whoami

# Create project from GitHub
echo "Creating Railway project from GitHub..."
railway link --project "legend-ai-python" 2>/dev/null || echo "Project already linked or not found"

# If project doesn't exist, create from GitHub
if ! railway status > /dev/null 2>&1; then
    echo "Creating new project from GitHub repository..."
    echo "Please go to https://railway.app/dashboard and:"
    echo "1. Click 'New Project'"
    echo "2. Click 'Deploy from GitHub'"
    echo "3. Search for 'legend-ai-python'"
    echo "4. Select the repository and deploy"
    echo ""
    echo "Then run: railway link"
    exit 1
fi

echo "✅ Project linked successfully"

# Add PostgreSQL
echo "Adding PostgreSQL database..."
railway add postgres

# Add Redis
echo "Adding Redis cache..."
railway add redis

# Set environment variables (use your own values)
echo "Setting environment variables..."
railway variables set TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-your-telegram-bot-token}"
railway variables set OPENROUTER_API_KEY="${OPENROUTER_API_KEY:-your-openrouter-api-key}"
railway variables set TWELVEDATA_API_KEY="${TWELVEDATA_API_KEY:-your-twelvedata-api-key}"
railway variables set CHARTIMG_API_KEY="${CHARTIMG_API_KEY:-your-chartimg-api-key}"
railway variables set APP_NAME="Legend AI"
railway variables set DEBUG="false"
railway variables set SECRET_KEY="${SECRET_KEY:-change-me}"

echo "✅ Environment variables set"

# Deploy
echo "Deploying application..."
railway deploy

# Get project URL
echo "Getting deployment URL..."
PROJECT_URL=$(railway domain)
echo "🚀 Deployment complete!"
echo "📍 Project URL: $PROJECT_URL"
echo ""
echo "Next steps:"
echo "1. Test health: curl $PROJECT_URL/health"
echo "2. Set webhook: Update Telegram webhook URL"
echo "3. Test bot commands"
echo ""
echo "🎉 Legend AI is now live on Railway!"
