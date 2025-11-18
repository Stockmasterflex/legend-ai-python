"""
Async database dependency for FastAPI
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator
import logging

from app.config import get_settings
from app.models import Base

logger = logging.getLogger(__name__)

# Global async engine
_async_engine = None
_async_session_maker = None


def get_async_engine():
    """Get or create async database engine"""
    global _async_engine
    if _async_engine is None:
        settings = get_settings()
        database_url = settings.database_url

        # Convert sync URL to async URL
        if database_url.startswith("sqlite"):
            async_url = database_url.replace("sqlite:///", "sqlite+aiosqlite:///")
        elif database_url.startswith("postgresql://"):
            async_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
        else:
            async_url = database_url

        _async_engine = create_async_engine(
            async_url,
            echo=False,
            poolclass=NullPool,  # Simple pooling for async
        )

    return _async_engine


def get_async_session_maker():
    """Get or create async session maker"""
    global _async_session_maker
    if _async_session_maker is None:
        engine = get_async_engine()
        _async_session_maker = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _async_session_maker


async def init_db():
    """Initialize database tables"""
    engine = get_async_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Async database tables initialized")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency to get async database session

    Usage in routers:
        @router.get("/endpoint")
        async def endpoint(db: AsyncSession = Depends(get_db)):
            ...
    """
    session_maker = get_async_session_maker()
    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
