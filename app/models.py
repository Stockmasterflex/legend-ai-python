"""
Database models for Legend AI
Phase 1.5: Database Integration
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()

# Enums for backtesting
class StrategyType(str, enum.Enum):
    YAML = "yaml"
    PYTHON = "python"
    VISUAL = "visual"
    TEMPLATE = "template"

class BacktestStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class OptimizationType(str, enum.Enum):
    GRID_SEARCH = "grid_search"
    RANDOM_SEARCH = "random_search"
    BAYESIAN = "bayesian"
    WALK_FORWARD = "walk_forward"

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


# =====================================================================
# BACKTESTING MODELS - Enterprise-grade backtesting platform
# =====================================================================

class StrategyTemplate(Base):
    """Pre-built strategy templates"""
    __tablename__ = "strategy_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    category = Column(String(50), index=True)  # "Pattern-Based", "Technical", "ML", "Hybrid"
    strategy_type = Column(String(20), nullable=False)  # YAML, Python, Visual
    template_config = Column(JSON, nullable=False)  # YAML content or Python code template
    parameters_schema = Column(JSON)  # JSON schema for parameter validation
    default_parameters = Column(JSON)  # Default parameter values
    risk_profile = Column(String(20))  # "conservative", "moderate", "aggressive"
    typical_win_rate = Column(Float, nullable=True)
    typical_sharpe = Column(Float, nullable=True)
    tags = Column(JSON)  # ["VCP", "swing", "momentum"]
    created_by = Column(String(100))
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Strategy(Base):
    """Trading strategy definition"""
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    strategy_type = Column(String(20), nullable=False)  # YAML, Python, Visual
    template_id = Column(Integer, ForeignKey("strategy_templates.id"), nullable=True)

    # Strategy content (one of these will be populated based on type)
    yaml_config = Column(Text, nullable=True)  # YAML strategy definition
    python_code = Column(Text, nullable=True)  # Python strategy code
    visual_config = Column(JSON, nullable=True)  # Visual builder JSON

    # Strategy parameters
    parameters = Column(JSON, nullable=False)  # Strategy-specific parameters
    entry_rules = Column(JSON)  # Entry condition rules
    exit_rules = Column(JSON)  # Exit condition rules
    risk_management = Column(JSON)  # Position sizing, stop loss rules

    # Metadata
    version = Column(String(20), default="1.0.0")
    is_active = Column(Boolean, default=True)
    user_id = Column(String(100), index=True, default="default")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class BacktestRun(Base):
    """Backtest execution record"""
    __tablename__ = "backtest_runs"

    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)

    # Time period
    start_date = Column(DateTime(timezone=True), nullable=False, index=True)
    end_date = Column(DateTime(timezone=True), nullable=False, index=True)

    # Capital and universe
    initial_capital = Column(Float, nullable=False)
    universe = Column(JSON)  # List of tickers or universe definition

    # Execution simulation parameters
    commission_model = Column(JSON)  # {"type": "fixed", "value": 0.01} or {"type": "percentage", "value": 0.001}
    slippage_model = Column(JSON)  # {"type": "fixed", "bps": 5} or {"type": "volume_based"}
    market_impact_model = Column(JSON, nullable=True)  # Advanced market impact simulation
    allow_partial_fills = Column(Boolean, default=False)

    # Results
    final_value = Column(Float)
    total_return = Column(Float)  # Percentage
    total_return_pct = Column(Float)
    annualized_return = Column(Float)
    sharpe_ratio = Column(Float)
    sortino_ratio = Column(Float)
    max_drawdown = Column(Float)  # Percentage
    max_drawdown_duration = Column(Integer)  # Days
    calmar_ratio = Column(Float)

    # Trade statistics
    total_trades = Column(Integer)
    winning_trades = Column(Integer)
    losing_trades = Column(Integer)
    win_rate = Column(Float)
    profit_factor = Column(Float)
    average_win = Column(Float)
    average_loss = Column(Float)
    largest_win = Column(Float)
    largest_loss = Column(Float)
    avg_bars_held = Column(Float)
    expectancy = Column(Float)

    # Additional metrics
    var_95 = Column(Float)  # Value at Risk (95%)
    cvar_95 = Column(Float)  # Conditional VaR
    beta = Column(Float, nullable=True)
    alpha = Column(Float, nullable=True)

    # Execution
    status = Column(String(20), default="pending", index=True)
    progress = Column(Float, default=0.0)  # 0-100
    error_message = Column(Text)

    # Timing
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Float)


class BacktestTrade(Base):
    """Individual trades within a backtest"""
    __tablename__ = "backtest_trades"

    id = Column(Integer, primary_key=True, index=True)
    backtest_run_id = Column(Integer, ForeignKey("backtest_runs.id"), index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True)

    # Entry
    entry_date = Column(DateTime(timezone=True), nullable=False, index=True)
    entry_price = Column(Float, nullable=False)
    entry_signal = Column(String(100))  # Signal that triggered entry
    pattern_type = Column(String(50))  # VCP, Cup & Handle, etc.

    # Exit
    exit_date = Column(DateTime(timezone=True), index=True)
    exit_price = Column(Float)
    exit_signal = Column(String(100))  # Signal that triggered exit
    exit_reason = Column(String(100))  # "target", "stop", "timeout", "signal"

    # Position
    position_size = Column(Integer, nullable=False)  # Number of shares
    position_value = Column(Float)  # Entry value in $

    # Costs
    entry_commission = Column(Float)
    exit_commission = Column(Float)
    slippage_cost = Column(Float)
    total_costs = Column(Float)

    # Performance
    gross_profit_loss = Column(Float)
    net_profit_loss = Column(Float)
    profit_loss_pct = Column(Float)
    r_multiple = Column(Float)  # Multiple of initial risk

    # Risk
    initial_stop = Column(Float)
    initial_risk = Column(Float)  # $ amount at risk
    mae = Column(Float)  # Maximum Adverse Excursion
    mfe = Column(Float)  # Maximum Favorable Excursion

    # Timing
    bars_held = Column(Integer)
    days_held = Column(Integer)

    # Context
    entry_context = Column(JSON)  # Market conditions, indicators at entry
    exit_context = Column(JSON)  # Market conditions at exit


class BacktestMetrics(Base):
    """Time-series metrics for backtest (equity curve, drawdown)"""
    __tablename__ = "backtest_metrics"

    id = Column(Integer, primary_key=True, index=True)
    backtest_run_id = Column(Integer, ForeignKey("backtest_runs.id"), index=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)

    # Portfolio value
    portfolio_value = Column(Float, nullable=False)
    cash = Column(Float, nullable=False)
    positions_value = Column(Float, nullable=False)

    # Positions
    open_positions = Column(Integer)
    position_details = Column(JSON)  # [{ticker, shares, value, unrealized_pnl}]

    # Performance
    daily_return = Column(Float)
    cumulative_return = Column(Float)
    drawdown_pct = Column(Float)
    drawdown_value = Column(Float)

    # Exposure
    market_exposure = Column(Float)  # % of capital in positions
    leverage = Column(Float, default=1.0)

    # Running statistics
    running_sharpe = Column(Float)
    running_volatility = Column(Float)


class WalkForwardRun(Base):
    """Walk-forward optimization run"""
    __tablename__ = "walk_forward_runs"

    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), index=True)
    name = Column(String(200), nullable=False)

    # Walk-forward configuration
    total_start_date = Column(DateTime(timezone=True), nullable=False)
    total_end_date = Column(DateTime(timezone=True), nullable=False)
    in_sample_period_days = Column(Integer, nullable=False)  # e.g., 252 (1 year)
    out_sample_period_days = Column(Integer, nullable=False)  # e.g., 63 (3 months)
    step_size_days = Column(Integer, nullable=False)  # Rolling window step

    # Optimization configuration
    parameter_ranges = Column(JSON, nullable=False)  # {"param1": [min, max], ...}
    optimization_metric = Column(String(50), default="sharpe_ratio")  # What to optimize for
    n_trials = Column(Integer, default=100)  # For Bayesian/Random optimization

    # Results aggregation
    total_windows = Column(Integer)
    completed_windows = Column(Integer, default=0)
    avg_in_sample_sharpe = Column(Float)
    avg_out_sample_sharpe = Column(Float)
    degradation_factor = Column(Float)  # out_sample / in_sample performance ratio

    # Overfitting detection
    is_overfit = Column(Boolean)
    overfitting_score = Column(Float)  # Higher = more overfit
    consistency_score = Column(Float)  # How consistent across windows

    # Best parameters across all windows
    robust_parameters = Column(JSON)  # Parameters that work best out-of-sample

    # Execution
    status = Column(String(20), default="pending", index=True)
    progress = Column(Float, default=0.0)
    error_message = Column(Text)

    # Timing
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Float)


class WalkForwardWindow(Base):
    """Individual window in walk-forward analysis"""
    __tablename__ = "walk_forward_windows"

    id = Column(Integer, primary_key=True, index=True)
    walk_forward_run_id = Column(Integer, ForeignKey("walk_forward_runs.id"), index=True)
    window_number = Column(Integer, nullable=False)

    # Window periods
    in_sample_start = Column(DateTime(timezone=True), nullable=False)
    in_sample_end = Column(DateTime(timezone=True), nullable=False)
    out_sample_start = Column(DateTime(timezone=True), nullable=False)
    out_sample_end = Column(DateTime(timezone=True), nullable=False)

    # In-sample optimization results
    in_sample_backtest_id = Column(Integer, ForeignKey("backtest_runs.id"))
    optimized_parameters = Column(JSON)
    in_sample_sharpe = Column(Float)
    in_sample_return = Column(Float)
    in_sample_max_dd = Column(Float)

    # Out-of-sample validation results
    out_sample_backtest_id = Column(Integer, ForeignKey("backtest_runs.id"))
    out_sample_sharpe = Column(Float)
    out_sample_return = Column(Float)
    out_sample_max_dd = Column(Float)

    # Performance degradation
    sharpe_degradation = Column(Float)  # (out - in) / in
    return_degradation = Column(Float)

    # Status
    status = Column(String(20), default="pending")
    completed_at = Column(DateTime(timezone=True))


class MonteCarloRun(Base):
    """Monte Carlo simulation run"""
    __tablename__ = "monte_carlo_runs"

    id = Column(Integer, primary_key=True, index=True)
    backtest_run_id = Column(Integer, ForeignKey("backtest_runs.id"), index=True)
    name = Column(String(200), nullable=False)

    # Simulation configuration
    n_simulations = Column(Integer, nullable=False, default=1000)
    simulation_types = Column(JSON)  # ["random_entry", "position_size_variation", "regime_change"]

    # Random entry configuration
    entry_delay_range = Column(JSON)  # {"min_days": -5, "max_days": 5}

    # Position size variation
    position_size_variation_pct = Column(Float)  # ±20% variation

    # Market regime simulation
    include_regime_changes = Column(Boolean, default=False)
    regime_parameters = Column(JSON)  # Bull/bear market adjustments

    # Aggregated results
    median_return = Column(Float)
    mean_return = Column(Float)
    std_return = Column(Float)

    # Confidence intervals
    ci_95_lower = Column(Float)  # 95% confidence interval lower bound
    ci_95_upper = Column(Float)  # 95% confidence interval upper bound
    ci_99_lower = Column(Float)
    ci_99_upper = Column(Float)

    # Risk metrics
    probability_of_profit = Column(Float)  # % of simulations with positive return
    worst_case_return = Column(Float)  # 5th percentile
    best_case_return = Column(Float)  # 95th percentile

    # Distribution
    return_distribution = Column(JSON)  # Histogram data
    sharpe_distribution = Column(JSON)
    max_dd_distribution = Column(JSON)

    # Status
    status = Column(String(20), default="pending", index=True)
    progress = Column(Float, default=0.0)
    completed_simulations = Column(Integer, default=0)

    # Timing
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Float)


class MonteCarloSimulation(Base):
    """Individual Monte Carlo simulation result"""
    __tablename__ = "monte_carlo_simulations"

    id = Column(Integer, primary_key=True, index=True)
    monte_carlo_run_id = Column(Integer, ForeignKey("monte_carlo_runs.id"), index=True)
    simulation_number = Column(Integer, nullable=False)

    # Applied variations
    variations_applied = Column(JSON)  # {"entry_delays": {...}, "position_adjustments": {...}}

    # Results
    total_return = Column(Float)
    sharpe_ratio = Column(Float)
    max_drawdown = Column(Float)
    win_rate = Column(Float)
    total_trades = Column(Integer)

    # Comparison to baseline
    return_diff_from_baseline = Column(Float)
    sharpe_diff_from_baseline = Column(Float)


class MLModel(Base):
    """Machine learning model for strategy enhancement"""
    __tablename__ = "ml_models"

    id = Column(Integer, primary_key=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    # Model type
    model_type = Column(String(50), nullable=False)  # "classifier", "regressor", "ensemble"
    algorithm = Column(String(50), nullable=False)  # "RandomForest", "XGBoost", "LSTM", etc.

    # Training configuration
    feature_config = Column(JSON, nullable=False)  # Feature engineering configuration
    hyperparameters = Column(JSON)  # Model hyperparameters
    training_data_config = Column(JSON)  # How training data is prepared

    # Model artifacts (stored as paths or serialized)
    model_path = Column(String(500))  # Path to saved model file
    scaler_path = Column(String(500))  # Path to saved scaler
    feature_importance = Column(JSON)  # Feature importance scores

    # Training results
    train_score = Column(Float)
    validation_score = Column(Float)
    test_score = Column(Float)
    cross_val_scores = Column(JSON)  # Array of CV scores

    # Performance metrics (for classifiers)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    auc_roc = Column(Float)

    # Performance metrics (for regressors)
    rmse = Column(Float)
    mae = Column(Float)
    r2_score = Column(Float)

    # Metadata
    version = Column(String(20), default="1.0.0")
    is_active = Column(Boolean, default=True)
    trained_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class HyperparameterOptimization(Base):
    """Hyperparameter optimization run"""
    __tablename__ = "hyperparameter_optimizations"

    id = Column(Integer, primary_key=True, index=True)
    ml_model_id = Column(Integer, ForeignKey("ml_models.id"), nullable=True, index=True)
    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=True, index=True)
    name = Column(String(200), nullable=False)

    # Optimization configuration
    optimization_type = Column(String(20), nullable=False)  # "grid", "random", "bayesian"
    parameter_space = Column(JSON, nullable=False)  # Parameter search space
    objective_metric = Column(String(50), default="sharpe_ratio")  # What to optimize
    n_trials = Column(Integer, default=100)

    # Results
    best_parameters = Column(JSON)
    best_score = Column(Float)
    all_trials = Column(JSON)  # History of all trials

    # Convergence analysis
    convergence_plot_data = Column(JSON)
    parameter_importance = Column(JSON)

    # Status
    status = Column(String(20), default="pending", index=True)
    progress = Column(Float, default=0.0)
    completed_trials = Column(Integer, default=0)

    # Timing
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Float)


class EnsembleModel(Base):
    """Ensemble model combining multiple models/strategies"""
    __tablename__ = "ensemble_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    # Ensemble configuration
    ensemble_type = Column(String(50), nullable=False)  # "voting", "stacking", "weighted", "custom"
    member_models = Column(JSON, nullable=False)  # List of model IDs or strategy IDs
    weights = Column(JSON)  # Weights for each member (if weighted ensemble)
    combination_method = Column(String(50))  # "average", "majority_vote", "learned"

    # Meta-learner (for stacking)
    meta_learner_config = Column(JSON)
    meta_learner_path = Column(String(500))

    # Performance
    backtest_id = Column(Integer, ForeignKey("backtest_runs.id"), nullable=True)
    ensemble_score = Column(Float)
    improvement_over_best_member = Column(Float)  # % improvement

    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
