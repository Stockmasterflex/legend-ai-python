"""
Model Selection Module

Provides tools for selecting ML algorithms, ensemble methods, and hyperparameter tuning.
"""

from typing import Dict, List, Optional, Any, Callable
import pandas as pd
import numpy as np
from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
    GradientBoostingClassifier,
    GradientBoostingRegressor,
    VotingClassifier,
    VotingRegressor,
    StackingClassifier,
    StackingRegressor,
    AdaBoostClassifier,
    AdaBoostRegressor,
)
from sklearn.linear_model import LogisticRegression, Ridge, Lasso, ElasticNet
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, cross_val_score
import xgboost as xgb
import lightgbm as lgb
import optuna
from optuna.samplers import TPESampler
import logging

logger = logging.getLogger(__name__)


class ModelSelector:
    """Comprehensive model selection and hyperparameter tuning toolkit"""

    def __init__(self, task_type: str = "classification", random_state: int = 42):
        """
        Initialize ModelSelector

        Args:
            task_type: 'classification' or 'regression'
            random_state: Random seed for reproducibility
        """
        self.task_type = task_type
        self.random_state = random_state
        self.models: Dict[str, Any] = {}
        self.best_model: Optional[Any] = None
        self.best_params: Optional[Dict] = None
        self.best_score: Optional[float] = None
        self._setup_default_models()

    def _setup_default_models(self):
        """Setup default models for classification and regression"""
        if self.task_type == "classification":
            self.models = {
                "random_forest": RandomForestClassifier(random_state=self.random_state),
                "xgboost": xgb.XGBClassifier(random_state=self.random_state, eval_metric='logloss'),
                "lightgbm": lgb.LGBMClassifier(random_state=self.random_state, verbose=-1),
                "logistic": LogisticRegression(random_state=self.random_state, max_iter=1000),
                "svm": SVC(random_state=self.random_state),
                "decision_tree": DecisionTreeClassifier(random_state=self.random_state),
                "knn": KNeighborsClassifier(),
                "naive_bayes": GaussianNB(),
                "gradient_boosting": GradientBoostingClassifier(random_state=self.random_state),
                "adaboost": AdaBoostClassifier(random_state=self.random_state),
            }
        else:  # regression
            self.models = {
                "random_forest": RandomForestRegressor(random_state=self.random_state),
                "xgboost": xgb.XGBRegressor(random_state=self.random_state),
                "lightgbm": lgb.LGBMRegressor(random_state=self.random_state, verbose=-1),
                "ridge": Ridge(random_state=self.random_state),
                "lasso": Lasso(random_state=self.random_state),
                "elasticnet": ElasticNet(random_state=self.random_state),
                "svm": SVR(),
                "decision_tree": DecisionTreeRegressor(random_state=self.random_state),
                "knn": KNeighborsRegressor(),
                "gradient_boosting": GradientBoostingRegressor(random_state=self.random_state),
                "adaboost": AdaBoostRegressor(random_state=self.random_state),
            }

    def get_default_param_grids(self) -> Dict[str, Dict]:
        """Get default hyperparameter grids for each algorithm"""
        if self.task_type == "classification":
            return {
                "random_forest": {
                    "n_estimators": [100, 200, 300],
                    "max_depth": [10, 20, 30, None],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4],
                    "max_features": ["sqrt", "log2"],
                },
                "xgboost": {
                    "n_estimators": [100, 200, 300],
                    "max_depth": [3, 5, 7, 9],
                    "learning_rate": [0.01, 0.05, 0.1, 0.2],
                    "subsample": [0.6, 0.8, 1.0],
                    "colsample_bytree": [0.6, 0.8, 1.0],
                },
                "lightgbm": {
                    "n_estimators": [100, 200, 300],
                    "max_depth": [3, 5, 7, 9],
                    "learning_rate": [0.01, 0.05, 0.1, 0.2],
                    "num_leaves": [31, 50, 70, 100],
                    "subsample": [0.6, 0.8, 1.0],
                },
                "logistic": {
                    "C": [0.001, 0.01, 0.1, 1, 10, 100],
                    "penalty": ["l1", "l2"],
                    "solver": ["liblinear", "saga"],
                },
                "svm": {
                    "C": [0.1, 1, 10, 100],
                    "kernel": ["linear", "rbf", "poly"],
                    "gamma": ["scale", "auto"],
                },
            }
        else:  # regression
            return {
                "random_forest": {
                    "n_estimators": [100, 200, 300],
                    "max_depth": [10, 20, 30, None],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4],
                },
                "xgboost": {
                    "n_estimators": [100, 200, 300],
                    "max_depth": [3, 5, 7, 9],
                    "learning_rate": [0.01, 0.05, 0.1, 0.2],
                    "subsample": [0.6, 0.8, 1.0],
                },
                "lightgbm": {
                    "n_estimators": [100, 200, 300],
                    "max_depth": [3, 5, 7, 9],
                    "learning_rate": [0.01, 0.05, 0.1, 0.2],
                    "num_leaves": [31, 50, 70, 100],
                },
                "ridge": {
                    "alpha": [0.001, 0.01, 0.1, 1, 10, 100],
                },
                "lasso": {
                    "alpha": [0.001, 0.01, 0.1, 1, 10, 100],
                },
                "elasticnet": {
                    "alpha": [0.001, 0.01, 0.1, 1, 10],
                    "l1_ratio": [0.1, 0.3, 0.5, 0.7, 0.9],
                },
            }

    def compare_models(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        models: Optional[List[str]] = None,
        cv: int = 5,
        scoring: Optional[str] = None,
    ) -> pd.DataFrame:
        """
        Compare multiple models using cross-validation

        Args:
            X_train: Training features
            y_train: Training target
            models: List of model names to compare (if None, use all)
            cv: Number of cross-validation folds
            scoring: Scoring metric (if None, uses default for task type)

        Returns:
            DataFrame with model comparison results
        """
        if models is None:
            models = list(self.models.keys())

        if scoring is None:
            scoring = "accuracy" if self.task_type == "classification" else "r2"

        results = []

        for model_name in models:
            if model_name not in self.models:
                logger.warning(f"Model '{model_name}' not found, skipping")
                continue

            logger.info(f"Evaluating {model_name}...")
            model = self.models[model_name]

            try:
                scores = cross_val_score(model, X_train, y_train, cv=cv, scoring=scoring)
                results.append({
                    "model": model_name,
                    "mean_score": scores.mean(),
                    "std_score": scores.std(),
                    "min_score": scores.min(),
                    "max_score": scores.max(),
                })
            except Exception as e:
                logger.error(f"Error evaluating {model_name}: {e}")
                continue

        comparison_df = pd.DataFrame(results).sort_values("mean_score", ascending=False)
        logger.info(f"\nModel Comparison:\n{comparison_df.to_string()}")

        return comparison_df

    def grid_search(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        model_name: str,
        param_grid: Optional[Dict] = None,
        cv: int = 5,
        scoring: Optional[str] = None,
        n_jobs: int = -1,
    ) -> Dict:
        """
        Perform grid search for hyperparameter tuning

        Args:
            X_train: Training features
            y_train: Training target
            model_name: Name of the model to tune
            param_grid: Parameter grid (if None, uses default)
            cv: Number of cross-validation folds
            scoring: Scoring metric
            n_jobs: Number of parallel jobs

        Returns:
            Dictionary with best parameters and score
        """
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found")

        model = self.models[model_name]

        if param_grid is None:
            default_grids = self.get_default_param_grids()
            param_grid = default_grids.get(model_name, {})

        if scoring is None:
            scoring = "accuracy" if self.task_type == "classification" else "r2"

        logger.info(f"Starting grid search for {model_name}...")

        grid_search = GridSearchCV(
            model,
            param_grid,
            cv=cv,
            scoring=scoring,
            n_jobs=n_jobs,
            verbose=1,
        )

        grid_search.fit(X_train, y_train)

        self.best_model = grid_search.best_estimator_
        self.best_params = grid_search.best_params_
        self.best_score = grid_search.best_score_

        logger.info(f"Best parameters: {self.best_params}")
        logger.info(f"Best score: {self.best_score:.4f}")

        return {
            "best_params": self.best_params,
            "best_score": self.best_score,
            "cv_results": pd.DataFrame(grid_search.cv_results_),
        }

    def random_search(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        model_name: str,
        param_distributions: Optional[Dict] = None,
        n_iter: int = 50,
        cv: int = 5,
        scoring: Optional[str] = None,
        n_jobs: int = -1,
    ) -> Dict:
        """
        Perform randomized search for hyperparameter tuning

        Args:
            X_train: Training features
            y_train: Training target
            model_name: Name of the model to tune
            param_distributions: Parameter distributions
            n_iter: Number of parameter settings sampled
            cv: Number of cross-validation folds
            scoring: Scoring metric
            n_jobs: Number of parallel jobs

        Returns:
            Dictionary with best parameters and score
        """
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found")

        model = self.models[model_name]

        if param_distributions is None:
            param_distributions = self.get_default_param_grids().get(model_name, {})

        if scoring is None:
            scoring = "accuracy" if self.task_type == "classification" else "r2"

        logger.info(f"Starting randomized search for {model_name}...")

        random_search = RandomizedSearchCV(
            model,
            param_distributions,
            n_iter=n_iter,
            cv=cv,
            scoring=scoring,
            n_jobs=n_jobs,
            random_state=self.random_state,
            verbose=1,
        )

        random_search.fit(X_train, y_train)

        self.best_model = random_search.best_estimator_
        self.best_params = random_search.best_params_
        self.best_score = random_search.best_score_

        logger.info(f"Best parameters: {self.best_params}")
        logger.info(f"Best score: {self.best_score:.4f}")

        return {
            "best_params": self.best_params,
            "best_score": self.best_score,
            "cv_results": pd.DataFrame(random_search.cv_results_),
        }

    def optuna_search(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        model_name: str,
        n_trials: int = 100,
        cv: int = 5,
        scoring: Optional[str] = None,
    ) -> Dict:
        """
        Perform Optuna-based hyperparameter optimization

        Args:
            X_train: Training features
            y_train: Training target
            model_name: Name of the model to tune
            n_trials: Number of optimization trials
            cv: Number of cross-validation folds
            scoring: Scoring metric

        Returns:
            Dictionary with best parameters and score
        """
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found")

        if scoring is None:
            scoring = "accuracy" if self.task_type == "classification" else "r2"

        def objective(trial):
            """Objective function for Optuna"""
            params = self._get_optuna_params(trial, model_name)

            if self.task_type == "classification":
                if model_name == "random_forest":
                    model = RandomForestClassifier(**params, random_state=self.random_state)
                elif model_name == "xgboost":
                    model = xgb.XGBClassifier(**params, random_state=self.random_state, eval_metric='logloss')
                elif model_name == "lightgbm":
                    model = lgb.LGBMClassifier(**params, random_state=self.random_state, verbose=-1)
                else:
                    raise ValueError(f"Optuna search not implemented for {model_name}")
            else:
                if model_name == "random_forest":
                    model = RandomForestRegressor(**params, random_state=self.random_state)
                elif model_name == "xgboost":
                    model = xgb.XGBRegressor(**params, random_state=self.random_state)
                elif model_name == "lightgbm":
                    model = lgb.LGBMRegressor(**params, random_state=self.random_state, verbose=-1)
                else:
                    raise ValueError(f"Optuna search not implemented for {model_name}")

            scores = cross_val_score(model, X_train, y_train, cv=cv, scoring=scoring)
            return scores.mean()

        logger.info(f"Starting Optuna optimization for {model_name}...")

        study = optuna.create_study(
            direction="maximize",
            sampler=TPESampler(seed=self.random_state),
        )
        study.optimize(objective, n_trials=n_trials, show_progress_bar=True)

        self.best_params = study.best_params
        self.best_score = study.best_value

        # Train final model with best params
        if self.task_type == "classification":
            if model_name == "random_forest":
                self.best_model = RandomForestClassifier(**self.best_params, random_state=self.random_state)
            elif model_name == "xgboost":
                self.best_model = xgb.XGBClassifier(**self.best_params, random_state=self.random_state, eval_metric='logloss')
            elif model_name == "lightgbm":
                self.best_model = lgb.LGBMClassifier(**self.best_params, random_state=self.random_state, verbose=-1)
        else:
            if model_name == "random_forest":
                self.best_model = RandomForestRegressor(**self.best_params, random_state=self.random_state)
            elif model_name == "xgboost":
                self.best_model = xgb.XGBRegressor(**self.best_params, random_state=self.random_state)
            elif model_name == "lightgbm":
                self.best_model = lgb.LGBMRegressor(**self.best_params, random_state=self.random_state, verbose=-1)

        self.best_model.fit(X_train, y_train)

        logger.info(f"Best parameters: {self.best_params}")
        logger.info(f"Best score: {self.best_score:.4f}")

        return {
            "best_params": self.best_params,
            "best_score": self.best_score,
            "study": study,
        }

    def _get_optuna_params(self, trial, model_name: str) -> Dict:
        """Get hyperparameter suggestions for Optuna trial"""
        if model_name == "random_forest":
            return {
                "n_estimators": trial.suggest_int("n_estimators", 100, 500),
                "max_depth": trial.suggest_int("max_depth", 5, 50),
                "min_samples_split": trial.suggest_int("min_samples_split", 2, 20),
                "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 10),
                "max_features": trial.suggest_categorical("max_features", ["sqrt", "log2"]),
            }
        elif model_name == "xgboost":
            return {
                "n_estimators": trial.suggest_int("n_estimators", 100, 500),
                "max_depth": trial.suggest_int("max_depth", 3, 12),
                "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
                "subsample": trial.suggest_float("subsample", 0.5, 1.0),
                "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
                "gamma": trial.suggest_float("gamma", 0.0, 5.0),
                "reg_alpha": trial.suggest_float("reg_alpha", 0.0, 1.0),
                "reg_lambda": trial.suggest_float("reg_lambda", 0.0, 1.0),
            }
        elif model_name == "lightgbm":
            return {
                "n_estimators": trial.suggest_int("n_estimators", 100, 500),
                "max_depth": trial.suggest_int("max_depth", 3, 12),
                "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
                "num_leaves": trial.suggest_int("num_leaves", 20, 150),
                "subsample": trial.suggest_float("subsample", 0.5, 1.0),
                "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
                "reg_alpha": trial.suggest_float("reg_alpha", 0.0, 1.0),
                "reg_lambda": trial.suggest_float("reg_lambda", 0.0, 1.0),
            }
        else:
            return {}

    def create_voting_ensemble(
        self,
        models: List[str],
        voting: str = "soft",
        weights: Optional[List[float]] = None,
    ) -> Any:
        """
        Create a voting ensemble from multiple models

        Args:
            models: List of model names to ensemble
            voting: 'soft' or 'hard' voting (classification only)
            weights: Optional weights for each model

        Returns:
            Voting ensemble model
        """
        estimators = [(name, self.models[name]) for name in models if name in self.models]

        if self.task_type == "classification":
            ensemble = VotingClassifier(estimators=estimators, voting=voting, weights=weights)
        else:
            ensemble = VotingRegressor(estimators=estimators, weights=weights)

        logger.info(f"Created voting ensemble with models: {models}")
        return ensemble

    def create_stacking_ensemble(
        self,
        base_models: List[str],
        meta_model: Optional[str] = None,
        cv: int = 5,
    ) -> Any:
        """
        Create a stacking ensemble

        Args:
            base_models: List of base model names
            meta_model: Meta-model name (if None, uses logistic/ridge)
            cv: Number of cross-validation folds

        Returns:
            Stacking ensemble model
        """
        estimators = [(name, self.models[name]) for name in base_models if name in self.models]

        if meta_model:
            final_estimator = self.models.get(meta_model)
        else:
            final_estimator = None  # Uses default

        if self.task_type == "classification":
            ensemble = StackingClassifier(
                estimators=estimators,
                final_estimator=final_estimator,
                cv=cv,
            )
        else:
            ensemble = StackingRegressor(
                estimators=estimators,
                final_estimator=final_estimator,
                cv=cv,
            )

        logger.info(f"Created stacking ensemble with base models: {base_models}")
        return ensemble
