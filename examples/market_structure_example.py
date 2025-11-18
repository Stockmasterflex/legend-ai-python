"""
Market Structure Analysis - Example Usage
Demonstrates how to use the market structure analysis module
"""
import asyncio
from datetime import datetime, timedelta
import numpy as np

from app.core.market_structure import (
    OrderBookLevel,
    OrderBookSnapshot,
    TickData,
    MarketStructureAnalyzer,
    OrderBookAnalyzer,
    TickAnalyzer,
    VWAPAnalyzer,
    MarketProfileAnalyzer,
    LiquidityAnalyzer
)
from app.core.market_structure_viz import MarketStructureVisualizer
from app.services.market_data import market_data_service


# ============================================================================
# Example 1: Basic VWAP Analysis
# ============================================================================

async def example_vwap_analysis():
    """
    Example: Analyze VWAP for a stock
    """
    print("=" * 60)
    print("Example 1: VWAP Analysis")
    print("=" * 60)

    # Fetch market data
    symbol = "AAPL"
    data = await market_data_service.get_price_data(symbol, period="1d", interval="5m")

    if data is None or len(data) == 0:
        print(f"No data available for {symbol}")
        return

    # Extract OHLCV
    highs = data['high'].tolist()
    lows = data['low'].tolist()
    closes = data['close'].tolist()
    volumes = data['volume'].tolist()
    timestamps = data.index.tolist()

    # Calculate typical price (HLC/3)
    typical_prices = [(h + l + c) / 3.0 for h, l, c in zip(highs, lows, closes)]

    # Initialize VWAP analyzer
    vwap_analyzer = VWAPAnalyzer()

    # Calculate VWAP
    vwap_levels = vwap_analyzer.calculate_vwap(typical_prices, volumes, timestamps)

    # Add bands
    vwap_levels = vwap_analyzer.calculate_vwap_bands(vwap_levels, closes, std_multiplier=1.0)

    # Analyze price vs VWAP
    stats = vwap_analyzer.analyze_price_vs_vwap(closes, vwap_levels)

    print(f"\nVWAP Analysis for {symbol}:")
    print(f"  Current Position: {stats['current_position']}")
    print(f"  Distance from VWAP: {stats['current_distance_pct']:.2f}%")
    print(f"  Bars Above VWAP: {stats['bars_above_vwap']} ({stats['percentage_above']:.1f}%)")
    print(f"  Bars Below VWAP: {stats['bars_below_vwap']}")
    print(f"  Max Distance Above: {stats['max_distance_above_pct']:.2f}%")
    print(f"  Max Distance Below: {stats['max_distance_below_pct']:.2f}%")

    # Detect mean reversion opportunities
    signals = vwap_analyzer.detect_vwap_mean_reversion(closes, vwap_levels, threshold_std=1.5)

    print(f"\nMean Reversion Signals: {len(signals)}")
    for signal in signals[-3:]:  # Show last 3 signals
        print(f"  - {signal['type']} at {signal['timestamp']} (Distance: {signal['distance_std']:.2f} std)")

    # Visualize
    visualizer = MarketStructureVisualizer()
    fig = visualizer.plot_vwap_analysis(closes, vwap_levels, timestamps)
    # Save or display the figure
    # fig.savefig('vwap_analysis.png')
    print("\n  Visualization created (use fig.savefig() to save)")


# ============================================================================
# Example 2: Market Profile Analysis
# ============================================================================

async def example_market_profile():
    """
    Example: Create and analyze market profile
    """
    print("\n" + "=" * 60)
    print("Example 2: Market Profile Analysis")
    print("=" * 60)

    # Fetch market data
    symbol = "SPY"
    data = await market_data_service.get_price_data(symbol, period="1d", interval="5m")

    if data is None or len(data) == 0:
        print(f"No data available for {symbol}")
        return

    # Extract OHLCV
    highs = data['high'].tolist()
    lows = data['low'].tolist()
    closes = data['close'].tolist()
    volumes = data['volume'].tolist()

    # Initialize analyzer
    mp_analyzer = MarketProfileAnalyzer()

    # Create volume profile
    volume_profile = mp_analyzer.create_volume_profile(
        highs, lows, closes, volumes, price_bins=50
    )

    # Calculate market profile
    market_profile = mp_analyzer.calculate_market_profile(volume_profile, value_area_percentage=0.70)

    print(f"\nMarket Profile for {symbol}:")
    print(f"  Point of Control: ${market_profile.point_of_control:.2f}")
    print(f"  Value Area High: ${market_profile.value_area_high:.2f}")
    print(f"  Value Area Low: ${market_profile.value_area_low:.2f}")
    print(f"  Value Area Range: ${market_profile.value_area_range:.2f}")
    print(f"  Total Volume: {market_profile.total_volume:,.0f}")

    # Analyze session distribution
    distribution = mp_analyzer.analyze_session_distribution(volume_profile, market_profile)

    print(f"\nSession Distribution:")
    print(f"  Session Bias: {distribution['session_bias']}")
    print(f"  Buy/Sell Ratio: {distribution['buy_sell_ratio']:.2f}")
    print(f"  Volume Above POC: {distribution['volume_above_poc_pct']:.1f}%")
    print(f"  Volume in Value Area: {distribution['value_area_percentage']:.1f}%")

    # Visualize
    visualizer = MarketStructureVisualizer()
    fig = visualizer.plot_market_profile(market_profile, current_price=closes[-1])
    print("\n  Visualization created")


# ============================================================================
# Example 3: Order Book Analysis (Simulated)
# ============================================================================

def example_order_book_analysis():
    """
    Example: Analyze order book depth and flow
    Note: Uses simulated order book data
    """
    print("\n" + "=" * 60)
    print("Example 3: Order Book Analysis (Simulated)")
    print("=" * 60)

    # Create simulated order book (in production, fetch from exchange)
    timestamp = datetime.now()

    bids = [
        OrderBookLevel(price=100.00, size=5000, num_orders=10),
        OrderBookLevel(price=99.95, size=3000, num_orders=8),
        OrderBookLevel(price=99.90, size=2000, num_orders=5),
        OrderBookLevel(price=99.85, size=1500, num_orders=4),
        OrderBookLevel(price=99.80, size=1000, num_orders=3),
        OrderBookLevel(price=99.75, size=800, num_orders=2),
        OrderBookLevel(price=99.70, size=600, num_orders=2),
        OrderBookLevel(price=99.65, size=500, num_orders=1),
    ]

    asks = [
        OrderBookLevel(price=100.05, size=4500, num_orders=9),
        OrderBookLevel(price=100.10, size=3500, num_orders=7),
        OrderBookLevel(price=100.15, size=2500, num_orders=6),
        OrderBookLevel(price=100.20, size=2000, num_orders=5),
        OrderBookLevel(price=100.25, size=1500, num_orders=4),
        OrderBookLevel(price=100.30, size=1200, num_orders=3),
        OrderBookLevel(price=100.35, size=1000, num_orders=3),
        OrderBookLevel(price=100.40, size=800, num_orders=2),
    ]

    order_book = OrderBookSnapshot(timestamp=timestamp, bids=bids, asks=asks)

    # Initialize analyzer
    ob_analyzer = OrderBookAnalyzer()

    # Analyze depth
    depth = ob_analyzer.analyze_depth(order_book, levels=5)

    print(f"\nOrder Book Depth (Top 5 Levels):")
    print(f"  Mid Price: ${depth['mid_price']:.2f}")
    print(f"  Spread: ${depth['spread']:.2f}")
    print(f"  Bid Volume: {depth['bid_volume']:,.0f}")
    print(f"  Ask Volume: {depth['ask_volume']:,.0f}")
    print(f"  Volume Imbalance: {depth['volume_imbalance']:.2%}")
    print(f"  Notional Imbalance: {depth['notional_imbalance']:.2%}")

    # Detect large orders
    large_orders = ob_analyzer.detect_large_orders(order_book)

    print(f"\nLarge Orders (>{large_orders['threshold']:,.0f} size):")
    print(f"  Large Bids: {len(large_orders['large_bids'])}")
    for bid in large_orders['large_bids'][:3]:
        print(f"    ${bid.price:.2f} - {bid.size:,.0f}")

    print(f"  Large Asks: {len(large_orders['large_asks'])}")
    for ask in large_orders['large_asks'][:3]:
        print(f"    ${ask.price:.2f} - {ask.size:,.0f}")

    # Visualize
    visualizer = MarketStructureVisualizer()
    fig = visualizer.plot_order_book_depth(order_book, levels=10)
    print("\n  Visualization created")


# ============================================================================
# Example 4: Tick-by-Tick Analysis (Simulated)
# ============================================================================

def example_tick_analysis():
    """
    Example: Analyze tick-by-tick trade data
    Note: Uses simulated tick data
    """
    print("\n" + "=" * 60)
    print("Example 4: Tick-by-Tick Analysis (Simulated)")
    print("=" * 60)

    # Generate simulated tick data
    np.random.seed(42)
    base_time = datetime.now() - timedelta(hours=1)
    ticks = []

    current_price = 100.0
    for i in range(500):
        # Random walk
        change = np.random.randn() * 0.02
        current_price += change

        # Random size with occasional large trades
        if np.random.random() < 0.1:  # 10% chance of large trade
            size = np.random.randint(500, 2000)
        else:
            size = np.random.randint(50, 300)

        # Bias towards buying or selling
        is_buy = np.random.random() > 0.45  # Slight bullish bias

        tick = TickData(
            timestamp=base_time + timedelta(seconds=i),
            price=current_price,
            size=size,
            is_aggressive_buy=is_buy
        )
        ticks.append(tick)

    # Initialize analyzer
    tick_analyzer = TickAnalyzer()

    # Calculate tick ratio
    tick_ratio = tick_analyzer.calculate_tick_ratio(ticks)

    print(f"\nTick Ratio Analysis ({len(ticks)} ticks):")
    print(f"  Upticks: {tick_ratio['upticks']}")
    print(f"  Downticks: {tick_ratio['downticks']}")
    print(f"  Ratio: {tick_ratio['ratio']:.2f}")
    print(f"  Uptick %: {tick_ratio['uptick_percentage']:.1f}%")

    # Analyze trade size distribution
    size_dist = tick_analyzer.analyze_trade_size_distribution(ticks)

    print(f"\nTrade Size Distribution:")
    print(f"  Mean: {size_dist['mean_size']:.0f}")
    print(f"  Median: {size_dist['median_size']:.0f}")
    print(f"  90th Percentile: {size_dist['percentile_90']:.0f}")
    print(f"  95th Percentile: {size_dist['percentile_95']:.0f}")
    print(f"  Max: {size_dist['max_size']:.0f}")

    # Classify fills
    fills = tick_analyzer.classify_fills(ticks)

    print(f"\nFill Classification:")
    print(f"  Aggressive Buy Volume: {fills['aggressive_buy_volume']:,.0f}")
    print(f"  Aggressive Sell Volume: {fills['aggressive_sell_volume']:,.0f}")
    print(f"  Delta: {fills['delta']:+,.0f}")
    print(f"  Delta %: {fills['delta_percentage']:+.2f}%")

    # Detect smart money
    smart_money = tick_analyzer.detect_smart_money(ticks, large_trade_percentile=90)

    print(f"\nSmart Money Detection:")
    print(f"  Signal: {smart_money['smart_money_signal']}")
    print(f"  Large Trades: {smart_money['large_trade_count']}")
    print(f"  Large Buy Volume: {smart_money['large_buy_volume']:,.0f}")
    print(f"  Large Sell Volume: {smart_money['large_sell_volume']:,.0f}")
    print(f"  Imbalance: {smart_money['large_trade_imbalance']:+.2%}")
    print(f"  Clusters Detected: {smart_money['clusters_detected']}")


# ============================================================================
# Example 5: Liquidity Analysis (Simulated)
# ============================================================================

def example_liquidity_analysis():
    """
    Example: Analyze liquidity zones and institutional levels
    """
    print("\n" + "=" * 60)
    print("Example 5: Liquidity Analysis (Simulated)")
    print("=" * 60)

    # Create multiple order book snapshots (simulated)
    order_books = []
    base_time = datetime.now() - timedelta(minutes=30)

    for i in range(20):
        timestamp = base_time + timedelta(minutes=i)

        # Price drifting upward
        base_price = 100.0 + i * 0.1

        bids = [
            OrderBookLevel(price=base_price - 0.05, size=np.random.randint(2000, 5000)),
            OrderBookLevel(price=base_price - 0.10, size=np.random.randint(1500, 3000)),
            OrderBookLevel(price=base_price - 0.15, size=np.random.randint(1000, 2500)),
            OrderBookLevel(price=99.50, size=np.random.randint(3000, 8000)),  # Strong support
            OrderBookLevel(price=99.00, size=np.random.randint(2000, 6000)),  # Strong support
        ]

        asks = [
            OrderBookLevel(price=base_price + 0.05, size=np.random.randint(2000, 5000)),
            OrderBookLevel(price=base_price + 0.10, size=np.random.randint(1500, 3000)),
            OrderBookLevel(price=base_price + 0.15, size=np.random.randint(1000, 2500)),
            OrderBookLevel(price=101.00, size=np.random.randint(4000, 10000)),  # Strong resistance
            OrderBookLevel(price=102.00, size=np.random.randint(3000, 8000)),  # Strong resistance
        ]

        order_books.append(OrderBookSnapshot(timestamp=timestamp, bids=bids, asks=asks))

    # Initialize analyzer
    liq_analyzer = LiquidityAnalyzer()

    # Identify liquidity zones
    liquidity_zones = liq_analyzer.identify_liquidity_zones(order_books, min_zone_size=5000)

    print(f"\nLiquidity Zones (Top 10):")
    for i, zone in enumerate(liquidity_zones[:10], 1):
        print(f"  {i}. ${zone.price_center:.2f} ({zone.zone_type})")
        print(f"     Strength: {zone.strength:.1f}% | Liquidity: {zone.total_liquidity:,.0f}")

    # Detect absorption zones
    absorption_zones = liq_analyzer.detect_absorption_zones(order_books)

    print(f"\nAbsorption Zones: {len(absorption_zones)}")
    for zone in absorption_zones[:5]:
        print(f"  ${zone.price_center:.2f} - Strength: {zone.strength:.1f}%")

    # Identify institutional levels
    institutional_levels = liq_analyzer.identify_institutional_levels(order_books)

    print(f"\nInstitutional Levels:")
    for level in institutional_levels[:5]:
        print(f"  {level['type']}: ${level['price']:.2f} (Strength: {level.get('strength', 0):.1f}%)")


# ============================================================================
# Example 6: Complete Market Structure Analysis
# ============================================================================

async def example_complete_analysis():
    """
    Example: Run complete market structure analysis
    """
    print("\n" + "=" * 60)
    print("Example 6: Complete Market Structure Analysis")
    print("=" * 60)

    # Fetch market data
    symbol = "TSLA"
    data = await market_data_service.get_price_data(symbol, period="1d", interval="5m")

    if data is None or len(data) == 0:
        print(f"No data available for {symbol}")
        return

    # Extract OHLCV
    highs = data['high'].tolist()
    lows = data['low'].tolist()
    closes = data['close'].tolist()
    volumes = data['volume'].tolist()
    timestamps = data.index.tolist()

    # Initialize unified analyzer
    analyzer = MarketStructureAnalyzer()

    # Run complete analysis
    result = analyzer.analyze_complete_structure(
        highs=highs,
        lows=lows,
        closes=closes,
        volumes=volumes,
        timestamps=timestamps
    )

    print(f"\nComplete Market Structure Analysis for {symbol}:")

    # VWAP Summary
    if 'vwap' in result and 'statistics' in result['vwap']:
        stats = result['vwap']['statistics']
        print(f"\n  VWAP:")
        print(f"    Position: {stats['current_position']}")
        print(f"    Distance: {stats['current_distance_pct']:.2f}%")
        print(f"    Mean Reversion Signals: {len(result['vwap'].get('mean_reversion_signals', []))}")

    # Market Profile Summary
    if 'market_profile' in result and 'profile' in result['market_profile']:
        profile = result['market_profile']['profile']
        dist = result['market_profile'].get('distribution', {})
        print(f"\n  Market Profile:")
        print(f"    POC: ${profile.point_of_control:.2f}")
        print(f"    Value Area: ${profile.value_area_low:.2f} - ${profile.value_area_high:.2f}")
        print(f"    Session Bias: {dist.get('session_bias', 'N/A')}")

    # Liquidity Summary
    if 'liquidity' in result:
        zones = result['liquidity'].get('zones', [])
        supply_demand = result['liquidity'].get('supply_demand', {})
        print(f"\n  Liquidity:")
        print(f"    Zones Identified: {len(zones)}")
        print(f"    Market Bias: {supply_demand.get('market_bias', 'N/A')}")

    # Create comprehensive dashboard
    visualizer = MarketStructureVisualizer()
    fig = visualizer.create_comprehensive_dashboard(result, closes, timestamps)
    print("\n  Comprehensive dashboard created")

    return result


# ============================================================================
# Main Execution
# ============================================================================

async def main():
    """
    Run all examples
    """
    print("\n" + "=" * 60)
    print("MARKET STRUCTURE ANALYSIS EXAMPLES")
    print("=" * 60)

    # Run async examples
    await example_vwap_analysis()
    await example_market_profile()

    # Run sync examples
    example_order_book_analysis()
    example_tick_analysis()
    example_liquidity_analysis()

    # Run complete analysis
    await example_complete_analysis()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
