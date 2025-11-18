"""
Patent Analysis Service
Tracks patent filings, R&D spending, and innovation metrics
"""
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy import select, and_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from app.config import get_settings
from app.services.cache import get_cache_service
from app.models import PatentFiling, RDSpending, Ticker

logger = logging.getLogger(__name__)


class PatentAnalysisService:
    """
    Service for patent and R&D analysis

    Features:
    - Track patent filings
    - Monitor R&D spending
    - Calculate innovation metrics
    - Compare innovation across competitors
    """

    def __init__(self):
        self.settings = get_settings()
        self.cache = get_cache_service()
        self.cache_prefix = "patent_analysis"
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get_patent_filings(
        self,
        db: AsyncSession,
        symbol: str,
        limit: int = 50,
        technology_category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get patent filings for a company

        Args:
            db: Database session
            symbol: Ticker symbol
            limit: Maximum number of patents to return
            technology_category: Filter by technology category

        Returns:
            List of patent filings
        """
        try:
            cache_key = f"{self.cache_prefix}:filings:{symbol}:{technology_category or 'all'}:{limit}"
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
            query = select(PatentFiling).where(PatentFiling.ticker_id == ticker.id)

            if technology_category:
                query = query.where(PatentFiling.technology_category == technology_category)

            query = query.order_by(desc(PatentFiling.filing_date)).limit(limit)

            result = await db.execute(query)
            patents = result.scalars().all()

            patents_data = []
            for patent in patents:
                patents_data.append({
                    "patent_number": patent.patent_number,
                    "title": patent.title,
                    "filing_date": patent.filing_date.isoformat() if patent.filing_date else None,
                    "publication_date": patent.publication_date.isoformat() if patent.publication_date else None,
                    "grant_date": patent.grant_date.isoformat() if patent.grant_date else None,
                    "status": patent.status,
                    "technology_category": patent.technology_category,
                    "patent_class": patent.patent_class,
                    "innovation_score": patent.innovation_score,
                    "citation_count": patent.citation_count,
                    "family_size": patent.family_size,
                    "abstract": patent.abstract[:200] + "..." if patent.abstract and len(patent.abstract) > 200 else patent.abstract,
                })

            await self.cache.set(cache_key, patents_data, ttl=86400)  # 24 hours
            return patents_data

        except Exception as e:
            logger.error(f"Error getting patent filings for {symbol}: {e}")
            return []

    async def get_patent_statistics(
        self,
        db: AsyncSession,
        symbol: str,
        lookback_months: int = 12
    ) -> Dict[str, Any]:
        """
        Get patent statistics for a company

        Args:
            db: Database session
            symbol: Ticker symbol
            lookback_months: Months to look back

        Returns:
            Patent statistics
        """
        try:
            cache_key = f"{self.cache_prefix}:stats:{symbol}:{lookback_months}"
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

            cutoff_date = datetime.utcnow() - timedelta(days=lookback_months * 30)

            # Total patents
            total_result = await db.execute(
                select(func.count(PatentFiling.id))
                .where(
                    and_(
                        PatentFiling.ticker_id == ticker.id,
                        PatentFiling.filing_date >= cutoff_date
                    )
                )
            )
            total_patents = total_result.scalar() or 0

            # Patents by status
            status_result = await db.execute(
                select(PatentFiling.status, func.count(PatentFiling.id))
                .where(
                    and_(
                        PatentFiling.ticker_id == ticker.id,
                        PatentFiling.filing_date >= cutoff_date
                    )
                )
                .group_by(PatentFiling.status)
            )
            patents_by_status = {status: count for status, count in status_result}

            # Patents by technology category
            tech_result = await db.execute(
                select(PatentFiling.technology_category, func.count(PatentFiling.id))
                .where(
                    and_(
                        PatentFiling.ticker_id == ticker.id,
                        PatentFiling.filing_date >= cutoff_date
                    )
                )
                .group_by(PatentFiling.technology_category)
                .order_by(desc(func.count(PatentFiling.id)))
                .limit(10)
            )
            top_technologies = [
                {"category": cat, "count": count}
                for cat, count in tech_result
            ]

            # Average citation count
            citation_result = await db.execute(
                select(func.avg(PatentFiling.citation_count))
                .where(
                    and_(
                        PatentFiling.ticker_id == ticker.id,
                        PatentFiling.filing_date >= cutoff_date
                    )
                )
            )
            avg_citations = citation_result.scalar() or 0

            # Patent filing trend (monthly)
            monthly_result = await db.execute(
                select(
                    func.date_trunc('month', PatentFiling.filing_date).label('month'),
                    func.count(PatentFiling.id).label('count')
                )
                .where(
                    and_(
                        PatentFiling.ticker_id == ticker.id,
                        PatentFiling.filing_date >= cutoff_date
                    )
                )
                .group_by('month')
                .order_by('month')
            )
            monthly_trend = [
                {
                    "month": month.isoformat() if month else None,
                    "count": count
                }
                for month, count in monthly_result
            ]

            stats = {
                "symbol": symbol.upper(),
                "lookback_months": lookback_months,
                "total_patents": total_patents,
                "patents_by_status": patents_by_status,
                "top_technologies": top_technologies,
                "avg_citations_per_patent": round(float(avg_citations), 2),
                "monthly_trend": monthly_trend,
                "filing_rate_per_month": round(total_patents / lookback_months, 2) if lookback_months > 0 else 0,
            }

            await self.cache.set(cache_key, stats, ttl=86400)  # 24 hours
            return stats

        except Exception as e:
            logger.error(f"Error getting patent statistics for {symbol}: {e}")
            return {"error": str(e)}

    async def get_rd_spending(
        self,
        db: AsyncSession,
        symbol: str,
        limit: int = 8
    ) -> List[Dict[str, Any]]:
        """
        Get R&D spending data for a company

        Args:
            db: Database session
            symbol: Ticker symbol
            limit: Number of periods to return

        Returns:
            R&D spending data
        """
        try:
            cache_key = f"{self.cache_prefix}:rd_spending:{symbol}:{limit}"
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

            # Get R&D data
            query = (
                select(RDSpending)
                .where(RDSpending.ticker_id == ticker.id)
                .order_by(desc(RDSpending.period_start))
                .limit(limit)
            )

            result = await db.execute(query)
            rd_data = result.scalars().all()

            spending_data = []
            for rd in rd_data:
                spending_data.append({
                    "period": rd.period,
                    "period_start": rd.period_start.isoformat() if rd.period_start else None,
                    "period_end": rd.period_end.isoformat() if rd.period_end else None,
                    "rd_spending": rd.rd_spending,
                    "rd_as_pct_revenue": rd.rd_as_pct_revenue,
                    "patent_filings_count": rd.patent_filings_count,
                    "patent_grants_count": rd.patent_grants_count,
                    "innovation_efficiency": rd.innovation_efficiency,
                    "rd_growth_yoy": rd.rd_growth_yoy,
                })

            await self.cache.set(cache_key, spending_data, ttl=86400)  # 24 hours
            return spending_data

        except Exception as e:
            logger.error(f"Error getting R&D spending for {symbol}: {e}")
            return []

    async def compare_innovation_metrics(
        self,
        db: AsyncSession,
        symbols: List[str],
        lookback_months: int = 12
    ) -> Dict[str, Any]:
        """
        Compare innovation metrics across multiple companies

        Args:
            db: Database session
            symbols: List of ticker symbols
            lookback_months: Months to look back

        Returns:
            Comparative innovation analysis
        """
        try:
            cache_key = f"{self.cache_prefix}:compare:{':'.join(sorted(symbols))}:{lookback_months}"
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

            comparisons = []
            for symbol in symbols:
                # Get patent stats
                patent_stats = await self.get_patent_statistics(
                    db, symbol, lookback_months
                )

                # Get latest R&D spending
                rd_data = await self.get_rd_spending(db, symbol, limit=1)
                latest_rd = rd_data[0] if rd_data else None

                comparison = {
                    "symbol": symbol.upper(),
                    "total_patents": patent_stats.get("total_patents", 0),
                    "filing_rate_per_month": patent_stats.get("filing_rate_per_month", 0),
                    "avg_citations_per_patent": patent_stats.get("avg_citations_per_patent", 0),
                    "rd_spending": latest_rd.get("rd_spending") if latest_rd else None,
                    "rd_as_pct_revenue": latest_rd.get("rd_as_pct_revenue") if latest_rd else None,
                    "innovation_efficiency": latest_rd.get("innovation_efficiency") if latest_rd else None,
                    "rd_growth_yoy": latest_rd.get("rd_growth_yoy") if latest_rd else None,
                    "top_technologies": patent_stats.get("top_technologies", [])[:3],  # Top 3
                }

                # Calculate innovation score (0-100)
                score = 0
                if comparison["total_patents"] > 0:
                    score += min(comparison["total_patents"] * 2, 30)  # Up to 30 points for volume
                if comparison["avg_citations_per_patent"] > 0:
                    score += min(comparison["avg_citations_per_patent"] * 5, 30)  # Up to 30 points for quality
                if comparison["rd_as_pct_revenue"]:
                    score += min(comparison["rd_as_pct_revenue"] * 2, 20)  # Up to 20 points for R&D intensity
                if comparison["innovation_efficiency"]:
                    score += min(comparison["innovation_efficiency"] * 10, 20)  # Up to 20 points for efficiency

                comparison["innovation_score"] = min(round(score, 2), 100)

                comparisons.append(comparison)

            # Rank by innovation score
            ranked = sorted(comparisons, key=lambda x: x["innovation_score"], reverse=True)

            # Add rankings
            for i, comp in enumerate(ranked):
                comp["rank"] = i + 1

            result = {
                "compared_at": datetime.utcnow().isoformat(),
                "lookback_months": lookback_months,
                "companies": ranked,
                "leader": ranked[0] if ranked else None,
                "summary": {
                    "total_patents_combined": sum(c["total_patents"] for c in comparisons),
                    "avg_innovation_score": round(sum(c["innovation_score"] for c in comparisons) / len(comparisons), 2) if comparisons else 0,
                }
            }

            await self.cache.set(cache_key, result, ttl=86400)  # 24 hours
            return result

        except Exception as e:
            logger.error(f"Error comparing innovation metrics: {e}")
            return {"error": str(e)}

    async def get_technology_trends(
        self,
        db: AsyncSession,
        industry: Optional[str] = None,
        lookback_months: int = 12,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Identify technology trends across industry

        Args:
            db: Database session
            industry: Filter by industry
            lookback_months: Months to look back
            limit: Number of top technologies

        Returns:
            Technology trend analysis
        """
        try:
            cache_key = f"{self.cache_prefix}:tech_trends:{industry or 'all'}:{lookback_months}"
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

            cutoff_date = datetime.utcnow() - timedelta(days=lookback_months * 30)

            # Build query
            query = (
                select(PatentFiling.technology_category, func.count(PatentFiling.id))
                .where(PatentFiling.filing_date >= cutoff_date)
            )

            # Add industry filter if specified
            if industry:
                query = query.join(Ticker, PatentFiling.ticker_id == Ticker.id)
                query = query.where(Ticker.industry == industry)

            query = query.group_by(PatentFiling.technology_category)
            query = query.order_by(desc(func.count(PatentFiling.id)))
            query = query.limit(limit)

            result = await db.execute(query)
            tech_trends = [
                {
                    "technology": tech,
                    "patent_count": count,
                    "trend": "emerging" if count > 10 else "growing" if count > 5 else "nascent"
                }
                for tech, count in result
            ]

            trends = {
                "industry": industry,
                "lookback_months": lookback_months,
                "top_technologies": tech_trends,
                "total_categories": len(tech_trends),
                "analyzed_at": datetime.utcnow().isoformat(),
            }

            await self.cache.set(cache_key, trends, ttl=86400)  # 24 hours
            return trends

        except Exception as e:
            logger.error(f"Error getting technology trends: {e}")
            return {"error": str(e)}

    async def close(self):
        """Cleanup resources"""
        await self.client.aclose()


# Global instance
patent_analysis_service = PatentAnalysisService()
