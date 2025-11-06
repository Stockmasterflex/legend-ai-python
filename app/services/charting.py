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
        Generate a chart for a ticker

        Args:
            ticker: Stock symbol (e.g., NVDA)
            timeframe: "1day" or "1week"
            width: Chart width (max 1920)
            height: Chart height (max 1080)

        Returns:
            URL of the generated chart or None if failed
        """
        try:
            # Check rate limit
            if not await self._check_rate_limit():
                logger.warning(f"Chart-IMG rate limit exceeded for {ticker}")
                return None

            # Check for dev key
            if self.api_key in ["dev-key", "", None]:
                logger.warning("Chart-IMG API key not configured, returning placeholder")
                return self._get_placeholder_url(ticker)

            # Map timeframe to Chart-IMG format
            timeframe_map = {
                "1day": "daily",
                "daily": "daily",
                "1week": "weekly",
                "weekly": "weekly"
            }
            period = timeframe_map.get(timeframe.lower(), "daily")

            # Build request
            params = {
                "symbol": ticker.upper(),
                "period": period,
                "width": min(width, 1920),
                "height": min(height, 1080),
                "api_key": self.api_key
            }

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(self.BASE_URL, params=params)

                if response.status_code == 200:
                    # Chart-IMG returns a URL or image URL
                    # Typically the response is JSON with chart URL
                    try:
                        data = response.json()
                        chart_url = data.get("url") or data.get("chart_url")
                        if chart_url:
                            logger.info(f"Chart generated for {ticker}: {chart_url[:80]}...")
                            return chart_url
                    except:
                        # If response is image data, return the request URL
                        logger.info(f"Chart generated for {ticker}")
                        return response.url.path
                else:
                    logger.error(f"Chart-IMG error for {ticker}: {response.status_code}")
                    return self._get_placeholder_url(ticker)

        except Exception as e:
            logger.error(f"Error generating chart for {ticker}: {e}")
            return self._get_placeholder_url(ticker)

    def _get_placeholder_url(self, ticker: str) -> str:
        """Get a placeholder chart URL when real API fails"""
        # TradingView lightweight chart embed or fallback
        return f"https://www.tradingview.com/chart/?symbol={ticker.upper()}"

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
