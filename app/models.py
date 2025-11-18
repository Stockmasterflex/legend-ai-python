"""
Database models for Legend AI
Phase 1.5: Database Integration
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

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

class UserProgress(Base):
    """User progress and gamification tracking"""
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), unique=True, index=True, nullable=False)
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    total_scans = Column(Integer, default=0)
    patterns_detected = Column(Integer, default=0)
    stocks_analyzed = Column(Integer, default=0)
    watchlist_items = Column(Integer, default=0)
    profitable_ideas = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_active_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Achievement(Base):
    """Available achievements"""
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    achievement_key = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(50))  # "patterns", "analysis", "watchlist", "streak"
    icon = Column(String(50))  # emoji or icon name
    required_count = Column(Integer, default=1)
    xp_reward = Column(Integer, default=100)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserAchievement(Base):
    """User unlocked achievements"""
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), index=True)
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    notified = Column(Boolean, default=False)

class TutorialProgress(Base):
    """User tutorial progress"""
    __tablename__ = "tutorial_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, nullable=False)
    tutorial_key = Column(String(100), index=True)  # "onboarding", "vcp_pattern", etc.
    step_number = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    skipped = Column(Boolean, default=False)
    last_viewed_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

class ActivityLog(Base):
    """User activity log for XP tracking"""
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, nullable=False)
    activity_type = Column(String(50), index=True)  # "scan", "analyze", "watchlist_add", etc.
    xp_earned = Column(Integer, default=0)
    metadata = Column(Text)  # JSON with activity details
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

class LearningContent(Base):
    """Educational content for learning center"""
    __tablename__ = "learning_content"

    id = Column(Integer, primary_key=True, index=True)
    content_key = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(String(50), index=True)  # "pattern", "strategy", "glossary", "tutorial"
    content_type = Column(String(50))  # "article", "video", "interactive"
    content = Column(Text)  # Markdown or HTML content
    video_url = Column(String(500), nullable=True)
    difficulty = Column(String(20))  # "beginner", "intermediate", "advanced"
    estimated_time = Column(Integer)  # minutes
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class UserLearningProgress(Base):
    """Track user progress through learning content"""
    __tablename__ = "user_learning_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, nullable=False)
    content_id = Column(Integer, ForeignKey("learning_content.id"), index=True)
    progress = Column(Integer, default=0)  # percentage 0-100
    completed = Column(Boolean, default=False)
    bookmarked = Column(Boolean, default=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    last_viewed_at = Column(DateTime(timezone=True), server_default=func.now())

class CommunityStats(Base):
    """Aggregate community statistics"""
    __tablename__ = "community_stats"

    id = Column(Integer, primary_key=True, index=True)
    stat_date = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    total_scans = Column(Integer, default=0)
    total_patterns = Column(Integer, default=0)
    top_pattern_type = Column(String(50))
    top_ticker = Column(String(10))
    active_users = Column(Integer, default=0)
    patterns_by_type = Column(Text)  # JSON with pattern type counts
