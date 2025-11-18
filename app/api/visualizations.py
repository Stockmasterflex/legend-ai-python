"""
Market Visualization API Endpoints

Provides data for:
1. Sector Heatmap
2. Stock Screener Heatmap
3. Pattern Distribution Map
4. Correlation Matrix
5. Market Breadth Dashboard (extends existing /api/market/internals)
"""

from fastapi import APIRouter, Query
from typing import Dict, Any, List, Optional
import logging
import asyncio
import numpy as np
from datetime import datetime, timedelta
from app.services.cache import get_cache_service
from app.services.market_data import market_data_service
from app.core.pattern_detector import PatternDetector

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/visualizations", tags=["visualizations"])

# Market sector definitions (SPDR sector ETFs)
SECTOR_ETFS = {
    "XLK": {"name": "Technology", "color": "#3b82f6"},
    "XLF": {"name": "Financials", "color": "#10b981"},
    "XLV": {"name": "Healthcare", "color": "#ef4444"},
    "XLE": {"name": "Energy", "color": "#f59e0b"},
    "XLY": {"name": "Consumer Discretionary", "color": "#8b5cf6"},
    "XLP": {"name": "Consumer Staples", "color": "#06b6d4"},
    "XLI": {"name": "Industrials", "color": "#f97316"},
    "XLB": {"name": "Materials", "color": "#84cc16"},
    "XLRE": {"name": "Real Estate", "color": "#ec4899"},
    "XLC": {"name": "Communication Services", "color": "#6366f1"},
    "XLU": {"name": "Utilities", "color": "#14b8a6"}
}


@router.get("/sectors")
async def get_sector_heatmap_data(
    period: str = Query("1day", description="Timeframe: 1day, 1week, 1month")
):
    """
    Get sector performance data for heatmap visualization

    Returns sector performance, market cap estimates, and metadata
    Cached for 10 minutes for performance
    """
    try:
        cache = get_cache_service()
        cache_key = f"sector_heatmap_{period}"
        cache_ttl = 600  # 10 minutes

        # Try cache first
        cached = await cache.get(cache_key)
        if cached:
            logger.info(f"📊 Sector data from cache ({period})")
            return {
                "success": True,
                "cached": True,
                "data": cached
            }

        # Calculate lookback based on period
        lookback_map = {
            "1day": 5,
            "1week": 30,
            "1month": 90
        }
        lookback = lookback_map.get(period, 30)

        # Fetch data for all sector ETFs
        sectors_data = []

        for ticker, info in SECTOR_ETFS.items():
            try:
                # Get time series data
                data = await asyncio.wait_for(
                    market_data_service.get_time_series(ticker, "1day", lookback),
                    timeout=5.0
                )

                if not data or not data.get("c"):
                    continue

                closes = data["c"]
                volumes = data.get("v", [0] * len(closes))

                # Calculate performance
                if period == "1day":
                    performance = ((closes[-1] - closes[-2]) / closes[-2] * 100) if len(closes) >= 2 else 0
                elif period == "1week":
                    performance = ((closes[-1] - closes[-5]) / closes[-5] * 100) if len(closes) >= 5 else 0
                else:  # 1month
                    performance = ((closes[-1] - closes[-20]) / closes[-20] * 100) if len(closes) >= 20 else 0

                # Get current quote for additional data
                quote = await market_data_service.get_quote(ticker)
                market_cap = quote.get("market_cap", 100000000000) if quote else 100000000000  # Default 100B

                sectors_data.append({
                    "ticker": ticker,
                    "name": info["name"],
                    "performance": round(performance, 2),
                    "price": round(closes[-1], 2),
                    "volume": int(volumes[-1]) if volumes else 0,
                    "market_cap": market_cap,
                    "color": info["color"],
                    "avg_volume": int(sum(volumes) / len(volumes)) if volumes else 0
                })

            except Exception as e:
                logger.warning(f"Failed to fetch {ticker}: {e}")
                continue

        # Sort by performance
        sectors_data.sort(key=lambda x: x["performance"], reverse=True)

        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "period": period,
            "sectors": sectors_data,
            "total_sectors": len(sectors_data)
        }

        # Cache the result
        await cache.set(cache_key, result, ttl=cache_ttl)

        return {
            "success": True,
            "cached": False,
            "data": result
        }

    except Exception as e:
        logger.error(f"Error fetching sector data: {e}")
        return {
            "success": False,
            "detail": str(e)
        }


@router.get("/screener")
async def get_stock_screener_data(
    universe: str = Query("sp500", description="Universe: sp500, nasdaq100, all"),
    color_by: str = Query("change", description="Color metric: change, rs_rating, volume"),
    size_by: str = Query("market_cap", description="Size metric: market_cap, volume"),
    limit: int = Query(100, description="Max stocks to return")
):
    """
    Get stock screener data for heatmap visualization

    Returns S&P 500 or NASDAQ 100 stocks with performance metrics
    Cached for 5 minutes
    """
    try:
        cache = get_cache_service()
        cache_key = f"screener_{universe}_{color_by}_{size_by}_{limit}"
        cache_ttl = 300  # 5 minutes

        # Try cache first
        cached = await cache.get(cache_key)
        if cached:
            logger.info(f"📊 Screener data from cache ({universe})")
            return {
                "success": True,
                "cached": True,
                "data": cached
            }

        # Get universe tickers
        from app.services.universe import universe_service

        if universe == "sp500":
            tickers = await universe_service.get_sp500_tickers()
        elif universe == "nasdaq100":
            tickers = await universe_service.get_nasdaq100_tickers()
        else:
            # Combine both
            sp500 = await universe_service.get_sp500_tickers()
            nasdaq = await universe_service.get_nasdaq100_tickers()
            tickers = list(set(sp500 + nasdaq))

        # Limit the number of tickers to process
        tickers = tickers[:limit]

        # Fetch data for each ticker
        stocks_data = []

        for ticker in tickers:
            try:
                # Get time series and quote
                data = await asyncio.wait_for(
                    market_data_service.get_time_series(ticker, "1day", 60),
                    timeout=3.0
                )

                if not data or not data.get("c"):
                    continue

                closes = data["c"]
                volumes = data.get("v", [0] * len(closes))

                # Calculate metrics
                pct_change = ((closes[-1] - closes[-2]) / closes[-2] * 100) if len(closes) >= 2 else 0

                # Simple RS rating (relative to SPY)
                rs_rating = 50  # Default neutral
                try:
                    spy_data = await market_data_service.get_time_series("SPY", "1day", 60)
                    if spy_data and spy_data.get("c"):
                        spy_closes = spy_data["c"]
                        stock_perf = (closes[-1] - closes[-20]) / closes[-20] if len(closes) >= 20 else 0
                        spy_perf = (spy_closes[-1] - spy_closes[-20]) / spy_closes[-20] if len(spy_closes) >= 20 else 0
                        rs_rating = 50 + (stock_perf - spy_perf) * 100
                        rs_rating = max(0, min(100, rs_rating))  # Clamp to 0-100
                except:
                    pass

                # Get quote for market cap
                quote = await market_data_service.get_quote(ticker)
                market_cap = quote.get("market_cap", 1000000000) if quote else 1000000000

                # Get sector info
                sector = "Other"
                for sector_ticker, sector_info in SECTOR_ETFS.items():
                    # Simple sector mapping (in production, use proper sector data)
                    sector = sector_info["name"]
                    break

                stocks_data.append({
                    "ticker": ticker,
                    "price": round(closes[-1], 2),
                    "change": round(pct_change, 2),
                    "volume": int(volumes[-1]) if volumes else 0,
                    "avg_volume": int(sum(volumes) / len(volumes)) if volumes else 0,
                    "market_cap": market_cap,
                    "rs_rating": round(rs_rating, 1),
                    "sector": sector
                })

            except Exception as e:
                logger.debug(f"Failed to fetch {ticker}: {e}")
                continue

        # Sort by the selected metric
        if color_by == "rs_rating":
            stocks_data.sort(key=lambda x: x["rs_rating"], reverse=True)
        elif color_by == "volume":
            stocks_data.sort(key=lambda x: x["volume"], reverse=True)
        else:
            stocks_data.sort(key=lambda x: x["change"], reverse=True)

        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "universe": universe,
            "color_by": color_by,
            "size_by": size_by,
            "stocks": stocks_data,
            "total_stocks": len(stocks_data)
        }

        # Cache the result
        await cache.set(cache_key, result, ttl=cache_ttl)

        return {
            "success": True,
            "cached": False,
            "data": result
        }

    except Exception as e:
        logger.error(f"Error fetching screener data: {e}")
        return {
            "success": False,
            "detail": str(e)
        }


@router.get("/patterns")
async def get_pattern_distribution_data(
    universe: str = Query("sp500", description="Universe: sp500, nasdaq100"),
    min_score: float = Query(0.5, description="Minimum pattern score (0-1)")
):
    """
    Get pattern distribution data for visualization

    Returns detected patterns across the universe with scores and metadata
    Cached for 15 minutes (expensive computation)
    """
    try:
        cache = get_cache_service()
        cache_key = f"pattern_dist_{universe}_{min_score}"
        cache_ttl = 900  # 15 minutes

        # Try cache first
        cached = await cache.get(cache_key)
        if cached:
            logger.info(f"📊 Pattern distribution from cache ({universe})")
            return {
                "success": True,
                "cached": True,
                "data": cached
            }

        # Get universe tickers (sample to avoid timeout)
        from app.services.universe import universe_service

        if universe == "sp500":
            tickers = await universe_service.get_sp500_tickers()
        else:
            tickers = await universe_service.get_nasdaq100_tickers()

        # Limit to first 50 for performance
        tickers = tickers[:50]

        # Scan for patterns
        patterns_data = []
        pattern_counts = {}

        # Create pattern detector instance
        detector = PatternDetector()

        for ticker in tickers:
            try:
                # Get price data
                price_data = await asyncio.wait_for(
                    market_data_service.get_time_series(ticker, "1day", 500),
                    timeout=5.0
                )

                if not price_data or not price_data.get("c"):
                    continue

                # Get SPY data for RS calculation
                spy_data = await market_data_service.get_time_series("SPY", "1day", 500)

                # Run pattern detection
                result = await asyncio.wait_for(
                    detector.analyze_ticker(ticker, price_data, spy_data),
                    timeout=5.0
                )

                if not result:
                    continue

                # Extract pattern information
                score = result.score / 10.0  # Normalize to 0-1 range
                if score < min_score:
                    continue

                pattern_type = result.pattern

                # Track pattern counts
                if pattern_type not in pattern_counts:
                    pattern_counts[pattern_type] = 0
                pattern_counts[pattern_type] += 1

                patterns_data.append({
                    "ticker": ticker,
                    "pattern_type": pattern_type,
                    "score": round(score, 2),
                    "timeframe": "1day",
                    "detected_at": datetime.utcnow().isoformat(),
                    "description": f"Entry: ${result.entry:.2f}, Target: ${result.target:.2f}",
                    "signal": "bullish"  # PatternDetector focuses on bullish patterns
                })

            except Exception as e:
                logger.debug(f"Failed to scan {ticker}: {e}")
                continue

        # Group patterns by type
        pattern_groups = {}
        for pattern in patterns_data:
            ptype = pattern["pattern_type"]
            if ptype not in pattern_groups:
                pattern_groups[ptype] = []
            pattern_groups[ptype].append(pattern)

        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "universe": universe,
            "min_score": min_score,
            "patterns": patterns_data,
            "pattern_counts": pattern_counts,
            "pattern_groups": pattern_groups,
            "total_patterns": len(patterns_data),
            "tickers_scanned": len(tickers)
        }

        # Cache the result
        await cache.set(cache_key, result, ttl=cache_ttl)

        return {
            "success": True,
            "cached": False,
            "data": result
        }

    except Exception as e:
        logger.error(f"Error fetching pattern distribution: {e}")
        return {
            "success": False,
            "detail": str(e)
        }


@router.get("/correlation")
async def get_correlation_matrix_data(
    tickers: str = Query("SPY,QQQ,IWM,DIA,XLK,XLF,XLV,XLE", description="Comma-separated tickers"),
    period: int = Query(60, description="Lookback period in days")
):
    """
    Get correlation matrix data for visualization

    Calculates correlation between specified tickers
    Cached for 30 minutes
    """
    try:
        cache = get_cache_service()
        ticker_list = [t.strip().upper() for t in tickers.split(",")]
        cache_key = f"correlation_{'_'.join(sorted(ticker_list))}_{period}"
        cache_ttl = 1800  # 30 minutes

        # Try cache first
        cached = await cache.get(cache_key)
        if cached:
            logger.info(f"📊 Correlation data from cache")
            return {
                "success": True,
                "cached": True,
                "data": cached
            }

        # Fetch data for all tickers
        price_data = {}

        for ticker in ticker_list:
            try:
                data = await asyncio.wait_for(
                    market_data_service.get_time_series(ticker, "1day", period),
                    timeout=5.0
                )

                if data and data.get("c"):
                    price_data[ticker] = data["c"]

            except Exception as e:
                logger.warning(f"Failed to fetch {ticker} for correlation: {e}")
                continue

        # Calculate correlation matrix
        if len(price_data) < 2:
            return {
                "success": False,
                "detail": "Not enough ticker data for correlation"
            }

        # Align all price series to same length
        min_length = min(len(prices) for prices in price_data.values())
        aligned_data = {ticker: prices[-min_length:] for ticker, prices in price_data.items()}

        # Calculate returns
        returns_data = {}
        for ticker, prices in aligned_data.items():
            returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]
            returns_data[ticker] = returns

        # Build correlation matrix
        tickers_ordered = sorted(returns_data.keys())
        correlation_matrix = []

        for ticker1 in tickers_ordered:
            row = []
            for ticker2 in tickers_ordered:
                if ticker1 == ticker2:
                    correlation = 1.0
                else:
                    # Calculate correlation coefficient
                    returns1 = returns_data[ticker1]
                    returns2 = returns_data[ticker2]
                    correlation = np.corrcoef(returns1, returns2)[0, 1]

                row.append({
                    "ticker1": ticker1,
                    "ticker2": ticker2,
                    "correlation": round(float(correlation), 3)
                })
            correlation_matrix.append(row)

        # Identify leading/lagging relationships
        leaders = []
        laggers = []

        # Simple heuristic: compare average correlation
        for ticker in tickers_ordered:
            avg_corr = 0
            count = 0
            for row in correlation_matrix:
                for cell in row:
                    if cell["ticker1"] == ticker and cell["ticker2"] != ticker:
                        avg_corr += cell["correlation"]
                        count += 1

            if count > 0:
                avg_corr /= count
                if avg_corr > 0.7:
                    leaders.append({"ticker": ticker, "avg_correlation": round(avg_corr, 3)})
                elif avg_corr < 0.3:
                    laggers.append({"ticker": ticker, "avg_correlation": round(avg_corr, 3)})

        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "tickers": tickers_ordered,
            "period_days": period,
            "correlation_matrix": correlation_matrix,
            "leaders": sorted(leaders, key=lambda x: x["avg_correlation"], reverse=True),
            "laggers": sorted(laggers, key=lambda x: x["avg_correlation"]),
            "data_points": min_length
        }

        # Cache the result
        await cache.set(cache_key, result, ttl=cache_ttl)

        return {
            "success": True,
            "cached": False,
            "data": result
        }

    except Exception as e:
        logger.error(f"Error calculating correlation matrix: {e}")
        return {
            "success": False,
            "detail": str(e)
        }


@router.get("/breadth")
async def get_market_breadth_data():
    """
    Get enhanced market breadth data for dashboard

    Extends the existing /api/market/internals with additional metrics
    Cached for 10 minutes
    """
    try:
        # Leverage existing market internals endpoint
        from app.api.market import get_market_internals

        internals = await get_market_internals()

        if not internals.get("success"):
            return internals

        # Add sector rotation data
        sectors_response = await get_sector_heatmap_data(period="1day")

        if sectors_response.get("success"):
            sectors_data = sectors_response["data"]["sectors"]

            # Calculate sector rotation metrics
            advancing_sectors = sum(1 for s in sectors_data if s["performance"] > 0)
            declining_sectors = sum(1 for s in sectors_data if s["performance"] < 0)

            # Identify rotation trends
            top_sectors = sorted(sectors_data, key=lambda x: x["performance"], reverse=True)[:3]
            bottom_sectors = sorted(sectors_data, key=lambda x: x["performance"])[:3]

            internals["data"]["sector_rotation"] = {
                "advancing_sectors": advancing_sectors,
                "declining_sectors": declining_sectors,
                "top_performers": [{"name": s["name"], "performance": s["performance"]} for s in top_sectors],
                "bottom_performers": [{"name": s["name"], "performance": s["performance"]} for s in bottom_sectors]
            }

        return internals

    except Exception as e:
        logger.error(f"Error fetching breadth data: {e}")
        return {
            "success": False,
            "detail": str(e)
        }
