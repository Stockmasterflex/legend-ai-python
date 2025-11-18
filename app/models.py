"""
Database models for Legend AI
Phase 1.5: Database Integration
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
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


# Tax Optimization Models

class HoldingPeriodEnum(enum.Enum):
    """Tax holding period classification"""
    SHORT_TERM = "short_term"  # <= 1 year
    LONG_TERM = "long_term"    # > 1 year


class WashSaleStatusEnum(enum.Enum):
    """Wash sale status"""
    CLEAN = "clean"
    VIOLATION = "violation"
    PENDING = "pending"


class TaxLot(Base):
    """Individual tax lot tracking for securities purchases"""
    __tablename__ = "tax_lots"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, default="default")
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=False)
    symbol = Column(String(10), index=True, nullable=False)

    # Purchase information
    quantity = Column(Float, nullable=False)
    remaining_quantity = Column(Float, nullable=False)  # After partial sales
    cost_basis = Column(Float, nullable=False)  # Total cost
    price_per_share = Column(Float, nullable=False)
    purchase_date = Column(DateTime(timezone=True), nullable=False, index=True)

    # Tax information
    holding_period = Column(Enum(HoldingPeriodEnum), nullable=True)
    wash_sale_disallowed = Column(Float, default=0.0)  # Loss disallowed due to wash sale
    adjusted_cost_basis = Column(Float, nullable=False)  # After wash sale adjustments

    # Metadata
    trade_id = Column(String(100), nullable=True, index=True)  # Link to original trade
    is_closed = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class CapitalGain(Base):
    """Realized capital gains and losses"""
    __tablename__ = "capital_gains"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, default="default")
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=False)
    symbol = Column(String(10), index=True, nullable=False)
    tax_lot_id = Column(Integer, ForeignKey("tax_lots.id"), index=True, nullable=False)

    # Sale information
    quantity = Column(Float, nullable=False)
    sale_price = Column(Float, nullable=False)
    sale_date = Column(DateTime(timezone=True), nullable=False, index=True)
    proceeds = Column(Float, nullable=False)  # quantity * sale_price

    # Cost basis
    cost_basis = Column(Float, nullable=False)
    adjusted_cost_basis = Column(Float, nullable=False)  # After wash sale adjustments

    # Gain/loss calculation
    gain_loss = Column(Float, nullable=False)  # proceeds - adjusted_cost_basis
    holding_period = Column(Enum(HoldingPeriodEnum), nullable=False)

    # Tax information
    wash_sale_loss_disallowed = Column(Float, default=0.0)
    tax_year = Column(Integer, index=True, nullable=False)

    # Metadata
    trade_id = Column(String(100), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class WashSale(Base):
    """Wash sale violation tracking (30-day rule)"""
    __tablename__ = "wash_sales"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, default="default")
    symbol = Column(String(10), index=True, nullable=False)

    # Loss sale information
    loss_sale_date = Column(DateTime(timezone=True), nullable=False, index=True)
    loss_amount = Column(Float, nullable=False)  # Negative value
    loss_quantity = Column(Float, nullable=False)
    loss_tax_lot_id = Column(Integer, ForeignKey("tax_lots.id"), nullable=False)

    # Replacement purchase information
    replacement_purchase_date = Column(DateTime(timezone=True), nullable=True, index=True)
    replacement_quantity = Column(Float, nullable=True)
    replacement_tax_lot_id = Column(Integer, ForeignKey("tax_lots.id"), nullable=True)

    # Wash sale details
    status = Column(Enum(WashSaleStatusEnum), nullable=False, default=WashSaleStatusEnum.PENDING)
    days_between = Column(Integer, nullable=True)  # Days between transactions
    disallowed_loss = Column(Float, default=0.0)  # Loss disallowed by IRS

    # Alternative suggestions
    suggested_alternatives = Column(JSON, nullable=True)  # List of similar securities

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)


class TaxHarvestLog(Base):
    """Tax loss harvesting opportunity and action log"""
    __tablename__ = "tax_harvest_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, default="default")

    # Opportunity details
    symbol = Column(String(10), index=True, nullable=False)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=False)
    tax_lot_id = Column(Integer, ForeignKey("tax_lots.id"), nullable=False)

    # Loss information
    unrealized_loss = Column(Float, nullable=False)  # Negative value
    current_price = Column(Float, nullable=False)
    cost_basis = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)

    # Tax benefit estimate
    estimated_tax_savings = Column(Float, nullable=False)
    tax_bracket = Column(Float, nullable=True)  # User's tax bracket

    # Action taken
    action_taken = Column(String(50), index=True)  # "harvested", "skipped", "pending"
    harvest_date = Column(DateTime(timezone=True), nullable=True)

    # Replacement security
    replacement_symbol = Column(String(10), nullable=True)
    replacement_similarity_score = Column(Float, nullable=True)  # 0-1, how similar

    # Metadata
    identified_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)  # When opportunity expires
    notes = Column(Text, nullable=True)
