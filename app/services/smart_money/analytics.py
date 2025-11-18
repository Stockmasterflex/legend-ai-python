"""
Smart Money Analytics Service

Aggregates and analyzes smart money data from all sources:
- Dark pool ratio and trends
- Institutional flows
- Accumulation/distribution analysis
- Composite smart money indicators
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import logging

from .models import (
    SmartMoneyFlow,
    SmartMoneyIndicators,
    Sentiment,
    SmartMoneyAlert
)
from .dark_pool import get_dark_pool_service
from .institutional import get_institutional_service
from .block_trades import get_block_trade_service

logger = logging.getLogger(__name__)


class SmartMoneyAnalyticsService:
    """Service for aggregated smart money analytics"""

    def __init__(self):
        self.dark_pool = get_dark_pool_service()
        self.institutional = get_institutional_service()
        self.block_trades = get_block_trade_service()

    async def get_smart_money_flow(
        self,
        symbol: str,
        date: Optional[datetime] = None,
        total_volume: Optional[int] = None
    ) -> SmartMoneyFlow:
        """
        Get comprehensive smart money flow for a symbol

        Args:
            symbol: Stock ticker symbol
            date: Date to analyze (defaults to today)
            total_volume: Total market volume for dark pool ratio calculation

        Returns:
            Smart money flow data
        """
        if not date:
            date = datetime.now()

        try:
            # Get dark pool data
            dp_summary = await self.dark_pool.get_daily_summary(symbol, date)
            dark_pool_volume = dp_summary.get("total_volume", 0)
            dark_pool_value = dp_summary.get("total_value", 0)

            # Calculate dark pool ratio
            if total_volume and total_volume > 0:
                dark_pool_ratio = dark_pool_volume / total_volume
            else:
                dark_pool_ratio = await self.dark_pool.calculate_dark_pool_ratio(
                    symbol, total_volume or dark_pool_volume, date
                )

            # Get block trades data
            block_trades = await self.block_trades.get_recent_blocks(
                symbol,
                hours=24
            )
            block_trades_count = len(block_trades)
            block_trades_value = sum(t.value for t in block_trades)

            # Get institutional flow
            inst_flow = await self.institutional.get_institutional_flow(symbol)
            institutional_buying = max(0, inst_flow.get("net_change_shares", 0)) * 178.50  # Example price
            institutional_selling = abs(min(0, inst_flow.get("net_change_shares", 0))) * 178.50
            net_institutional_flow = institutional_buying - institutional_selling

            # Get insider sentiment
            insider_sentiment = await self.institutional.analyze_insider_sentiment(symbol)
            insider_buying = insider_sentiment.get("total_buy_value", 0)
            insider_selling = insider_sentiment.get("total_sell_value", 0)
            net_insider_flow = insider_buying - insider_selling

            # Calculate smart money confidence score (0-100)
            confidence = await self._calculate_confidence_score(
                dark_pool_ratio=dark_pool_ratio,
                institutional_flow=net_institutional_flow,
                insider_flow=net_insider_flow,
                block_trades_count=block_trades_count
            )

            # Determine accumulation/distribution
            accum_dist = await self._determine_accumulation_distribution(
                net_institutional_flow=net_institutional_flow,
                net_insider_flow=net_insider_flow,
                dark_pool_sentiment=dp_summary.get("sentiment", {}).get("bullish_percentage", 50)
            )

            return SmartMoneyFlow(
                symbol=symbol,
                date=date,
                dark_pool_volume=dark_pool_volume,
                dark_pool_value=dark_pool_value,
                dark_pool_ratio=round(dark_pool_ratio, 4),
                block_trades_count=block_trades_count,
                block_trades_value=block_trades_value,
                institutional_buying=institutional_buying,
                institutional_selling=institutional_selling,
                net_institutional_flow=net_institutional_flow,
                insider_buying=insider_buying,
                insider_selling=insider_selling,
                net_insider_flow=net_insider_flow,
                smart_money_confidence=round(confidence, 2),
                accumulation_distribution=accum_dist
            )

        except Exception as e:
            logger.error(f"Error getting smart money flow for {symbol}: {e}")
            return self._empty_flow(symbol, date)

    async def get_smart_money_indicators(
        self,
        symbol: str,
        price_change: Optional[float] = None
    ) -> SmartMoneyIndicators:
        """
        Get comprehensive smart money indicators

        Args:
            symbol: Stock ticker symbol
            price_change: Recent price change percentage for divergence analysis

        Returns:
            Smart money indicators
        """
        try:
            timestamp = datetime.now()

            # Dark pool metrics
            dp_summary = await self.dark_pool.get_daily_summary(symbol)
            dp_patterns = await self.dark_pool.get_historical_patterns(symbol, days=30)

            dark_pool_ratio = dp_summary.get("total_volume", 0) / 10_000_000  # Normalized
            dp_bullish_pct = dp_summary.get("sentiment", {}).get("bullish_percentage", 50)

            dark_pool_sentiment = (
                Sentiment.BULLISH if dp_bullish_pct > 60 else
                Sentiment.BEARISH if dp_bullish_pct < 40 else
                Sentiment.NEUTRAL
            )
            dark_pool_trend = dp_patterns.get("volume_trend", "stable")

            # Institutional metrics
            inst_flow = await self.institutional.get_institutional_flow(symbol)
            institutional_ownership = inst_flow.get("institutional_ownership", 0)
            inst_flow_5d = inst_flow.get("net_change_shares", 0) * 178.50
            inst_flow_20d = inst_flow_5d * 4  # Approximate

            # Determine institutional momentum
            flow_pct = inst_flow.get("net_change_percentage", 0)
            if flow_pct > 2:
                inst_momentum = "strong_buying"
            elif flow_pct > 0:
                inst_momentum = "buying"
            elif flow_pct < -2:
                inst_momentum = "strong_selling"
            elif flow_pct < 0:
                inst_momentum = "selling"
            else:
                inst_momentum = "neutral"

            # Block trade metrics
            blocks = await self.block_trades.get_recent_blocks(symbol, hours=24)
            block_trade_frequency = len(blocks)

            block_bullish = len([b for b in blocks if b.sentiment == Sentiment.BULLISH])
            block_bearish = len([b for b in blocks if b.sentiment == Sentiment.BEARISH])

            block_sentiment = (
                Sentiment.BULLISH if block_bullish > block_bearish else
                Sentiment.BEARISH if block_bearish > block_bullish else
                Sentiment.NEUTRAL
            )

            # Unusual activity score
            unusual = await self.dark_pool.detect_unusual_activity(symbol)
            unusual_score = min(100, unusual.get("volume_ratio", 1) * 25)

            # Calculate composite indicators
            smart_money_index = await self._calculate_smart_money_index(
                dark_pool_sentiment=dark_pool_sentiment,
                institutional_momentum=inst_momentum,
                block_sentiment=block_sentiment,
                unusual_score=unusual_score
            )

            # Divergence score
            divergence_score = 0.0
            if price_change is not None:
                divergence = await self.block_trades.detect_smart_money_divergence(
                    symbol, price_change, days=5
                )
                if divergence.get("has_divergence"):
                    divergence_score = abs(divergence.get("smart_money_flow", 0) - price_change)

            # Accumulation score (-100 to 100)
            accumulation_score = await self._calculate_accumulation_score(
                institutional_flow=inst_flow_5d,
                dark_pool_sentiment=dp_bullish_pct
            )

            return SmartMoneyIndicators(
                symbol=symbol,
                timestamp=timestamp,
                dark_pool_ratio=round(dark_pool_ratio, 4),
                dark_pool_sentiment=dark_pool_sentiment,
                dark_pool_trend=dark_pool_trend,
                institutional_ownership=institutional_ownership,
                institutional_flow_5d=inst_flow_5d,
                institutional_flow_20d=inst_flow_20d,
                institutional_momentum=inst_momentum,
                block_trade_frequency=block_trade_frequency,
                block_trade_sentiment=block_sentiment,
                unusual_activity_score=round(unusual_score, 2),
                smart_money_index=round(smart_money_index, 2),
                divergence_score=round(divergence_score, 2),
                accumulation_score=round(accumulation_score, 2)
            )

        except Exception as e:
            logger.error(f"Error getting smart money indicators for {symbol}: {e}")
            return self._empty_indicators(symbol)

    async def get_dashboard_data(
        self,
        symbol: str,
        price_change: Optional[float] = None,
        total_volume: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get complete dashboard data for a symbol

        Args:
            symbol: Stock ticker symbol
            price_change: Recent price change percentage
            total_volume: Total market volume

        Returns:
            Complete dashboard data
        """
        try:
            # Get all components in parallel
            flow_task = self.get_smart_money_flow(symbol, total_volume=total_volume)
            indicators_task = self.get_smart_money_indicators(symbol, price_change)
            dp_prints_task = self.dark_pool.get_realtime_prints(symbol, limit=20)
            inst_holders_task = self.institutional.get_top_holders(symbol, limit=10)
            blocks_task = self.block_trades.get_recent_blocks(symbol, hours=24)
            alerts_task = self.block_trades.get_alerts(symbol, hours=24)

            flow, indicators, dp_prints, holders, blocks, alerts = await asyncio.gather(
                flow_task,
                indicators_task,
                dp_prints_task,
                inst_holders_task,
                blocks_task,
                alerts_task
            )

            # Get options positioning
            options_positioning = await self.block_trades.analyze_options_positioning(symbol)

            # Get insider sentiment
            insider_sentiment = await self.institutional.analyze_insider_sentiment(symbol)

            return {
                "symbol": symbol,
                "timestamp": datetime.now().isoformat(),
                "smart_money_flow": flow.model_dump(),
                "indicators": indicators.model_dump(),
                "dark_pool": {
                    "recent_prints": [p.model_dump() for p in dp_prints],
                    "summary": await self.dark_pool.get_daily_summary(symbol)
                },
                "institutional": {
                    "top_holders": [h.model_dump() for h in holders],
                    "flow": await self.institutional.get_institutional_flow(symbol),
                    "insider_sentiment": insider_sentiment
                },
                "block_trades": {
                    "recent_blocks": [b.model_dump() for b in blocks],
                    "options_positioning": options_positioning
                },
                "alerts": [a.model_dump() for a in alerts]
            }

        except Exception as e:
            logger.error(f"Error getting dashboard data for {symbol}: {e}")
            return {"symbol": symbol, "error": str(e)}

    async def _calculate_confidence_score(
        self,
        dark_pool_ratio: float,
        institutional_flow: float,
        insider_flow: float,
        block_trades_count: int
    ) -> float:
        """Calculate smart money confidence score (0-100)"""
        try:
            score = 50.0  # Base score

            # Dark pool contribution (±15 points)
            if dark_pool_ratio > 0.4:
                score += 15
            elif dark_pool_ratio > 0.3:
                score += 10
            elif dark_pool_ratio > 0.2:
                score += 5

            # Institutional flow contribution (±20 points)
            if institutional_flow > 500_000_000:
                score += 20
            elif institutional_flow > 100_000_000:
                score += 10
            elif institutional_flow < -500_000_000:
                score -= 20
            elif institutional_flow < -100_000_000:
                score -= 10

            # Insider flow contribution (±10 points)
            if insider_flow > 50_000_000:
                score += 10
            elif insider_flow > 10_000_000:
                score += 5
            elif insider_flow < -50_000_000:
                score -= 10
            elif insider_flow < -10_000_000:
                score -= 5

            # Block trades contribution (±5 points)
            if block_trades_count > 50:
                score += 5
            elif block_trades_count > 30:
                score += 3

            # Clamp to 0-100
            return max(0, min(100, score))

        except Exception as e:
            logger.error(f"Error calculating confidence score: {e}")
            return 50.0

    async def _determine_accumulation_distribution(
        self,
        net_institutional_flow: float,
        net_insider_flow: float,
        dark_pool_sentiment: float
    ) -> str:
        """Determine if accumulation or distribution is occurring"""
        try:
            # Weighted score
            inst_weight = 0.6
            insider_weight = 0.2
            dp_weight = 0.2

            score = (
                (1 if net_institutional_flow > 0 else -1) * inst_weight +
                (1 if net_insider_flow > 0 else -1) * insider_weight +
                ((dark_pool_sentiment - 50) / 50) * dp_weight
            )

            if score > 0.3:
                return "accumulation"
            elif score < -0.3:
                return "distribution"
            else:
                return "neutral"

        except Exception as e:
            logger.error(f"Error determining accumulation/distribution: {e}")
            return "neutral"

    async def _calculate_smart_money_index(
        self,
        dark_pool_sentiment: Sentiment,
        institutional_momentum: str,
        block_sentiment: Sentiment,
        unusual_score: float
    ) -> float:
        """Calculate composite smart money index (0-100)"""
        try:
            score = 0.0

            # Dark pool (25 points)
            if dark_pool_sentiment == Sentiment.BULLISH:
                score += 25
            elif dark_pool_sentiment == Sentiment.BEARISH:
                score += 0
            else:
                score += 12.5

            # Institutional (35 points)
            inst_scores = {
                "strong_buying": 35,
                "buying": 25,
                "neutral": 17.5,
                "selling": 10,
                "strong_selling": 0
            }
            score += inst_scores.get(institutional_momentum, 17.5)

            # Block trades (25 points)
            if block_sentiment == Sentiment.BULLISH:
                score += 25
            elif block_sentiment == Sentiment.BEARISH:
                score += 0
            else:
                score += 12.5

            # Unusual activity (15 points)
            score += min(15, unusual_score * 0.15)

            return min(100, score)

        except Exception as e:
            logger.error(f"Error calculating smart money index: {e}")
            return 50.0

    async def _calculate_accumulation_score(
        self,
        institutional_flow: float,
        dark_pool_sentiment: float
    ) -> float:
        """Calculate accumulation score (-100 to 100)"""
        try:
            # Institutional flow component (-50 to 50)
            inst_score = min(50, max(-50, institutional_flow / 10_000_000))

            # Dark pool component (-50 to 50)
            dp_score = (dark_pool_sentiment - 50)

            # Combined score
            return inst_score + (dp_score * 0.5)

        except Exception as e:
            logger.error(f"Error calculating accumulation score: {e}")
            return 0.0

    def _empty_flow(self, symbol: str, date: datetime) -> SmartMoneyFlow:
        """Return empty flow structure"""
        return SmartMoneyFlow(
            symbol=symbol,
            date=date,
            dark_pool_volume=0,
            dark_pool_value=0,
            dark_pool_ratio=0,
            block_trades_count=0,
            block_trades_value=0,
            institutional_buying=0,
            institutional_selling=0,
            net_institutional_flow=0,
            insider_buying=0,
            insider_selling=0,
            net_insider_flow=0,
            smart_money_confidence=50,
            accumulation_distribution="neutral"
        )

    def _empty_indicators(self, symbol: str) -> SmartMoneyIndicators:
        """Return empty indicators structure"""
        return SmartMoneyIndicators(
            symbol=symbol,
            timestamp=datetime.now(),
            dark_pool_ratio=0,
            dark_pool_sentiment=Sentiment.NEUTRAL,
            dark_pool_trend="stable",
            institutional_ownership=0,
            institutional_flow_5d=0,
            institutional_flow_20d=0,
            institutional_momentum="neutral",
            block_trade_frequency=0,
            block_trade_sentiment=Sentiment.NEUTRAL,
            unusual_activity_score=0,
            smart_money_index=50,
            divergence_score=0,
            accumulation_score=0
        )


# Global instance
_analytics_service = None


def get_analytics_service() -> SmartMoneyAnalyticsService:
    """Get or create analytics service instance"""
    global _analytics_service
    if _analytics_service is None:
        _analytics_service = SmartMoneyAnalyticsService()
    return _analytics_service
