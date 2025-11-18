"""
Walk-Forward Testing
Implements walk-forward optimization and out-of-sample validation
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

from .engine import BacktestEngine, BacktestResult
from .strategy import Strategy

logger = logging.getLogger(__name__)


@dataclass
class WalkForwardWindow:
    """Single walk-forward window"""
    window_num: int
    in_sample_start: datetime
    in_sample_end: datetime
    out_of_sample_start: datetime
    out_of_sample_end: datetime

    # Results
    in_sample_result: Optional[BacktestResult] = None
    out_of_sample_result: Optional[BacktestResult] = None

    # Optimized parameters (if applicable)
    optimized_params: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "window_num": self.window_num,
            "in_sample_period": {
                "start": self.in_sample_start.isoformat(),
                "end": self.in_sample_end.isoformat(),
            },
            "out_of_sample_period": {
                "start": self.out_of_sample_start.isoformat(),
                "end": self.out_of_sample_end.isoformat(),
            },
            "in_sample_metrics": self.in_sample_result.metrics.to_dict() if self.in_sample_result else None,
            "out_of_sample_metrics": self.out_of_sample_result.metrics.to_dict() if self.out_of_sample_result else None,
            "optimized_params": self.optimized_params
        }


@dataclass
class WalkForwardResult:
    """Complete walk-forward analysis results"""
    strategy_name: str
    total_windows: int
    in_sample_ratio: float  # e.g., 0.7 for 70% in-sample, 30% out-of-sample

    # Individual windows
    windows: List[WalkForwardWindow]

    # Aggregate results
    combined_in_sample_return: float
    combined_out_of_sample_return: float
    combined_in_sample_return_pct: float
    combined_out_of_sample_return_pct: float

    # Degradation metrics
    performance_degradation: float  # Difference between in-sample and out-of-sample
    degradation_pct: float

    # Consistency metrics
    out_of_sample_win_rate: float  # % of windows profitable out-of-sample
    correlation_in_out: float  # Correlation between in-sample and out-of-sample returns

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "strategy_name": self.strategy_name,
            "total_windows": self.total_windows,
            "in_sample_ratio": self.in_sample_ratio,
            "windows": [w.to_dict() for w in self.windows],
            "aggregate_results": {
                "in_sample_return": self.combined_in_sample_return,
                "out_of_sample_return": self.combined_out_of_sample_return,
                "in_sample_return_pct": self.combined_in_sample_return_pct,
                "out_of_sample_return_pct": self.combined_out_of_sample_return_pct,
            },
            "degradation": {
                "absolute": self.performance_degradation,
                "percentage": self.degradation_pct,
            },
            "consistency": {
                "out_of_sample_win_rate": self.out_of_sample_win_rate,
                "correlation_in_out": self.correlation_in_out,
            }
        }


class WalkForwardAnalyzer:
    """
    Walk-forward testing framework

    Divides data into rolling in-sample (training) and out-of-sample (testing) windows
    """

    def __init__(
        self,
        in_sample_ratio: float = 0.7,  # 70% in-sample, 30% out-of-sample
        anchored: bool = False,  # Anchored (expanding) or rolling window
    ):
        """
        Initialize walk-forward analyzer

        Args:
            in_sample_ratio: Ratio of in-sample to total window (e.g., 0.7 = 70% in-sample)
            anchored: If True, in-sample window expands; if False, it rolls
        """
        self.in_sample_ratio = in_sample_ratio
        self.anchored = anchored

    def run_walk_forward(
        self,
        strategy: Strategy,
        data: Dict[str, pd.DataFrame],
        num_windows: int = 5,
        initial_capital: float = 100000,
        optimize_params: bool = False,
        param_optimizer: Optional[Callable] = None
    ) -> WalkForwardResult:
        """
        Run walk-forward analysis

        Args:
            strategy: Trading strategy to test
            data: Dictionary of ticker -> OHLCV DataFrame
            num_windows: Number of walk-forward windows
            initial_capital: Starting capital
            optimize_params: Whether to optimize parameters in each window
            param_optimizer: Function to optimize strategy parameters

        Returns:
            WalkForwardResult with complete analysis
        """
        logger.info(f"Starting walk-forward analysis with {num_windows} windows")

        # Create windows
        windows = self._create_windows(data, num_windows)

        # Run backtest for each window
        results_windows = []

        for window in windows:
            logger.info(f"Processing window {window.window_num}/{num_windows}")

            # Optimize parameters on in-sample data if requested
            if optimize_params and param_optimizer:
                optimized_params = param_optimizer(
                    strategy,
                    data,
                    window.in_sample_start,
                    window.in_sample_end
                )
                strategy.set_parameters(**optimized_params)
                window.optimized_params = optimized_params

            # Run in-sample backtest
            engine_in = BacktestEngine(initial_capital=initial_capital)
            in_sample_result = engine_in.run_backtest(
                strategy,
                data,
                window.in_sample_start,
                window.in_sample_end
            )
            window.in_sample_result = in_sample_result

            # Run out-of-sample backtest (with same parameters)
            engine_out = BacktestEngine(initial_capital=initial_capital)
            out_sample_result = engine_out.run_backtest(
                strategy,
                data,
                window.out_of_sample_start,
                window.out_of_sample_end
            )
            window.out_of_sample_result = out_sample_result

            results_windows.append(window)

        # Calculate aggregate metrics
        result = self._aggregate_results(strategy.name, results_windows)

        logger.info(f"Walk-forward complete: Out-of-sample return {result.combined_out_of_sample_return_pct:.2f}%")

        return result

    def _create_windows(
        self,
        data: Dict[str, pd.DataFrame],
        num_windows: int
    ) -> List[WalkForwardWindow]:
        """Create walk-forward windows"""
        # Get all available dates
        all_dates = set()
        for df in data.values():
            all_dates.update(df.index)
        all_dates = sorted(all_dates)

        if len(all_dates) < 100:
            raise ValueError("Insufficient data for walk-forward analysis")

        windows = []
        total_days = len(all_dates)

        if self.anchored:
            # Anchored (expanding window)
            # First window uses first X% of data for in-sample
            first_in_sample_size = int(total_days * self.in_sample_ratio / num_windows)

            for i in range(num_windows):
                # In-sample: from start to expanding end
                in_sample_start = all_dates[0]
                in_sample_end_idx = min(
                    first_in_sample_size + int(i * total_days / num_windows),
                    total_days - 1
                )
                in_sample_end = all_dates[in_sample_end_idx]

                # Out-of-sample: next segment
                out_sample_start_idx = in_sample_end_idx + 1
                out_sample_end_idx = min(
                    in_sample_end_idx + int(total_days * (1 - self.in_sample_ratio) / num_windows),
                    total_days - 1
                )

                if out_sample_start_idx >= total_days:
                    break

                out_sample_start = all_dates[out_sample_start_idx]
                out_sample_end = all_dates[out_sample_end_idx]

                window = WalkForwardWindow(
                    window_num=i + 1,
                    in_sample_start=in_sample_start,
                    in_sample_end=in_sample_end,
                    out_of_sample_start=out_sample_start,
                    out_of_sample_end=out_sample_end
                )
                windows.append(window)

        else:
            # Rolling window
            window_size = total_days // num_windows
            in_sample_size = int(window_size * self.in_sample_ratio)
            out_sample_size = window_size - in_sample_size

            for i in range(num_windows):
                start_idx = i * window_size
                in_sample_end_idx = start_idx + in_sample_size
                out_sample_end_idx = min(in_sample_end_idx + out_sample_size, total_days - 1)

                if in_sample_end_idx >= total_days or out_sample_end_idx >= total_days:
                    break

                window = WalkForwardWindow(
                    window_num=i + 1,
                    in_sample_start=all_dates[start_idx],
                    in_sample_end=all_dates[in_sample_end_idx],
                    out_of_sample_start=all_dates[in_sample_end_idx + 1],
                    out_of_sample_end=all_dates[out_sample_end_idx]
                )
                windows.append(window)

        return windows

    def _aggregate_results(
        self,
        strategy_name: str,
        windows: List[WalkForwardWindow]
    ) -> WalkForwardResult:
        """Aggregate results from all windows"""
        # Calculate combined returns
        in_sample_returns = []
        out_sample_returns = []

        for window in windows:
            if window.in_sample_result:
                in_sample_returns.append(window.in_sample_result.metrics.total_return_pct)
            if window.out_of_sample_result:
                out_sample_returns.append(window.out_of_sample_result.metrics.total_return_pct)

        # Combined metrics
        combined_in_return = sum(in_sample_returns)
        combined_out_return = sum(out_sample_returns)

        avg_in_return_pct = np.mean(in_sample_returns) if in_sample_returns else 0
        avg_out_return_pct = np.mean(out_sample_returns) if out_sample_returns else 0

        # Performance degradation
        degradation = avg_in_return_pct - avg_out_return_pct
        degradation_pct = (degradation / avg_in_return_pct * 100) if avg_in_return_pct != 0 else 0

        # Out-of-sample win rate
        out_wins = sum(1 for r in out_sample_returns if r > 0)
        out_win_rate = (out_wins / len(out_sample_returns)) if out_sample_returns else 0

        # Correlation between in-sample and out-of-sample
        if len(in_sample_returns) > 1 and len(out_sample_returns) > 1:
            correlation = np.corrcoef(in_sample_returns, out_sample_returns)[0, 1]
        else:
            correlation = 0

        return WalkForwardResult(
            strategy_name=strategy_name,
            total_windows=len(windows),
            in_sample_ratio=self.in_sample_ratio,
            windows=windows,
            combined_in_sample_return=combined_in_return,
            combined_out_of_sample_return=combined_out_return,
            combined_in_sample_return_pct=avg_in_return_pct,
            combined_out_of_sample_return_pct=avg_out_return_pct,
            performance_degradation=degradation,
            degradation_pct=degradation_pct,
            out_of_sample_win_rate=out_win_rate * 100,
            correlation_in_out=correlation
        )

    @staticmethod
    def assess_robustness(wf_result: WalkForwardResult) -> Dict[str, Any]:
        """
        Assess strategy robustness based on walk-forward results

        Args:
            wf_result: Walk-forward results

        Returns:
            Dictionary with robustness assessment
        """
        # Check degradation
        degradation_acceptable = abs(wf_result.degradation_pct) < 30  # Less than 30% degradation

        # Check out-of-sample win rate
        out_win_acceptable = wf_result.out_of_sample_win_rate > 50  # More than 50% profitable

        # Check correlation
        correlation_acceptable = wf_result.correlation_in_out > 0.3  # Some positive correlation

        # Overall robustness score
        robustness_score = 0
        if degradation_acceptable:
            robustness_score += 40
        if out_win_acceptable:
            robustness_score += 30
        if correlation_acceptable:
            robustness_score += 30

        # Determine rating
        if robustness_score >= 80:
            rating = "Excellent"
            interpretation = "Strategy shows strong robustness across different market periods."
        elif robustness_score >= 60:
            rating = "Good"
            interpretation = "Strategy demonstrates reasonable robustness with some variation."
        elif robustness_score >= 40:
            rating = "Fair"
            interpretation = "Strategy shows moderate robustness. Consider refinements."
        else:
            rating = "Poor"
            interpretation = "Strategy may be overfit. Significant performance degradation observed."

        return {
            "robustness_score": robustness_score,
            "rating": rating,
            "interpretation": interpretation,
            "criteria": {
                "degradation_acceptable": degradation_acceptable,
                "degradation_pct": wf_result.degradation_pct,
                "out_of_sample_win_rate_acceptable": out_win_acceptable,
                "out_of_sample_win_rate": wf_result.out_of_sample_win_rate,
                "correlation_acceptable": correlation_acceptable,
                "correlation": wf_result.correlation_in_out,
            },
            "recommendations": WalkForwardAnalyzer._generate_recommendations(
                degradation_acceptable,
                out_win_acceptable,
                correlation_acceptable,
                wf_result
            )
        }

    @staticmethod
    def _generate_recommendations(
        degradation_ok: bool,
        win_rate_ok: bool,
        correlation_ok: bool,
        wf_result: WalkForwardResult
    ) -> List[str]:
        """Generate recommendations based on walk-forward results"""
        recommendations = []

        if not degradation_ok:
            recommendations.append(
                f"High performance degradation ({wf_result.degradation_pct:.1f}%). "
                "Consider simplifying strategy or using more robust parameters."
            )

        if not win_rate_ok:
            recommendations.append(
                f"Low out-of-sample win rate ({wf_result.out_of_sample_win_rate:.1f}%). "
                "Strategy may not be consistent across market conditions."
            )

        if not correlation_ok:
            recommendations.append(
                f"Low correlation between in-sample and out-of-sample ({wf_result.correlation_in_out:.2f}). "
                "Strategy performance may be highly sensitive to time period."
            )

        if wf_result.combined_out_of_sample_return_pct < 0:
            recommendations.append(
                "Negative out-of-sample returns. Strategy needs significant revision."
            )

        if not recommendations:
            recommendations.append(
                "Strategy shows good robustness. Consider live testing with small capital."
            )

        return recommendations
