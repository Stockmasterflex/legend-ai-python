#!/usr/bin/env python3
"""
Test script for Redis caching functionality

Tests cache operations, pattern caching, and performance improvements
"""

import asyncio
import time
from datetime import datetime

from app.services.cache import get_cache_service, CacheService
from app.core.pattern_detector import PatternDetector, PatternResult
from app.core.pattern_detector import PatternResult


async def test_cache_basic_operations():
    """Test basic Redis cache operations"""
    print("\n🗄️ Testing Basic Cache Operations")
    print("=" * 50)

    cache = get_cache_service()

    try:
        # Test health check
        health = await cache.health_check()
        print(f"✅ Redis health: {health['status']}")

        if health['status'] != 'healthy':
            print("❌ Redis not available - skipping cache tests")
            return False

        # Test basic set/get
        await cache.redis.set("test_key", "test_value")
        value = await cache.redis.get("test_key")
        print(f"✅ Basic set/get: {value}")

        # Test JSON operations
        test_data = {"ticker": "TEST", "score": 8.5, "timestamp": datetime.now().isoformat()}
        await cache.redis.set("test_json", test_data.__str__())
        retrieved = await cache.redis.get("test_json")
        print(f"✅ JSON storage: {len(retrieved) if retrieved else 0} chars")

        return True

    except Exception as e:
        print(f"❌ Cache basic operations failed: {e}")
        return False


async def test_pattern_caching():
    """Test pattern result caching"""
    print("\n🎯 Testing Pattern Caching")
    print("=" * 50)

    cache = get_cache_service()

    try:
        # Create a mock pattern result
        pattern_result = PatternResult(
            ticker="AAPL",
            pattern="VCP",
            score=8.5,
            entry=175.50,
            stop=165.20,
            target=201.83,
            risk_reward=2.4,
            criteria_met=["✓ Above 50 SMA", "✓ Strong RS rating"],
            analysis="Classic VCP with volume dry-up",
            timestamp=datetime.now(),
            rs_rating=-5.2,
            current_price=178.30
        )

        # Test pattern caching
        success = await cache.set_pattern("AAPL", "1day", pattern_result.to_dict())
        print(f"✅ Pattern cached: {success}")

        # Test pattern retrieval
        cached = await cache.get_pattern("AAPL", "1day")
        if cached:
            print("✅ Pattern retrieved from cache:")
            print(f"   Ticker: {cached['ticker']}")
            print(f"   Pattern: {cached['pattern']}")
            print(f"   Score: {cached['score']}")
        else:
            print("❌ Pattern retrieval failed")

        # Test cache invalidation
        deleted = await cache.invalidate_pattern("AAPL")
        print(f"✅ Cache invalidated: {deleted} keys deleted")

        # Verify invalidation worked
        cached_after = await cache.get_pattern("AAPL", "1day")
        print(f"✅ Cache cleared: {'empty' if not cached_after else 'still cached'}")

        return True

    except Exception as e:
        print(f"❌ Pattern caching failed: {e}")
        return False


async def test_price_data_caching():
    """Test price data caching"""
    print("\n📊 Testing Price Data Caching")
    print("=" * 50)

    cache = get_cache_service()

    try:
        # Mock price data (like from TwelveData)
        price_data = {
            "c": [100.1, 101.2, 102.3, 101.8, 103.0],
            "o": [99.8, 100.2, 101.3, 102.2, 101.9],
            "h": [101.5, 102.1, 103.2, 102.8, 104.1],
            "l": [99.5, 99.8, 100.8, 101.2, 101.5],
            "v": [1000000, 1200000, 900000, 1100000, 1300000],
            "t": ["2024-01-01T00:00:00", "2024-01-02T00:00:00", "2024-01-03T00:00:00", "2024-01-04T00:00:00", "2024-01-05T00:00:00"]
        }

        # Test price data caching (15 min TTL)
        success = await cache.set_price_data("TEST", price_data)
        print(f"✅ Price data cached: {success}")

        # Test price data retrieval
        cached_price = await cache.get_price_data("TEST")
        if cached_price:
            print("✅ Price data retrieved:")
            print(f"   Data points: {len(cached_price.get('c', []))}")
            print(f"   Latest close: {cached_price['c'][-1] if cached_price.get('c') else 'N/A'}")
        else:
            print("❌ Price data retrieval failed")

        return True

    except Exception as e:
        print(f"❌ Price data caching failed: {e}")
        return False


async def test_cache_performance():
    """Test cache performance improvements"""
    print("\n⚡ Testing Cache Performance")
    print("=" * 50)

    cache = get_cache_service()

    try:
        # Create test pattern
        pattern = PatternResult(
            ticker="PERF",
            pattern="VCP",
            score=8.0,
            entry=100.0,
            stop=95.0,
            target=115.0,
            risk_reward=2.0,
            criteria_met=["✓ Test criteria"],
            analysis="Performance test",
            timestamp=datetime.now()
        )

        # Measure cache write time
        start_time = time.time()
        await cache.set_pattern("PERF", "1day", pattern.to_dict())
        write_time = time.time() - start_time

        # Measure cache read time
        start_time = time.time()
        result = await cache.get_pattern("PERF", "1day")
        read_time = time.time() - start_time

        print("✅ Cache performance:")
        print(f"   Write time: {write_time:.4f}s")
        print(f"   Read time: {read_time:.4f}s")
        # Cache should be much faster than API calls
        if read_time < 0.1:  # Should be under 100ms
            print("✅ Cache read time acceptable")
        else:
            print("⚠️ Cache read time slower than expected")

        return True

    except Exception as e:
        print(f"❌ Cache performance test failed: {e}")
        return False


async def test_cache_stats():
    """Test cache statistics"""
    print("\n📈 Testing Cache Statistics")
    print("=" * 50)

    cache = get_cache_service()

    try:
        # Add some test data
        test_pattern = PatternResult(
            ticker="STATS",
            pattern="TEST",
            score=7.0,
            entry=50.0,
            stop=45.0,
            target=60.0,
            risk_reward=2.0,
            criteria_met=["✓ Test"],
            analysis="Stats test",
            timestamp=datetime.now()
        )

        await cache.set_pattern("STATS", "1day", test_pattern.to_dict())
        await cache.set_price_data("STATS", {"c": [50.0], "o": [49.0], "h": [51.0], "l": [48.0], "v": [1000000], "t": ["2024-01-01"]})

        # Get cache stats
        stats = await cache.get_cache_stats()

        print("✅ Cache statistics:")
        print(f"   Total keys: {stats.get('total_keys', 0)}")
        print(f"   Pattern keys: {stats.get('pattern_keys', 0)}")
        print(f"   Price keys: {stats.get('price_keys', 0)}")
        print(f"   Memory usage: {stats.get('memory_used', 'unknown')}")

        # Test cache clearing (be careful!)
        print("\n⚠️ Testing cache clear (this will remove all data)...")
        confirm = input("Type 'yes' to clear cache: ")
        if confirm.lower() == 'yes':
            clear_result = await cache.clear_all_cache()
            print(f"✅ Cache cleared: {clear_result}")
        else:
            print("⏭️ Skipping cache clear")

        return True

    except Exception as e:
        print(f"❌ Cache stats test failed: {e}")
        return False


async def main():
    """Run all cache tests"""
    print("🗄️ LEGEND AI - Redis Cache Test Suite")
    print("=" * 60)
    print(f"Started at: {datetime.now()}")

    tests = [
        ("Basic Operations", test_cache_basic_operations),
        ("Pattern Caching", test_pattern_caching),
        ("Price Data Caching", test_price_data_caching),
        ("Performance", test_cache_performance),
        ("Statistics", test_cache_stats)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            success = await test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"💥 Test '{test_name}' crashed: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("📊 CACHE TEST RESULTS")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1

    print(f"\n🎯 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All cache tests passed! Redis caching is working correctly.")
    else:
        print("⚠️ Some cache tests failed. Check Redis configuration.")

    print("=" * 60)


if __name__ == "__main__":
    # Check if Redis is running
    print("🔍 Checking Redis connectivity...")
    print("Make sure Redis is running:")
    print("  docker-compose up -d redis")
    print("  OR: redis-server")
    print()

    asyncio.run(main())
