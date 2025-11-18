"""
Multi-Channel Alert Delivery System
Supports: Telegram, Email, SMS (Twilio), Discord, Slack, Push Notifications, Webhooks
"""
import logging
import httpx
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models import AlertLog, AlertDelivery
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class AlertDeliveryService:
    """Service for delivering alerts across multiple channels"""

    def __init__(self, db: Session):
        self.db = db
        self.telegram_api_key = settings.telegram_bot_token
        self.telegram_chat_id = settings.telegram_chat_id
        self.sendgrid_api_key = settings.sendgrid_api_key
        self.alert_email = settings.alert_email
        self.twilio_account_sid = getattr(settings, "twilio_account_sid", None)
        self.twilio_auth_token = getattr(settings, "twilio_auth_token", None)
        self.twilio_phone_number = getattr(settings, "twilio_phone_number", None)
        self.alert_phone_number = getattr(settings, "alert_phone_number", None)

    async def deliver_alert(self, alert_log: AlertLog, channels: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Deliver alert to all specified channels

        Args:
            alert_log: AlertLog to deliver
            channels: List of channels to deliver to (defaults to alert_log.delivery_channels)

        Returns:
            Dict with delivery results per channel
        """
        if channels is None:
            channels = alert_log.delivery_channels or []

        results = {}
        delivery_status = {}

        for channel in channels:
            try:
                # Create delivery record
                delivery = AlertDelivery(
                    alert_log_id=alert_log.id,
                    channel=channel,
                    status="pending",
                    attempts=0
                )
                self.db.add(delivery)
                self.db.commit()
                self.db.refresh(delivery)

                # Attempt delivery
                success, result = await self._deliver_to_channel(channel, alert_log, delivery)

                # Update delivery record
                delivery.attempts += 1
                delivery.last_attempt_at = datetime.now()

                if success:
                    delivery.status = "sent"
                    delivery.delivered_at = datetime.now()
                    delivery_status[channel] = "sent"
                    results[channel] = {"success": True, "result": result}
                else:
                    delivery.status = "failed"
                    delivery.failed_at = datetime.now()
                    delivery.error_message = str(result)
                    delivery_status[channel] = "failed"
                    results[channel] = {"success": False, "error": str(result)}

                self.db.commit()

            except Exception as e:
                logger.error(f"Error delivering to {channel}: {e}")
                delivery_status[channel] = "failed"
                results[channel] = {"success": False, "error": str(e)}

        # Update alert_log delivery status
        alert_log.delivery_status = delivery_status
        alert_log.status = "sent" if any(r.get("success") for r in results.values()) else "failed"
        self.db.commit()

        return results

    async def _deliver_to_channel(self, channel: str, alert_log: AlertLog, delivery: AlertDelivery) -> tuple[bool, Any]:
        """
        Deliver alert to a specific channel

        Returns:
            Tuple of (success: bool, result: Any)
        """
        try:
            if channel == "telegram":
                return await self._send_telegram(alert_log, delivery)
            elif channel == "email":
                return await self._send_email(alert_log, delivery)
            elif channel == "sms":
                return await self._send_sms(alert_log, delivery)
            elif channel == "discord":
                return await self._send_discord(alert_log, delivery)
            elif channel == "slack":
                return await self._send_slack(alert_log, delivery)
            elif channel == "webhook":
                return await self._send_webhook(alert_log, delivery)
            elif channel == "push":
                return await self._send_push(alert_log, delivery)
            else:
                logger.warning(f"Unknown channel: {channel}")
                return False, f"Unknown channel: {channel}"

        except Exception as e:
            logger.error(f"Error delivering to {channel}: {e}")
            return False, str(e)

    async def _send_telegram(self, alert_log: AlertLog, delivery: AlertDelivery) -> tuple[bool, Any]:
        """Send alert via Telegram"""
        if not self.telegram_api_key or not self.telegram_chat_id:
            return False, "Telegram not configured"

        try:
            url = f"https://api.telegram.org/bot{self.telegram_api_key}/sendMessage"

            # Create inline keyboard with actions
            keyboard = {
                "inline_keyboard": [[
                    {"text": "✅ Acknowledge", "callback_data": f"ack_{alert_log.id}"},
                    {"text": "❌ Dismiss", "callback_data": f"dismiss_{alert_log.id}"}
                ]]
            }

            payload = {
                "chat_id": self.telegram_chat_id,
                "text": alert_log.alert_message,
                "parse_mode": "Markdown",
                "reply_markup": keyboard
            }

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                result = response.json()

                # Store message ID
                if result.get("ok"):
                    delivery.external_id = str(result.get("result", {}).get("message_id"))
                    delivery.channel_metadata = result

                return True, result

        except Exception as e:
            logger.error(f"Telegram delivery failed: {e}")
            return False, str(e)

    async def _send_email(self, alert_log: AlertLog, delivery: AlertDelivery) -> tuple[bool, Any]:
        """Send alert via Email (SendGrid)"""
        if not self.sendgrid_api_key or not self.alert_email:
            return False, "Email not configured"

        try:
            # Format HTML email
            html_content = self._format_email_html(alert_log)

            # SendGrid API request
            url = "https://api.sendgrid.com/v3/mail/send"

            payload = {
                "personalizations": [{
                    "to": [{"email": self.alert_email}],
                    "subject": f"🚨 {alert_log.alert_title}"
                }],
                "from": {
                    "email": "alerts@legendai.com",
                    "name": "Legend AI Alerts"
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

                # Store message ID from headers
                message_id = response.headers.get("X-Message-Id")
                if message_id:
                    delivery.external_id = message_id

                return True, {"status": response.status_code, "message_id": message_id}

        except Exception as e:
            logger.error(f"Email delivery failed: {e}")
            return False, str(e)

    async def _send_sms(self, alert_log: AlertLog, delivery: AlertDelivery) -> tuple[bool, Any]:
        """Send alert via SMS (Twilio)"""
        if not all([self.twilio_account_sid, self.twilio_auth_token, self.twilio_phone_number, self.alert_phone_number]):
            return False, "SMS (Twilio) not configured"

        try:
            # Format SMS message (keep it short)
            sms_message = self._format_sms_message(alert_log)

            # Twilio API request
            url = f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_account_sid}/Messages.json"

            data = {
                "From": self.twilio_phone_number,
                "To": self.alert_phone_number,
                "Body": sms_message
            }

            auth = (self.twilio_account_sid, self.twilio_auth_token)

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(url, data=data, auth=auth)
                response.raise_for_status()
                result = response.json()

                # Store message SID
                if result.get("sid"):
                    delivery.external_id = result["sid"]
                    delivery.channel_metadata = result

                return True, result

        except Exception as e:
            logger.error(f"SMS delivery failed: {e}")
            return False, str(e)

    async def _send_discord(self, alert_log: AlertLog, delivery: AlertDelivery) -> tuple[bool, Any]:
        """Send alert via Discord webhook"""
        # Get Discord webhook URL from alert rule's delivery_config
        rule = alert_log.rule if hasattr(alert_log, 'rule') else None
        webhook_url = None

        if rule and rule.delivery_config:
            webhook_url = rule.delivery_config.get("discord_webhook_url")

        if not webhook_url:
            # Try to get from settings
            webhook_url = getattr(settings, "discord_webhook_url", None)

        if not webhook_url:
            return False, "Discord webhook not configured"

        try:
            # Format Discord embed
            embed = {
                "embeds": [{
                    "title": f"🚨 {alert_log.alert_title}",
                    "description": alert_log.alert_message,
                    "color": 15158332,  # Red color
                    "fields": [
                        {"name": "Alert Type", "value": alert_log.alert_type.upper(), "inline": True},
                        {"name": "Price", "value": f"${alert_log.trigger_price:.2f}" if alert_log.trigger_price else "N/A", "inline": True}
                    ],
                    "timestamp": datetime.now().isoformat(),
                    "footer": {"text": "Legend AI Alert System"}
                }]
            }

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(webhook_url, json=embed)
                response.raise_for_status()

                return True, {"status": response.status_code}

        except Exception as e:
            logger.error(f"Discord delivery failed: {e}")
            return False, str(e)

    async def _send_slack(self, alert_log: AlertLog, delivery: AlertDelivery) -> tuple[bool, Any]:
        """Send alert via Slack webhook"""
        # Get Slack webhook URL from alert rule's delivery_config
        rule = alert_log.rule if hasattr(alert_log, 'rule') else None
        webhook_url = None

        if rule and rule.delivery_config:
            webhook_url = rule.delivery_config.get("slack_webhook_url")

        if not webhook_url:
            # Try to get from settings
            webhook_url = getattr(settings, "slack_webhook_url", None)

        if not webhook_url:
            return False, "Slack webhook not configured"

        try:
            # Format Slack message
            payload = {
                "text": f"🚨 *{alert_log.alert_title}*",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"🚨 {alert_log.alert_title}"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": alert_log.alert_message
                        }
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": f"Alert Type: *{alert_log.alert_type.upper()}*  |  Price: *${alert_log.trigger_price:.2f}*" if alert_log.trigger_price else f"Alert Type: *{alert_log.alert_type.upper()}*"
                            }
                        ]
                    }
                ]
            }

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(webhook_url, json=payload)
                response.raise_for_status()

                return True, {"status": response.status_code}

        except Exception as e:
            logger.error(f"Slack delivery failed: {e}")
            return False, str(e)

    async def _send_webhook(self, alert_log: AlertLog, delivery: AlertDelivery) -> tuple[bool, Any]:
        """Send alert via custom webhook"""
        # Get webhook URL from alert rule's delivery_config
        rule = alert_log.rule if hasattr(alert_log, 'rule') else None
        webhook_url = None

        if rule and rule.delivery_config:
            webhook_url = rule.delivery_config.get("webhook_url")

        if not webhook_url:
            return False, "Custom webhook not configured"

        try:
            # Format webhook payload
            payload = {
                "alert_id": alert_log.id,
                "rule_id": alert_log.rule_id,
                "ticker_id": alert_log.ticker_id,
                "alert_type": alert_log.alert_type,
                "alert_title": alert_log.alert_title,
                "alert_message": alert_log.alert_message,
                "trigger_price": alert_log.trigger_price,
                "trigger_value": alert_log.trigger_value,
                "trigger_data": alert_log.trigger_data,
                "timestamp": alert_log.alert_sent_at.isoformat() if alert_log.alert_sent_at else datetime.now().isoformat()
            }

            # Get custom headers if specified
            custom_headers = {}
            if rule and rule.delivery_config:
                custom_headers = rule.delivery_config.get("webhook_headers", {})

            headers = {
                "Content-Type": "application/json",
                **custom_headers
            }

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(webhook_url, json=payload, headers=headers)
                response.raise_for_status()

                delivery.channel_metadata = {
                    "status_code": response.status_code,
                    "response": response.text[:1000]  # Store first 1000 chars
                }

                return True, {"status": response.status_code, "response": response.text}

        except Exception as e:
            logger.error(f"Webhook delivery failed: {e}")
            return False, str(e)

    async def _send_push(self, alert_log: AlertLog, delivery: AlertDelivery) -> tuple[bool, Any]:
        """Send push notification (web push)"""
        # This would require web push setup with service workers
        # For now, return a placeholder
        return False, "Push notifications not yet implemented (requires web push setup)"

    def _format_email_html(self, alert_log: AlertLog) -> str:
        """Format HTML email for alert"""
        return f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #e74c3c; color: white; padding: 20px; border-radius: 8px; }}
        .content {{ background: #f5f5f5; padding: 20px; margin-top: 20px; border-radius: 8px; }}
        .alert-type {{ display: inline-block; padding: 5px 10px; background: #667eea; color: white; border-radius: 4px; }}
        .price {{ font-size: 24px; font-weight: bold; color: #e74c3c; }}
        .footer {{ text-align: center; margin-top: 30px; font-size: 12px; color: #999; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚨 {alert_log.alert_title}</h1>
        </div>

        <div class="content">
            <p><span class="alert-type">{alert_log.alert_type.upper()}</span></p>

            {f'<p class="price">${alert_log.trigger_price:.2f}</p>' if alert_log.trigger_price else ''}

            <pre style="white-space: pre-wrap; font-family: monospace; background: white; padding: 15px; border-radius: 6px;">
{alert_log.alert_message}
            </pre>

            <p style="margin-top: 20px; color: #666;">
                <strong>Triggered:</strong> {alert_log.alert_sent_at.strftime('%Y-%m-%d %H:%M:%S') if alert_log.alert_sent_at else datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        </div>

        <div class="footer">
            <p>This is an automated alert from Legend AI</p>
            <p>Always do your own research before making trading decisions</p>
        </div>
    </div>
</body>
</html>
"""

    def _format_sms_message(self, alert_log: AlertLog) -> str:
        """Format SMS message (keep it short - 160 chars recommended)"""
        ticker_symbol = ""
        if alert_log.ticker_id:
            from app.models import Ticker
            ticker = self.db.query(Ticker).filter(Ticker.id == alert_log.ticker_id).first()
            if ticker:
                ticker_symbol = ticker.symbol

        price_str = f"${alert_log.trigger_price:.2f}" if alert_log.trigger_price else ""

        return f"🚨 {ticker_symbol} {alert_log.alert_type.upper()} {price_str} - {alert_log.alert_title[:50]}"

    async def retry_failed_delivery(self, delivery: AlertDelivery) -> tuple[bool, Any]:
        """Retry a failed delivery"""
        if delivery.attempts >= delivery.max_attempts:
            return False, "Max attempts reached"

        # Get alert log
        alert_log = self.db.query(AlertLog).filter(AlertLog.id == delivery.alert_log_id).first()
        if not alert_log:
            return False, "Alert log not found"

        # Retry delivery
        success, result = await self._deliver_to_channel(delivery.channel, alert_log, delivery)

        return success, result
