"""
Auto-posting API endpoints
Manage scheduled posts, analytics, and community engagement
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

from app.services.database import get_db
from app.services.content_generator import ContentGenerator
from app.services.social_poster import SocialPoster
from app.services.auto_posting import AutoPostingService
from app.services.community_engagement import CommunityEngagementService
from app.models import (
    ScheduledPost, PostLog, PostAnalytics,
    CommunityEngagement as CommunityEngagementModel
)
from app.config import get_settings

router = APIRouter(prefix="/api/v1/auto-posting", tags=["auto-posting"])


# Pydantic models for requests/responses
class SchedulePostRequest(BaseModel):
    """Request to schedule a post"""
    pattern_scan_id: int
    platforms: List[str] = Field(..., description="List of platforms: twitter, reddit, linkedin, stocktwits")
    scheduled_time: Optional[datetime] = None
    post_immediately: bool = False


class SchedulePostResponse(BaseModel):
    """Response for scheduled post"""
    id: int
    status: str
    scheduled_time: datetime
    platforms: List[str]
    content_type: str


class PostAnalyticsResponse(BaseModel):
    """Analytics for a post"""
    post_id: int
    platform: str
    likes: int
    shares: int
    comments: int
    impressions: int
    engagement_rate: float
    checked_at: datetime


class AnalyticsSummaryResponse(BaseModel):
    """Summary of analytics"""
    total_posts: int
    total_likes: int
    total_shares: int
    total_comments: int
    total_engagement: int
    avg_engagement_rate: float
    follower_growth: int
    platform: str


class EngagementStatsResponse(BaseModel):
    """Community engagement statistics"""
    total_engagements: int
    replies: int
    follows: int
    dms: int
    completed: int
    failed: int
    pending: int


class UpdateScheduleRequest(BaseModel):
    """Update scheduled post"""
    scheduled_time: Optional[datetime] = None
    status: Optional[str] = None  # pending, cancelled
    platforms: Optional[List[str]] = None


# Initialize services (will be properly configured with credentials)
content_generator = ContentGenerator()


def get_auto_posting_service(db: Session = Depends(get_db)) -> AutoPostingService:
    """Get auto-posting service instance"""
    settings = get_settings()

    # Initialize social poster with credentials from settings
    social_poster = SocialPoster(
        twitter_credentials=settings.TWITTER_CREDENTIALS if hasattr(settings, 'TWITTER_CREDENTIALS') else None,
        reddit_credentials=settings.REDDIT_CREDENTIALS if hasattr(settings, 'REDDIT_CREDENTIALS') else None,
        linkedin_credentials=settings.LINKEDIN_CREDENTIALS if hasattr(settings, 'LINKEDIN_CREDENTIALS') else None
    )

    return AutoPostingService(db, content_generator, social_poster)


def get_community_service(db: Session = Depends(get_db)) -> CommunityEngagementService:
    """Get community engagement service instance"""
    settings = get_settings()
    social_poster = SocialPoster(
        twitter_credentials=settings.TWITTER_CREDENTIALS if hasattr(settings, 'TWITTER_CREDENTIALS') else None,
        reddit_credentials=settings.REDDIT_CREDENTIALS if hasattr(settings, 'REDDIT_CREDENTIALS') else None
    )

    return CommunityEngagementService(db, social_poster)


@router.post("/schedule", response_model=SchedulePostResponse)
async def schedule_post(
    request: SchedulePostRequest,
    service: AutoPostingService = Depends(get_auto_posting_service)
):
    """
    Schedule a post for a detected pattern

    - **pattern_scan_id**: ID of the pattern scan to post about
    - **platforms**: List of platforms to post to (twitter, reddit, linkedin, stocktwits)
    - **scheduled_time**: When to post (optional, will use optimal time if not provided)
    - **post_immediately**: Post immediately instead of scheduling
    """
    try:
        scheduled_post = await service.schedule_pattern_post(
            pattern_scan_id=request.pattern_scan_id,
            platforms=request.platforms,
            scheduled_time=request.scheduled_time,
            post_immediately=request.post_immediately
        )

        return SchedulePostResponse(
            id=scheduled_post.id,
            status=scheduled_post.status,
            scheduled_time=scheduled_post.scheduled_time,
            platforms=scheduled_post.platforms,
            content_type=scheduled_post.content_type
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to schedule post: {str(e)}")


@router.get("/scheduled", response_model=List[SchedulePostResponse])
async def get_scheduled_posts(
    status: Optional[str] = Query(None, description="Filter by status: pending, posted, failed"),
    platform: Optional[str] = Query(None, description="Filter by platform"),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get scheduled posts

    - **status**: Filter by status (pending, posted, failed, cancelled)
    - **platform**: Filter by platform
    - **limit**: Maximum number of posts to return
    """
    query = db.query(ScheduledPost)

    if status:
        query = query.filter(ScheduledPost.status == status)

    if platform:
        query = query.filter(ScheduledPost.platforms.contains([platform]))

    posts = query.order_by(ScheduledPost.scheduled_time.desc()).limit(limit).all()

    return [
        SchedulePostResponse(
            id=post.id,
            status=post.status,
            scheduled_time=post.scheduled_time,
            platforms=post.platforms,
            content_type=post.content_type
        )
        for post in posts
    ]


@router.put("/scheduled/{post_id}")
async def update_scheduled_post(
    post_id: int,
    request: UpdateScheduleRequest,
    db: Session = Depends(get_db)
):
    """
    Update a scheduled post

    - **post_id**: ID of the post to update
    - **scheduled_time**: New scheduled time
    - **status**: New status (pending, cancelled)
    - **platforms**: Update platforms to post to
    """
    post = db.query(ScheduledPost).filter(ScheduledPost.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Scheduled post not found")

    if post.status in ["posted", "posting"]:
        raise HTTPException(status_code=400, detail="Cannot update post that is already posted or posting")

    if request.scheduled_time:
        post.scheduled_time = request.scheduled_time

    if request.status:
        if request.status not in ["pending", "cancelled"]:
            raise HTTPException(status_code=400, detail="Invalid status")
        post.status = request.status

    if request.platforms:
        post.platforms = request.platforms

    db.commit()

    return {"message": "Scheduled post updated successfully", "id": post_id}


@router.delete("/scheduled/{post_id}")
async def delete_scheduled_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a scheduled post

    - **post_id**: ID of the post to delete
    """
    post = db.query(ScheduledPost).filter(ScheduledPost.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Scheduled post not found")

    if post.status in ["posted", "posting"]:
        raise HTTPException(status_code=400, detail="Cannot delete post that is already posted or posting")

    db.delete(post)
    db.commit()

    return {"message": "Scheduled post deleted successfully", "id": post_id}


@router.get("/analytics/summary", response_model=AnalyticsSummaryResponse)
async def get_analytics_summary(
    platform: Optional[str] = Query(None, description="Filter by platform"),
    days: int = Query(7, ge=1, le=90, description="Number of days to analyze"),
    service: AutoPostingService = Depends(get_auto_posting_service)
):
    """
    Get analytics summary for posts

    - **platform**: Filter by specific platform (optional)
    - **days**: Number of days to include in summary (1-90)
    """
    summary = service.get_analytics_summary(platform=platform, days=days)

    return AnalyticsSummaryResponse(**summary)


@router.get("/analytics/posts", response_model=List[PostAnalyticsResponse])
async def get_post_analytics(
    platform: Optional[str] = Query(None, description="Filter by platform"),
    days: int = Query(7, ge=1, le=90),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get detailed analytics for individual posts

    - **platform**: Filter by platform
    - **days**: Number of days to include
    - **limit**: Maximum number of posts to return
    """
    cutoff_date = datetime.now() - timedelta(days=days)

    query = db.query(PostAnalytics).join(PostLog).filter(
        PostLog.posted_at >= cutoff_date
    )

    if platform:
        query = query.filter(PostAnalytics.platform == platform)

    analytics = query.order_by(PostAnalytics.checked_at.desc()).limit(limit).all()

    return [
        PostAnalyticsResponse(
            post_id=a.post_log_id,
            platform=a.platform,
            likes=a.likes,
            shares=a.shares,
            comments=a.comments,
            impressions=a.impressions,
            engagement_rate=a.engagement_rate,
            checked_at=a.checked_at
        )
        for a in analytics
    ]


@router.get("/analytics/best-times")
async def get_best_posting_times(
    platform: str = Query(..., description="Platform to analyze"),
    db: Session = Depends(get_db)
):
    """
    Get best posting times based on historical engagement

    - **platform**: Platform to analyze (twitter, reddit, linkedin)
    """
    # Get posts from last 30 days
    cutoff_date = datetime.now() - timedelta(days=30)

    analytics = db.query(PostAnalytics).join(PostLog).filter(
        PostLog.posted_at >= cutoff_date,
        PostAnalytics.platform == platform
    ).all()

    if not analytics:
        return {"message": "Not enough data to determine best posting times"}

    # Analyze engagement by hour
    hour_engagement = {}
    for a in analytics:
        post_log = db.query(PostLog).filter(PostLog.id == a.post_log_id).first()
        if post_log and post_log.posted_at:
            hour = post_log.posted_at.hour
            if hour not in hour_engagement:
                hour_engagement[hour] = {"total_engagement": 0, "count": 0}

            hour_engagement[hour]["total_engagement"] += a.engagement_rate
            hour_engagement[hour]["count"] += 1

    # Calculate average engagement per hour
    avg_engagement_by_hour = {
        hour: data["total_engagement"] / data["count"]
        for hour, data in hour_engagement.items()
    }

    # Get top 3 hours
    best_hours = sorted(avg_engagement_by_hour.items(), key=lambda x: x[1], reverse=True)[:3]

    return {
        "platform": platform,
        "best_posting_hours": [
            {"hour": hour, "avg_engagement_rate": round(rate, 2)}
            for hour, rate in best_hours
        ]
    }


@router.post("/engagement/process-mentions")
async def process_mentions(
    platform: str = Query(..., description="Platform to process mentions from"),
    limit: int = Query(50, ge=1, le=100),
    service: CommunityEngagementService = Depends(get_community_service)
):
    """
    Process and respond to mentions

    - **platform**: Platform to process (twitter, reddit)
    - **limit**: Maximum number of mentions to process
    """
    try:
        await service.process_mentions(platform, limit)
        return {"message": f"Processed mentions for {platform}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process mentions: {str(e)}")


@router.post("/engagement/process-followers")
async def process_new_followers(
    platform: str = Query(..., description="Platform to process followers from"),
    service: CommunityEngagementService = Depends(get_community_service)
):
    """
    Process new followers and follow back

    - **platform**: Platform to process (twitter)
    """
    try:
        await service.process_new_followers(platform)
        return {"message": f"Processed new followers for {platform}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process followers: {str(e)}")


@router.get("/engagement/stats", response_model=EngagementStatsResponse)
async def get_engagement_stats(
    days: int = Query(7, ge=1, le=90),
    service: CommunityEngagementService = Depends(get_community_service)
):
    """
    Get community engagement statistics

    - **days**: Number of days to include in stats
    """
    stats = service.get_engagement_stats(days=days)
    return EngagementStatsResponse(**stats)


@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint for auto-posting service
    """
    try:
        # Check database connection
        pending_count = db.query(ScheduledPost).filter(
            ScheduledPost.status == "pending"
        ).count()

        # Check recent posts
        cutoff_date = datetime.now() - timedelta(hours=24)
        recent_posts = db.query(PostLog).filter(
            PostLog.posted_at >= cutoff_date
        ).count()

        return {
            "status": "healthy",
            "pending_posts": pending_count,
            "posts_last_24h": recent_posts,
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")
