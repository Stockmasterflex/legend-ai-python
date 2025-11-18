"""
Chart generation resource
"""

from typing import Optional, List, TYPE_CHECKING
from ..models import ChartResult

if TYPE_CHECKING:
    from ..client import LegendAI, AsyncLegendAI


class ChartsResource:
    """Synchronous chart generation resource"""

    def __init__(self, client: "LegendAI"):
        self._client = client

    def generate(
        self,
        ticker: str,
        interval: str = "1day",
        entry: Optional[float] = None,
        stop: Optional[float] = None,
        target: Optional[float] = None,
        indicators: Optional[List[str]] = None,
    ) -> ChartResult:
        """
        Generate a professional chart

        Args:
            ticker: Stock ticker symbol
            interval: Time interval
            entry: Entry price to mark on chart
            stop: Stop loss price to mark
            target: Target price to mark
            indicators: List of indicators to add

        Returns:
            ChartResult with chart URL
        """
        payload = {
            "ticker": ticker,
            "interval": interval,
        }
        if entry is not None:
            payload["entry"] = entry
        if stop is not None:
            payload["stop"] = stop
        if target is not None:
            payload["target"] = target
        if indicators:
            payload["indicators"] = indicators

        response = self._client.request("POST", "/api/charts/generate", json=payload)
        return ChartResult.from_dict(response)


class AsyncChartsResource:
    """Asynchronous chart generation resource"""

    def __init__(self, client: "AsyncLegendAI"):
        self._client = client

    async def generate(
        self,
        ticker: str,
        interval: str = "1day",
        entry: Optional[float] = None,
        stop: Optional[float] = None,
        target: Optional[float] = None,
        indicators: Optional[List[str]] = None,
    ) -> ChartResult:
        """Generate a professional chart (async)"""
        payload = {
            "ticker": ticker,
            "interval": interval,
        }
        if entry is not None:
            payload["entry"] = entry
        if stop is not None:
            payload["stop"] = stop
        if target is not None:
            payload["target"] = target
        if indicators:
            payload["indicators"] = indicators

        response = await self._client.request("POST", "/api/charts/generate", json=payload)
        return ChartResult.from_dict(response)
