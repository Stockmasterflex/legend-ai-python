"""
Trade management resource
"""

from typing import Optional, TYPE_CHECKING
from ..models import Trade

if TYPE_CHECKING:
    from ..client import LegendAI, AsyncLegendAI


class TradesResource:
    """Synchronous trade management resource"""

    def __init__(self, client: "LegendAI"):
        self._client = client

    def create(
        self,
        ticker: str,
        entry_price: float,
        stop_loss: float,
        target_price: Optional[float] = None,
        position_size: Optional[int] = None,
        risk_amount: Optional[float] = None,
    ) -> dict:
        """
        Create a new trade entry

        Args:
            ticker: Stock ticker symbol
            entry_price: Entry price
            stop_loss: Stop loss price
            target_price: Target price
            position_size: Number of shares
            risk_amount: Dollar amount at risk

        Returns:
            Response with trade_id
        """
        payload = {
            "ticker": ticker,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
        }
        if target_price is not None:
            payload["target_price"] = target_price
        if position_size is not None:
            payload["position_size"] = position_size
        if risk_amount is not None:
            payload["risk_amount"] = risk_amount

        return self._client.request("POST", "/api/trades/create", json=payload)


class AsyncTradesResource:
    """Asynchronous trade management resource"""

    def __init__(self, client: "AsyncLegendAI"):
        self._client = client

    async def create(
        self,
        ticker: str,
        entry_price: float,
        stop_loss: float,
        target_price: Optional[float] = None,
        position_size: Optional[int] = None,
        risk_amount: Optional[float] = None,
    ) -> dict:
        """Create a new trade entry (async)"""
        payload = {
            "ticker": ticker,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
        }
        if target_price is not None:
            payload["target_price"] = target_price
        if position_size is not None:
            payload["position_size"] = position_size
        if risk_amount is not None:
            payload["risk_amount"] = risk_amount

        return await self._client.request("POST", "/api/trades/create", json=payload)
