"""
Trade Reporting Service
Generate PDF reports, tax documents, and performance letters
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
import json
import csv
from io import StringIO, BytesIO

from app.models import TradeJournal, Ticker, TradeStatus
from app.services.trade_journal import TradeJournalService

logger = logging.getLogger(__name__)


class TradeReportingService:
    """Service for generating trade reports and exports"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.journal_service = TradeJournalService(db)

    # ==================== CSV EXPORTS ====================

    async def export_trades_csv(
        self,
        user_id: str = "default",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> str:
        """Export trades to CSV format"""

        trades = await self.journal_service.get_trades(
            user_id=user_id,
            status=TradeStatus.CLOSED,
            start_date=start_date,
            end_date=end_date,
            limit=10000
        )

        # Create CSV in memory
        output = StringIO()
        writer = csv.writer(output)

        # Headers
        writer.writerow([
            'Trade ID', 'Date Opened', 'Date Closed', 'Ticker', 'Pattern',
            'Entry Price', 'Exit Price', 'Position Size',
            'Gross P&L', 'Net P&L', 'R-Multiple', 'Fees',
            'Holding Hours', 'Win/Loss', 'Exit Reason',
            'Emotional State Entry', 'Emotional State Exit',
            'What Went Well', 'What Went Wrong', 'Lessons Learned'
        ])

        # Data rows
        for trade in trades:
            # Get ticker symbol
            ticker = await self.db.get(Ticker, trade.ticker_id)
            ticker_symbol = ticker.symbol if ticker else "UNKNOWN"

            writer.writerow([
                trade.trade_id,
                trade.entry_timestamp.strftime('%Y-%m-%d %H:%M:%S') if trade.entry_timestamp else '',
                trade.exit_timestamp.strftime('%Y-%m-%d %H:%M:%S') if trade.exit_timestamp else '',
                ticker_symbol,
                trade.pattern_identified,
                trade.actual_entry_price or trade.planned_entry,
                trade.exit_price,
                trade.actual_position_size or trade.planned_position_size,
                trade.gross_pnl or 0,
                trade.net_pnl or 0,
                trade.r_multiple or 0,
                trade.fees_paid or 0,
                trade.holding_period_hours or 0,
                'Win' if trade.net_pnl and trade.net_pnl > 0 else 'Loss',
                trade.exit_reason or '',
                trade.emotional_state_entry.value if trade.emotional_state_entry else '',
                trade.emotional_state_exit.value if trade.emotional_state_exit else '',
                trade.what_went_well or '',
                trade.what_went_wrong or '',
                trade.lessons_learned or ''
            ])

        csv_content = output.getvalue()
        output.close()

        return csv_content

    async def export_tax_report_csv(
        self,
        user_id: str = "default",
        year: int = None
    ) -> str:
        """
        Export trades for tax reporting (IRS Form 8949 compatible)
        """

        if year is None:
            year = datetime.now().year

        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31, 23, 59, 59)

        trades = await self.journal_service.get_trades(
            user_id=user_id,
            status=TradeStatus.CLOSED,
            start_date=start_date,
            end_date=end_date,
            limit=10000
        )

        # Create CSV for tax reporting
        output = StringIO()
        writer = csv.writer(output)

        # Headers (Form 8949 compatible)
        writer.writerow([
            'Description of Property',
            'Date Acquired',
            'Date Sold',
            'Proceeds',
            'Cost Basis',
            'Gain or Loss',
            'Short-term or Long-term'
        ])

        # Data rows
        for trade in trades:
            ticker = await self.db.get(Ticker, trade.ticker_id)
            ticker_symbol = ticker.symbol if ticker else "UNKNOWN"

            description = f"{trade.actual_position_size or trade.planned_position_size} shares {ticker_symbol}"
            date_acquired = trade.entry_timestamp.strftime('%m/%d/%Y') if trade.entry_timestamp else ''
            date_sold = trade.exit_timestamp.strftime('%m/%d/%Y') if trade.exit_timestamp else ''

            entry_price = trade.actual_entry_price or trade.planned_entry
            position_size = trade.actual_position_size or trade.planned_position_size

            proceeds = trade.exit_price * position_size if trade.exit_price else 0
            cost_basis = entry_price * position_size
            gain_loss = trade.net_pnl or 0

            # Determine short-term vs long-term (365 days)
            holding_days = trade.holding_period_hours / 24 if trade.holding_period_hours else 0
            term = "Long-term" if holding_days > 365 else "Short-term"

            writer.writerow([
                description,
                date_acquired,
                date_sold,
                f"${proceeds:.2f}",
                f"${cost_basis:.2f}",
                f"${gain_loss:.2f}",
                term
            ])

        csv_content = output.getvalue()
        output.close()

        return csv_content

    # ==================== JSON EXPORTS ====================

    async def export_trades_json(
        self,
        user_id: str = "default",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Export trades to JSON format"""

        trades = await self.journal_service.get_trades(
            user_id=user_id,
            status=TradeStatus.CLOSED,
            start_date=start_date,
            end_date=end_date,
            limit=10000
        )

        # Build comprehensive JSON export
        trades_data = []
        for trade in trades:
            ticker = await self.db.get(Ticker, trade.ticker_id)
            ticker_symbol = ticker.symbol if ticker else "UNKNOWN"

            trade_dict = {
                "trade_id": trade.trade_id,
                "ticker": ticker_symbol,
                "pattern": trade.pattern_identified,
                "status": trade.status.value,
                "planning": {
                    "thesis": trade.thesis,
                    "planned_entry": trade.planned_entry,
                    "planned_stop": trade.planned_stop,
                    "planned_target": trade.planned_target,
                    "planned_position_size": trade.planned_position_size,
                    "planned_risk_reward": trade.planned_risk_reward,
                    "checklist_completed": trade.checklist_completed,
                    "checklist_data": trade.checklist_data
                },
                "execution": {
                    "entry_timestamp": trade.entry_timestamp.isoformat() if trade.entry_timestamp else None,
                    "exit_timestamp": trade.exit_timestamp.isoformat() if trade.exit_timestamp else None,
                    "actual_entry_price": trade.actual_entry_price,
                    "actual_exit_price": trade.exit_price,
                    "actual_position_size": trade.actual_position_size,
                    "entry_slippage": trade.entry_slippage,
                    "exit_slippage": trade.exit_slippage,
                    "slippage_cost": trade.slippage_cost
                },
                "performance": {
                    "gross_pnl": trade.gross_pnl,
                    "net_pnl": trade.net_pnl,
                    "r_multiple": trade.r_multiple,
                    "fees_paid": trade.fees_paid,
                    "holding_period_hours": trade.holding_period_hours,
                    "mae": trade.mae,
                    "mfe": trade.mfe
                },
                "psychology": {
                    "emotional_state_entry": trade.emotional_state_entry.value if trade.emotional_state_entry else None,
                    "emotional_state_exit": trade.emotional_state_exit.value if trade.emotional_state_exit else None,
                    "market_condition": trade.market_condition.value if trade.market_condition else None
                },
                "review": {
                    "what_went_well": trade.what_went_well,
                    "what_went_wrong": trade.what_went_wrong,
                    "lessons_learned": trade.lessons_learned,
                    "follow_through_notes": trade.follow_through_notes
                }
            }

            trades_data.append(trade_dict)

        # Add summary statistics
        analytics = await self.journal_service.get_performance_analytics(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )

        export_data = {
            "export_date": datetime.now().isoformat(),
            "user_id": user_id,
            "period": {
                "start": start_date.isoformat() if start_date else None,
                "end": end_date.isoformat() if end_date else None
            },
            "summary": analytics,
            "trades": trades_data
        }

        return export_data

    # ==================== PERFORMANCE REPORTS ====================

    async def generate_performance_letter(
        self,
        user_id: str = "default",
        period: str = "monthly"
    ) -> str:
        """
        Generate a performance letter (text format)

        This is like a fund manager's monthly letter to investors
        """

        # Determine date range
        now = datetime.now()
        if period == "daily":
            start_date = now - timedelta(days=1)
        elif period == "weekly":
            start_date = now - timedelta(weeks=1)
        elif period == "monthly":
            start_date = now - timedelta(days=30)
        elif period == "quarterly":
            start_date = now - timedelta(days=90)
        elif period == "yearly":
            start_date = now - timedelta(days=365)
        else:
            start_date = None

        # Get analytics
        analytics = await self.journal_service.get_performance_analytics(
            user_id=user_id,
            start_date=start_date
        )

        # Get pattern performance
        patterns = await self.journal_service.get_pattern_performance(user_id=user_id)

        # Get mistakes
        mistakes = await self.journal_service.get_mistake_analysis(user_id=user_id)

        # Build letter
        letter = f"""
TRADING PERFORMANCE LETTER
{'=' * 60}

Period: {period.upper()}
Report Date: {now.strftime('%B %d, %Y')}
Trader ID: {user_id}

{'=' * 60}

EXECUTIVE SUMMARY
{'-' * 60}

Total Trades: {analytics.get('total_trades', 0)}
Win Rate: {analytics.get('win_rate', 0):.1f}%
Total P&L: ${analytics.get('total_pnl', 0):,.2f}
Average R-Multiple: {analytics.get('average_r_multiple', 0):.2f}R

Winning Trades: {analytics.get('winning_trades', 0)}
Losing Trades: {analytics.get('losing_trades', 0)}
Average Win: ${analytics.get('average_win', 0):,.2f}
Average Loss: ${analytics.get('average_loss', 0):,.2f}

{'=' * 60}

BEST & WORST TRADES
{'-' * 60}

Best Trade:
  Trade ID: {analytics.get('best_trade', {}).get('trade_id', 'N/A')}
  P&L: ${analytics.get('best_trade', {}).get('pnl', 0):,.2f}
  R-Multiple: {analytics.get('best_trade', {}).get('r_multiple', 0):.2f}R

Worst Trade:
  Trade ID: {analytics.get('worst_trade', {}).get('trade_id', 'N/A')}
  P&L: ${analytics.get('worst_trade', {}).get('pnl', 0):,.2f}
  R-Multiple: {analytics.get('worst_trade', {}).get('r_multiple', 0):.2f}R

{'=' * 60}

PATTERN PERFORMANCE
{'-' * 60}

"""

        for pattern in patterns[:5]:  # Top 5 patterns
            letter += f"""
{pattern['pattern']}:
  Total Trades: {pattern['total_trades']}
  Win Rate: {pattern['win_rate']:.1f}%
  Avg R-Multiple: {pattern['avg_r_multiple']:.2f}R
  Total P&L: ${pattern['total_pnl']:,.2f}
"""

        letter += f"""
{'=' * 60}

MISTAKE ANALYSIS
{'-' * 60}

"""

        for mistake in mistakes[:5]:  # Top 5 mistakes
            letter += f"""
{mistake['category'].upper()} - {mistake['mistake_type']}:
  Occurrences: {mistake['occurrences']}
  Avg Impact: ${mistake['avg_impact']:,.2f}
"""

        letter += f"""
{'=' * 60}

RECOMMENDATIONS
{'-' * 60}

"""

        # Add recommendations based on performance
        win_rate = analytics.get('win_rate', 0)
        avg_r = analytics.get('average_r_multiple', 0)

        if win_rate < 40:
            letter += "⚠️  Win rate below 40% - Review entry criteria\n"
        if avg_r < 1.0:
            letter += "⚠️  Average R-multiple below 1.0 - Focus on risk management\n"
        if win_rate > 60 and avg_r > 1.5:
            letter += "✅  Excellent performance - Continue current strategy\n"

        letter += f"""
{'=' * 60}

End of Report
"""

        return letter

    async def generate_accountability_report(
        self,
        user_id: str = "default"
    ) -> Dict[str, Any]:
        """
        Generate an accountability report with key metrics
        """

        # Last 30 days performance
        start_date = datetime.now() - timedelta(days=30)

        trades = await self.journal_service.get_trades(
            user_id=user_id,
            status=TradeStatus.CLOSED,
            start_date=start_date,
            limit=1000
        )

        # Calculate accountability metrics
        total_trades = len(trades)
        trades_with_plan = sum(1 for t in trades if t.checklist_completed)
        trades_with_review = sum(1 for t in trades if t.what_went_well or t.what_went_wrong)

        # Emotional discipline
        emotional_trades = sum(1 for t in trades if t.emotional_state_entry in ['GREEDY', 'FEARFUL', 'IMPULSIVE'])

        # Slippage tracking
        total_slippage = sum(abs(t.slippage_cost) for t in trades if t.slippage_cost)
        avg_slippage = total_slippage / total_trades if total_trades > 0 else 0

        # Rule following
        trades_hit_stop = sum(1 for t in trades if t.exit_reason == 'stop')
        trades_hit_target = sum(1 for t in trades if t.exit_reason == 'target')
        trades_manual_exit = sum(1 for t in trades if t.exit_reason == 'manual')

        return {
            "period": "Last 30 days",
            "discipline_score": {
                "planning_rate": (trades_with_plan / total_trades * 100) if total_trades > 0 else 0,
                "review_rate": (trades_with_review / total_trades * 100) if total_trades > 0 else 0,
                "emotional_control": ((total_trades - emotional_trades) / total_trades * 100) if total_trades > 0 else 0
            },
            "execution_quality": {
                "total_slippage": round(total_slippage, 2),
                "avg_slippage_per_trade": round(avg_slippage, 2),
                "slippage_as_pct_of_pnl": 0  # Calculate if needed
            },
            "rule_adherence": {
                "stopped_out": trades_hit_stop,
                "hit_target": trades_hit_target,
                "manual_exits": trades_manual_exit,
                "rule_following_rate": ((trades_hit_stop + trades_hit_target) / total_trades * 100) if total_trades > 0 else 0
            },
            "total_trades": total_trades,
            "trades_with_full_documentation": sum(1 for t in trades if t.checklist_completed and t.what_went_well)
        }


def get_reporting_service(db: AsyncSession) -> TradeReportingService:
    """Get reporting service instance"""
    return TradeReportingService(db)
