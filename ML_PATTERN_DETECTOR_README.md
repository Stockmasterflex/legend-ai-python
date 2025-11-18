# ML Pattern Detector

Comprehensive machine learning system for detecting trading chart patterns using ensemble methods.

## Overview

This ML pattern detector combines three powerful machine learning approaches:
- **Random Forest**: Ensemble of decision trees for robust pattern classification
- **XGBoost**: Gradient boosting for high-performance pattern detection
- **Neural Network**: Deep learning for complex pattern recognition
- **Ensemble Model**: Combines all three approaches for optimal performance

## Architecture

```
app/ml/
├── models/              # ML model implementations
│   ├── random_forest_model.py
│   ├── xgboost_model.py
│   ├── neural_network_model.py
│   ├── ensemble_model.py
│   └── model_registry.py
├── features/            # Feature engineering
│   └── feature_engineering.py
├── data/               # Data collection and labeling
│   ├── data_collector.py
│   └── manual_labeler.py
├── training/           # Training pipeline
│   └── training_pipeline.py
├── evaluation/         # Backtesting and evaluation
│   └── backtesting.py
└── monitoring/         # Metrics tracking
    └── metrics_tracker.py
```

## Features

### 1. Feature Engineering (20+ Technical Indicators)

**Price Action Features:**
- Price ranges, candlestick patterns
- Price changes over multiple periods
- Distance from 52-week highs/lows

**Volume Features:**
- On-Balance Volume (OBV)
- Volume profile and z-scores
- Volume-price correlation

**Technical Indicators:**
- Moving Averages (SMA, EMA)
- MACD (Moving Average Convergence Divergence)
- RSI (Relative Strength Index)
- Bollinger Bands
- Stochastic Oscillator
- ADX (Average Directional Index)
- ATR (Average True Range)
- Money Flow Index (MFI)

**Trend Features:**
- Linear regression slopes
- Trend strength indicators
- Moving average crossovers

**Volatility Features:**
- Historical volatility
- Parkinson's volatility
- Garman-Klass volatility

**Pattern-Specific Features:**
- Pivot points
- Consolidation detection
- Breakout potential

## Quick Start

### 1. Data Collection

```python
from app.ml.data.data_collector import DataCollector
from app.services.market_data import MarketDataService

# Initialize
market_data = MarketDataService()
collector = DataCollector(market_data)

# Collect historical data
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
labeled_patterns = await collector.create_labeled_dataset(
    tickers=tickers,
    years=10,
    examples_per_pattern=100
)
```

### 2. Training Models

```python
from app.ml.training.training_pipeline import TrainingPipeline

# Initialize pipeline
pipeline = TrainingPipeline(
    train_ratio=0.7,
    val_ratio=0.15,
    test_ratio=0.15
)

# Train all models
results = pipeline.train_all_models(
    patterns=labeled_patterns,
    tune_hyperparameters=True  # Optional
)

# Train individual model
model, metrics = pipeline.train_model(
    model_type='ensemble',  # or 'rf', 'xgboost', 'nn'
    train_patterns=train_patterns,
    val_patterns=val_patterns
)
```

### 3. Evaluation and Backtesting

```python
from app.ml.evaluation.backtesting import Backtester

# Initialize backtester
backtester = Backtester()

# Backtest model
results = backtester.backtest_model(
    model=model,
    X_test=X_test,
    y_test=y_test,
    test_patterns=test_patterns
)

# Generate report
report = backtester.generate_report(results)
print(report)
```

### 4. Making Predictions

```python
from app.ml.models.ensemble_model import EnsemblePatternDetector
from app.ml.features.feature_engineering import FeatureEngineer

# Load trained model
model = EnsemblePatternDetector()
model.load('ensemble_trained_20250101_120000')

# Prepare features
engineer = FeatureEngineer()
features_df = engineer.compute_all_features(ohlcv_data)

# Get latest features
latest_features = features_df.iloc[-1]
feature_names = engineer.get_feature_names(features_df)
X = np.array([[latest_features[name] for name in feature_names]])

# Predict
predictions = model.predict_with_details(X)
print(f"ML Score: {predictions['ensemble'][0]:.4f}")
print(f"Prediction: {predictions['ensemble_labels'][0]}")
```

## API Usage

### ML Pattern Detection Endpoint

```bash
# Detect patterns using ML
curl -X POST "http://localhost:8000/api/ml/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "interval": "1day",
    "model_type": "ensemble",
    "threshold": 0.5,
    "include_rule_based": true
  }'
```

### Training Endpoint

```bash
# Start training (background task)
curl -X POST "http://localhost:8000/api/ml/train" \
  -H "Content-Type: application/json" \
  -d '{
    "tickers": ["AAPL", "MSFT", "GOOGL"],
    "years": 5,
    "model_type": "ensemble",
    "tune_hyperparameters": false,
    "examples_per_pattern": 100
  }'
```

### Model Management

```bash
# Load a specific model
curl -X POST "http://localhost:8000/api/ml/model/load?model_name=ensemble_trained_20250101"

# List available models
curl "http://localhost:8000/api/ml/models/list"

# Get model info
curl "http://localhost:8000/api/ml/model/info"
```

## Model Registry

The model registry provides version control and lifecycle management:

```python
from app.ml.models.model_registry import ModelRegistry, ModelMetadata

# Initialize registry
registry = ModelRegistry()

# Register a model
metadata = ModelMetadata(
    model_id="ensemble_v1",
    model_type="ensemble",
    version="1.0.0",
    created_at=datetime.now().isoformat(),
    created_by="system",
    training_data_info={"n_samples": 1000, "tickers": ["AAPL", "MSFT"]},
    performance_metrics={"f1_score": 0.85, "accuracy": 0.83},
    hyperparameters={},
    feature_names=feature_names,
    n_features=len(feature_names),
    n_training_samples=1000,
    tags=["production"]
)

model_id = registry.register_model(
    model_name="pattern_detector",
    model_type="ensemble",
    version="1.0.0",
    model_path="/path/to/model",
    metadata=metadata,
    promote_to_production=True
)

# List all models
models = registry.list_models()

# Get production model
prod_model = registry.get_model("pattern_detector", use_production=True)

# Compare versions
comparison = registry.compare_versions(
    "pattern_detector",
    version1="1.0.0",
    version2="1.1.0"
)
```

## Monitoring and Metrics

Track model performance in production:

```python
from app.ml.monitoring.metrics_tracker import MLMetricsTracker

# Initialize tracker
tracker = MLMetricsTracker()

# Log predictions
tracker.log_prediction(
    model_name="pattern_detector",
    model_version="1.0.0",
    ticker="AAPL",
    prediction=1,
    probability=0.85,
    features=features_dict
)

# Log actual outcomes
tracker.log_actual_outcome(
    prediction_id="pred_12345",
    actual_label=1,
    success_metric=12.5  # % gain
)

# Compute accuracy over time
accuracy_metrics = tracker.compute_accuracy_over_time(
    model_name="pattern_detector",
    model_version="1.0.0",
    days=30
)

# Detect data drift
drift_metrics = tracker.detect_data_drift(
    model_name="pattern_detector",
    baseline_days=30,
    recent_days=7
)
```

## Performance Metrics

The system tracks comprehensive metrics:

**Classification Metrics:**
- Accuracy
- Precision
- Recall
- F1 Score
- AUC-ROC
- Confusion Matrix

**Trading Metrics:**
- Win Rate
- Average Return
- Total Return
- Sharpe Ratio
- Max Return
- Min Return

**Pattern-Specific Metrics:**
- Performance by pattern type
- False positive analysis
- False negative analysis

## Hyperparameter Tuning

Automated hyperparameter tuning using Grid Search or Random Search:

```python
# Tune Random Forest
best_model, best_params = pipeline.tune_hyperparameters(
    model_type='rf',
    X_train=X_train,
    y_train=y_train,
    search_method='random',
    n_iter=20,
    cv_folds=5
)

# Tune XGBoost
best_model, best_params = pipeline.tune_hyperparameters(
    model_type='xgboost',
    X_train=X_train,
    y_train=y_train,
    search_method='grid',
    cv_folds=5
)
```

## Manual Labeling

For supervised learning with manual labels:

```python
from app.ml.data.manual_labeler import ManualLabeler

# Initialize labeler
labeler = ManualLabeler()

# Add manual labels
labeler.add_label(
    ticker="AAPL",
    pattern_type="VCP",
    window_start="2020-01-01",
    window_end="2020-03-01",
    label=1,  # Successful pattern
    notes="Clean VCP with volume contraction",
    quality_score=5
)

# Create labeling batch
labeler.create_labeling_batch(
    pattern_data=detected_patterns,
    batch_size=50
)

# Import labeled batch
labeler.import_labeled_batch('path/to/labeled_batch.json')
```

## Testing

Run comprehensive tests:

```bash
# Run all ML tests
pytest tests/test_ml_models.py -v

# Run specific test
pytest tests/test_ml_models.py::test_ensemble_training -v

# Run with coverage
pytest tests/test_ml_models.py --cov=app/ml --cov-report=html
```

## Directory Structure

```
data/
├── ml_training/          # Training data
│   ├── labeled_patterns_*.json
│   └── manual_labels.json
└── market_data/          # Historical market data

models/
├── random_forest/        # RF models
├── xgboost/             # XGBoost models
├── neural_network/      # NN models
├── ensemble/            # Ensemble models
└── registry/            # Model registry

results/
├── training/            # Training results
├── backtesting/         # Backtest results
└── comparison/          # Model comparisons

metrics/
└── ml/                  # ML metrics
    ├── predictions.jsonl
    ├── outcomes.jsonl
    ├── daily_metrics.json
    └── drift_metrics.json
```

## Best Practices

1. **Data Collection**: Collect diverse patterns across multiple tickers and time periods
2. **Feature Engineering**: Use domain knowledge to create meaningful features
3. **Train/Val/Test Split**: Always use proper data splitting (70/15/15)
4. **Cross-Validation**: Use k-fold CV to ensure model robustness
5. **Hyperparameter Tuning**: Tune hyperparameters on validation set
6. **Ensemble Methods**: Combine multiple models for better performance
7. **Monitoring**: Track model performance in production
8. **Drift Detection**: Monitor for data drift and retrain when needed
9. **Version Control**: Use model registry for version management
10. **Backtesting**: Always backtest on out-of-sample data

## Troubleshooting

**Issue: Model not training**
- Check data quality and sufficient samples
- Verify features are computed correctly
- Check for NaN values in features

**Issue: Poor performance**
- Collect more training data
- Tune hyperparameters
- Add more relevant features
- Try different model types

**Issue: Data drift detected**
- Retrain model with recent data
- Update feature engineering
- Adjust model parameters

## Future Enhancements

- [ ] Online learning for continuous model updates
- [ ] Multi-timeframe pattern detection
- [ ] Sector-specific models
- [ ] Reinforcement learning for optimal entry/exit
- [ ] SHAP values for feature importance
- [ ] AutoML for hyperparameter optimization
- [ ] Model ensembling with different architectures
- [ ] Real-time prediction streaming

## License

See main project LICENSE file.

## Support

For issues or questions, please create an issue in the GitHub repository.
