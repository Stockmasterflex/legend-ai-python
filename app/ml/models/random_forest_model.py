"""
Random Forest classifier for pattern detection.

Ensemble learning approach using multiple decision trees.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
from pathlib import Path
from datetime import datetime


class RandomForestPatternDetector:
    """Random Forest model for pattern detection."""

    def __init__(
        self,
        n_estimators: int = 200,
        max_depth: Optional[int] = 20,
        min_samples_split: int = 10,
        min_samples_leaf: int = 4,
        max_features: str = 'sqrt',
        class_weight: str = 'balanced',
        random_state: int = 42
    ):
        """
        Initialize Random Forest detector.

        Args:
            n_estimators: Number of trees in the forest
            max_depth: Maximum depth of trees
            min_samples_split: Minimum samples required to split
            min_samples_leaf: Minimum samples required at leaf
            max_features: Number of features for best split
            class_weight: Weights for imbalanced classes
            random_state: Random seed
        """
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            max_features=max_features,
            class_weight=class_weight,
            random_state=random_state,
            n_jobs=-1  # Use all CPU cores
        )
        self.scaler = StandardScaler()
        self.feature_names = []
        self.is_trained = False
        self.model_dir = Path('models/random_forest')
        self.model_dir.mkdir(parents=True, exist_ok=True)

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
        cv_folds: int = 5
    ) -> Dict:
        """
        Train the Random Forest model.

        Args:
            X_train: Training features
            y_train: Training labels
            feature_names: Names of features
            cv_folds: Number of cross-validation folds

        Returns:
            Dictionary with training metrics
        """
        # Store feature names
        self.feature_names = feature_names

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)

        # Perform cross-validation
        cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
        cv_scores = cross_val_score(
            self.model,
            X_train_scaled,
            y_train,
            cv=cv,
            scoring='f1',
            n_jobs=-1
        )

        # Train on full training set
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True

        # Get training predictions
        y_pred_train = self.model.predict(X_train_scaled)
        y_pred_proba_train = self.model.predict_proba(X_train_scaled)[:, 1]

        # Calculate metrics
        train_metrics = {
            'cv_scores': cv_scores.tolist(),
            'cv_mean': float(cv_scores.mean()),
            'cv_std': float(cv_scores.std()),
            'train_accuracy': float(self.model.score(X_train_scaled, y_train)),
            'train_auc': float(roc_auc_score(y_train, y_pred_proba_train)),
            'n_samples': len(X_train),
            'n_features': len(feature_names),
            'class_distribution': {
                'negative': int(np.sum(y_train == 0)),
                'positive': int(np.sum(y_train == 1))
            }
        }

        print(f"Random Forest Training Complete:")
        print(f"  CV F1 Score: {train_metrics['cv_mean']:.4f} (+/- {train_metrics['cv_std']:.4f})")
        print(f"  Training Accuracy: {train_metrics['train_accuracy']:.4f}")
        print(f"  Training AUC: {train_metrics['train_auc']:.4f}")

        return train_metrics

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
        return self.model.predict(X_scaled)

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
        return self.model.predict_proba(X_scaled)[:, 1]

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
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]

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

        print(f"\nRandom Forest Evaluation:")
        print(f"  Accuracy: {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall: {metrics['recall']:.4f}")
        print(f"  F1 Score: {metrics['f1']:.4f}")
        print(f"  AUC: {metrics['auc']:.4f}")

        return metrics

    def get_feature_importance(self, top_n: int = 20) -> pd.DataFrame:
        """
        Get feature importance scores.

        Args:
            top_n: Number of top features to return

        Returns:
            DataFrame with feature importance
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before getting feature importance")

        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        })

        importance_df = importance_df.sort_values('importance', ascending=False)
        return importance_df.head(top_n)

    def save(self, model_name: Optional[str] = None):
        """
        Save model to disk.

        Args:
            model_name: Optional model name (default: timestamp)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")

        if model_name is None:
            model_name = f"rf_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        model_path = self.model_dir / f"{model_name}.joblib"
        scaler_path = self.model_dir / f"{model_name}_scaler.joblib"
        metadata_path = self.model_dir / f"{model_name}_metadata.json"

        # Save model and scaler
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)

        # Save metadata
        import json
        metadata = {
            'feature_names': self.feature_names,
            'n_features': len(self.feature_names),
            'model_type': 'RandomForest',
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
        model_path = self.model_dir / f"{model_name}.joblib"
        scaler_path = self.model_dir / f"{model_name}_scaler.joblib"
        metadata_path = self.model_dir / f"{model_name}_metadata.json"

        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")

        # Load model and scaler
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)

        # Load metadata
        import json
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        self.feature_names = metadata['feature_names']
        self.is_trained = True

        print(f"Model loaded from {model_path}")
