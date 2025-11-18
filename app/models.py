"""
Database models for Legend AI
Phase 1.5: Database Integration
Phase 2.0: Social Trading Community
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, ForeignKey, Index, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Ticker(Base):
    """Stock ticker information"""
    __tablename__ = "tickers"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), unique=True, index=True, nullable=False)
    name = Column(String(255))
    sector = Column(String(100))
    industry = Column(String(100))
    exchange = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class PatternScan(Base):
    """Pattern scanning results"""
    __tablename__ = "pattern_scans"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True)
    pattern_type = Column(String(50), index=True)  # VCP, Cup & Handle, etc.
    score = Column(Float, nullable=False)
    entry_price = Column(Float)
    stop_price = Column(Float)
    target_price = Column(Float)
    risk_reward_ratio = Column(Float)
    criteria_met = Column(Text)  # JSON string of met criteria
    analysis = Column(Text)
    current_price = Column(Float)
    volume_dry_up = Column(Boolean, default=False)
    consolidation_days = Column(Integer)
    chart_url = Column(Text, nullable=True)  # URL to generated chart
    rs_rating = Column(Float, nullable=True)  # Relative strength rating
    scanned_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

class Watchlist(Base):
    """User watchlist with status tracking and alerts"""
    __tablename__ = "watchlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, default="default")  # Telegram user ID or "default"
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True)
    status = Column(String(50), default="Watching", index=True)  # "Watching", "Breaking Out", "Triggered", "Completed", "Skipped"
    target_entry = Column(Float, nullable=True)  # Expected entry price
    target_stop = Column(Float, nullable=True)  # Expected stop price
    target_price = Column(Float, nullable=True)  # Target price for take-profit
    reason = Column(Text)  # Why this ticker is on watchlist
    notes = Column(Text)  # Additional notes
    alerts_enabled = Column(Boolean, default=True)  # Enable/disable price alerts
    alert_threshold = Column(Float, nullable=True)  # Alert when price moves this %
    added_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    triggered_at = Column(DateTime(timezone=True), nullable=True, index=True)  # When pattern triggered
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ScanLog(Base):
    """Universe scanning logs"""
    __tablename__ = "scan_logs"

    id = Column(Integer, primary_key=True, index=True)
    scan_type = Column(String(50), index=True)  # daily, weekly, custom
    tickers_scanned = Column(Integer)
    patterns_found = Column(Integer)
    start_time = Column(DateTime(timezone=True), index=True)
    end_time = Column(DateTime(timezone=True))
    status = Column(String(20))  # completed, failed, partial
    error_message = Column(Text)

class UniverseScan(Base):
    """Universe scanning results"""
    __tablename__ = "universe_scans"

    id = Column(Integer, primary_key=True, index=True)
    scan_date = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    universe = Column(String(50), index=True)  # "SP500", "NASDAQ100", "CUSTOM"
    total_scanned = Column(Integer)
    patterns_found = Column(Integer)
    top_score = Column(Float, nullable=True)  # Best score found in scan
    duration_seconds = Column(Float)  # How long scan took
    status = Column(String(20))  # "completed", "failed", "partial"
    error_message = Column(Text, nullable=True)

class AlertLog(Base):
    """Alert trigger history"""
    __tablename__ = "alert_logs"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True)
    alert_type = Column(String(50), index=True)  # "price", "pattern", "breakout", "volume"
    trigger_price = Column(Float, nullable=True)
    trigger_value = Column(Float, nullable=True)
    alert_sent_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    sent_via = Column(String(50))  # "telegram", "email", "push"
    user_id = Column(String(100), nullable=True, index=True)
    status = Column(String(20), default="sent")  # "sent", "failed", "acknowledged"


# ============================================================================
# SOCIAL TRADING COMMUNITY MODELS
# ============================================================================

class User(Base):
    """User accounts for social trading platform"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    trade_posts = relationship("TradePost", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    reactions = relationship("Reaction", back_populates="user", cascade="all, delete-orphan")


class UserProfile(Base):
    """Public trading profiles for users"""
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    trading_since = Column(DateTime(timezone=True), nullable=True)
    preferred_strategies = Column(JSON, nullable=True)  # ["VCP", "Cup & Handle", etc.]
    preferred_tickers = Column(JSON, nullable=True)  # Favorite tickers to trade

    # Public stats
    total_posts = Column(Integer, default=0)
    total_followers = Column(Integer, default=0)
    total_following = Column(Integer, default=0)
    win_rate = Column(Float, nullable=True)  # Percentage of successful trades
    total_trades_shared = Column(Integer, default=0)
    successful_trades = Column(Integer, default=0)
    avg_return = Column(Float, nullable=True)  # Average return percentage

    # Privacy settings
    is_public = Column(Boolean, default=True)
    show_stats = Column(Boolean, default=True)
    allow_copy_trading = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="profile")

    __table_args__ = (Index('idx_profile_public_stats', 'is_public', 'total_followers'),)


class Follow(Base):
    """Following relationships between users"""
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    following_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Copy trading settings
    copy_trading_enabled = Column(Boolean, default=False)
    copy_percentage = Column(Float, nullable=True)  # Percentage of portfolio to allocate
    max_position_size = Column(Float, nullable=True)  # Max $ per position when copying

    __table_args__ = (
        Index('idx_follow_relationship', 'follower_id', 'following_id', unique=True),
    )


class TradePost(Base):
    """Trade ideas and updates shared by users"""
    __tablename__ = "trade_posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), nullable=True, index=True)

    # Post content
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    post_type = Column(String(50), index=True)  # "idea", "entry", "exit", "update", "analysis"

    # Trade details (optional)
    entry_price = Column(Float, nullable=True)
    stop_price = Column(Float, nullable=True)
    target_price = Column(Float, nullable=True)
    position_size = Column(Float, nullable=True)
    pattern_type = Column(String(50), nullable=True)  # VCP, Cup & Handle, etc.

    # Trade outcome (for completed trades)
    exit_price = Column(Float, nullable=True)
    profit_loss = Column(Float, nullable=True)
    profit_loss_percent = Column(Float, nullable=True)
    trade_status = Column(String(50), default="active")  # "active", "closed", "stopped"

    # Engagement metrics
    views_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    reactions_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)

    # Chart annotations (JSON)
    chart_annotations = Column(JSON, nullable=True)

    # Visibility
    is_public = Column(Boolean, default=True)
    is_pinned = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="trade_posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    reactions = relationship("Reaction", back_populates="post", cascade="all, delete-orphan")
    charts = relationship("TradePostChart", back_populates="post", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_post_ticker_date', 'ticker_id', 'created_at'),
        Index('idx_post_type_public', 'post_type', 'is_public', 'created_at'),
    )


class TradePostChart(Base):
    """Charts attached to trade posts"""
    __tablename__ = "trade_post_charts"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("trade_posts.id"), nullable=False, index=True)
    chart_url = Column(String(500), nullable=False)
    chart_type = Column(String(50), nullable=True)  # "candlestick", "line", "volume"
    timeframe = Column(String(20), nullable=True)  # "1D", "4H", "1H", etc.
    annotations = Column(JSON, nullable=True)  # Drawing annotations
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    post = relationship("TradePost", back_populates="charts")


class Comment(Base):
    """Comments on trade posts"""
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    post_id = Column(Integer, ForeignKey("trade_posts.id"), nullable=False, index=True)
    parent_comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True, index=True)  # For threaded replies

    content = Column(Text, nullable=False)
    reactions_count = Column(Integer, default=0)

    is_edited = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="comments")
    post = relationship("TradePost", back_populates="comments")
    reactions = relationship("Reaction", back_populates="comment", cascade="all, delete-orphan")

    # Self-referential relationship for threaded comments
    replies = relationship("Comment", backref="parent", remote_side=[id])

    __table_args__ = (Index('idx_comment_post_date', 'post_id', 'created_at'),)


class Reaction(Base):
    """Reactions (likes, etc.) on posts and comments"""
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    post_id = Column(Integer, ForeignKey("trade_posts.id"), nullable=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True, index=True)

    reaction_type = Column(String(50), default="like")  # "like", "bullish", "bearish", "fire", etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="reactions")
    post = relationship("TradePost", back_populates="reactions")
    comment = relationship("Comment", back_populates="reactions")

    __table_args__ = (
        Index('idx_reaction_post_user', 'post_id', 'user_id', unique=True),
        Index('idx_reaction_comment_user', 'comment_id', 'user_id', unique=True),
    )


class LeaderboardStats(Base):
    """Aggregated statistics for leaderboards"""
    __tablename__ = "leaderboard_stats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)

    # Performance metrics
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    losing_trades = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)

    # Returns
    total_return = Column(Float, default=0.0)  # Total cumulative return %
    avg_return_per_trade = Column(Float, default=0.0)
    best_trade_return = Column(Float, nullable=True)
    worst_trade_return = Column(Float, nullable=True)

    # Risk metrics
    sharpe_ratio = Column(Float, nullable=True)
    max_drawdown = Column(Float, nullable=True)
    avg_hold_time_days = Column(Float, nullable=True)

    # Social metrics
    total_followers = Column(Integer, default=0)
    total_posts = Column(Integer, default=0)
    total_reactions = Column(Integer, default=0)

    # Ranking
    overall_rank = Column(Integer, nullable=True, index=True)
    weekly_rank = Column(Integer, nullable=True)
    monthly_rank = Column(Integer, nullable=True)

    # Time period for stats
    period = Column(String(20), default="all_time")  # "all_time", "monthly", "weekly"
    period_start = Column(DateTime(timezone=True), nullable=True)
    period_end = Column(DateTime(timezone=True), nullable=True)

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('idx_leaderboard_rank', 'overall_rank', 'win_rate'),
        Index('idx_leaderboard_period', 'period', 'updated_at'),
    )


class TrendingTicker(Base):
    """Trending tickers based on community activity"""
    __tablename__ = "trending_tickers"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), nullable=False, index=True)

    # Engagement metrics
    mention_count = Column(Integer, default=0)  # Number of posts mentioning this ticker
    follower_count = Column(Integer, default=0)  # Users watching this ticker
    bullish_sentiment = Column(Integer, default=0)  # Bullish reactions/comments
    bearish_sentiment = Column(Integer, default=0)  # Bearish reactions/comments

    # Calculated metrics
    sentiment_score = Column(Float, default=0.0)  # Net sentiment (-100 to +100)
    trending_score = Column(Float, default=0.0)  # Overall trending score

    # Time window
    time_window = Column(String(20), default="24h")  # "1h", "24h", "7d", "30d"
    window_start = Column(DateTime(timezone=True), nullable=False, index=True)
    window_end = Column(DateTime(timezone=True), nullable=False)

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('idx_trending_score', 'time_window', 'trending_score'),
        Index('idx_trending_window', 'ticker_id', 'time_window', 'window_start', unique=True),
    )


class TrendingPattern(Base):
    """Trending patterns based on community discussions"""
    __tablename__ = "trending_patterns"

    id = Column(Integer, primary_key=True, index=True)
    pattern_type = Column(String(50), nullable=False, index=True)

    # Activity metrics
    mention_count = Column(Integer, default=0)
    post_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)  # Successful trades with this pattern
    failure_count = Column(Integer, default=0)

    # Performance
    avg_return = Column(Float, nullable=True)
    success_rate = Column(Float, nullable=True)

    # Trending score
    trending_score = Column(Float, default=0.0)

    # Time window
    time_window = Column(String(20), default="7d")
    window_start = Column(DateTime(timezone=True), nullable=False, index=True)
    window_end = Column(DateTime(timezone=True), nullable=False)

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('idx_pattern_trending', 'time_window', 'trending_score'),
    )
