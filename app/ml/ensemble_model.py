"""
Ensemble Model for Price Forecasting
Combines LSTM, Random Forest, and Gradient Boosting predictions
"""

import numpy as np
import pandas as pd
from typing import Tuple, Optional, Dict, Any, List
import logging
from pathlib import Path
import joblib

from app.ml.lstm_model import LSTMPricePredictor
from app.ml.random_forest_model import RandomForestPricePredictor
from app.ml.gradient_boosting_model import GradientBoostingPricePredictor

logger = logging.getLogger(__name__)


class EnsemblePricePredictor:
    """
    Ensemble model combining LSTM, Random Forest, and Gradient Boosting
    """

    def __init__(
        self,
        lstm_config: Optional[Dict[str, Any]] = None,
        rf_config: Optional[Dict[str, Any]] = None,
        gb_config: Optional[Dict[str, Any]] = None,
        weights: Optional[Dict[str, float]] = None
    ):
        """
        Initialize Ensemble predictor

        Args:
            lstm_config: Configuration for LSTM model
            rf_config: Configuration for Random Forest model
            gb_config: Configuration for Gradient Boosting model
            weights: Custom weights for each model {'lstm': 0.4, 'rf': 0.3, 'gb': 0.3}
        """
        # Initialize individual models
        self.lstm_model = LSTMPricePredictor(**(lstm_config or {}))
        self.rf_model = RandomForestPricePredictor(**(rf_config or {}))
        self.gb_model = GradientBoostingPricePredictor(**(gb_config or {}))

        # Set weights (default to equal weighting)
        self.weights = weights or {'lstm': 0.33, 'rf': 0.33, 'gb': 0.34}
        self._normalize_weights()

        self.is_trained = False
        self.model_performance: Dict[str, Dict[str, float]] = {}

    def _normalize_weights(self):
        """Ensure weights sum to 1.0"""
        total = sum(self.weights.values())
        if total > 0:
            self.weights = {k: v / total for k, v in self.weights.items()}
        logger.info(f"Model weights: {self.weights}")

    def train(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: Optional[pd.DataFrame] = None,
        y_val: Optional[pd.Series] = None,
        train_lstm: bool = True,
        train_rf: bool = True,
        train_gb: bool = True,
        lstm_epochs: int = 50,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Train all ensemble models

        Args:
            X_train: Training features
            y_train: Training targets
            X_val: Validation features
            y_val: Validation targets
            train_lstm: Whether to train LSTM
            train_rf: Whether to train Random Forest
            train_gb: Whether to train Gradient Boosting
            lstm_epochs: Number of epochs for LSTM
            verbose: Whether to print progress

        Returns:
            Combined training metrics
        """
        logger.info("Starting ensemble model training")
        results = {}

        # Train LSTM
        if train_lstm:
            try:
                logger.info("Training LSTM model...")
                lstm_result = self.lstm_model.train(
                    X_train, y_train,
                    X_val, y_val,
                    epochs=lstm_epochs,
                    verbose=1 if verbose else 0
                )
                results['lstm'] = lstm_result
                self.model_performance['lstm'] = {
                    'final_loss': lstm_result['loss'][-1],
                    'final_mae': lstm_result['mae'][-1]
                }
                logger.info(f"LSTM training complete - MAE: {lstm_result['mae'][-1]:.4f}")
            except Exception as e:
                logger.error(f"LSTM training failed: {str(e)}")
                results['lstm'] = {'error': str(e)}

        # Train Random Forest
        if train_rf:
            try:
                logger.info("Training Random Forest model...")
                rf_result = self.rf_model.train(X_train, y_train)
                results['rf'] = rf_result
                self.model_performance['rf'] = {
                    'r2_score': rf_result['r2_score'],
                    'mae': rf_result['mae']
                }
                logger.info(f"Random Forest training complete - MAE: {rf_result['mae']:.4f}")
            except Exception as e:
                logger.error(f"Random Forest training failed: {str(e)}")
                results['rf'] = {'error': str(e)}

        # Train Gradient Boosting
        if train_gb:
            try:
                logger.info("Training Gradient Boosting model...")
                gb_result = self.gb_model.train(
                    X_train, y_train,
                    X_val, y_val,
                    verbose=verbose
                )
                results['gb'] = gb_result
                self.model_performance['gb'] = {
                    'mae': gb_result['mae'],
                    'rmse': gb_result['rmse']
                }
                logger.info(f"Gradient Boosting training complete - MAE: {gb_result['mae']:.4f}")
            except Exception as e:
                logger.error(f"Gradient Boosting training failed: {str(e)}")
                results['gb'] = {'error': str(e)}

        # Optimize weights based on validation performance if available
        if X_val is not None and y_val is not None:
            self._optimize_weights(X_val, y_val)

        self.is_trained = True
        logger.info("Ensemble model training complete")

        return {
            'individual_results': results,
            'weights': self.weights,
            'performance': self.model_performance
        }

    def _optimize_weights(self, X_val: pd.DataFrame, y_val: pd.Series):
        """
        Optimize ensemble weights based on validation performance

        Args:
            X_val: Validation features
            y_val: Validation targets
        """
        logger.info("Optimizing ensemble weights...")

        # Get predictions from each model
        predictions = {}
        maes = {}

        # LSTM predictions
        if self.lstm_model.is_trained:
            try:
                lstm_preds, _, _ = self.lstm_model.predict(X_val, return_confidence=False)
                # Align predictions with targets (LSTM creates sequences)
                if len(lstm_preds) < len(y_val):
                    y_val_aligned = y_val.iloc[-len(lstm_preds):].values
                else:
                    y_val_aligned = y_val.values
                    lstm_preds = lstm_preds[:len(y_val)]

                predictions['lstm'] = lstm_preds
                maes['lstm'] = np.mean(np.abs(y_val_aligned - lstm_preds))
            except Exception as e:
                logger.warning(f"Could not get LSTM predictions for weight optimization: {e}")

        # Random Forest predictions
        if self.rf_model.is_trained:
            try:
                rf_preds, _, _ = self.rf_model.predict(X_val, return_confidence=False)
                predictions['rf'] = rf_preds
                maes['rf'] = np.mean(np.abs(y_val - rf_preds))
            except Exception as e:
                logger.warning(f"Could not get RF predictions for weight optimization: {e}")

        # Gradient Boosting predictions
        if self.gb_model.is_trained:
            try:
                gb_preds, _, _ = self.gb_model.predict(X_val, return_confidence=False)
                predictions['gb'] = gb_preds
                maes['gb'] = np.mean(np.abs(y_val - gb_preds))
            except Exception as e:
                logger.warning(f"Could not get GB predictions for weight optimization: {e}")

        # Calculate inverse MAE weights (better models get higher weight)
        if maes:
            inverse_maes = {k: 1.0 / v if v > 0 else 0.0 for k, v in maes.items()}
            total = sum(inverse_maes.values())
            if total > 0:
                optimized_weights = {k: v / total for k, v in inverse_maes.items()}
                # Blend optimized weights with original weights (70% optimized, 30% original)
                for key in self.weights:
                    if key in optimized_weights:
                        self.weights[key] = 0.7 * optimized_weights[key] + 0.3 * self.weights[key]

                self._normalize_weights()
                logger.info(f"Optimized weights based on validation MAE: {self.weights}")

    def predict(
        self,
        X: pd.DataFrame,
        return_confidence: bool = True,
        return_individual: bool = False
    ) -> Tuple[np.ndarray, Optional[np.ndarray], Optional[np.ndarray], Optional[Dict[str, np.ndarray]]]:
        """
        Make ensemble predictions

        Args:
            X: Features to predict on
            return_confidence: Whether to return confidence intervals
            return_individual: Whether to return individual model predictions

        Returns:
            Tuple of (ensemble_predictions, lower_bound, upper_bound, individual_predictions)
        """
        if not self.is_trained:
            raise ValueError("Ensemble must be trained before making predictions")

        predictions_list = []
        weights_list = []
        individual_preds = {}
        all_lower_bounds = []
        all_upper_bounds = []

        # LSTM predictions
        if self.lstm_model.is_trained and self.weights.get('lstm', 0) > 0:
            try:
                lstm_pred, lstm_lower, lstm_upper = self.lstm_model.predict(
                    X, return_confidence=return_confidence, n_simulations=50
                )
                predictions_list.append(lstm_pred)
                weights_list.append(self.weights['lstm'])
                individual_preds['lstm'] = lstm_pred
                if return_confidence and lstm_lower is not None:
                    all_lower_bounds.append(lstm_lower)
                    all_upper_bounds.append(lstm_upper)
            except Exception as e:
                logger.warning(f"LSTM prediction failed: {e}")

        # Random Forest predictions
        if self.rf_model.is_trained and self.weights.get('rf', 0) > 0:
            try:
                rf_pred, rf_lower, rf_upper = self.rf_model.predict(
                    X, return_confidence=return_confidence
                )
                predictions_list.append(rf_pred)
                weights_list.append(self.weights['rf'])
                individual_preds['rf'] = rf_pred
                if return_confidence and rf_lower is not None:
                    all_lower_bounds.append(rf_lower)
                    all_upper_bounds.append(rf_upper)
            except Exception as e:
                logger.warning(f"Random Forest prediction failed: {e}")

        # Gradient Boosting predictions
        if self.gb_model.is_trained and self.weights.get('gb', 0) > 0:
            try:
                gb_pred, gb_lower, gb_upper = self.gb_model.predict(
                    X, return_confidence=return_confidence
                )
                predictions_list.append(gb_pred)
                weights_list.append(self.weights['gb'])
                individual_preds['gb'] = gb_pred
                if return_confidence and gb_lower is not None:
                    all_lower_bounds.append(gb_lower)
                    all_upper_bounds.append(gb_upper)
            except Exception as e:
                logger.warning(f"Gradient Boosting prediction failed: {e}")

        if not predictions_list:
            raise ValueError("No models available for prediction")

        # Handle different prediction lengths (LSTM may produce fewer predictions)
        min_length = min(len(p) for p in predictions_list)
        predictions_aligned = [p[-min_length:] for p in predictions_list]
        weights_normalized = np.array(weights_list) / sum(weights_list)

        # Weighted ensemble prediction
        ensemble_pred = np.average(predictions_aligned, axis=0, weights=weights_normalized)

        # Combine confidence intervals
        lower_bound = None
        upper_bound = None
        if return_confidence and all_lower_bounds:
            all_lower_aligned = [lb[-min_length:] for lb in all_lower_bounds]
            all_upper_aligned = [ub[-min_length:] for ub in all_upper_bounds]
            lower_bound = np.average(all_lower_aligned, axis=0, weights=weights_normalized)
            upper_bound = np.average(all_upper_aligned, axis=0, weights=weights_normalized)

        return (
            ensemble_pred,
            lower_bound,
            upper_bound,
            individual_preds if return_individual else None
        )

    def get_model_contributions(self) -> Dict[str, float]:
        """
        Get the contribution weight of each model

        Returns:
            Dictionary of model weights
        """
        return self.weights.copy()

    def get_feature_importance(self, top_n: int = 20) -> Dict[str, pd.DataFrame]:
        """
        Get feature importance from tree-based models

        Args:
            top_n: Number of top features to return

        Returns:
            Dictionary of feature importance DataFrames for each model
        """
        importance_dict = {}

        if self.rf_model.is_trained:
            try:
                importance_dict['rf'] = self.rf_model.get_feature_importance(top_n)
            except Exception as e:
                logger.warning(f"Could not get RF feature importance: {e}")

        if self.gb_model.is_trained:
            try:
                importance_dict['gb'] = self.gb_model.get_feature_importance(top_n)
            except Exception as e:
                logger.warning(f"Could not get GB feature importance: {e}")

        return importance_dict

    def save(self, model_dir: str, ensemble_name: str = "ensemble"):
        """
        Save all ensemble models

        Args:
            model_dir: Directory to save models
            ensemble_name: Base name for ensemble files
        """
        if not self.is_trained:
            raise ValueError("Ensemble must be trained before saving")

        model_path = Path(model_dir)
        model_path.mkdir(parents=True, exist_ok=True)

        # Save individual models
        if self.lstm_model.is_trained:
            self.lstm_model.save(model_dir, f"{ensemble_name}_lstm")

        if self.rf_model.is_trained:
            self.rf_model.save(model_dir, f"{ensemble_name}_rf")

        if self.gb_model.is_trained:
            self.gb_model.save(model_dir, f"{ensemble_name}_gb")

        # Save ensemble configuration
        config = {
            'weights': self.weights,
            'model_performance': self.model_performance,
            'is_trained': self.is_trained
        }
        joblib.dump(config, model_path / f"{ensemble_name}_config.pkl")

        logger.info(f"Ensemble model saved to {model_path}")

    def load(self, model_dir: str, ensemble_name: str = "ensemble"):
        """
        Load all ensemble models

        Args:
            model_dir: Directory containing the models
            ensemble_name: Base name for ensemble files
        """
        model_path = Path(model_dir)

        # Load ensemble configuration
        config = joblib.load(model_path / f"{ensemble_name}_config.pkl")
        self.weights = config['weights']
        self.model_performance = config['model_performance']

        # Load individual models
        lstm_path = model_path / f"{ensemble_name}_lstm.keras"
        if lstm_path.exists():
            self.lstm_model.load(model_dir, f"{ensemble_name}_lstm")

        rf_path = model_path / f"{ensemble_name}_rf.pkl"
        if rf_path.exists():
            self.rf_model.load(model_dir, f"{ensemble_name}_rf")

        gb_xgb_path = model_path / f"{ensemble_name}_gb.xgb"
        gb_lgb_path = model_path / f"{ensemble_name}_gb.lgb"
        if gb_xgb_path.exists() or gb_lgb_path.exists():
            self.gb_model.load(model_dir, f"{ensemble_name}_gb")

        self.is_trained = True
        logger.info(f"Ensemble model loaded from {model_path}")
