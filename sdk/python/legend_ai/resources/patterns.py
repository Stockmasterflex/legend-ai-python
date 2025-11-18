"""
Pattern detection resource
"""

from typing import Optional, TYPE_CHECKING
from ..models import PatternResult

if TYPE_CHECKING:
    from ..client import LegendAI, AsyncLegendAI


class PatternsResource:
    """Synchronous pattern detection resource"""

    def __init__(self, client: "LegendAI"):
        self._client = client

    def detect(
        self,
        ticker: str,
        interval: str = "1day",
        use_yahoo_fallback: bool = False,
    ) -> PatternResult:
        """
        Detect chart patterns for a ticker

        Args:
            ticker: Stock ticker symbol (e.g., "AAPL")
            interval: Time interval ("1day", "1week", "1hour", "4hour")
            use_yahoo_fallback: Use Yahoo Finance as fallback

        Returns:
            PatternResult with detected pattern and scores

        Example:
            >>> result = client.patterns.detect("AAPL")
            >>> print(f"{result.pattern}: {result.score}/10")
        """
        response = self._client.request(
            "POST",
            "/api/patterns/detect",
            json={
                "ticker": ticker,
                "interval": interval,
                "use_yahoo_fallback": use_yahoo_fallback,
            },
        )
        return PatternResult.from_dict(response)

    def health(self) -> dict:
        """Check pattern service health"""
        return self._client.request("GET", "/api/patterns/health")


class AsyncPatternsResource:
    """Asynchronous pattern detection resource"""

    def __init__(self, client: "AsyncLegendAI"):
        self._client = client

    async def detect(
        self,
        ticker: str,
        interval: str = "1day",
        use_yahoo_fallback: bool = False,
    ) -> PatternResult:
        """
        Detect chart patterns for a ticker (async)

        Args:
            ticker: Stock ticker symbol (e.g., "AAPL")
            interval: Time interval ("1day", "1week", "1hour", "4hour")
            use_yahoo_fallback: Use Yahoo Finance as fallback

        Returns:
            PatternResult with detected pattern and scores

        Example:
            >>> result = await client.patterns.detect("AAPL")
            >>> print(f"{result.pattern}: {result.score}/10")
        """
        response = await self._client.request(
            "POST",
            "/api/patterns/detect",
            json={
                "ticker": ticker,
                "interval": interval,
                "use_yahoo_fallback": use_yahoo_fallback,
            },
        )
        return PatternResult.from_dict(response)

    async def health(self) -> dict:
        """Check pattern service health"""
        return await self._client.request("GET", "/api/patterns/health")
