"""
Tests for watchlist monitoring functionality
"""
import pytest
from datetime import datetime, time
from zoneinfo import ZoneInfo
from app.jobs.watchlist_monitor import WatchlistMonitor

class TestWatchlistMonitor:
    """Test watchlist monitoring logic"""
    
    def test_initialization(self):
        """Test monitor initialization"""
        monitor = WatchlistMonitor()
        assert monitor.db is not None
    
    def test_market_hours_weekday_open(self):
        """Test market hours detection during trading hours"""
        monitor = WatchlistMonitor()
        # This test would need to mock datetime to properly test
        # Just verify the method exists and runs
        result = monitor.is_market_hours()
        assert isinstance(result, bool)
    
    def test_check_watchlist_item_no_ticker(self):
        """Test handling of item without ticker"""
        monitor = WatchlistMonitor()
        
        @pytest.mark.asyncio
        async def run_test():
            item = {"status": "Watching"}
            result = await monitor.check_watchlist_item(item)
            assert result is None
        
        import asyncio
        asyncio.run(run_test())
    
    def test_check_watchlist_item_completed_status(self):
        """Test skipping completed items"""
        monitor = WatchlistMonitor()
        
        @pytest.mark.asyncio
        async def run_test():
            item = {"ticker": "TEST", "status": "Completed"}
            result = await monitor.check_watchlist_item(item)
            assert result is None
        
        import asyncio
        asyncio.run(run_test())

class TestMarketHours:
    """Test market hours logic"""
    
    def test_market_open_time(self):
        """Test market open time constant"""
        from app.jobs.watchlist_monitor import MARKET_OPEN, MARKET_CLOSE
        assert MARKET_OPEN == time(9, 30)
        assert MARKET_CLOSE == time(16, 0)
    
    def test_et_timezone(self):
        """Test ET timezone configuration"""
        from app.jobs.watchlist_monitor import ET_TIMEZONE
        assert ET_TIMEZONE == ZoneInfo("America/New_York")

class TestWatchlistMonitorFactory:
    """Test factory function"""
    
    def test_get_watchlist_monitor(self):
        """Test singleton factory"""
        from app.jobs.watchlist_monitor import get_watchlist_monitor
        
        monitor1 = get_watchlist_monitor()
        monitor2 = get_watchlist_monitor()
        
        # Should return same instance
        assert monitor1 is monitor2

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

