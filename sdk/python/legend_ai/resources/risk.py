"""
Risk management resource
"""

from typing import Optional, TYPE_CHECKING
from ..models import PositionSize

if TYPE_CHECKING:
    from ..client import LegendAI, AsyncLegendAI


class RiskResource:
    """Synchronous risk management resource"""

    def __init__(self, client: "LegendAI"):
        self._client = client

    def calculate_position(
        self,
        account_size: float,
        entry_price: float,
        stop_loss_price: float,
        target_price: Optional[float] = None,
        risk_percentage: float = 2.0,
    ) -> PositionSize:
        """
        Calculate position size using 2% risk rule

        Args:
            account_size: Total account size
            entry_price: Entry price per share
            stop_loss_price: Stop loss price
            target_price: Target price (optional)
            risk_percentage: Risk percentage (default: 2.0)

        Returns:
            PositionSize with calculations
        """
        payload = {
            "account_size": account_size,
            "entry_price": entry_price,
            "stop_loss_price": stop_loss_price,
            "risk_percentage": risk_percentage,
        }
        if target_price is not None:
            payload["target_price"] = target_price

        response = self._client.request("POST", "/api/risk/calculate-position", json=payload)
        return PositionSize.from_dict(response)


class AsyncRiskResource:
    """Asynchronous risk management resource"""

    def __init__(self, client: "AsyncLegendAI"):
        self._client = client

    async def calculate_position(
        self,
        account_size: float,
        entry_price: float,
        stop_loss_price: float,
        target_price: Optional[float] = None,
        risk_percentage: float = 2.0,
    ) -> PositionSize:
        """Calculate position size using 2% risk rule (async)"""
        payload = {
            "account_size": account_size,
            "entry_price": entry_price,
            "stop_loss_price": stop_loss_price,
            "risk_percentage": risk_percentage,
        }
        if target_price is not None:
            payload["target_price"] = target_price

        response = await self._client.request("POST", "/api/risk/calculate-position", json=payload)
        return PositionSize.from_dict(response)
