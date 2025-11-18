"""
Market data resource
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import LegendAI, AsyncLegendAI


class MarketResource:
    """Synchronous market data resource"""

    def __init__(self, client: "LegendAI"):
        self._client = client

    def internals(self) -> dict:
        """Get market internals (breadth, advance/decline, regime)"""
        return self._client.request("GET", "/api/market/internals")

    def breadth(self) -> dict:
        """Get market breadth metrics"""
        return self._client.request("GET", "/api/market/breadth")

    def regime(self) -> dict:
        """Get market regime classification"""
        return self._client.request("GET", "/api/market/regime")


class AsyncMarketResource:
    """Asynchronous market data resource"""

    def __init__(self, client: "AsyncLegendAI"):
        self._client = client

    async def internals(self) -> dict:
        """Get market internals (async)"""
        return await self._client.request("GET", "/api/market/internals")

    async def breadth(self) -> dict:
        """Get market breadth metrics (async)"""
        return await self._client.request("GET", "/api/market/breadth")

    async def regime(self) -> dict:
        """Get market regime classification (async)"""
        return await self._client.request("GET", "/api/market/regime")
