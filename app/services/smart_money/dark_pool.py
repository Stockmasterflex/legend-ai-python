"""
Dark Pool Tracking Service

Monitors and analyzes dark pool prints, including:
- Real-time prints
- Size and price analysis
- Premium/discount calculations
- Historical patterns
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import logging
from collections import defaultdict
import statistics

from .models import DarkPoolPrint, Sentiment

logger = logging.getLogger(__name__)


class DarkPoolService:
    """Service for tracking dark pool activity"""

    def __init__(self):
        # In-memory storage for demo (replace with database in production)
        self._prints: Dict[str, List[DarkPoolPrint]] = defaultdict(list)
        self._historical_data: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    async def get_realtime_prints(
        self,
        symbol: str,
        limit: int = 50,
        min_size: Optional[int] = None,
        min_value: Optional[float] = None
    ) -> List[DarkPoolPrint]:
        """
        Get real-time dark pool prints for a symbol

        Args:
            symbol: Stock ticker symbol
            limit: Maximum number of prints to return
            min_size: Minimum share size filter
            min_value: Minimum dollar value filter

        Returns:
            List of dark pool prints
        """
        try:
            # Get prints for symbol
            prints = self._prints.get(symbol, [])

            # Apply filters
            filtered = prints
            if min_size:
                filtered = [p for p in filtered if p.size >= min_size]
            if min_value:
                filtered = [p for p in filtered if p.value >= min_value]

            # Sort by timestamp descending and limit
            filtered.sort(key=lambda x: x.timestamp, reverse=True)
            return filtered[:limit]

        except Exception as e:
            logger.error(f"Error getting dark pool prints for {symbol}: {e}")
            return []

    async def get_daily_summary(
        self,
        symbol: str,
        date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get daily dark pool summary for a symbol

        Args:
            symbol: Stock ticker symbol
            date: Date to analyze (defaults to today)

        Returns:
            Dictionary with daily statistics
        """
        if not date:
            date = datetime.now()

        try:
            # Get prints for the day
            prints = await self.get_prints_for_date(symbol, date)

            if not prints:
                return self._empty_summary(symbol, date)

            # Calculate statistics
            total_prints = len(prints)
            total_volume = sum(p.size for p in prints)
            total_value = sum(p.value for p in prints)
            avg_price = statistics.mean(p.price for p in prints)
            avg_size = total_volume / total_prints if total_prints > 0 else 0

            # Premium/discount analysis
            premium_prints = [p for p in prints if p.is_premium]
            discount_prints = [p for p in prints if not p.is_premium]
            premium_percentage = (len(premium_prints) / total_prints * 100) if total_prints > 0 else 0

            # Sentiment analysis
            bullish = len([p for p in prints if p.sentiment == Sentiment.BULLISH])
            bearish = len([p for p in prints if p.sentiment == Sentiment.BEARISH])
            neutral = len([p for p in prints if p.sentiment == Sentiment.NEUTRAL])

            # Large blocks (>$1M)
            large_blocks = [p for p in prints if p.value >= 1_000_000]
            large_blocks_value = sum(p.value for p in large_blocks)

            return {
                "symbol": symbol,
                "date": date.isoformat(),
                "total_prints": total_prints,
                "total_volume": total_volume,
                "total_value": total_value,
                "average_price": round(avg_price, 2),
                "average_size": int(avg_size),
                "premium_prints": len(premium_prints),
                "discount_prints": len(discount_prints),
                "premium_percentage": round(premium_percentage, 2),
                "sentiment": {
                    "bullish": bullish,
                    "bearish": bearish,
                    "neutral": neutral,
                    "bullish_percentage": round(bullish / total_prints * 100, 2) if total_prints > 0 else 0
                },
                "large_blocks": {
                    "count": len(large_blocks),
                    "value": large_blocks_value,
                    "percentage_of_value": round(large_blocks_value / total_value * 100, 2) if total_value > 0 else 0
                }
            }

        except Exception as e:
            logger.error(f"Error getting daily summary for {symbol}: {e}")
            return self._empty_summary(symbol, date)

    async def get_prints_for_date(
        self,
        symbol: str,
        date: datetime
    ) -> List[DarkPoolPrint]:
        """Get all prints for a specific date"""
        try:
            prints = self._prints.get(symbol, [])
            date_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
            date_end = date_start + timedelta(days=1)

            return [
                p for p in prints
                if date_start <= p.timestamp < date_end
            ]
        except Exception as e:
            logger.error(f"Error getting prints for date {date}: {e}")
            return []

    async def get_historical_patterns(
        self,
        symbol: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Analyze historical dark pool patterns

        Args:
            symbol: Stock ticker symbol
            days: Number of days to analyze

        Returns:
            Historical pattern analysis
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)

            # Get all prints in range
            all_prints = self._prints.get(symbol, [])
            period_prints = [
                p for p in all_prints
                if start_date <= p.timestamp <= end_date
            ]

            if not period_prints:
                return self._empty_patterns(symbol, days)

            # Daily aggregation
            daily_stats = defaultdict(lambda: {
                "volume": 0,
                "value": 0,
                "prints": 0,
                "premium_count": 0
            })

            for print_item in period_prints:
                day = print_item.timestamp.date().isoformat()
                daily_stats[day]["volume"] += print_item.size
                daily_stats[day]["value"] += print_item.value
                daily_stats[day]["prints"] += 1
                if print_item.is_premium:
                    daily_stats[day]["premium_count"] += 1

            # Calculate averages
            daily_volumes = [s["volume"] for s in daily_stats.values()]
            daily_values = [s["value"] for s in daily_stats.values()]

            avg_daily_volume = statistics.mean(daily_volumes) if daily_volumes else 0
            avg_daily_value = statistics.mean(daily_values) if daily_values else 0

            # Trend analysis
            recent_volume = sum(daily_volumes[-5:]) / 5 if len(daily_volumes) >= 5 else avg_daily_volume
            volume_trend = "increasing" if recent_volume > avg_daily_volume * 1.1 else \
                          "decreasing" if recent_volume < avg_daily_volume * 0.9 else "stable"

            return {
                "symbol": symbol,
                "period_days": days,
                "total_prints": len(period_prints),
                "total_volume": sum(p.size for p in period_prints),
                "total_value": sum(p.value for p in period_prints),
                "average_daily_volume": int(avg_daily_volume),
                "average_daily_value": round(avg_daily_value, 2),
                "volume_trend": volume_trend,
                "premium_percentage": round(
                    len([p for p in period_prints if p.is_premium]) / len(period_prints) * 100, 2
                ) if period_prints else 0,
                "daily_breakdown": dict(daily_stats)
            }

        except Exception as e:
            logger.error(f"Error analyzing historical patterns for {symbol}: {e}")
            return self._empty_patterns(symbol, days)

    async def calculate_dark_pool_ratio(
        self,
        symbol: str,
        total_volume: int,
        date: Optional[datetime] = None
    ) -> float:
        """
        Calculate dark pool volume ratio

        Args:
            symbol: Stock ticker symbol
            total_volume: Total market volume for the period
            date: Date to calculate for (defaults to today)

        Returns:
            Dark pool ratio (dark pool volume / total volume)
        """
        try:
            if not date:
                date = datetime.now()

            prints = await self.get_prints_for_date(symbol, date)
            dark_pool_volume = sum(p.size for p in prints)

            if total_volume == 0:
                return 0.0

            return dark_pool_volume / total_volume

        except Exception as e:
            logger.error(f"Error calculating dark pool ratio for {symbol}: {e}")
            return 0.0

    async def detect_unusual_activity(
        self,
        symbol: str,
        lookback_days: int = 30
    ) -> Dict[str, Any]:
        """
        Detect unusual dark pool activity

        Args:
            symbol: Stock ticker symbol
            lookback_days: Days to compare against

        Returns:
            Unusual activity metrics
        """
        try:
            # Get historical baseline
            patterns = await self.get_historical_patterns(symbol, lookback_days)
            avg_daily_volume = patterns.get("average_daily_volume", 0)
            avg_daily_value = patterns.get("average_daily_value", 0)

            # Get today's activity
            today_summary = await self.get_daily_summary(symbol)
            today_volume = today_summary.get("total_volume", 0)
            today_value = today_summary.get("total_value", 0)

            # Calculate ratios
            volume_ratio = today_volume / avg_daily_volume if avg_daily_volume > 0 else 0
            value_ratio = today_value / avg_daily_value if avg_daily_value > 0 else 0

            # Determine if unusual
            is_unusual = volume_ratio > 2.0 or value_ratio > 2.0

            return {
                "symbol": symbol,
                "is_unusual": is_unusual,
                "volume_ratio": round(volume_ratio, 2),
                "value_ratio": round(value_ratio, 2),
                "today_volume": today_volume,
                "average_volume": avg_daily_volume,
                "today_value": today_value,
                "average_value": avg_daily_value,
                "severity": "high" if volume_ratio > 3.0 else "medium" if volume_ratio > 2.0 else "low"
            }

        except Exception as e:
            logger.error(f"Error detecting unusual activity for {symbol}: {e}")
            return {"symbol": symbol, "is_unusual": False, "error": str(e)}

    async def add_print(self, print_data: DarkPoolPrint) -> None:
        """Add a new dark pool print (for simulation/testing)"""
        self._prints[print_data.symbol].append(print_data)

        # Keep only recent prints (last 30 days)
        cutoff = datetime.now() - timedelta(days=30)
        self._prints[print_data.symbol] = [
            p for p in self._prints[print_data.symbol]
            if p.timestamp >= cutoff
        ]

    def _empty_summary(self, symbol: str, date: datetime) -> Dict[str, Any]:
        """Return empty summary structure"""
        return {
            "symbol": symbol,
            "date": date.isoformat(),
            "total_prints": 0,
            "total_volume": 0,
            "total_value": 0,
            "average_price": 0,
            "average_size": 0,
            "premium_prints": 0,
            "discount_prints": 0,
            "premium_percentage": 0,
            "sentiment": {
                "bullish": 0,
                "bearish": 0,
                "neutral": 0,
                "bullish_percentage": 0
            },
            "large_blocks": {
                "count": 0,
                "value": 0,
                "percentage_of_value": 0
            }
        }

    def _empty_patterns(self, symbol: str, days: int) -> Dict[str, Any]:
        """Return empty patterns structure"""
        return {
            "symbol": symbol,
            "period_days": days,
            "total_prints": 0,
            "total_volume": 0,
            "total_value": 0,
            "average_daily_volume": 0,
            "average_daily_value": 0,
            "volume_trend": "stable",
            "premium_percentage": 0,
            "daily_breakdown": {}
        }

    async def generate_sample_data(self, symbol: str, days: int = 7) -> None:
        """Generate sample dark pool data for testing"""
        import random

        base_price = 150.0
        now = datetime.now()

        for day in range(days):
            date = now - timedelta(days=day)

            # Generate 20-50 prints per day
            num_prints = random.randint(20, 50)

            for _ in range(num_prints):
                # Random time during trading day
                hour = random.randint(9, 15)
                minute = random.randint(0, 59)
                timestamp = date.replace(hour=hour, minute=minute, second=0, microsecond=0)

                # Random price variation
                market_price = base_price + random.uniform(-5, 5)
                premium_discount = random.uniform(-2, 2)
                price = market_price * (1 + premium_discount / 100)

                # Random size
                size = random.randint(10000, 1000000)
                value = price * size

                # Determine sentiment
                if premium_discount > 0.5:
                    sentiment = Sentiment.BULLISH
                elif premium_discount < -0.5:
                    sentiment = Sentiment.BEARISH
                else:
                    sentiment = Sentiment.NEUTRAL

                print_data = DarkPoolPrint(
                    symbol=symbol,
                    timestamp=timestamp,
                    price=round(price, 2),
                    size=size,
                    value=round(value, 2),
                    exchange="DARK_POOL",
                    premium_discount=round(premium_discount, 2),
                    market_price=round(market_price, 2),
                    is_premium=premium_discount > 0,
                    sentiment=sentiment
                )

                await self.add_print(print_data)

        logger.info(f"Generated {days} days of sample data for {symbol}")


# Global instance
_dark_pool_service = None


def get_dark_pool_service() -> DarkPoolService:
    """Get or create dark pool service instance"""
    global _dark_pool_service
    if _dark_pool_service is None:
        _dark_pool_service = DarkPoolService()
    return _dark_pool_service
