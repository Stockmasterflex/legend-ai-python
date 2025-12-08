"""
Hyperparameter Optimization Module
Implements various optimization strategies for ML models and trading parameters
"""

import itertools
import logging
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class OptimizationType(str, Enum):
    """Types of optimization strategies"""

    GRID = "grid"
    RANDOM = "random"
    BAYESIAN = "bayesian"
    GENETIC = "genetic"


@dataclass
class OptimizationConfig:
    """Configuration for hyperparameter optimization"""

    optimization_type: OptimizationType = OptimizationType.GRID
    parameter_space: Dict[str, List[Any]] = field(default_factory=dict)
    n_trials: int = 100
    objective_metric: str = "val_accuracy"
    maximize: bool = True
    early_stopping_rounds: int = 10
    cv_folds: int = 5
    random_seed: Optional[int] = None
    parallel_trials: int = 1


@dataclass
class TrialResult:
    """Result from a single optimization trial"""

    trial_id: int
    params: Dict[str, Any]
    objective_value: float
    metrics: Dict[str, float]
    duration_seconds: float
    status: str  # completed, failed, pruned


class HyperparameterOptimizer:
    """
    Hyperparameter Optimization Engine

    Supports multiple optimization strategies:
    1. Grid Search - Exhaustive search over parameter grid
    2. Random Search - Random sampling from parameter space
    3. Bayesian Optimization - Sequential model-based optimization
    4. Genetic Algorithm - Evolution-based optimization
    """

    def __init__(self, config: OptimizationConfig):
        self.config = config
        self.trials: List[TrialResult] = []
        self.best_params: Optional[Dict[str, Any]] = None
        self.best_score: Optional[float] = None
        self.is_running = False
        self.progress = 0.0

        if config.random_seed is not None:
            random.seed(config.random_seed)

    async def optimize(
        self,
        objective_fn: Callable[[Dict[str, Any]], float],
        progress_callback: Optional[Callable[[float], None]] = None,
    ) -> Dict[str, Any]:
        """
        Run hyperparameter optimization

        Args:
            objective_fn: Function that takes params dict and returns objective value
            progress_callback: Optional callback for progress updates

        Returns:
            Dictionary with best parameters and optimization history
        """
        self.is_running = True
        self.trials = []
        self.best_params = None
        self.best_score = None

        logger.info(f"Starting {self.config.optimization_type.value} optimization")

        if self.config.optimization_type == OptimizationType.GRID:
            result = await self._grid_search(objective_fn, progress_callback)
        elif self.config.optimization_type == OptimizationType.RANDOM:
            result = await self._random_search(objective_fn, progress_callback)
        elif self.config.optimization_type == OptimizationType.BAYESIAN:
            result = await self._bayesian_search(objective_fn, progress_callback)
        elif self.config.optimization_type == OptimizationType.GENETIC:
            result = await self._genetic_search(objective_fn, progress_callback)
        else:
            raise ValueError(
                f"Unknown optimization type: {self.config.optimization_type}"
            )

        self.is_running = False
        return result

    async def _grid_search(
        self,
        objective_fn: Callable,
        progress_callback: Optional[Callable] = None,
    ) -> Dict[str, Any]:
        """
        Exhaustive grid search over all parameter combinations
        """
        param_names = list(self.config.parameter_space.keys())
        param_values = list(self.config.parameter_space.values())

        all_combinations = list(itertools.product(*param_values))
        n_combinations = len(all_combinations)

        logger.info(f"Grid search with {n_combinations} parameter combinations")

        for i, combination in enumerate(all_combinations):
            params = dict(zip(param_names, combination))

            try:
                score = objective_fn(params)

                trial = TrialResult(
                    trial_id=i,
                    params=params,
                    objective_value=score,
                    metrics={self.config.objective_metric: score},
                    duration_seconds=0,  # Track in production
                    status="completed",
                )
                self.trials.append(trial)

                # Update best
                if self.best_score is None or self._is_better(score, self.best_score):
                    self.best_score = score
                    self.best_params = params

            except Exception as e:
                logger.error(f"Trial {i} failed: {e}")
                self.trials.append(
                    TrialResult(
                        trial_id=i,
                        params=params,
                        objective_value=0,
                        metrics={},
                        duration_seconds=0,
                        status="failed",
                    )
                )

            self.progress = (i + 1) / n_combinations * 100
            if progress_callback:
                progress_callback(self.progress)

        return self._compile_results()

    async def _random_search(
        self,
        objective_fn: Callable,
        progress_callback: Optional[Callable] = None,
    ) -> Dict[str, Any]:
        """
        Random sampling from parameter space
        """
        logger.info(f"Random search with {self.config.n_trials} trials")

        for i in range(self.config.n_trials):
            # Sample random parameters
            params = {
                name: random.choice(values)
                for name, values in self.config.parameter_space.items()
            }

            try:
                score = objective_fn(params)

                trial = TrialResult(
                    trial_id=i,
                    params=params,
                    objective_value=score,
                    metrics={self.config.objective_metric: score},
                    duration_seconds=0,
                    status="completed",
                )
                self.trials.append(trial)

                if self.best_score is None or self._is_better(score, self.best_score):
                    self.best_score = score
                    self.best_params = params

            except Exception as e:
                logger.error(f"Trial {i} failed: {e}")
                self.trials.append(
                    TrialResult(
                        trial_id=i,
                        params=params,
                        objective_value=0,
                        metrics={},
                        duration_seconds=0,
                        status="failed",
                    )
                )

            self.progress = (i + 1) / self.config.n_trials * 100
            if progress_callback:
                progress_callback(self.progress)

        return self._compile_results()

    async def _bayesian_search(
        self,
        objective_fn: Callable,
        progress_callback: Optional[Callable] = None,
    ) -> Dict[str, Any]:
        """
        Bayesian optimization using surrogate model

        Note: This is a simplified implementation.
        In production, use libraries like Optuna or scikit-optimize.
        """
        logger.info(f"Bayesian search with {self.config.n_trials} trials")

        # Start with random exploration
        exploration_ratio = 0.3
        n_exploration = int(self.config.n_trials * exploration_ratio)

        for i in range(self.config.n_trials):
            if i < n_exploration:
                # Exploration phase: random sampling
                params = {
                    name: random.choice(values)
                    for name, values in self.config.parameter_space.items()
                }
            else:
                # Exploitation phase: sample near best known
                if self.best_params:
                    params = self._sample_near_best()
                else:
                    params = {
                        name: random.choice(values)
                        for name, values in self.config.parameter_space.items()
                    }

            try:
                score = objective_fn(params)

                trial = TrialResult(
                    trial_id=i,
                    params=params,
                    objective_value=score,
                    metrics={self.config.objective_metric: score},
                    duration_seconds=0,
                    status="completed",
                )
                self.trials.append(trial)

                if self.best_score is None or self._is_better(score, self.best_score):
                    self.best_score = score
                    self.best_params = params

            except Exception as e:
                logger.error(f"Trial {i} failed: {e}")

            self.progress = (i + 1) / self.config.n_trials * 100
            if progress_callback:
                progress_callback(self.progress)

        return self._compile_results()

    async def _genetic_search(
        self,
        objective_fn: Callable,
        progress_callback: Optional[Callable] = None,
    ) -> Dict[str, Any]:
        """
        Genetic algorithm optimization
        """
        population_size = min(50, self.config.n_trials // 5)
        n_generations = self.config.n_trials // population_size

        logger.info(
            f"Genetic search: {population_size} population, {n_generations} generations"
        )

        # Initialize population
        population = [
            {
                name: random.choice(values)
                for name, values in self.config.parameter_space.items()
            }
            for _ in range(population_size)
        ]

        trial_id = 0

        for gen in range(n_generations):
            # Evaluate population
            scores = []
            for params in population:
                try:
                    score = objective_fn(params)
                    scores.append((params, score))

                    self.trials.append(
                        TrialResult(
                            trial_id=trial_id,
                            params=params,
                            objective_value=score,
                            metrics={self.config.objective_metric: score},
                            duration_seconds=0,
                            status="completed",
                        )
                    )
                    trial_id += 1

                    if self.best_score is None or self._is_better(
                        score, self.best_score
                    ):
                        self.best_score = score
                        self.best_params = params

                except Exception as e:
                    logger.error(f"Evaluation failed: {e}")
                    scores.append(
                        (
                            params,
                            float("-inf") if self.config.maximize else float("inf"),
                        )
                    )

            # Selection: keep top 50%
            scores.sort(key=lambda x: x[1], reverse=self.config.maximize)
            survivors = [s[0] for s in scores[: population_size // 2]]

            # Crossover and mutation to create new population
            population = survivors.copy()
            while len(population) < population_size:
                parent1, parent2 = random.sample(survivors, 2)
                child = self._crossover(parent1, parent2)
                child = self._mutate(child)
                population.append(child)

            self.progress = (gen + 1) / n_generations * 100
            if progress_callback:
                progress_callback(self.progress)

        return self._compile_results()

    def _is_better(self, score: float, best: float) -> bool:
        """Check if score is better than best based on maximize setting"""
        if self.config.maximize:
            return score > best
        return score < best

    def _sample_near_best(self) -> Dict[str, Any]:
        """Sample parameters near the current best"""
        params = {}
        for name, values in self.config.parameter_space.items():
            if name in self.best_params:
                best_val = self.best_params[name]
                if best_val in values:
                    idx = values.index(best_val)
                    # Sample within 2 positions of best
                    min_idx = max(0, idx - 2)
                    max_idx = min(len(values) - 1, idx + 2)
                    params[name] = values[random.randint(min_idx, max_idx)]
                else:
                    params[name] = random.choice(values)
            else:
                params[name] = random.choice(values)
        return params

    def _crossover(self, parent1: Dict, parent2: Dict) -> Dict:
        """Crossover two parameter sets"""
        child = {}
        for name in self.config.parameter_space.keys():
            child[name] = random.choice([parent1.get(name), parent2.get(name)])
        return child

    def _mutate(self, params: Dict, mutation_rate: float = 0.1) -> Dict:
        """Mutate parameters with given probability"""
        mutated = params.copy()
        for name, values in self.config.parameter_space.items():
            if random.random() < mutation_rate:
                mutated[name] = random.choice(values)
        return mutated

    def _compile_results(self) -> Dict[str, Any]:
        """Compile optimization results"""
        completed_trials = [t for t in self.trials if t.status == "completed"]

        return {
            "status": "completed",
            "optimization_type": self.config.optimization_type.value,
            "n_trials": len(self.trials),
            "n_completed": len(completed_trials),
            "best_params": self.best_params,
            "best_score": self.best_score,
            "all_results": [
                {
                    "trial_id": t.trial_id,
                    "params": t.params,
                    "objective_value": t.objective_value,
                    "status": t.status,
                }
                for t in self.trials
            ],
            "parameter_importance": self._calculate_parameter_importance(
                completed_trials
            ),
        }

    def _calculate_parameter_importance(
        self,
        trials: List[TrialResult],
    ) -> Dict[str, float]:
        """
        Calculate parameter importance based on variance contribution

        Simplified implementation using correlation-based importance
        """
        if len(trials) < 10:
            return {}

        importance = {}

        for param_name, param_values in self.config.parameter_space.items():
            if len(param_values) <= 1:
                importance[param_name] = 0
                continue

            # Group scores by parameter value
            value_scores: Dict[Any, List[float]] = {}
            for trial in trials:
                val = trial.params.get(param_name)
                if val not in value_scores:
                    value_scores[val] = []
                value_scores[val].append(trial.objective_value)

            # Calculate variance between groups vs within groups
            if len(value_scores) > 1:
                group_means = [
                    sum(scores) / len(scores)
                    for scores in value_scores.values()
                    if scores
                ]
                if group_means:
                    global_mean = sum(group_means) / len(group_means)
                    between_var = sum(
                        (m - global_mean) ** 2 for m in group_means
                    ) / len(group_means)
                    importance[param_name] = between_var
                else:
                    importance[param_name] = 0
            else:
                importance[param_name] = 0

        # Normalize to 0-100
        max_importance = max(importance.values()) if importance else 1
        if max_importance > 0:
            importance = {k: (v / max_importance) * 100 for k, v in importance.items()}

        return importance
