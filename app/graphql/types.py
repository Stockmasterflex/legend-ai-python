"""
GraphQL Types
Strawberry types for all models and DTOs
"""

import strawberry
from typing import Optional, List
from datetime import datetime
from enum import Enum


# Enums
@strawberry.enum
class WatchlistStatus(Enum):
    """Watchlist item status"""
    WATCHING = "Watching"
    BREAKING_OUT = "Breaking Out"
    TRIGGERED = "Triggered"
    COMPLETED = "Completed"
    SKIPPED = "Skipped"


@strawberry.enum
class PatternType(Enum):
    """Chart pattern types"""
    VCP = "VCP"
    CUP_AND_HANDLE = "Cup & Handle"
    FLAT_BASE = "Flat Base"
    HIGH_TIGHT_FLAG = "High Tight Flag"
    DOUBLE_BOTTOM = "Double Bottom"
    ASCENDING_TRIANGLE = "Ascending Triangle"


@strawberry.enum
class ScanStatus(Enum):
    """Scan completion status"""
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


@strawberry.enum
class AlertType(Enum):
    """Alert types"""
    PRICE = "price"
    PATTERN = "pattern"
    BREAKOUT = "breakout"
    VOLUME = "volume"


@strawberry.enum
class AlertStatus(Enum):
    """Alert delivery status"""
    SENT = "sent"
    FAILED = "failed"
    ACKNOWLEDGED = "acknowledged"


@strawberry.enum
class Universe(Enum):
    """Market universe options"""
    SP500 = "SP500"
    NASDAQ100 = "NASDAQ100"
    CUSTOM = "CUSTOM"


# Core Types
@strawberry.type
class Ticker:
    """Stock ticker information"""
    id: int
    symbol: str
    name: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    exchange: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


@strawberry.type
class PatternScan:
    """Pattern detection result"""
    id: int
    ticker_id: int
    pattern_type: str
    score: float
    entry_price: Optional[float] = None
    stop_price: Optional[float] = None
    target_price: Optional[float] = None
    risk_reward_ratio: Optional[float] = None
    criteria_met: Optional[str] = None  # JSON string
    analysis: Optional[str] = None
    current_price: Optional[float] = None
    volume_dry_up: bool = False
    consolidation_days: Optional[int] = None
    chart_url: Optional[str] = None
    rs_rating: Optional[float] = None
    scanned_at: datetime

    # Resolved fields
    ticker: Optional["Ticker"] = None


@strawberry.type
class WatchlistItem:
    """Watchlist entry with tracking"""
    id: int
    user_id: str
    ticker_id: int
    status: str
    target_entry: Optional[float] = None
    target_stop: Optional[float] = None
    target_price: Optional[float] = None
    reason: Optional[str] = None
    notes: Optional[str] = None
    alerts_enabled: bool = True
    alert_threshold: Optional[float] = None
    added_at: datetime
    triggered_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Resolved fields
    ticker: Optional["Ticker"] = None


@strawberry.type
class ScanLog:
    """Universe scan execution log"""
    id: int
    scan_type: str
    tickers_scanned: Optional[int] = None
    patterns_found: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None
    error_message: Optional[str] = None


@strawberry.type
class UniverseScan:
    """Universe scan results"""
    id: int
    scan_date: datetime
    universe: str
    total_scanned: Optional[int] = None
    patterns_found: Optional[int] = None
    top_score: Optional[float] = None
    duration_seconds: Optional[float] = None
    status: Optional[str] = None
    error_message: Optional[str] = None


@strawberry.type
class AlertLog:
    """Alert trigger history"""
    id: int
    ticker_id: int
    alert_type: str
    trigger_price: Optional[float] = None
    trigger_value: Optional[float] = None
    alert_sent_at: datetime
    sent_via: Optional[str] = None
    user_id: Optional[str] = None
    status: str = "sent"

    # Resolved fields
    ticker: Optional["Ticker"] = None


# Response Types
@strawberry.type
class PatternResult:
    """Real-time pattern detection result"""
    ticker: str
    pattern: str
    score: float
    entry: float
    stop: float
    target: float
    risk_reward: float
    criteria_met: List[str]
    analysis: str
    timestamp: datetime
    rs_rating: Optional[float] = None
    current_price: Optional[float] = None
    support_start: Optional[float] = None
    support_end: Optional[float] = None
    volume_increasing: Optional[bool] = None
    consolidation_days: Optional[int] = None
    chart_url: Optional[str] = None


@strawberry.type
class ScanResult:
    """Quick scan result"""
    ticker: str
    pattern: str
    score: float
    entry: float
    stop: float
    target: float
    risk_reward: float
    chart_url: Optional[str] = None


@strawberry.type
class MarketInternals:
    """Market breadth and internal metrics"""
    date: str
    advancing: int
    declining: int
    unchanged: int
    new_highs: int
    new_lows: int
    advance_decline_ratio: float
    market_breadth: str
    sentiment: str


@strawberry.type
class PositionSize:
    """Position sizing calculation"""
    shares: int
    dollar_amount: float
    risk_per_share: float
    total_risk: float
    position_percent: float


# Input Types
@strawberry.input
class PatternDetectInput:
    """Input for pattern detection"""
    ticker: str
    interval: str = "1d"
    use_yahoo_fallback: bool = False


@strawberry.input
class UniverseScanInput:
    """Input for universe scanning"""
    universe: Universe = Universe.SP500
    min_score: float = 7.0
    max_results: int = 50
    pattern_types: Optional[List[str]] = None


@strawberry.input
class WatchlistAddInput:
    """Input for adding to watchlist"""
    ticker: str
    user_id: str = "default"
    reason: Optional[str] = None
    alerts_enabled: bool = True
    alert_threshold: Optional[float] = None


@strawberry.input
class WatchlistUpdateInput:
    """Input for updating watchlist item"""
    id: int
    status: Optional[WatchlistStatus] = None
    target_entry: Optional[float] = None
    target_stop: Optional[float] = None
    target_price: Optional[float] = None
    notes: Optional[str] = None
    alerts_enabled: Optional[bool] = None


@strawberry.input
class PositionSizeInput:
    """Input for position sizing"""
    entry: float
    stop: float
    account_size: float
    risk_percent: float = 1.0
    target: Optional[float] = None


@strawberry.input
class ChartGenerateInput:
    """Input for chart generation"""
    ticker: str
    interval: str = "1d"
    timeframe: str = "6mo"
    indicators: Optional[List[str]] = None


# Pagination
@strawberry.type
class PageInfo:
    """Pagination information"""
    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str] = None
    end_cursor: Optional[str] = None
    total_count: int


@strawberry.type
class PatternScanEdge:
    """Pattern scan edge for pagination"""
    cursor: str
    node: PatternScan


@strawberry.type
class PatternScanConnection:
    """Paginated pattern scans"""
    edges: List[PatternScanEdge]
    page_info: PageInfo


# Subscription Events
@strawberry.type
class PatternDetectedEvent:
    """Real-time pattern detection event"""
    ticker: str
    pattern: str
    score: float
    entry: float
    timestamp: datetime


@strawberry.type
class PriceAlertEvent:
    """Real-time price alert event"""
    ticker: str
    price: float
    alert_type: str
    message: str
    timestamp: datetime


@strawberry.type
class ScanProgressEvent:
    """Real-time scan progress event"""
    scan_id: int
    progress: float  # 0.0 to 1.0
    tickers_scanned: int
    patterns_found: int
    current_ticker: Optional[str] = None
