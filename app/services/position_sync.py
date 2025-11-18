"""
Position Synchronization Service

Syncs positions from broker and provides real-time P&L tracking.
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel
import asyncio

from app.brokers.base import BaseBroker, Position, Account

logger = logging.getLogger(__name__)


class PositionWithPnL(BaseModel):
    """Position with detailed P&L information"""
    # Position data
    symbol: str
    quantity: float
    side: str
    avg_entry_price: float
    current_price: float

    # Value metrics
    market_value: float
    cost_basis: float

    # P&L metrics
    unrealized_pl: float
    unrealized_pl_percent: float
    unrealized_pl_per_share: float

    # Risk metrics
    risk_amount: Optional[float] = None
    risk_percent: Optional[float] = None
    r_multiple: Optional[float] = None  # Current P&L in R multiples

    # Additional data
    asset_class: str = "equity"
    exchange: Optional[str] = None
    updated_at: datetime


class PortfolioSummary(BaseModel):
    """Portfolio summary with aggregate P&L"""
    # Account metrics
    total_equity: float
    cash: float
    buying_power: float
    portfolio_value: float

    # P&L metrics
    total_unrealized_pl: float
    total_unrealized_pl_percent: float
    total_realized_pl_today: float

    # Position metrics
    total_positions: int
    long_positions: int
    short_positions: int
    total_market_value: float

    # Top positions
    top_gainers: List[Dict[str, Any]]
    top_losers: List[Dict[str, Any]]

    # Account status
    pattern_day_trader: bool
    account_blocked: bool
    trading_blocked: bool

    # Updated timestamp
    updated_at: datetime


class PositionSyncService:
    """
    Service for syncing positions from broker and tracking P&L.

    Provides real-time position monitoring and portfolio analytics.
    """

    def __init__(self, broker: BaseBroker):
        """
        Initialize position sync service.

        Args:
            broker: Connected broker instance
        """
        self.broker = broker
        self._positions_cache: Dict[str, PositionWithPnL] = {}
        self._last_sync: Optional[datetime] = None

    async def sync_positions(self, force: bool = False) -> List[PositionWithPnL]:
        """
        Sync positions from broker.

        Args:
            force: Force sync even if recently synced

        Returns:
            List[PositionWithPnL]: List of positions with P&L
        """
        if not self.broker.is_connected():
            raise RuntimeError("Broker not connected")

        # Get positions from broker
        broker_positions = await self.broker.get_positions()

        # Convert to PositionWithPnL
        positions = []
        for pos in broker_positions:
            position_with_pl = self._calculate_position_pl(pos)
            positions.append(position_with_pl)
            self._positions_cache[pos.symbol] = position_with_pl

        self._last_sync = datetime.now()
        logger.info(f"Synced {len(positions)} positions from broker")

        return positions

    async def get_position(self, symbol: str, use_cache: bool = True) -> Optional[PositionWithPnL]:
        """
        Get position for symbol.

        Args:
            symbol: Symbol
            use_cache: Use cached position if available

        Returns:
            Optional[PositionWithPnL]: Position or None
        """
        if use_cache and symbol in self._positions_cache:
            return self._positions_cache[symbol]

        if not self.broker.is_connected():
            raise RuntimeError("Broker not connected")

        broker_position = await self.broker.get_position(symbol)
        if not broker_position:
            return None

        position_with_pl = self._calculate_position_pl(broker_position)
        self._positions_cache[symbol] = position_with_pl

        return position_with_pl

    async def get_portfolio_summary(self) -> PortfolioSummary:
        """
        Get portfolio summary with aggregate metrics.

        Returns:
            PortfolioSummary: Portfolio summary
        """
        if not self.broker.is_connected():
            raise RuntimeError("Broker not connected")

        # Get account info
        account = await self.broker.get_account()

        # Sync positions
        positions = await self.sync_positions()

        # Calculate aggregate metrics
        long_positions = [p for p in positions if p.side == "buy"]
        short_positions = [p for p in positions if p.side == "sell"]
        total_market_value = sum(p.market_value for p in positions)

        # Sort by P&L
        sorted_by_pl = sorted(positions, key=lambda p: p.unrealized_pl, reverse=True)
        top_gainers = [
            {
                "symbol": p.symbol,
                "unrealized_pl": p.unrealized_pl,
                "unrealized_pl_percent": p.unrealized_pl_percent,
            }
            for p in sorted_by_pl[:5] if p.unrealized_pl > 0
        ]
        top_losers = [
            {
                "symbol": p.symbol,
                "unrealized_pl": p.unrealized_pl,
                "unrealized_pl_percent": p.unrealized_pl_percent,
            }
            for p in sorted_by_pl[-5:] if p.unrealized_pl < 0
        ]
        top_losers.reverse()  # Show worst first

        return PortfolioSummary(
            total_equity=account.equity,
            cash=account.cash,
            buying_power=account.buying_power,
            portfolio_value=account.portfolio_value,
            total_unrealized_pl=account.unrealized_pl,
            total_unrealized_pl_percent=(account.unrealized_pl / account.equity * 100) if account.equity > 0 else 0,
            total_realized_pl_today=account.realized_pl_today,
            total_positions=len(positions),
            long_positions=len(long_positions),
            short_positions=len(short_positions),
            total_market_value=total_market_value,
            top_gainers=top_gainers,
            top_losers=top_losers,
            pattern_day_trader=account.pattern_day_trader,
            account_blocked=account.account_blocked,
            trading_blocked=account.trading_blocked,
            updated_at=datetime.now(),
        )

    async def track_position_pl(
        self,
        symbol: str,
        entry_price: float,
        stop_loss: Optional[float] = None,
        target: Optional[float] = None,
        interval_seconds: int = 5,
        max_updates: int = 100,
    ) -> None:
        """
        Track position P&L in real-time (for monitoring/logging).

        Args:
            symbol: Symbol to track
            entry_price: Entry price for R-multiple calculation
            stop_loss: Stop loss price for risk calculation
            target: Target price for reward calculation
            interval_seconds: Update interval in seconds
            max_updates: Maximum number of updates before stopping
        """
        update_count = 0

        while update_count < max_updates:
            try:
                position = await self.get_position(symbol, use_cache=False)

                if not position:
                    logger.warning(f"No position found for {symbol}, stopping tracking")
                    break

                # Calculate R-multiple if stop loss provided
                r_multiple = None
                if stop_loss and entry_price:
                    risk_per_share = abs(entry_price - stop_loss)
                    pl_per_share = position.current_price - entry_price
                    if risk_per_share > 0:
                        r_multiple = pl_per_share / risk_per_share

                logger.info(
                    f"Position: {symbol} | "
                    f"Qty: {position.quantity} | "
                    f"Entry: ${entry_price:.2f} | "
                    f"Current: ${position.current_price:.2f} | "
                    f"P&L: ${position.unrealized_pl:.2f} ({position.unrealized_pl_percent:.2f}%)"
                    + (f" | R: {r_multiple:.2f}" if r_multiple else "")
                )

                update_count += 1
                await asyncio.sleep(interval_seconds)

            except Exception as e:
                logger.error(f"Error tracking position {symbol}: {e}")
                await asyncio.sleep(interval_seconds)

    def _calculate_position_pl(self, position: Position) -> PositionWithPnL:
        """Calculate detailed P&L for position"""
        pl_per_share = position.current_price - position.avg_entry_price

        return PositionWithPnL(
            symbol=position.symbol,
            quantity=position.quantity,
            side=position.side.value,
            avg_entry_price=position.avg_entry_price,
            current_price=position.current_price,
            market_value=position.market_value,
            cost_basis=position.cost_basis,
            unrealized_pl=position.unrealized_pl,
            unrealized_pl_percent=position.unrealized_pl_percent,
            unrealized_pl_per_share=pl_per_share,
            asset_class=position.asset_class,
            exchange=position.exchange,
            updated_at=datetime.now(),
        )

    async def calculate_risk_metrics(
        self,
        symbol: str,
        entry_price: float,
        stop_loss: float,
        account_size: float,
    ) -> Dict[str, Any]:
        """
        Calculate risk metrics for a position.

        Args:
            symbol: Symbol
            entry_price: Entry price
            stop_loss: Stop loss price
            account_size: Total account size

        Returns:
            Dict with risk metrics
        """
        position = await self.get_position(symbol)

        if not position:
            return {"error": "Position not found"}

        # Risk calculations
        risk_per_share = abs(entry_price - stop_loss)
        risk_amount = position.quantity * risk_per_share
        risk_percent = (risk_amount / account_size) * 100

        # Current P&L in R multiples
        pl_per_share = position.current_price - entry_price
        r_multiple = pl_per_share / risk_per_share if risk_per_share > 0 else 0

        return {
            "symbol": symbol,
            "quantity": position.quantity,
            "entry_price": entry_price,
            "current_price": position.current_price,
            "stop_loss": stop_loss,
            "risk_per_share": risk_per_share,
            "risk_amount": risk_amount,
            "risk_percent": risk_percent,
            "unrealized_pl": position.unrealized_pl,
            "r_multiple": r_multiple,
        }
