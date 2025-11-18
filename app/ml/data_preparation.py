"""
Data Preparation Module

Provides tools for data cleaning, feature selection, and train/test splitting.
"""

from typing import Dict, List, Optional, Tuple, Union
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold, TimeSeriesSplit
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, LabelEncoder
from sklearn.feature_selection import (
    mutual_info_classif,
    mutual_info_regression,
    SelectKBest,
    RFE,
    f_classif,
    f_regression,
)
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from scipy import stats
import logging

logger = logging.getLogger(__name__)


class DataPreparation:
    """Comprehensive data preparation toolkit for ML training"""

    def __init__(self):
        self.scaler: Optional[Union[StandardScaler, MinMaxScaler, RobustScaler]] = None
        self.label_encoders: Dict[str, LabelEncoder] = {}
        self.feature_importance: Optional[pd.Series] = None
        self.selected_features: Optional[List[str]] = None

    def clean_data(
        self,
        df: pd.DataFrame,
        missing_strategy: str = "mean",
        outlier_method: str = "iqr",
        outlier_threshold: float = 3.0,
    ) -> pd.DataFrame:
        """
        Clean data by handling missing values and outliers

        Args:
            df: Input DataFrame
            missing_strategy: Strategy for handling missing values
                - 'mean': Fill with column mean
                - 'median': Fill with column median
                - 'mode': Fill with column mode
                - 'drop': Drop rows with missing values
                - 'forward_fill': Forward fill missing values
                - 'backward_fill': Backward fill missing values
            outlier_method: Method for detecting outliers
                - 'iqr': Interquartile range method
                - 'zscore': Z-score method
                - 'none': No outlier detection
            outlier_threshold: Threshold for outlier detection

        Returns:
            Cleaned DataFrame
        """
        df_clean = df.copy()

        # Handle missing values
        if missing_strategy == "drop":
            df_clean = df_clean.dropna()
            logger.info(f"Dropped {len(df) - len(df_clean)} rows with missing values")
        elif missing_strategy == "mean":
            numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
            df_clean[numeric_cols] = df_clean[numeric_cols].fillna(
                df_clean[numeric_cols].mean()
            )
        elif missing_strategy == "median":
            numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
            df_clean[numeric_cols] = df_clean[numeric_cols].fillna(
                df_clean[numeric_cols].median()
            )
        elif missing_strategy == "mode":
            for col in df_clean.columns:
                if df_clean[col].isna().any():
                    df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
        elif missing_strategy == "forward_fill":
            df_clean = df_clean.fillna(method="ffill")
        elif missing_strategy == "backward_fill":
            df_clean = df_clean.fillna(method="bfill")

        # Handle outliers
        if outlier_method != "none":
            numeric_cols = df_clean.select_dtypes(include=[np.number]).columns

            for col in numeric_cols:
                if outlier_method == "iqr":
                    Q1 = df_clean[col].quantile(0.25)
                    Q3 = df_clean[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - outlier_threshold * IQR
                    upper_bound = Q3 + outlier_threshold * IQR
                    outliers = (df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)
                elif outlier_method == "zscore":
                    z_scores = np.abs(stats.zscore(df_clean[col].dropna()))
                    outliers = z_scores > outlier_threshold

                # Cap outliers instead of removing them
                if outlier_method == "iqr":
                    df_clean.loc[df_clean[col] < lower_bound, col] = lower_bound
                    df_clean.loc[df_clean[col] > upper_bound, col] = upper_bound

        logger.info(f"Data cleaning complete. Shape: {df_clean.shape}")
        return df_clean

    def select_features(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        method: str = "correlation",
        n_features: Optional[int] = None,
        task_type: str = "classification",
        threshold: float = 0.1,
    ) -> Tuple[pd.DataFrame, List[str]]:
        """
        Select features using various methods

        Args:
            X: Feature DataFrame
            y: Target variable
            method: Feature selection method
                - 'correlation': Correlation-based selection
                - 'mutual_info': Mutual information
                - 'rfe': Recursive Feature Elimination
                - 'tree_importance': Tree-based feature importance
                - 'statistical': Statistical tests (f_classif/f_regression)
            n_features: Number of features to select (if None, uses threshold)
            task_type: 'classification' or 'regression'
            threshold: Minimum importance threshold

        Returns:
            Tuple of (selected features DataFrame, list of selected feature names)
        """
        logger.info(f"Starting feature selection using method: {method}")

        if method == "correlation":
            # Calculate correlation with target
            correlations = X.corrwith(y).abs().sort_values(ascending=False)

            if n_features:
                selected = correlations.head(n_features).index.tolist()
            else:
                selected = correlations[correlations >= threshold].index.tolist()

            self.feature_importance = correlations

        elif method == "mutual_info":
            # Mutual information
            if task_type == "classification":
                mi_scores = mutual_info_classif(X, y)
            else:
                mi_scores = mutual_info_regression(X, y)

            mi_scores = pd.Series(mi_scores, index=X.columns).sort_values(ascending=False)

            if n_features:
                selected = mi_scores.head(n_features).index.tolist()
            else:
                selected = mi_scores[mi_scores >= threshold].index.tolist()

            self.feature_importance = mi_scores

        elif method == "rfe":
            # Recursive Feature Elimination
            if task_type == "classification":
                estimator = RandomForestClassifier(n_estimators=100, random_state=42)
            else:
                estimator = RandomForestRegressor(n_estimators=100, random_state=42)

            n_features_to_select = n_features if n_features else max(1, int(len(X.columns) * 0.5))
            selector = RFE(estimator, n_features_to_select=n_features_to_select)
            selector.fit(X, y)

            selected = X.columns[selector.support_].tolist()
            rankings = pd.Series(selector.ranking_, index=X.columns)
            self.feature_importance = 1 / rankings  # Inverse ranking

        elif method == "tree_importance":
            # Tree-based feature importance
            if task_type == "classification":
                model = RandomForestClassifier(n_estimators=100, random_state=42)
            else:
                model = RandomForestRegressor(n_estimators=100, random_state=42)

            model.fit(X, y)
            importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)

            if n_features:
                selected = importances.head(n_features).index.tolist()
            else:
                selected = importances[importances >= threshold].index.tolist()

            self.feature_importance = importances

        elif method == "statistical":
            # Statistical tests
            if task_type == "classification":
                selector = SelectKBest(f_classif, k=n_features if n_features else "all")
            else:
                selector = SelectKBest(f_regression, k=n_features if n_features else "all")

            selector.fit(X, y)
            scores = pd.Series(selector.scores_, index=X.columns).sort_values(ascending=False)

            if n_features:
                selected = scores.head(n_features).index.tolist()
            else:
                selected = scores[scores >= threshold].index.tolist()

            self.feature_importance = scores

        else:
            raise ValueError(f"Unknown feature selection method: {method}")

        self.selected_features = selected
        logger.info(f"Selected {len(selected)} features: {selected}")

        return X[selected], selected

    def scale_features(
        self,
        X: pd.DataFrame,
        method: str = "standard",
        fit: bool = True,
    ) -> pd.DataFrame:
        """
        Scale features using various methods

        Args:
            X: Feature DataFrame
            method: Scaling method
                - 'standard': StandardScaler (z-score normalization)
                - 'minmax': MinMaxScaler (0-1 normalization)
                - 'robust': RobustScaler (robust to outliers)
            fit: Whether to fit the scaler (True for training, False for test)

        Returns:
            Scaled DataFrame
        """
        if fit or self.scaler is None:
            if method == "standard":
                self.scaler = StandardScaler()
            elif method == "minmax":
                self.scaler = MinMaxScaler()
            elif method == "robust":
                self.scaler = RobustScaler()
            else:
                raise ValueError(f"Unknown scaling method: {method}")

            scaled_data = self.scaler.fit_transform(X)
        else:
            scaled_data = self.scaler.transform(X)

        return pd.DataFrame(scaled_data, columns=X.columns, index=X.index)

    def encode_categorical(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        method: str = "label",
    ) -> pd.DataFrame:
        """
        Encode categorical variables

        Args:
            df: Input DataFrame
            columns: List of columns to encode (if None, auto-detect)
            method: Encoding method
                - 'label': Label encoding
                - 'onehot': One-hot encoding

        Returns:
            DataFrame with encoded categorical variables
        """
        df_encoded = df.copy()

        if columns is None:
            columns = df_encoded.select_dtypes(include=["object", "category"]).columns.tolist()

        if method == "label":
            for col in columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    df_encoded[col] = self.label_encoders[col].fit_transform(df_encoded[col].astype(str))
                else:
                    df_encoded[col] = self.label_encoders[col].transform(df_encoded[col].astype(str))

        elif method == "onehot":
            df_encoded = pd.get_dummies(df_encoded, columns=columns, drop_first=True)

        return df_encoded

    def split_data(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        test_size: float = 0.2,
        validation_size: Optional[float] = None,
        stratify: bool = False,
        random_state: int = 42,
    ) -> Union[
        Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series],
        Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]
    ]:
        """
        Split data into train/test or train/validation/test sets

        Args:
            X: Features
            y: Target
            test_size: Proportion of test set
            validation_size: Proportion of validation set (if None, no validation set)
            stratify: Whether to stratify split based on target
            random_state: Random seed

        Returns:
            Tuple of (X_train, X_test, y_train, y_test) or
            (X_train, X_val, X_test, y_train, y_val, y_test)
        """
        stratify_param = y if stratify else None

        if validation_size is None:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, stratify=stratify_param, random_state=random_state
            )
            logger.info(f"Split data: train={len(X_train)}, test={len(X_test)}")
            return X_train, X_test, y_train, y_test
        else:
            # First split: train+val vs test
            X_temp, X_test, y_temp, y_test = train_test_split(
                X, y, test_size=test_size, stratify=stratify_param, random_state=random_state
            )

            # Second split: train vs val
            val_ratio = validation_size / (1 - test_size)
            stratify_param_temp = y_temp if stratify else None
            X_train, X_val, y_train, y_val = train_test_split(
                X_temp, y_temp, test_size=val_ratio, stratify=stratify_param_temp, random_state=random_state
            )

            logger.info(f"Split data: train={len(X_train)}, val={len(X_val)}, test={len(X_test)}")
            return X_train, X_val, X_test, y_train, y_val, y_test

    def setup_cross_validation(
        self,
        n_splits: int = 5,
        cv_type: str = "kfold",
        shuffle: bool = True,
        random_state: int = 42,
    ):
        """
        Setup cross-validation strategy

        Args:
            n_splits: Number of folds
            cv_type: Type of cross-validation
                - 'kfold': K-Fold CV
                - 'stratified': Stratified K-Fold CV
                - 'timeseries': Time Series Split
            shuffle: Whether to shuffle data (not applicable for timeseries)
            random_state: Random seed

        Returns:
            Cross-validation splitter object
        """
        if cv_type == "kfold":
            cv = KFold(n_splits=n_splits, shuffle=shuffle, random_state=random_state)
        elif cv_type == "stratified":
            cv = StratifiedKFold(n_splits=n_splits, shuffle=shuffle, random_state=random_state)
        elif cv_type == "timeseries":
            cv = TimeSeriesSplit(n_splits=n_splits)
        else:
            raise ValueError(f"Unknown CV type: {cv_type}")

        logger.info(f"Setup {cv_type} cross-validation with {n_splits} splits")
        return cv

    def get_feature_importance_report(self) -> Optional[pd.DataFrame]:
        """
        Get feature importance report from last feature selection

        Returns:
            DataFrame with feature names and importance scores
        """
        if self.feature_importance is None:
            return None

        report = pd.DataFrame({
            "feature": self.feature_importance.index,
            "importance": self.feature_importance.values,
        }).sort_values("importance", ascending=False)

        return report
