import logging
import aiohttp
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from textblob import TextBlob
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class NewsService:
    def __init__(self):
        self.api_key = settings.finnhub_api_key
        self.base_url = "https://finnhub.io/api/v1"
        self.session = None

    async def _get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def get_market_news(self, category: str = "general") -> List[Dict]:
        """Get general market news"""
        if not self.api_key:
            return []

        try:
            session = await self._get_session()
            url = f"{self.base_url}/news?category={category}&token={self.api_key}"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_news(data[:10]) # Limit to 10
                else:
                    logger.error(f"Finnhub news error: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"News fetch error: {e}")
            return []

    async def get_company_news(self, symbol: str) -> List[Dict]:
        """Get specific company news"""
        if not self.api_key:
            return []

        try:
            session = await self._get_session()
            # Get last 7 days
            to_date = datetime.now().strftime("%Y-%m-%d")
            from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            
            url = f"{self.base_url}/company-news?symbol={symbol}&from={from_date}&to={to_date}&token={self.api_key}"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._process_news(data[:5])
                return []
        except Exception as e:
            logger.error(f"Company news error: {e}")
            return []

    def _process_news(self, news_items: List[Dict]) -> List[Dict]:
        """Add sentiment analysis to news"""
        processed = []
        for item in news_items:
            headline = item.get('headline', '')
            summary = item.get('summary', '')
            text = f"{headline} {summary}"
            
            # Sentiment Analysis
            blob = TextBlob(text)
            sentiment_score = blob.sentiment.polarity
            
            sentiment = "Neutral"
            if sentiment_score > 0.1: sentiment = "Positive"
            if sentiment_score < -0.1: sentiment = "Negative"
            
            processed.append({
                "id": item.get('id'),
                "headline": headline,
                "summary": summary,
                "source": item.get('source'),
                "url": item.get('url'),
                "datetime": item.get('datetime'),
                "sentiment": sentiment,
                "sentiment_score": round(sentiment_score, 2),
                "image": item.get('image')
            })
        return processed

news_service = NewsService()
