"""
Market Structure Visualization Utilities
Provides visualization functions for market structure analysis
"""
from typing import List, Dict, Any, Optional, Tuple
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
import numpy as np
from datetime import datetime
import io
import base64

from app.core.market_structure import (
    OrderBookSnapshot,
    VWAPLevel,
    VolumeProfileLevel,
    MarketProfileResult,
    LiquidityZone
)


class MarketStructureVisualizer:
    """Visualization tools for market structure analysis"""

    def __init__(self, style: str = 'dark_background'):
        """
        Initialize visualizer

        Args:
            style: Matplotlib style ('dark_background', 'seaborn', 'ggplot', etc.)
        """
        self.style = style
        plt.style.use(style)

    def plot_order_book_depth(
        self,
        order_book: OrderBookSnapshot,
        levels: int = 20,
        figsize: Tuple[int, int] = (12, 6)
    ) -> Figure:
        """
        Visualize order book depth

        Args:
            order_book: Order book snapshot
            levels: Number of levels to display
            figsize: Figure size

        Returns:
            Matplotlib figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

        # Get bid/ask data
        bids = order_book.bids[:levels]
        asks = order_book.asks[:levels]

        bid_prices = [b.price for b in bids]
        bid_sizes = [b.size for b in bids]
        bid_cumulative = np.cumsum(bid_sizes)

        ask_prices = [a.price for a in asks]
        ask_sizes = [a.size for a in asks]
        ask_cumulative = np.cumsum(ask_sizes)

        # Plot 1: Individual levels
        ax1.barh(bid_prices, bid_sizes, color='green', alpha=0.6, label='Bids')
        ax1.barh(ask_prices, [-s for s in ask_sizes], color='red', alpha=0.6, label='Asks')
        ax1.axhline(order_book.mid_price, color='yellow', linestyle='--', linewidth=2, label=f'Mid: ${order_book.mid_price:.2f}')
        ax1.set_xlabel('Size')
        ax1.set_ylabel('Price')
        ax1.set_title('Order Book Depth')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Plot 2: Cumulative depth
        ax2.plot(bid_cumulative, bid_prices, color='green', linewidth=2, label='Cumulative Bids')
        ax2.plot(ask_cumulative, ask_prices, color='red', linewidth=2, label='Cumulative Asks')
        ax2.axhline(order_book.mid_price, color='yellow', linestyle='--', linewidth=2, label=f'Mid: ${order_book.mid_price:.2f}')
        ax2.set_xlabel('Cumulative Size')
        ax2.set_ylabel('Price')
        ax2.set_title('Cumulative Depth')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_order_flow_imbalance(
        self,
        imbalance_data: List[Dict[str, Any]],
        figsize: Tuple[int, int] = (14, 8)
    ) -> Figure:
        """
        Plot order flow imbalance over time

        Args:
            imbalance_data: List of imbalance metrics from OrderBookAnalyzer
            figsize: Figure size

        Returns:
            Matplotlib figure
        """
        fig, axes = plt.subplots(3, 1, figsize=figsize, sharex=True)

        timestamps = [d['timestamp'] for d in imbalance_data]
        volume_imb = [d['volume_imbalance'] for d in imbalance_data]
        notional_imb = [d['notional_imbalance'] for d in imbalance_data]
        spreads = [d['spread'] for d in imbalance_data]

        # Plot 1: Volume Imbalance
        colors = ['green' if x > 0 else 'red' for x in volume_imb]
        axes[0].bar(timestamps, volume_imb, color=colors, alpha=0.7)
        axes[0].axhline(0, color='white', linestyle='--', linewidth=1)
        axes[0].set_ylabel('Volume Imbalance')
        axes[0].set_title('Order Flow Imbalance Analysis')
        axes[0].grid(True, alpha=0.3)

        # Plot 2: Notional Imbalance
        colors = ['green' if x > 0 else 'red' for x in notional_imb]
        axes[1].bar(timestamps, notional_imb, color=colors, alpha=0.7)
        axes[1].axhline(0, color='white', linestyle='--', linewidth=1)
        axes[1].set_ylabel('Notional Imbalance')
        axes[1].grid(True, alpha=0.3)

        # Plot 3: Spread
        axes[2].plot(timestamps, spreads, color='cyan', linewidth=2)
        axes[2].fill_between(timestamps, spreads, alpha=0.3, color='cyan')
        axes[2].set_ylabel('Spread ($)')
        axes[2].set_xlabel('Time')
        axes[2].grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_vwap_analysis(
        self,
        prices: List[float],
        vwap_levels: List[VWAPLevel],
        timestamps: Optional[List[datetime]] = None,
        figsize: Tuple[int, int] = (14, 8)
    ) -> Figure:
        """
        Plot VWAP with bands and price action

        Args:
            prices: Price series
            vwap_levels: VWAP levels with bands
            timestamps: Optional timestamps
            figsize: Figure size

        Returns:
            Matplotlib figure
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True, height_ratios=[3, 1])

        x_axis = timestamps if timestamps else range(len(prices))
        vwaps = [v.vwap for v in vwap_levels]
        upper_bands = [v.upper_band for v in vwap_levels]
        lower_bands = [v.lower_band for v in vwap_levels]

        # Plot 1: Price and VWAP
        ax1.plot(x_axis, prices, color='white', linewidth=2, label='Price', alpha=0.9)
        ax1.plot(x_axis, vwaps, color='yellow', linewidth=2, label='VWAP')
        ax1.plot(x_axis, upper_bands, color='red', linewidth=1, linestyle='--', alpha=0.7, label='Upper Band')
        ax1.plot(x_axis, lower_bands, color='green', linewidth=1, linestyle='--', alpha=0.7, label='Lower Band')

        # Fill between bands
        ax1.fill_between(x_axis, upper_bands, lower_bands, alpha=0.2, color='gray')

        # Highlight areas above/below VWAP
        for i in range(len(prices)):
            if prices[i] > vwaps[i]:
                ax1.scatter(x_axis[i], prices[i], color='green', s=10, alpha=0.3)
            else:
                ax1.scatter(x_axis[i], prices[i], color='red', s=10, alpha=0.3)

        ax1.set_ylabel('Price')
        ax1.set_title('VWAP Analysis with Bands')
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)

        # Plot 2: Distance from VWAP
        distances = [(p - v.vwap) / v.vwap * 100 for p, v in zip(prices, vwap_levels)]
        colors = ['green' if d > 0 else 'red' for d in distances]
        ax2.bar(x_axis, distances, color=colors, alpha=0.7)
        ax2.axhline(0, color='white', linestyle='--', linewidth=1)
        ax2.set_ylabel('Distance from VWAP (%)')
        ax2.set_xlabel('Time')
        ax2.grid(True, alpha=0.3)

        if timestamps:
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            plt.xticks(rotation=45)

        plt.tight_layout()
        return fig

    def plot_volume_profile(
        self,
        volume_profile: List[VolumeProfileLevel],
        current_price: Optional[float] = None,
        figsize: Tuple[int, int] = (10, 12)
    ) -> Figure:
        """
        Plot volume profile by price level

        Args:
            volume_profile: Volume profile data
            current_price: Optional current price to highlight
            figsize: Figure size

        Returns:
            Matplotlib figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

        prices = [level.price for level in volume_profile]
        volumes = [level.volume for level in volume_profile]
        buy_volumes = [level.buy_volume for level in volume_profile]
        sell_volumes = [level.sell_volume for level in volume_profile]

        # Plot 1: Total volume profile
        ax1.barh(prices, volumes, color='blue', alpha=0.6)
        if current_price:
            ax1.axhline(current_price, color='yellow', linestyle='--', linewidth=2, label=f'Current: ${current_price:.2f}')
        ax1.set_xlabel('Volume')
        ax1.set_ylabel('Price')
        ax1.set_title('Volume Profile')
        if current_price:
            ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Plot 2: Buy/Sell volume breakdown
        ax2.barh(prices, buy_volumes, color='green', alpha=0.6, label='Buy Volume')
        ax2.barh(prices, [-v for v in sell_volumes], color='red', alpha=0.6, label='Sell Volume')
        if current_price:
            ax2.axhline(current_price, color='yellow', linestyle='--', linewidth=2)
        ax2.set_xlabel('Volume (Buy/Sell)')
        ax2.set_ylabel('Price')
        ax2.set_title('Buy/Sell Volume Profile')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_market_profile(
        self,
        market_profile: MarketProfileResult,
        current_price: Optional[float] = None,
        figsize: Tuple[int, int] = (12, 10)
    ) -> Figure:
        """
        Plot market profile with POC and value area

        Args:
            market_profile: Market profile result
            current_price: Optional current price
            figsize: Figure size

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=figsize)

        prices = [level.price for level in market_profile.volume_profile]
        volumes = [level.volume for level in market_profile.volume_profile]

        # Plot volume profile
        ax.barh(prices, volumes, color='cyan', alpha=0.5, label='Volume')

        # Highlight Point of Control
        poc_volume = next(
            (level.volume for level in market_profile.volume_profile if level.price == market_profile.point_of_control),
            0
        )
        ax.barh([market_profile.point_of_control], [poc_volume], color='yellow', alpha=0.8, label='Point of Control')

        # Highlight Value Area
        value_area_prices = [
            level.price for level in market_profile.volume_profile
            if market_profile.value_area_low <= level.price <= market_profile.value_area_high
        ]
        value_area_volumes = [
            level.volume for level in market_profile.volume_profile
            if market_profile.value_area_low <= level.price <= market_profile.value_area_high
        ]
        ax.barh(value_area_prices, value_area_volumes, color='orange', alpha=0.3, label='Value Area')

        # Add horizontal lines for value area boundaries
        ax.axhline(market_profile.value_area_high, color='orange', linestyle='--', linewidth=2, label=f'VAH: ${market_profile.value_area_high:.2f}')
        ax.axhline(market_profile.value_area_low, color='orange', linestyle='--', linewidth=2, label=f'VAL: ${market_profile.value_area_low:.2f}')

        # Current price
        if current_price:
            ax.axhline(current_price, color='white', linestyle='-', linewidth=2, label=f'Current: ${current_price:.2f}')

        ax.set_xlabel('Volume')
        ax.set_ylabel('Price')
        ax.set_title('Market Profile Analysis')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def plot_liquidity_heatmap(
        self,
        liquidity_zones: List[LiquidityZone],
        price_range: Optional[Tuple[float, float]] = None,
        figsize: Tuple[int, int] = (12, 10)
    ) -> Figure:
        """
        Plot liquidity heatmap showing zones of high liquidity

        Args:
            liquidity_zones: List of liquidity zones
            price_range: Optional (min_price, max_price) for y-axis
            figsize: Figure size

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=figsize)

        # Sort zones by price
        sorted_zones = sorted(liquidity_zones, key=lambda z: z.price_center)

        # Color mapping based on zone type
        color_map = {
            'support': 'green',
            'resistance': 'red',
            'absorption': 'yellow',
            'unknown': 'gray'
        }

        for zone in sorted_zones:
            color = color_map.get(zone.zone_type, 'gray')
            alpha = min(0.8, zone.strength / 100)

            # Draw rectangle for the zone
            height = zone.price_high - zone.price_low
            width = zone.total_liquidity

            ax.barh(
                zone.price_low,
                width,
                height=height,
                color=color,
                alpha=alpha,
                edgecolor='white',
                linewidth=0.5
            )

            # Add label for strong zones
            if zone.strength > 70:
                ax.text(
                    width * 0.5,
                    zone.price_center,
                    f'{zone.zone_type.upper()}\n{zone.strength:.0f}%',
                    ha='center',
                    va='center',
                    fontsize=8,
                    color='white',
                    weight='bold'
                )

        ax.set_xlabel('Liquidity')
        ax.set_ylabel('Price')
        ax.set_title('Liquidity Heatmap')

        if price_range:
            ax.set_ylim(price_range)

        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='green', alpha=0.6, label='Support'),
            Patch(facecolor='red', alpha=0.6, label='Resistance'),
            Patch(facecolor='yellow', alpha=0.6, label='Absorption')
        ]
        ax.legend(handles=legend_elements, loc='best')
        ax.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        return fig

    def plot_tick_analysis(
        self,
        ticks_data: Dict[str, Any],
        figsize: Tuple[int, int] = (14, 10)
    ) -> Figure:
        """
        Plot tick-by-tick analysis

        Args:
            ticks_data: Tick analysis results from TickAnalyzer
            figsize: Figure size

        Returns:
            Matplotlib figure
        """
        fig = plt.figure(figsize=figsize)
        gs = GridSpec(3, 2, figure=fig)

        # Plot 1: Uptick/Downtick Ratio
        ax1 = fig.add_subplot(gs[0, :])
        tick_ratio = ticks_data.get('tick_ratio', {})
        categories = ['Upticks', 'Downticks']
        values = [tick_ratio.get('upticks', 0), tick_ratio.get('downticks', 0)]
        colors = ['green', 'red']
        ax1.bar(categories, values, color=colors, alpha=0.7)
        ax1.set_title(f"Uptick/Downtick Analysis (Ratio: {tick_ratio.get('ratio', 0):.2f})")
        ax1.set_ylabel('Count')
        ax1.grid(True, alpha=0.3)

        # Plot 2: Trade Size Distribution
        ax2 = fig.add_subplot(gs[1, 0])
        size_dist = ticks_data.get('size_distribution', {})
        if size_dist:
            stats = [
                size_dist.get('percentile_25', 0),
                size_dist.get('median_size', 0),
                size_dist.get('percentile_75', 0),
                size_dist.get('percentile_90', 0),
                size_dist.get('percentile_95', 0)
            ]
            labels = ['P25', 'P50', 'P75', 'P90', 'P95']
            ax2.bar(labels, stats, color='cyan', alpha=0.7)
            ax2.set_title('Trade Size Distribution')
            ax2.set_ylabel('Size')
            ax2.grid(True, alpha=0.3)

        # Plot 3: Aggressive vs Passive
        ax3 = fig.add_subplot(gs[1, 1])
        fills = ticks_data.get('fill_classification', {})
        if fills:
            categories = ['Aggressive Buy', 'Aggressive Sell']
            volumes = [fills.get('aggressive_buy_volume', 0), fills.get('aggressive_sell_volume', 0)]
            colors = ['green', 'red']
            ax3.bar(categories, volumes, color=colors, alpha=0.7)
            ax3.set_title('Aggressive Fill Classification')
            ax3.set_ylabel('Volume')
            ax3.grid(True, alpha=0.3)
            plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')

        # Plot 4: Smart Money Indicator
        ax4 = fig.add_subplot(gs[2, :])
        smart_money = ticks_data.get('smart_money', {})
        if smart_money:
            categories = ['Large Buy Volume', 'Large Sell Volume']
            volumes = [smart_money.get('large_buy_volume', 0), smart_money.get('large_sell_volume', 0)]
            colors = ['green', 'red']
            bars = ax4.bar(categories, volumes, color=colors, alpha=0.7)
            ax4.set_title(f"Smart Money Detection - Signal: {smart_money.get('smart_money_signal', 'NEUTRAL')}")
            ax4.set_ylabel('Volume')
            ax4.grid(True, alpha=0.3)

            # Add cluster information as text
            clusters = smart_money.get('clusters_detected', 0)
            ax4.text(
                0.5, 0.95,
                f"Clusters Detected: {clusters}",
                transform=ax4.transAxes,
                ha='center',
                va='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            )

        plt.tight_layout()
        return fig

    def create_comprehensive_dashboard(
        self,
        analysis_result: Dict[str, Any],
        prices: List[float],
        timestamps: Optional[List[datetime]] = None,
        figsize: Tuple[int, int] = (20, 16)
    ) -> Figure:
        """
        Create comprehensive market structure dashboard

        Args:
            analysis_result: Complete analysis from MarketStructureAnalyzer
            prices: Price series
            timestamps: Optional timestamps
            figsize: Figure size

        Returns:
            Matplotlib figure with complete dashboard
        """
        fig = plt.figure(figsize=figsize)
        gs = GridSpec(4, 2, figure=fig, hspace=0.3, wspace=0.3)

        x_axis = timestamps if timestamps else range(len(prices))

        # Plot 1: Price with VWAP
        ax1 = fig.add_subplot(gs[0, :])
        vwap_data = analysis_result.get('vwap', {})
        if 'levels' in vwap_data and not isinstance(vwap_data['levels'], str):
            vwap_levels = vwap_data['levels']
            vwaps = [v.vwap for v in vwap_levels]
            upper_bands = [v.upper_band for v in vwap_levels]
            lower_bands = [v.lower_band for v in vwap_levels]

            ax1.plot(x_axis, prices, color='white', linewidth=2, label='Price')
            ax1.plot(x_axis, vwaps, color='yellow', linewidth=2, label='VWAP')
            ax1.plot(x_axis, upper_bands, 'r--', alpha=0.5, label='Upper Band')
            ax1.plot(x_axis, lower_bands, 'g--', alpha=0.5, label='Lower Band')
            ax1.fill_between(x_axis, upper_bands, lower_bands, alpha=0.1, color='gray')

        ax1.set_title('Price Action with VWAP')
        ax1.set_ylabel('Price')
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)

        # Plot 2: Volume Profile
        ax2 = fig.add_subplot(gs[1, 0])
        mp_data = analysis_result.get('market_profile', {})
        if 'volume_profile' in mp_data and not isinstance(mp_data['volume_profile'], str):
            volume_profile = mp_data['volume_profile']
            prices_vp = [level.price for level in volume_profile]
            volumes_vp = [level.volume for level in volume_profile]
            ax2.barh(prices_vp, volumes_vp, color='cyan', alpha=0.6)
            ax2.set_xlabel('Volume')
            ax2.set_ylabel('Price')
            ax2.set_title('Volume Profile')
            ax2.grid(True, alpha=0.3)

            # Add POC if available
            if 'profile' in mp_data:
                profile = mp_data['profile']
                ax2.axhline(profile.point_of_control, color='yellow', linestyle='--', linewidth=2)

        # Plot 3: Market Profile with Value Area
        ax3 = fig.add_subplot(gs[1, 1])
        if 'profile' in mp_data and not isinstance(mp_data.get('volume_profile'), str):
            profile = mp_data['profile']
            volume_profile = mp_data['volume_profile']

            prices_vp = [level.price for level in volume_profile]
            buy_volumes = [level.buy_volume for level in volume_profile]
            sell_volumes = [level.sell_volume for level in volume_profile]

            ax3.barh(prices_vp, buy_volumes, color='green', alpha=0.5, label='Buy')
            ax3.barh(prices_vp, [-v for v in sell_volumes], color='red', alpha=0.5, label='Sell')
            ax3.axhline(profile.point_of_control, color='yellow', linestyle='-', linewidth=2, label='POC')
            ax3.axhline(profile.value_area_high, color='orange', linestyle='--', linewidth=1.5, label='VAH')
            ax3.axhline(profile.value_area_low, color='orange', linestyle='--', linewidth=1.5, label='VAL')

            ax3.set_xlabel('Volume')
            ax3.set_ylabel('Price')
            ax3.set_title('Market Profile (Buy/Sell)')
            ax3.legend(loc='best', fontsize=8)
            ax3.grid(True, alpha=0.3)

        # Plot 4: Liquidity Zones
        ax4 = fig.add_subplot(gs[2, :])
        liquidity_data = analysis_result.get('liquidity', {})
        if 'zones' in liquidity_data and liquidity_data['zones']:
            zones = liquidity_data['zones'][:10]  # Top 10 zones

            color_map = {'support': 'green', 'resistance': 'red', 'absorption': 'yellow'}

            for i, zone in enumerate(zones):
                color = color_map.get(zone.zone_type, 'gray')
                ax4.barh(
                    i,
                    zone.total_liquidity,
                    color=color,
                    alpha=min(0.8, zone.strength / 100)
                )
                ax4.text(
                    zone.total_liquidity * 0.5,
                    i,
                    f'{zone.zone_type}: ${zone.price_center:.2f}',
                    ha='center',
                    va='center',
                    fontsize=9,
                    color='white'
                )

            ax4.set_xlabel('Liquidity')
            ax4.set_ylabel('Zone Rank')
            ax4.set_title('Top Liquidity Zones')
            ax4.grid(True, alpha=0.3, axis='x')

        # Plot 5: Supply/Demand Analysis
        ax5 = fig.add_subplot(gs[3, 0])
        if 'supply_demand' in liquidity_data and liquidity_data['supply_demand']:
            sd = liquidity_data['supply_demand']
            categories = ['Buy Volume', 'Sell Volume']
            volumes = [sd.get('total_buy_volume', 0), sd.get('total_sell_volume', 0)]
            colors = ['green', 'red']
            ax5.bar(categories, volumes, color=colors, alpha=0.7)
            ax5.set_title(f"Supply/Demand - Bias: {sd.get('market_bias', 'NEUTRAL')}")
            ax5.set_ylabel('Volume')
            ax5.grid(True, alpha=0.3)

        # Plot 6: Summary Statistics
        ax6 = fig.add_subplot(gs[3, 1])
        ax6.axis('off')

        summary_text = "MARKET STRUCTURE SUMMARY\n" + "="*30 + "\n\n"

        # VWAP Stats
        if 'statistics' in vwap_data:
            stats = vwap_data['statistics']
            summary_text += f"VWAP:\n"
            summary_text += f"  Position: {stats.get('current_position', 'N/A')}\n"
            summary_text += f"  Distance: {stats.get('current_distance_pct', 0):.2f}%\n"
            summary_text += f"  Above: {stats.get('percentage_above', 0):.1f}%\n\n"

        # Market Profile Stats
        if 'distribution' in mp_data:
            dist = mp_data['distribution']
            summary_text += f"Market Profile:\n"
            summary_text += f"  Bias: {dist.get('session_bias', 'N/A')}\n"
            summary_text += f"  B/S Ratio: {dist.get('buy_sell_ratio', 0):.2f}\n"
            summary_text += f"  Value Area: {dist.get('value_area_percentage', 0):.1f}%\n\n"

        # Tick Analysis
        tick_data = analysis_result.get('tick_analysis', {})
        if 'smart_money' in tick_data:
            sm = tick_data['smart_money']
            summary_text += f"Smart Money:\n"
            summary_text += f"  Signal: {sm.get('smart_money_signal', 'N/A')}\n"
            summary_text += f"  Clusters: {sm.get('clusters_detected', 0)}\n"
            summary_text += f"  Imbalance: {sm.get('large_trade_imbalance', 0):.2f}\n"

        ax6.text(0.1, 0.9, summary_text, transform=ax6.transAxes,
                fontsize=10, verticalalignment='top', family='monospace',
                bbox=dict(boxstyle='round', facecolor='black', alpha=0.8, edgecolor='cyan'))

        fig.suptitle('Comprehensive Market Structure Analysis', fontsize=16, weight='bold')

        return fig

    def fig_to_base64(self, fig: Figure) -> str:
        """
        Convert matplotlib figure to base64 encoded string

        Args:
            fig: Matplotlib figure

        Returns:
            Base64 encoded string
        """
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close(fig)
        return img_base64

    def fig_to_bytes(self, fig: Figure, format: str = 'png') -> bytes:
        """
        Convert matplotlib figure to bytes

        Args:
            fig: Matplotlib figure
            format: Image format (png, jpg, svg, pdf)

        Returns:
            Image bytes
        """
        buf = io.BytesIO()
        fig.savefig(buf, format=format, dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_bytes = buf.read()
        buf.close()
        plt.close(fig)
        return img_bytes
