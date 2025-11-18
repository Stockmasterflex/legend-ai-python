#!/usr/bin/env python3
"""
Test script for Legend AI critical fixes

Tests:
1. Manual universe seed endpoint
2. Health check after seeding
3. Top setups with timeout protection
4. Scanner endpoints
"""
import asyncio
import sys
import httpx
from datetime import datetime

# Change this to your Railway URL or localhost
BASE_URL = "https://legend-ai-python-production.up.railway.app"
# BASE_URL = "http://localhost:8000"  # For local testing


async def test_fixes():
    """Run all tests"""
    print("=" * 80)
    print("LEGEND AI - CRITICAL FIXES TEST SUITE")
    print("=" * 80)
    print(f"Testing against: {BASE_URL}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    async with httpx.AsyncClient(timeout=30.0) as client:

        # Test 1: Manual universe seed
        print("\n" + "=" * 80)
        print("TEST 1: Manual Universe Seed")
        print("=" * 80)
        try:
            print("Calling POST /api/universe/seed...")
            r = await client.post(f"{BASE_URL}/api/universe/seed")
            print(f"Status: {r.status_code}")

            if r.status_code == 200:
                data = r.json()
                print(f"✅ SUCCESS")
                print(f"   Symbols loaded: {data.get('symbols_loaded', 0)}")
                print(f"   Message: {data.get('message', 'N/A')}")
                print(f"   Timestamp: {data.get('timestamp', 'N/A')}")
            else:
                print(f"❌ FAILED: {r.status_code}")
                print(f"   Response: {r.text[:200]}")
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")

        # Test 2: Health check after seed
        print("\n" + "=" * 80)
        print("TEST 2: Health Check (Universe Status)")
        print("=" * 80)
        try:
            print("Calling GET /health...")
            r = await client.get(f"{BASE_URL}/health")
            print(f"Status: {r.status_code}")

            if r.status_code == 200:
                health = r.json()
                universe = health.get('universe', {})
                print(f"✅ SUCCESS")
                print(f"   Universe seeded: {universe.get('seeded', False)}")
                print(f"   Cached symbols: {universe.get('cached_symbols', 0)}")

                if universe.get('seeded'):
                    print("   ✅ Universe is properly seeded!")
                else:
                    print("   ⚠️ Universe NOT seeded - run Test 1 first")
            else:
                print(f"❌ FAILED: {r.status_code}")
                print(f"   Response: {r.text[:200]}")
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")

        # Test 3: Top setups with timeout (should complete in <15s)
        print("\n" + "=" * 80)
        print("TEST 3: Top Setups (Timeout Protection)")
        print("=" * 80)
        try:
            print("Calling GET /api/top-setups?limit=3...")
            print("This should complete in <15 seconds (timeout protection)...")

            start_time = datetime.now()
            r = await client.get(f"{BASE_URL}/api/top-setups?limit=3")
            duration = (datetime.now() - start_time).total_seconds()

            print(f"Status: {r.status_code}")
            print(f"Duration: {duration:.2f} seconds")

            if r.status_code == 200:
                data = r.json()
                print(f"✅ SUCCESS")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Count: {data.get('count', 0)}")
                print(f"   Cached: {data.get('cached', False)}")
                print(f"   Min score: {data.get('min_score', 0)}")

                if duration > 15:
                    print(f"   ⚠️ WARNING: Request took {duration:.2f}s (>15s timeout)")
                else:
                    print(f"   ✅ Completed within timeout ({duration:.2f}s)")

                if data.get('count', 0) > 0:
                    print(f"   ✅ Found {data['count']} top setups")
                    # Show first result
                    if data.get('results'):
                        first = data['results'][0]
                        print(f"   Sample: {first.get('ticker')} - {first.get('pattern')} ({first.get('score')}/10)")
                else:
                    print("   ℹ️ No setups found (may need to wait for universe to populate)")
            else:
                print(f"❌ FAILED: {r.status_code}")
                print(f"   Response: {r.text[:200]}")
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")

        # Test 4: Quick scan endpoint
        print("\n" + "=" * 80)
        print("TEST 4: Quick Scan Endpoint")
        print("=" * 80)
        try:
            print("Calling POST /api/universe/scan/quick...")
            r = await client.post(
                f"{BASE_URL}/api/universe/scan/quick",
                json={
                    "universe": "nasdaq100",
                    "limit": 5,
                    "min_score": 6.0,
                    "timeframe": "1day"
                }
            )
            print(f"Status: {r.status_code}")

            if r.status_code == 200:
                data = r.json()
                print(f"✅ SUCCESS")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Results: {len(data.get('data', []))}")

                if data.get('data'):
                    print(f"   Sample tickers: {[x.get('ticker') for x in data['data'][:3]]}")
            else:
                print(f"❌ FAILED: {r.status_code}")
                print(f"   Response: {r.text[:200]}")
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")

        # Test 5: Multi-pattern scanner
        print("\n" + "=" * 80)
        print("TEST 5: Multi-Pattern Scanner")
        print("=" * 80)
        try:
            print("Calling GET /api/scan/patterns?limit=3...")
            r = await client.get(f"{BASE_URL}/api/scan/patterns?limit=3&min_score=6.0")
            print(f"Status: {r.status_code}")

            if r.status_code == 200:
                data = r.json()
                print(f"✅ SUCCESS")
                print(f"   Success: {data.get('success', False)}")
                print(f"   Universe size: {data.get('universe_size', 0)}")
                print(f"   Results: {len(data.get('results', []))}")
                print(f"   Total hits: {data.get('meta', {}).get('total_hits', 0)}")
            else:
                print(f"❌ FAILED: {r.status_code}")
                print(f"   Response: {r.text[:200]}")
        except Exception as e:
            print(f"❌ EXCEPTION: {e}")

    print("\n" + "=" * 80)
    print("TESTS COMPLETED")
    print("=" * 80)
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)


if __name__ == "__main__":
    try:
        asyncio.run(test_fixes())
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        sys.exit(1)
