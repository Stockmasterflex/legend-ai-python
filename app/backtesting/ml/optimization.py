"""
Hyperparameter Optimization
Grid Search, Random Search, and Bayesian Optimization for ML models
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
import logging
from itertools import product
import random

import pandas as pd
import numpy as np

from .models import MLModel, ModelConfig, ModelType

logger = logging.getLogger(__name__)


class OptimizationType(str, Enum):
    """Optimization types"""
    GRID_SEARCH = "grid_search"
    RANDOM_SEARCH = "random_search"
    BAYESIAN = "bayesian"


@dataclass
class OptimizationConfig:
    """Hyperparameter optimization configuration"""
    model_type: ModelType
    parameter_space: Dict[str, List[Any]]  # {"n_estimators": [50, 100, 200], ...}
    optimization_type: OptimizationType = OptimizationType.GRID_SEARCH
    n_trials: int = 100  # For random/bayesian search
    objective_metric: str = "val_accuracy"  # What to optimize
    cv_folds: int = 5
    random_state: int = 42


class HyperparameterOptimizer:
    """
    Hyperparameter optimization engine
    Supports grid search, random search, and Bayesian optimization
    """

    def __init__(self, config: OptimizationConfig):
        """
        Initialize optimizer

        Args:
            config: Optimization configuration
        """
        self.config = config
        self.results: List[Dict[str, Any]] = []
        self.best_params: Optional[Dict[str, Any]] = None
        self.best_score: float = -np.inf

    async def optimize(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        on_trial_complete: Optional[Callable] = None,
    ) -> Dict[str, Any]:
        """
        Run hyperparameter optimization

        Args:
            X: Training features
            y: Training labels
            on_trial_complete: Callback after each trial

        Returns:
            Optimization results
        """
        logger.info(f"Starting {self.config.optimization_type} optimization")

        if self.config.optimization_type == OptimizationType.GRID_SEARCH:
            await self._grid_search(X, y, on_trial_complete)

        elif self.config.optimization_type == OptimizationType.RANDOM_SEARCH:
            await self._random_search(X, y, on_trial_complete)

        elif self.config.optimization_type == OptimizationType.BAYESIAN:
            await self._bayesian_optimization(X, y, on_trial_complete)

        else:
            raise ValueError(f"Unknown optimization type: {self.config.optimization_type}")

        logger.info(f"Optimization completed. Best score: {self.best_score:.4f}")
        logger.info(f"Best parameters: {self.best_params}")

        return {
            "best_params": self.best_params,
            "best_score": self.best_score,
            "all_trials": self.results,
            "n_trials": len(self.results),
        }

    async def _grid_search(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        on_trial_complete: Optional[Callable] = None,
    ):
        """Grid search optimization"""
        # Generate all parameter combinations
        param_names = list(self.config.parameter_space.keys())
        param_values = list(self.config.parameter_space.values())
        param_combinations = list(product(*param_values))

        n_combinations = len(param_combinations)
        logger.info(f"Grid search: testing {n_combinations} combinations")

        for i, param_combo in enumerate(param_combinations):
            # Create parameter dictionary
            params = dict(zip(param_names, param_combo))

            # Evaluate parameters
            score, metrics = await self._evaluate_parameters(X, y, params)

            # Store result
            result = {
                "trial_number": i + 1,
                "parameters": params,
                "score": score,
                "metrics": metrics,
            }
            self.results.append(result)

            # Update best
            if score > self.best_score:
                self.best_score = score
                self.best_params = params
                logger.info(f"New best score: {score:.4f} with params: {params}")

            # Callback
            if on_trial_complete:
                await on_trial_complete(result, i + 1, n_combinations)

            if (i + 1) % 10 == 0:
                logger.info(f"Completed {i + 1}/{n_combinations} combinations")

    async def _random_search(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        on_trial_complete: Optional[Callable] = None,
    ):
        """Random search optimization"""
        logger.info(f"Random search: testing {self.config.n_trials} random combinations")

        for trial in range(self.config.n_trials):
            # Generate random parameters
            params = {}
            for param_name, param_range in self.config.parameter_space.items():
                if isinstance(param_range, list):
                    params[param_name] = random.choice(param_range)
                elif isinstance(param_range, tuple) and len(param_range) == 2:
                    # Assume (min, max) range
                    if isinstance(param_range[0], int):
                        params[param_name] = random.randint(param_range[0], param_range[1])
                    else:
                        params[param_name] = random.uniform(param_range[0], param_range[1])

            # Evaluate parameters
            score, metrics = await self._evaluate_parameters(X, y, params)

            # Store result
            result = {
                "trial_number": trial + 1,
                "parameters": params,
                "score": score,
                "metrics": metrics,
            }
            self.results.append(result)

            # Update best
            if score > self.best_score:
                self.best_score = score
                self.best_params = params
                logger.info(f"New best score: {score:.4f} with params: {params}")

            # Callback
            if on_trial_complete:
                await on_trial_complete(result, trial + 1, self.config.n_trials)

            if (trial + 1) % 10 == 0:
                logger.info(f"Completed {trial + 1}/{self.config.n_trials} trials")

    async def _bayesian_optimization(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        on_trial_complete: Optional[Callable] = None,
    ):
        """
        Bayesian optimization using Optuna (if available)
        Falls back to random search if Optuna not installed
        """
        try:
            import optuna
            optuna.logging.set_verbosity(optuna.logging.WARNING)

            def objective(trial):
                # Sample parameters
                params = {}
                for param_name, param_range in self.config.parameter_space.items():
                    if isinstance(param_range, list):
                        # Categorical
                        params[param_name] = trial.suggest_categorical(param_name, param_range)
                    elif isinstance(param_range, tuple) and len(param_range) == 2:
                        # Numeric range
                        if isinstance(param_range[0], int):
                            params[param_name] = trial.suggest_int(param_name, param_range[0], param_range[1])
                        else:
                            params[param_name] = trial.suggest_float(param_name, param_range[0], param_range[1])

                # Evaluate
                import asyncio
                score, metrics = asyncio.run(self._evaluate_parameters(X, y, params))

                # Store result
                result = {
                    "trial_number": trial.number + 1,
                    "parameters": params,
                    "score": score,
                    "metrics": metrics,
                }
                self.results.append(result)

                if score > self.best_score:
                    self.best_score = score
                    self.best_params = params

                return score

            # Create study
            study = optuna.create_study(
                direction="maximize",
                sampler=optuna.samplers.TPESampler(seed=self.config.random_state),
            )

            # Optimize
            study.optimize(objective, n_trials=self.config.n_trials)

            logger.info(f"Bayesian optimization completed with {len(study.trials)} trials")

        except ImportError:
            logger.warning("Optuna not installed, falling back to random search")
            await self._random_search(X, y, on_trial_complete)

    async def _evaluate_parameters(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        params: Dict[str, Any],
    ) -> tuple:
        """
        Evaluate a set of hyperparameters

        Args:
            X: Features
            y: Labels
            params: Hyperparameters to test

        Returns:
            (score, metrics) tuple
        """
        # Create model config
        model_config = ModelConfig(
            model_type=self.config.model_type,
            hyperparameters=params,
            cv_folds=self.config.cv_folds,
            random_state=self.config.random_state,
        )

        # Train model
        model = MLModel(model_config)
        metrics = model.train(X, y)

        # Extract objective metric
        score = metrics.get(self.config.objective_metric, 0.0)

        return score, metrics

    def get_best_model(self, X: pd.DataFrame, y: pd.Series) -> MLModel:
        """
        Get model with best parameters

        Args:
            X: Features
            y: Labels

        Returns:
            Trained model with best parameters
        """
        if self.best_params is None:
            raise ValueError("No optimization results available")

        model_config = ModelConfig(
            model_type=self.config.model_type,
            hyperparameters=self.best_params,
            cv_folds=self.config.cv_folds,
            random_state=self.config.random_state,
        )

        model = MLModel(model_config)
        model.train(X, y)

        return model

    def get_optimization_history(self) -> pd.DataFrame:
        """Get optimization history as DataFrame"""
        if not self.results:
            return pd.DataFrame()

        history = []
        for result in self.results:
            row = {
                "trial_number": result["trial_number"],
                "score": result["score"],
                **result["parameters"],
            }
            history.append(row)

        return pd.DataFrame(history)

    def plot_optimization_history(self) -> Dict[str, Any]:
        """Get data for plotting optimization history"""
        df = self.get_optimization_history()

        if df.empty:
            return {}

        return {
            "trial_numbers": df["trial_number"].tolist(),
            "scores": df["score"].tolist(),
            "best_scores": df["score"].cummax().tolist(),
        }

    def get_parameter_importance(self) -> pd.DataFrame:
        """
        Analyze parameter importance
        Based on correlation between parameter values and scores
        """
        df = self.get_optimization_history()

        if df.empty:
            return pd.DataFrame()

        importance = []
        param_cols = [col for col in df.columns if col not in ["trial_number", "score"]]

        for param in param_cols:
            # For categorical parameters, calculate average score per category
            if df[param].dtype == "object" or df[param].nunique() < 10:
                importance_score = df.groupby(param)["score"].mean().std()
            else:
                # For numeric parameters, calculate correlation
                importance_score = abs(df[param].corr(df["score"]))

            importance.append({
                "parameter": param,
                "importance": importance_score,
            })

        importance_df = pd.DataFrame(importance)
        importance_df = importance_df.sort_values("importance", ascending=False)

        return importance_df
