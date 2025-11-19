"""
Authentication Service
JWT-based authentication for multi-user support
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models import User
from app.services.database import DatabaseService

settings = get_settings()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """
    Handles user authentication and JWT token management
    """

    def __init__(self):
        self.db_service = DatabaseService()
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes

    def hash_password(self, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against hash"""
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create JWT access token

        Args:
            data: Data to encode in token
            expires_delta: Token expiration time

        Returns:
            JWT token string
        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

        return encoded_jwt

    def decode_access_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Decode and validate JWT token

        Args:
            token: JWT token string

        Returns:
            Decoded token data or None if invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate user with username and password

        Args:
            username: Username or email
            password: Plain text password

        Returns:
            User object if authenticated, None otherwise
        """
        async with self.db_service.get_session() as session:
            # Find user by username or email
            result = await session.execute(
                select(User).where(
                    (User.username == username) | (User.email == username)
                )
            )

            user = result.scalar_one_or_none()

            if not user:
                return None

            if not self.verify_password(password, user.hashed_password):
                return None

            if not user.is_active:
                return None

            # Update last login
            user.last_login_at = datetime.utcnow()
            await session.commit()

            return user

    async def get_current_user(self, token: str) -> Optional[User]:
        """
        Get user from JWT token

        Args:
            token: JWT token string

        Returns:
            User object or None
        """
        payload = self.decode_access_token(token)

        if not payload:
            return None

        user_id = payload.get("sub")

        if not user_id:
            return None

        async with self.db_service.get_session() as session:
            result = await session.execute(
                select(User).where(User.id == int(user_id))
            )

            user = result.scalar_one_or_none()

            if not user or not user.is_active:
                return None

            return user

    async def create_user(
        self,
        username: str,
        email: str,
        password: str,
        full_name: Optional[str] = None,
        telegram_user_id: Optional[str] = None
    ) -> User:
        """
        Create a new user

        Args:
            username: Unique username
            email: User email
            password: Plain text password
            full_name: Full name (optional)
            telegram_user_id: Telegram user ID (optional)

        Returns:
            Created User object

        Raises:
            ValueError: If username or email already exists
        """
        async with self.db_service.get_session() as session:
            # Check if username exists
            result = await session.execute(
                select(User).where(User.username == username)
            )
            if result.scalar_one_or_none():
                raise ValueError(f"Username {username} already exists")

            # Check if email exists
            result = await session.execute(
                select(User).where(User.email == email)
            )
            if result.scalar_one_or_none():
                raise ValueError(f"Email {email} already exists")

            # Create user
            user = User(
                username=username,
                email=email,
                hashed_password=self.hash_password(password),
                full_name=full_name,
                telegram_user_id=telegram_user_id,
                is_active=True,
                is_admin=False
            )

            session.add(user)
            await session.commit()
            await session.refresh(user)

            return user

    async def update_api_usage(self, user_id: int, endpoint: str):
        """
        Track API usage for a user

        Args:
            user_id: User ID
            endpoint: API endpoint called
        """
        async with self.db_service.get_session() as session:
            result = await session.execute(
                select(User).where(User.id == user_id)
            )

            user = result.scalar_one_or_none()

            if user:
                user.api_calls_count += 1
                user.last_api_call_at = datetime.utcnow()
                await session.commit()

    async def check_rate_limit(self, user_id: int) -> bool:
        """
        Check if user is within rate limit

        Args:
            user_id: User ID

        Returns:
            True if within limit, False if exceeded
        """
        async with self.db_service.get_session() as session:
            result = await session.execute(
                select(User).where(User.id == user_id)
            )

            user = result.scalar_one_or_none()

            if not user:
                return False

            # Check daily limit
            if user.last_api_call_at:
                if user.last_api_call_at.date() != datetime.utcnow().date():
                    # Reset daily counter
                    user.api_calls_count = 0
                    await session.commit()

            # Check against quota
            return user.api_calls_count < user.api_quota_per_day

    async def get_user_by_telegram_id(self, telegram_user_id: str) -> Optional[User]:
        """Get user by Telegram user ID"""
        async with self.db_service.get_session() as session:
            result = await session.execute(
                select(User).where(User.telegram_user_id == telegram_user_id)
            )

            return result.scalar_one_or_none()
