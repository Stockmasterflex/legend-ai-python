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

class TradingViewAlert(Base):
    """TradingView webhook alerts"""
    __tablename__ = "tradingview_alerts"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=True)
    symbol = Column(String(20), index=True, nullable=False)  # Raw symbol from TradingView
    alert_type = Column(String(50), index=True)  # "price", "indicator", "pattern", "breakout", "stop_loss"
    alert_name = Column(String(255))  # Name of the alert in TradingView
    message = Column(Text)  # Full alert message/payload
    trigger_price = Column(Float, nullable=True)
    trigger_time = Column(String(100), nullable=True)  # TradingView timestamp
    interval = Column(String(20), nullable=True)  # Timeframe: 1m, 5m, 15m, 1h, 4h, 1D, 1W
    indicator_values = Column(Text, nullable=True)  # JSON string of indicator values
    strategy_name = Column(String(100), nullable=True)  # Strategy that triggered the alert
    action = Column(String(20), nullable=True)  # "buy", "sell", "long", "short", "exit"
    processed = Column(Boolean, default=False, index=True)  # Whether alert has been processed
    confirmed = Column(Boolean, default=False)  # Whether pattern/signal was confirmed by Legend AI
    legend_score = Column(Float, nullable=True)  # Legend AI confirmation score
    webhook_ip = Column(String(50), nullable=True)  # IP address of webhook sender
    received_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)

class TradingViewStrategy(Base):
    """TradingView strategies imported for backtesting"""
    __tablename__ = "tradingview_strategies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    pine_script_code = Column(Text, nullable=True)  # Optional Pine Script code
    strategy_config = Column(Text)  # JSON string of strategy parameters
    timeframe = Column(String(20))  # Default timeframe for strategy
    indicators_used = Column(Text)  # JSON array of indicators
    entry_conditions = Column(Text)  # JSON description of entry rules
    exit_conditions = Column(Text)  # JSON description of exit rules
    risk_reward_ratio = Column(Float, nullable=True)
    win_rate = Column(Float, nullable=True)  # Historical win rate from TradingView
    profit_factor = Column(Float, nullable=True)
    max_drawdown = Column(Float, nullable=True)
    total_trades = Column(Integer, nullable=True)
    backtest_results = Column(Text, nullable=True)  # JSON of Legend AI backtest results
    legend_optimized = Column(Boolean, default=False)  # Whether optimized by Legend AI
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class TradingViewSync(Base):
    """Bidirectional sync between Legend AI and TradingView"""
    __tablename__ = "tradingview_sync"

    id = Column(Integer, primary_key=True, index=True)
    sync_type = Column(String(50), index=True)  # "watchlist", "pattern", "alert", "chart"
    legend_id = Column(Integer, nullable=True)  # ID in Legend AI system (pattern_scan, watchlist, etc.)
    tradingview_alert_id = Column(String(255), nullable=True)  # TradingView alert ID
    symbol = Column(String(20), index=True)
    direction = Column(String(20))  # "legend_to_tv", "tv_to_legend", "bidirectional"
    status = Column(String(20), default="pending")  # "pending", "synced", "failed"
    sync_data = Column(Text)  # JSON of sync payload
    error_message = Column(Text, nullable=True)
    last_synced_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
