"""
Tests for Advanced Risk Management System
"""
import pytest
from datetime import datetime

from app.services.advanced_risk_manager import AdvancedRiskManager
from app.services.portfolio_heat_monitor import PortfolioHeatMonitor
from app.services.risk_visualizer import RiskVisualizer
from app.core.risk_models import PortfolioPosition, VolatilityRegime


class TestAdvancedRiskManager:
    """Test advanced risk manager"""

    def setup_method(self):
        self.manager = AdvancedRiskManager()

    # ========================================================================
    # KELLY CRITERION TESTS
    # ========================================================================

    def test_kelly_criterion_basic(self):
        """Test Kelly Criterion with profitable system"""
        result = self.manager.calculate_kelly_criterion(
            account_size=100000,
            win_rate=0.6,
            avg_win_dollars=500,
            avg_loss_dollars=300,
            kelly_fraction="half",
            entry_price=100,
            stop_loss=98
        )

        assert result.kelly_percentage > 0
        assert result.adjusted_percentage < result.kelly_percentage
        assert result.kelly_fraction == "half"
        assert result.position_size > 0
        assert result.edge > 0
        assert len(result.notes) > 0

    def test_kelly_criterion_no_edge(self):
        """Test Kelly with no positive edge"""
        result = self.manager.calculate_kelly_criterion(
            account_size=100000,
            win_rate=0.4,  # Low win rate
            avg_win_dollars=300,
            avg_loss_dollars=500,  # Losses bigger than wins
            kelly_fraction="half"
        )

        assert result.kelly_percentage <= 0
        assert result.position_size == 0
        assert "No positive edge" in result.notes[0]

    def test_kelly_fractions(self):
        """Test different Kelly fractions"""
        base_result = self.manager.calculate_kelly_criterion(
            account_size=100000,
            win_rate=0.6,
            avg_win_dollars=500,
            avg_loss_dollars=300,
            kelly_fraction="full"
        )

        half_result = self.manager.calculate_kelly_criterion(
            account_size=100000,
            win_rate=0.6,
            avg_win_dollars=500,
            avg_loss_dollars=300,
            kelly_fraction="half"
        )

        quarter_result = self.manager.calculate_kelly_criterion(
            account_size=100000,
            win_rate=0.6,
            avg_win_dollars=500,
            avg_loss_dollars=300,
            kelly_fraction="quarter"
        )

        # Verify fractions are correct
        assert abs(half_result.adjusted_percentage - base_result.adjusted_percentage / 2) < 0.01
        assert abs(quarter_result.adjusted_percentage - base_result.adjusted_percentage / 4) < 0.01

    # ========================================================================
    # FIXED FRACTIONAL TESTS
    # ========================================================================

    def test_fixed_fractional_basic(self):
        """Test basic fixed fractional sizing"""
        result = self.manager.calculate_fixed_fractional(
            account_size=100000,
            entry_price=100,
            stop_loss=98,
            risk_percentage=0.02
        )

        assert result.risk_percentage == 2.0
        assert result.position_size > 0
        assert result.position_dollars == result.position_size * 100
        assert result.risk_dollars == 100000 * 0.02

    def test_fixed_fractional_correlation_adjustment(self):
        """Test correlation adjustment reduces position size"""
        base_result = self.manager.calculate_fixed_fractional(
            account_size=100000,
            entry_price=100,
            stop_loss=98,
            risk_percentage=0.02,
            correlation_adjustment=1.0
        )

        adjusted_result = self.manager.calculate_fixed_fractional(
            account_size=100000,
            entry_price=100,
            stop_loss=98,
            risk_percentage=0.02,
            correlation_adjustment=0.5  # 50% correlated
        )

        assert adjusted_result.position_size < base_result.position_size
        assert adjusted_result.position_size == base_result.position_size // 2

    def test_fixed_fractional_position_heat(self):
        """Test position heat calculation"""
        result = self.manager.calculate_fixed_fractional(
            account_size=100000,
            entry_price=1000,  # High price
            stop_loss=900,
            risk_percentage=0.02
        )

        expected_heat = (result.position_dollars / 100000) * 100
        assert abs(result.position_heat - expected_heat) < 0.01

    # ========================================================================
    # VOLATILITY-BASED TESTS
    # ========================================================================

    def test_volatility_based_atr(self):
        """Test ATR-based position sizing"""
        result = self.manager.calculate_volatility_based(
            account_size=100000,
            entry_price=100,
            atr=2.0,
            atr_multiplier=2.0,
            risk_percentage=0.02
        )

        assert result.atr == 2.0
        assert result.stop_distance == 4.0  # 2.0 * 2.0
        assert result.position_size > 0

    def test_volatility_regime_low_vix(self):
        """Test low volatility regime increases position size"""
        result = self.manager.calculate_volatility_based(
            account_size=100000,
            entry_price=100,
            atr=2.0,
            vix=12.0  # Low VIX
        )

        assert result.volatility_regime == VolatilityRegime.LOW
        assert result.volatility_adjustment == 1.2

    def test_volatility_regime_high_vix(self):
        """Test high volatility regime reduces position size"""
        result = self.manager.calculate_volatility_based(
            account_size=100000,
            entry_price=100,
            atr=2.0,
            vix=40.0  # High VIX
        )

        assert result.volatility_regime == VolatilityRegime.HIGH
        assert result.volatility_adjustment == 0.5

    # ========================================================================
    # DYNAMIC SCALING TESTS
    # ========================================================================

    def test_dynamic_scaling_high_confidence(self):
        """Test dynamic scaling with high confidence"""
        result = self.manager.calculate_dynamic_scaling(
            account_size=100000,
            entry_price=100,
            stop_loss=98,
            confidence_score=90,
            market_regime="bull"
        )

        # High confidence + bull market should increase size
        assert result.risk_percentage > 2.0

    def test_dynamic_scaling_low_confidence(self):
        """Test dynamic scaling with low confidence"""
        result = self.manager.calculate_dynamic_scaling(
            account_size=100000,
            entry_price=100,
            stop_loss=98,
            confidence_score=30,
            market_regime="bear"
        )

        # Low confidence + bear market should reduce size
        assert result.risk_percentage < 2.0

    # ========================================================================
    # COMPARISON TESTS
    # ========================================================================

    def test_compare_methods(self):
        """Test method comparison"""
        results = self.manager.compare_methods(
            account_size=100000,
            entry_price=100,
            stop_loss=98,
            win_rate=0.6,
            avg_win=500,
            avg_loss=300,
            atr=2.0,
            vix=20.0
        )

        assert 'fixed_2pct' in results
        assert 'fixed_1pct' in results
        assert 'kelly_half' in results
        assert 'kelly_quarter' in results
        assert 'atr_based' in results


class TestPortfolioHeatMonitor:
    """Test portfolio heat monitor"""

    def setup_method(self):
        self.monitor = PortfolioHeatMonitor()

    def get_sample_positions(self):
        """Create sample positions for testing"""
        return [
            PortfolioPosition(
                symbol="AAPL",
                shares=100,
                entry_price=150,
                current_price=155,
                stop_loss=145,
                target=165,
                entry_date=datetime(2024, 1, 1),
                sector="Technology"
            ),
            PortfolioPosition(
                symbol="MSFT",
                shares=50,
                entry_price=300,
                current_price=310,
                stop_loss=290,
                target=330,
                entry_date=datetime(2024, 1, 2),
                sector="Technology"
            ),
            PortfolioPosition(
                symbol="JPM",
                shares=200,
                entry_price=150,
                current_price=148,
                stop_loss=145,
                target=160,
                entry_date=datetime(2024, 1, 3),
                sector="Finance"
            )
        ]

    def test_portfolio_heat_basic(self):
        """Test basic portfolio heat calculation"""
        positions = self.get_sample_positions()
        heat = self.monitor.calculate_portfolio_heat(
            positions=positions,
            cash=50000
        )

        assert heat.num_positions == 3
        assert heat.total_account_value > 0
        assert heat.total_risk_dollars > 0
        assert heat.total_risk_percentage > 0
        assert heat.heat_score >= 0

    def test_empty_portfolio(self):
        """Test empty portfolio"""
        heat = self.monitor.calculate_portfolio_heat(
            positions=[],
            cash=100000
        )

        assert heat.num_positions == 0
        assert heat.total_risk_dollars == 0
        assert heat.total_risk_percentage == 0
        assert heat.heat_score == 0

    def test_sector_concentration(self):
        """Test sector concentration calculation"""
        positions = self.get_sample_positions()
        heat = self.monitor.calculate_portfolio_heat(
            positions=positions,
            cash=50000
        )

        assert "Technology" in heat.sector_concentration
        assert "Finance" in heat.sector_concentration
        assert heat.sector_concentration["Technology"] > 0

    def test_heat_score_calculation(self):
        """Test heat score calculation"""
        positions = self.get_sample_positions()
        heat = self.monitor.calculate_portfolio_heat(
            positions=positions,
            cash=50000
        )

        heat_score = heat.calculate_heat_score()
        assert 0 <= heat_score <= 100

    def test_risk_limits_warning(self):
        """Test risk limit warnings"""
        # Create high-risk portfolio
        positions = [
            PortfolioPosition(
                symbol=f"STOCK{i}",
                shares=1000,
                entry_price=100,
                current_price=100,
                stop_loss=90,
                target=120,
                entry_date=datetime(2024, 1, 1),
                sector="Technology"
            )
            for i in range(10)
        ]

        heat = self.monitor.calculate_portfolio_heat(
            positions=positions,
            cash=10000,
            max_portfolio_risk_pct=10.0
        )

        warnings = heat.check_limits()
        # Should have warnings due to high risk
        assert len(warnings) > 0 or heat.is_overheated

    def test_max_drawdown_projection(self):
        """Test max drawdown projection"""
        positions = self.get_sample_positions()

        projection = self.monitor.project_max_drawdown(
            positions=positions,
            account_value=100000,
            scenario="all_stops"
        )

        assert 'scenarios' in projection
        assert 'all_stops' in projection['scenarios']
        assert 'worst_case' in projection['scenarios']
        assert projection['total_risk_dollars'] > 0

    def test_position_heat_limit_check(self):
        """Test position heat limit check"""
        result = self.monitor.check_position_heat_limit(
            new_position_value=10000,
            current_portfolio_value=100000,
            max_position_pct=20.0
        )

        assert result['approved'] == True
        assert result['position_percentage'] < 20.0

        # Test exceeding limit
        result = self.monitor.check_position_heat_limit(
            new_position_value=50000,
            current_portfolio_value=100000,
            max_position_pct=20.0
        )

        assert result['approved'] == False

    def test_suggest_position_reduction(self):
        """Test position reduction suggestions"""
        positions = self.get_sample_positions()
        heat = self.monitor.calculate_portfolio_heat(
            positions=positions,
            cash=50000
        )

        suggestion = self.monitor.suggest_position_reduction(
            heat=heat,
            target_risk_pct=5.0
        )

        assert 'action_needed' in suggestion
        assert 'suggestions' in suggestion


class TestRiskVisualizer:
    """Test risk visualizer"""

    def setup_method(self):
        self.visualizer = RiskVisualizer()
        self.monitor = PortfolioHeatMonitor()

    def get_sample_heat(self):
        """Get sample portfolio heat for testing"""
        positions = [
            PortfolioPosition(
                symbol="AAPL",
                shares=100,
                entry_price=150,
                current_price=155,
                stop_loss=145,
                target=165,
                entry_date=datetime(2024, 1, 1),
                sector="Technology"
            ),
            PortfolioPosition(
                symbol="MSFT",
                shares=50,
                entry_price=300,
                current_price=310,
                stop_loss=290,
                target=330,
                entry_date=datetime(2024, 1, 2),
                sector="Technology"
            )
        ]

        heat = self.monitor.calculate_portfolio_heat(positions, 50000)
        viz_data = self.monitor.generate_visualization_data(heat)

        return heat, viz_data

    def test_risk_pyramid_chart(self):
        """Test risk pyramid chart generation"""
        heat, viz_data = self.get_sample_heat()
        chart = self.visualizer.generate_risk_pyramid_chart(viz_data)

        assert chart['type'] == 'pyramid'
        assert 'tiers' in chart
        assert len(chart['tiers']) == 3

    def test_position_size_chart(self):
        """Test position size chart generation"""
        heat, viz_data = self.get_sample_heat()
        chart = self.visualizer.generate_position_size_chart(viz_data, 'value')

        assert chart['type'] == 'horizontal_bar'
        assert len(chart['labels']) > 0
        assert len(chart['data']) > 0

    def test_heat_map_chart(self):
        """Test heat map chart generation"""
        heat, viz_data = self.get_sample_heat()
        chart = self.visualizer.generate_heat_map_chart(viz_data)

        assert chart['type'] == 'heat_map'
        assert 'matrix_data' in chart

    def test_heat_gauge(self):
        """Test heat gauge generation"""
        heat, viz_data = self.get_sample_heat()
        gauge = self.visualizer.generate_heat_gauge(heat)

        assert gauge['type'] == 'gauge'
        assert 0 <= gauge['value'] <= 100
        assert 'status' in gauge

    def test_sector_concentration_chart(self):
        """Test sector concentration chart"""
        heat, viz_data = self.get_sample_heat()
        chart = self.visualizer.generate_sector_concentration_chart(heat)

        assert chart['type'] == 'horizontal_bar'
        assert 'labels' in chart

    def test_risk_dashboard(self):
        """Test complete dashboard generation"""
        heat, viz_data = self.get_sample_heat()
        dashboard = self.visualizer.generate_risk_dashboard(heat, viz_data)

        assert 'summary' in dashboard
        assert 'charts' in dashboard
        assert 'limits' in dashboard
        assert 'positions' in dashboard
        assert len(dashboard['positions']) > 0

    def test_text_heat_map(self):
        """Test ASCII heat map generation"""
        heat, viz_data = self.get_sample_heat()
        text_map = self.visualizer.generate_text_heat_map(viz_data)

        assert isinstance(text_map, str)
        assert len(text_map) > 0
        assert "PORTFOLIO HEAT MAP" in text_map


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
