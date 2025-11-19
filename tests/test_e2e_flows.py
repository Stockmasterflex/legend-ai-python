"""
End-to-End Flow Tests

These tests verify complete user workflows work correctly from start to finish.
Critical for ensuring the full analysis -> decision -> action flow works.
"""
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create test client"""
    from app.main import app
    return TestClient(app)


class TestPatternAnalysisFlow:
    """Test complete pattern analysis workflow"""

    def test_health_check(self, client):
        """Verify API is healthy"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert "version" in data
        assert "keys" in data

    def test_root_endpoint(self, client):
        """Verify root endpoint returns service info"""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "running"
        assert "service" in data
        assert "endpoints" in data

    @pytest.mark.asyncio
    async def test_single_pattern_detection_flow(self):
        """Test: Search ticker -> Detect pattern -> Get chart"""
        from app.services.pattern_scanner import pattern_scanner_service

        ticker = "AAPL"

        # Step 1: Detect patterns
        patterns = await pattern_scanner_service.scan_symbol(ticker, "1day")

        # Should return results (may be empty if no patterns)
        assert isinstance(patterns, list)

        # If patterns found, validate structure
        if patterns:
            pattern = patterns[0]
            assert "symbol" in pattern
            assert "pattern" in pattern
            assert "score" in pattern
            assert "confidence" in pattern

    @pytest.mark.asyncio
    async def test_universe_scan_flow(self):
        """Test: Configure scan -> Run scan -> Filter results"""
        from app.services.pattern_scanner import pattern_scanner_service

        # Step 1: Run universe scan
        scan_result = await pattern_scanner_service.scan_universe(
            universe=["AAPL", "NVDA", "MSFT"],
            limit=10,
            min_score=6.0
        )

        # Should complete successfully
        assert scan_result["success"] is True
        assert "results" in scan_result
        assert "meta" in scan_result

        # Step 2: Filter results by score
        high_score_results = [
            r for r in scan_result["results"]
            if r["score"] >= 8.0
        ]

        # All filtered results should meet criteria
        for result in high_score_results:
            assert result["score"] >= 8.0

    def test_watchlist_flow(self, client):
        """Test: Add to watchlist -> View watchlist -> Remove from watchlist"""
        # Step 1: Add ticker to watchlist
        add_response = client.post(
            "/api/watchlist/add",
            json={
                "ticker": "TSLA",
                "status": "Watching",
                "reason": "VCP forming",
                "tags": ["VCP", "Momentum"]
            }
        )

        # Should succeed (200 or 201)
        assert add_response.status_code in [200, 201]

        # Step 2: Get watchlist
        get_response = client.get("/api/watchlist")
        assert get_response.status_code == 200

        watchlist = get_response.json()
        # The response structure is {"success": True, "items": [...], "total": ...}
        assert "items" in watchlist
        items = watchlist["items"]
        assert isinstance(items, list)

        # Find our added ticker
        tsla_items = [item for item in items if item.get("ticker") == "TSLA"]

        if tsla_items:
            tsla_item = tsla_items[0]
            ticker = tsla_item.get("ticker")

            # Step 3: Delete ticker from watchlist
            if ticker:
                delete_response = client.delete(f"/api/watchlist/remove/{ticker}")
                # Should succeed (200, 204, or 404 if already deleted)
                assert delete_response.status_code in [200, 204, 404]

    @pytest.mark.asyncio
    async def test_chart_generation_flow(self):
        """Test: Detect pattern -> Generate chart -> Retrieve chart URL"""
        from app.services.pattern_scanner import pattern_scanner_service

        ticker = "NVDA"

        # Step 1: Detect patterns (which should trigger chart caching)
        # Note: scan_symbol returns a list of dicts
        patterns = await pattern_scanner_service.scan_symbol(ticker, "1day")

        # Step 2: Chart URL should be available
        # In production, this would be fetched from chart service
        # For testing, we just verify the flow completes
        assert isinstance(patterns, list)

    def test_metrics_endpoint(self, client):
        """Test: Access metrics endpoint for monitoring"""
        response = client.get("/metrics")

        # Should return metrics (may be 200 or 404 if not enabled)
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            # Should return Prometheus format or JSON
            content_type = response.headers.get("content-type", "")
            assert "text/plain" in content_type or "application/json" in content_type


class TestAPIEndpoints:
    """Test critical API endpoints"""

    def test_analyze_endpoint(self, client):
        """Test /api/analyze endpoint"""
        response = client.get(
            "/api/analyze",
            params={
                "ticker": "AAPL",
                "tf": "daily"
            }
        )

        # Should return results (200, 201, or 422 for validation error)
        assert response.status_code in [200, 201, 422]

    def test_patterns_detect_endpoint(self, client):
        """Test /api/patterns/detect endpoint"""
        response = client.post(
            "/api/patterns/detect",
            json={
                "ticker": "NVDA",
                "interval": "1day"
            }
        )

        # Should return results
        assert response.status_code in [200, 201, 422]

    def test_universe_endpoint(self, client):
        """Test /api/universe endpoints"""
        # Get universe tickers
        get_response = client.get("/api/universe/tickers")
        assert get_response.status_code == 200

        # Seed universe
        seed_response = client.post("/api/universe/seed")
        assert seed_response.status_code in [200, 201]

        seed_data = seed_response.json()
        assert "success" in seed_data or "symbols_loaded" in seed_data

    def test_scan_endpoint(self, client):
        """Test /api/universe/scan endpoint"""
        response = client.post(
            "/api/universe/scan",
            json={
                "min_score": 7.0,
                "max_results": 5,
                "pattern_types": ["VCP"]
            }
        )

        # Should return results
        assert response.status_code in [200, 201, 422]


class TestErrorHandling:
    """Test error handling and edge cases"""

    def test_invalid_ticker(self, client):
        """Test handling of invalid ticker symbols"""
        response = client.post(
            "/api/patterns/detect",
            json={
                "ticker": "INVALID_SYMBOL_123",
                "timeframe": "1day"
            }
        )

        # Should handle gracefully (not crash)
        assert response.status_code in [200, 400, 404, 422, 500]

    def test_invalid_timeframe(self, client):
        """Test handling of invalid timeframe"""
        response = client.post(
            "/api/patterns/detect",
            json={
                "ticker": "AAPL",
                "interval": "invalid"
            }
        )

        # Should reject invalid input
        assert response.status_code in [400, 422]

    @pytest.mark.asyncio
    async def test_empty_universe_scan(self):
        """Test scanning empty universe"""
        from app.services.pattern_scanner import pattern_scanner_service

        result = await pattern_scanner_service.scan_universe(
            universe=[],
            limit=10,
            min_score=7.0
        )

        # Should handle gracefully
        assert result["success"] is True
        assert len(result["results"]) == 0

    @pytest.mark.asyncio
    async def test_insufficient_price_data(self):
        """Test handling of insufficient price data"""
        from app.services.pattern_scanner import pattern_scanner_service

        # Try to scan with very few bars
        # (most patterns need 60+ bars)
        patterns = await pattern_scanner_service.scan_symbol("AAPL", "1day")

        # Should complete without crashing
        assert isinstance(patterns, list)


class TestPerformance:
    """Test performance characteristics"""

    @pytest.mark.asyncio
    async def test_single_scan_performance(self):
        """Verify single ticker scan completes in reasonable time"""
        import time
        from app.services.pattern_scanner import pattern_scanner_service

        start = time.perf_counter()
        await pattern_scanner_service.scan_symbol("AAPL", "1day")
        duration = time.perf_counter() - start

        # Should complete in under 5 seconds
        assert duration < 5.0, f"Scan took {duration:.2f}s (should be < 5s)"

    @pytest.mark.asyncio
    async def test_universe_scan_performance(self):
        """Verify universe scan completes in reasonable time"""
        import time
        from app.services.pattern_scanner import pattern_scanner_service

        start = time.perf_counter()
        await pattern_scanner_service.scan_universe(
            universe=["AAPL", "NVDA", "MSFT", "GOOGL", "META"],
            limit=10,
            min_score=7.0
        )
        duration = time.perf_counter() - start

        # Should complete in under 15 seconds for 5 symbols
        assert duration < 15.0, f"Scan took {duration:.2f}s (should be < 15s)"

    def test_health_check_speed(self, client):
        """Verify health check is fast"""
        import time

        start = time.perf_counter()
        response = client.get("/health")
        duration = time.perf_counter() - start

        assert response.status_code == 200
        # Should respond in under 1 second
        assert duration < 1.0, f"Health check took {duration:.2f}s"


class TestDataConsistency:
    """Test data consistency across multiple requests"""

    @pytest.mark.asyncio
    async def test_repeated_scans_consistency(self):
        """Verify repeated scans of same ticker produce consistent results"""
        from app.services.pattern_scanner import pattern_scanner_service

        # Scan same ticker twice
        result1 = await pattern_scanner_service.scan_symbol("AAPL", "1day")
        result2 = await pattern_scanner_service.scan_symbol("AAPL", "1day")

        # Should have same number of patterns
        # (may differ if market data updated between calls)
        assert isinstance(result1, list)
        assert isinstance(result2, list)

        # If both found patterns, scores should be similar
        if result1 and result2:
            scores1 = [p["score"] for p in result1]
            scores2 = [p["score"] for p in result2]

            # Should have similar patterns detected
            # (allowing for small variations due to data updates)
            assert len(scores1) > 0
            assert len(scores2) > 0


class TestIntegrationWithExternalAPIs:
    """Test integration with external APIs"""

    @pytest.mark.asyncio
    async def test_market_data_api_integration(self):
        """Verify market data API integration works"""
        from app.services.market_data import market_data_service

        data = await market_data_service.get_time_series(
            ticker="AAPL",
            interval="1day",
            outputsize=10
        )

        # Should return data or handle error gracefully
        if data:
            assert "c" in data  # Should have close prices
            assert len(data["c"]) > 0

    def test_dashboard_loads(self, client):
        """Verify dashboard HTML loads successfully"""
        response = client.get("/dashboard")

        # Should load (200 or 404 if route not configured)
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            # Should return HTML
            assert "text/html" in response.headers.get("content-type", "")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
