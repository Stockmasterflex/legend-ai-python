"""
PDF Export Service for Trade Plans
Generates professional PDF documents with charts, tables, and analysis
"""
import logging
import os
from typing import Optional
from datetime import datetime
from io import BytesIO
import httpx

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from app.services.plan_generator import TradePlanData

logger = logging.getLogger(__name__)


class PDFExportService:
    """Service for exporting trade plans to PDF"""

    def __init__(self, output_dir: str = "trade_plans"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Define custom styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""

        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#283593'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))

        # Subsection style
        self.styles.add(ParagraphStyle(
            name='SubSection',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#3f51b5'),
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))

        # Risk warning style
        self.styles.add(ParagraphStyle(
            name='RiskWarning',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.red,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))

    async def generate_pdf(
        self,
        plan_data: TradePlanData,
        filename: Optional[str] = None
    ) -> str:
        """
        Generate PDF trade plan document

        Args:
            plan_data: TradePlanData object with complete plan details
            filename: Optional custom filename

        Returns:
            Path to generated PDF file
        """

        # Generate filename
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{plan_data.ticker}_{timestamp}_trade_plan.pdf"

        filepath = os.path.join(self.output_dir, filename)

        # Create PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Build content
        story = []

        # Header
        story.extend(self._build_header(plan_data))
        story.append(Spacer(1, 0.2 * inch))

        # Pattern Analysis Section
        story.extend(self._build_pattern_section(plan_data))
        story.append(Spacer(1, 0.2 * inch))

        # Entry & Exit Levels Section
        story.extend(self._build_levels_section(plan_data))
        story.append(Spacer(1, 0.2 * inch))

        # Multi-Scenario Analysis
        story.extend(self._build_scenarios_section(plan_data))
        story.append(Spacer(1, 0.2 * inch))

        # Position Sizing Section
        story.extend(self._build_position_section(plan_data))
        story.append(Spacer(1, 0.2 * inch))

        # Chart (if available)
        if plan_data.chart_url:
            story.extend(await self._build_chart_section(plan_data.chart_url))
            story.append(Spacer(1, 0.2 * inch))

        # AI Analysis Section
        story.extend(self._build_ai_analysis_section(plan_data))
        story.append(Spacer(1, 0.2 * inch))

        # Pre-Trade Checklist
        story.extend(self._build_checklist_section(plan_data))
        story.append(Spacer(1, 0.2 * inch))

        # Risk Factors
        story.extend(self._build_risk_factors_section(plan_data))
        story.append(Spacer(1, 0.2 * inch))

        # Footer/Disclaimer
        story.extend(self._build_footer())

        # Build PDF
        doc.build(story)

        logger.info(f"✅ PDF generated: {filepath}")
        return filepath

    def _build_header(self, plan_data: TradePlanData) -> list:
        """Build document header"""
        elements = []

        # Title
        title = Paragraph(
            f"Trade Plan: {plan_data.ticker}",
            self.styles['CustomTitle']
        )
        elements.append(title)

        # Date and pattern info
        date_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        subtitle = Paragraph(
            f"<b>Generated:</b> {date_str} | "
            f"<b>Pattern:</b> {plan_data.pattern_type} | "
            f"<b>Score:</b> {plan_data.pattern_score:.1f}/10",
            self.styles['Normal']
        )
        elements.append(subtitle)

        # Horizontal line
        elements.append(Spacer(1, 0.1 * inch))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#283593')))

        return elements

    def _build_pattern_section(self, plan_data: TradePlanData) -> list:
        """Build pattern analysis section"""
        elements = []

        elements.append(Paragraph("Pattern Analysis", self.styles['SectionHeader']))

        # Pattern details table
        data = [
            ['Pattern Type', plan_data.pattern_type],
            ['Confidence Score', f"{plan_data.pattern_score:.1f}/10"],
            ['Current Price', f"${plan_data.current_price:.2f}"],
        ]

        table = Table(data, colWidths=[2.5 * inch, 3.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8eaf6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))

        elements.append(table)
        elements.append(Spacer(1, 0.1 * inch))

        # Pattern analysis text
        if plan_data.pattern_analysis:
            elements.append(Paragraph("<b>Analysis:</b>", self.styles['SubSection']))
            elements.append(Paragraph(plan_data.pattern_analysis, self.styles['Normal']))

        return elements

    def _build_levels_section(self, plan_data: TradePlanData) -> list:
        """Build entry and exit levels section"""
        elements = []

        elements.append(Paragraph("Entry & Exit Levels", self.styles['SectionHeader']))

        # Levels table
        data = [
            ['Level', 'Price', 'Notes'],
            ['Entry Zone Low', f"${plan_data.entry_zone.low:.2f}", ''],
            ['Optimal Entry', f"${plan_data.entry_zone.optimal:.2f}", 'Recommended'],
            ['Entry Zone High', f"${plan_data.entry_zone.high:.2f}", ''],
            ['Initial Stop Loss', f"${plan_data.stop_levels.initial_stop:.2f}", 'Hard stop'],
            ['Invalidation Price', f"${plan_data.stop_levels.invalidation_price:.2f}", 'Pattern fails'],
        ]

        table = Table(data, colWidths=[2 * inch, 1.5 * inch, 2.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#283593')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
        ]))

        elements.append(table)
        elements.append(Spacer(1, 0.1 * inch))

        # Entry reasoning
        elements.append(Paragraph(plan_data.entry_zone.reasoning, self.styles['Normal']))

        return elements

    def _build_scenarios_section(self, plan_data: TradePlanData) -> list:
        """Build multi-scenario analysis section"""
        elements = []

        elements.append(Paragraph("Multi-Scenario Price Targets", self.styles['SectionHeader']))

        scenarios = plan_data.scenario_analysis

        # Scenarios table
        data = [
            ['Scenario', 'Target Price', 'Risk:Reward', 'Probability'],
            [
                'Best Case',
                f"${scenarios.best_case_target:.2f}",
                f"{scenarios.best_case_rr:.2f}R",
                f"{scenarios.probability_estimates.get('best', 0)*100:.0f}%"
            ],
            [
                'Base Case',
                f"${scenarios.base_case_target:.2f}",
                f"{scenarios.base_case_rr:.2f}R",
                f"{scenarios.probability_estimates.get('base', 0)*100:.0f}%"
            ],
            [
                'Worst Case',
                f"${scenarios.worst_case_target:.2f}",
                f"{scenarios.worst_case_rr:.2f}R",
                f"{scenarios.probability_estimates.get('worst', 0)*100:.0f}%"
            ],
        ]

        table = Table(data, colWidths=[1.5 * inch, 1.5 * inch, 1.5 * inch, 1.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#283593')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [
                colors.HexColor('#c8e6c9'),
                colors.HexColor('#fff9c4'),
                colors.HexColor('#ffccbc')
            ])
        ]))

        elements.append(table)

        return elements

    def _build_position_section(self, plan_data: TradePlanData) -> list:
        """Build position sizing section"""
        elements = []

        elements.append(Paragraph("Position Sizing & Risk Management", self.styles['SectionHeader']))

        # Position details table
        data = [
            ['Position Size', f"{plan_data.position_size} shares"],
            ['Position Value', f"${plan_data.position_value:,.2f}"],
            ['Risk Amount', f"${plan_data.risk_amount:,.2f}"],
            ['Risk Per Share', f"${abs(plan_data.entry_zone.optimal - plan_data.stop_levels.initial_stop):.2f}"],
        ]

        table = Table(data, colWidths=[2.5 * inch, 3.5 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8eaf6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))

        elements.append(table)

        return elements

    async def _build_chart_section(self, chart_url: str) -> list:
        """Build chart section with downloaded chart image"""
        elements = []

        try:
            # Download chart image
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(chart_url)
                response.raise_for_status()

                # Create image from bytes
                img_data = BytesIO(response.content)
                img = Image(img_data, width=6 * inch, height=3.5 * inch)

                elements.append(Paragraph("Price Chart", self.styles['SectionHeader']))
                elements.append(img)

        except Exception as e:
            logger.warning(f"Failed to download chart: {e}")
            elements.append(Paragraph(
                f"Chart available at: {chart_url}",
                self.styles['Normal']
            ))

        return elements

    def _build_ai_analysis_section(self, plan_data: TradePlanData) -> list:
        """Build AI analysis section"""
        elements = []

        elements.append(Paragraph("AI-Powered Analysis", self.styles['SectionHeader']))

        # Split AI notes into paragraphs
        for paragraph in plan_data.ai_notes.split('\n\n'):
            if paragraph.strip():
                elements.append(Paragraph(paragraph.strip(), self.styles['Normal']))
                elements.append(Spacer(1, 0.05 * inch))

        return elements

    def _build_checklist_section(self, plan_data: TradePlanData) -> list:
        """Build pre-trade checklist section"""
        elements = []

        elements.append(Paragraph("Pre-Trade Checklist", self.styles['SectionHeader']))

        # Create checklist items
        for item in plan_data.checklist:
            elements.append(Paragraph(f"☐ {item}", self.styles['Normal']))
            elements.append(Spacer(1, 0.05 * inch))

        return elements

    def _build_risk_factors_section(self, plan_data: TradePlanData) -> list:
        """Build risk factors section"""
        elements = []

        if plan_data.risk_factors:
            elements.append(Paragraph("Risk Factors", self.styles['SectionHeader']))

            for risk in plan_data.risk_factors:
                elements.append(Paragraph(risk, self.styles['RiskWarning']))
                elements.append(Spacer(1, 0.05 * inch))

        return elements

    def _build_footer(self) -> list:
        """Build document footer"""
        elements = []

        elements.append(Spacer(1, 0.3 * inch))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
        elements.append(Spacer(1, 0.1 * inch))

        disclaimer = Paragraph(
            "<i>This trade plan is generated by Legend AI for informational purposes only. "
            "It is not financial advice. Trading involves substantial risk of loss. "
            "Always conduct your own research and consult with a licensed financial advisor "
            "before making investment decisions. Past performance does not guarantee future results.</i>",
            self.styles['Normal']
        )
        elements.append(disclaimer)

        return elements


# Global instance
_pdf_service: Optional[PDFExportService] = None


def get_pdf_export_service(output_dir: str = "trade_plans") -> PDFExportService:
    """Get or create PDF export service singleton"""
    global _pdf_service
    if _pdf_service is None:
        _pdf_service = PDFExportService(output_dir=output_dir)
    return _pdf_service
