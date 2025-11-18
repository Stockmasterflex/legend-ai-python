"""
Trade Journal Service
Comprehensive professional trade journaling system
"""
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import select, func, and_, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.models import (
    TradeJournal, TradeTag, TradeMistake, Playbook, TradeLesson, TradeReview,
    Ticker, PatternScan, TradeStatus, EmotionalState, MarketCondition
)

logger = logging.getLogger(__name__)


class TradeJournalService:
    """Service for managing comprehensive trade journaling"""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ==================== PRE-TRADE PLANNING ====================

    async def create_trade_plan(
        self,
        ticker: str,
        pattern_identified: str,
        thesis: str,
        planned_entry: float,
        planned_stop: float,
        planned_target: float,
        planned_position_size: int,
        checklist_data: Optional[Dict] = None,
        screenshot_url: Optional[str] = None,
        user_id: str = "default"
    ) -> TradeJournal:
        """Create a pre-trade plan with checklist"""

        # Get or create ticker
        ticker_obj = await self._get_or_create_ticker(ticker.upper())

        # Calculate risk/reward
        risk_per_share = abs(planned_entry - planned_stop)
        reward_per_share = abs(planned_target - planned_entry)
        planned_risk_amount = risk_per_share * planned_position_size
        planned_risk_reward = reward_per_share / risk_per_share if risk_per_share > 0 else 0

        # Generate trade ID
        trade_id = f"TRD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"

        # Create journal entry
        trade = TradeJournal(
            trade_id=trade_id,
            user_id=user_id,
            ticker_id=ticker_obj.id,
            pattern_identified=pattern_identified,
            thesis=thesis,
            planned_entry=planned_entry,
            planned_stop=planned_stop,
            planned_target=planned_target,
            planned_position_size=planned_position_size,
            planned_risk_amount=planned_risk_amount,
            planned_risk_reward=planned_risk_reward,
            checklist_data=checklist_data,
            screenshot_url=screenshot_url,
            status=TradeStatus.PLANNED
        )

        self.db.add(trade)
        await self.db.commit()
        await self.db.refresh(trade)

        logger.info(f"✅ Trade plan created: {trade_id} - {ticker} @ ${planned_entry:.2f}")

        return trade

    async def complete_checklist(
        self,
        trade_id: str,
        checklist_data: Dict
    ) -> TradeJournal:
        """Complete pre-trade checklist"""

        trade = await self._get_trade_by_id(trade_id)
        trade.checklist_data = checklist_data
        trade.checklist_completed = all(checklist_data.values())

        await self.db.commit()
        await self.db.refresh(trade)

        return trade

    # ==================== TRADE EXECUTION ====================

    async def execute_entry(
        self,
        trade_id: str,
        actual_entry_price: float,
        actual_position_size: int,
        actual_stop_price: Optional[float] = None,
        emotional_state: Optional[EmotionalState] = None,
        market_condition: Optional[MarketCondition] = None,
        market_context: Optional[str] = None
    ) -> TradeJournal:
        """Execute trade entry and track slippage"""

        trade = await self._get_trade_by_id(trade_id)

        # Calculate slippage
        entry_slippage = actual_entry_price - trade.planned_entry
        slippage_cost = entry_slippage * actual_position_size

        # Update trade
        trade.actual_entry_price = actual_entry_price
        trade.actual_position_size = actual_position_size
        trade.actual_stop_price = actual_stop_price or trade.planned_stop
        trade.entry_slippage = entry_slippage
        trade.slippage_cost = slippage_cost
        trade.entry_timestamp = datetime.now()
        trade.status = TradeStatus.OPEN
        trade.emotional_state_entry = emotional_state
        trade.market_condition = market_condition
        trade.market_context = market_context

        await self.db.commit()
        await self.db.refresh(trade)

        logger.info(f"✅ Trade entered: {trade_id} @ ${actual_entry_price:.2f} (slippage: ${slippage_cost:.2f})")

        return trade

    async def add_partial_exit(
        self,
        trade_id: str,
        exit_price: float,
        shares_sold: int,
        reason: str
    ) -> TradeJournal:
        """Record a partial exit"""

        trade = await self._get_trade_by_id(trade_id)

        # Calculate partial P&L
        partial_pnl = (exit_price - trade.actual_entry_price) * shares_sold

        # Add to partial exits list
        partial_exit = {
            "timestamp": datetime.now().isoformat(),
            "price": exit_price,
            "shares": shares_sold,
            "reason": reason,
            "pnl": partial_pnl
        }

        if trade.partial_exits:
            trade.partial_exits.append(partial_exit)
        else:
            trade.partial_exits = [partial_exit]

        await self.db.commit()
        await self.db.refresh(trade)

        return trade

    async def execute_exit(
        self,
        trade_id: str,
        exit_price: float,
        exit_reason: str,
        emotional_state: Optional[EmotionalState] = None,
        fees_paid: float = 0.0,
        follow_through_notes: Optional[str] = None
    ) -> TradeJournal:
        """Execute trade exit and calculate final metrics"""

        trade = await self._get_trade_by_id(trade_id)

        # Calculate remaining position (after partial exits)
        shares_exited_partial = 0
        if trade.partial_exits:
            shares_exited_partial = sum(e['shares'] for e in trade.partial_exits)

        remaining_shares = trade.actual_position_size - shares_exited_partial

        # Calculate slippage on exit
        exit_slippage = exit_price - (trade.planned_target if exit_price > trade.actual_entry_price else trade.actual_stop_price)

        # Calculate gross P&L
        gross_pnl = (exit_price - trade.actual_entry_price) * remaining_shares

        # Add partial exit P&L
        if trade.partial_exits:
            gross_pnl += sum(e['pnl'] for e in trade.partial_exits)

        # Calculate net P&L
        net_pnl = gross_pnl - fees_paid - (trade.slippage_cost or 0)

        # Calculate R-multiple
        risk_amount = trade.planned_risk_amount
        r_multiple = net_pnl / risk_amount if risk_amount > 0 else 0

        # Calculate holding period
        entry_time = trade.entry_timestamp
        exit_time = datetime.now()
        holding_period_hours = (exit_time - entry_time).total_seconds() / 3600

        # Update trade
        trade.exit_price = exit_price
        trade.exit_timestamp = exit_time
        trade.exit_reason = exit_reason
        trade.exit_slippage = exit_slippage
        trade.gross_pnl = gross_pnl
        trade.net_pnl = net_pnl
        trade.r_multiple = r_multiple
        trade.fees_paid = fees_paid
        trade.holding_period_hours = holding_period_hours
        trade.emotional_state_exit = emotional_state
        trade.follow_through_notes = follow_through_notes
        trade.status = TradeStatus.CLOSED

        await self.db.commit()
        await self.db.refresh(trade)

        logger.info(f"✅ Trade closed: {trade_id} - P&L: ${net_pnl:.2f} ({r_multiple:.2f}R)")

        return trade

    async def cancel_trade(self, trade_id: str, reason: str) -> TradeJournal:
        """Cancel a planned trade"""

        trade = await self._get_trade_by_id(trade_id)
        trade.status = TradeStatus.CANCELLED
        trade.follow_through_notes = reason

        await self.db.commit()
        await self.db.refresh(trade)

        return trade

    # ==================== POST-TRADE REVIEW ====================

    async def add_trade_notes(
        self,
        trade_id: str,
        what_went_well: Optional[str] = None,
        what_went_wrong: Optional[str] = None,
        lessons_learned: Optional[str] = None
    ) -> TradeJournal:
        """Add post-trade review notes"""

        trade = await self._get_trade_by_id(trade_id)

        if what_went_well:
            trade.what_went_well = what_went_well
        if what_went_wrong:
            trade.what_went_wrong = what_went_wrong
        if lessons_learned:
            trade.lessons_learned = lessons_learned

        await self.db.commit()
        await self.db.refresh(trade)

        return trade

    async def add_trade_tag(self, trade_id: str, tag: str) -> TradeTag:
        """Add a tag to a trade"""

        trade = await self._get_trade_by_id(trade_id)

        tag_obj = TradeTag(
            trade_journal_id=trade.id,
            tag=tag.lower()
        )

        self.db.add(tag_obj)
        await self.db.commit()
        await self.db.refresh(tag_obj)

        return tag_obj

    async def add_mistake(
        self,
        trade_id: str,
        category: str,
        mistake_type: str,
        description: str,
        impact: str
    ) -> TradeMistake:
        """Categorize a trading mistake"""

        trade = await self._get_trade_by_id(trade_id)

        mistake = TradeMistake(
            trade_journal_id=trade.id,
            category=category,
            mistake_type=mistake_type,
            description=description,
            impact=impact
        )

        self.db.add(mistake)
        await self.db.commit()
        await self.db.refresh(mistake)

        return mistake

    # ==================== PLAYBOOKS & LEARNING ====================

    async def create_playbook(
        self,
        name: str,
        description: str,
        pattern_type: str,
        entry_criteria: List[str],
        exit_criteria: List[str],
        risk_management: Dict,
        user_id: str = "default"
    ) -> Playbook:
        """Create a trading playbook"""

        playbook = Playbook(
            user_id=user_id,
            name=name,
            description=description,
            pattern_type=pattern_type,
            entry_criteria=entry_criteria,
            exit_criteria=exit_criteria,
            risk_management=risk_management
        )

        self.db.add(playbook)
        await self.db.commit()
        await self.db.refresh(playbook)

        return playbook

    async def update_playbook_stats(self, playbook_id: int):
        """Update playbook statistics from trades"""

        playbook = await self.db.get(Playbook, playbook_id)

        # Get all trades using this pattern
        result = await self.db.execute(
            select(TradeJournal).where(
                and_(
                    TradeJournal.pattern_identified == playbook.pattern_type,
                    TradeJournal.status == TradeStatus.CLOSED
                )
            )
        )
        trades = result.scalars().all()

        if trades:
            total_trades = len(trades)
            winning_trades = sum(1 for t in trades if t.net_pnl and t.net_pnl > 0)
            avg_r = sum(t.r_multiple for t in trades if t.r_multiple) / total_trades

            playbook.total_trades = total_trades
            playbook.winning_trades = winning_trades
            playbook.success_rate = (winning_trades / total_trades) * 100
            playbook.avg_r_multiple = avg_r

            await self.db.commit()

    async def add_lesson(
        self,
        title: str,
        lesson: str,
        pattern_type: Optional[str] = None,
        importance: str = "medium",
        user_id: str = "default"
    ) -> TradeLesson:
        """Record a trading lesson"""

        lesson_obj = TradeLesson(
            user_id=user_id,
            title=title,
            lesson=lesson,
            pattern_type=pattern_type,
            importance=importance,
            trades_count=1,
            last_occurred=datetime.now()
        )

        self.db.add(lesson_obj)
        await self.db.commit()
        await self.db.refresh(lesson_obj)

        return lesson_obj

    # ==================== ANALYTICS & QUERIES ====================

    async def get_trades(
        self,
        user_id: str = "default",
        status: Optional[TradeStatus] = None,
        pattern: Optional[str] = None,
        tags: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 50
    ) -> List[TradeJournal]:
        """Get trades with filters"""

        query = select(TradeJournal).where(TradeJournal.user_id == user_id)

        if status:
            query = query.where(TradeJournal.status == status)
        if pattern:
            query = query.where(TradeJournal.pattern_identified == pattern)
        if start_date:
            query = query.where(TradeJournal.created_at >= start_date)
        if end_date:
            query = query.where(TradeJournal.created_at <= end_date)

        # Handle tags filter
        if tags:
            # Join with TradeTag and filter
            query = query.join(TradeTag).where(TradeTag.tag.in_(tags))

        query = query.order_by(desc(TradeJournal.created_at)).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_performance_analytics(
        self,
        user_id: str = "default",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Calculate comprehensive performance analytics"""

        query = select(TradeJournal).where(
            and_(
                TradeJournal.user_id == user_id,
                TradeJournal.status == TradeStatus.CLOSED
            )
        )

        if start_date:
            query = query.where(TradeJournal.exit_timestamp >= start_date)
        if end_date:
            query = query.where(TradeJournal.exit_timestamp <= end_date)

        result = await self.db.execute(query)
        trades = result.scalars().all()

        if not trades:
            return {"total_trades": 0, "message": "No closed trades found"}

        # Basic metrics
        total_trades = len(trades)
        winners = [t for t in trades if t.net_pnl and t.net_pnl > 0]
        losers = [t for t in trades if t.net_pnl and t.net_pnl <= 0]

        win_count = len(winners)
        loss_count = len(losers)
        win_rate = (win_count / total_trades) * 100

        # P&L metrics
        total_pnl = sum(t.net_pnl for t in trades if t.net_pnl)
        avg_win = sum(t.net_pnl for t in winners) / win_count if win_count > 0 else 0
        avg_loss = sum(t.net_pnl for t in losers) / loss_count if loss_count > 0 else 0

        # R-multiple distribution
        r_multiples = [t.r_multiple for t in trades if t.r_multiple]
        avg_r = sum(r_multiples) / len(r_multiples) if r_multiples else 0

        # Best/Worst trades
        best_trade = max(trades, key=lambda t: t.net_pnl or 0)
        worst_trade = min(trades, key=lambda t: t.net_pnl or 0)

        # Time analysis
        holding_times = [t.holding_period_hours for t in trades if t.holding_period_hours]
        avg_holding_time = sum(holding_times) / len(holding_times) if holding_times else 0

        return {
            "total_trades": total_trades,
            "winning_trades": win_count,
            "losing_trades": loss_count,
            "win_rate": round(win_rate, 2),
            "total_pnl": round(total_pnl, 2),
            "average_win": round(avg_win, 2),
            "average_loss": round(avg_loss, 2),
            "average_r_multiple": round(avg_r, 2),
            "best_trade": {
                "trade_id": best_trade.trade_id,
                "pnl": round(best_trade.net_pnl, 2),
                "r_multiple": round(best_trade.r_multiple, 2) if best_trade.r_multiple else 0
            },
            "worst_trade": {
                "trade_id": worst_trade.trade_id,
                "pnl": round(worst_trade.net_pnl, 2),
                "r_multiple": round(worst_trade.r_multiple, 2) if worst_trade.r_multiple else 0
            },
            "avg_holding_time_hours": round(avg_holding_time, 2)
        }

    async def get_pattern_performance(
        self,
        user_id: str = "default"
    ) -> List[Dict[str, Any]]:
        """Get performance breakdown by pattern"""

        result = await self.db.execute(
            select(
                TradeJournal.pattern_identified,
                func.count(TradeJournal.id).label('total'),
                func.sum(func.case((TradeJournal.net_pnl > 0, 1), else_=0)).label('wins'),
                func.avg(TradeJournal.r_multiple).label('avg_r'),
                func.sum(TradeJournal.net_pnl).label('total_pnl')
            ).where(
                and_(
                    TradeJournal.user_id == user_id,
                    TradeJournal.status == TradeStatus.CLOSED
                )
            ).group_by(TradeJournal.pattern_identified)
        )

        patterns = []
        for row in result:
            pattern, total, wins, avg_r, total_pnl = row
            win_rate = (wins / total * 100) if total > 0 else 0

            patterns.append({
                "pattern": pattern,
                "total_trades": total,
                "wins": wins or 0,
                "win_rate": round(win_rate, 2),
                "avg_r_multiple": round(float(avg_r), 2) if avg_r else 0,
                "total_pnl": round(float(total_pnl), 2) if total_pnl else 0
            })

        return sorted(patterns, key=lambda x: x['total_pnl'], reverse=True)

    async def get_mistake_analysis(
        self,
        user_id: str = "default"
    ) -> List[Dict[str, Any]]:
        """Analyze common mistakes"""

        # Join trades with mistakes
        result = await self.db.execute(
            select(
                TradeMistake.category,
                TradeMistake.mistake_type,
                func.count(TradeMistake.id).label('count'),
                func.avg(TradeJournal.net_pnl).label('avg_impact')
            ).join(
                TradeJournal
            ).where(
                TradeJournal.user_id == user_id
            ).group_by(
                TradeMistake.category,
                TradeMistake.mistake_type
            ).order_by(
                desc('count')
            )
        )

        mistakes = []
        for row in result:
            category, mistake_type, count, avg_impact = row
            mistakes.append({
                "category": category,
                "mistake_type": mistake_type,
                "occurrences": count,
                "avg_impact": round(float(avg_impact), 2) if avg_impact else 0
            })

        return mistakes

    # ==================== HELPER METHODS ====================

    async def _get_trade_by_id(self, trade_id: str) -> TradeJournal:
        """Get trade by trade_id"""
        result = await self.db.execute(
            select(TradeJournal).where(TradeJournal.trade_id == trade_id)
        )
        trade = result.scalar_one_or_none()

        if not trade:
            raise ValueError(f"Trade {trade_id} not found")

        return trade

    async def _get_or_create_ticker(self, symbol: str) -> Ticker:
        """Get or create ticker"""
        result = await self.db.execute(
            select(Ticker).where(Ticker.symbol == symbol)
        )
        ticker = result.scalar_one_or_none()

        if not ticker:
            ticker = Ticker(symbol=symbol)
            self.db.add(ticker)
            await self.db.commit()
            await self.db.refresh(ticker)

        return ticker


def get_trade_journal_service(db: AsyncSession) -> TradeJournalService:
    """Get trade journal service instance"""
    return TradeJournalService(db)
