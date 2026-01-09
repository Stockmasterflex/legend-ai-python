
"""
Market Regime Filter
Analyzes broad market conditions (SPY, QQQ, VIX) to determine the environment.
"""
import logging
from typing import Dict, Any, Optional
import pandas as pd

logger = logging.getLogger(__name__)

class MarketRegimeFilter:
    """
    Determines if the market is in a Bull, Bear, or Neutral/Correction phase.
    """
    def __init__(self):
        pass

    async def analyze_regime(self) -> Dict[str, Any]:
        """
        Analyze current market regime.
        Returns dict with keys: 'trend', 'volatility', 'score_factor'
        """
        # In a real implementation, this would fetch SPY/QQQ data.
        # For now, we return a default safe assumption or fetch via market_data_service if possible.
        # Since this method is async, we can await data.
        
        try:
            from app.services.market_data import market_data_service
            # Fetch SPY data
            spy_data = await market_data_service.get_time_series("SPY", "1day", 200)
            if not spy_data or not spy_data.get('c'):
                return self._default_regime()
                
            closes = spy_data.get('c')
            current_price = closes[-1]
            ma50 = sum(closes[-50:]) / 50 if len(closes) >= 50 else current_price
            ma200 = sum(closes[-200:]) / 200 if len(closes) >= 200 else current_price
            
            trend = "NEUTRAL"
            if current_price > ma200:
                trend = "BULL" if current_price > ma50 else "CORRECTION"
            else:
                trend = "BEAR" if current_price < ma50 else "RECOVERY"
                
            return {
                "trend": trend,
                "volatility": "NORMAL", # Placeholder for VIX check
                "ma200": ma200,
                "ma50": ma50,
                "above_200": current_price > ma200
            }
            
        except ImportError:
            logger.warning("MarketData helper not available")
            return self._default_regime()
        except Exception as e:
            logger.error(f"Failed to analyze regime: {e}")
            return self._default_regime()

    def _default_regime(self):
        return {"trend": "NEUTRAL", "volatility": "NORMAL", "above_200": True}
