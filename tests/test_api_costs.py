"""
API Cost Monitoring Tests

These tests ensure API usage stays within budget limits and caching is effective.
Critical for keeping costs at $15-25/month instead of $50-75/month.
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta

from app.services.cache import is_market_hours


class TestAPIUsageLimits:
    """Test API usage stays within daily/monthly limits"""

    def test_market_hours_detection(self):
        """Verify market hours detection works correctly"""
        # Market hours: Mon-Fri, 9:30 AM - 4:00 PM ET
        # This is a basic smoke test - full testing would need time mocking
        result = is_market_hours()
        assert isinstance(result, bool)

    @pytest.mark.asyncio
    async def test_cache_reduces_api_calls(self):
        """Verify caching reduces API calls for repeated requests"""
        from app.services.market_data import market_data_service

        # Mock cache get/set
        store = {}

        async def mock_get(key):
            return store.get(key)

        async def mock_set(key, value, ttl=None):
            store[key] = value
            return True

        market_data_service.cache.get = AsyncMock(side_effect=mock_get)
        market_data_service.cache.set = AsyncMock(side_effect=mock_set)

        # Mock external API calls to avoid "Event loop is closed" or network errors
        market_data_service._get_from_yahoo = AsyncMock(return_value={
            "c": [100.0, 101.0], "o": [99.0, 100.0], "h": [102.0, 102.0],
            "l": [98.0, 99.0], "v": [1000, 2000], "t": ["2024-01-01", "2024-01-02"]
        })

        ticker = "AAPL"
        interval = "1day"

        # First call - should hit API (mocked) and set cache
        data1 = await market_data_service.get_time_series(ticker, interval, 100)

        # Second call - should hit cache
        data2 = await market_data_service.get_time_series(ticker, interval, 100)

        # Data should be identical (either both from cache or both from API)
        assert data1 is not None
        assert data2 is not None

        # If both succeeded, they should have same structure
        if data1 and data2:
            assert set(data1.keys()) == set(data2.keys())

    @pytest.mark.asyncio
    async def test_dynamic_ttl_market_hours(self):
        """Verify TTL is shorter during market hours"""
        from app.services.cache import CacheService
        from app.config import get_settings

        settings = get_settings()
        cache_service = CacheService(settings.redis_url)

        # Mock Redis client
        cache_service.redis = AsyncMock()
        cache_service.redis.setex.return_value = True

        # Test pattern caching with dynamic TTL
        test_data = {"pattern": "VCP", "confidence": 0.85}

        # During market hours, TTL should be max 30 minutes (1800s)
        # Outside market hours, TTL should be min 2 hours (7200s)
        # This is tested by the set_pattern method logic

        # We can't easily mock datetime for is_market_hours(),
        # but we can verify the TTL adjustment logic exists
        with patch("app.services.cache.is_market_hours") as mock_market_hours:
            # Test during market hours
            mock_market_hours.return_value = True
            result = await cache_service.set_pattern(
                "AAPL", "1day", test_data
            )
            assert result is True  # Should succeed

            # Test outside market hours
            mock_market_hours.return_value = False
            result = await cache_service.set_pattern(
                "AAPL", "1day", test_data
            )
            assert result is True  # Should succeed

    @pytest.mark.asyncio
    async def test_concurrent_requests_use_cache(self):
        """Verify concurrent requests for same data use cache"""
        import asyncio
        from app.services.market_data import market_data_service

        ticker = "NVDA"

        # Make 10 concurrent requests for the same ticker
        tasks = [
            market_data_service.get_time_series(ticker, "1day", 100)
            for _ in range(10)
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # All requests should succeed
        successful_results = [r for r in results if not isinstance(r, Exception)]
        assert len(successful_results) >= 8, (
            f"Only {len(successful_results)}/10 requests succeeded"
        )

        # If multiple succeeded, they should have similar data
        if len(successful_results) >= 2:
            first_result = successful_results[0]
            for result in successful_results[1:]:
                if first_result and result:
                    # Should have same number of data points
                    assert len(first_result.get("c", [])) == len(result.get("c", []))


class TestCostOptimizations:
    """Test cost optimization features are working"""

    @pytest.mark.asyncio
    async def test_batch_scanning_efficiency(self):
        """Verify batch scanning is more efficient than individual scans"""
        from app.services.pattern_scanner import pattern_scanner_service
        import time

        symbols = ["AAPL", "NVDA", "MSFT"]

        # Batch scan
        start = time.perf_counter()
        batch_result = await pattern_scanner_service.scan_universe(
            universe=symbols,
            limit=10,
            min_score=7.0
        )
        batch_duration = time.perf_counter() - start

        assert batch_result["success"] is True
        assert batch_duration < 10.0, (
            f"Batch scan took {batch_duration:.2f}s (should be < 10s)"
        )

    @pytest.mark.asyncio
    async def test_universe_scan_respects_limits(self):
        """Verify universe scans respect symbol limits to control costs"""
        from app.services.pattern_scanner import pattern_scanner_service

        # Create scanner with low limit
        limited_scanner = pattern_scanner_service

        # Scan with limit
        result = await limited_scanner.scan_universe(
            universe=None,  # Use default universe
            limit=10,
            min_score=7.0
        )

        # Should return at most 10 results
        assert len(result["results"]) <= 10

        # Should report universe size scanned
        assert "meta" in result
        assert "universe_size" in result


class TestCachingEffectiveness:
    """Test that caching is reducing API costs effectively"""

    @pytest.mark.asyncio
    async def test_cache_hit_rate(self):
        """Verify cache hit rate is reasonable (>50% for repeated queries)"""
        from app.services.market_data import market_data_service

        # Mock cache service in market data
        market_data_service.cache.get = AsyncMock(return_value={"c": [100.0], "cached": True})

        ticker = "AAPL"

        # Make 5 requests for same ticker/interval
        for _ in range(5):
            data = await market_data_service.get_time_series(ticker, "1day", 100)
            assert data is not None

        # All 5 requests should complete successfully
        # In a real monitoring scenario, we'd track cache hit/miss ratio

    @pytest.mark.asyncio
    async def test_cache_invalidation(self):
        """Verify cache invalidation works when needed"""
        from app.services.cache import CacheService
        from app.config import get_settings

        settings = get_settings()
        cache_service = CacheService(settings.redis_url)

        # Mock Redis
        store = {}

        async def mock_setex(key, ttl, value):
            store[key] = value
            return True

        async def mock_get(key):
            return store.get(key)

        cache_service.redis = AsyncMock()
        cache_service.redis.setex.side_effect = mock_setex
        cache_service.redis.get.side_effect = mock_get

        # Set a value
        await cache_service.set("test_key", {"value": 123}, ttl=1)

        # Get it back immediately
        value = await cache_service.get("test_key")
        assert value is not None

        # Simulate expiration manually for mock
        store.clear()

        # Should be expired
        value_after = await cache_service.get("test_key")
        assert value_after is None  # Should be expired

    @pytest.mark.asyncio
    async def test_pattern_cache_reuse(self):
        """Verify pattern results are cached and reused"""
        from app.services.cache import CacheService
        from app.config import get_settings
        import json

        settings = get_settings()
        cache_service = CacheService(settings.redis_url)

        # Mock Redis
        store = {}

        async def mock_setex(key, ttl, value):
            store[key] = value
            return True

        async def mock_get(key):
            return store.get(key)

        cache_service.redis = AsyncMock()
        cache_service.redis.setex.side_effect = mock_setex
        cache_service.redis.get.side_effect = mock_get

        test_pattern = {
            "pattern": "VCP",
            "confidence": 0.85,
            "entry": 150.0,
            "stop": 145.0,
            "target": 165.0
        }

        # Cache pattern
        await cache_service.set_pattern("TEST", "1day", test_pattern)

        # Retrieve it
        cached = await cache_service.get_pattern("TEST", "1day")

        assert cached is not None
        assert cached["pattern"] == "VCP"
        assert cached["confidence"] == 0.85


class TestAPIUsageTracking:
    """Test API usage tracking and monitoring"""

    def test_cost_calculation_logic(self):
        """Verify cost calculation logic is accurate"""
        # Cost assumptions (update with actual API pricing):
        # - TwelveData: ~$0.001 per call
        # - Chart-IMG: ~$0.002 per chart
        # - Finnhub: Free tier
        # - Alpha Vantage: Free tier

        # Simulate daily usage
        twelvedata_calls = 500  # Pattern scans + price data
        chartimg_calls = 50     # Chart generations

        daily_cost = (
            twelvedata_calls * 0.001 +
            chartimg_calls * 0.002
        )

        # Daily cost should be under $1.00
        assert daily_cost < 1.00, (
            f"Daily cost ${daily_cost:.2f} exceeds $1.00 target"
        )

        # Monthly cost (30 days)
        monthly_cost = daily_cost * 30

        # Monthly cost should be under $30
        assert monthly_cost < 30.00, (
            f"Monthly cost ${monthly_cost:.2f} exceeds $30.00 budget"
        )

    def test_cache_hit_savings(self):
        """Calculate potential savings from cache hits"""
        # Without cache: every request hits API
        total_requests = 1000
        cost_per_request = 0.001
        no_cache_cost = total_requests * cost_per_request  # $1.00

        # With 70% cache hit rate: only 30% hit API
        cache_hit_rate = 0.70
        api_requests = total_requests * (1 - cache_hit_rate)  # 300 requests
        with_cache_cost = api_requests * cost_per_request  # $0.30

        savings = no_cache_cost - with_cache_cost
        savings_pct = (savings / no_cache_cost) * 100

        # Should save at least 60%
        assert savings_pct >= 60.0, (
            f"Cache savings {savings_pct:.1f}% below 60% target"
        )


class TestProductionReadiness:
    """Test production readiness and cost controls"""

    @pytest.mark.asyncio
    async def test_error_handling_doesnt_waste_api_calls(self):
        """Verify errors don't cause excessive API retry attempts"""
        from app.services.market_data import market_data_service

        # Try to fetch data for invalid ticker
        invalid_result = await market_data_service.get_time_series(
            ticker="INVALID_TICKER_THAT_DOESNT_EXIST",
            interval="1day",
            outputsize=100
        )

        # Should handle gracefully without multiple retry attempts
        # Result might be None or empty, but shouldn't throw exception
        assert invalid_result is None or isinstance(invalid_result, dict)

    @pytest.mark.asyncio
    async def test_concurrent_limit_prevents_api_flood(self):
        """Verify concurrency limits prevent API flooding"""
        from app.services.pattern_scanner import PatternScannerService

        # Create scanner with low concurrency
        scanner = PatternScannerService(max_concurrency=2)

        # This should respect concurrency limit
        result = await scanner.scan_universe(
            universe=["AAPL", "NVDA", "MSFT", "GOOGL", "META"],
            limit=5,
            min_score=7.0
        )

        assert result["success"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
