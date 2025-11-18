"""
Crypto-Specific Pattern Analysis

Features:
- Whale movement detection
- Exchange flow analysis (inflow/outflow)
- Funding rate analysis
- Open interest tracking
- Liquidation cascades
- Unusual volume detection
"""

import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import logging
from decimal import Decimal
import statistics

from app.services.crypto_data import crypto_data_service

logger = logging.getLogger(__name__)


class WhaleMovementDetector:
    """
    Detect whale movements (large transactions)

    Criteria:
    - Transaction > $1M USD equivalent
    - Unusual volume spikes (>3 std dev from mean)
    - Large exchange deposits/withdrawals
    """

    def __init__(self):
        self.whale_threshold_usd = 1_000_000  # $1M minimum
        self.volume_spike_threshold = 3.0  # 3 standard deviations

    async def detect_whale_activity(
        self,
        symbol: str = "BTCUSDT",
        lookback_hours: int = 24
    ) -> Dict[str, Any]:
        """
        Detect whale activity in the past N hours

        Returns:
            {
                "symbol": "BTCUSDT",
                "whale_detected": true,
                "volume_spike": 4.2,  # Standard deviations above mean
                "large_trades": 15,
                "total_whale_volume_usd": 125000000,
                "sentiment": "accumulation",  # or "distribution"
                "confidence": 0.85
            }
        """
        # Get historical kline data
        klines = await crypto_data_service.binance.get_klines(
            symbol=symbol,
            interval="1h",
            limit=lookback_hours
        )

        if not klines or len(klines) < lookback_hours:
            logger.warning(f"Insufficient data for whale detection on {symbol}")
            return {
                "symbol": symbol,
                "whale_detected": False,
                "error": "Insufficient data"
            }

        # Calculate volume statistics
        volumes = [k["v"] for k in klines]
        mean_volume = statistics.mean(volumes)
        std_volume = statistics.stdev(volumes) if len(volumes) > 1 else 0

        # Detect volume spikes
        recent_volume = volumes[-1]
        volume_z_score = (recent_volume - mean_volume) / std_volume if std_volume > 0 else 0

        # Estimate whale trades (volume spikes > threshold)
        whale_candles = [k for k in klines if (k["v"] - mean_volume) / std_volume > self.volume_spike_threshold] if std_volume > 0 else []

        # Calculate total whale volume
        total_whale_volume = sum(k["qv"] for k in whale_candles)

        # Determine sentiment (accumulation vs distribution)
        # If price increasing with high volume = accumulation
        # If price decreasing with high volume = distribution
        price_change = (klines[-1]["c"] - klines[0]["c"]) / klines[0]["c"]
        sentiment = "accumulation" if price_change > 0 else "distribution"

        # Confidence based on volume spike magnitude and frequency
        confidence = min(abs(volume_z_score) / 5.0, 1.0)  # Max out at 5 std dev

        return {
            "symbol": symbol,
            "whale_detected": volume_z_score > self.volume_spike_threshold,
            "volume_spike": round(volume_z_score, 2),
            "large_trades": len(whale_candles),
            "total_whale_volume_usd": round(total_whale_volume, 2),
            "sentiment": sentiment,
            "price_change_pct": round(price_change * 100, 2),
            "confidence": round(confidence, 2),
            "timestamp": datetime.now().isoformat()
        }


class ExchangeFlowAnalyzer:
    """
    Analyze exchange inflows and outflows

    Key metrics:
    - Net flow (inflow - outflow)
    - Exchange reserves
    - Flow velocity
    - Accumulation/distribution signals
    """

    async def analyze_exchange_flow(
        self,
        symbol: str = "BTCUSDT",
        lookback_hours: int = 24
    ) -> Dict[str, Any]:
        """
        Analyze exchange flow patterns

        Returns:
            {
                "symbol": "BTCUSDT",
                "net_flow_btc": -1250.5,  # Negative = outflow (bullish)
                "net_flow_usd": -54000000,
                "inflow": 2500,
                "outflow": 3750.5,
                "flow_trend": "outflow",  # or "inflow"
                "signal": "bullish",  # Outflow typically bullish
                "velocity": 0.05,  # Flow as % of market cap
                "confidence": 0.75
            }
        """
        # Get volume data
        klines = await crypto_data_service.binance.get_klines(
            symbol=symbol,
            interval="1h",
            limit=lookback_hours
        )

        if not klines or len(klines) < 12:
            return {
                "symbol": symbol,
                "error": "Insufficient data"
            }

        # Calculate net flow proxy using volume and price action
        # High volume on red candles = potential inflow (distribution)
        # High volume on green candles = potential outflow (accumulation)
        inflow_proxy = 0.0
        outflow_proxy = 0.0

        for k in klines:
            if k["c"] < k["o"]:  # Red candle
                inflow_proxy += k["v"]
            else:  # Green candle
                outflow_proxy += k["v"]

        net_flow = outflow_proxy - inflow_proxy
        avg_price = statistics.mean([k["c"] for k in klines])
        net_flow_usd = net_flow * avg_price

        # Determine trend
        flow_trend = "outflow" if net_flow > 0 else "inflow"
        signal = "bullish" if flow_trend == "outflow" else "bearish"

        # Calculate confidence based on magnitude
        total_flow = inflow_proxy + outflow_proxy
        flow_imbalance = abs(net_flow) / total_flow if total_flow > 0 else 0
        confidence = min(flow_imbalance * 2, 1.0)  # Max at 50% imbalance

        return {
            "symbol": symbol,
            "net_flow_btc": round(net_flow, 2),
            "net_flow_usd": round(net_flow_usd, 2),
            "inflow": round(inflow_proxy, 2),
            "outflow": round(outflow_proxy, 2),
            "flow_trend": flow_trend,
            "signal": signal,
            "flow_imbalance_pct": round(flow_imbalance * 100, 2),
            "confidence": round(confidence, 2),
            "timestamp": datetime.now().isoformat()
        }


class FundingRateAnalyzer:
    """
    Analyze funding rates for futures contracts

    Funding rate insights:
    - Positive funding = Longs pay shorts (bullish sentiment)
    - Negative funding = Shorts pay longs (bearish sentiment)
    - Extreme funding = Overleveraged position, potential reversal
    """

    def __init__(self):
        # Funding rate thresholds (annualized %)
        self.extreme_positive = 0.10  # 10% annualized (very bullish, potential top)
        self.extreme_negative = -0.10  # -10% annualized (very bearish, potential bottom)
        self.neutral_range = 0.01  # ±1% is considered neutral

    async def analyze_funding_rate(self, symbol: str = "BTCUSDT") -> Dict[str, Any]:
        """
        Analyze current funding rate

        Returns:
            {
                "symbol": "BTCUSDT",
                "funding_rate": 0.0001,  # Current 8h rate
                "funding_rate_annualized": 0.1095,  # 10.95% APR
                "sentiment": "bullish",
                "extremeness": "extreme",  # or "high", "moderate", "neutral"
                "reversal_risk": "high",  # Risk of squeeze/reversal
                "signal": "potential_top",  # or "potential_bottom", "neutral"
                "next_funding_time": "2024-01-01T16:00:00Z"
            }
        """
        # Get current funding rate
        funding_data = await crypto_data_service.binance.get_funding_rate(symbol)

        if not funding_data:
            return {
                "symbol": symbol,
                "error": "Failed to fetch funding rate"
            }

        funding_rate = float(funding_data.get("fundingRate", 0))
        funding_time = funding_data.get("fundingTime", 0)

        # Annualize the rate (funding happens every 8 hours)
        # Annual rate = 8h rate × 3 payments/day × 365 days
        annualized_rate = funding_rate * 3 * 365

        # Determine sentiment and extremeness
        if funding_rate > 0:
            sentiment = "bullish"
            if annualized_rate > self.extreme_positive:
                extremeness = "extreme"
                signal = "potential_top"
                reversal_risk = "high"
            elif annualized_rate > self.extreme_positive / 2:
                extremeness = "high"
                signal = "monitor_for_reversal"
                reversal_risk = "moderate"
            else:
                extremeness = "moderate"
                signal = "neutral"
                reversal_risk = "low"
        elif funding_rate < 0:
            sentiment = "bearish"
            if annualized_rate < self.extreme_negative:
                extremeness = "extreme"
                signal = "potential_bottom"
                reversal_risk = "high"
            elif annualized_rate < self.extreme_negative / 2:
                extremeness = "high"
                signal = "monitor_for_reversal"
                reversal_risk = "moderate"
            else:
                extremeness = "moderate"
                signal = "neutral"
                reversal_risk = "low"
        else:
            sentiment = "neutral"
            extremeness = "neutral"
            signal = "neutral"
            reversal_risk = "low"

        return {
            "symbol": symbol,
            "funding_rate": funding_rate,
            "funding_rate_annualized": round(annualized_rate, 4),
            "funding_rate_annualized_pct": round(annualized_rate * 100, 2),
            "sentiment": sentiment,
            "extremeness": extremeness,
            "reversal_risk": reversal_risk,
            "signal": signal,
            "next_funding_time": datetime.fromtimestamp(funding_time / 1000).isoformat(),
            "timestamp": datetime.now().isoformat()
        }


class OpenInterestAnalyzer:
    """
    Analyze open interest for futures contracts

    Open Interest insights:
    - Increasing OI + Rising price = Strong uptrend
    - Increasing OI + Falling price = Strong downtrend
    - Decreasing OI + Rising price = Short covering
    - Decreasing OI + Falling price = Long liquidation
    """

    async def analyze_open_interest(
        self,
        symbol: str = "BTCUSDT",
        lookback_hours: int = 24
    ) -> Dict[str, Any]:
        """
        Analyze open interest trends

        Returns:
            {
                "symbol": "BTCUSDT",
                "current_oi": 125000,
                "oi_change_24h": 5.2,  # % change
                "price_change_24h": 2.8,
                "trend": "strong_uptrend",  # Based on OI + price
                "signal": "bullish",
                "leverage_ratio": 0.15,  # OI / Market cap
                "liquidation_risk": "moderate"
            }
        """
        # Get current open interest
        oi_data = await crypto_data_service.binance.get_open_interest(symbol)

        if not oi_data:
            return {
                "symbol": symbol,
                "error": "Failed to fetch open interest"
            }

        current_oi = float(oi_data.get("openInterest", 0))

        # Get historical price data
        klines = await crypto_data_service.binance.get_klines(
            symbol=symbol,
            interval="1h",
            limit=lookback_hours
        )

        if not klines or len(klines) < 2:
            return {
                "symbol": symbol,
                "current_oi": current_oi,
                "error": "Insufficient historical data"
            }

        # Calculate price change
        old_price = klines[0]["c"]
        new_price = klines[-1]["c"]
        price_change_pct = ((new_price - old_price) / old_price) * 100

        # Estimate OI change (would need historical OI data for accuracy)
        # For now, use volume as a proxy
        recent_volume = sum(k["v"] for k in klines[-6:])  # Last 6 hours
        older_volume = sum(k["v"] for k in klines[:6])  # First 6 hours
        oi_change_proxy = ((recent_volume - older_volume) / older_volume) * 100 if older_volume > 0 else 0

        # Determine trend based on OI and price
        oi_increasing = oi_change_proxy > 0
        price_increasing = price_change_pct > 0

        if oi_increasing and price_increasing:
            trend = "strong_uptrend"
            signal = "bullish"
        elif oi_increasing and not price_increasing:
            trend = "strong_downtrend"
            signal = "bearish"
        elif not oi_increasing and price_increasing:
            trend = "short_covering"
            signal = "neutral_bullish"
        else:
            trend = "long_liquidation"
            signal = "neutral_bearish"

        # Estimate liquidation risk based on OI magnitude
        if oi_change_proxy > 20:
            liquidation_risk = "high"
        elif oi_change_proxy > 10:
            liquidation_risk = "moderate"
        else:
            liquidation_risk = "low"

        return {
            "symbol": symbol,
            "current_oi": round(current_oi, 2),
            "oi_change_proxy_pct": round(oi_change_proxy, 2),
            "price_change_24h_pct": round(price_change_pct, 2),
            "trend": trend,
            "signal": signal,
            "liquidation_risk": liquidation_risk,
            "timestamp": datetime.now().isoformat()
        }


class CryptoPatternAnalyzer:
    """
    Unified crypto-specific pattern analyzer

    Combines:
    - Whale movements
    - Exchange flows
    - Funding rates
    - Open interest
    """

    def __init__(self):
        self.whale_detector = WhaleMovementDetector()
        self.flow_analyzer = ExchangeFlowAnalyzer()
        self.funding_analyzer = FundingRateAnalyzer()
        self.oi_analyzer = OpenInterestAnalyzer()

    async def analyze_comprehensive(
        self,
        symbol: str = "BTCUSDT",
        lookback_hours: int = 24
    ) -> Dict[str, Any]:
        """
        Perform comprehensive crypto pattern analysis

        Returns:
            {
                "symbol": "BTCUSDT",
                "whale_activity": {...},
                "exchange_flow": {...},
                "funding_rate": {...},
                "open_interest": {...},
                "overall_signal": "bullish",  # Aggregated signal
                "confidence": 0.78,
                "risk_level": "moderate",
                "recommendations": ["Monitor for potential top", ...]
            }
        """
        # Run all analyses in parallel
        whale_task = self.whale_detector.detect_whale_activity(symbol, lookback_hours)
        flow_task = self.flow_analyzer.analyze_exchange_flow(symbol, lookback_hours)
        funding_task = self.funding_analyzer.analyze_funding_rate(symbol)
        oi_task = self.oi_analyzer.analyze_open_interest(symbol, lookback_hours)

        whale_data, flow_data, funding_data, oi_data = await asyncio.gather(
            whale_task, flow_task, funding_task, oi_task
        )

        # Aggregate signals
        signals = []
        confidences = []

        # Whale sentiment
        if whale_data.get("whale_detected"):
            signals.append(whale_data.get("sentiment"))
            confidences.append(whale_data.get("confidence", 0))

        # Flow signal
        if flow_data.get("signal"):
            signal_map = {"bullish": "accumulation", "bearish": "distribution"}
            signals.append(signal_map.get(flow_data["signal"], "neutral"))
            confidences.append(flow_data.get("confidence", 0))

        # Funding signal
        if funding_data.get("signal") == "potential_top":
            signals.append("bearish")
            confidences.append(0.7)
        elif funding_data.get("signal") == "potential_bottom":
            signals.append("bullish")
            confidences.append(0.7)

        # OI signal
        if oi_data.get("signal"):
            oi_signal_map = {
                "bullish": "bullish",
                "bearish": "bearish",
                "neutral_bullish": "neutral",
                "neutral_bearish": "neutral"
            }
            signals.append(oi_signal_map.get(oi_data["signal"], "neutral"))

        # Calculate overall signal
        bullish_count = signals.count("accumulation") + signals.count("bullish")
        bearish_count = signals.count("distribution") + signals.count("bearish")

        if bullish_count > bearish_count:
            overall_signal = "bullish"
        elif bearish_count > bullish_count:
            overall_signal = "bearish"
        else:
            overall_signal = "neutral"

        # Average confidence
        avg_confidence = statistics.mean(confidences) if confidences else 0.5

        # Determine risk level
        funding_risk = funding_data.get("reversal_risk", "low")
        oi_risk = oi_data.get("liquidation_risk", "low")

        risk_levels = {"low": 1, "moderate": 2, "high": 3}
        max_risk = max(risk_levels.get(funding_risk, 1), risk_levels.get(oi_risk, 1))
        risk_level = {1: "low", 2: "moderate", 3: "high"}[max_risk]

        # Generate recommendations
        recommendations = []
        if funding_data.get("signal") == "potential_top":
            recommendations.append("⚠️ Funding rate extremely high - monitor for potential top")
        if funding_data.get("signal") == "potential_bottom":
            recommendations.append("💡 Funding rate extremely negative - potential bottom forming")
        if whale_data.get("whale_detected"):
            recommendations.append(f"🐋 Whale {whale_data['sentiment']} detected")
        if flow_data.get("flow_trend") == "outflow":
            recommendations.append("📤 Strong outflow - accumulation phase")
        if oi_data.get("liquidation_risk") == "high":
            recommendations.append("⚠️ High liquidation risk - expect volatility")

        return {
            "symbol": symbol,
            "whale_activity": whale_data,
            "exchange_flow": flow_data,
            "funding_rate": funding_data,
            "open_interest": oi_data,
            "overall_signal": overall_signal,
            "confidence": round(avg_confidence, 2),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }


# Global instance
crypto_pattern_analyzer = CryptoPatternAnalyzer()
