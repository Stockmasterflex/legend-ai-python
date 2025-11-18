# AI Price Forecasting

## Overview

The AI Price Forecasting system provides advanced machine learning-powered stock price predictions with confidence intervals, probability cones, and comprehensive performance tracking.

## Features

### 1. Prediction Models

- **LSTM Neural Networks**: Deep learning model for sequential time series prediction
- **Random Forest**: Ensemble tree-based model with feature importance
- **Gradient Boosting**: XGBoost and LightGBM implementations for high accuracy
- **Ensemble Models**: Combines all three models with optimized weighting

### 2. Feature Engineering

Comprehensive technical indicator extraction:

- **Moving Averages**: SMA, EMA (5, 10, 20, 50, 100, 200 periods)
- **Volatility**: Bollinger Bands, ATR, Standard Deviation
- **Momentum**: RSI, MACD, Stochastic Oscillator, ROC
- **Trend**: ADX, Directional Movement Indicators
- **Volume**: OBV, MFI, VWAP, Volume Ratios
- **Market Regime**: Bullish/Bearish/Ranging/Volatile detection

### 3. Forecast Visualization

- **Probability Cones**: Multiple confidence level visualization
- **Confidence Intervals**: 50%, 70%, 90% prediction bands
- **Support/Resistance Bands**: Automatic level detection
- **Multi-timeframe Charts**: Compare 1D, 1W, 1M forecasts

### 4. Model Performance

- **Accuracy Metrics**: MAE, RMSE, MAPE, R², Directional Accuracy
- **Backtesting**: Walk-forward validation on historical data
- **Model Comparison**: Side-by-side performance analysis
- **Trading Metrics**: Win rate, Sharpe ratio, Max drawdown
- **Continuous Learning**: Automated model retraining

## API Endpoints

### POST /api/forecast/predict

Predict future stock prices.

**Request:**
```json
{
  "ticker": "AAPL",
  "interval": "1day",
  "model_type": "ensemble",
  "forecast_days": 5,
  "return_confidence": true,
  "return_visualization": false
}
```

**Response:**
```json
{
  "success": true,
  "ticker": "AAPL",
  "current_price": 175.50,
  "forecast_dates": ["2025-01-01", "2025-01-02", "2025-01-03"],
  "forecasted_prices": [176.20, 177.50, 178.10],
  "confidence_lower": [174.00, 175.00, 176.00],
  "confidence_upper": [178.50, 180.00, 180.50],
  "predicted_returns": [0.40, 1.14, 1.48],
  "model_type": "ensemble"
}
```

### POST /api/forecast/train

Train a new forecasting model.

**Request:**
```json
{
  "ticker": "AAPL",
  "interval": "1day",
  "model_type": "ensemble",
  "lookback_days": 252,
  "test_size": 0.2,
  "save_model": true
}
```

**Response:**
```json
{
  "success": true,
  "ticker": "AAPL",
  "model_type": "ensemble",
  "training_metrics": {
    "individual_results": {
      "lstm": {"loss": [0.05], "mae": [1.2]},
      "rf": {"mae": 1.1, "r2_score": 0.85},
      "gb": {"mae": 1.0, "rmse": 1.5}
    },
    "weights": {"lstm": 0.33, "rf": 0.33, "gb": 0.34}
  },
  "message": "Model trained successfully on 252 samples"
}
```

### POST /api/forecast/backtest

Perform walk-forward backtesting.

**Request:**
```json
{
  "ticker": "AAPL",
  "model_type": "ensemble",
  "window_size": 100,
  "forecast_horizon": 1
}
```

**Response:**
```json
{
  "success": true,
  "ticker": "AAPL",
  "backtest_results": {
    "metrics": {
      "mae": 1.5,
      "rmse": 2.1,
      "mape": 1.8,
      "directional_accuracy": 65.5,
      "win_rate": 62.0,
      "sharpe_ratio": 1.2
    },
    "n_predictions": 150
  },
  "performance_report": {
    "recommendations": [
      "Strong directional accuracy > 65%: Good for trading signals",
      "Model performance is moderate. Monitor and retrain periodically."
    ]
  }
}
```

### GET /api/forecast/models

List all loaded models.

**Response:**
```json
{
  "success": true,
  "loaded_models": ["AAPL_ensemble", "TSLA_rf", "SPY_xgboost"],
  "count": 3
}
```

### GET /api/forecast/model-info/{ticker}/{model_type}

Get detailed model information.

**Response:**
```json
{
  "success": true,
  "ticker": "AAPL",
  "model_info": {
    "model_type": "ensemble",
    "is_trained": true,
    "model_weights": {"lstm": 0.35, "rf": 0.32, "gb": 0.33},
    "training_metrics": {...}
  }
}
```

### GET /api/forecast/feature-importance/{ticker}/{model_type}

Get top feature importance.

**Response:**
```json
{
  "success": true,
  "ticker": "AAPL",
  "model_type": "ensemble",
  "feature_importance": {
    "type": "ensemble",
    "importance": {
      "rf": [
        {"feature": "rsi_14", "importance": 0.15},
        {"feature": "macd_histogram", "importance": 0.12}
      ]
    }
  }
}
```

## Python Usage

### Basic Forecasting

```python
from app.ml.price_forecaster import PriceForecastingService
import pandas as pd

# Load historical data
df = pd.read_csv('AAPL_historical.csv', index_col='date', parse_dates=True)

# Create forecasting service
forecaster = PriceForecastingService(model_type='ensemble')

# Train model
metrics = forecaster.train_model(df, forecast_horizon=1, test_size=0.2)
print(f"Training MAE: {metrics['test_metrics']['mae']:.2f}")

# Make predictions
result = forecaster.predict(df, return_confidence=True)
print(f"Predicted prices: {result['predictions'][:5]}")

# Forecast future
forecast = forecaster.forecast_future(df, n_days=5)
print(f"5-day forecast: {forecast['forecasted_prices']}")
```

### Feature Engineering

```python
from app.ml.feature_engineering import FeatureEngineer

# Initialize feature engineer
engineer = FeatureEngineer()

# Prepare features
engineered_df = engineer.prepare_features(df)
print(f"Generated {len(engineer.feature_names)} features")

# Get ML-ready dataset
X_train, X_test, y_train, y_test = engineer.prepare_ml_dataset(
    engineered_df,
    target_column='close',
    forecast_horizon=1,
    test_size=0.2
)
```

### Custom Model Training

```python
from app.ml.lstm_model import LSTMPricePredictor
from app.ml.random_forest_model import RandomForestPricePredictor
from app.ml.gradient_boosting_model import GradientBoostingPricePredictor

# Train LSTM
lstm = LSTMPricePredictor(sequence_length=60, lstm_units=(128, 64))
lstm.train(X_train, y_train, X_val=X_test, y_val=y_test, epochs=50)

# Train Random Forest
rf = RandomForestPricePredictor(n_estimators=200, max_depth=20)
rf.train(X_train, y_train)

# Train XGBoost
xgb = GradientBoostingPricePredictor(model_type='xgboost', n_estimators=300)
xgb.train(X_train, y_train, X_val=X_test, y_val=y_test)

# Make predictions
lstm_pred, lstm_lower, lstm_upper = lstm.predict(X_test)
rf_pred, rf_lower, rf_upper = rf.predict(X_test)
xgb_pred, _, _ = xgb.predict(X_test)
```

### Performance Tracking

```python
from app.ml.model_performance import PerformanceTracker

# Initialize tracker
tracker = PerformanceTracker()

# Calculate metrics
actual = y_test.values
predicted = lstm_pred

metrics = tracker.calculate_accuracy_metrics(actual, predicted)
print(f"MAE: {metrics['mae']:.2f}")
print(f"Directional Accuracy: {metrics['directional_accuracy']:.1f}%")

# Backtest model
backtest_results = tracker.backtest_model(
    forecaster,
    historical_data=df,
    window_size=100,
    forecast_horizon=1,
    step_size=5
)

# Generate report
report = tracker.generate_performance_report('ensemble', backtest_results)
print("\nRecommendations:")
for rec in report['recommendations']:
    print(f"- {rec}")
```

### Visualization

```python
from app.ml.forecast_visualization import ForecastVisualizer
import matplotlib.pyplot as plt

# Create visualizer
visualizer = ForecastVisualizer()

# Probability cone
viz_data = visualizer.create_probability_cone(
    historical_prices=df['close'].tail(60),
    forecast_dates=forecast_dates,
    forecast_prices=forecast_prices,
    confidence_intervals=[
        (lower_50, upper_50),
        (lower_70, upper_70),
        (lower_90, upper_90)
    ],
    confidence_levels=[0.5, 0.7, 0.9],
    title="AAPL 5-Day Forecast"
)

# Display chart
import base64
from IPython.display import Image
Image(base64.b64decode(viz_data['image_base64']))

# Support/Resistance levels
support, resistance = visualizer.calculate_support_resistance_levels(
    df['close'].values,
    n_levels=3
)
print(f"Support levels: {support}")
print(f"Resistance levels: {resistance}")
```

## Model Details

### LSTM Neural Network

- **Architecture**: 3-layer LSTM with Dropout and Batch Normalization
- **Sequence Length**: 60 time steps default
- **Training**: Adam optimizer with early stopping
- **Confidence Intervals**: Monte Carlo Dropout sampling

### Random Forest

- **Trees**: 200 estimators default
- **Max Depth**: 20 levels
- **Feature Selection**: Sqrt(n_features) per split
- **Confidence Intervals**: Tree prediction variance

### Gradient Boosting

- **Implementation**: XGBoost and LightGBM
- **Boosting Rounds**: 300 default
- **Learning Rate**: 0.05
- **Early Stopping**: 50 rounds patience

### Ensemble Model

- **Combination**: Weighted average of all models
- **Weight Optimization**: Based on validation performance
- **Adaptive Weighting**: Adjusts to market conditions

## Performance Metrics

### Accuracy Metrics

- **MAE (Mean Absolute Error)**: Average prediction error
- **RMSE (Root Mean Square Error)**: Penalizes large errors
- **MAPE (Mean Absolute Percentage Error)**: Percentage error
- **R² (Coefficient of Determination)**: Variance explained
- **Directional Accuracy**: % of correct trend predictions

### Trading Metrics

- **Win Rate**: % of profitable predictions
- **Average Return**: Mean return when following signals
- **Sharpe Ratio**: Risk-adjusted returns
- **Max Drawdown**: Largest peak-to-trough decline

## Best Practices

1. **Data Quality**: Use at least 200+ data points for training
2. **Feature Selection**: More features isn't always better - use feature importance
3. **Model Selection**: Start with ensemble, then optimize individual models
4. **Backtesting**: Always backtest before live use
5. **Retraining**: Retrain models monthly or when performance degrades
6. **Risk Management**: Use confidence intervals for position sizing
7. **Ensemble Weighting**: Let the system optimize weights automatically

## Database Storage

Forecasts are stored in the `price_predictions` table:

```sql
CREATE TABLE price_predictions (
    id SERIAL PRIMARY KEY,
    ticker_id INTEGER,
    model_type VARCHAR(50),
    prediction_date TIMESTAMP,
    target_date TIMESTAMP,
    timeframe VARCHAR(20),
    predicted_price FLOAT,
    confidence_lower FLOAT,
    confidence_upper FLOAT,
    actual_price FLOAT,
    accuracy_score FLOAT,
    market_regime VARCHAR(50),
    feature_importance JSONB
);
```

Performance metrics in `model_performance` table:

```sql
CREATE TABLE model_performance (
    id SERIAL PRIMARY KEY,
    model_type VARCHAR(50),
    evaluation_period VARCHAR(50),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    mae FLOAT,
    rmse FLOAT,
    r2_score FLOAT,
    directional_accuracy FLOAT,
    win_rate FLOAT,
    sharpe_ratio FLOAT
);
```

## Troubleshooting

### Common Issues

**Insufficient Data Error**
- Ensure at least 100+ historical data points
- Use longer timeframe if daily data is sparse

**High MAPE (>10%)**
- Retrain model with more data
- Try different model type (ensemble often best)
- Check for data quality issues

**Poor Directional Accuracy (<55%)**
- Add more technical indicators
- Increase training window size
- Consider market regime filtering

**Model Loading Failures**
- Check model file paths
- Ensure model was saved after training
- Verify TensorFlow compatibility for LSTM

## Future Enhancements

- [ ] Sentiment analysis integration
- [ ] Multi-asset correlation features
- [ ] Transformer models (Attention mechanism)
- [ ] Real-time model updating
- [ ] Auto-ML hyperparameter tuning
- [ ] Portfolio-level forecasting
- [ ] Options pricing predictions

## References

- [Deep Learning for Time Series Forecasting](https://machinelearningmastery.com/deep-learning-for-time-series-forecasting/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [Technical Analysis Library](https://technical-analysis-library-in-python.readthedocs.io/)
