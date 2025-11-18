"""
Model Performance Tracking and Backtesting
Tracks accuracy metrics, performs backtesting, and compares model performance
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
from sqlalchemy.orm import Session

from app.models import ModelPerformance, PricePrediction
from app.ml.price_forecaster import PriceForecastingService

logger = logging.getLogger(__name__)


class PerformanceTracker:
    """
    Tracks and analyzes model performance
    """

    def __init__(self, db_session: Optional[Session] = None):
        """
        Initialize performance tracker

        Args:
            db_session: Database session for storing results
        """
        self.db_session = db_session

    def calculate_accuracy_metrics(
        self,
        actual: np.ndarray,
        predicted: np.ndarray,
        prices: Optional[np.ndarray] = None
    ) -> Dict[str, float]:
        """
        Calculate comprehensive accuracy metrics

        Args:
            actual: Actual values
            predicted: Predicted values
            prices: Actual prices (for calculating returns-based metrics)

        Returns:
            Dictionary of accuracy metrics
        """
        # Basic regression metrics
        mae = np.mean(np.abs(actual - predicted))
        rmse = np.sqrt(np.mean((actual - predicted) ** 2))
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100

        # R-squared
        ss_res = np.sum((actual - predicted) ** 2)
        ss_tot = np.sum((actual - np.mean(actual)) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        # Directional accuracy
        if len(actual) > 1 and len(predicted) > 1:
            actual_direction = np.sign(np.diff(actual))
            pred_direction = np.sign(np.diff(predicted))
            directional_accuracy = np.mean(actual_direction == pred_direction) * 100
        else:
            directional_accuracy = 0

        # Max error
        max_error = np.max(np.abs(actual - predicted))

        metrics = {
            'mae': float(mae),
            'rmse': float(rmse),
            'mape': float(mape),
            'r2_score': float(r2),
            'directional_accuracy': float(directional_accuracy),
            'max_error': float(max_error),
            'n_samples': len(actual)
        }

        # Trading-specific metrics if prices provided
        if prices is not None:
            trading_metrics = self._calculate_trading_metrics(actual, predicted, prices)
            metrics.update(trading_metrics)

        return metrics

    def _calculate_trading_metrics(
        self,
        actual: np.ndarray,
        predicted: np.ndarray,
        prices: np.ndarray
    ) -> Dict[str, float]:
        """
        Calculate trading-specific metrics

        Args:
            actual: Actual future prices
            predicted: Predicted future prices
            prices: Current prices

        Returns:
            Dictionary of trading metrics
        """
        # Simulate trading based on predictions
        actual_returns = (actual - prices) / prices
        predicted_returns = (predicted - prices) / prices

        # Win rate (correct direction predictions)
        correct_direction = np.sign(actual_returns) == np.sign(predicted_returns)
        win_rate = np.mean(correct_direction) * 100

        # Average return when following predictions
        predicted_trades = predicted_returns * np.sign(predicted_returns)  # Take position based on prediction
        actual_trade_returns = actual_returns * np.sign(predicted_returns)  # Actual return of those positions

        avg_return = np.mean(actual_trade_returns) * 100

        # Sharpe ratio (assuming daily returns)
        if len(actual_trade_returns) > 1:
            sharpe_ratio = np.mean(actual_trade_returns) / (np.std(actual_trade_returns) + 1e-10) * np.sqrt(252)
        else:
            sharpe_ratio = 0

        # Max drawdown
        cumulative_returns = np.cumprod(1 + actual_trade_returns)
        running_max = np.maximum.accumulate(cumulative_returns)
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = np.min(drawdown) * 100

        return {
            'win_rate': float(win_rate),
            'avg_return': float(avg_return),
            'sharpe_ratio': float(sharpe_ratio),
            'max_drawdown': float(max_drawdown)
        }

    def backtest_model(
        self,
        forecasting_service: PriceForecastingService,
        historical_data: pd.DataFrame,
        window_size: int = 100,
        forecast_horizon: int = 1,
        step_size: int = 1
    ) -> Dict[str, Any]:
        """
        Perform walk-forward backtesting

        Args:
            forecasting_service: Forecasting service with trained model
            historical_data: Full historical dataset
            window_size: Size of training window
            forecast_horizon: Days ahead to predict
            step_size: Days to step forward in each iteration

        Returns:
            Dictionary with backtest results
        """
        logger.info(f"Starting backtest with {len(historical_data)} samples")

        predictions = []
        actuals = []
        dates = []
        errors = []

        n_iterations = (len(historical_data) - window_size - forecast_horizon) // step_size

        for i in range(0, n_iterations * step_size, step_size):
            try:
                # Split data
                train_end = window_size + i
                test_idx = train_end + forecast_horizon

                if test_idx >= len(historical_data):
                    break

                train_data = historical_data.iloc[:train_end]
                test_data = historical_data.iloc[test_idx]

                # Make prediction
                prediction_result = forecasting_service.predict(train_data, return_confidence=False)

                if prediction_result['predictions']:
                    pred_price = prediction_result['predictions'][-1]
                    actual_price = test_data['close']

                    predictions.append(pred_price)
                    actuals.append(actual_price)
                    dates.append(historical_data.index[test_idx])
                    errors.append(abs(pred_price - actual_price))

            except Exception as e:
                logger.warning(f"Backtest iteration {i} failed: {e}")
                continue

        if not predictions:
            return {'error': 'No predictions generated during backtest'}

        # Calculate metrics
        predictions_arr = np.array(predictions)
        actuals_arr = np.array(actuals)

        metrics = self.calculate_accuracy_metrics(actuals_arr, predictions_arr)

        # Additional backtest-specific analysis
        results = {
            'metrics': metrics,
            'predictions': predictions,
            'actuals': actuals,
            'dates': dates,
            'errors': errors,
            'n_predictions': len(predictions),
            'avg_error': np.mean(errors),
            'median_error': np.median(errors),
            'window_size': window_size,
            'forecast_horizon': forecast_horizon
        }

        logger.info(f"Backtest complete: {len(predictions)} predictions, MAE: {metrics['mae']:.4f}")

        return results

    def compare_models(
        self,
        models: Dict[str, PriceForecastingService],
        test_data: pd.DataFrame,
        test_targets: pd.Series
    ) -> pd.DataFrame:
        """
        Compare performance of multiple models

        Args:
            models: Dictionary of {model_name: forecasting_service}
            test_data: Test features
            test_targets: Test targets

        Returns:
            DataFrame with comparison results
        """
        logger.info(f"Comparing {len(models)} models")

        results = []

        for model_name, forecasting_service in models.items():
            try:
                # Make predictions
                prediction_result = forecasting_service.predict(
                    test_data,
                    return_confidence=False
                )

                predictions = np.array(prediction_result['predictions'])

                # Align predictions with targets (handle LSTM sequence mismatch)
                if len(predictions) < len(test_targets):
                    test_targets_aligned = test_targets.iloc[-len(predictions):].values
                else:
                    test_targets_aligned = test_targets.values
                    predictions = predictions[:len(test_targets)]

                # Calculate metrics
                metrics = self.calculate_accuracy_metrics(
                    test_targets_aligned,
                    predictions
                )

                metrics['model_name'] = model_name
                metrics['n_predictions'] = len(predictions)

                results.append(metrics)

            except Exception as e:
                logger.error(f"Model {model_name} comparison failed: {e}")
                results.append({
                    'model_name': model_name,
                    'error': str(e)
                })

        # Create comparison DataFrame
        comparison_df = pd.DataFrame(results)

        # Sort by MAE (lower is better)
        if 'mae' in comparison_df.columns:
            comparison_df = comparison_df.sort_values('mae')

        logger.info("Model comparison complete")

        return comparison_df

    def save_performance_to_db(
        self,
        model_type: str,
        model_version: str,
        metrics: Dict[str, Any],
        start_date: datetime,
        end_date: datetime,
        evaluation_period: str = "daily"
    ) -> Optional[ModelPerformance]:
        """
        Save performance metrics to database

        Args:
            model_type: Type of model
            model_version: Model version identifier
            metrics: Dictionary of performance metrics
            start_date: Start date of evaluation period
            end_date: End date of evaluation period
            evaluation_period: Period type (daily, weekly, monthly)

        Returns:
            ModelPerformance object if saved successfully
        """
        if not self.db_session:
            logger.warning("No database session available, cannot save performance")
            return None

        try:
            performance = ModelPerformance(
                model_type=model_type,
                model_version=model_version,
                evaluation_period=evaluation_period,
                start_date=start_date,
                end_date=end_date,
                mae=metrics.get('mae'),
                rmse=metrics.get('rmse'),
                mape=metrics.get('mape'),
                r2_score=metrics.get('r2_score'),
                directional_accuracy=metrics.get('directional_accuracy'),
                win_rate=metrics.get('win_rate'),
                avg_return=metrics.get('avg_return'),
                sharpe_ratio=metrics.get('sharpe_ratio'),
                max_drawdown=metrics.get('max_drawdown'),
                total_predictions=metrics.get('n_samples', 0)
            )

            self.db_session.add(performance)
            self.db_session.commit()

            logger.info(f"Performance metrics saved for {model_type} v{model_version}")

            return performance

        except Exception as e:
            logger.error(f"Failed to save performance to database: {e}")
            self.db_session.rollback()
            return None

    def get_historical_performance(
        self,
        model_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve historical performance metrics from database

        Args:
            model_type: Filter by model type (None for all)
            limit: Maximum number of records to return

        Returns:
            List of performance records
        """
        if not self.db_session:
            logger.warning("No database session available")
            return []

        try:
            query = self.db_session.query(ModelPerformance)

            if model_type:
                query = query.filter(ModelPerformance.model_type == model_type)

            query = query.order_by(ModelPerformance.created_at.desc()).limit(limit)

            results = []
            for perf in query.all():
                results.append({
                    'id': perf.id,
                    'model_type': perf.model_type,
                    'model_version': perf.model_version,
                    'evaluation_period': perf.evaluation_period,
                    'start_date': perf.start_date.isoformat() if perf.start_date else None,
                    'end_date': perf.end_date.isoformat() if perf.end_date else None,
                    'mae': perf.mae,
                    'rmse': perf.rmse,
                    'mape': perf.mape,
                    'r2_score': perf.r2_score,
                    'directional_accuracy': perf.directional_accuracy,
                    'win_rate': perf.win_rate,
                    'avg_return': perf.avg_return,
                    'sharpe_ratio': perf.sharpe_ratio,
                    'max_drawdown': perf.max_drawdown,
                    'total_predictions': perf.total_predictions,
                    'created_at': perf.created_at.isoformat() if perf.created_at else None
                })

            return results

        except Exception as e:
            logger.error(f"Failed to retrieve historical performance: {e}")
            return []

    def generate_performance_report(
        self,
        model_type: str,
        backtest_results: Dict[str, Any],
        comparison_results: Optional[pd.DataFrame] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive performance report

        Args:
            model_type: Type of model
            backtest_results: Results from backtesting
            comparison_results: Results from model comparison

        Returns:
            Dictionary with formatted report
        """
        report = {
            'model_type': model_type,
            'generated_at': datetime.now().isoformat(),
            'backtest_summary': {
                'n_predictions': backtest_results.get('n_predictions'),
                'window_size': backtest_results.get('window_size'),
                'forecast_horizon': backtest_results.get('forecast_horizon'),
                'metrics': backtest_results.get('metrics', {})
            }
        }

        # Add error analysis
        if 'errors' in backtest_results:
            errors = backtest_results['errors']
            report['error_analysis'] = {
                'mean_error': float(np.mean(errors)),
                'median_error': float(np.median(errors)),
                'std_error': float(np.std(errors)),
                'max_error': float(np.max(errors)),
                'min_error': float(np.min(errors))
            }

        # Add comparison if available
        if comparison_results is not None:
            report['model_comparison'] = comparison_results.to_dict('records')

        # Add recommendations
        report['recommendations'] = self._generate_recommendations(backtest_results)

        return report

    def _generate_recommendations(self, backtest_results: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations based on performance

        Args:
            backtest_results: Backtest results

        Returns:
            List of recommendation strings
        """
        recommendations = []
        metrics = backtest_results.get('metrics', {})

        # Check MAE
        mape = metrics.get('mape', 0)
        if mape > 10:
            recommendations.append("MAPE > 10%: Consider retraining model with more data or adjusting hyperparameters")
        elif mape < 3:
            recommendations.append("Excellent MAPE < 3%: Model performing very well")

        # Check directional accuracy
        dir_acc = metrics.get('directional_accuracy', 0)
        if dir_acc < 55:
            recommendations.append("Directional accuracy < 55%: Model struggling with trend direction")
        elif dir_acc > 65:
            recommendations.append("Strong directional accuracy > 65%: Good for trading signals")

        # Check R²
        r2 = metrics.get('r2_score', 0)
        if r2 < 0.3:
            recommendations.append("Low R² < 0.3: Model not capturing much variance, consider feature engineering")
        elif r2 > 0.7:
            recommendations.append("High R² > 0.7: Model explaining variance well")

        if not recommendations:
            recommendations.append("Model performance is moderate. Monitor and retrain periodically.")

        return recommendations
