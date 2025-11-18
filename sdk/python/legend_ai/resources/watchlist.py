"""
Watchlist resource
"""

from typing import Optional, List, TYPE_CHECKING
from ..models import WatchlistItem

if TYPE_CHECKING:
    from ..client import LegendAI, AsyncLegendAI


class WatchlistResource:
    """Synchronous watchlist resource"""

    def __init__(self, client: "LegendAI"):
        self._client = client

    def list(self, user_id: str = "default") -> List[WatchlistItem]:
        """
        Get all watchlist items

        Args:
            user_id: User ID (default: "default")

        Returns:
            List of WatchlistItem objects
        """
        response = self._client.request("GET", f"/api/watchlist?user_id={user_id}")
        items = response.get("items", [])
        return [WatchlistItem.from_dict(item) for item in items]

    def add(
        self,
        ticker: str,
        user_id: str = "default",
        reason: Optional[str] = None,
        target_entry: Optional[float] = None,
        target_stop: Optional[float] = None,
    ) -> dict:
        """
        Add ticker to watchlist

        Args:
            ticker: Stock ticker symbol
            user_id: User ID
            reason: Reason for adding
            target_entry: Target entry price
            target_stop: Target stop loss price

        Returns:
            Response dictionary
        """
        payload = {"ticker": ticker, "user_id": user_id}
        if reason:
            payload["reason"] = reason
        if target_entry is not None:
            payload["target_entry"] = target_entry
        if target_stop is not None:
            payload["target_stop"] = target_stop

        return self._client.request("POST", "/api/watchlist/add", json=payload)

    def remove(self, ticker: str, user_id: str = "default") -> dict:
        """Remove ticker from watchlist"""
        return self._client.request("DELETE", f"/api/watchlist/remove/{ticker}?user_id={user_id}")


class AsyncWatchlistResource:
    """Asynchronous watchlist resource"""

    def __init__(self, client: "AsyncLegendAI"):
        self._client = client

    async def list(self, user_id: str = "default") -> List[WatchlistItem]:
        """Get all watchlist items (async)"""
        response = await self._client.request("GET", f"/api/watchlist?user_id={user_id}")
        items = response.get("items", [])
        return [WatchlistItem.from_dict(item) for item in items]

    async def add(
        self,
        ticker: str,
        user_id: str = "default",
        reason: Optional[str] = None,
        target_entry: Optional[float] = None,
        target_stop: Optional[float] = None,
    ) -> dict:
        """Add ticker to watchlist (async)"""
        payload = {"ticker": ticker, "user_id": user_id}
        if reason:
            payload["reason"] = reason
        if target_entry is not None:
            payload["target_entry"] = target_entry
        if target_stop is not None:
            payload["target_stop"] = target_stop

        return await self._client.request("POST", "/api/watchlist/add", json=payload)

    async def remove(self, ticker: str, user_id: str = "default") -> dict:
        """Remove ticker from watchlist (async)"""
        return await self._client.request("DELETE", f"/api/watchlist/remove/{ticker}?user_id={user_id}")
