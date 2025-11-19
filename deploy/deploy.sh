#!/bin/bash
# Legend AI - One-Click Deployment Script
# This script automates the entire deployment process with validation and rollback

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_FILE="${SCRIPT_DIR}/logs/deploy_$(date +%Y%m%d_%H%M%S).log"
ROLLBACK_TAG="pre-deploy-$(date +%Y%m%d-%H%M%S)"

# Create logs directory
mkdir -p "${SCRIPT_DIR}/logs"

# Logging function
log() {
    echo -e "${2:-$NC}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
}

log_success() { log "$1" "$GREEN"; }
log_error() { log "$1" "$RED"; }
log_warning() { log "$1" "$YELLOW"; }
log_info() { log "$1" "$BLUE"; }

# Telegram notification function
send_telegram() {
    local message="$1"
    if [[ -n "${TELEGRAM_BOT_TOKEN}" && -n "${TELEGRAM_CHAT_ID}" ]]; then
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d "chat_id=${TELEGRAM_CHAT_ID}" \
            -d "text=${message}" \
            -d "parse_mode=Markdown" > /dev/null 2>&1 || true
    fi
}

# Error handler
handle_error() {
    log_error "❌ Deployment failed at step: $1"
    send_telegram "🚨 *Deployment Failed*%0A%0AStep: $1%0ATime: $(date)%0A%0ACheck logs: ${LOG_FILE}"

    log_warning "Starting automatic rollback..."
    bash "${SCRIPT_DIR}/rollback.sh" "$ROLLBACK_TAG"
    exit 1
}

# Main deployment process
main() {
    log_info "🚀 Starting Legend AI Deployment"
    log_info "================================================"

    cd "$PROJECT_ROOT"

    # Step 1: Pre-deployment validation
    log_info "Step 1/7: Running pre-deployment validation..."
    if ! bash "${SCRIPT_DIR}/pre-deploy-check.sh"; then
        handle_error "Pre-deployment validation"
    fi
    log_success "✓ Pre-deployment validation passed"

    # Step 2: Create rollback point
    log_info "Step 2/7: Creating rollback point..."
    git tag -f "$ROLLBACK_TAG" || handle_error "Creating rollback tag"
    log_success "✓ Rollback point created: $ROLLBACK_TAG"

    # Step 3: Environment variable check
    log_info "Step 3/7: Checking environment variables..."
    if ! python "${SCRIPT_DIR}/check_env_vars.py"; then
        handle_error "Environment variable validation"
    fi
    log_success "✓ Environment variables validated"

    # Step 4: Database migrations
    log_info "Step 4/7: Running database migrations..."
    if ! python "${SCRIPT_DIR}/run_migrations.py"; then
        handle_error "Database migrations"
    fi
    log_success "✓ Database migrations completed"

    # Step 5: Build and deploy
    log_info "Step 5/7: Building application..."

    # For Railway deployment
    if [[ -n "${RAILWAY_ENVIRONMENT}" ]]; then
        log_info "Detected Railway environment - deployment handled by Railway"
    # For Docker deployment
    elif command -v docker &> /dev/null; then
        log_info "Building Docker image..."
        docker-compose build || handle_error "Docker build"
        docker-compose up -d || handle_error "Docker deployment"
    else
        log_info "Starting application with uvicorn..."
        source venv/bin/activate 2>/dev/null || true
        pip install -r requirements.txt || handle_error "Dependencies installation"
    fi
    log_success "✓ Application deployed"

    # Step 6: Wait for application to start
    log_info "Step 6/7: Waiting for application to start (30s)..."
    sleep 30

    # Step 7: Post-deployment smoke tests
    log_info "Step 7/7: Running smoke tests..."
    if ! bash "${SCRIPT_DIR}/smoke-tests.sh"; then
        handle_error "Smoke tests"
    fi
    log_success "✓ Smoke tests passed"

    # Success!
    log_success "================================================"
    log_success "🎉 Deployment completed successfully!"
    log_success "Deployed at: $(date)"
    log_success "Rollback tag: $ROLLBACK_TAG"

    send_telegram "✅ *Deployment Successful*%0A%0ATime: $(date)%0ARollback tag: \`${ROLLBACK_TAG}\`%0A%0AAll systems operational!"
}

# Run main deployment
main "$@"
