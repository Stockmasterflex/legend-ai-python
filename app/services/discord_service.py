"""
Service layer for Discord bot database operations.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.config import get_settings
from app.models_discord import (
    Base,
    DiscordUser,
    DiscordWatchlist,
    DiscordAlert,
    ServerConfig,
    SharedWatchlist,
    SharedWatchlistItem,
    PaperTrade,
    TradingCall,
    PatternAlert,
)

logger = logging.getLogger(__name__)


class DiscordService:
    """Database service for Discord bot."""

    def __init__(self):
        self.settings = get_settings()
        self.engine = None
        self.SessionLocal = None

        if self.settings.database_url:
            self._init_db()

    def _init_db(self):
        """Initialize database connection."""
        try:
            self.engine = create_engine(self.settings.database_url)
            self.SessionLocal = sessionmaker(bind=self.engine)

            # Create tables
            Base.metadata.create_all(self.engine)

            logger.info("Discord database initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Discord database: {e}")

    def _get_session(self) -> Session:
        """Get database session."""
        if not self.SessionLocal:
            raise RuntimeError("Database not initialized")
        return self.SessionLocal()

    # ==================== USER OPERATIONS ====================

    def get_or_create_user(
        self, discord_id: str, username: str, discriminator: str = None
    ) -> DiscordUser:
        """Get existing user or create new one."""
        with self._get_session() as session:
            user = session.query(DiscordUser).filter_by(discord_id=discord_id).first()

            if not user:
                user = DiscordUser(
                    discord_id=discord_id,
                    username=username,
                    discriminator=discriminator,
                )
                session.add(user)
                session.commit()
                session.refresh(user)

            return user

    def update_user_stats(
        self,
        discord_id: str,
        correct_calls: int = None,
        total_calls: int = None,
        paper_balance: float = None,
    ) -> bool:
        """Update user statistics."""
        try:
            with self._get_session() as session:
                user = session.query(DiscordUser).filter_by(discord_id=discord_id).first()

                if not user:
                    return False

                if correct_calls is not None:
                    user.correct_calls = correct_calls
                if total_calls is not None:
                    user.total_calls = total_calls
                if paper_balance is not None:
                    user.paper_balance = paper_balance

                user.updated_at = datetime.utcnow()
                session.commit()

                return True
        except SQLAlchemyError as e:
            logger.error(f"Error updating user stats: {e}")
            return False

    # ==================== WATCHLIST OPERATIONS ====================

    def add_to_watchlist(
        self,
        discord_id: str,
        ticker: str,
        pattern: str = None,
        entry_price: float = None,
        stop_loss: float = None,
        target: float = None,
        notes: str = None,
    ) -> bool:
        """Add ticker to user's watchlist."""
        try:
            with self._get_session() as session:
                user = session.query(DiscordUser).filter_by(discord_id=discord_id).first()

                if not user:
                    return False

                # Check if already exists
                existing = (
                    session.query(DiscordWatchlist)
                    .filter_by(user_id=user.id, ticker=ticker)
                    .first()
                )

                if existing:
                    # Update existing
                    existing.pattern = pattern
                    existing.entry_price = entry_price
                    existing.stop_loss = stop_loss
                    existing.target = target
                    existing.notes = notes
                    existing.is_active = True
                else:
                    # Create new
                    item = DiscordWatchlist(
                        user_id=user.id,
                        ticker=ticker,
                        pattern=pattern,
                        entry_price=entry_price,
                        stop_loss=stop_loss,
                        target=target,
                        notes=notes,
                    )
                    session.add(item)

                session.commit()
                return True
        except SQLAlchemyError as e:
            logger.error(f"Error adding to watchlist: {e}")
            return False

    def remove_from_watchlist(self, discord_id: str, ticker: str) -> bool:
        """Remove ticker from watchlist."""
        try:
            with self._get_session() as session:
                user = session.query(DiscordUser).filter_by(discord_id=discord_id).first()

                if not user:
                    return False

                item = (
                    session.query(DiscordWatchlist)
                    .filter_by(user_id=user.id, ticker=ticker)
                    .first()
                )

                if item:
                    session.delete(item)
                    session.commit()
                    return True

                return False
        except SQLAlchemyError as e:
            logger.error(f"Error removing from watchlist: {e}")
            return False

    def get_watchlist(self, discord_id: str) -> List[Dict[str, Any]]:
        """Get user's watchlist."""
        try:
            with self._get_session() as session:
                user = session.query(DiscordUser).filter_by(discord_id=discord_id).first()

                if not user:
                    return []

                items = (
                    session.query(DiscordWatchlist)
                    .filter_by(user_id=user.id, is_active=True)
                    .all()
                )

                return [
                    {
                        "ticker": item.ticker,
                        "pattern": item.pattern,
                        "entry_price": item.entry_price,
                        "stop_loss": item.stop_loss,
                        "target": item.target,
                        "notes": item.notes,
                        "added_at": item.added_at,
                    }
                    for item in items
                ]
        except SQLAlchemyError as e:
            logger.error(f"Error getting watchlist: {e}")
            return []

    # ==================== ALERT OPERATIONS ====================

    def create_alert(
        self,
        discord_id: str,
        ticker: str,
        alert_type: str,
        threshold: float = None,
        pattern_name: str = None,
    ) -> bool:
        """Create price or pattern alert."""
        try:
            with self._get_session() as session:
                user = session.query(DiscordUser).filter_by(discord_id=discord_id).first()

                if not user:
                    return False

                alert = DiscordAlert(
                    user_id=user.id,
                    ticker=ticker,
                    alert_type=alert_type,
                    threshold=threshold,
                    pattern_name=pattern_name,
                )

                session.add(alert)
                session.commit()

                return True
        except SQLAlchemyError as e:
            logger.error(f"Error creating alert: {e}")
            return False

    def get_active_alerts(self, ticker: str = None) -> List[Dict[str, Any]]:
        """Get active alerts (optionally filtered by ticker)."""
        try:
            with self._get_session() as session:
                query = session.query(DiscordAlert).filter_by(is_active=True)

                if ticker:
                    query = query.filter_by(ticker=ticker)

                alerts = query.all()

                return [
                    {
                        "id": alert.id,
                        "user_id": alert.user_id,
                        "discord_id": alert.user.discord_id,
                        "ticker": alert.ticker,
                        "alert_type": alert.alert_type,
                        "threshold": alert.threshold,
                        "pattern_name": alert.pattern_name,
                    }
                    for alert in alerts
                ]
        except SQLAlchemyError as e:
            logger.error(f"Error getting alerts: {e}")
            return []

    def trigger_alert(self, alert_id: int) -> bool:
        """Mark alert as triggered."""
        try:
            with self._get_session() as session:
                alert = session.query(DiscordAlert).filter_by(id=alert_id).first()

                if alert:
                    alert.triggered_at = datetime.utcnow()
                    alert.is_active = False
                    session.commit()
                    return True

                return False
        except SQLAlchemyError as e:
            logger.error(f"Error triggering alert: {e}")
            return False

    # ==================== PAPER TRADING ====================

    def create_paper_trade(
        self,
        discord_id: str,
        ticker: str,
        side: str,
        entry_price: float,
        shares: int,
    ) -> Optional[int]:
        """Create paper trade."""
        try:
            with self._get_session() as session:
                user = session.query(DiscordUser).filter_by(discord_id=discord_id).first()

                if not user:
                    return None

                trade = PaperTrade(
                    user_id=user.id,
                    ticker=ticker,
                    side=side,
                    entry_price=entry_price,
                    shares=shares,
                )

                session.add(trade)
                session.commit()
                session.refresh(trade)

                return trade.id
        except SQLAlchemyError as e:
            logger.error(f"Error creating paper trade: {e}")
            return None

    def close_paper_trade(
        self, trade_id: int, exit_price: float
    ) -> Optional[Dict[str, Any]]:
        """Close paper trade and calculate P&L."""
        try:
            with self._get_session() as session:
                trade = session.query(PaperTrade).filter_by(id=trade_id).first()

                if not trade or trade.status != "open":
                    return None

                trade.exit_price = exit_price
                trade.exit_time = datetime.utcnow()
                trade.status = "closed"

                # Calculate P&L
                if trade.side == "long":
                    pnl = (exit_price - trade.entry_price) * trade.shares
                else:  # short
                    pnl = (trade.entry_price - exit_price) * trade.shares

                pnl_pct = (pnl / (trade.entry_price * trade.shares)) * 100

                trade.realized_pnl = pnl
                trade.realized_pnl_pct = pnl_pct

                # Update user balance
                user = trade.user
                user.paper_balance += pnl
                user.total_trades += 1

                session.commit()

                return {
                    "ticker": trade.ticker,
                    "pnl": pnl,
                    "pnl_pct": pnl_pct,
                    "new_balance": user.paper_balance,
                }
        except SQLAlchemyError as e:
            logger.error(f"Error closing paper trade: {e}")
            return None

    def get_open_trades(self, discord_id: str) -> List[Dict[str, Any]]:
        """Get user's open paper trades."""
        try:
            with self._get_session() as session:
                user = session.query(DiscordUser).filter_by(discord_id=discord_id).first()

                if not user:
                    return []

                trades = (
                    session.query(PaperTrade)
                    .filter_by(user_id=user.id, status="open")
                    .all()
                )

                return [
                    {
                        "id": trade.id,
                        "ticker": trade.ticker,
                        "side": trade.side,
                        "entry_price": trade.entry_price,
                        "shares": trade.shares,
                        "entry_time": trade.entry_time,
                    }
                    for trade in trades
                ]
        except SQLAlchemyError as e:
            logger.error(f"Error getting open trades: {e}")
            return []

    # ==================== LEADERBOARD ====================

    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get trading call leaderboard."""
        try:
            with self._get_session() as session:
                users = (
                    session.query(DiscordUser)
                    .filter(DiscordUser.total_calls > 0)
                    .order_by(
                        desc(DiscordUser.correct_calls / DiscordUser.total_calls),
                        desc(DiscordUser.total_calls),
                    )
                    .limit(limit)
                    .all()
                )

                return [
                    {
                        "rank": i + 1,
                        "username": user.username,
                        "discord_id": user.discord_id,
                        "total_calls": user.total_calls,
                        "correct_calls": user.correct_calls,
                        "accuracy": (
                            user.correct_calls / user.total_calls * 100
                            if user.total_calls > 0
                            else 0
                        ),
                    }
                    for i, user in enumerate(users)
                ]
        except SQLAlchemyError as e:
            logger.error(f"Error getting leaderboard: {e}")
            return []

    # ==================== TRADING CALLS ====================

    def create_trading_call(
        self,
        discord_id: str,
        ticker: str,
        call_type: str,
        entry_price: float,
        target_price: float = None,
        stop_loss: float = None,
        reasoning: str = None,
        message_id: str = None,
        channel_id: str = None,
        guild_id: str = None,
    ) -> Optional[int]:
        """Create trading call for leaderboard tracking."""
        try:
            with self._get_session() as session:
                user = session.query(DiscordUser).filter_by(discord_id=discord_id).first()

                if not user:
                    return None

                call = TradingCall(
                    user_id=user.id,
                    ticker=ticker,
                    call_type=call_type,
                    entry_price=entry_price,
                    target_price=target_price,
                    stop_loss=stop_loss,
                    reasoning=reasoning,
                    message_id=message_id,
                    channel_id=channel_id,
                    guild_id=guild_id,
                )

                session.add(call)
                session.commit()
                session.refresh(call)

                return call.id
        except SQLAlchemyError as e:
            logger.error(f"Error creating trading call: {e}")
            return None

    def validate_trading_call(
        self, call_id: int, was_correct: bool, actual_move_pct: float
    ) -> bool:
        """Validate trading call (after target or stop hit)."""
        try:
            with self._get_session() as session:
                call = session.query(TradingCall).filter_by(id=call_id).first()

                if not call:
                    return False

                call.is_validated = True
                call.was_correct = was_correct
                call.actual_move_pct = actual_move_pct
                call.validated_at = datetime.utcnow()

                # Update user stats
                user = call.user
                user.total_calls += 1
                if was_correct:
                    user.correct_calls += 1

                session.commit()

                return True
        except SQLAlchemyError as e:
            logger.error(f"Error validating trading call: {e}")
            return False

    # ==================== SERVER CONFIG ====================

    def get_server_config(self, guild_id: str) -> Optional[Dict[str, Any]]:
        """Get server configuration."""
        try:
            with self._get_session() as session:
                config = (
                    session.query(ServerConfig).filter_by(guild_id=guild_id).first()
                )

                if not config:
                    return None

                return {
                    "channel_market_updates": config.channel_market_updates,
                    "channel_signals": config.channel_signals,
                    "channel_daily_picks": config.channel_daily_picks,
                    "enable_daily_brief": config.enable_daily_brief,
                    "enable_pattern_alerts": config.enable_pattern_alerts,
                    "enable_top_picks": config.enable_top_picks,
                    "daily_brief_time": config.daily_brief_time,
                    "daily_picks_time": config.daily_picks_time,
                }
        except SQLAlchemyError as e:
            logger.error(f"Error getting server config: {e}")
            return None

    def update_server_config(self, guild_id: str, **kwargs) -> bool:
        """Update server configuration."""
        try:
            with self._get_session() as session:
                config = (
                    session.query(ServerConfig).filter_by(guild_id=guild_id).first()
                )

                if not config:
                    config = ServerConfig(guild_id=guild_id)
                    session.add(config)

                for key, value in kwargs.items():
                    if hasattr(config, key):
                        setattr(config, key, value)

                config.updated_at = datetime.utcnow()
                session.commit()

                return True
        except SQLAlchemyError as e:
            logger.error(f"Error updating server config: {e}")
            return False


# Global instance
discord_service = DiscordService()
