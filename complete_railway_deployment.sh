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

# Set environment variables
echo "Setting environment variables..."
railway variables set TELEGRAM_BOT_TOKEN="8072569977:AAH6ajboc0Tl9LHUp1VUj3eQHy_XF6naGB4"
railway variables set OPENROUTER_API_KEY="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"
railway variables set TWELVEDATA_API_KEY="14b61f5898d1412681a8dfc878f857b4"
railway variables set CHARTIMG_API_KEY="tGvkXDWnfI5G8WX6VnsIJ3xLvnfLt56x6Q8UaNbU"
railway variables set GOOGLE_SHEETS_ID="1g6vBpp3-d9C-fMYFz4P7BU_Vq5FNDd-VBzxDjw2kDLk"
railway variables set APP_NAME="Legend AI"
railway variables set DEBUG="false"
railway variables set SECRET_KEY="af10148245a5421e4df19595b6d530434ed6b4c1266636371814bad48a0b775d"

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
