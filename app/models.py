"""
Database models for Legend AI
Phase 1.5: Database Integration
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

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

class WatchlistGroup(Base):
    """Watchlist collections for organizing multiple watchlists"""
    __tablename__ = "watchlist_groups"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    color = Column(String(20), default="#3B82F6")  # Hex color code
    strategy = Column(String(100), nullable=True)  # Swing, Day Trading, Long-term, etc.
    position = Column(Integer, default=0)  # For drag-and-drop ordering
    is_default = Column(Boolean, default=False)
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
    group_id = Column(Integer, ForeignKey("watchlist_groups.id"), index=True, nullable=True)  # Watchlist group
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True)
    status = Column(String(50), default="Watching", index=True)  # "Watching", "Breaking Out", "Triggered", "Completed", "Skipped"

    # Organization fields
    color = Column(String(20), nullable=True)  # Individual ticker color (hex)
    category = Column(String(100), nullable=True)  # Auto-categorized or manual (e.g., "Technology", "Healthcare")
    pattern_type = Column(String(50), nullable=True, index=True)  # VCP, Cup & Handle, etc.
    position = Column(Integer, default=0)  # For drag-and-drop ordering within group
    strength_score = Column(Float, nullable=True)  # Overall strength for sorting (0-100)

    # Price targets
    target_entry = Column(Float, nullable=True)  # Expected entry price
    target_stop = Column(Float, nullable=True)  # Expected stop price
    target_price = Column(Float, nullable=True)  # Target price for take-profit

    # Notes and analysis
    reason = Column(Text)  # Why this ticker is on watchlist
    notes = Column(Text)  # Additional notes
    tags = Column(JSON, nullable=True)  # Flexible tagging system ["swing", "earnings-play"]

    # Alerts
    alerts_enabled = Column(Boolean, default=True)  # Enable/disable price alerts
    alert_threshold = Column(Float, nullable=True)  # Alert when price moves this %

    # Performance tracking
    entry_price = Column(Float, nullable=True)  # Actual entry price
    exit_price = Column(Float, nullable=True)  # Actual exit price
    profit_loss_pct = Column(Float, nullable=True)  # Performance if traded

    # Timestamps
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
