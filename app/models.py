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

class AlertRule(Base):
    """User-defined alert rules with conditions"""
    __tablename__ = "alert_rules"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, default="default")
    name = Column(String(200), nullable=False)  # User-friendly name
    description = Column(Text, nullable=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=True)  # None for global rules
    alert_type = Column(String(50), index=True, nullable=False)  # "price", "pattern", "volume", "indicator", "news", "options_flow"

    # Condition logic
    condition_logic = Column(String(10), default="AND")  # "AND" or "OR" for multiple conditions
    conditions = Column(JSON, nullable=False)  # List of conditions [{field, operator, value}]

    # Delivery settings
    delivery_channels = Column(JSON, nullable=False)  # ["telegram", "email", "sms", "discord", "slack", "webhook", "push"]
    delivery_config = Column(JSON, nullable=True)  # Channel-specific config (webhook URLs, etc.)

    # Schedule and control
    is_enabled = Column(Boolean, default=True, index=True)
    is_snoozed = Column(Boolean, default=False)
    snoozed_until = Column(DateTime(timezone=True), nullable=True)
    check_frequency = Column(Integer, default=60)  # Seconds between checks
    cooldown_period = Column(Integer, default=3600)  # Seconds before re-alerting
    last_triggered_at = Column(DateTime(timezone=True), nullable=True, index=True)
    trigger_count = Column(Integer, default=0)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String(50), default="user")  # "user" or "ai" for AI-suggested alerts

class AlertCondition(Base):
    """Individual conditions for alert rules"""
    __tablename__ = "alert_conditions"

    id = Column(Integer, primary_key=True, index=True)
    rule_id = Column(Integer, ForeignKey("alert_rules.id", ondelete="CASCADE"), index=True)

    # Condition definition
    field = Column(String(100), nullable=False)  # "price", "volume", "rsi", "macd", "sentiment", etc.
    operator = Column(String(20), nullable=False)  # "greater_than", "less_than", "equals", "crosses_above", "crosses_below", "percentage_change"
    value = Column(Float, nullable=False)
    value_type = Column(String(20), default="absolute")  # "absolute", "percentage", "ratio"

    # Time-based conditions
    time_window = Column(Integer, nullable=True)  # Time window in seconds (e.g., "volume > X in last 5 minutes")
    comparison_period = Column(String(50), nullable=True)  # "1min", "5min", "1hour", "1day", etc.

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AlertLog(Base):
    """Alert trigger history with comprehensive tracking"""
    __tablename__ = "alert_logs"

    id = Column(Integer, primary_key=True, index=True)
    rule_id = Column(Integer, ForeignKey("alert_rules.id", ondelete="SET NULL"), index=True, nullable=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=True)
    user_id = Column(String(100), index=True, default="default")

    # Alert details
    alert_type = Column(String(50), index=True)  # "price", "pattern", "volume", "indicator", "news", "options_flow"
    alert_title = Column(String(200))
    alert_message = Column(Text)

    # Trigger information
    trigger_price = Column(Float, nullable=True)
    trigger_value = Column(Float, nullable=True)
    trigger_data = Column(JSON, nullable=True)  # Additional trigger context
    conditions_met = Column(JSON, nullable=True)  # Which conditions were met

    # Delivery tracking
    delivery_channels = Column(JSON)  # Channels alert was sent to
    delivery_status = Column(JSON)  # Status per channel
    sent_via = Column(String(200))  # Comma-separated list for backward compatibility

    # Status
    status = Column(String(20), default="sent", index=True)  # "sent", "failed", "acknowledged", "dismissed"
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    dismissed_at = Column(DateTime(timezone=True), nullable=True)

    # Performance tracking
    response_time_ms = Column(Integer, nullable=True)  # Time taken to evaluate and send

    # Timestamps
    alert_sent_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

class AlertDelivery(Base):
    """Track delivery attempts per channel"""
    __tablename__ = "alert_deliveries"

    id = Column(Integer, primary_key=True, index=True)
    alert_log_id = Column(Integer, ForeignKey("alert_logs.id", ondelete="CASCADE"), index=True)

    # Delivery details
    channel = Column(String(50), index=True)  # "telegram", "email", "sms", "discord", "slack", "webhook", "push"
    status = Column(String(20), default="pending")  # "pending", "sent", "failed", "retrying"

    # Attempt tracking
    attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)
    last_attempt_at = Column(DateTime(timezone=True), nullable=True)
    next_retry_at = Column(DateTime(timezone=True), nullable=True)

    # Result
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    failed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)

    # Channel-specific metadata
    external_id = Column(String(200), nullable=True)  # Message ID from external service
    channel_metadata = Column(JSON, nullable=True)  # Channel-specific data

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
