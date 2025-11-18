"""
Comprehensive tests for market structure analysis module
"""
import pytest
from datetime import datetime, timedelta
import numpy as np

from app.core.market_structure import (
    OrderBookLevel,
    OrderBookSnapshot,
    TickData,
    VWAPLevel,
    VolumeProfileLevel,
    MarketProfileResult,
    LiquidityZone,
    OrderBookAnalyzer,
    TickAnalyzer,
    VWAPAnalyzer,
    MarketProfileAnalyzer,
    LiquidityAnalyzer,
    MarketStructureAnalyzer
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def sample_order_book():
    """Create a sample order book snapshot"""
    timestamp = datetime.now()

    bids = [
        OrderBookLevel(price=100.0, size=500, num_orders=5),
        OrderBookLevel(price=99.5, size=300, num_orders=3),
        OrderBookLevel(price=99.0, size=200, num_orders=2),
        OrderBookLevel(price=98.5, size=150, num_orders=2),
        OrderBookLevel(price=98.0, size=100, num_orders=1),
    ]

    asks = [
        OrderBookLevel(price=100.5, size=400, num_orders=4),
        OrderBookLevel(price=101.0, size=350, num_orders=4),
        OrderBookLevel(price=101.5, size=250, num_orders=3),
        OrderBookLevel(price=102.0, size=200, num_orders=2),
        OrderBookLevel(price=102.5, size=150, num_orders=2),
    ]

    return OrderBookSnapshot(timestamp=timestamp, bids=bids, asks=asks)


@pytest.fixture
def sample_order_books():
    """Create multiple order book snapshots over time"""
    base_time = datetime.now()
    order_books = []

    for i in range(10):
        timestamp = base_time + timedelta(seconds=i)

        # Simulate changing order book
        bid_offset = np.random.uniform(-1, 1)
        ask_offset = np.random.uniform(-1, 1)

        bids = [
            OrderBookLevel(price=100.0 + bid_offset, size=500 + i*10, num_orders=5),
            OrderBookLevel(price=99.5 + bid_offset, size=300 + i*5, num_orders=3),
            OrderBookLevel(price=99.0 + bid_offset, size=200, num_orders=2),
        ]

        asks = [
            OrderBookLevel(price=100.5 + ask_offset, size=400 + i*8, num_orders=4),
            OrderBookLevel(price=101.0 + ask_offset, size=350, num_orders=4),
            OrderBookLevel(price=101.5 + ask_offset, size=250, num_orders=3),
        ]

        order_books.append(OrderBookSnapshot(timestamp=timestamp, bids=bids, asks=asks))

    return order_books


@pytest.fixture
def sample_ticks():
    """Create sample tick data"""
    base_time = datetime.now()
    ticks = []

    prices = [100.0, 100.1, 100.2, 100.15, 100.3, 100.25, 100.4, 100.5, 100.45, 100.6]
    sizes = [100, 150, 200, 120, 300, 180, 250, 400, 220, 500]
    is_buy = [True, True, True, False, True, False, True, True, False, True]

    for i in range(len(prices)):
        tick = TickData(
            timestamp=base_time + timedelta(seconds=i),
            price=prices[i],
            size=sizes[i],
            is_aggressive_buy=is_buy[i]
        )
        ticks.append(tick)

    return ticks


@pytest.fixture
def sample_ohlcv():
    """Create sample OHLCV data"""
    np.random.seed(42)
    n_bars = 100

    base_price = 100.0
    prices = base_price + np.cumsum(np.random.randn(n_bars) * 0.5)

    data = {
        'highs': [p + abs(np.random.randn() * 0.3) for p in prices],
        'lows': [p - abs(np.random.randn() * 0.3) for p in prices],
        'closes': prices.tolist(),
        'volumes': [np.random.randint(10000, 100000) for _ in range(n_bars)],
        'timestamps': [datetime.now() + timedelta(minutes=i) for i in range(n_bars)]
    }

    return data


# ============================================================================
# Order Book Analysis Tests
# ============================================================================

class TestOrderBookAnalyzer:
    """Tests for OrderBookAnalyzer"""

    def test_analyze_depth(self, sample_order_book):
        """Test order book depth analysis"""
        analyzer = OrderBookAnalyzer()
        depth = analyzer.analyze_depth(sample_order_book, levels=5)

        assert 'bid_volume' in depth
        assert 'ask_volume' in depth
        assert 'volume_imbalance' in depth
        assert 'spread' in depth
        assert depth['bid_volume'] > 0
        assert depth['ask_volume'] > 0
        assert -1 <= depth['volume_imbalance'] <= 1

    def test_detect_large_orders(self, sample_order_book):
        """Test large order detection"""
        analyzer = OrderBookAnalyzer()
        large_orders = analyzer.detect_large_orders(sample_order_book)

        assert 'large_bids' in large_orders
        assert 'large_asks' in large_orders
        assert 'threshold' in large_orders
        assert isinstance(large_orders['large_bids'], list)
        assert isinstance(large_orders['large_asks'], list)

    def test_identify_support_resistance(self, sample_order_books):
        """Test support/resistance identification"""
        analyzer = OrderBookAnalyzer()
        levels = analyzer.identify_support_resistance(sample_order_books)

        assert 'support' in levels
        assert 'resistance' in levels
        assert isinstance(levels['support'], list)
        assert isinstance(levels['resistance'], list)

    def test_calculate_order_flow_imbalance(self, sample_order_books):
        """Test order flow imbalance calculation"""
        analyzer = OrderBookAnalyzer()
        imbalances = analyzer.calculate_order_flow_imbalance(sample_order_books)

        assert len(imbalances) == len(sample_order_books)
        assert all('volume_imbalance' in imb for imb in imbalances)
        assert all('timestamp' in imb for imb in imbalances)


# ============================================================================
# Tick Analysis Tests
# ============================================================================

class TestTickAnalyzer:
    """Tests for TickAnalyzer"""

    def test_calculate_tick_ratio(self, sample_ticks):
        """Test uptick/downtick ratio calculation"""
        analyzer = TickAnalyzer()
        ratio = analyzer.calculate_tick_ratio(sample_ticks)

        assert 'upticks' in ratio
        assert 'downticks' in ratio
        assert 'ratio' in ratio
        assert 'total_ticks' in ratio
        assert ratio['upticks'] + ratio['downticks'] == ratio['total_ticks']

    def test_analyze_trade_size_distribution(self, sample_ticks):
        """Test trade size distribution analysis"""
        analyzer = TickAnalyzer()
        dist = analyzer.analyze_trade_size_distribution(sample_ticks)

        assert 'mean_size' in dist
        assert 'median_size' in dist
        assert 'std_size' in dist
        assert 'percentile_90' in dist
        assert dist['mean_size'] > 0
        assert dist['median_size'] > 0

    def test_classify_fills(self, sample_ticks):
        """Test aggressive vs passive fill classification"""
        analyzer = TickAnalyzer()
        fills = analyzer.classify_fills(sample_ticks)

        assert 'aggressive_buy_volume' in fills
        assert 'aggressive_sell_volume' in fills
        assert 'delta' in fills
        assert fills['aggressive_buy_volume'] + fills['aggressive_sell_volume'] == fills['total_volume']

    def test_detect_smart_money(self, sample_ticks):
        """Test smart money detection"""
        analyzer = TickAnalyzer()
        smart_money = analyzer.detect_smart_money(sample_ticks)

        assert 'large_trade_count' in smart_money
        assert 'smart_money_signal' in smart_money
        assert smart_money['smart_money_signal'] in ['BULLISH', 'BEARISH', 'NEUTRAL']


# ============================================================================
# VWAP Analysis Tests
# ============================================================================

class TestVWAPAnalyzer:
    """Tests for VWAPAnalyzer"""

    def test_calculate_vwap(self, sample_ohlcv):
        """Test VWAP calculation"""
        analyzer = VWAPAnalyzer()
        typical_prices = [(h + l + c) / 3 for h, l, c in zip(
            sample_ohlcv['highs'],
            sample_ohlcv['lows'],
            sample_ohlcv['closes']
        )]

        vwap_levels = analyzer.calculate_vwap(
            typical_prices,
            sample_ohlcv['volumes'],
            sample_ohlcv['timestamps']
        )

        assert len(vwap_levels) == len(typical_prices)
        assert all(isinstance(level, VWAPLevel) for level in vwap_levels)
        assert all(level.vwap > 0 for level in vwap_levels)

    def test_calculate_vwap_bands(self, sample_ohlcv):
        """Test VWAP bands calculation"""
        analyzer = VWAPAnalyzer()
        typical_prices = [(h + l + c) / 3 for h, l, c in zip(
            sample_ohlcv['highs'],
            sample_ohlcv['lows'],
            sample_ohlcv['closes']
        )]

        vwap_levels = analyzer.calculate_vwap(typical_prices, sample_ohlcv['volumes'])
        vwap_levels = analyzer.calculate_vwap_bands(vwap_levels, sample_ohlcv['closes'])

        # Check that bands are set
        for i, level in enumerate(vwap_levels):
            if i >= 20:  # After minimum window
                assert level.upper_band >= level.vwap
                assert level.lower_band <= level.vwap

    def test_analyze_price_vs_vwap(self, sample_ohlcv):
        """Test price vs VWAP analysis"""
        analyzer = VWAPAnalyzer()
        typical_prices = [(h + l + c) / 3 for h, l, c in zip(
            sample_ohlcv['highs'],
            sample_ohlcv['lows'],
            sample_ohlcv['closes']
        )]

        vwap_levels = analyzer.calculate_vwap(typical_prices, sample_ohlcv['volumes'])
        stats = analyzer.analyze_price_vs_vwap(sample_ohlcv['closes'], vwap_levels)

        assert 'bars_above_vwap' in stats
        assert 'bars_below_vwap' in stats
        assert 'current_position' in stats
        assert stats['current_position'] in ['ABOVE', 'BELOW']

    def test_detect_vwap_mean_reversion(self, sample_ohlcv):
        """Test VWAP mean reversion detection"""
        analyzer = VWAPAnalyzer()
        typical_prices = [(h + l + c) / 3 for h, l, c in zip(
            sample_ohlcv['highs'],
            sample_ohlcv['lows'],
            sample_ohlcv['closes']
        )]

        vwap_levels = analyzer.calculate_vwap(typical_prices, sample_ohlcv['volumes'])
        vwap_levels = analyzer.calculate_vwap_bands(vwap_levels, sample_ohlcv['closes'])

        signals = analyzer.detect_vwap_mean_reversion(sample_ohlcv['closes'], vwap_levels)

        assert isinstance(signals, list)
        for signal in signals:
            assert 'type' in signal
            assert signal['type'] in ['MEAN_REVERSION_LONG', 'MEAN_REVERSION_SHORT']


# ============================================================================
# Market Profile Tests
# ============================================================================

class TestMarketProfileAnalyzer:
    """Tests for MarketProfileAnalyzer"""

    def test_create_volume_profile(self, sample_ohlcv):
        """Test volume profile creation"""
        analyzer = MarketProfileAnalyzer()
        profile = analyzer.create_volume_profile(
            sample_ohlcv['highs'],
            sample_ohlcv['lows'],
            sample_ohlcv['closes'],
            sample_ohlcv['volumes']
        )

        assert len(profile) > 0
        assert all(isinstance(level, VolumeProfileLevel) for level in profile)
        assert all(level.volume > 0 for level in profile)
        assert all(level.buy_volume + level.sell_volume == level.volume for level in profile)

    def test_calculate_market_profile(self, sample_ohlcv):
        """Test market profile calculation"""
        analyzer = MarketProfileAnalyzer()
        volume_profile = analyzer.create_volume_profile(
            sample_ohlcv['highs'],
            sample_ohlcv['lows'],
            sample_ohlcv['closes'],
            sample_ohlcv['volumes']
        )

        market_profile = analyzer.calculate_market_profile(volume_profile)

        assert isinstance(market_profile, MarketProfileResult)
        assert market_profile.point_of_control > 0
        assert market_profile.value_area_high >= market_profile.value_area_low
        assert market_profile.total_volume > 0

    def test_analyze_session_distribution(self, sample_ohlcv):
        """Test session distribution analysis"""
        analyzer = MarketProfileAnalyzer()
        volume_profile = analyzer.create_volume_profile(
            sample_ohlcv['highs'],
            sample_ohlcv['lows'],
            sample_ohlcv['closes'],
            sample_ohlcv['volumes']
        )

        market_profile = analyzer.calculate_market_profile(volume_profile)
        distribution = analyzer.analyze_session_distribution(volume_profile, market_profile)

        assert 'volume_above_poc' in distribution
        assert 'volume_below_poc' in distribution
        assert 'session_bias' in distribution
        assert distribution['session_bias'] in ['BULLISH', 'BEARISH']


# ============================================================================
# Liquidity Analysis Tests
# ============================================================================

class TestLiquidityAnalyzer:
    """Tests for LiquidityAnalyzer"""

    def test_identify_liquidity_zones(self, sample_order_books):
        """Test liquidity zone identification"""
        analyzer = LiquidityAnalyzer()
        zones = analyzer.identify_liquidity_zones(sample_order_books, min_zone_size=100.0)

        assert isinstance(zones, list)
        for zone in zones:
            assert isinstance(zone, LiquidityZone)
            assert zone.total_liquidity >= 100.0
            assert 0 <= zone.strength <= 100

    def test_detect_absorption_zones(self, sample_order_books):
        """Test absorption zone detection"""
        analyzer = LiquidityAnalyzer()
        absorption_zones = analyzer.detect_absorption_zones(sample_order_books)

        assert isinstance(absorption_zones, list)
        for zone in absorption_zones:
            assert zone.zone_type == 'absorption'

    def test_analyze_supply_demand_imbalance(self, sample_ohlcv):
        """Test supply/demand imbalance analysis"""
        # Create volume profile first
        mp_analyzer = MarketProfileAnalyzer()
        volume_profile = mp_analyzer.create_volume_profile(
            sample_ohlcv['highs'],
            sample_ohlcv['lows'],
            sample_ohlcv['closes'],
            sample_ohlcv['volumes']
        )

        analyzer = LiquidityAnalyzer()
        imbalance = analyzer.analyze_supply_demand_imbalance(volume_profile)

        assert 'total_buy_volume' in imbalance
        assert 'total_sell_volume' in imbalance
        assert 'market_bias' in imbalance
        assert imbalance['market_bias'] in ['DEMAND', 'SUPPLY']

    def test_identify_institutional_levels(self, sample_order_books, sample_ticks):
        """Test institutional level identification"""
        analyzer = LiquidityAnalyzer()
        levels = analyzer.identify_institutional_levels(sample_order_books, sample_ticks)

        assert isinstance(levels, list)
        for level in levels:
            assert 'price' in level
            assert 'type' in level
            assert level['type'] in ['ROUND_NUMBER', 'BLOCK_TRADE_CLUSTER']


# ============================================================================
# Unified Market Structure Analyzer Tests
# ============================================================================

class TestMarketStructureAnalyzer:
    """Tests for unified MarketStructureAnalyzer"""

    def test_analyze_complete_structure(self, sample_ohlcv, sample_order_books, sample_ticks):
        """Test complete market structure analysis"""
        analyzer = MarketStructureAnalyzer()

        result = analyzer.analyze_complete_structure(
            highs=sample_ohlcv['highs'],
            lows=sample_ohlcv['lows'],
            closes=sample_ohlcv['closes'],
            volumes=sample_ohlcv['volumes'],
            timestamps=sample_ohlcv['timestamps'],
            order_books=sample_order_books,
            ticks=sample_ticks
        )

        # Verify all major components are present
        assert 'vwap' in result
        assert 'market_profile' in result
        assert 'order_book' in result
        assert 'tick_analysis' in result
        assert 'liquidity' in result

        # Verify VWAP components
        if 'error' not in result['vwap']:
            assert 'levels' in result['vwap']
            assert 'statistics' in result['vwap']

        # Verify Market Profile components
        if 'error' not in result['market_profile']:
            assert 'profile' in result['market_profile']
            assert 'volume_profile' in result['market_profile']

        # Verify Order Book components
        if 'error' not in result['order_book']:
            assert 'depth' in result['order_book']
            assert 'large_orders' in result['order_book']

        # Verify Tick Analysis components
        if 'error' not in result['tick_analysis']:
            assert 'tick_ratio' in result['tick_analysis']
            assert 'smart_money' in result['tick_analysis']

        # Verify Liquidity components
        if 'error' not in result['liquidity']:
            assert 'zones' in result['liquidity']
            assert 'supply_demand' in result['liquidity']

    def test_analyze_without_optional_data(self, sample_ohlcv):
        """Test analysis with only OHLCV data (no order books or ticks)"""
        analyzer = MarketStructureAnalyzer()

        result = analyzer.analyze_complete_structure(
            highs=sample_ohlcv['highs'],
            lows=sample_ohlcv['lows'],
            closes=sample_ohlcv['closes'],
            volumes=sample_ohlcv['volumes'],
            timestamps=sample_ohlcv['timestamps']
        )

        # Should still have VWAP and Market Profile
        assert 'vwap' in result
        assert 'market_profile' in result
        assert 'liquidity' in result

        # Order book and tick analysis should not error (but might be limited)
        assert 'order_book' not in result or result.get('order_book') is None
        assert 'tick_analysis' not in result or result.get('tick_analysis') is None


# ============================================================================
# Edge Cases and Error Handling
# ============================================================================

class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_data_handling(self):
        """Test handling of empty data"""
        analyzer = TickAnalyzer()
        result = analyzer.calculate_tick_ratio([])
        assert result['total_ticks'] == 0

    def test_single_data_point(self):
        """Test handling of single data point"""
        analyzer = VWAPAnalyzer()
        vwap = analyzer.calculate_vwap([100.0], [1000.0])
        assert len(vwap) == 1
        assert vwap[0].vwap == 100.0

    def test_mismatched_array_lengths(self):
        """Test error handling for mismatched array lengths"""
        analyzer = VWAPAnalyzer()

        with pytest.raises(ValueError):
            analyzer.calculate_vwap([100.0, 101.0], [1000.0])  # Different lengths

    def test_zero_volume_handling(self):
        """Test handling of zero volume"""
        analyzer = VWAPAnalyzer()
        # Should handle gracefully
        vwap = analyzer.calculate_vwap([100.0], [0.0])
        assert len(vwap) == 1


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests combining multiple analyzers"""

    def test_full_analysis_pipeline(self, sample_ohlcv, sample_order_books, sample_ticks):
        """Test complete analysis pipeline"""
        # Initialize all analyzers
        ob_analyzer = OrderBookAnalyzer()
        tick_analyzer = TickAnalyzer()
        vwap_analyzer = VWAPAnalyzer()
        mp_analyzer = MarketProfileAnalyzer()
        liq_analyzer = LiquidityAnalyzer()

        # Run all analyses
        ob_depth = ob_analyzer.analyze_depth(sample_order_books[-1])
        tick_ratio = tick_analyzer.calculate_tick_ratio(sample_ticks)

        typical_prices = [(h + l + c) / 3 for h, l, c in zip(
            sample_ohlcv['highs'],
            sample_ohlcv['lows'],
            sample_ohlcv['closes']
        )]
        vwap_levels = vwap_analyzer.calculate_vwap(typical_prices, sample_ohlcv['volumes'])

        volume_profile = mp_analyzer.create_volume_profile(
            sample_ohlcv['highs'],
            sample_ohlcv['lows'],
            sample_ohlcv['closes'],
            sample_ohlcv['volumes']
        )
        market_profile = mp_analyzer.calculate_market_profile(volume_profile)

        liquidity_zones = liq_analyzer.identify_liquidity_zones(sample_order_books)

        # Verify all analyses completed successfully
        assert ob_depth is not None
        assert tick_ratio is not None
        assert len(vwap_levels) > 0
        assert market_profile is not None
        assert isinstance(liquidity_zones, list)

    def test_cross_validation(self, sample_ohlcv):
        """Test cross-validation between different analysis methods"""
        mp_analyzer = MarketProfileAnalyzer()
        vwap_analyzer = VWAPAnalyzer()

        # Create volume profile
        volume_profile = mp_analyzer.create_volume_profile(
            sample_ohlcv['highs'],
            sample_ohlcv['lows'],
            sample_ohlcv['closes'],
            sample_ohlcv['volumes']
        )

        # Calculate VWAP
        typical_prices = [(h + l + c) / 3 for h, l, c in zip(
            sample_ohlcv['highs'],
            sample_ohlcv['lows'],
            sample_ohlcv['closes']
        )]
        vwap_levels = vwap_analyzer.calculate_vwap(typical_prices, sample_ohlcv['volumes'])

        # Both should give reasonable price ranges
        vp_prices = [level.price for level in volume_profile]
        vwap_prices = [level.vwap for level in vwap_levels]

        assert min(vp_prices) <= max(vwap_prices)
        assert max(vp_prices) >= min(vwap_prices)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
