"""
GraphQL Query Resolvers
All read operations for the Legend AI API
"""

import strawberry
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
import json

from .types import (
    Ticker, PatternScan, WatchlistItem, ScanLog, UniverseScan,
    AlertLog, PatternResult, ScanResult, MarketInternals,
    PatternScanConnection, PatternScanEdge, PageInfo
)
from .context import GraphQLContext
from app.models import (
    Ticker as TickerModel,
    PatternScan as PatternScanModel,
    Watchlist as WatchlistModel,
    ScanLog as ScanLogModel,
    UniverseScan as UniverseScanModel,
    AlertLog as AlertLogModel
)
from app.core.pattern_detector import detect_pattern
from app.services.market_data import MarketDataService
from app.services.cache import get_redis_cache


def convert_ticker(model: TickerModel) -> Ticker:
    """Convert SQLAlchemy model to GraphQL type"""
    return Ticker(
        id=model.id,
        symbol=model.symbol,
        name=model.name,
        sector=model.sector,
        industry=model.industry,
        exchange=model.exchange,
        created_at=model.created_at,
        updated_at=model.updated_at
    )


def convert_pattern_scan(model: PatternScanModel, ticker: Optional[Ticker] = None) -> PatternScan:
    """Convert SQLAlchemy model to GraphQL type"""
    return PatternScan(
        id=model.id,
        ticker_id=model.ticker_id,
        pattern_type=model.pattern_type,
        score=model.score,
        entry_price=model.entry_price,
        stop_price=model.stop_price,
        target_price=model.target_price,
        risk_reward_ratio=model.risk_reward_ratio,
        criteria_met=model.criteria_met,
        analysis=model.analysis,
        current_price=model.current_price,
        volume_dry_up=model.volume_dry_up,
        consolidation_days=model.consolidation_days,
        chart_url=model.chart_url,
        rs_rating=model.rs_rating,
        scanned_at=model.scanned_at,
        ticker=ticker
    )


def convert_watchlist(model: WatchlistModel, ticker: Optional[Ticker] = None) -> WatchlistItem:
    """Convert SQLAlchemy model to GraphQL type"""
    return WatchlistItem(
        id=model.id,
        user_id=model.user_id,
        ticker_id=model.ticker_id,
        status=model.status,
        target_entry=model.target_entry,
        target_stop=model.target_stop,
        target_price=model.target_price,
        reason=model.reason,
        notes=model.notes,
        alerts_enabled=model.alerts_enabled,
        alert_threshold=model.alert_threshold,
        added_at=model.added_at,
        triggered_at=model.triggered_at,
        updated_at=model.updated_at,
        ticker=ticker
    )


def convert_alert_log(model: AlertLogModel, ticker: Optional[Ticker] = None) -> AlertLog:
    """Convert SQLAlchemy model to GraphQL type"""
    return AlertLog(
        id=model.id,
        ticker_id=model.ticker_id,
        alert_type=model.alert_type,
        trigger_price=model.trigger_price,
        trigger_value=model.trigger_value,
        alert_sent_at=model.alert_sent_at,
        sent_via=model.sent_via,
        user_id=model.user_id,
        status=model.status,
        ticker=ticker
    )


@strawberry.type
class Query:
    """Root Query type"""

    @strawberry.field(description="Get a ticker by symbol")
    async def ticker(
        self,
        symbol: str,
        info: strawberry.Info[GraphQLContext]
    ) -> Optional[Ticker]:
        """Fetch ticker by symbol with DataLoader"""
        context = info.context
        ticker_model = await context.get_ticker_by_symbol_loader().load(symbol.upper())
        return convert_ticker(ticker_model) if ticker_model else None

    @strawberry.field(description="Search tickers by query")
    async def search_tickers(
        self,
        query: str,
        limit: int = 10,
        info: strawberry.Info[GraphQLContext]
    ) -> List[Ticker]:
        """Search tickers by symbol or name"""
        context = info.context
        search_term = f"%{query.upper()}%"

        result = await context.db.execute(
            select(TickerModel)
            .where(
                (TickerModel.symbol.ilike(search_term)) |
                (TickerModel.name.ilike(search_term))
            )
            .limit(limit)
        )
        tickers = result.scalars().all()
        return [convert_ticker(t) for t in tickers]

    @strawberry.field(description="Get all tickers in a sector")
    async def tickers_by_sector(
        self,
        sector: str,
        limit: int = 50,
        info: strawberry.Info[GraphQLContext]
    ) -> List[Ticker]:
        """Get tickers filtered by sector"""
        context = info.context
        result = await context.db.execute(
            select(TickerModel)
            .where(TickerModel.sector == sector)
            .limit(limit)
        )
        tickers = result.scalars().all()
        return [convert_ticker(t) for t in tickers]

    @strawberry.field(description="Detect patterns for a ticker in real-time")
    async def detect_pattern(
        self,
        ticker: str,
        interval: str = "1d",
        info: strawberry.Info[GraphQLContext]
    ) -> Optional[PatternResult]:
        """Real-time pattern detection"""
        context = info.context

        # Check cache first
        cache_key = f"pattern:{ticker}:{interval}"
        cached = await context.cache.get(cache_key)

        if cached:
            data = json.loads(cached)
            return PatternResult(**data)

        # Detect pattern
        try:
            result = await detect_pattern(ticker, interval)
            if result:
                pattern_data = PatternResult(
                    ticker=result.ticker,
                    pattern=result.pattern,
                    score=result.score,
                    entry=result.entry,
                    stop=result.stop,
                    target=result.target,
                    risk_reward=result.risk_reward,
                    criteria_met=result.criteria_met,
                    analysis=result.analysis,
                    timestamp=result.timestamp,
                    rs_rating=result.rs_rating,
                    current_price=result.current_price,
                    support_start=result.support_start,
                    support_end=result.support_end,
                    volume_increasing=result.volume_increasing,
                    consolidation_days=result.consolidation_days,
                    chart_url=result.chart_url
                )

                # Cache result for 5 minutes
                await context.cache.setex(
                    cache_key,
                    300,
                    json.dumps({k: str(v) if isinstance(v, datetime) else v
                               for k, v in pattern_data.__dict__.items()})
                )

                return pattern_data
        except Exception as e:
            print(f"Pattern detection error: {e}")
            return None

    @strawberry.field(description="Get pattern scans for a ticker")
    async def pattern_scans(
        self,
        ticker: str,
        limit: int = 10,
        info: strawberry.Info[GraphQLContext]
    ) -> List[PatternScan]:
        """Get historical pattern scans"""
        context = info.context

        # Get ticker first
        ticker_model = await context.get_ticker_by_symbol_loader().load(ticker.upper())
        if not ticker_model:
            return []

        # Use DataLoader to get scans
        scan_models = await context.get_pattern_scans_loader().load(ticker_model.id)
        ticker_obj = convert_ticker(ticker_model)

        return [convert_pattern_scan(scan, ticker_obj) for scan in scan_models[:limit]]

    @strawberry.field(description="Get top pattern setups across all tickers")
    async def top_setups(
        self,
        min_score: float = 7.0,
        limit: int = 20,
        pattern_type: Optional[str] = None,
        info: strawberry.Info[GraphQLContext]
    ) -> List[PatternScan]:
        """Get top pattern setups"""
        context = info.context

        # Build query
        query = select(PatternScanModel).where(PatternScanModel.score >= min_score)
        if pattern_type:
            query = query.where(PatternScanModel.pattern_type == pattern_type)

        query = query.order_by(desc(PatternScanModel.score)).limit(limit)

        result = await context.db.execute(query)
        scans = result.scalars().all()

        # Load tickers with DataLoader
        ticker_ids = [scan.ticker_id for scan in scans]
        ticker_loader = context.get_ticker_loader()
        tickers = await ticker_loader.load_many(ticker_ids)

        # Convert to GraphQL types
        return [
            convert_pattern_scan(scan, convert_ticker(ticker) if ticker else None)
            for scan, ticker in zip(scans, tickers)
        ]

    @strawberry.field(description="Get watchlist for a user")
    async def watchlist(
        self,
        user_id: str = "default",
        status: Optional[str] = None,
        info: strawberry.Info[GraphQLContext]
    ) -> List[WatchlistItem]:
        """Get user watchlist"""
        context = info.context

        query = select(WatchlistModel).where(WatchlistModel.user_id == user_id)
        if status:
            query = query.where(WatchlistModel.status == status)

        query = query.order_by(desc(WatchlistModel.added_at))

        result = await context.db.execute(query)
        items = result.scalars().all()

        # Load tickers with DataLoader
        ticker_ids = [item.ticker_id for item in items]
        ticker_loader = context.get_ticker_loader()
        tickers = await ticker_loader.load_many(ticker_ids)

        return [
            convert_watchlist(item, convert_ticker(ticker) if ticker else None)
            for item, ticker in zip(items, tickers)
        ]

    @strawberry.field(description="Get scan history")
    async def scan_history(
        self,
        limit: int = 10,
        info: strawberry.Info[GraphQLContext]
    ) -> List[UniverseScan]:
        """Get universe scan history"""
        context = info.context

        result = await context.db.execute(
            select(UniverseScanModel)
            .order_by(desc(UniverseScanModel.scan_date))
            .limit(limit)
        )
        scans = result.scalars().all()

        return [
            UniverseScan(
                id=scan.id,
                scan_date=scan.scan_date,
                universe=scan.universe,
                total_scanned=scan.total_scanned,
                patterns_found=scan.patterns_found,
                top_score=scan.top_score,
                duration_seconds=scan.duration_seconds,
                status=scan.status,
                error_message=scan.error_message
            )
            for scan in scans
        ]

    @strawberry.field(description="Get recent alerts")
    async def recent_alerts(
        self,
        ticker: Optional[str] = None,
        user_id: Optional[str] = None,
        limit: int = 20,
        info: strawberry.Info[GraphQLContext]
    ) -> List[AlertLog]:
        """Get recent alert history"""
        context = info.context

        query = select(AlertLogModel)

        if ticker:
            # Get ticker ID first
            ticker_model = await context.get_ticker_by_symbol_loader().load(ticker.upper())
            if ticker_model:
                query = query.where(AlertLogModel.ticker_id == ticker_model.id)

        if user_id:
            query = query.where(AlertLogModel.user_id == user_id)

        query = query.order_by(desc(AlertLogModel.alert_sent_at)).limit(limit)

        result = await context.db.execute(query)
        alerts = result.scalars().all()

        # Load tickers with DataLoader
        ticker_ids = [alert.ticker_id for alert in alerts]
        ticker_loader = context.get_ticker_loader()
        tickers = await ticker_loader.load_many(ticker_ids)

        return [
            convert_alert_log(alert, convert_ticker(ticker) if ticker else None)
            for alert, ticker in zip(alerts, tickers)
        ]

    @strawberry.field(description="Get market internals/breadth")
    async def market_internals(
        self,
        info: strawberry.Info[GraphQLContext]
    ) -> Optional[MarketInternals]:
        """Get current market internals"""
        context = info.context

        # Check cache first
        cache_key = "market:internals"
        cached = await context.cache.get(cache_key)

        if cached:
            data = json.loads(cached)
            return MarketInternals(**data)

        # This would integrate with your market data service
        # For now, return a placeholder
        return None

    @strawberry.field(description="Search patterns across universe")
    async def search_patterns(
        self,
        pattern_type: Optional[str] = None,
        min_score: float = 7.0,
        sector: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        info: strawberry.Info[GraphQLContext]
    ) -> List[PatternScan]:
        """Advanced pattern search with filters"""
        context = info.context

        query = select(PatternScanModel).where(PatternScanModel.score >= min_score)

        if pattern_type:
            query = query.where(PatternScanModel.pattern_type == pattern_type)

        if sector:
            # Join with ticker to filter by sector
            query = query.join(TickerModel).where(TickerModel.sector == sector)

        query = (query
                .order_by(desc(PatternScanModel.score))
                .offset(offset)
                .limit(limit))

        result = await context.db.execute(query)
        scans = result.scalars().all()

        # Load tickers
        ticker_ids = [scan.ticker_id for scan in scans]
        ticker_loader = context.get_ticker_loader()
        tickers = await ticker_loader.load_many(ticker_ids)

        return [
            convert_pattern_scan(scan, convert_ticker(ticker) if ticker else None)
            for scan, ticker in zip(scans, tickers)
        ]

    @strawberry.field(description="Get statistics summary")
    async def stats(
        self,
        info: strawberry.Info[GraphQLContext]
    ) -> str:
        """Get platform statistics as JSON"""
        context = info.context

        # Count queries
        total_tickers = await context.db.scalar(select(func.count(TickerModel.id)))
        total_scans = await context.db.scalar(select(func.count(PatternScanModel.id)))
        total_watchlist = await context.db.scalar(select(func.count(WatchlistModel.id)))

        # Recent scans (last 24h)
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_scans = await context.db.scalar(
            select(func.count(PatternScanModel.id))
            .where(PatternScanModel.scanned_at >= yesterday)
        )

        return json.dumps({
            "total_tickers": total_tickers,
            "total_scans": total_scans,
            "total_watchlist_items": total_watchlist,
            "scans_last_24h": recent_scans,
            "timestamp": datetime.utcnow().isoformat()
        })
