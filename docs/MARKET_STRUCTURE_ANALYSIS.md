# Market Structure Analysis

Comprehensive deep market structure analysis module for Legend AI Python. This module provides advanced order book, tick-by-tick, VWAP, market profile, and liquidity analysis capabilities.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Components](#components)
  - [Order Book Analysis](#order-book-analysis)
  - [Tick-by-Tick Analysis](#tick-by-tick-analysis)
  - [VWAP Analysis](#vwap-analysis)
  - [Market Profile](#market-profile)
  - [Liquidity Analysis](#liquidity-analysis)
- [Visualization](#visualization)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Best Practices](#best-practices)

## Overview

The Market Structure Analysis module provides institutional-grade market microstructure analysis tools. It helps traders and analysts understand:

- **Order book dynamics** - Bid/ask depth, large orders, support/resistance levels, order flow imbalance
- **Tick data patterns** - Uptick/downtick ratios, trade size distributions, smart money detection
- **VWAP behavior** - Intraday VWAP, bands, mean reversion opportunities
- **Market profile** - Volume profile by price, point of control, value area
- **Liquidity zones** - Where liquidity sits, absorption zones, institutional levels

## Features

### 1. Order Book Visualization

- **Depth Analysis**: Analyze bid/ask depth across multiple levels
- **Large Order Detection**: Identify unusually large orders in the book
- **Support/Resistance**: Extract support/resistance from order book clustering
- **Order Flow Imbalance**: Track imbalances between bid and ask side

### 2. Tick-by-Tick Analysis

- **Uptick/Downtick Ratio**: Calculate buying vs selling pressure
- **Trade Size Distribution**: Analyze distribution of trade sizes
- **Aggressive vs Passive Fills**: Classify trades by aggressor side
- **Smart Money Detection**: Identify institutional trading patterns

### 3. VWAP Analysis

- **Intraday VWAP**: Calculate volume-weighted average price
- **VWAP Bands**: Standard deviation bands around VWAP
- **Above/Below Statistics**: Price behavior relative to VWAP
- **Mean Reversion**: Detect mean reversion opportunities

### 4. Market Profile

- **Volume Profile**: Volume distribution by price level
- **Point of Control**: Price level with highest volume
- **Value Area**: Range containing 70% of volume
- **Session Distribution**: Buy/sell volume analysis

### 5. Liquidity Heatmap

- **Liquidity Zones**: Identify areas of high liquidity
- **Absorption Zones**: Detect where large volume was absorbed
- **Supply/Demand Imbalances**: Analyze buying vs selling pressure
- **Institutional Levels**: Identify round numbers and block trade levels

## Installation

The module is included in the Legend AI Python package. No additional installation required.

```python
from app.core.market_structure import MarketStructureAnalyzer
from app.core.market_structure_viz import MarketStructureVisualizer
```

## Quick Start

### Basic VWAP Analysis

```python
from app.core.market_structure import VWAPAnalyzer

# Prepare data
typical_prices = [(h + l + c) / 3 for h, l, c in zip(highs, lows, closes)]

# Initialize analyzer
vwap_analyzer = VWAPAnalyzer()

# Calculate VWAP
vwap_levels = vwap_analyzer.calculate_vwap(typical_prices, volumes, timestamps)

# Add bands
vwap_levels = vwap_analyzer.calculate_vwap_bands(vwap_levels, closes)

# Analyze
stats = vwap_analyzer.analyze_price_vs_vwap(closes, vwap_levels)
print(f"Position: {stats['current_position']}")
print(f"Distance: {stats['current_distance_pct']:.2f}%")
```

### Complete Market Structure Analysis

```python
from app.core.market_structure import MarketStructureAnalyzer

# Initialize
analyzer = MarketStructureAnalyzer()

# Run complete analysis
result = analyzer.analyze_complete_structure(
    highs=highs,
    lows=lows,
    closes=closes,
    volumes=volumes,
    timestamps=timestamps
)

# Access results
vwap_stats = result['vwap']['statistics']
market_profile = result['market_profile']['profile']
liquidity_zones = result['liquidity']['zones']
```

## Components

### Order Book Analysis

The `OrderBookAnalyzer` provides tools to analyze order book depth and structure.

#### Key Methods

**`analyze_depth(order_book, levels=10)`**
- Analyzes bid/ask depth
- Returns volume and notional imbalances
- Calculates spread and mid price

**`detect_large_orders(order_book)`**
- Detects unusually large orders
- Uses percentile-based thresholds
- Returns large bids and asks

**`identify_support_resistance(order_books)`**
- Identifies support/resistance from order clustering
- Tracks price levels with high cumulative size
- Returns top support and resistance levels

**`calculate_order_flow_imbalance(order_books)`**
- Tracks order flow imbalance over time
- Monitors changes in bid/ask balance
- Returns time series of imbalance metrics

#### Example

```python
from app.core.market_structure import OrderBookAnalyzer, OrderBookSnapshot, OrderBookLevel

# Create order book
bids = [OrderBookLevel(price=100.0, size=5000, num_orders=10), ...]
asks = [OrderBookLevel(price=100.5, size=4500, num_orders=9), ...]
order_book = OrderBookSnapshot(timestamp=datetime.now(), bids=bids, asks=asks)

# Analyze
analyzer = OrderBookAnalyzer()
depth = analyzer.analyze_depth(order_book)

print(f"Volume Imbalance: {depth['volume_imbalance']:.2%}")
print(f"Spread: ${depth['spread']:.2f}")
```

### Tick-by-Tick Analysis

The `TickAnalyzer` analyzes individual trades to detect patterns and smart money activity.

#### Key Methods

**`calculate_tick_ratio(ticks)`**
- Calculates uptick/downtick ratio
- Measures buying vs selling pressure
- Returns tick statistics

**`analyze_trade_size_distribution(ticks)`**
- Analyzes distribution of trade sizes
- Calculates percentiles and statistics
- Identifies size patterns

**`classify_fills(ticks)`**
- Classifies aggressive vs passive fills
- Calculates volume delta
- Determines buy/sell pressure

**`detect_smart_money(ticks)`**
- Detects large block trades
- Identifies trade clustering
- Generates smart money signal

#### Example

```python
from app.core.market_structure import TickAnalyzer, TickData

# Analyze ticks
analyzer = TickAnalyzer()
smart_money = analyzer.detect_smart_money(ticks)

print(f"Signal: {smart_money['smart_money_signal']}")
print(f"Large Trades: {smart_money['large_trade_count']}")
print(f"Clusters: {smart_money['clusters_detected']}")
```

### VWAP Analysis

The `VWAPAnalyzer` calculates and analyzes Volume-Weighted Average Price.

#### Key Methods

**`calculate_vwap(prices, volumes, timestamps)`**
- Calculates intraday VWAP
- Supports cumulative calculation
- Returns VWAP levels

**`calculate_vwap_bands(vwap_levels, prices, std_multiplier=1.0)`**
- Adds standard deviation bands
- Configurable band width
- Returns updated VWAP levels

**`analyze_price_vs_vwap(prices, vwap_levels)`**
- Analyzes price behavior vs VWAP
- Calculates percentage above/below
- Returns statistical measures

**`detect_vwap_mean_reversion(prices, vwap_levels, threshold_std=1.5)`**
- Detects mean reversion opportunities
- Identifies extreme deviations
- Returns trading signals

#### Example

```python
from app.core.market_structure import VWAPAnalyzer

analyzer = VWAPAnalyzer()

# Calculate VWAP
typical_prices = [(h + l + c) / 3 for h, l, c in zip(highs, lows, closes)]
vwap_levels = analyzer.calculate_vwap(typical_prices, volumes)
vwap_levels = analyzer.calculate_vwap_bands(vwap_levels, closes)

# Detect signals
signals = analyzer.detect_vwap_mean_reversion(closes, vwap_levels)
for signal in signals:
    print(f"{signal['type']} at {signal['price']:.2f}")
```

### Market Profile

The `MarketProfileAnalyzer` creates volume profiles and identifies key price levels.

#### Key Methods

**`create_volume_profile(highs, lows, closes, volumes, price_bins=50)`**
- Creates volume profile by price
- Distributes volume across price levels
- Classifies buy/sell volume

**`calculate_market_profile(volume_profile, value_area_percentage=0.70)`**
- Calculates Point of Control (POC)
- Identifies Value Area High/Low
- Returns complete market profile

**`analyze_session_distribution(volume_profile, market_profile)`**
- Analyzes volume distribution
- Calculates buy/sell ratios
- Determines session bias

#### Example

```python
from app.core.market_structure import MarketProfileAnalyzer

analyzer = MarketProfileAnalyzer()

# Create volume profile
volume_profile = analyzer.create_volume_profile(highs, lows, closes, volumes)

# Calculate market profile
market_profile = analyzer.calculate_market_profile(volume_profile)

print(f"POC: ${market_profile.point_of_control:.2f}")
print(f"Value Area: ${market_profile.value_area_low:.2f} - ${market_profile.value_area_high:.2f}")
```

### Liquidity Analysis

The `LiquidityAnalyzer` identifies liquidity zones and institutional levels.

#### Key Methods

**`identify_liquidity_zones(order_books, min_zone_size=1000.0)`**
- Identifies high liquidity zones
- Clusters nearby price levels
- Returns ranked zones

**`detect_absorption_zones(order_books)`**
- Detects price levels where volume was absorbed
- Tracks order book changes
- Identifies institutional activity

**`analyze_supply_demand_imbalance(volume_profile)`**
- Analyzes buy/sell imbalances
- Identifies supply/demand zones
- Returns market bias

**`identify_institutional_levels(order_books, ticks)`**
- Identifies round number levels
- Detects block trade levels
- Returns institutional price levels

#### Example

```python
from app.core.market_structure import LiquidityAnalyzer

analyzer = LiquidityAnalyzer()

# Identify liquidity zones
zones = analyzer.identify_liquidity_zones(order_books)

for zone in zones[:5]:
    print(f"{zone.zone_type}: ${zone.price_center:.2f} (Strength: {zone.strength:.1f}%)")
```

## Visualization

The `MarketStructureVisualizer` provides comprehensive visualization tools.

### Available Visualizations

1. **Order Book Depth** - Bid/ask depth visualization
2. **Order Flow Imbalance** - Imbalance over time
3. **VWAP Analysis** - Price with VWAP bands
4. **Volume Profile** - Volume by price level
5. **Market Profile** - POC and value area
6. **Liquidity Heatmap** - Liquidity zones
7. **Tick Analysis** - Tick statistics
8. **Comprehensive Dashboard** - All-in-one view

### Example

```python
from app.core.market_structure_viz import MarketStructureVisualizer

visualizer = MarketStructureVisualizer()

# Create VWAP chart
fig = visualizer.plot_vwap_analysis(closes, vwap_levels, timestamps)
fig.savefig('vwap_analysis.png')

# Create comprehensive dashboard
fig = visualizer.create_comprehensive_dashboard(result, closes, timestamps)
fig.savefig('market_structure_dashboard.png')
```

## API Reference

### Data Classes

#### `OrderBookLevel`
```python
@dataclass
class OrderBookLevel:
    price: float
    size: float
    num_orders: int = 1
```

#### `OrderBookSnapshot`
```python
@dataclass
class OrderBookSnapshot:
    timestamp: datetime
    bids: List[OrderBookLevel]
    asks: List[OrderBookLevel]
```

#### `TickData`
```python
@dataclass
class TickData:
    timestamp: datetime
    price: float
    size: float
    is_aggressive_buy: bool
```

#### `VWAPLevel`
```python
@dataclass
class VWAPLevel:
    timestamp: datetime
    vwap: float
    upper_band: float
    lower_band: float
    cumulative_volume: float
    cumulative_pv: float
```

#### `VolumeProfileLevel`
```python
@dataclass
class VolumeProfileLevel:
    price: float
    volume: float
    buy_volume: float
    sell_volume: float
```

#### `MarketProfileResult`
```python
@dataclass
class MarketProfileResult:
    point_of_control: float
    value_area_high: float
    value_area_low: float
    volume_profile: List[VolumeProfileLevel]
    total_volume: float
```

#### `LiquidityZone`
```python
@dataclass
class LiquidityZone:
    price_low: float
    price_high: float
    total_liquidity: float
    zone_type: str  # "support", "resistance", "absorption"
    strength: float  # 0-100
```

## Examples

See `examples/market_structure_example.py` for comprehensive examples including:

1. Basic VWAP Analysis
2. Market Profile Analysis
3. Order Book Analysis
4. Tick-by-Tick Analysis
5. Liquidity Analysis
6. Complete Market Structure Analysis

## Best Practices

### 1. Data Quality

- Use high-quality, tick-level data when available
- Ensure timestamps are properly synchronized
- Filter out outliers and erroneous data

### 2. Time Frames

- VWAP is most useful for intraday analysis
- Market Profile works best on daily or session data
- Order book analysis requires real-time or near-real-time data

### 3. Parameter Tuning

- Adjust percentile thresholds for large order detection
- Tune VWAP band multipliers based on volatility
- Set appropriate minimum zone sizes for liquidity analysis

### 4. Performance

- Use caching for repeated analyses
- Batch process multiple symbols when possible
- Consider using asyncio for concurrent processing

### 5. Interpretation

- Combine multiple indicators for confirmation
- Consider market context (trending vs ranging)
- Use liquidity zones for entry/exit planning
- Monitor order flow for trend confirmation

## Testing

Run the comprehensive test suite:

```bash
pytest tests/test_market_structure.py -v
```

## Contributing

When contributing to the market structure module:

1. Add comprehensive tests for new features
2. Update documentation
3. Include usage examples
4. Ensure backward compatibility
5. Follow existing code style

## License

Part of Legend AI Python - See main project license.

## Support

For questions or issues:
- Check the examples directory
- Review test cases for usage patterns
- Consult the API reference above
