"""
Forecast Visualization
Creates probability cones, confidence intervals, and support/resistance band visualizations
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple
import logging
from datetime import datetime, timedelta
import json

# Import plotting libraries
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO
import base64

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    logging.warning("Plotly not available, falling back to matplotlib only")

logger = logging.getLogger(__name__)


class ForecastVisualizer:
    """
    Visualization tools for price forecasts
    """

    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize visualizer

        Args:
            style: Matplotlib style to use
        """
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')

    def create_probability_cone(
        self,
        historical_prices: pd.Series,
        forecast_dates: List[datetime],
        forecast_prices: np.ndarray,
        confidence_intervals: List[Tuple[np.ndarray, np.ndarray]],
        confidence_levels: List[float] = [0.5, 0.7, 0.9],
        title: str = "Price Forecast with Probability Cone"
    ) -> Dict[str, Any]:
        """
        Create probability cone visualization

        Args:
            historical_prices: Historical price data (indexed by date)
            forecast_dates: Dates for forecasts
            forecast_prices: Forecasted prices
            confidence_intervals: List of (lower, upper) bounds for each confidence level
            confidence_levels: Confidence levels (e.g., [0.5, 0.7, 0.9])
            title: Chart title

        Returns:
            Dictionary with visualization data and chart image
        """
        logger.info("Creating probability cone visualization")

        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(14, 7))

        # Plot historical prices
        hist_dates = historical_prices.index if hasattr(historical_prices.index, '__len__') else range(len(historical_prices))
        ax.plot(hist_dates, historical_prices.values, label='Historical', color='black', linewidth=2)

        # Plot forecast
        ax.plot(forecast_dates, forecast_prices, label='Forecast', color='blue', linewidth=2, linestyle='--')

        # Plot probability cone (confidence intervals)
        colors = ['lightblue', 'lightsteelblue', 'lightgray']
        alphas = [0.6, 0.4, 0.2]

        for i, (lower, upper) in enumerate(confidence_intervals):
            conf_level = confidence_levels[i] if i < len(confidence_levels) else 0.5
            color = colors[i] if i < len(colors) else 'lightgray'
            alpha = alphas[i] if i < len(alphas) else 0.2

            ax.fill_between(
                forecast_dates,
                lower,
                upper,
                alpha=alpha,
                color=color,
                label=f'{int(conf_level*100)}% Confidence'
            )

        # Formatting
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price ($)', fontsize=12)
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)

        # Format x-axis dates
        if isinstance(hist_dates[0], (datetime, pd.Timestamp)):
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.xticks(rotation=45)

        plt.tight_layout()

        # Convert to base64 for API response
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)

        return {
            'type': 'probability_cone',
            'image_base64': image_base64,
            'format': 'png',
            'confidence_levels': confidence_levels
        }

    def create_confidence_interval_chart(
        self,
        dates: List[datetime],
        actual_prices: Optional[np.ndarray],
        predicted_prices: np.ndarray,
        lower_bound: np.ndarray,
        upper_bound: np.ndarray,
        title: str = "Price Forecast with Confidence Intervals"
    ) -> Dict[str, Any]:
        """
        Create confidence interval chart

        Args:
            dates: Dates for data points
            actual_prices: Actual prices (if available)
            predicted_prices: Predicted prices
            lower_bound: Lower confidence bound
            upper_bound: Upper confidence bound
            title: Chart title

        Returns:
            Dictionary with chart data and image
        """
        logger.info("Creating confidence interval chart")

        fig, ax = plt.subplots(figsize=(14, 7))

        # Plot actual prices if available
        if actual_prices is not None:
            ax.plot(dates, actual_prices, label='Actual', color='black', linewidth=2)

        # Plot predictions
        ax.plot(dates, predicted_prices, label='Predicted', color='blue', linewidth=2, linestyle='--')

        # Plot confidence intervals
        ax.fill_between(
            dates,
            lower_bound,
            upper_bound,
            alpha=0.3,
            color='lightblue',
            label='90% Confidence Interval'
        )

        # Formatting
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price ($)', fontsize=12)
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)

        # Format x-axis
        if isinstance(dates[0], (datetime, pd.Timestamp)):
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.xticks(rotation=45)

        plt.tight_layout()

        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)

        return {
            'type': 'confidence_interval',
            'image_base64': image_base64,
            'format': 'png'
        }

    def create_support_resistance_bands(
        self,
        dates: List[datetime],
        prices: np.ndarray,
        support_levels: List[float],
        resistance_levels: List[float],
        title: str = "Price with Support/Resistance Bands"
    ) -> Dict[str, Any]:
        """
        Create support/resistance bands visualization

        Args:
            dates: Dates for price data
            prices: Price data
            support_levels: List of support price levels
            resistance_levels: List of resistance price levels
            title: Chart title

        Returns:
            Dictionary with chart data and image
        """
        logger.info("Creating support/resistance bands chart")

        fig, ax = plt.subplots(figsize=(14, 7))

        # Plot prices
        ax.plot(dates, prices, label='Price', color='black', linewidth=2)

        # Plot support levels
        for i, level in enumerate(support_levels):
            ax.axhline(y=level, color='green', linestyle='--', alpha=0.6,
                      label=f'Support {i+1}' if i == 0 else '')

        # Plot resistance levels
        for i, level in enumerate(resistance_levels):
            ax.axhline(y=level, color='red', linestyle='--', alpha=0.6,
                      label=f'Resistance {i+1}' if i == 0 else '')

        # Formatting
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price ($)', fontsize=12)
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)

        # Format x-axis
        if isinstance(dates[0], (datetime, pd.Timestamp)):
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.xticks(rotation=45)

        plt.tight_layout()

        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)

        return {
            'type': 'support_resistance',
            'image_base64': image_base64,
            'format': 'png',
            'support_levels': support_levels,
            'resistance_levels': resistance_levels
        }

    def create_multi_timeframe_forecast(
        self,
        forecasts: Dict[str, Dict[str, Any]],
        title: str = "Multi-Timeframe Price Forecasts"
    ) -> Dict[str, Any]:
        """
        Create multi-timeframe forecast visualization

        Args:
            forecasts: Dictionary of forecasts for different timeframes
                      {'1D': {...}, '1W': {...}, '1M': {...}}
            title: Chart title

        Returns:
            Dictionary with chart data and image
        """
        logger.info("Creating multi-timeframe forecast chart")

        fig, axes = plt.subplots(len(forecasts), 1, figsize=(14, 5 * len(forecasts)))

        if len(forecasts) == 1:
            axes = [axes]

        for ax, (timeframe, forecast_data) in zip(axes, forecasts.items()):
            dates = forecast_data.get('dates', [])
            prices = forecast_data.get('prices', [])
            lower = forecast_data.get('lower_bound', None)
            upper = forecast_data.get('upper_bound', None)

            # Plot forecast
            ax.plot(dates, prices, label=f'{timeframe} Forecast', linewidth=2)

            # Plot confidence interval if available
            if lower is not None and upper is not None:
                ax.fill_between(dates, lower, upper, alpha=0.3, label='90% CI')

            ax.set_title(f'{timeframe} Forecast', fontsize=12, fontweight='bold')
            ax.set_xlabel('Date', fontsize=10)
            ax.set_ylabel('Price ($)', fontsize=10)
            ax.legend(loc='upper left', fontsize=9)
            ax.grid(True, alpha=0.3)

            # Format x-axis
            if dates and isinstance(dates[0], (datetime, pd.Timestamp)):
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

        plt.suptitle(title, fontsize=14, fontweight='bold', y=1.0)
        plt.tight_layout()

        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)

        return {
            'type': 'multi_timeframe',
            'image_base64': image_base64,
            'format': 'png',
            'timeframes': list(forecasts.keys())
        }

    def create_interactive_forecast_plotly(
        self,
        historical_data: pd.DataFrame,
        forecast_data: Dict[str, Any]
    ) -> Optional[str]:
        """
        Create interactive Plotly forecast chart

        Args:
            historical_data: DataFrame with historical OHLCV data
            forecast_data: Dictionary with forecast information

        Returns:
            HTML string of Plotly chart, or None if Plotly unavailable
        """
        if not PLOTLY_AVAILABLE:
            logger.warning("Plotly not available, skipping interactive chart")
            return None

        logger.info("Creating interactive Plotly forecast chart")

        # Create figure with secondary y-axis
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=[0.7, 0.3],
            subplot_titles=('Price Forecast', 'Volume')
        )

        # Historical candlestick
        fig.add_trace(
            go.Candlestick(
                x=historical_data.index,
                open=historical_data['open'],
                high=historical_data['high'],
                low=historical_data['low'],
                close=historical_data['close'],
                name='Historical',
                increasing_line_color='green',
                decreasing_line_color='red'
            ),
            row=1, col=1
        )

        # Forecast line
        forecast_dates = forecast_data.get('dates', [])
        forecast_prices = forecast_data.get('prices', [])

        if forecast_dates and forecast_prices:
            fig.add_trace(
                go.Scatter(
                    x=forecast_dates,
                    y=forecast_prices,
                    mode='lines',
                    name='Forecast',
                    line=dict(color='blue', width=2, dash='dash')
                ),
                row=1, col=1
            )

            # Confidence intervals
            lower = forecast_data.get('lower_bound')
            upper = forecast_data.get('upper_bound')

            if lower is not None and upper is not None:
                fig.add_trace(
                    go.Scatter(
                        x=forecast_dates + forecast_dates[::-1],
                        y=list(upper) + list(lower[::-1]),
                        fill='toself',
                        fillcolor='rgba(0, 100, 255, 0.2)',
                        line=dict(color='rgba(255,255,255,0)'),
                        name='90% Confidence',
                        showlegend=True
                    ),
                    row=1, col=1
                )

        # Volume bars
        fig.add_trace(
            go.Bar(
                x=historical_data.index,
                y=historical_data['volume'],
                name='Volume',
                marker_color='lightblue'
            ),
            row=2, col=1
        )

        # Update layout
        fig.update_layout(
            title='Price Forecast with Confidence Intervals',
            xaxis_rangeslider_visible=False,
            height=800,
            showlegend=True,
            hovermode='x unified'
        )

        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)

        # Convert to HTML
        html_str = fig.to_html(include_plotlyjs='cdn')

        return html_str

    def calculate_support_resistance_levels(
        self,
        prices: np.ndarray,
        n_levels: int = 3
    ) -> Tuple[List[float], List[float]]:
        """
        Calculate support and resistance levels from price data

        Args:
            prices: Array of historical prices
            n_levels: Number of support/resistance levels to find

        Returns:
            Tuple of (support_levels, resistance_levels)
        """
        # Find local minima (support) and maxima (resistance)
        window = 5

        support_levels = []
        resistance_levels = []

        for i in range(window, len(prices) - window):
            # Check for local minimum
            if prices[i] == min(prices[i-window:i+window+1]):
                support_levels.append(float(prices[i]))

            # Check for local maximum
            if prices[i] == max(prices[i-window:i+window+1]):
                resistance_levels.append(float(prices[i]))

        # Cluster similar levels
        def cluster_levels(levels, n_clusters):
            if not levels or n_clusters == 0:
                return []

            levels = sorted(levels)
            clusters = []

            # Simple k-means-like clustering
            step = len(levels) // n_clusters
            for i in range(0, len(levels), max(1, step)):
                chunk = levels[i:i+step] if i+step < len(levels) else levels[i:]
                if chunk:
                    clusters.append(np.mean(chunk))

            return sorted(set(clusters))[:n_clusters]

        support_levels = cluster_levels(support_levels, n_levels)
        resistance_levels = cluster_levels(resistance_levels, n_levels)

        return support_levels, resistance_levels
