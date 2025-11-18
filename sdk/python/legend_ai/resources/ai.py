"""
AI assistant resource
"""

from typing import Optional, TYPE_CHECKING
from ..models import AIResponse

if TYPE_CHECKING:
    from ..client import LegendAI, AsyncLegendAI


class AIResource:
    """Synchronous AI assistant resource"""

    def __init__(self, client: "LegendAI"):
        self._client = client

    def chat(
        self,
        message: str,
        symbol: Optional[str] = None,
        include_market_data: bool = False,
        conversation_id: Optional[str] = None,
    ) -> AIResponse:
        """
        Chat with AI trading assistant

        Args:
            message: Your message/question
            symbol: Optional stock symbol for context
            include_market_data: Include market data in context
            conversation_id: ID for multi-turn conversations

        Returns:
            AIResponse with AI's response
        """
        payload = {"message": message}
        if symbol:
            payload["symbol"] = symbol
        if include_market_data:
            payload["include_market_data"] = True
        if conversation_id:
            payload["conversation_id"] = conversation_id

        response = self._client.request("POST", "/api/ai/chat", json=payload)
        return AIResponse.from_dict(response)

    def analyze(self, symbol: str) -> dict:
        """
        Get AI-powered stock analysis

        Args:
            symbol: Stock ticker symbol

        Returns:
            Analysis dictionary
        """
        return self._client.request(
            "POST",
            "/api/ai/analyze",
            json={"symbol": symbol},
        )


class AsyncAIResource:
    """Asynchronous AI assistant resource"""

    def __init__(self, client: "AsyncLegendAI"):
        self._client = client

    async def chat(
        self,
        message: str,
        symbol: Optional[str] = None,
        include_market_data: bool = False,
        conversation_id: Optional[str] = None,
    ) -> AIResponse:
        """Chat with AI trading assistant (async)"""
        payload = {"message": message}
        if symbol:
            payload["symbol"] = symbol
        if include_market_data:
            payload["include_market_data"] = True
        if conversation_id:
            payload["conversation_id"] = conversation_id

        response = await self._client.request("POST", "/api/ai/chat", json=payload)
        return AIResponse.from_dict(response)

    async def analyze(self, symbol: str) -> dict:
        """Get AI-powered stock analysis (async)"""
        return await self._client.request(
            "POST",
            "/api/ai/analyze",
            json={"symbol": symbol},
        )
