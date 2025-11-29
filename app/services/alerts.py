"""
Real-time pattern alerts service for swing traders
Monitors watchlist for pattern formations and sends alerts via email/SMS/Telegram
"""

import logging
from datetime import datetime
from typing import Any, Dict, Optional

import httpx

from app.config import get_settings
from app.core.pattern_detector import PatternDetector
from app.services.cache import get_cache_service
from app.services.market_data import market_data_service

logger = logging.getLogger(__name__)
settings = get_settings()


class AlertService:
    """Service for monitoring patterns and sending alerts"""

    def __init__(self):
        self.detector = PatternDetector()
        self.cache = get_cache_service()
        self.min_confidence_threshold = 0.75  # Only alert on strong patterns
        self.telegram_api_key = settings.telegram_bot_token
        self.telegram_chat_id = settings.telegram_chat_id
        self.sendgrid_api_key = settings.sendgrid_api_key
        self.alert_email = settings.alert_email
        self.last_alerted = {}  # Track last alert time per ticker to avoid spam

    async def monitor_watchlist(self) -> Dict[str, Any]:
        """
        Monitor all watchlist stocks for pattern formations

        Returns:
            Dict with monitoring results and any alerts sent
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

            logger.info(f"📊 Monitoring {len(watchlist_items)} stocks for patterns...")

            for item in watchlist_items:
                ticker = item.get("ticker", "").upper()

                try:
                    # Fetch fresh market data
                    price_data = await market_data_service.get_time_series(
                        ticker=ticker, interval="1day", outputsize=500
                    )

                    if not price_data:
                        logger.debug(f"⚠️ No price data for {ticker}")
                        continue

                    # Analyze for patterns
                    spy_data = await market_data_service.get_time_series(
                        "SPY", "1day", 500
                    )
                    pattern_result = await self.detector.analyze_ticker(
                        ticker, price_data, spy_data
                    )

                    monitored_count += 1

                    if (
                        pattern_result
                        and pattern_result.score >= self.min_confidence_threshold
                    ):
                        # Check if we've already alerted recently (within 6 hours)
                        last_alert_time = self.last_alerted.get(ticker)
                        if (
                            last_alert_time
                            and (datetime.now() - last_alert_time).total_seconds()
                            < 6 * 3600
                        ):
                            logger.debug(
                                f"⏭️ {ticker} already alerted recently, skipping"
                            )
                            continue

                        # Send alert
                        alert_data = {
                            "ticker": ticker,
                            "pattern": pattern_result.pattern,
                            "confidence": pattern_result.score,
                            "entry": pattern_result.entry,
                            "stop": pattern_result.stop,
                            "target": pattern_result.target,
                            "risk_reward": pattern_result.risk_reward,
                            "current_price": pattern_result.current_price,
                            "reason": item.get("reason", "No reason specified"),
                        }

                        # Send to all configured channels
                        await self._send_alerts(alert_data)

                        self.last_alerted[ticker] = datetime.now()
                        alerts_sent.append(alert_data)

                        logger.info(
                            f"🚨 ALERT: {ticker} - {pattern_result.pattern} (Score: {pattern_result.score:.2f})"
                        )

                except Exception as e:
                    logger.warning(f"⚠️ Error monitoring {ticker}: {e}")
                    continue

            logger.info(
                f"✅ Monitoring complete: {monitored_count} monitored, {len(alerts_sent)} alerts sent"
            )

            return {
                "success": True,
                "monitored": monitored_count,
                "alerts_sent": len(alerts_sent),
                "alerts": alerts_sent,
            }

        except Exception as e:
            logger.error(f"❌ Monitoring error: {e}")
            return {"success": False, "error": str(e)}

    async def _send_alerts(self, alert_data: Dict[str, Any]) -> None:
        """Send alert to all configured channels (Telegram, Email, SMS)"""

        # Format alert message
        message = self._format_alert_message(alert_data)

        # Send to Telegram
        if self.telegram_api_key and self.telegram_chat_id:
            try:
                await self._send_telegram_alert(message, alert_data)
                logger.info(f"✉️ Telegram alert sent for {alert_data['ticker']}")
            except Exception as e:
                logger.warning(f"⚠️ Telegram alert failed: {e}")

        # Send to Email
        if self.sendgrid_api_key and self.alert_email:
            try:
                await self._send_email_alert(message, alert_data)
                logger.info(f"📧 Email alert sent for {alert_data['ticker']}")
            except Exception as e:
                logger.warning(f"⚠️ Email alert failed: {e}")

    def _format_alert_message(self, alert: Dict[str, Any]) -> str:
        """Format alert message for sending"""

        msg = f"""
🚨 PATTERN ALERT
================

📊 Stock: {alert['ticker']}
🎯 Pattern: {alert['pattern']}
📈 Confidence: {alert['confidence']:.1%}
💰 Current Price: ${alert['current_price']:.2f}

📍 Entry Points:
  Entry: ${alert['entry']:.2f}
  Stop: ${alert['stop']:.2f}
  Target: ${alert['target']:.2f}
  R:R Ratio: {alert['risk_reward']:.2f}:1

📝 Reason: {alert['reason']}

⏰ Alert Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✅ Ready to Trade!
"""
        return msg

    async def _send_telegram_alert(self, message: str, alert: Dict[str, Any]) -> None:
        """Send alert via Telegram"""

        url = f"https://api.telegram.org/bot{self.telegram_api_key}/sendMessage"

        # Create inline keyboard with quick actions
        keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": "📊 View Chart",
                        "url": f"https://www.tradingview.com/chart/?symbol={alert['ticker']}",
                    },
                    {
                        "text": "📈 Add to Watchlist",
                        "callback_data": f"add_{alert['ticker']}",
                    },
                ]
            ]
        }

        payload = {
            "chat_id": self.telegram_chat_id,
            "text": message,
            "parse_mode": "Markdown",
            "reply_markup": keyboard,
        }

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()

    async def _send_email_alert(self, message: str, alert: Dict[str, Any]) -> None:
        """Send alert via SendGrid email"""

        if not self.sendgrid_api_key:
            return

        # Format HTML email
        html_content = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #667eea; color: white; padding: 20px; border-radius: 8px; }}
        .content {{ background: #f5f5f5; padding: 20px; margin-top: 20px; border-radius: 8px; }}
        .key-info {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 15px; }}
        .info-box {{ background: white; padding: 15px; border-radius: 6px; border-left: 4px solid #667eea; }}
        .label {{ font-weight: bold; color: #667eea; }}
        .alert {{ color: #e74c3c; font-weight: bold; }}
        .footer {{ text-align: center; margin-top: 30px; font-size: 12px; color: #999; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚨 Pattern Alert - {alert['ticker']}</h1>
        </div>

        <div class="content">
            <p><strong>Pattern Type:</strong> <span class="alert">{alert['pattern']}</span></p>
            <p><strong>Confidence Score:</strong> {alert['confidence']:.1%}</p>
            <p><strong>Current Price:</strong> ${alert['current_price']:.2f}</p>

            <div class="key-info">
                <div class="info-box">
                    <div class="label">Entry Price</div>
                    <div>${alert['entry']:.2f}</div>
                </div>
                <div class="info-box">
                    <div class="label">Stop Loss</div>
                    <div>${alert['stop']:.2f}</div>
                </div>
                <div class="info-box">
                    <div class="label">Target Price</div>
                    <div>${alert['target']:.2f}</div>
                </div>
                <div class="info-box">
                    <div class="label">Risk:Reward Ratio</div>
                    <div>{alert['risk_reward']:.2f}:1</div>
                </div>
            </div>

            <p style="margin-top: 20px;"><strong>Reason for Monitoring:</strong></p>
            <p>{alert['reason']}</p>

            <p style="margin-top: 20px; text-align: center;">
                <a href="https://www.tradingview.com/chart/?symbol={alert['ticker']}"
                   style="display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 6px;">
                   📊 View Chart on TradingView
                </a>
            </p>
        </div>

        <div class="footer">
            <p>Alert sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by Legend AI</p>
            <p>This is an automated alert. Always do your own research before trading.</p>
        </div>
    </div>
</body>
</html>
"""

        # SendGrid API request
        url = "https://api.sendgrid.com/v3/mail/send"

        payload = {
            "personalizations": [
                {
                    "to": [{"email": self.alert_email}],
                    "subject": f"🚨 Pattern Alert: {alert['ticker']} - {alert['pattern']}",
                }
            ],
            "from": {"email": "alerts@legendai.com", "name": "Legend AI Alerts"},
            "content": [{"type": "text/html", "value": html_content}],
        }

        headers = {
            "Authorization": f"Bearer {self.sendgrid_api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code not in [200, 202]:
                raise Exception(
                    f"SendGrid error: {response.status_code} - {response.text}"
                )


# Global alert service instance
_alert_service: Optional[AlertService] = None


def get_alert_service() -> AlertService:
    """Get or create alert service singleton"""
    global _alert_service
    if _alert_service is None:
        _alert_service = AlertService()
    return _alert_service
