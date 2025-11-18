"""
Competitor Analysis Service
Tracks competitors, peer comparison, and relative performance
"""
import asyncio
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy import select, and_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
import numpy as np

from app.config import get_settings
from app.services.cache import get_cache_service
from app.services.market_data import market_data_service
from app.services.pattern_scanner import pattern_scanner_service
from app.core.metrics import relative_strength_metrics
from app.models import (
    CompetitorGroup, CompetitorGroupMember, CompetitorTracking,
    Ticker, PatternScan
)

logger = logging.getLogger(__name__)


class CompetitorAnalysisService:
    """
    Service for competitor tracking and analysis

    Features:
    - Create and manage competitor groups
    - Track relative performance
    - Identify market leaders and laggards
    - Peer comparison metrics
    """

    def __init__(self):
        self.settings = get_settings()
        self.cache = get_cache_service()
        self.cache_prefix = "competitor_analysis"

    async def create_competitor_group(
        self,
        db: AsyncSession,
        name: str,
        symbols: List[str],
        industry: str,
        sector: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new competitor group

        Args:
            db: Database session
            name: Group name (e.g., "EV Manufacturers")
            symbols: List of ticker symbols
            industry: Industry classification
            sector: Sector classification
            description: Optional description

        Returns:
            Created group info
        """
        try:
            # Create the group
            group = CompetitorGroup(
                name=name,
                description=description,
                industry=industry,
                sector=sector
            )
            db.add(group)
            await db.flush()

            # Add members
            added_members = []
            for symbol in symbols:
                # Get or create ticker
                result = await db.execute(
                    select(Ticker).where(Ticker.symbol == symbol.upper())
                )
                ticker = result.scalar_one_or_none()

                if not ticker:
                    ticker = Ticker(
                        symbol=symbol.upper(),
                        industry=industry,
                        sector=sector
                    )
                    db.add(ticker)
                    await db.flush()

                # Add to group
                member = CompetitorGroupMember(
                    group_id=group.id,
                    ticker_id=ticker.id,
                    is_primary=(symbol == symbols[0])  # First is primary
                )
                db.add(member)
                added_members.append(symbol.upper())

            await db.commit()

            # Invalidate cache
            await self.cache.delete(f"{self.cache_prefix}:groups")

            logger.info(f"Created competitor group '{name}' with {len(added_members)} members")

            return {
                "group_id": group.id,
                "name": name,
                "industry": industry,
                "sector": sector,
                "members": added_members,
                "created_at": group.created_at.isoformat() if group.created_at else None
            }

        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating competitor group: {e}")
            raise

    async def get_competitor_groups(
        self,
        db: AsyncSession,
        industry: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all competitor groups, optionally filtered by industry"""
        try:
            cache_key = f"{self.cache_prefix}:groups:{industry or 'all'}"
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

            query = select(CompetitorGroup)
            if industry:
                query = query.where(CompetitorGroup.industry == industry)

            result = await db.execute(query.order_by(desc(CompetitorGroup.created_at)))
            groups = result.scalars().all()

            groups_data = []
            for group in groups:
                # Get member count
                member_result = await db.execute(
                    select(func.count(CompetitorGroupMember.id))
                    .where(CompetitorGroupMember.group_id == group.id)
                )
                member_count = member_result.scalar()

                groups_data.append({
                    "id": group.id,
                    "name": group.name,
                    "industry": group.industry,
                    "sector": group.sector,
                    "description": group.description,
                    "member_count": member_count,
                    "created_at": group.created_at.isoformat() if group.created_at else None
                })

            await self.cache.set(cache_key, groups_data, ttl=3600)
            return groups_data

        except Exception as e:
            logger.error(f"Error getting competitor groups: {e}")
            return []

    async def analyze_competitor_group(
        self,
        db: AsyncSession,
        group_id: int,
        timeframe: str = "1day",
        lookback_days: int = 90
    ) -> Dict[str, Any]:
        """
        Perform comprehensive analysis on a competitor group

        Args:
            db: Database session
            group_id: Competitor group ID
            timeframe: Data timeframe (1day, 1week, etc.)
            lookback_days: Days of historical data

        Returns:
            Comprehensive analysis with rankings, trends, and metrics
        """
        try:
            # Check cache
            cache_key = f"{self.cache_prefix}:analysis:{group_id}:{timeframe}:{lookback_days}"
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

            # Get group info
            group_result = await db.execute(
                select(CompetitorGroup).where(CompetitorGroup.id == group_id)
            )
            group = group_result.scalar_one_or_none()
            if not group:
                raise ValueError(f"Group {group_id} not found")

            # Get members
            members_result = await db.execute(
                select(CompetitorGroupMember, Ticker)
                .join(Ticker, CompetitorGroupMember.ticker_id == Ticker.id)
                .where(CompetitorGroupMember.group_id == group_id)
            )
            members = members_result.all()

            if not members:
                return {
                    "error": "No members in group",
                    "group_id": group_id,
                    "group_name": group.name
                }

            # Fetch market data for all symbols in parallel
            symbols = [ticker.symbol for _, ticker in members]
            logger.info(f"Analyzing {len(symbols)} competitors in group '{group.name}'")

            # Get SPY data for RS calculation
            spy_data = await market_data_service.get_time_series(
                "SPY", timeframe, lookback_days
            )
            spy_closes = [bar["close"] for bar in spy_data.get("bars", [])] if spy_data else []

            # Analyze each competitor
            competitor_analyses = []
            tasks = []
            for member, ticker in members:
                tasks.append(self._analyze_competitor(
                    ticker, timeframe, lookback_days, spy_closes, member.is_primary
                ))

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Error analyzing {symbols[i]}: {result}")
                    continue
                if result:
                    competitor_analyses.append(result)

            if not competitor_analyses:
                return {
                    "error": "Failed to analyze competitors",
                    "group_id": group_id,
                    "group_name": group.name
                }

            # Calculate group statistics
            group_stats = self._calculate_group_stats(competitor_analyses)

            # Rank competitors
            ranked_competitors = self._rank_competitors(competitor_analyses)

            # Identify trends
            trends = self._identify_trends(ranked_competitors)

            analysis = {
                "group_id": group_id,
                "group_name": group.name,
                "industry": group.industry,
                "sector": group.sector,
                "analyzed_at": datetime.utcnow().isoformat(),
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "competitor_count": len(competitor_analyses),
                "group_statistics": group_stats,
                "competitors": ranked_competitors,
                "trends": trends,
                "leaders": ranked_competitors[:3],  # Top 3
                "laggards": ranked_competitors[-3:],  # Bottom 3
            }

            # Cache for 1 hour
            await self.cache.set(cache_key, analysis, ttl=3600)

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing competitor group {group_id}: {e}")
            raise

    async def _analyze_competitor(
        self,
        ticker: Ticker,
        timeframe: str,
        lookback_days: int,
        spy_closes: List[float],
        is_primary: bool
    ) -> Optional[Dict[str, Any]]:
        """Analyze a single competitor"""
        try:
            symbol = ticker.symbol

            # Get market data
            data = await market_data_service.get_time_series(
                symbol, timeframe, lookback_days
            )

            if not data or "bars" not in data or not data["bars"]:
                logger.warning(f"No data for {symbol}")
                return None

            bars = data["bars"]
            closes = [bar["close"] for bar in bars]
            volumes = [bar["volume"] for bar in bars]

            # Current metrics
            current_price = closes[-1] if closes else 0
            current_volume = volumes[-1] if volumes else 0

            # Price changes
            price_change_1d = ((closes[-1] - closes[-2]) / closes[-2] * 100) if len(closes) > 1 else 0
            price_change_1w = ((closes[-1] - closes[-5]) / closes[-5] * 100) if len(closes) > 5 else 0
            price_change_1m = ((closes[-1] - closes[-20]) / closes[-20] * 100) if len(closes) > 20 else 0
            price_change_3m = ((closes[-1] - closes[-60]) / closes[-60] * 100) if len(closes) > 60 else 0

            # Relative strength vs SPY
            rs_rating = 50.0
            if spy_closes and len(closes) == len(spy_closes):
                rs_metrics = relative_strength_metrics(closes, spy_closes)
                rs_rating = rs_metrics.get("rs_rank", 50.0)

            # Pattern analysis
            pattern_score = 0.0
            best_pattern = None
            try:
                # Create DataFrame for pattern detection
                df = pd.DataFrame(bars)
                if "timestamp" in df.columns:
                    df["timestamp"] = pd.to_datetime(df["timestamp"])

                # Scan for patterns (just get the best one for performance)
                scan_results = await pattern_scanner_service.scan_symbol(
                    symbol, timeframe, limit_patterns=1
                )

                if scan_results and "patterns" in scan_results:
                    patterns = scan_results["patterns"]
                    if patterns:
                        best = max(patterns, key=lambda p: p.get("confidence", 0))
                        pattern_score = best.get("confidence", 0) * 100
                        best_pattern = best.get("pattern", "None")
            except Exception as e:
                logger.debug(f"Pattern analysis failed for {symbol}: {e}")

            # Volume trend
            avg_volume_10d = sum(volumes[-10:]) / min(10, len(volumes)) if volumes else 0
            volume_trend = ((current_volume - avg_volume_10d) / avg_volume_10d * 100) if avg_volume_10d > 0 else 0

            return {
                "symbol": symbol,
                "name": ticker.name or symbol,
                "is_primary": is_primary,
                "price": round(current_price, 2),
                "volume": int(current_volume),
                "price_change_1d": round(price_change_1d, 2),
                "price_change_1w": round(price_change_1w, 2),
                "price_change_1m": round(price_change_1m, 2),
                "price_change_3m": round(price_change_3m, 2),
                "rs_rating": round(rs_rating, 2),
                "pattern_score": round(pattern_score, 2),
                "best_pattern": best_pattern,
                "volume_trend": round(volume_trend, 2),
                "avg_volume_10d": int(avg_volume_10d),
            }

        except Exception as e:
            logger.error(f"Error analyzing competitor {ticker.symbol}: {e}")
            return None

    def _calculate_group_stats(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate group-level statistics"""
        if not analyses:
            return {}

        prices = [a["price"] for a in analyses]
        price_changes_1d = [a["price_change_1d"] for a in analyses]
        price_changes_1m = [a["price_change_1m"] for a in analyses]
        rs_ratings = [a["rs_rating"] for a in analyses]
        pattern_scores = [a["pattern_score"] for a in analyses]

        return {
            "avg_price": round(np.mean(prices), 2),
            "median_price": round(np.median(prices), 2),
            "avg_price_change_1d": round(np.mean(price_changes_1d), 2),
            "avg_price_change_1m": round(np.mean(price_changes_1m), 2),
            "avg_rs_rating": round(np.mean(rs_ratings), 2),
            "avg_pattern_score": round(np.mean(pattern_scores), 2),
            "price_dispersion": round(np.std(prices), 2),
            "performance_dispersion": round(np.std(price_changes_1m), 2),
        }

    def _rank_competitors(self, analyses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank competitors by composite score"""
        if not analyses:
            return []

        # Calculate composite scores
        for analysis in analyses:
            # Weighted score: RS (40%) + Pattern (30%) + 1M Performance (30%)
            composite = (
                analysis["rs_rating"] * 0.4 +
                analysis["pattern_score"] * 0.3 +
                (analysis["price_change_1m"] + 100) * 0.3  # Normalize to 0-200 range
            )
            analysis["composite_score"] = round(composite, 2)

        # Sort by composite score
        ranked = sorted(analyses, key=lambda x: x["composite_score"], reverse=True)

        # Add rankings and percentiles
        for i, analysis in enumerate(ranked):
            analysis["rank"] = i + 1
            analysis["percentile"] = round((len(ranked) - i) / len(ranked) * 100, 1)

            # Add relative performance vs group average
            avg_1m = np.mean([a["price_change_1m"] for a in analyses])
            analysis["vs_group_avg_1m"] = round(analysis["price_change_1m"] - avg_1m, 2)

        return ranked

    def _identify_trends(self, ranked: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identify trends in the competitor group"""
        if not ranked:
            return {}

        # Performance trends
        positive_1m = sum(1 for a in ranked if a["price_change_1m"] > 0)
        strong_performers = sum(1 for a in ranked if a["price_change_1m"] > 10)

        # Pattern trends
        patterns_detected = sum(1 for a in ranked if a["best_pattern"])

        # Momentum trends
        positive_momentum = sum(1 for a in ranked if a["price_change_1w"] > a["price_change_1m"] / 4)

        return {
            "group_momentum": "bullish" if positive_1m > len(ranked) / 2 else "bearish",
            "positive_performers_pct": round(positive_1m / len(ranked) * 100, 1),
            "strong_performers_pct": round(strong_performers / len(ranked) * 100, 1),
            "patterns_detected_pct": round(patterns_detected / len(ranked) * 100, 1),
            "positive_momentum_pct": round(positive_momentum / len(ranked) * 100, 1),
            "trend_strength": "strong" if strong_performers > len(ranked) / 3 else "moderate" if positive_1m > len(ranked) / 2 else "weak"
        }

    async def compare_stocks(
        self,
        symbols: List[str],
        timeframe: str = "1day",
        lookback_days: int = 90
    ) -> Dict[str, Any]:
        """
        Compare multiple stocks side-by-side

        Args:
            symbols: List of ticker symbols (2-10)
            timeframe: Data timeframe
            lookback_days: Days of historical data

        Returns:
            Comparison metrics and rankings
        """
        try:
            if len(symbols) < 2 or len(symbols) > 10:
                raise ValueError("Must compare between 2 and 10 stocks")

            # Get SPY data
            spy_data = await market_data_service.get_time_series(
                "SPY", timeframe, lookback_days
            )
            spy_closes = [bar["close"] for bar in spy_data.get("bars", [])] if spy_data else []

            # Analyze each stock
            analyses = []
            for symbol in symbols:
                ticker = Ticker(symbol=symbol.upper())  # Mock ticker for analysis
                analysis = await self._analyze_competitor(
                    ticker, timeframe, lookback_days, spy_closes, False
                )
                if analysis:
                    analyses.append(analysis)

            if not analyses:
                return {"error": "Failed to analyze stocks"}

            # Rank and compare
            ranked = self._rank_competitors(analyses)
            stats = self._calculate_group_stats(analyses)

            return {
                "compared_at": datetime.utcnow().isoformat(),
                "timeframe": timeframe,
                "lookback_days": lookback_days,
                "stock_count": len(analyses),
                "statistics": stats,
                "stocks": ranked,
                "best_performer": ranked[0] if ranked else None,
                "worst_performer": ranked[-1] if ranked else None,
            }

        except Exception as e:
            logger.error(f"Error comparing stocks: {e}")
            raise

    async def close(self):
        """Cleanup resources"""
        pass


# Global instance
competitor_analysis_service = CompetitorAnalysisService()
