"""
Alert Scheduler - Background task scheduler for monitoring alert rules
Uses APScheduler to continuously monitor and trigger alerts
"""
import logging
import asyncio
from typing import Optional
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session

from app.models import AlertRule, Ticker
from app.services.database import get_db
from app.services.market_data import market_data_service
from app.services.alert_rule_engine import AlertRuleEngine
from app.services.alert_delivery import AlertDeliveryService

logger = logging.getLogger(__name__)


class AlertScheduler:
    """Background scheduler for monitoring alert rules"""

    def __init__(self):
        self.scheduler: Optional[AsyncIOScheduler] = None
        self.is_running = False
        self.monitored_rules = set()

    def start(self):
        """Start the alert scheduler"""
        if self.is_running:
            logger.warning("Alert scheduler is already running")
            return

        try:
            self.scheduler = AsyncIOScheduler()

            # Add main monitoring job (runs every minute)
            self.scheduler.add_job(
                self._monitor_all_rules,
                trigger=IntervalTrigger(seconds=60),
                id="monitor_all_rules",
                name="Monitor all active alert rules",
                replace_existing=True
            )

            # Start scheduler
            self.scheduler.start()
            self.is_running = True

            logger.info("🚀 Alert scheduler started successfully")

        except Exception as e:
            logger.error(f"Error starting alert scheduler: {e}")
            raise

    def stop(self):
        """Stop the alert scheduler"""
        if not self.is_running or not self.scheduler:
            logger.warning("Alert scheduler is not running")
            return

        try:
            self.scheduler.shutdown(wait=True)
            self.is_running = False
            logger.info("⏹️ Alert scheduler stopped")

        except Exception as e:
            logger.error(f"Error stopping alert scheduler: {e}")

    async def _monitor_all_rules(self):
        """Monitor all active alert rules"""
        try:
            # Get database session
            db = next(get_db())

            try:
                # Get all enabled rules that are not snoozed
                rules = db.query(AlertRule).filter(
                    AlertRule.is_enabled == True,
                    AlertRule.is_snoozed == False
                ).all()

                logger.info(f"📊 Monitoring {len(rules)} active alert rules")

                # Process each rule
                for rule in rules:
                    try:
                        await self._check_rule(rule, db)
                    except Exception as e:
                        logger.error(f"Error checking rule {rule.id}: {e}")
                        continue

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Error in monitor_all_rules: {e}")

    async def _check_rule(self, rule: AlertRule, db: Session):
        """
        Check a single alert rule and trigger if conditions are met

        Args:
            rule: AlertRule to check
            db: Database session
        """
        try:
            # Get ticker if specified
            ticker = None
            if rule.ticker_id:
                ticker = db.query(Ticker).filter(Ticker.id == rule.ticker_id).first()
                if not ticker:
                    logger.warning(f"Ticker not found for rule {rule.id}")
                    return

            # Get market data
            market_data = await self._get_market_data_for_rule(rule, ticker, db)
            if not market_data:
                logger.debug(f"No market data for rule {rule.id}")
                return

            # Evaluate rule
            engine = AlertRuleEngine(db)
            triggered, context = await engine.evaluate_rule(rule, market_data)

            if triggered:
                logger.info(f"🚨 Alert rule triggered: {rule.name} (ID: {rule.id})")

                # Create alert log
                alert_log = await engine.trigger_alert(rule, context)

                # Deliver alert
                delivery_service = AlertDeliveryService(db)
                delivery_results = await delivery_service.deliver_alert(alert_log)

                logger.info(f"✅ Alert delivered: {rule.name} - Results: {delivery_results}")

            else:
                logger.debug(f"Rule {rule.id} not triggered. Reason: {context.get('reason', 'conditions not met')}")

        except Exception as e:
            logger.error(f"Error checking rule {rule.id} ({rule.name}): {e}")

    async def _get_market_data_for_rule(self, rule: AlertRule, ticker: Optional[Ticker], db: Session) -> Optional[dict]:
        """
        Get market data needed to evaluate a rule

        Args:
            rule: AlertRule to get data for
            ticker: Ticker object
            db: Database session

        Returns:
            Dictionary with market data and calculated indicators
        """
        try:
            if not ticker:
                return None

            # Get price data
            price_data = await market_data_service.get_time_series(
                ticker=ticker.symbol,
                interval="1day",
                outputsize=100
            )

            if not price_data or len(price_data) == 0:
                return None

            # Get current and previous data
            current = price_data[-1]
            previous = price_data[-2] if len(price_data) > 1 else current

            # Calculate basic indicators
            market_data = {
                "ticker": ticker.symbol,
                "close": current.get("close"),
                "open": current.get("open"),
                "high": current.get("high"),
                "low": current.get("low"),
                "volume": current.get("volume"),
                "previous_close": previous.get("close"),
                "previous_value": previous.get("close"),  # For cross detection
            }

            # Calculate additional fields based on alert type
            if rule.alert_type in ["indicator", "pattern"]:
                indicators = await self._calculate_indicators(price_data)
                market_data["indicators"] = indicators

            # Calculate volume metrics
            if len(price_data) >= 20:
                avg_volume = sum(d.get("volume", 0) for d in price_data[-20:]) / 20
                market_data["avg_volume"] = avg_volume

            return market_data

        except Exception as e:
            logger.error(f"Error getting market data for rule {rule.id}: {e}")
            return None

    async def _calculate_indicators(self, price_data: list) -> dict:
        """Calculate technical indicators from price data"""
        try:
            indicators = {}

            if len(price_data) < 20:
                return indicators

            # RSI
            indicators["rsi"] = await self._calculate_rsi(price_data)

            # MACD
            macd_data = await self._calculate_macd(price_data)
            indicators.update(macd_data)

            # Moving averages
            closes = [d["close"] for d in price_data]

            if len(closes) >= 20:
                indicators["sma_20"] = sum(closes[-20:]) / 20

            if len(closes) >= 50:
                indicators["sma_50"] = sum(closes[-50:]) / 50

            if len(closes) >= 200:
                indicators["sma_200"] = sum(closes[-200:]) / 200

            # EMA
            if len(closes) >= 20:
                indicators["ema_20"] = self._calculate_ema(closes, 20)

            if len(closes) >= 50:
                indicators["ema_50"] = self._calculate_ema(closes, 50)

            return indicators

        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return {}

    async def _calculate_rsi(self, price_data: list, period: int = 14) -> float:
        """Calculate RSI"""
        try:
            if len(price_data) < period + 1:
                return 50.0

            closes = [d["close"] for d in price_data[-period-1:]]

            gains = []
            losses = []

            for i in range(1, len(closes)):
                change = closes[i] - closes[i-1]
                if change > 0:
                    gains.append(change)
                    losses.append(0)
                else:
                    gains.append(0)
                    losses.append(abs(change))

            avg_gain = sum(gains) / period
            avg_loss = sum(losses) / period

            if avg_loss == 0:
                return 100.0

            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

            return rsi

        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return 50.0

    async def _calculate_macd(self, price_data: list) -> dict:
        """Calculate MACD"""
        try:
            if len(price_data) < 26:
                return {"macd": 0, "macd_signal": 0, "macd_histogram": 0}

            closes = [d["close"] for d in price_data]

            # Calculate EMAs
            ema_12 = self._calculate_ema(closes, 12)
            ema_26 = self._calculate_ema(closes, 26)

            macd_line = ema_12 - ema_26

            # Signal line (9-period EMA of MACD)
            # For simplicity, using approximation
            signal_line = macd_line * 0.9  # Simplified

            histogram = macd_line - signal_line

            return {
                "macd": macd_line,
                "macd_signal": signal_line,
                "macd_histogram": histogram
            }

        except Exception as e:
            logger.error(f"Error calculating MACD: {e}")
            return {"macd": 0, "macd_signal": 0, "macd_histogram": 0}

    def _calculate_ema(self, data: list, period: int) -> float:
        """Calculate Exponential Moving Average"""
        try:
            if len(data) < period:
                return sum(data) / len(data)

            multiplier = 2 / (period + 1)
            ema = sum(data[:period]) / period  # Initial SMA

            for price in data[period:]:
                ema = (price - ema) * multiplier + ema

            return ema

        except Exception as e:
            logger.error(f"Error calculating EMA: {e}")
            return 0.0

    def get_status(self) -> dict:
        """Get scheduler status"""
        return {
            "is_running": self.is_running,
            "jobs": len(self.scheduler.get_jobs()) if self.scheduler else 0,
            "next_run": self.scheduler.get_job("monitor_all_rules").next_run_time.isoformat() if self.scheduler and self.scheduler.get_job("monitor_all_rules") else None
        }


# Global scheduler instance
_scheduler: Optional[AlertScheduler] = None


def get_alert_scheduler() -> AlertScheduler:
    """Get or create alert scheduler singleton"""
    global _scheduler
    if _scheduler is None:
        _scheduler = AlertScheduler()
    return _scheduler


async def start_alert_scheduler():
    """Start the global alert scheduler"""
    scheduler = get_alert_scheduler()
    scheduler.start()


async def stop_alert_scheduler():
    """Stop the global alert scheduler"""
    scheduler = get_alert_scheduler()
    scheduler.stop()
