"""
DataLoaders for efficient batching and caching
Prevents N+1 query problems in GraphQL
"""

from typing import List, Optional
from aiodataloader import DataLoader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Ticker, PatternScan, Watchlist, AlertLog


class TickerLoader(DataLoader):
    """Batch load tickers by ID"""

    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def batch_load_fn(self, ticker_ids: List[int]) -> List[Optional[Ticker]]:
        """Load multiple tickers in a single query"""
        result = await self.session.execute(
            select(Ticker).where(Ticker.id.in_(ticker_ids))
        )
        tickers = result.scalars().all()

        # Create a map for O(1) lookup
        ticker_map = {ticker.id: ticker for ticker in tickers}

        # Return in the same order as requested IDs
        return [ticker_map.get(tid) for tid in ticker_ids]


class TickerBySymbolLoader(DataLoader):
    """Batch load tickers by symbol"""

    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def batch_load_fn(self, symbols: List[str]) -> List[Optional[Ticker]]:
        """Load multiple tickers by symbol in a single query"""
        result = await self.session.execute(
            select(Ticker).where(Ticker.symbol.in_(symbols))
        )
        tickers = result.scalars().all()

        # Create a map for O(1) lookup
        ticker_map = {ticker.symbol.upper(): ticker for ticker in tickers}

        # Return in the same order as requested symbols
        return [ticker_map.get(symbol.upper()) for symbol in symbols]


class PatternScansByTickerLoader(DataLoader):
    """Batch load pattern scans by ticker ID"""

    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def batch_load_fn(self, ticker_ids: List[int]) -> List[List[PatternScan]]:
        """Load pattern scans for multiple tickers"""
        result = await self.session.execute(
            select(PatternScan)
            .where(PatternScan.ticker_id.in_(ticker_ids))
            .order_by(PatternScan.scanned_at.desc())
        )
        scans = result.scalars().all()

        # Group by ticker_id
        scan_map = {}
        for scan in scans:
            if scan.ticker_id not in scan_map:
                scan_map[scan.ticker_id] = []
            scan_map[scan.ticker_id].append(scan)

        # Return in the same order as requested IDs
        return [scan_map.get(tid, []) for tid in ticker_ids]


class WatchlistByTickerLoader(DataLoader):
    """Batch load watchlist items by ticker ID"""

    def __init__(self, session: AsyncSession, user_id: str = "default"):
        super().__init__()
        self.session = session
        self.user_id = user_id

    async def batch_load_fn(self, ticker_ids: List[int]) -> List[Optional[Watchlist]]:
        """Load watchlist items for multiple tickers"""
        result = await self.session.execute(
            select(Watchlist)
            .where(
                Watchlist.ticker_id.in_(ticker_ids),
                Watchlist.user_id == self.user_id
            )
        )
        items = result.scalars().all()

        # Create a map for O(1) lookup
        item_map = {item.ticker_id: item for item in items}

        # Return in the same order as requested IDs
        return [item_map.get(tid) for tid in ticker_ids]


class AlertsByTickerLoader(DataLoader):
    """Batch load alerts by ticker ID"""

    def __init__(self, session: AsyncSession):
        super().__init__()
        self.session = session

    async def batch_load_fn(self, ticker_ids: List[int]) -> List[List[AlertLog]]:
        """Load alerts for multiple tickers"""
        result = await self.session.execute(
            select(AlertLog)
            .where(AlertLog.ticker_id.in_(ticker_ids))
            .order_by(AlertLog.alert_sent_at.desc())
        )
        alerts = result.scalars().all()

        # Group by ticker_id
        alert_map = {}
        for alert in alerts:
            if alert.ticker_id not in alert_map:
                alert_map[alert.ticker_id] = []
            alert_map[alert.ticker_id].append(alert)

        # Return in the same order as requested IDs
        return [alert_map.get(tid, []) for tid in ticker_ids]


def create_dataloaders(session: AsyncSession, user_id: str = "default") -> dict:
    """Create all dataloaders for a request"""
    return {
        "ticker_loader": TickerLoader(session),
        "ticker_by_symbol_loader": TickerBySymbolLoader(session),
        "pattern_scans_by_ticker_loader": PatternScansByTickerLoader(session),
        "watchlist_by_ticker_loader": WatchlistByTickerLoader(session, user_id),
        "alerts_by_ticker_loader": AlertsByTickerLoader(session),
    }
