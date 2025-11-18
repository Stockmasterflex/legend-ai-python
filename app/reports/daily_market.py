"""
Daily Market Report Generator

Generates comprehensive daily market reports including:
- Market summary
- Top movers
- New patterns detected
- Sector performance
- Key levels to watch
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from decimal import Decimal

from pydantic import BaseModel
from reportlab.platypus import Paragraph, Spacer, Table, KeepTogether
from reportlab.lib.units import inch
from reportlab.lib import colors

from .base import BaseReport, ReportConfig, ReportSection
from ..models import PatternScan, Ticker
from sqlalchemy.orm import Session
from sqlalchemy import desc, func


class MarketSummaryData(BaseModel):
    """Market summary statistics"""
    date: datetime
    total_scanned: int
    patterns_found: int
    breakouts: int
    setups: int
    avg_rs_rating: float
    market_breadth: Dict[str, int]  # advancing, declining, unchanged
    volume_analysis: Dict[str, Any]


class TopMoverData(BaseModel):
    """Top mover stock data"""
    symbol: str
    name: str
    price_change_pct: float
    volume_ratio: float
    rs_rating: Optional[float] = None
    sector: Optional[str] = None
    pattern: Optional[str] = None


class SectorPerformanceData(BaseModel):
    """Sector performance data"""
    sector: str
    avg_change_pct: float
    num_stocks: int
    leaders: List[str]
    laggards: List[str]


class KeyLevelData(BaseModel):
    """Key support/resistance levels"""
    symbol: str
    current_price: float
    support_levels: List[float]
    resistance_levels: List[float]
    trend: str  # up, down, sideways


class DailyMarketReport(BaseReport):
    """Generates daily market reports"""

    def __init__(
        self,
        config: ReportConfig,
        db: Optional[Session] = None,
        date: Optional[datetime] = None
    ):
        super().__init__(config)
        self.db = db
        self.report_date = date or datetime.now()
        self.data: Dict[str, Any] = {}

    async def fetch_data(self):
        """Fetch all data needed for the report"""
        if not self.db:
            return

        # Get recent pattern scans
        scans = (
            self.db.query(PatternScan)
            .filter(PatternScan.created_at >= self.report_date - timedelta(days=1))
            .order_by(desc(PatternScan.score))
            .all()
        )

        self.data['scans'] = scans

        # Get top movers
        self.data['top_movers'] = self._get_top_movers(scans)

        # Get sector performance
        self.data['sector_performance'] = self._get_sector_performance(scans)

        # Get new patterns
        self.data['new_patterns'] = self._get_new_patterns(scans)

        # Get key levels
        self.data['key_levels'] = self._get_key_levels(scans)

        # Calculate market summary
        self.data['summary'] = self._calculate_summary(scans)

    def _get_top_movers(self, scans: List[PatternScan], limit: int = 10) -> List[TopMoverData]:
        """Get top performing stocks"""
        movers = []

        for scan in scans[:limit]:
            if scan.ticker:
                mover = TopMoverData(
                    symbol=scan.ticker.symbol,
                    name=scan.ticker.name or scan.ticker.symbol,
                    price_change_pct=float(scan.score),  # Using score as proxy
                    volume_ratio=2.5,  # Placeholder
                    rs_rating=scan.rs_rating,
                    sector=scan.ticker.sector,
                    pattern=scan.pattern_type,
                )
                movers.append(mover)

        return movers

    def _get_sector_performance(self, scans: List[PatternScan]) -> List[SectorPerformanceData]:
        """Calculate sector performance"""
        sector_data = {}

        for scan in scans:
            if scan.ticker and scan.ticker.sector:
                sector = scan.ticker.sector
                if sector not in sector_data:
                    sector_data[sector] = {
                        'stocks': [],
                        'scores': [],
                    }
                sector_data[sector]['stocks'].append(scan.ticker.symbol)
                sector_data[sector]['scores'].append(float(scan.score))

        sectors = []
        for sector, data in sector_data.items():
            avg_change = sum(data['scores']) / len(data['scores']) if data['scores'] else 0
            sorted_stocks = sorted(
                zip(data['stocks'], data['scores']),
                key=lambda x: x[1],
                reverse=True
            )

            sectors.append(SectorPerformanceData(
                sector=sector,
                avg_change_pct=avg_change,
                num_stocks=len(data['stocks']),
                leaders=[s[0] for s in sorted_stocks[:3]],
                laggards=[s[0] for s in sorted_stocks[-3:]],
            ))

        return sorted(sectors, key=lambda x: x.avg_change_pct, reverse=True)

    def _get_new_patterns(self, scans: List[PatternScan]) -> List[PatternScan]:
        """Get newly detected patterns"""
        # Filter for high-quality patterns
        return [
            scan for scan in scans
            if scan.score >= 7.0 and scan.pattern_type
        ][:15]

    def _get_key_levels(self, scans: List[PatternScan]) -> List[KeyLevelData]:
        """Get key support/resistance levels"""
        levels = []

        for scan in scans[:10]:
            if scan.entry_price and scan.stop_loss:
                levels.append(KeyLevelData(
                    symbol=scan.ticker.symbol if scan.ticker else scan.symbol,
                    current_price=float(scan.entry_price),
                    support_levels=[float(scan.stop_loss)],
                    resistance_levels=[float(scan.target_price)] if scan.target_price else [],
                    trend="up" if scan.score > 7 else "sideways",
                ))

        return levels

    def _calculate_summary(self, scans: List[PatternScan]) -> MarketSummaryData:
        """Calculate market summary statistics"""
        total_scanned = len(set(scan.symbol for scan in scans))
        patterns_found = len(scans)
        breakouts = len([s for s in scans if s.score >= 8.0])
        setups = len([s for s in scans if 6.0 <= s.score < 8.0])

        rs_ratings = [s.rs_rating for s in scans if s.rs_rating]
        avg_rs = sum(rs_ratings) / len(rs_ratings) if rs_ratings else 0

        return MarketSummaryData(
            date=self.report_date,
            total_scanned=total_scanned,
            patterns_found=patterns_found,
            breakouts=breakouts,
            setups=setups,
            avg_rs_rating=avg_rs,
            market_breadth={
                'advancing': breakouts,
                'declining': 0,
                'unchanged': total_scanned - breakouts - setups,
            },
            volume_analysis={
                'above_average': len([s for s in scans if s.volume_score and s.volume_score > 1.5]),
                'below_average': len([s for s in scans if s.volume_score and s.volume_score < 1.0]),
            },
        )

    def build(self):
        """Build the daily market report"""
        # Market Summary Section
        self._add_market_summary()

        # Top Movers Section
        self._add_top_movers()

        # New Patterns Section
        self._add_new_patterns()

        # Sector Performance Section
        self._add_sector_performance()

        # Key Levels Section
        self._add_key_levels()

    def _add_market_summary(self):
        """Add market summary section"""
        summary = self.data.get('summary')
        if not summary:
            return

        content = []

        # Summary metrics table
        data = [
            ['Metric', 'Value'],
            ['Total Stocks Scanned', f"{summary.total_scanned:,}"],
            ['Patterns Found', f"{summary.patterns_found:,}"],
            ['Breakout Candidates', f"{summary.breakouts:,}"],
            ['Setup Candidates', f"{summary.setups:,}"],
            ['Avg RS Rating', f"{summary.avg_rs_rating:.1f}"],
        ]

        table = self._create_table(data)
        content.append(table)
        content.append(Spacer(1, 0.2*inch))

        # Market breadth
        breadth_text = (
            f"<b>Market Breadth:</b> {summary.market_breadth['advancing']} advancing, "
            f"{summary.market_breadth['declining']} declining, "
            f"{summary.market_breadth['unchanged']} unchanged"
        )
        content.append(Paragraph(breadth_text, self.styles['Body']))

        # Volume analysis
        vol_analysis = summary.volume_analysis
        vol_text = (
            f"<b>Volume Analysis:</b> {vol_analysis['above_average']} stocks with "
            f"above-average volume, {vol_analysis['below_average']} below average"
        )
        content.append(Paragraph(vol_text, self.styles['Body']))

        section = ReportSection(
            title="Market Summary",
            content=content,
            order=1,
        )
        self.add_section(section)

    def _add_top_movers(self):
        """Add top movers section"""
        movers = self.data.get('top_movers', [])
        if not movers:
            return

        content = []

        # Create table
        data = [['Symbol', 'Name', 'Change %', 'RS Rating', 'Sector', 'Pattern']]

        for mover in movers:
            data.append([
                mover.symbol,
                mover.name[:30],  # Truncate long names
                f"{mover.price_change_pct:+.2f}%",
                f"{mover.rs_rating:.0f}" if mover.rs_rating else "N/A",
                mover.sector[:20] if mover.sector else "N/A",
                mover.pattern or "N/A",
            ])

        col_widths = [0.8*inch, 1.8*inch, 0.9*inch, 0.9*inch, 1.3*inch, 1.3*inch]
        table = self._create_table(data, col_widths=col_widths)
        content.append(table)

        section = ReportSection(
            title="Top Movers",
            content=content,
            order=2,
        )
        self.add_section(section)

    def _add_new_patterns(self):
        """Add newly detected patterns section"""
        patterns = self.data.get('new_patterns', [])
        if not patterns:
            return

        content = []

        # Create table
        data = [['Symbol', 'Pattern', 'Score', 'Entry', 'Target', 'Stop', 'R/R']]

        for pattern in patterns:
            rr_ratio = "N/A"
            if pattern.risk_reward_ratio:
                rr_ratio = f"{pattern.risk_reward_ratio:.2f}"

            data.append([
                pattern.symbol,
                pattern.pattern_type or "N/A",
                f"{pattern.score:.1f}",
                f"${pattern.entry_price:.2f}" if pattern.entry_price else "N/A",
                f"${pattern.target_price:.2f}" if pattern.target_price else "N/A",
                f"${pattern.stop_loss:.2f}" if pattern.stop_loss else "N/A",
                rr_ratio,
            ])

        col_widths = [0.8*inch, 1.2*inch, 0.7*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.7*inch]
        table = self._create_table(data, col_widths=col_widths)
        content.append(table)

        section = ReportSection(
            title="New Patterns Detected",
            content=content,
            order=3,
        )
        self.add_section(section)

    def _add_sector_performance(self):
        """Add sector performance section"""
        sectors = self.data.get('sector_performance', [])
        if not sectors:
            return

        content = []

        # Create table
        data = [['Sector', 'Avg Change %', '# Stocks', 'Leaders', 'Laggards']]

        for sector in sectors:
            data.append([
                sector.sector[:25],
                f"{sector.avg_change_pct:+.2f}%",
                str(sector.num_stocks),
                ", ".join(sector.leaders),
                ", ".join(sector.laggards),
            ])

        col_widths = [1.5*inch, 1.0*inch, 0.8*inch, 1.8*inch, 1.8*inch]
        table = self._create_table(data, col_widths=col_widths)
        content.append(table)

        section = ReportSection(
            title="Sector Performance",
            content=content,
            order=4,
        )
        self.add_section(section)

    def _add_key_levels(self):
        """Add key levels to watch section"""
        levels = self.data.get('key_levels', [])
        if not levels:
            return

        content = []

        # Create table
        data = [['Symbol', 'Current Price', 'Support', 'Resistance', 'Trend']]

        for level in levels:
            support = ", ".join([f"${s:.2f}" for s in level.support_levels])
            resistance = ", ".join([f"${r:.2f}" for r in level.resistance_levels])

            data.append([
                level.symbol,
                f"${level.current_price:.2f}",
                support,
                resistance,
                level.trend.upper(),
            ])

        col_widths = [0.8*inch, 1.2*inch, 1.5*inch, 1.5*inch, 0.9*inch]
        table = self._create_table(data, col_widths=col_widths)
        content.append(table)

        section = ReportSection(
            title="Key Levels to Watch",
            content=content,
            order=5,
        )
        self.add_section(section)
