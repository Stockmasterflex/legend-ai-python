"""
Training pipeline for ML pattern detection models.

Handles data splitting, cross-validation, hyperparameter tuning, and model training.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional, Any
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import json
from pathlib import Path

from app.ml.models.random_forest_model import RandomForestPatternDetector
from app.ml.models.xgboost_model import XGBoostPatternDetector
from app.ml.models.neural_network_model import NeuralNetworkPatternDetector
from app.ml.models.ensemble_model import EnsemblePatternDetector
from app.ml.features.feature_engineering import FeatureEngineer


class TrainingPipeline:
    """Complete training pipeline for ML models."""

    def __init__(
        self,
        train_ratio: float = 0.7,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        random_state: int = 42
    ):
        """
        Initialize training pipeline.

        Args:
            train_ratio: Proportion of data for training
            val_ratio: Proportion of data for validation
            test_ratio: Proportion of data for testing
            random_state: Random seed for reproducibility
        """
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
        self.random_state = random_state

        self.feature_engineer = FeatureEngineer()
        self.results_dir = Path('results/training')
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def split_data(
        self,
        patterns: List[Dict]
    ) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """
        Split data into train, validation, and test sets.

        Args:
            patterns: List of labeled patterns

        Returns:
            Tuple of (train_patterns, val_patterns, test_patterns)
        """
        # Extract labels for stratification
        labels = [p['label'] for p in patterns]

        # First split: train+val vs test
        train_val_patterns, test_patterns = train_test_split(
            patterns,
            test_size=self.test_ratio,
            stratify=labels,
            random_state=self.random_state
        )

        # Second split: train vs val
        train_val_labels = [p['label'] for p in train_val_patterns]
        val_size = self.val_ratio / (self.train_ratio + self.val_ratio)

        train_patterns, val_patterns = train_test_split(
            train_val_patterns,
            test_size=val_size,
            stratify=train_val_labels,
            random_state=self.random_state
        )

        print(f"Data split:")
        print(f"  Training: {len(train_patterns)} samples ({self.train_ratio * 100:.0f}%)")
        print(f"  Validation: {len(val_patterns)} samples ({self.val_ratio * 100:.0f}%)")
        print(f"  Test: {len(test_patterns)} samples ({self.test_ratio * 100:.0f}%)")

        return train_patterns, val_patterns, test_patterns

    def prepare_features(
        self,
        patterns: List[Dict],
        feature_cols: Optional[List[str]] = None
    ) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """
        Prepare feature matrices from patterns.

        Args:
            patterns: List of patterns with features
            feature_cols: Optional list of feature columns

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

        # Convert to numpy
        X = features_df.values
        feature_names = features_df.columns.tolist()

        # Handle NaN values
        X = np.nan_to_num(X, nan=0.0, posinf=1e10, neginf=-1e10)

        return X, y, feature_names

    def cross_validate(
        self,
        model: Any,
        X: np.ndarray,
        y: np.ndarray,
        cv_folds: int = 5
    ) -> Dict:
        """
        Perform k-fold cross-validation.

        Args:
            model: Model to cross-validate
            X: Features
            y: Labels
            cv_folds: Number of folds

        Returns:
            Dictionary with CV results
        """
        from sklearn.model_selection import cross_validate

        cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=self.random_state)

        scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']

        cv_results = cross_validate(
            model,
            X,
            y,
            cv=cv,
            scoring=scoring,
            return_train_score=True,
            n_jobs=-1
        )

        # Aggregate results
        results = {
            'cv_folds': cv_folds,
            'metrics': {}
        }

        for metric in scoring:
            test_key = f'test_{metric}'
            train_key = f'train_{metric}'

            results['metrics'][metric] = {
                'test_mean': float(cv_results[test_key].mean()),
                'test_std': float(cv_results[test_key].std()),
                'train_mean': float(cv_results[train_key].mean()),
                'train_std': float(cv_results[train_key].std())
            }

        return results

    def tune_hyperparameters(
        self,
        model_type: str,
        X_train: np.ndarray,
        y_train: np.ndarray,
        search_method: str = 'random',
        n_iter: int = 20,
        cv_folds: int = 5
    ) -> Tuple[Any, Dict]:
        """
        Tune hyperparameters using grid search or random search.

        Args:
            model_type: Type of model ('rf', 'xgboost', 'nn')
            X_train: Training features
            y_train: Training labels
            search_method: 'grid' or 'random'
            n_iter: Number of iterations for random search
            cv_folds: Number of CV folds

        Returns:
            Tuple of (best_model, best_params)
        """
        print(f"\nTuning hyperparameters for {model_type}...")

        # Define parameter grids
        param_grids = {
            'rf': {
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 20, 30, None],
                'min_samples_split': [5, 10, 15],
                'min_samples_leaf': [2, 4, 8],
                'max_features': ['sqrt', 'log2']
            },
            'xgboost': {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 5, 7],
                'learning_rate': [0.01, 0.05, 0.1],
                'subsample': [0.7, 0.8, 0.9],
                'colsample_bytree': [0.7, 0.8, 0.9],
                'gamma': [0, 0.1, 0.2]
            }
        }

        if model_type not in param_grids:
            raise ValueError(f"Unknown model type: {model_type}")

        # Create base model
        if model_type == 'rf':
            from sklearn.ensemble import RandomForestClassifier
            base_model = RandomForestClassifier(random_state=self.random_state, n_jobs=-1)
        elif model_type == 'xgboost':
            import xgboost as xgb
            base_model = xgb.XGBClassifier(
                random_state=self.random_state,
                tree_method='hist',
                eval_metric='logloss',
                use_label_encoder=False,
                n_jobs=-1
            )

        # Perform search
        cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=self.random_state)

        if search_method == 'grid':
            search = GridSearchCV(
                base_model,
                param_grids[model_type],
                cv=cv,
                scoring='f1',
                n_jobs=-1,
                verbose=1
            )
        else:  # random search
            search = RandomizedSearchCV(
                base_model,
                param_grids[model_type],
                n_iter=n_iter,
                cv=cv,
                scoring='f1',
                n_jobs=-1,
                random_state=self.random_state,
                verbose=1
            )

        # Fit search
        search.fit(X_train, y_train)

        print(f"Best parameters: {search.best_params_}")
        print(f"Best CV F1 score: {search.best_score_:.4f}")

        return search.best_estimator_, search.best_params_

    def train_model(
        self,
        model_type: str,
        train_patterns: List[Dict],
        val_patterns: List[Dict],
        feature_cols: Optional[List[str]] = None,
        tune_hyperparameters: bool = False
    ) -> Tuple[Any, Dict]:
        """
        Train a single model.

        Args:
            model_type: Type of model ('rf', 'xgboost', 'nn', 'ensemble')
            train_patterns: Training patterns
            val_patterns: Validation patterns
            feature_cols: Optional feature columns to use
            tune_hyperparameters: Whether to tune hyperparameters

        Returns:
            Tuple of (trained_model, metrics)
        """
        print(f"\n{'=' * 80}")
        print(f"Training {model_type.upper()} Model")
        print(f"{'=' * 80}")

        # Prepare data
        X_train, y_train, feature_names = self.prepare_features(train_patterns, feature_cols)
        X_val, y_val, _ = self.prepare_features(val_patterns, feature_cols)

        # Initialize model
        if model_type == 'rf':
            model = RandomForestPatternDetector()
        elif model_type == 'xgboost':
            model = XGBoostPatternDetector()
        elif model_type == 'nn':
            model = NeuralNetworkPatternDetector()
        elif model_type == 'ensemble':
            model = EnsemblePatternDetector()
        else:
            raise ValueError(f"Unknown model type: {model_type}")

        # Hyperparameter tuning
        if tune_hyperparameters and model_type in ['rf', 'xgboost']:
            print("\nPerforming hyperparameter tuning...")
            best_model, best_params = self.tune_hyperparameters(
                model_type,
                X_train,
                y_train
            )

            # Update model with best parameters
            if model_type == 'rf':
                model.model = best_model
            elif model_type == 'xgboost':
                model.model = best_model

        # Train model
        if model_type == 'ensemble':
            metrics = model.train(
                X_train, y_train, feature_names,
                X_val=X_val, y_val=y_val,
                patterns_train=train_patterns,
                patterns_val=val_patterns
            )
        elif model_type in ['xgboost', 'nn']:
            metrics = model.train(
                X_train, y_train, feature_names,
                X_val=X_val, y_val=y_val
            )
        else:
            metrics = model.train(X_train, y_train, feature_names)

        return model, metrics

    def train_all_models(
        self,
        patterns: List[Dict],
        feature_cols: Optional[List[str]] = None,
        tune_hyperparameters: bool = False
    ) -> Dict[str, Tuple[Any, Dict]]:
        """
        Train all models (RF, XGBoost, NN, Ensemble).

        Args:
            patterns: All labeled patterns
            feature_cols: Optional feature columns
            tune_hyperparameters: Whether to tune hyperparameters

        Returns:
            Dictionary mapping model_type to (model, metrics)
        """
        # Split data
        train_patterns, val_patterns, test_patterns = self.split_data(patterns)

        # Store splits for later use
        self.train_patterns = train_patterns
        self.val_patterns = val_patterns
        self.test_patterns = test_patterns

        # Train all models
        results = {}

        for model_type in ['rf', 'xgboost', 'nn', 'ensemble']:
            model, metrics = self.train_model(
                model_type,
                train_patterns,
                val_patterns,
                feature_cols=feature_cols,
                tune_hyperparameters=tune_hyperparameters and model_type != 'ensemble'
            )

            results[model_type] = (model, metrics)

        # Save training results
        self._save_training_results(results)

        return results

    def evaluate_all_models(
        self,
        models: Dict[str, Tuple[Any, Dict]],
        test_patterns: Optional[List[Dict]] = None
    ) -> Dict[str, Dict]:
        """
        Evaluate all trained models on test set.

        Args:
            models: Dictionary of trained models
            test_patterns: Test patterns (uses stored if not provided)

        Returns:
            Dictionary of evaluation metrics for each model
        """
        if test_patterns is None:
            test_patterns = self.test_patterns

        if test_patterns is None:
            raise ValueError("No test data available")

        # Prepare test data
        X_test, y_test, _ = self.prepare_features(test_patterns)

        print(f"\n{'=' * 80}")
        print("Evaluating All Models on Test Set")
        print(f"{'=' * 80}")

        evaluation_results = {}

        for model_type, (model, _) in models.items():
            print(f"\n{model_type.upper()} Evaluation:")
            metrics = model.evaluate(X_test, y_test)
            evaluation_results[model_type] = metrics

        # Save evaluation results
        self._save_evaluation_results(evaluation_results)

        return evaluation_results

    def _save_training_results(self, results: Dict[str, Tuple[Any, Dict]]):
        """Save training results to disk."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = self.results_dir / f'training_results_{timestamp}.json'

        # Extract metrics only (models are saved separately)
        metrics_only = {
            model_type: metrics
            for model_type, (_, metrics) in results.items()
        }

        with open(results_file, 'w') as f:
            json.dump(metrics_only, f, indent=2)

        print(f"\nTraining results saved to {results_file}")

    def _save_evaluation_results(self, results: Dict[str, Dict]):
        """Save evaluation results to disk."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = self.results_dir / f'evaluation_results_{timestamp}.json'

        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\nEvaluation results saved to {results_file}")

    def compare_models(self, evaluation_results: Dict[str, Dict]) -> pd.DataFrame:
        """
        Compare performance of all models.

        Args:
            evaluation_results: Evaluation metrics for all models

        Returns:
            DataFrame with comparison
        """
        comparison_data = []

        for model_type, metrics in evaluation_results.items():
            comparison_data.append({
                'Model': model_type.upper(),
                'Accuracy': metrics['accuracy'],
                'Precision': metrics['precision'],
                'Recall': metrics['recall'],
                'F1 Score': metrics['f1'],
                'AUC': metrics['auc']
            })

        df = pd.DataFrame(comparison_data)
        df = df.sort_values('F1 Score', ascending=False)

        print("\nModel Comparison:")
        print(df.to_string(index=False))

        return df
