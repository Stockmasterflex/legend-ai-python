"""
Pydantic schemas for Social Trading Community
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime


# ============================================================================
# AUTH SCHEMAS
# ============================================================================

class UserRegister(BaseModel):
    """User registration request"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username must be alphanumeric (underscores and hyphens allowed)')
        return v


class UserLogin(BaseModel):
    """User login request"""
    username: str
    password: str


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data"""
    username: Optional[str] = None


# ============================================================================
# USER PROFILE SCHEMAS
# ============================================================================

class UserProfileBase(BaseModel):
    """Base user profile schema"""
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    trading_since: Optional[datetime] = None
    preferred_strategies: Optional[List[str]] = None
    preferred_tickers: Optional[List[str]] = None
    is_public: bool = True
    show_stats: bool = True
    allow_copy_trading: bool = True


class UserProfileCreate(UserProfileBase):
    """Create user profile"""
    pass


class UserProfileUpdate(UserProfileBase):
    """Update user profile"""
    pass


class UserProfileResponse(UserProfileBase):
    """User profile response"""
    id: int
    user_id: int
    username: str
    total_posts: int
    total_followers: int
    total_following: int
    win_rate: Optional[float]
    total_trades_shared: int
    successful_trades: int
    avg_return: Optional[float]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """User response (public info)"""
    id: int
    username: str
    full_name: Optional[str]
    created_at: datetime
    profile: Optional[UserProfileResponse] = None

    class Config:
        from_attributes = True


# ============================================================================
# FOLLOW SCHEMAS
# ============================================================================

class FollowCreate(BaseModel):
    """Follow a user"""
    following_id: int
    copy_trading_enabled: bool = False
    copy_percentage: Optional[float] = Field(None, ge=0, le=100)
    max_position_size: Optional[float] = Field(None, ge=0)


class FollowUpdate(BaseModel):
    """Update follow settings"""
    copy_trading_enabled: Optional[bool] = None
    copy_percentage: Optional[float] = Field(None, ge=0, le=100)
    max_position_size: Optional[float] = Field(None, ge=0)


class FollowResponse(BaseModel):
    """Follow relationship response"""
    id: int
    follower_id: int
    following_id: int
    following_username: str
    copy_trading_enabled: bool
    copy_percentage: Optional[float]
    max_position_size: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# TRADE POST SCHEMAS
# ============================================================================

class TradePostBase(BaseModel):
    """Base trade post schema"""
    title: str = Field(..., min_length=5, max_length=255)
    content: str = Field(..., min_length=10)
    ticker_symbol: Optional[str] = None
    post_type: str = Field(default="idea")  # idea, entry, exit, update, analysis
    entry_price: Optional[float] = Field(None, ge=0)
    stop_price: Optional[float] = Field(None, ge=0)
    target_price: Optional[float] = Field(None, ge=0)
    position_size: Optional[float] = Field(None, ge=0)
    pattern_type: Optional[str] = None
    chart_annotations: Optional[dict] = None
    is_public: bool = True


class TradePostCreate(TradePostBase):
    """Create trade post"""
    pass


class TradePostUpdate(BaseModel):
    """Update trade post"""
    title: Optional[str] = Field(None, min_length=5, max_length=255)
    content: Optional[str] = Field(None, min_length=10)
    post_type: Optional[str] = None
    exit_price: Optional[float] = Field(None, ge=0)
    profit_loss: Optional[float] = None
    profit_loss_percent: Optional[float] = None
    trade_status: Optional[str] = None  # active, closed, stopped
    chart_annotations: Optional[dict] = None
    is_public: Optional[bool] = None
    is_pinned: Optional[bool] = None


class TradePostChartResponse(BaseModel):
    """Trade post chart response"""
    id: int
    chart_url: str
    chart_type: Optional[str]
    timeframe: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class TradePostResponse(BaseModel):
    """Trade post response"""
    id: int
    user_id: int
    username: str
    ticker_symbol: Optional[str]
    title: str
    content: str
    post_type: str
    entry_price: Optional[float]
    stop_price: Optional[float]
    target_price: Optional[float]
    position_size: Optional[float]
    pattern_type: Optional[str]
    exit_price: Optional[float]
    profit_loss: Optional[float]
    profit_loss_percent: Optional[float]
    trade_status: str
    views_count: int
    comments_count: int
    reactions_count: int
    shares_count: int
    chart_annotations: Optional[dict]
    is_public: bool
    is_pinned: bool
    created_at: datetime
    updated_at: Optional[datetime]
    charts: List[TradePostChartResponse] = []

    class Config:
        from_attributes = True


class TradePostListResponse(BaseModel):
    """Paginated trade post list response"""
    posts: List[TradePostResponse]
    total: int
    page: int
    page_size: int


# ============================================================================
# COMMENT SCHEMAS
# ============================================================================

class CommentCreate(BaseModel):
    """Create comment"""
    content: str = Field(..., min_length=1, max_length=2000)
    parent_comment_id: Optional[int] = None


class CommentUpdate(BaseModel):
    """Update comment"""
    content: str = Field(..., min_length=1, max_length=2000)


class CommentResponse(BaseModel):
    """Comment response"""
    id: int
    user_id: int
    username: str
    post_id: int
    parent_comment_id: Optional[int]
    content: str
    reactions_count: int
    is_edited: bool
    is_deleted: bool
    created_at: datetime
    updated_at: Optional[datetime]
    replies: List['CommentResponse'] = []

    class Config:
        from_attributes = True


# ============================================================================
# REACTION SCHEMAS
# ============================================================================

class ReactionCreate(BaseModel):
    """Create reaction"""
    reaction_type: str = Field(default="like")  # like, bullish, bearish, fire


class ReactionResponse(BaseModel):
    """Reaction response"""
    id: int
    user_id: int
    username: str
    reaction_type: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# LEADERBOARD SCHEMAS
# ============================================================================

class LeaderboardEntry(BaseModel):
    """Leaderboard entry"""
    rank: int
    user_id: int
    username: str
    avatar_url: Optional[str]
    total_trades: int
    win_rate: float
    total_return: float
    avg_return_per_trade: float
    total_followers: int
    total_posts: int

    class Config:
        from_attributes = True


class LeaderboardResponse(BaseModel):
    """Leaderboard response"""
    leaderboard: List[LeaderboardEntry]
    period: str
    updated_at: datetime


# ============================================================================
# SOCIAL ANALYTICS SCHEMAS
# ============================================================================

class TrendingTickerResponse(BaseModel):
    """Trending ticker response"""
    ticker_symbol: str
    mention_count: int
    follower_count: int
    sentiment_score: float
    bullish_sentiment: int
    bearish_sentiment: int
    trending_score: float
    time_window: str

    class Config:
        from_attributes = True


class TrendingPatternResponse(BaseModel):
    """Trending pattern response"""
    pattern_type: str
    mention_count: int
    post_count: int
    success_rate: Optional[float]
    avg_return: Optional[float]
    trending_score: float
    time_window: str

    class Config:
        from_attributes = True


class CommunityStatsResponse(BaseModel):
    """Overall community statistics"""
    total_users: int
    total_posts: int
    total_comments: int
    total_reactions: int
    active_users_24h: int
    trending_tickers: List[TrendingTickerResponse]
    trending_patterns: List[TrendingPatternResponse]


class CrowdSentimentResponse(BaseModel):
    """Crowd sentiment for a ticker"""
    ticker_symbol: str
    total_mentions: int
    bullish_count: int
    bearish_count: int
    neutral_count: int
    sentiment_score: float  # -100 to +100
    avg_target_price: Optional[float]
    most_common_pattern: Optional[str]


# Update CommentResponse forward reference
CommentResponse.model_rebuild()
