"""
Gradient Boosting Models for Price Forecasting
Implements XGBoost and LightGBM for price prediction
"""

import numpy as np
import pandas as pd
from typing import Tuple, Optional, Dict, Any, List, Literal
import logging
from pathlib import Path

import xgboost as xgb
import lightgbm as lgb
from sklearn.preprocessing import StandardScaler
import joblib

logger = logging.getLogger(__name__)


class GradientBoostingPricePredictor:
    """
    Gradient Boosting-based price forecasting model
    Supports both XGBoost and LightGBM
    """

    def __init__(
        self,
        model_type: Literal['xgboost', 'lightgbm'] = 'xgboost',
        n_estimators: int = 300,
        learning_rate: float = 0.05,
        max_depth: int = 6,
        min_child_weight: int = 1,
        subsample: float = 0.8,
        colsample_bytree: float = 0.8,
        random_state: int = 42,
        n_jobs: int = -1
    ):
        """
        Initialize Gradient Boosting predictor

        Args:
            model_type: Type of model ('xgboost' or 'lightgbm')
            n_estimators: Number of boosting rounds
            learning_rate: Learning rate
            max_depth: Maximum tree depth
            min_child_weight: Minimum sum of instance weight in a child
            subsample: Subsample ratio of training instances
            colsample_bytree: Subsample ratio of columns when constructing each tree
            random_state: Random seed
            n_jobs: Number of parallel jobs
        """
        self.model_type = model_type
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_child_weight = min_child_weight
        self.subsample = subsample
        self.colsample_bytree = colsample_bytree
        self.random_state = random_state
        self.n_jobs = n_jobs

        self.model: Optional[Any] = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names: List[str] = []
        self.feature_importance: Optional[pd.DataFrame] = None

    def train(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: Optional[pd.DataFrame] = None,
        y_val: Optional[pd.Series] = None,
        scale_features: bool = True,
        early_stopping_rounds: int = 50,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Train the Gradient Boosting model

        Args:
            X_train: Training features
            y_train: Training targets
            X_val: Validation features (optional)
            y_val: Validation targets (optional)
            scale_features: Whether to scale features
            early_stopping_rounds: Early stopping patience
            verbose: Whether to print training progress

        Returns:
            Training metrics dictionary
        """
        logger.info(f"Starting {self.model_type.upper()} model training")

        # Store feature names
        self.feature_names = list(X_train.columns)

        # Scale features if requested
        if scale_features:
            X_train_processed = self.scaler.fit_transform(X_train)
            if X_val is not None:
                X_val_processed = self.scaler.transform(X_val)
        else:
            X_train_processed = X_train.values
            X_val_processed = X_val.values if X_val is not None else None

        # Train based on model type
        if self.model_type == 'xgboost':
            train_result = self._train_xgboost(
                X_train_processed, y_train,
                X_val_processed, y_val,
                early_stopping_rounds, verbose
            )
        else:  # lightgbm
            train_result = self._train_lightgbm(
                X_train_processed, y_train,
                X_val_processed, y_val,
                early_stopping_rounds, verbose
            )

        # Calculate feature importance
        self._calculate_feature_importance()

        self.is_trained = True
        logger.info(f"{self.model_type.upper()} training complete")

        return train_result

    def _train_xgboost(
        self,
        X_train: np.ndarray,
        y_train: pd.Series,
        X_val: Optional[np.ndarray],
        y_val: Optional[pd.Series],
        early_stopping_rounds: int,
        verbose: bool
    ) -> Dict[str, Any]:
        """Train XGBoost model"""
        # Prepare data
        dtrain = xgb.DMatrix(X_train, label=y_train, feature_names=self.feature_names)

        # Parameters
        params = {
            'objective': 'reg:squarederror',
            'learning_rate': self.learning_rate,
            'max_depth': self.max_depth,
            'min_child_weight': self.min_child_weight,
            'subsample': self.subsample,
            'colsample_bytree': self.colsample_bytree,
            'seed': self.random_state,
            'nthread': self.n_jobs if self.n_jobs > 0 else -1,
            'eval_metric': 'rmse'
        }

        # Evaluation list
        evallist = [(dtrain, 'train')]
        if X_val is not None and y_val is not None:
            dval = xgb.DMatrix(X_val, label=y_val, feature_names=self.feature_names)
            evallist.append((dval, 'val'))

        # Train model
        evals_result = {}
        self.model = xgb.train(
            params,
            dtrain,
            num_boost_round=self.n_estimators,
            evals=evallist,
            early_stopping_rounds=early_stopping_rounds if X_val is not None else None,
            evals_result=evals_result,
            verbose_eval=10 if verbose else False
        )

        # Calculate metrics
        train_predictions = self.model.predict(dtrain)
        train_mae = np.mean(np.abs(y_train - train_predictions))
        train_rmse = np.sqrt(np.mean((y_train - train_predictions) ** 2))

        result = {
            'mae': train_mae,
            'rmse': train_rmse,
            'n_features': len(self.feature_names),
            'n_samples': len(X_train),
            'best_iteration': self.model.best_iteration if hasattr(self.model, 'best_iteration') else self.n_estimators
        }

        if X_val is not None:
            val_predictions = self.model.predict(dval)
            val_mae = np.mean(np.abs(y_val - val_predictions))
            val_rmse = np.sqrt(np.mean((y_val - val_predictions) ** 2))
            result['val_mae'] = val_mae
            result['val_rmse'] = val_rmse

        return result

    def _train_lightgbm(
        self,
        X_train: np.ndarray,
        y_train: pd.Series,
        X_val: Optional[np.ndarray],
        y_val: Optional[pd.Series],
        early_stopping_rounds: int,
        verbose: bool
    ) -> Dict[str, Any]:
        """Train LightGBM model"""
        # Prepare data
        train_data = lgb.Dataset(X_train, label=y_train, feature_name=self.feature_names)

        # Parameters
        params = {
            'objective': 'regression',
            'metric': 'rmse',
            'learning_rate': self.learning_rate,
            'max_depth': self.max_depth,
            'min_child_weight': self.min_child_weight,
            'subsample': self.subsample,
            'colsample_bytree': self.colsample_bytree,
            'seed': self.random_state,
            'num_threads': self.n_jobs if self.n_jobs > 0 else -1,
            'verbose': -1
        }

        # Validation data
        valid_sets = [train_data]
        valid_names = ['train']
        if X_val is not None and y_val is not None:
            val_data = lgb.Dataset(X_val, label=y_val, feature_name=self.feature_names, reference=train_data)
            valid_sets.append(val_data)
            valid_names.append('val')

        # Callbacks
        callbacks = []
        if verbose:
            callbacks.append(lgb.log_evaluation(period=10))
        if X_val is not None:
            callbacks.append(lgb.early_stopping(stopping_rounds=early_stopping_rounds))

        # Train model
        self.model = lgb.train(
            params,
            train_data,
            num_boost_round=self.n_estimators,
            valid_sets=valid_sets,
            valid_names=valid_names,
            callbacks=callbacks
        )

        # Calculate metrics
        train_predictions = self.model.predict(X_train)
        train_mae = np.mean(np.abs(y_train - train_predictions))
        train_rmse = np.sqrt(np.mean((y_train - train_predictions) ** 2))

        result = {
            'mae': train_mae,
            'rmse': train_rmse,
            'n_features': len(self.feature_names),
            'n_samples': len(X_train),
            'best_iteration': self.model.best_iteration if hasattr(self.model, 'best_iteration') else self.n_estimators
        }

        if X_val is not None:
            val_predictions = self.model.predict(X_val)
            val_mae = np.mean(np.abs(y_val - val_predictions))
            val_rmse = np.sqrt(np.mean((y_val - val_predictions) ** 2))
            result['val_mae'] = val_mae
            result['val_rmse'] = val_rmse

        return result

    def predict(
        self,
        X: pd.DataFrame,
        return_confidence: bool = False
    ) -> Tuple[np.ndarray, Optional[np.ndarray], Optional[np.ndarray]]:
        """
        Make predictions with the Gradient Boosting model

        Args:
            X: Features to predict on
            return_confidence: Whether to return confidence intervals (approximate)

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
        if self.model_type == 'xgboost':
            dmatrix = xgb.DMatrix(X_processed, feature_names=self.feature_names)
            predictions = self.model.predict(dmatrix)
        else:  # lightgbm
            predictions = self.model.predict(X_processed)

        # Approximate confidence intervals (gradient boosting doesn't naturally provide them)
        lower_bound = None
        upper_bound = None

        if return_confidence:
            # Use prediction std based on residuals during training (simplified approach)
            # A more sophisticated approach would use quantile regression
            # For now, use a simple heuristic: ±1.5 * std of predictions
            std_estimate = np.std(predictions) * 0.3  # Conservative estimate
            lower_bound = predictions - 1.96 * std_estimate
            upper_bound = predictions + 1.96 * std_estimate

        return predictions, lower_bound, upper_bound

    def _calculate_feature_importance(self):
        """Calculate and store feature importance"""
        if self.model is None:
            return

        if self.model_type == 'xgboost':
            importance_dict = self.model.get_score(importance_type='weight')
            # Map feature names
            importance_data = []
            for fname, score in importance_dict.items():
                # XGBoost uses f0, f1, ... notation
                if fname.startswith('f'):
                    try:
                        idx = int(fname[1:])
                        if idx < len(self.feature_names):
                            importance_data.append({
                                'feature': self.feature_names[idx],
                                'importance': score
                            })
                    except ValueError:
                        pass
            importance_df = pd.DataFrame(importance_data)
        else:  # lightgbm
            importance_df = pd.DataFrame({
                'feature': self.feature_names,
                'importance': self.model.feature_importance(importance_type='gain')
            })

        importance_df = importance_df.sort_values('importance', ascending=False)
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

    def save(self, model_dir: str, model_name: str = "gradient_boosting_model"):
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

        # Save model (different format for XGBoost vs LightGBM)
        if self.model_type == 'xgboost':
            self.model.save_model(str(model_path / f"{model_name}.xgb"))
        else:  # lightgbm
            self.model.save_model(str(model_path / f"{model_name}.lgb"))

        # Save scaler
        joblib.dump(self.scaler, model_path / f"{model_name}_scaler.pkl")

        # Save configuration
        config = {
            'model_type': self.model_type,
            'n_estimators': self.n_estimators,
            'learning_rate': self.learning_rate,
            'max_depth': self.max_depth,
            'min_child_weight': self.min_child_weight,
            'subsample': self.subsample,
            'colsample_bytree': self.colsample_bytree,
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

        logger.info(f"{self.model_type.upper()} model saved to {model_path}")

    def load(self, model_dir: str, model_name: str = "gradient_boosting_model"):
        """
        Load a trained model and scaler

        Args:
            model_dir: Directory containing the model
            model_name: Name of the model files
        """
        model_path = Path(model_dir)

        # Load configuration
        config = joblib.load(model_path / f"{model_name}_config.pkl")
        self.model_type = config['model_type']
        self.n_estimators = config['n_estimators']
        self.learning_rate = config['learning_rate']
        self.max_depth = config['max_depth']
        self.min_child_weight = config['min_child_weight']
        self.subsample = config['subsample']
        self.colsample_bytree = config['colsample_bytree']
        self.random_state = config['random_state']
        self.feature_names = config['feature_names']

        # Load model (different format for XGBoost vs LightGBM)
        if self.model_type == 'xgboost':
            self.model = xgb.Booster()
            self.model.load_model(str(model_path / f"{model_name}.xgb"))
        else:  # lightgbm
            self.model = lgb.Booster(model_file=str(model_path / f"{model_name}.lgb"))

        # Load scaler
        self.scaler = joblib.load(model_path / f"{model_name}_scaler.pkl")

        # Load feature importance if exists
        importance_path = model_path / f"{model_name}_feature_importance.csv"
        if importance_path.exists():
            self.feature_importance = pd.read_csv(importance_path)

        self.is_trained = True
        logger.info(f"{self.model_type.upper()} model loaded from {model_path}")
