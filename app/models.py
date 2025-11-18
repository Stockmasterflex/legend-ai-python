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

class CompetitorGroup(Base):
    """Group of competing stocks in the same industry"""
    __tablename__ = "competitor_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)  # "EV Manufacturers", "Cloud Software"
    description = Column(Text)
    industry = Column(String(100), index=True)
    sector = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class CompetitorGroupMember(Base):
    """Members of a competitor group"""
    __tablename__ = "competitor_group_members"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("competitor_groups.id"), index=True, nullable=False)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=False)
    is_primary = Column(Boolean, default=False)  # Primary company being compared against
    added_at = Column(DateTime(timezone=True), server_default=func.now())

class CompetitorTracking(Base):
    """Historical performance tracking for competitors"""
    __tablename__ = "competitor_tracking"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("competitor_groups.id"), index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True)
    tracking_date = Column(DateTime(timezone=True), index=True, server_default=func.now())

    # Performance metrics
    price = Column(Float)
    price_change_1d = Column(Float)  # % change
    price_change_1w = Column(Float)
    price_change_1m = Column(Float)
    price_change_3m = Column(Float)
    volume = Column(Float)
    market_cap = Column(Float, nullable=True)

    # Relative metrics
    rs_rating = Column(Float)  # vs SPY
    rs_vs_group = Column(Float)  # vs competitor average
    market_share_proxy = Column(Float)  # Volume-based market share estimate

    # Pattern & technical
    pattern_score = Column(Float)  # Best pattern score
    best_pattern = Column(String(50))
    legend_score = Column(Float)

    # Rankings
    rank_in_group = Column(Integer)
    percentile = Column(Float)

class SocialSentiment(Base):
    """Social media sentiment tracking"""
    __tablename__ = "social_sentiment"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=False)
    source = Column(String(50), index=True)  # "twitter", "reddit", "stocktwits"
    sentiment_date = Column(DateTime(timezone=True), index=True, server_default=func.now())

    # Sentiment metrics
    sentiment_score = Column(Float)  # -1 to 1
    sentiment_label = Column(String(20))  # "bullish", "bearish", "neutral"
    mention_count = Column(Integer)
    positive_mentions = Column(Integer)
    negative_mentions = Column(Integer)
    neutral_mentions = Column(Integer)

    # Engagement metrics
    total_engagement = Column(Integer)  # Likes, retweets, comments
    reach = Column(Integer, nullable=True)  # Estimated reach
    trending = Column(Boolean, default=False)

    # Sample data
    sample_posts = Column(Text)  # JSON array of sample posts

class PatentFiling(Base):
    """Patent filings and R&D tracking"""
    __tablename__ = "patent_filings"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=False)

    # Patent info
    patent_number = Column(String(50), unique=True, index=True)
    title = Column(Text)
    filing_date = Column(DateTime(timezone=True), index=True)
    publication_date = Column(DateTime(timezone=True), nullable=True)
    grant_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50))  # "filed", "published", "granted", "expired"

    # Classification
    technology_category = Column(String(100), index=True)
    patent_class = Column(String(50))
    innovation_score = Column(Float, nullable=True)  # Estimated innovation score

    # Metrics
    citation_count = Column(Integer, default=0)
    family_size = Column(Integer, default=1)  # Number of related patents

    # Metadata
    inventors = Column(Text)  # JSON array
    abstract = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class RDSpending(Base):
    """R&D spending tracking"""
    __tablename__ = "rd_spending"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=False)
    period = Column(String(20), index=True)  # "Q1 2024", "FY 2023"
    period_start = Column(DateTime(timezone=True), index=True)
    period_end = Column(DateTime(timezone=True))

    # Spending metrics
    rd_spending = Column(Float)  # R&D spending in USD
    rd_as_pct_revenue = Column(Float)  # R&D as % of revenue
    patent_filings_count = Column(Integer, default=0)
    patent_grants_count = Column(Integer, default=0)

    # Innovation metrics
    innovation_efficiency = Column(Float, nullable=True)  # Patents per $ spent
    rd_growth_yoy = Column(Float, nullable=True)  # YoY growth %

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AnalystCoverage(Base):
    """Analyst ratings and coverage tracking"""
    __tablename__ = "analyst_coverage"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=False)

    # Analyst info
    analyst_firm = Column(String(100))
    analyst_name = Column(String(100))

    # Rating info
    rating_date = Column(DateTime(timezone=True), index=True, server_default=func.now())
    rating = Column(String(20))  # "Buy", "Sell", "Hold", "Outperform", etc.
    previous_rating = Column(String(20), nullable=True)
    rating_change = Column(String(20))  # "Upgrade", "Downgrade", "Initiate", "Reiterate"

    # Price targets
    price_target = Column(Float)
    previous_price_target = Column(Float, nullable=True)
    price_target_change_pct = Column(Float, nullable=True)

    # Sentiment
    sentiment = Column(String(20))  # "bullish", "bearish", "neutral"
    confidence = Column(Float, nullable=True)  # Analyst confidence score

    # Additional data
    report_title = Column(Text)
    summary = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AnalystConsensus(Base):
    """Aggregated analyst consensus"""
    __tablename__ = "analyst_consensus"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=False)
    consensus_date = Column(DateTime(timezone=True), index=True, server_default=func.now())

    # Consensus metrics
    total_analysts = Column(Integer)
    buy_count = Column(Integer, default=0)
    hold_count = Column(Integer, default=0)
    sell_count = Column(Integer, default=0)

    # Ratings
    consensus_rating = Column(String(20))  # "Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"
    consensus_score = Column(Float)  # 1-5 scale

    # Price targets
    avg_price_target = Column(Float)
    high_price_target = Column(Float)
    low_price_target = Column(Float)
    median_price_target = Column(Float)

    # Trends
    upgrades_last_30d = Column(Integer, default=0)
    downgrades_last_30d = Column(Integer, default=0)
    sentiment_trend = Column(String(20))  # "improving", "deteriorating", "stable"

class SupplyChainRelationship(Base):
    """Supply chain relationships (suppliers, customers)"""
    __tablename__ = "supply_chain_relationships"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=False)

    # Relationship info
    relationship_type = Column(String(20), index=True)  # "supplier", "customer", "partner"
    related_company_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=True)
    related_company_name = Column(String(255))  # For non-public companies

    # Dependency metrics
    revenue_contribution_pct = Column(Float, nullable=True)  # % of revenue
    dependency_level = Column(String(20))  # "critical", "high", "medium", "low"
    relationship_status = Column(String(20))  # "active", "at_risk", "terminated"

    # Geographic info
    primary_geography = Column(String(50))  # "North America", "Asia", etc.
    geographic_risk_score = Column(Float, nullable=True)

    # Metadata
    relationship_start_date = Column(DateTime(timezone=True), nullable=True)
    last_verified = Column(DateTime(timezone=True))
    source = Column(String(100))  # Where this info came from
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class SupplyChainRisk(Base):
    """Supply chain risk events and monitoring"""
    __tablename__ = "supply_chain_risks"

    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), index=True, nullable=False)
    risk_date = Column(DateTime(timezone=True), index=True, server_default=func.now())

    # Risk details
    risk_type = Column(String(50), index=True)  # "supplier_issue", "geographic", "material_shortage", etc.
    risk_level = Column(String(20))  # "critical", "high", "medium", "low"
    affected_relationships = Column(Text)  # JSON array of relationship IDs

    # Impact
    estimated_impact = Column(Text)  # Description of impact
    revenue_at_risk_pct = Column(Float, nullable=True)
    mitigation_status = Column(String(20))  # "unmitigated", "in_progress", "mitigated"

    # Details
    description = Column(Text)
    source = Column(String(100))
    resolution_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
