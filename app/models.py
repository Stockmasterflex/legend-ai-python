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

class Backtest(Base):
    """Backtest configuration and results"""
    __tablename__ = "backtests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    strategy_type = Column(String(100), index=True)  # "pattern_based", "indicator_based", "custom"
    strategy_config = Column(Text)  # JSON configuration of strategy
    ticker = Column(String(10), nullable=True)  # Null means multiple tickers
    universe = Column(String(50), nullable=True)  # "SP500", "NASDAQ100", etc.
    start_date = Column(DateTime(timezone=True), nullable=False, index=True)
    end_date = Column(DateTime(timezone=True), nullable=False, index=True)
    initial_capital = Column(Float, nullable=False)
    position_sizing_method = Column(String(50))  # "fixed", "percent", "kelly", "risk_based"
    risk_per_trade = Column(Float)  # Risk percentage per trade
    commission_per_trade = Column(Float, default=0.0)
    slippage_percent = Column(Float, default=0.0)

    # Performance metrics
    final_capital = Column(Float)
    total_return = Column(Float)
    total_return_pct = Column(Float)
    sharpe_ratio = Column(Float)
    sortino_ratio = Column(Float)
    max_drawdown = Column(Float)
    max_drawdown_pct = Column(Float)
    calmar_ratio = Column(Float)
    win_rate = Column(Float)
    loss_rate = Column(Float)
    total_trades = Column(Integer)
    winning_trades = Column(Integer)
    losing_trades = Column(Integer)
    avg_win = Column(Float)
    avg_loss = Column(Float)
    largest_win = Column(Float)
    largest_loss = Column(Float)
    profit_factor = Column(Float)
    expectancy = Column(Float)
    avg_trade_duration_days = Column(Float)

    # Monte Carlo results
    monte_carlo_runs = Column(Integer, nullable=True)
    monte_carlo_mean_return = Column(Float, nullable=True)
    monte_carlo_std_return = Column(Float, nullable=True)
    monte_carlo_var_95 = Column(Float, nullable=True)  # Value at Risk 95%

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(20), default="pending")  # "pending", "running", "completed", "failed"
    error_message = Column(Text, nullable=True)

class BacktestTrade(Base):
    """Individual trade from a backtest"""
    __tablename__ = "backtest_trades"

    id = Column(Integer, primary_key=True, index=True)
    backtest_id = Column(Integer, ForeignKey("backtests.id"), index=True, nullable=False)
    ticker = Column(String(10), nullable=False, index=True)
    signal_type = Column(String(50))  # Pattern or indicator that triggered entry

    # Entry details
    entry_date = Column(DateTime(timezone=True), nullable=False, index=True)
    entry_price = Column(Float, nullable=False)
    entry_reason = Column(Text)

    # Position details
    position_size = Column(Integer, nullable=False)  # Number of shares
    position_value = Column(Float, nullable=False)  # Total position value
    stop_loss = Column(Float)
    target_price = Column(Float)

    # Exit details
    exit_date = Column(DateTime(timezone=True), nullable=True, index=True)
    exit_price = Column(Float, nullable=True)
    exit_reason = Column(String(100))  # "target", "stop_loss", "signal", "end_of_period"

    # Performance
    profit_loss = Column(Float)
    profit_loss_pct = Column(Float)
    r_multiple = Column(Float)  # Profit/loss relative to risk
    commission_paid = Column(Float, default=0.0)
    duration_days = Column(Integer)
    mae = Column(Float)  # Maximum Adverse Excursion
    mfe = Column(Float)  # Maximum Favorable Excursion

    # Status
    status = Column(String(20))  # "open", "closed", "stopped"
    is_win = Column(Boolean)
