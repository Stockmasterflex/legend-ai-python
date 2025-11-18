"""
Database models for Legend AI
Phase 1.5: Database Integration
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, ForeignKey, JSON
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


class ScheduledPost(Base):
    """Scheduled social media posts"""
    __tablename__ = "scheduled_posts"

    id = Column(Integer, primary_key=True, index=True)
    content_type = Column(String(50), index=True)  # "tweet", "chart_annotation", "performance_summary", "pattern_explanation"
    platforms = Column(JSON)  # ["twitter", "stocktwits", "linkedin", "reddit"]
    ticker_id = Column(Integer, ForeignKey("tickers.id"), nullable=True, index=True)
    pattern_scan_id = Column(Integer, ForeignKey("pattern_scans.id"), nullable=True, index=True)
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    image_url = Column(Text, nullable=True)  # Chart image or other media
    hashtags = Column(JSON, nullable=True)  # ["trading", "stockmarket", "technicalanalysis"]
    scheduled_time = Column(DateTime(timezone=True), index=True)
    status = Column(String(20), default="pending", index=True)  # "pending", "posted", "failed", "cancelled"
    posted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    error_message = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)  # Additional metadata


class PostLog(Base):
    """Log of posted content across platforms"""
    __tablename__ = "post_logs"

    id = Column(Integer, primary_key=True, index=True)
    scheduled_post_id = Column(Integer, ForeignKey("scheduled_posts.id"), nullable=True, index=True)
    platform = Column(String(50), index=True)  # "twitter", "stocktwits", "linkedin", "reddit"
    post_id = Column(String(255), nullable=True)  # Platform-specific post ID
    content = Column(Text, nullable=False)
    url = Column(Text, nullable=True)  # URL to the posted content
    posted_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    status = Column(String(20), default="success")  # "success", "failed"
    error_message = Column(Text, nullable=True)
    compliance_disclaimer = Column(Text, nullable=True)  # Disclaimer added to post


class PostAnalytics(Base):
    """Engagement analytics for posted content"""
    __tablename__ = "post_analytics"

    id = Column(Integer, primary_key=True, index=True)
    post_log_id = Column(Integer, ForeignKey("post_logs.id"), index=True)
    platform = Column(String(50), index=True)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)  # (likes + shares + comments) / impressions
    follower_count = Column(Integer, nullable=True)  # Follower count at time of check
    checked_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    metadata = Column(JSON, nullable=True)  # Additional platform-specific metrics


class CommunityEngagement(Base):
    """Community engagement actions (replies, follows, DMs)"""
    __tablename__ = "community_engagements"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), index=True)
    engagement_type = Column(String(50), index=True)  # "reply", "follow", "dm", "like", "share"
    target_user = Column(String(255), nullable=True)  # Username or user ID
    target_post_id = Column(String(255), nullable=True)  # Post/tweet ID
    content = Column(Text, nullable=True)  # Reply or DM content
    status = Column(String(20), default="pending", index=True)  # "pending", "completed", "failed"
    executed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    error_message = Column(Text, nullable=True)


class ComplianceLog(Base):
    """Compliance and disclaimer tracking"""
    __tablename__ = "compliance_logs"

    id = Column(Integer, primary_key=True, index=True)
    post_log_id = Column(Integer, ForeignKey("post_logs.id"), nullable=True, index=True)
    compliance_type = Column(String(50), index=True)  # "sec_disclaimer", "risk_warning", "performance_disclaimer"
    disclaimer_text = Column(Text, nullable=False)
    platform = Column(String(50), index=True)
    added_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    verified = Column(Boolean, default=False)  # Manual verification flag
