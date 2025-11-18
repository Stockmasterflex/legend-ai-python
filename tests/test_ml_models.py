"""
Comprehensive tests for ML pattern detection models.

Tests feature engineering, model training, prediction, and backtesting.
"""

import pytest
import numpy as np
import pandas as pd
from typing import List, Dict

from app.ml.features.feature_engineering import FeatureEngineer
from app.ml.models.random_forest_model import RandomForestPatternDetector
from app.ml.models.xgboost_model import XGBoostPatternDetector
from app.ml.models.neural_network_model import NeuralNetworkPatternDetector
from app.ml.models.ensemble_model import EnsemblePatternDetector
from app.ml.training.training_pipeline import TrainingPipeline
from app.ml.evaluation.backtesting import Backtester, ModelComparator


# Test Fixtures

@pytest.fixture
def sample_ohlcv_data():
    """Generate sample OHLCV data for testing."""
    np.random.seed(42)
    n_samples = 200

    dates = pd.date_range(start='2020-01-01', periods=n_samples, freq='D')
    close_prices = 100 + np.cumsum(np.random.randn(n_samples) * 2)

    df = pd.DataFrame({
        'datetime': dates,
        'open': close_prices + np.random.randn(n_samples) * 0.5,
        'high': close_prices + np.abs(np.random.randn(n_samples)) * 1.5,
        'low': close_prices - np.abs(np.random.randn(n_samples)) * 1.5,
        'close': close_prices,
        'volume': np.random.randint(1000000, 10000000, n_samples)
    })

    return df


@pytest.fixture
def sample_labeled_patterns():
    """Generate sample labeled patterns for testing."""
    np.random.seed(42)

    patterns = []
    for i in range(200):
        # Create random features
        features = {
            f'feature_{j}': np.random.randn() for j in range(30)
        }

        # Create label (50/50 split)
        label = 1 if i % 2 == 0 else 0

        pattern = {
            'ticker': f'TICKER{i % 10}',
            'pattern_type': ['VCP', 'CUP_HANDLE', 'TRIANGLE'][i % 3],
            'window_start': '2020-01-01',
            'window_end': '2020-03-01',
            'features': features,
            'label': label,
            'success_metric': np.random.randn() * 10,
            'confidence_score': np.random.rand()
        }

        patterns.append(pattern)

    return patterns


# Feature Engineering Tests

def test_feature_engineer_initialization():
    """Test FeatureEngineer initialization."""
    engineer = FeatureEngineer()
    assert engineer is not None
    assert hasattr(engineer, 'compute_all_features')


def test_compute_all_features(sample_ohlcv_data):
    """Test feature computation."""
    engineer = FeatureEngineer()
    features_df = engineer.compute_all_features(sample_ohlcv_data)

    assert not features_df.empty
    assert len(features_df) <= len(sample_ohlcv_data)  # Some rows dropped due to indicators

    # Check that features were computed
    feature_names = engineer.get_feature_names(features_df)
    assert len(feature_names) >= 20  # Should have 20+ features


def test_feature_names(sample_ohlcv_data):
    """Test feature name extraction."""
    engineer = FeatureEngineer()
    features_df = engineer.compute_all_features(sample_ohlcv_data)
    feature_names = engineer.get_feature_names(features_df)

    # Check for expected feature categories
    assert any('rsi' in name.lower() for name in feature_names)
    assert any('macd' in name.lower() for name in feature_names)
    assert any('volume' in name.lower() for name in feature_names)
    assert any('sma' in name.lower() for name in feature_names)


# Random Forest Model Tests

def test_random_forest_initialization():
    """Test Random Forest model initialization."""
    model = RandomForestPatternDetector()
    assert model is not None
    assert not model.is_trained


def test_random_forest_prepare_data(sample_labeled_patterns):
    """Test data preparation for Random Forest."""
    model = RandomForestPatternDetector()
    X, y, feature_names = model.prepare_data(sample_labeled_patterns)

    assert X.shape[0] == len(sample_labeled_patterns)
    assert len(y) == len(sample_labeled_patterns)
    assert len(feature_names) > 0


def test_random_forest_training(sample_labeled_patterns):
    """Test Random Forest training."""
    model = RandomForestPatternDetector(n_estimators=10)  # Small for speed
    X, y, feature_names = model.prepare_data(sample_labeled_patterns)

    metrics = model.train(X, y, feature_names, cv_folds=2)

    assert model.is_trained
    assert 'cv_mean' in metrics
    assert 'train_accuracy' in metrics
    assert metrics['cv_mean'] >= 0 and metrics['cv_mean'] <= 1


def test_random_forest_prediction(sample_labeled_patterns):
    """Test Random Forest prediction."""
    model = RandomForestPatternDetector(n_estimators=10)
    X, y, feature_names = model.prepare_data(sample_labeled_patterns)

    model.train(X, y, feature_names, cv_folds=2)

    # Predict on same data
    y_pred = model.predict(X)
    y_pred_proba = model.predict_proba(X)

    assert len(y_pred) == len(y)
    assert len(y_pred_proba) == len(y)
    assert all((y_pred == 0) | (y_pred == 1))
    assert all((y_pred_proba >= 0) & (y_pred_proba <= 1))


def test_random_forest_feature_importance(sample_labeled_patterns):
    """Test feature importance extraction."""
    model = RandomForestPatternDetector(n_estimators=10)
    X, y, feature_names = model.prepare_data(sample_labeled_patterns)

    model.train(X, y, feature_names, cv_folds=2)

    importance_df = model.get_feature_importance(top_n=10)

    assert len(importance_df) <= 10
    assert 'feature' in importance_df.columns
    assert 'importance' in importance_df.columns


# XGBoost Model Tests

def test_xgboost_initialization():
    """Test XGBoost model initialization."""
    model = XGBoostPatternDetector()
    assert model is not None
    assert not model.is_trained


def test_xgboost_training(sample_labeled_patterns):
    """Test XGBoost training."""
    model = XGBoostPatternDetector(n_estimators=10)
    X, y, feature_names = model.prepare_data(sample_labeled_patterns)

    # Split for validation
    split_idx = int(len(X) * 0.8)
    X_train, X_val = X[:split_idx], X[split_idx:]
    y_train, y_val = y[:split_idx], y[split_idx:]

    metrics = model.train(X_train, y_train, feature_names, X_val=X_val, y_val=y_val, cv_folds=2)

    assert model.is_trained
    assert 'cv_mean' in metrics
    assert 'val_accuracy' in metrics


def test_xgboost_prediction(sample_labeled_patterns):
    """Test XGBoost prediction."""
    model = XGBoostPatternDetector(n_estimators=10)
    X, y, feature_names = model.prepare_data(sample_labeled_patterns)

    model.train(X, y, feature_names, cv_folds=2)

    y_pred = model.predict(X)
    y_pred_proba = model.predict_proba(X)

    assert len(y_pred) == len(y)
    assert len(y_pred_proba) == len(y)


# Neural Network Model Tests

def test_neural_network_initialization():
    """Test Neural Network model initialization."""
    model = NeuralNetworkPatternDetector()
    assert model is not None
    assert not model.is_trained


def test_neural_network_training(sample_labeled_patterns):
    """Test Neural Network training."""
    model = NeuralNetworkPatternDetector(hidden_layers=[32, 16])  # Small for speed
    X, y, feature_names = model.prepare_data(sample_labeled_patterns)

    # Split for validation
    split_idx = int(len(X) * 0.8)
    X_train, X_val = X[:split_idx], X[split_idx:]
    y_train, y_val = y[:split_idx], y[split_idx:]

    metrics = model.train(
        X_train, y_train, feature_names,
        X_val=X_val, y_val=y_val,
        epochs=5,  # Few epochs for speed
        verbose=0
    )

    assert model.is_trained
    assert 'final_train_accuracy' in metrics


def test_neural_network_prediction(sample_labeled_patterns):
    """Test Neural Network prediction."""
    model = NeuralNetworkPatternDetector(hidden_layers=[32, 16])
    X, y, feature_names = model.prepare_data(sample_labeled_patterns)

    model.train(X, y, feature_names, epochs=5, verbose=0)

    y_pred = model.predict(X)
    y_pred_proba = model.predict_proba(X)

    assert len(y_pred) == len(y)
    assert len(y_pred_proba) == len(y)


# Ensemble Model Tests

def test_ensemble_initialization():
    """Test Ensemble model initialization."""
    model = EnsemblePatternDetector()
    assert model is not None
    assert not model.is_trained


def test_ensemble_training(sample_labeled_patterns):
    """Test Ensemble model training."""
    model = EnsemblePatternDetector()

    # Use small models for speed
    model.rf_model = RandomForestPatternDetector(n_estimators=10)
    model.xgb_model = XGBoostPatternDetector(n_estimators=10)
    model.nn_model = NeuralNetworkPatternDetector(hidden_layers=[32, 16])

    X, y, feature_names = model.rf_model.prepare_data(sample_labeled_patterns)

    # Split for validation
    split_idx = int(len(X) * 0.8)
    X_train, X_val = X[:split_idx], X[split_idx:]
    y_train, y_val = y[:split_idx], y[split_idx:]

    metrics = model.train(X_train, y_train, feature_names, X_val=X_val, y_val=y_val)

    assert model.is_trained
    assert 'random_forest' in metrics
    assert 'xgboost' in metrics
    assert 'neural_network' in metrics


def test_ensemble_prediction_with_details(sample_labeled_patterns):
    """Test Ensemble prediction with details."""
    model = EnsemblePatternDetector()
    model.rf_model = RandomForestPatternDetector(n_estimators=10)
    model.xgb_model = XGBoostPatternDetector(n_estimators=10)
    model.nn_model = NeuralNetworkPatternDetector(hidden_layers=[32, 16])

    X, y, feature_names = model.rf_model.prepare_data(sample_labeled_patterns)

    model.train(X, y, feature_names)

    predictions = model.predict_with_details(X)

    assert 'random_forest' in predictions
    assert 'xgboost' in predictions
    assert 'neural_network' in predictions
    assert 'ensemble' in predictions
    assert 'ensemble_labels' in predictions


# Training Pipeline Tests

def test_training_pipeline_initialization():
    """Test TrainingPipeline initialization."""
    pipeline = TrainingPipeline()
    assert pipeline is not None
    assert pipeline.train_ratio == 0.7
    assert pipeline.val_ratio == 0.15
    assert pipeline.test_ratio == 0.15


def test_training_pipeline_split_data(sample_labeled_patterns):
    """Test data splitting."""
    pipeline = TrainingPipeline()
    train, val, test = pipeline.split_data(sample_labeled_patterns)

    total = len(train) + len(val) + len(test)
    assert total == len(sample_labeled_patterns)

    # Check approximate ratios
    assert abs(len(train) / total - 0.7) < 0.1
    assert abs(len(val) / total - 0.15) < 0.1
    assert abs(len(test) / total - 0.15) < 0.1


def test_training_pipeline_prepare_features(sample_labeled_patterns):
    """Test feature preparation."""
    pipeline = TrainingPipeline()
    X, y, feature_names = pipeline.prepare_features(sample_labeled_patterns)

    assert X.shape[0] == len(sample_labeled_patterns)
    assert len(y) == len(sample_labeled_patterns)
    assert len(feature_names) > 0


# Backtesting Tests

def test_backtester_initialization():
    """Test Backtester initialization."""
    backtester = Backtester()
    assert backtester is not None


def test_backtester_metrics(sample_labeled_patterns):
    """Test backtest metrics computation."""
    # Train a simple model
    model = RandomForestPatternDetector(n_estimators=10)
    X, y, feature_names = model.prepare_data(sample_labeled_patterns)
    model.train(X, y, feature_names, cv_folds=2)

    # Backtest
    backtester = Backtester()
    results = backtester.backtest_model(model, X, y, sample_labeled_patterns)

    assert 'accuracy' in results
    assert 'precision' in results
    assert 'recall' in results
    assert 'f1_score' in results
    assert 'auc_roc' in results
    assert 'confusion_matrix_analysis' in results
    assert 'trading_performance' in results


def test_backtester_report_generation(sample_labeled_patterns):
    """Test backtest report generation."""
    model = RandomForestPatternDetector(n_estimators=10)
    X, y, feature_names = model.prepare_data(sample_labeled_patterns)
    model.train(X, y, feature_names, cv_folds=2)

    backtester = Backtester()
    results = backtester.backtest_model(model, X, y, sample_labeled_patterns)
    report = backtester.generate_report(results)

    assert isinstance(report, str)
    assert 'BACKTEST REPORT' in report
    assert 'Accuracy' in report
    assert 'F1 Score' in report


def test_model_comparator():
    """Test ModelComparator."""
    comparator = ModelComparator()
    assert comparator is not None

    # Create sample results
    model_results = {
        'RF': {
            'accuracy': 0.85,
            'precision': 0.82,
            'recall': 0.88,
            'f1_score': 0.85,
            'auc_roc': 0.90
        },
        'XGB': {
            'accuracy': 0.87,
            'precision': 0.84,
            'recall': 0.90,
            'f1_score': 0.87,
            'auc_roc': 0.92
        }
    }

    comparison_df = comparator.compare_models(model_results)

    assert len(comparison_df) == 2
    assert 'Model' in comparison_df.columns
    assert 'F1 Score' in comparison_df.columns


# Integration Tests

def test_end_to_end_training_and_prediction(sample_labeled_patterns):
    """Test end-to-end training and prediction pipeline."""
    # Create pipeline
    pipeline = TrainingPipeline()

    # Split data
    train_patterns, val_patterns, test_patterns = pipeline.split_data(sample_labeled_patterns)

    # Train model
    model, metrics = pipeline.train_model(
        'rf',
        train_patterns,
        val_patterns,
        tune_hyperparameters=False
    )

    # Prepare test data
    X_test, y_test, _ = pipeline.prepare_features(test_patterns)

    # Evaluate
    eval_metrics = model.evaluate(X_test, y_test)

    assert 'accuracy' in eval_metrics
    assert 'f1' in eval_metrics

    # Backtest
    backtester = Backtester()
    backtest_results = backtester.backtest_model(model, X_test, y_test, test_patterns)

    assert 'trading_performance' in backtest_results
    assert 'pattern_analysis' in backtest_results


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
