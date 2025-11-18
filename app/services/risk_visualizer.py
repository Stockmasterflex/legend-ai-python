"""
Risk Visualization Service
Generate visual representations of portfolio risk
"""
import logging
from typing import List, Dict, Optional
import json

from app.core.risk_models import (
    PortfolioHeat,
    RiskVisualization,
    PortfolioPosition
)

logger = logging.getLogger(__name__)


class RiskVisualizer:
    """
    Generate risk visualization data for charts and displays

    Creates data for:
    - Risk pyramid chart
    - Position size comparison
    - Heat map by ticker
    - Risk distribution pie
    - Sector concentration
    """

    def __init__(self):
        pass

    # ========================================================================
    # RISK PYRAMID
    # ========================================================================

    def generate_risk_pyramid_chart(
        self,
        viz: RiskVisualization
    ) -> dict:
        """
        Generate risk pyramid chart data

        Returns chart configuration for frontend rendering
        """

        if not viz.pyramid:
            return {}

        pyramid = viz.pyramid

        return {
            'type': 'pyramid',
            'title': 'Risk Pyramid - Position Allocation',
            'description': 'Conservative base (40%), Moderate middle (40%), Aggressive top (20%)',
            'tiers': [
                {
                    'level': 'Tier 1 - Conservative Base',
                    'allocation': pyramid.tier1_pct,
                    'positions': pyramid.tier1_conservative,
                    'count': len(pyramid.tier1_conservative),
                    'color': '#2ecc71',  # Green
                    'description': 'Low-risk, core positions'
                },
                {
                    'level': 'Tier 2 - Moderate Growth',
                    'allocation': pyramid.tier2_pct,
                    'positions': pyramid.tier2_moderate,
                    'count': len(pyramid.tier2_moderate),
                    'color': '#f39c12',  # Orange
                    'description': 'Balanced risk/reward'
                },
                {
                    'level': 'Tier 3 - Aggressive Opportunities',
                    'allocation': pyramid.tier3_pct,
                    'positions': pyramid.tier3_aggressive,
                    'count': len(pyramid.tier3_aggressive),
                    'color': '#e74c3c',  # Red
                    'description': 'High-risk, high-reward'
                }
            ],
            'visualization_type': 'stacked_pyramid'
        }

    # ========================================================================
    # POSITION SIZE COMPARISON
    # ========================================================================

    def generate_position_size_chart(
        self,
        viz: RiskVisualization,
        sort_by: str = 'value'  # 'value' or 'risk'
    ) -> dict:
        """
        Generate horizontal bar chart comparing position sizes

        Args:
            viz: Risk visualization data
            sort_by: Sort by 'value' or 'risk'

        Returns:
            Chart configuration
        """

        if sort_by == 'risk':
            data = sorted(
                viz.position_risks.items(),
                key=lambda x: x[1],
                reverse=True
            )
            title = 'Position Risk Comparison'
            value_label = 'Risk ($)'
        else:
            data = sorted(
                viz.position_sizes.items(),
                key=lambda x: x[1],
                reverse=True
            )
            title = 'Position Size Comparison'
            value_label = 'Position Value ($)'

        symbols = [item[0] for item in data]
        values = [item[1] for item in data]

        return {
            'type': 'horizontal_bar',
            'title': title,
            'labels': symbols,
            'data': values,
            'value_label': value_label,
            'colors': self._generate_gradient_colors(len(symbols)),
            'visualization_type': 'bar_chart'
        }

    # ========================================================================
    # HEAT MAP
    # ========================================================================

    def generate_heat_map_chart(
        self,
        viz: RiskVisualization
    ) -> dict:
        """
        Generate heat map showing risk, size, and P&L by ticker

        Returns:
            Heat map chart configuration
        """

        symbols = list(viz.heat_map.keys())

        # Build matrix data
        matrix_data = []

        for symbol in symbols:
            data = viz.heat_map[symbol]
            matrix_data.append({
                'symbol': symbol,
                'risk_pct': data['risk_pct'],
                'size_pct': data['size_pct'],
                'pnl_pct': data['pnl_pct'],
                'heat_score': data['risk_pct'] + (data['size_pct'] * 0.5)  # Composite heat
            })

        # Sort by heat score
        matrix_data.sort(key=lambda x: x['heat_score'], reverse=True)

        return {
            'type': 'heat_map',
            'title': 'Portfolio Heat Map by Ticker',
            'symbols': [d['symbol'] for d in matrix_data],
            'metrics': {
                'risk': [d['risk_pct'] for d in matrix_data],
                'size': [d['size_pct'] for d in matrix_data],
                'pnl': [d['pnl_pct'] for d in matrix_data],
                'heat': [d['heat_score'] for d in matrix_data]
            },
            'matrix_data': matrix_data,
            'color_scale': {
                'low': '#2ecc71',
                'medium': '#f39c12',
                'high': '#e74c3c'
            },
            'visualization_type': 'heat_map'
        }

    # ========================================================================
    # RISK DISTRIBUTION PIE
    # ========================================================================

    def generate_risk_distribution_pie(
        self,
        viz: RiskVisualization
    ) -> dict:
        """
        Generate pie chart of risk distribution

        Returns:
            Pie chart configuration
        """

        return {
            'type': 'pie',
            'title': 'Risk Distribution',
            'labels': list(viz.risk_distribution.keys()),
            'data': list(viz.risk_distribution.values()),
            'colors': ['#e74c3c', '#2ecc71', '#3498db'],
            'visualization_type': 'pie_chart'
        }

    # ========================================================================
    # SECTOR CONCENTRATION
    # ========================================================================

    def generate_sector_concentration_chart(
        self,
        heat: PortfolioHeat
    ) -> dict:
        """
        Generate sector concentration chart

        Args:
            heat: Portfolio heat data

        Returns:
            Chart configuration
        """

        if not heat.sector_concentration:
            return {}

        sectors = list(heat.sector_concentration.keys())
        percentages = list(heat.sector_concentration.values())

        return {
            'type': 'horizontal_bar',
            'title': 'Sector Concentration',
            'labels': sectors,
            'data': percentages,
            'value_label': 'Allocation (%)',
            'colors': self._generate_sector_colors(len(sectors)),
            'max_limit': heat.max_sector_concentration_pct,
            'visualization_type': 'bar_chart'
        }

    # ========================================================================
    # PORTFOLIO HEAT GAUGE
    # ========================================================================

    def generate_heat_gauge(
        self,
        heat: PortfolioHeat
    ) -> dict:
        """
        Generate heat gauge visualization

        Args:
            heat: Portfolio heat data

        Returns:
            Gauge chart configuration
        """

        heat_score = heat.heat_score

        # Determine status
        if heat_score < 30:
            status = 'low'
            color = '#2ecc71'
            message = '✅ Portfolio risk is LOW - room for growth'
        elif heat_score < 60:
            status = 'moderate'
            color = '#f39c12'
            message = '⚠️ Portfolio risk is MODERATE - monitor closely'
        elif heat_score < 80:
            status = 'elevated'
            color = '#e67e22'
            message = '⚠️ Portfolio risk is ELEVATED - consider reducing'
        else:
            status = 'critical'
            color = '#e74c3c'
            message = '❌ Portfolio risk is CRITICAL - reduce immediately'

        return {
            'type': 'gauge',
            'title': 'Portfolio Heat Score',
            'value': heat_score,
            'min': 0,
            'max': 100,
            'status': status,
            'color': color,
            'message': message,
            'thresholds': [
                {'value': 30, 'label': 'Low', 'color': '#2ecc71'},
                {'value': 60, 'label': 'Moderate', 'color': '#f39c12'},
                {'value': 80, 'label': 'Elevated', 'color': '#e67e22'},
                {'value': 100, 'label': 'Critical', 'color': '#e74c3c'}
            ],
            'visualization_type': 'gauge'
        }

    # ========================================================================
    # RISK TIMELINE (for historical tracking)
    # ========================================================================

    def generate_risk_timeline_chart(
        self,
        historical_data: List[Dict]
    ) -> dict:
        """
        Generate risk timeline chart

        Args:
            historical_data: List of {date, risk_pct, heat_score, positions}

        Returns:
            Timeline chart configuration
        """

        dates = [d['date'] for d in historical_data]
        risk_pcts = [d['risk_pct'] for d in historical_data]
        heat_scores = [d['heat_score'] for d in historical_data]
        num_positions = [d['positions'] for d in historical_data]

        return {
            'type': 'line',
            'title': 'Portfolio Risk Timeline',
            'x_axis': dates,
            'series': [
                {
                    'name': 'Risk %',
                    'data': risk_pcts,
                    'color': '#e74c3c',
                    'yAxis': 0
                },
                {
                    'name': 'Heat Score',
                    'data': heat_scores,
                    'color': '#f39c12',
                    'yAxis': 0
                },
                {
                    'name': '# Positions',
                    'data': num_positions,
                    'color': '#3498db',
                    'yAxis': 1
                }
            ],
            'y_axes': [
                {'title': 'Percentage / Score'},
                {'title': 'Positions', 'opposite': True}
            ],
            'visualization_type': 'multi_series_line'
        }

    # ========================================================================
    # COMPREHENSIVE DASHBOARD
    # ========================================================================

    def generate_risk_dashboard(
        self,
        heat: PortfolioHeat,
        viz: RiskVisualization
    ) -> dict:
        """
        Generate complete risk dashboard with all visualizations

        Args:
            heat: Portfolio heat data
            viz: Visualization data

        Returns:
            Complete dashboard configuration
        """

        return {
            'summary': {
                'total_account_value': heat.total_account_value,
                'total_risk_dollars': heat.total_risk_dollars,
                'total_risk_percentage': heat.total_risk_percentage,
                'num_positions': heat.num_positions,
                'heat_score': heat.heat_score,
                'is_overheated': heat.is_overheated,
                'warnings': heat.warnings
            },
            'charts': {
                'heat_gauge': self.generate_heat_gauge(heat),
                'risk_pyramid': self.generate_risk_pyramid_chart(viz),
                'position_sizes': self.generate_position_size_chart(viz, 'value'),
                'position_risks': self.generate_position_size_chart(viz, 'risk'),
                'heat_map': self.generate_heat_map_chart(viz),
                'risk_distribution': self.generate_risk_distribution_pie(viz),
                'sector_concentration': self.generate_sector_concentration_chart(heat)
            },
            'limits': {
                'max_portfolio_risk': heat.max_portfolio_risk_pct,
                'max_position_size': heat.max_single_position_pct,
                'max_sector_concentration': heat.max_sector_concentration_pct,
                'current_largest_position': heat.largest_position_pct,
                'current_largest_risk': heat.largest_risk_pct
            },
            'positions': [
                {
                    'symbol': p.symbol,
                    'shares': p.shares,
                    'market_value': p.market_value,
                    'cost_basis': p.cost_basis,
                    'unrealized_pnl': p.unrealized_pnl,
                    'pnl_percentage': p.pnl_percentage,
                    'risk_dollars': p.risk_dollars,
                    'sector': p.sector
                }
                for p in heat.positions
            ]
        }

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    def _generate_gradient_colors(self, count: int) -> List[str]:
        """Generate gradient colors from green to red"""
        if count == 0:
            return []
        if count == 1:
            return ['#3498db']

        colors = []
        for i in range(count):
            ratio = i / (count - 1)
            # Interpolate from green to red via yellow
            if ratio < 0.5:
                # Green to yellow
                r = int(46 + (243 - 46) * (ratio * 2))
                g = int(204 + (156 - 204) * (ratio * 2))
                b = int(113 + (18 - 113) * (ratio * 2))
            else:
                # Yellow to red
                r = int(243 + (231 - 243) * ((ratio - 0.5) * 2))
                g = int(156 + (76 - 156) * ((ratio - 0.5) * 2))
                b = int(18 + (60 - 18) * ((ratio - 0.5) * 2))

            colors.append(f'#{r:02x}{g:02x}{b:02x}')

        return colors

    def _generate_sector_colors(self, count: int) -> List[str]:
        """Generate distinct colors for sectors"""
        base_colors = [
            '#3498db',  # Blue
            '#2ecc71',  # Green
            '#f39c12',  # Orange
            '#e74c3c',  # Red
            '#9b59b6',  # Purple
            '#1abc9c',  # Turquoise
            '#34495e',  # Dark gray
            '#e67e22',  # Pumpkin
            '#95a5a6',  # Silver
            '#16a085'   # Green sea
        ]

        # Repeat if more sectors than colors
        colors = []
        for i in range(count):
            colors.append(base_colors[i % len(base_colors)])

        return colors

    # ========================================================================
    # ASCII/TEXT VISUALIZATIONS (for terminal/API)
    # ========================================================================

    def generate_text_heat_map(
        self,
        viz: RiskVisualization,
        width: int = 50
    ) -> str:
        """
        Generate ASCII heat map for terminal display

        Args:
            viz: Visualization data
            width: Character width

        Returns:
            ASCII art heat map
        """

        lines = []
        lines.append("=" * width)
        lines.append("PORTFOLIO HEAT MAP".center(width))
        lines.append("=" * width)

        for symbol, data in sorted(
            viz.heat_map.items(),
            key=lambda x: x[1]['heat_score'] if 'heat_score' in x[1] else x[1]['risk_pct'],
            reverse=True
        ):
            risk_pct = data['risk_pct']
            size_pct = data['size_pct']
            pnl_pct = data['pnl_pct']

            # Create bar
            bar_length = int((risk_pct / 10) * width) if risk_pct > 0 else 1
            bar = '█' * min(bar_length, width - 20)

            # Color indicator
            if risk_pct > 5:
                indicator = '🔥'
            elif risk_pct > 3:
                indicator = '⚠️ '
            else:
                indicator = '✅'

            line = f"{indicator} {symbol:8s} {bar:20s} Risk: {risk_pct:5.2f}% | Size: {size_pct:5.2f}% | P&L: {pnl_pct:+6.2f}%"
            lines.append(line)

        lines.append("=" * width)

        return "\n".join(lines)


# Global singleton
_visualizer: Optional[RiskVisualizer] = None


def get_visualizer() -> RiskVisualizer:
    """Get or create risk visualizer singleton"""
    global _visualizer
    if _visualizer is None:
        _visualizer = RiskVisualizer()
    return _visualizer
