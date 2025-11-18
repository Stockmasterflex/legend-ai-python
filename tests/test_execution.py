"""
Tests for Intelligent Trade Execution System
"""

import pytest
from datetime import datetime, timedelta
from app.services.execution.algorithms import (
    TWAPAlgorithm,
    VWAPAlgorithm,
    ImplementationShortfallAlgorithm,
    PercentageOfVolumeAlgorithm,
    AlgorithmFactory
)
from app.services.execution.venue_selection import VenueInfo, VenueSelector, SmartRouter
from app.services.execution.order_slicer import OrderSlicer, AdaptiveSlicer, MarketImpactCalculator
from app.services.execution.analytics import ExecutionAnalyzer, Fill, BenchmarkCalculator
from app.services.execution.dark_pool import DarkPoolRouter, DarkPoolVenue, SizeDiscovery
from app.services.execution.execution_service import ExecutionService


class TestExecutionAlgorithms:
    """Test execution algorithms"""

    def test_twap_algorithm(self):
        """Test TWAP algorithm generates correct slices"""
        algo = TWAPAlgorithm(
            ticker="AAPL",
            side="buy",
            total_quantity=1000,
            duration_minutes=60,
            num_slices=10
        )

        slices = algo.generate_slices()

        assert len(slices) == 10
        assert sum(s.quantity for s in slices) == 1000
        assert all(s.quantity > 0 for s in slices)

    def test_vwap_algorithm(self):
        """Test VWAP algorithm generates volume-weighted slices"""
        algo = VWAPAlgorithm(
            ticker="AAPL",
            side="buy",
            total_quantity=1000,
            duration_minutes=60
        )

        slices = algo.generate_slices()

        assert len(slices) > 0
        assert sum(s.quantity for s in slices) <= 1000 * 1.1  # Allow some variance
        assert all(s.quantity > 0 for s in slices)

    def test_implementation_shortfall(self):
        """Test Implementation Shortfall algorithm is front-loaded"""
        algo = ImplementationShortfallAlgorithm(
            ticker="AAPL",
            side="buy",
            total_quantity=1000,
            duration_minutes=60,
            urgency=0.8  # High urgency
        )

        slices = algo.generate_slices()

        # First slice should be larger than last slice for high urgency
        assert len(slices) > 2
        assert slices[0].quantity > slices[-1].quantity

    def test_pov_algorithm(self):
        """Test Percentage of Volume algorithm"""
        algo = PercentageOfVolumeAlgorithm(
            ticker="AAPL",
            side="buy",
            total_quantity=1000,
            duration_minutes=60,
            target_pov=10.0,
            estimated_daily_volume=1000000
        )

        slices = algo.generate_slices()

        assert len(slices) > 0
        total = sum(s.quantity for s in slices)
        assert 950 <= total <= 1050  # Allow some variance

    def test_algorithm_factory(self):
        """Test algorithm factory creates correct types"""
        twap = AlgorithmFactory.create_algorithm(
            "twap", "AAPL", "buy", 1000, 60
        )
        assert isinstance(twap, TWAPAlgorithm)

        vwap = AlgorithmFactory.create_algorithm(
            "vwap", "AAPL", "buy", 1000, 60
        )
        assert isinstance(vwap, VWAPAlgorithm)

        is_algo = AlgorithmFactory.create_algorithm(
            "is", "AAPL", "buy", 1000, 60
        )
        assert isinstance(is_algo, ImplementationShortfallAlgorithm)

        pov = AlgorithmFactory.create_algorithm(
            "pov", "AAPL", "buy", 1000, 60
        )
        assert isinstance(pov, PercentageOfVolumeAlgorithm)

    def test_invalid_algorithm_type(self):
        """Test factory raises error for invalid algorithm"""
        with pytest.raises(ValueError):
            AlgorithmFactory.create_algorithm(
                "invalid", "AAPL", "buy", 1000, 60
            )


class TestVenueSelection:
    """Test venue selection and routing"""

    def get_mock_venues(self):
        """Create mock venues for testing"""
        return [
            VenueInfo(
                venue_id=1, name="Alpaca", venue_type="broker",
                commission_rate=0.0, commission_type="per_share",
                min_commission=0.0, liquidity_score=85.0,
                avg_fill_quality=88.0, supports_dark_pool=False,
                supports_iceberg=True, is_active=True
            ),
            VenueInfo(
                venue_id=2, name="Interactive Brokers", venue_type="broker",
                commission_rate=0.0035, commission_type="per_share",
                min_commission=0.35, liquidity_score=95.0,
                avg_fill_quality=92.0, supports_dark_pool=True,
                supports_iceberg=True, is_active=True
            ),
            VenueInfo(
                venue_id=3, name="Charles Schwab", venue_type="broker",
                commission_rate=0.0, commission_type="per_share",
                min_commission=0.0, liquidity_score=90.0,
                avg_fill_quality=89.0, supports_dark_pool=False,
                supports_iceberg=True, is_active=True
            )
        ]

    def test_venue_selector(self):
        """Test venue selection"""
        selector = VenueSelector()
        venues = self.get_mock_venues()

        best = selector.select_best_venue(
            venues=venues,
            ticker="AAPL",
            quantity=1000,
            price=150.0,
            order_size_category="medium"
        )

        assert best is not None
        assert best.venue.venue_id in [1, 2, 3]
        assert best.total_score > 0

    def test_smart_router_single_venue(self):
        """Test smart router with small order"""
        selector = VenueSelector()
        router = SmartRouter(selector)
        venues = self.get_mock_venues()

        # Small order should go to single venue
        allocations = router.route_order(
            venues=venues,
            ticker="AAPL",
            total_quantity=500,
            price=150.0
        )

        assert len(allocations) == 1
        assert allocations[0][1] == 500

    def test_smart_router_multiple_venues(self):
        """Test smart router with large order"""
        selector = VenueSelector()
        router = SmartRouter(selector)
        venues = self.get_mock_venues()

        # Large order can be split
        allocations = router.route_order(
            venues=venues,
            ticker="AAPL",
            total_quantity=10000,
            price=150.0,
            use_multiple_venues=True,
            max_venues=3
        )

        assert len(allocations) <= 3
        assert sum(qty for _, qty in allocations) == 10000


class TestOrderSlicer:
    """Test order slicing"""

    def test_basic_slicing(self):
        """Test basic order slicing"""
        slicer = OrderSlicer(min_slice_size=100)

        slices = slicer.slice_order(
            total_quantity=1000,
            num_slices=5
        )

        assert len(slices) == 5
        assert sum(slices) == 1000
        assert all(s >= 100 for s in slices)

    def test_iceberg_order(self):
        """Test iceberg order creation"""
        slicer = OrderSlicer()

        clips = slicer.create_iceberg_order(
            total_quantity=5000,
            display_quantity=500
        )

        assert len(clips) > 1
        assert clips[0].display_quantity == 500
        assert clips[0].is_iceberg
        assert sum(c.quantity for c in clips) == 5000

    def test_adaptive_slicer(self):
        """Test adaptive slicing based on market conditions"""
        adaptive = AdaptiveSlicer()

        slices = adaptive.slice_with_market_impact(
            total_quantity=10000,
            avg_daily_volume=1000000,
            current_volatility=0.02,
            spread_bps=5.0
        )

        assert len(slices) > 0
        assert sum(slices) <= 10000 * 1.1  # Allow some variance

    def test_market_impact_calculator(self):
        """Test market impact estimation"""
        impact = MarketImpactCalculator.estimate_impact_bps(
            order_quantity=5000,
            avg_daily_volume=1000000,
            volatility=0.02,
            spread_bps=5.0
        )

        assert impact > 0
        assert impact < 100  # Reasonable range


class TestExecutionAnalytics:
    """Test execution analytics"""

    def get_mock_fills(self):
        """Create mock fills for testing"""
        return [
            Fill(
                fill_id="fill_1",
                timestamp=datetime.now(),
                quantity=300,
                price=150.10,
                venue_name="Alpaca",
                commission=0.0
            ),
            Fill(
                fill_id="fill_2",
                timestamp=datetime.now() + timedelta(minutes=10),
                quantity=400,
                price=150.15,
                venue_name="IB",
                commission=1.40
            ),
            Fill(
                fill_id="fill_3",
                timestamp=datetime.now() + timedelta(minutes=20),
                quantity=300,
                price=150.12,
                venue_name="Schwab",
                commission=0.0
            )
        ]

    def test_execution_analysis(self):
        """Test execution quality analysis"""
        analyzer = ExecutionAnalyzer()
        fills = self.get_mock_fills()

        report = analyzer.analyze_execution(
            order_id="TEST_001",
            ticker="AAPL",
            side="buy",
            total_quantity=1000,
            fills=fills,
            arrival_price=150.00,
            vwap_benchmark=150.10,
            market_volume=100000
        )

        assert report.order_id == "TEST_001"
        assert report.filled_quantity == 1000
        assert report.avg_fill_price > 0
        assert report.slippage_vs_arrival is not None
        assert 0 <= report.overall_quality_score <= 100
        assert report.quality_grade in ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]

    def test_benchmark_calculator(self):
        """Test benchmark calculations"""
        prices = [150.0, 150.5, 150.2, 150.3]
        volumes = [1000, 2000, 1500, 1200]

        vwap = BenchmarkCalculator.calculate_vwap(prices, volumes)
        assert 150.0 <= vwap <= 150.5

        twap = BenchmarkCalculator.calculate_twap(prices)
        assert 150.0 <= twap <= 150.5

    def test_slippage_calculation(self):
        """Test slippage calculation"""
        analyzer = ExecutionAnalyzer()

        # For buy: higher price = positive slippage (bad)
        slippage_buy = analyzer._calculate_slippage_bps(150.10, 150.00, "buy")
        assert slippage_buy > 0

        # For sell: lower price = positive slippage (bad)
        slippage_sell = analyzer._calculate_slippage_bps(149.90, 150.00, "sell")
        assert slippage_sell > 0


class TestDarkPool:
    """Test dark pool routing"""

    def get_mock_dark_pools(self):
        """Create mock dark pools"""
        return [
            DarkPoolVenue(
                venue_id=10, name="Sigma X",
                min_size=100, max_size=None,
                typical_spread_improvement_bps=2.5,
                fill_rate=45.0, avg_fill_time_ms=150.0,
                supports_midpoint_peg=True,
                supports_size_discovery=True,
                is_active=True
            ),
            DarkPoolVenue(
                venue_id=11, name="UBS ATS",
                min_size=100, max_size=50000,
                typical_spread_improvement_bps=2.0,
                fill_rate=38.0, avg_fill_time_ms=200.0,
                supports_midpoint_peg=True,
                supports_size_discovery=False,
                is_active=True
            )
        ]

    def test_dark_pool_routing(self):
        """Test dark pool routing"""
        router = DarkPoolRouter()
        dark_pools = self.get_mock_dark_pools()

        orders = router.route_to_dark_pools(
            ticker="AAPL",
            side="buy",
            quantity=5000,
            limit_price=150.50,
            nbbo_mid=150.45,
            dark_pools=dark_pools,
            strategy="aggressive"
        )

        assert len(orders) > 0
        assert all(o.time_in_force == "IOC" for o in orders)

    def test_size_discovery(self):
        """Test size discovery"""
        discovery = SizeDiscovery()
        dark_pools = self.get_mock_dark_pools()

        discovered = discovery.probe_for_size(
            ticker="AAPL",
            side="buy",
            estimated_size=10000,
            dark_pools=dark_pools,
            nbbo_mid=150.45
        )

        assert len(discovered) > 0
        assert all(size > 0 for size in discovered.values())


class TestExecutionService:
    """Test execution service orchestrator"""

    def test_create_execution_order(self):
        """Test creating execution order"""
        service = ExecutionService()

        result = service.create_execution_order(
            ticker="AAPL",
            side="buy",
            quantity=1000,
            algo_type="twap",
            duration_minutes=60
        )

        assert result["success"] is True
        assert "execution_plan" in result
        assert result["execution_plan"]["num_slices"] > 0

    def test_create_iceberg_order(self):
        """Test creating iceberg order"""
        service = ExecutionService()

        result = service.create_iceberg_order(
            ticker="AAPL",
            side="buy",
            total_quantity=5000,
            display_quantity=500
        )

        assert result["success"] is True
        assert result["total_quantity"] == 5000
        assert result["display_quantity"] == 500
        assert result["hidden_quantity"] == 4500

    def test_get_execution_summary(self):
        """Test getting execution summary"""
        service = ExecutionService()

        summary = service.get_execution_summary()

        assert summary["status"] == "operational"
        assert "algorithms" in summary["capabilities"]
        assert len(summary["capabilities"]["algorithms"]) == 4


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
