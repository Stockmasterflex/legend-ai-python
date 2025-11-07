"""
Trade Management Service
Track open/closed trades with P&L calculation and statistics
"""
import logging
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import dataclass, asdict
import uuid

from app.services.cache import get_cache_service

logger = logging.getLogger(__name__)


@dataclass
class Trade:
    """Trade record"""
    trade_id: str
    ticker: str
    entry_price: float
    stop_loss: float
    target_price: float
    position_size: int
    risk_amount: float
    reward_amount: float
    status: str  # "open", "closed"
    entry_date: str
    exit_date: Optional[str] = None
    exit_price: Optional[float] = None
    profit_loss: Optional[float] = None
    profit_loss_pct: Optional[float] = None
    win: Optional[bool] = None  # True if profit, False if loss
    r_multiple: Optional[float] = None  # Profit/Risk multiple
    notes: Optional[str] = None


class TradeManager:
    """Service for managing trades and statistics"""

    def __init__(self):
        self.cache = get_cache_service()

    async def create_trade(
        self,
        ticker: str,
        entry_price: float,
        stop_loss: float,
        target_price: float,
        position_size: int,
        risk_amount: float,
        notes: Optional[str] = None
    ) -> Trade:
        """Create a new trade"""

        trade_id = str(uuid.uuid4())[:8]
        reward_amount = abs(target_price - entry_price) * position_size

        trade = Trade(
            trade_id=trade_id,
            ticker=ticker.upper(),
            entry_price=entry_price,
            stop_loss=stop_loss,
            target_price=target_price,
            position_size=position_size,
            risk_amount=risk_amount,
            reward_amount=reward_amount,
            status="open",
            entry_date=datetime.now().isoformat(),
            notes=notes or ""
        )

        # Store in cache
        cache = await self.cache._get_redis()
        trade_key = f"trade:{trade_id}"
        await cache.setex(trade_key, 30 * 24 * 3600, json.dumps(asdict(trade)))

        # Add to open trades list
        await cache.lpush(f"trades:open", trade_id)

        logger.info(f"✅ Trade created: {trade_id} - {ticker} @ ${entry_price:.2f}")

        return trade

    async def close_trade(
        self,
        trade_id: str,
        exit_price: float
    ) -> Trade:
        """Close a trade and calculate P&L"""

        # Retrieve trade
        cache = await self.cache._get_redis()
        trade_data = await cache.get(f"trade:{trade_id}")

        if not trade_data:
            raise ValueError(f"Trade {trade_id} not found")

        trade_dict = json.loads(trade_data)
        trade = Trade(**trade_dict)

        # Calculate P&L
        profit_loss = (exit_price - trade.entry_price) * trade.position_size
        profit_loss_pct = ((exit_price - trade.entry_price) / trade.entry_price) * 100

        # Determine if win/loss
        is_long = trade.target_price > trade.entry_price
        win = profit_loss > 0

        # Calculate R multiple
        if trade.risk_amount > 0:
            r_multiple = profit_loss / trade.risk_amount
        else:
            r_multiple = 0

        # Update trade
        trade.status = "closed"
        trade.exit_date = datetime.now().isoformat()
        trade.exit_price = exit_price
        trade.profit_loss = profit_loss
        trade.profit_loss_pct = profit_loss_pct
        trade.win = win
        trade.r_multiple = r_multiple

        # Update cache
        trade_key = f"trade:{trade_id}"
        await cache.setex(trade_key, 30 * 24 * 3600, json.dumps(asdict(trade)))

        # Move from open to closed
        await cache.lrem(f"trades:open", 1, trade_id)
        await cache.lpush(f"trades:closed", trade_id)

        logger.info(f"✅ Trade closed: {trade_id} - P&L: ${profit_loss:.2f} ({profit_loss_pct:.2f}%)")

        return trade

    async def get_open_trades(self) -> List[Trade]:
        """Get all open trades"""

        cache = await self.cache._get_redis()
        trade_ids = await cache.lrange(f"trades:open", 0, -1)

        trades = []
        for trade_id in trade_ids:
            trade_data = await cache.get(f"trade:{trade_id}")
            if trade_data:
                trades.append(Trade(**json.loads(trade_data)))

        return trades

    async def get_closed_trades(self, limit: int = 50) -> List[Trade]:
        """Get closed trades"""

        cache = await self.cache._get_redis()
        trade_ids = await cache.lrange(f"trades:closed", 0, limit - 1)

        trades = []
        for trade_id in trade_ids:
            trade_data = await cache.get(f"trade:{trade_id}")
            if trade_data:
                trades.append(Trade(**json.loads(trade_data)))

        return trades

    async def get_statistics(self) -> Dict[str, Any]:
        """Calculate trading statistics from closed trades"""

        closed_trades = await self.get_closed_trades(limit=1000)

        if not closed_trades:
            return {
                "total_trades": 0,
                "message": "No closed trades yet"
            }

        total_trades = len(closed_trades)
        winning_trades = [t for t in closed_trades if t.win]
        losing_trades = [t for t in closed_trades if not t.win]

        wins = len(winning_trades)
        losses = len(losing_trades)
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0

        total_profit_loss = sum(t.profit_loss for t in closed_trades if t.profit_loss)
        total_risk = sum(t.risk_amount for t in closed_trades)

        avg_win = sum(t.profit_loss for t in winning_trades if t.profit_loss) / wins if wins > 0 else 0
        avg_loss = sum(t.profit_loss for t in losing_trades if t.profit_loss) / losses if losses > 0 else 0

        avg_r_multiple = sum(t.r_multiple for t in closed_trades if t.r_multiple) / total_trades if total_trades > 0 else 0

        # Expectancy = (Win% × Avg Win) + (Loss% × Avg Loss)
        expectancy = (win_rate / 100 * avg_win) + ((1 - win_rate / 100) * avg_loss)

        return {
            "total_trades": total_trades,
            "winning_trades": wins,
            "losing_trades": losses,
            "win_rate_pct": round(win_rate, 2),
            "total_profit_loss": round(total_profit_loss, 2),
            "total_risk": round(total_risk, 2),
            "profit_factor": round(total_profit_loss / abs(sum(t.profit_loss for t in losing_trades if t.profit_loss)), 2) if sum(t.profit_loss for t in losing_trades if t.profit_loss) else 0,
            "average_win": round(avg_win, 2),
            "average_loss": round(avg_loss, 2),
            "average_r_multiple": round(avg_r_multiple, 2),
            "expectancy_per_trade": round(expectancy, 2),
            "expectancy_description": self._describe_expectancy(expectancy)
        }

    def _describe_expectancy(self, expectancy: float) -> str:
        """Describe trading expectancy quality"""
        if expectancy > 1.0:
            return "✅ Excellent - Strong positive expectancy"
        elif expectancy > 0.5:
            return "✅ Good - Positive expectancy"
        elif expectancy > 0:
            return "⚠️ Fair - Slightly positive expectancy"
        else:
            return "❌ Negative - Losing edge - Review strategy"


# Global instance
_trade_manager: Optional[TradeManager] = None


def get_trade_manager() -> TradeManager:
    """Get or create trade manager singleton"""
    global _trade_manager
    if _trade_manager is None:
        _trade_manager = TradeManager()
    return _trade_manager
