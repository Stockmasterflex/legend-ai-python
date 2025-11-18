"""
Engagement and Gamification API
Provides endpoints for user progress, achievements, and engagement features
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

from app.services.engagement import EngagementService
from app.services.tutorial import TutorialService
from app.services.learning_center import LearningCenterService


router = APIRouter(prefix="/api/engagement", tags=["engagement"])


# Mock database dependency (replace with actual DB setup)
def get_db():
    """Get database session - Replace with actual DB implementation"""
    # For now, this is a placeholder
    # In production, this would return an actual SQLAlchemy session
    pass


# Pydantic models
class ActivityTrack(BaseModel):
    activity_type: str
    metadata: Optional[Dict[str, Any]] = None


class TutorialStep(BaseModel):
    tutorial_key: str


class ProgressUpdate(BaseModel):
    content_key: str
    progress: int
    completed: bool = False


# ===== User Progress & Stats =====

@router.get("/stats/{user_id}")
async def get_user_stats(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get comprehensive user statistics including level, XP, achievements, and streaks

    **Returns:**
    - User level and XP progress
    - Activity statistics
    - Unlocked achievements
    - Current and longest streaks
    """
    try:
        stats = await EngagementService.get_user_stats(db, user_id)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/track/{user_id}")
async def track_activity(
    user_id: str,
    activity: ActivityTrack,
    db: Session = Depends(get_db)
):
    """
    Track user activity and award XP

    **Activity Types:**
    - `scan`: Pattern scan (+10 XP)
    - `analyze`: Stock analysis (+20 XP)
    - `watchlist_add`: Add to watchlist (+15 XP)
    - `pattern_detect`: Pattern detected (+25 XP)
    - `profitable_idea`: Profitable trade idea (+50 XP)
    - `tutorial_complete`: Complete tutorial (+100 XP)
    - `learning_complete`: Complete learning content (+30 XP)

    **Returns:**
    - XP earned
    - Level up status
    - New achievements unlocked
    """
    try:
        result = await EngagementService.track_activity(
            db, user_id, activity.activity_type, activity.metadata
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/leaderboard")
async def get_leaderboard(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get top users by XP

    **Returns:**
    - Top users ranked by XP
    - User level, XP, and streak information
    """
    try:
        leaderboard = await EngagementService.get_leaderboard(db, limit)
        return {"leaderboard": leaderboard}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== Achievements =====

@router.get("/achievements/{user_id}")
async def get_user_achievements(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Get user's unlocked achievements

    **Available Achievements:**
    - First Pattern Detected (1 pattern)
    - 10 Stocks Analyzed
    - First Profitable Trade Idea
    - Watchlist Master (50+ stocks)
    - Pattern Expert (100 scans)
    - Week Warrior (7-day streak)
    - Month Master (30-day streak)
    """
    try:
        stats = await EngagementService.get_user_stats(db, user_id)
        return {
            "achievements": stats["achievements"],
            "total": stats["total_achievements"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== Tutorials & Onboarding =====

@router.get("/tutorials")
async def get_tutorials():
    """
    Get all available tutorials

    **Available Tutorials:**
    - Onboarding walkthrough
    - VCP Pattern education
    - Cup & Handle guide
    - Risk Management 101
    """
    tutorials = await TutorialService.get_all_tutorials()
    return {"tutorials": tutorials}


@router.get("/tutorials/{tutorial_key}")
async def get_tutorial(tutorial_key: str):
    """Get specific tutorial definition"""
    tutorial = await TutorialService.get_tutorial(tutorial_key)
    if not tutorial:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    return tutorial


@router.post("/tutorials/{user_id}/start")
async def start_tutorial(
    user_id: str,
    step: TutorialStep,
    db: Session = Depends(get_db)
):
    """
    Start or resume a tutorial

    **Returns:**
    - Tutorial information
    - Current step data
    - Progress tracking
    """
    try:
        result = await TutorialService.start_tutorial(db, user_id, step.tutorial_key)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tutorials/{user_id}/next")
async def next_tutorial_step(
    user_id: str,
    step: TutorialStep,
    db: Session = Depends(get_db)
):
    """Move to next tutorial step"""
    try:
        result = await TutorialService.next_step(db, user_id, step.tutorial_key)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tutorials/{user_id}/skip")
async def skip_tutorial(
    user_id: str,
    step: TutorialStep,
    db: Session = Depends(get_db)
):
    """Skip a tutorial"""
    try:
        result = await TutorialService.skip_tutorial(db, user_id, step.tutorial_key)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tutorials/{user_id}/progress/{tutorial_key}")
async def get_tutorial_progress(
    user_id: str,
    tutorial_key: str,
    db: Session = Depends(get_db)
):
    """Get user's tutorial progress"""
    try:
        progress = await TutorialService.get_user_tutorial_progress(db, user_id, tutorial_key)
        return progress or {"message": "Tutorial not started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/onboarding/{user_id}")
async def check_onboarding(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Check if user should see onboarding

    **Returns:**
    - Boolean indicating if onboarding should be shown
    """
    try:
        should_show = await TutorialService.should_show_onboarding(db, user_id)
        return {"show_onboarding": should_show}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tooltips")
async def get_tooltips():
    """
    Get all tooltip definitions for UI elements

    **Tooltips include:**
    - Pattern scanner
    - VCP score explanation
    - Entry/stop/target prices
    - Risk/reward ratio
    - Volume analysis
    - Relative strength
    """
    tooltips = await TutorialService.get_all_tooltips()
    return {"tooltips": tooltips}


@router.get("/tooltips/{tooltip_key}")
async def get_tooltip(tooltip_key: str):
    """Get specific tooltip"""
    tooltip = await TutorialService.get_tooltip(tooltip_key)
    if not tooltip:
        raise HTTPException(status_code=404, detail="Tooltip not found")
    return tooltip


# ===== Learning Center =====

@router.get("/learning")
async def get_learning_content(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all learning content

    **Categories:**
    - `pattern`: Pattern education
    - `strategy`: Trading strategies
    - `glossary`: Trading terms
    - `best_practice`: Best practices

    **Difficulty:**
    - `beginner`
    - `intermediate`
    - `advanced`
    """
    try:
        content = await LearningCenterService.get_all_content(db, category, difficulty)
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/learning/{content_key}")
async def get_learning_content_detail(
    content_key: str,
    db: Session = Depends(get_db)
):
    """Get detailed learning content"""
    try:
        content = await LearningCenterService.get_content(db, content_key)
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/learning/categories/list")
async def get_learning_categories(db: Session = Depends(get_db)):
    """
    Get all learning categories with counts

    **Returns:**
    - Category name, icon, description
    - Number of articles in each category
    """
    try:
        categories = await LearningCenterService.get_categories(db)
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/learning/{user_id}/progress")
async def track_learning_progress(
    user_id: str,
    progress: ProgressUpdate,
    db: Session = Depends(get_db)
):
    """Track user progress on learning content"""
    try:
        result = await LearningCenterService.track_progress(
            db, user_id, progress.content_key, progress.progress, progress.completed
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/learning/{user_id}/progress")
async def get_user_learning_progress(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get user's learning progress"""
    try:
        progress = await LearningCenterService.get_user_progress(db, user_id)
        return {"progress": progress}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/learning/{user_id}/bookmark/{content_key}")
async def toggle_bookmark(
    user_id: str,
    content_key: str,
    db: Session = Depends(get_db)
):
    """Bookmark or unbookmark learning content"""
    try:
        result = await LearningCenterService.toggle_bookmark(db, user_id, content_key)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/learning/{user_id}/bookmarks")
async def get_bookmarks(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get user's bookmarked content"""
    try:
        bookmarks = await LearningCenterService.get_bookmarks(db, user_id)
        return {"bookmarks": bookmarks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== Community Stats =====

@router.get("/community/stats")
async def get_community_stats(db: Session = Depends(get_db)):
    """
    Get community statistics and social proof

    **Returns:**
    - Patterns detected today
    - Top pattern this week
    - Most watched ticker
    - Active users count
    """
    try:
        stats = await EngagementService.get_community_stats(db)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/init")
async def init_engagement_data(db: Session = Depends(get_db)):
    """
    Initialize engagement system (Admin only)

    **Initializes:**
    - Achievement definitions
    - Learning content
    - Community stats
    """
    try:
        await EngagementService.init_achievements(db)
        await LearningCenterService.init_content(db)
        await EngagementService.update_community_stats(db)
        return {"message": "Engagement system initialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
