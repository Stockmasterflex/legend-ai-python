"""
Chart-IMG service for generating trading charts
Pro plan: 500 daily calls, 10/sec rate limit, no watermark
"""
import logging
import asyncio
from typing import Optional, Dict, Any
import httpx
from datetime import datetime
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class ChartingService:
    """Generate trading charts using Chart-IMG API"""

    BASE_URL = "https://chart-img.com/chart"

    def __init__(self):
        self.api_key = settings.chartimg_api_key
        self.daily_limit = settings.chartimg_daily_limit
        self.rate_limit = 10  # 10 calls/sec
        self.call_count = 0
        self.last_reset = datetime.now()

    async def _check_rate_limit(self):
        """Simple rate limit check"""
        now = datetime.now()
        if (now - self.last_reset).total_seconds() >= 86400:
            self.call_count = 0
            self.last_reset = now

        if self.call_count >= self.daily_limit:
            logger.warning(f"Chart-IMG daily limit reached ({self.daily_limit})")
            return False

        self.call_count += 1
        return True

    async def generate_chart(
        self,
        ticker: str,
        timeframe: str = "1day",
        width: int = 1200,
        height: int = 600
    ) -> Optional[str]:
        """
        Generate a chart for a ticker using TradingView embed

        Args:
            ticker: Stock symbol (e.g., NVDA)
            timeframe: "1day" or "1week"
            width: Chart width (unused - TradingView is responsive)
            height: Chart height (unused - TradingView is responsive)

        Returns:
            URL of the TradingView embed chart
        """
        try:
            # Always use TradingView embed - it's reliable and doesn't require API key
            logger.info(f"📊 Chart URL generated for {ticker}")
            return self._get_placeholder_url(ticker)

        except Exception as e:
            logger.warning(f"⚠️ Chart generation error for {ticker}: {e}")
            return self._get_placeholder_url(ticker)

    def _get_placeholder_url(self, ticker: str) -> str:
        """Get a TradingView embed chart URL - works reliably"""
        # Use TradingView's lightweight embed which always works
        return f"https://www.tradingview.com/widgetembed/?symbol={ticker.upper()}&interval=D&hidesidetoolbar=0&hidetopmenu=0&style=1&locale=en&withdateranges=1"

    async def get_chart_batch(
        self,
        tickers: list[str],
        timeframe: str = "1day"
    ) -> Dict[str, Optional[str]]:
        """
        Generate charts for multiple tickers with rate limiting

        Args:
            tickers: List of stock symbols
            timeframe: Chart timeframe

        Returns:
            Dict mapping ticker -> chart URL
        """
        results = {}

        # Rate limit: max 10/sec = 100ms per call
        delay = 0.1

        for ticker in tickers:
            chart_url = await self.generate_chart(ticker, timeframe)
            results[ticker] = chart_url
            await asyncio.sleep(delay)

        return results


# Singleton instance
_charting_service: Optional[ChartingService] = None

def get_charting_service() -> ChartingService:
    """Get or create charting service singleton"""
    global _charting_service
    if _charting_service is None:
        _charting_service = ChartingService()
    return _charting_service
