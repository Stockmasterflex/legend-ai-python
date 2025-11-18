"""
Trade Plan Library Service
Manages trade plan storage, tracking, and analytics
"""
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from collections import defaultdict

from sqlalchemy import select, and_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TradePlan, Ticker

logger = logging.getLogger(__name__)


class TradePlanLibrary:
    """Service for managing trade plan library and analytics"""

    async def get_all_plans(
        self,
        db: AsyncSession,
        user_id: str = "default",
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get all trade plans with optional filtering

        Args:
            db: Database session
            user_id: User ID for filtering
            status: Optional status filter (planned, active, completed, cancelled)
            limit: Maximum number of results
            offset: Offset for pagination

        Returns:
            List of trade plans with ticker info
        """
        query = (
            select(TradePlan, Ticker)
            .join(Ticker, TradePlan.ticker_id == Ticker.id)
            .where(TradePlan.user_id == user_id)
            .order_by(desc(TradePlan.created_at))
            .limit(limit)
            .offset(offset)
        )

        if status:
            query = query.where(TradePlan.status == status)

        result = await db.execute(query)
        plans = result.all()

        return [
            {
                "id": plan.id,
                "ticker": ticker.symbol,
                "pattern_type": plan.pattern_type,
                "pattern_score": plan.pattern_score,
                "status": plan.status,
                "entry_zone": {
                    "low": plan.entry_zone_low,
                    "high": plan.entry_zone_high,
                    "optimal": plan.optimal_entry
                },
                "stop": plan.initial_stop,
                "targets": {
                    "best": plan.best_case_target,
                    "base": plan.base_case_target,
                    "worst": plan.worst_case_target
                },
                "position_size": plan.position_size,
                "risk_amount": plan.risk_amount,
                "outcome": plan.outcome,
                "pnl_amount": plan.pnl_amount,
                "pnl_percentage": plan.pnl_percentage,
                "created_at": plan.created_at.isoformat() if plan.created_at else None,
                "pdf_path": plan.pdf_path
            }
            for plan, ticker in plans
        ]

    async def get_plan_by_id(
        self,
        db: AsyncSession,
        plan_id: int,
        user_id: str = "default"
    ) -> Optional[Dict[str, Any]]:
        """Get detailed trade plan by ID"""
        result = await db.execute(
            select(TradePlan, Ticker)
            .join(Ticker, TradePlan.ticker_id == Ticker.id)
            .where(and_(
                TradePlan.id == plan_id,
                TradePlan.user_id == user_id
            ))
        )

        row = result.first()
        if not row:
            return None

        plan, ticker = row

        return {
            "id": plan.id,
            "ticker": ticker.symbol,
            "ticker_name": ticker.name,
            "pattern_type": plan.pattern_type,
            "pattern_score": plan.pattern_score,
            "current_price": plan.current_price,
            "entry_zone": {
                "low": plan.entry_zone_low,
                "high": plan.entry_zone_high,
                "optimal": plan.optimal_entry
            },
            "stop_levels": {
                "initial": plan.initial_stop,
                "trailing": plan.trailing_stop,
                "invalidation": plan.invalidation_price
            },
            "targets": {
                "best": {"price": plan.best_case_target, "rr": plan.best_case_rr},
                "base": {"price": plan.base_case_target, "rr": plan.base_case_rr},
                "worst": {"price": plan.worst_case_target, "rr": plan.worst_case_rr}
            },
            "position": {
                "size": plan.position_size,
                "value": plan.position_value,
                "risk_amount": plan.risk_amount,
                "risk_percentage": plan.risk_percentage
            },
            "details": {
                "timeframe": plan.timeframe,
                "strategy": plan.strategy,
                "notes": plan.notes,
                "checklist": plan.checklist,
            },
            "execution": {
                "status": plan.status,
                "entry_date": plan.entry_date.isoformat() if plan.entry_date else None,
                "exit_date": plan.exit_date.isoformat() if plan.exit_date else None,
                "entry_price_actual": plan.entry_price_actual,
                "exit_price_actual": plan.exit_price_actual
            },
            "outcome": {
                "result": plan.outcome,
                "pnl_amount": plan.pnl_amount,
                "pnl_percentage": plan.pnl_percentage,
                "target_hit": plan.target_hit,
                "lessons_learned": plan.lessons_learned
            },
            "files": {
                "pdf_path": plan.pdf_path,
                "chart_url": plan.chart_url
            },
            "created_at": plan.created_at.isoformat() if plan.created_at else None,
            "updated_at": plan.updated_at.isoformat() if plan.updated_at else None
        }

    async def update_plan_outcome(
        self,
        db: AsyncSession,
        plan_id: int,
        outcome: str,
        exit_price: float,
        lessons_learned: Optional[str] = None
    ) -> bool:
        """
        Update trade plan with outcome and P&L

        Args:
            db: Database session
            plan_id: Trade plan ID
            outcome: Outcome (win, loss, breakeven, stopped)
            exit_price: Actual exit price
            lessons_learned: Optional lessons learned text

        Returns:
            True if updated successfully
        """
        result = await db.execute(
            select(TradePlan).where(TradePlan.id == plan_id)
        )

        plan = result.scalar_one_or_none()
        if not plan:
            return False

        # Calculate P&L
        if plan.entry_price_actual:
            price_diff = exit_price - plan.entry_price_actual
            pnl_amount = price_diff * plan.position_size
            pnl_percentage = (price_diff / plan.entry_price_actual) * 100

            plan.pnl_amount = pnl_amount
            plan.pnl_percentage = pnl_percentage

        # Determine which target was hit
        target_hit = "none"
        if exit_price >= plan.best_case_target:
            target_hit = "best"
        elif exit_price >= plan.base_case_target:
            target_hit = "base"
        elif exit_price >= plan.worst_case_target:
            target_hit = "worst"

        plan.outcome = outcome
        plan.exit_price_actual = exit_price
        plan.exit_date = datetime.utcnow()
        plan.target_hit = target_hit
        plan.status = "completed"

        if lessons_learned:
            plan.lessons_learned = lessons_learned

        await db.commit()

        logger.info(f"✅ Updated plan {plan_id} outcome: {outcome}, P&L: ${plan.pnl_amount:.2f}")
        return True

    async def get_analytics(
        self,
        db: AsyncSession,
        user_id: str = "default",
        days: int = 90
    ) -> Dict[str, Any]:
        """
        Get comprehensive trade plan analytics

        Args:
            db: Database session
            user_id: User ID
            days: Number of days to analyze

        Returns:
            Analytics dictionary with various metrics
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        # Get all completed plans in timeframe
        result = await db.execute(
            select(TradePlan, Ticker)
            .join(Ticker, TradePlan.ticker_id == Ticker.id)
            .where(and_(
                TradePlan.user_id == user_id,
                TradePlan.status == "completed",
                TradePlan.created_at >= cutoff_date
            ))
        )

        plans = result.all()

        if not plans:
            return {
                "total_plans": 0,
                "message": "No completed trades in timeframe"
            }

        # Calculate overall statistics
        total_plans = len(plans)
        wins = sum(1 for p, _ in plans if p.outcome == "win")
        losses = sum(1 for p, _ in plans if p.outcome == "loss")
        breakevens = sum(1 for p, _ in plans if p.outcome == "breakeven")
        stopped = sum(1 for p, _ in plans if p.outcome == "stopped")

        win_rate = (wins / total_plans * 100) if total_plans > 0 else 0

        # P&L statistics
        total_pnl = sum(p.pnl_amount for p, _ in plans if p.pnl_amount is not None)
        avg_win = sum(p.pnl_amount for p, _ in plans if p.outcome == "win" and p.pnl_amount) / wins if wins > 0 else 0
        avg_loss = sum(p.pnl_amount for p, _ in plans if p.outcome == "loss" and p.pnl_amount) / losses if losses > 0 else 0

        # Pattern performance
        pattern_stats = await self._get_pattern_statistics(plans)

        # Target hit statistics
        target_stats = self._get_target_statistics(plans)

        # Recent performance
        recent_plans = sorted(plans, key=lambda x: x[0].created_at, reverse=True)[:10]
        recent_performance = [
            {
                "ticker": ticker.symbol,
                "pattern": plan.pattern_type,
                "outcome": plan.outcome,
                "pnl": plan.pnl_amount,
                "date": plan.created_at.strftime("%Y-%m-%d") if plan.created_at else None
            }
            for plan, ticker in recent_plans
        ]

        # Generate improvement suggestions
        suggestions = self._generate_improvement_suggestions(
            win_rate, pattern_stats, avg_win, avg_loss
        )

        return {
            "total_plans": total_plans,
            "timeframe_days": days,
            "overall": {
                "wins": wins,
                "losses": losses,
                "breakevens": breakevens,
                "stopped": stopped,
                "win_rate": round(win_rate, 2),
                "total_pnl": round(total_pnl, 2),
                "avg_win": round(avg_win, 2),
                "avg_loss": round(avg_loss, 2),
                "profit_factor": round(abs(avg_win / avg_loss), 2) if avg_loss != 0 else 0
            },
            "by_pattern": pattern_stats,
            "target_performance": target_stats,
            "recent_trades": recent_performance,
            "improvement_suggestions": suggestions
        }

    async def _get_pattern_statistics(
        self,
        plans: List[tuple]
    ) -> Dict[str, Dict[str, Any]]:
        """Calculate win rate by pattern type"""
        pattern_data = defaultdict(lambda: {"wins": 0, "losses": 0, "total": 0, "pnl": 0})

        for plan, ticker in plans:
            pattern = plan.pattern_type
            pattern_data[pattern]["total"] += 1

            if plan.outcome == "win":
                pattern_data[pattern]["wins"] += 1
            elif plan.outcome == "loss":
                pattern_data[pattern]["losses"] += 1

            if plan.pnl_amount:
                pattern_data[pattern]["pnl"] += plan.pnl_amount

        # Calculate win rates
        result = {}
        for pattern, data in pattern_data.items():
            win_rate = (data["wins"] / data["total"] * 100) if data["total"] > 0 else 0
            result[pattern] = {
                "total": data["total"],
                "wins": data["wins"],
                "losses": data["losses"],
                "win_rate": round(win_rate, 2),
                "total_pnl": round(data["pnl"], 2)
            }

        return dict(sorted(result.items(), key=lambda x: x[1]["total"], reverse=True))

    def _get_target_statistics(self, plans: List[tuple]) -> Dict[str, int]:
        """Calculate how often each target level is hit"""
        target_counts = {
            "best": 0,
            "base": 0,
            "worst": 0,
            "none": 0
        }

        for plan, _ in plans:
            if plan.target_hit:
                target_counts[plan.target_hit] += 1

        return target_counts

    def _generate_improvement_suggestions(
        self,
        win_rate: float,
        pattern_stats: Dict[str, Dict],
        avg_win: float,
        avg_loss: float
    ) -> List[str]:
        """Generate AI-powered improvement suggestions"""
        suggestions = []

        # Win rate suggestions
        if win_rate < 50:
            suggestions.append(
                f"⚠️ Win rate at {win_rate:.1f}% is below 50%. "
                "Consider being more selective with entry criteria."
            )
        elif win_rate > 70:
            suggestions.append(
                f"✅ Excellent win rate of {win_rate:.1f}%! "
                "You might be able to increase position sizes slightly."
            )

        # Pattern-specific suggestions
        if pattern_stats:
            best_pattern = max(pattern_stats.items(), key=lambda x: x[1]["win_rate"])
            worst_pattern = min(pattern_stats.items(), key=lambda x: x[1]["win_rate"])

            if best_pattern[1]["win_rate"] > 70:
                suggestions.append(
                    f"✅ {best_pattern[0]} pattern has {best_pattern[1]['win_rate']:.1f}% win rate. "
                    "Focus more on this pattern type."
                )

            if worst_pattern[1]["win_rate"] < 40 and worst_pattern[1]["total"] >= 5:
                suggestions.append(
                    f"⚠️ {worst_pattern[0]} pattern has only {worst_pattern[1]['win_rate']:.1f}% win rate. "
                    "Consider avoiding or refining this setup."
                )

        # Risk/reward suggestions
        if avg_win and avg_loss:
            rr_ratio = abs(avg_win / avg_loss)
            if rr_ratio < 1.5:
                suggestions.append(
                    f"⚠️ Average R:R ratio of {rr_ratio:.2f} is low. "
                    "Aim for higher reward targets or tighter stops."
                )
            elif rr_ratio > 2.5:
                suggestions.append(
                    f"✅ Excellent R:R ratio of {rr_ratio:.2f}! "
                    "Your trade selection is strong."
                )

        # General suggestions
        if not suggestions:
            suggestions.append(
                "✅ Overall performance is solid. Keep following your system!"
            )

        return suggestions


# Global instance
_library: Optional[TradePlanLibrary] = None


def get_trade_plan_library() -> TradePlanLibrary:
    """Get or create trade plan library singleton"""
    global _library
    if _library is None:
        _library = TradePlanLibrary()
    return _library
