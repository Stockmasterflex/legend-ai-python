"""
News Service - Fetches market news with sentiment analysis
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import aiohttp
from textblob import TextBlob

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class NewsService:
    """Service for fetching and analyzing market news"""

    def __init__(self):
        self.api_key = settings.finnhub_api_key
        self.base_url = "https://finnhub.io/api/v1"
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self._session

    async def close(self):
        """Close the aiohttp session"""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def get_market_news(self, category: str = "general") -> List[Dict]:
        """
        Get general market news

        Args:
            category: News category (general, forex, crypto, merger)

        Returns:
            List of news items with sentiment analysis
        """
        if not self.api_key:
            logger.warning("Finnhub API key not configured - returning empty news")
            return []

        try:
            session = await self._get_session()
            url = f"{self.base_url}/news?category={category}&token={self.api_key}"

            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_news(data[:10])  # Limit to 10
                else:
                    logger.error(f"Finnhub news error: {response.status}")
                    return []
        except aiohttp.ClientError as e:
            logger.error(f"Network error fetching news: {e}")
            return []
        except Exception as e:
            logger.error(f"News fetch error: {e}")
            return []

    async def get_company_news(self, symbol: str, days: int = 7) -> List[Dict]:
        """
        Get specific company news

        Args:
            symbol: Stock symbol
            days: Number of days of history (default 7)

        Returns:
            List of company news items with sentiment
        """
        if not self.api_key:
            logger.warning("Finnhub API key not configured")
            return []

        try:
            session = await self._get_session()
            to_date = datetime.now().strftime("%Y-%m-%d")
            from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

            url = f"{self.base_url}/company-news?symbol={symbol}&from={from_date}&to={to_date}&token={self.api_key}"

            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_news(data[:5])
                elif response.status == 429:
                    logger.warning("Finnhub rate limit hit")
                    return []
                else:
                    logger.error(f"Finnhub company news error: {response.status}")
                    return []
        except aiohttp.ClientError as e:
            logger.error(f"Network error fetching company news: {e}")
            return []
        except Exception as e:
            logger.error(f"Company news error: {e}")
            return []

    async def get_market_sentiment(self, symbol: str) -> Dict:
        """
        Get overall market sentiment for a symbol based on recent news

        Args:
            symbol: Stock symbol

        Returns:
            Sentiment summary dict
        """
        news = await self.get_company_news(symbol, days=3)

        if not news:
            return {
                "symbol": symbol,
                "overall_sentiment": "neutral",
                "score": 0.0,
                "news_count": 0,
                "positive_count": 0,
                "negative_count": 0,
                "neutral_count": 0,
            }

        positive = sum(1 for n in news if n.get("sentiment") == "Positive")
        negative = sum(1 for n in news if n.get("sentiment") == "Negative")
        neutral = sum(1 for n in news if n.get("sentiment") == "Neutral")

        avg_score = sum(n.get("sentiment_score", 0) for n in news) / len(news)

        if avg_score > 0.1:
            overall = "bullish"
        elif avg_score < -0.1:
            overall = "bearish"
        else:
            overall = "neutral"

        return {
            "symbol": symbol,
            "overall_sentiment": overall,
            "score": round(avg_score, 3),
            "news_count": len(news),
            "positive_count": positive,
            "negative_count": negative,
            "neutral_count": neutral,
        }

    def _process_news(self, news_items: List[Dict]) -> List[Dict]:
        """
        Add sentiment analysis to news items

        Args:
            news_items: Raw news items from Finnhub

        Returns:
            Processed news items with sentiment
        """
        processed = []
        for item in news_items:
            headline = item.get("headline", "")
            summary = item.get("summary", "")
            text = f"{headline} {summary}"

            # Sentiment Analysis using TextBlob
            try:
                blob = TextBlob(text)
                sentiment_score = blob.sentiment.polarity
            except Exception:
                sentiment_score = 0.0

            # Classify sentiment
            if sentiment_score > 0.1:
                sentiment = "Positive"
            elif sentiment_score < -0.1:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"

            # Convert Unix timestamp to ISO format
            timestamp = item.get("datetime")
            if timestamp:
                try:
                    timestamp_iso = datetime.fromtimestamp(timestamp).isoformat()
                except (ValueError, OSError):
                    timestamp_iso = None
            else:
                timestamp_iso = None

            processed.append(
                {
                    "id": item.get("id"),
                    "headline": headline,
                    "summary": summary,
                    "source": item.get("source"),
                    "url": item.get("url"),
                    "datetime": timestamp_iso,
                    "timestamp": timestamp,
                    "sentiment": sentiment,
                    "sentiment_score": round(sentiment_score, 3),
                    "image": item.get("image"),
                    "related": (
                        item.get("related", "").split(",")
                        if item.get("related")
                        else []
                    ),
                }
            )
        return processed


# Global instance
news_service = NewsService()
