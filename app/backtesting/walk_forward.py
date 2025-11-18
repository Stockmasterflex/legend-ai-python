"""
Walk-Forward Optimization
Rolling window optimization with out-of-sample validation and overfitting detection
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any, Tuple
import asyncio
import logging
import numpy as np
import pandas as pd
from itertools import product

from .engine import BacktestEngine, BacktestConfig
from .strategy import Strategy
from .metrics import calculate_metrics, overfitting_score as calc_overfit_score

logger = logging.getLogger(__name__)


@dataclass
class WalkForwardWindow:
    """Single walk-forward window"""
    window_number: int
    in_sample_start: datetime
    in_sample_end: datetime
    out_sample_start: datetime
    out_sample_end: datetime

    # Results
    optimized_parameters: Optional[Dict[str, Any]] = None
    in_sample_metrics: Optional[Dict] = None
    out_sample_metrics: Optional[Dict] = None


@dataclass
class WalkForwardConfig:
    """Walk-forward optimization configuration"""
    strategy: Strategy
    start_date: datetime
    end_date: datetime
    initial_capital: float
    universe: List[str]

    # Window configuration
    in_sample_days: int = 252  # 1 year
    out_sample_days: int = 63  # 3 months (quarter)
    step_days: int = 63  # Roll forward by 3 months

    # Optimization
    parameter_ranges: Dict[str, List[Any]]  # {"param1": [val1, val2, ...], ...}
    optimization_metric: str = "sharpe_ratio"  # What to optimize
    optimization_type: str = "grid"  # grid, random, bayesian

    # For random/bayesian
    n_trials: int = 100

    # Data provider
    data_provider: Optional[Callable] = None

    # Callbacks
    on_window_complete: Optional[Callable] = None
    on_progress: Optional[Callable] = None


class WalkForwardOptimizer:
    """
    Walk-forward optimizer with out-of-sample validation
    """

    def __init__(self, config: WalkForwardConfig):
        """
        Initialize walk-forward optimizer

        Args:
            config: Walk-forward configuration
        """
        self.config = config
        self.windows: List[WalkForwardWindow] = []
        self.results: Dict[str, Any] = {}
        self.is_running = False

    async def run(self) -> Dict:
        """
        Run walk-forward optimization

        Returns:
            Optimization results
        """
        logger.info("Starting walk-forward optimization")
        self.is_running = True

        try:
            # Generate windows
            self._generate_windows()

            logger.info(f"Generated {len(self.windows)} walk-forward windows")

            # Process each window
            for i, window in enumerate(self.windows):
                if not self.is_running:
                    break

                logger.info(f"Processing window {window.window_number}/{len(self.windows)}")

                # Optimize on in-sample period
                best_params = await self._optimize_window(window)
                window.optimized_parameters = best_params

                # Validate on out-of-sample period
                out_sample_results = await self._validate_window(window)
                window.out_sample_metrics = out_sample_results

                # Callback
                if self.config.on_window_complete:
                    await self.config.on_window_complete(window, i + 1, len(self.windows))

                # Progress
                if self.config.on_progress:
                    progress = ((i + 1) / len(self.windows)) * 100
                    await self.config.on_progress(progress)

            # Aggregate results
            self._aggregate_results()

            logger.info("Walk-forward optimization completed")

            return self.results

        except Exception as e:
            logger.error(f"Walk-forward optimization failed: {e}")
            raise

        finally:
            self.is_running = False

    def _generate_windows(self):
        """Generate all walk-forward windows"""
        current_start = self.config.start_date
        window_number = 1

        while True:
            # In-sample period
            in_sample_start = current_start
            in_sample_end = in_sample_start + timedelta(days=self.config.in_sample_days)

            # Out-of-sample period
            out_sample_start = in_sample_end + timedelta(days=1)
            out_sample_end = out_sample_start + timedelta(days=self.config.out_sample_days)

            # Check if we've exceeded the end date
            if out_sample_end > self.config.end_date:
                break

            # Create window
            window = WalkForwardWindow(
                window_number=window_number,
                in_sample_start=in_sample_start,
                in_sample_end=in_sample_end,
                out_sample_start=out_sample_start,
                out_sample_end=out_sample_end,
            )

            self.windows.append(window)

            # Move to next window
            current_start += timedelta(days=self.config.step_days)
            window_number += 1

    async def _optimize_window(self, window: WalkForwardWindow) -> Dict[str, Any]:
        """
        Optimize parameters for a window's in-sample period

        Args:
            window: Walk-forward window

        Returns:
            Best parameters
        """
        if self.config.optimization_type == "grid":
            return await self._grid_search(window)
        elif self.config.optimization_type == "random":
            return await self._random_search(window)
        elif self.config.optimization_type == "bayesian":
            return await self._bayesian_search(window)
        else:
            raise ValueError(f"Unknown optimization type: {self.config.optimization_type}")

    async def _grid_search(self, window: WalkForwardWindow) -> Dict[str, Any]:
        """Grid search optimization"""
        param_names = list(self.config.parameter_ranges.keys())
        param_values = list(self.config.parameter_ranges.values())

        # Generate all combinations
        param_combinations = list(product(*param_values))

        logger.info(f"Grid search: testing {len(param_combinations)} parameter combinations")

        best_score = -np.inf
        best_params = None

        for i, param_combo in enumerate(param_combinations):
            # Create parameter dict
            params = dict(zip(param_names, param_combo))

            # Run backtest with these parameters
            score, metrics = await self._run_optimization_backtest(
                window.in_sample_start,
                window.in_sample_end,
                params,
            )

            if score > best_score:
                best_score = score
                best_params = params
                window.in_sample_metrics = metrics

            if (i + 1) % 10 == 0:
                logger.debug(f"Tested {i + 1}/{len(param_combinations)} combinations")

        logger.info(f"Best {self.config.optimization_metric}: {best_score:.4f} with params: {best_params}")

        return best_params

    async def _random_search(self, window: WalkForwardWindow) -> Dict[str, Any]:
        """Random search optimization"""
        logger.info(f"Random search: testing {self.config.n_trials} random combinations")

        best_score = -np.inf
        best_params = None

        for trial in range(self.config.n_trials):
            # Generate random parameters
            params = {}
            for param_name, param_range in self.config.parameter_ranges.items():
                params[param_name] = np.random.choice(param_range)

            # Run backtest
            score, metrics = await self._run_optimization_backtest(
                window.in_sample_start,
                window.in_sample_end,
                params,
            )

            if score > best_score:
                best_score = score
                best_params = params
                window.in_sample_metrics = metrics

        logger.info(f"Best {self.config.optimization_metric}: {best_score:.4f} with params: {best_params}")

        return best_params

    async def _bayesian_search(self, window: WalkForwardWindow) -> Dict[str, Any]:
        """
        Bayesian optimization (simplified version)
        For production, use libraries like Optuna or scikit-optimize
        """
        # This is a placeholder - implement with Optuna in production
        logger.warning("Bayesian optimization not fully implemented, falling back to random search")
        return await self._random_search(window)

    async def _run_optimization_backtest(
        self,
        start_date: datetime,
        end_date: datetime,
        parameters: Dict[str, Any],
    ) -> Tuple[float, Dict]:
        """
        Run backtest with specific parameters

        Args:
            start_date: Backtest start
            end_date: Backtest end
            parameters: Strategy parameters

        Returns:
            (optimization_metric_value, all_metrics)
        """
        # Update strategy parameters
        strategy = self.config.strategy
        for key, value in parameters.items():
            strategy.set_parameter(key, value)

        # Create backtest config
        backtest_config = BacktestConfig(
            strategy=strategy,
            start_date=start_date,
            end_date=end_date,
            initial_capital=self.config.initial_capital,
            universe=self.config.universe,
            data_provider=self.config.data_provider,
        )

        # Run backtest
        engine = BacktestEngine(backtest_config)
        results = await engine.run()

        # Extract optimization metric
        performance = results.get("performance", {})
        metric_value = performance.get(self.config.optimization_metric, 0.0)

        return metric_value, performance

    async def _validate_window(self, window: WalkForwardWindow) -> Dict:
        """
        Validate optimized parameters on out-of-sample period

        Args:
            window: Walk-forward window with optimized parameters

        Returns:
            Out-of-sample metrics
        """
        if window.optimized_parameters is None:
            return {}

        logger.info(f"Validating window {window.window_number} on out-of-sample period")

        # Run backtest on out-of-sample period
        _, metrics = await self._run_optimization_backtest(
            window.out_sample_start,
            window.out_sample_end,
            window.optimized_parameters,
        )

        return metrics

    def _aggregate_results(self):
        """Aggregate results across all windows"""
        if len(self.windows) == 0:
            return

        # Collect metrics from all windows
        in_sample_sharpes = []
        out_sample_sharpes = []
        in_sample_returns = []
        out_sample_returns = []
        degradations = []

        for window in self.windows:
            if window.in_sample_metrics and window.out_sample_metrics:
                in_sharpe = window.in_sample_metrics.get("sharpe_ratio", 0)
                out_sharpe = window.out_sample_metrics.get("sharpe_ratio", 0)
                in_return = window.in_sample_metrics.get("total_return", 0)
                out_return = window.out_sample_metrics.get("total_return", 0)

                in_sample_sharpes.append(in_sharpe)
                out_sample_sharpes.append(out_sharpe)
                in_sample_returns.append(in_return)
                out_sample_returns.append(out_return)

                # Calculate degradation
                if in_sharpe > 0:
                    degradation = (in_sharpe - out_sharpe) / in_sharpe
                    degradations.append(degradation)

        # Aggregate statistics
        self.results = {
            "total_windows": len(self.windows),
            "avg_in_sample_sharpe": np.mean(in_sample_sharpes) if in_sample_sharpes else 0,
            "avg_out_sample_sharpe": np.mean(out_sample_sharpes) if out_sample_sharpes else 0,
            "avg_in_sample_return": np.mean(in_sample_returns) if in_sample_returns else 0,
            "avg_out_sample_return": np.mean(out_sample_returns) if out_sample_returns else 0,
            "avg_degradation": np.mean(degradations) if degradations else 0,
            "degradation_std": np.std(degradations) if degradations else 0,
            "consistency_score": 1.0 - np.std(out_sample_sharpes) if out_sample_sharpes else 0,
        }

        # Overfitting detection
        if in_sample_sharpes and out_sample_sharpes:
            avg_in_sharpe = np.mean(in_sample_sharpes)
            avg_out_sharpe = np.mean(out_sample_sharpes)
            avg_in_return = np.mean(in_sample_returns)
            avg_out_return = np.mean(out_sample_returns)
            n_params = len(self.config.parameter_ranges)

            overfit_score = calc_overfit_score(
                avg_in_sharpe,
                avg_out_sharpe,
                avg_in_return,
                avg_out_return,
                n_params,
            )

            self.results["overfitting_score"] = overfit_score
            self.results["is_overfit"] = overfit_score > 0.5  # Threshold

        # Robust parameters (most common across windows)
        self.results["robust_parameters"] = self._find_robust_parameters()

        # Window details
        self.results["windows"] = [
            {
                "window_number": w.window_number,
                "in_sample_start": w.in_sample_start.isoformat(),
                "in_sample_end": w.in_sample_end.isoformat(),
                "out_sample_start": w.out_sample_start.isoformat(),
                "out_sample_end": w.out_sample_end.isoformat(),
                "optimized_parameters": w.optimized_parameters,
                "in_sample_metrics": w.in_sample_metrics,
                "out_sample_metrics": w.out_sample_metrics,
            }
            for w in self.windows
        ]

    def _find_robust_parameters(self) -> Dict[str, Any]:
        """
        Find the most robust parameters across windows
        Uses frequency analysis and out-of-sample performance weighting
        """
        if len(self.windows) == 0:
            return {}

        # For each parameter, track values and their out-of-sample performance
        param_performance: Dict[str, Dict[Any, List[float]]] = {}

        for window in self.windows:
            if window.optimized_parameters and window.out_sample_metrics:
                out_sharpe = window.out_sample_metrics.get("sharpe_ratio", 0)

                for param_name, param_value in window.optimized_parameters.items():
                    if param_name not in param_performance:
                        param_performance[param_name] = {}

                    if param_value not in param_performance[param_name]:
                        param_performance[param_name][param_value] = []

                    param_performance[param_name][param_value].append(out_sharpe)

        # Find best value for each parameter
        robust_params = {}
        for param_name, values_dict in param_performance.items():
            # Calculate average out-of-sample performance for each value
            value_scores = {
                value: np.mean(sharpes)
                for value, sharpes in values_dict.items()
            }

            # Select value with best average out-of-sample performance
            best_value = max(value_scores.items(), key=lambda x: x[1])[0]
            robust_params[param_name] = best_value

        return robust_params

    def stop(self):
        """Stop optimization"""
        self.is_running = False

    def get_results(self) -> Dict:
        """Get optimization results"""
        return self.results

    def get_windows(self) -> List[WalkForwardWindow]:
        """Get all windows"""
        return self.windows
