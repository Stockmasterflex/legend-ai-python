"""
Database models for Legend AI
Phase 1.5: Database Integration
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

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


# Trade Journaling System Models

class TradeStatus(enum.Enum):
    """Trade status enumeration"""
    PLANNED = "planned"
    OPEN = "open"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class EmotionalState(enum.Enum):
    """Emotional state during trade"""
    CONFIDENT = "confident"
    FEARFUL = "fearful"
    GREEDY = "greedy"
    NEUTRAL = "neutral"
    ANXIOUS = "anxious"
    DISCIPLINED = "disciplined"
    IMPULSIVE = "impulsive"


class MarketCondition(enum.Enum):
    """Market condition during trade"""
    TRENDING_UP = "trending_up"
    TRENDING_DOWN = "trending_down"
    CONSOLIDATING = "consolidating"
    VOLATILE = "volatile"
    QUIET = "quiet"


class TradeJournal(Base):
    """Comprehensive trade journal entry"""
    __tablename__ = "trade_journals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, default="default")
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True)
    pattern_scan_id = Column(Integer, ForeignKey("pattern_scans.id"), nullable=True, index=True)

    # Trade Identification
    trade_id = Column(String(50), unique=True, index=True)  # Unique trade identifier
    status = Column(SQLEnum(TradeStatus), default=TradeStatus.PLANNED, index=True)

    # Pre-Trade Planning
    pattern_identified = Column(String(100))  # Pattern type
    thesis = Column(Text)  # Trade thesis/reason
    planned_entry = Column(Float)
    planned_stop = Column(Float)
    planned_target = Column(Float)
    planned_position_size = Column(Integer)
    planned_risk_amount = Column(Float)
    planned_risk_reward = Column(Float)
    checklist_completed = Column(Boolean, default=False)
    checklist_data = Column(JSON, nullable=True)  # Pre-trade checklist items
    screenshot_url = Column(Text, nullable=True)  # Chart screenshot before entry

    # Actual Execution
    actual_entry_price = Column(Float, nullable=True)
    actual_stop_price = Column(Float, nullable=True)
    actual_target_price = Column(Float, nullable=True)
    actual_position_size = Column(Integer, nullable=True)
    entry_timestamp = Column(DateTime(timezone=True), nullable=True, index=True)
    exit_timestamp = Column(DateTime(timezone=True), nullable=True, index=True)

    # Slippage Tracking
    entry_slippage = Column(Float, nullable=True)  # Difference from planned
    exit_slippage = Column(Float, nullable=True)
    slippage_cost = Column(Float, nullable=True)  # Dollar cost of slippage

    # Exit Details
    exit_price = Column(Float, nullable=True)
    exit_reason = Column(String(100), nullable=True)  # "target", "stop", "manual", "trailing_stop"
    partial_exits = Column(JSON, nullable=True)  # List of partial exit records

    # Performance Metrics
    gross_pnl = Column(Float, nullable=True)
    net_pnl = Column(Float, nullable=True)  # After fees/slippage
    r_multiple = Column(Float, nullable=True)  # Actual R achieved
    fees_paid = Column(Float, nullable=True)
    holding_period_hours = Column(Float, nullable=True)
    mae = Column(Float, nullable=True)  # Maximum Adverse Excursion
    mfe = Column(Float, nullable=True)  # Maximum Favorable Excursion

    # Emotional & Market Context
    emotional_state_entry = Column(SQLEnum(EmotionalState), nullable=True)
    emotional_state_exit = Column(SQLEnum(EmotionalState), nullable=True)
    market_condition = Column(SQLEnum(MarketCondition), nullable=True)
    market_context = Column(Text, nullable=True)  # Market notes

    # Follow-through & Notes
    follow_through_notes = Column(Text, nullable=True)
    what_went_well = Column(Text, nullable=True)
    what_went_wrong = Column(Text, nullable=True)
    lessons_learned = Column(Text, nullable=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TradeTag(Base):
    """Tags for organizing trades"""
    __tablename__ = "trade_tags"

    id = Column(Integer, primary_key=True, index=True)
    trade_journal_id = Column(Integer, ForeignKey("trade_journals.id"), index=True)
    tag = Column(String(50), index=True)  # "lesson", "mistake", "perfect", "revenge_trade", etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TradeMistake(Base):
    """Categorized trade mistakes"""
    __tablename__ = "trade_mistakes"

    id = Column(Integer, primary_key=True, index=True)
    trade_journal_id = Column(Integer, ForeignKey("trade_journals.id"), index=True)
    category = Column(String(50), index=True)  # "entry", "exit", "sizing", "emotional", "planning"
    mistake_type = Column(String(100))  # "entered_too_early", "cut_winner_short", "oversized", etc.
    description = Column(Text)
    impact = Column(String(20))  # "minor", "moderate", "major"
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Playbook(Base):
    """Trading playbooks and strategies"""
    __tablename__ = "playbooks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, default="default")
    name = Column(String(100), index=True)  # "VCP Breakout Strategy"
    description = Column(Text)
    pattern_type = Column(String(50), index=True)  # Link to pattern
    entry_criteria = Column(JSON)  # List of entry rules
    exit_criteria = Column(JSON)  # List of exit rules
    risk_management = Column(JSON)  # Position sizing, stops, etc.
    success_rate = Column(Float, nullable=True)  # Calculated from trades
    avg_r_multiple = Column(Float, nullable=True)
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TradeLesson(Base):
    """Lessons learned from trading"""
    __tablename__ = "trade_lessons"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, default="default")
    title = Column(String(200))
    lesson = Column(Text)
    pattern_type = Column(String(50), nullable=True, index=True)
    importance = Column(String(20))  # "low", "medium", "high", "critical"
    trades_count = Column(Integer, default=0)  # How many trades taught this
    last_occurred = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TradeReview(Base):
    """Periodic trade reviews"""
    __tablename__ = "trade_reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, default="default")
    review_period = Column(String(20))  # "daily", "weekly", "monthly"
    start_date = Column(DateTime(timezone=True), index=True)
    end_date = Column(DateTime(timezone=True), index=True)

    # Summary Stats
    total_trades = Column(Integer)
    winning_trades = Column(Integer)
    losing_trades = Column(Integer)
    win_rate = Column(Float)
    avg_win = Column(Float)
    avg_loss = Column(Float)
    total_pnl = Column(Float)
    best_trade_id = Column(String(50), nullable=True)
    worst_trade_id = Column(String(50), nullable=True)

    # Review Notes
    review_notes = Column(Text)
    improvement_areas = Column(JSON)  # List of areas to improve
    goals_next_period = Column(JSON)  # Goals for next period

    created_at = Column(DateTime(timezone=True), server_default=func.now())
