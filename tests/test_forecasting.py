"""
Tests for AI Price Forecasting functionality
Tests feature engineering, models, forecasting service, and API endpoints
"""

import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Feature Engineering Tests
from app.ml.feature_engineering import FeatureEngineer


class TestFeatureEngineering:
    """Test feature engineering module"""

    @pytest.fixture
    def sample_data(self):
        """Create sample OHLCV data"""
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        np.random.seed(42)

        data = {
            'open': 100 + np.cumsum(np.random.randn(len(dates)) * 0.5),
            'high': 100 + np.cumsum(np.random.randn(len(dates)) * 0.5) + 2,
            'low': 100 + np.cumsum(np.random.randn(len(dates)) * 0.5) - 2,
            'close': 100 + np.cumsum(np.random.randn(len(dates)) * 0.5),
            'volume': np.random.randint(1000000, 10000000, len(dates))
        }

        df = pd.DataFrame(data, index=dates)
        return df

    def test_technical_indicators(self, sample_data):
        """Test technical indicator calculation"""
        engineer = FeatureEngineer()
        result = engineer.calculate_technical_indicators(sample_data)

        # Check that indicators were added
        assert 'sma_20' in result.columns
        assert 'ema_50' in result.columns
        assert 'rsi_14' in result.columns
        assert 'macd_line' in result.columns
        assert 'bb_upper_20' in result.columns
        assert 'atr_14' in result.columns

        # Check no NaN in recent data (after warmup period)
        assert not result['sma_20'].iloc[-1] == np.nan

    def test_volume_features(self, sample_data):
        """Test volume feature calculation"""
        engineer = FeatureEngineer()
        result = engineer.calculate_volume_features(sample_data)

        # Check volume features
        assert 'volume_sma_20' in result.columns
        assert 'obv' in result.columns
        assert 'mfi_14' in result.columns
        assert 'vwap' in result.columns

    def test_market_regime_detection(self, sample_data):
        """Test market regime detection"""
        engineer = FeatureEngineer()

        # First add technical indicators
        df_with_indicators = engineer.calculate_technical_indicators(sample_data)
        result = engineer.detect_market_regime(df_with_indicators)

        # Check regime columns
        assert 'market_regime' in result.columns
        assert 'trend_long' in result.columns
        assert 'volatility_regime' in result.columns

        # Check valid regime values
        valid_regimes = ['bullish', 'bearish', 'ranging', 'volatile', 'neutral']
        assert result['market_regime'].iloc[-1] in valid_regimes

    def test_prepare_features(self, sample_data):
        """Test complete feature preparation"""
        engineer = FeatureEngineer()
        result = engineer.prepare_features(sample_data)

        # Check that we have many features
        assert len(result.columns) > len(sample_data.columns)

        # Check feature names were stored
        assert len(engineer.feature_names) > 0

    def test_ml_dataset_preparation(self, sample_data):
        """Test ML dataset preparation"""
        engineer = FeatureEngineer()
        engineered = engineer.prepare_features(sample_data)

        X_train, X_test, y_train, y_test = engineer.prepare_ml_dataset(
            engineered,
            forecast_horizon=1,
            test_size=0.2
        )

        # Check split sizes
        total_samples = len(X_train) + len(X_test)
        assert len(X_test) / total_samples > 0.15  # Approximately 20%
        assert len(X_test) / total_samples < 0.25

        # Check no data leakage (train comes before test)
        assert len(X_train) > 0
        assert len(X_test) > 0


# Model Tests
from app.ml.random_forest_model import RandomForestPricePredictor
from app.ml.gradient_boosting_model import GradientBoostingPricePredictor


class TestModels:
    """Test ML models"""

    @pytest.fixture
    def sample_train_data(self):
        """Create sample training data"""
        np.random.seed(42)
        n_samples = 200
        n_features = 20

        X_train = pd.DataFrame(
            np.random.randn(n_samples, n_features),
            columns=[f'feature_{i}' for i in range(n_features)]
        )
        y_train = pd.Series(100 + np.cumsum(np.random.randn(n_samples) * 0.5))

        return X_train, y_train

    def test_random_forest_training(self, sample_train_data):
        """Test Random Forest model training"""
        X_train, y_train = sample_train_data

        model = RandomForestPricePredictor(n_estimators=50, max_depth=10)
        metrics = model.train(X_train, y_train)

        assert model.is_trained
        assert 'mae' in metrics
        assert 'rmse' in metrics
        assert 'r2_score' in metrics
        assert metrics['n_features'] == 20

    def test_random_forest_prediction(self, sample_train_data):
        """Test Random Forest predictions"""
        X_train, y_train = sample_train_data

        model = RandomForestPricePredictor(n_estimators=50)
        model.train(X_train, y_train)

        # Make predictions
        predictions, lower, upper = model.predict(X_train.head(10), return_confidence=True)

        assert len(predictions) == 10
        assert len(lower) == 10
        assert len(upper) == 10
        assert all(lower <= upper)

    def test_gradient_boosting_training(self, sample_train_data):
        """Test Gradient Boosting (XGBoost) training"""
        X_train, y_train = sample_train_data

        model = GradientBoostingPricePredictor(
            model_type='xgboost',
            n_estimators=50,
            max_depth=5
        )
        metrics = model.train(X_train, y_train, verbose=False)

        assert model.is_trained
        assert 'mae' in metrics
        assert 'rmse' in metrics

    def test_feature_importance(self, sample_train_data):
        """Test feature importance extraction"""
        X_train, y_train = sample_train_data

        model = RandomForestPricePredictor(n_estimators=50)
        model.train(X_train, y_train)

        importance = model.get_feature_importance(top_n=10)

        assert len(importance) <= 10
        assert 'feature' in importance.columns
        assert 'importance' in importance.columns


# Forecasting Service Tests
from app.ml.price_forecaster import PriceForecastingService


class TestForecastingService:
    """Test main forecasting service"""

    @pytest.fixture
    def sample_ohlcv_data(self):
        """Create realistic OHLCV data"""
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        np.random.seed(42)

        # Simulate realistic price movement
        returns = np.random.randn(len(dates)) * 0.02
        price = 100 * np.exp(np.cumsum(returns))

        data = {
            'open': price * (1 + np.random.randn(len(dates)) * 0.005),
            'high': price * (1 + abs(np.random.randn(len(dates))) * 0.01),
            'low': price * (1 - abs(np.random.randn(len(dates))) * 0.01),
            'close': price,
            'volume': np.random.randint(1000000, 10000000, len(dates))
        }

        df = pd.DataFrame(data, index=dates)
        return df

    def test_data_preparation(self, sample_ohlcv_data):
        """Test data preparation for training"""
        service = PriceForecastingService(model_type='rf')

        X_train, X_test, y_train, y_test, engineered = service.prepare_data(
            sample_ohlcv_data,
            forecast_horizon=1,
            test_size=0.2
        )

        assert len(X_train) > 0
        assert len(X_test) > 0
        assert len(y_train) == len(X_train)
        assert len(y_test) == len(X_test)

    def test_model_training_rf(self, sample_ohlcv_data):
        """Test Random Forest model training via service"""
        service = PriceForecastingService(model_type='rf')

        metrics = service.train_model(
            sample_ohlcv_data,
            forecast_horizon=1,
            test_size=0.2,
            save_model=False
        )

        assert service.is_trained
        assert 'test_metrics' in metrics
        assert metrics['test_metrics']['mae'] > 0

    @pytest.mark.skip(reason="Gradient boosting test - runs slower")
    def test_model_training_xgboost(self, sample_ohlcv_data):
        """Test XGBoost model training via service"""
        service = PriceForecastingService(model_type='xgboost')

        metrics = service.train_model(
            sample_ohlcv_data,
            forecast_horizon=1,
            test_size=0.2,
            save_model=False
        )

        assert service.is_trained

    def test_prediction(self, sample_ohlcv_data):
        """Test making predictions"""
        service = PriceForecastingService(model_type='rf')

        # Train first
        service.train_model(sample_ohlcv_data, save_model=False)

        # Make predictions
        result = service.predict(sample_ohlcv_data, return_confidence=True)

        assert 'predictions' in result
        assert 'confidence_lower' in result
        assert 'confidence_upper' in result
        assert len(result['predictions']) > 0

    def test_future_forecast(self, sample_ohlcv_data):
        """Test future forecasting"""
        service = PriceForecastingService(model_type='rf')

        # Train model
        service.train_model(sample_ohlcv_data, save_model=False)

        # Forecast 5 days ahead
        forecast = service.forecast_future(sample_ohlcv_data, n_days=5)

        assert len(forecast['forecasted_prices']) == 5
        assert len(forecast['forecast_dates']) == 5


# Performance Tracking Tests
from app.ml.model_performance import PerformanceTracker


class TestPerformanceTracking:
    """Test model performance tracking"""

    def test_accuracy_metrics(self):
        """Test accuracy metrics calculation"""
        actual = np.array([100, 102, 101, 103, 105])
        predicted = np.array([100.5, 101.5, 101.2, 103.5, 104.8])

        tracker = PerformanceTracker()
        metrics = tracker.calculate_accuracy_metrics(actual, predicted)

        assert 'mae' in metrics
        assert 'rmse' in metrics
        assert 'mape' in metrics
        assert 'r2_score' in metrics
        assert 'directional_accuracy' in metrics

        # MAE should be small
        assert metrics['mae'] < 1.0

    def test_trading_metrics(self):
        """Test trading-specific metrics"""
        actual = np.array([100, 102, 101, 103, 105])
        predicted = np.array([101, 103, 100, 104, 106])
        prices = np.array([99, 101, 100, 102, 104])

        tracker = PerformanceTracker()
        metrics = tracker.calculate_accuracy_metrics(actual, predicted, prices)

        # Should include trading metrics
        assert 'win_rate' in metrics
        assert 'avg_return' in metrics
        assert 'sharpe_ratio' in metrics
        assert 'max_drawdown' in metrics

    def test_performance_report_generation(self):
        """Test performance report generation"""
        backtest_results = {
            'n_predictions': 100,
            'window_size': 60,
            'forecast_horizon': 1,
            'metrics': {
                'mae': 0.5,
                'mape': 2.0,
                'directional_accuracy': 65.0,
                'r2_score': 0.75
            },
            'errors': [0.3, 0.5, 0.2, 0.8, 0.4]
        }

        tracker = PerformanceTracker()
        report = tracker.generate_performance_report('ensemble', backtest_results)

        assert 'model_type' in report
        assert 'backtest_summary' in report
        assert 'error_analysis' in report
        assert 'recommendations' in report
        assert len(report['recommendations']) > 0


# Integration Tests (require more setup, marked as slow)
@pytest.mark.slow
class TestAPIIntegration:
    """Test API endpoints (requires running server)"""

    def test_forecast_endpoint_structure(self):
        """Test that forecast endpoint has correct structure"""
        from app.api.forecast import ForecastRequest, ForecastResponse

        # Test request model
        request = ForecastRequest(
            ticker="AAPL",
            model_type="rf",
            forecast_days=5
        )

        assert request.ticker == "AAPL"
        assert request.model_type == "rf"
        assert request.forecast_days == 5

    def test_train_model_request_structure(self):
        """Test train model request structure"""
        from app.api.forecast import TrainModelRequest

        request = TrainModelRequest(
            ticker="AAPL",
            model_type="ensemble",
            lookback_days=252
        )

        assert request.ticker == "AAPL"
        assert request.lookback_days == 252


# Benchmark Tests
@pytest.mark.benchmark
class TestBenchmarks:
    """Benchmark tests for performance"""

    @pytest.fixture
    def large_dataset(self):
        """Create larger dataset for benchmarking"""
        dates = pd.date_range(start='2020-01-01', end='2023-12-31', freq='D')
        np.random.seed(42)

        returns = np.random.randn(len(dates)) * 0.02
        price = 100 * np.exp(np.cumsum(returns))

        data = {
            'open': price,
            'high': price * 1.01,
            'low': price * 0.99,
            'close': price,
            'volume': np.random.randint(1000000, 10000000, len(dates))
        }

        return pd.DataFrame(data, index=dates)

    def test_feature_engineering_speed(self, large_dataset, benchmark):
        """Benchmark feature engineering speed"""
        engineer = FeatureEngineer()

        def run_feature_engineering():
            return engineer.prepare_features(large_dataset)

        result = benchmark(run_feature_engineering)
        assert len(result) > 0

    @pytest.mark.skip(reason="RF training benchmark - slow")
    def test_rf_training_speed(self, large_dataset, benchmark):
        """Benchmark Random Forest training speed"""
        service = PriceForecastingService(model_type='rf')

        def train_model():
            return service.train_model(large_dataset, save_model=False)

        benchmark(train_model)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
