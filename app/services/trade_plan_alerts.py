"""
Smart Alerts Service for Trade Plans
Monitors active trade plans and sends alerts for:
- Entry zone hits
- Stop loss triggers
- Target achievement
- Pattern invalidation
"""
import logging
import asyncio
from typing import Optional, List, Dict, Any
from datetime import datetime
import httpx

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TradePlan, TradePlanAlert, Ticker
from app.services.market_data import market_data_service
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class TradePlanAlertService:
    """Service for monitoring trade plans and sending smart alerts"""

    def __init__(self):
        self.telegram_api_key = settings.telegram_bot_token
        self.telegram_chat_id = settings.telegram_chat_id
        self.check_interval = 300  # Check every 5 minutes

    async def monitor_active_plans(self, db: AsyncSession) -> Dict[str, Any]:
        """
        Monitor all active trade plans and trigger alerts

        Args:
            db: Database session

        Returns:
            Monitoring results with alerts triggered
        """
        try:
            # Get all active/planned trade plans
            result = await db.execute(
                select(TradePlan, Ticker)
                .join(Ticker, TradePlan.ticker_id == Ticker.id)
                .where(TradePlan.status.in_(["planned", "active"]))
            )

            plans = result.all()

            if not plans:
                logger.info("📋 No active trade plans to monitor")
                return {"success": True, "monitored": 0, "alerts_triggered": 0}

            alerts_triggered = []
            monitored_count = 0

            logger.info(f"📊 Monitoring {len(plans)} active trade plans...")

            for trade_plan, ticker in plans:
                try:
                    # Get current price
                    current_price = await self._get_current_price(ticker.symbol)

                    if current_price is None:
                        logger.warning(f"⚠️ Unable to get price for {ticker.symbol}")
                        continue

                    monitored_count += 1

                    # Check all alert conditions
                    triggered = await self._check_alerts(
                        db, trade_plan, ticker, current_price
                    )

                    alerts_triggered.extend(triggered)

                except Exception as e:
                    logger.warning(f"⚠️ Error monitoring {ticker.symbol}: {e}")
                    continue

            # Commit any alert updates
            await db.commit()

            logger.info(
                f"✅ Monitoring complete: {monitored_count} monitored, "
                f"{len(alerts_triggered)} alerts triggered"
            )

            return {
                "success": True,
                "monitored": monitored_count,
                "alerts_triggered": len(alerts_triggered),
                "alerts": alerts_triggered
            }

        except Exception as e:
            logger.error(f"❌ Monitoring error: {e}")
            return {"success": False, "error": str(e)}

    async def _get_current_price(self, ticker: str) -> Optional[float]:
        """Get current price for ticker"""
        try:
            quote = await market_data_service.get_quote(ticker)
            return quote.get("price") if quote else None
        except Exception as e:
            logger.warning(f"Error getting price for {ticker}: {e}")
            return None

    async def _check_alerts(
        self,
        db: AsyncSession,
        trade_plan: TradePlan,
        ticker: Ticker,
        current_price: float
    ) -> List[Dict[str, Any]]:
        """
        Check all alert conditions for a trade plan

        Returns:
            List of triggered alerts
        """
        triggered_alerts = []

        # 1. Check entry zone alert
        if trade_plan.status == "planned":
            if (trade_plan.entry_zone_low <= current_price <= trade_plan.entry_zone_high):
                alert = await self._trigger_alert(
                    db, trade_plan, ticker, current_price,
                    "entry_zone",
                    f"💰 {ticker.symbol} has entered the entry zone at ${current_price:.2f}"
                )
                if alert:
                    triggered_alerts.append(alert)

        # 2. Check stop loss alert
        if trade_plan.status == "active":
            if current_price <= trade_plan.initial_stop:
                alert = await self._trigger_alert(
                    db, trade_plan, ticker, current_price,
                    "stop_loss",
                    f"🛑 {ticker.symbol} hit stop loss at ${current_price:.2f}"
                )
                if alert:
                    triggered_alerts.append(alert)
                    # Update plan status
                    trade_plan.status = "completed"
                    trade_plan.outcome = "stopped"
                    trade_plan.exit_date = datetime.utcnow()
                    trade_plan.exit_price_actual = current_price

        # 3. Check target alerts
        if trade_plan.status == "active":
            # Best case target
            if current_price >= trade_plan.best_case_target:
                alert = await self._trigger_alert(
                    db, trade_plan, ticker, current_price,
                    "target_best",
                    f"🎯 {ticker.symbol} hit BEST CASE target at ${current_price:.2f}!"
                )
                if alert:
                    triggered_alerts.append(alert)

            # Base case target
            elif current_price >= trade_plan.base_case_target:
                alert = await self._trigger_alert(
                    db, trade_plan, ticker, current_price,
                    "target_base",
                    f"🎯 {ticker.symbol} hit BASE CASE target at ${current_price:.2f}"
                )
                if alert:
                    triggered_alerts.append(alert)

            # Worst case target
            elif trade_plan.worst_case_target and current_price >= trade_plan.worst_case_target:
                alert = await self._trigger_alert(
                    db, trade_plan, ticker, current_price,
                    "target_worst",
                    f"🎯 {ticker.symbol} hit WORST CASE target at ${current_price:.2f}"
                )
                if alert:
                    triggered_alerts.append(alert)

        # 4. Check pattern invalidation
        if current_price <= trade_plan.invalidation_price:
            alert = await self._trigger_alert(
                db, trade_plan, ticker, current_price,
                "invalidation",
                f"⚠️ {ticker.symbol} pattern INVALIDATED at ${current_price:.2f}"
            )
            if alert:
                triggered_alerts.append(alert)
                if trade_plan.status != "completed":
                    trade_plan.status = "cancelled"

        return triggered_alerts

    async def _trigger_alert(
        self,
        db: AsyncSession,
        trade_plan: TradePlan,
        ticker: Ticker,
        current_price: float,
        alert_type: str,
        message: str
    ) -> Optional[Dict[str, Any]]:
        """
        Trigger and send an alert

        Args:
            db: Database session
            trade_plan: TradePlan object
            ticker: Ticker object
            current_price: Current price that triggered alert
            alert_type: Type of alert
            message: Alert message

        Returns:
            Alert data if sent, None if already triggered
        """
        # Check if this alert was already triggered
        existing_alert = await db.execute(
            select(TradePlanAlert).where(
                and_(
                    TradePlanAlert.trade_plan_id == trade_plan.id,
                    TradePlanAlert.alert_type == alert_type,
                    TradePlanAlert.is_triggered == True
                )
            )
        )

        if existing_alert.scalar_one_or_none():
            return None  # Alert already triggered

        # Create alert record
        alert = TradePlanAlert(
            trade_plan_id=trade_plan.id,
            alert_type=alert_type,
            trigger_price=current_price,
            is_triggered=True,
            triggered_at=datetime.utcnow()
        )

        db.add(alert)

        # Send notification
        notification_sent = await self._send_notification(
            trade_plan, ticker, current_price, alert_type, message
        )

        if notification_sent:
            alert.notification_sent = True
            alert.notification_sent_at = datetime.utcnow()

        logger.info(f"🚨 Alert triggered: {message}")

        return {
            "ticker": ticker.symbol,
            "alert_type": alert_type,
            "price": current_price,
            "message": message,
            "sent": notification_sent
        }

    async def _send_notification(
        self,
        trade_plan: TradePlan,
        ticker: Ticker,
        current_price: float,
        alert_type: str,
        message: str
    ) -> bool:
        """
        Send notification via configured channels

        Args:
            trade_plan: TradePlan object
            ticker: Ticker object
            current_price: Current price
            alert_type: Type of alert
            message: Alert message

        Returns:
            True if sent successfully
        """
        try:
            # Build detailed message
            detailed_message = self._format_alert_message(
                trade_plan, ticker, current_price, alert_type, message
            )

            # Send to Telegram
            if self.telegram_api_key and self.telegram_chat_id:
                await self._send_telegram(detailed_message, ticker.symbol)
                return True

            return False

        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            return False

    def _format_alert_message(
        self,
        trade_plan: TradePlan,
        ticker: Ticker,
        current_price: float,
        alert_type: str,
        message: str
    ) -> str:
        """Format detailed alert message"""

        # Emoji for alert type
        emoji_map = {
            "entry_zone": "💰",
            "stop_loss": "🛑",
            "target_best": "🎯🎯🎯",
            "target_base": "🎯🎯",
            "target_worst": "🎯",
            "invalidation": "⚠️"
        }

        emoji = emoji_map.get(alert_type, "🔔")

        msg = f"""
{emoji} TRADE PLAN ALERT
{'='*30}

{message}

📊 Plan Details:
  Pattern: {trade_plan.pattern_type} ({trade_plan.pattern_score:.1f}/10)
  Entry Zone: ${trade_plan.entry_zone_low:.2f} - ${trade_plan.entry_zone_high:.2f}
  Stop Loss: ${trade_plan.initial_stop:.2f}
  Targets: ${trade_plan.worst_case_target:.2f} / ${trade_plan.base_case_target:.2f} / ${trade_plan.best_case_target:.2f}

📈 Position:
  Size: {trade_plan.position_size} shares
  Risk: ${trade_plan.risk_amount:.2f}

⏰ Alert Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""

        # Add action items based on alert type
        if alert_type == "entry_zone":
            msg += "\n✅ ACTION: Review plan and consider staged entry"
        elif alert_type == "stop_loss":
            msg += "\n🛑 ACTION: Exit position immediately"
        elif "target" in alert_type:
            msg += "\n✅ ACTION: Consider taking profits or trailing stop"
        elif alert_type == "invalidation":
            msg += "\n⚠️ ACTION: Cancel or re-evaluate plan"

        return msg

    async def _send_telegram(self, message: str, ticker: str) -> None:
        """Send alert via Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_api_key}/sendMessage"

            # Create inline keyboard
            keyboard = {
                "inline_keyboard": [[
                    {"text": "📊 View Chart", "url": f"https://www.tradingview.com/chart/?symbol={ticker}"},
                ]]
            }

            payload = {
                "chat_id": self.telegram_chat_id,
                "text": message,
                "parse_mode": "Markdown",
                "reply_markup": keyboard
            }

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                logger.info(f"✉️ Telegram alert sent for {ticker}")

        except Exception as e:
            logger.error(f"Telegram send failed: {e}")
            raise

    async def create_alerts_for_plan(
        self,
        db: AsyncSession,
        trade_plan_id: int
    ) -> List[TradePlanAlert]:
        """
        Create alert records for a new trade plan

        Args:
            db: Database session
            trade_plan_id: Trade plan ID

        Returns:
            List of created alert records
        """
        # Get trade plan
        result = await db.execute(
            select(TradePlan).where(TradePlan.id == trade_plan_id)
        )
        trade_plan = result.scalar_one_or_none()

        if not trade_plan:
            raise ValueError(f"Trade plan {trade_plan_id} not found")

        alerts = []

        # Entry zone alert
        if trade_plan.status == "planned":
            alerts.append(TradePlanAlert(
                trade_plan_id=trade_plan_id,
                alert_type="entry_zone",
                trigger_price=trade_plan.entry_zone_low,
                is_triggered=False
            ))

        # Stop loss alert
        alerts.append(TradePlanAlert(
            trade_plan_id=trade_plan_id,
            alert_type="stop_loss",
            trigger_price=trade_plan.initial_stop,
            is_triggered=False
        ))

        # Target alerts
        alerts.append(TradePlanAlert(
            trade_plan_id=trade_plan_id,
            alert_type="target_worst",
            trigger_price=trade_plan.worst_case_target,
            is_triggered=False
        ))

        alerts.append(TradePlanAlert(
            trade_plan_id=trade_plan_id,
            alert_type="target_base",
            trigger_price=trade_plan.base_case_target,
            is_triggered=False
        ))

        alerts.append(TradePlanAlert(
            trade_plan_id=trade_plan_id,
            alert_type="target_best",
            trigger_price=trade_plan.best_case_target,
            is_triggered=False
        ))

        # Invalidation alert
        alerts.append(TradePlanAlert(
            trade_plan_id=trade_plan_id,
            alert_type="invalidation",
            trigger_price=trade_plan.invalidation_price,
            is_triggered=False
        ))

        # Add to database
        for alert in alerts:
            db.add(alert)

        await db.commit()

        logger.info(f"✅ Created {len(alerts)} alerts for trade plan {trade_plan_id}")
        return alerts


# Global instance
_alert_service: Optional[TradePlanAlertService] = None


def get_trade_plan_alert_service() -> TradePlanAlertService:
    """Get or create trade plan alert service singleton"""
    global _alert_service
    if _alert_service is None:
        _alert_service = TradePlanAlertService()
    return _alert_service
