"""
Core correlation statistics and analysis functions.

This module provides statistical functions for calculating correlations,
pair trading signals, and market leadership metrics.
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd
from scipy import stats
from datetime import datetime, timedelta


class CorrelationStats:
    """Core statistical functions for correlation analysis."""

    @staticmethod
    def calculate_correlation_matrix(
        price_data: Dict[str, pd.DataFrame],
        method: str = "pearson",
        min_periods: int = 20
    ) -> pd.DataFrame:
        """
        Calculate correlation matrix for multiple tickers.

        Args:
            price_data: Dict of {ticker: DataFrame with 'close' column}
            method: 'pearson', 'spearman', or 'kendall'
            min_periods: Minimum number of observations required

        Returns:
            DataFrame with correlation matrix
        """
        # Extract close prices and align dates
        prices = {}
        for ticker, df in price_data.items():
            if 'close' in df.columns:
                prices[ticker] = df['close']
            elif 'Close' in df.columns:
                prices[ticker] = df['Close']

        if not prices:
            return pd.DataFrame()

        # Create aligned DataFrame
        price_df = pd.DataFrame(prices)

        # Calculate correlation
        if method == "pearson":
            corr_matrix = price_df.corr(method='pearson', min_periods=min_periods)
        elif method == "spearman":
            corr_matrix = price_df.corr(method='spearman', min_periods=min_periods)
        elif method == "kendall":
            corr_matrix = price_df.corr(method='kendall', min_periods=min_periods)
        else:
            raise ValueError(f"Unknown correlation method: {method}")

        return corr_matrix

    @staticmethod
    def calculate_rolling_correlation(
        series1: pd.Series,
        series2: pd.Series,
        window: int = 20,
        min_periods: Optional[int] = None
    ) -> pd.Series:
        """
        Calculate rolling correlation between two price series.

        Args:
            series1: First price series
            series2: Second price series
            window: Rolling window size
            min_periods: Minimum periods (defaults to window)

        Returns:
            Series of rolling correlations
        """
        if min_periods is None:
            min_periods = window

        return series1.rolling(window=window, min_periods=min_periods).corr(series2)

    @staticmethod
    def find_correlated_pairs(
        corr_matrix: pd.DataFrame,
        min_correlation: float = 0.7,
        max_correlation: float = 0.95
    ) -> List[Dict]:
        """
        Find pairs of tickers with correlation in specified range.

        Args:
            corr_matrix: Correlation matrix
            min_correlation: Minimum correlation threshold
            max_correlation: Maximum correlation threshold (to avoid identical stocks)

        Returns:
            List of dicts with pair information
        """
        pairs = []
        tickers = corr_matrix.columns.tolist()

        for i, ticker1 in enumerate(tickers):
            for ticker2 in tickers[i+1:]:
                corr = corr_matrix.loc[ticker1, ticker2]

                if pd.notna(corr) and min_correlation <= abs(corr) <= max_correlation:
                    pairs.append({
                        'ticker1': ticker1,
                        'ticker2': ticker2,
                        'correlation': float(corr),
                        'abs_correlation': abs(float(corr)),
                        'relationship': 'positive' if corr > 0 else 'negative'
                    })

        # Sort by absolute correlation
        pairs.sort(key=lambda x: x['abs_correlation'], reverse=True)

        return pairs

    @staticmethod
    def calculate_spread(
        price1: pd.Series,
        price2: pd.Series,
        normalize: bool = True
    ) -> pd.Series:
        """
        Calculate price spread between two series.

        Args:
            price1: First price series
            price2: Second price series
            normalize: Whether to normalize prices first

        Returns:
            Series representing the spread
        """
        if normalize:
            # Normalize to same starting point
            norm_price1 = price1 / price1.iloc[0] * 100
            norm_price2 = price2 / price2.iloc[0] * 100
            return norm_price1 - norm_price2
        else:
            return price1 - price2

    @staticmethod
    def detect_divergence(
        spread: pd.Series,
        window: int = 20,
        std_threshold: float = 2.0
    ) -> Dict:
        """
        Detect divergence in spread for pair trading signals.

        Args:
            spread: Price spread series
            window: Rolling window for stats
            std_threshold: Standard deviation threshold for signals

        Returns:
            Dict with divergence analysis
        """
        # Calculate rolling statistics
        rolling_mean = spread.rolling(window=window).mean()
        rolling_std = spread.rolling(window=window).std()

        # Current values
        current_spread = spread.iloc[-1]
        current_mean = rolling_mean.iloc[-1]
        current_std = rolling_std.iloc[-1]

        # Z-score
        if current_std > 0:
            z_score = (current_spread - current_mean) / current_std
        else:
            z_score = 0

        # Generate signal
        signal = None
        if z_score > std_threshold:
            signal = 'short_spread'  # Spread too high, expect mean reversion
        elif z_score < -std_threshold:
            signal = 'long_spread'  # Spread too low, expect mean reversion

        return {
            'current_spread': float(current_spread),
            'mean_spread': float(current_mean),
            'std_spread': float(current_std),
            'z_score': float(z_score),
            'signal': signal,
            'threshold': std_threshold
        }

    @staticmethod
    def calculate_beta(
        stock_returns: pd.Series,
        market_returns: pd.Series,
        min_periods: int = 20
    ) -> float:
        """
        Calculate beta (systematic risk) of a stock relative to market.

        Args:
            stock_returns: Stock return series
            market_returns: Market/benchmark return series
            min_periods: Minimum periods required

        Returns:
            Beta value
        """
        # Align the series
        aligned = pd.DataFrame({
            'stock': stock_returns,
            'market': market_returns
        }).dropna()

        if len(aligned) < min_periods:
            return np.nan

        # Calculate covariance and variance
        covariance = aligned['stock'].cov(aligned['market'])
        market_variance = aligned['market'].var()

        if market_variance > 0:
            beta = covariance / market_variance
        else:
            beta = np.nan

        return float(beta)

    @staticmethod
    def calculate_lead_lag(
        series1: pd.Series,
        series2: pd.Series,
        max_lag: int = 5
    ) -> Dict:
        """
        Determine lead-lag relationship between two series.

        Args:
            series1: First price series
            series2: Second price series
            max_lag: Maximum lag to test (in periods)

        Returns:
            Dict with lead-lag analysis
        """
        correlations = {}

        # Test different lags
        for lag in range(-max_lag, max_lag + 1):
            if lag < 0:
                # series1 leads series2
                s1 = series1.iloc[:-abs(lag)]
                s2 = series2.iloc[abs(lag):]
            elif lag > 0:
                # series2 leads series1
                s1 = series1.iloc[lag:]
                s2 = series2.iloc[:-lag]
            else:
                # No lag
                s1 = series1
                s2 = series2

            # Calculate correlation
            if len(s1) > 0 and len(s2) > 0:
                corr = s1.corr(s2)
                if pd.notna(corr):
                    correlations[lag] = float(corr)

        # Find best correlation
        if correlations:
            best_lag = max(correlations.items(), key=lambda x: abs(x[1]))

            result = {
                'best_lag': best_lag[0],
                'best_correlation': best_lag[1],
                'all_correlations': correlations
            }

            # Interpret the relationship
            if best_lag[0] < 0:
                result['leader'] = 'series1'
                result['lag_periods'] = abs(best_lag[0])
            elif best_lag[0] > 0:
                result['leader'] = 'series2'
                result['lag_periods'] = best_lag[0]
            else:
                result['leader'] = 'simultaneous'
                result['lag_periods'] = 0

            return result

        return {
            'best_lag': 0,
            'best_correlation': 0,
            'leader': 'unknown',
            'lag_periods': 0,
            'all_correlations': {}
        }

    @staticmethod
    def portfolio_correlation_analysis(
        portfolio_weights: Dict[str, float],
        corr_matrix: pd.DataFrame
    ) -> Dict:
        """
        Analyze correlation structure of a portfolio.

        Args:
            portfolio_weights: Dict of {ticker: weight}
            corr_matrix: Correlation matrix

        Returns:
            Dict with portfolio correlation metrics
        """
        tickers = list(portfolio_weights.keys())
        weights = np.array([portfolio_weights[t] for t in tickers])

        # Filter correlation matrix to portfolio tickers
        port_corr = corr_matrix.loc[tickers, tickers]

        # Calculate average correlation
        # Exclude diagonal (self-correlation = 1)
        mask = ~np.eye(len(tickers), dtype=bool)
        avg_correlation = port_corr.values[mask].mean()

        # Calculate weighted correlation
        weighted_corr = 0
        for i, t1 in enumerate(tickers):
            for j, t2 in enumerate(tickers):
                if i != j:
                    weighted_corr += weights[i] * weights[j] * port_corr.loc[t1, t2]

        # Find highly correlated pairs in portfolio
        high_corr_pairs = []
        for i, t1 in enumerate(tickers):
            for t2 in tickers[i+1:]:
                corr = port_corr.loc[t1, t2]
                if abs(corr) > 0.7:  # High correlation threshold
                    high_corr_pairs.append({
                        'ticker1': t1,
                        'ticker2': t2,
                        'correlation': float(corr),
                        'combined_weight': portfolio_weights[t1] + portfolio_weights[t2]
                    })

        # Calculate diversification ratio
        # DR = sum(weights) / sqrt(weights' * CorrMatrix * weights)
        portfolio_variance = weights @ port_corr.values @ weights
        portfolio_volatility = np.sqrt(portfolio_variance) if portfolio_variance > 0 else 0

        return {
            'average_correlation': float(avg_correlation),
            'weighted_correlation': float(weighted_corr),
            'portfolio_volatility': float(portfolio_volatility),
            'high_correlation_pairs': high_corr_pairs,
            'diversification_score': float(1 - avg_correlation),  # Higher is better
            'num_tickers': len(tickers)
        }

    @staticmethod
    def identify_redundant_holdings(
        portfolio_weights: Dict[str, float],
        corr_matrix: pd.DataFrame,
        correlation_threshold: float = 0.8
    ) -> List[Dict]:
        """
        Identify redundant holdings (highly correlated) in portfolio.

        Args:
            portfolio_weights: Dict of {ticker: weight}
            correlation_threshold: Threshold for considering holdings redundant

        Returns:
            List of redundant pairs with suggestions
        """
        tickers = list(portfolio_weights.keys())
        redundant = []

        for i, t1 in enumerate(tickers):
            for t2 in tickers[i+1:]:
                corr = corr_matrix.loc[t1, t2]

                if abs(corr) >= correlation_threshold:
                    w1 = portfolio_weights[t1]
                    w2 = portfolio_weights[t2]

                    # Suggest keeping the one with higher weight
                    if w1 > w2:
                        keep, reduce = t1, t2
                    else:
                        keep, reduce = t2, t1

                    redundant.append({
                        'ticker1': t1,
                        'ticker2': t2,
                        'correlation': float(corr),
                        'weight1': w1,
                        'weight2': w2,
                        'suggested_keep': keep,
                        'suggested_reduce': reduce,
                        'potential_savings': min(w1, w2)
                    })

        return sorted(redundant, key=lambda x: abs(x['correlation']), reverse=True)
