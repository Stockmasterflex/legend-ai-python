"""
Random Forest Model for Price Forecasting
Implements ensemble tree-based prediction with feature importance
"""

import numpy as np
import pandas as pd
from typing import Tuple, Optional, Dict, Any, List
import logging
from pathlib import Path

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib

logger = logging.getLogger(__name__)


class RandomForestPricePredictor:
    """
    Random Forest-based price forecasting model
    """

    def __init__(
        self,
        n_estimators: int = 200,
        max_depth: Optional[int] = 20,
        min_samples_split: int = 5,
        min_samples_leaf: int = 2,
        max_features: str = 'sqrt',
        random_state: int = 42,
        n_jobs: int = -1
    ):
        """
        Initialize Random Forest predictor

        Args:
            n_estimators: Number of trees in the forest
            max_depth: Maximum depth of trees
            min_samples_split: Minimum samples required to split a node
            min_samples_leaf: Minimum samples required at leaf node
            max_features: Number of features to consider for best split
            random_state: Random seed for reproducibility
            n_jobs: Number of parallel jobs (-1 for all cores)
        """
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.random_state = random_state
        self.n_jobs = n_jobs

        self.model: Optional[RandomForestRegressor] = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names: List[str] = []
        self.feature_importance: Optional[pd.DataFrame] = None

    def train(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        scale_features: bool = True
    ) -> Dict[str, Any]:
        """
        Train the Random Forest model

        Args:
            X_train: Training features
            y_train: Training targets
            scale_features: Whether to scale features

        Returns:
            Training metrics dictionary
        """
        logger.info("Starting Random Forest model training")

        # Store feature names
        self.feature_names = list(X_train.columns)

        # Scale features if requested
        if scale_features:
            X_train_processed = self.scaler.fit_transform(X_train)
        else:
            X_train_processed = X_train.values

        # Initialize model
        self.model = RandomForestRegressor(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            min_samples_split=self.min_samples_split,
            min_samples_leaf=self.min_samples_leaf,
            max_features=self.max_features,
            random_state=self.random_state,
            n_jobs=self.n_jobs,
            verbose=0
        )

        # Train model
        self.model.fit(X_train_processed, y_train)

        # Calculate feature importance
        self._calculate_feature_importance()

        self.is_trained = True

        # Calculate training metrics
        train_score = self.model.score(X_train_processed, y_train)
        train_predictions = self.model.predict(X_train_processed)
        train_mae = np.mean(np.abs(y_train - train_predictions))
        train_rmse = np.sqrt(np.mean((y_train - train_predictions) ** 2))

        logger.info(f"Random Forest training complete - R²: {train_score:.4f}, MAE: {train_mae:.4f}")

        return {
            'r2_score': train_score,
            'mae': train_mae,
            'rmse': train_rmse,
            'n_features': len(self.feature_names),
            'n_samples': len(X_train)
        }

    def predict(
        self,
        X: pd.DataFrame,
        return_confidence: bool = True,
        confidence_level: float = 0.9
    ) -> Tuple[np.ndarray, Optional[np.ndarray], Optional[np.ndarray]]:
        """
        Make predictions with the Random Forest model

        Args:
            X: Features to predict on
            return_confidence: Whether to return confidence intervals
            confidence_level: Confidence level for intervals (e.g., 0.9 for 90%)

        Returns:
            Tuple of (predictions, lower_bound, upper_bound)
        """
        if not self.is_trained or self.model is None:
            raise ValueError("Model must be trained before making predictions")

        # Scale features if scaler was fitted
        if hasattr(self.scaler, 'mean_'):
            X_processed = self.scaler.transform(X)
        else:
            X_processed = X.values

        # Make predictions
        predictions = self.model.predict(X_processed)

        # Calculate confidence intervals using individual tree predictions
        lower_bound = None
        upper_bound = None

        if return_confidence:
            # Get predictions from all trees
            all_tree_predictions = np.array([
                tree.predict(X_processed) for tree in self.model.estimators_
            ])

            # Calculate percentiles for confidence intervals
            lower_percentile = (1 - confidence_level) / 2 * 100
            upper_percentile = (1 + confidence_level) / 2 * 100

            lower_bound = np.percentile(all_tree_predictions, lower_percentile, axis=0)
            upper_bound = np.percentile(all_tree_predictions, upper_percentile, axis=0)

        return predictions, lower_bound, upper_bound

    def predict_with_uncertainty(
        self,
        X: pd.DataFrame
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict with uncertainty estimates using tree variance

        Args:
            X: Features to predict on

        Returns:
            Tuple of (predictions, std_dev)
        """
        if not self.is_trained or self.model is None:
            raise ValueError("Model must be trained before making predictions")

        # Scale features if scaler was fitted
        if hasattr(self.scaler, 'mean_'):
            X_processed = self.scaler.transform(X)
        else:
            X_processed = X.values

        # Get predictions from all trees
        all_tree_predictions = np.array([
            tree.predict(X_processed) for tree in self.model.estimators_
        ])

        # Calculate mean and standard deviation
        predictions = np.mean(all_tree_predictions, axis=0)
        std_dev = np.std(all_tree_predictions, axis=0)

        return predictions, std_dev

    def _calculate_feature_importance(self):
        """Calculate and store feature importance"""
        if self.model is None:
            return

        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)

        self.feature_importance = importance_df
        logger.info(f"Top 5 important features: {importance_df.head()['feature'].tolist()}")

    def get_feature_importance(self, top_n: Optional[int] = None) -> pd.DataFrame:
        """
        Get feature importance ranking

        Args:
            top_n: Return only top N features (None for all)

        Returns:
            DataFrame with features and their importance scores
        """
        if self.feature_importance is None:
            raise ValueError("Model must be trained to get feature importance")

        if top_n is not None:
            return self.feature_importance.head(top_n)
        return self.feature_importance

    def save(self, model_dir: str, model_name: str = "random_forest_model"):
        """
        Save the trained model and scaler

        Args:
            model_dir: Directory to save model
            model_name: Name for the model files
        """
        if not self.is_trained or self.model is None:
            raise ValueError("Model must be trained before saving")

        model_path = Path(model_dir)
        model_path.mkdir(parents=True, exist_ok=True)

        # Save model
        joblib.dump(self.model, model_path / f"{model_name}.pkl")

        # Save scaler
        joblib.dump(self.scaler, model_path / f"{model_name}_scaler.pkl")

        # Save configuration and metadata
        config = {
            'n_estimators': self.n_estimators,
            'max_depth': self.max_depth,
            'min_samples_split': self.min_samples_split,
            'min_samples_leaf': self.min_samples_leaf,
            'max_features': self.max_features,
            'random_state': self.random_state,
            'feature_names': self.feature_names
        }
        joblib.dump(config, model_path / f"{model_name}_config.pkl")

        # Save feature importance
        if self.feature_importance is not None:
            self.feature_importance.to_csv(
                model_path / f"{model_name}_feature_importance.csv",
                index=False
            )

        logger.info(f"Random Forest model saved to {model_path}")

    def load(self, model_dir: str, model_name: str = "random_forest_model"):
        """
        Load a trained model and scaler

        Args:
            model_dir: Directory containing the model
            model_name: Name of the model files
        """
        model_path = Path(model_dir)

        # Load configuration
        config = joblib.load(model_path / f"{model_name}_config.pkl")
        self.n_estimators = config['n_estimators']
        self.max_depth = config['max_depth']
        self.min_samples_split = config['min_samples_split']
        self.min_samples_leaf = config['min_samples_leaf']
        self.max_features = config['max_features']
        self.random_state = config['random_state']
        self.feature_names = config['feature_names']

        # Load model
        self.model = joblib.load(model_path / f"{model_name}.pkl")

        # Load scaler
        self.scaler = joblib.load(model_path / f"{model_name}_scaler.pkl")

        # Load feature importance if exists
        importance_path = model_path / f"{model_name}_feature_importance.csv"
        if importance_path.exists():
            self.feature_importance = pd.read_csv(importance_path)

        self.is_trained = True
        logger.info(f"Random Forest model loaded from {model_path}")
