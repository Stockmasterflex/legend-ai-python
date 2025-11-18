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

class MarketAnalysis(Base):
    """AI-powered market analysis results"""
    __tablename__ = "market_analysis"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=True)
    analysis_type = Column(String(50), index=True)  # "chart", "news", "sentiment", "technical", "brief"
    ai_model = Column(String(100))  # Model used: "claude-sonnet-4", "gpt-4", "gemini-pro"
    analysis_text = Column(Text)  # Full AI analysis
    support_levels = Column(Text, nullable=True)  # JSON array of support prices
    resistance_levels = Column(Text, nullable=True)  # JSON array of resistance prices
    trend_direction = Column(String(20), nullable=True)  # "bullish", "bearish", "neutral", "mixed"
    sentiment_score = Column(Float, nullable=True)  # -1.0 to 1.0
    risk_assessment = Column(Text, nullable=True)  # AI risk analysis
    trade_ideas = Column(Text, nullable=True)  # JSON array of trade ideas
    confidence_score = Column(Float, nullable=True)  # 0-100
    chart_url = Column(Text, nullable=True)  # Chart analyzed
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

class NewsArticle(Base):
    """Scraped news articles for market analysis"""
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=True)
    title = Column(String(500), nullable=False)
    source = Column(String(100))  # "bloomberg", "reuters", "yahoo", etc.
    url = Column(Text, unique=True)
    content = Column(Text, nullable=True)  # Article text
    author = Column(String(200), nullable=True)
    published_at = Column(DateTime(timezone=True), index=True, nullable=True)
    scraped_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    category = Column(String(50), nullable=True)  # "earnings", "macro", "sector", etc.

class NewsSentiment(Base):
    """AI sentiment analysis of news articles"""
    __tablename__ = "news_sentiment"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("news_articles.id"), index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=True)
    ai_model = Column(String(100))  # Model used for sentiment analysis
    sentiment = Column(String(20), index=True)  # "bullish", "bearish", "neutral"
    sentiment_score = Column(Float)  # -1.0 (very bearish) to 1.0 (very bullish)
    key_points = Column(Text, nullable=True)  # JSON array of key takeaways
    impact_assessment = Column(Text, nullable=True)  # How news affects stock
    relevance_score = Column(Float, nullable=True)  # How relevant to ticker (0-1)
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

class MarketBrief(Base):
    """Daily AI-generated market briefs"""
    __tablename__ = "market_briefs"

    id = Column(Integer, primary_key=True, index=True)
    brief_date = Column(DateTime(timezone=True), index=True, nullable=False)
    market_summary = Column(Text)  # Overall market analysis
    top_movers = Column(Text)  # JSON array of top gaining/losing stocks with AI analysis
    sector_performance = Column(Text)  # JSON object of sector analysis
    pattern_highlights = Column(Text)  # JSON array of notable pattern detections
    risk_factors = Column(Text, nullable=True)  # AI-identified risks
    trade_ideas = Column(Text, nullable=True)  # JSON array of AI trade ideas
    market_sentiment = Column(String(20))  # "bullish", "bearish", "neutral", "mixed"
    sentiment_score = Column(Float, nullable=True)  # Overall market sentiment -1 to 1
    ai_model = Column(String(100))  # Primary model used
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    sent_to_telegram = Column(Boolean, default=False)
    telegram_sent_at = Column(DateTime(timezone=True), nullable=True)

class AIQuery(Base):
    """Natural language query history and responses"""
    __tablename__ = "ai_queries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), index=True)  # Telegram user ID or "api"
    query_text = Column(Text, nullable=False)  # User's natural language query
    query_type = Column(String(50), nullable=True)  # "search", "analysis", "education", "alert"
    ai_model = Column(String(100))  # Model that processed query
    response_text = Column(Text)  # AI response
    tickers_mentioned = Column(Text, nullable=True)  # JSON array of ticker symbols
    actions_taken = Column(Text, nullable=True)  # JSON array of actions (scans run, etc.)
    results_found = Column(Integer, nullable=True)  # Number of results
    execution_time_ms = Column(Float, nullable=True)  # How long to process
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    response_rating = Column(Integer, nullable=True)  # User feedback 1-5
