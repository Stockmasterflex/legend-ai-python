"""
Ensemble model combining Random Forest, XGBoost, and Neural Network.

Uses weighted voting or stacking for final predictions.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
from pathlib import Path
from datetime import datetime

from app.ml.models.random_forest_model import RandomForestPatternDetector
from app.ml.models.xgboost_model import XGBoostPatternDetector
from app.ml.models.neural_network_model import NeuralNetworkPatternDetector


class EnsemblePatternDetector:
    """Ensemble model combining multiple ML approaches."""

    def __init__(
        self,
        ensemble_method: str = 'weighted_voting',
        rf_weight: float = 0.33,
        xgb_weight: float = 0.34,
        nn_weight: float = 0.33,
        use_stacking: bool = False
    ):
        """
        Initialize Ensemble detector.

        Args:
            ensemble_method: Method for combining predictions ('weighted_voting' or 'stacking')
            rf_weight: Weight for Random Forest predictions
            xgb_weight: Weight for XGBoost predictions
            nn_weight: Weight for Neural Network predictions
            use_stacking: Whether to use meta-learner stacking
        """
        self.ensemble_method = ensemble_method
        self.rf_weight = rf_weight
        self.xgb_weight = xgb_weight
        self.nn_weight = nn_weight
        self.use_stacking = use_stacking

        # Initialize base models
        self.rf_model = RandomForestPatternDetector()
        self.xgb_model = XGBoostPatternDetector()
        self.nn_model = NeuralNetworkPatternDetector()

        # Meta-learner for stacking
        self.meta_learner = LogisticRegression() if use_stacking else None

        self.is_trained = False
        self.model_dir = Path('models/ensemble')
        self.model_dir.mkdir(parents=True, exist_ok=True)

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        feature_names: List[str],
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
        patterns_train: Optional[List[Dict]] = None,
        patterns_val: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Train all base models and ensemble.

        Args:
            X_train: Training features
            y_train: Training labels
            feature_names: Names of features
            X_val: Validation features (optional)
            y_val: Validation labels (optional)
            patterns_train: Training patterns with features (optional)
            patterns_val: Validation patterns with features (optional)

        Returns:
            Dictionary with training metrics for all models
        """
        print("=" * 80)
        print("Training Ensemble Model")
        print("=" * 80)

        metrics = {}

        # Train Random Forest
        print("\n[1/3] Training Random Forest...")
        rf_metrics = self.rf_model.train(X_train, y_train, feature_names)
        metrics['random_forest'] = rf_metrics

        # Train XGBoost
        print("\n[2/3] Training XGBoost...")
        xgb_metrics = self.xgb_model.train(
            X_train, y_train, feature_names,
            X_val=X_val, y_val=y_val
        )
        metrics['xgboost'] = xgb_metrics

        # Train Neural Network
        print("\n[3/3] Training Neural Network...")
        nn_metrics = self.nn_model.train(
            X_train, y_train, feature_names,
            X_val=X_val, y_val=y_val,
            verbose=0
        )
        metrics['neural_network'] = nn_metrics

        # Train meta-learner if using stacking
        if self.use_stacking and self.meta_learner is not None:
            print("\n[Meta] Training Meta-Learner for Stacking...")
            meta_features_train = self._get_base_predictions(X_train)

            self.meta_learner.fit(meta_features_train, y_train)

            # Evaluate meta-learner
            if X_val is not None and y_val is not None:
                meta_features_val = self._get_base_predictions(X_val)
                meta_pred = self.meta_learner.predict(meta_features_val)

                from sklearn.metrics import accuracy_score, f1_score
                meta_accuracy = accuracy_score(y_val, meta_pred)
                meta_f1 = f1_score(y_val, meta_pred, zero_division=0)

                print(f"  Meta-Learner Validation Accuracy: {meta_accuracy:.4f}")
                print(f"  Meta-Learner Validation F1: {meta_f1:.4f}")

                metrics['meta_learner'] = {
                    'val_accuracy': float(meta_accuracy),
                    'val_f1': float(meta_f1)
                }

        self.is_trained = True

        # Evaluate ensemble
        if X_val is not None and y_val is not None:
            print("\n[Ensemble] Evaluating Ensemble Model...")
            ensemble_metrics = self.evaluate(X_val, y_val)
            metrics['ensemble'] = ensemble_metrics

        print("\n" + "=" * 80)
        print("Ensemble Training Complete")
        print("=" * 80)

        return metrics

    def _get_base_predictions(self, X: np.ndarray) -> np.ndarray:
        """
        Get predictions from all base models.

        Args:
            X: Features

        Returns:
            Array of shape (n_samples, 3) with base model predictions
        """
        rf_pred = self.rf_model.predict_proba(X)
        xgb_pred = self.xgb_model.predict_proba(X)
        nn_pred = self.nn_model.predict_proba(X)

        return np.column_stack([rf_pred, xgb_pred, nn_pred])

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict pattern labels using ensemble.

        Args:
            X: Features to predict

        Returns:
            Array of predictions (0 or 1)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")

        proba = self.predict_proba(X)
        return (proba > 0.5).astype(int)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict pattern probabilities using ensemble.

        Args:
            X: Features to predict

        Returns:
            Array of probabilities for positive class
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")

        if self.use_stacking and self.meta_learner is not None:
            # Use meta-learner predictions
            meta_features = self._get_base_predictions(X)
            return self.meta_learner.predict_proba(meta_features)[:, 1]
        else:
            # Use weighted voting
            rf_pred = self.rf_model.predict_proba(X)
            xgb_pred = self.xgb_model.predict_proba(X)
            nn_pred = self.nn_model.predict_proba(X)

            # Weighted average
            ensemble_pred = (
                self.rf_weight * rf_pred +
                self.xgb_weight * xgb_pred +
                self.nn_weight * nn_pred
            )

            return ensemble_pred

    def predict_with_details(self, X: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Predict with detailed breakdown from each model.

        Args:
            X: Features to predict

        Returns:
            Dictionary with predictions from each model and ensemble
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")

        rf_pred = self.rf_model.predict_proba(X)
        xgb_pred = self.xgb_model.predict_proba(X)
        nn_pred = self.nn_model.predict_proba(X)
        ensemble_pred = self.predict_proba(X)

        return {
            'random_forest': rf_pred,
            'xgboost': xgb_pred,
            'neural_network': nn_pred,
            'ensemble': ensemble_pred,
            'ensemble_labels': (ensemble_pred > 0.5).astype(int)
        }

    def evaluate(
        self,
        X_test: np.ndarray,
        y_test: np.ndarray,
        show_individual: bool = False
    ) -> Dict:
        """
        Evaluate ensemble model on test set.

        Args:
            X_test: Test features
            y_test: Test labels
            show_individual: Whether to show individual model metrics

        Returns:
            Dictionary with evaluation metrics
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")

        # Get predictions from all models
        predictions = self.predict_with_details(X_test)

        # Evaluate ensemble
        y_pred = predictions['ensemble_labels']
        y_pred_proba = predictions['ensemble']

        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

        metrics = {
            'accuracy': float(accuracy_score(y_test, y_pred)),
            'precision': float(precision_score(y_test, y_pred, zero_division=0)),
            'recall': float(recall_score(y_test, y_pred, zero_division=0)),
            'f1': float(f1_score(y_test, y_pred, zero_division=0)),
            'auc': float(roc_auc_score(y_test, y_pred_proba)),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }

        print(f"\nEnsemble Model Evaluation:")
        print(f"  Accuracy: {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall: {metrics['recall']:.4f}")
        print(f"  F1 Score: {metrics['f1']:.4f}")
        print(f"  AUC: {metrics['auc']:.4f}")

        # Individual model metrics
        if show_individual:
            print("\nIndividual Model Performance:")

            for model_name in ['random_forest', 'xgboost', 'neural_network']:
                y_pred_model = (predictions[model_name] > 0.5).astype(int)
                acc = accuracy_score(y_test, y_pred_model)
                f1 = f1_score(y_test, y_pred_model, zero_division=0)
                auc = roc_auc_score(y_test, predictions[model_name])

                print(f"  {model_name.title()}: Acc={acc:.4f}, F1={f1:.4f}, AUC={auc:.4f}")

                metrics[f'{model_name}_accuracy'] = float(acc)
                metrics[f'{model_name}_f1'] = float(f1)
                metrics[f'{model_name}_auc'] = float(auc)

        return metrics

    def get_feature_importance(self, top_n: int = 20) -> Dict[str, pd.DataFrame]:
        """
        Get feature importance from each model.

        Args:
            top_n: Number of top features to return

        Returns:
            Dictionary with feature importance from each model
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before getting feature importance")

        importance = {}

        # Random Forest importance
        importance['random_forest'] = self.rf_model.get_feature_importance(top_n)

        # XGBoost importance
        importance['xgboost'] = self.xgb_model.get_feature_importance(top_n=top_n)

        # Aggregate importance
        all_features = {}

        for model_name, df in importance.items():
            for _, row in df.iterrows():
                feature = row['feature'] if 'feature' in row else row.name
                imp = row['importance']

                if feature not in all_features:
                    all_features[feature] = []
                all_features[feature].append(imp)

        # Average importance across models
        avg_importance = {
            feature: np.mean(imps) for feature, imps in all_features.items()
        }

        importance['ensemble'] = pd.DataFrame({
            'feature': list(avg_importance.keys()),
            'importance': list(avg_importance.values())
        }).sort_values('importance', ascending=False).head(top_n)

        return importance

    def save(self, model_name: Optional[str] = None):
        """
        Save ensemble model to disk.

        Args:
            model_name: Optional model name (default: timestamp)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")

        if model_name is None:
            model_name = f"ensemble_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Save base models
        self.rf_model.save(f"{model_name}_rf")
        self.xgb_model.save(f"{model_name}_xgb")
        self.nn_model.save(f"{model_name}_nn")

        # Save meta-learner if using stacking
        if self.use_stacking and self.meta_learner is not None:
            meta_path = self.model_dir / f"{model_name}_meta.joblib"
            joblib.dump(self.meta_learner, meta_path)

        # Save ensemble metadata
        import json
        metadata_path = self.model_dir / f"{model_name}_metadata.json"

        metadata = {
            'model_type': 'Ensemble',
            'ensemble_method': self.ensemble_method,
            'weights': {
                'random_forest': self.rf_weight,
                'xgboost': self.xgb_weight,
                'neural_network': self.nn_weight
            },
            'use_stacking': self.use_stacking,
            'base_models': {
                'random_forest': f"{model_name}_rf",
                'xgboost': f"{model_name}_xgb",
                'neural_network': f"{model_name}_nn"
            },
            'saved_at': datetime.now().isoformat()
        }

        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"Ensemble model saved with prefix: {model_name}")

    def load(self, model_name: str):
        """
        Load ensemble model from disk.

        Args:
            model_name: Name of ensemble model to load
        """
        metadata_path = self.model_dir / f"{model_name}_metadata.json"

        if not metadata_path.exists():
            raise FileNotFoundError(f"Ensemble metadata not found: {metadata_path}")

        # Load metadata
        import json
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        # Load base models
        self.rf_model.load(metadata['base_models']['random_forest'])
        self.xgb_model.load(metadata['base_models']['xgboost'])
        self.nn_model.load(metadata['base_models']['neural_network'])

        # Load ensemble parameters
        self.ensemble_method = metadata['ensemble_method']
        self.rf_weight = metadata['weights']['random_forest']
        self.xgb_weight = metadata['weights']['xgboost']
        self.nn_weight = metadata['weights']['neural_network']
        self.use_stacking = metadata['use_stacking']

        # Load meta-learner if exists
        if self.use_stacking:
            meta_path = self.model_dir / f"{model_name}_meta.joblib"
            if meta_path.exists():
                self.meta_learner = joblib.load(meta_path)

        self.is_trained = True

        print(f"Ensemble model loaded: {model_name}")
