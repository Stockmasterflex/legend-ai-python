"""
Screen Scheduler Service

Handles scheduled execution of saved screens with email notifications.
"""
import asyncio
import logging
import json
from datetime import datetime, timezone, time as dt_time
from typing import List, Dict, Any, Optional
import csv
import io

from app.services.saved_screen_service import get_saved_screen_service
from app.services.alerts import AlertService
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class ScreenSchedulerService:
    """Service for running scheduled screens and sending notifications"""

    def __init__(self):
        self.alert_service = AlertService()
        self.running = False

    async def run_scheduled_screens(self):
        """
        Check and run all scheduled screens that are due

        Should be called periodically (e.g., every 15 minutes)
        """
        try:
            screen_service = get_saved_screen_service()
            scheduled_screens = screen_service.get_scheduled_screens()

            if not scheduled_screens:
                logger.debug("No scheduled screens found")
                return

            current_time = datetime.now(timezone.utc)
            current_hour_minute = current_time.strftime("%H:%M")

            for screen in scheduled_screens:
                try:
                    # Check if this screen is due to run
                    if self._is_due(screen, current_time, current_hour_minute):
                        logger.info(f"Running scheduled screen: {screen['name']}")
                        await self._run_and_notify(screen)
                except Exception as e:
                    logger.error(f"Failed to run scheduled screen {screen.get('name')}: {e}")

        except Exception as e:
            logger.error(f"Error in run_scheduled_screens: {e}")

    def _is_due(
        self,
        screen: Dict[str, Any],
        current_time: datetime,
        current_hour_minute: str
    ) -> bool:
        """Check if a screen is due to run"""
        frequency = screen.get("schedule_frequency")
        schedule_time = screen.get("schedule_time")

        if not frequency or not schedule_time:
            return False

        # Check if the scheduled time matches current time
        if schedule_time != current_hour_minute:
            return False

        # Check last run time to avoid duplicate runs
        last_run = screen.get("last_run_at")
        if last_run:
            try:
                last_run_dt = datetime.fromisoformat(last_run.replace("Z", "+00:00"))
                time_since_last_run = (current_time - last_run_dt).total_seconds()

                # Don't run if we ran in the last hour
                if time_since_last_run < 3600:
                    return False
            except Exception as e:
                logger.debug(f"Error parsing last_run_at: {e}")

        # Check frequency
        if frequency == "daily":
            return True
        elif frequency == "weekly":
            # Run on Mondays (weekday 0)
            return current_time.weekday() == 0
        elif frequency == "hourly":
            return True  # Already checked time match above

        return False

    async def _run_and_notify(self, screen: Dict[str, Any]):
        """Run a screen and send notifications if configured"""
        try:
            screen_service = get_saved_screen_service()

            # Run the screen
            results = await screen_service.run_screen(
                screen_id=screen["id"],
                limit=100,
                save_results=True
            )

            result_count = len(results.get("results", []))
            logger.info(f"Screen '{screen['name']}' found {result_count} matches")

            # Send email if configured
            if screen.get("email_results") and result_count > 0:
                await self._send_email_report(screen, results)

            # Send alerts if configured and matches found
            if screen.get("alert_on_match") and result_count > 0:
                await self._send_match_alerts(screen, results)

        except Exception as e:
            logger.error(f"Failed to run and notify for screen {screen.get('name')}: {e}")
            raise

    async def _send_email_report(self, screen: Dict[str, Any], results: Dict[str, Any]):
        """Send email report with screen results"""
        try:
            alert_email = settings.alert_email
            if not alert_email:
                logger.warning("No alert email configured, skipping email report")
                return

            # Generate email content
            subject = f"Screen Results: {screen['name']}"
            body = self._generate_email_body(screen, results)

            # Send via the alert service's email method
            await self._send_email(
                to_email=alert_email,
                subject=subject,
                body=body,
                html=True
            )

            logger.info(f"Email report sent for screen: {screen['name']}")

        except Exception as e:
            logger.error(f"Failed to send email report: {e}")

    async def _send_match_alerts(self, screen: Dict[str, Any], results: Dict[str, Any]):
        """Send alerts for screen matches"""
        try:
            matches = results.get("results", [])[:10]  # Top 10 matches

            if settings.telegram_bot_token and settings.telegram_chat_id:
                message = self._generate_telegram_message(screen, matches)
                await self._send_telegram(message)

        except Exception as e:
            logger.error(f"Failed to send match alerts: {e}")

    def _generate_email_body(self, screen: Dict[str, Any], results: Dict[str, Any]) -> str:
        """Generate HTML email body"""
        matches = results.get("results", [])
        meta = results.get("meta", {})

        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #34495e; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th {{ background-color: #3498db; color: white; padding: 12px; text-align: left; }}
                td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                tr:hover {{ background-color: #f5f5f5; }}
                .footer {{ margin-top: 30px; color: #7f8c8d; font-size: 12px; }}
            </style>
        </head>
        <body>
            <h1>Screen Results: {screen['name']}</h1>
            <p><strong>Description:</strong> {screen.get('description', 'N/A')}</p>
            <p><strong>Run Date:</strong> {results.get('as_of', 'N/A')}</p>
            <p><strong>Matches Found:</strong> {len(matches)} / {meta.get('total_scanned', 0)} scanned</p>

            <h2>Top Matches</h2>
            <table>
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Name</th>
                        <th>Sector</th>
                        <th>Price</th>
                        <th>Volume</th>
                        <th>RS Rating</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
        """

        for match in matches[:20]:  # Top 20
            html += f"""
                    <tr>
                        <td><strong>{match.get('symbol', 'N/A')}</strong></td>
                        <td>{match.get('name', 'N/A')}</td>
                        <td>{match.get('sector', 'N/A')}</td>
                        <td>${match.get('price', 0):.2f}</td>
                        <td>{match.get('volume', 0):,}</td>
                        <td>{match.get('rs_rating', 0):.1f}</td>
                        <td>{match.get('score', 0):.1f}</td>
                    </tr>
            """

        html += """
                </tbody>
            </table>

            <div class="footer">
                <p>This is an automated report from Legend AI Stock Screener.</p>
            </div>
        </body>
        </html>
        """

        return html

    def _generate_telegram_message(self, screen: Dict[str, Any], matches: List[Dict[str, Any]]) -> str:
        """Generate Telegram message"""
        message = f"📊 *Screen Alert: {screen['name']}*\n\n"
        message += f"Found {len(matches)} matches\n\n"

        for i, match in enumerate(matches[:5], 1):  # Top 5 for Telegram
            message += f"{i}. *{match.get('symbol')}* - {match.get('name', 'N/A')}\n"
            message += f"   Price: ${match.get('price', 0):.2f} | "
            message += f"RS: {match.get('rs_rating', 0):.1f} | "
            message += f"Score: {match.get('score', 0):.1f}\n\n"

        return message

    async def _send_email(self, to_email: str, subject: str, body: str, html: bool = False):
        """Send email using SendGrid"""
        import httpx

        if not settings.sendgrid_api_key:
            logger.warning("SendGrid API key not configured")
            return

        try:
            url = "https://api.sendgrid.com/v3/mail/send"
            headers = {
                "Authorization": f"Bearer {settings.sendgrid_api_key}",
                "Content-Type": "application/json"
            }

            content_type = "text/html" if html else "text/plain"
            data = {
                "personalizations": [{
                    "to": [{"email": to_email}],
                    "subject": subject
                }],
                "from": {"email": settings.alert_email or "noreply@legendai.com"},
                "content": [{
                    "type": content_type,
                    "value": body
                }]
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data, headers=headers)
                response.raise_for_status()

            logger.info(f"Email sent successfully to {to_email}")

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise

    async def _send_telegram(self, message: str):
        """Send Telegram message"""
        import httpx

        if not settings.telegram_bot_token or not settings.telegram_chat_id:
            logger.warning("Telegram not configured")
            return

        try:
            url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
            data = {
                "chat_id": settings.telegram_chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data)
                response.raise_for_status()

            logger.info("Telegram alert sent successfully")

        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")

    def generate_csv_export(self, results: List[Dict[str, Any]]) -> str:
        """Generate CSV export of screen results"""
        output = io.StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=[
                "symbol", "name", "sector", "industry",
                "price", "volume", "avg_volume",
                "rs_rating", "score"
            ]
        )

        writer.writeheader()
        for result in results:
            writer.writerow({
                "symbol": result.get("symbol", ""),
                "name": result.get("name", ""),
                "sector": result.get("sector", ""),
                "industry": result.get("industry", ""),
                "price": result.get("price", 0),
                "volume": result.get("volume", 0),
                "avg_volume": result.get("avg_volume", 0),
                "rs_rating": result.get("rs_rating", 0),
                "score": result.get("score", 0),
            })

        return output.getvalue()


# Global instance
screen_scheduler_service = ScreenSchedulerService()
