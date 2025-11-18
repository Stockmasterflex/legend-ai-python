"""
Engagement and Gamification Service
Handles user progress, achievements, XP, and streaks
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import json
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.models import (
    UserProgress, Achievement, UserAchievement, ActivityLog,
    TutorialProgress, UserLearningProgress, LearningContent, CommunityStats
)


# XP Rewards for different activities
XP_REWARDS = {
    "scan": 10,
    "analyze": 20,
    "watchlist_add": 15,
    "pattern_detect": 25,
    "profitable_idea": 50,
    "tutorial_complete": 100,
    "daily_login": 5,
    "learning_complete": 30,
}

# Level thresholds (cumulative XP needed)
LEVEL_THRESHOLDS = [
    0,      # Level 1
    100,    # Level 2
    250,    # Level 3
    500,    # Level 4
    1000,   # Level 5
    2000,   # Level 6
    3500,   # Level 7
    5500,   # Level 8
    8000,   # Level 9
    12000,  # Level 10
]

# Achievement definitions
ACHIEVEMENTS = [
    {
        "achievement_key": "first_pattern",
        "name": "First Pattern Detected",
        "description": "Detected your first trading pattern",
        "category": "patterns",
        "icon": "🎯",
        "required_count": 1,
        "xp_reward": 50,
    },
    {
        "achievement_key": "10_stocks",
        "name": "10 Stocks Analyzed",
        "description": "Analyzed 10 different stocks",
        "category": "analysis",
        "icon": "📊",
        "required_count": 10,
        "xp_reward": 100,
    },
    {
        "achievement_key": "first_profitable",
        "name": "First Profitable Trade Idea",
        "description": "Generated your first profitable trade idea",
        "category": "trading",
        "icon": "💰",
        "required_count": 1,
        "xp_reward": 100,
    },
    {
        "achievement_key": "watchlist_master",
        "name": "Watchlist Master",
        "description": "Added 50+ stocks to your watchlist",
        "category": "watchlist",
        "icon": "📋",
        "required_count": 50,
        "xp_reward": 200,
    },
    {
        "achievement_key": "pattern_expert",
        "name": "Pattern Expert",
        "description": "Completed 100 pattern scans",
        "category": "patterns",
        "icon": "🔍",
        "required_count": 100,
        "xp_reward": 250,
    },
    {
        "achievement_key": "week_warrior",
        "name": "Week Warrior",
        "description": "Maintained a 7-day streak",
        "category": "streak",
        "icon": "🔥",
        "required_count": 7,
        "xp_reward": 150,
    },
    {
        "achievement_key": "month_master",
        "name": "Month Master",
        "description": "Maintained a 30-day streak",
        "category": "streak",
        "icon": "⭐",
        "required_count": 30,
        "xp_reward": 500,
    },
]


class EngagementService:
    """Service for managing user engagement and gamification"""

    @staticmethod
    async def init_achievements(db: Session):
        """Initialize achievement definitions in database"""
        for achievement_data in ACHIEVEMENTS:
            existing = db.query(Achievement).filter(
                Achievement.achievement_key == achievement_data["achievement_key"]
            ).first()

            if not existing:
                achievement = Achievement(**achievement_data)
                db.add(achievement)

        db.commit()

    @staticmethod
    async def get_or_create_user_progress(db: Session, user_id: str) -> UserProgress:
        """Get or create user progress record"""
        progress = db.query(UserProgress).filter(UserProgress.user_id == user_id).first()

        if not progress:
            progress = UserProgress(user_id=user_id)
            db.add(progress)
            db.commit()
            db.refresh(progress)

        return progress

    @staticmethod
    async def track_activity(
        db: Session,
        user_id: str,
        activity_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Track user activity and award XP
        Returns: dict with xp_earned, level_up, new_achievements
        """
        # Get or create user progress
        progress = await EngagementService.get_or_create_user_progress(db, user_id)

        # Calculate XP for this activity
        xp_earned = XP_REWARDS.get(activity_type, 0)

        # Update progress stats
        old_level = progress.level
        progress.xp += xp_earned

        # Update activity-specific counters
        if activity_type == "scan":
            progress.total_scans += 1
        elif activity_type == "analyze":
            progress.stocks_analyzed += 1
        elif activity_type == "pattern_detect":
            progress.patterns_detected += 1
        elif activity_type == "watchlist_add":
            progress.watchlist_items += 1
        elif activity_type == "profitable_idea":
            progress.profitable_ideas += 1

        # Update streak
        await EngagementService._update_streak(progress)

        # Calculate new level
        new_level = EngagementService._calculate_level(progress.xp)
        level_up = new_level > old_level
        progress.level = new_level

        # Log the activity
        activity_log = ActivityLog(
            user_id=user_id,
            activity_type=activity_type,
            xp_earned=xp_earned,
            metadata=json.dumps(metadata) if metadata else None
        )
        db.add(activity_log)

        db.commit()
        db.refresh(progress)

        # Check for new achievements
        new_achievements = await EngagementService._check_achievements(db, user_id, progress)

        return {
            "xp_earned": xp_earned,
            "total_xp": progress.xp,
            "level": progress.level,
            "level_up": level_up,
            "new_achievements": new_achievements,
            "streak": progress.current_streak,
        }

    @staticmethod
    def _calculate_level(xp: int) -> int:
        """Calculate level based on XP"""
        for level, threshold in enumerate(LEVEL_THRESHOLDS, start=1):
            if xp < threshold:
                return level - 1
        return len(LEVEL_THRESHOLDS)

    @staticmethod
    async def _update_streak(progress: UserProgress):
        """Update user's daily streak"""
        today = datetime.utcnow().date()

        if progress.last_active_date:
            last_active = progress.last_active_date.date()
            days_diff = (today - last_active).days

            if days_diff == 0:
                # Same day, no change
                pass
            elif days_diff == 1:
                # Consecutive day, increment streak
                progress.current_streak += 1
                if progress.current_streak > progress.longest_streak:
                    progress.longest_streak = progress.current_streak
            else:
                # Streak broken
                progress.current_streak = 1
        else:
            # First activity
            progress.current_streak = 1
            progress.longest_streak = 1

        progress.last_active_date = datetime.utcnow()

    @staticmethod
    async def _check_achievements(
        db: Session,
        user_id: str,
        progress: UserProgress
    ) -> List[Dict[str, Any]]:
        """Check and award new achievements"""
        new_achievements = []

        # Get all achievements
        all_achievements = db.query(Achievement).all()

        # Get user's unlocked achievements
        unlocked_ids = [
            ua.achievement_id
            for ua in db.query(UserAchievement).filter(
                UserAchievement.user_id == user_id
            ).all()
        ]

        for achievement in all_achievements:
            if achievement.id in unlocked_ids:
                continue

            # Check if user qualifies for this achievement
            qualified = False

            if achievement.achievement_key == "first_pattern":
                qualified = progress.patterns_detected >= 1
            elif achievement.achievement_key == "10_stocks":
                qualified = progress.stocks_analyzed >= 10
            elif achievement.achievement_key == "first_profitable":
                qualified = progress.profitable_ideas >= 1
            elif achievement.achievement_key == "watchlist_master":
                qualified = progress.watchlist_items >= 50
            elif achievement.achievement_key == "pattern_expert":
                qualified = progress.total_scans >= 100
            elif achievement.achievement_key == "week_warrior":
                qualified = progress.current_streak >= 7
            elif achievement.achievement_key == "month_master":
                qualified = progress.current_streak >= 30

            if qualified:
                # Award achievement
                user_achievement = UserAchievement(
                    user_id=user_id,
                    achievement_id=achievement.id
                )
                db.add(user_achievement)

                # Award XP bonus
                progress.xp += achievement.xp_reward

                new_achievements.append({
                    "id": achievement.id,
                    "name": achievement.name,
                    "description": achievement.description,
                    "icon": achievement.icon,
                    "xp_reward": achievement.xp_reward,
                })

        if new_achievements:
            db.commit()

        return new_achievements

    @staticmethod
    async def get_user_stats(db: Session, user_id: str) -> Dict[str, Any]:
        """Get comprehensive user stats"""
        progress = await EngagementService.get_or_create_user_progress(db, user_id)

        # Get unlocked achievements
        unlocked = db.query(Achievement, UserAchievement).join(
            UserAchievement, Achievement.id == UserAchievement.achievement_id
        ).filter(UserAchievement.user_id == user_id).all()

        achievements_list = [
            {
                "id": ach.id,
                "name": ach.name,
                "description": ach.description,
                "icon": ach.icon,
                "unlocked_at": ua.unlocked_at.isoformat(),
            }
            for ach, ua in unlocked
        ]

        # Calculate progress to next level
        current_threshold = LEVEL_THRESHOLDS[min(progress.level - 1, len(LEVEL_THRESHOLDS) - 1)]
        next_threshold = LEVEL_THRESHOLDS[min(progress.level, len(LEVEL_THRESHOLDS) - 1)]
        level_progress = 0
        if next_threshold > current_threshold:
            level_progress = int(((progress.xp - current_threshold) / (next_threshold - current_threshold)) * 100)

        return {
            "user_id": user_id,
            "level": progress.level,
            "xp": progress.xp,
            "level_progress": level_progress,
            "next_level_xp": next_threshold,
            "stats": {
                "total_scans": progress.total_scans,
                "patterns_detected": progress.patterns_detected,
                "stocks_analyzed": progress.stocks_analyzed,
                "watchlist_items": progress.watchlist_items,
                "profitable_ideas": progress.profitable_ideas,
            },
            "streak": {
                "current": progress.current_streak,
                "longest": progress.longest_streak,
                "last_active": progress.last_active_date.isoformat() if progress.last_active_date else None,
            },
            "achievements": achievements_list,
            "total_achievements": len(achievements_list),
        }

    @staticmethod
    async def get_leaderboard(db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top users by XP"""
        top_users = db.query(UserProgress).order_by(
            UserProgress.xp.desc()
        ).limit(limit).all()

        return [
            {
                "rank": idx + 1,
                "user_id": user.user_id,
                "level": user.level,
                "xp": user.xp,
                "streak": user.current_streak,
            }
            for idx, user in enumerate(top_users)
        ]

    @staticmethod
    async def update_community_stats(db: Session):
        """Update daily community statistics"""
        today = datetime.utcnow().date()

        # Check if stats for today already exist
        existing = db.query(CommunityStats).filter(
            func.date(CommunityStats.stat_date) == today
        ).first()

        if existing:
            return existing

        # Calculate today's stats
        # Total active users today
        active_users = db.query(func.count(func.distinct(ActivityLog.user_id))).filter(
            func.date(ActivityLog.created_at) == today
        ).scalar() or 0

        # Total scans today
        total_scans = db.query(func.count(ActivityLog.id)).filter(
            and_(
                func.date(ActivityLog.created_at) == today,
                ActivityLog.activity_type == "scan"
            )
        ).scalar() or 0

        # Total patterns detected today
        total_patterns = db.query(func.count(ActivityLog.id)).filter(
            and_(
                func.date(ActivityLog.created_at) == today,
                ActivityLog.activity_type == "pattern_detect"
            )
        ).scalar() or 0

        stats = CommunityStats(
            stat_date=datetime.utcnow(),
            total_scans=total_scans,
            total_patterns=total_patterns,
            active_users=active_users,
            top_pattern_type="VCP",  # This would come from actual data
            top_ticker="NVDA",  # This would come from actual data
            patterns_by_type=json.dumps({})  # Placeholder
        )

        db.add(stats)
        db.commit()
        db.refresh(stats)

        return stats

    @staticmethod
    async def get_community_stats(db: Session) -> Dict[str, Any]:
        """Get latest community statistics"""
        latest = db.query(CommunityStats).order_by(
            CommunityStats.stat_date.desc()
        ).first()

        if not latest:
            # Create initial stats
            latest = await EngagementService.update_community_stats(db)

        return {
            "patterns_detected_today": latest.total_patterns,
            "top_pattern_week": latest.top_pattern_type,
            "most_watched_ticker": latest.top_ticker,
            "active_users_today": latest.active_users,
            "total_scans_today": latest.total_scans,
        }
