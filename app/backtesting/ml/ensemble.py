"""
Ensemble Methods
Combining multiple models for improved performance
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum
import logging

import pandas as pd
import numpy as np
from sklearn.ensemble import VotingClassifier, VotingRegressor, StackingClassifier, StackingRegressor
from sklearn.linear_model import LogisticRegression, Ridge

from .models import MLModel

logger = logging.getLogger(__name__)


class EnsembleType(str, Enum):
    """Ensemble types"""
    VOTING = "voting"
    STACKING = "stacking"
    WEIGHTED = "weighted"
    BLENDING = "blending"


@dataclass
class EnsembleConfig:
    """Ensemble configuration"""
    ensemble_type: EnsembleType
    member_models: List[MLModel]
    weights: Optional[List[float]] = None  # For weighted voting
    meta_learner: Optional[str] = None  # For stacking
    voting_method: str = "soft"  # "soft" or "hard" for voting classifiers


class EnsembleModel:
    """
    Ensemble model combining multiple ML models
    """

    def __init__(self, config: EnsembleConfig):
        """
        Initialize ensemble model

        Args:
            config: Ensemble configuration
        """
        self.config = config
        self.ensemble = None
        self.is_trained = False
        self.member_predictions: Dict[str, np.ndarray] = {}

    def train(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """
        Train ensemble model

        Args:
            X: Features
            y: Labels

        Returns:
            Training metrics
        """
        logger.info(f"Training {self.config.ensemble_type} ensemble with {len(self.config.member_models)} models")

        if self.config.ensemble_type == EnsembleType.VOTING:
            metrics = self._train_voting(X, y)

        elif self.config.ensemble_type == EnsembleType.STACKING:
            metrics = self._train_stacking(X, y)

        elif self.config.ensemble_type == EnsembleType.WEIGHTED:
            metrics = self._train_weighted(X, y)

        elif self.config.ensemble_type == EnsembleType.BLENDING:
            metrics = self._train_blending(X, y)

        else:
            raise ValueError(f"Unknown ensemble type: {self.config.ensemble_type}")

        self.is_trained = True

        return metrics

    def _train_voting(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Train voting ensemble"""
        # Prepare estimators
        estimators = []
        for i, model in enumerate(self.config.member_models):
            if not model.is_trained:
                model.train(X, y)

            estimators.append((f"model_{i}", model.model))

        # Determine if classification or regression
        is_classifier = self.config.member_models[0]._is_classifier()

        # Create voting ensemble
        if is_classifier:
            self.ensemble = VotingClassifier(
                estimators=estimators,
                voting=self.config.voting_method,
                weights=self.config.weights,
            )
        else:
            self.ensemble = VotingRegressor(
                estimators=estimators,
                weights=self.config.weights,
            )

        # Train ensemble (already trained, but fit is needed for sklearn)
        # Note: This is a bit redundant, but required by sklearn's API
        X_array = X.values if hasattr(X, 'values') else X
        self.ensemble.fit(X_array, y)

        # Evaluate
        predictions = self.ensemble.predict(X_array)

        if is_classifier:
            from sklearn.metrics import accuracy_score, f1_score
            metrics = {
                "ensemble_accuracy": accuracy_score(y, predictions),
                "ensemble_f1": f1_score(y, predictions, average="binary"),
            }
        else:
            from sklearn.metrics import mean_squared_error, r2_score
            metrics = {
                "ensemble_rmse": np.sqrt(mean_squared_error(y, predictions)),
                "ensemble_r2": r2_score(y, predictions),
            }

        # Compare with individual models
        for i, model in enumerate(self.config.member_models):
            model_preds = model.predict(X)
            if is_classifier:
                from sklearn.metrics import accuracy_score
                metrics[f"model_{i}_accuracy"] = accuracy_score(y, model_preds)
            else:
                from sklearn.metrics import r2_score
                metrics[f"model_{i}_r2"] = r2_score(y, model_preds)

        return metrics

    def _train_stacking(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Train stacking ensemble"""
        # Prepare base estimators
        estimators = []
        for i, model in enumerate(self.config.member_models):
            if not model.is_trained:
                model.train(X, y)

            estimators.append((f"model_{i}", model.model))

        # Determine if classification or regression
        is_classifier = self.config.member_models[0]._is_classifier()

        # Meta-learner
        if self.config.meta_learner:
            if self.config.meta_learner == "logistic":
                final_estimator = LogisticRegression()
            elif self.config.meta_learner == "ridge":
                final_estimator = Ridge()
            else:
                # Use first model type as meta-learner
                final_estimator = None
        else:
            final_estimator = None

        # Create stacking ensemble
        if is_classifier:
            self.ensemble = StackingClassifier(
                estimators=estimators,
                final_estimator=final_estimator,
                cv=5,
            )
        else:
            self.ensemble = StackingRegressor(
                estimators=estimators,
                final_estimator=final_estimator,
                cv=5,
            )

        # Train
        X_array = X.values if hasattr(X, 'values') else X
        self.ensemble.fit(X_array, y)

        # Evaluate
        predictions = self.ensemble.predict(X_array)

        if is_classifier:
            from sklearn.metrics import accuracy_score, f1_score
            metrics = {
                "ensemble_accuracy": accuracy_score(y, predictions),
                "ensemble_f1": f1_score(y, predictions, average="binary"),
            }
        else:
            from sklearn.metrics import mean_squared_error, r2_score
            metrics = {
                "ensemble_rmse": np.sqrt(mean_squared_error(y, predictions)),
                "ensemble_r2": r2_score(y, predictions),
            }

        return metrics

    def _train_weighted(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Train weighted average ensemble (custom implementation)"""
        # Train all member models
        all_predictions = []

        for i, model in enumerate(self.config.member_models):
            if not model.is_trained:
                model.train(X, y)

            preds = model.predict(X)
            all_predictions.append(preds)
            self.member_predictions[f"model_{i}"] = preds

        # Convert to array
        predictions_array = np.array(all_predictions)  # Shape: (n_models, n_samples)

        # Apply weights
        if self.config.weights:
            weights = np.array(self.config.weights).reshape(-1, 1)
        else:
            # Equal weights
            weights = np.ones((len(self.config.member_models), 1)) / len(self.config.member_models)

        # Weighted average
        ensemble_predictions = np.sum(predictions_array * weights, axis=0)

        # For classification, round to nearest class
        is_classifier = self.config.member_models[0]._is_classifier()
        if is_classifier:
            ensemble_predictions = np.round(ensemble_predictions).astype(int)

        # Evaluate
        if is_classifier:
            from sklearn.metrics import accuracy_score, f1_score
            metrics = {
                "ensemble_accuracy": accuracy_score(y, ensemble_predictions),
                "ensemble_f1": f1_score(y, ensemble_predictions, average="binary"),
            }
        else:
            from sklearn.metrics import mean_squared_error, r2_score
            metrics = {
                "ensemble_rmse": np.sqrt(mean_squared_error(y, ensemble_predictions)),
                "ensemble_r2": r2_score(y, ensemble_predictions),
            }

        return metrics

    def _train_blending(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """
        Train blending ensemble
        Uses holdout set for meta-learner training
        """
        from sklearn.model_selection import train_test_split

        # Split data
        X_train, X_blend, y_train, y_blend = train_test_split(
            X, y,
            test_size=0.3,
            shuffle=False,
        )

        # Train base models on train set
        blend_features = []

        for i, model in enumerate(self.config.member_models):
            # Train on train set
            model.train(X_train, y_train)

            # Predict on blend set
            blend_preds = model.predict(X_blend)
            blend_features.append(blend_preds)

        # Create blend features
        blend_X = np.column_stack(blend_features)

        # Train meta-learner
        is_classifier = self.config.member_models[0]._is_classifier()

        if is_classifier:
            meta_learner = LogisticRegression()
        else:
            meta_learner = Ridge()

        meta_learner.fit(blend_X, y_blend)

        self.ensemble = meta_learner

        # Evaluate on blend set
        predictions = meta_learner.predict(blend_X)

        if is_classifier:
            from sklearn.metrics import accuracy_score, f1_score
            metrics = {
                "ensemble_accuracy": accuracy_score(y_blend, predictions),
                "ensemble_f1": f1_score(y_blend, predictions, average="binary"),
            }
        else:
            from sklearn.metrics import mean_squared_error, r2_score
            metrics = {
                "ensemble_rmse": np.sqrt(mean_squared_error(y_blend, predictions)),
                "ensemble_r2": r2_score(y_blend, predictions),
            }

        return metrics

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions with ensemble"""
        if not self.is_trained:
            raise ValueError("Ensemble not trained")

        if self.config.ensemble_type == EnsembleType.WEIGHTED:
            # Custom weighted prediction
            all_predictions = []

            for model in self.config.member_models:
                preds = model.predict(X)
                all_predictions.append(preds)

            predictions_array = np.array(all_predictions)

            if self.config.weights:
                weights = np.array(self.config.weights).reshape(-1, 1)
            else:
                weights = np.ones((len(self.config.member_models), 1)) / len(self.config.member_models)

            ensemble_predictions = np.sum(predictions_array * weights, axis=0)

            is_classifier = self.config.member_models[0]._is_classifier()
            if is_classifier:
                ensemble_predictions = np.round(ensemble_predictions).astype(int)

            return ensemble_predictions

        elif self.config.ensemble_type == EnsembleType.BLENDING:
            # Blending prediction
            blend_features = []

            for model in self.config.member_models:
                preds = model.predict(X)
                blend_features.append(preds)

            blend_X = np.column_stack(blend_features)
            return self.ensemble.predict(blend_X)

        else:
            # Voting or Stacking
            X_array = X.values if hasattr(X, 'values') else X
            return self.ensemble.predict(X_array)

    def get_diversity_metrics(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """
        Calculate ensemble diversity metrics
        Higher diversity often leads to better ensemble performance
        """
        # Get predictions from all models
        predictions = []

        for model in self.config.member_models:
            preds = model.predict(X)
            predictions.append(preds)

        predictions = np.array(predictions)  # Shape: (n_models, n_samples)

        # Calculate pairwise disagreement
        n_models = len(self.config.member_models)
        disagreements = []

        for i in range(n_models):
            for j in range(i + 1, n_models):
                disagreement = np.mean(predictions[i] != predictions[j])
                disagreements.append(disagreement)

        avg_disagreement = np.mean(disagreements) if disagreements else 0.0

        # Calculate correlation between predictions (for regression)
        is_classifier = self.config.member_models[0]._is_classifier()

        if not is_classifier:
            correlations = []
            for i in range(n_models):
                for j in range(i + 1, n_models):
                    corr = np.corrcoef(predictions[i], predictions[j])[0, 1]
                    correlations.append(corr)

            avg_correlation = np.mean(correlations) if correlations else 0.0
        else:
            avg_correlation = None

        return {
            "n_models": n_models,
            "avg_pairwise_disagreement": avg_disagreement,
            "avg_pairwise_correlation": avg_correlation,
            "diversity_score": avg_disagreement if is_classifier else (1 - avg_correlation) if avg_correlation else 0,
        }

    @staticmethod
    def find_optimal_weights(
        models: List[MLModel],
        X_val: pd.DataFrame,
        y_val: pd.Series,
        is_classifier: bool = True,
    ) -> List[float]:
        """
        Find optimal weights for weighted ensemble using validation set

        Args:
            models: List of trained models
            X_val: Validation features
            y_val: Validation labels
            is_classifier: Whether this is classification

        Returns:
            Optimal weights
        """
        from scipy.optimize import minimize

        # Get predictions from all models
        predictions = np.array([model.predict(X_val) for model in models])

        def objective(weights):
            """Objective function to minimize"""
            weights = weights / weights.sum()  # Normalize
            ensemble_pred = np.sum(predictions * weights.reshape(-1, 1), axis=0)

            if is_classifier:
                ensemble_pred = np.round(ensemble_pred).astype(int)
                from sklearn.metrics import accuracy_score
                return -accuracy_score(y_val, ensemble_pred)  # Negative because we minimize
            else:
                from sklearn.metrics import mean_squared_error
                return mean_squared_error(y_val, ensemble_pred)

        # Initial weights (equal)
        n_models = len(models)
        initial_weights = np.ones(n_models) / n_models

        # Constraints: weights sum to 1, all positive
        constraints = {"type": "eq", "fun": lambda w: w.sum() - 1}
        bounds = [(0, 1) for _ in range(n_models)]

        # Optimize
        result = minimize(
            objective,
            initial_weights,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )

        optimal_weights = result.x / result.x.sum()  # Normalize

        logger.info(f"Found optimal weights: {optimal_weights}")

        return optimal_weights.tolist()
