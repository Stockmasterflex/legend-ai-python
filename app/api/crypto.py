"""
Crypto Trading Analysis API Endpoints

Endpoints:
- GET /crypto/price/{symbol} - Real-time price data
- GET /crypto/patterns/{symbol} - Crypto-specific pattern analysis
- GET /crypto/defi/yields - Top DeFi yields
- GET /crypto/defi/gas - Current gas prices
- GET /crypto/correlation - Cross-asset correlation analysis
- POST /crypto/alerts/monitor - Monitor crypto alerts
- GET /crypto/market/overview - Market overview
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import logging

from app.services.crypto_data import crypto_data_service
from app.services.crypto_patterns import crypto_pattern_analyzer
from app.services.defi_analytics import defi_analytics_service
from app.services.correlation_analysis import correlation_analysis_service
from app.services.crypto_alerts import crypto_alert_service

router = APIRouter(prefix="/crypto", tags=["crypto"])
logger = logging.getLogger(__name__)


@router.get("/price/{symbol}")
async def get_crypto_price(
    symbol: str,
    quote_currency: str = "USDT"
):
    """
    Get real-time crypto price

    Args:
        symbol: Crypto symbol (e.g., BTC, ETH)
        quote_currency: Quote currency (default: USDT)

    Returns:
        {
            "symbol": "BTC",
            "price": 43250.50,
            "source": "binance",
            "timestamp": 1234567890
        }
    """
    try:
        price_data = await crypto_data_service.get_realtime_price(symbol, quote_currency)

        if not price_data:
            raise HTTPException(status_code=404, detail=f"Price data not found for {symbol}")

        return price_data

    except Exception as e:
        logger.exception(f"Failed to get price for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ticker/{symbol}")
async def get_crypto_ticker(symbol: str = "BTCUSDT"):
    """
    Get 24h ticker statistics

    Args:
        symbol: Trading pair (e.g., BTCUSDT)

    Returns:
        24h ticker data including volume, high, low, price change
    """
    try:
        ticker_data = await crypto_data_service.binance.get_24h_ticker(symbol)

        if not ticker_data:
            raise HTTPException(status_code=404, detail=f"Ticker data not found for {symbol}")

        return ticker_data

    except Exception as e:
        logger.exception(f"Failed to get ticker for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patterns/{symbol}")
async def analyze_crypto_patterns(
    symbol: str = "BTCUSDT",
    lookback_hours: int = Query(24, ge=1, le=168)
):
    """
    Analyze crypto-specific patterns

    Args:
        symbol: Trading pair (e.g., BTCUSDT)
        lookback_hours: Lookback period in hours (1-168)

    Returns:
        {
            "whale_activity": {...},
            "exchange_flow": {...},
            "funding_rate": {...},
            "open_interest": {...},
            "overall_signal": "bullish",
            "confidence": 0.78,
            "risk_level": "moderate",
            "recommendations": [...]
        }
    """
    try:
        analysis = await crypto_pattern_analyzer.analyze_comprehensive(symbol, lookback_hours)

        return analysis

    except Exception as e:
        logger.exception(f"Failed to analyze patterns for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/whale/{symbol}")
async def detect_whale_activity(
    symbol: str = "BTCUSDT",
    lookback_hours: int = Query(24, ge=1, le=168)
):
    """
    Detect whale movements

    Returns whale activity analysis including volume spikes and sentiment
    """
    try:
        whale_data = await crypto_pattern_analyzer.whale_detector.detect_whale_activity(
            symbol, lookback_hours
        )

        return whale_data

    except Exception as e:
        logger.exception(f"Failed to detect whale activity for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/funding/{symbol}")
async def get_funding_rate(symbol: str = "BTCUSDT"):
    """
    Get funding rate analysis

    Returns current funding rate with extremeness analysis and reversal risk
    """
    try:
        funding_data = await crypto_pattern_analyzer.funding_analyzer.analyze_funding_rate(symbol)

        return funding_data

    except Exception as e:
        logger.exception(f"Failed to get funding rate for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/defi/yields")
async def get_top_yields(
    min_tvl: float = Query(1_000_000, ge=0),
    min_apy: float = Query(5.0, ge=0),
    max_il_risk: str = Query("moderate", regex="^(low|moderate|high)$"),
    chains: Optional[List[str]] = Query(None)
):
    """
    Get top DeFi yield farming opportunities

    Args:
        min_tvl: Minimum TVL in USD
        min_apy: Minimum APY percentage
        max_il_risk: Maximum impermanent loss risk (low, moderate, high)
        chains: List of blockchain networks to filter (optional)

    Returns:
        List of top yield opportunities sorted by risk-adjusted return
    """
    try:
        yields = await defi_analytics_service.yield_optimizer.find_top_yields(
            min_tvl=min_tvl,
            min_apy=min_apy,
            max_il_risk=max_il_risk,
            chains=chains
        )

        return {"yields": yields, "count": len(yields)}

    except Exception as e:
        logger.exception(f"Failed to get yields: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/defi/gas")
async def get_gas_prices(chain: str = "ethereum"):
    """
    Get current gas prices

    Args:
        chain: Blockchain network (default: ethereum)

    Returns:
        Gas prices for slow, standard, fast, and instant transactions
    """
    try:
        gas_data = await defi_analytics_service.gas_optimizer.get_gas_prices(chain)

        if not gas_data:
            raise HTTPException(status_code=404, detail=f"Gas data not available for {chain}")

        return gas_data

    except Exception as e:
        logger.exception(f"Failed to get gas prices for {chain}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/defi/analytics")
async def get_defi_analytics(
    protocols: Optional[List[str]] = Query(None),
    chains: Optional[List[str]] = Query(None),
    min_apy: float = Query(5.0, ge=0)
):
    """
    Get comprehensive DeFi analytics

    Returns:
        {
            "top_yields": [...],
            "gas_prices": {...},
            "defi_metrics": {...},
            "recommendations": [...]
        }
    """
    try:
        analytics = await defi_analytics_service.get_comprehensive_analysis(
            protocols=protocols,
            chains=chains,
            min_apy=min_apy
        )

        return analytics

    except Exception as e:
        logger.exception(f"Failed to get DeFi analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/correlation")
async def get_correlation_analysis():
    """
    Get comprehensive cross-asset correlation analysis

    Returns:
        {
            "btc_spy_correlation": {...},
            "btc_dominance": {...},
            "market_regime": {...},
            "flight_to_safety": {...},
            "overall_assessment": "...",
            "trading_implications": [...]
        }
    """
    try:
        analysis = await correlation_analysis_service.get_comprehensive_analysis()

        return analysis

    except Exception as e:
        logger.exception(f"Failed to get correlation analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/correlation/btc-spy")
async def get_btc_spy_correlation(lookback_days: int = Query(90, ge=30, le=365)):
    """
    Get BTC vs SPY correlation analysis

    Args:
        lookback_days: Lookback period in days (30-365)

    Returns:
        Correlation analysis between Bitcoin and S&P 500
    """
    try:
        analysis = await correlation_analysis_service.crypto_stock_corr.analyze_btc_spy_correlation(
            lookback_days
        )

        return analysis

    except Exception as e:
        logger.exception(f"Failed to get BTC-SPY correlation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dominance")
async def get_bitcoin_dominance():
    """
    Get Bitcoin dominance analysis

    Returns:
        {
            "btc_dominance": 52.5,
            "eth_dominance": 17.2,
            "regime": "btc_led",
            "signal": "flight_to_quality",
            "interpretation": "..."
        }
    """
    try:
        dominance = await correlation_analysis_service.btc_dominance.get_bitcoin_dominance()

        return dominance

    except Exception as e:
        logger.exception(f"Failed to get Bitcoin dominance: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/market/regime")
async def get_market_regime():
    """
    Detect current market regime (risk-on/risk-off)

    Returns:
        {
            "regime": "risk_on",
            "confidence": 0.75,
            "indicators": {...},
            "interpretation": "...",
            "recommendation": "..."
        }
    """
    try:
        regime = await correlation_analysis_service.risk_indicator.detect_market_regime()

        return regime

    except Exception as e:
        logger.exception(f"Failed to detect market regime: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/alerts/monitor")
async def monitor_crypto_alerts(
    price_watchlist: Optional[List[dict]] = None,
    symbols: Optional[List[str]] = None
):
    """
    Monitor all crypto alert types

    Request body:
        {
            "price_watchlist": [
                {
                    "symbol": "BTCUSDT",
                    "alert_above": 50000,
                    "alert_below": 40000
                }
            ],
            "symbols": ["BTCUSDT", "ETHUSDT"]
        }

    Returns:
        {
            "price_alerts": [...],
            "whale_alerts": [...],
            "flow_alerts": [...],
            "gas_alerts": [...],
            "funding_alerts": [...],
            "oi_alerts": [...],
            "dominance_alerts": [...],
            "total_alerts": 10
        }
    """
    try:
        alerts = await crypto_alert_service.monitor_all(
            price_watchlist=price_watchlist,
            symbols=symbols
        )

        return alerts

    except Exception as e:
        logger.exception(f"Failed to monitor alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/market/overview")
async def get_market_overview():
    """
    Get comprehensive crypto market overview

    Returns:
        {
            "btc_price": {...},
            "eth_price": {...},
            "market_cap": {...},
            "dominance": {...},
            "correlation": {...},
            "top_gainers": [...],
            "top_losers": [...]
        }
    """
    try:
        # Get BTC and ETH prices
        btc_price = await crypto_data_service.get_realtime_price("BTC", "USDT")
        eth_price = await crypto_data_service.get_realtime_price("ETH", "USDT")

        # Get global market data
        global_data = await crypto_data_service.coingecko.get_global_market_data()

        # Get dominance
        dominance = await correlation_analysis_service.btc_dominance.get_bitcoin_dominance()

        # Get top coins
        top_coins = await crypto_data_service.coingecko.get_top_coins(per_page=20)

        # Calculate gainers/losers
        gainers = sorted(
            [c for c in (top_coins or []) if c.get("price_change_percentage_24h", 0) > 0],
            key=lambda x: x.get("price_change_percentage_24h", 0),
            reverse=True
        )[:5]

        losers = sorted(
            [c for c in (top_coins or []) if c.get("price_change_percentage_24h", 0) < 0],
            key=lambda x: x.get("price_change_percentage_24h", 0)
        )[:5]

        return {
            "btc_price": btc_price,
            "eth_price": eth_price,
            "global_market": global_data,
            "dominance": dominance,
            "top_gainers": gainers,
            "top_losers": losers,
            "timestamp": btc_price.get("timestamp") if btc_price else None
        }

    except Exception as e:
        logger.exception(f"Failed to get market overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))
