"""
Universe scanning resource
"""

from typing import Optional, List, TYPE_CHECKING
from ..models import ScanResult

if TYPE_CHECKING:
    from ..client import LegendAI, AsyncLegendAI


class UniverseResource:
    """Synchronous universe scanning resource"""

    def __init__(self, client: "LegendAI"):
        self._client = client

    def scan(
        self,
        universe: str = "SP500",
        min_score: float = 7.0,
        max_results: int = 20,
        pattern_types: Optional[List[str]] = None,
    ) -> List[ScanResult]:
        """
        Scan market universe for patterns

        Args:
            universe: Universe to scan ("SP500", "NASDAQ100", "CUSTOM")
            min_score: Minimum pattern score (0-10)
            max_results: Maximum results to return
            pattern_types: Filter by pattern types

        Returns:
            List of ScanResult objects
        """
        payload = {
            "universe": universe,
            "min_score": min_score,
            "max_results": max_results,
        }
        if pattern_types:
            payload["pattern_types"] = pattern_types

        response = self._client.request("POST", "/api/universe/scan", json=payload)
        results = response.get("results", [])
        return [ScanResult.from_dict(r) for r in results]

    def get_tickers(self, universe: str = "SP500") -> List[str]:
        """Get list of tickers in universe"""
        response = self._client.request("GET", f"/api/universe/tickers?universe={universe}")
        return response.get("tickers", [])


class AsyncUniverseResource:
    """Asynchronous universe scanning resource"""

    def __init__(self, client: "AsyncLegendAI"):
        self._client = client

    async def scan(
        self,
        universe: str = "SP500",
        min_score: float = 7.0,
        max_results: int = 20,
        pattern_types: Optional[List[str]] = None,
    ) -> List[ScanResult]:
        """Scan market universe for patterns (async)"""
        payload = {
            "universe": universe,
            "min_score": min_score,
            "max_results": max_results,
        }
        if pattern_types:
            payload["pattern_types"] = pattern_types

        response = await self._client.request("POST", "/api/universe/scan", json=payload)
        results = response.get("results", [])
        return [ScanResult.from_dict(r) for r in results]

    async def get_tickers(self, universe: str = "SP500") -> List[str]:
        """Get list of tickers in universe"""
        response = await self._client.request("GET", f"/api/universe/tickers?universe={universe}")
        return response.get("tickers", [])
