from fastapi import APIRouter
import logging
from typing import Dict

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/market", tags=["market"])

@router.get("/internals")
async def get_market_internals():
    """Get market internals and regime"""
    try:
        from app.services.market_data import market_data_service

        # Get SPY price data
        spy_data = await market_data_service.get_time_series("SPY", "1day", 200)

        if not spy_data or not spy_data.get("c"):
            return {
                "success": False,
                "detail": "Could not fetch market data"
            }

        prices = spy_data["c"]
        current_price = prices[-1]
        sma_50 = sum(prices[-50:]) / 50 if len(prices) >= 50 else current_price
        sma_200 = sum(prices[-200:]) / 200 if len(prices) >= 200 else current_price

        # Determine market regime
        if current_price > sma_50 > sma_200:
            regime = "🟢 UPTREND"
            status = "Bullish"
        elif current_price > sma_200:
            regime = "🟡 CONSOLIDATION"
            status = "Neutral"
        else:
            regime = "🔴 DOWNTREND"
            status = "Bearish"

        return {
            "success": True,
            "data": {
                "spy_price": round(current_price, 2),
                "sma_50": round(sma_50, 2),
                "sma_200": round(sma_200, 2),
                "regime": regime,
                "status": status
            }
        }
    except Exception as e:
        logger.error(f"Error getting market internals: {e}")
        return {
            "success": False,
            "detail": str(e)
        }

