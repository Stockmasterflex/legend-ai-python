"""
Real-Time News Sentiment Analysis Service
Multi-source news aggregation with AI-powered sentiment scoring
"""
import httpx
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timedelta
import asyncio
import logging
from enum import Enum
import json
import re
from collections import defaultdict

from app.config import get_settings
from app.services.cache import get_cache_service
from app.models import NewsArticle, SentimentScore
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class NewsSource(str, Enum):
    ALPHA_VANTAGE = "alpha_vantage"
    FINNHUB = "finnhub"
    NEWSAPI = "newsapi"
    BENZINGA = "benzinga"
    CACHE = "cache"


class SentimentAnalyzer(str, Enum):
    VADER = "vader"
    FINBERT = "finbert"
    OPENAI = "openai"


class SentimentService:
    """
    Real-time news sentiment analysis service with multi-source aggregation

    Features:
    - Multi-source news aggregation (Alpha Vantage, Finnhub, NewsAPI, Benzinga)
    - AI-powered sentiment analysis (VADER, FinBERT, OpenAI)
    - Real-time sentiment scoring and trend detection
    - Breaking news alerts
    - Price correlation and impact analysis
    - Redis caching for performance
    """

    def __init__(self):
        self.settings = get_settings()
        self.cache = get_cache_service()
        self.client = httpx.AsyncClient(timeout=30.0)

        # API usage tracking
        self.usage_key_prefix = "sentiment_api_usage"

        # Lazy load sentiment analyzers
        self._vader_analyzer = None
        self._finbert_model = None
        self._finbert_tokenizer = None

        # Breaking news keywords
        self.breaking_keywords = set(
            kw.strip().lower()
            for kw in self.settings.breaking_news_keywords.split(',')
        )

    async def get_usage_stats(self) -> Dict[str, Any]:
        """Get current API usage for news sources"""
        try:
            alpha_usage = await self.cache.get(f"{self.usage_key_prefix}:alphavantage") or 0
            finnhub_usage = await self.cache.get(f"{self.usage_key_prefix}:finnhub") or 0
            newsapi_usage = await self.cache.get(f"{self.usage_key_prefix}:newsapi") or 0
            benzinga_usage = await self.cache.get(f"{self.usage_key_prefix}:benzinga") or 0

            return {
                "alphavantage": {
                    "used": int(alpha_usage),
                    "limit": self.settings.alpha_vantage_daily_limit,
                    "remaining": self.settings.alpha_vantage_daily_limit - int(alpha_usage),
                },
                "finnhub": {
                    "used": int(finnhub_usage),
                    "limit": self.settings.finnhub_daily_limit,
                    "remaining": self.settings.finnhub_daily_limit - int(finnhub_usage),
                },
                "newsapi": {
                    "used": int(newsapi_usage),
                    "limit": self.settings.newsapi_daily_limit,
                    "remaining": self.settings.newsapi_daily_limit - int(newsapi_usage),
                },
                "benzinga": {
                    "used": int(benzinga_usage),
                    "limit": self.settings.benzinga_daily_limit,
                    "remaining": self.settings.benzinga_daily_limit - int(benzinga_usage),
                }
            }
        except Exception as e:
            logger.warning(f"Error getting sentiment API usage stats: {e}")
            return {"error": str(e)}

    async def _increment_usage(self, source: NewsSource):
        """Increment API usage counter (resets daily)"""
        try:
            key = f"{self.usage_key_prefix}:{source.value}"
            current = await self.cache.get(key) or 0
            await self.cache.set(key, int(current) + 1, ttl=86400)  # 24 hours
        except Exception as e:
            logger.warning(f"Error incrementing usage for {source}: {e}")

    async def _check_rate_limit(self, source: NewsSource) -> bool:
        """Check if we can make a request to this source"""
        try:
            key = f"{self.usage_key_prefix}:{source.value}"
            current = await self.cache.get(key) or 0

            limits = {
                NewsSource.ALPHA_VANTAGE: self.settings.alpha_vantage_daily_limit,
                NewsSource.FINNHUB: self.settings.finnhub_daily_limit,
                NewsSource.NEWSAPI: self.settings.newsapi_daily_limit,
                NewsSource.BENZINGA: self.settings.benzinga_daily_limit,
            }

            limit = limits.get(source, 999999)
            can_request = int(current) < limit

            if not can_request:
                logger.warning(f"Rate limit reached for {source.value}")

            return can_request
        except Exception as e:
            logger.warning(f"Error checking rate limit for {source}: {e}")
            return True  # Allow request if check fails

    # ========== News Aggregation ==========

    async def fetch_news_alpha_vantage(
        self,
        symbol: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Fetch news from Alpha Vantage News API"""
        if not self.settings.alpha_vantage_api_key:
            logger.warning("Alpha Vantage API key not configured")
            return []

        if not await self._check_rate_limit(NewsSource.ALPHA_VANTAGE):
            return []

        try:
            # Alpha Vantage News & Sentiment API
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "NEWS_SENTIMENT",
                "tickers": symbol,
                "apikey": self.settings.alpha_vantage_api_key,
                "limit": limit,
            }

            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            await self._increment_usage(NewsSource.ALPHA_VANTAGE)

            if "feed" not in data:
                logger.warning(f"No news feed in Alpha Vantage response for {symbol}")
                return []

            articles = []
            for item in data.get("feed", [])[:limit]:
                # Find ticker sentiment in the article
                ticker_sentiment = 0.0
                for ticker_data in item.get("ticker_sentiment", []):
                    if ticker_data.get("ticker") == symbol:
                        ticker_sentiment = float(ticker_data.get("ticker_sentiment_score", 0))
                        break

                articles.append({
                    "title": item.get("title"),
                    "summary": item.get("summary"),
                    "url": item.get("url"),
                    "source": item.get("source"),
                    "author": item.get("authors", [None])[0] if item.get("authors") else None,
                    "published_at": datetime.fromisoformat(item["time_published"].replace("T", " ").replace("Z", "")),
                    "category": item.get("category_within_source"),
                    "topics": [t.get("topic") for t in item.get("topics", [])],
                    "image_url": item.get("banner_image"),
                    "overall_sentiment_score": float(item.get("overall_sentiment_score", 0)),
                    "ticker_sentiment_score": ticker_sentiment,
                    "sentiment_label": item.get("overall_sentiment_label", "Neutral"),
                    "is_breaking": self._is_breaking_news(item.get("title", "")),
                    "fetched_source": NewsSource.ALPHA_VANTAGE,
                })

            logger.info(f"Fetched {len(articles)} articles from Alpha Vantage for {symbol}")
            return articles

        except Exception as e:
            logger.error(f"Error fetching Alpha Vantage news for {symbol}: {e}")
            return []

    async def fetch_news_finnhub(
        self,
        symbol: str,
        days_back: int = 7
    ) -> List[Dict[str, Any]]:
        """Fetch news from Finnhub"""
        if not self.settings.finnhub_api_key:
            logger.warning("Finnhub API key not configured")
            return []

        if not await self._check_rate_limit(NewsSource.FINNHUB):
            return []

        try:
            from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
            to_date = datetime.now().strftime("%Y-%m-%d")

            url = f"https://finnhub.io/api/v1/company-news"
            params = {
                "symbol": symbol,
                "from": from_date,
                "to": to_date,
                "token": self.settings.finnhub_api_key,
            }

            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            await self._increment_usage(NewsSource.FINNHUB)

            articles = []
            for item in data:
                articles.append({
                    "title": item.get("headline"),
                    "summary": item.get("summary"),
                    "url": item.get("url"),
                    "source": item.get("source"),
                    "author": None,
                    "published_at": datetime.fromtimestamp(item.get("datetime", 0)),
                    "category": item.get("category"),
                    "topics": [],
                    "image_url": item.get("image"),
                    "overall_sentiment_score": None,  # Finnhub doesn't provide sentiment
                    "ticker_sentiment_score": None,
                    "sentiment_label": None,
                    "is_breaking": self._is_breaking_news(item.get("headline", "")),
                    "fetched_source": NewsSource.FINNHUB,
                })

            logger.info(f"Fetched {len(articles)} articles from Finnhub for {symbol}")
            return articles

        except Exception as e:
            logger.error(f"Error fetching Finnhub news for {symbol}: {e}")
            return []

    async def fetch_news_newsapi(
        self,
        symbol: str,
        company_name: Optional[str] = None,
        days_back: int = 7
    ) -> List[Dict[str, Any]]:
        """Fetch news from NewsAPI"""
        if not self.settings.newsapi_api_key:
            logger.warning("NewsAPI key not configured")
            return []

        if not await self._check_rate_limit(NewsSource.NEWSAPI):
            return []

        try:
            # Build search query
            query = f"{symbol}"
            if company_name:
                query += f" OR {company_name}"

            from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")

            url = "https://newsapi.org/v2/everything"
            params = {
                "q": query,
                "from": from_date,
                "sortBy": "publishedAt",
                "language": "en",
                "apiKey": self.settings.newsapi_api_key,
            }

            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            await self._increment_usage(NewsSource.NEWSAPI)

            articles = []
            for item in data.get("articles", []):
                articles.append({
                    "title": item.get("title"),
                    "summary": item.get("description"),
                    "url": item.get("url"),
                    "source": item.get("source", {}).get("name"),
                    "author": item.get("author"),
                    "published_at": datetime.fromisoformat(item["publishedAt"].replace("Z", "+00:00")),
                    "category": None,
                    "topics": [],
                    "image_url": item.get("urlToImage"),
                    "overall_sentiment_score": None,
                    "ticker_sentiment_score": None,
                    "sentiment_label": None,
                    "is_breaking": self._is_breaking_news(item.get("title", "")),
                    "fetched_source": NewsSource.NEWSAPI,
                })

            logger.info(f"Fetched {len(articles)} articles from NewsAPI for {symbol}")
            return articles

        except Exception as e:
            logger.error(f"Error fetching NewsAPI news for {symbol}: {e}")
            return []

    async def aggregate_news(
        self,
        symbol: str,
        limit: int = 50,
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Aggregate news from multiple sources
        Returns unified list of news articles with deduplication
        """
        cache_key = f"news_aggregated:{symbol}:{limit}"

        # Check cache first
        if use_cache:
            cached = await self.cache.get(cache_key)
            if cached:
                logger.info(f"Returning cached news for {symbol}")
                return json.loads(cached)

        # Fetch from all available sources in parallel
        tasks = []

        if self.settings.alpha_vantage_api_key:
            tasks.append(self.fetch_news_alpha_vantage(symbol, limit))

        if self.settings.finnhub_api_key:
            tasks.append(self.fetch_news_finnhub(symbol))

        if self.settings.newsapi_api_key:
            tasks.append(self.fetch_news_newsapi(symbol))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Flatten and deduplicate articles
        all_articles = []
        seen_urls = set()

        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Error in news fetch task: {result}")
                continue

            for article in result:
                url = article.get("url")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    all_articles.append(article)

        # Sort by published date (newest first)
        all_articles.sort(key=lambda x: x.get("published_at", datetime.min), reverse=True)

        # Limit results
        all_articles = all_articles[:limit]

        # Cache results
        if all_articles:
            await self.cache.set(
                cache_key,
                json.dumps(all_articles, default=str),
                ttl=self.settings.cache_ttl_news
            )

        logger.info(f"Aggregated {len(all_articles)} unique articles for {symbol}")
        return all_articles

    # ========== Sentiment Analysis ==========

    def _get_vader_analyzer(self):
        """Lazy load VADER sentiment analyzer"""
        if self._vader_analyzer is None:
            try:
                from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
                self._vader_analyzer = SentimentIntensityAnalyzer()
                logger.info("VADER sentiment analyzer loaded")
            except ImportError:
                logger.error("vaderSentiment not installed. Run: pip install vaderSentiment")
                raise
        return self._vader_analyzer

    def _get_finbert_model(self):
        """Lazy load FinBERT model for financial sentiment analysis"""
        if self._finbert_model is None or self._finbert_tokenizer is None:
            try:
                from transformers import AutoTokenizer, AutoModelForSequenceClassification
                import torch

                model_name = "ProsusAI/finbert"
                self._finbert_tokenizer = AutoTokenizer.from_pretrained(model_name)
                self._finbert_model = AutoModelForSequenceClassification.from_pretrained(model_name)
                logger.info("FinBERT model loaded")
            except ImportError:
                logger.error("transformers not installed. Run: pip install transformers torch")
                raise
        return self._finbert_tokenizer, self._finbert_model

    async def analyze_sentiment_vader(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using VADER (fast, good for social media/news)"""
        try:
            analyzer = self._get_vader_analyzer()
            scores = analyzer.polarity_scores(text)

            # VADER returns: neg, neu, pos, compound
            # compound is the overall score (-1 to 1)
            return {
                "score": scores["compound"],
                "positive": scores["pos"],
                "negative": scores["neg"],
                "neutral": scores["neu"],
                "sentiment_label": self._get_sentiment_label(scores["compound"]),
                "confidence": max(scores["pos"], scores["neg"], scores["neu"]),
                "analyzer": SentimentAnalyzer.VADER.value,
            }
        except Exception as e:
            logger.error(f"Error in VADER sentiment analysis: {e}")
            return self._default_sentiment()

    async def analyze_sentiment_finbert(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using FinBERT (slower, specialized for finance)"""
        try:
            import torch
            tokenizer, model = self._get_finbert_model()

            # Tokenize and predict
            inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            outputs = model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

            # FinBERT classes: negative, neutral, positive
            probs = predictions.detach().numpy()[0]
            negative, neutral, positive = probs

            # Calculate compound score (-1 to 1)
            score = positive - negative

            return {
                "score": float(score),
                "positive": float(positive),
                "negative": float(negative),
                "neutral": float(neutral),
                "sentiment_label": self._get_sentiment_label(score),
                "confidence": float(max(probs)),
                "analyzer": SentimentAnalyzer.FINBERT.value,
            }
        except Exception as e:
            logger.error(f"Error in FinBERT sentiment analysis: {e}")
            # Fallback to VADER
            return await self.analyze_sentiment_vader(text)

    async def analyze_sentiment_openai(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using OpenAI GPT models"""
        try:
            if not self.settings.openai_api_key and not self.settings.openrouter_api_key:
                logger.warning("No OpenAI/OpenRouter API key configured, falling back to VADER")
                return await self.analyze_sentiment_vader(text)

            # Use OpenAI API for sentiment analysis
            # This is more expensive but very accurate
            # Implementation would use the AI service
            # For now, fallback to VADER
            logger.info("OpenAI sentiment analysis not yet implemented, using VADER")
            return await self.analyze_sentiment_vader(text)

        except Exception as e:
            logger.error(f"Error in OpenAI sentiment analysis: {e}")
            return await self.analyze_sentiment_vader(text)

    async def analyze_sentiment(
        self,
        text: str,
        analyzer: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze sentiment using the configured analyzer

        Args:
            text: Text to analyze
            analyzer: Override analyzer (vader, finbert, openai)

        Returns:
            Sentiment analysis result with score, labels, and confidence
        """
        if not text:
            return self._default_sentiment()

        analyzer = analyzer or self.settings.sentiment_analyzer

        if analyzer == "finbert":
            return await self.analyze_sentiment_finbert(text)
        elif analyzer == "openai":
            return await self.analyze_sentiment_openai(text)
        else:
            return await self.analyze_sentiment_vader(text)

    def _get_sentiment_label(self, score: float) -> str:
        """Convert sentiment score to label"""
        if score >= self.settings.sentiment_threshold_positive:
            return "positive"
        elif score <= self.settings.sentiment_threshold_negative:
            return "negative"
        else:
            return "neutral"

    def _default_sentiment(self) -> Dict[str, Any]:
        """Return default neutral sentiment"""
        return {
            "score": 0.0,
            "positive": 0.0,
            "negative": 0.0,
            "neutral": 1.0,
            "sentiment_label": "neutral",
            "confidence": 0.0,
            "analyzer": "default",
        }

    # ========== News & Sentiment Integration ==========

    async def get_news_with_sentiment(
        self,
        symbol: str,
        limit: int = 50,
        use_cache: bool = True,
        analyzer: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get news articles with sentiment analysis

        Returns articles with sentiment scores attached
        """
        cache_key = f"news_sentiment:{symbol}:{limit}:{analyzer or 'default'}"

        if use_cache:
            cached = await self.cache.get(cache_key)
            if cached:
                logger.info(f"Returning cached news with sentiment for {symbol}")
                return json.loads(cached)

        # Get aggregated news
        articles = await self.aggregate_news(symbol, limit, use_cache)

        # Analyze sentiment for each article
        for article in articles:
            # If article already has sentiment from source (e.g., Alpha Vantage), use it
            if article.get("overall_sentiment_score") is not None:
                # Normalize to our format
                article["sentiment"] = {
                    "score": article["overall_sentiment_score"],
                    "sentiment_label": article.get("sentiment_label", "neutral"),
                    "analyzer": "source_provided",
                    "confidence": 0.8,  # Assume high confidence from source
                }
            else:
                # Analyze using our analyzer
                text = f"{article.get('title', '')} {article.get('summary', '')}"
                sentiment = await self.analyze_sentiment(text, analyzer)
                article["sentiment"] = sentiment

        # Cache results
        if articles:
            await self.cache.set(
                cache_key,
                json.dumps(articles, default=str),
                ttl=self.settings.cache_ttl_sentiment
            )

        return articles

    # ========== Sentiment Trends & Shifts ==========

    async def get_sentiment_trend(
        self,
        symbol: str,
        hours_back: int = 24,
    ) -> Dict[str, Any]:
        """
        Get sentiment trend over time

        Returns:
            - Current sentiment score
            - Historical trend
            - Sentiment shift detection
        """
        cache_key = f"sentiment_trend:{symbol}:{hours_back}"

        cached = await self.cache.get(cache_key)
        if cached:
            return json.loads(cached)

        # Get news with sentiment
        articles = await self.get_news_with_sentiment(symbol, limit=100)

        # Filter by time window
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        recent_articles = [
            a for a in articles
            if a.get("published_at") and a["published_at"] > cutoff_time
        ]

        if not recent_articles:
            return {
                "symbol": symbol,
                "current_sentiment": 0.0,
                "sentiment_label": "neutral",
                "article_count": 0,
                "trend": "neutral",
                "shift_detected": False,
            }

        # Calculate current sentiment (weighted by recency)
        total_weight = 0
        weighted_sentiment = 0

        for article in recent_articles:
            sentiment = article.get("sentiment", {})
            score = sentiment.get("score", 0)

            # Weight more recent articles higher
            hours_old = (datetime.now() - article["published_at"]).total_seconds() / 3600
            weight = max(0.1, 1.0 - (hours_old / hours_back))

            weighted_sentiment += score * weight
            total_weight += weight

        current_sentiment = weighted_sentiment / total_weight if total_weight > 0 else 0

        # Detect sentiment shift
        # Compare first half vs second half of time window
        midpoint = cutoff_time + timedelta(hours=hours_back/2)

        older_articles = [a for a in recent_articles if a["published_at"] < midpoint]
        newer_articles = [a for a in recent_articles if a["published_at"] >= midpoint]

        older_sentiment = sum(a.get("sentiment", {}).get("score", 0) for a in older_articles) / len(older_articles) if older_articles else 0
        newer_sentiment = sum(a.get("sentiment", {}).get("score", 0) for a in newer_articles) / len(newer_articles) if newer_articles else 0

        shift_magnitude = abs(newer_sentiment - older_sentiment)
        shift_detected = shift_magnitude >= self.settings.sentiment_shift_threshold

        # Determine trend
        if shift_detected:
            trend = "improving" if newer_sentiment > older_sentiment else "deteriorating"
        else:
            trend = "stable"

        result = {
            "symbol": symbol,
            "current_sentiment": round(current_sentiment, 4),
            "sentiment_label": self._get_sentiment_label(current_sentiment),
            "article_count": len(recent_articles),
            "hours_analyzed": hours_back,
            "trend": trend,
            "shift_detected": shift_detected,
            "shift_magnitude": round(shift_magnitude, 4) if shift_detected else 0,
            "older_sentiment": round(older_sentiment, 4),
            "newer_sentiment": round(newer_sentiment, 4),
            "positive_count": sum(1 for a in recent_articles if a.get("sentiment", {}).get("sentiment_label") == "positive"),
            "negative_count": sum(1 for a in recent_articles if a.get("sentiment", {}).get("sentiment_label") == "negative"),
            "neutral_count": sum(1 for a in recent_articles if a.get("sentiment", {}).get("sentiment_label") == "neutral"),
            "breaking_news_count": sum(1 for a in recent_articles if a.get("is_breaking")),
        }

        # Cache for shorter time since this is real-time data
        await self.cache.set(
            cache_key,
            json.dumps(result, default=str),
            ttl=300  # 5 minutes
        )

        return result

    # ========== Breaking News Detection ==========

    def _is_breaking_news(self, title: str) -> bool:
        """Detect if news is breaking/urgent based on keywords"""
        if not title:
            return False

        title_lower = title.lower()
        return any(keyword in title_lower for keyword in self.breaking_keywords)

    async def get_breaking_news(
        self,
        symbol: str,
        hours_back: int = 2
    ) -> List[Dict[str, Any]]:
        """Get breaking news for a symbol"""
        articles = await self.get_news_with_sentiment(symbol, limit=50)

        # Filter breaking news
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        breaking = [
            a for a in articles
            if a.get("is_breaking") and a.get("published_at", datetime.min) > cutoff_time
        ]

        # Sort by published date (newest first)
        breaking.sort(key=lambda x: x.get("published_at", datetime.min), reverse=True)

        return breaking

    # ========== News Impact Analysis ==========

    async def analyze_news_impact(
        self,
        symbol: str,
        hours_back: int = 24,
    ) -> Dict[str, Any]:
        """
        Analyze correlation between news sentiment and price/volume changes

        Correlates sentiment shifts with:
        - Price movements
        - Volume changes
        - Volatility spikes
        """
        try:
            from app.services.market_data import market_data_service

            # Get sentiment trend
            sentiment_trend = await self.get_sentiment_trend(symbol, hours_back)

            # Get news with sentiment
            articles = await self.get_news_with_sentiment(symbol, limit=100)

            # Get current market data
            market_data = await market_data_service.get_quote(symbol)
            if not market_data or "error" in market_data:
                logger.warning(f"Could not fetch market data for {symbol}")
                return {
                    "symbol": symbol,
                    "error": "Market data unavailable",
                    "sentiment_trend": sentiment_trend,
                }

            current_price = market_data.get("price", 0)
            current_volume = market_data.get("volume", 0)

            # Calculate impact metrics
            impacts = []
            for article in articles:
                sentiment = article.get("sentiment", {})
                published_at = article.get("published_at")

                if not published_at:
                    continue

                # Calculate time since publication
                hours_since = (datetime.now() - published_at).total_seconds() / 3600

                if hours_since > hours_back:
                    continue

                # Estimate impact score based on:
                # 1. Sentiment strength
                # 2. Recency (more recent = higher impact)
                # 3. Breaking news (higher impact)
                sentiment_score = abs(sentiment.get("score", 0))
                recency_factor = max(0.1, 1.0 - (hours_since / hours_back))
                breaking_factor = 2.0 if article.get("is_breaking") else 1.0

                impact_score = sentiment_score * recency_factor * breaking_factor

                impacts.append({
                    "title": article.get("title"),
                    "published_at": published_at,
                    "hours_since": round(hours_since, 2),
                    "sentiment_score": sentiment.get("score", 0),
                    "sentiment_label": sentiment.get("sentiment_label"),
                    "is_breaking": article.get("is_breaking", False),
                    "impact_score": round(impact_score, 4),
                })

            # Sort by impact score
            impacts.sort(key=lambda x: x["impact_score"], reverse=True)

            # Calculate aggregate impact
            total_impact = sum(i["impact_score"] for i in impacts)
            avg_impact = total_impact / len(impacts) if impacts else 0

            # Determine if sentiment likely impacting price
            high_impact_threshold = 0.5
            has_high_impact = avg_impact > high_impact_threshold

            # Pattern invalidation warning
            # If strong negative sentiment + breaking news, warn about pattern risk
            pattern_risk = False
            risk_reason = None

            if sentiment_trend.get("shift_detected"):
                if sentiment_trend.get("newer_sentiment", 0) < -0.3:
                    pattern_risk = True
                    risk_reason = "Significant negative sentiment shift detected"
                elif sentiment_trend.get("breaking_news_count", 0) > 0:
                    if sentiment_trend.get("negative_count", 0) > sentiment_trend.get("positive_count", 0):
                        pattern_risk = True
                        risk_reason = "Breaking news with negative sentiment"

            return {
                "symbol": symbol,
                "current_price": current_price,
                "current_volume": current_volume,
                "sentiment_trend": sentiment_trend,
                "impact_analysis": {
                    "total_articles_analyzed": len(impacts),
                    "total_impact_score": round(total_impact, 4),
                    "average_impact_score": round(avg_impact, 4),
                    "has_high_impact": has_high_impact,
                    "high_impact_threshold": high_impact_threshold,
                },
                "top_impact_news": impacts[:10],  # Top 10 highest impact
                "pattern_invalidation_warning": {
                    "risk_detected": pattern_risk,
                    "reason": risk_reason,
                    "recommendation": "Monitor price action closely and consider tightening stops" if pattern_risk else None,
                },
                "opportunity_alerts": self._detect_opportunities(sentiment_trend, impacts),
            }

        except Exception as e:
            logger.error(f"Error analyzing news impact for {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": str(e),
            }

    def _detect_opportunities(
        self,
        sentiment_trend: Dict[str, Any],
        impacts: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """Detect trading opportunities based on sentiment"""
        opportunities = []

        # Opportunity 1: Strong positive sentiment shift
        if sentiment_trend.get("shift_detected"):
            if sentiment_trend.get("trend") == "improving":
                if sentiment_trend.get("newer_sentiment", 0) > 0.3:
                    opportunities.append({
                        "type": "bullish_sentiment_shift",
                        "signal": "Strong positive sentiment shift detected",
                        "action": "Watch for breakout confirmation",
                        "confidence": "medium",
                    })

        # Opportunity 2: Negative sentiment but price holding
        # (potential contrarian setup)
        if sentiment_trend.get("current_sentiment", 0) < -0.2:
            opportunities.append({
                "type": "contrarian_setup",
                "signal": "Negative sentiment present",
                "action": "Monitor for potential capitulation bottom",
                "confidence": "low",
            })

        # Opportunity 3: Breaking news with strong positive sentiment
        breaking_positive = [
            i for i in impacts
            if i.get("is_breaking") and i.get("sentiment_label") == "positive"
        ]
        if breaking_positive:
            opportunities.append({
                "type": "breaking_news_catalyst",
                "signal": f"Breaking news with positive sentiment ({len(breaking_positive)} articles)",
                "action": "Watch for immediate price reaction",
                "confidence": "high",
            })

        # Opportunity 4: Sentiment alignment with technical setup
        if sentiment_trend.get("positive_count", 0) > sentiment_trend.get("negative_count", 0) * 2:
            opportunities.append({
                "type": "sentiment_confirmation",
                "signal": "Strong positive sentiment consensus",
                "action": "Look for technical confirmation (volume, breakout)",
                "confidence": "medium",
            })

        return opportunities

    async def get_volume_correlation(
        self,
        symbol: str,
        hours_back: int = 24,
    ) -> Dict[str, Any]:
        """
        Analyze correlation between news frequency and volume changes

        High news volume often correlates with trading volume spikes
        """
        try:
            from app.services.market_data import market_data_service

            # Get news articles
            articles = await self.get_news_with_sentiment(symbol, limit=100)

            # Filter by time window
            cutoff_time = datetime.now() - timedelta(hours=hours_back)
            recent_articles = [
                a for a in articles
                if a.get("published_at") and a["published_at"] > cutoff_time
            ]

            # Get historical volume (if available)
            # For now, we'll just report news frequency
            hours_with_news = defaultdict(int)
            for article in recent_articles:
                hour = article["published_at"].replace(minute=0, second=0, microsecond=0)
                hours_with_news[hour] += 1

            # Find peak news hours
            if hours_with_news:
                peak_hour = max(hours_with_news.items(), key=lambda x: x[1])
                avg_news_per_hour = sum(hours_with_news.values()) / len(hours_with_news)

                return {
                    "symbol": symbol,
                    "hours_analyzed": hours_back,
                    "total_articles": len(recent_articles),
                    "hours_with_news": len(hours_with_news),
                    "peak_news_hour": peak_hour[0].isoformat(),
                    "peak_news_count": peak_hour[1],
                    "avg_news_per_hour": round(avg_news_per_hour, 2),
                    "news_intensity": "high" if avg_news_per_hour > 5 else "medium" if avg_news_per_hour > 2 else "low",
                    "volume_spike_likely": peak_hour[1] > 10,  # More than 10 articles in one hour
                }
            else:
                return {
                    "symbol": symbol,
                    "hours_analyzed": hours_back,
                    "total_articles": 0,
                    "news_intensity": "none",
                    "volume_spike_likely": False,
                }

        except Exception as e:
            logger.error(f"Error analyzing volume correlation for {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": str(e),
            }

    # ========== Utility Methods ==========

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Singleton instance
_sentiment_service = None


def get_sentiment_service() -> SentimentService:
    """Get or create sentiment service instance"""
    global _sentiment_service
    if _sentiment_service is None:
        _sentiment_service = SentimentService()
    return _sentiment_service
