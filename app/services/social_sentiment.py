"""
Social Sentiment Service
Tracks social media sentiment from Twitter, Reddit, and StockTwits
"""
import logging
import json
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy import select, and_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from app.config import get_settings
from app.services.cache import get_cache_service
from app.models import SocialSentiment, Ticker

logger = logging.getLogger(__name__)


class SocialSentimentService:
    """
    Service for tracking social media sentiment

    Features:
    - Track Twitter mentions and sentiment
    - Monitor Reddit discussions
    - StockTwits sentiment analysis
    - Trend detection and alerts
    """

    def __init__(self):
        self.settings = get_settings()
        self.cache = get_cache_service()
        self.cache_prefix = "social_sentiment"
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get_sentiment(
        self,
        db: AsyncSession,
        symbol: str,
        source: Optional[str] = None,
        lookback_days: int = 7
    ) -> List[Dict[str, Any]]:
        """
        Get social sentiment data for a symbol

        Args:
            db: Database session
            symbol: Ticker symbol
            source: Filter by source (twitter, reddit, stocktwits)
            lookback_days: Days to look back

        Returns:
            List of sentiment records
        """
        try:
            cache_key = f"{self.cache_prefix}:sentiment:{symbol}:{source or 'all'}:{lookback_days}"
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

            # Get ticker
            result = await db.execute(
                select(Ticker).where(Ticker.symbol == symbol.upper())
            )
            ticker = result.scalar_one_or_none()
            if not ticker:
                return []

            cutoff_date = datetime.utcnow() - timedelta(days=lookback_days)

            # Build query
            query = select(SocialSentiment).where(
                and_(
                    SocialSentiment.ticker_id == ticker.id,
                    SocialSentiment.sentiment_date >= cutoff_date
                )
            )

            if source:
                query = query.where(SocialSentiment.source == source)

            query = query.order_by(desc(SocialSentiment.sentiment_date))

            result = await db.execute(query)
            sentiments = result.scalars().all()

            sentiment_data = []
            for sentiment in sentiments:
                sentiment_data.append({
                    "source": sentiment.source,
                    "sentiment_date": sentiment.sentiment_date.isoformat() if sentiment.sentiment_date else None,
                    "sentiment_score": sentiment.sentiment_score,
                    "sentiment_label": sentiment.sentiment_label,
                    "mention_count": sentiment.mention_count,
                    "positive_mentions": sentiment.positive_mentions,
                    "negative_mentions": sentiment.negative_mentions,
                    "neutral_mentions": sentiment.neutral_mentions,
                    "total_engagement": sentiment.total_engagement,
                    "reach": sentiment.reach,
                    "trending": sentiment.trending,
                })

            await self.cache.set(cache_key, sentiment_data, ttl=1800)  # 30 minutes
            return sentiment_data

        except Exception as e:
            logger.error(f"Error getting sentiment for {symbol}: {e}")
            return []

    async def get_aggregated_sentiment(
        self,
        db: AsyncSession,
        symbol: str,
        lookback_days: int = 7
    ) -> Dict[str, Any]:
        """
        Get aggregated sentiment across all sources

        Args:
            db: Database session
            symbol: Ticker symbol
            lookback_days: Days to look back

        Returns:
            Aggregated sentiment metrics
        """
        try:
            cache_key = f"{self.cache_prefix}:aggregated:{symbol}:{lookback_days}"
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

            # Get ticker
            result = await db.execute(
                select(Ticker).where(Ticker.symbol == symbol.upper())
            )
            ticker = result.scalar_one_or_none()
            if not ticker:
                return {"error": "Ticker not found"}

            cutoff_date = datetime.utcnow() - timedelta(days=lookback_days)

            # Get all sentiment records
            query = select(SocialSentiment).where(
                and_(
                    SocialSentiment.ticker_id == ticker.id,
                    SocialSentiment.sentiment_date >= cutoff_date
                )
            )

            result = await db.execute(query)
            sentiments = result.scalars().all()

            if not sentiments:
                return {
                    "symbol": symbol.upper(),
                    "lookback_days": lookback_days,
                    "overall_sentiment": "neutral",
                    "overall_score": 0.0,
                    "total_mentions": 0,
                    "sources": []
                }

            # Aggregate by source
            by_source = {}
            total_mentions = 0
            total_engagement = 0
            weighted_sentiment_sum = 0
            total_weight = 0

            for sentiment in sentiments:
                source = sentiment.source
                if source not in by_source:
                    by_source[source] = {
                        "source": source,
                        "mention_count": 0,
                        "avg_sentiment": 0.0,
                        "total_engagement": 0,
                        "sentiment_scores": [],
                        "trending_count": 0,
                    }

                by_source[source]["mention_count"] += sentiment.mention_count
                by_source[source]["total_engagement"] += sentiment.total_engagement
                by_source[source]["sentiment_scores"].append(sentiment.sentiment_score)
                if sentiment.trending:
                    by_source[source]["trending_count"] += 1

                total_mentions += sentiment.mention_count
                total_engagement += sentiment.total_engagement

                # Weight sentiment by mention count
                weight = sentiment.mention_count
                weighted_sentiment_sum += sentiment.sentiment_score * weight
                total_weight += weight

            # Calculate averages per source
            for source_data in by_source.values():
                scores = source_data["sentiment_scores"]
                source_data["avg_sentiment"] = round(sum(scores) / len(scores), 3) if scores else 0.0
                source_data["sentiment_label"] = self._score_to_label(source_data["avg_sentiment"])
                del source_data["sentiment_scores"]  # Remove intermediate data

            # Overall sentiment
            overall_score = weighted_sentiment_sum / total_weight if total_weight > 0 else 0.0
            overall_label = self._score_to_label(overall_score)

            # Sentiment trend (compare first half to second half)
            mid_point = len(sentiments) // 2
            if mid_point > 0:
                first_half_avg = sum(s.sentiment_score for s in sentiments[:mid_point]) / mid_point
                second_half_avg = sum(s.sentiment_score for s in sentiments[mid_point:]) / (len(sentiments) - mid_point)
                sentiment_trend = "improving" if second_half_avg > first_half_avg + 0.1 else "declining" if second_half_avg < first_half_avg - 0.1 else "stable"
            else:
                sentiment_trend = "stable"

            # Check if trending
            is_trending = any(s.trending for s in sentiments)

            aggregated = {
                "symbol": symbol.upper(),
                "lookback_days": lookback_days,
                "overall_sentiment": overall_label,
                "overall_score": round(overall_score, 3),
                "sentiment_trend": sentiment_trend,
                "total_mentions": total_mentions,
                "total_engagement": total_engagement,
                "is_trending": is_trending,
                "sources": list(by_source.values()),
                "analyzed_at": datetime.utcnow().isoformat(),
            }

            await self.cache.set(cache_key, aggregated, ttl=1800)  # 30 minutes
            return aggregated

        except Exception as e:
            logger.error(f"Error getting aggregated sentiment for {symbol}: {e}")
            return {"error": str(e)}

    async def get_sentiment_comparison(
        self,
        db: AsyncSession,
        symbols: List[str],
        lookback_days: int = 7
    ) -> Dict[str, Any]:
        """
        Compare sentiment across multiple stocks

        Args:
            db: Database session
            symbols: List of ticker symbols
            lookback_days: Days to look back

        Returns:
            Comparative sentiment analysis
        """
        try:
            cache_key = f"{self.cache_prefix}:comparison:{':'.join(sorted(symbols))}:{lookback_days}"
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

            comparisons = []
            for symbol in symbols:
                sentiment = await self.get_aggregated_sentiment(db, symbol, lookback_days)
                if "error" not in sentiment:
                    comparisons.append(sentiment)

            # Rank by overall score
            ranked = sorted(comparisons, key=lambda x: x["overall_score"], reverse=True)

            # Add rankings
            for i, comp in enumerate(ranked):
                comp["rank"] = i + 1

            result = {
                "compared_at": datetime.utcnow().isoformat(),
                "lookback_days": lookback_days,
                "stocks": ranked,
                "most_positive": ranked[0] if ranked else None,
                "most_negative": ranked[-1] if ranked else None,
                "summary": {
                    "avg_sentiment_score": round(sum(c["overall_score"] for c in comparisons) / len(comparisons), 3) if comparisons else 0,
                    "total_mentions": sum(c["total_mentions"] for c in comparisons),
                    "trending_count": sum(1 for c in comparisons if c.get("is_trending")),
                }
            }

            await self.cache.set(cache_key, result, ttl=1800)  # 30 minutes
            return result

        except Exception as e:
            logger.error(f"Error comparing sentiment: {e}")
            return {"error": str(e)}

    async def get_trending_stocks(
        self,
        db: AsyncSession,
        source: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Get currently trending stocks on social media

        Args:
            db: Database session
            source: Filter by source
            limit: Number of stocks to return

        Returns:
            List of trending stocks
        """
        try:
            cache_key = f"{self.cache_prefix}:trending:{source or 'all'}:{limit}"
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

            # Get recent sentiment data (last 24 hours)
            cutoff_date = datetime.utcnow() - timedelta(hours=24)

            query = (
                select(
                    Ticker.symbol,
                    Ticker.name,
                    func.sum(SocialSentiment.mention_count).label('total_mentions'),
                    func.sum(SocialSentiment.total_engagement).label('total_engagement'),
                    func.avg(SocialSentiment.sentiment_score).label('avg_sentiment')
                )
                .join(Ticker, SocialSentiment.ticker_id == Ticker.id)
                .where(SocialSentiment.sentiment_date >= cutoff_date)
            )

            if source:
                query = query.where(SocialSentiment.source == source)

            query = (
                query.group_by(Ticker.symbol, Ticker.name)
                .order_by(desc('total_mentions'))
                .limit(limit)
            )

            result = await db.execute(query)
            trending = []

            for row in result:
                trending.append({
                    "symbol": row.symbol,
                    "name": row.name,
                    "total_mentions": int(row.total_mentions),
                    "total_engagement": int(row.total_engagement),
                    "avg_sentiment": round(float(row.avg_sentiment), 3),
                    "sentiment_label": self._score_to_label(float(row.avg_sentiment)),
                })

            await self.cache.set(cache_key, trending, ttl=1800)  # 30 minutes
            return trending

        except Exception as e:
            logger.error(f"Error getting trending stocks: {e}")
            return []

    async def get_sentiment_timeline(
        self,
        db: AsyncSession,
        symbol: str,
        source: Optional[str] = None,
        lookback_days: int = 30
    ) -> Dict[str, Any]:
        """
        Get sentiment timeline for charting

        Args:
            db: Database session
            symbol: Ticker symbol
            source: Filter by source
            lookback_days: Days to look back

        Returns:
            Timeline data with daily sentiment
        """
        try:
            cache_key = f"{self.cache_prefix}:timeline:{symbol}:{source or 'all'}:{lookback_days}"
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

            # Get ticker
            result = await db.execute(
                select(Ticker).where(Ticker.symbol == symbol.upper())
            )
            ticker = result.scalar_one_or_none()
            if not ticker:
                return {"error": "Ticker not found"}

            cutoff_date = datetime.utcnow() - timedelta(days=lookback_days)

            # Get daily aggregated sentiment
            query = (
                select(
                    func.date_trunc('day', SocialSentiment.sentiment_date).label('date'),
                    func.avg(SocialSentiment.sentiment_score).label('avg_sentiment'),
                    func.sum(SocialSentiment.mention_count).label('total_mentions'),
                    func.sum(SocialSentiment.total_engagement).label('total_engagement')
                )
                .where(
                    and_(
                        SocialSentiment.ticker_id == ticker.id,
                        SocialSentiment.sentiment_date >= cutoff_date
                    )
                )
            )

            if source:
                query = query.where(SocialSentiment.source == source)

            query = query.group_by('date').order_by('date')

            result = await db.execute(query)
            timeline = []

            for row in result:
                timeline.append({
                    "date": row.date.isoformat() if row.date else None,
                    "avg_sentiment": round(float(row.avg_sentiment), 3),
                    "sentiment_label": self._score_to_label(float(row.avg_sentiment)),
                    "total_mentions": int(row.total_mentions),
                    "total_engagement": int(row.total_engagement),
                })

            data = {
                "symbol": symbol.upper(),
                "source": source or "all",
                "lookback_days": lookback_days,
                "timeline": timeline,
                "data_points": len(timeline),
            }

            await self.cache.set(cache_key, data, ttl=1800)  # 30 minutes
            return data

        except Exception as e:
            logger.error(f"Error getting sentiment timeline for {symbol}: {e}")
            return {"error": str(e)}

    def _score_to_label(self, score: float) -> str:
        """Convert sentiment score to label"""
        if score >= 0.3:
            return "bullish"
        elif score <= -0.3:
            return "bearish"
        else:
            return "neutral"

    async def close(self):
        """Cleanup resources"""
        await self.client.aclose()


# Global instance
social_sentiment_service = SocialSentimentService()
