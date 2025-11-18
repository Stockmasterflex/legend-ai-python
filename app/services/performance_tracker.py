"""
Performance Tracking Module for Paper Trading Automation

Tracks all paper trades, calculates performance metrics,
generates reports, and provides learning insights.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


class TradeOutcome(Enum):
    """Trade outcome classification"""
    WIN = "win"
    LOSS = "loss"
    BREAKEVEN = "breakeven"
    OPEN = "open"


class MistakeCategory(Enum):
    """Common trading mistakes"""
    PREMATURE_EXIT = "premature_exit"
    LATE_EXIT = "late_exit"
    POOR_ENTRY = "poor_entry"
    OVERSIZED = "oversized"
    UNDERSIZED = "undersized"
    VIOLATED_STOP = "violated_stop"
    EMOTIONAL = "emotional"
    IGNORED_SIGNAL = "ignored_signal"
    OTHER = "other"


@dataclass
class TradeRecord:
    """Detailed trade record"""
    trade_id: str
    ticker: str

    # Trade details
    entry_date: datetime
    entry_price: float
    quantity: int
    position_value: float

    # Exit details
    exit_date: Optional[datetime] = None
    exit_price: Optional[float] = None

    # Risk/Reward
    stop_loss: float = 0.0
    target_price: float = 0.0
    risk_amount: float = 0.0
    reward_amount: float = 0.0
    risk_reward_ratio: float = 0.0

    # Performance
    pnl: float = 0.0
    pnl_percent: float = 0.0
    r_multiple: float = 0.0  # Profit/Loss in terms of initial risk
    outcome: TradeOutcome = TradeOutcome.OPEN

    # Context
    signal_type: Optional[str] = None
    pattern_type: Optional[str] = None
    setup_quality: float = 0.0  # 0-100
    sector: Optional[str] = None
    industry: Optional[str] = None

    # Learning
    notes: str = ""
    mistakes: List[str] = field(default_factory=list)
    lessons_learned: List[str] = field(default_factory=list)

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.position_value = self.quantity * self.entry_price
        self.risk_amount = self.quantity * (self.entry_price - self.stop_loss)
        self.reward_amount = self.quantity * (self.target_price - self.entry_price)
        if self.risk_amount > 0:
            self.risk_reward_ratio = self.reward_amount / self.risk_amount

    def close_trade(self, exit_price: float, exit_date: Optional[datetime] = None) -> None:
        """Close the trade and calculate metrics"""
        self.exit_price = exit_price
        self.exit_date = exit_date or datetime.now()

        # Calculate P&L
        self.pnl = self.quantity * (exit_price - self.entry_price)
        self.pnl_percent = ((exit_price / self.entry_price) - 1) * 100

        # Calculate R-multiple
        if self.risk_amount > 0:
            self.r_multiple = self.pnl / self.risk_amount

        # Determine outcome
        if self.pnl > 0:
            self.outcome = TradeOutcome.WIN
        elif self.pnl < 0:
            self.outcome = TradeOutcome.LOSS
        else:
            self.outcome = TradeOutcome.BREAKEVEN

    @property
    def days_held(self) -> int:
        """Calculate days held"""
        if not self.exit_date:
            return (datetime.now() - self.entry_date).days
        return (self.exit_date - self.entry_date).days

    @property
    def is_winner(self) -> bool:
        """Check if trade is a winner"""
        return self.outcome == TradeOutcome.WIN


@dataclass
class PerformanceMetrics:
    """Comprehensive performance metrics"""
    # Overview
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    breakeven_trades: int = 0
    open_trades: int = 0

    # Win rate
    win_rate: float = 0.0
    loss_rate: float = 0.0

    # P&L
    total_pnl: float = 0.0
    total_pnl_percent: float = 0.0
    average_win: float = 0.0
    average_loss: float = 0.0
    largest_win: float = 0.0
    largest_loss: float = 0.0

    # Risk metrics
    average_r_multiple: float = 0.0
    expectancy: float = 0.0  # Average $ per trade
    profit_factor: float = 0.0  # Gross profit / Gross loss

    # Efficiency
    average_days_held: float = 0.0
    best_day_return: float = 0.0
    worst_day_return: float = 0.0

    # Streaks
    current_streak: int = 0
    longest_win_streak: int = 0
    longest_loss_streak: int = 0

    # By category
    by_signal_type: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    by_sector: Dict[str, Dict[str, Any]] = field(default_factory=dict)


@dataclass
class PerformanceReport:
    """Full performance report"""
    period_start: datetime
    period_end: datetime
    metrics: PerformanceMetrics
    recent_trades: List[TradeRecord]
    top_performers: List[TradeRecord]
    worst_performers: List[TradeRecord]
    common_mistakes: Dict[str, int]
    recommendations: List[str]
    generated_at: datetime = field(default_factory=datetime.now)


class PerformanceTracker:
    """
    Track and analyze trading performance
    """

    def __init__(self):
        self.trades: Dict[str, TradeRecord] = {}
        self.closed_trades: List[TradeRecord] = []
        self.open_trades: Dict[str, TradeRecord] = {}
        self.logger = logging.getLogger(__name__)

    def add_trade(self, trade: TradeRecord) -> None:
        """Add a new trade"""
        self.trades[trade.trade_id] = trade
        self.open_trades[trade.trade_id] = trade
        self.logger.info(
            f"Added trade {trade.trade_id}: {trade.ticker} @ ${trade.entry_price:.2f}"
        )

    def close_trade(
        self,
        trade_id: str,
        exit_price: float,
        exit_date: Optional[datetime] = None,
        notes: Optional[str] = None,
        mistakes: Optional[List[str]] = None,
        lessons: Optional[List[str]] = None
    ) -> Optional[TradeRecord]:
        """Close a trade and record results"""
        if trade_id not in self.open_trades:
            self.logger.error(f"Trade {trade_id} not found in open trades")
            return None

        trade = self.open_trades[trade_id]
        trade.close_trade(exit_price, exit_date)

        if notes:
            trade.notes = notes
        if mistakes:
            trade.mistakes.extend(mistakes)
        if lessons:
            trade.lessons_learned.extend(lessons)

        # Move to closed trades
        self.closed_trades.append(trade)
        del self.open_trades[trade_id]

        self.logger.info(
            f"Closed trade {trade_id}: {trade.outcome.value} "
            f"P&L=${trade.pnl:.2f} ({trade.pnl_percent:+.2f}%) R={trade.r_multiple:.2f}"
        )

        return trade

    def calculate_metrics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> PerformanceMetrics:
        """
        Calculate performance metrics

        Args:
            start_date: Start date for filtering (optional)
            end_date: End date for filtering (optional)

        Returns:
            PerformanceMetrics object
        """
        # Filter trades by date
        trades = self.closed_trades
        if start_date:
            trades = [t for t in trades if t.entry_date >= start_date]
        if end_date:
            trades = [t for t in trades if t.entry_date <= end_date]

        if not trades:
            return PerformanceMetrics()

        # Count outcomes
        winners = [t for t in trades if t.outcome == TradeOutcome.WIN]
        losers = [t for t in trades if t.outcome == TradeOutcome.LOSS]
        breakeven = [t for t in trades if t.outcome == TradeOutcome.BREAKEVEN]

        total_trades = len(trades)
        winning_trades = len(winners)
        losing_trades = len(losers)

        # Calculate win rate
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0.0
        loss_rate = (losing_trades / total_trades * 100) if total_trades > 0 else 0.0

        # Calculate P&L metrics
        total_pnl = sum(t.pnl for t in trades)
        average_win = sum(t.pnl for t in winners) / len(winners) if winners else 0.0
        average_loss = sum(t.pnl for t in losers) / len(losers) if losers else 0.0
        largest_win = max((t.pnl for t in winners), default=0.0)
        largest_loss = min((t.pnl for t in losers), default=0.0)

        # Calculate risk metrics
        average_r = sum(t.r_multiple for t in trades) / len(trades) if trades else 0.0
        expectancy = total_pnl / total_trades if total_trades > 0 else 0.0

        gross_profit = sum(t.pnl for t in winners)
        gross_loss = abs(sum(t.pnl for t in losers))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0.0

        # Calculate days held
        avg_days = sum(t.days_held for t in trades) / len(trades) if trades else 0.0

        # Calculate streaks
        current_streak = self._calculate_current_streak()
        longest_win, longest_loss = self._calculate_longest_streaks(trades)

        # By category analysis
        by_signal = self._analyze_by_category(trades, lambda t: t.signal_type)
        by_sector = self._analyze_by_category(trades, lambda t: t.sector)

        metrics = PerformanceMetrics(
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            breakeven_trades=len(breakeven),
            open_trades=len(self.open_trades),
            win_rate=win_rate,
            loss_rate=loss_rate,
            total_pnl=total_pnl,
            average_win=average_win,
            average_loss=average_loss,
            largest_win=largest_win,
            largest_loss=largest_loss,
            average_r_multiple=average_r,
            expectancy=expectancy,
            profit_factor=profit_factor,
            average_days_held=avg_days,
            current_streak=current_streak,
            longest_win_streak=longest_win,
            longest_loss_streak=longest_loss,
            by_signal_type=by_signal,
            by_sector=by_sector
        )

        self.logger.info(
            f"Calculated metrics: {total_trades} trades, "
            f"{win_rate:.1f}% win rate, ${total_pnl:,.2f} P&L"
        )

        return metrics

    def generate_report(
        self,
        days: int = 30,
        top_n: int = 5
    ) -> PerformanceReport:
        """
        Generate comprehensive performance report

        Args:
            days: Number of days to include
            top_n: Number of top/worst trades to include

        Returns:
            PerformanceReport object
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Calculate metrics
        metrics = self.calculate_metrics(start_date, end_date)

        # Get recent trades
        recent = sorted(
            [t for t in self.closed_trades if t.entry_date >= start_date],
            key=lambda t: t.entry_date,
            reverse=True
        )[:10]

        # Get top performers
        all_closed = [t for t in self.closed_trades if t.entry_date >= start_date]
        top_performers = sorted(
            all_closed,
            key=lambda t: t.pnl,
            reverse=True
        )[:top_n]

        # Get worst performers
        worst_performers = sorted(
            all_closed,
            key=lambda t: t.pnl
        )[:top_n]

        # Analyze mistakes
        common_mistakes = {}
        for trade in all_closed:
            for mistake in trade.mistakes:
                common_mistakes[mistake] = common_mistakes.get(mistake, 0) + 1

        # Generate recommendations
        recommendations = self._generate_recommendations(metrics, common_mistakes)

        report = PerformanceReport(
            period_start=start_date,
            period_end=end_date,
            metrics=metrics,
            recent_trades=recent,
            top_performers=top_performers,
            worst_performers=worst_performers,
            common_mistakes=common_mistakes,
            recommendations=recommendations
        )

        self.logger.info(f"Generated performance report for {days} days")
        return report

    def add_mistake(
        self,
        trade_id: str,
        mistake_category: MistakeCategory,
        description: str
    ) -> bool:
        """Record a trading mistake"""
        if trade_id not in self.trades:
            return False

        trade = self.trades[trade_id]
        mistake_text = f"{mistake_category.value}: {description}"
        trade.mistakes.append(mistake_text)

        self.logger.info(f"Recorded mistake for trade {trade_id}: {mistake_text}")
        return True

    def add_lesson(self, trade_id: str, lesson: str) -> bool:
        """Record a lesson learned"""
        if trade_id not in self.trades:
            return False

        trade = self.trades[trade_id]
        trade.lessons_learned.append(lesson)

        self.logger.info(f"Recorded lesson for trade {trade_id}: {lesson}")
        return True

    def get_trade(self, trade_id: str) -> Optional[TradeRecord]:
        """Get trade by ID"""
        return self.trades.get(trade_id)

    def get_open_trades(self) -> List[TradeRecord]:
        """Get all open trades"""
        return list(self.open_trades.values())

    def get_closed_trades(
        self,
        limit: Optional[int] = None
    ) -> List[TradeRecord]:
        """Get closed trades, optionally limited"""
        trades = sorted(self.closed_trades, key=lambda t: t.exit_date, reverse=True)
        return trades[:limit] if limit else trades

    def _calculate_current_streak(self) -> int:
        """Calculate current win/loss streak"""
        if not self.closed_trades:
            return 0

        sorted_trades = sorted(self.closed_trades, key=lambda t: t.exit_date or t.entry_date)

        if not sorted_trades:
            return 0

        last_outcome = sorted_trades[-1].outcome
        streak = 0

        for trade in reversed(sorted_trades):
            if trade.outcome == last_outcome:
                streak += 1
            else:
                break

        # Negative for loss streak
        if last_outcome == TradeOutcome.LOSS:
            streak = -streak

        return streak

    def _calculate_longest_streaks(
        self,
        trades: List[TradeRecord]
    ) -> tuple[int, int]:
        """Calculate longest win and loss streaks"""
        if not trades:
            return 0, 0

        sorted_trades = sorted(trades, key=lambda t: t.exit_date or t.entry_date)

        longest_win = 0
        longest_loss = 0
        current_win = 0
        current_loss = 0

        for trade in sorted_trades:
            if trade.outcome == TradeOutcome.WIN:
                current_win += 1
                current_loss = 0
                longest_win = max(longest_win, current_win)
            elif trade.outcome == TradeOutcome.LOSS:
                current_loss += 1
                current_win = 0
                longest_loss = max(longest_loss, current_loss)

        return longest_win, longest_loss

    def _analyze_by_category(
        self,
        trades: List[TradeRecord],
        key_func
    ) -> Dict[str, Dict[str, Any]]:
        """Analyze trades by category"""
        categories = {}

        for trade in trades:
            category = key_func(trade)
            if not category:
                continue

            if category not in categories:
                categories[category] = {
                    "count": 0,
                    "wins": 0,
                    "losses": 0,
                    "total_pnl": 0.0,
                    "win_rate": 0.0
                }

            cat = categories[category]
            cat["count"] += 1
            cat["total_pnl"] += trade.pnl

            if trade.outcome == TradeOutcome.WIN:
                cat["wins"] += 1
            elif trade.outcome == TradeOutcome.LOSS:
                cat["losses"] += 1

        # Calculate win rates
        for category in categories.values():
            if category["count"] > 0:
                category["win_rate"] = (category["wins"] / category["count"]) * 100

        return categories

    def _generate_recommendations(
        self,
        metrics: PerformanceMetrics,
        mistakes: Dict[str, int]
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Win rate recommendations
        if metrics.win_rate < 50:
            recommendations.append(
                "Win rate below 50% - Focus on higher quality setups and better entry timing"
            )

        # Profit factor recommendations
        if metrics.profit_factor < 1.5:
            recommendations.append(
                "Profit factor below 1.5 - Consider letting winners run longer or cutting losses faster"
            )

        # Average R-multiple recommendations
        if metrics.average_r_multiple < 1.0:
            recommendations.append(
                "Average R-multiple below 1.0 - You're losing more than you risk on average. "
                "Review your exit strategy"
            )

        # Loss streak recommendations
        if metrics.current_streak < -3:
            recommendations.append(
                f"On a {abs(metrics.current_streak)}-trade losing streak - "
                "Consider reducing position size or taking a break"
            )

        # Mistake-based recommendations
        if mistakes:
            top_mistake = max(mistakes.items(), key=lambda x: x[1])
            recommendations.append(
                f"Most common mistake: {top_mistake[0]} ({top_mistake[1]} times) - "
                "Create a rule to prevent this"
            )

        # Positive reinforcement
        if metrics.win_rate >= 60 and metrics.profit_factor >= 2.0:
            recommendations.append(
                "Excellent performance! Continue following your trading plan"
            )

        return recommendations

    def export_to_json(self, filepath: str) -> bool:
        """Export all trades to JSON file"""
        try:
            data = {
                "trades": [
                    {
                        "trade_id": t.trade_id,
                        "ticker": t.ticker,
                        "entry_date": t.entry_date.isoformat(),
                        "entry_price": t.entry_price,
                        "exit_date": t.exit_date.isoformat() if t.exit_date else None,
                        "exit_price": t.exit_price,
                        "quantity": t.quantity,
                        "pnl": t.pnl,
                        "pnl_percent": t.pnl_percent,
                        "r_multiple": t.r_multiple,
                        "outcome": t.outcome.value,
                        "notes": t.notes,
                        "mistakes": t.mistakes,
                        "lessons_learned": t.lessons_learned
                    }
                    for t in self.closed_trades
                ],
                "exported_at": datetime.now().isoformat()
            }

            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)

            self.logger.info(f"Exported {len(self.closed_trades)} trades to {filepath}")
            return True

        except Exception as e:
            self.logger.error(f"Error exporting trades: {e}", exc_info=True)
            return False
