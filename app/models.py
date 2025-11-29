"""
Database models for Legend AI
Phase 1.5: Database Integration
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, ForeignKey, BigInteger, JSON
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

class RSHistory(Base):
    """Relative Strength rating history for tracking changes over time"""
    __tablename__ = "rs_history"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id", ondelete="CASCADE"), index=True, nullable=False)
    rs_rating = Column(Integer, nullable=False, index=True)  # 0-99 percentile rank
    raw_score = Column(Float, nullable=True)  # Weighted performance score
    q1_performance = Column(Float, nullable=True)  # Quarter 1 performance %
    q2_performance = Column(Float, nullable=True)  # Quarter 2 performance %
    q3_performance = Column(Float, nullable=True)  # Quarter 3 performance %
    q4_performance = Column(Float, nullable=True)  # Quarter 4 (most recent) performance %
    one_year_performance = Column(Float, nullable=True)  # Total 1-year performance %
    percentile = Column(Float, nullable=True)  # Exact percentile (0-100)
    universe_rank = Column(Integer, nullable=True)  # Rank within universe
    universe_size = Column(Integer, nullable=True)  # Total stocks in universe
    calculated_at = Column(DateTime(timezone=True), server_default=func.now(), index=True, nullable=False)

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


class UniverseSymbol(Base):
    """Authorized universe ticker list (S&P 500 + NASDAQ 100)."""
    __tablename__ = "universe_symbols"

    symbol = Column(String(10), primary_key=True, index=True)
    name = Column(String(255))
    sector = Column(String(100))
    industry = Column(String(100))
    market_cap = Column(BigInteger)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Trade(Base):
    """Trade journal entries"""
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), index=True, nullable=False)
    pattern = Column(String(50))
    entry_date = Column(DateTime(timezone=True), index=True)
    entry_price = Column(Float, nullable=False)
    stop_price = Column(Float, nullable=False)
    target_price = Column(Float)
    exit_date = Column(DateTime(timezone=True), nullable=True, index=True)
    exit_price = Column(Float, nullable=True)
    shares = Column(Integer, nullable=False)
    profit_loss = Column(Float, nullable=True)  # Dollar P&L
    r_multiple = Column(Float, nullable=True)  # R achieved
    status = Column(String(20), default="Open", index=True)  # Open, Closed, Stopped
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

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
    """User portfolio container"""
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    name = Column(String(100))
    initial_capital = Column(Float)
    cash_balance = Column(Float)
    total_value = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Position(Base):
    """Individual portfolio position"""
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True)
    quantity = Column(Float)
    avg_cost_basis = Column(Float)
    total_cost = Column(Float)
    current_price = Column(Float, nullable=True)
    current_value = Column(Float, nullable=True)
    unrealized_pnl = Column(Float, nullable=True)
    unrealized_pnl_pct = Column(Float, nullable=True)
    stop_loss = Column(Float, nullable=True)
    target_price = Column(Float, nullable=True)
    position_size_pct = Column(Float, nullable=True)
    status = Column(String(20), default="open")  # open, closed, partial
    notes = Column(Text, nullable=True)
    opened_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# =====================================================================
# Backtesting Models
# =====================================================================

class Strategy(Base):
    """Trading strategy definition"""
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    strategy_type = Column(String(20), nullable=False)  # yaml, python, visual
    yaml_config = Column(Text, nullable=True)
    python_code = Column(Text, nullable=True)
    visual_config = Column(JSON, nullable=True)
    parameters = Column(JSON, nullable=True)
    entry_rules = Column(JSON, nullable=True)
    exit_rules = Column(JSON, nullable=True)
    risk_management = Column(JSON, nullable=True)
    template_id = Column(Integer, ForeignKey("strategy_templates.id"), nullable=True)
    version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class BacktestRun(Base):
    """Backtest execution record"""
    __tablename__ = "backtest_runs"

    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), index=True)
    name = Column(String(100))
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    initial_capital = Column(Float, default=100000.0)
    universe = Column(JSON)  # List of ticker symbols
    commission_model = Column(JSON, nullable=True)
    slippage_model = Column(JSON, nullable=True)
    market_impact_model = Column(JSON, nullable=True)
    allow_partial_fills = Column(Boolean, default=False)
    status = Column(String(20), default="pending")  # pending, running, completed, failed
    progress = Column(Float, default=0.0)  # 0-100
    final_value = Column(Float, nullable=True)
    total_return = Column(Float, nullable=True)
    sharpe_ratio = Column(Float, nullable=True)
    max_drawdown = Column(Float, nullable=True)
    total_trades = Column(Integer, nullable=True)
    win_rate = Column(Float, nullable=True)
    profit_factor = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)


class BacktestTrade(Base):
    """Individual trade from backtest"""
    __tablename__ = "backtest_trades"

    id = Column(Integer, primary_key=True, index=True)
    backtest_run_id = Column(Integer, ForeignKey("backtest_runs.id", ondelete="CASCADE"), index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True)
    entry_date = Column(DateTime(timezone=True))
    exit_date = Column(DateTime(timezone=True), nullable=True)
    entry_price = Column(Float)
    exit_price = Column(Float, nullable=True)
    position_size = Column(Float)
    direction = Column(String(10), default="long")  # long, short
    gross_profit_loss = Column(Float, nullable=True)
    commission = Column(Float, nullable=True)
    slippage = Column(Float, nullable=True)
    net_profit_loss = Column(Float, nullable=True)
    profit_loss_pct = Column(Float, nullable=True)
    r_multiple = Column(Float, nullable=True)
    days_held = Column(Integer, nullable=True)
    exit_reason = Column(String(50), nullable=True)  # target, stop, signal, timeout
    entry_signal = Column(JSON, nullable=True)
    exit_signal = Column(JSON, nullable=True)


class BacktestMetrics(Base):
    """Detailed metrics for backtest run"""
    __tablename__ = "backtest_metrics"

    id = Column(Integer, primary_key=True, index=True)
    backtest_run_id = Column(Integer, ForeignKey("backtest_runs.id", ondelete="CASCADE"), unique=True)
    total_return = Column(Float)
    annualized_return = Column(Float)
    sharpe_ratio = Column(Float)
    sortino_ratio = Column(Float)
    calmar_ratio = Column(Float)
    max_drawdown = Column(Float)
    max_drawdown_duration_days = Column(Integer)
    win_rate = Column(Float)
    profit_factor = Column(Float)
    avg_win = Column(Float)
    avg_loss = Column(Float)
    largest_win = Column(Float)
    largest_loss = Column(Float)
    avg_trade_duration_days = Column(Float)
    total_trades = Column(Integer)
    winning_trades = Column(Integer)
    losing_trades = Column(Integer)
    exposure_pct = Column(Float)  # % of time in market
    volatility = Column(Float)
    beta = Column(Float, nullable=True)
    alpha = Column(Float, nullable=True)
    equity_curve = Column(JSON, nullable=True)  # Array of equity values
    drawdown_curve = Column(JSON, nullable=True)  # Array of drawdown values
    monthly_returns = Column(JSON, nullable=True)  # Dict of monthly returns


class StrategyTemplate(Base):
    """Pre-built strategy templates"""
    __tablename__ = "strategy_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    category = Column(String(50), index=True)  # momentum, mean-reversion, breakout, etc.
    strategy_type = Column(String(20))  # yaml, python, visual
    template_config = Column(JSON)  # Full strategy configuration
    parameters_schema = Column(JSON)  # JSON schema for parameters
    default_parameters = Column(JSON)
    risk_profile = Column(String(20))  # conservative, moderate, aggressive
    typical_win_rate = Column(Float, nullable=True)
    typical_sharpe = Column(Float, nullable=True)
    tags = Column(JSON, nullable=True)  # Array of tags
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class WalkForwardRun(Base):
    """Walk-forward optimization run"""
    __tablename__ = "walk_forward_runs"

    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), index=True)
    name = Column(String(100))
    total_start_date = Column(DateTime(timezone=True))
    total_end_date = Column(DateTime(timezone=True))
    in_sample_period_days = Column(Integer)
    out_sample_period_days = Column(Integer)
    step_size_days = Column(Integer)
    parameter_ranges = Column(JSON)
    optimization_metric = Column(String(50))  # sharpe_ratio, total_return, etc.
    n_trials = Column(Integer)
    status = Column(String(20), default="pending")
    progress = Column(Float, default=0.0)
    n_windows = Column(Integer, nullable=True)
    completed_windows = Column(Integer, nullable=True)
    combined_oos_return = Column(Float, nullable=True)
    combined_oos_sharpe = Column(Float, nullable=True)
    robustness_score = Column(Float, nullable=True)
    window_results = Column(JSON, nullable=True)  # Array of window results
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)


class MonteCarloRun(Base):
    """Monte Carlo simulation run"""
    __tablename__ = "monte_carlo_runs"

    id = Column(Integer, primary_key=True, index=True)
    backtest_run_id = Column(Integer, ForeignKey("backtest_runs.id"), index=True)
    name = Column(String(100))
    n_simulations = Column(Integer)
    simulation_types = Column(JSON)  # Array of simulation types
    entry_delay_range = Column(JSON, nullable=True)
    position_size_variation_pct = Column(Float, nullable=True)
    include_regime_changes = Column(Boolean, default=False)
    status = Column(String(20), default="pending")
    progress = Column(Float, default=0.0)
    baseline_return = Column(Float, nullable=True)
    mean_return = Column(Float, nullable=True)
    median_return = Column(Float, nullable=True)
    return_std = Column(Float, nullable=True)
    percentile_5 = Column(Float, nullable=True)
    percentile_95 = Column(Float, nullable=True)
    probability_of_profit = Column(Float, nullable=True)
    value_at_risk_95 = Column(Float, nullable=True)
    return_distribution = Column(JSON, nullable=True)  # Histogram data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)


class HyperparameterOptimization(Base):
    """ML hyperparameter optimization run"""
    __tablename__ = "hyperparameter_optimizations"

    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=True, index=True)
    model_type = Column(String(50))
    parameter_space = Column(JSON)
    optimization_type = Column(String(20))  # grid, random, bayesian, genetic
    n_trials = Column(Integer)
    objective_metric = Column(String(50))
    status = Column(String(20), default="pending")
    progress = Column(Float, default=0.0)
    best_params = Column(JSON, nullable=True)
    best_score = Column(Float, nullable=True)
    all_results = Column(JSON, nullable=True)  # Array of trial results
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
