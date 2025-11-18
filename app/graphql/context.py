"""
GraphQL Context
Provides database session, dataloaders, cache, and auth info
"""

from typing import Optional
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from .dataloaders import create_dataloaders


@dataclass
class GraphQLContext:
    """GraphQL request context"""
    db: AsyncSession
    cache: Redis
    dataloaders: dict
    user_id: Optional[str] = "default"
    request: Optional[any] = None

    @classmethod
    def create(
        cls,
        db: AsyncSession,
        cache: Redis,
        user_id: str = "default",
        request = None
    ) -> "GraphQLContext":
        """Create a new context with dataloaders"""
        dataloaders = create_dataloaders(db, user_id)
        return cls(
            db=db,
            cache=cache,
            dataloaders=dataloaders,
            user_id=user_id,
            request=request
        )

    def get_ticker_loader(self):
        """Get ticker dataloader"""
        return self.dataloaders["ticker_loader"]

    def get_ticker_by_symbol_loader(self):
        """Get ticker by symbol dataloader"""
        return self.dataloaders["ticker_by_symbol_loader"]

    def get_pattern_scans_loader(self):
        """Get pattern scans dataloader"""
        return self.dataloaders["pattern_scans_by_ticker_loader"]

    def get_watchlist_loader(self):
        """Get watchlist dataloader"""
        return self.dataloaders["watchlist_by_ticker_loader"]

    def get_alerts_loader(self):
        """Get alerts dataloader"""
        return self.dataloaders["alerts_by_ticker_loader"]
