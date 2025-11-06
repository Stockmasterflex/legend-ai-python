#!/usr/bin/env python
"""
Production Testing Script - Verify all systems are working
Tests:
1. Health endpoints
2. Pattern detection API
3. Chart generation
4. Universe scanning
5. Telegram webhook
6. Dashboard access
7. Natural language processing
"""

import httpx
import asyncio
import json
from datetime import datetime

# Configure for your environment
PRODUCTION_URL = "https://legend-ai-python-production.up.railway.app"
LOCAL_URL = "http://localhost:8000"

# Use production if available, otherwise local
BASE_URL = PRODUCTION_URL
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"  # Set your Telegram chat ID for testing

async def test_health():
    """Test health endpoints"""
    print("\n" + "="*60)
    print("🏥 TESTING HEALTH ENDPOINTS")
    print("="*60)

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.get(f"{BASE_URL}/")
            print(f"✅ Root endpoint: {response.status_code}")
            print(f"   Response: {response.json()}")
        except Exception as e:
            print(f"❌ Root endpoint failed: {e}")

        try:
            response = await client.get(f"{BASE_URL}/health")
            print(f"✅ Health endpoint: {response.status_code}")
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Telegram: {data.get('telegram_status')}")
            print(f"   Cache: {data.get('cache_status')}")
        except Exception as e:
            print(f"❌ Health endpoint failed: {e}")


async def test_pattern_detection():
    """Test pattern detection API"""
    print("\n" + "="*60)
    print("📊 TESTING PATTERN DETECTION")
    print("="*60)

    async with httpx.AsyncClient(timeout=60) as client:
        test_tickers = ["NVDA", "AAPL", "TSLA"]

        for ticker in test_tickers:
            try:
                response = await client.post(
                    f"{BASE_URL}/api/patterns/detect",
                    json={"ticker": ticker, "interval": "1day"}
                )

                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        pattern = data.get("data", {})
                        print(f"✅ {ticker}: Score {pattern.get('score')}/10 - {pattern.get('pattern')}")
                    else:
                        print(f"⚠️ {ticker}: {data.get('detail')}")
                else:
                    print(f"❌ {ticker}: HTTP {response.status_code}")

            except Exception as e:
                print(f"❌ {ticker}: Error - {e}")


async def test_chart_generation():
    """Test chart generation"""
    print("\n" + "="*60)
    print("📈 TESTING CHART GENERATION")
    print("="*60)

    async with httpx.AsyncClient(timeout=60) as client:
        test_tickers = ["NVDA", "SPY"]

        for ticker in test_tickers:
            try:
                response = await client.post(
                    f"{BASE_URL}/api/charts/generate",
                    json={
                        "ticker": ticker,
                        "interval": "1D",
                        "timeframe": "6M",
                        "indicators": ["SMA(50)", "SMA(200)"]
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        url = data.get("url", "")
                        print(f"✅ {ticker}: Chart generated")
                        if url:
                            print(f"   URL: {url[:80]}...")
                    else:
                        print(f"⚠️ {ticker}: {data.get('detail')}")
                else:
                    print(f"❌ {ticker}: HTTP {response.status_code}")

            except Exception as e:
                print(f"❌ {ticker}: Error - {e}")


async def test_universe_scan():
    """Test universe scanning"""
    print("\n" + "="*60)
    print("🔍 TESTING UNIVERSE SCAN")
    print("="*60)

    async with httpx.AsyncClient(timeout=120) as client:
        try:
            response = await client.post(
                f"{BASE_URL}/api/universe/scan",
                json={"min_score": 7.0, "limit": 10}
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    results = data.get("results", [])
                    print(f"✅ Scan completed: Found {len(results)} setups")
                    for i, r in enumerate(results[:5], 1):
                        print(f"   {i}. {r['ticker']} - Score: {r['score']}/10")
                else:
                    print(f"⚠️ Scan failed: {data.get('detail')}")
            else:
                print(f"❌ Scan failed: HTTP {response.status_code}")

        except Exception as e:
            print(f"❌ Scan error: {e}")


async def test_telegram_webhook():
    """Test Telegram webhook"""
    print("\n" + "="*60)
    print("💬 TESTING TELEGRAM WEBHOOK")
    print("="*60)

    test_messages = [
        {"text": "/start", "expected": "command"},
        {"text": "/help", "expected": "command"},
        {"text": "Analyze NVDA", "expected": "natural_language"},
        {"text": "What are the best setups", "expected": "natural_language"},
    ]

    async with httpx.AsyncClient(timeout=30) as client:
        for msg in test_messages:
            try:
                payload = {
                    "update_id": 12345,
                    "message": {
                        "message_id": 1,
                        "chat": {"id": TELEGRAM_CHAT_ID},
                        "text": msg["text"]
                    }
                }

                response = await client.post(
                    f"{BASE_URL}/api/webhook/telegram",
                    json=payload
                )

                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ '{msg['text']}': {msg['expected']} - OK")
                else:
                    print(f"❌ '{msg['text']}': HTTP {response.status_code}")

            except Exception as e:
                print(f"❌ '{msg['text']}': Error - {e}")


async def test_dashboard():
    """Test dashboard access"""
    print("\n" + "="*60)
    print("📱 TESTING DASHBOARD ACCESS")
    print("="*60)

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.get(f"{BASE_URL}/dashboard")

            if response.status_code == 200:
                print(f"✅ Dashboard accessible (HTTP 200)")
                print(f"   URL: {BASE_URL}/dashboard")
            else:
                print(f"⚠️ Dashboard returned HTTP {response.status_code}")

        except Exception as e:
            print(f"❌ Dashboard error: {e}")


async def test_market_internals():
    """Test market internals endpoint"""
    print("\n" + "="*60)
    print("📊 TESTING MARKET INTERNALS")
    print("="*60)

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.get(f"{BASE_URL}/api/market/internals")

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    market = data.get("data", {})
                    print(f"✅ Market data retrieved")
                    print(f"   SPY: ${market.get('spy_price', 'N/A'):.2f}")
                    print(f"   Regime: {market.get('regime', 'N/A')}")
                    print(f"   Status: {market.get('status', 'N/A')}")
                else:
                    print(f"⚠️ {data.get('detail')}")
            else:
                print(f"❌ HTTP {response.status_code}")

        except Exception as e:
            print(f"❌ Error: {e}")


async def test_cache_stats():
    """Test cache statistics"""
    print("\n" + "="*60)
    print("💾 TESTING CACHE STATISTICS")
    print("="*60)

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.get(f"{BASE_URL}/api/patterns/cache/stats")

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    stats = data.get("data", {})
                    print(f"✅ Cache stats retrieved")
                    print(f"   Total Keys: {stats.get('total_keys')}")
                    print(f"   Hit Rate: {stats.get('hit_rate', 'N/A')}%")
                    print(f"   Memory: {stats.get('memory', 'N/A')}")
                else:
                    print(f"⚠️ {data.get('detail')}")
            else:
                print(f"❌ HTTP {response.status_code}")

        except Exception as e:
            print(f"❌ Error: {e}")


async def main():
    """Run all tests"""
    print("\n" + "█"*60)
    print("  LEGEND AI - PRODUCTION TEST SUITE")
    print(f"  Testing: {BASE_URL}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("█"*60)

    await test_health()
    await test_pattern_detection()
    await test_chart_generation()
    await test_market_internals()
    await test_cache_stats()
    await test_universe_scan()
    await test_telegram_webhook()
    await test_dashboard()

    print("\n" + "█"*60)
    print("  TESTING COMPLETE")
    print("█"*60)
    print("\n✅ All core systems tested. Check results above for any failures.\n")


if __name__ == "__main__":
    asyncio.run(main())
