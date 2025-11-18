"""
Custom Report Builder

Allows users to create custom reports with:
- Drag-and-drop sections
- Choose metrics
- Add custom notes
- Brand with logo
- Template library
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from enum import Enum

from pydantic import BaseModel, Field
from reportlab.platypus import Paragraph, Spacer, Table, KeepTogether, PageBreak, Image as RLImage
from reportlab.lib.units import inch
from reportlab.lib import colors

from .base import BaseReport, ReportConfig, ReportSection


class SectionType(str, Enum):
    """Available section types"""
    TEXT = "text"
    TABLE = "table"
    CHART = "chart"
    METRICS = "metrics"
    WATCHLIST = "watchlist"
    PATTERNS = "patterns"
    PERFORMANCE = "performance"
    RISK_METRICS = "risk_metrics"
    CUSTOM_NOTES = "custom_notes"
    IMAGE = "image"
    DIVIDER = "divider"


class MetricType(str, Enum):
    """Available metric types"""
    WIN_RATE = "win_rate"
    TOTAL_RETURN = "total_return"
    AVG_RETURN = "avg_return"
    SHARPE_RATIO = "sharpe_ratio"
    MAX_DRAWDOWN = "max_drawdown"
    PATTERN_COUNT = "pattern_count"
    TRADE_COUNT = "trade_count"
    RS_RATING_AVG = "rs_rating_avg"
    RISK_REWARD_RATIO = "risk_reward_ratio"


class CustomSection(BaseModel):
    """Custom report section configuration"""
    section_type: SectionType
    title: str
    order: int = 0
    config: Dict[str, Any] = Field(default_factory=dict)
    data: Optional[Dict[str, Any]] = None
    page_break_before: bool = False
    page_break_after: bool = False


class ReportTemplate(BaseModel):
    """Saved report template"""
    template_id: str
    name: str
    description: str
    sections: List[CustomSection]
    default_config: ReportConfig
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    tags: List[str] = Field(default_factory=list)


class CustomReportBuilder(BaseReport):
    """Build custom reports from user-defined sections"""

    def __init__(self, config: ReportConfig):
        super().__init__(config)
        self.custom_sections: List[CustomSection] = []
        self.metrics: Dict[MetricType, Any] = {}
        self.custom_notes: List[str] = []

    def add_custom_section(self, section: CustomSection):
        """Add a custom section to the report"""
        self.custom_sections.append(section)

    def add_metric(self, metric_type: MetricType, value: Any):
        """Add a metric to display"""
        self.metrics[metric_type] = value

    def add_note(self, note: str):
        """Add a custom note"""
        self.custom_notes.append(note)

    def load_template(self, template: ReportTemplate):
        """Load a saved template"""
        self.custom_sections = template.sections
        # Update config with template defaults (but preserve any user overrides)
        if template.default_config:
            for field, value in template.default_config.dict().items():
                if not getattr(self.config, field):
                    setattr(self.config, field, value)

    def save_template(
        self,
        template_id: str,
        name: str,
        description: str,
        tags: Optional[List[str]] = None
    ) -> ReportTemplate:
        """Save current configuration as a template"""
        return ReportTemplate(
            template_id=template_id,
            name=name,
            description=description,
            sections=self.custom_sections,
            default_config=self.config,
            tags=tags or [],
        )

    def build(self):
        """Build the custom report"""
        # Sort sections by order
        sorted_sections = sorted(self.custom_sections, key=lambda s: s.order)

        for custom_section in sorted_sections:
            content = self._build_section_content(custom_section)

            section = ReportSection(
                title=custom_section.title,
                content=content,
                order=custom_section.order,
                page_break_before=custom_section.page_break_before,
                page_break_after=custom_section.page_break_after,
            )
            self.add_section(section)

    def _build_section_content(self, section: CustomSection) -> List[Any]:
        """Build content for a custom section"""
        content = []

        if section.section_type == SectionType.TEXT:
            content.extend(self._build_text_section(section))

        elif section.section_type == SectionType.TABLE:
            content.extend(self._build_table_section(section))

        elif section.section_type == SectionType.CHART:
            content.extend(self._build_chart_section(section))

        elif section.section_type == SectionType.METRICS:
            content.extend(self._build_metrics_section(section))

        elif section.section_type == SectionType.WATCHLIST:
            content.extend(self._build_watchlist_section(section))

        elif section.section_type == SectionType.PATTERNS:
            content.extend(self._build_patterns_section(section))

        elif section.section_type == SectionType.PERFORMANCE:
            content.extend(self._build_performance_section(section))

        elif section.section_type == SectionType.RISK_METRICS:
            content.extend(self._build_risk_metrics_section(section))

        elif section.section_type == SectionType.CUSTOM_NOTES:
            content.extend(self._build_notes_section(section))

        elif section.section_type == SectionType.IMAGE:
            content.extend(self._build_image_section(section))

        elif section.section_type == SectionType.DIVIDER:
            content.extend(self._build_divider_section(section))

        return content

    def _build_text_section(self, section: CustomSection) -> List[Any]:
        """Build a text section"""
        content = []
        text = section.config.get('text', '')

        if text:
            para = Paragraph(text, self.styles['Body'])
            content.append(para)
            content.append(Spacer(1, 0.1*inch))

        return content

    def _build_table_section(self, section: CustomSection) -> List[Any]:
        """Build a table section"""
        content = []
        data = section.data or section.config.get('data', [])

        if data:
            col_widths = section.config.get('col_widths')
            header_row = section.config.get('header_row', True)

            table = self._create_table(data, col_widths=col_widths, header_row=header_row)
            content.append(table)
            content.append(Spacer(1, 0.15*inch))

        return content

    def _build_chart_section(self, section: CustomSection) -> List[Any]:
        """Build a chart section"""
        content = []

        chart_type = section.config.get('chart_type', 'line')
        chart_data = section.data or section.config.get('data', {})
        title = section.config.get('chart_title', '')

        if chart_data:
            chart_path = self._create_chart(chart_type, chart_data, title=title)
            if chart_path:
                img = RLImage(chart_path, width=6*inch, height=3*inch)
                content.append(img)
                content.append(Spacer(1, 0.15*inch))

        return content

    def _build_metrics_section(self, section: CustomSection) -> List[Any]:
        """Build a metrics section"""
        content = []

        # Get selected metrics
        selected_metrics = section.config.get('metrics', [])
        if not selected_metrics:
            selected_metrics = list(self.metrics.keys())

        if not selected_metrics:
            return content

        # Build metrics table
        data = [['Metric', 'Value']]

        metric_labels = {
            MetricType.WIN_RATE: 'Win Rate',
            MetricType.TOTAL_RETURN: 'Total Return',
            MetricType.AVG_RETURN: 'Avg Return',
            MetricType.SHARPE_RATIO: 'Sharpe Ratio',
            MetricType.MAX_DRAWDOWN: 'Max Drawdown',
            MetricType.PATTERN_COUNT: 'Patterns Found',
            MetricType.TRADE_COUNT: 'Total Trades',
            MetricType.RS_RATING_AVG: 'Avg RS Rating',
            MetricType.RISK_REWARD_RATIO: 'Avg R/R Ratio',
        }

        for metric_type in selected_metrics:
            if metric_type in self.metrics:
                label = metric_labels.get(metric_type, str(metric_type))
                value = self.metrics[metric_type]

                # Format value based on type
                if metric_type in [MetricType.WIN_RATE, MetricType.TOTAL_RETURN,
                                   MetricType.AVG_RETURN, MetricType.MAX_DRAWDOWN]:
                    formatted_value = f"{value:.2f}%"
                elif metric_type == MetricType.SHARPE_RATIO:
                    formatted_value = f"{value:.2f}"
                elif metric_type == MetricType.RISK_REWARD_RATIO:
                    formatted_value = f"1:{value:.2f}"
                else:
                    formatted_value = str(value)

                data.append([label, formatted_value])

        if len(data) > 1:  # Has data beyond header
            table = self._create_table(data, col_widths=[2.5*inch, 2*inch])
            content.append(table)
            content.append(Spacer(1, 0.15*inch))

        return content

    def _build_watchlist_section(self, section: CustomSection) -> List[Any]:
        """Build a watchlist section"""
        content = []

        watchlist_data = section.data or section.config.get('watchlist', [])

        if watchlist_data:
            # Build watchlist table
            data = [['Symbol', 'Name', 'Price', 'Change %', 'Status']]

            for item in watchlist_data:
                data.append([
                    item.get('symbol', ''),
                    item.get('name', ''),
                    f"${item.get('price', 0):.2f}",
                    f"{item.get('change_pct', 0):+.2f}%",
                    item.get('status', ''),
                ])

            col_widths = [0.8*inch, 1.8*inch, 1*inch, 1*inch, 1.2*inch]
            table = self._create_table(data, col_widths=col_widths)
            content.append(table)
            content.append(Spacer(1, 0.15*inch))

        return content

    def _build_patterns_section(self, section: CustomSection) -> List[Any]:
        """Build a patterns section"""
        content = []

        patterns_data = section.data or section.config.get('patterns', [])

        if patterns_data:
            # Build patterns table
            data = [['Symbol', 'Pattern', 'Score', 'Entry', 'Target', 'Stop']]

            for pattern in patterns_data:
                data.append([
                    pattern.get('symbol', ''),
                    pattern.get('pattern_type', ''),
                    f"{pattern.get('score', 0):.1f}",
                    f"${pattern.get('entry_price', 0):.2f}",
                    f"${pattern.get('target_price', 0):.2f}",
                    f"${pattern.get('stop_loss', 0):.2f}",
                ])

            col_widths = [0.8*inch, 1.3*inch, 0.6*inch, 0.9*inch, 0.9*inch, 0.9*inch]
            table = self._create_table(data, col_widths=col_widths)
            content.append(table)
            content.append(Spacer(1, 0.15*inch))

        return content

    def _build_performance_section(self, section: CustomSection) -> List[Any]:
        """Build a performance section"""
        content = []

        perf_data = section.data or section.config.get('performance', {})

        if perf_data:
            data = [
                ['Metric', 'Value'],
                ['Total Trades', str(perf_data.get('total_trades', 0))],
                ['Win Rate', f"{perf_data.get('win_rate', 0):.1f}%"],
                ['Total Return', f"{perf_data.get('total_return', 0):+.2f}%"],
                ['Avg Return', f"{perf_data.get('avg_return', 0):+.2f}%"],
                ['Best Trade', f"{perf_data.get('best_trade', 0):+.2f}%"],
                ['Worst Trade', f"{perf_data.get('worst_trade', 0):.2f}%"],
            ]

            table = self._create_table(data, col_widths=[2*inch, 2*inch])
            content.append(table)
            content.append(Spacer(1, 0.15*inch))

        return content

    def _build_risk_metrics_section(self, section: CustomSection) -> List[Any]:
        """Build a risk metrics section"""
        content = []

        risk_data = section.data or section.config.get('risk', {})

        if risk_data:
            data = [
                ['Risk Metric', 'Value'],
                ['Max Drawdown', f"{risk_data.get('max_drawdown', 0):.2f}%"],
                ['Avg Risk/Trade', f"{risk_data.get('avg_risk', 2.0):.2f}%"],
                ['Risk/Reward Ratio', f"1:{risk_data.get('rr_ratio', 0):.2f}"],
                ['Volatility', f"{risk_data.get('volatility', 0):.2f}%"],
            ]

            if 'var_95' in risk_data:
                data.append(['VaR (95%)', f"{risk_data['var_95']:.2f}%"])

            table = self._create_table(data, col_widths=[2*inch, 2*inch])
            content.append(table)
            content.append(Spacer(1, 0.15*inch))

        return content

    def _build_notes_section(self, section: CustomSection) -> List[Any]:
        """Build a custom notes section"""
        content = []

        notes = section.data or section.config.get('notes', [])
        if not notes and self.custom_notes:
            notes = self.custom_notes

        if notes:
            for note in notes:
                para = Paragraph(f"• {note}", self.styles['BodyLeft'])
                content.append(para)

            content.append(Spacer(1, 0.1*inch))

        return content

    def _build_image_section(self, section: CustomSection) -> List[Any]:
        """Build an image section"""
        content = []

        image_path = section.config.get('image_path', '')
        width = section.config.get('width', 5*inch)
        height = section.config.get('height', 3*inch)

        if image_path and image_path.startswith(('http://', 'https://', '/')):
            try:
                img = RLImage(image_path, width=width, height=height)
                content.append(img)
                content.append(Spacer(1, 0.15*inch))
            except Exception as e:
                # Fallback: show error message
                error_text = f"<i>Image could not be loaded: {image_path}</i>"
                content.append(Paragraph(error_text, self.styles['Body']))

        return content

    def _build_divider_section(self, section: CustomSection) -> List[Any]:
        """Build a divider section"""
        return [Spacer(1, 0.3*inch)]


# Pre-built template library
class TemplateLibrary:
    """Library of pre-built report templates"""

    @staticmethod
    def get_daily_summary_template() -> ReportTemplate:
        """Daily market summary template"""
        return ReportTemplate(
            template_id="daily_summary",
            name="Daily Market Summary",
            description="Quick daily market overview with top movers and patterns",
            sections=[
                CustomSection(
                    section_type=SectionType.METRICS,
                    title="Market Metrics",
                    order=1,
                    config={'metrics': [
                        MetricType.PATTERN_COUNT,
                        MetricType.RS_RATING_AVG,
                    ]},
                ),
                CustomSection(
                    section_type=SectionType.PATTERNS,
                    title="Top Patterns",
                    order=2,
                ),
                CustomSection(
                    section_type=SectionType.WATCHLIST,
                    title="Watchlist",
                    order=3,
                ),
            ],
            default_config=ReportConfig(
                title="Daily Market Summary",
                theme='professional',
            ),
            tags=["daily", "summary", "quick"],
        )

    @staticmethod
    def get_weekly_performance_template() -> ReportTemplate:
        """Weekly performance review template"""
        return ReportTemplate(
            template_id="weekly_performance",
            name="Weekly Performance Review",
            description="Comprehensive weekly performance analysis",
            sections=[
                CustomSection(
                    section_type=SectionType.PERFORMANCE,
                    title="Performance Summary",
                    order=1,
                ),
                CustomSection(
                    section_type=SectionType.RISK_METRICS,
                    title="Risk Analysis",
                    order=2,
                ),
                CustomSection(
                    section_type=SectionType.PATTERNS,
                    title="Best Setups",
                    order=3,
                ),
                CustomSection(
                    section_type=SectionType.CUSTOM_NOTES,
                    title="Lessons Learned",
                    order=4,
                ),
            ],
            default_config=ReportConfig(
                title="Weekly Performance Review",
                theme='professional',
            ),
            tags=["weekly", "performance", "review"],
        )

    @staticmethod
    def get_trade_journal_template() -> ReportTemplate:
        """Trade journal template"""
        return ReportTemplate(
            template_id="trade_journal",
            name="Trade Journal",
            description="Detailed trade journal with notes and analysis",
            sections=[
                CustomSection(
                    section_type=SectionType.TABLE,
                    title="Trade Details",
                    order=1,
                ),
                CustomSection(
                    section_type=SectionType.CHART,
                    title="Performance Chart",
                    order=2,
                    config={'chart_type': 'line'},
                ),
                CustomSection(
                    section_type=SectionType.METRICS,
                    title="Trade Metrics",
                    order=3,
                ),
                CustomSection(
                    section_type=SectionType.CUSTOM_NOTES,
                    title="Trade Notes",
                    order=4,
                ),
            ],
            default_config=ReportConfig(
                title="Trade Journal",
                theme='minimal',
            ),
            tags=["journal", "trades", "detailed"],
        )

    @staticmethod
    def list_templates() -> List[ReportTemplate]:
        """Get all available templates"""
        return [
            TemplateLibrary.get_daily_summary_template(),
            TemplateLibrary.get_weekly_performance_template(),
            TemplateLibrary.get_trade_journal_template(),
        ]
