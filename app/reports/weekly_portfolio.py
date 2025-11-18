"""
Weekly Portfolio Review Report Generator

Generates comprehensive weekly portfolio review reports including:
- Performance summary
- Best/worst trades
- Pattern success rates
- Risk metrics
- Next week outlook
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from decimal import Decimal

from pydantic import BaseModel
from reportlab.platypus import Paragraph, Spacer, Table, KeepTogether, PageBreak
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

from .base import BaseReport, ReportConfig, ReportSection
from ..models import PatternScan
from sqlalchemy.orm import Session
from sqlalchemy import desc, func


class PerformanceSummary(BaseModel):
    """Weekly performance summary"""
    week_start: datetime
    week_end: datetime
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    total_return_pct: float
    avg_return_pct: float
    best_trade_pct: float
    worst_trade_pct: float
    total_patterns_analyzed: int
    sharpe_ratio: Optional[float] = None


class TradeResult(BaseModel):
    """Individual trade result"""
    symbol: str
    entry_date: datetime
    exit_date: Optional[datetime] = None
    entry_price: float
    exit_price: Optional[float] = None
    return_pct: float
    pattern: str
    status: str  # win, loss, open
    holding_days: int


class PatternStats(BaseModel):
    """Pattern success statistics"""
    pattern_type: str
    total_occurrences: int
    successful: int
    failed: int
    success_rate: float
    avg_return: float
    best_return: float
    worst_return: float


class RiskMetrics(BaseModel):
    """Risk metrics for the week"""
    max_drawdown_pct: float
    avg_risk_per_trade: float
    total_risk_exposure: float
    risk_reward_ratio: float
    volatility: float
    var_95: Optional[float] = None  # Value at Risk


class WeeklyPortfolioReport(BaseReport):
    """Generates weekly portfolio review reports"""

    def __init__(
        self,
        config: ReportConfig,
        db: Optional[Session] = None,
        week_end: Optional[datetime] = None
    ):
        super().__init__(config)
        self.db = db
        self.week_end = week_end or datetime.now()
        self.week_start = self.week_end - timedelta(days=7)
        self.data: Dict[str, Any] = {}

    async def fetch_data(self):
        """Fetch all data needed for the weekly report"""
        if not self.db:
            # Use mock data if no database
            self._generate_mock_data()
            return

        # Get pattern scans from the week
        scans = (
            self.db.query(PatternScan)
            .filter(
                PatternScan.created_at >= self.week_start,
                PatternScan.created_at <= self.week_end
            )
            .order_by(desc(PatternScan.score))
            .all()
        )

        self.data['scans'] = scans

        # Calculate performance summary
        self.data['performance'] = self._calculate_performance(scans)

        # Get best/worst trades
        self.data['best_trades'] = self._get_best_trades(scans, limit=5)
        self.data['worst_trades'] = self._get_worst_trades(scans, limit=5)

        # Calculate pattern success rates
        self.data['pattern_stats'] = self._calculate_pattern_stats(scans)

        # Calculate risk metrics
        self.data['risk_metrics'] = self._calculate_risk_metrics(scans)

        # Generate outlook
        self.data['outlook'] = self._generate_outlook(scans)

    def _generate_mock_data(self):
        """Generate mock data for demonstration"""
        import random

        # Mock performance
        self.data['performance'] = PerformanceSummary(
            week_start=self.week_start,
            week_end=self.week_end,
            total_trades=24,
            winning_trades=16,
            losing_trades=8,
            win_rate=66.67,
            total_return_pct=8.5,
            avg_return_pct=0.35,
            best_trade_pct=12.3,
            worst_trade_pct=-3.2,
            total_patterns_analyzed=156,
            sharpe_ratio=1.8,
        )

        # Mock trades
        symbols = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'AMD', 'META', 'NFLX']
        patterns = ['VCP', 'Cup & Handle', 'Flat Base', 'Ascending Triangle']

        self.data['best_trades'] = [
            TradeResult(
                symbol=random.choice(symbols),
                entry_date=self.week_start + timedelta(days=random.randint(0, 5)),
                exit_date=self.week_start + timedelta(days=random.randint(3, 7)),
                entry_price=random.uniform(100, 500),
                exit_price=random.uniform(110, 550),
                return_pct=random.uniform(5, 15),
                pattern=random.choice(patterns),
                status='win',
                holding_days=random.randint(1, 5),
            )
            for _ in range(5)
        ]

        self.data['worst_trades'] = [
            TradeResult(
                symbol=random.choice(symbols),
                entry_date=self.week_start + timedelta(days=random.randint(0, 5)),
                exit_date=self.week_start + timedelta(days=random.randint(3, 7)),
                entry_price=random.uniform(100, 500),
                exit_price=random.uniform(90, 480),
                return_pct=random.uniform(-5, -1),
                pattern=random.choice(patterns),
                status='loss',
                holding_days=random.randint(1, 5),
            )
            for _ in range(5)
        ]

        # Mock pattern stats
        self.data['pattern_stats'] = [
            PatternStats(
                pattern_type=pattern,
                total_occurrences=random.randint(5, 20),
                successful=random.randint(3, 15),
                failed=random.randint(1, 8),
                success_rate=random.uniform(50, 85),
                avg_return=random.uniform(2, 8),
                best_return=random.uniform(10, 20),
                worst_return=random.uniform(-5, -1),
            )
            for pattern in patterns
        ]

        # Mock risk metrics
        self.data['risk_metrics'] = RiskMetrics(
            max_drawdown_pct=5.2,
            avg_risk_per_trade=2.0,
            total_risk_exposure=15.5,
            risk_reward_ratio=3.2,
            volatility=18.5,
            var_95=2.8,
        )

        self.data['outlook'] = {
            'key_opportunities': [
                'Technology sector showing strong momentum',
                'Several VCP patterns forming in growth stocks',
                'Market breadth improving week over week',
            ],
            'risks': [
                'Increased volatility expected next week',
                'Key support levels being tested',
                'Overbought conditions in some leaders',
            ],
            'action_items': [
                'Watch for VCP breakouts in NVDA, AMD',
                'Tighten stops on extended positions',
                'Prepare shopping list for pullbacks',
            ],
        }

    def _calculate_performance(self, scans: List[PatternScan]) -> PerformanceSummary:
        """Calculate weekly performance metrics"""
        # This would integrate with actual trade tracking
        # For now, using pattern scores as proxy

        total_trades = len(scans)
        winning = len([s for s in scans if s.score >= 7.0])
        losing = total_trades - winning

        win_rate = (winning / total_trades * 100) if total_trades > 0 else 0

        return PerformanceSummary(
            week_start=self.week_start,
            week_end=self.week_end,
            total_trades=total_trades,
            winning_trades=winning,
            losing_trades=losing,
            win_rate=win_rate,
            total_return_pct=5.0,  # Placeholder
            avg_return_pct=0.21,  # Placeholder
            best_trade_pct=10.0,  # Placeholder
            worst_trade_pct=-2.5,  # Placeholder
            total_patterns_analyzed=total_trades,
        )

    def _get_best_trades(self, scans: List[PatternScan], limit: int = 5) -> List[TradeResult]:
        """Get best performing trades"""
        top_scans = sorted(scans, key=lambda s: s.score, reverse=True)[:limit]

        trades = []
        for scan in top_scans:
            trade = TradeResult(
                symbol=scan.symbol,
                entry_date=scan.created_at,
                entry_price=float(scan.entry_price) if scan.entry_price else 0,
                return_pct=float(scan.score),  # Using score as proxy
                pattern=scan.pattern_type or "Unknown",
                status='win',
                holding_days=3,  # Placeholder
            )
            trades.append(trade)

        return trades

    def _get_worst_trades(self, scans: List[PatternScan], limit: int = 5) -> List[TradeResult]:
        """Get worst performing trades"""
        bottom_scans = sorted(scans, key=lambda s: s.score)[:limit]

        trades = []
        for scan in bottom_scans:
            trade = TradeResult(
                symbol=scan.symbol,
                entry_date=scan.created_at,
                entry_price=float(scan.entry_price) if scan.entry_price else 0,
                return_pct=-float(scan.score / 2),  # Negative return
                pattern=scan.pattern_type or "Unknown",
                status='loss',
                holding_days=2,  # Placeholder
            )
            trades.append(trade)

        return trades

    def _calculate_pattern_stats(self, scans: List[PatternScan]) -> List[PatternStats]:
        """Calculate success rates by pattern type"""
        pattern_data = {}

        for scan in scans:
            pattern = scan.pattern_type or "Unknown"
            if pattern not in pattern_data:
                pattern_data[pattern] = {
                    'total': 0,
                    'successful': 0,
                    'returns': [],
                }

            pattern_data[pattern]['total'] += 1
            if scan.score >= 7.0:
                pattern_data[pattern]['successful'] += 1
            pattern_data[pattern]['returns'].append(float(scan.score))

        stats = []
        for pattern, data in pattern_data.items():
            total = data['total']
            successful = data['successful']
            failed = total - successful
            success_rate = (successful / total * 100) if total > 0 else 0
            returns = data['returns']

            stats.append(PatternStats(
                pattern_type=pattern,
                total_occurrences=total,
                successful=successful,
                failed=failed,
                success_rate=success_rate,
                avg_return=sum(returns) / len(returns) if returns else 0,
                best_return=max(returns) if returns else 0,
                worst_return=min(returns) if returns else 0,
            ))

        return sorted(stats, key=lambda s: s.success_rate, reverse=True)

    def _calculate_risk_metrics(self, scans: List[PatternScan]) -> RiskMetrics:
        """Calculate risk metrics"""
        if not scans:
            return RiskMetrics(
                max_drawdown_pct=0,
                avg_risk_per_trade=2.0,
                total_risk_exposure=0,
                risk_reward_ratio=0,
                volatility=0,
            )

        # Calculate from scan data
        scores = [float(s.score) for s in scans]
        avg_score = sum(scores) / len(scores)

        rr_ratios = [s.risk_reward_ratio for s in scans if s.risk_reward_ratio]
        avg_rr = sum(rr_ratios) / len(rr_ratios) if rr_ratios else 0

        return RiskMetrics(
            max_drawdown_pct=3.5,  # Placeholder
            avg_risk_per_trade=2.0,
            total_risk_exposure=10.0,
            risk_reward_ratio=avg_rr,
            volatility=15.0,  # Placeholder
            var_95=2.5,
        )

    def _generate_outlook(self, scans: List[PatternScan]) -> Dict[str, List[str]]:
        """Generate next week outlook"""
        high_quality = len([s for s in scans if s.score >= 8.0])

        outlook = {
            'key_opportunities': [],
            'risks': [],
            'action_items': [],
        }

        if high_quality > 10:
            outlook['key_opportunities'].append(
                f'{high_quality} high-quality setups identified'
            )

        return outlook

    def build(self):
        """Build the weekly portfolio report"""
        # Performance Summary Section
        self._add_performance_summary()

        # Best Trades Section
        self._add_best_trades()

        # Worst Trades Section
        self._add_worst_trades()

        # Pattern Success Rates Section
        self._add_pattern_stats()

        # Risk Metrics Section
        self._add_risk_metrics()

        # Next Week Outlook Section
        self._add_outlook()

    def _add_performance_summary(self):
        """Add performance summary section"""
        perf = self.data.get('performance')
        if not perf:
            return

        content = []

        # Title paragraph
        date_range = f"{perf.week_start.strftime('%b %d')} - {perf.week_end.strftime('%b %d, %Y')}"
        content.append(Paragraph(f"<b>Week of {date_range}</b>", self.styles['Body']))
        content.append(Spacer(1, 0.1*inch))

        # Performance metrics table
        data = [
            ['Metric', 'Value'],
            ['Total Trades', str(perf.total_trades)],
            ['Winning Trades', f"{perf.winning_trades} ({perf.win_rate:.1f}%)"],
            ['Losing Trades', f"{perf.losing_trades} ({100-perf.win_rate:.1f}%)"],
            ['Total Return', f"{perf.total_return_pct:+.2f}%"],
            ['Avg Return per Trade', f"{perf.avg_return_pct:+.2f}%"],
            ['Best Trade', f"{perf.best_trade_pct:+.2f}%"],
            ['Worst Trade', f"{perf.worst_trade_pct:.2f}%"],
            ['Patterns Analyzed', str(perf.total_patterns_analyzed)],
        ]

        if perf.sharpe_ratio:
            data.append(['Sharpe Ratio', f"{perf.sharpe_ratio:.2f}"])

        table = self._create_table(data, col_widths=[2.5*inch, 2*inch])
        content.append(table)

        # Performance commentary
        content.append(Spacer(1, 0.15*inch))
        commentary = self._generate_performance_commentary(perf)
        content.append(Paragraph(commentary, self.styles['Body']))

        section = ReportSection(
            title="Performance Summary",
            content=content,
            order=1,
        )
        self.add_section(section)

    def _generate_performance_commentary(self, perf: PerformanceSummary) -> str:
        """Generate performance commentary"""
        if perf.win_rate >= 70:
            quality = "exceptional"
        elif perf.win_rate >= 60:
            quality = "strong"
        elif perf.win_rate >= 50:
            quality = "solid"
        else:
            quality = "challenging"

        return (
            f"This week showed <b>{quality}</b> performance with a win rate of "
            f"{perf.win_rate:.1f}%. The portfolio generated {perf.total_return_pct:+.2f}% "
            f"returns across {perf.total_trades} trades. "
            f"The best trade gained {perf.best_trade_pct:.1f}% while the worst trade "
            f"lost {abs(perf.worst_trade_pct):.1f}%."
        )

    def _add_best_trades(self):
        """Add best trades section"""
        trades = self.data.get('best_trades', [])
        if not trades:
            return

        content = []

        # Create table
        data = [['Symbol', 'Entry Date', 'Entry Price', 'Exit Price', 'Return %', 'Pattern', 'Days']]

        for trade in trades:
            data.append([
                trade.symbol,
                trade.entry_date.strftime('%m/%d'),
                f"${trade.entry_price:.2f}",
                f"${trade.exit_price:.2f}" if trade.exit_price else "Open",
                f"{trade.return_pct:+.2f}%",
                trade.pattern,
                str(trade.holding_days),
            ])

        col_widths = [0.7*inch, 0.9*inch, 1.0*inch, 1.0*inch, 0.9*inch, 1.3*inch, 0.6*inch]
        table = self._create_table(data, col_widths=col_widths)
        content.append(table)

        section = ReportSection(
            title="Best Trades",
            content=content,
            order=2,
        )
        self.add_section(section)

    def _add_worst_trades(self):
        """Add worst trades section"""
        trades = self.data.get('worst_trades', [])
        if not trades:
            return

        content = []

        # Create table
        data = [['Symbol', 'Entry Date', 'Entry Price', 'Exit Price', 'Return %', 'Pattern', 'Days']]

        for trade in trades:
            data.append([
                trade.symbol,
                trade.entry_date.strftime('%m/%d'),
                f"${trade.entry_price:.2f}",
                f"${trade.exit_price:.2f}" if trade.exit_price else "Open",
                f"{trade.return_pct:.2f}%",
                trade.pattern,
                str(trade.holding_days),
            ])

        col_widths = [0.7*inch, 0.9*inch, 1.0*inch, 1.0*inch, 0.9*inch, 1.3*inch, 0.6*inch]
        table = self._create_table(data, col_widths=col_widths)
        content.append(table)

        section = ReportSection(
            title="Worst Trades (Lessons Learned)",
            content=content,
            order=3,
        )
        self.add_section(section)

    def _add_pattern_stats(self):
        """Add pattern success rates section"""
        stats = self.data.get('pattern_stats', [])
        if not stats:
            return

        content = []

        # Create table
        data = [['Pattern', 'Total', 'Success', 'Success %', 'Avg Return', 'Best', 'Worst']]

        for stat in stats:
            data.append([
                stat.pattern_type,
                str(stat.total_occurrences),
                f"{stat.successful}/{stat.total_occurrences}",
                f"{stat.success_rate:.1f}%",
                f"{stat.avg_return:+.2f}%",
                f"{stat.best_return:+.2f}%",
                f"{stat.worst_return:.2f}%",
            ])

        col_widths = [1.3*inch, 0.6*inch, 0.8*inch, 0.9*inch, 1.0*inch, 0.8*inch, 0.8*inch]
        table = self._create_table(data, col_widths=col_widths)
        content.append(table)

        # Add insights
        content.append(Spacer(1, 0.15*inch))
        if stats:
            best_pattern = max(stats, key=lambda s: s.success_rate)
            insight = (
                f"<b>Top Performer:</b> {best_pattern.pattern_type} showed the highest "
                f"success rate at {best_pattern.success_rate:.1f}% with an average return "
                f"of {best_pattern.avg_return:.2f}%."
            )
            content.append(Paragraph(insight, self.styles['Body']))

        section = ReportSection(
            title="Pattern Success Rates",
            content=content,
            order=4,
        )
        self.add_section(section)

    def _add_risk_metrics(self):
        """Add risk metrics section"""
        risk = self.data.get('risk_metrics')
        if not risk:
            return

        content = []

        # Risk metrics table
        data = [
            ['Risk Metric', 'Value'],
            ['Max Drawdown', f"{risk.max_drawdown_pct:.2f}%"],
            ['Avg Risk per Trade', f"{risk.avg_risk_per_trade:.2f}%"],
            ['Total Risk Exposure', f"{risk.total_risk_exposure:.2f}%"],
            ['Risk/Reward Ratio', f"1:{risk.risk_reward_ratio:.2f}"],
            ['Portfolio Volatility', f"{risk.volatility:.2f}%"],
        ]

        if risk.var_95:
            data.append(['VaR (95%)', f"{risk.var_95:.2f}%"])

        table = self._create_table(data, col_widths=[2.5*inch, 2*inch])
        content.append(table)

        # Risk assessment
        content.append(Spacer(1, 0.15*inch))
        assessment = self._generate_risk_assessment(risk)
        content.append(Paragraph(assessment, self.styles['Body']))

        section = ReportSection(
            title="Risk Metrics",
            content=content,
            order=5,
        )
        self.add_section(section)

    def _generate_risk_assessment(self, risk: RiskMetrics) -> str:
        """Generate risk assessment commentary"""
        if risk.max_drawdown_pct < 5:
            risk_level = "low"
        elif risk.max_drawdown_pct < 10:
            risk_level = "moderate"
        else:
            risk_level = "elevated"

        return (
            f"The portfolio maintained a <b>{risk_level}</b> risk profile this week "
            f"with a maximum drawdown of {risk.max_drawdown_pct:.2f}%. "
            f"The average risk/reward ratio of 1:{risk.risk_reward_ratio:.2f} "
            f"demonstrates {'strong' if risk.risk_reward_ratio >= 3 else 'adequate'} "
            f"risk management discipline."
        )

    def _add_outlook(self):
        """Add next week outlook section"""
        outlook = self.data.get('outlook')
        if not outlook:
            return

        content = []

        # Key Opportunities
        content.append(Paragraph("<b>Key Opportunities:</b>", self.styles['Heading2']))
        for opp in outlook.get('key_opportunities', []):
            content.append(Paragraph(f"• {opp}", self.styles['BodyLeft']))
        content.append(Spacer(1, 0.1*inch))

        # Risks to Monitor
        if outlook.get('risks'):
            content.append(Paragraph("<b>Risks to Monitor:</b>", self.styles['Heading2']))
            for risk in outlook['risks']:
                content.append(Paragraph(f"• {risk}", self.styles['BodyLeft']))
            content.append(Spacer(1, 0.1*inch))

        # Action Items
        if outlook.get('action_items'):
            content.append(Paragraph("<b>Action Items:</b>", self.styles['Heading2']))
            for item in outlook['action_items']:
                content.append(Paragraph(f"• {item}", self.styles['BodyLeft']))

        section = ReportSection(
            title="Next Week Outlook",
            content=content,
            order=6,
        )
        self.add_section(section)
