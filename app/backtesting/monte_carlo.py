"""
Monte Carlo Simulation
Randomized simulations for strategy robustness testing
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any, Tuple
import asyncio
import logging
import numpy as np
import pandas as pd
import random

from .engine import BacktestEngine, BacktestConfig
from .strategy import Strategy
from .metrics import calculate_metrics, monte_carlo_confidence_bands

logger = logging.getLogger(__name__)


@dataclass
class MonteCarloConfig:
    """Monte Carlo simulation configuration"""
    baseline_backtest_results: Dict  # Results from original backtest
    strategy: Strategy
    start_date: datetime
    end_date: datetime
    initial_capital: float
    universe: List[str]

    # Simulation settings
    n_simulations: int = 1000
    simulation_types: List[str] = None  # ["random_entry", "position_size", "regime"]

    # Random entry timing
    entry_delay_min_days: int = -5  # Can enter up to 5 days before signal
    entry_delay_max_days: int = 5   # Can enter up to 5 days after signal

    # Position size variation
    position_size_variation_pct: float = 20.0  # ±20% variation

    # Market regime simulation
    include_regime_changes: bool = False
    bull_market_adjustment: float = 1.2  # 20% better in bull markets
    bear_market_adjustment: float = 0.8  # 20% worse in bear markets
    regime_change_probability: float = 0.05  # 5% chance of regime change per month

    # Data provider
    data_provider: Optional[Callable] = None

    # Callbacks
    on_simulation_complete: Optional[Callable] = None
    on_progress: Optional[Callable] = None


@dataclass
class MonteCarloSimulation:
    """Single Monte Carlo simulation result"""
    simulation_number: int
    variations_applied: Dict[str, Any]
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    total_trades: int


class MonteCarloEngine:
    """
    Monte Carlo simulation engine
    Tests strategy robustness through randomized variations
    """

    def __init__(self, config: MonteCarloConfig):
        """
        Initialize Monte Carlo engine

        Args:
            config: Monte Carlo configuration
        """
        self.config = config
        self.simulations: List[MonteCarloSimulation] = []
        self.results: Dict[str, Any] = {}
        self.is_running = False

    async def run(self) -> Dict:
        """
        Run Monte Carlo simulations

        Returns:
            Simulation results with statistics and confidence bands
        """
        logger.info(f"Starting Monte Carlo simulations ({self.config.n_simulations} runs)")
        self.is_running = True

        try:
            # Default simulation types if not specified
            if self.config.simulation_types is None:
                self.config.simulation_types = ["random_entry", "position_size"]

            # Run simulations
            for i in range(self.config.n_simulations):
                if not self.is_running:
                    break

                # Generate random variations
                variations = self._generate_variations()

                # Run simulation with variations
                sim_result = await self._run_simulation(i + 1, variations)

                if sim_result:
                    self.simulations.append(sim_result)

                # Callback
                if self.config.on_simulation_complete:
                    await self.config.on_simulation_complete(sim_result, i + 1, self.config.n_simulations)

                # Progress
                if self.config.on_progress:
                    progress = ((i + 1) / self.config.n_simulations) * 100
                    await self.config.on_progress(progress)

                if (i + 1) % 100 == 0:
                    logger.info(f"Completed {i + 1}/{self.config.n_simulations} simulations")

            # Aggregate results
            self._aggregate_results()

            logger.info("Monte Carlo simulations completed")

            return self.results

        except Exception as e:
            logger.error(f"Monte Carlo simulation failed: {e}")
            raise

        finally:
            self.is_running = False

    def _generate_variations(self) -> Dict[str, Any]:
        """Generate random variations for this simulation"""
        variations = {}

        if "random_entry" in self.config.simulation_types:
            # Random entry delay for each trade
            variations["entry_delay_days"] = random.randint(
                self.config.entry_delay_min_days,
                self.config.entry_delay_max_days,
            )

        if "position_size" in self.config.simulation_types:
            # Random position size adjustment
            variation_pct = random.uniform(
                -self.config.position_size_variation_pct,
                self.config.position_size_variation_pct,
            )
            variations["position_size_multiplier"] = 1.0 + (variation_pct / 100)

        if "regime" in self.config.simulation_types and self.config.include_regime_changes:
            # Generate random regime changes throughout the period
            variations["market_regimes"] = self._generate_market_regimes()

        return variations

    def _generate_market_regimes(self) -> List[Tuple[datetime, str, float]]:
        """
        Generate random market regime changes

        Returns:
            List of (date, regime, adjustment_factor) tuples
        """
        regimes = []
        current_date = self.config.start_date
        current_regime = "neutral"
        current_adjustment = 1.0

        while current_date < self.config.end_date:
            # Check for regime change (monthly)
            if random.random() < self.config.regime_change_probability:
                # Change regime
                new_regime = random.choice(["bull", "bear", "neutral"])

                if new_regime == "bull":
                    current_adjustment = self.config.bull_market_adjustment
                elif new_regime == "bear":
                    current_adjustment = self.config.bear_market_adjustment
                else:
                    current_adjustment = 1.0

                current_regime = new_regime
                regimes.append((current_date, current_regime, current_adjustment))

            # Move to next month
            current_date += timedelta(days=30)

        return regimes

    async def _run_simulation(
        self,
        sim_number: int,
        variations: Dict[str, Any],
    ) -> Optional[MonteCarloSimulation]:
        """
        Run a single Monte Carlo simulation

        Args:
            sim_number: Simulation number
            variations: Applied variations

        Returns:
            Simulation result
        """
        try:
            # Create modified strategy
            modified_strategy = self._apply_variations_to_strategy(variations)

            # Create backtest config
            backtest_config = BacktestConfig(
                strategy=modified_strategy,
                start_date=self.config.start_date,
                end_date=self.config.end_date,
                initial_capital=self.config.initial_capital,
                universe=self.config.universe,
                data_provider=self.config.data_provider,
            )

            # Run backtest
            engine = BacktestEngine(backtest_config)
            results = await engine.run()

            # Extract metrics
            performance = results.get("performance", {})

            return MonteCarloSimulation(
                simulation_number=sim_number,
                variations_applied=variations,
                total_return=performance.get("total_return", 0.0),
                sharpe_ratio=performance.get("sharpe_ratio", 0.0),
                max_drawdown=performance.get("max_drawdown", 0.0),
                win_rate=performance.get("win_rate", 0.0),
                total_trades=performance.get("total_trades", 0),
            )

        except Exception as e:
            logger.error(f"Simulation {sim_number} failed: {e}")
            return None

    def _apply_variations_to_strategy(self, variations: Dict[str, Any]) -> Strategy:
        """
        Create a modified strategy with variations applied

        Args:
            variations: Variations to apply

        Returns:
            Modified strategy instance
        """
        # Clone the strategy (simplified - in production, implement proper cloning)
        modified_strategy = self.config.strategy

        # Apply entry delay
        if "entry_delay_days" in variations:
            # Store variation for use during backtesting
            modified_strategy.set_parameter("_mc_entry_delay", variations["entry_delay_days"])

        # Apply position size multiplier
        if "position_size_multiplier" in variations:
            modified_strategy.set_parameter("_mc_position_multiplier", variations["position_size_multiplier"])

        # Apply market regime adjustments
        if "market_regimes" in variations:
            modified_strategy.set_parameter("_mc_regimes", variations["market_regimes"])

        return modified_strategy

    def _aggregate_results(self):
        """Aggregate results across all simulations"""
        if len(self.simulations) == 0:
            return

        # Extract metrics
        returns = [sim.total_return for sim in self.simulations]
        sharpes = [sim.sharpe_ratio for sim in self.simulations]
        drawdowns = [sim.max_drawdown for sim in self.simulations]

        # Baseline comparison
        baseline_return = self.config.baseline_backtest_results.get("performance", {}).get("total_return", 0)
        baseline_sharpe = self.config.baseline_backtest_results.get("performance", {}).get("sharpe_ratio", 0)

        # Calculate statistics
        self.results = {
            "n_simulations": len(self.simulations),
            "baseline_return": baseline_return,
            "baseline_sharpe": baseline_sharpe,

            # Return statistics
            "median_return": np.median(returns),
            "mean_return": np.mean(returns),
            "std_return": np.std(returns),
            "min_return": np.min(returns),
            "max_return": np.max(returns),

            # Confidence intervals (returns)
            "ci_95_lower_return": np.percentile(returns, 2.5),
            "ci_95_upper_return": np.percentile(returns, 97.5),
            "ci_99_lower_return": np.percentile(returns, 0.5),
            "ci_99_upper_return": np.percentile(returns, 99.5),

            # Sharpe statistics
            "median_sharpe": np.median(sharpes),
            "mean_sharpe": np.mean(sharpes),
            "std_sharpe": np.std(sharpes),

            # Confidence intervals (Sharpe)
            "ci_95_lower_sharpe": np.percentile(sharpes, 2.5),
            "ci_95_upper_sharpe": np.percentile(sharpes, 97.5),

            # Drawdown statistics
            "median_drawdown": np.median(drawdowns),
            "mean_drawdown": np.mean(drawdowns),
            "worst_drawdown": np.max(drawdowns),

            # Risk metrics
            "probability_of_profit": (np.array(returns) > 0).sum() / len(returns) * 100,
            "probability_of_loss": (np.array(returns) < 0).sum() / len(returns) * 100,

            # Percentiles
            "return_5th_percentile": np.percentile(returns, 5),   # Worst case
            "return_95th_percentile": np.percentile(returns, 95),  # Best case

            # Distribution data (for histograms)
            "return_distribution": {
                "bins": list(np.histogram(returns, bins=50)[1]),
                "counts": list(np.histogram(returns, bins=50)[0]),
            },
            "sharpe_distribution": {
                "bins": list(np.histogram(sharpes, bins=50)[1]),
                "counts": list(np.histogram(sharpes, bins=50)[0]),
            },
            "drawdown_distribution": {
                "bins": list(np.histogram(drawdowns, bins=50)[1]),
                "counts": list(np.histogram(drawdowns, bins=50)[0]),
            },

            # Comparison to baseline
            "better_than_baseline_pct": (np.array(returns) > baseline_return).sum() / len(returns) * 100,
            "return_diff_from_baseline_mean": np.mean(returns) - baseline_return,
            "return_diff_from_baseline_median": np.median(returns) - baseline_return,

            # Individual simulations (summary)
            "top_10_simulations": sorted(
                [
                    {
                        "simulation_number": sim.simulation_number,
                        "total_return": sim.total_return,
                        "sharpe_ratio": sim.sharpe_ratio,
                        "variations": sim.variations_applied,
                    }
                    for sim in self.simulations
                ],
                key=lambda x: x["total_return"],
                reverse=True,
            )[:10],

            "bottom_10_simulations": sorted(
                [
                    {
                        "simulation_number": sim.simulation_number,
                        "total_return": sim.total_return,
                        "sharpe_ratio": sim.sharpe_ratio,
                        "variations": sim.variations_applied,
                    }
                    for sim in self.simulations
                ],
                key=lambda x: x["total_return"],
            )[:10],
        }

        # Robustness score (0-100)
        # Higher score = more robust (tight distribution, consistently positive)
        consistency = max(0, 100 - (np.std(returns) / max(abs(np.mean(returns)), 1) * 100))
        profitability = self.results["probability_of_profit"]
        robustness_score = (consistency * 0.5 + profitability * 0.5)
        self.results["robustness_score"] = robustness_score

    def stop(self):
        """Stop simulations"""
        self.is_running = False

    def get_results(self) -> Dict:
        """Get simulation results"""
        return self.results

    def get_simulations(self) -> List[MonteCarloSimulation]:
        """Get all simulations"""
        return self.simulations

    def export_results(self) -> pd.DataFrame:
        """Export simulation results as DataFrame"""
        return pd.DataFrame([
            {
                "simulation_number": sim.simulation_number,
                "total_return": sim.total_return,
                "sharpe_ratio": sim.sharpe_ratio,
                "max_drawdown": sim.max_drawdown,
                "win_rate": sim.win_rate,
                "total_trades": sim.total_trades,
                **sim.variations_applied,
            }
            for sim in self.simulations
        ])
