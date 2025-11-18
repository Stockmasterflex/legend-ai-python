"""
Analyst Coverage Service
Tracks analyst ratings, price targets, and consensus
"""
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy import select, and_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from app.config import get_settings
from app.services.cache import get_cache_service
from app.models import AnalystCoverage, AnalystConsensus, Ticker

logger = logging.getLogger(__name__)


class AnalystCoverageService:
    """
    Service for analyst coverage tracking

    Features:
    - Track analyst ratings and changes
    - Monitor price target updates
    - Calculate consensus ratings
    - Detect upgrades/downgrades
    """

    def __init__(self):
        self.settings = get_settings()
        self.cache = get_cache_service()
        self.cache_prefix = "analyst_coverage"
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get_analyst_ratings(
        self,
        db: AsyncSession,
        symbol: str,
        limit: int = 50,
        lookback_days: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get analyst ratings for a symbol

        Args:
            db: Database session
            symbol: Ticker symbol
            limit: Maximum number of ratings to return
            lookback_days: Optional days to look back

        Returns:
            List of analyst ratings
        """
        try:
            cache_key = f"{self.cache_prefix}:ratings:{symbol}:{limit}:{lookback_days or 'all'}"
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

            # Build query
            query = select(AnalystCoverage).where(AnalystCoverage.ticker_id == ticker.id)

            if lookback_days:
                cutoff_date = datetime.utcnow() - timedelta(days=lookback_days)
                query = query.where(AnalystCoverage.rating_date >= cutoff_date)

            query = query.order_by(desc(AnalystCoverage.rating_date)).limit(limit)

            result = await db.execute(query)
            ratings = result.scalars().all()

            ratings_data = []
            for rating in ratings:
                ratings_data.append({
                    "analyst_firm": rating.analyst_firm,
                    "analyst_name": rating.analyst_name,
                    "rating_date": rating.rating_date.isoformat() if rating.rating_date else None,
                    "rating": rating.rating,
                    "previous_rating": rating.previous_rating,
                    "rating_change": rating.rating_change,
                    "price_target": rating.price_target,
                    "previous_price_target": rating.previous_price_target,
                    "price_target_change_pct": rating.price_target_change_pct,
                    "sentiment": rating.sentiment,
                    "confidence": rating.confidence,
                    "report_title": rating.report_title,
                    "summary": rating.summary[:200] + "..." if rating.summary and len(rating.summary) > 200 else rating.summary,
                })

            await self.cache.set(cache_key, ratings_data, ttl=3600)  # 1 hour
            return ratings_data

        except Exception as e:
            logger.error(f"Error getting analyst ratings for {symbol}: {e}")
            return []

    async def get_consensus(
        self,
        db: AsyncSession,
        symbol: str
    ) -> Dict[str, Any]:
        """
        Get current analyst consensus for a symbol

        Args:
            db: Database session
            symbol: Ticker symbol

        Returns:
            Consensus data
        """
        try:
            cache_key = f"{self.cache_prefix}:consensus:{symbol}"
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

            # Get latest consensus
            query = (
                select(AnalystConsensus)
                .where(AnalystConsensus.ticker_id == ticker.id)
                .order_by(desc(AnalystConsensus.consensus_date))
                .limit(1)
            )

            result = await db.execute(query)
            consensus = result.scalar_one_or_none()

            if not consensus:
                # Calculate consensus from individual ratings
                consensus_data = await self._calculate_consensus(db, ticker.id)
                return {
                    "symbol": symbol.upper(),
                    "calculated": True,
                    **consensus_data
                }

            consensus_data = {
                "symbol": symbol.upper(),
                "consensus_date": consensus.consensus_date.isoformat() if consensus.consensus_date else None,
                "total_analysts": consensus.total_analysts,
                "buy_count": consensus.buy_count,
                "hold_count": consensus.hold_count,
                "sell_count": consensus.sell_count,
                "consensus_rating": consensus.consensus_rating,
                "consensus_score": consensus.consensus_score,
                "avg_price_target": consensus.avg_price_target,
                "high_price_target": consensus.high_price_target,
                "low_price_target": consensus.low_price_target,
                "median_price_target": consensus.median_price_target,
                "upgrades_last_30d": consensus.upgrades_last_30d,
                "downgrades_last_30d": consensus.downgrades_last_30d,
                "sentiment_trend": consensus.sentiment_trend,
                "calculated": False,
            }

            await self.cache.set(cache_key, consensus_data, ttl=3600)  # 1 hour
            return consensus_data

        except Exception as e:
            logger.error(f"Error getting consensus for {symbol}: {e}")
            return {"error": str(e)}

    async def _calculate_consensus(
        self,
        db: AsyncSession,
        ticker_id: int
    ) -> Dict[str, Any]:
        """Calculate consensus from individual ratings"""
        try:
            # Get ratings from last 90 days
            cutoff_date = datetime.utcnow() - timedelta(days=90)

            result = await db.execute(
                select(AnalystCoverage)
                .where(
                    and_(
                        AnalystCoverage.ticker_id == ticker_id,
                        AnalystCoverage.rating_date >= cutoff_date
                    )
                )
            )
            ratings = result.scalars().all()

            if not ratings:
                return {
                    "total_analysts": 0,
                    "consensus_rating": "N/A",
                }

            # Count ratings
            buy_count = sum(1 for r in ratings if r.rating and "buy" in r.rating.lower())
            hold_count = sum(1 for r in ratings if r.rating and "hold" in r.rating.lower())
            sell_count = sum(1 for r in ratings if r.rating and "sell" in r.rating.lower())

            # Calculate consensus score (1-5 scale)
            total = len(ratings)
            score = ((buy_count * 5) + (hold_count * 3) + (sell_count * 1)) / total if total > 0 else 3

            # Determine consensus rating
            if score >= 4.5:
                consensus_rating = "Strong Buy"
            elif score >= 3.5:
                consensus_rating = "Buy"
            elif score >= 2.5:
                consensus_rating = "Hold"
            elif score >= 1.5:
                consensus_rating = "Sell"
            else:
                consensus_rating = "Strong Sell"

            # Price targets
            price_targets = [r.price_target for r in ratings if r.price_target]
            avg_pt = sum(price_targets) / len(price_targets) if price_targets else None
            high_pt = max(price_targets) if price_targets else None
            low_pt = min(price_targets) if price_targets else None
            median_pt = sorted(price_targets)[len(price_targets) // 2] if price_targets else None

            # Recent changes
            cutoff_30d = datetime.utcnow() - timedelta(days=30)
            recent_ratings = [r for r in ratings if r.rating_date >= cutoff_30d]
            upgrades = sum(1 for r in recent_ratings if r.rating_change == "Upgrade")
            downgrades = sum(1 for r in recent_ratings if r.rating_change == "Downgrade")

            # Sentiment trend
            if upgrades > downgrades * 1.5:
                sentiment_trend = "improving"
            elif downgrades > upgrades * 1.5:
                sentiment_trend = "deteriorating"
            else:
                sentiment_trend = "stable"

            return {
                "total_analysts": total,
                "buy_count": buy_count,
                "hold_count": hold_count,
                "sell_count": sell_count,
                "consensus_rating": consensus_rating,
                "consensus_score": round(score, 2),
                "avg_price_target": round(avg_pt, 2) if avg_pt else None,
                "high_price_target": round(high_pt, 2) if high_pt else None,
                "low_price_target": round(low_pt, 2) if low_pt else None,
                "median_price_target": round(median_pt, 2) if median_pt else None,
                "upgrades_last_30d": upgrades,
                "downgrades_last_30d": downgrades,
                "sentiment_trend": sentiment_trend,
            }

        except Exception as e:
            logger.error(f"Error calculating consensus: {e}")
            return {}

    async def get_rating_changes(
        self,
        db: AsyncSession,
        symbol: Optional[str] = None,
        change_type: Optional[str] = None,
        lookback_days: int = 30,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get analyst rating changes

        Args:
            db: Database session
            symbol: Optional ticker symbol filter
            change_type: Filter by change type (Upgrade, Downgrade)
            lookback_days: Days to look back
            limit: Maximum number of changes

        Returns:
            List of rating changes
        """
        try:
            cache_key = f"{self.cache_prefix}:changes:{symbol or 'all'}:{change_type or 'all'}:{lookback_days}:{limit}"
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

            cutoff_date = datetime.utcnow() - timedelta(days=lookback_days)

            # Build query
            query = (
                select(AnalystCoverage, Ticker.symbol, Ticker.name)
                .join(Ticker, AnalystCoverage.ticker_id == Ticker.id)
                .where(
                    and_(
                        AnalystCoverage.rating_date >= cutoff_date,
                        AnalystCoverage.rating_change.in_(["Upgrade", "Downgrade"])
                    )
                )
            )

            if symbol:
                query = query.where(Ticker.symbol == symbol.upper())

            if change_type:
                query = query.where(AnalystCoverage.rating_change == change_type)

            query = query.order_by(desc(AnalystCoverage.rating_date)).limit(limit)

            result = await db.execute(query)
            changes = []

            for coverage, ticker_symbol, ticker_name in result:
                changes.append({
                    "symbol": ticker_symbol,
                    "company_name": ticker_name,
                    "analyst_firm": coverage.analyst_firm,
                    "rating_date": coverage.rating_date.isoformat() if coverage.rating_date else None,
                    "change_type": coverage.rating_change,
                    "old_rating": coverage.previous_rating,
                    "new_rating": coverage.rating,
                    "price_target": coverage.price_target,
                    "sentiment": coverage.sentiment,
                    "summary": coverage.summary[:150] + "..." if coverage.summary and len(coverage.summary) > 150 else coverage.summary,
                })

            await self.cache.set(cache_key, changes, ttl=1800)  # 30 minutes
            return changes

        except Exception as e:
            logger.error(f"Error getting rating changes: {e}")
            return []

    async def compare_analyst_coverage(
        self,
        db: AsyncSession,
        symbols: List[str]
    ) -> Dict[str, Any]:
        """
        Compare analyst coverage across multiple stocks

        Args:
            db: Database session
            symbols: List of ticker symbols

        Returns:
            Comparative analyst coverage
        """
        try:
            cache_key = f"{self.cache_prefix}:compare:{':'.join(sorted(symbols))}"
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

            comparisons = []
            for symbol in symbols:
                consensus = await self.get_consensus(db, symbol)
                if "error" not in consensus:
                    comparisons.append(consensus)

            # Rank by consensus score
            ranked = sorted(
                [c for c in comparisons if c.get("consensus_score")],
                key=lambda x: x["consensus_score"],
                reverse=True
            )

            # Add rankings
            for i, comp in enumerate(ranked):
                comp["rank"] = i + 1

            result = {
                "compared_at": datetime.utcnow().isoformat(),
                "stocks": ranked,
                "highest_rated": ranked[0] if ranked else None,
                "lowest_rated": ranked[-1] if ranked else None,
                "summary": {
                    "avg_consensus_score": round(sum(c["consensus_score"] for c in ranked) / len(ranked), 2) if ranked else 0,
                    "total_analysts_combined": sum(c.get("total_analysts", 0) for c in comparisons),
                    "most_upgrades": max(comparisons, key=lambda x: x.get("upgrades_last_30d", 0)) if comparisons else None,
                    "most_downgrades": max(comparisons, key=lambda x: x.get("downgrades_last_30d", 0)) if comparisons else None,
                }
            }

            await self.cache.set(cache_key, result, ttl=3600)  # 1 hour
            return result

        except Exception as e:
            logger.error(f"Error comparing analyst coverage: {e}")
            return {"error": str(e)}

    async def get_price_target_analysis(
        self,
        db: AsyncSession,
        symbol: str,
        current_price: float
    ) -> Dict[str, Any]:
        """
        Analyze price targets vs current price

        Args:
            db: Database session
            symbol: Ticker symbol
            current_price: Current stock price

        Returns:
            Price target analysis
        """
        try:
            cache_key = f"{self.cache_prefix}:price_target:{symbol}:{current_price}"
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

            consensus = await self.get_consensus(db, symbol)
            if "error" in consensus:
                return consensus

            avg_target = consensus.get("avg_price_target")
            high_target = consensus.get("high_price_target")
            low_target = consensus.get("low_price_target")

            if not avg_target:
                return {"error": "No price targets available"}

            # Calculate upside/downside
            avg_upside = ((avg_target - current_price) / current_price * 100)
            high_upside = ((high_target - current_price) / current_price * 100) if high_target else None
            low_upside = ((low_target - current_price) / current_price * 100) if low_target else None

            # Determine recommendation
            if avg_upside > 20:
                recommendation = "Strong upside potential"
            elif avg_upside > 10:
                recommendation = "Moderate upside potential"
            elif avg_upside > 0:
                recommendation = "Limited upside potential"
            elif avg_upside > -10:
                recommendation = "Limited downside risk"
            else:
                recommendation = "Significant downside risk"

            analysis = {
                "symbol": symbol.upper(),
                "current_price": current_price,
                "avg_price_target": avg_target,
                "high_price_target": high_target,
                "low_price_target": low_target,
                "avg_upside_pct": round(avg_upside, 2),
                "high_upside_pct": round(high_upside, 2) if high_upside else None,
                "low_upside_pct": round(low_upside, 2) if low_upside else None,
                "target_range_pct": round(high_upside - low_upside, 2) if high_upside and low_upside else None,
                "recommendation": recommendation,
                "consensus_rating": consensus.get("consensus_rating"),
                "total_analysts": consensus.get("total_analysts"),
            }

            await self.cache.set(cache_key, analysis, ttl=1800)  # 30 minutes
            return analysis

        except Exception as e:
            logger.error(f"Error analyzing price targets for {symbol}: {e}")
            return {"error": str(e)}

    async def close(self):
        """Cleanup resources"""
        await self.client.aclose()


# Global instance
analyst_coverage_service = AnalystCoverageService()
