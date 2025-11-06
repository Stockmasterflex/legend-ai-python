#!/bin/bash

# Test script for dashboard and Telegram fixes
# Tests the critical issues that were just fixed

API_BASE="${1:-https://legend-ai-python-production.up.railway.app}"
CHAT_ID="${2:-999999999}"  # dummy chat ID for testing

echo "=========================================="
echo "Testing Dashboard & Telegram Fixes"
echo "API Base: $API_BASE"
echo "=========================================="

# Test 1: Pattern Detection (Dashboard feature)
echo -e "\n✅ TEST 1: Pattern Detection (Dashboard)"
echo "Testing: /api/patterns/detect"
curl -s -X POST "$API_BASE/api/patterns/detect" \
  -H "Content-Type: application/json" \
  -d '{"ticker":"NVDA","interval":"1day"}' | jq -r '.data | "Pattern: \(.pattern), Score: \(.score)/10"' 2>/dev/null || echo "❌ No response"

# Test 2: Watchlist (Dashboard feature)
echo -e "\n✅ TEST 2: Watchlist Get"
echo "Testing: /api/watchlist"
curl -s -X GET "$API_BASE/api/watchlist" \
  -H "Content-Type: application/json" | jq -r 'if .success then "✅ Watchlist accessible (\(.items | length) items)" else "❌ Failed" end' 2>/dev/null || echo "❌ No response"

# Test 3: Watchlist Add (Dashboard feature)
echo -e "\n✅ TEST 3: Add to Watchlist"
echo "Testing: /api/watchlist/add"
curl -s -X POST "$API_BASE/api/watchlist/add" \
  -H "Content-Type: application/json" \
  -d '{"ticker":"TSLA","reason":"Test"}' | jq -r 'if .success then "✅ Add successful" else "❌ Failed: " + (.detail // "unknown") end' 2>/dev/null || echo "❌ No response"

# Test 4: Telegram Webhook (CRITICAL FIX)
echo -e "\n✅ TEST 4: Telegram Webhook"
echo "Testing: /api/webhook/telegram (CRITICAL - was /api/api/webhook/telegram)"
curl -s -X POST "$API_BASE/api/webhook/telegram" \
  -H "Content-Type: application/json" \
  -d "{\"update_id\":1,\"message\":{\"message_id\":1,\"chat\":{\"id\":$CHAT_ID},\"text\":\"/help\"}}" | jq -r 'if .ok then "✅ Telegram endpoint working" else "❌ Failed" end' 2>/dev/null || echo "❌ No response"

# Test 5: Health Check
echo -e "\n✅ TEST 5: API Health"
echo "Testing: /health"
curl -s -X GET "$API_BASE/health" | jq -r 'if .status then "✅ API Status: \(.status)" else "❌ Failed" end' 2>/dev/null || echo "❌ No response"

echo -e "\n=========================================="
echo "Testing Complete!"
echo "=========================================="
