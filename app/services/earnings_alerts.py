"""
Earnings alerts service
Monitors earnings calendar and sends alerts for watchlist stocks
"""
import asyncio
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import httpx

from app.config import get_settings
from app.services.cache import get_cache_service
from app.services.earnings import get_earnings_service
from app.services.market_data import market_data_service

logger = logging.getLogger(__name__)
settings = get_settings()


class EarningsAlertService:
    """Service for earnings-related alerts"""

    def __init__(self):
        self.earnings_service = get_earnings_service()
        self.cache = get_cache_service()
        self.telegram_api_key = settings.telegram_bot_token
        self.telegram_chat_id = settings.telegram_chat_id
        self.sendgrid_api_key = settings.sendgrid_api_key
        self.alert_email = settings.alert_email
        self.last_alerted = {}  # Track last alert time per ticker to avoid spam

    async def monitor_watchlist_earnings(self) -> Dict[str, Any]:
        """
        Monitor watchlist for upcoming earnings and send alerts

        Checks for:
        - Upcoming earnings (configurable days ahead)
        - Earnings surprises (after earnings are reported)
        - Price gaps on earnings day
        - Volume spikes on earnings day
        - Post-earnings pattern formations
        """
        try:
            from app.api.watchlist import watchlist_service

            # Get watchlist
            watchlist_items = await watchlist_service.get_watchlist()

            if not watchlist_items:
                logger.info("📋 Watchlist is empty, nothing to monitor")
                return {"success": True, "monitored": 0, "alerts_sent": 0}

            alerts_sent = []
            monitored_count = 0

            logger.info(f"📊 Monitoring {len(watchlist_items)} stocks for earnings...")

            for item in watchlist_items:
                ticker = item.get("ticker", "").upper()

                try:
                    # Check for upcoming earnings
                    upcoming_alert = await self._check_upcoming_earnings(ticker)
                    if upcoming_alert:
                        await self._send_alert(upcoming_alert)
                        alerts_sent.append(upcoming_alert)

                    # Check for recent earnings surprises
                    surprise_alert = await self._check_earnings_surprise(ticker)
                    if surprise_alert:
                        await self._send_alert(surprise_alert)
                        alerts_sent.append(surprise_alert)

                    # Check for post-earnings patterns
                    pattern_alert = await self._check_post_earnings_pattern(ticker)
                    if pattern_alert:
                        await self._send_alert(pattern_alert)
                        alerts_sent.append(pattern_alert)

                    monitored_count += 1

                except Exception as e:
                    logger.warning(f"⚠️ Error monitoring {ticker} earnings: {e}")
                    continue

            logger.info(f"✅ Earnings monitoring complete: {monitored_count} monitored, {len(alerts_sent)} alerts sent")

            return {
                "success": True,
                "monitored": monitored_count,
                "alerts_sent": len(alerts_sent),
                "alerts": alerts_sent
            }

        except Exception as e:
            logger.error(f"❌ Earnings monitoring error: {e}")
            return {"success": False, "error": str(e)}

    async def _check_upcoming_earnings(
        self,
        ticker: str,
        days_ahead: int = 7
    ) -> Optional[Dict[str, Any]]:
        """Check if ticker has earnings coming up in next N days"""

        # Check cooldown
        alert_key = f"earnings_upcoming:{ticker}"
        if await self._is_on_cooldown(alert_key, hours=24):
            return None

        # Get earnings calendar
        start = datetime.now()
        end = start + timedelta(days=days_ahead)

        calendar = await self.earnings_service.get_earnings_calendar(
            start_date=start,
            end_date=end,
            ticker=ticker
        )

        if not calendar:
            return None

        # Find the next earnings event
        next_earnings = calendar[0]
        earnings_date = next_earnings.get("earnings_date")

        if not earnings_date:
            return None

        days_until = (earnings_date - datetime.now()).days

        # Only alert if within the specified window
        if 0 <= days_until <= days_ahead:
            # Get historical performance
            historical = await self.earnings_service.get_historical_beat_miss(ticker, limit=8)

            # Mark as alerted
            await self._mark_alerted(alert_key)

            return {
                "type": "upcoming_earnings",
                "ticker": ticker,
                "earnings_date": earnings_date.strftime("%Y-%m-%d"),
                "days_until": days_until,
                "report_time": next_earnings.get("report_time", "TNS"),
                "eps_estimate": next_earnings.get("eps_estimate"),
                "revenue_estimate": next_earnings.get("revenue_estimate"),
                "beat_rate": historical.get("beat_rate", 0),
                "avg_surprise_pct": historical.get("avg_surprise_pct", 0)
            }

        return None

    async def _check_earnings_surprise(
        self,
        ticker: str,
        surprise_threshold: float = 5.0
    ) -> Optional[Dict[str, Any]]:
        """Check for significant earnings surprise in last 24 hours"""

        # Check cooldown
        alert_key = f"earnings_surprise:{ticker}"
        if await self._is_on_cooldown(alert_key, hours=24):
            return None

        # Get recent earnings (last 30 days)
        start = datetime.now() - timedelta(days=30)
        end = datetime.now()

        calendar = await self.earnings_service.get_earnings_calendar(
            start_date=start,
            end_date=end,
            ticker=ticker
        )

        if not calendar:
            return None

        # Check most recent earnings
        for event in calendar:
            eps_actual = event.get("eps_actual")
            eps_estimate = event.get("eps_estimate")
            earnings_date = event.get("earnings_date")

            if not eps_actual or not eps_estimate or not earnings_date:
                continue

            # Check if earnings were in last 24 hours
            hours_since = (datetime.now() - earnings_date).total_seconds() / 3600
            if hours_since > 24:
                continue

            # Calculate surprise
            surprise_pct = ((eps_actual - eps_estimate) / abs(eps_estimate)) * 100

            # Alert if significant surprise
            if abs(surprise_pct) >= surprise_threshold:
                # Get price reaction
                reaction = await self.earnings_service.analyze_earnings_reaction(
                    ticker, earnings_date, eps_actual, eps_estimate
                )

                # Mark as alerted
                await self._mark_alerted(alert_key)

                return {
                    "type": "earnings_surprise",
                    "ticker": ticker,
                    "earnings_date": earnings_date.strftime("%Y-%m-%d"),
                    "eps_actual": eps_actual,
                    "eps_estimate": eps_estimate,
                    "surprise_pct": surprise_pct,
                    "beat_or_miss": "beat" if surprise_pct > 0 else "miss",
                    "gap_pct": reaction.get("gap_percent"),
                    "day_move_pct": reaction.get("day_move_percent"),
                    "volume_ratio": reaction.get("volume_ratio")
                }

        return None

    async def _check_post_earnings_pattern(
        self,
        ticker: str
    ) -> Optional[Dict[str, Any]]:
        """Check for pattern formation after recent earnings"""

        # Check cooldown
        alert_key = f"earnings_pattern:{ticker}"
        if await self._is_on_cooldown(alert_key, hours=48):
            return None

        # Get earnings in last 10 days
        start = datetime.now() - timedelta(days=10)
        end = datetime.now()

        calendar = await self.earnings_service.get_earnings_calendar(
            start_date=start,
            end_date=end,
            ticker=ticker
        )

        if not calendar:
            return None

        # Check if we had earnings in last 10 days
        recent_earnings = None
        for event in calendar:
            earnings_date = event.get("earnings_date")
            if earnings_date:
                days_since = (datetime.now() - earnings_date).days
                if 1 <= days_since <= 10:
                    recent_earnings = event
                    break

        if not recent_earnings:
            return None

        # Check for pattern formation
        try:
            from app.core.pattern_detector import PatternDetector

            detector = PatternDetector()

            # Get price data
            price_data = await market_data_service.get_time_series(
                ticker=ticker,
                interval="1day",
                outputsize=500
            )

            if not price_data:
                return None

            # Analyze for patterns
            spy_data = await market_data_service.get_time_series("SPY", "1day", 500)
            pattern_result = await detector.analyze_ticker(ticker, price_data, spy_data)

            # If strong pattern found (confidence >= 75%)
            if pattern_result and pattern_result.score >= 0.75:
                # Mark as alerted
                await self._mark_alerted(alert_key)

                return {
                    "type": "post_earnings_pattern",
                    "ticker": ticker,
                    "earnings_date": recent_earnings.get("earnings_date").strftime("%Y-%m-%d"),
                    "days_since_earnings": (datetime.now() - recent_earnings.get("earnings_date")).days,
                    "pattern": pattern_result.pattern,
                    "confidence": pattern_result.score,
                    "entry": pattern_result.entry,
                    "stop": pattern_result.stop,
                    "target": pattern_result.target,
                    "risk_reward": pattern_result.risk_reward
                }

        except Exception as e:
            logger.warning(f"Error checking post-earnings pattern for {ticker}: {e}")

        return None

    async def _is_on_cooldown(self, alert_key: str, hours: int = 24) -> bool:
        """Check if alert is on cooldown"""
        last_alert = await self.cache.get(f"alert_cooldown:{alert_key}")
        if last_alert:
            return True
        return False

    async def _mark_alerted(self, alert_key: str, hours: int = 24):
        """Mark alert as sent with cooldown"""
        await self.cache.set(
            f"alert_cooldown:{alert_key}",
            datetime.now().isoformat(),
            ttl=hours * 3600
        )

    async def _send_alert(self, alert_data: Dict[str, Any]) -> None:
        """Send earnings alert via Telegram and Email"""

        message = self._format_alert_message(alert_data)

        # Send to Telegram
        if self.telegram_api_key and self.telegram_chat_id:
            try:
                await self._send_telegram_alert(message, alert_data)
                logger.info(f"✉️ Telegram earnings alert sent for {alert_data['ticker']}")
            except Exception as e:
                logger.warning(f"⚠️ Telegram alert failed: {e}")

        # Send to Email
        if self.sendgrid_api_key and self.alert_email:
            try:
                await self._send_email_alert(message, alert_data)
                logger.info(f"📧 Email earnings alert sent for {alert_data['ticker']}")
            except Exception as e:
                logger.warning(f"⚠️ Email alert failed: {e}")

    def _format_alert_message(self, alert: Dict[str, Any]) -> str:
        """Format earnings alert message"""

        alert_type = alert.get("type")
        ticker = alert.get("ticker")

        if alert_type == "upcoming_earnings":
            msg = f"""
📅 UPCOMING EARNINGS ALERT
========================

📊 Stock: {ticker}
🗓️ Earnings Date: {alert['earnings_date']}
⏰ Report Time: {alert['report_time']}
⏳ Days Until: {alert['days_until']}

📈 Consensus Estimates:
  EPS: ${alert.get('eps_estimate', 'N/A')}
  Revenue: ${alert.get('revenue_estimate', 'N/A')}M

📊 Historical Performance:
  Beat Rate: {alert['beat_rate']:.1%}
  Avg Surprise: {alert['avg_surprise_pct']:.1f}%

💡 Prepare for potential volatility around earnings!
"""

        elif alert_type == "earnings_surprise":
            beat_miss = alert.get('beat_or_miss')
            emoji = "🎯" if beat_miss == "beat" else "❌"

            msg = f"""
{emoji} EARNINGS SURPRISE ALERT
==========================

📊 Stock: {ticker}
🗓️ Reported: {alert['earnings_date']}
{'🎉' if beat_miss == 'beat' else '😞'} Result: {beat_miss.upper()}

📈 Results:
  EPS Actual: ${alert['eps_actual']:.2f}
  EPS Estimate: ${alert['eps_estimate']:.2f}
  Surprise: {alert['surprise_pct']:+.1f}%

💹 Price Reaction:
  Gap: {alert.get('gap_pct', 0):+.2f}%
  Day Move: {alert.get('day_move_pct', 0):+.2f}%
  Volume: {alert.get('volume_ratio', 1):.1f}x average

🎯 Monitor for follow-through!
"""

        elif alert_type == "post_earnings_pattern":
            msg = f"""
🎯 POST-EARNINGS PATTERN ALERT
==============================

📊 Stock: {ticker}
🗓️ Earnings Date: {alert['earnings_date']}
📅 Days Since: {alert['days_since_earnings']}

🎨 Pattern Detected:
  Type: {alert['pattern']}
  Confidence: {alert['confidence']:.1%}

📍 Trade Setup:
  Entry: ${alert['entry']:.2f}
  Stop: ${alert['stop']:.2f}
  Target: ${alert['target']:.2f}
  R:R Ratio: {alert['risk_reward']:.2f}:1

✅ Post-earnings consolidation may offer entry opportunity!
"""

        else:
            msg = f"Unknown earnings alert type: {alert_type}"

        return msg

    async def _send_telegram_alert(self, message: str, alert: Dict[str, Any]) -> None:
        """Send alert via Telegram"""
        url = f"https://api.telegram.org/bot{self.telegram_api_key}/sendMessage"

        ticker = alert.get("ticker")
        keyboard = {
            "inline_keyboard": [[
                {"text": "📊 View Chart", "url": f"https://www.tradingview.com/chart/?symbol={ticker}"},
                {"text": "📈 Earnings Calendar", "callback_data": f"earnings_{ticker}"}
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

    async def _send_email_alert(self, message: str, alert: Dict[str, Any]) -> None:
        """Send alert via SendGrid email"""
        if not self.sendgrid_api_key:
            return

        ticker = alert.get("ticker")
        alert_type = alert.get("type", "").replace("_", " ").title()

        # Format HTML email
        html_content = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #667eea; color: white; padding: 20px; border-radius: 8px; }}
        .content {{ background: #f5f5f5; padding: 20px; margin-top: 20px; border-radius: 8px; }}
        .highlight {{ background: white; padding: 15px; margin: 15px 0; border-left: 4px solid #667eea; }}
        pre {{ font-family: monospace; white-space: pre-wrap; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📅 Earnings Alert - {ticker}</h1>
            <p>{alert_type}</p>
        </div>
        <div class="content">
            <div class="highlight">
                <pre>{message}</pre>
            </div>
            <p style="text-align: center; margin-top: 20px;">
                <a href="https://www.tradingview.com/chart/?symbol={ticker}"
                   style="display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 6px;">
                   📊 View Chart on TradingView
                </a>
            </p>
        </div>
        <div style="text-align: center; margin-top: 30px; font-size: 12px; color: #999;">
            <p>Alert sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by Legend AI</p>
        </div>
    </div>
</body>
</html>
"""

        url = "https://api.sendgrid.com/v3/mail/send"

        payload = {
            "personalizations": [{
                "to": [{"email": self.alert_email}],
                "subject": f"📅 Earnings Alert: {ticker} - {alert_type}"
            }],
            "from": {
                "email": "alerts@legendai.com",
                "name": "Legend AI Earnings Alerts"
            },
            "content": [{
                "type": "text/html",
                "value": html_content
            }]
        }

        headers = {
            "Authorization": f"Bearer {self.sendgrid_api_key}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code not in [200, 202]:
                raise Exception(f"SendGrid error: {response.status_code} - {response.text}")


# Global service instance
_earnings_alert_service: Optional[EarningsAlertService] = None


def get_earnings_alert_service() -> EarningsAlertService:
    """Get or create earnings alert service singleton"""
    global _earnings_alert_service
    if _earnings_alert_service is None:
        _earnings_alert_service = EarningsAlertService()
    return _earnings_alert_service
