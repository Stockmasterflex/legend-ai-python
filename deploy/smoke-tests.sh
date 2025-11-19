#!/bin/bash
# Post-deployment smoke tests
# Quick validation that critical endpoints are working

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Determine base URL
if [ -n "$RAILWAY_PUBLIC_DOMAIN" ]; then
    BASE_URL="https://${RAILWAY_PUBLIC_DOMAIN}"
elif [ -n "$BASE_URL" ]; then
    BASE_URL="$BASE_URL"
else
    BASE_URL="http://localhost:8000"
fi

echo -e "${BLUE}Running smoke tests against: ${BASE_URL}${NC}\n"

# Test counter
PASSED=0
FAILED=0

# Test function
test_endpoint() {
    local name="$1"
    local endpoint="$2"
    local expected_status="${3:-200}"

    echo -n "Testing $name... "

    response=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}${endpoint}" 2>&1)

    if [ "$response" = "$expected_status" ]; then
        echo -e "${GREEN}✓ Passed (HTTP $response)${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ Failed (HTTP $response, expected $expected_status)${NC}"
        ((FAILED++))
        return 1
    fi
}

# Test health endpoint
test_endpoint "Health Check" "/health" "200"

# Test healthz endpoint
test_endpoint "Kubernetes Health" "/healthz" "200"

# Test version endpoint
test_endpoint "Version Info" "/api/version" "200"

# Test metrics endpoint
test_endpoint "Prometheus Metrics" "/metrics" "200"

# Test analyze endpoint (should return 422 without params, not 500)
echo -n "Testing Analyze Endpoint... "
response=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/api/analyze" 2>&1)
if [ "$response" = "200" ] || [ "$response" = "422" ]; then
    echo -e "${GREEN}✓ Passed (HTTP $response)${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ Failed (HTTP $response)${NC}"
    ((FAILED++))
fi

# Test scan endpoint
echo -n "Testing Scan Endpoint... "
response=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/api/scan?limit=5" 2>&1)
if [ "$response" = "200" ] || [ "$response" = "422" ]; then
    echo -e "${GREEN}✓ Passed (HTTP $response)${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ Failed (HTTP $response)${NC}"
    ((FAILED++))
fi

# Test watchlist endpoint
test_endpoint "Watchlist" "/api/watchlist" "200"

# Test detailed health check
echo -n "Testing Detailed Health... "
health_response=$(curl -s "${BASE_URL}/health/detailed" 2>&1)
if echo "$health_response" | grep -q "status"; then
    echo -e "${GREEN}✓ Passed${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ Failed${NC}"
    ((FAILED++))
fi

# Detailed health check for Redis
echo -n "Checking Redis connection... "
if echo "$health_response" | grep -q '"redis".*"configured"'; then
    echo -e "${GREEN}✓ Configured${NC}"
elif echo "$health_response" | grep -q '"redis".*"not_configured"'; then
    echo -e "${YELLOW}⚠ Not configured${NC}"
else
    echo -e "${YELLOW}⚠ Unknown status${NC}"
fi

# Check Telegram bot
echo -n "Checking Telegram bot... "
if echo "$health_response" | grep -q '"telegram".*"configured"'; then
    echo -e "${GREEN}✓ Configured${NC}"
elif echo "$health_response" | grep -q '"telegram".*"not_configured"'; then
    echo -e "${YELLOW}⚠ Not configured${NC}"
else
    echo -e "${YELLOW}⚠ Unknown status${NC}"
fi

# Summary
echo ""
echo "========================================"
echo -e "Smoke Test Results:"
echo -e "  ${GREEN}Passed: $PASSED${NC}"
echo -e "  ${RED}Failed: $FAILED${NC}"
echo "========================================"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All smoke tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some smoke tests failed!${NC}"
    exit 1
fi
