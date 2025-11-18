"""
Multi-Ticker Comparison Service
Provides side-by-side analysis, correlation, relative strength, and pair trading analytics.
"""
from __future__ import annotations

import asyncio
import logging
import math
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.stattools import coint

from app.core.metrics import (
    compute_atr,
    last_valid,
    percentage_distance,
    relative_strength_metrics,
    sanitize_series,
)
from app.services.market_data import market_data_service

logger = logging.getLogger(__name__)


class TickerComparisonService:
    """
    Multi-ticker comparison service with advanced analytics:
    - Multi-chart synchronized data
    - Relative strength analysis (vs SPY, vs sector)
    - Correlation analysis (price, volume, patterns)
    - Pair trading analytics (spread, z-score, cointegration)
    - Metrics comparison table
    """

    def __init__(self):
        self.market_data = market_data_service

    async def compare_tickers(
        self,
        tickers: List[str],
        interval: str = "1day",
        bars: int = 252,
        benchmark: str = "SPY",
    ) -> Dict[str, Any]:
        """
        Compare multiple tickers with comprehensive analytics.

        Args:
            tickers: List of ticker symbols to compare
            interval: Time interval (1day, 1hour, etc.)
            bars: Number of bars to fetch
            benchmark: Benchmark symbol for relative strength (default: SPY)

        Returns:
            Dictionary with comparison data, metrics, and analytics
        """
        if not tickers or len(tickers) < 2:
            return {"error": "At least 2 tickers required for comparison"}

        if len(tickers) > 9:
            return {"error": "Maximum 9 tickers allowed for comparison"}

        try:
            # Fetch data for all tickers + benchmark in parallel
            all_symbols = list(set(tickers + [benchmark]))
            tasks = [
                self.market_data.get_time_series(symbol, interval, bars)
                for symbol in all_symbols
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Build data dictionary
            data_map: Dict[str, Dict[str, Any]] = {}
            for symbol, result in zip(all_symbols, results):
                if isinstance(result, Exception):
                    logger.warning(f"Error fetching {symbol}: {result}")
                    data_map[symbol] = {"error": str(result)}
                else:
                    data_map[symbol] = result

            # Validate we have benchmark data
            if benchmark not in data_map or "error" in data_map[benchmark]:
                return {"error": f"Failed to fetch benchmark data for {benchmark}"}

            benchmark_closes = data_map[benchmark].get("c", [])
            if not benchmark_closes:
                return {"error": f"No price data for benchmark {benchmark}"}

            # Build comprehensive comparison
            comparison = {
                "tickers": tickers,
                "benchmark": benchmark,
                "interval": interval,
                "bars": bars,
                "timestamp": datetime.utcnow().isoformat(),
                "chart_data": {},
                "metrics": {},
                "relative_strength": {},
                "correlation_matrix": {},
                "leader_laggard": {},
            }

            # Process each ticker
            valid_tickers = []
            for ticker in tickers:
                if ticker not in data_map or "error" in data_map[ticker]:
                    comparison["chart_data"][ticker] = {"error": "No data available"}
                    continue

                ticker_data = data_map[ticker]
                if not ticker_data.get("c"):
                    comparison["chart_data"][ticker] = {"error": "No price data"}
                    continue

                valid_tickers.append(ticker)

                # Chart data (OHLCV + timestamps)
                comparison["chart_data"][ticker] = {
                    "timestamps": ticker_data.get("t", []),
                    "open": ticker_data.get("o", []),
                    "high": ticker_data.get("h", []),
                    "low": ticker_data.get("l", []),
                    "close": ticker_data.get("c", []),
                    "volume": ticker_data.get("v", []),
                }

                # Metrics
                closes = ticker_data.get("c", [])
                highs = ticker_data.get("h", [])
                lows = ticker_data.get("l", [])
                volumes = ticker_data.get("v", [])

                comparison["metrics"][ticker] = self._calculate_metrics(
                    closes, highs, lows, volumes
                )

                # Relative strength vs benchmark
                comparison["relative_strength"][ticker] = self._calculate_relative_strength(
                    closes, benchmark_closes, ticker, benchmark
                )

            # Correlation analysis (only for valid tickers)
            if len(valid_tickers) >= 2:
                comparison["correlation_matrix"] = self._calculate_correlation_matrix(
                    valid_tickers, data_map
                )
                comparison["leader_laggard"] = self._identify_leaders_laggards(
                    valid_tickers, data_map, benchmark_closes
                )

            return comparison

        except Exception as e:
            logger.error(f"Error in compare_tickers: {e}", exc_info=True)
            return {"error": f"Comparison failed: {str(e)}"}

    async def pair_trading_analysis(
        self,
        ticker1: str,
        ticker2: str,
        interval: str = "1day",
        bars: int = 252,
    ) -> Dict[str, Any]:
        """
        Analyze pair trading opportunities between two tickers.

        Returns:
            - Spread chart
            - Z-score calculations
            - Mean reversion signals
            - Cointegration test results
        """
        try:
            # Fetch data for both tickers
            data1, data2 = await asyncio.gather(
                self.market_data.get_time_series(ticker1, interval, bars),
                self.market_data.get_time_series(ticker2, interval, bars),
            )

            if "error" in str(data1) or "error" in str(data2):
                return {"error": "Failed to fetch ticker data"}

            closes1 = data1.get("c", [])
            closes2 = data2.get("c", [])
            timestamps = data1.get("t", [])

            if not closes1 or not closes2:
                return {"error": "No price data available"}

            # Align data (use minimum length)
            min_len = min(len(closes1), len(closes2))
            closes1 = closes1[-min_len:]
            closes2 = closes2[-min_len:]
            timestamps = timestamps[-min_len:]

            # Calculate spread (simple ratio)
            spread = self._calculate_spread(closes1, closes2)

            # Calculate z-score
            z_scores = self._calculate_zscore(spread)

            # Mean reversion signals
            signals = self._generate_mean_reversion_signals(z_scores)

            # Cointegration test
            cointegration = self._test_cointegration(closes1, closes2)

            # Hedge ratio (optimal ratio for pair trading)
            hedge_ratio = self._calculate_hedge_ratio(closes1, closes2)

            return {
                "ticker1": ticker1,
                "ticker2": ticker2,
                "interval": interval,
                "bars": min_len,
                "timestamps": timestamps,
                "spread": sanitize_series(spread),
                "z_scores": sanitize_series(z_scores),
                "signals": signals,
                "cointegration": cointegration,
                "hedge_ratio": hedge_ratio,
                "statistics": {
                    "spread_mean": float(np.mean(spread)),
                    "spread_std": float(np.std(spread)),
                    "current_spread": spread[-1] if spread else None,
                    "current_zscore": z_scores[-1] if z_scores else None,
                },
            }

        except Exception as e:
            logger.error(f"Error in pair_trading_analysis: {e}", exc_info=True)
            return {"error": f"Pair trading analysis failed: {str(e)}"}

    async def relative_strength_ranking(
        self,
        tickers: List[str],
        benchmark: str = "SPY",
        interval: str = "1day",
        bars: int = 100,
    ) -> Dict[str, Any]:
        """
        Rank tickers by relative strength vs benchmark.

        Returns ranked list with RS metrics.
        """
        try:
            # Fetch benchmark
            benchmark_data = await self.market_data.get_time_series(benchmark, interval, bars)
            benchmark_closes = benchmark_data.get("c", [])

            if not benchmark_closes:
                return {"error": f"No benchmark data for {benchmark}"}

            # Fetch all tickers in parallel
            tasks = [
                self.market_data.get_time_series(ticker, interval, bars)
                for ticker in tickers
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Calculate RS for each ticker
            rankings = []
            for ticker, result in zip(tickers, results):
                if isinstance(result, Exception) or "error" in str(result):
                    continue

                closes = result.get("c", [])
                if not closes:
                    continue

                rs_metrics = relative_strength_metrics(closes, benchmark_closes)

                rankings.append({
                    "ticker": ticker,
                    "rs_rank": rs_metrics.get("rank"),
                    "rs_current": rs_metrics.get("current"),
                    "rs_slope": rs_metrics.get("slope"),
                    "delta_vs_benchmark": rs_metrics.get("delta_vs_spy"),
                })

            # Sort by RS rank (descending)
            rankings.sort(key=lambda x: x.get("rs_rank") or 0, reverse=True)

            # Identify best/worst performers
            best = rankings[:5] if len(rankings) >= 5 else rankings
            worst = rankings[-5:] if len(rankings) >= 5 else []

            return {
                "benchmark": benchmark,
                "total_tickers": len(rankings),
                "rankings": rankings,
                "best_performers": best,
                "worst_performers": worst,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(f"Error in relative_strength_ranking: {e}", exc_info=True)
            return {"error": f"RS ranking failed: {str(e)}"}

    # ========== Private Helper Methods ==========

    def _calculate_metrics(
        self,
        closes: List[float],
        highs: List[float],
        lows: List[float],
        volumes: List[float],
    ) -> Dict[str, Any]:
        """Calculate comprehensive metrics for a ticker."""
        if not closes:
            return {}

        try:
            current_price = last_valid(closes) or 0

            # Price changes
            returns_1d = ((closes[-1] / closes[-2]) - 1) * 100 if len(closes) >= 2 else None
            returns_5d = ((closes[-1] / closes[-6]) - 1) * 100 if len(closes) >= 6 else None
            returns_20d = ((closes[-1] / closes[-21]) - 1) * 100 if len(closes) >= 21 else None
            returns_60d = ((closes[-1] / closes[-61]) - 1) * 100 if len(closes) >= 61 else None

            # Volatility
            returns = [
                (closes[i] / closes[i-1] - 1) * 100
                for i in range(1, len(closes))
                if closes[i-1] != 0
            ]
            volatility = float(np.std(returns[-20:])) if len(returns) >= 20 else None

            # ATR
            atr_values = compute_atr(highs, lows, closes, 14)
            current_atr = atr_values[-1] if atr_values else None
            atr_percent = (current_atr / current_price * 100) if current_atr and current_price else None

            # Volume metrics
            avg_volume_20 = float(np.mean(volumes[-20:])) if len(volumes) >= 20 else None
            current_volume = volumes[-1] if volumes else None
            volume_ratio = (current_volume / avg_volume_20) if current_volume and avg_volume_20 else None

            # High/Low metrics
            high_52w = max(highs[-252:]) if len(highs) >= 252 else max(highs) if highs else None
            low_52w = min(lows[-252:]) if len(lows) >= 252 else min(lows) if lows else None
            dist_from_high = percentage_distance(current_price, high_52w)
            dist_from_low = percentage_distance(current_price, low_52w)

            return {
                "current_price": round(current_price, 2) if current_price else None,
                "returns_1d": round(returns_1d, 2) if returns_1d else None,
                "returns_5d": round(returns_5d, 2) if returns_5d else None,
                "returns_20d": round(returns_20d, 2) if returns_20d else None,
                "returns_60d": round(returns_60d, 2) if returns_60d else None,
                "volatility_20d": round(volatility, 2) if volatility else None,
                "atr_14": round(current_atr, 2) if current_atr else None,
                "atr_percent": round(atr_percent, 2) if atr_percent else None,
                "volume_current": int(current_volume) if current_volume else None,
                "volume_avg_20d": int(avg_volume_20) if avg_volume_20 else None,
                "volume_ratio": round(volume_ratio, 2) if volume_ratio else None,
                "high_52w": round(high_52w, 2) if high_52w else None,
                "low_52w": round(low_52w, 2) if low_52w else None,
                "dist_from_high_pct": dist_from_high,
                "dist_from_low_pct": dist_from_low,
            }
        except Exception as e:
            logger.warning(f"Error calculating metrics: {e}")
            return {}

    def _calculate_relative_strength(
        self,
        closes: List[float],
        benchmark_closes: List[float],
        ticker: str,
        benchmark: str,
    ) -> Dict[str, Any]:
        """Calculate relative strength metrics vs benchmark."""
        try:
            rs_metrics = relative_strength_metrics(closes, benchmark_closes)

            # Add interpretation
            rs_rank = rs_metrics.get("rank")
            if rs_rank is not None:
                if rs_rank >= 80:
                    strength = "Very Strong"
                elif rs_rank >= 60:
                    strength = "Strong"
                elif rs_rank >= 40:
                    strength = "Neutral"
                elif rs_rank >= 20:
                    strength = "Weak"
                else:
                    strength = "Very Weak"
            else:
                strength = "Unknown"

            return {
                **rs_metrics,
                "benchmark": benchmark,
                "strength_label": strength,
            }
        except Exception as e:
            logger.warning(f"Error calculating relative strength for {ticker}: {e}")
            return {}

    def _calculate_correlation_matrix(
        self,
        tickers: List[str],
        data_map: Dict[str, Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Calculate price and volume correlation matrix."""
        try:
            # Build price and volume matrices
            min_len = min(
                len(data_map[t].get("c", []))
                for t in tickers
                if t in data_map and "c" in data_map[t]
            )

            if min_len < 2:
                return {"error": "Insufficient data for correlation"}

            # Price correlation
            price_matrix = {}
            volume_matrix = {}

            for i, ticker1 in enumerate(tickers):
                price_matrix[ticker1] = {}
                volume_matrix[ticker1] = {}

                for ticker2 in tickers:
                    if ticker1 == ticker2:
                        price_matrix[ticker1][ticker2] = 1.0
                        volume_matrix[ticker1][ticker2] = 1.0
                        continue

                    closes1 = data_map[ticker1].get("c", [])[-min_len:]
                    closes2 = data_map[ticker2].get("c", [])[-min_len:]
                    volumes1 = data_map[ticker1].get("v", [])[-min_len:]
                    volumes2 = data_map[ticker2].get("v", [])[-min_len:]

                    # Price correlation
                    if len(closes1) >= 2 and len(closes2) >= 2:
                        price_corr, _ = stats.pearsonr(closes1, closes2)
                        price_matrix[ticker1][ticker2] = round(float(price_corr), 3)
                    else:
                        price_matrix[ticker1][ticker2] = None

                    # Volume correlation
                    if len(volumes1) >= 2 and len(volumes2) >= 2:
                        vol_corr, _ = stats.pearsonr(volumes1, volumes2)
                        volume_matrix[ticker1][ticker2] = round(float(vol_corr), 3)
                    else:
                        volume_matrix[ticker1][ticker2] = None

            return {
                "price_correlation": price_matrix,
                "volume_correlation": volume_matrix,
                "tickers": tickers,
            }
        except Exception as e:
            logger.warning(f"Error calculating correlation matrix: {e}")
            return {"error": str(e)}

    def _identify_leaders_laggards(
        self,
        tickers: List[str],
        data_map: Dict[str, Dict[str, Any]],
        benchmark_closes: List[float],
    ) -> Dict[str, Any]:
        """Identify leaders and laggards based on relative strength."""
        try:
            rankings = []

            for ticker in tickers:
                closes = data_map[ticker].get("c", [])
                if not closes:
                    continue

                rs_metrics = relative_strength_metrics(closes, benchmark_closes)
                rs_rank = rs_metrics.get("rank")
                rs_slope = rs_metrics.get("slope")

                if rs_rank is not None and rs_slope is not None:
                    rankings.append({
                        "ticker": ticker,
                        "rs_rank": rs_rank,
                        "rs_slope": rs_slope,
                    })

            # Sort by RS rank
            rankings.sort(key=lambda x: x["rs_rank"], reverse=True)

            # Identify leaders (top 30%) and laggards (bottom 30%)
            total = len(rankings)
            leader_count = max(1, int(total * 0.3))
            laggard_count = max(1, int(total * 0.3))

            leaders = rankings[:leader_count]
            laggards = rankings[-laggard_count:]

            return {
                "leaders": leaders,
                "laggards": laggards,
                "total_analyzed": total,
            }
        except Exception as e:
            logger.warning(f"Error identifying leaders/laggards: {e}")
            return {}

    def _calculate_spread(self, closes1: List[float], closes2: List[float]) -> List[float]:
        """Calculate price spread (ratio) between two tickers."""
        spread = []
        for c1, c2 in zip(closes1, closes2):
            if c2 != 0:
                spread.append(c1 / c2)
            else:
                spread.append(np.nan)
        return spread

    def _calculate_zscore(self, spread: List[float], window: int = 20) -> List[float]:
        """Calculate rolling z-score of spread."""
        z_scores = []
        for i in range(len(spread)):
            if i < window - 1:
                z_scores.append(np.nan)
                continue

            window_data = spread[i - window + 1 : i + 1]
            mean = np.mean(window_data)
            std = np.std(window_data)

            if std != 0:
                z_score = (spread[i] - mean) / std
                z_scores.append(z_score)
            else:
                z_scores.append(np.nan)

        return z_scores

    def _generate_mean_reversion_signals(
        self,
        z_scores: List[float],
        entry_threshold: float = 2.0,
        exit_threshold: float = 0.5,
    ) -> Dict[str, Any]:
        """Generate mean reversion trading signals based on z-scores."""
        if not z_scores or len(z_scores) < 2:
            return {"signals": [], "current_signal": None}

        signals = []
        current_z = z_scores[-1]

        # Signal logic
        if not math.isnan(current_z):
            if current_z > entry_threshold:
                signal = "SHORT_SPREAD"  # Spread too high, expect reversion
                strength = min(100, abs(current_z - entry_threshold) * 20)
            elif current_z < -entry_threshold:
                signal = "LONG_SPREAD"  # Spread too low, expect reversion
                strength = min(100, abs(current_z + entry_threshold) * 20)
            elif abs(current_z) < exit_threshold:
                signal = "EXIT"  # Close to mean, exit positions
                strength = 0
            else:
                signal = "HOLD"
                strength = 0
        else:
            signal = "NO_SIGNAL"
            strength = 0

        return {
            "current_signal": signal,
            "current_zscore": round(current_z, 2) if not math.isnan(current_z) else None,
            "signal_strength": round(strength, 1),
            "entry_threshold": entry_threshold,
            "exit_threshold": exit_threshold,
        }

    def _test_cointegration(
        self,
        closes1: List[float],
        closes2: List[float],
    ) -> Dict[str, Any]:
        """Test for cointegration between two price series."""
        try:
            # Engle-Granger cointegration test
            score, p_value, _ = coint(closes1, closes2)

            # Interpretation
            if p_value < 0.01:
                result = "Strongly Cointegrated"
            elif p_value < 0.05:
                result = "Cointegrated"
            elif p_value < 0.10:
                result = "Weakly Cointegrated"
            else:
                result = "Not Cointegrated"

            return {
                "test_statistic": round(float(score), 4),
                "p_value": round(float(p_value), 4),
                "result": result,
                "is_cointegrated": p_value < 0.05,
            }
        except Exception as e:
            logger.warning(f"Cointegration test failed: {e}")
            return {
                "error": str(e),
                "result": "Test Failed",
                "is_cointegrated": False,
            }

    def _calculate_hedge_ratio(
        self,
        closes1: List[float],
        closes2: List[float],
    ) -> float:
        """Calculate optimal hedge ratio using linear regression."""
        try:
            # Linear regression: closes1 = beta * closes2 + alpha
            slope, intercept, r_value, p_value, std_err = stats.linregress(closes2, closes1)
            return round(float(slope), 4)
        except Exception as e:
            logger.warning(f"Hedge ratio calculation failed: {e}")
            return 1.0


# Singleton instance
ticker_comparison_service = TickerComparisonService()
