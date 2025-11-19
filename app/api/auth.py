"""
Authentication API Endpoints
User registration, login, and token management
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import timedelta

from app.services.auth import AuthService
from app.models import User


router = APIRouter()
auth_service = AuthService()
security = HTTPBearer()


class UserRegisterRequest(BaseModel):
    """User registration request"""
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    telegram_user_id: Optional[str] = None


class UserLoginRequest(BaseModel):
    """User login request"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """
    Dependency to get current authenticated user from JWT token
    """
    token = credentials.credentials
    user = await auth_service.get_current_user(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to get current active user
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


async def get_current_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Dependency to get current admin user
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return current_user


@router.post("/register", response_model=TokenResponse)
async def register(request: UserRegisterRequest):
    """
    Register a new user

    Creates account and returns JWT token
    """
    try:
        # Create user
        user = await auth_service.create_user(
            username=request.username,
            email=request.email,
            password=request.password,
            full_name=request.full_name,
            telegram_user_id=request.telegram_user_id
        )

        # Create access token
        access_token = auth_service.create_access_token(
            data={"sub": str(user.id), "username": user.username}
        )

        return TokenResponse(
            access_token=access_token,
            expires_in=auth_service.access_token_expire_minutes * 60,
            user={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "is_admin": user.is_admin
            }
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(request: UserLoginRequest):
    """
    Login with username/email and password

    Returns JWT token for authentication
    """
    user = await auth_service.authenticate_user(request.username, request.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = auth_service.create_access_token(
        data={"sub": str(user.id), "username": user.username}
    )

    return TokenResponse(
        access_token=access_token,
        expires_in=auth_service.access_token_expire_minutes * 60,
        user={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            is_admin": user.is_admin,
            "api_quota": user.api_quota_per_day,
            "api_calls_today": user.api_calls_count
        }
    )


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current user profile

    Requires authentication
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "telegram_user_id": current_user.telegram_user_id,
        "is_admin": current_user.is_admin,
        "api_quota_per_day": current_user.api_quota_per_day,
        "api_calls_count": current_user.api_calls_count,
        "created_at": current_user.created_at.isoformat(),
        "last_login_at": current_user.last_login_at.isoformat() if current_user.last_login_at else None
    }


@router.get("/usage")
async def get_usage(current_user: User = Depends(get_current_active_user)):
    """
    Get API usage statistics for current user

    Shows quota and remaining calls
    """
    remaining = current_user.api_quota_per_day - current_user.api_calls_count

    return {
        "user_id": current_user.id,
        "username": current_user.username,
        "api_quota_per_day": current_user.api_quota_per_day,
        "api_calls_today": current_user.api_calls_count,
        "remaining_calls": max(0, remaining),
        "percentage_used": (current_user.api_calls_count / current_user.api_quota_per_day * 100) if current_user.api_quota_per_day > 0 else 0,
        "last_api_call": current_user.last_api_call_at.isoformat() if current_user.last_api_call_at else None
    }


@router.post("/refresh")
async def refresh_token(current_user: User = Depends(get_current_active_user)):
    """
    Refresh JWT token

    Returns a new token with extended expiration
    """
    access_token = auth_service.create_access_token(
        data={"sub": str(current_user.id), "username": current_user.username}
    )

    return TokenResponse(
        access_token=access_token,
        expires_in=auth_service.access_token_expire_minutes * 60,
        user={
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email
        }
    )
