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

class EarningsCalendar(Base):
    """Earnings calendar and historical data"""
    __tablename__ = "earnings_calendar"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=False)
    earnings_date = Column(DateTime(timezone=True), index=True, nullable=False)
    fiscal_quarter = Column(String(10))  # "Q1", "Q2", "Q3", "Q4"
    fiscal_year = Column(Integer)
    report_time = Column(String(10))  # "BMO" (before market open), "AMC" (after market close), "TNS" (time not supplied)

    # Consensus estimates
    eps_estimate = Column(Float, nullable=True)
    revenue_estimate = Column(Float, nullable=True)  # In millions

    # Actual results (filled after earnings release)
    eps_actual = Column(Float, nullable=True)
    revenue_actual = Column(Float, nullable=True)  # In millions

    # Beat/miss metrics
    eps_surprise = Column(Float, nullable=True)  # Difference: actual - estimate
    eps_surprise_pct = Column(Float, nullable=True)  # Percentage: (actual - estimate) / estimate * 100
    revenue_surprise = Column(Float, nullable=True)
    revenue_surprise_pct = Column(Float, nullable=True)

    # Status
    is_confirmed = Column(Boolean, default=False)  # Whether date is confirmed
    has_reported = Column(Boolean, default=False, index=True)  # Whether earnings have been reported

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class EarningsReaction(Base):
    """Pre/Post earnings price reaction analysis"""
    __tablename__ = "earnings_reactions"

    id = Column(Integer, primary_key=True, index=True)
    earnings_id = Column(Integer, ForeignKey("earnings_calendar.id"), index=True, nullable=False)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=False)

    # Pre-earnings data (day before earnings)
    pre_close_price = Column(Float, nullable=True)
    pre_volume = Column(Float, nullable=True)
    pre_iv = Column(Float, nullable=True)  # Implied volatility before earnings

    # Post-earnings data (gap on earnings day)
    post_open_price = Column(Float, nullable=True)
    post_close_price = Column(Float, nullable=True)
    post_volume = Column(Float, nullable=True)
    post_iv = Column(Float, nullable=True)  # Implied volatility after earnings

    # Gap and move analysis
    gap_percent = Column(Float, nullable=True)  # (post_open - pre_close) / pre_close * 100
    day_move_percent = Column(Float, nullable=True)  # (post_close - pre_close) / pre_close * 100
    intraday_move_percent = Column(Float, nullable=True)  # Max intraday move

    # Volume analysis
    volume_ratio = Column(Float, nullable=True)  # post_volume / avg_volume
    relative_volume = Column(Float, nullable=True)  # vs 20-day average

    # Volatility metrics
    iv_change = Column(Float, nullable=True)  # Change in implied volatility
    realized_vs_expected = Column(Float, nullable=True)  # Actual move vs expected (from IV)

    # Multi-day reaction
    week_move_percent = Column(Float, nullable=True)  # Move 1 week after earnings
    month_move_percent = Column(Float, nullable=True)  # Move 1 month after earnings

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class EarningsAlert(Base):
    """Earnings-related alerts configuration and history"""
    __tablename__ = "earnings_alerts"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=False)
    user_id = Column(String(100), index=True, default="default")

    # Alert triggers
    alert_before_earnings = Column(Boolean, default=True)  # Alert N days before earnings
    days_before = Column(Integer, default=7)  # Alert 7 days before
    alert_on_surprise = Column(Boolean, default=True)  # Alert on significant beat/miss
    surprise_threshold = Column(Float, default=5.0)  # Alert if surprise > 5%
    alert_on_gap = Column(Boolean, default=True)  # Alert on significant gap
    gap_threshold = Column(Float, default=3.0)  # Alert if gap > 3%
    alert_on_volume = Column(Boolean, default=True)  # Alert on unusual volume
    volume_threshold = Column(Float, default=2.0)  # Alert if volume > 2x average
    alert_on_pattern = Column(Boolean, default=True)  # Alert on post-earnings pattern

    # Last alert tracking
    last_alert_type = Column(String(50), nullable=True)
    last_alert_sent = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
