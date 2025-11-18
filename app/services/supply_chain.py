"""
Supply Chain Service
Tracks supplier relationships, customer dependencies, and supply chain risks
"""
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy import select, and_, or_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from app.config import get_settings
from app.services.cache import get_cache_service
from app.models import SupplyChainRelationship, SupplyChainRisk, Ticker

logger = logging.getLogger(__name__)


class SupplyChainService:
    """
    Service for supply chain analysis

    Features:
    - Track supplier and customer relationships
    - Monitor dependency levels
    - Assess geographic exposure
    - Identify supply chain risks
    """

    def __init__(self):
        self.settings = get_settings()
        self.cache = get_cache_service()
        self.cache_prefix = "supply_chain"
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get_relationships(
        self,
        db: AsyncSession,
        symbol: str,
        relationship_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get supply chain relationships for a company

        Args:
            db: Database session
            symbol: Ticker symbol
            relationship_type: Filter by type (supplier, customer, partner)

        Returns:
            List of relationships
        """
        try:
            cache_key = f"{self.cache_prefix}:relationships:{symbol}:{relationship_type or 'all'}"
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
            query = select(SupplyChainRelationship).where(
                SupplyChainRelationship.ticker_id == ticker.id
            )

            if relationship_type:
                query = query.where(SupplyChainRelationship.relationship_type == relationship_type)

            query = query.order_by(desc(SupplyChainRelationship.revenue_contribution_pct))

            result = await db.execute(query)
            relationships = result.scalars().all()

            relationships_data = []
            for rel in relationships:
                # Get related company info if available
                related_company_name = rel.related_company_name
                related_company_symbol = None

                if rel.related_company_id:
                    company_result = await db.execute(
                        select(Ticker).where(Ticker.id == rel.related_company_id)
                    )
                    related_company = company_result.scalar_one_or_none()
                    if related_company:
                        related_company_name = related_company.name or related_company.symbol
                        related_company_symbol = related_company.symbol

                relationships_data.append({
                    "relationship_type": rel.relationship_type,
                    "related_company": related_company_name,
                    "related_symbol": related_company_symbol,
                    "revenue_contribution_pct": rel.revenue_contribution_pct,
                    "dependency_level": rel.dependency_level,
                    "relationship_status": rel.relationship_status,
                    "primary_geography": rel.primary_geography,
                    "geographic_risk_score": rel.geographic_risk_score,
                    "relationship_start_date": rel.relationship_start_date.isoformat() if rel.relationship_start_date else None,
                    "last_verified": rel.last_verified.isoformat() if rel.last_verified else None,
                    "source": rel.source,
                    "notes": rel.notes,
                })

            await self.cache.set(cache_key, relationships_data, ttl=86400)  # 24 hours
            return relationships_data

        except Exception as e:
            logger.error(f"Error getting relationships for {symbol}: {e}")
            return []

    async def get_dependency_analysis(
        self,
        db: AsyncSession,
        symbol: str
    ) -> Dict[str, Any]:
        """
        Analyze supplier and customer dependencies

        Args:
            db: Database session
            symbol: Ticker symbol

        Returns:
            Dependency analysis
        """
        try:
            cache_key = f"{self.cache_prefix}:dependency:{symbol}"
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

            # Get all relationships
            suppliers = await self.get_relationships(db, symbol, "supplier")
            customers = await self.get_relationships(db, symbol, "customer")
            partners = await self.get_relationships(db, symbol, "partner")

            # Calculate dependencies
            supplier_concentration = sum(
                s.get("revenue_contribution_pct", 0) or 0
                for s in suppliers
                if s.get("revenue_contribution_pct")
            )

            customer_concentration = sum(
                c.get("revenue_contribution_pct", 0) or 0
                for c in customers
                if c.get("revenue_contribution_pct")
            )

            # Count critical relationships
            critical_suppliers = sum(
                1 for s in suppliers
                if s.get("dependency_level") == "critical"
            )

            critical_customers = sum(
                1 for c in customers
                if c.get("dependency_level") == "critical"
            )

            # Geographic exposure
            geographies = {}
            for rel in suppliers + customers + partners:
                geo = rel.get("primary_geography")
                if geo:
                    geographies[geo] = geographies.get(geo, 0) + 1

            # Risk assessment
            risk_level = "low"
            risk_factors = []

            if supplier_concentration > 50:
                risk_level = "high"
                risk_factors.append("High supplier concentration")
            elif supplier_concentration > 30:
                risk_level = "medium"
                risk_factors.append("Moderate supplier concentration")

            if customer_concentration > 50:
                risk_level = "high"
                risk_factors.append("High customer concentration")
            elif customer_concentration > 30:
                if risk_level == "low":
                    risk_level = "medium"
                risk_factors.append("Moderate customer concentration")

            if critical_suppliers > 5:
                risk_factors.append("Multiple critical suppliers")
            if critical_customers > 5:
                risk_factors.append("Multiple critical customers")

            # Diversification score (0-100)
            diversification = 100
            if supplier_concentration > 0:
                diversification -= min(supplier_concentration * 0.5, 30)
            if customer_concentration > 0:
                diversification -= min(customer_concentration * 0.5, 30)
            if len(geographies) < 3:
                diversification -= 20

            analysis = {
                "symbol": symbol.upper(),
                "supplier_count": len(suppliers),
                "customer_count": len(customers),
                "partner_count": len(partners),
                "supplier_concentration_pct": round(supplier_concentration, 2),
                "customer_concentration_pct": round(customer_concentration, 2),
                "critical_suppliers": critical_suppliers,
                "critical_customers": critical_customers,
                "geographic_exposure": geographies,
                "diversification_score": max(round(diversification, 2), 0),
                "risk_level": risk_level,
                "risk_factors": risk_factors,
                "top_suppliers": suppliers[:5],  # Top 5
                "top_customers": customers[:5],  # Top 5
                "analyzed_at": datetime.utcnow().isoformat(),
            }

            await self.cache.set(cache_key, analysis, ttl=86400)  # 24 hours
            return analysis

        except Exception as e:
            logger.error(f"Error analyzing dependencies for {symbol}: {e}")
            return {"error": str(e)}

    async def get_supply_chain_risks(
        self,
        db: AsyncSession,
        symbol: str,
        active_only: bool = True,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get supply chain risks for a company

        Args:
            db: Database session
            symbol: Ticker symbol
            active_only: Only return unresolved risks
            limit: Maximum number of risks to return

        Returns:
            List of supply chain risks
        """
        try:
            cache_key = f"{self.cache_prefix}:risks:{symbol}:{active_only}:{limit}"
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
            query = select(SupplyChainRisk).where(SupplyChainRisk.ticker_id == ticker.id)

            if active_only:
                query = query.where(
                    or_(
                        SupplyChainRisk.mitigation_status == "unmitigated",
                        SupplyChainRisk.mitigation_status == "in_progress"
                    )
                )

            query = query.order_by(desc(SupplyChainRisk.risk_date)).limit(limit)

            result = await db.execute(query)
            risks = result.scalars().all()

            risks_data = []
            for risk in risks:
                risks_data.append({
                    "risk_date": risk.risk_date.isoformat() if risk.risk_date else None,
                    "risk_type": risk.risk_type,
                    "risk_level": risk.risk_level,
                    "description": risk.description,
                    "estimated_impact": risk.estimated_impact,
                    "revenue_at_risk_pct": risk.revenue_at_risk_pct,
                    "mitigation_status": risk.mitigation_status,
                    "source": risk.source,
                    "resolution_date": risk.resolution_date.isoformat() if risk.resolution_date else None,
                })

            await self.cache.set(cache_key, risks_data, ttl=3600)  # 1 hour
            return risks_data

        except Exception as e:
            logger.error(f"Error getting supply chain risks for {symbol}: {e}")
            return []

    async def get_risk_summary(
        self,
        db: AsyncSession,
        symbol: str
    ) -> Dict[str, Any]:
        """
        Get risk summary for a company

        Args:
            db: Database session
            symbol: Ticker symbol

        Returns:
            Risk summary
        """
        try:
            cache_key = f"{self.cache_prefix}:risk_summary:{symbol}"
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

            # Count risks by level
            level_result = await db.execute(
                select(SupplyChainRisk.risk_level, func.count(SupplyChainRisk.id))
                .where(
                    and_(
                        SupplyChainRisk.ticker_id == ticker.id,
                        SupplyChainRisk.mitigation_status.in_(["unmitigated", "in_progress"])
                    )
                )
                .group_by(SupplyChainRisk.risk_level)
            )
            risks_by_level = {level: count for level, count in level_result}

            # Count risks by type
            type_result = await db.execute(
                select(SupplyChainRisk.risk_type, func.count(SupplyChainRisk.id))
                .where(
                    and_(
                        SupplyChainRisk.ticker_id == ticker.id,
                        SupplyChainRisk.mitigation_status.in_(["unmitigated", "in_progress"])
                    )
                )
                .group_by(SupplyChainRisk.risk_type)
            )
            risks_by_type = {risk_type: count for risk_type, count in type_result}

            # Calculate total revenue at risk
            revenue_result = await db.execute(
                select(func.sum(SupplyChainRisk.revenue_at_risk_pct))
                .where(
                    and_(
                        SupplyChainRisk.ticker_id == ticker.id,
                        SupplyChainRisk.mitigation_status.in_(["unmitigated", "in_progress"])
                    )
                )
            )
            total_revenue_at_risk = revenue_result.scalar() or 0

            # Get recent risks
            recent_risks = await self.get_supply_chain_risks(db, symbol, active_only=True, limit=5)

            # Overall risk score (0-100)
            risk_score = 0
            risk_score += risks_by_level.get("critical", 0) * 25
            risk_score += risks_by_level.get("high", 0) * 15
            risk_score += risks_by_level.get("medium", 0) * 5
            risk_score += risks_by_level.get("low", 0) * 1
            risk_score = min(risk_score, 100)

            summary = {
                "symbol": symbol.upper(),
                "total_active_risks": sum(risks_by_level.values()),
                "risks_by_level": risks_by_level,
                "risks_by_type": risks_by_type,
                "total_revenue_at_risk_pct": round(float(total_revenue_at_risk), 2),
                "risk_score": risk_score,
                "risk_rating": "critical" if risk_score > 75 else "high" if risk_score > 50 else "medium" if risk_score > 25 else "low",
                "recent_risks": recent_risks,
                "analyzed_at": datetime.utcnow().isoformat(),
            }

            await self.cache.set(cache_key, summary, ttl=3600)  # 1 hour
            return summary

        except Exception as e:
            logger.error(f"Error getting risk summary for {symbol}: {e}")
            return {"error": str(e)}

    async def compare_supply_chain(
        self,
        db: AsyncSession,
        symbols: List[str]
    ) -> Dict[str, Any]:
        """
        Compare supply chain metrics across companies

        Args:
            db: Database session
            symbols: List of ticker symbols

        Returns:
            Comparative supply chain analysis
        """
        try:
            cache_key = f"{self.cache_prefix}:compare:{':'.join(sorted(symbols))}"
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

            comparisons = []
            for symbol in symbols:
                # Get dependency analysis
                dependency = await self.get_dependency_analysis(db, symbol)

                # Get risk summary
                risks = await self.get_risk_summary(db, symbol)

                if "error" not in dependency and "error" not in risks:
                    comparisons.append({
                        "symbol": symbol.upper(),
                        "supplier_count": dependency.get("supplier_count", 0),
                        "customer_count": dependency.get("customer_count", 0),
                        "diversification_score": dependency.get("diversification_score", 0),
                        "supplier_concentration_pct": dependency.get("supplier_concentration_pct", 0),
                        "customer_concentration_pct": dependency.get("customer_concentration_pct", 0),
                        "risk_score": risks.get("risk_score", 0),
                        "risk_rating": risks.get("risk_rating", "low"),
                        "total_active_risks": risks.get("total_active_risks", 0),
                    })

            # Rank by diversification score (higher is better)
            ranked = sorted(comparisons, key=lambda x: x["diversification_score"], reverse=True)

            # Add rankings
            for i, comp in enumerate(ranked):
                comp["rank"] = i + 1

            result = {
                "compared_at": datetime.utcnow().isoformat(),
                "stocks": ranked,
                "most_diversified": ranked[0] if ranked else None,
                "least_diversified": ranked[-1] if ranked else None,
                "highest_risk": max(comparisons, key=lambda x: x["risk_score"]) if comparisons else None,
                "lowest_risk": min(comparisons, key=lambda x: x["risk_score"]) if comparisons else None,
                "summary": {
                    "avg_diversification": round(sum(c["diversification_score"] for c in comparisons) / len(comparisons), 2) if comparisons else 0,
                    "avg_risk_score": round(sum(c["risk_score"] for c in comparisons) / len(comparisons), 2) if comparisons else 0,
                }
            }

            await self.cache.set(cache_key, result, ttl=86400)  # 24 hours
            return result

        except Exception as e:
            logger.error(f"Error comparing supply chain: {e}")
            return {"error": str(e)}

    async def get_geographic_exposure(
        self,
        db: AsyncSession,
        symbol: str
    ) -> Dict[str, Any]:
        """
        Analyze geographic exposure through supply chain

        Args:
            db: Database session
            symbol: Ticker symbol

        Returns:
            Geographic exposure analysis
        """
        try:
            cache_key = f"{self.cache_prefix}:geographic:{symbol}"
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

            relationships = await self.get_relationships(db, symbol)

            # Aggregate by geography
            by_geography = {}
            total_relationships = len(relationships)

            for rel in relationships:
                geo = rel.get("primary_geography")
                if geo:
                    if geo not in by_geography:
                        by_geography[geo] = {
                            "geography": geo,
                            "relationship_count": 0,
                            "avg_risk_score": 0,
                            "risk_scores": [],
                            "critical_dependencies": 0,
                        }

                    by_geography[geo]["relationship_count"] += 1

                    if rel.get("geographic_risk_score"):
                        by_geography[geo]["risk_scores"].append(rel["geographic_risk_score"])

                    if rel.get("dependency_level") == "critical":
                        by_geography[geo]["critical_dependencies"] += 1

            # Calculate averages
            for geo_data in by_geography.values():
                scores = geo_data["risk_scores"]
                geo_data["avg_risk_score"] = round(sum(scores) / len(scores), 2) if scores else 0
                geo_data["percentage_of_relationships"] = round(
                    geo_data["relationship_count"] / total_relationships * 100, 2
                ) if total_relationships > 0 else 0
                del geo_data["risk_scores"]  # Remove intermediate data

            # Sort by relationship count
            sorted_geographies = sorted(
                by_geography.values(),
                key=lambda x: x["relationship_count"],
                reverse=True
            )

            exposure = {
                "symbol": symbol.upper(),
                "total_relationships": total_relationships,
                "geographies": sorted_geographies,
                "geographic_diversity": len(by_geography),
                "concentration_risk": "high" if len(by_geography) < 3 else "medium" if len(by_geography) < 5 else "low",
                "analyzed_at": datetime.utcnow().isoformat(),
            }

            await self.cache.set(cache_key, exposure, ttl=86400)  # 24 hours
            return exposure

        except Exception as e:
            logger.error(f"Error analyzing geographic exposure for {symbol}: {e}")
            return {"error": str(e)}

    async def close(self):
        """Cleanup resources"""
        await self.client.aclose()


# Global instance
supply_chain_service = SupplyChainService()
