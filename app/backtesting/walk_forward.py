"""
Walk-Forward Optimization Module
Implements rolling window optimization for strategy robustness testing
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class WalkForwardConfig:
    """Configuration for walk-forward optimization"""

    in_sample_days: int = 252  # ~1 year
    out_sample_days: int = 63  # ~3 months
    step_days: int = 63  # Step size between windows
    parameter_ranges: Dict[str, List[Any]] = field(default_factory=dict)
    optimization_metric: str = "sharpe_ratio"
    optimization_type: str = "grid"  # grid, random, bayesian
    n_trials: int = 100
    min_trades_per_window: int = 10
    parallel_windows: bool = False


@dataclass
class WindowResult:
    """Results from a single walk-forward window"""

    window_id: int
    in_sample_start: datetime
    in_sample_end: datetime
    out_sample_start: datetime
    out_sample_end: datetime
    best_params: Dict[str, Any]
    in_sample_metric: float
    out_sample_metric: float
    out_sample_return: float
    out_sample_sharpe: float
    out_sample_trades: int
    degradation_pct: float  # IS vs OOS performance difference


class WalkForwardOptimizer:
    """
    Walk-Forward Optimization Engine

    Performs rolling window optimization to test strategy robustness:
    1. Optimize parameters on in-sample period
    2. Test optimized parameters on out-of-sample period
    3. Roll forward and repeat
    4. Combine OOS results for final performance estimate
    """

    def __init__(
        self,
        config: WalkForwardConfig,
        backtest_engine: Any = None,
        data_provider: Any = None,
    ):
        self.config = config
        self.backtest_engine = backtest_engine
        self.data_provider = data_provider
        self.window_results: List[WindowResult] = []
        self.is_running = False
        self.progress = 0.0

    def generate_windows(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> List[Dict[str, datetime]]:
        """
        Generate walk-forward windows based on configuration

        Returns list of windows with in-sample and out-sample date ranges
        """
        windows = []
        current_start = start_date

        while True:
            in_sample_end = current_start + timedelta(days=self.config.in_sample_days)
            out_sample_start = in_sample_end
            out_sample_end = out_sample_start + timedelta(
                days=self.config.out_sample_days
            )

            # Check if we have enough data for this window
            if out_sample_end > end_date:
                break

            windows.append(
                {
                    "in_sample_start": current_start,
                    "in_sample_end": in_sample_end,
                    "out_sample_start": out_sample_start,
                    "out_sample_end": out_sample_end,
                }
            )

            # Step forward
            current_start += timedelta(days=self.config.step_days)

        return windows

    async def run(
        self,
        strategy: Any,
        start_date: datetime,
        end_date: datetime,
        universe: List[str],
        progress_callback: Optional[Callable[[float], None]] = None,
    ) -> Dict[str, Any]:
        """
        Execute walk-forward optimization

        Args:
            strategy: Strategy to optimize
            start_date: Start of total period
            end_date: End of total period
            universe: List of ticker symbols
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary with combined results and window details
        """
        self.is_running = True
        self.window_results = []

        windows = self.generate_windows(start_date, end_date)
        n_windows = len(windows)

        if n_windows == 0:
            logger.warning("No valid walk-forward windows generated")
            return {
                "status": "failed",
                "error": "Insufficient data for walk-forward optimization",
            }

        logger.info(f"Starting walk-forward optimization with {n_windows} windows")

        combined_oos_returns = []
        combined_oos_sharpes = []

        for i, window in enumerate(windows):
            try:
                # Optimize on in-sample period
                best_params, is_metric = await self._optimize_in_sample(
                    strategy,
                    window["in_sample_start"],
                    window["in_sample_end"],
                    universe,
                )

                # Test on out-of-sample period
                oos_results = await self._test_out_of_sample(
                    strategy,
                    best_params,
                    window["out_sample_start"],
                    window["out_sample_end"],
                    universe,
                )

                # Calculate degradation
                degradation = 0.0
                if is_metric != 0:
                    degradation = (
                        (
                            is_metric
                            - oos_results.get(self.config.optimization_metric, 0)
                        )
                        / abs(is_metric)
                    ) * 100

                result = WindowResult(
                    window_id=i,
                    in_sample_start=window["in_sample_start"],
                    in_sample_end=window["in_sample_end"],
                    out_sample_start=window["out_sample_start"],
                    out_sample_end=window["out_sample_end"],
                    best_params=best_params,
                    in_sample_metric=is_metric,
                    out_sample_metric=oos_results.get(
                        self.config.optimization_metric, 0
                    ),
                    out_sample_return=oos_results.get("total_return", 0),
                    out_sample_sharpe=oos_results.get("sharpe_ratio", 0),
                    out_sample_trades=oos_results.get("total_trades", 0),
                    degradation_pct=degradation,
                )

                self.window_results.append(result)
                combined_oos_returns.append(result.out_sample_return)
                combined_oos_sharpes.append(result.out_sample_sharpe)

            except Exception as e:
                logger.error(f"Error processing window {i}: {e}")

            # Update progress
            self.progress = (i + 1) / n_windows * 100
            if progress_callback:
                progress_callback(self.progress)

        self.is_running = False

        # Calculate combined results
        combined_return = sum(combined_oos_returns) if combined_oos_returns else 0
        avg_sharpe = (
            sum(combined_oos_sharpes) / len(combined_oos_sharpes)
            if combined_oos_sharpes
            else 0
        )

        # Calculate robustness score (% of windows with positive OOS)
        positive_windows = sum(
            1 for r in self.window_results if r.out_sample_return > 0
        )
        robustness_score = (
            (positive_windows / len(self.window_results) * 100)
            if self.window_results
            else 0
        )

        return {
            "status": "completed",
            "n_windows": n_windows,
            "combined_oos_return": combined_return,
            "combined_oos_sharpe": avg_sharpe,
            "robustness_score": robustness_score,
            "avg_degradation": (
                sum(r.degradation_pct for r in self.window_results)
                / len(self.window_results)
                if self.window_results
                else 0
            ),
            "window_results": [
                {
                    "window_id": r.window_id,
                    "best_params": r.best_params,
                    "is_metric": r.in_sample_metric,
                    "oos_metric": r.out_sample_metric,
                    "oos_return": r.out_sample_return,
                    "oos_sharpe": r.out_sample_sharpe,
                    "degradation_pct": r.degradation_pct,
                }
                for r in self.window_results
            ],
        }

    async def _optimize_in_sample(
        self,
        strategy: Any,
        start_date: datetime,
        end_date: datetime,
        universe: List[str],
    ) -> tuple:
        """
        Optimize strategy parameters on in-sample period

        Returns (best_params, best_metric_value)
        """
        # Placeholder implementation
        # In production, implement grid/random/bayesian search
        logger.info(f"Optimizing on in-sample period: {start_date} to {end_date}")

        best_params = {}
        best_metric = 0.0

        # Return default params for now
        return best_params, best_metric

    async def _test_out_of_sample(
        self,
        strategy: Any,
        params: Dict[str, Any],
        start_date: datetime,
        end_date: datetime,
        universe: List[str],
    ) -> Dict[str, Any]:
        """
        Test optimized parameters on out-of-sample period

        Returns backtest metrics dictionary
        """
        # Placeholder implementation
        logger.info(f"Testing on out-of-sample period: {start_date} to {end_date}")

        return {
            "total_return": 0.0,
            "sharpe_ratio": 0.0,
            "total_trades": 0,
        }
