"""
Block Trade Alerts Service

Monitors and alerts on large block trades:
- Large volume spikes
- Unusual options sweeps
- Options positioning analysis
- Smart money divergence detection
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import logging
from collections import defaultdict
import statistics

from .models import BlockTrade, TradeType, Sentiment, SmartMoneyAlert

logger = logging.getLogger(__name__)


class BlockTradeService:
    """Service for tracking block trades and unusual activity"""

    def __init__(self):
        # In-memory storage (replace with database in production)
        self._trades: Dict[str, List[BlockTrade]] = defaultdict(list)
        self._alerts: Dict[str, List[SmartMoneyAlert]] = defaultdict(list)
        self._volume_baselines: Dict[str, float] = {}

    async def get_recent_blocks(
        self,
        symbol: str,
        hours: int = 24,
        min_value: Optional[float] = None,
        trade_type: Optional[TradeType] = None
    ) -> List[BlockTrade]:
        """
        Get recent block trades

        Args:
            symbol: Stock ticker symbol
            hours: Number of hours to look back
            min_value: Minimum dollar value filter
            trade_type: Filter by trade type

        Returns:
            List of block trades
        """
        try:
            trades = self._trades.get(symbol, [])

            # Filter by time
            cutoff = datetime.now() - timedelta(hours=hours)
            filtered = [t for t in trades if t.timestamp >= cutoff]

            # Apply filters
            if min_value:
                filtered = [t for t in filtered if t.value >= min_value]

            if trade_type:
                filtered = [t for t in filtered if t.trade_type == trade_type]

            # Sort by timestamp descending
            filtered.sort(key=lambda x: x.timestamp, reverse=True)

            return filtered

        except Exception as e:
            logger.error(f"Error getting recent blocks for {symbol}: {e}")
            return []

    async def get_unusual_options_activity(
        self,
        symbol: str,
        hours: int = 24,
        min_premium: Optional[float] = None
    ) -> List[BlockTrade]:
        """
        Get unusual options activity

        Args:
            symbol: Stock ticker symbol
            hours: Number of hours to look back
            min_premium: Minimum premium filter

        Returns:
            List of unusual options trades
        """
        try:
            trades = await self.get_recent_blocks(symbol, hours)

            # Filter for options only
            options_trades = [t for t in trades if t.is_options]

            # Filter by premium if specified
            if min_premium:
                options_trades = [t for t in options_trades if t.premium and t.premium >= min_premium]

            # Filter for unusual activity (sweeps with high volume ratio)
            unusual = [
                t for t in options_trades
                if t.trade_type == TradeType.SWEEP and t.volume_ratio >= 2.0
            ]

            return unusual

        except Exception as e:
            logger.error(f"Error getting unusual options activity for {symbol}: {e}")
            return []

    async def detect_volume_spikes(
        self,
        symbol: str,
        current_volume: int,
        threshold: float = 2.0
    ) -> Dict[str, Any]:
        """
        Detect unusual volume spikes

        Args:
            symbol: Stock ticker symbol
            current_volume: Current volume to compare
            threshold: Multiple of average volume to trigger alert

        Returns:
            Volume spike analysis
        """
        try:
            # Get or calculate baseline average volume
            baseline = await self._get_volume_baseline(symbol)

            if baseline == 0:
                return {
                    "symbol": symbol,
                    "is_spike": False,
                    "current_volume": current_volume,
                    "baseline_volume": 0,
                    "volume_ratio": 0,
                    "message": "Insufficient baseline data"
                }

            # Calculate ratio
            volume_ratio = current_volume / baseline

            # Determine if spike
            is_spike = volume_ratio >= threshold

            # Severity
            if volume_ratio >= 5.0:
                severity = "extreme"
            elif volume_ratio >= 3.0:
                severity = "high"
            elif volume_ratio >= threshold:
                severity = "medium"
            else:
                severity = "low"

            return {
                "symbol": symbol,
                "is_spike": is_spike,
                "current_volume": current_volume,
                "baseline_volume": int(baseline),
                "volume_ratio": round(volume_ratio, 2),
                "severity": severity,
                "message": f"Volume is {volume_ratio:.1f}x average" if is_spike else "Normal volume"
            }

        except Exception as e:
            logger.error(f"Error detecting volume spike for {symbol}: {e}")
            return {"symbol": symbol, "is_spike": False, "error": str(e)}

    async def analyze_options_positioning(
        self,
        symbol: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """
        Analyze smart money options positioning

        Args:
            symbol: Stock ticker symbol
            days: Number of days to analyze

        Returns:
            Options positioning analysis
        """
        try:
            cutoff = datetime.now() - timedelta(days=days)
            trades = self._trades.get(symbol, [])

            # Filter for options in timeframe
            options = [
                t for t in trades
                if t.is_options and t.timestamp >= cutoff
            ]

            if not options:
                return self._empty_options_positioning(symbol, days)

            # Separate calls and puts
            calls = [t for t in options if t.call_put == "CALL"]
            puts = [t for t in options if t.call_put == "PUT"]

            # Calculate metrics
            total_call_premium = sum(t.premium for t in calls if t.premium)
            total_put_premium = sum(t.premium for t in puts if t.premium)
            total_premium = total_call_premium + total_put_premium

            call_put_ratio = total_call_premium / total_put_premium if total_put_premium > 0 else float('inf')

            # Determine sentiment
            if call_put_ratio > 2.0:
                sentiment = "strongly_bullish"
            elif call_put_ratio > 1.2:
                sentiment = "bullish"
            elif call_put_ratio < 0.5:
                sentiment = "strongly_bearish"
            elif call_put_ratio < 0.8:
                sentiment = "bearish"
            else:
                sentiment = "neutral"

            # Sweeps analysis
            call_sweeps = [t for t in calls if t.trade_type == TradeType.SWEEP]
            put_sweeps = [t for t in puts if t.trade_type == TradeType.SWEEP]

            return {
                "symbol": symbol,
                "period_days": days,
                "total_options_trades": len(options),
                "call_trades": len(calls),
                "put_trades": len(puts),
                "total_call_premium": round(total_call_premium, 2),
                "total_put_premium": round(total_put_premium, 2),
                "total_premium": round(total_premium, 2),
                "call_put_ratio": round(call_put_ratio, 2) if call_put_ratio != float('inf') else "inf",
                "sentiment": sentiment,
                "call_sweeps": len(call_sweeps),
                "put_sweeps": len(put_sweeps),
                "sweep_sentiment": "bullish" if len(call_sweeps) > len(put_sweeps) else
                                  "bearish" if len(put_sweeps) > len(call_sweeps) else "neutral"
            }

        except Exception as e:
            logger.error(f"Error analyzing options positioning for {symbol}: {e}")
            return self._empty_options_positioning(symbol, days)

    async def detect_smart_money_divergence(
        self,
        symbol: str,
        price_change: float,
        days: int = 5
    ) -> Dict[str, Any]:
        """
        Detect divergence between price and smart money flow

        Args:
            symbol: Stock ticker symbol
            price_change: Percentage price change over period
            days: Number of days to analyze

        Returns:
            Divergence analysis
        """
        try:
            cutoff = datetime.now() - timedelta(days=days)
            trades = self._trades.get(symbol, [])

            # Get trades in period
            period_trades = [t for t in trades if t.timestamp >= cutoff]

            if not period_trades:
                return {
                    "symbol": symbol,
                    "has_divergence": False,
                    "message": "Insufficient trade data"
                }

            # Calculate smart money flow
            bullish_value = sum(t.value for t in period_trades if t.sentiment == Sentiment.BULLISH)
            bearish_value = sum(t.value for t in period_trades if t.sentiment == Sentiment.BEARISH)
            net_flow = bullish_value - bearish_value
            total_flow = bullish_value + bearish_value

            # Calculate flow percentage
            flow_percentage = (net_flow / total_flow * 100) if total_flow > 0 else 0

            # Detect divergence
            # Bullish divergence: Price down but smart money buying
            # Bearish divergence: Price up but smart money selling
            divergence_threshold = 10  # 10% difference

            has_divergence = False
            divergence_type = None

            if price_change < -5 and flow_percentage > divergence_threshold:
                has_divergence = True
                divergence_type = "bullish"
                message = "Price declining but smart money accumulating (bullish divergence)"
            elif price_change > 5 and flow_percentage < -divergence_threshold:
                has_divergence = True
                divergence_type = "bearish"
                message = "Price rising but smart money distributing (bearish divergence)"
            else:
                message = "Price and smart money flow aligned"

            return {
                "symbol": symbol,
                "has_divergence": has_divergence,
                "divergence_type": divergence_type,
                "price_change": round(price_change, 2),
                "smart_money_flow": round(flow_percentage, 2),
                "bullish_flow": round(bullish_value, 2),
                "bearish_flow": round(bearish_value, 2),
                "net_flow": round(net_flow, 2),
                "message": message
            }

        except Exception as e:
            logger.error(f"Error detecting divergence for {symbol}: {e}")
            return {"symbol": symbol, "has_divergence": False, "error": str(e)}

    async def get_alerts(
        self,
        symbol: str,
        hours: int = 24,
        severity: Optional[str] = None
    ) -> List[SmartMoneyAlert]:
        """
        Get smart money alerts

        Args:
            symbol: Stock ticker symbol
            hours: Number of hours to look back
            severity: Filter by severity level

        Returns:
            List of alerts
        """
        try:
            alerts = self._alerts.get(symbol, [])

            # Filter by time
            cutoff = datetime.now() - timedelta(hours=hours)
            filtered = [a for a in alerts if a.timestamp >= cutoff]

            # Filter by severity
            if severity:
                filtered = [a for a in filtered if a.severity == severity]

            # Sort by timestamp descending
            filtered.sort(key=lambda x: x.timestamp, reverse=True)

            return filtered

        except Exception as e:
            logger.error(f"Error getting alerts for {symbol}: {e}")
            return []

    async def create_alert(
        self,
        symbol: str,
        alert_type: str,
        severity: str,
        title: str,
        message: str,
        data: Dict[str, Any],
        sentiment: Sentiment
    ) -> SmartMoneyAlert:
        """Create and store a new alert"""
        alert = SmartMoneyAlert(
            symbol=symbol,
            timestamp=datetime.now(),
            alert_type=alert_type,
            severity=severity,
            title=title,
            message=message,
            data=data,
            sentiment=sentiment
        )

        self._alerts[symbol].append(alert)

        # Keep only recent alerts (last 7 days)
        cutoff = datetime.now() - timedelta(days=7)
        self._alerts[symbol] = [
            a for a in self._alerts[symbol]
            if a.timestamp >= cutoff
        ]

        return alert

    async def add_trade(self, trade: BlockTrade) -> None:
        """Add a new block trade"""
        self._trades[trade.symbol].append(trade)

        # Keep only recent trades (last 30 days)
        cutoff = datetime.now() - timedelta(days=30)
        self._trades[trade.symbol] = [
            t for t in self._trades[trade.symbol]
            if t.timestamp >= cutoff
        ]

        # Check for alert conditions
        await self._check_alert_conditions(trade)

    async def _check_alert_conditions(self, trade: BlockTrade) -> None:
        """Check if trade triggers any alerts"""
        try:
            # Large block alert (>$10M)
            if trade.value >= 10_000_000:
                await self.create_alert(
                    symbol=trade.symbol,
                    alert_type="large_block",
                    severity="high",
                    title=f"Large Block Trade: ${trade.value/1_000_000:.1f}M",
                    message=f"{trade.trade_type.value.upper()} block of {trade.size:,} shares at ${trade.price:.2f}",
                    data={
                        "value": trade.value,
                        "size": trade.size,
                        "price": trade.price,
                        "trade_type": trade.trade_type.value
                    },
                    sentiment=trade.sentiment
                )

            # Unusual options sweep
            if trade.is_options and trade.trade_type == TradeType.SWEEP and trade.volume_ratio >= 3.0:
                await self.create_alert(
                    symbol=trade.symbol,
                    alert_type="unusual_options",
                    severity="high",
                    title=f"Unusual Options Sweep Detected",
                    message=f"{trade.call_put} sweep with {trade.volume_ratio:.1f}x normal volume",
                    data={
                        "strike": trade.strike,
                        "expiration": trade.expiration.isoformat() if trade.expiration else None,
                        "call_put": trade.call_put,
                        "premium": trade.premium,
                        "volume_ratio": trade.volume_ratio
                    },
                    sentiment=trade.sentiment
                )

        except Exception as e:
            logger.error(f"Error checking alert conditions: {e}")

    async def _get_volume_baseline(self, symbol: str) -> float:
        """Get or calculate volume baseline"""
        # Check cache
        if symbol in self._volume_baselines:
            return self._volume_baselines[symbol]

        # Calculate from historical trades
        trades = self._trades.get(symbol, [])
        if not trades:
            return 0.0

        # Get last 20 days
        cutoff = datetime.now() - timedelta(days=20)
        recent = [t for t in trades if t.timestamp >= cutoff]

        if not recent:
            return 0.0

        # Calculate average daily volume
        daily_volumes = defaultdict(int)
        for trade in recent:
            day = trade.timestamp.date().isoformat()
            daily_volumes[day] += trade.size

        if not daily_volumes:
            return 0.0

        baseline = statistics.mean(daily_volumes.values())
        self._volume_baselines[symbol] = baseline

        return baseline

    def _empty_options_positioning(self, symbol: str, days: int) -> Dict[str, Any]:
        """Return empty options positioning structure"""
        return {
            "symbol": symbol,
            "period_days": days,
            "total_options_trades": 0,
            "call_trades": 0,
            "put_trades": 0,
            "total_call_premium": 0,
            "total_put_premium": 0,
            "total_premium": 0,
            "call_put_ratio": 0,
            "sentiment": "neutral",
            "call_sweeps": 0,
            "put_sweeps": 0,
            "sweep_sentiment": "neutral"
        }

    async def generate_sample_data(self, symbol: str, days: int = 7) -> None:
        """Generate sample block trade data for testing"""
        import random

        base_price = 178.50
        now = datetime.now()

        for day in range(days):
            date = now - timedelta(days=day)

            # Generate 10-30 block trades per day
            num_trades = random.randint(10, 30)

            for _ in range(num_trades):
                # Random time during trading day
                hour = random.randint(9, 15)
                minute = random.randint(0, 59)
                timestamp = date.replace(hour=hour, minute=minute, second=0, microsecond=0)

                # Determine if options trade
                is_options = random.random() < 0.4

                if is_options:
                    # Options trade
                    call_put = random.choice(["CALL", "PUT"])
                    strike = base_price + random.choice([-10, -5, 0, 5, 10])
                    exp_days = random.choice([7, 14, 30, 60])
                    expiration = timestamp + timedelta(days=exp_days)
                    size = random.randint(100, 1000)
                    premium = random.uniform(1.0, 10.0)
                    value = size * premium * 100  # Options contract multiplier

                    trade = BlockTrade(
                        symbol=symbol,
                        timestamp=timestamp,
                        trade_type=random.choice([TradeType.SWEEP, TradeType.BLOCK]),
                        price=base_price,
                        size=size,
                        value=round(value, 2),
                        is_options=True,
                        strike=strike,
                        expiration=expiration,
                        call_put=call_put,
                        sentiment=Sentiment.BULLISH if call_put == "CALL" else Sentiment.BEARISH,
                        premium=round(premium, 2),
                        volume_ratio=random.uniform(1.0, 5.0)
                    )
                else:
                    # Stock block trade
                    size = random.randint(50000, 500000)
                    price = base_price + random.uniform(-2, 2)
                    value = size * price

                    trade = BlockTrade(
                        symbol=symbol,
                        timestamp=timestamp,
                        trade_type=random.choice([TradeType.BLOCK, TradeType.SPLIT]),
                        price=round(price, 2),
                        size=size,
                        value=round(value, 2),
                        is_options=False,
                        sentiment=random.choice([Sentiment.BULLISH, Sentiment.BEARISH, Sentiment.NEUTRAL]),
                        volume_ratio=random.uniform(1.5, 4.0)
                    )

                await self.add_trade(trade)

        logger.info(f"Generated {days} days of sample block trade data for {symbol}")


# Global instance
_block_trade_service = None


def get_block_trade_service() -> BlockTradeService:
    """Get or create block trade service instance"""
    global _block_trade_service
    if _block_trade_service is None:
        _block_trade_service = BlockTradeService()
    return _block_trade_service
