#!/bin/bash
# Legend AI - Complete Deployment Script
# This script handles GitHub push and Railway deployment

set -e

echo '🚀 Legend AI - Complete Deployment Script'
echo '=========================================='

# Check if GitHub remote is configured
if ! git remote get-url origin > /dev/null 2>&1; then
    echo '❌ GitHub remote not configured!'
    echo 'Please provide your GitHub repository URL:'
    echo 'Example: https://github.com/YOUR_USERNAME/legend-ai-python.git'
    read -p 'GitHub URL: ' GITHUB_URL
    
    if [ -z "$GITHUB_URL" ]; then
        echo '❌ No GitHub URL provided. Exiting.'
        exit 1
    fi
    
    echo "📤 Adding GitHub remote: $GITHUB_URL"
    git remote add origin "$GITHUB_URL"
fi

echo '📤 Pushing code to GitHub...'
git push -u origin master

echo '✅ Code pushed to GitHub successfully!'

echo ''
echo '🎯 Next Steps:'
echo '1. Go to https://railway.app/dashboard'
echo '2. Click "New Project" → "Deploy from GitHub"'
echo '3. Search for and select: legend-ai-python'
echo '4. Railway will auto-deploy using the Dockerfile'
echo ''
echo '5. Add PostgreSQL and Redis plugins in Railway'
echo '6. Set environment variables in Railway dashboard'
echo '7. Update Telegram webhook with Railway URL'
echo ''
echo '🔗 Your GitHub repository is ready for Railway deployment!'

