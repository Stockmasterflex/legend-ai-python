"""
Watchlist Alerts Service
Monitors watchlist tickers and sends real-time alerts when patterns form or price targets hit
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Watchlist, Ticker, AlertLog, PatternScan
from app.services.database import DatabaseService
from app.services.market_data import MarketDataService
from app.services.pattern_scanner import PatternScannerService
from app.api.telegram_enhanced import TelegramService
import logging

logger = logging.getLogger(__name__)


class WatchlistAlertsService:
    """
    Monitors watchlist and sends alerts
    """

    def __init__(self):
        self.db_service = DatabaseService()
        self.market_service = MarketDataService()
        self.scanner_service = PatternScannerService()
        self.telegram_service = TelegramService()
        self.is_running = False

    async def start_monitoring(self, interval_minutes: int = 5):
        """
        Start monitoring watchlist in background

        Args:
            interval_minutes: How often to check (default: 5 minutes)
        """
        self.is_running = True
        logger.info(f"Starting watchlist monitoring (every {interval_minutes} minutes)")

        while self.is_running:
            try:
                await self.check_watchlist()
            except Exception as e:
                logger.error(f"Error in watchlist monitoring: {e}")

            # Wait for next check
            await asyncio.sleep(interval_minutes * 60)

    def stop_monitoring(self):
        """Stop the monitoring loop"""
        self.is_running = False
        logger.info("Stopping watchlist monitoring")

    async def check_watchlist(self):
        """Check all watchlist items for alerts"""
        logger.info("Checking watchlist for alerts...")

        async with self.db_service.get_session() as session:
            # Get all active watchlist items with alerts enabled
            result = await session.execute(
                select(Watchlist)
                .join(Ticker)
                .where(
                    and_(
                        Watchlist.status.in_(['active', 'watching']),
                        Watchlist.alerts_enabled == True
                    )
                )
            )

            watchlist_items = result.scalars().all()

            logger.info(f"Found {len(watchlist_items)} watchlist items to check")

            for item in watchlist_items:
                await self._check_watchlist_item(item, session)

    async def _check_watchlist_item(self, item: Watchlist, session: AsyncSession):
        """Check a single watchlist item for alerts"""
        try:
            ticker_symbol = item.ticker.symbol

            # Get current price
            quote = await self.market_service.get_quote(ticker_symbol)

            if not quote:
                logger.warning(f"Could not get quote for {ticker_symbol}")
                return

            current_price = quote.get('price', 0)

            # Check for price alerts
            if item.alert_on_price_target and item.target_entry:
                if current_price <= item.target_entry:
                    await self._send_price_alert(
                        item,
                        "Target Entry Price Reached",
                        current_price,
                        session
                    )

            if item.alert_on_stop_loss and item.target_stop:
                if current_price <= item.target_stop:
                    await self._send_price_alert(
                        item,
                        "Stop Loss Triggered",
                        current_price,
                        session
                    )

            # Check for pattern formation
            if item.alert_on_pattern:
                await self._check_pattern_alerts(item, ticker_symbol, session)

        except Exception as e:
            logger.error(f"Error checking {item.ticker.symbol}: {e}")

    async def _send_price_alert(
        self,
        item: Watchlist,
        alert_type: str,
        current_price: float,
        session: AsyncSession
    ):
        """Send price-based alert"""

        # Check alert frequency (don't spam)
        if not await self._should_send_alert(item, alert_type, session):
            return

        ticker_symbol = item.ticker.symbol
        user_id = item.user_id

        # Create alert message
        message = f"🚨 *{alert_type}*\n\n"
        message += f"Ticker: `{ticker_symbol}`\n"
        message += f"Current Price: ${current_price:.2f}\n"

        if item.target_entry:
            message += f"Target Entry: ${item.target_entry:.2f}\n"
        if item.target_stop:
            message += f"Stop Loss: ${item.target_stop:.2f}\n"

        message += f"\n_Alert triggered at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_"

        # Send Telegram alert
        try:
            await self.telegram_service.send_message(user_id, message)

            # Log alert
            alert_log = AlertLog(
                ticker_id=item.ticker_id,
                user_id=user_id,
                alert_type=alert_type,
                trigger_price=current_price,
                message=message,
                sent_via='telegram',
                status='sent'
            )
            session.add(alert_log)

            # Update watchlist item
            item.last_alerted_at = datetime.utcnow()

            await session.commit()

            logger.info(f"Sent {alert_type} alert for {ticker_symbol} to {user_id}")

        except Exception as e:
            logger.error(f"Failed to send alert: {e}")

            # Log failed alert
            alert_log = AlertLog(
                ticker_id=item.ticker_id,
                user_id=user_id,
                alert_type=alert_type,
                trigger_price=current_price,
                message=message,
                sent_via='telegram',
                status='failed',
                error_message=str(e)
            )
            session.add(alert_log)
            await session.commit()

    async def _check_pattern_alerts(
        self,
        item: Watchlist,
        ticker_symbol: str,
        session: AsyncSession
    ):
        """Check for new pattern formation"""

        # Get latest pattern scan for this ticker
        result = await session.execute(
            select(PatternScan)
            .where(PatternScan.ticker_id == item.ticker_id)
            .order_by(PatternScan.scanned_at.desc())
            .limit(1)
        )

        latest_scan = result.scalar_one_or_none()

        # Check if pattern was scanned recently (within last hour)
        if latest_scan and latest_scan.scanned_at > datetime.utcnow() - timedelta(hours=1):
            # Pattern already detected recently, check if we already alerted
            if latest_scan.scanned_at > (item.last_alerted_at or datetime.min):
                # New pattern detected since last alert
                await self._send_pattern_alert(item, latest_scan, session)
        else:
            # Run pattern detection
            try:
                patterns = await self.scanner_service.scan_symbol(ticker_symbol)

                if patterns:
                    # New patterns found
                    best_pattern = max(patterns, key=lambda p: p.confidence)

                    if best_pattern.confidence >= 0.6:  # Threshold
                        await self._send_pattern_alert(
                            item,
                            None,  # No scan record yet
                            session,
                            pattern_result=best_pattern
                        )

            except Exception as e:
                logger.error(f"Error scanning {ticker_symbol} for patterns: {e}")

    async def _send_pattern_alert(
        self,
        item: Watchlist,
        scan: Optional[PatternScan],
        session: AsyncSession,
        pattern_result=None
    ):
        """Send pattern formation alert"""

        if not await self._should_send_alert(item, "Pattern Detected", session):
            return

        ticker_symbol = item.ticker.symbol
        user_id = item.user_id

        # Determine pattern details
        if scan:
            pattern_type = scan.pattern_type
            confidence = scan.score
            entry = scan.entry_price
            target = scan.target_price
            stop = scan.stop_loss
        elif pattern_result:
            pattern_type = pattern_result.pattern
            confidence = pattern_result.confidence
            entry = pattern_result.entry
            target = pattern_result.target
            stop = pattern_result.stop
        else:
            return

        # Create alert message
        message = f"📊 *Pattern Detected*\n\n"
        message += f"Ticker: `{ticker_symbol}`\n"
        message += f"Pattern: *{pattern_type}*\n"
        message += f"Confidence: {confidence*100:.1f}%\n\n"
        message += f"Entry: ${entry:.2f}\n"
        message += f"Target: ${target:.2f} (+{((target-entry)/entry*100):.1f}%)\n"
        message += f"Stop: ${stop:.2f} (-{((entry-stop)/entry*100):.1f}%)\n"

        risk_reward = (target - entry) / (entry - stop) if entry > stop else 0
        message += f"Risk/Reward: {risk_reward:.2f}\n"

        message += f"\n_Detected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_"

        # Send Telegram alert
        try:
            await self.telegram_service.send_message(user_id, message)

            # If pattern has chart URL, send it
            if pattern_result and pattern_result.chart_url:
                await self.telegram_service.send_photo(
                    user_id,
                    pattern_result.chart_url,
                    f"{ticker_symbol} - {pattern_type}"
                )

            # Log alert
            alert_log = AlertLog(
                ticker_id=item.ticker_id,
                user_id=user_id,
                alert_type="Pattern Detected",
                trigger_price=entry,
                message=message,
                sent_via='telegram',
                status='sent',
                metadata={'pattern': pattern_type, 'confidence': confidence}
            )
            session.add(alert_log)

            # Update watchlist item
            item.last_alerted_at = datetime.utcnow()

            await session.commit()

            logger.info(f"Sent pattern alert for {ticker_symbol} ({pattern_type}) to {user_id}")

        except Exception as e:
            logger.error(f"Failed to send pattern alert: {e}")

    async def _should_send_alert(
        self,
        item: Watchlist,
        alert_type: str,
        session: AsyncSession
    ) -> bool:
        """
        Check if alert should be sent based on frequency settings

        Args:
            item: Watchlist item
            alert_type: Type of alert
            session: Database session

        Returns:
            True if alert should be sent
        """
        # Check alert frequency setting
        frequency = item.alert_frequency or 'once'

        if frequency == 'disabled':
            return False

        if frequency == 'always':
            return True

        # For 'once' or 'daily', check last alert
        if not item.last_alerted_at:
            return True

        # Check if we already sent this type of alert
        result = await session.execute(
            select(AlertLog)
            .where(
                and_(
                    AlertLog.ticker_id == item.ticker_id,
                    AlertLog.user_id == item.user_id,
                    AlertLog.alert_type == alert_type,
                    AlertLog.status == 'sent'
                )
            )
            .order_by(AlertLog.created_at.desc())
            .limit(1)
        )

        last_alert = result.scalar_one_or_none()

        if not last_alert:
            return True

        if frequency == 'once':
            # Only alert once per pattern/price level
            return False

        if frequency == 'daily':
            # Alert once per day
            return last_alert.created_at < datetime.utcnow() - timedelta(days=1)

        if frequency == 'hourly':
            # Alert once per hour
            return last_alert.created_at < datetime.utcnow() - timedelta(hours=1)

        return True

    async def get_alert_history(
        self,
        user_id: str,
        limit: int = 50,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """Get alert history for a user"""

        cutoff = datetime.utcnow() - timedelta(days=days)

        async with self.db_service.get_session() as session:
            result = await session.execute(
                select(AlertLog)
                .join(Ticker)
                .where(
                    and_(
                        AlertLog.user_id == user_id,
                        AlertLog.created_at >= cutoff
                    )
                )
                .order_by(AlertLog.created_at.desc())
                .limit(limit)
            )

            alerts = result.scalars().all()

            history = []
            for alert in alerts:
                history.append({
                    'id': alert.id,
                    'ticker': alert.ticker.symbol,
                    'alert_type': alert.alert_type,
                    'trigger_price': alert.trigger_price,
                    'sent_at': alert.created_at.isoformat(),
                    'sent_via': alert.sent_via,
                    'status': alert.status,
                    'message': alert.message
                })

            return history

    async def mute_ticker_alerts(
        self,
        user_id: str,
        ticker_symbol: str,
        duration_hours: Optional[int] = None
    ):
        """Temporarily mute alerts for a ticker"""

        async with self.db_service.get_session() as session:
            # Find watchlist item
            result = await session.execute(
                select(Watchlist)
                .join(Ticker)
                .where(
                    and_(
                        Watchlist.user_id == user_id,
                        Ticker.symbol == ticker_symbol
                    )
                )
            )

            item = result.scalar_one_or_none()

            if not item:
                raise ValueError(f"Ticker {ticker_symbol} not in watchlist")

            # Mute alerts
            item.alerts_enabled = False

            if duration_hours:
                item.muted_until = datetime.utcnow() + timedelta(hours=duration_hours)

            await session.commit()

    async def unmute_ticker_alerts(self, user_id: str, ticker_symbol: str):
        """Unmute alerts for a ticker"""

        async with self.db_service.get_session() as session:
            result = await session.execute(
                select(Watchlist)
                .join(Ticker)
                .where(
                    and_(
                        Watchlist.user_id == user_id,
                        Ticker.symbol == ticker_symbol
                    )
                )
            )

            item = result.scalar_one_or_none()

            if not item:
                raise ValueError(f"Ticker {ticker_symbol} not in watchlist")

            item.alerts_enabled = True
            item.muted_until = None

            await session.commit()
