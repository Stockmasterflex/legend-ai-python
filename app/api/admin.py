"""
Admin API Endpoints
User management and system administration
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import select, func

from app.services.database import DatabaseService
from app.models import User, PatternScan, Watchlist, AlertLog, UniverseScan
from app.api.auth import get_current_admin_user


router = APIRouter()
db_service = DatabaseService()


class UserUpdateRequest(BaseModel):
    """Request to update user"""
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    api_quota_per_day: Optional[int] = None


@router.get("/users")
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user)
):
    """
    List all users

    Admin only
    """
    async with db_service.get_session() as session:
        result = await session.execute(
            select(User)
            .offset(skip)
            .limit(limit)
        )

        users = result.scalars().all()

        return {
            "success": True,
            "data": [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                    "is_active": user.is_active,
                    "is_admin": user.is_admin,
                    "api_quota": user.api_quota_per_day,
                    "api_calls": user.api_calls_count,
                    "created_at": user.created_at.isoformat(),
                    "last_login": user.last_login_at.isoformat() if user.last_login_at else None
                }
                for user in users
            ],
            "count": len(users)
        }


@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user)
):
    """
    Get specific user details

    Admin only
    """
    async with db_service.get_session() as session:
        result = await session.execute(
            select(User).where(User.id == user_id)
        )

        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Get user statistics
        watchlist_count = await session.execute(
            select(func.count(Watchlist.id)).where(Watchlist.user_id == str(user_id))
        )
        alerts_count = await session.execute(
            select(func.count(AlertLog.id)).where(AlertLog.user_id == str(user_id))
        )

        return {
            "success": True,
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "telegram_user_id": user.telegram_user_id,
                "is_active": user.is_active,
                "is_admin": user.is_admin,
                "api_quota_per_day": user.api_quota_per_day,
                "api_calls_count": user.api_calls_count,
                "last_api_call_at": user.last_api_call_at.isoformat() if user.last_api_call_at else None,
                "created_at": user.created_at.isoformat(),
                "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None,
                "statistics": {
                    "watchlist_count": watchlist_count.scalar(),
                    "alerts_count": alerts_count.scalar()
                }
            }
        }


@router.patch("/users/{user_id}")
async def update_user(
    user_id: int,
    request: UserUpdateRequest,
    current_user: User = Depends(get_current_admin_user)
):
    """
    Update user settings

    Admin only
    """
    async with db_service.get_session() as session:
        result = await session.execute(
            select(User).where(User.id == user_id)
        )

        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update fields
        if request.is_active is not None:
            user.is_active = request.is_active

        if request.is_admin is not None:
            user.is_admin = request.is_admin

        if request.api_quota_per_day is not None:
            user.api_quota_per_day = request.api_quota_per_day

        await session.commit()

        return {
            "success": True,
            "message": f"User {user_id} updated"
        }


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin_user)
):
    """
    Delete user

    Admin only
    """
    async with db_service.get_session() as session:
        result = await session.execute(
            select(User).where(User.id == user_id)
        )

        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Don't allow deleting yourself
        if user.id == current_user.id:
            raise HTTPException(status_code=400, detail="Cannot delete yourself")

        await session.delete(user)
        await session.commit()

        return {
            "success": True,
            "message": f"User {user_id} deleted"
        }


@router.get("/stats")
async def get_system_stats(current_user: User = Depends(get_current_admin_user)):
    """
    Get system-wide statistics

    Admin only
    """
    async with db_service.get_session() as session:
        # Count users
        total_users = await session.execute(select(func.count(User.id)))
        active_users = await session.execute(
            select(func.count(User.id)).where(User.is_active == True)
        )

        # Count patterns
        total_patterns = await session.execute(select(func.count(PatternScan.id)))

        # Count watchlist items
        total_watchlist = await session.execute(select(func.count(Watchlist.id)))

        # Count alerts
        total_alerts = await session.execute(select(func.count(AlertLog.id)))

        # Count scans
        total_scans = await session.execute(select(func.count(UniverseScan.id)))

        # API usage
        total_api_calls = await session.execute(select(func.sum(User.api_calls_count)))

        return {
            "success": True,
            "data": {
                "users": {
                    "total": total_users.scalar(),
                    "active": active_users.scalar()
                },
                "patterns": {
                    "total": total_patterns.scalar()
                },
                "watchlist": {
                    "total_items": total_watchlist.scalar()
                },
                "alerts": {
                    "total": total_alerts.scalar()
                },
                "scans": {
                    "total": total_scans.scalar()
                },
                "api": {
                    "total_calls_today": total_api_calls.scalar() or 0
                }
            }
        }
