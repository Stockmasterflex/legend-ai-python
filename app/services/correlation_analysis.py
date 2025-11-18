"""
Correlation Analysis Service

Provides high-level correlation analysis features including:
- Correlation heatmaps
- Pair trading signals
- Portfolio diversification analysis
- Market leadership identification
"""

from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import json

from app.core.correlation_stats import CorrelationStats
from app.services.market_data import MarketDataService
from app.services.cache import get_cache_service

logger = logging.getLogger(__name__)


class CorrelationAnalysisService:
    """Service for correlation analysis and pair trading."""

    def __init__(self):
        self.market_data = MarketDataService()
        self.cache = get_cache_service()
        self.stats = CorrelationStats()

    async def get_correlation_heatmap(
        self,
        tickers: List[str],
        period: str = "1month",
        interval: str = "1day",
        method: str = "pearson"
    ) -> Dict:
        """
        Generate correlation heatmap data for multiple tickers.

        Args:
            tickers: List of ticker symbols
            period: Time period (1month, 3month, 6month, 1year)
            interval: Data interval (1day, 1hour)
            method: Correlation method (pearson, spearman, kendall)

        Returns:
            Dict with correlation matrix and metadata
        """
        cache_key = f"correlation_heatmap:{','.join(sorted(tickers))}:{period}:{interval}:{method}"

        # Check cache
        cached = await self.cache.get(cache_key)
        if cached:
            logger.info(f"Cache hit for correlation heatmap: {cache_key}")
            return json.loads(cached)

        try:
            # Fetch price data for all tickers
            price_data = {}
            failed_tickers = []

            for ticker in tickers:
                try:
                    data = await self.market_data.get_time_series(
                        symbol=ticker,
                        interval=interval,
                        outputsize=self._period_to_outputsize(period)
                    )

                    if data and 'values' in data and data['values']:
                        # Convert to DataFrame
                        df = pd.DataFrame(data['values'])
                        df['datetime'] = pd.to_datetime(df['datetime'])
                        df = df.set_index('datetime')
                        df['close'] = pd.to_numeric(df['close'], errors='coerce')
                        price_data[ticker] = df
                    else:
                        failed_tickers.append(ticker)

                except Exception as e:
                    logger.warning(f"Failed to fetch data for {ticker}: {e}")
                    failed_tickers.append(ticker)

            if len(price_data) < 2:
                return {
                    'error': 'Insufficient data',
                    'message': f'Need at least 2 tickers with data, got {len(price_data)}',
                    'failed_tickers': failed_tickers
                }

            # Calculate correlation matrix
            corr_matrix = self.stats.calculate_correlation_matrix(
                price_data,
                method=method,
                min_periods=10
            )

            # Prepare response
            result = {
                'correlation_matrix': corr_matrix.to_dict(),
                'tickers': corr_matrix.columns.tolist(),
                'method': method,
                'period': period,
                'interval': interval,
                'failed_tickers': failed_tickers,
                'timestamp': datetime.now().isoformat(),
                'heatmap_data': self._prepare_heatmap_data(corr_matrix)
            }

            # Cache for 1 hour
            await self.cache.set(cache_key, json.dumps(result), ttl=3600)

            return result

        except Exception as e:
            logger.error(f"Error generating correlation heatmap: {e}")
            return {'error': str(e)}

    async def find_pair_trading_opportunities(
        self,
        tickers: List[str],
        period: str = "3month",
        min_correlation: float = 0.7,
        max_correlation: float = 0.95,
        top_n: int = 20
    ) -> Dict:
        """
        Find correlated pairs suitable for pair trading.

        Args:
            tickers: List of ticker symbols to analyze
            period: Historical period for correlation
            min_correlation: Minimum correlation threshold
            max_correlation: Maximum correlation (avoid identical stocks)
            top_n: Number of top pairs to return

        Returns:
            Dict with pair trading opportunities
        """
        cache_key = f"pair_trading:{','.join(sorted(tickers))}:{period}:{min_correlation}:{max_correlation}"

        cached = await self.cache.get(cache_key)
        if cached:
            return json.loads(cached)

        try:
            # Get price data
            price_data = {}
            for ticker in tickers:
                try:
                    data = await self.market_data.get_time_series(
                        symbol=ticker,
                        interval="1day",
                        outputsize=self._period_to_outputsize(period)
                    )

                    if data and 'values' in data and data['values']:
                        df = pd.DataFrame(data['values'])
                        df['datetime'] = pd.to_datetime(df['datetime'])
                        df = df.set_index('datetime').sort_index()
                        df['close'] = pd.to_numeric(df['close'], errors='coerce')
                        price_data[ticker] = df
                except Exception as e:
                    logger.warning(f"Failed to fetch {ticker}: {e}")

            if len(price_data) < 2:
                return {'error': 'Insufficient data for pair analysis'}

            # Calculate correlation matrix
            corr_matrix = self.stats.calculate_correlation_matrix(price_data)

            # Find correlated pairs
            pairs = self.stats.find_correlated_pairs(
                corr_matrix,
                min_correlation=min_correlation,
                max_correlation=max_correlation
            )

            # Analyze each pair for trading signals
            pair_signals = []
            for pair in pairs[:top_n]:
                t1, t2 = pair['ticker1'], pair['ticker2']

                # Get price series
                p1 = price_data[t1]['close']
                p2 = price_data[t2]['close']

                # Calculate spread
                spread = self.stats.calculate_spread(p1, p2, normalize=True)

                # Detect divergence
                divergence = self.stats.detect_divergence(spread, window=20, std_threshold=2.0)

                # Calculate rolling correlation
                rolling_corr = self.stats.calculate_rolling_correlation(p1, p2, window=20)

                # Check lead-lag relationship
                lead_lag = self.stats.calculate_lead_lag(p1, p2, max_lag=5)

                pair_signals.append({
                    'ticker1': t1,
                    'ticker2': t2,
                    'correlation': pair['correlation'],
                    'relationship': pair['relationship'],
                    'current_spread': divergence['current_spread'],
                    'mean_spread': divergence['mean_spread'],
                    'z_score': divergence['z_score'],
                    'signal': divergence['signal'],
                    'current_correlation': float(rolling_corr.iloc[-1]) if len(rolling_corr) > 0 else None,
                    'lead_lag': lead_lag,
                    'spread_history': spread.tail(30).to_dict() if len(spread) > 0 else {}
                })

            result = {
                'pairs': pair_signals,
                'total_pairs_found': len(pairs),
                'period': period,
                'min_correlation': min_correlation,
                'max_correlation': max_correlation,
                'timestamp': datetime.now().isoformat()
            }

            # Cache for 30 minutes
            await self.cache.set(cache_key, json.dumps(result), ttl=1800)

            return result

        except Exception as e:
            logger.error(f"Error finding pair trading opportunities: {e}")
            return {'error': str(e)}

    async def analyze_portfolio_diversification(
        self,
        portfolio: Dict[str, float],
        period: str = "3month"
    ) -> Dict:
        """
        Analyze correlation and diversification of a portfolio.

        Args:
            portfolio: Dict of {ticker: weight}
            period: Historical period for analysis

        Returns:
            Dict with diversification analysis
        """
        tickers = list(portfolio.keys())
        cache_key = f"portfolio_diversification:{','.join(sorted(tickers))}:{period}"

        cached = await self.cache.get(cache_key)
        if cached:
            return json.loads(cached)

        try:
            # Fetch price data
            price_data = {}
            for ticker in tickers:
                try:
                    data = await self.market_data.get_time_series(
                        symbol=ticker,
                        interval="1day",
                        outputsize=self._period_to_outputsize(period)
                    )

                    if data and 'values' in data and data['values']:
                        df = pd.DataFrame(data['values'])
                        df['datetime'] = pd.to_datetime(df['datetime'])
                        df = df.set_index('datetime')
                        df['close'] = pd.to_numeric(df['close'], errors='coerce')
                        price_data[ticker] = df
                except Exception as e:
                    logger.warning(f"Failed to fetch {ticker}: {e}")

            if len(price_data) < 2:
                return {'error': 'Insufficient data for portfolio analysis'}

            # Calculate correlation matrix
            corr_matrix = self.stats.calculate_correlation_matrix(price_data)

            # Portfolio correlation analysis
            port_analysis = self.stats.portfolio_correlation_analysis(
                portfolio,
                corr_matrix
            )

            # Identify redundant holdings
            redundant = self.stats.identify_redundant_holdings(
                portfolio,
                corr_matrix,
                correlation_threshold=0.8
            )

            # Calculate diversification suggestions
            suggestions = self._generate_diversification_suggestions(
                portfolio,
                corr_matrix,
                redundant
            )

            result = {
                'portfolio_metrics': port_analysis,
                'redundant_holdings': redundant,
                'suggestions': suggestions,
                'correlation_matrix': corr_matrix.to_dict(),
                'period': period,
                'timestamp': datetime.now().isoformat()
            }

            # Cache for 1 hour
            await self.cache.set(cache_key, json.dumps(result), ttl=3600)

            return result

        except Exception as e:
            logger.error(f"Error analyzing portfolio diversification: {e}")
            return {'error': str(e)}

    async def analyze_market_leadership(
        self,
        tickers: List[str],
        benchmark: str = "SPY",
        period: str = "3month"
    ) -> Dict:
        """
        Analyze which tickers lead or lag the market.

        Args:
            tickers: List of ticker symbols
            benchmark: Market benchmark (default SPY)
            period: Historical period

        Returns:
            Dict with leadership analysis
        """
        cache_key = f"market_leadership:{','.join(sorted(tickers))}:{benchmark}:{period}"

        cached = await self.cache.get(cache_key)
        if cached:
            return json.loads(cached)

        try:
            # Fetch benchmark data
            benchmark_data = await self.market_data.get_time_series(
                symbol=benchmark,
                interval="1day",
                outputsize=self._period_to_outputsize(period)
            )

            if not benchmark_data or 'values' not in benchmark_data:
                return {'error': f'Failed to fetch benchmark data for {benchmark}'}

            bench_df = pd.DataFrame(benchmark_data['values'])
            bench_df['datetime'] = pd.to_datetime(bench_df['datetime'])
            bench_df = bench_df.set_index('datetime').sort_index()
            bench_df['close'] = pd.to_numeric(bench_df['close'], errors='coerce')
            bench_returns = bench_df['close'].pct_change().dropna()

            # Analyze each ticker
            leadership_analysis = []

            for ticker in tickers:
                try:
                    # Fetch ticker data
                    data = await self.market_data.get_time_series(
                        symbol=ticker,
                        interval="1day",
                        outputsize=self._period_to_outputsize(period)
                    )

                    if not data or 'values' not in data:
                        continue

                    df = pd.DataFrame(data['values'])
                    df['datetime'] = pd.to_datetime(df['datetime'])
                    df = df.set_index('datetime').sort_index()
                    df['close'] = pd.to_numeric(df['close'], errors='coerce')

                    # Calculate returns
                    returns = df['close'].pct_change().dropna()

                    # Calculate beta
                    beta = self.stats.calculate_beta(returns, bench_returns, min_periods=20)

                    # Calculate lead-lag with benchmark
                    lead_lag = self.stats.calculate_lead_lag(
                        df['close'],
                        bench_df['close'],
                        max_lag=5
                    )

                    # Calculate correlation with benchmark
                    correlation = returns.corr(bench_returns)

                    # Determine leadership category
                    if lead_lag['lag_periods'] > 0 and lead_lag['leader'] == 'series1':
                        leadership_type = 'leader'
                    elif lead_lag['lag_periods'] > 0 and lead_lag['leader'] == 'series2':
                        leadership_type = 'laggard'
                    else:
                        leadership_type = 'simultaneous'

                    leadership_analysis.append({
                        'ticker': ticker,
                        'beta': beta,
                        'correlation': float(correlation),
                        'lead_lag_periods': lead_lag['lag_periods'],
                        'leadership_type': leadership_type,
                        'lead_lag_correlation': lead_lag['best_correlation'],
                        'interpretation': self._interpret_leadership(beta, correlation, leadership_type)
                    })

                except Exception as e:
                    logger.warning(f"Failed to analyze {ticker}: {e}")

            # Sort by absolute beta (most sensitive to market)
            leadership_analysis.sort(key=lambda x: abs(x.get('beta', 0)), reverse=True)

            result = {
                'leadership_analysis': leadership_analysis,
                'benchmark': benchmark,
                'period': period,
                'leaders': [x for x in leadership_analysis if x['leadership_type'] == 'leader'],
                'laggards': [x for x in leadership_analysis if x['leadership_type'] == 'laggard'],
                'timestamp': datetime.now().isoformat()
            }

            # Cache for 1 hour
            await self.cache.set(cache_key, json.dumps(result), ttl=3600)

            return result

        except Exception as e:
            logger.error(f"Error analyzing market leadership: {e}")
            return {'error': str(e)}

    # Helper methods

    def _period_to_outputsize(self, period: str) -> int:
        """Convert period string to outputsize."""
        mapping = {
            '1week': 7,
            '2week': 14,
            '1month': 30,
            '3month': 90,
            '6month': 180,
            '1year': 365,
            '2year': 730
        }
        return mapping.get(period, 90)

    def _prepare_heatmap_data(self, corr_matrix: pd.DataFrame) -> List[Dict]:
        """Convert correlation matrix to heatmap-friendly format."""
        heatmap_data = []
        tickers = corr_matrix.columns.tolist()

        for i, ticker1 in enumerate(tickers):
            for j, ticker2 in enumerate(tickers):
                corr_value = corr_matrix.loc[ticker1, ticker2]
                if pd.notna(corr_value):
                    heatmap_data.append({
                        'x': ticker1,
                        'y': ticker2,
                        'value': float(corr_value),
                        'color': self._correlation_to_color(corr_value)
                    })

        return heatmap_data

    def _correlation_to_color(self, corr: float) -> str:
        """Map correlation value to color code."""
        if corr > 0.7:
            return 'strong_positive'
        elif corr > 0.3:
            return 'moderate_positive'
        elif corr > -0.3:
            return 'weak'
        elif corr > -0.7:
            return 'moderate_negative'
        else:
            return 'strong_negative'

    def _generate_diversification_suggestions(
        self,
        portfolio: Dict[str, float],
        corr_matrix: pd.DataFrame,
        redundant: List[Dict]
    ) -> List[Dict]:
        """Generate suggestions for improving portfolio diversification."""
        suggestions = []

        # Suggest reducing redundant holdings
        if redundant:
            total_redundant_weight = sum(r['potential_savings'] for r in redundant)
            suggestions.append({
                'type': 'reduce_redundancy',
                'message': f'Consider reducing {len(redundant)} highly correlated pairs',
                'potential_improvement': f'{total_redundant_weight:.1%} weight can be reallocated',
                'pairs': redundant[:5]  # Top 5
            })

        # Suggest adding uncorrelated assets
        avg_corr = corr_matrix.values[~np.eye(len(corr_matrix), dtype=bool)].mean()
        if avg_corr > 0.6:
            suggestions.append({
                'type': 'add_diversification',
                'message': 'Portfolio average correlation is high',
                'current_avg_correlation': float(avg_corr),
                'recommendation': 'Consider adding assets from different sectors or asset classes'
            })

        return suggestions

    def _interpret_leadership(self, beta: float, correlation: float, leadership_type: str) -> str:
        """Generate human-readable interpretation of leadership metrics."""
        if pd.isna(beta):
            return "Insufficient data for analysis"

        interpretations = []

        # Beta interpretation
        if beta > 1.2:
            interpretations.append("High volatility relative to market")
        elif beta < 0.8:
            interpretations.append("Low volatility relative to market")
        else:
            interpretations.append("Similar volatility to market")

        # Correlation interpretation
        if abs(correlation) > 0.7:
            interpretations.append("strongly correlated")
        elif abs(correlation) > 0.3:
            interpretations.append("moderately correlated")
        else:
            interpretations.append("weakly correlated")

        # Leadership interpretation
        if leadership_type == 'leader':
            interpretations.append("tends to move before the market")
        elif leadership_type == 'laggard':
            interpretations.append("tends to follow market movements")
        else:
            interpretations.append("moves with the market")

        return "; ".join(interpretations)
