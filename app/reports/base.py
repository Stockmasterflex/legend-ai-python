"""
Base classes for PDF report generation
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from io import BytesIO
from enum import Enum

from pydantic import BaseModel, Field
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image as RLImage,
    KeepTogether,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from jinja2 import Template


class ReportFormat(str, Enum):
    """Supported report formats"""
    PDF = "pdf"
    HTML = "html"


class PageSize(str, Enum):
    """Page size options"""
    LETTER = "letter"
    A4 = "a4"


class ReportTheme(str, Enum):
    """Report theme/branding"""
    DEFAULT = "default"
    DARK = "dark"
    PROFESSIONAL = "professional"
    MINIMAL = "minimal"


class ReportSection(BaseModel):
    """Represents a section in a report"""
    title: str
    content: Union[str, List[Any]]
    order: int = 0
    page_break_before: bool = False
    page_break_after: bool = False


class ReportConfig(BaseModel):
    """Configuration for report generation"""
    title: str
    subtitle: Optional[str] = None
    author: str = "Legend AI Trading Platform"
    format: ReportFormat = ReportFormat.PDF
    page_size: PageSize = PageSize.LETTER
    theme: ReportTheme = ReportTheme.PROFESSIONAL
    logo_path: Optional[str] = None
    include_header: bool = True
    include_footer: bool = True
    include_page_numbers: bool = True
    include_timestamp: bool = True
    timestamp: Optional[datetime] = None

    # Branding
    primary_color: str = "#1f77b4"  # Blue
    secondary_color: str = "#2ca02c"  # Green
    accent_color: str = "#ff7f0e"  # Orange
    text_color: str = "#333333"

    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BaseReport:
    """Base class for all PDF reports"""

    def __init__(self, config: ReportConfig):
        self.config = config
        self.sections: List[ReportSection] = []
        self.styles = self._create_styles()
        self.story: List[Any] = []

    def _create_styles(self) -> Dict[str, ParagraphStyle]:
        """Create custom paragraph styles"""
        base_styles = getSampleStyleSheet()

        custom_styles = {
            'Title': ParagraphStyle(
                'CustomTitle',
                parent=base_styles['Title'],
                fontSize=24,
                textColor=colors.HexColor(self.config.primary_color),
                spaceAfter=12,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold',
            ),
            'Subtitle': ParagraphStyle(
                'CustomSubtitle',
                parent=base_styles['Normal'],
                fontSize=14,
                textColor=colors.HexColor(self.config.secondary_color),
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName='Helvetica-Oblique',
            ),
            'Heading1': ParagraphStyle(
                'CustomHeading1',
                parent=base_styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor(self.config.primary_color),
                spaceAfter=12,
                spaceBefore=12,
                fontName='Helvetica-Bold',
                borderPadding=5,
                borderColor=colors.HexColor(self.config.primary_color),
                borderWidth=0,
                leftIndent=0,
            ),
            'Heading2': ParagraphStyle(
                'CustomHeading2',
                parent=base_styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor(self.config.text_color),
                spaceAfter=8,
                spaceBefore=8,
                fontName='Helvetica-Bold',
            ),
            'Body': ParagraphStyle(
                'CustomBody',
                parent=base_styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor(self.config.text_color),
                spaceAfter=6,
                alignment=TA_JUSTIFY,
            ),
            'BodyLeft': ParagraphStyle(
                'CustomBodyLeft',
                parent=base_styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor(self.config.text_color),
                spaceAfter=6,
                alignment=TA_LEFT,
            ),
            'Metric': ParagraphStyle(
                'CustomMetric',
                parent=base_styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor(self.config.text_color),
                spaceAfter=4,
                fontName='Helvetica-Bold',
            ),
            'Footer': ParagraphStyle(
                'CustomFooter',
                parent=base_styles['Normal'],
                fontSize=8,
                textColor=colors.gray,
                alignment=TA_CENTER,
            ),
        }

        return custom_styles

    def add_section(self, section: ReportSection):
        """Add a section to the report"""
        self.sections.append(section)

    def _add_header(self):
        """Add report header"""
        if not self.config.include_header:
            return

        # Logo
        if self.config.logo_path and Path(self.config.logo_path).exists():
            logo = RLImage(self.config.logo_path, width=1*inch, height=0.5*inch)
            logo.hAlign = 'LEFT'
            self.story.append(logo)
            self.story.append(Spacer(1, 0.2*inch))

        # Title
        title = Paragraph(self.config.title, self.styles['Title'])
        self.story.append(title)

        # Subtitle
        if self.config.subtitle:
            subtitle = Paragraph(self.config.subtitle, self.styles['Subtitle'])
            self.story.append(subtitle)

        # Timestamp
        if self.config.include_timestamp:
            timestamp = self.config.timestamp or datetime.now()
            timestamp_text = f"Generated: {timestamp.strftime('%B %d, %Y at %I:%M %p')}"
            timestamp_para = Paragraph(timestamp_text, self.styles['Footer'])
            self.story.append(timestamp_para)

        self.story.append(Spacer(1, 0.3*inch))

    def _add_footer(self, canvas, doc):
        """Add page footer (callback for PageTemplate)"""
        if not self.config.include_footer:
            return

        canvas.saveState()

        # Page number
        if self.config.include_page_numbers:
            page_num = f"Page {doc.page}"
            canvas.setFont('Helvetica', 8)
            canvas.setFillColor(colors.gray)
            canvas.drawRightString(
                doc.pagesize[0] - 0.75*inch,
                0.5*inch,
                page_num
            )

        # Footer text
        footer_text = f"{self.config.author} | Confidential"
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.gray)
        canvas.drawString(
            0.75*inch,
            0.5*inch,
            footer_text
        )

        canvas.restoreState()

    def _create_table(
        self,
        data: List[List[Any]],
        col_widths: Optional[List[float]] = None,
        style: Optional[TableStyle] = None,
        header_row: bool = True
    ) -> Table:
        """Create a styled table"""
        if not data:
            return None

        # Default table style
        default_style = TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0 if header_row else -1),
             colors.HexColor(self.config.primary_color) if header_row else colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0 if header_row else -1),
             colors.whitesmoke if header_row else colors.HexColor(self.config.text_color)),
            ('FONTNAME', (0, 0), (-1, 0 if header_row else -1),
             'Helvetica-Bold' if header_row else 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            # Body styling
            ('BACKGROUND', (0, 1 if header_row else 0), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1 if header_row else 0), (-1, -1),
             [colors.white, colors.HexColor('#f0f0f0')]),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ])

        table_style = style or default_style
        table = Table(data, colWidths=col_widths)
        table.setStyle(table_style)

        return table

    def _create_chart(
        self,
        chart_type: str,
        data: Dict[str, Any],
        title: str = "",
        **kwargs
    ) -> Optional[str]:
        """Create a matplotlib chart and return path to saved image"""
        fig, ax = plt.subplots(figsize=(8, 4))

        if chart_type == "line":
            x = data.get("x", [])
            y = data.get("y", [])
            ax.plot(x, y, color=self.config.primary_color, linewidth=2)

        elif chart_type == "bar":
            x = data.get("x", [])
            y = data.get("y", [])
            ax.bar(x, y, color=self.config.primary_color)

        elif chart_type == "pie":
            labels = data.get("labels", [])
            values = data.get("values", [])
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)

        if title:
            ax.set_title(title, fontsize=12, color=self.config.primary_color)

        ax.grid(True, alpha=0.3)
        plt.tight_layout()

        # Save to temporary file
        chart_path = f"/tmp/chart_{datetime.now().timestamp()}.png"
        plt.savefig(chart_path, dpi=150, bbox_inches='tight')
        plt.close()

        return chart_path

    def build(self) -> List[Any]:
        """Build the report story (must be implemented by subclasses)"""
        raise NotImplementedError("Subclasses must implement build()")

    def generate(self, output_path: Optional[str] = None) -> Union[str, BytesIO]:
        """Generate the PDF report"""
        # Build the story
        self.story = []
        self._add_header()
        self.build()

        # Sort sections by order
        self.sections.sort(key=lambda s: s.order)

        # Add sections to story
        for section in self.sections:
            if section.page_break_before:
                self.story.append(PageBreak())

            # Add section title
            if section.title:
                self.story.append(Paragraph(section.title, self.styles['Heading1']))
                self.story.append(Spacer(1, 0.15*inch))

            # Add section content
            if isinstance(section.content, str):
                self.story.append(Paragraph(section.content, self.styles['Body']))
            elif isinstance(section.content, list):
                for item in section.content:
                    self.story.append(item)

            self.story.append(Spacer(1, 0.2*inch))

            if section.page_break_after:
                self.story.append(PageBreak())

        # Create PDF
        page_size = letter if self.config.page_size == PageSize.LETTER else A4

        if output_path:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=page_size,
                leftMargin=0.75*inch,
                rightMargin=0.75*inch,
                topMargin=1*inch,
                bottomMargin=1*inch,
            )
            doc.build(self.story, onFirstPage=self._add_footer, onLaterPages=self._add_footer)
            return output_path
        else:
            # Generate to BytesIO
            buffer = BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=page_size,
                leftMargin=0.75*inch,
                rightMargin=0.75*inch,
                topMargin=1*inch,
                bottomMargin=1*inch,
            )
            doc.build(self.story, onFirstPage=self._add_footer, onLaterPages=self._add_footer)
            buffer.seek(0)
            return buffer

    def generate_html(self) -> str:
        """Generate HTML version of the report"""
        # Build sections first
        self.build()

        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{{ title }}</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    color: {{ text_color }};
                }
                h1 {
                    color: {{ primary_color }};
                    border-bottom: 2px solid {{ primary_color }};
                    padding-bottom: 10px;
                }
                h2 {
                    color: {{ secondary_color }};
                    margin-top: 30px;
                }
                .header {
                    text-align: center;
                    margin-bottom: 40px;
                }
                .timestamp {
                    color: #666;
                    font-size: 12px;
                    text-align: center;
                }
                .section {
                    margin-bottom: 30px;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }
                th {
                    background-color: {{ primary_color }};
                    color: white;
                    padding: 10px;
                    text-align: left;
                }
                td {
                    padding: 8px;
                    border: 1px solid #ddd;
                }
                tr:nth-child(even) {
                    background-color: #f0f0f0;
                }
                .footer {
                    margin-top: 50px;
                    padding-top: 20px;
                    border-top: 1px solid #ccc;
                    text-align: center;
                    color: #666;
                    font-size: 12px;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{{ title }}</h1>
                {% if subtitle %}
                <h2>{{ subtitle }}</h2>
                {% endif %}
                <p class="timestamp">{{ timestamp }}</p>
            </div>

            {% for section in sections %}
            <div class="section">
                <h2>{{ section.title }}</h2>
                {{ section.content }}
            </div>
            {% endfor %}

            <div class="footer">
                {{ author }} | Confidential
            </div>
        </body>
        </html>
        """

        template = Template(html_template)
        timestamp = self.config.timestamp or datetime.now()

        return template.render(
            title=self.config.title,
            subtitle=self.config.subtitle,
            timestamp=timestamp.strftime('%B %d, %Y at %I:%M %p'),
            primary_color=self.config.primary_color,
            secondary_color=self.config.secondary_color,
            text_color=self.config.text_color,
            author=self.config.author,
            sections=self.sections,
        )
