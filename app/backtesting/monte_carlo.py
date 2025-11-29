"""
Monte Carlo Simulation Module
Implements various Monte Carlo methods for strategy robustness testing
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import random
import logging
import statistics

logger = logging.getLogger(__name__)


@dataclass
class MonteCarloConfig:
    """Configuration for Monte Carlo simulation"""
    n_simulations: int = 1000
    simulation_types: List[str] = field(default_factory=lambda: ["random_entry", "position_size"])
    entry_delay_min_days: int = -5
    entry_delay_max_days: int = 5
    position_size_variation_pct: float = 20.0
    trade_shuffle: bool = True
    bootstrap_trades: bool = True
    include_regime_changes: bool = False
    confidence_levels: List[float] = field(default_factory=lambda: [0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95])
    random_seed: Optional[int] = None


@dataclass
class SimulationResult:
    """Result from a single Monte Carlo simulation"""
    simulation_id: int
    simulation_type: str
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    total_trades: int
    modifications: Dict[str, Any]


class MonteCarloEngine:
    """
    Monte Carlo Simulation Engine
    
    Provides various simulation methods to test strategy robustness:
    1. Random Entry Timing - Vary entry dates within a window
    2. Position Size Variation - Vary position sizes
    3. Trade Shuffling - Randomize trade sequence
    4. Bootstrap Resampling - Sample trades with replacement
    5. Regime Simulation - Simulate different market conditions
    """
    
    def __init__(self, config: MonteCarloConfig):
        self.config = config
        self.results: List[SimulationResult] = []
        self.is_running = False
        self.progress = 0.0
        
        if config.random_seed is not None:
            random.seed(config.random_seed)
    
    async def run(
        self,
        baseline_trades: List[Dict[str, Any]],
        baseline_metrics: Dict[str, Any],
        progress_callback: Optional[Callable[[float], None]] = None,
    ) -> Dict[str, Any]:
        """
        Execute Monte Carlo simulations
        
        Args:
            baseline_trades: List of trades from baseline backtest
            baseline_metrics: Metrics from baseline backtest
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary with simulation statistics and distributions
        """
        self.is_running = True
        self.results = []
        
        if not baseline_trades:
            logger.warning("No baseline trades provided for Monte Carlo simulation")
            return {
                "status": "failed",
                "error": "No baseline trades provided",
            }
        
        logger.info(f"Starting Monte Carlo simulation with {self.config.n_simulations} iterations")
        
        returns = []
        sharpes = []
        drawdowns = []
        
        for i in range(self.config.n_simulations):
            try:
                # Run simulation based on configured types
                sim_trades = baseline_trades.copy()
                modifications = {}
                
                for sim_type in self.config.simulation_types:
                    if sim_type == "random_entry":
                        sim_trades, mod = self._apply_random_entry(sim_trades)
                        modifications.update(mod)
                    elif sim_type == "position_size":
                        sim_trades, mod = self._apply_position_size_variation(sim_trades)
                        modifications.update(mod)
                    elif sim_type == "trade_shuffle":
                        sim_trades, mod = self._apply_trade_shuffle(sim_trades)
                        modifications.update(mod)
                    elif sim_type == "bootstrap":
                        sim_trades, mod = self._apply_bootstrap(sim_trades)
                        modifications.update(mod)
                
                # Calculate metrics for modified trades
                metrics = self._calculate_metrics(sim_trades)
                
                result = SimulationResult(
                    simulation_id=i,
                    simulation_type=",".join(self.config.simulation_types),
                    total_return=metrics["total_return"],
                    sharpe_ratio=metrics["sharpe_ratio"],
                    max_drawdown=metrics["max_drawdown"],
                    win_rate=metrics["win_rate"],
                    profit_factor=metrics["profit_factor"],
                    total_trades=len(sim_trades),
                    modifications=modifications,
                )
                
                self.results.append(result)
                returns.append(result.total_return)
                sharpes.append(result.sharpe_ratio)
                drawdowns.append(result.max_drawdown)
                
            except Exception as e:
                logger.error(f"Error in simulation {i}: {e}")
            
            # Update progress
            self.progress = (i + 1) / self.config.n_simulations * 100
            if progress_callback:
                progress_callback(self.progress)
        
        self.is_running = False
        
        # Calculate statistics
        return self._compile_results(
            returns=returns,
            sharpes=sharpes,
            drawdowns=drawdowns,
            baseline_return=baseline_metrics.get("total_return", 0),
        )
    
    def _apply_random_entry(self, trades: List[Dict]) -> tuple:
        """
        Apply random entry timing variation
        
        Shifts entry dates within configured window
        """
        modified_trades = []
        delays = []
        
        for trade in trades:
            delay = random.randint(
                self.config.entry_delay_min_days,
                self.config.entry_delay_max_days
            )
            delays.append(delay)
            
            modified_trade = trade.copy()
            # In production, adjust entry_date by delay days
            modified_trades.append(modified_trade)
        
        return modified_trades, {"avg_delay_days": statistics.mean(delays) if delays else 0}
    
    def _apply_position_size_variation(self, trades: List[Dict]) -> tuple:
        """
        Apply position size variation
        
        Randomly adjusts position sizes within configured percentage
        """
        modified_trades = []
        size_factors = []
        
        for trade in trades:
            factor = 1 + random.uniform(
                -self.config.position_size_variation_pct / 100,
                self.config.position_size_variation_pct / 100
            )
            size_factors.append(factor)
            
            modified_trade = trade.copy()
            if "position_size" in modified_trade:
                modified_trade["position_size"] *= factor
            modified_trades.append(modified_trade)
        
        return modified_trades, {"avg_size_factor": statistics.mean(size_factors) if size_factors else 1}
    
    def _apply_trade_shuffle(self, trades: List[Dict]) -> tuple:
        """
        Shuffle trade sequence
        
        Tests if order of trades affects overall results
        """
        shuffled = trades.copy()
        random.shuffle(shuffled)
        return shuffled, {"shuffled": True}
    
    def _apply_bootstrap(self, trades: List[Dict]) -> tuple:
        """
        Bootstrap resampling
        
        Sample trades with replacement to simulate different trade sequences
        """
        n_trades = len(trades)
        resampled = [random.choice(trades) for _ in range(n_trades)]
        return resampled, {"bootstrap": True, "unique_trades": len(set(id(t) for t in resampled))}
    
    def _calculate_metrics(self, trades: List[Dict]) -> Dict[str, float]:
        """
        Calculate performance metrics for a set of trades
        """
        if not trades:
            return {
                "total_return": 0,
                "sharpe_ratio": 0,
                "max_drawdown": 0,
                "win_rate": 0,
                "profit_factor": 0,
            }
        
        # Simple metrics calculation
        pnls = [t.get("net_profit_loss", 0) for t in trades]
        total_return = sum(pnls)
        
        wins = [p for p in pnls if p > 0]
        losses = [p for p in pnls if p < 0]
        
        win_rate = len(wins) / len(pnls) if pnls else 0
        
        gross_profit = sum(wins) if wins else 0
        gross_loss = abs(sum(losses)) if losses else 0.0001  # Avoid division by zero
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        
        # Simplified Sharpe (in production, use proper calculation)
        if len(pnls) > 1:
            avg_return = statistics.mean(pnls)
            std_return = statistics.stdev(pnls) if len(pnls) > 1 else 0.0001
            sharpe_ratio = (avg_return / std_return) * (252 ** 0.5) if std_return > 0 else 0
        else:
            sharpe_ratio = 0
        
        # Simplified max drawdown
        cumulative = []
        running_sum = 0
        for pnl in pnls:
            running_sum += pnl
            cumulative.append(running_sum)
        
        peak = 0
        max_dd = 0
        for value in cumulative:
            if value > peak:
                peak = value
            dd = (peak - value) / peak if peak > 0 else 0
            if dd > max_dd:
                max_dd = dd
        
        return {
            "total_return": total_return,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_dd * 100,  # As percentage
            "win_rate": win_rate * 100,
            "profit_factor": profit_factor,
        }
    
    def _compile_results(
        self,
        returns: List[float],
        sharpes: List[float],
        drawdowns: List[float],
        baseline_return: float,
    ) -> Dict[str, Any]:
        """
        Compile simulation results into summary statistics
        """
        if not returns:
            return {
                "status": "failed",
                "error": "No valid simulation results",
            }
        
        returns_sorted = sorted(returns)
        n = len(returns_sorted)
        
        # Calculate percentiles
        percentiles = {}
        for level in self.config.confidence_levels:
            idx = int(level * n)
            idx = max(0, min(idx, n - 1))
            percentiles[f"p{int(level * 100)}"] = returns_sorted[idx]
        
        # Probability of profit
        prob_profit = sum(1 for r in returns if r > 0) / n
        
        # Value at Risk (95%)
        var_95 = returns_sorted[int(0.05 * n)]
        
        # Conditional Value at Risk (Expected Shortfall)
        cvar_95_idx = int(0.05 * n)
        cvar_95 = statistics.mean(returns_sorted[:cvar_95_idx + 1]) if cvar_95_idx >= 0 else returns_sorted[0]
        
        return {
            "status": "completed",
            "n_simulations": n,
            "baseline_return": baseline_return,
            "mean_return": statistics.mean(returns),
            "median_return": statistics.median(returns),
            "return_std": statistics.stdev(returns) if n > 1 else 0,
            "min_return": min(returns),
            "max_return": max(returns),
            "percentiles": percentiles,
            "probability_of_profit": prob_profit * 100,
            "value_at_risk_95": var_95,
            "conditional_var_95": cvar_95,
            "sharpe_stats": {
                "mean": statistics.mean(sharpes) if sharpes else 0,
                "std": statistics.stdev(sharpes) if len(sharpes) > 1 else 0,
            },
            "drawdown_stats": {
                "mean": statistics.mean(drawdowns) if drawdowns else 0,
                "max": max(drawdowns) if drawdowns else 0,
            },
            "return_distribution": self._create_histogram(returns, bins=50),
        }
    
    def _create_histogram(self, data: List[float], bins: int = 50) -> Dict[str, Any]:
        """
        Create histogram data for visualization
        """
        if not data:
            return {"edges": [], "counts": []}
        
        min_val = min(data)
        max_val = max(data)
        
        if min_val == max_val:
            return {"edges": [min_val, max_val], "counts": [len(data)]}
        
        bin_width = (max_val - min_val) / bins
        edges = [min_val + i * bin_width for i in range(bins + 1)]
        counts = [0] * bins
        
        for value in data:
            bin_idx = int((value - min_val) / bin_width)
            bin_idx = min(bin_idx, bins - 1)  # Handle edge case
            counts[bin_idx] += 1
        
        return {"edges": edges, "counts": counts}
