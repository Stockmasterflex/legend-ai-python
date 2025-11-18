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

class PricePrediction(Base):
    """AI price predictions and forecasts"""
    __tablename__ = "price_predictions"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True)
    model_type = Column(String(50), index=True)  # "LSTM", "RandomForest", "GradientBoosting", "Ensemble"
    prediction_date = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    target_date = Column(DateTime(timezone=True), index=True)  # Future date being predicted
    timeframe = Column(String(20), index=True)  # "1D", "1W", "1M", "3M"

    # Predictions
    predicted_price = Column(Float, nullable=False)
    predicted_high = Column(Float, nullable=True)  # Upper bound
    predicted_low = Column(Float, nullable=True)  # Lower bound
    confidence_score = Column(Float, nullable=True)  # 0-1 confidence

    # Probability bands
    prob_upper_90 = Column(Float, nullable=True)  # 90% confidence upper
    prob_lower_90 = Column(Float, nullable=True)  # 90% confidence lower
    prob_upper_70 = Column(Float, nullable=True)  # 70% confidence upper
    prob_lower_70 = Column(Float, nullable=True)  # 70% confidence lower
    prob_upper_50 = Column(Float, nullable=True)  # 50% confidence upper
    prob_lower_50 = Column(Float, nullable=True)  # 50% confidence lower

    # Support/Resistance
    support_levels = Column(JSON, nullable=True)  # Array of support prices
    resistance_levels = Column(JSON, nullable=True)  # Array of resistance prices

    # Feature importance
    feature_importance = Column(JSON, nullable=True)  # Top features used

    # Actual results (filled in later for backtesting)
    actual_price = Column(Float, nullable=True)
    accuracy_score = Column(Float, nullable=True)  # How accurate was prediction

    # Market regime at prediction time
    market_regime = Column(String(50), nullable=True)  # "bullish", "bearish", "ranging", "volatile"

    # Metadata
    model_version = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ModelPerformance(Base):
    """Model performance metrics and backtesting results"""
    __tablename__ = "model_performance"

    id = Column(Integer, primary_key=True, index=True)
    model_type = Column(String(50), index=True)  # "LSTM", "RandomForest", etc.
    model_version = Column(String(50), nullable=True)

    # Time period for metrics
    evaluation_period = Column(String(50), index=True)  # "daily", "weekly", "monthly"
    start_date = Column(DateTime(timezone=True), index=True)
    end_date = Column(DateTime(timezone=True), index=True)

    # Accuracy metrics
    mae = Column(Float, nullable=True)  # Mean Absolute Error
    rmse = Column(Float, nullable=True)  # Root Mean Square Error
    mape = Column(Float, nullable=True)  # Mean Absolute Percentage Error
    r2_score = Column(Float, nullable=True)  # R-squared
    directional_accuracy = Column(Float, nullable=True)  # % correct direction predictions

    # Trading metrics (if predictions used for trading)
    win_rate = Column(Float, nullable=True)
    avg_return = Column(Float, nullable=True)
    sharpe_ratio = Column(Float, nullable=True)
    max_drawdown = Column(Float, nullable=True)

    # Sample size
    total_predictions = Column(Integer)
    total_tickers = Column(Integer, nullable=True)

    # Detailed results
    performance_by_ticker = Column(JSON, nullable=True)  # Breakdown by ticker
    performance_by_timeframe = Column(JSON, nullable=True)  # Breakdown by timeframe

    # Training info
    training_samples = Column(Integer, nullable=True)
    training_duration_seconds = Column(Float, nullable=True)

    # Metadata
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

class ForecastJob(Base):
    """Batch forecasting job tracking"""
    __tablename__ = "forecast_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_type = Column(String(50), index=True)  # "single_ticker", "universe", "watchlist"
    status = Column(String(20), index=True)  # "pending", "running", "completed", "failed"

    # Job parameters
    ticker_symbols = Column(JSON, nullable=True)  # List of tickers to forecast
    model_types = Column(JSON, nullable=True)  # List of models to use
    timeframes = Column(JSON, nullable=True)  # List of timeframes

    # Progress tracking
    total_tasks = Column(Integer, nullable=True)
    completed_tasks = Column(Integer, default=0)
    failed_tasks = Column(Integer, default=0)

    # Timing
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Results
    predictions_generated = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    created_by = Column(String(100), nullable=True)  # User ID
