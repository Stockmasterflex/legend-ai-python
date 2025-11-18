"""
Main client for Legend AI API
"""

from typing import Optional, List, Dict, Any
import httpx
from .exceptions import APIError, RateLimitError, AuthenticationError, ValidationError
from .resources.patterns import PatternsResource, AsyncPatternsResource
from .resources.charts import ChartsResource, AsyncChartsResource
from .resources.universe import UniverseResource, AsyncUniverseResource
from .resources.ai import AIResource, AsyncAIResource
from .resources.watchlist import WatchlistResource, AsyncWatchlistResource
from .resources.risk import RiskResource, AsyncRiskResource
from .resources.trades import TradesResource, AsyncTradesResource
from .resources.market import MarketResource, AsyncMarketResource


class LegendAI:
    """
    Synchronous Legend AI API Client

    Args:
        api_key: Optional API key for authentication
        base_url: Base URL for the API (default: production)
        timeout: Request timeout in seconds (default: 30)

    Example:
        >>> client = LegendAI()
        >>> pattern = client.patterns.detect("AAPL")
        >>> print(pattern.score)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://legend-ai-python-production.up.railway.app",
        timeout: float = 30.0,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        # HTTP client
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["X-API-Key"] = api_key

        self._client = httpx.Client(
            base_url=self.base_url,
            headers=headers,
            timeout=timeout,
        )

        # Resources
        self.patterns = PatternsResource(self)
        self.charts = ChartsResource(self)
        self.universe = UniverseResource(self)
        self.ai = AIResource(self)
        self.watchlist = WatchlistResource(self)
        self.risk = RiskResource(self)
        self.trades = TradesResource(self)
        self.market = MarketResource(self)

    def request(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an HTTP request to the API"""
        try:
            response = self._client.request(
                method=method,
                url=path,
                json=json,
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            self._handle_error(e)
        except httpx.RequestError as e:
            raise APIError(f"Request failed: {str(e)}")

    def _handle_error(self, error: httpx.HTTPStatusError) -> None:
        """Handle HTTP errors"""
        status_code = error.response.status_code
        try:
            error_data = error.response.json()
            message = error_data.get("error") or error_data.get("detail", "Unknown error")
        except Exception:
            message = error.response.text or "Unknown error"

        if status_code == 401:
            raise AuthenticationError(message)
        elif status_code == 429:
            raise RateLimitError(message)
        elif status_code == 400:
            raise ValidationError(message)
        else:
            raise APIError(f"{status_code}: {message}")

    def health(self) -> Dict[str, Any]:
        """Get API health status"""
        return self.request("GET", "/health")

    def version(self) -> Dict[str, Any]:
        """Get API version information"""
        return self.request("GET", "/api/version")

    def close(self) -> None:
        """Close the HTTP client"""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncLegendAI:
    """
    Asynchronous Legend AI API Client

    Args:
        api_key: Optional API key for authentication
        base_url: Base URL for the API (default: production)
        timeout: Request timeout in seconds (default: 30)

    Example:
        >>> async with AsyncLegendAI() as client:
        ...     pattern = await client.patterns.detect("AAPL")
        ...     print(pattern.score)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://legend-ai-python-production.up.railway.app",
        timeout: float = 30.0,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        # HTTP client
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["X-API-Key"] = api_key

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=timeout,
        )

        # Resources
        self.patterns = AsyncPatternsResource(self)
        self.charts = AsyncChartsResource(self)
        self.universe = AsyncUniverseResource(self)
        self.ai = AsyncAIResource(self)
        self.watchlist = AsyncWatchlistResource(self)
        self.risk = AsyncRiskResource(self)
        self.trades = AsyncTradesResource(self)
        self.market = AsyncMarketResource(self)

    async def request(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make an async HTTP request to the API"""
        try:
            response = await self._client.request(
                method=method,
                url=path,
                json=json,
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            self._handle_error(e)
        except httpx.RequestError as e:
            raise APIError(f"Request failed: {str(e)}")

    def _handle_error(self, error: httpx.HTTPStatusError) -> None:
        """Handle HTTP errors"""
        status_code = error.response.status_code
        try:
            error_data = error.response.json()
            message = error_data.get("error") or error_data.get("detail", "Unknown error")
        except Exception:
            message = error.response.text or "Unknown error"

        if status_code == 401:
            raise AuthenticationError(message)
        elif status_code == 429:
            raise RateLimitError(message)
        elif status_code == 400:
            raise ValidationError(message)
        else:
            raise APIError(f"{status_code}: {message}")

    async def health(self) -> Dict[str, Any]:
        """Get API health status"""
        return await self.request("GET", "/health")

    async def version(self) -> Dict[str, Any]:
        """Get API version information"""
        return await self.request("GET", "/api/version")

    async def close(self) -> None:
        """Close the HTTP client"""
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
