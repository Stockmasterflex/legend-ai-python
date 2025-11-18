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

class HistoricalPlayback(Base):
    """Historical data playback sessions"""
    __tablename__ = "historical_playbacks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, nullable=False)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True)
    start_date = Column(DateTime(timezone=True), nullable=False, index=True)
    end_date = Column(DateTime(timezone=True), nullable=False)
    current_position = Column(DateTime(timezone=True), nullable=False)  # Current playback position
    playback_speed = Column(Float, default=1.0)  # 1x, 2x, 0.5x, etc.
    status = Column(String(20), default="paused", index=True)  # "playing", "paused", "completed"
    interval = Column(String(20), default="1day")  # "1min", "5min", "1hour", "1day"
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class PlaybackAnnotation(Base):
    """Annotations on playback sessions"""
    __tablename__ = "playback_annotations"

    id = Column(Integer, primary_key=True, index=True)
    playback_id = Column(Integer, ForeignKey("historical_playbacks.id"), index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)  # Time in playback
    annotation_type = Column(String(50))  # "note", "entry", "exit", "pattern", "support", "resistance"
    title = Column(String(255))
    content = Column(Text)
    price_level = Column(Float, nullable=True)  # Price level for markers
    metadata = Column(Text, nullable=True)  # JSON for additional data
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SimulationAccount(Base):
    """Paper trading simulation accounts"""
    __tablename__ = "simulation_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, nullable=False)
    name = Column(String(255))
    initial_balance = Column(Float, nullable=False, default=100000.0)
    current_balance = Column(Float, nullable=False, default=100000.0)
    cash_balance = Column(Float, nullable=False, default=100000.0)
    total_pnl = Column(Float, default=0.0)
    total_pnl_pct = Column(Float, default=0.0)
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    losing_trades = Column(Integer, default=0)
    win_rate = Column(Float, default=0.0)
    max_drawdown = Column(Float, default=0.0)
    sharpe_ratio = Column(Float, nullable=True)
    status = Column(String(20), default="active", index=True)  # "active", "paused", "closed"
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class SimulationTrade(Base):
    """Trades executed in simulation mode"""
    __tablename__ = "simulation_trades"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("simulation_accounts.id"), index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True)
    trade_type = Column(String(20), nullable=False)  # "long", "short"
    entry_date = Column(DateTime(timezone=True), nullable=False, index=True)
    entry_price = Column(Float, nullable=False)
    position_size = Column(Integer, nullable=False)
    stop_loss = Column(Float, nullable=True)
    target_price = Column(Float, nullable=True)
    exit_date = Column(DateTime(timezone=True), nullable=True)
    exit_price = Column(Float, nullable=True)
    exit_reason = Column(String(100), nullable=True)  # "target", "stop", "manual"
    pnl = Column(Float, default=0.0)
    pnl_pct = Column(Float, default=0.0)
    r_multiple = Column(Float, nullable=True)
    status = Column(String(20), default="open", index=True)  # "open", "closed"
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class WhatIfScenario(Base):
    """What-if analysis scenarios"""
    __tablename__ = "what_if_scenarios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, nullable=False)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True)
    scenario_name = Column(String(255))
    scenario_type = Column(String(50), index=True)  # "entry_timing", "exit_timing", "position_size", "stop_loss"
    base_date = Column(DateTime(timezone=True), nullable=False)
    base_price = Column(Float, nullable=False)

    # Scenario parameters
    alternative_entry_price = Column(Float, nullable=True)
    alternative_entry_date = Column(DateTime(timezone=True), nullable=True)
    alternative_exit_price = Column(Float, nullable=True)
    alternative_exit_date = Column(DateTime(timezone=True), nullable=True)
    alternative_stop_loss = Column(Float, nullable=True)
    alternative_position_size = Column(Integer, nullable=True)

    # Results
    base_pnl = Column(Float, default=0.0)
    alternative_pnl = Column(Float, default=0.0)
    pnl_difference = Column(Float, default=0.0)
    pnl_difference_pct = Column(Float, default=0.0)

    description = Column(Text, nullable=True)
    results_data = Column(Text, nullable=True)  # JSON with detailed results
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

class PatternQuiz(Base):
    """Pattern recognition quizzes"""
    __tablename__ = "pattern_quizzes"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True)
    quiz_date = Column(DateTime(timezone=True), nullable=False, index=True)  # Historical date for quiz
    pattern_type = Column(String(50), index=True)  # Correct pattern type
    difficulty = Column(String(20), default="medium")  # "easy", "medium", "hard"
    question = Column(Text, nullable=False)
    correct_answer = Column(String(100), nullable=False)
    answer_options = Column(Text, nullable=True)  # JSON array of options
    explanation = Column(Text, nullable=True)
    chart_data = Column(Text, nullable=True)  # JSON with OHLCV data
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class QuizAttempt(Base):
    """User quiz attempts"""
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("pattern_quizzes.id"), index=True)
    user_id = Column(String(100), index=True, nullable=False)
    user_answer = Column(String(100))
    is_correct = Column(Boolean, nullable=False)
    time_taken_seconds = Column(Integer, nullable=True)
    score = Column(Float, default=0.0)  # Scoring based on accuracy and speed
    attempted_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

class ReplayBookmark(Base):
    """Bookmarked replay sessions"""
    __tablename__ = "replay_bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True, nullable=False)
    playback_id = Column(Integer, ForeignKey("historical_playbacks.id"), index=True)
    bookmark_name = Column(String(255))
    description = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)  # Comma-separated or JSON
    is_favorite = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class SharedReplay(Base):
    """Shared replay sessions"""
    __tablename__ = "shared_replays"

    id = Column(Integer, primary_key=True, index=True)
    playback_id = Column(Integer, ForeignKey("historical_playbacks.id"), index=True)
    share_token = Column(String(64), unique=True, index=True, nullable=False)  # Unique share URL token
    shared_by = Column(String(100), index=True, nullable=False)
    title = Column(String(255))
    description = Column(Text, nullable=True)
    is_public = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    expiration_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
