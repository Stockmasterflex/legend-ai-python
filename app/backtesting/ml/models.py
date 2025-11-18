"""
ML Model Training and Management
Comprehensive model training framework for trading strategies
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import logging
import pickle
import json
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, TimeSeriesSplit
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

logger = logging.getLogger(__name__)


class ModelType(str, Enum):
    """ML model types"""
    RANDOM_FOREST_CLASSIFIER = "random_forest_classifier"
    RANDOM_FOREST_REGRESSOR = "random_forest_regressor"
    GRADIENT_BOOSTING_CLASSIFIER = "gradient_boosting_classifier"
    XGBOOST_CLASSIFIER = "xgboost_classifier"
    LIGHTGBM_CLASSIFIER = "lightgbm_classifier"
    NEURAL_NETWORK = "neural_network"


@dataclass
class ModelConfig:
    """ML model configuration"""
    model_type: ModelType
    hyperparameters: Dict[str, Any] = None
    scaler_type: str = "standard"  # "standard", "robust", "none"
    test_size: float = 0.2
    validation_size: float = 0.2
    cv_folds: int = 5
    random_state: int = 42


class MLModel:
    """
    Machine learning model wrapper
    Handles training, evaluation, and prediction
    """

    def __init__(self, config: ModelConfig):
        """
        Initialize ML model

        Args:
            config: Model configuration
        """
        self.config = config
        self.model = None
        self.scaler = None
        self.feature_names: List[str] = []
        self.metrics: Dict[str, float] = {}
        self.is_trained = False

        self._initialize_model()
        self._initialize_scaler()

    def _initialize_model(self):
        """Initialize the ML model"""
        hyperparams = self.config.hyperparameters or {}

        if self.config.model_type == ModelType.RANDOM_FOREST_CLASSIFIER:
            self.model = RandomForestClassifier(
                n_estimators=hyperparams.get("n_estimators", 100),
                max_depth=hyperparams.get("max_depth", None),
                min_samples_split=hyperparams.get("min_samples_split", 2),
                min_samples_leaf=hyperparams.get("min_samples_leaf", 1),
                random_state=self.config.random_state,
                n_jobs=-1,
            )

        elif self.config.model_type == ModelType.RANDOM_FOREST_REGRESSOR:
            self.model = RandomForestRegressor(
                n_estimators=hyperparams.get("n_estimators", 100),
                max_depth=hyperparams.get("max_depth", None),
                min_samples_split=hyperparams.get("min_samples_split", 2),
                min_samples_leaf=hyperparams.get("min_samples_leaf", 1),
                random_state=self.config.random_state,
                n_jobs=-1,
            )

        elif self.config.model_type == ModelType.GRADIENT_BOOSTING_CLASSIFIER:
            self.model = GradientBoostingClassifier(
                n_estimators=hyperparams.get("n_estimators", 100),
                learning_rate=hyperparams.get("learning_rate", 0.1),
                max_depth=hyperparams.get("max_depth", 3),
                random_state=self.config.random_state,
            )

        else:
            raise ValueError(f"Model type {self.config.model_type} not yet implemented")

    def _initialize_scaler(self):
        """Initialize feature scaler"""
        if self.config.scaler_type == "standard":
            self.scaler = StandardScaler()
        elif self.config.scaler_type == "robust":
            self.scaler = RobustScaler()
        elif self.config.scaler_type == "none":
            self.scaler = None
        else:
            raise ValueError(f"Unknown scaler type: {self.config.scaler_type}")

    def train(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        feature_names: Optional[List[str]] = None,
    ) -> Dict[str, float]:
        """
        Train the model

        Args:
            X: Features
            y: Labels
            feature_names: List of feature names

        Returns:
            Training metrics
        """
        logger.info(f"Training {self.config.model_type} model...")

        self.feature_names = feature_names or list(X.columns)

        # Split data
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y,
            test_size=self.config.test_size,
            random_state=self.config.random_state,
            shuffle=False,  # Preserve time order
        )

        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp,
            test_size=self.config.validation_size / (1 - self.config.test_size),
            random_state=self.config.random_state,
            shuffle=False,
        )

        logger.info(f"Train size: {len(X_train)}, Val size: {len(X_val)}, Test size: {len(X_test)}")

        # Scale features
        if self.scaler:
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_val_scaled = self.scaler.transform(X_val)
            X_test_scaled = self.scaler.transform(X_test)
        else:
            X_train_scaled = X_train.values
            X_val_scaled = X_val.values
            X_test_scaled = X_test.values

        # Train model
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True

        # Evaluate
        y_train_pred = self.model.predict(X_train_scaled)
        y_val_pred = self.model.predict(X_val_scaled)
        y_test_pred = self.model.predict(X_test_scaled)

        # Calculate metrics
        if self._is_classifier():
            self.metrics = {
                "train_accuracy": accuracy_score(y_train, y_train_pred),
                "val_accuracy": accuracy_score(y_val, y_val_pred),
                "test_accuracy": accuracy_score(y_test, y_test_pred),
                "train_precision": precision_score(y_train, y_train_pred, average="binary"),
                "val_precision": precision_score(y_val, y_val_pred, average="binary"),
                "test_precision": precision_score(y_test, y_test_pred, average="binary"),
                "train_recall": recall_score(y_train, y_train_pred, average="binary"),
                "val_recall": recall_score(y_val, y_val_pred, average="binary"),
                "test_recall": recall_score(y_test, y_test_pred, average="binary"),
                "train_f1": f1_score(y_train, y_train_pred, average="binary"),
                "val_f1": f1_score(y_val, y_val_pred, average="binary"),
                "test_f1": f1_score(y_test, y_test_pred, average="binary"),
            }

            # ROC AUC (if probability predictions available)
            if hasattr(self.model, "predict_proba"):
                y_train_proba = self.model.predict_proba(X_train_scaled)[:, 1]
                y_val_proba = self.model.predict_proba(X_val_scaled)[:, 1]
                y_test_proba = self.model.predict_proba(X_test_scaled)[:, 1]

                self.metrics["train_auc"] = roc_auc_score(y_train, y_train_proba)
                self.metrics["val_auc"] = roc_auc_score(y_val, y_val_proba)
                self.metrics["test_auc"] = roc_auc_score(y_test, y_test_proba)

        else:  # Regressor
            self.metrics = {
                "train_rmse": np.sqrt(mean_squared_error(y_train, y_train_pred)),
                "val_rmse": np.sqrt(mean_squared_error(y_val, y_val_pred)),
                "test_rmse": np.sqrt(mean_squared_error(y_test, y_test_pred)),
                "train_mae": mean_absolute_error(y_train, y_train_pred),
                "val_mae": mean_absolute_error(y_val, y_val_pred),
                "test_mae": mean_absolute_error(y_test, y_test_pred),
                "train_r2": r2_score(y_train, y_train_pred),
                "val_r2": r2_score(y_val, y_val_pred),
                "test_r2": r2_score(y_test, y_test_pred),
            }

        # Cross-validation
        cv_scores = self._cross_validate(X_temp, y_temp)
        self.metrics["cv_mean"] = cv_scores.mean()
        self.metrics["cv_std"] = cv_scores.std()

        # Feature importance
        if hasattr(self.model, "feature_importances_"):
            self.metrics["feature_importance"] = dict(zip(
                self.feature_names,
                self.model.feature_importances_
            ))

        logger.info(f"Training completed. Test accuracy/R2: {self.metrics.get('test_accuracy') or self.metrics.get('test_r2'):.4f}")

        return self.metrics

    def _cross_validate(self, X: pd.DataFrame, y: pd.Series) -> np.ndarray:
        """Perform time series cross-validation"""
        tscv = TimeSeriesSplit(n_splits=self.config.cv_folds)

        # Scale if needed
        if self.scaler:
            X_scaled = self.scaler.transform(X)
        else:
            X_scaled = X.values

        # Choose scoring metric
        scoring = "accuracy" if self._is_classifier() else "r2"

        cv_scores = cross_val_score(
            self.model,
            X_scaled,
            y,
            cv=tscv,
            scoring=scoring,
            n_jobs=-1,
        )

        return cv_scores

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions"""
        if not self.is_trained:
            raise ValueError("Model not trained")

        if self.scaler:
            X_scaled = self.scaler.transform(X)
        else:
            X_scaled = X.values

        return self.model.predict(X_scaled)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Get probability predictions (classifiers only)"""
        if not self.is_trained:
            raise ValueError("Model not trained")

        if not hasattr(self.model, "predict_proba"):
            raise ValueError("Model does not support probability predictions")

        if self.scaler:
            X_scaled = self.scaler.transform(X)
        else:
            X_scaled = X.values

        return self.model.predict_proba(X_scaled)

    def save(self, path: str):
        """Save model to disk"""
        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)

        # Save model
        with open(path, "wb") as f:
            pickle.dump(self.model, f)

        # Save scaler
        if self.scaler:
            scaler_path = path_obj.parent / f"{path_obj.stem}_scaler.pkl"
            with open(scaler_path, "wb") as f:
                pickle.dump(self.scaler, f)

        # Save metadata
        metadata = {
            "model_type": self.config.model_type.value,
            "feature_names": self.feature_names,
            "metrics": {k: float(v) if isinstance(v, (int, float, np.number)) else v
                       for k, v in self.metrics.items()},
            "hyperparameters": self.config.hyperparameters,
        }

        metadata_path = path_obj.parent / f"{path_obj.stem}_metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"Model saved to {path}")

    @classmethod
    def load(cls, path: str) -> "MLModel":
        """Load model from disk"""
        path_obj = Path(path)

        # Load metadata
        metadata_path = path_obj.parent / f"{path_obj.stem}_metadata.json"
        with open(metadata_path, "r") as f:
            metadata = json.load(f)

        # Create config
        config = ModelConfig(
            model_type=ModelType(metadata["model_type"]),
            hyperparameters=metadata.get("hyperparameters"),
        )

        # Create instance
        instance = cls(config)

        # Load model
        with open(path, "rb") as f:
            instance.model = pickle.load(f)

        # Load scaler
        scaler_path = path_obj.parent / f"{path_obj.stem}_scaler.pkl"
        if scaler_path.exists():
            with open(scaler_path, "rb") as f:
                instance.scaler = pickle.load(f)

        # Restore metadata
        instance.feature_names = metadata["feature_names"]
        instance.metrics = metadata["metrics"]
        instance.is_trained = True

        logger.info(f"Model loaded from {path}")

        return instance

    def _is_classifier(self) -> bool:
        """Check if model is a classifier"""
        return "classifier" in self.config.model_type.value.lower()

    def get_feature_importance(self, top_n: int = 20) -> pd.DataFrame:
        """Get top N most important features"""
        if "feature_importance" not in self.metrics:
            return pd.DataFrame()

        importance_dict = self.metrics["feature_importance"]
        importance_df = pd.DataFrame({
            "feature": list(importance_dict.keys()),
            "importance": list(importance_dict.values()),
        })

        return importance_df.nlargest(top_n, "importance")


class ModelTrainer:
    """
    High-level model training orchestrator
    """

    @staticmethod
    async def train_multiple_models(
        X: pd.DataFrame,
        y: pd.Series,
        model_configs: List[ModelConfig],
    ) -> List[Tuple[MLModel, Dict[str, float]]]:
        """
        Train multiple models and compare

        Args:
            X: Features
            y: Labels
            model_configs: List of model configurations

        Returns:
            List of (model, metrics) tuples
        """
        results = []

        for config in model_configs:
            logger.info(f"Training model: {config.model_type}")

            model = MLModel(config)
            metrics = model.train(X, y)

            results.append((model, metrics))

        # Sort by performance
        metric_key = "test_accuracy" if results[0][0]._is_classifier() else "test_r2"
        results.sort(key=lambda x: x[1].get(metric_key, 0), reverse=True)

        logger.info("Model comparison:")
        for i, (model, metrics) in enumerate(results):
            logger.info(f"{i+1}. {model.config.model_type}: {metrics.get(metric_key):.4f}")

        return results

    @staticmethod
    def compare_models(models: List[Tuple[MLModel, Dict[str, float]]]) -> pd.DataFrame:
        """Create comparison DataFrame"""
        comparison = []

        for model, metrics in models:
            row = {
                "model_type": model.config.model_type.value,
                **metrics,
            }
            comparison.append(row)

        return pd.DataFrame(comparison)
