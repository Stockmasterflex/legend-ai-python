"""
LSTM Neural Network for Price Forecasting
Implements time series prediction using Long Short-Term Memory networks
"""

import numpy as np
import pandas as pd
from typing import Tuple, Optional, Dict, Any
import logging
from pathlib import Path

# Suppress TensorFlow warnings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.preprocessing import StandardScaler
import joblib

logger = logging.getLogger(__name__)


class LSTMPricePredictor:
    """
    LSTM-based price forecasting model
    """

    def __init__(
        self,
        sequence_length: int = 60,
        n_features: Optional[int] = None,
        lstm_units: Tuple[int, ...] = (128, 64, 32),
        dropout_rate: float = 0.2,
        learning_rate: float = 0.001
    ):
        """
        Initialize LSTM predictor

        Args:
            sequence_length: Number of time steps to look back
            n_features: Number of input features (set during training)
            lstm_units: Tuple of units for each LSTM layer
            dropout_rate: Dropout rate for regularization
            learning_rate: Learning rate for optimizer
        """
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.lstm_units = lstm_units
        self.dropout_rate = dropout_rate
        self.learning_rate = learning_rate

        self.model: Optional[keras.Model] = None
        self.scaler_X = StandardScaler()
        self.scaler_y = StandardScaler()
        self.is_trained = False

    def _build_model(self) -> keras.Model:
        """
        Build LSTM model architecture

        Returns:
            Compiled Keras model
        """
        model = Sequential()

        # First LSTM layer
        model.add(LSTM(
            units=self.lstm_units[0],
            return_sequences=True if len(self.lstm_units) > 1 else False,
            input_shape=(self.sequence_length, self.n_features)
        ))
        model.add(Dropout(self.dropout_rate))
        model.add(BatchNormalization())

        # Additional LSTM layers
        for i, units in enumerate(self.lstm_units[1:], 1):
            return_sequences = i < len(self.lstm_units) - 1
            model.add(LSTM(units=units, return_sequences=return_sequences))
            model.add(Dropout(self.dropout_rate))
            model.add(BatchNormalization())

        # Output layer
        model.add(Dense(units=1))

        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss='mse',
            metrics=['mae', 'mape']
        )

        logger.info(f"LSTM model built with architecture: {self.lstm_units}")
        return model

    def _create_sequences(
        self,
        X: np.ndarray,
        y: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create sequences for LSTM training

        Args:
            X: Feature array
            y: Target array

        Returns:
            Tuple of (sequences, targets)
        """
        sequences = []
        targets = []

        for i in range(len(X) - self.sequence_length):
            sequences.append(X[i:i + self.sequence_length])
            targets.append(y[i + self.sequence_length])

        return np.array(sequences), np.array(targets)

    def train(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: Optional[pd.DataFrame] = None,
        y_val: Optional[pd.Series] = None,
        epochs: int = 100,
        batch_size: int = 32,
        verbose: int = 1
    ) -> Dict[str, Any]:
        """
        Train the LSTM model

        Args:
            X_train: Training features
            y_train: Training targets
            X_val: Validation features (optional)
            y_val: Validation targets (optional)
            epochs: Number of training epochs
            batch_size: Batch size for training
            verbose: Verbosity level

        Returns:
            Training history dictionary
        """
        logger.info("Starting LSTM model training")

        # Set number of features
        self.n_features = X_train.shape[1]

        # Scale features and targets
        X_train_scaled = self.scaler_X.fit_transform(X_train)
        y_train_scaled = self.scaler_y.fit_transform(y_train.values.reshape(-1, 1)).flatten()

        # Create sequences
        X_seq, y_seq = self._create_sequences(X_train_scaled, y_train_scaled)

        logger.info(f"Created {len(X_seq)} training sequences")

        # Prepare validation data if provided
        validation_data = None
        if X_val is not None and y_val is not None:
            X_val_scaled = self.scaler_X.transform(X_val)
            y_val_scaled = self.scaler_y.transform(y_val.values.reshape(-1, 1)).flatten()
            X_val_seq, y_val_seq = self._create_sequences(X_val_scaled, y_val_scaled)
            validation_data = (X_val_seq, y_val_seq)
            logger.info(f"Created {len(X_val_seq)} validation sequences")

        # Build model
        self.model = self._build_model()

        # Callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_loss' if validation_data else 'loss',
                patience=15,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss' if validation_data else 'loss',
                factor=0.5,
                patience=5,
                min_lr=1e-6,
                verbose=1
            )
        ]

        # Train model
        history = self.model.fit(
            X_seq,
            y_seq,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=validation_data,
            callbacks=callbacks,
            verbose=verbose
        )

        self.is_trained = True
        logger.info("LSTM model training complete")

        return {
            'loss': history.history['loss'],
            'mae': history.history['mae'],
            'val_loss': history.history.get('val_loss', []),
            'val_mae': history.history.get('val_mae', [])
        }

    def predict(
        self,
        X: pd.DataFrame,
        return_confidence: bool = True,
        n_simulations: int = 100
    ) -> Tuple[np.ndarray, Optional[np.ndarray], Optional[np.ndarray]]:
        """
        Make predictions with the LSTM model

        Args:
            X: Features to predict on
            return_confidence: Whether to return confidence intervals
            n_simulations: Number of Monte Carlo simulations for confidence

        Returns:
            Tuple of (predictions, lower_bound, upper_bound)
        """
        if not self.is_trained or self.model is None:
            raise ValueError("Model must be trained before making predictions")

        # Scale features
        X_scaled = self.scaler_X.transform(X)

        # Create sequences
        X_seq, _ = self._create_sequences(X_scaled, np.zeros(len(X_scaled)))

        if len(X_seq) == 0:
            raise ValueError(f"Not enough data to create sequences. Need at least {self.sequence_length} samples")

        # Make predictions
        predictions_scaled = self.model.predict(X_seq, verbose=0)

        # Inverse transform predictions
        predictions = self.scaler_y.inverse_transform(predictions_scaled).flatten()

        # Calculate confidence intervals using dropout as Bayesian approximation
        lower_bound = None
        upper_bound = None

        if return_confidence:
            # Enable dropout during prediction for Monte Carlo estimation
            predictions_mc = []
            for _ in range(n_simulations):
                pred_mc = self.model(X_seq, training=True)
                pred_mc_inv = self.scaler_y.inverse_transform(pred_mc.numpy()).flatten()
                predictions_mc.append(pred_mc_inv)

            predictions_mc = np.array(predictions_mc)

            # Calculate 90% confidence intervals
            lower_bound = np.percentile(predictions_mc, 5, axis=0)
            upper_bound = np.percentile(predictions_mc, 95, axis=0)

        return predictions, lower_bound, upper_bound

    def predict_future(
        self,
        X_recent: pd.DataFrame,
        n_steps: int = 5,
        return_confidence: bool = True
    ) -> Tuple[np.ndarray, Optional[np.ndarray], Optional[np.ndarray]]:
        """
        Predict multiple steps into the future

        Args:
            X_recent: Recent feature data (at least sequence_length samples)
            n_steps: Number of steps to predict ahead
            return_confidence: Whether to return confidence intervals

        Returns:
            Tuple of (predictions, lower_bounds, upper_bounds)
        """
        if not self.is_trained or self.model is None:
            raise ValueError("Model must be trained before making predictions")

        predictions = []
        lower_bounds = [] if return_confidence else None
        upper_bounds = [] if return_confidence else None

        # Scale the input
        X_scaled = self.scaler_X.transform(X_recent)

        # Start with the most recent sequence
        current_sequence = X_scaled[-self.sequence_length:]

        for _ in range(n_steps):
            # Reshape for prediction
            X_input = current_sequence.reshape(1, self.sequence_length, self.n_features)

            # Predict next value
            pred_scaled = self.model.predict(X_input, verbose=0)
            pred = self.scaler_y.inverse_transform(pred_scaled).flatten()[0]
            predictions.append(pred)

            # Calculate confidence if requested
            if return_confidence:
                # Monte Carlo for confidence
                mc_preds = []
                for _ in range(50):
                    mc_pred = self.model(X_input, training=True)
                    mc_pred_inv = self.scaler_y.inverse_transform(mc_pred.numpy()).flatten()[0]
                    mc_preds.append(mc_pred_inv)

                lower_bounds.append(np.percentile(mc_preds, 5))
                upper_bounds.append(np.percentile(mc_preds, 95))

            # Update sequence (simplified - using last feature values as proxy)
            # In a real scenario, you'd need to update all features appropriately
            next_features = current_sequence[-1].copy()
            current_sequence = np.vstack([current_sequence[1:], next_features])

        predictions = np.array(predictions)
        lower_bounds = np.array(lower_bounds) if return_confidence else None
        upper_bounds = np.array(upper_bounds) if return_confidence else None

        return predictions, lower_bounds, upper_bounds

    def save(self, model_dir: str, model_name: str = "lstm_model"):
        """
        Save the trained model and scalers

        Args:
            model_dir: Directory to save model
            model_name: Name for the model files
        """
        if not self.is_trained or self.model is None:
            raise ValueError("Model must be trained before saving")

        model_path = Path(model_dir)
        model_path.mkdir(parents=True, exist_ok=True)

        # Save Keras model
        self.model.save(model_path / f"{model_name}.keras")

        # Save scalers
        joblib.dump(self.scaler_X, model_path / f"{model_name}_scaler_X.pkl")
        joblib.dump(self.scaler_y, model_path / f"{model_name}_scaler_y.pkl")

        # Save configuration
        config = {
            'sequence_length': self.sequence_length,
            'n_features': self.n_features,
            'lstm_units': self.lstm_units,
            'dropout_rate': self.dropout_rate,
            'learning_rate': self.learning_rate
        }
        joblib.dump(config, model_path / f"{model_name}_config.pkl")

        logger.info(f"LSTM model saved to {model_path}")

    def load(self, model_dir: str, model_name: str = "lstm_model"):
        """
        Load a trained model and scalers

        Args:
            model_dir: Directory containing the model
            model_name: Name of the model files
        """
        model_path = Path(model_dir)

        # Load configuration
        config = joblib.load(model_path / f"{model_name}_config.pkl")
        self.sequence_length = config['sequence_length']
        self.n_features = config['n_features']
        self.lstm_units = config['lstm_units']
        self.dropout_rate = config['dropout_rate']
        self.learning_rate = config['learning_rate']

        # Load Keras model
        self.model = load_model(model_path / f"{model_name}.keras")

        # Load scalers
        self.scaler_X = joblib.load(model_path / f"{model_name}_scaler_X.pkl")
        self.scaler_y = joblib.load(model_path / f"{model_name}_scaler_y.pkl")

        self.is_trained = True
        logger.info(f"LSTM model loaded from {model_path}")
