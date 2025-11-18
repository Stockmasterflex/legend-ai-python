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

class TradePlan(Base):
    """AI-generated trade plans with multi-scenario analysis"""
    __tablename__ = "trade_plans"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True)
    user_id = Column(String(100), index=True, default="default")

    # Pattern Analysis
    pattern_type = Column(String(50), index=True)  # VCP, Cup & Handle, etc.
    pattern_score = Column(Float)  # Confidence score 0-10
    current_price = Column(Float)

    # Entry Zones
    entry_zone_low = Column(Float)
    entry_zone_high = Column(Float)
    optimal_entry = Column(Float)

    # Stop Levels
    initial_stop = Column(Float)
    trailing_stop = Column(Float, nullable=True)
    invalidation_price = Column(Float)  # Pattern invalidation level

    # Multi-Scenario Targets
    best_case_target = Column(Float)
    best_case_rr = Column(Float)  # Risk/reward for best case
    base_case_target = Column(Float)
    base_case_rr = Column(Float)
    worst_case_target = Column(Float, nullable=True)
    worst_case_rr = Column(Float, nullable=True)

    # Position Sizing
    account_size = Column(Float)
    risk_percentage = Column(Float, default=2.0)  # % of account to risk
    position_size = Column(Integer)  # Number of shares
    position_value = Column(Float)  # Dollar value
    risk_amount = Column(Float)  # Dollar risk

    # Plan Details
    timeframe = Column(String(20))  # "1day", "1week", etc.
    strategy = Column(String(50))  # "swing", "position", "momentum"
    notes = Column(Text)  # AI-generated analysis and notes
    checklist = Column(Text)  # JSON string of pre-trade checklist items
    alerts_config = Column(Text)  # JSON string of alert configurations

    # Trade Execution Tracking
    status = Column(String(20), default="planned", index=True)  # planned, active, completed, cancelled
    entry_date = Column(DateTime(timezone=True), nullable=True)
    exit_date = Column(DateTime(timezone=True), nullable=True)
    entry_price_actual = Column(Float, nullable=True)
    exit_price_actual = Column(Float, nullable=True)

    # Outcome Tracking
    outcome = Column(String(20), nullable=True, index=True)  # "win", "loss", "breakeven", "stopped"
    pnl_amount = Column(Float, nullable=True)  # Profit/loss in dollars
    pnl_percentage = Column(Float, nullable=True)  # Profit/loss %
    target_hit = Column(String(20), nullable=True)  # "best", "base", "worst", "none"
    lessons_learned = Column(Text, nullable=True)  # Post-trade analysis

    # PDF Export
    pdf_path = Column(String(255), nullable=True)  # Path to generated PDF
    chart_url = Column(Text, nullable=True)  # URL to chart image

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class TradePlanAlert(Base):
    """Smart alerts for trade plans"""
    __tablename__ = "trade_plan_alerts"

    id = Column(Integer, primary_key=True, index=True)
    trade_plan_id = Column(Integer, ForeignKey("trade_plans.id"), index=True)
    alert_type = Column(String(50), index=True)  # "entry_zone", "stop_loss", "target_hit", "invalidation"
    trigger_price = Column(Float)
    is_triggered = Column(Boolean, default=False, index=True)
    triggered_at = Column(DateTime(timezone=True), nullable=True)
    notification_sent = Column(Boolean, default=False)
    notification_sent_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
