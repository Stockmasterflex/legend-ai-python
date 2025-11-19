"""
Cross-Asset Correlation Analysis

Features:
- Crypto vs stocks correlation
- Bitcoin dominance tracking
- Risk-on/risk-off indicators
- Flight to safety detection
- Market regime classification
"""

import asyncio
import numpy as np
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timedelta
import logging
import statistics
from scipy import stats
from scipy.stats import pearsonr

from app.services.crypto_data import crypto_data_service
from app.services.market_data import market_data_service

logger = logging.getLogger(__name__)


class CorrelationCalculator:
    """
    Calculate correlations between different asset classes
    """

    def calculate_correlation(
        self,
        series1: List[float],
        series2: List[float]
    ) -> Optional[float]:
        """
        Calculate Pearson correlation coefficient

        Returns:
            Correlation coefficient (-1 to 1)
            None if insufficient data
        """
        if len(series1) != len(series2) or len(series1) < 2:
            return None

        try:
            correlation, _ = pearsonr(series1, series2)
            return correlation
        except Exception as e:
            logger.error(f"Correlation calculation failed: {e}")
            return None

    def calculate_rolling_correlation(
        self,
        series1: List[float],
        series2: List[float],
        window: int = 30
    ) -> List[float]:
        """
        Calculate rolling correlation over a window

        Returns:
            List of correlation coefficients
        """
        if len(series1) != len(series2) or len(series1) < window:
            return []

        correlations = []
        for i in range(window, len(series1) + 1):
            window_series1 = series1[i-window:i]
            window_series2 = series2[i-window:i]
            corr = self.calculate_correlation(window_series1, window_series2)
            if corr is not None:
                correlations.append(corr)

        return correlations


class CryptoStockCorrelation:
    """
    Analyze correlation between crypto and stock markets

    Key metrics:
    - BTC vs SPY correlation
    - ETH vs QQQ correlation
    - Crypto vs tech stocks
    - Leading/lagging relationships
    """

    def __init__(self):
        self.correlation_calc = CorrelationCalculator()

    async def analyze_btc_spy_correlation(
        self,
        lookback_days: int = 90
    ) -> Dict[str, Any]:
        """
        Analyze BTC vs SPY (S&P 500 ETF) correlation

        Returns:
            {
                "correlation": 0.65,
                "trend": "increasing",  # or "decreasing", "stable"
                "regime": "risk_on",  # or "risk_off", "decoupled"
                "strength": "strong",  # weak, moderate, strong
                "recent_30d": 0.72,
                "recent_7d": 0.85,
                "interpretation": "BTC following stock market"
            }
        """
        try:
            # Get BTC data
            btc_klines = await crypto_data_service.binance.get_klines(
                symbol="BTCUSDT",
                interval="1d",
                limit=lookback_days
            )

            if not btc_klines or len(btc_klines) < 30:
                return {"error": "Insufficient BTC data"}

            # Get SPY data (using market_data_service)
            spy_data = await market_data_service.get_time_series("SPY", "1day", lookback_days)

            if not spy_data or len(spy_data.get("c", [])) < 30:
                return {"error": "Insufficient SPY data"}

            # Align data (take minimum length)
            min_length = min(len(btc_klines), len(spy_data["c"]))
            btc_prices = [k["c"] for k in btc_klines[:min_length]]
            spy_prices = spy_data["c"][:min_length]

            # Calculate returns
            btc_returns = [(btc_prices[i] - btc_prices[i-1]) / btc_prices[i-1] for i in range(1, len(btc_prices))]
            spy_returns = [(spy_prices[i] - spy_prices[i-1]) / spy_prices[i-1] for i in range(1, len(spy_prices))]

            # Overall correlation
            overall_corr = self.correlation_calc.calculate_correlation(btc_returns, spy_returns)

            # Recent correlations
            corr_30d = self.correlation_calc.calculate_correlation(btc_returns[-30:], spy_returns[-30:]) if len(btc_returns) >= 30 else None
            corr_7d = self.correlation_calc.calculate_correlation(btc_returns[-7:], spy_returns[-7:]) if len(btc_returns) >= 7 else None

            # Determine trend
            if corr_7d is not None and corr_30d is not None:
                if corr_7d > corr_30d + 0.1:
                    trend = "increasing"
                elif corr_7d < corr_30d - 0.1:
                    trend = "decreasing"
                else:
                    trend = "stable"
            else:
                trend = "unknown"

            # Classify regime
            if overall_corr and overall_corr > 0.5:
                regime = "risk_on"  # BTC moving with stocks
            elif overall_corr and overall_corr < -0.3:
                regime = "risk_off"  # BTC moving inverse to stocks
            else:
                regime = "decoupled"  # BTC moving independently

            # Correlation strength
            if overall_corr is None:
                strength = "unknown"
            elif abs(overall_corr) > 0.7:
                strength = "strong"
            elif abs(overall_corr) > 0.3:
                strength = "moderate"
            else:
                strength = "weak"

            # Interpretation
            if regime == "risk_on" and strength in ["strong", "moderate"]:
                interpretation = "BTC following stock market - treat as risk asset"
            elif regime == "risk_off":
                interpretation = "BTC moving inverse to stocks - potential safe haven"
            elif regime == "decoupled":
                interpretation = "BTC moving independently - crypto-specific factors dominating"
            else:
                interpretation = "Unclear correlation pattern"

            return {
                "correlation": round(overall_corr, 3) if overall_corr else None,
                "trend": trend,
                "regime": regime,
                "strength": strength,
                "recent_30d": round(corr_30d, 3) if corr_30d else None,
                "recent_7d": round(corr_7d, 3) if corr_7d else None,
                "interpretation": interpretation,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.exception(f"BTC-SPY correlation analysis failed: {e}")
            return {"error": str(e)}


class BitcoinDominanceTracker:
    """
    Track Bitcoin dominance in crypto market

    Bitcoin dominance indicates:
    - High dominance (>50%): BTC leading, altcoin weakness
    - Low dominance (<40%): Altcoin season
    - Rising dominance: Flight to quality
    - Falling dominance: Risk appetite for altcoins
    """

    async def get_bitcoin_dominance(self) -> Dict[str, Any]:
        """
        Get current Bitcoin dominance

        Returns:
            {
                "btc_dominance": 52.5,
                "eth_dominance": 17.2,
                "others_dominance": 30.3,
                "trend": "increasing",
                "regime": "btc_led",  # or "altcoin_season", "balanced"
                "signal": "flight_to_quality",
                "interpretation": "..."
            }
        """
        try:
            # Get global market data from CoinGecko
            global_data = await crypto_data_service.coingecko.get_global_market_data()

            if not global_data:
                return {"error": "Failed to fetch market data"}

            # Extract dominance data
            market_cap_percentage = global_data.get("market_cap_percentage", {})
            btc_dominance = market_cap_percentage.get("btc", 0)
            eth_dominance = market_cap_percentage.get("eth", 0)
            others_dominance = 100 - btc_dominance - eth_dominance

            # Get historical BTC prices to determine trend
            btc_klines = await crypto_data_service.binance.get_klines(
                symbol="BTCUSDT",
                interval="1d",
                limit=30
            )

            # Estimate trend (would need historical dominance data for accuracy)
            # For now, use BTC price momentum as proxy
            if btc_klines and len(btc_klines) >= 7:
                recent_btc_change = (btc_klines[-1]["c"] - btc_klines[-7]["c"]) / btc_klines[-7]["c"]
                trend = "increasing" if recent_btc_change > 0.05 else "decreasing" if recent_btc_change < -0.05 else "stable"
            else:
                trend = "unknown"

            # Classify regime
            if btc_dominance > 50:
                regime = "btc_led"
            elif btc_dominance < 40:
                regime = "altcoin_season"
            else:
                regime = "balanced"

            # Generate signal
            if trend == "increasing" and btc_dominance > 45:
                signal = "flight_to_quality"
            elif trend == "decreasing" and btc_dominance < 50:
                signal = "alt_rotation"
            else:
                signal = "neutral"

            # Interpretation
            if regime == "btc_led":
                interpretation = "Bitcoin dominance high - BTC leading market, altcoins may underperform"
            elif regime == "altcoin_season":
                interpretation = "Bitcoin dominance low - Altcoin season, higher risk appetite"
            else:
                interpretation = "Balanced market - BTC and altcoins moving together"

            return {
                "btc_dominance": round(btc_dominance, 2),
                "eth_dominance": round(eth_dominance, 2),
                "others_dominance": round(others_dominance, 2),
                "trend": trend,
                "regime": regime,
                "signal": signal,
                "interpretation": interpretation,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.exception(f"Bitcoin dominance tracking failed: {e}")
            return {"error": str(e)}


class RiskOnOffIndicator:
    """
    Detect risk-on vs risk-off market conditions

    Risk-on indicators:
    - Stocks rising, VIX falling
    - Crypto rising with stocks
    - High-yield bonds outperforming
    - Cyclicals outperforming defensives

    Risk-off indicators:
    - Stocks falling, VIX rising
    - Flight to bonds/gold
    - Defensive sectors outperforming
    - Crypto selling off
    """

    async def detect_market_regime(self) -> Dict[str, Any]:
        """
        Detect current market regime

        Returns:
            {
                "regime": "risk_on",  # or "risk_off", "neutral"
                "confidence": 0.75,
                "indicators": {
                    "stocks": "rising",
                    "crypto": "rising",
                    "vix": "low",
                    "correlation": "high"
                },
                "interpretation": "...",
                "recommendation": "..."
            }
        """
        try:
            # Get SPY data (stocks proxy)
            spy_data = await market_data_service.get_time_series("SPY", "1day", 30)

            # Get BTC data (crypto proxy)
            btc_klines = await crypto_data_service.binance.get_klines(
                symbol="BTCUSDT",
                interval="1d",
                limit=30
            )

            if not spy_data or not btc_klines:
                return {"error": "Insufficient data"}

            # Calculate recent performance
            spy_7d_change = ((spy_data["c"][-1] - spy_data["c"][-7]) / spy_data["c"][-7]) * 100 if len(spy_data["c"]) >= 7 else 0
            btc_7d_change = ((btc_klines[-1]["c"] - btc_klines[-7]["c"]) / btc_klines[-7]["c"]) * 100 if len(btc_klines) >= 7 else 0

            # Score indicators
            indicators = {}
            risk_on_score = 0
            total_indicators = 0

            # Stocks indicator
            if spy_7d_change > 2:
                indicators["stocks"] = "rising"
                risk_on_score += 1
            elif spy_7d_change < -2:
                indicators["stocks"] = "falling"
            else:
                indicators["stocks"] = "neutral"
            total_indicators += 1

            # Crypto indicator
            if btc_7d_change > 5:
                indicators["crypto"] = "rising"
                risk_on_score += 1
            elif btc_7d_change < -5:
                indicators["crypto"] = "falling"
            else:
                indicators["crypto"] = "neutral"
            total_indicators += 1

            # VIX proxy (inverse of stock momentum)
            if spy_7d_change > 2:
                indicators["vix"] = "low"
                risk_on_score += 1
            elif spy_7d_change < -2:
                indicators["vix"] = "high"
            else:
                indicators["vix"] = "neutral"
            total_indicators += 1

            # Correlation indicator
            if spy_7d_change * btc_7d_change > 0 and abs(spy_7d_change) > 1 and abs(btc_7d_change) > 3:
                indicators["correlation"] = "high"
                risk_on_score += 1 if spy_7d_change > 0 else 0
            else:
                indicators["correlation"] = "low"
            total_indicators += 1

            # Determine regime
            confidence = risk_on_score / total_indicators

            if confidence >= 0.6:
                regime = "risk_on"
            elif confidence <= 0.3:
                regime = "risk_off"
            else:
                regime = "neutral"

            # Interpretation
            if regime == "risk_on":
                interpretation = "Risk-on environment - stocks and crypto rising together, investors taking risk"
                recommendation = "Favorable for crypto and growth assets"
            elif regime == "risk_off":
                interpretation = "Risk-off environment - flight to safety, risk assets selling off"
                recommendation = "Caution advised - consider defensive positioning"
            else:
                interpretation = "Neutral market - mixed signals, no clear trend"
                recommendation = "Wait for clearer signals before major positioning"

            return {
                "regime": regime,
                "confidence": round(confidence, 2),
                "indicators": indicators,
                "spy_7d_change": round(spy_7d_change, 2),
                "btc_7d_change": round(btc_7d_change, 2),
                "interpretation": interpretation,
                "recommendation": recommendation,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.exception(f"Risk regime detection failed: {e}")
            return {"error": str(e)}


class FlightToSafetyDetector:
    """
    Detect flight to safety events

    Indicators:
    - Gold rising sharply
    - Treasury bonds rallying (TLT)
    - Dollar strengthening (DXY)
    - Crypto and stocks selling off
    - VIX spiking
    """

    async def detect_flight_to_safety(self) -> Dict[str, Any]:
        """
        Detect if market is experiencing flight to safety

        Returns:
            {
                "flight_to_safety": true,
                "severity": "moderate",  # or "high", "low"
                "indicators": {
                    "stocks_down": true,
                    "crypto_down": true,
                    "gold_up": true,
                    "bonds_up": true
                },
                "recommendation": "...",
                "duration_estimate": "1-2 weeks"
            }
        """
        try:
            # Get market data
            spy_data = await market_data_service.get_time_series("SPY", "1day", 14)
            btc_klines = await crypto_data_service.binance.get_klines("BTCUSDT", "1d", 14)
            gld_data = await market_data_service.get_time_series("GLD", "1day", 14)  # Gold ETF

            if not all([spy_data, btc_klines, gld_data]):
                return {"error": "Insufficient data"}

            # Calculate 7-day changes
            spy_change = ((spy_data["c"][-1] - spy_data["c"][-7]) / spy_data["c"][-7]) * 100 if len(spy_data["c"]) >= 7 else 0
            btc_change = ((btc_klines[-1]["c"] - btc_klines[-7]["c"]) / btc_klines[-7]["c"]) * 100 if len(btc_klines) >= 7 else 0
            gld_change = ((gld_data["c"][-1] - gld_data["c"][-7]) / gld_data["c"][-7]) * 100 if len(gld_data["c"]) >= 7 else 0

            # Score indicators
            indicators = {}
            safety_score = 0

            # Stocks down
            if spy_change < -3:
                indicators["stocks_down"] = True
                safety_score += 1
            else:
                indicators["stocks_down"] = False

            # Crypto down
            if btc_change < -5:
                indicators["crypto_down"] = True
                safety_score += 1
            else:
                indicators["crypto_down"] = False

            # Gold up
            if gld_change > 2:
                indicators["gold_up"] = True
                safety_score += 1
            else:
                indicators["gold_up"] = False

            # Determine if flight to safety
            flight_to_safety = safety_score >= 2

            # Severity
            if safety_score >= 3:
                severity = "high"
                duration_estimate = "2-4 weeks"
            elif safety_score == 2:
                severity = "moderate"
                duration_estimate = "1-2 weeks"
            else:
                severity = "low"
                duration_estimate = "< 1 week"

            # Recommendation
            if flight_to_safety:
                recommendation = "⚠️ Flight to safety detected - reduce risk exposure, consider defensive assets"
            else:
                recommendation = "No significant flight to safety - normal market conditions"

            return {
                "flight_to_safety": flight_to_safety,
                "severity": severity,
                "indicators": indicators,
                "safety_score": safety_score,
                "spy_change_7d": round(spy_change, 2),
                "btc_change_7d": round(btc_change, 2),
                "gld_change_7d": round(gld_change, 2),
                "recommendation": recommendation,
                "duration_estimate": duration_estimate,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.exception(f"Flight to safety detection failed: {e}")
            return {"error": str(e)}


class CorrelationAnalysisService:
    """
    Unified correlation analysis service
    """

    def __init__(self):
        self.crypto_stock_corr = CryptoStockCorrelation()
        self.btc_dominance = BitcoinDominanceTracker()
        self.risk_indicator = RiskOnOffIndicator()
        self.safety_detector = FlightToSafetyDetector()

    async def get_comprehensive_analysis(self) -> Dict[str, Any]:
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
        # Run all analyses in parallel
        btc_spy_task = self.crypto_stock_corr.analyze_btc_spy_correlation()
        dominance_task = self.btc_dominance.get_bitcoin_dominance()
        regime_task = self.risk_indicator.detect_market_regime()
        safety_task = self.safety_detector.detect_flight_to_safety()

        results = await asyncio.gather(
            btc_spy_task,
            dominance_task,
            regime_task,
            safety_task,
            return_exceptions=True
        )

        btc_spy, dominance, regime, safety = results

        # Handle exceptions
        if isinstance(btc_spy, Exception):
            btc_spy = {"error": str(btc_spy)}
        if isinstance(dominance, Exception):
            dominance = {"error": str(dominance)}
        if isinstance(regime, Exception):
            regime = {"error": str(regime)}
        if isinstance(safety, Exception):
            safety = {"error": str(safety)}

        # Overall assessment
        if safety.get("flight_to_safety"):
            overall_assessment = "🚨 Flight to safety - high risk environment"
        elif regime.get("regime") == "risk_on":
            overall_assessment = "📈 Risk-on environment - favorable for crypto"
        elif regime.get("regime") == "risk_off":
            overall_assessment = "📉 Risk-off environment - defensive positioning advised"
        else:
            overall_assessment = "⚖️ Neutral market conditions"

        # Trading implications
        implications = []

        if btc_spy.get("correlation", 0) > 0.7:
            implications.append("BTC highly correlated with stocks - watch equity markets closely")

        if dominance.get("regime") == "btc_led":
            implications.append("BTC dominance high - focus on BTC over altcoins")
        elif dominance.get("regime") == "altcoin_season":
            implications.append("Altcoin season - altcoins may outperform BTC")

        if regime.get("regime") == "risk_on":
            implications.append("Risk-on environment - suitable for long positions")
        elif regime.get("regime") == "risk_off":
            implications.append("Risk-off environment - reduce exposure or hedge")

        if safety.get("flight_to_safety"):
            implications.append("Flight to safety - expect increased volatility")

        return {
            "btc_spy_correlation": btc_spy,
            "btc_dominance": dominance,
            "market_regime": regime,
            "flight_to_safety": safety,
            "overall_assessment": overall_assessment,
            "trading_implications": implications,
            "timestamp": datetime.now().isoformat()
        }


# Global instance
correlation_analysis_service = CorrelationAnalysisService()
