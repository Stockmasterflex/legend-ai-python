"""
Deep Market Structure Analysis Module
Provides advanced order book, tick-by-tick, VWAP, market profile, and liquidity analysis
"""
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


# ============================================================================
# Data Classes for Market Structure Components
# ============================================================================

@dataclass
class OrderBookLevel:
    """Represents a single level in the order book"""
    price: float
    size: float
    num_orders: int = 1

    @property
    def notional_value(self) -> float:
        return self.price * self.size


@dataclass
class OrderBookSnapshot:
    """Complete order book snapshot at a point in time"""
    timestamp: datetime
    bids: List[OrderBookLevel]  # Sorted descending by price
    asks: List[OrderBookLevel]  # Sorted ascending by price

    @property
    def spread(self) -> float:
        """Bid-ask spread"""
        if self.bids and self.asks:
            return self.asks[0].price - self.bids[0].price
        return 0.0

    @property
    def mid_price(self) -> float:
        """Mid price"""
        if self.bids and self.asks:
            return (self.bids[0].price + self.asks[0].price) / 2.0
        return 0.0


@dataclass
class TickData:
    """Individual tick/trade data"""
    timestamp: datetime
    price: float
    size: float
    is_aggressive_buy: bool  # True if aggressor was buyer

    @property
    def direction(self) -> str:
        return "uptick" if self.is_aggressive_buy else "downtick"


@dataclass
class VWAPLevel:
    """VWAP calculation at a point in time"""
    timestamp: datetime
    vwap: float
    upper_band: float
    lower_band: float
    cumulative_volume: float
    cumulative_pv: float  # price * volume


@dataclass
class VolumeProfileLevel:
    """Volume at a specific price level"""
    price: float
    volume: float
    buy_volume: float
    sell_volume: float

    @property
    def delta(self) -> float:
        """Buy volume - sell volume"""
        return self.buy_volume - self.sell_volume

    @property
    def buy_ratio(self) -> float:
        """Ratio of buy volume to total volume"""
        return self.buy_volume / self.volume if self.volume > 0 else 0.5


@dataclass
class MarketProfileResult:
    """Market profile analysis result"""
    point_of_control: float  # Price with highest volume
    value_area_high: float
    value_area_low: float
    volume_profile: List[VolumeProfileLevel]
    total_volume: float

    @property
    def value_area_range(self) -> float:
        return self.value_area_high - self.value_area_low


@dataclass
class LiquidityZone:
    """Identified liquidity zone"""
    price_low: float
    price_high: float
    total_liquidity: float
    zone_type: str  # "support", "resistance", "absorption"
    strength: float  # 0-100

    @property
    def price_center(self) -> float:
        return (self.price_low + self.price_high) / 2.0


# ============================================================================
# Order Book Analysis
# ============================================================================

class OrderBookAnalyzer:
    """Analyzes order book depth and structure"""

    def __init__(self, large_order_threshold_percentile: float = 90.0):
        self.large_order_threshold_percentile = large_order_threshold_percentile

    def analyze_depth(self, order_book: OrderBookSnapshot, levels: int = 10) -> Dict[str, Any]:
        """
        Analyze bid/ask depth

        Args:
            order_book: Order book snapshot
            levels: Number of levels to analyze

        Returns:
            Dict with depth metrics
        """
        bid_depth = order_book.bids[:levels]
        ask_depth = order_book.asks[:levels]

        bid_volume = sum(level.size for level in bid_depth)
        ask_volume = sum(level.size for level in ask_depth)

        bid_notional = sum(level.notional_value for level in bid_depth)
        ask_notional = sum(level.notional_value for level in ask_depth)

        return {
            "bid_volume": bid_volume,
            "ask_volume": ask_volume,
            "bid_notional": bid_notional,
            "ask_notional": ask_notional,
            "volume_imbalance": (bid_volume - ask_volume) / (bid_volume + ask_volume) if (bid_volume + ask_volume) > 0 else 0,
            "notional_imbalance": (bid_notional - ask_notional) / (bid_notional + ask_notional) if (bid_notional + ask_notional) > 0 else 0,
            "spread": order_book.spread,
            "mid_price": order_book.mid_price,
            "levels_analyzed": min(levels, len(bid_depth), len(ask_depth))
        }

    def detect_large_orders(self, order_book: OrderBookSnapshot) -> Dict[str, List[OrderBookLevel]]:
        """
        Detect unusually large orders in the book

        Returns:
            Dict with 'large_bids' and 'large_asks'
        """
        all_sizes = [level.size for level in order_book.bids + order_book.asks]

        if not all_sizes:
            return {"large_bids": [], "large_asks": []}

        threshold = np.percentile(all_sizes, self.large_order_threshold_percentile)

        large_bids = [level for level in order_book.bids if level.size >= threshold]
        large_asks = [level for level in order_book.asks if level.size >= threshold]

        return {
            "large_bids": large_bids,
            "large_asks": large_asks,
            "threshold": threshold
        }

    def identify_support_resistance(
        self,
        order_books: List[OrderBookSnapshot],
        price_tolerance: float = 0.001
    ) -> Dict[str, List[float]]:
        """
        Identify support and resistance levels from order book data

        Args:
            order_books: List of order book snapshots over time
            price_tolerance: Price clustering tolerance (e.g., 0.001 = 0.1%)

        Returns:
            Dict with 'support' and 'resistance' price levels
        """
        # Collect all bid and ask prices with their cumulative sizes
        bid_clusters = defaultdict(float)
        ask_clusters = defaultdict(float)

        for ob in order_books:
            for bid in ob.bids:
                # Round price to create clusters
                cluster_price = round(bid.price / (1 + price_tolerance)) * (1 + price_tolerance)
                bid_clusters[cluster_price] += bid.size

            for ask in ob.asks:
                cluster_price = round(ask.price / (1 + price_tolerance)) * (1 + price_tolerance)
                ask_clusters[cluster_price] += ask.size

        # Sort by volume and get top levels
        support_levels = sorted(bid_clusters.items(), key=lambda x: x[1], reverse=True)[:10]
        resistance_levels = sorted(ask_clusters.items(), key=lambda x: x[1], reverse=True)[:10]

        return {
            "support": [price for price, _ in support_levels],
            "resistance": [price for price, _ in resistance_levels],
            "support_with_size": support_levels,
            "resistance_with_size": resistance_levels
        }

    def calculate_order_flow_imbalance(
        self,
        order_books: List[OrderBookSnapshot],
        window_size: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Calculate order flow imbalance over time

        Args:
            order_books: Time series of order book snapshots
            window_size: Number of levels to analyze

        Returns:
            List of imbalance metrics over time
        """
        results = []

        for ob in order_books:
            depth_analysis = self.analyze_depth(ob, levels=window_size)

            results.append({
                "timestamp": ob.timestamp,
                "volume_imbalance": depth_analysis["volume_imbalance"],
                "notional_imbalance": depth_analysis["notional_imbalance"],
                "spread": depth_analysis["spread"],
                "mid_price": depth_analysis["mid_price"]
            })

        return results


# ============================================================================
# Tick-by-Tick Analysis
# ============================================================================

class TickAnalyzer:
    """Analyzes tick-by-tick trade data"""

    def calculate_tick_ratio(self, ticks: List[TickData]) -> Dict[str, Any]:
        """
        Calculate uptick/downtick ratio

        Args:
            ticks: List of tick data

        Returns:
            Dict with tick statistics
        """
        if not ticks:
            return {
                "upticks": 0,
                "downticks": 0,
                "ratio": 1.0,
                "total_ticks": 0
            }

        upticks = sum(1 for tick in ticks if tick.is_aggressive_buy)
        downticks = len(ticks) - upticks

        return {
            "upticks": upticks,
            "downticks": downticks,
            "ratio": upticks / downticks if downticks > 0 else float('inf'),
            "uptick_percentage": (upticks / len(ticks)) * 100,
            "total_ticks": len(ticks)
        }

    def analyze_trade_size_distribution(self, ticks: List[TickData]) -> Dict[str, Any]:
        """
        Analyze distribution of trade sizes

        Returns:
            Statistical measures of trade sizes
        """
        if not ticks:
            return {}

        sizes = [tick.size for tick in ticks]

        return {
            "mean_size": np.mean(sizes),
            "median_size": np.median(sizes),
            "std_size": np.std(sizes),
            "min_size": np.min(sizes),
            "max_size": np.max(sizes),
            "percentile_25": np.percentile(sizes, 25),
            "percentile_75": np.percentile(sizes, 75),
            "percentile_90": np.percentile(sizes, 90),
            "percentile_95": np.percentile(sizes, 95),
            "total_volume": sum(sizes)
        }

    def classify_fills(self, ticks: List[TickData]) -> Dict[str, Any]:
        """
        Classify trades as aggressive vs passive fills

        Args:
            ticks: List of tick data

        Returns:
            Dict with fill classification
        """
        if not ticks:
            return {}

        aggressive_buy_volume = sum(tick.size for tick in ticks if tick.is_aggressive_buy)
        aggressive_sell_volume = sum(tick.size for tick in ticks if not tick.is_aggressive_buy)
        total_volume = aggressive_buy_volume + aggressive_sell_volume

        return {
            "aggressive_buy_volume": aggressive_buy_volume,
            "aggressive_sell_volume": aggressive_sell_volume,
            "total_volume": total_volume,
            "aggressive_buy_ratio": aggressive_buy_volume / total_volume if total_volume > 0 else 0.5,
            "delta": aggressive_buy_volume - aggressive_sell_volume,
            "delta_percentage": ((aggressive_buy_volume - aggressive_sell_volume) / total_volume * 100) if total_volume > 0 else 0
        }

    def detect_smart_money(
        self,
        ticks: List[TickData],
        large_trade_percentile: float = 90.0,
        min_cluster_size: int = 3
    ) -> Dict[str, Any]:
        """
        Detect potential 'smart money' activity

        Looks for:
        - Large block trades
        - Clustered large trades
        - Aggressive buying/selling in size

        Args:
            ticks: List of tick data
            large_trade_percentile: Percentile threshold for "large" trades
            min_cluster_size: Minimum trades to be considered a cluster

        Returns:
            Dict with smart money indicators
        """
        if not ticks:
            return {}

        sizes = [tick.size for tick in ticks]
        large_threshold = np.percentile(sizes, large_trade_percentile)

        large_trades = [tick for tick in ticks if tick.size >= large_threshold]
        large_buy_volume = sum(tick.size for tick in large_trades if tick.is_aggressive_buy)
        large_sell_volume = sum(tick.size for tick in large_trades if not tick.is_aggressive_buy)

        # Detect clusters of large trades
        clusters = self._detect_trade_clusters(large_trades, time_window_seconds=60)

        return {
            "large_trade_count": len(large_trades),
            "large_trade_threshold": large_threshold,
            "large_buy_volume": large_buy_volume,
            "large_sell_volume": large_sell_volume,
            "large_trade_imbalance": (large_buy_volume - large_sell_volume) / (large_buy_volume + large_sell_volume) if (large_buy_volume + large_sell_volume) > 0 else 0,
            "clusters_detected": len(clusters),
            "clusters": clusters,
            "smart_money_signal": "BULLISH" if large_buy_volume > large_sell_volume * 1.5 else "BEARISH" if large_sell_volume > large_buy_volume * 1.5 else "NEUTRAL"
        }

    def _detect_trade_clusters(
        self,
        trades: List[TickData],
        time_window_seconds: int = 60
    ) -> List[Dict[str, Any]]:
        """Detect clusters of trades within time windows"""
        if not trades:
            return []

        # Sort by timestamp
        sorted_trades = sorted(trades, key=lambda t: t.timestamp)
        clusters = []

        i = 0
        while i < len(sorted_trades):
            cluster_start = sorted_trades[i].timestamp
            cluster_trades = [sorted_trades[i]]

            j = i + 1
            while j < len(sorted_trades):
                time_diff = (sorted_trades[j].timestamp - cluster_start).total_seconds()
                if time_diff <= time_window_seconds:
                    cluster_trades.append(sorted_trades[j])
                    j += 1
                else:
                    break

            if len(cluster_trades) >= 2:
                cluster_volume = sum(t.size for t in cluster_trades)
                cluster_value = sum(t.price * t.size for t in cluster_trades)

                clusters.append({
                    "start_time": cluster_start,
                    "end_time": cluster_trades[-1].timestamp,
                    "trade_count": len(cluster_trades),
                    "total_volume": cluster_volume,
                    "total_value": cluster_value,
                    "avg_price": cluster_value / cluster_volume if cluster_volume > 0 else 0
                })

            i = j if j > i else i + 1

        return clusters


# ============================================================================
# VWAP Analysis
# ============================================================================

class VWAPAnalyzer:
    """Volume-Weighted Average Price analysis"""

    def calculate_vwap(
        self,
        prices: List[float],
        volumes: List[float],
        timestamps: Optional[List[datetime]] = None
    ) -> List[VWAPLevel]:
        """
        Calculate intraday VWAP

        Args:
            prices: Price series (typically typical price: (H+L+C)/3)
            volumes: Volume series
            timestamps: Optional timestamps for each data point

        Returns:
            List of VWAP levels
        """
        if len(prices) != len(volumes):
            raise ValueError("Prices and volumes must have same length")

        results = []
        cumulative_pv = 0.0
        cumulative_volume = 0.0

        for i, (price, volume) in enumerate(zip(prices, volumes)):
            cumulative_pv += price * volume
            cumulative_volume += volume

            vwap = cumulative_pv / cumulative_volume if cumulative_volume > 0 else price

            # Calculate standard deviation bands (will be refined with rolling window)
            upper_band = vwap  # Placeholder
            lower_band = vwap  # Placeholder

            timestamp = timestamps[i] if timestamps and i < len(timestamps) else datetime.now()

            results.append(VWAPLevel(
                timestamp=timestamp,
                vwap=vwap,
                upper_band=upper_band,
                lower_band=lower_band,
                cumulative_volume=cumulative_volume,
                cumulative_pv=cumulative_pv
            ))

        return results

    def calculate_vwap_bands(
        self,
        vwap_levels: List[VWAPLevel],
        prices: List[float],
        std_multiplier: float = 1.0
    ) -> List[VWAPLevel]:
        """
        Add standard deviation bands to VWAP

        Args:
            vwap_levels: VWAP levels from calculate_vwap
            prices: Original price series
            std_multiplier: Standard deviation multiplier for bands

        Returns:
            Updated VWAP levels with bands
        """
        if len(vwap_levels) != len(prices):
            raise ValueError("VWAP levels and prices must have same length")

        for i, level in enumerate(vwap_levels):
            if i < 20:  # Need minimum data for std calculation
                level.upper_band = level.vwap
                level.lower_band = level.vwap
                continue

            # Calculate rolling standard deviation
            window_prices = prices[max(0, i-20):i+1]
            window_vwap = [vwap_levels[j].vwap for j in range(max(0, i-20), i+1)]

            deviations = [p - v for p, v in zip(window_prices, window_vwap)]
            std = np.std(deviations)

            level.upper_band = level.vwap + (std * std_multiplier)
            level.lower_band = level.vwap - (std * std_multiplier)

        return vwap_levels

    def analyze_price_vs_vwap(
        self,
        prices: List[float],
        vwap_levels: List[VWAPLevel]
    ) -> Dict[str, Any]:
        """
        Analyze price behavior relative to VWAP

        Returns:
            Statistics about price vs VWAP
        """
        if len(prices) != len(vwap_levels):
            raise ValueError("Prices and VWAP levels must have same length")

        above_vwap = sum(1 for p, v in zip(prices, vwap_levels) if p > v.vwap)
        below_vwap = len(prices) - above_vwap

        # Calculate distances from VWAP
        distances = [(p - v.vwap) / v.vwap * 100 for p, v in zip(prices, vwap_levels)]

        return {
            "bars_above_vwap": above_vwap,
            "bars_below_vwap": below_vwap,
            "percentage_above": (above_vwap / len(prices)) * 100,
            "avg_distance_pct": np.mean(distances),
            "max_distance_above_pct": max(distances),
            "max_distance_below_pct": min(distances),
            "current_position": "ABOVE" if prices[-1] > vwap_levels[-1].vwap else "BELOW",
            "current_distance_pct": distances[-1]
        }

    def detect_vwap_mean_reversion(
        self,
        prices: List[float],
        vwap_levels: List[VWAPLevel],
        threshold_std: float = 1.5
    ) -> List[Dict[str, Any]]:
        """
        Detect potential mean reversion opportunities

        Args:
            prices: Price series
            vwap_levels: VWAP levels with bands
            threshold_std: Threshold for mean reversion signal (in standard deviations)

        Returns:
            List of mean reversion signals
        """
        signals = []

        for i, (price, vwap) in enumerate(zip(prices, vwap_levels)):
            if i < 1:
                continue

            # Calculate distance from VWAP in terms of band width
            band_width = vwap.upper_band - vwap.lower_band
            if band_width == 0:
                continue

            distance_in_std = (price - vwap.vwap) / (band_width / 2)

            # Detect extreme deviations
            if abs(distance_in_std) >= threshold_std:
                signal_type = "MEAN_REVERSION_SHORT" if distance_in_std > 0 else "MEAN_REVERSION_LONG"

                signals.append({
                    "index": i,
                    "timestamp": vwap.timestamp,
                    "type": signal_type,
                    "price": price,
                    "vwap": vwap.vwap,
                    "distance_std": distance_in_std,
                    "upper_band": vwap.upper_band,
                    "lower_band": vwap.lower_band
                })

        return signals


# ============================================================================
# Market Profile Analysis
# ============================================================================

class MarketProfileAnalyzer:
    """Market Profile and Volume Profile analysis"""

    def create_volume_profile(
        self,
        highs: List[float],
        lows: List[float],
        closes: List[float],
        volumes: List[float],
        ticks: Optional[List[TickData]] = None,
        price_bins: int = 50
    ) -> List[VolumeProfileLevel]:
        """
        Create volume profile by price level

        Args:
            highs, lows, closes: OHLC data
            volumes: Volume data
            ticks: Optional tick data for buy/sell classification
            price_bins: Number of price bins to create

        Returns:
            List of volume profile levels
        """
        if not (len(highs) == len(lows) == len(closes) == len(volumes)):
            raise ValueError("All price/volume arrays must have same length")

        # Determine price range
        all_prices = highs + lows
        min_price = min(all_prices)
        max_price = max(all_prices)

        # Create price bins
        bin_size = (max_price - min_price) / price_bins

        # Initialize volume buckets
        volume_by_price = defaultdict(lambda: {"total": 0.0, "buy": 0.0, "sell": 0.0})

        # Distribute volume across price levels
        for i, (high, low, close, volume) in enumerate(zip(highs, lows, closes, volumes)):
            # Typical price
            typical_price = (high + low + close) / 3.0

            # Find bin
            bin_index = min(int((typical_price - min_price) / bin_size), price_bins - 1)
            bin_price = min_price + (bin_index * bin_size)

            volume_by_price[bin_price]["total"] += volume

            # If we have tick data, use it for buy/sell classification
            # Otherwise, use simplified heuristic
            if close > (high + low) / 2:
                volume_by_price[bin_price]["buy"] += volume * 0.6
                volume_by_price[bin_price]["sell"] += volume * 0.4
            else:
                volume_by_price[bin_price]["buy"] += volume * 0.4
                volume_by_price[bin_price]["sell"] += volume * 0.6

        # Convert to VolumeProfileLevel objects
        profile = []
        for price, vol_data in sorted(volume_by_price.items()):
            profile.append(VolumeProfileLevel(
                price=price,
                volume=vol_data["total"],
                buy_volume=vol_data["buy"],
                sell_volume=vol_data["sell"]
            ))

        return profile

    def calculate_market_profile(
        self,
        volume_profile: List[VolumeProfileLevel],
        value_area_percentage: float = 0.70
    ) -> MarketProfileResult:
        """
        Calculate market profile metrics

        Args:
            volume_profile: Volume profile from create_volume_profile
            value_area_percentage: Percentage of volume for value area (default 70%)

        Returns:
            Market profile result with POC and value area
        """
        if not volume_profile:
            raise ValueError("Volume profile cannot be empty")

        # Find Point of Control (price with highest volume)
        poc_level = max(volume_profile, key=lambda x: x.volume)
        point_of_control = poc_level.price

        # Calculate total volume
        total_volume = sum(level.volume for level in volume_profile)

        # Find Value Area (contains X% of total volume)
        target_volume = total_volume * value_area_percentage

        # Sort by volume to find highest volume levels
        sorted_by_volume = sorted(volume_profile, key=lambda x: x.volume, reverse=True)

        value_area_volume = 0.0
        value_area_prices = []

        for level in sorted_by_volume:
            if value_area_volume < target_volume:
                value_area_volume += level.volume
                value_area_prices.append(level.price)
            else:
                break

        # Value area high/low
        value_area_high = max(value_area_prices) if value_area_prices else point_of_control
        value_area_low = min(value_area_prices) if value_area_prices else point_of_control

        return MarketProfileResult(
            point_of_control=point_of_control,
            value_area_high=value_area_high,
            value_area_low=value_area_low,
            volume_profile=volume_profile,
            total_volume=total_volume
        )

    def analyze_session_distribution(
        self,
        volume_profile: List[VolumeProfileLevel],
        market_profile: MarketProfileResult
    ) -> Dict[str, Any]:
        """
        Analyze volume distribution within session

        Returns:
            Distribution metrics
        """
        total_volume = market_profile.total_volume

        # Volume above/below POC
        volume_above_poc = sum(
            level.volume for level in volume_profile
            if level.price > market_profile.point_of_control
        )
        volume_below_poc = sum(
            level.volume for level in volume_profile
            if level.price < market_profile.point_of_control
        )

        # Volume in/out of value area
        volume_in_value_area = sum(
            level.volume for level in volume_profile
            if market_profile.value_area_low <= level.price <= market_profile.value_area_high
        )
        volume_out_value_area = total_volume - volume_in_value_area

        # Buy/sell distribution
        total_buy_volume = sum(level.buy_volume for level in volume_profile)
        total_sell_volume = sum(level.sell_volume for level in volume_profile)

        return {
            "volume_above_poc": volume_above_poc,
            "volume_below_poc": volume_below_poc,
            "volume_above_poc_pct": (volume_above_poc / total_volume * 100) if total_volume > 0 else 0,
            "volume_in_value_area": volume_in_value_area,
            "volume_out_value_area": volume_out_value_area,
            "value_area_percentage": (volume_in_value_area / total_volume * 100) if total_volume > 0 else 0,
            "total_buy_volume": total_buy_volume,
            "total_sell_volume": total_sell_volume,
            "buy_sell_ratio": total_buy_volume / total_sell_volume if total_sell_volume > 0 else float('inf'),
            "session_bias": "BULLISH" if total_buy_volume > total_sell_volume else "BEARISH"
        }


# ============================================================================
# Liquidity Heatmap Analysis
# ============================================================================

class LiquidityAnalyzer:
    """Analyzes liquidity zones and institutional levels"""

    def identify_liquidity_zones(
        self,
        order_books: List[OrderBookSnapshot],
        min_zone_size: float = 1000.0,
        price_tolerance: float = 0.002
    ) -> List[LiquidityZone]:
        """
        Identify zones of high liquidity

        Args:
            order_books: Historical order book snapshots
            min_zone_size: Minimum cumulative size to be considered a zone
            price_tolerance: Price clustering tolerance

        Returns:
            List of identified liquidity zones
        """
        # Aggregate liquidity by price level
        liquidity_map = defaultdict(float)

        for ob in order_books:
            for bid in ob.bids:
                price_key = round(bid.price / (1 + price_tolerance)) * (1 + price_tolerance)
                liquidity_map[price_key] += bid.size

            for ask in ob.asks:
                price_key = round(ask.price / (1 + price_tolerance)) * (1 + price_tolerance)
                liquidity_map[price_key] += ask.size

        # Identify zones
        zones = []
        sorted_prices = sorted(liquidity_map.keys())

        i = 0
        while i < len(sorted_prices):
            zone_start = sorted_prices[i]
            zone_liquidity = liquidity_map[zone_start]
            zone_end = zone_start

            # Extend zone while prices are close and liquidity is high
            j = i + 1
            while j < len(sorted_prices):
                next_price = sorted_prices[j]
                price_diff_pct = abs(next_price - zone_end) / zone_end

                if price_diff_pct <= price_tolerance and liquidity_map[next_price] >= min_zone_size * 0.3:
                    zone_liquidity += liquidity_map[next_price]
                    zone_end = next_price
                    j += 1
                else:
                    break

            if zone_liquidity >= min_zone_size:
                # Determine zone type based on current price
                if order_books:
                    current_mid = order_books[-1].mid_price
                    if zone_start > current_mid * 1.01:
                        zone_type = "resistance"
                    elif zone_start < current_mid * 0.99:
                        zone_type = "support"
                    else:
                        zone_type = "absorption"
                else:
                    zone_type = "unknown"

                # Calculate strength (relative to max liquidity)
                max_liquidity = max(liquidity_map.values())
                strength = min(100.0, (zone_liquidity / max_liquidity) * 100)

                zones.append(LiquidityZone(
                    price_low=zone_start,
                    price_high=zone_end,
                    total_liquidity=zone_liquidity,
                    zone_type=zone_type,
                    strength=strength
                ))

            i = j if j > i else i + 1

        return sorted(zones, key=lambda z: z.strength, reverse=True)

    def detect_absorption_zones(
        self,
        order_books: List[OrderBookSnapshot],
        volume_threshold_percentile: float = 75.0
    ) -> List[LiquidityZone]:
        """
        Detect price levels where large volume was absorbed

        Args:
            order_books: Historical order book snapshots
            volume_threshold_percentile: Percentile for "large" volume

        Returns:
            List of absorption zones
        """
        # Track volume changes at each price level
        volume_changes = defaultdict(list)

        for i in range(1, len(order_books)):
            prev_ob = order_books[i-1]
            curr_ob = order_books[i]

            # Check for large volume disappearances (absorption)
            prev_bids = {level.price: level.size for level in prev_ob.bids}
            curr_bids = {level.price: level.size for level in curr_ob.bids}

            for price, prev_size in prev_bids.items():
                curr_size = curr_bids.get(price, 0)
                if prev_size > curr_size:
                    absorbed = prev_size - curr_size
                    volume_changes[price].append(absorbed)

        # Find significant absorption levels
        all_absorptions = [sum(changes) for changes in volume_changes.values()]
        if not all_absorptions:
            return []

        threshold = np.percentile(all_absorptions, volume_threshold_percentile)

        absorption_zones = []
        for price, changes in volume_changes.items():
            total_absorbed = sum(changes)
            if total_absorbed >= threshold:
                absorption_zones.append(LiquidityZone(
                    price_low=price * 0.999,
                    price_high=price * 1.001,
                    total_liquidity=total_absorbed,
                    zone_type="absorption",
                    strength=min(100.0, (total_absorbed / max(all_absorptions)) * 100)
                ))

        return sorted(absorption_zones, key=lambda z: z.strength, reverse=True)

    def analyze_supply_demand_imbalance(
        self,
        volume_profile: List[VolumeProfileLevel]
    ) -> Dict[str, Any]:
        """
        Analyze supply/demand imbalances from volume profile

        Args:
            volume_profile: Volume profile by price level

        Returns:
            Supply/demand metrics
        """
        if not volume_profile:
            return {}

        # Find levels with significant buy/sell imbalances
        imbalance_levels = []

        for level in volume_profile:
            imbalance_ratio = level.buy_volume / level.sell_volume if level.sell_volume > 0 else float('inf')

            if imbalance_ratio > 2.0 or imbalance_ratio < 0.5:
                imbalance_levels.append({
                    "price": level.price,
                    "type": "DEMAND" if imbalance_ratio > 1.0 else "SUPPLY",
                    "ratio": imbalance_ratio,
                    "total_volume": level.volume,
                    "delta": level.delta
                })

        # Overall market imbalance
        total_buy = sum(level.buy_volume for level in volume_profile)
        total_sell = sum(level.sell_volume for level in volume_profile)

        return {
            "imbalance_levels": sorted(imbalance_levels, key=lambda x: abs(x["ratio"] - 1.0), reverse=True),
            "total_buy_volume": total_buy,
            "total_sell_volume": total_sell,
            "overall_imbalance": (total_buy - total_sell) / (total_buy + total_sell) if (total_buy + total_sell) > 0 else 0,
            "market_bias": "DEMAND" if total_buy > total_sell else "SUPPLY"
        }

    def identify_institutional_levels(
        self,
        order_books: List[OrderBookSnapshot],
        ticks: Optional[List[TickData]] = None,
        round_number_tolerance: float = 0.0001
    ) -> List[Dict[str, Any]]:
        """
        Identify potential institutional price levels

        Looks for:
        - Round numbers (psychological levels)
        - High liquidity zones
        - Large block trade levels

        Args:
            order_books: Historical order book data
            ticks: Optional tick data for block trade detection
            round_number_tolerance: Tolerance for round number detection

        Returns:
            List of institutional levels
        """
        institutional_levels = []

        # 1. Identify round numbers with high liquidity
        liquidity_zones = self.identify_liquidity_zones(order_books)

        for zone in liquidity_zones:
            price = zone.price_center

            # Check if it's a round number
            for magnitude in [1.0, 5.0, 10.0, 50.0, 100.0]:
                if abs(price % magnitude) / magnitude <= round_number_tolerance:
                    institutional_levels.append({
                        "price": price,
                        "type": "ROUND_NUMBER",
                        "magnitude": magnitude,
                        "liquidity": zone.total_liquidity,
                        "strength": zone.strength,
                        "zone_type": zone.zone_type
                    })
                    break

        # 2. Add high-volume block trade levels
        if ticks:
            smart_money_analyzer = TickAnalyzer()
            smart_money = smart_money_analyzer.detect_smart_money(ticks)

            for cluster in smart_money.get("clusters", []):
                institutional_levels.append({
                    "price": cluster["avg_price"],
                    "type": "BLOCK_TRADE_CLUSTER",
                    "volume": cluster["total_volume"],
                    "value": cluster["total_value"],
                    "trade_count": cluster["trade_count"],
                    "strength": min(100.0, cluster["total_volume"] / 10000 * 100)  # Normalize
                })

        return sorted(institutional_levels, key=lambda x: x.get("strength", 0), reverse=True)


# ============================================================================
# Unified Market Structure Analysis
# ============================================================================

class MarketStructureAnalyzer:
    """
    Unified interface for all market structure analysis
    """

    def __init__(self):
        self.order_book_analyzer = OrderBookAnalyzer()
        self.tick_analyzer = TickAnalyzer()
        self.vwap_analyzer = VWAPAnalyzer()
        self.market_profile_analyzer = MarketProfileAnalyzer()
        self.liquidity_analyzer = LiquidityAnalyzer()

    def analyze_complete_structure(
        self,
        highs: List[float],
        lows: List[float],
        closes: List[float],
        volumes: List[float],
        timestamps: Optional[List[datetime]] = None,
        order_books: Optional[List[OrderBookSnapshot]] = None,
        ticks: Optional[List[TickData]] = None
    ) -> Dict[str, Any]:
        """
        Perform complete market structure analysis

        Args:
            highs, lows, closes: OHLC price data
            volumes: Volume data
            timestamps: Optional timestamps
            order_books: Optional order book data
            ticks: Optional tick data

        Returns:
            Complete market structure analysis
        """
        result = {}

        # 1. VWAP Analysis
        try:
            typical_prices = [(h + l + c) / 3.0 for h, l, c in zip(highs, lows, closes)]
            vwap_levels = self.vwap_analyzer.calculate_vwap(typical_prices, volumes, timestamps)
            vwap_levels = self.vwap_analyzer.calculate_vwap_bands(vwap_levels, closes)

            result["vwap"] = {
                "levels": vwap_levels,
                "statistics": self.vwap_analyzer.analyze_price_vs_vwap(closes, vwap_levels),
                "mean_reversion_signals": self.vwap_analyzer.detect_vwap_mean_reversion(closes, vwap_levels)
            }
        except Exception as e:
            logger.error(f"VWAP analysis failed: {e}")
            result["vwap"] = {"error": str(e)}

        # 2. Market Profile
        try:
            volume_profile = self.market_profile_analyzer.create_volume_profile(
                highs, lows, closes, volumes, ticks
            )
            market_profile = self.market_profile_analyzer.calculate_market_profile(volume_profile)

            result["market_profile"] = {
                "profile": market_profile,
                "volume_profile": volume_profile,
                "distribution": self.market_profile_analyzer.analyze_session_distribution(
                    volume_profile, market_profile
                )
            }
        except Exception as e:
            logger.error(f"Market profile analysis failed: {e}")
            result["market_profile"] = {"error": str(e)}

        # 3. Order Book Analysis (if available)
        if order_books:
            try:
                latest_depth = self.order_book_analyzer.analyze_depth(order_books[-1])
                large_orders = self.order_book_analyzer.detect_large_orders(order_books[-1])
                support_resistance = self.order_book_analyzer.identify_support_resistance(order_books)
                order_flow = self.order_book_analyzer.calculate_order_flow_imbalance(order_books)

                result["order_book"] = {
                    "depth": latest_depth,
                    "large_orders": large_orders,
                    "support_resistance": support_resistance,
                    "order_flow_imbalance": order_flow
                }
            except Exception as e:
                logger.error(f"Order book analysis failed: {e}")
                result["order_book"] = {"error": str(e)}

        # 4. Tick Analysis (if available)
        if ticks:
            try:
                tick_ratio = self.tick_analyzer.calculate_tick_ratio(ticks)
                size_dist = self.tick_analyzer.analyze_trade_size_distribution(ticks)
                fills = self.tick_analyzer.classify_fills(ticks)
                smart_money = self.tick_analyzer.detect_smart_money(ticks)

                result["tick_analysis"] = {
                    "tick_ratio": tick_ratio,
                    "size_distribution": size_dist,
                    "fill_classification": fills,
                    "smart_money": smart_money
                }
            except Exception as e:
                logger.error(f"Tick analysis failed: {e}")
                result["tick_analysis"] = {"error": str(e)}

        # 5. Liquidity Analysis
        try:
            if order_books:
                liquidity_zones = self.liquidity_analyzer.identify_liquidity_zones(order_books)
                absorption_zones = self.liquidity_analyzer.detect_absorption_zones(order_books)
                institutional_levels = self.liquidity_analyzer.identify_institutional_levels(
                    order_books, ticks
                )
            else:
                liquidity_zones = []
                absorption_zones = []
                institutional_levels = []

            # Always analyze supply/demand from volume profile
            volume_profile = result.get("market_profile", {}).get("volume_profile", [])
            supply_demand = self.liquidity_analyzer.analyze_supply_demand_imbalance(volume_profile)

            result["liquidity"] = {
                "zones": liquidity_zones,
                "absorption_zones": absorption_zones,
                "supply_demand": supply_demand,
                "institutional_levels": institutional_levels
            }
        except Exception as e:
            logger.error(f"Liquidity analysis failed: {e}")
            result["liquidity"] = {"error": str(e)}

        return result
