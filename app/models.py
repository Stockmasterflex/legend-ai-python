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

class Portfolio(Base):
    """Portfolio tracking for users"""
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, default="default")
    name = Column(String(255), default="My Portfolio")
    initial_capital = Column(Float, nullable=False)
    cash_balance = Column(Float, nullable=False)
    total_value = Column(Float, nullable=True)  # Cached total portfolio value
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Position(Base):
    """Individual position tracking with cost basis"""
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True)
    quantity = Column(Float, nullable=False)
    avg_cost_basis = Column(Float, nullable=False)  # Average entry price
    current_price = Column(Float, nullable=True)  # Latest market price
    total_cost = Column(Float, nullable=False)  # Total invested
    current_value = Column(Float, nullable=True)  # Current market value
    unrealized_pnl = Column(Float, nullable=True)  # Unrealized profit/loss
    unrealized_pnl_pct = Column(Float, nullable=True)  # Unrealized P&L percentage
    stop_loss = Column(Float, nullable=True)
    target_price = Column(Float, nullable=True)
    position_size_pct = Column(Float, nullable=True)  # % of portfolio
    status = Column(String(20), default="open", index=True)  # open, closed, partial
    opened_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class TradeJournal(Base):
    """Comprehensive trade journal with lessons learned"""
    __tablename__ = "trade_journals"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), index=True)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True)
    trade_type = Column(String(20), index=True)  # "entry", "exit", "add", "trim"
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    entry_reason = Column(Text)  # Why entered the trade
    exit_reason = Column(Text, nullable=True)  # Why exited (if applicable)
    setup_type = Column(String(100), nullable=True)  # Pattern/setup used
    screenshot_url = Column(Text, nullable=True)  # Chart screenshot URL
    lessons_learned = Column(Text, nullable=True)  # Post-trade reflection
    emotions = Column(String(255), nullable=True)  # Emotional state during trade
    tags = Column(Text, nullable=True)  # Comma-separated tags (win, loss, breakout, etc.)
    r_multiple = Column(Float, nullable=True)  # Risk multiple achieved
    profit_loss = Column(Float, nullable=True)  # Realized P&L for exits
    profit_loss_pct = Column(Float, nullable=True)  # P&L percentage
    trade_grade = Column(String(5), nullable=True)  # A+, A, B, C, D, F
    mistakes_made = Column(Text, nullable=True)  # What went wrong
    what_went_well = Column(Text, nullable=True)  # What went right
    traded_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
