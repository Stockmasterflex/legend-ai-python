"""
GraphQL API Router
FastAPI integration for GraphQL endpoint
"""

from fastapi import APIRouter, Request, Depends
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from redis.asyncio import Redis
from typing import Optional

from app.graphql.schema import schema
from app.graphql.context import GraphQLContext
from app.config import get_settings
from app.services.cache import get_cache_service

settings = get_settings()

# Create async database engine for GraphQL
# Convert synchronous database URL to async
db_url = settings.database_url
if db_url.startswith("postgresql://"):
    async_db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif db_url.startswith("sqlite://"):
    async_db_url = db_url.replace("sqlite://", "sqlite+aiosqlite://", 1)
else:
    async_db_url = db_url

async_engine = create_async_engine(
    async_db_url,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db_session() -> AsyncSession:
    """Get async database session"""
    async with AsyncSessionLocal() as session:
        yield session


async def get_context(
    request: Request,
    db: AsyncSession = Depends(get_db_session),
) -> GraphQLContext:
    """
    Create GraphQL context for each request
    Includes database session, Redis cache, and dataloaders
    """
    # Get Redis cache service
    cache_service = get_cache_service()
    cache = await cache_service._get_redis()

    # Extract user ID from request (if auth is implemented)
    # For now, use default user
    user_id = "default"

    # Check for Authorization header (future enhancement)
    auth_header = request.headers.get("Authorization")
    if auth_header:
        # TODO: Validate JWT token and extract user_id
        pass

    # Create context with all dependencies
    context = GraphQLContext.create(
        db=db,
        cache=cache,
        user_id=user_id,
        request=request
    )

    return context


# Create GraphQL router with Strawberry
graphql_router = GraphQLRouter(
    schema,
    context_getter=get_context,
    graphiql=True,  # Enable GraphiQL playground
)

# Create FastAPI router
router = APIRouter(prefix="/graphql", tags=["graphql"])

# Mount GraphQL routes
router.include_router(graphql_router, prefix="")
