"""
API Usage Monitoring and Cost Dashboard

Provides real-time insights into:
- API call usage across all providers
- Cache hit rates and efficiency
- Cost projections and savings
- Optimization recommendations
"""
from fastapi import APIRouter
from typing import Dict, Any, List
from datetime import datetime
import logging

from app.services.market_data import market_data_service
from app.services.cache import get_cache_service
from app.config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api-usage", tags=["monitoring"])


@router.get("", response_model=Dict[str, Any])
async def get_api_usage_dashboard():
    """
    Comprehensive API usage monitoring dashboard

    Returns:
        - Current API usage for all providers
        - Cache statistics and hit rates
        - Cost projections based on current usage
        - Optimization recommendations
        - Estimated monthly savings from optimizations
    """
    settings = get_settings()
    cache = get_cache_service()

    try:
        # Get API usage stats
        usage_stats = await market_data_service.get_usage_stats()

        # Get cache statistics
        cache_stats = await cache.get_cache_stats()

        # Calculate cost projections
        cost_analysis = _calculate_cost_projections(usage_stats, cache_stats)

        # Generate optimization recommendations
        recommendations = _generate_recommendations(usage_stats, cache_stats)

        return {
            "timestamp": datetime.now().isoformat(),
            "api_usage": usage_stats,
            "cache_performance": cache_stats,
            "cost_analysis": cost_analysis,
            "recommendations": recommendations,
            "status": "healthy"
        }

    except Exception as e:
        logger.error(f"Error generating API usage dashboard: {e}")
        return {
            "error": str(e),
            "status": "error"
        }


@router.get("/summary", response_model=Dict[str, Any])
async def get_usage_summary():
    """
    Quick summary of API usage and cost savings

    Perfect for displaying in the main dashboard
    """
    try:
        usage_stats = await market_data_service.get_usage_stats()
        cache = get_cache_service()
        cache_stats = await cache.get_cache_stats()

        # Calculate daily cost
        daily_cost = _calculate_daily_cost(usage_stats)

        # Calculate cache savings
        cache_hit_rate = cache_stats.get("redis_hit_rate", 0)
        estimated_saved_calls = int((cache_hit_rate / 100) * 1000)  # Estimate

        return {
            "daily_api_calls": sum(
                api["used"] for api in usage_stats.values() if isinstance(api, dict)
            ),
            "daily_cost_usd": round(daily_cost, 2),
            "monthly_projection_usd": round(daily_cost * 30, 2),
            "cache_hit_rate": round(cache_hit_rate, 1),
            "estimated_calls_saved": estimated_saved_calls,
            "status": "optimized" if cache_hit_rate > 50 else "needs_optimization"
        }

    except Exception as e:
        logger.error(f"Error generating usage summary: {e}")
        return {"error": str(e)}


@router.get("/sources", response_model=Dict[str, Any])
async def get_source_distribution():
    """
    Show distribution of API calls across different data sources

    Helps identify which sources are being used most and optimize accordingly
    """
    try:
        usage_stats = await market_data_service.get_usage_stats()

        total_calls = sum(
            api["used"] for api in usage_stats.values() if isinstance(api, dict)
        )

        sources = []
        for source_name, stats in usage_stats.items():
            if isinstance(stats, dict) and "used" in stats:
                sources.append({
                    "name": source_name,
                    "calls": stats["used"],
                    "limit": stats["limit"],
                    "remaining": stats["remaining"],
                    "percent_used": round(stats["percent"], 1),
                    "percent_of_total": round((stats["used"] / max(total_calls, 1)) * 100, 1),
                    "cost_per_call": _get_cost_per_call(source_name),
                    "daily_cost": round(stats["used"] * _get_cost_per_call(source_name), 4)
                })

        return {
            "total_calls": total_calls,
            "sources": sources,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error getting source distribution: {e}")
        return {"error": str(e)}


def _calculate_cost_projections(usage_stats: Dict, cache_stats: Dict) -> Dict[str, Any]:
    """Calculate cost projections based on current usage"""

    # Current daily costs (all free tier usage = $0)
    current_daily_cost = 0.0

    # TwelveData, Finnhub, Alpha Vantage are all free tier
    # Only Chart-IMG PRO is paid (~$9/month fixed)
    chart_img_monthly = 9.0

    # Calculate what it would cost WITHOUT optimization
    unoptimized_costs = {
        "twelvedata": usage_stats.get("twelvedata", {}).get("used", 0) * 0.01,  # Hypothetical paid tier
        "finnhub": usage_stats.get("finnhub", {}).get("used", 0) * 0.005,
        "alphavantage": usage_stats.get("alphavantage", {}).get("used", 0) * 0.01,
    }
    unoptimized_daily = sum(unoptimized_costs.values())

    # Cache savings
    cache_hit_rate = cache_stats.get("redis_hit_rate", 0)
    estimated_calls_without_cache = int((100 / max(100 - cache_hit_rate, 1)) * 1000)
    additional_cost_without_cache = (estimated_calls_without_cache - 1000) * 0.008

    return {
        "current": {
            "daily_usd": round(current_daily_cost, 2),
            "monthly_usd": round(chart_img_monthly, 2),
            "annual_usd": round(chart_img_monthly * 12, 2)
        },
        "without_optimization": {
            "daily_usd": round(unoptimized_daily, 2),
            "monthly_usd": round(unoptimized_daily * 30 + chart_img_monthly, 2),
            "annual_usd": round((unoptimized_daily * 30 + chart_img_monthly) * 12, 2)
        },
        "savings": {
            "daily_usd": round(unoptimized_daily - current_daily_cost, 2),
            "monthly_usd": round((unoptimized_daily - current_daily_cost) * 30, 2),
            "annual_usd": round((unoptimized_daily - current_daily_cost) * 365, 2),
            "cache_savings_usd": round(additional_cost_without_cache * 30, 2)
        },
        "breakdown": {
            "free_tier_apis": "TwelveData (800/day) + Finnhub (60/day) + Alpha Vantage (500/day) = FREE",
            "chart_img": f"${chart_img_monthly}/month (PRO plan)",
            "redis_cache": "FREE (Upstash 10k cmds/day)",
            "yahoo_finance": "FREE (unlimited, used for historical data)"
        }
    }


def _calculate_daily_cost(usage_stats: Dict) -> float:
    """Calculate estimated daily cost in USD"""
    # Currently on free tiers, so cost is $0 for API calls
    # Only fixed cost is Chart-IMG PRO at ~$9/month = $0.30/day
    return 0.30


def _get_cost_per_call(source: str) -> float:
    """Get cost per API call for each source (for hypothetical paid scenarios)"""
    costs = {
        "twelvedata": 0.0,  # Free tier (800/day)
        "finnhub": 0.0,     # Free tier (60/day)
        "alphavantage": 0.0, # Free tier (500/day)
        "yahoo": 0.0        # Always free
    }
    return costs.get(source, 0.0)


def _generate_recommendations(usage_stats: Dict, cache_stats: Dict) -> List[Dict[str, Any]]:
    """Generate optimization recommendations based on usage patterns"""
    recommendations = []

    # Check cache hit rate
    cache_hit_rate = cache_stats.get("redis_hit_rate", 0)
    if cache_hit_rate < 50:
        recommendations.append({
            "priority": "high",
            "category": "caching",
            "title": "Low cache hit rate detected",
            "description": f"Current hit rate: {cache_hit_rate:.1f}%. Increase TTLs for historical data.",
            "potential_savings": "30-50% reduction in API calls",
            "action": "Already implemented: Smart TTLs with market hours awareness"
        })
    elif cache_hit_rate > 80:
        recommendations.append({
            "priority": "low",
            "category": "caching",
            "title": "Excellent cache performance",
            "description": f"Cache hit rate: {cache_hit_rate:.1f}%. System is well optimized.",
            "potential_savings": "N/A",
            "action": "Continue monitoring"
        })

    # Check TwelveData usage
    twelvedata = usage_stats.get("twelvedata", {})
    if twelvedata.get("percent", 0) > 75:
        recommendations.append({
            "priority": "medium",
            "category": "rate_limits",
            "title": "TwelveData approaching daily limit",
            "description": f"Using {twelvedata.get('used')}/{twelvedata.get('limit')} calls ({twelvedata.get('percent'):.1f}%)",
            "potential_savings": "Prevent service disruption",
            "action": "Enable prefer_free mode for historical data requests"
        })

    # Check for optimization opportunities
    total_calls = sum(api.get("used", 0) for api in usage_stats.values() if isinstance(api, dict))
    if total_calls > 100:
        recommendations.append({
            "priority": "medium",
            "category": "batching",
            "title": "Use batch API for bulk requests",
            "description": f"Detected {total_calls} API calls today. Batch requests reduce latency.",
            "potential_savings": "50-70% faster bulk operations",
            "action": "Use market_data_service.get_time_series_batch() for scanner"
        })

    # Always recommend monitoring
    recommendations.append({
        "priority": "low",
        "category": "monitoring",
        "title": "Regular usage monitoring",
        "description": "Check this dashboard daily to catch anomalies early",
        "potential_savings": "Prevent unexpected costs",
        "action": "Bookmark /api-usage endpoint"
    })

    return recommendations
