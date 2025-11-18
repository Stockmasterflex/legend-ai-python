"""
Monte Carlo Simulation for Strategy Validation
Randomizes trade sequences to assess strategy robustness
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class MonteCarloResult:
    """Results from Monte Carlo simulation"""
    num_simulations: int
    original_return: float
    original_return_pct: float

    # Distribution statistics
    mean_return: float
    median_return: float
    std_return: float
    min_return: float
    max_return: float

    # Percentiles
    percentile_5: float
    percentile_25: float
    percentile_75: float
    percentile_95: float

    # Risk metrics
    var_95: float  # Value at Risk (95% confidence)
    cvar_95: float  # Conditional VaR (expected loss beyond VaR)

    # Probability metrics
    prob_profit: float  # Probability of making profit
    prob_above_original: float  # Probability of beating original result

    # All simulation results
    all_returns: List[float]
    all_returns_pct: List[float]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "num_simulations": self.num_simulations,
            "original_return": self.original_return,
            "original_return_pct": self.original_return_pct,
            "statistics": {
                "mean_return": self.mean_return,
                "median_return": self.median_return,
                "std_return": self.std_return,
                "min_return": self.min_return,
                "max_return": self.max_return,
            },
            "percentiles": {
                "5th": self.percentile_5,
                "25th": self.percentile_25,
                "75th": self.percentile_75,
                "95th": self.percentile_95,
            },
            "risk": {
                "var_95": self.var_95,
                "cvar_95": self.cvar_95,
            },
            "probabilities": {
                "prob_profit": self.prob_profit,
                "prob_above_original": self.prob_above_original,
            }
        }


class MonteCarloSimulator:
    """
    Monte Carlo simulation for backtesting results

    Randomly reorders trades to assess if results are due to skill or luck
    """

    @staticmethod
    def run_simulation(
        trades: List[Dict[str, Any]],
        initial_capital: float,
        num_simulations: int = 1000,
        replacement: bool = True
    ) -> MonteCarloResult:
        """
        Run Monte Carlo simulation by randomizing trade order

        Args:
            trades: List of trade dictionaries with 'profit_loss'
            initial_capital: Starting capital
            num_simulations: Number of Monte Carlo runs
            replacement: Sample with replacement (allows duplicate trades)

        Returns:
            MonteCarloResult with statistics
        """
        logger.info(f"Running Monte Carlo simulation with {num_simulations} iterations")

        if not trades:
            return MonteCarloSimulator._empty_result(initial_capital)

        # Extract trade P&Ls
        trade_pnls = [t.get("profit_loss", 0) for t in trades]
        original_return = sum(trade_pnls)
        original_return_pct = (original_return / initial_capital) * 100

        # Run simulations
        simulation_returns = []

        for i in range(num_simulations):
            # Randomly reorder trades
            if replacement:
                simulated_trades = np.random.choice(trade_pnls, size=len(trade_pnls), replace=True)
            else:
                simulated_trades = np.random.permutation(trade_pnls)

            # Calculate cumulative return
            total_return = np.sum(simulated_trades)
            simulation_returns.append(total_return)

        simulation_returns = np.array(simulation_returns)
        simulation_returns_pct = (simulation_returns / initial_capital) * 100

        # Calculate statistics
        mean_return = np.mean(simulation_returns)
        median_return = np.median(simulation_returns)
        std_return = np.std(simulation_returns)
        min_return = np.min(simulation_returns)
        max_return = np.max(simulation_returns)

        # Percentiles
        percentile_5 = np.percentile(simulation_returns, 5)
        percentile_25 = np.percentile(simulation_returns, 25)
        percentile_75 = np.percentile(simulation_returns, 75)
        percentile_95 = np.percentile(simulation_returns, 95)

        # Value at Risk (95% confidence) - worst 5% of outcomes
        var_95 = percentile_5

        # Conditional VaR - average of worst 5%
        worst_5_pct = simulation_returns[simulation_returns <= percentile_5]
        cvar_95 = np.mean(worst_5_pct) if len(worst_5_pct) > 0 else var_95

        # Probability metrics
        prob_profit = np.sum(simulation_returns > 0) / num_simulations
        prob_above_original = np.sum(simulation_returns >= original_return) / num_simulations

        logger.info(f"Monte Carlo complete: Mean return ${mean_return:.2f}, " +
                   f"Prob profit: {prob_profit:.1%}")

        return MonteCarloResult(
            num_simulations=num_simulations,
            original_return=original_return,
            original_return_pct=original_return_pct,
            mean_return=mean_return,
            median_return=median_return,
            std_return=std_return,
            min_return=min_return,
            max_return=max_return,
            percentile_5=percentile_5,
            percentile_25=percentile_25,
            percentile_75=percentile_75,
            percentile_95=percentile_95,
            var_95=var_95,
            cvar_95=cvar_95,
            prob_profit=prob_profit,
            prob_above_original=prob_above_original,
            all_returns=simulation_returns.tolist(),
            all_returns_pct=simulation_returns_pct.tolist()
        )

    @staticmethod
    def run_equity_curve_simulation(
        trades: List[Dict[str, Any]],
        initial_capital: float,
        num_simulations: int = 1000
    ) -> Dict[str, Any]:
        """
        Run Monte Carlo simulation and generate equity curve statistics

        Args:
            trades: List of trade dictionaries
            initial_capital: Starting capital
            num_simulations: Number of simulations

        Returns:
            Dictionary with equity curve statistics
        """
        if not trades:
            return {}

        trade_pnls = [t.get("profit_loss", 0) for t in trades]
        num_trades = len(trade_pnls)

        # Run simulations and track equity curves
        all_equity_curves = []

        for _ in range(num_simulations):
            # Randomly reorder trades
            simulated_trades = np.random.permutation(trade_pnls)

            # Build equity curve
            equity = initial_capital
            equity_curve = [equity]

            for pnl in simulated_trades:
                equity += pnl
                equity_curve.append(equity)

            all_equity_curves.append(equity_curve)

        # Convert to numpy array (simulations x timesteps)
        equity_array = np.array(all_equity_curves)

        # Calculate statistics at each point
        mean_curve = np.mean(equity_array, axis=0)
        median_curve = np.median(equity_array, axis=0)
        percentile_5 = np.percentile(equity_array, 5, axis=0)
        percentile_25 = np.percentile(equity_array, 25, axis=0)
        percentile_75 = np.percentile(equity_array, 75, axis=0)
        percentile_95 = np.percentile(equity_array, 95, axis=0)

        # Calculate drawdown statistics across simulations
        max_drawdowns = []
        for equity_curve in all_equity_curves:
            running_max = np.maximum.accumulate(equity_curve)
            drawdown = (np.array(equity_curve) - running_max) / running_max
            max_drawdowns.append(np.min(drawdown) * 100)

        return {
            "mean_curve": mean_curve.tolist(),
            "median_curve": median_curve.tolist(),
            "percentile_5": percentile_5.tolist(),
            "percentile_25": percentile_25.tolist(),
            "percentile_75": percentile_75.tolist(),
            "percentile_95": percentile_95.tolist(),
            "max_drawdown_stats": {
                "mean": np.mean(max_drawdowns),
                "median": np.median(max_drawdowns),
                "worst": np.min(max_drawdowns),
                "best": np.max(max_drawdowns),
            }
        }

    @staticmethod
    def assess_statistical_significance(
        trades: List[Dict[str, Any]],
        initial_capital: float,
        num_simulations: int = 10000,
        confidence_level: float = 0.95
    ) -> Dict[str, Any]:
        """
        Assess if trading results are statistically significant

        Tests if the observed results are likely due to skill vs luck

        Args:
            trades: List of trades
            initial_capital: Starting capital
            num_simulations: Number of simulations
            confidence_level: Confidence level (e.g., 0.95 for 95%)

        Returns:
            Dictionary with significance analysis
        """
        if not trades:
            return {"significant": False, "reason": "No trades"}

        # Run Monte Carlo
        mc_result = MonteCarloSimulator.run_simulation(
            trades, initial_capital, num_simulations
        )

        # Calculate confidence interval
        lower_percentile = ((1 - confidence_level) / 2) * 100
        upper_percentile = (confidence_level + (1 - confidence_level) / 2) * 100

        lower_bound = np.percentile(mc_result.all_returns, lower_percentile)
        upper_bound = np.percentile(mc_result.all_returns, upper_percentile)

        # Check if original result is outside confidence interval
        is_significant = (
            mc_result.original_return > upper_bound or
            mc_result.original_return < lower_bound
        )

        # Calculate Z-score
        z_score = (
            (mc_result.original_return - mc_result.mean_return) / mc_result.std_return
            if mc_result.std_return > 0 else 0
        )

        # Determine direction
        if mc_result.original_return > mc_result.mean_return:
            direction = "outperformance"
        elif mc_result.original_return < mc_result.mean_return:
            direction = "underperformance"
        else:
            direction = "neutral"

        return {
            "significant": is_significant,
            "confidence_level": confidence_level,
            "z_score": z_score,
            "direction": direction,
            "original_return": mc_result.original_return,
            "mean_simulated_return": mc_result.mean_return,
            "std_simulated_return": mc_result.std_return,
            "confidence_interval": {
                "lower": lower_bound,
                "upper": upper_bound
            },
            "percentile_rank": mc_result.prob_above_original * 100,
            "interpretation": MonteCarloSimulator._interpret_significance(
                is_significant, z_score, direction, mc_result.prob_above_original
            )
        }

    @staticmethod
    def _interpret_significance(
        is_significant: bool,
        z_score: float,
        direction: str,
        percentile_rank: float
    ) -> str:
        """Generate human-readable interpretation"""
        if not is_significant:
            return (
                "Results are not statistically significant. "
                "Performance could be attributed to random chance."
            )

        if direction == "outperformance":
            return (
                f"Results show statistically significant outperformance (Z={z_score:.2f}). "
                f"Only {(1-percentile_rank)*100:.1f}% of random simulations achieved this result. "
                "Strategy appears to have genuine edge."
            )
        else:
            return (
                f"Results show statistically significant underperformance (Z={z_score:.2f}). "
                "Strategy may have systematic bias or poor market conditions."
            )

    @staticmethod
    def _empty_result(initial_capital: float) -> MonteCarloResult:
        """Return empty Monte Carlo result"""
        return MonteCarloResult(
            num_simulations=0,
            original_return=0,
            original_return_pct=0,
            mean_return=0,
            median_return=0,
            std_return=0,
            min_return=0,
            max_return=0,
            percentile_5=0,
            percentile_25=0,
            percentile_75=0,
            percentile_95=0,
            var_95=0,
            cvar_95=0,
            prob_profit=0,
            prob_above_original=0,
            all_returns=[],
            all_returns_pct=[]
        )
