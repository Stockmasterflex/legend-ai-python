from fastapi import APIRouter
import logging
import asyncio
from typing import Dict, Any
from datetime import datetime
from app.services.cache import get_cache_service
from app.services.market_data import market_data_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/market", tags=["market"])


async def _calculate_market_breadth(universe_tickers: list, max_tickers: int = 50) -> Dict[str, Any]:
    """
    Calculate market breadth metrics (advance/decline, % above EMA, new highs/lows)
    
    For performance, sample the universe if it's too large
    """
    try:
        # Sample tickers to avoid API rate limit issues
        sample_size = min(len(universe_tickers), max_tickers)
        sampled = universe_tickers[:sample_size] if len(universe_tickers) > sample_size else universe_tickers
        
        advances = 0
        declines = 0
        above_50ema = 0
        above_200ema = 0
        new_highs_52w = 0
        new_lows_52w = 0
        
        for ticker in sampled:
            try:
                # Get price data (non-blocking with timeout)
                data = await asyncio.wait_for(
                    market_data_service.get_time_series(ticker, "1day", 252),
                    timeout=5.0,
                )
                
                if not data or not data.get("c"):
                    continue
                
                closes = data["c"]
                highs = data.get("h", closes)
                lows = data.get("l", closes)
                
                current = closes[-1]
                
                # Advance/Decline
                if len(closes) >= 5 and closes[-1] > closes[-5]:
                    advances += 1
                elif len(closes) >= 5:
                    declines += 1
                
                # % above EMA 50 & 200
                if len(closes) >= 50:
                    ema_50 = _calculate_ema(closes, 50)
                    if current > ema_50:
                        above_50ema += 1
                
                if len(closes) >= 200:
                    ema_200 = _calculate_ema(closes, 200)
                    if current > ema_200:
                        above_200ema += 1
                
                # New highs/lows (52-week)
                if len(highs) >= 252:
                    high_52w = max(highs[-252:])
                    low_52w = min(lows[-252:])
                    if current >= high_52w * 0.99:  # Within 1% of 52-week high
                        new_highs_52w += 1
                    if current <= low_52w * 1.01:  # Within 1% of 52-week low
                        new_lows_52w += 1
                        
            except Exception as e:
                logger.debug(f"Failed to fetch breadth data for {ticker}: {e}")
                continue
        
        # Calculate percentages
        total = advances + declines
        pct_advances = (advances / total * 100) if total > 0 else 0
        pct_above_50ema = (above_50ema / sample_size * 100) if sample_size > 0 else 0
        pct_above_200ema = (above_200ema / sample_size * 100) if sample_size > 0 else 0
        
        return {
            "advances": advances,
            "declines": declines,
            "advance_decline_ratio": round(pct_advances, 1),
            "pct_above_50ema": round(pct_above_50ema, 1),
            "pct_above_200ema": round(pct_above_200ema, 1),
            "new_highs_52w": new_highs_52w,
            "new_lows_52w": new_lows_52w,
            "sample_size": sample_size,
            "tickers_sampled": sample_size
        }
    except Exception as e:
        logger.warning(f"Failed to calculate market breadth: {e}")
        return {
            "advances": 0,
            "declines": 0,
            "advance_decline_ratio": 0,
            "pct_above_50ema": 0,
            "pct_above_200ema": 0,
            "new_highs_52w": 0,
            "new_lows_52w": 0,
            "sample_size": 0,
            "error": str(e)
        }


def _calculate_ema(prices: list, period: int) -> float:
    """Calculate Exponential Moving Average"""
    if len(prices) < period:
        return sum(prices) / len(prices)
    
    multiplier = 2 / (period + 1)
    ema = sum(prices[-period:]) / period
    
    for price in prices[-period+1:]:
        ema = price * multiplier + ema * (1 - multiplier)
    
    return ema


def _get_market_regime_label(spy_price: float, sma_50: float, sma_200: float) -> Dict[str, str]:
    """
    Determine market regime with color codes and detailed label
    """
    if spy_price > sma_50 > sma_200:
        return {
            "regime": "STRONG UPTREND",
            "emoji": "🟢",
            "color": "green",
            "signal": "Bullish",
            "confidence": "High"
        }
    elif spy_price > sma_200 > sma_50:
        return {
            "regime": "UPTREND",
            "emoji": "🟢",
            "color": "green",
            "signal": "Bullish",
            "confidence": "Medium"
        }
    elif spy_price > sma_200:
        return {
            "regime": "CONSOLIDATION",
            "emoji": "🟡",
            "color": "yellow",
            "signal": "Neutral",
            "confidence": "Medium"
        }
    elif sma_50 > sma_200:
        return {
            "regime": "CHOPPY DOWNTREND",
            "emoji": "🔴",
            "color": "red",
            "signal": "Bearish",
            "confidence": "Medium"
        }
    else:
        return {
            "regime": "DOWNTREND",
            "emoji": "🔴",
            "color": "red",
            "signal": "Bearish",
            "confidence": "High"
        }


async def _fetch_vix_level() -> Dict[str, Any]:
    """
    Try to fetch VIX level for volatility metrics
    Falls back gracefully if unavailable
    """
    try:
        # Try to get VIX data (^VIX or TVIX)
        vix_data = await asyncio.wait_for(
            market_data_service.get_quote("^VIX"),
            timeout=5.0,
        )
        
        if vix_data and "last_price" in vix_data:
            vix_price = float(vix_data["last_price"])
            
            # Interpret VIX level
            if vix_price < 15:
                volatility = "Low (Complacent)"
            elif vix_price < 20:
                volatility = "Normal"
            elif vix_price < 30:
                volatility = "Elevated (Caution)"
            else:
                volatility = "High (Fear)"
            
            return {
                "vix_level": round(vix_price, 2),
                "volatility_status": volatility,
                "success": True
            }
    except Exception as e:
        logger.debug(f"VIX fetch failed (non-critical): {e}")
    
    return {
        "vix_level": None,
        "volatility_status": "Unknown",
        "success": False
    }


@router.get("/internals")
async def get_market_internals():
    """
    Get comprehensive market internals and regime analysis
    
    Returns:
    - SPY price and moving averages
    - Market regime (uptrend, downtrend, consolidation)
    - Market breadth (advance/decline, % above EMA, new highs/lows)
    - VIX volatility level
    - API usage statistics
    - Cached for 10 minutes for performance
    """
    try:
        cache = get_cache_service()
        cache_key = "market_internals"
        cache_ttl = 600  # 10 minutes
        
        # Try to get from cache first
        cached = await cache.get(cache_key)
        if cached:
            logger.info("📊 Market internals from cache")
            return {
                "success": True,
                "cached": True,
                "data": cached
            }
        
        # Fetch fresh SPY data
        spy_data = await market_data_service.get_time_series("SPY", "1day", 200)

        if not spy_data or not spy_data.get("c"):
            return {
                "success": False,
                "detail": "Could not fetch market data"
            }

        # Extract price and moving averages
        prices = spy_data["c"]
        current_price = prices[-1]
        
        # Calculate SMAs
        sma_50 = sum(prices[-50:]) / 50 if len(prices) >= 50 else current_price
        sma_200 = sum(prices[-200:]) / 200 if len(prices) >= 200 else current_price
        
        # Get regime label
        regime_info = _get_market_regime_label(current_price, sma_50, sma_200)

        # Get market breadth (this can be slow, so we cache heavily)
        try:
            from app.services.universe import universe_service

            # UniverseService exposes async helpers for ticker lists
            try:
                sp500_list = await universe_service.get_sp500_tickers()
            except AttributeError:
                # Legacy fallback to static data module if service API changes
                from app.services import universe_data

                logger.warning("UniverseService missing get_sp500_tickers(); using static fallback list")
                sp500_list = universe_data.get_sp500()

            breadth = await _calculate_market_breadth(sp500_list[:30])  # Sample 30 for speed
        except Exception as e:
            logger.warning(f"Market breadth calculation failed: {e}")
            breadth = {
                "error": "Breadth calculation unavailable",
                "advances": 0,
                "declines": 0
            }

        # Get VIX level
        vix_info = await _fetch_vix_level()

        # Get API usage
        try:
            api_usage = await market_data_service.get_usage_stats()
        except Exception as e:
            logger.warning(f"Failed to fetch API usage stats: {e}")
            api_usage = {"status": "unknown"}

        # Build response
        internals_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "spy_price": round(current_price, 2),
            "sma_50": round(sma_50, 2),
            "sma_200": round(sma_200, 2),
            "regime": f"{regime_info['emoji']} {regime_info['regime']}",
            "regime_details": {
                "label": regime_info["regime"],
                "signal": regime_info["signal"],
                "confidence": regime_info["confidence"],
                "color": regime_info["color"]
            },
            "market_breadth": breadth,
            "volatility": vix_info,
            "api_usage": api_usage
        }

        # Cache for performance
        await cache.set(cache_key, internals_data, ttl=cache_ttl)

        return {
            "success": True,
            "cached": False,
            "data": internals_data,
            "cache_ttl_seconds": cache_ttl
        }

    except Exception as e:
        logger.error(f"Error getting market internals: {e}")
        return {
            "success": False,
            "detail": str(e)
        }


@router.get("/health")
async def market_health():
    """Health check for market data service"""
    try:
        # Quick test
        test_data = await market_data_service.get_quote("SPY")
        
        status = "connected" if test_data else "error"
        
        return {
            "status": "healthy",
            "market_data_api": status,
            "service": "ready",
            "test_ticker": "SPY",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "market_data_api": "disconnected",
            "error": str(e)
        }
