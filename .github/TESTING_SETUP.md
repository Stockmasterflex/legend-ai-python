# Testing & CI/CD Setup Guide

This document explains how to set up and use the automated testing pipeline for Legend AI.

## 📋 Table of Contents

- [Local Testing](#local-testing)
- [GitHub Actions Setup](#github-actions-setup)
- [Railway Deployment](#railway-deployment)
- [Slack Notifications](#slack-notifications)
- [Telegram Notifications](#telegram-notifications)
- [Troubleshooting](#troubleshooting)

## 🧪 Local Testing

### Running All Tests

```bash
# Run all tests with coverage
pytest

# Run specific test suites
pytest tests/test_all_detectors_unit.py        # Unit tests only
pytest tests/test_api_integration.py           # Integration tests only
pytest tests/test_performance_benchmarks.py    # Benchmarks only

# Run tests by marker
pytest -m unit                                 # Unit tests
pytest -m integration                          # Integration tests
pytest -m benchmark                            # Benchmarks
pytest -m "not slow"                          # Skip slow tests
```

### Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=app --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux

# Coverage summary in terminal
pytest --cov=app --cov-report=term-missing
```

### Performance Benchmarks

```bash
# Run all benchmarks
pytest -m benchmark -v

# Run specific benchmarks
pytest tests/test_performance_benchmarks.py::test_benchmark_vcp_detector -v

# Show slowest tests
pytest --durations=10
```

## 🚀 GitHub Actions Setup

### Automatic Triggers

The CI/CD pipeline runs automatically on:

- **Push** to `main`, `develop`, or `claude/**` branches
- **Pull requests** to `main`, `develop`, or `claude` branches

### Manual Trigger

You can manually trigger the workflow from the GitHub Actions tab.

### Workflow Jobs

1. **Unit Tests** - Tests all pattern detectors
2. **Integration Tests** - Tests all API endpoints (with Redis service)
3. **Performance Benchmarks** - Performance regression tests
4. **Full Test Suite** - Complete test coverage with metrics
5. **Security Scan** - Safety and Bandit security checks
6. **Deploy to Railway** - Automatic deployment on test pass
7. **Notifications** - Slack/Telegram alerts

## 🚂 Railway Deployment

### Setup Railway Token

1. **Get Railway Token:**
   ```bash
   # Install Railway CLI
   curl -fsSL https://railway.app/install.sh | sh

   # Login to Railway
   railway login

   # Get your token
   railway whoami
   ```

2. **Add to GitHub Secrets:**
   - Go to your repository on GitHub
   - Navigate to **Settings > Secrets and variables > Actions**
   - Click **New repository secret**
   - Name: `RAILWAY_TOKEN`
   - Value: Your Railway API token
   - Click **Add secret**

### Railway Project Setup

1. **Create Railway Project:**
   ```bash
   railway init
   ```

2. **Create Services:**
   ```bash
   # Production service
   railway service create legend-ai-production

   # Staging service (optional)
   railway service create legend-ai-staging
   ```

3. **Configure Environment:**
   ```bash
   railway variables set PYTHON_VERSION=3.11
   railway variables set REDIS_URL=<your-redis-url>
   ```

### Deployment Behavior

- **`main` branch** → Deploys to `legend-ai-production`
- **`develop` branch** → Deploys to `legend-ai-staging`
- **Other branches** → No deployment
- **Deployment only happens if all tests pass**

## 💬 Slack Notifications

### Setup Slack Webhook

1. **Create Slack App:**
   - Go to https://api.slack.com/apps
   - Click **Create New App**
   - Choose **From scratch**
   - Name: "Legend AI CI/CD"
   - Select your workspace

2. **Enable Incoming Webhooks:**
   - In your app settings, go to **Incoming Webhooks**
   - Toggle **Activate Incoming Webhooks** to On
   - Click **Add New Webhook to Workspace**
   - Select the channel for notifications
   - Click **Allow**

3. **Copy Webhook URL:**
   - Copy the **Webhook URL** (starts with `https://hooks.slack.com/...`)

4. **Add to GitHub Secrets:**
   - Go to **Settings > Secrets and variables > Actions**
   - Click **New repository secret**
   - Name: `SLACK_WEBHOOK_URL`
   - Value: Your webhook URL
   - Click **Add secret**

### Notification Format

Slack notifications include:
- ✅/❌ Test status
- Branch name
- Commit message and link
- Author
- Test duration
- Link to workflow run

## 📱 Telegram Notifications

### Setup Telegram Bot

1. **Create Bot:**
   - Open Telegram and search for [@BotFather](https://t.me/botfather)
   - Send `/newbot`
   - Follow prompts to create your bot
   - Copy the **Bot Token** (format: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)

2. **Get Chat ID:**
   ```bash
   # Method 1: Send a message to your bot, then visit:
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates

   # Look for "chat":{"id": YOUR_CHAT_ID}

   # Method 2: Use @userinfobot
   # Send any message to @userinfobot to get your chat ID
   ```

3. **Add to GitHub Secrets:**
   - **Secret 1:**
     - Name: `TELEGRAM_BOT_TOKEN`
     - Value: Your bot token from BotFather
   - **Secret 2:**
     - Name: `TELEGRAM_CHAT_ID`
     - Value: Your chat ID (or channel ID like `-1001234567890`)

### Notification Format

Telegram notifications include:
- ✅/❌ Test status (with emoji)
- Branch name
- Commit message
- Author
- Test duration
- Direct link to workflow run

## 🔧 Troubleshooting

### Tests Fail Locally But Pass in CI

```bash
# Ensure same Python version
python --version  # Should be 3.11

# Clear cache and reinstall
pip cache purge
pip install -r requirements.txt --force-reinstall

# Clear pytest cache
rm -rf .pytest_cache __pycache__
```

### Redis Connection Errors in Integration Tests

```bash
# Start local Redis
docker run -d -p 6379:6379 redis:7-alpine

# Or use system Redis
redis-server

# Set environment variable
export REDIS_URL=redis://localhost:6379
```

### Coverage Too Low

```bash
# Identify uncovered code
pytest --cov=app --cov-report=term-missing

# Focus on specific modules
pytest --cov=app.core.detectors --cov-report=html
```

### Performance Benchmarks Failing

```bash
# Run benchmarks with detailed output
pytest tests/test_performance_benchmarks.py -v -s

# Skip benchmarks during development
pytest -m "not benchmark"
```

### Railway Deployment Fails

```bash
# Check Railway CLI
railway --version

# Verify authentication
railway whoami

# Check deployment logs
railway logs

# Manual deployment
railway up --service legend-ai-production
```

### Notifications Not Sending

1. **Verify Secrets:**
   ```bash
   # Check if secrets are set in GitHub
   # Go to Settings > Secrets > Actions
   # Ensure SLACK_WEBHOOK_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID exist
   ```

2. **Test Slack Webhook:**
   ```bash
   curl -X POST YOUR_SLACK_WEBHOOK_URL \
     -H 'Content-Type: application/json' \
     -d '{"text":"Test from Legend AI"}'
   ```

3. **Test Telegram Bot:**
   ```bash
   curl "https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=Test"
   ```

## 📊 Monitoring Test Health

### View Test Trends

- Go to **Actions** tab in GitHub
- Click on **Test & Deploy** workflow
- View success/failure trends over time

### Coverage Trends

- Download coverage artifacts from workflow runs
- Compare `coverage.json` across runs
- Use tools like [Codecov](https://codecov.io) for visualization

### Performance Monitoring

- Review benchmark results in workflow artifacts
- Compare durations across runs
- Set up alerts for performance regressions

## 🎯 Best Practices

1. **Run tests locally before pushing:**
   ```bash
   pytest -v
   ```

2. **Write tests for new features:**
   - Unit tests for detectors
   - Integration tests for API endpoints
   - Benchmarks for performance-critical code

3. **Keep coverage above 60%:**
   - Aim for 80%+ on critical modules
   - Use `pytest --cov-report=term-missing` to find gaps

4. **Monitor performance:**
   - Run benchmarks regularly
   - Investigate slowdowns immediately

5. **Review CI logs:**
   - Check for warnings
   - Monitor resource usage
   - Optimize slow tests

## 📚 Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Railway Documentation](https://docs.railway.app/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Slack API Documentation](https://api.slack.com/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

**Need help?** Open an issue or reach out to the team!
