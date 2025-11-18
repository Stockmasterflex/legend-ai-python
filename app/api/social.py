"""
Social Trading Community API
Endpoints for user profiles, following, trade sharing, and community features
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta

from app.models import (
    User, UserProfile, Follow, TradePost, Comment, Reaction,
    LeaderboardStats, TrendingTicker, TrendingPattern, Ticker
)
from app.schemas.social import (
    UserRegister, UserLogin, Token, UserResponse, UserProfileResponse,
    UserProfileUpdate, FollowCreate, FollowUpdate, FollowResponse,
    TradePostCreate, TradePostUpdate, TradePostResponse, TradePostListResponse,
    CommentCreate, CommentUpdate, CommentResponse,
    ReactionCreate, ReactionResponse,
    LeaderboardResponse, LeaderboardEntry,
    TrendingTickerResponse, TrendingPatternResponse,
    CommunityStatsResponse, CrowdSentimentResponse
)
from app.services.auth import (
    get_password_hash, create_access_token, authenticate_user, get_current_user
)
from app.services.database import get_database_service

router = APIRouter(prefix="/api/social", tags=["social"])


def get_db():
    """Get database session"""
    db_service = get_database_service()
    db = db_service.get_db()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if username exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if email exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        is_active=True
    )
    db.add(user)
    db.flush()

    # Create default profile
    profile = UserProfile(user_id=user.id)
    db.add(profile)

    db.commit()
    db.refresh(user)
    db.refresh(profile)

    user.profile = profile
    return user


@router.post("/auth/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login and get access token"""
    user = authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last login
    user.last_login = datetime.utcnow()
    db.add(user)
    db.commit()

    # Create access token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user's profile"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    current_user.profile = profile
    return current_user


# ============================================================================
# USER PROFILE ENDPOINTS
# ============================================================================

@router.get("/users/{username}", response_model=UserProfileResponse)
async def get_user_profile(username: str, db: Session = Depends(get_db)):
    """Get user profile by username"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    if not profile or not profile.is_public:
        raise HTTPException(status_code=404, detail="Profile not found or private")

    # Add username to response
    profile_dict = {
        **profile.__dict__,
        'username': user.username
    }
    return profile_dict


@router.put("/profile", response_model=UserProfileResponse)
async def update_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    # Update fields
    for field, value in profile_data.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)

    profile_dict = {
        **profile.__dict__,
        'username': current_user.username
    }
    return profile_dict


# ============================================================================
# FOLLOW ENDPOINTS
# ============================================================================

@router.post("/follow", response_model=FollowResponse, status_code=status.HTTP_201_CREATED)
async def follow_user(
    follow_data: FollowCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Follow a user"""
    # Check if user exists
    following_user = db.query(User).filter(User.id == follow_data.following_id).first()
    if not following_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Can't follow yourself
    if current_user.id == follow_data.following_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")

    # Check if already following
    existing = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.following_id == follow_data.following_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already following this user")

    # Create follow relationship
    follow = Follow(
        follower_id=current_user.id,
        following_id=follow_data.following_id,
        copy_trading_enabled=follow_data.copy_trading_enabled,
        copy_percentage=follow_data.copy_percentage,
        max_position_size=follow_data.max_position_size
    )
    db.add(follow)

    # Update follower counts
    follower_profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    following_profile = db.query(UserProfile).filter(UserProfile.user_id == follow_data.following_id).first()

    if follower_profile:
        follower_profile.total_following += 1
    if following_profile:
        following_profile.total_followers += 1

    db.commit()
    db.refresh(follow)

    return {
        **follow.__dict__,
        'following_username': following_user.username
    }


@router.delete("/follow/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Unfollow a user"""
    follow = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.following_id == user_id
    ).first()

    if not follow:
        raise HTTPException(status_code=404, detail="Not following this user")

    # Update follower counts
    follower_profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    following_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    if follower_profile:
        follower_profile.total_following = max(0, follower_profile.total_following - 1)
    if following_profile:
        following_profile.total_followers = max(0, following_profile.total_followers - 1)

    db.delete(follow)
    db.commit()


@router.get("/following", response_model=List[FollowResponse])
async def get_following(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of users I'm following"""
    follows = db.query(Follow, User.username).join(
        User, Follow.following_id == User.id
    ).filter(
        Follow.follower_id == current_user.id
    ).all()

    return [
        {**follow.__dict__, 'following_username': username}
        for follow, username in follows
    ]


@router.get("/followers", response_model=List[dict])
async def get_followers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of my followers"""
    followers = db.query(User).join(
        Follow, Follow.follower_id == User.id
    ).filter(
        Follow.following_id == current_user.id
    ).all()

    return [
        {'id': user.id, 'username': user.username, 'full_name': user.full_name}
        for user in followers
    ]


# ============================================================================
# TRADE POST ENDPOINTS
# ============================================================================

@router.post("/posts", response_model=TradePostResponse, status_code=status.HTTP_201_CREATED)
async def create_trade_post(
    post_data: TradePostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new trade post"""
    # Get or create ticker if symbol provided
    ticker_id = None
    if post_data.ticker_symbol:
        ticker = db.query(Ticker).filter(
            Ticker.symbol == post_data.ticker_symbol.upper()
        ).first()
        if not ticker:
            ticker = Ticker(symbol=post_data.ticker_symbol.upper())
            db.add(ticker)
            db.flush()
        ticker_id = ticker.id

    # Create post
    post = TradePost(
        user_id=current_user.id,
        ticker_id=ticker_id,
        title=post_data.title,
        content=post_data.content,
        post_type=post_data.post_type,
        entry_price=post_data.entry_price,
        stop_price=post_data.stop_price,
        target_price=post_data.target_price,
        position_size=post_data.position_size,
        pattern_type=post_data.pattern_type,
        chart_annotations=post_data.chart_annotations,
        is_public=post_data.is_public
    )
    db.add(post)

    # Update user profile post count
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if profile:
        profile.total_posts += 1

    db.commit()
    db.refresh(post)

    return {
        **post.__dict__,
        'username': current_user.username,
        'ticker_symbol': post_data.ticker_symbol,
        'charts': []
    }


@router.get("/posts", response_model=TradePostListResponse)
async def get_trade_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    post_type: Optional[str] = None,
    ticker_symbol: Optional[str] = None,
    username: Optional[str] = None,
    following_only: bool = False,
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get trade posts with filtering and pagination"""
    query = db.query(TradePost, User.username, Ticker.symbol).join(
        User, TradePost.user_id == User.id
    ).outerjoin(
        Ticker, TradePost.ticker_id == Ticker.id
    ).filter(TradePost.is_public == True)

    # Apply filters
    if post_type:
        query = query.filter(TradePost.post_type == post_type)

    if ticker_symbol:
        query = query.filter(Ticker.symbol == ticker_symbol.upper())

    if username:
        query = query.filter(User.username == username)

    if following_only and current_user:
        # Only show posts from users I'm following
        following_ids = db.query(Follow.following_id).filter(
            Follow.follower_id == current_user.id
        ).all()
        following_ids = [fid[0] for fid in following_ids]
        query = query.filter(TradePost.user_id.in_(following_ids))

    # Get total count
    total = query.count()

    # Paginate
    offset = (page - 1) * page_size
    posts_data = query.order_by(desc(TradePost.created_at)).offset(offset).limit(page_size).all()

    posts = [
        {**post.__dict__, 'username': username, 'ticker_symbol': symbol, 'charts': []}
        for post, username, symbol in posts_data
    ]

    return {
        'posts': posts,
        'total': total,
        'page': page,
        'page_size': page_size
    }


@router.get("/posts/{post_id}", response_model=TradePostResponse)
async def get_trade_post(post_id: int, db: Session = Depends(get_db)):
    """Get a specific trade post"""
    result = db.query(TradePost, User.username, Ticker.symbol).join(
        User, TradePost.user_id == User.id
    ).outerjoin(
        Ticker, TradePost.ticker_id == Ticker.id
    ).filter(TradePost.id == post_id).first()

    if not result:
        raise HTTPException(status_code=404, detail="Post not found")

    post, username, symbol = result

    if not post.is_public:
        raise HTTPException(status_code=403, detail="Post is private")

    # Increment view count
    post.views_count += 1
    db.commit()

    return {
        **post.__dict__,
        'username': username,
        'ticker_symbol': symbol,
        'charts': []
    }


@router.put("/posts/{post_id}", response_model=TradePostResponse)
async def update_trade_post(
    post_id: int,
    post_data: TradePostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a trade post"""
    post = db.query(TradePost).filter(TradePost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    # Update fields
    for field, value in post_data.model_dump(exclude_unset=True).items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)

    ticker_symbol = None
    if post.ticker_id:
        ticker = db.query(Ticker).filter(Ticker.id == post.ticker_id).first()
        if ticker:
            ticker_symbol = ticker.symbol

    return {
        **post.__dict__,
        'username': current_user.username,
        'ticker_symbol': ticker_symbol,
        'charts': []
    }


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trade_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a trade post"""
    post = db.query(TradePost).filter(TradePost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    # Update user profile post count
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if profile:
        profile.total_posts = max(0, profile.total_posts - 1)

    db.delete(post)
    db.commit()


# ============================================================================
# COMMENT ENDPOINTS
# ============================================================================

@router.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a comment to a post"""
    # Check if post exists
    post = db.query(TradePost).filter(TradePost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Create comment
    comment = Comment(
        user_id=current_user.id,
        post_id=post_id,
        content=comment_data.content,
        parent_comment_id=comment_data.parent_comment_id
    )
    db.add(comment)

    # Update post comment count
    post.comments_count += 1

    db.commit()
    db.refresh(comment)

    return {
        **comment.__dict__,
        'username': current_user.username,
        'replies': []
    }


@router.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
async def get_comments(post_id: int, db: Session = Depends(get_db)):
    """Get comments for a post"""
    comments = db.query(Comment, User.username).join(
        User, Comment.user_id == User.id
    ).filter(
        Comment.post_id == post_id,
        Comment.is_deleted == False,
        Comment.parent_comment_id == None  # Only top-level comments
    ).order_by(Comment.created_at.desc()).all()

    result = []
    for comment, username in comments:
        # Get replies for this comment
        replies = db.query(Comment, User.username).join(
            User, Comment.user_id == User.id
        ).filter(
            Comment.parent_comment_id == comment.id,
            Comment.is_deleted == False
        ).order_by(Comment.created_at).all()

        comment_dict = {
            **comment.__dict__,
            'username': username,
            'replies': [
                {**reply.__dict__, 'username': reply_username, 'replies': []}
                for reply, reply_username in replies
            ]
        }
        result.append(comment_dict)

    return result


@router.put("/comments/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a comment"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")

    comment.content = comment_data.content
    comment.is_edited = True

    db.commit()
    db.refresh(comment)

    return {
        **comment.__dict__,
        'username': current_user.username,
        'replies': []
    }


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a comment (soft delete)"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

    # Soft delete
    comment.is_deleted = True
    comment.content = "[deleted]"

    # Update post comment count
    post = db.query(TradePost).filter(TradePost.id == comment.post_id).first()
    if post:
        post.comments_count = max(0, post.comments_count - 1)

    db.commit()


# ============================================================================
# REACTION ENDPOINTS
# ============================================================================

@router.post("/posts/{post_id}/reactions", response_model=ReactionResponse, status_code=status.HTTP_201_CREATED)
async def add_post_reaction(
    post_id: int,
    reaction_data: ReactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a reaction to a post"""
    # Check if post exists
    post = db.query(TradePost).filter(TradePost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if already reacted
    existing = db.query(Reaction).filter(
        Reaction.user_id == current_user.id,
        Reaction.post_id == post_id
    ).first()

    if existing:
        # Update reaction type
        existing.reaction_type = reaction_data.reaction_type
        db.commit()
        db.refresh(existing)
        return {
            **existing.__dict__,
            'username': current_user.username
        }

    # Create new reaction
    reaction = Reaction(
        user_id=current_user.id,
        post_id=post_id,
        reaction_type=reaction_data.reaction_type
    )
    db.add(reaction)

    # Update post reaction count
    post.reactions_count += 1

    db.commit()
    db.refresh(reaction)

    return {
        **reaction.__dict__,
        'username': current_user.username
    }


@router.delete("/posts/{post_id}/reactions", status_code=status.HTTP_204_NO_CONTENT)
async def remove_post_reaction(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove reaction from a post"""
    reaction = db.query(Reaction).filter(
        Reaction.user_id == current_user.id,
        Reaction.post_id == post_id
    ).first()

    if not reaction:
        raise HTTPException(status_code=404, detail="Reaction not found")

    # Update post reaction count
    post = db.query(TradePost).filter(TradePost.id == post_id).first()
    if post:
        post.reactions_count = max(0, post.reactions_count - 1)

    db.delete(reaction)
    db.commit()


# ============================================================================
# LEADERBOARD ENDPOINTS
# ============================================================================

@router.get("/leaderboard", response_model=LeaderboardResponse)
async def get_leaderboard(
    period: str = Query("all_time", regex="^(all_time|monthly|weekly)$"),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get trading leaderboard"""
    leaderboard_data = db.query(
        LeaderboardStats, User.username, UserProfile.avatar_url
    ).join(
        User, LeaderboardStats.user_id == User.id
    ).outerjoin(
        UserProfile, User.id == UserProfile.user_id
    ).filter(
        LeaderboardStats.period == period
    ).order_by(
        desc(LeaderboardStats.win_rate),
        desc(LeaderboardStats.total_return)
    ).limit(limit).all()

    entries = [
        LeaderboardEntry(
            rank=idx + 1,
            user_id=stats.user_id,
            username=username,
            avatar_url=avatar_url,
            total_trades=stats.total_trades,
            win_rate=stats.win_rate,
            total_return=stats.total_return,
            avg_return_per_trade=stats.avg_return_per_trade,
            total_followers=stats.total_followers,
            total_posts=stats.total_posts
        )
        for idx, (stats, username, avatar_url) in enumerate(leaderboard_data)
    ]

    return LeaderboardResponse(
        leaderboard=entries,
        period=period,
        updated_at=datetime.utcnow()
    )


# ============================================================================
# SOCIAL ANALYTICS ENDPOINTS
# ============================================================================

@router.get("/analytics/trending-tickers", response_model=List[TrendingTickerResponse])
async def get_trending_tickers(
    time_window: str = Query("24h", regex="^(1h|24h|7d|30d)$"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get trending tickers"""
    trending = db.query(TrendingTicker, Ticker.symbol).join(
        Ticker, TrendingTicker.ticker_id == Ticker.id
    ).filter(
        TrendingTicker.time_window == time_window
    ).order_by(
        desc(TrendingTicker.trending_score)
    ).limit(limit).all()

    return [
        TrendingTickerResponse(
            ticker_symbol=symbol,
            mention_count=trend.mention_count,
            follower_count=trend.follower_count,
            sentiment_score=trend.sentiment_score,
            bullish_sentiment=trend.bullish_sentiment,
            bearish_sentiment=trend.bearish_sentiment,
            trending_score=trend.trending_score,
            time_window=trend.time_window
        )
        for trend, symbol in trending
    ]


@router.get("/analytics/trending-patterns", response_model=List[TrendingPatternResponse])
async def get_trending_patterns(
    time_window: str = Query("7d", regex="^(1h|24h|7d|30d)$"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get trending patterns"""
    patterns = db.query(TrendingPattern).filter(
        TrendingPattern.time_window == time_window
    ).order_by(
        desc(TrendingPattern.trending_score)
    ).limit(limit).all()

    return [
        TrendingPatternResponse(
            pattern_type=pattern.pattern_type,
            mention_count=pattern.mention_count,
            post_count=pattern.post_count,
            success_rate=pattern.success_rate,
            avg_return=pattern.avg_return,
            trending_score=pattern.trending_score,
            time_window=pattern.time_window
        )
        for pattern in patterns
    ]


@router.get("/analytics/community-stats", response_model=CommunityStatsResponse)
async def get_community_stats(db: Session = Depends(get_db)):
    """Get overall community statistics"""
    total_users = db.query(func.count(User.id)).scalar()
    total_posts = db.query(func.count(TradePost.id)).scalar()
    total_comments = db.query(func.count(Comment.id)).scalar()
    total_reactions = db.query(func.count(Reaction.id)).scalar()

    # Active users in last 24h
    yesterday = datetime.utcnow() - timedelta(days=1)
    active_users_24h = db.query(func.count(func.distinct(User.id))).filter(
        User.last_login >= yesterday
    ).scalar()

    # Get top trending tickers and patterns
    trending_tickers_data = db.query(TrendingTicker, Ticker.symbol).join(
        Ticker, TrendingTicker.ticker_id == Ticker.id
    ).filter(
        TrendingTicker.time_window == "24h"
    ).order_by(desc(TrendingTicker.trending_score)).limit(5).all()

    trending_tickers = [
        TrendingTickerResponse(
            ticker_symbol=symbol,
            mention_count=trend.mention_count,
            follower_count=trend.follower_count,
            sentiment_score=trend.sentiment_score,
            bullish_sentiment=trend.bullish_sentiment,
            bearish_sentiment=trend.bearish_sentiment,
            trending_score=trend.trending_score,
            time_window=trend.time_window
        )
        for trend, symbol in trending_tickers_data
    ]

    trending_patterns_data = db.query(TrendingPattern).filter(
        TrendingPattern.time_window == "7d"
    ).order_by(desc(TrendingPattern.trending_score)).limit(5).all()

    trending_patterns = [
        TrendingPatternResponse(
            pattern_type=pattern.pattern_type,
            mention_count=pattern.mention_count,
            post_count=pattern.post_count,
            success_rate=pattern.success_rate,
            avg_return=pattern.avg_return,
            trending_score=pattern.trending_score,
            time_window=pattern.time_window
        )
        for pattern in trending_patterns_data
    ]

    return CommunityStatsResponse(
        total_users=total_users or 0,
        total_posts=total_posts or 0,
        total_comments=total_comments or 0,
        total_reactions=total_reactions or 0,
        active_users_24h=active_users_24h or 0,
        trending_tickers=trending_tickers,
        trending_patterns=trending_patterns
    )


@router.get("/analytics/sentiment/{ticker_symbol}", response_model=CrowdSentimentResponse)
async def get_crowd_sentiment(ticker_symbol: str, db: Session = Depends(get_db)):
    """Get crowd sentiment for a specific ticker"""
    ticker = db.query(Ticker).filter(Ticker.symbol == ticker_symbol.upper()).first()
    if not ticker:
        raise HTTPException(status_code=404, detail="Ticker not found")

    # Count posts mentioning this ticker
    total_mentions = db.query(func.count(TradePost.id)).filter(
        TradePost.ticker_id == ticker.id
    ).scalar()

    # Count bullish/bearish reactions
    bullish = db.query(func.count(Reaction.id)).join(
        TradePost, Reaction.post_id == TradePost.id
    ).filter(
        TradePost.ticker_id == ticker.id,
        Reaction.reaction_type == 'bullish'
    ).scalar()

    bearish = db.query(func.count(Reaction.id)).join(
        TradePost, Reaction.post_id == TradePost.id
    ).filter(
        TradePost.ticker_id == ticker.id,
        Reaction.reaction_type == 'bearish'
    ).scalar()

    neutral = total_mentions - (bullish + bearish) if total_mentions > 0 else 0

    # Calculate sentiment score (-100 to +100)
    sentiment_score = 0.0
    if total_mentions > 0:
        sentiment_score = ((bullish - bearish) / total_mentions) * 100

    # Get average target price
    avg_target = db.query(func.avg(TradePost.target_price)).filter(
        TradePost.ticker_id == ticker.id,
        TradePost.target_price != None
    ).scalar()

    # Get most common pattern
    most_common_pattern = db.query(
        TradePost.pattern_type,
        func.count(TradePost.pattern_type).label('count')
    ).filter(
        TradePost.ticker_id == ticker.id,
        TradePost.pattern_type != None
    ).group_by(
        TradePost.pattern_type
    ).order_by(
        desc('count')
    ).first()

    return CrowdSentimentResponse(
        ticker_symbol=ticker_symbol.upper(),
        total_mentions=total_mentions or 0,
        bullish_count=bullish or 0,
        bearish_count=bearish or 0,
        neutral_count=neutral or 0,
        sentiment_score=sentiment_score,
        avg_target_price=float(avg_target) if avg_target else None,
        most_common_pattern=most_common_pattern[0] if most_common_pattern else None
    )
