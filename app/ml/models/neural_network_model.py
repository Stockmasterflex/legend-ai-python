"""
Neural Network for pattern detection.

Deep learning approach using TensorFlow/Keras.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, callbacks
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
from pathlib import Path
from datetime import datetime


class NeuralNetworkPatternDetector:
    """Neural Network model for pattern detection."""

    def __init__(
        self,
        hidden_layers: List[int] = [256, 128, 64, 32],
        dropout_rate: float = 0.3,
        learning_rate: float = 0.001,
        activation: str = 'relu',
        batch_norm: bool = True,
        random_state: int = 42
    ):
        """
        Initialize Neural Network detector.

        Args:
            hidden_layers: List of hidden layer sizes
            dropout_rate: Dropout rate for regularization
            learning_rate: Learning rate for optimizer
            activation: Activation function
            batch_norm: Whether to use batch normalization
            random_state: Random seed
        """
        self.hidden_layers = hidden_layers
        self.dropout_rate = dropout_rate
        self.learning_rate = learning_rate
        self.activation = activation
        self.batch_norm = batch_norm
        self.random_state = random_state

        # Set random seeds
        np.random.seed(random_state)
        tf.random.set_seed(random_state)

        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False
        self.model_dir = Path('models/neural_network')
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.training_history = None

    def _build_model(self, input_dim: int) -> keras.Model:
        """
        Build the neural network architecture.

        Args:
            input_dim: Number of input features

        Returns:
            Compiled Keras model
        """
        model = models.Sequential()

        # Input layer
        model.add(layers.Input(shape=(input_dim,)))

        # Hidden layers
        for i, units in enumerate(self.hidden_layers):
            model.add(layers.Dense(units, activation=self.activation))

            if self.batch_norm:
                model.add(layers.BatchNormalization())

            model.add(layers.Dropout(self.dropout_rate))

        # Output layer
        model.add(layers.Dense(1, activation='sigmoid'))

        # Compile model
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate),
            loss='binary_crossentropy',
            metrics=['accuracy', keras.metrics.AUC(name='auc')]
        )

        return model

    def prepare_data(
        self,
        patterns: List[Dict],
        feature_cols: Optional[List[str]] = None
    ) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        Prepare data for training.

        Args:
            patterns: List of labeled patterns with features
            feature_cols: Optional list of feature columns to use

        Returns:
            Tuple of (X, y, feature_names)
        """
        # Convert to DataFrame
        df = pd.DataFrame(patterns)

        # Extract features
        features_df = pd.DataFrame(df['features'].tolist())

        # Select features
        if feature_cols is not None:
            features_df = features_df[feature_cols]

        # Get labels
        y = df['label'].values

        # Convert to numpy arrays
        X = features_df.values
        feature_names = features_df.columns.tolist()

        # Handle NaN values
        X = np.nan_to_num(X, nan=0.0, posinf=1e10, neginf=-1e10)

        return X, y, feature_names

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        feature_names: List[str],
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
        epochs: int = 100,
        batch_size: int = 32,
        early_stopping_patience: int = 15,
        verbose: int = 1
    ) -> Dict:
        """
        Train the Neural Network model.

        Args:
            X_train: Training features
            y_train: Training labels
            feature_names: Names of features
            X_val: Validation features (optional)
            y_val: Validation labels (optional)
            epochs: Number of training epochs
            batch_size: Batch size for training
            early_stopping_patience: Patience for early stopping
            verbose: Verbosity level

        Returns:
            Dictionary with training metrics
        """
        # Store feature names
        self.feature_names = feature_names

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)

        # Prepare validation set
        validation_data = None
        if X_val is not None and y_val is not None:
            X_val_scaled = self.scaler.transform(X_val)
            validation_data = (X_val_scaled, y_val)

        # Build model
        self.model = self._build_model(input_dim=X_train_scaled.shape[1])

        # Callbacks
        callback_list = [
            callbacks.EarlyStopping(
                monitor='val_loss' if validation_data else 'loss',
                patience=early_stopping_patience,
                restore_best_weights=True,
                verbose=1
            ),
            callbacks.ReduceLROnPlateau(
                monitor='val_loss' if validation_data else 'loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            )
        ]

        # Train model
        history = self.model.fit(
            X_train_scaled,
            y_train,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callback_list,
            verbose=verbose,
            class_weight=self._compute_class_weights(y_train)
        )

        self.is_trained = True
        self.training_history = history.history

        # Get training predictions
        y_pred_proba_train = self.model.predict(X_train_scaled, verbose=0).flatten()
        y_pred_train = (y_pred_proba_train > 0.5).astype(int)

        # Calculate metrics
        train_metrics = {
            'final_train_loss': float(history.history['loss'][-1]),
            'final_train_accuracy': float(history.history['accuracy'][-1]),
            'final_train_auc': float(history.history['auc'][-1]),
            'train_auc': float(roc_auc_score(y_train, y_pred_proba_train)),
            'epochs_trained': len(history.history['loss']),
            'n_samples': len(X_train),
            'n_features': len(feature_names),
            'class_distribution': {
                'negative': int(np.sum(y_train == 0)),
                'positive': int(np.sum(y_train == 1))
            }
        }

        # Validation metrics
        if validation_data is not None:
            train_metrics['final_val_loss'] = float(history.history['val_loss'][-1])
            train_metrics['final_val_accuracy'] = float(history.history['val_accuracy'][-1])
            train_metrics['final_val_auc'] = float(history.history['val_auc'][-1])

            y_pred_proba_val = self.model.predict(X_val_scaled, verbose=0).flatten()
            train_metrics['val_auc'] = float(roc_auc_score(y_val, y_pred_proba_val))

        print(f"\nNeural Network Training Complete:")
        print(f"  Epochs Trained: {train_metrics['epochs_trained']}")
        print(f"  Training Accuracy: {train_metrics['final_train_accuracy']:.4f}")
        print(f"  Training AUC: {train_metrics['train_auc']:.4f}")

        if validation_data is not None:
            print(f"  Validation Accuracy: {train_metrics['final_val_accuracy']:.4f}")
            print(f"  Validation AUC: {train_metrics['val_auc']:.4f}")

        return train_metrics

    def _compute_class_weights(self, y: np.ndarray) -> Dict[int, float]:
        """Compute class weights for imbalanced data."""
        from sklearn.utils.class_weight import compute_class_weight

        classes = np.unique(y)
        weights = compute_class_weight('balanced', classes=classes, y=y)

        return {int(c): float(w) for c, w in zip(classes, weights)}

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict pattern labels.

        Args:
            X: Features to predict

        Returns:
            Array of predictions (0 or 1)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")

        X_scaled = self.scaler.transform(X)
        y_pred_proba = self.model.predict(X_scaled, verbose=0).flatten()
        return (y_pred_proba > 0.5).astype(int)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict pattern probabilities.

        Args:
            X: Features to predict

        Returns:
            Array of probabilities for positive class
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")

        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled, verbose=0).flatten()

    def evaluate(
        self,
        X_test: np.ndarray,
        y_test: np.ndarray
    ) -> Dict:
        """
        Evaluate model on test set.

        Args:
            X_test: Test features
            y_test: Test labels

        Returns:
            Dictionary with evaluation metrics
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")

        X_test_scaled = self.scaler.transform(X_test)

        # Predictions
        y_pred_proba = self.model.predict(X_test_scaled, verbose=0).flatten()
        y_pred = (y_pred_proba > 0.5).astype(int)

        # Metrics
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

        metrics = {
            'accuracy': float(accuracy_score(y_test, y_pred)),
            'precision': float(precision_score(y_test, y_pred, zero_division=0)),
            'recall': float(recall_score(y_test, y_pred, zero_division=0)),
            'f1': float(f1_score(y_test, y_pred, zero_division=0)),
            'auc': float(roc_auc_score(y_test, y_pred_proba)),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }

        print(f"\nNeural Network Evaluation:")
        print(f"  Accuracy: {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall: {metrics['recall']:.4f}")
        print(f"  F1 Score: {metrics['f1']:.4f}")
        print(f"  AUC: {metrics['auc']:.4f}")

        return metrics

    def save(self, model_name: Optional[str] = None):
        """
        Save model to disk.

        Args:
            model_name: Optional model name (default: timestamp)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")

        if model_name is None:
            model_name = f"nn_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        model_path = self.model_dir / model_name
        scaler_path = self.model_dir / f"{model_name}_scaler.joblib"
        metadata_path = self.model_dir / f"{model_name}_metadata.json"

        # Save model (Keras format)
        self.model.save(str(model_path))

        # Save scaler
        joblib.dump(self.scaler, scaler_path)

        # Save metadata
        import json
        metadata = {
            'feature_names': self.feature_names,
            'n_features': len(self.feature_names),
            'model_type': 'NeuralNetwork',
            'architecture': {
                'hidden_layers': self.hidden_layers,
                'dropout_rate': self.dropout_rate,
                'activation': self.activation,
                'batch_norm': self.batch_norm
            },
            'training_history': {k: [float(v) for v in vals] for k, vals in self.training_history.items()} if self.training_history else None,
            'saved_at': datetime.now().isoformat()
        }

        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"Model saved to {model_path}")

    def load(self, model_name: str):
        """
        Load model from disk.

        Args:
            model_name: Name of model to load
        """
        model_path = self.model_dir / model_name
        scaler_path = self.model_dir / f"{model_name}_scaler.joblib"
        metadata_path = self.model_dir / f"{model_name}_metadata.json"

        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")

        # Load model
        self.model = keras.models.load_model(str(model_path))

        # Load scaler
        self.scaler = joblib.load(scaler_path)

        # Load metadata
        import json
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        self.feature_names = metadata['feature_names']
        self.training_history = metadata.get('training_history')

        # Restore architecture params
        if 'architecture' in metadata:
            arch = metadata['architecture']
            self.hidden_layers = arch.get('hidden_layers', self.hidden_layers)
            self.dropout_rate = arch.get('dropout_rate', self.dropout_rate)
            self.activation = arch.get('activation', self.activation)
            self.batch_norm = arch.get('batch_norm', self.batch_norm)

        self.is_trained = True

        print(f"Model loaded from {model_path}")
