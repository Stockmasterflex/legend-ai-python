"""
Price Forecasting Service
Orchestrates feature engineering, model training, prediction, and persistence
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
import logging
from pathlib import Path

from app.ml.feature_engineering import FeatureEngineer
from app.ml.ensemble_model import EnsemblePricePredictor
from app.ml.lstm_model import LSTMPricePredictor
from app.ml.random_forest_model import RandomForestPricePredictor
from app.ml.gradient_boosting_model import GradientBoostingPricePredictor

logger = logging.getLogger(__name__)


class PriceForecastingService:
    """
    Main service for price forecasting
    Handles data preparation, model training, prediction, and result storage
    """

    def __init__(
        self,
        model_dir: str = "models",
        use_ensemble: bool = True,
        model_type: str = "ensemble"  # 'ensemble', 'lstm', 'rf', 'xgboost', 'lightgbm'
    ):
        """
        Initialize forecasting service

        Args:
            model_dir: Directory for saving/loading models
            use_ensemble: Whether to use ensemble model
            model_type: Type of model to use
        """
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)

        self.feature_engineer = FeatureEngineer()
        self.model_type = model_type
        self.use_ensemble = use_ensemble

        # Initialize model
        if use_ensemble or model_type == "ensemble":
            self.model = EnsemblePricePredictor()
        elif model_type == "lstm":
            self.model = LSTMPricePredictor()
        elif model_type == "rf":
            self.model = RandomForestPricePredictor()
        elif model_type in ["xgboost", "lightgbm"]:
            self.model = GradientBoostingPricePredictor(model_type=model_type)
        else:
            raise ValueError(f"Unknown model type: {model_type}")

        self.is_trained = False
        self.training_metrics: Dict[str, Any] = {}

    def prepare_data(
        self,
        df: pd.DataFrame,
        forecast_horizon: int = 1,
        test_size: float = 0.2
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.DataFrame]:
        """
        Prepare data for model training

        Args:
            df: DataFrame with OHLCV data
            forecast_horizon: Days ahead to predict
            test_size: Fraction for test set

        Returns:
            Tuple of (X_train, X_test, y_train, y_test, engineered_df)
        """
        logger.info(f"Preparing data with {len(df)} samples")

        # Engineer features
        engineered_df = self.feature_engineer.prepare_features(df)

        # Prepare ML dataset
        X_train, X_test, y_train, y_test = self.feature_engineer.prepare_ml_dataset(
            engineered_df,
            target_column='close',
            forecast_horizon=forecast_horizon,
            test_size=test_size
        )

        logger.info(f"Data prepared: {len(X_train)} train, {len(X_test)} test samples")

        return X_train, X_test, y_train, y_test, engineered_df

    def train_model(
        self,
        df: pd.DataFrame,
        forecast_horizon: int = 1,
        test_size: float = 0.2,
        save_model: bool = True,
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Train the forecasting model

        Args:
            df: DataFrame with OHLCV data
            forecast_horizon: Days ahead to predict
            test_size: Fraction for test set
            save_model: Whether to save trained model
            model_name: Custom model name for saving

        Returns:
            Training metrics dictionary
        """
        logger.info("Starting model training")

        # Prepare data
        X_train, X_test, y_train, y_test, _ = self.prepare_data(
            df, forecast_horizon, test_size
        )

        # Train based on model type
        if isinstance(self.model, EnsemblePricePredictor):
            metrics = self.model.train(
                X_train, y_train,
                X_test, y_test,
                verbose=True
            )
        elif isinstance(self.model, LSTMPricePredictor):
            metrics = self.model.train(
                X_train, y_train,
                X_test, y_test,
                epochs=100,
                verbose=1
            )
        else:  # RF or GB
            metrics = self.model.train(X_train, y_train)

        self.is_trained = True
        self.training_metrics = metrics

        # Evaluate on test set
        test_metrics = self.evaluate(X_test, y_test)
        metrics['test_metrics'] = test_metrics

        # Save model if requested
        if save_model:
            save_name = model_name or f"{self.model_type}_model"
            self.save_model(save_name)

        logger.info(f"Model training complete. Test MAE: {test_metrics.get('mae', 'N/A')}")

        return metrics

    def evaluate(
        self,
        X_test: pd.DataFrame,
        y_test: pd.Series
    ) -> Dict[str, float]:
        """
        Evaluate model on test data

        Args:
            X_test: Test features
            y_test: Test targets

        Returns:
            Dictionary of evaluation metrics
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")

        logger.info("Evaluating model...")

        # Make predictions
        if isinstance(self.model, EnsemblePricePredictor):
            predictions, _, _, _ = self.model.predict(X_test, return_confidence=False)
        else:
            predictions, _, _ = self.model.predict(X_test, return_confidence=False)

        # Handle different prediction lengths (LSTM)
        if len(predictions) < len(y_test):
            y_test_aligned = y_test.iloc[-len(predictions):].values
        else:
            y_test_aligned = y_test.values
            predictions = predictions[:len(y_test)]

        # Calculate metrics
        mae = np.mean(np.abs(y_test_aligned - predictions))
        rmse = np.sqrt(np.mean((y_test_aligned - predictions) ** 2))
        mape = np.mean(np.abs((y_test_aligned - predictions) / y_test_aligned)) * 100

        # Directional accuracy
        actual_direction = np.sign(np.diff(y_test_aligned))
        pred_direction = np.sign(np.diff(predictions))
        directional_accuracy = np.mean(actual_direction == pred_direction) * 100

        # R-squared
        ss_res = np.sum((y_test_aligned - predictions) ** 2)
        ss_tot = np.sum((y_test_aligned - np.mean(y_test_aligned)) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        metrics = {
            'mae': float(mae),
            'rmse': float(rmse),
            'mape': float(mape),
            'r2_score': float(r2),
            'directional_accuracy': float(directional_accuracy),
            'n_samples': len(y_test_aligned)
        }

        logger.info(f"Evaluation complete - MAE: {mae:.4f}, RMSE: {rmse:.4f}, R²: {r2:.4f}")

        return metrics

    def predict(
        self,
        df: pd.DataFrame,
        return_confidence: bool = True,
        return_individual: bool = False
    ) -> Dict[str, Any]:
        """
        Make price predictions

        Args:
            df: DataFrame with OHLCV data
            return_confidence: Whether to return confidence intervals
            return_individual: Whether to return individual model predictions (ensemble only)

        Returns:
            Dictionary with predictions and metadata
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")

        logger.info(f"Making predictions for {len(df)} samples")

        # Prepare features
        engineered_df = self.feature_engineer.prepare_features(df)

        # Remove rows with NaN
        engineered_df_clean = engineered_df.dropna()

        # Get feature columns (excluding OHLCV and other metadata)
        feature_cols = [col for col in engineered_df_clean.columns if col not in [
            'open', 'high', 'low', 'close', 'volume',
            'date', 'timestamp', 'target', 'market_regime', 'volatility_regime', 'trend_strength'
        ]]

        X = engineered_df_clean[feature_cols]

        # Make predictions
        if isinstance(self.model, EnsemblePricePredictor):
            predictions, lower, upper, individual = self.model.predict(
                X,
                return_confidence=return_confidence,
                return_individual=return_individual
            )
        else:
            predictions, lower, upper = self.model.predict(X, return_confidence=return_confidence)
            individual = None

        # Get current prices for comparison
        current_prices = engineered_df_clean['close'].values

        # Calculate predicted returns
        if len(predictions) == len(current_prices):
            predicted_returns = ((predictions - current_prices) / current_prices) * 100
        else:
            # Handle LSTM sequence mismatch
            current_prices_aligned = current_prices[-len(predictions):]
            predicted_returns = ((predictions - current_prices_aligned) / current_prices_aligned) * 100

        result = {
            'predictions': predictions.tolist(),
            'predicted_returns': predicted_returns.tolist(),
            'confidence_lower': lower.tolist() if lower is not None else None,
            'confidence_upper': upper.tolist() if upper is not None else None,
            'timestamps': engineered_df_clean.index[-len(predictions):].tolist() if hasattr(engineered_df_clean.index, 'tolist') else None,
            'model_type': self.model_type,
            'n_predictions': len(predictions)
        }

        if individual and return_individual:
            result['individual_predictions'] = {
                k: v.tolist() for k, v in individual.items()
            }

        logger.info(f"Generated {len(predictions)} predictions")

        return result

    def forecast_future(
        self,
        df: pd.DataFrame,
        n_days: int = 5,
        confidence_level: float = 0.9
    ) -> Dict[str, Any]:
        """
        Forecast future prices (multi-step ahead)

        Args:
            df: Historical DataFrame with OHLCV data
            n_days: Number of days to forecast
            confidence_level: Confidence level for intervals

        Returns:
            Dictionary with forecasts and confidence intervals
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before forecasting")

        logger.info(f"Forecasting {n_days} days ahead")

        # Prepare features
        engineered_df = self.feature_engineer.prepare_features(df)
        engineered_df_clean = engineered_df.dropna()

        # Get recent data
        recent_data = engineered_df_clean.tail(100)  # Use last 100 samples

        feature_cols = [col for col in recent_data.columns if col not in [
            'open', 'high', 'low', 'close', 'volume',
            'date', 'timestamp', 'target', 'market_regime', 'volatility_regime', 'trend_strength'
        ]]

        X_recent = recent_data[feature_cols]

        # Forecast based on model type
        if isinstance(self.model, LSTMPricePredictor):
            predictions, lower, upper = self.model.predict_future(
                X_recent,
                n_steps=n_days,
                return_confidence=True
            )
        else:
            # For non-sequential models, we can only predict one step ahead reliably
            # For multi-step, we'd need to iteratively predict and update features
            predictions, lower, upper = self.model.predict(X_recent.tail(1), return_confidence=True)
            predictions = np.repeat(predictions[-1], n_days)  # Simple extension
            if lower is not None:
                lower = np.repeat(lower[-1], n_days)
            if upper is not None:
                upper = np.repeat(upper[-1], n_days)

        # Generate future dates
        last_date = df.index[-1] if hasattr(df.index, '__getitem__') else datetime.now()
        if isinstance(last_date, str):
            last_date = pd.to_datetime(last_date)

        future_dates = [last_date + timedelta(days=i+1) for i in range(n_days)]

        result = {
            'forecast_dates': [d.isoformat() if hasattr(d, 'isoformat') else str(d) for d in future_dates],
            'forecasted_prices': predictions.tolist(),
            'confidence_lower': lower.tolist() if lower is not None else None,
            'confidence_upper': upper.tolist() if upper is not None else None,
            'confidence_level': confidence_level,
            'model_type': self.model_type
        }

        logger.info(f"Generated forecast for {n_days} days")

        return result

    def get_feature_importance(self, top_n: int = 20) -> Dict[str, Any]:
        """
        Get feature importance from the model

        Args:
            top_n: Number of top features to return

        Returns:
            Dictionary with feature importance data
        """
        if not self.is_trained:
            raise ValueError("Model must be trained to get feature importance")

        if isinstance(self.model, EnsemblePricePredictor):
            importance = self.model.get_feature_importance(top_n)
            return {
                'type': 'ensemble',
                'importance': {k: v.to_dict('records') for k, v in importance.items()}
            }
        elif isinstance(self.model, (RandomForestPricePredictor, GradientBoostingPricePredictor)):
            importance_df = self.model.get_feature_importance(top_n)
            return {
                'type': self.model_type,
                'importance': importance_df.to_dict('records')
            }
        else:
            return {'type': self.model_type, 'importance': None}

    def save_model(self, model_name: str):
        """
        Save the trained model

        Args:
            model_name: Name for the saved model
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")

        self.model.save(str(self.model_dir), model_name)
        logger.info(f"Model saved as '{model_name}' in {self.model_dir}")

    def load_model(self, model_name: str):
        """
        Load a previously trained model

        Args:
            model_name: Name of the model to load
        """
        self.model.load(str(self.model_dir), model_name)
        self.is_trained = True
        logger.info(f"Model '{model_name}' loaded from {self.model_dir}")

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model

        Returns:
            Dictionary with model information
        """
        info = {
            'model_type': self.model_type,
            'is_trained': self.is_trained,
            'use_ensemble': self.use_ensemble,
            'training_metrics': self.training_metrics
        }

        if isinstance(self.model, EnsemblePricePredictor):
            info['model_weights'] = self.model.get_model_contributions()
            info['model_performance'] = self.model.model_performance

        return info
