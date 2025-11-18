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

class MacroEvent(Base):
    """Economic calendar and macro events"""
    __tablename__ = "macro_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(50), index=True)  # "FOMC", "CPI", "PPI", "GDP", "UNEMPLOYMENT", "EARNINGS", "OPTIONS_EXP", "DIVIDEND"
    event_name = Column(String(255), nullable=False)
    event_date = Column(DateTime(timezone=True), index=True, nullable=False)
    event_time = Column(String(20), nullable=True)  # "09:30 ET", "14:00 ET", etc.
    importance = Column(String(20), index=True)  # "HIGH", "MEDIUM", "LOW"
    previous_value = Column(Float, nullable=True)
    forecast_value = Column(Float, nullable=True)
    actual_value = Column(Float, nullable=True)
    country = Column(String(10), default="US")
    source = Column(String(50))  # API source
    description = Column(Text, nullable=True)
    url = Column(String(500), nullable=True)  # Link to more info
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class EventImpact(Base):
    """Historical market reaction to macro events"""
    __tablename__ = "event_impacts"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("macro_events.id"), index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=True)  # NULL for market indices
    symbol = Column(String(20), index=True)  # "SPY", "QQQ", "IWM", sector tickers
    price_before = Column(Float, nullable=False)
    price_after_1h = Column(Float, nullable=True)
    price_after_1d = Column(Float, nullable=True)
    price_after_1w = Column(Float, nullable=True)
    volatility_before = Column(Float, nullable=True)  # ATR or IV
    volatility_after = Column(Float, nullable=True)
    volume_ratio = Column(Float, nullable=True)  # Volume vs average
    percent_change_1h = Column(Float, nullable=True)
    percent_change_1d = Column(Float, nullable=True)
    percent_change_1w = Column(Float, nullable=True)
    direction = Column(String(10), nullable=True)  # "UP", "DOWN", "NEUTRAL"
    magnitude = Column(String(20), nullable=True)  # "EXTREME", "HIGH", "MODERATE", "LOW"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MarketRegime(Base):
    """Market regime detection and tracking"""
    __tablename__ = "market_regimes"

    id = Column(Integer, primary_key=True, index=True)
    detection_date = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    regime_type = Column(String(50), index=True)  # "BULL", "BEAR", "SIDEWAYS"
    volatility_regime = Column(String(50), index=True)  # "HIGH_VOL", "LOW_VOL", "NORMAL"
    rate_environment = Column(String(50), index=True)  # "RISING", "FALLING", "STABLE"
    seasonal_pattern = Column(String(50), nullable=True)  # "SELL_IN_MAY", "SANTA_RALLY", "JANUARY_EFFECT"
    vix_level = Column(Float, nullable=True)
    vix_percentile = Column(Float, nullable=True)  # Historical percentile
    trend_strength = Column(Float, nullable=True)  # ADX or similar
    market_breadth = Column(Float, nullable=True)  # Advance/decline ratio
    fed_funds_rate = Column(Float, nullable=True)
    rate_trend = Column(String(20), nullable=True)  # "HIKING", "CUTTING", "PAUSE"
    confidence_score = Column(Float, nullable=True)  # 0-100 confidence in regime
    indicators = Column(JSON, nullable=True)  # Supporting indicators as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
