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

class Venue(Base):
    """Trading venue/broker information"""
    __tablename__ = "venues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)  # "Alpaca", "Interactive Brokers", etc.
    venue_type = Column(String(50), nullable=False)  # "broker", "dark_pool", "exchange"
    is_active = Column(Boolean, default=True)
    commission_rate = Column(Float, default=0.0)  # Commission per share or percentage
    commission_type = Column(String(20), default="per_share")  # "per_share", "percentage", "flat"
    min_commission = Column(Float, default=0.0)
    liquidity_score = Column(Float, nullable=True)  # 0-100 score
    avg_fill_quality = Column(Float, nullable=True)  # Historical fill quality metric
    supports_dark_pool = Column(Boolean, default=False)
    supports_iceberg = Column(Boolean, default=False)
    api_endpoint = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ExecutionOrder(Base):
    """Parent execution order"""
    __tablename__ = "execution_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(50), unique=True, nullable=False, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True)
    side = Column(String(10), nullable=False)  # "buy", "sell"
    order_type = Column(String(50), nullable=False)  # "market", "limit", "twap", "vwap", "pov", "is"
    total_quantity = Column(Integer, nullable=False)
    filled_quantity = Column(Integer, default=0)
    remaining_quantity = Column(Integer, nullable=False)
    limit_price = Column(Float, nullable=True)
    avg_fill_price = Column(Float, nullable=True)
    status = Column(String(20), nullable=False, index=True)  # "pending", "active", "completed", "cancelled", "failed"

    # Execution algorithm parameters
    algo_type = Column(String(50), nullable=True)  # "twap", "vwap", "pov", "is"
    algo_params = Column(Text, nullable=True)  # JSON of algo parameters

    # Timing
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, nullable=True)

    # Analytics
    slippage_bps = Column(Float, nullable=True)  # Slippage in basis points
    total_cost = Column(Float, nullable=True)
    market_impact_bps = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ChildOrder(Base):
    """Child orders from order slicing"""
    __tablename__ = "child_orders"

    id = Column(Integer, primary_key=True, index=True)
    child_order_id = Column(String(50), unique=True, nullable=False, index=True)
    parent_order_id = Column(Integer, ForeignKey("execution_orders.id"), index=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), index=True, nullable=True)

    quantity = Column(Integer, nullable=False)
    filled_quantity = Column(Integer, default=0)
    limit_price = Column(Float, nullable=True)
    fill_price = Column(Float, nullable=True)

    status = Column(String(20), nullable=False)  # "pending", "sent", "filled", "partial", "cancelled"
    is_iceberg = Column(Boolean, default=False)
    display_quantity = Column(Integer, nullable=True)  # For iceberg orders

    # Routing
    route_type = Column(String(50), nullable=True)  # "smart", "direct", "dark_pool"

    submitted_at = Column(DateTime(timezone=True), nullable=True)
    filled_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

class ExecutionMetrics(Base):
    """Execution quality metrics and analytics"""
    __tablename__ = "execution_metrics"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("execution_orders.id"), index=True)

    # Benchmark prices
    arrival_price = Column(Float, nullable=True)  # Price when order received
    vwap_benchmark = Column(Float, nullable=True)  # Market VWAP during execution
    twap_benchmark = Column(Float, nullable=True)  # Market TWAP during execution

    # Performance metrics
    slippage_vs_arrival = Column(Float, nullable=True)  # Basis points
    slippage_vs_vwap = Column(Float, nullable=True)
    slippage_vs_twap = Column(Float, nullable=True)

    # Cost analysis
    total_commission = Column(Float, nullable=True)
    price_improvement = Column(Float, nullable=True)  # If negative, it's price deterioration
    opportunity_cost = Column(Float, nullable=True)

    # Market impact
    participation_rate = Column(Float, nullable=True)  # % of market volume
    market_impact_bps = Column(Float, nullable=True)

    # Venue performance
    venue_breakdown = Column(Text, nullable=True)  # JSON of fills by venue
    dark_pool_fills = Column(Integer, default=0)
    dark_pool_fill_rate = Column(Float, nullable=True)

    calculated_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

class VenuePerformance(Base):
    """Historical venue performance tracking"""
    __tablename__ = "venue_performance"

    id = Column(Integer, primary_key=True, index=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=True)

    # Performance metrics
    total_orders = Column(Integer, default=0)
    avg_fill_time_ms = Column(Float, nullable=True)
    fill_rate = Column(Float, nullable=True)  # % of orders filled
    avg_slippage_bps = Column(Float, nullable=True)
    price_improvement_bps = Column(Float, nullable=True)

    # Time period
    period_start = Column(DateTime(timezone=True), index=True)
    period_end = Column(DateTime(timezone=True), index=True)

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
