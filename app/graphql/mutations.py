"""
GraphQL Mutation Resolvers
All write operations for the Legend AI API
"""

import strawberry
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
import json

from .types import (
    WatchlistItem, PatternResult, PositionSize,
    WatchlistAddInput, WatchlistUpdateInput, PositionSizeInput,
    PatternDetectInput, UniverseScanInput, ChartGenerateInput,
    Ticker
)
from .context import GraphQLContext
from .queries import convert_ticker, convert_watchlist
from app.models import (
    Ticker as TickerModel,
    Watchlist as WatchlistModel,
    PatternScan as PatternScanModel
)
from app.core.pattern_detector import detect_pattern
from app.services.charting import generate_chart


@strawberry.type
class Mutation:
    """Root Mutation type"""

    @strawberry.mutation(description="Add a ticker to watchlist")
    async def add_to_watchlist(
        self,
        input: WatchlistAddInput,
        info: strawberry.Info[GraphQLContext]
    ) -> Optional[WatchlistItem]:
        """Add ticker to user's watchlist"""
        context = info.context

        # Get or create ticker
        ticker_model = await context.get_ticker_by_symbol_loader().load(input.ticker.upper())

        if not ticker_model:
            # Create new ticker entry
            ticker_model = TickerModel(symbol=input.ticker.upper())
            context.db.add(ticker_model)
            await context.db.flush()

        # Check if already in watchlist
        existing = await context.db.execute(
            select(WatchlistModel).where(
                WatchlistModel.ticker_id == ticker_model.id,
                WatchlistModel.user_id == input.user_id
            )
        )
        if existing.scalar_one_or_none():
            return None  # Already exists

        # Create watchlist item
        watchlist_item = WatchlistModel(
            user_id=input.user_id,
            ticker_id=ticker_model.id,
            reason=input.reason,
            alerts_enabled=input.alerts_enabled,
            alert_threshold=input.alert_threshold,
            status="Watching"
        )

        context.db.add(watchlist_item)
        await context.db.commit()
        await context.db.refresh(watchlist_item)

        ticker_obj = convert_ticker(ticker_model)
        return convert_watchlist(watchlist_item, ticker_obj)

    @strawberry.mutation(description="Update watchlist item")
    async def update_watchlist(
        self,
        input: WatchlistUpdateInput,
        info: strawberry.Info[GraphQLContext]
    ) -> Optional[WatchlistItem]:
        """Update watchlist item status and settings"""
        context = info.context

        # Get watchlist item
        result = await context.db.execute(
            select(WatchlistModel).where(WatchlistModel.id == input.id)
        )
        item = result.scalar_one_or_none()

        if not item:
            return None

        # Update fields
        if input.status is not None:
            item.status = input.status.value
            if input.status.value == "Triggered":
                item.triggered_at = datetime.utcnow()

        if input.target_entry is not None:
            item.target_entry = input.target_entry

        if input.target_stop is not None:
            item.target_stop = input.target_stop

        if input.target_price is not None:
            item.target_price = input.target_price

        if input.notes is not None:
            item.notes = input.notes

        if input.alerts_enabled is not None:
            item.alerts_enabled = input.alerts_enabled

        item.updated_at = datetime.utcnow()

        await context.db.commit()
        await context.db.refresh(item)

        # Load ticker
        ticker_model = await context.get_ticker_loader().load(item.ticker_id)
        ticker_obj = convert_ticker(ticker_model) if ticker_model else None

        return convert_watchlist(item, ticker_obj)

    @strawberry.mutation(description="Remove ticker from watchlist")
    async def remove_from_watchlist(
        self,
        ticker: str,
        user_id: str = "default",
        info: strawberry.Info[GraphQLContext]
    ) -> bool:
        """Remove ticker from watchlist"""
        context = info.context

        # Get ticker
        ticker_model = await context.get_ticker_by_symbol_loader().load(ticker.upper())
        if not ticker_model:
            return False

        # Delete watchlist item
        await context.db.execute(
            delete(WatchlistModel).where(
                WatchlistModel.ticker_id == ticker_model.id,
                WatchlistModel.user_id == user_id
            )
        )
        await context.db.commit()

        # Clear cache
        cache_key = f"watchlist:{user_id}"
        await context.cache.delete(cache_key)

        return True

    @strawberry.mutation(description="Run pattern detection and save results")
    async def scan_pattern(
        self,
        input: PatternDetectInput,
        info: strawberry.Info[GraphQLContext]
    ) -> Optional[PatternResult]:
        """Detect pattern and save to database"""
        context = info.context

        # Run pattern detection
        try:
            result = await detect_pattern(input.ticker, input.interval)
            if not result:
                return None

            # Get or create ticker
            ticker_model = await context.get_ticker_by_symbol_loader().load(input.ticker.upper())
            if not ticker_model:
                ticker_model = TickerModel(symbol=input.ticker.upper())
                context.db.add(ticker_model)
                await context.db.flush()

            # Save pattern scan
            pattern_scan = PatternScanModel(
                ticker_id=ticker_model.id,
                pattern_type=result.pattern,
                score=result.score,
                entry_price=result.entry,
                stop_price=result.stop,
                target_price=result.target,
                risk_reward_ratio=result.risk_reward,
                criteria_met=json.dumps(result.criteria_met),
                analysis=result.analysis,
                current_price=result.current_price,
                consolidation_days=result.consolidation_days,
                chart_url=result.chart_url,
                rs_rating=result.rs_rating,
                volume_dry_up=result.volume_increasing if result.volume_increasing else False
            )

            context.db.add(pattern_scan)
            await context.db.commit()

            # Cache result
            cache_key = f"pattern:{input.ticker}:{input.interval}"
            await context.cache.setex(
                cache_key,
                300,  # 5 minutes
                json.dumps({
                    "ticker": result.ticker,
                    "pattern": result.pattern,
                    "score": result.score,
                    "entry": result.entry,
                    "stop": result.stop,
                    "target": result.target,
                    "risk_reward": result.risk_reward,
                    "criteria_met": result.criteria_met,
                    "analysis": result.analysis,
                    "timestamp": result.timestamp.isoformat(),
                    "rs_rating": result.rs_rating,
                    "current_price": result.current_price,
                    "chart_url": result.chart_url
                })
            )

            return PatternResult(
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

        except Exception as e:
            print(f"Scan error: {e}")
            return None

    @strawberry.mutation(description="Calculate position size")
    async def calculate_position_size(
        self,
        input: PositionSizeInput,
        info: strawberry.Info[GraphQLContext]
    ) -> PositionSize:
        """Calculate position sizing for a trade"""
        risk_per_share = abs(input.entry - input.stop)
        max_risk_amount = input.account_size * (input.risk_percent / 100)
        shares = int(max_risk_amount / risk_per_share)
        dollar_amount = shares * input.entry
        position_percent = (dollar_amount / input.account_size) * 100

        return PositionSize(
            shares=shares,
            dollar_amount=dollar_amount,
            risk_per_share=risk_per_share,
            total_risk=max_risk_amount,
            position_percent=position_percent
        )

    @strawberry.mutation(description="Generate chart for a ticker")
    async def generate_chart(
        self,
        input: ChartGenerateInput,
        info: strawberry.Info[GraphQLContext]
    ) -> Optional[str]:
        """Generate and return chart URL"""
        context = info.context

        cache_key = f"chart:{input.ticker}:{input.interval}:{input.timeframe}"
        cached = await context.cache.get(cache_key)

        if cached:
            return cached.decode() if isinstance(cached, bytes) else cached

        try:
            # Generate chart
            chart_url = await generate_chart(
                ticker=input.ticker,
                interval=input.interval,
                timeframe=input.timeframe
            )

            if chart_url:
                # Cache for 1 hour
                await context.cache.setex(cache_key, 3600, chart_url)

            return chart_url

        except Exception as e:
            print(f"Chart generation error: {e}")
            return None

    @strawberry.mutation(description="Clear cache for a specific key pattern")
    async def clear_cache(
        self,
        pattern: str,
        info: strawberry.Info[GraphQLContext]
    ) -> bool:
        """Clear cache entries matching pattern"""
        context = info.context

        try:
            # Get all keys matching pattern
            keys = []
            async for key in context.cache.scan_iter(match=pattern):
                keys.append(key)

            # Delete keys
            if keys:
                await context.cache.delete(*keys)

            return True

        except Exception as e:
            print(f"Cache clear error: {e}")
            return False

    @strawberry.mutation(description="Bulk add tickers to watchlist")
    async def bulk_add_to_watchlist(
        self,
        tickers: list[str],
        user_id: str = "default",
        reason: Optional[str] = None,
        info: strawberry.Info[GraphQLContext]
    ) -> int:
        """Add multiple tickers to watchlist at once"""
        context = info.context
        added_count = 0

        for ticker_symbol in tickers:
            # Get or create ticker
            ticker_model = await context.get_ticker_by_symbol_loader().load(ticker_symbol.upper())

            if not ticker_model:
                ticker_model = TickerModel(symbol=ticker_symbol.upper())
                context.db.add(ticker_model)
                await context.db.flush()

            # Check if already exists
            existing = await context.db.execute(
                select(WatchlistModel).where(
                    WatchlistModel.ticker_id == ticker_model.id,
                    WatchlistModel.user_id == user_id
                )
            )

            if not existing.scalar_one_or_none():
                # Add to watchlist
                watchlist_item = WatchlistModel(
                    user_id=user_id,
                    ticker_id=ticker_model.id,
                    reason=reason,
                    status="Watching"
                )
                context.db.add(watchlist_item)
                added_count += 1

        await context.db.commit()

        # Clear watchlist cache
        await context.cache.delete(f"watchlist:{user_id}")

        return added_count

    @strawberry.mutation(description="Delete old pattern scans")
    async def cleanup_old_scans(
        self,
        days_old: int = 30,
        info: strawberry.Info[GraphQLContext]
    ) -> int:
        """Remove pattern scans older than X days"""
        context = info.context

        cutoff_date = datetime.utcnow() - timedelta(days=days_old)

        result = await context.db.execute(
            delete(PatternScanModel).where(
                PatternScanModel.scanned_at < cutoff_date
            )
        )

        await context.db.commit()

        return result.rowcount
