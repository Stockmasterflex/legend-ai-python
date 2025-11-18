"""
Database models for Discord bot features.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text,
    ForeignKey, UniqueConstraint, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class DiscordUser(Base):
    """Discord user profile and settings."""
    __tablename__ = "discord_users"

    id = Column(Integer, primary_key=True)
    discord_id = Column(String(100), unique=True, nullable=False, index=True)
    username = Column(String(100), nullable=False)
    discriminator = Column(String(10))
    avatar_url = Column(String(500))

    # Settings
    timezone = Column(String(50), default="UTC")
    notifications_enabled = Column(Boolean, default=True)
    daily_brief_enabled = Column(Boolean, default=True)

    # Stats
    total_calls = Column(Integer, default=0)
    correct_calls = Column(Integer, default=0)
    total_trades = Column(Integer, default=0)
    paper_balance = Column(Float, default=100000.0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    watchlist_items = relationship("DiscordWatchlist", back_populates="user", cascade="all, delete-orphan")
    alerts = relationship("DiscordAlert", back_populates="user", cascade="all, delete-orphan")
    trades = relationship("PaperTrade", back_populates="user", cascade="all, delete-orphan")
    calls = relationship("TradingCall", back_populates="user", cascade="all, delete-orphan")


class DiscordWatchlist(Base):
    """User watchlist items."""
    __tablename__ = "discord_watchlist"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("discord_users.id", ondelete="CASCADE"), nullable=False)
    ticker = Column(String(20), nullable=False)

    # Analysis context
    pattern = Column(String(50))
    entry_price = Column(Float)
    stop_loss = Column(Float)
    target = Column(Float)
    notes = Column(Text)

    # Tracking
    is_active = Column(Boolean, default=True)
    added_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('user_id', 'ticker', name='uq_user_ticker'),
        Index('idx_watchlist_user', 'user_id'),
    )

    user = relationship("DiscordUser", back_populates="watchlist_items")


class DiscordAlert(Base):
    """Price and pattern alerts."""
    __tablename__ = "discord_alerts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("discord_users.id", ondelete="CASCADE"), nullable=False)
    ticker = Column(String(20), nullable=False)

    # Alert conditions
    alert_type = Column(String(50), nullable=False)  # price_above, price_below, pattern, rsi_oversold, etc.
    threshold = Column(Float)  # For price alerts
    pattern_name = Column(String(50))  # For pattern alerts

    # Status
    is_active = Column(Boolean, default=True)
    triggered_at = Column(DateTime)
    last_checked = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_alerts_active', 'is_active', 'ticker'),
    )

    user = relationship("DiscordUser", back_populates="alerts")


class ServerConfig(Base):
    """Discord server configuration."""
    __tablename__ = "discord_server_config"

    id = Column(Integer, primary_key=True)
    guild_id = Column(String(100), unique=True, nullable=False, index=True)
    guild_name = Column(String(200))

    # Channel IDs
    channel_market_updates = Column(String(100))
    channel_signals = Column(String(100))
    channel_daily_picks = Column(String(100))
    channel_discussions = Column(String(100))

    # Role IDs for permissions
    role_premium = Column(String(100))
    role_moderator = Column(String(100))
    role_trader = Column(String(100))

    # Feature flags
    enable_daily_brief = Column(Boolean, default=True)
    enable_pattern_alerts = Column(Boolean, default=True)
    enable_top_picks = Column(Boolean, default=True)
    enable_leaderboard = Column(Boolean, default=True)

    # Timing settings
    daily_brief_time = Column(String(10), default="09:00")  # UTC time
    daily_picks_time = Column(String(10), default="08:30")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SharedWatchlist(Base):
    """Community shared watchlists."""
    __tablename__ = "discord_shared_watchlists"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    creator_id = Column(Integer, ForeignKey("discord_users.id"), nullable=False)
    guild_id = Column(String(100), nullable=False)

    # Access control
    is_public = Column(Boolean, default=True)

    # Stats
    follower_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index('idx_shared_watchlist_guild', 'guild_id'),
    )


class SharedWatchlistItem(Base):
    """Items in shared watchlists."""
    __tablename__ = "discord_shared_watchlist_items"

    id = Column(Integer, primary_key=True)
    watchlist_id = Column(Integer, ForeignKey("discord_shared_watchlists.id", ondelete="CASCADE"), nullable=False)
    ticker = Column(String(20), nullable=False)
    reason = Column(Text)
    added_by_id = Column(Integer, ForeignKey("discord_users.id"))

    added_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('watchlist_id', 'ticker', name='uq_watchlist_ticker'),
    )


class PaperTrade(Base):
    """Paper trading for competitions."""
    __tablename__ = "discord_paper_trades"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("discord_users.id", ondelete="CASCADE"), nullable=False)
    ticker = Column(String(20), nullable=False)

    # Trade details
    side = Column(String(10), nullable=False)  # long, short
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float)
    shares = Column(Integer, nullable=False)

    # P&L
    realized_pnl = Column(Float)
    realized_pnl_pct = Column(Float)

    # Status
    status = Column(String(20), default="open")  # open, closed

    # Timestamps
    entry_time = Column(DateTime, default=datetime.utcnow)
    exit_time = Column(DateTime)

    __table_args__ = (
        Index('idx_paper_trades_user', 'user_id'),
        Index('idx_paper_trades_status', 'status'),
    )

    user = relationship("DiscordUser", back_populates="trades")


class TradingCall(Base):
    """Trading calls made by users (for leaderboard)."""
    __tablename__ = "discord_trading_calls"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("discord_users.id", ondelete="CASCADE"), nullable=False)
    ticker = Column(String(20), nullable=False)

    # Call details
    call_type = Column(String(20), nullable=False)  # bullish, bearish, neutral
    entry_price = Column(Float, nullable=False)
    target_price = Column(Float)
    stop_loss = Column(Float)
    reasoning = Column(Text)

    # Validation
    is_validated = Column(Boolean, default=False)
    was_correct = Column(Boolean)
    actual_move_pct = Column(Float)

    # Message tracking
    message_id = Column(String(100))
    channel_id = Column(String(100))
    guild_id = Column(String(100))

    created_at = Column(DateTime, default=datetime.utcnow)
    validated_at = Column(DateTime)

    __table_args__ = (
        Index('idx_calls_user', 'user_id'),
        Index('idx_calls_ticker', 'ticker'),
    )

    user = relationship("DiscordUser", back_populates="calls")


class PatternAlert(Base):
    """Pattern alerts sent to channels."""
    __tablename__ = "discord_pattern_alerts"

    id = Column(Integer, primary_key=True)
    guild_id = Column(String(100), nullable=False)
    ticker = Column(String(20), nullable=False)

    # Pattern info
    pattern_name = Column(String(50), nullable=False)
    confidence = Column(Float)
    timeframe = Column(String(10), default="daily")

    # Price context
    price = Column(Float)
    change_pct = Column(Float)

    # Message tracking
    message_id = Column(String(100))
    channel_id = Column(String(100))

    sent_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_pattern_alerts_guild', 'guild_id'),
        Index('idx_pattern_alerts_sent', 'sent_at'),
    )
