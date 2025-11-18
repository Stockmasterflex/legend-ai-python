"""
Portfolio Heat Monitor
Track portfolio-level risk, concentration, and heat metrics
"""
import logging
import math
from typing import List, Dict, Optional
from collections import defaultdict

from app.core.risk_models import (
    PortfolioPosition,
    PortfolioHeat,
    RiskPyramid,
    RiskVisualization
)

logger = logging.getLogger(__name__)


class PortfolioHeatMonitor:
    """
    Monitor and analyze portfolio-level risk

    Tracks:
    - Total portfolio heat (risk across all positions)
    - Position concentration
    - Sector concentration
    - Correlation-adjusted risk
    - Max drawdown projections
    """

    def __init__(
        self,
        max_portfolio_risk_pct: float = 10.0,
        max_single_position_pct: float = 20.0,
        max_sector_concentration_pct: float = 30.0
    ):
        """
        Initialize portfolio heat monitor

        Args:
            max_portfolio_risk_pct: Max total portfolio risk %
            max_single_position_pct: Max single position size %
            max_sector_concentration_pct: Max sector allocation %
        """
        self.max_portfolio_risk_pct = max_portfolio_risk_pct
        self.max_single_position_pct = max_single_position_pct
        self.max_sector_concentration_pct = max_sector_concentration_pct

    # ========================================================================
    # PORTFOLIO HEAT CALCULATION
    # ========================================================================

    def calculate_portfolio_heat(
        self,
        positions: List[PortfolioPosition],
        cash: float,
        correlation_matrix: Optional[Dict[str, Dict[str, float]]] = None
    ) -> PortfolioHeat:
        """
        Calculate comprehensive portfolio heat metrics

        Args:
            positions: List of open positions
            cash: Available cash
            correlation_matrix: Optional correlation between positions

        Returns:
            PortfolioHeat with all risk metrics
        """

        if not positions:
            # Empty portfolio
            return PortfolioHeat(
                total_account_value=cash,
                total_positions_value=0,
                total_cash=cash,
                total_risk_dollars=0,
                total_risk_percentage=0,
                num_positions=0
            )

        # Calculate totals
        total_positions_value = sum(p.market_value for p in positions)
        total_account_value = total_positions_value + cash
        total_risk_dollars = sum(p.risk_dollars for p in positions)

        # Calculate risk percentage
        if total_account_value > 0:
            total_risk_percentage = (total_risk_dollars / total_account_value) * 100
        else:
            total_risk_percentage = 0

        # Find largest position
        largest_position_value = max((p.market_value for p in positions), default=0)
        largest_position_pct = (largest_position_value / total_account_value * 100) if total_account_value > 0 else 0

        # Find largest risk
        largest_risk = max((p.risk_dollars for p in positions), default=0)
        largest_risk_pct = (largest_risk / total_account_value * 100) if total_account_value > 0 else 0

        # Calculate sector concentration
        sector_concentration = self._calculate_sector_concentration(
            positions, total_account_value
        )

        # Calculate correlation-adjusted risk
        correlation_adjusted_risk = None
        if correlation_matrix:
            correlation_adjusted_risk = self._calculate_correlation_adjusted_risk(
                positions, correlation_matrix, total_account_value
            )

        # Build PortfolioHeat object
        heat = PortfolioHeat(
            total_account_value=total_account_value,
            total_positions_value=total_positions_value,
            total_cash=cash,
            total_risk_dollars=total_risk_dollars,
            total_risk_percentage=total_risk_percentage,
            positions=positions,
            num_positions=len(positions),
            largest_position_pct=largest_position_pct,
            largest_risk_pct=largest_risk_pct,
            sector_concentration=sector_concentration,
            correlation_adjusted_risk=correlation_adjusted_risk,
            max_portfolio_risk_pct=self.max_portfolio_risk_pct,
            max_single_position_pct=self.max_single_position_pct,
            max_sector_concentration_pct=self.max_sector_concentration_pct
        )

        # Calculate heat score
        heat.calculate_heat_score()

        # Check limits
        heat.check_limits()

        return heat

    # ========================================================================
    # SECTOR CONCENTRATION
    # ========================================================================

    def _calculate_sector_concentration(
        self,
        positions: List[PortfolioPosition],
        total_account_value: float
    ) -> Dict[str, float]:
        """Calculate sector concentration percentages"""

        sector_values = defaultdict(float)

        for position in positions:
            sector = position.sector or "Unknown"
            sector_values[sector] += position.market_value

        # Convert to percentages
        sector_pct = {}
        for sector, value in sector_values.items():
            pct = (value / total_account_value * 100) if total_account_value > 0 else 0
            sector_pct[sector] = round(pct, 2)

        return dict(sorted(sector_pct.items(), key=lambda x: x[1], reverse=True))

    # ========================================================================
    # CORRELATION ANALYSIS
    # ========================================================================

    def _calculate_correlation_adjusted_risk(
        self,
        positions: List[PortfolioPosition],
        correlation_matrix: Dict[str, Dict[str, float]],
        total_account_value: float
    ) -> float:
        """
        Calculate portfolio risk adjusted for correlation

        Uses portfolio variance formula:
        σ²_p = Σ w_i² σ_i² + Σ Σ w_i w_j σ_i σ_j ρ_ij

        Simplified version for risk calculation
        """

        if len(positions) < 2:
            # No correlation with single position
            return positions[0].risk_dollars if positions else 0

        # Build risk weights
        symbols = [p.symbol for p in positions]
        risk_amounts = [p.risk_dollars for p in positions]
        weights = [r / sum(risk_amounts) if sum(risk_amounts) > 0 else 0
                  for r in risk_amounts]

        # Calculate variance
        variance = 0.0

        # Individual variances
        for i, (symbol_i, weight_i, risk_i) in enumerate(zip(symbols, weights, risk_amounts)):
            variance += (weight_i ** 2) * (risk_i ** 2)

        # Covariances
        for i, symbol_i in enumerate(symbols):
            for j, symbol_j in enumerate(symbols):
                if i < j:  # Only upper triangle
                    correlation = correlation_matrix.get(symbol_i, {}).get(symbol_j, 0)
                    variance += 2 * weights[i] * weights[j] * risk_amounts[i] * risk_amounts[j] * correlation

        # Standard deviation (adjusted risk)
        adjusted_risk = math.sqrt(abs(variance))

        return adjusted_risk

    # ========================================================================
    # MAX DRAWDOWN PROJECTION
    # ========================================================================

    def project_max_drawdown(
        self,
        positions: List[PortfolioPosition],
        account_value: float,
        scenario: str = "all_stops"  # "all_stops", "50pct_stops", "worst_case"
    ) -> dict:
        """
        Project maximum drawdown under various scenarios

        Args:
            positions: Open positions
            account_value: Total account value
            scenario: "all_stops", "50pct_stops", "worst_case"

        Returns:
            Drawdown projections
        """

        total_risk = sum(p.risk_dollars for p in positions)

        scenarios = {}

        # Scenario 1: All positions hit stops
        all_stops_loss = total_risk
        all_stops_pct = (all_stops_loss / account_value * 100) if account_value > 0 else 0
        scenarios['all_stops'] = {
            'loss_dollars': all_stops_loss,
            'loss_percentage': all_stops_pct,
            'remaining_capital': account_value - all_stops_loss,
            'description': 'All positions hit stop loss'
        }

        # Scenario 2: 50% of positions hit stops
        half_stops_loss = total_risk * 0.5
        half_stops_pct = (half_stops_loss / account_value * 100) if account_value > 0 else 0
        scenarios['50pct_stops'] = {
            'loss_dollars': half_stops_loss,
            'loss_percentage': half_stops_pct,
            'remaining_capital': account_value - half_stops_loss,
            'description': '50% of positions hit stop loss'
        }

        # Scenario 3: Worst case (double the stop distance)
        worst_case_loss = total_risk * 2  # Stops fail, double loss
        worst_case_pct = (worst_case_loss / account_value * 100) if account_value > 0 else 0
        scenarios['worst_case'] = {
            'loss_dollars': worst_case_loss,
            'loss_percentage': worst_case_pct,
            'remaining_capital': max(0, account_value - worst_case_loss),
            'description': 'Stops fail - double normal risk (disaster scenario)'
        }

        return {
            'current_account_value': account_value,
            'total_risk_dollars': total_risk,
            'total_risk_percentage': (total_risk / account_value * 100) if account_value > 0 else 0,
            'scenarios': scenarios,
            'recommendation': self._get_drawdown_recommendation(all_stops_pct)
        }

    def _get_drawdown_recommendation(self, drawdown_pct: float) -> str:
        """Get recommendation based on projected drawdown"""
        if drawdown_pct < 5:
            return "✅ Conservative risk - well protected"
        elif drawdown_pct < 10:
            return "✅ Moderate risk - acceptable exposure"
        elif drawdown_pct < 15:
            return "⚠️ Elevated risk - consider reducing positions"
        else:
            return "❌ High risk - reduce exposure immediately"

    # ========================================================================
    # RISK VISUALIZATION DATA
    # ========================================================================

    def generate_visualization_data(
        self,
        heat: PortfolioHeat
    ) -> RiskVisualization:
        """
        Generate data for risk visualizations

        Creates data for:
        - Position size comparison
        - Heat map by ticker
        - Risk distribution
        - Risk pyramid
        """

        # Position sizes
        position_sizes = {
            p.symbol: p.market_value for p in heat.positions
        }

        # Position risks
        position_risks = {
            p.symbol: p.risk_dollars for p in heat.positions
        }

        # Heat map data
        heat_map = {}
        for p in heat.positions:
            if heat.total_account_value > 0:
                risk_pct = (p.risk_dollars / heat.total_account_value) * 100
                size_pct = (p.market_value / heat.total_account_value) * 100
            else:
                risk_pct = 0
                size_pct = 0

            heat_map[p.symbol] = {
                'risk_pct': round(risk_pct, 2),
                'size_pct': round(size_pct, 2),
                'pnl_pct': round(p.pnl_percentage, 2)
            }

        # Risk distribution
        risk_distribution = {
            'position_risk': (heat.total_risk_dollars / heat.total_account_value * 100) if heat.total_account_value > 0 else 0,
            'cash': (heat.total_cash / heat.total_account_value * 100) if heat.total_account_value > 0 else 100,
            'unrealized_pnl': sum((p.unrealized_pnl / heat.total_account_value * 100) if heat.total_account_value > 0 else 0 for p in heat.positions)
        }

        # Risk pyramid
        pyramid = self._build_risk_pyramid(heat.positions)

        # Chart data for plotting
        chart_data = {
            'symbols': [p.symbol for p in heat.positions],
            'position_values': [p.market_value for p in heat.positions],
            'risk_values': [p.risk_dollars for p in heat.positions],
            'pnl_values': [p.unrealized_pnl for p in heat.positions],
            'sectors': [p.sector or 'Unknown' for p in heat.positions]
        }

        return RiskVisualization(
            position_sizes=position_sizes,
            position_risks=position_risks,
            heat_map=heat_map,
            risk_distribution=risk_distribution,
            pyramid=pyramid,
            chart_data=chart_data
        )

    def _build_risk_pyramid(
        self,
        positions: List[PortfolioPosition]
    ) -> RiskPyramid:
        """
        Build risk pyramid: 40% conservative, 40% moderate, 20% aggressive

        Based on risk/reward and position size
        """

        # Sort by risk (ascending)
        sorted_positions = sorted(positions, key=lambda p: p.risk_dollars)

        total_positions = len(sorted_positions)

        # Allocate to tiers
        tier1_count = int(total_positions * 0.4)
        tier2_count = int(total_positions * 0.4)

        tier1 = [p.symbol for p in sorted_positions[:tier1_count]]
        tier2 = [p.symbol for p in sorted_positions[tier1_count:tier1_count + tier2_count]]
        tier3 = [p.symbol for p in sorted_positions[tier1_count + tier2_count:]]

        return RiskPyramid(
            tier1_conservative=tier1,
            tier2_moderate=tier2,
            tier3_aggressive=tier3
        )

    # ========================================================================
    # POSITION HEAT LIMITS
    # ========================================================================

    def check_position_heat_limit(
        self,
        new_position_value: float,
        current_portfolio_value: float,
        max_position_pct: float = 20.0
    ) -> dict:
        """
        Check if adding a new position would exceed heat limits

        Args:
            new_position_value: Dollar value of new position
            current_portfolio_value: Current total portfolio value
            max_position_pct: Max % for single position

        Returns:
            Dict with approval status and details
        """

        total_value = current_portfolio_value + new_position_value
        position_pct = (new_position_value / total_value * 100) if total_value > 0 else 0

        approved = position_pct <= max_position_pct

        return {
            'approved': approved,
            'position_percentage': round(position_pct, 2),
            'max_allowed_percentage': max_position_pct,
            'position_value': new_position_value,
            'total_portfolio_value': total_value,
            'message': (
                f"✅ Position approved: {position_pct:.1f}% of portfolio"
                if approved else
                f"❌ Position too large: {position_pct:.1f}% exceeds {max_position_pct}% limit"
            )
        }

    def suggest_position_reduction(
        self,
        heat: PortfolioHeat,
        target_risk_pct: float = 8.0
    ) -> dict:
        """
        Suggest which positions to reduce to meet target risk

        Args:
            heat: Current portfolio heat
            target_risk_pct: Target total risk percentage

        Returns:
            Reduction suggestions
        """

        if heat.total_risk_percentage <= target_risk_pct:
            return {
                'action_needed': False,
                'current_risk': heat.total_risk_percentage,
                'target_risk': target_risk_pct,
                'message': '✅ Portfolio risk within target'
            }

        # Calculate reduction needed
        excess_risk = heat.total_risk_percentage - target_risk_pct
        excess_dollars = (excess_risk / 100) * heat.total_account_value

        # Sort positions by risk (largest first)
        sorted_positions = sorted(
            heat.positions,
            key=lambda p: p.risk_dollars,
            reverse=True
        )

        # Suggest reducing largest positions first
        suggestions = []
        remaining_reduction = excess_dollars

        for position in sorted_positions:
            if remaining_reduction <= 0:
                break

            reduction_amount = min(position.risk_dollars * 0.5, remaining_reduction)  # Max 50% reduction
            new_shares = int(position.shares * (1 - reduction_amount / position.risk_dollars))

            suggestions.append({
                'symbol': position.symbol,
                'current_shares': position.shares,
                'suggested_shares': new_shares,
                'reduction_shares': position.shares - new_shares,
                'risk_reduction': reduction_amount
            })

            remaining_reduction -= reduction_amount

        return {
            'action_needed': True,
            'current_risk': heat.total_risk_percentage,
            'target_risk': target_risk_pct,
            'excess_risk_pct': excess_risk,
            'excess_risk_dollars': excess_dollars,
            'suggestions': suggestions,
            'message': f'⚠️ Reduce {len(suggestions)} position(s) to meet {target_risk_pct}% target'
        }


# Global singleton
_heat_monitor: Optional[PortfolioHeatMonitor] = None


def get_heat_monitor(
    max_portfolio_risk_pct: float = 10.0,
    max_single_position_pct: float = 20.0,
    max_sector_concentration_pct: float = 30.0
) -> PortfolioHeatMonitor:
    """Get or create portfolio heat monitor singleton"""
    global _heat_monitor
    if _heat_monitor is None:
        _heat_monitor = PortfolioHeatMonitor(
            max_portfolio_risk_pct,
            max_single_position_pct,
            max_sector_concentration_pct
        )
    return _heat_monitor
