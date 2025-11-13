#!/bin/bash
# Production endpoint testing script

BASE_URL="${1:-https://legend-ai-python-production.up.railway.app}"

echo "🧪 Testing Legend AI Production Endpoints"
echo "=========================================="
echo "Base URL: $BASE_URL"
echo ""

# Test health endpoint
echo "1️⃣ Testing /health..."
HEALTH=$(curl -s "$BASE_URL/health")
echo "$HEALTH" | python3 -m json.tool 2>/dev/null || echo "$HEALTH"
echo ""

# Test version endpoint
echo "2️⃣ Testing /version..."
VERSION=$(curl -s "$BASE_URL/version")
echo "$VERSION" | python3 -m json.tool 2>/dev/null || echo "$VERSION"
echo ""

# Test analyze endpoint (without requiring params)
echo "3️⃣ Testing /api/analyze (expect 422 without params)..."
ANALYZE=$(curl -s "$BASE_URL/api/analyze")
echo "$ANALYZE" | python3 -m json.tool 2>/dev/null | head -20
echo ""

# Test analyze with params
echo "4️⃣ Testing /api/analyze?ticker=AAPL&tf=daily..."
ANALYZE_FULL=$(curl -s "$BASE_URL/api/analyze?ticker=AAPL&tf=daily")
echo "$ANALYZE_FULL" | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"✅ Success: {d.get('success')}\"); print(f\"   Chart URL: {d.get('chart_url', 'N/A')[:80]}...\"); print(f\"   Patterns: {list(d.get('patterns', {}).keys()) if d.get('patterns') else 'N/A'}\")" 2>/dev/null || echo "❌ Failed"
echo ""

# Test scan endpoint (disabled by default)
echo "5️⃣ Testing /api/scan (expect disabled or enabled)..."
SCAN=$(curl -s "$BASE_URL/api/scan?limit=5")
echo "$SCAN" | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"   Status: {d.get('meta', {}).get('reason', 'enabled')}\"); print(f\"   Results: {len(d.get('results', []))}\"); print(f\"   Universe: {d.get('universe_size', 0)}\")" 2>/dev/null || echo "$SCAN" | head -10
echo ""

# Test top setups
echo "6️⃣ Testing /api/top-setups..."
SETUPS=$(curl -s "$BASE_URL/api/top-setups?limit=3")
echo "$SETUPS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"   Success: {d.get('success')}\"); print(f\"   Count: {d.get('count')}\"); print(f\"   Cached: {d.get('cached')}\")" 2>/dev/null || echo "$SETUPS" | head -10
echo ""

# Test watchlist
echo "7️⃣ Testing /api/watchlist..."
WATCHLIST=$(curl -s "$BASE_URL/api/watchlist")
echo "$WATCHLIST" | python3 -m json.tool 2>/dev/null | head -15
echo ""

# Test market internals
echo "8️⃣ Testing /api/market/internals..."
INTERNALS=$(curl -s "$BASE_URL/api/market/internals")
echo "$INTERNALS" | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"   SPY Price: {d.get('data', {}).get('spy_price')}\"); print(f\"   Cached: {d.get('cached')}\")" 2>/dev/null || echo "$INTERNALS" | head -10
echo ""

# Test metrics endpoint
echo "9️⃣ Testing /api/metrics (Prometheus)..."
METRICS=$(curl -s "$BASE_URL/api/metrics" | head -20)
echo "$METRICS"
echo ""

# Test dashboard
echo "🔟 Testing /dashboard..."
DASH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/dashboard")
echo "   HTTP Status: $DASH_STATUS"
echo ""

echo "✅ All endpoint tests complete!"
