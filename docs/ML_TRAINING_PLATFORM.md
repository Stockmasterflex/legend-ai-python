# ML Training Platform Documentation

## Overview

The ML Training Platform provides a comprehensive solution for training, evaluating, and deploying custom machine learning models. It includes tools for data preparation, model selection, hyperparameter tuning, real-time training monitoring, and model deployment with A/B testing capabilities.

## Features

### 1. Data Preparation
- **Data Cleaning**: Handle missing values, outliers, and data quality issues
- **Feature Selection**: Multiple methods including correlation, mutual information, RFE, and tree-based importance
- **Feature Scaling**: StandardScaler, MinMaxScaler, RobustScaler
- **Data Splitting**: Train/test/validation splits with stratification support
- **Cross-Validation**: K-Fold, Stratified K-Fold, Time Series Split

### 2. Model Selection
- **Algorithms Supported**:
  - **Classification**: Random Forest, XGBoost, LightGBM, Logistic Regression, SVM, Decision Tree, KNN, Naive Bayes, Gradient Boosting, AdaBoost
  - **Regression**: Random Forest, XGBoost, LightGBM, Ridge, Lasso, ElasticNet, SVR, Decision Tree, KNN, Gradient Boosting, AdaBoost
- **Ensemble Methods**: Voting, Stacking, Bagging
- **Hyperparameter Tuning**: Grid Search, Random Search, Optuna (Bayesian Optimization)

### 3. Training Dashboard
- Real-time training progress monitoring
- Loss curves visualization
- Validation metrics tracking
- Early stopping with configurable patience
- Training time and performance metrics

### 4. Model Evaluation
- **Classification Metrics**: Accuracy, Precision, Recall, F1-Score, ROC-AUC, Confusion Matrix
- **Regression Metrics**: R², RMSE, MAE, MAPE, Explained Variance
- **Visualizations**: Confusion Matrix, ROC Curve, Precision-Recall Curve, Feature Importance, Residual Plots
- Prediction examples and error analysis

### 5. Model Deployment
- Save and load trained models
- Model versioning and metadata tracking
- Model status management (Training, Staged, Production, Archived)
- Promote/demote models
- Rollback to previous versions
- A/B testing between models
- Model comparison and benchmarking

## Architecture

```
app/ml/
├── __init__.py              # Package initialization
├── data_preparation.py      # Data cleaning and feature engineering
├── model_selection.py       # Model selection and hyperparameter tuning
├── training.py              # Training dashboard and monitoring
├── evaluation.py            # Model evaluation and metrics
├── deployment.py            # Model deployment and versioning
└── models.py                # Database models
```

## API Endpoints

### Data Management

#### Upload Dataset
```http
POST /api/ml/datasets/upload
Content-Type: multipart/form-data

Body:
- file: CSV or Excel file
- name: Dataset name (optional)
- target_column: Target variable name (optional)

Response:
{
  "dataset_id": "uuid",
  "name": "dataset.csv",
  "rows": 1000,
  "columns": 20,
  "column_names": [...],
  "missing_values": {...}
}
```

#### Get Dataset Info
```http
GET /api/ml/datasets/{dataset_id}

Response:
{
  "dataset_id": "uuid",
  "rows": 1000,
  "columns": 20,
  "column_names": [...],
  "dtypes": {...},
  "missing_values": {...},
  "numeric_stats": {...}
}
```

#### List Datasets
```http
GET /api/ml/datasets

Response: Array of dataset summaries
```

### Data Preparation

#### Clean Data
```http
POST /api/ml/data/clean

Body:
{
  "dataset_id": "uuid",
  "missing_strategy": "mean",  // mean, median, mode, drop, forward_fill, backward_fill
  "outlier_method": "iqr",     // iqr, zscore, none
  "outlier_threshold": 3.0
}

Response:
{
  "status": "success",
  "cleaned_dataset_id": "uuid",
  "original_rows": 1000,
  "cleaned_rows": 980
}
```

#### Select Features
```http
POST /api/ml/data/select-features

Body:
{
  "dataset_id": "uuid",
  "target_column": "target",
  "method": "tree_importance",  // correlation, mutual_info, rfe, tree_importance, statistical
  "n_features": 10,
  "task_type": "classification"
}

Response:
{
  "status": "success",
  "selected_features": [...],
  "feature_importance": [...]
}
```

#### Split Data
```http
POST /api/ml/data/split

Body:
{
  "dataset_id": "uuid",
  "target_column": "target",
  "test_size": 0.2,
  "validation_size": 0.1,
  "stratify": true
}

Response:
{
  "status": "success",
  "train_samples": 700,
  "validation_samples": 100,
  "test_samples": 200
}
```

### Model Training

#### Train Model
```http
POST /api/ml/models/train

Body:
{
  "dataset_id": "uuid",
  "target_column": "target",
  "task_type": "classification",
  "algorithm": "random_forest",
  "hyperparameters": {...},
  "test_size": 0.2,
  "validation_size": 0.1,
  "scaling_method": "standard",
  "feature_selection": {
    "method": "tree_importance",
    "n_features": 10
  },
  "early_stopping": true,
  "early_stopping_patience": 10
}

Response:
{
  "status": "success",
  "job_id": "uuid",
  "message": "Training job started"
}
```

#### Get Training Job Status
```http
GET /api/ml/models/train/{job_id}

Response:
{
  "job_id": "uuid",
  "status": "completed",  // pending, running, completed, failed
  "created_at": "2024-01-01T00:00:00",
  "completed_at": "2024-01-01T00:05:00",
  "results": {
    "evaluation": {...},
    "training_history": [...],
    "training_summary": {...}
  }
}
```

#### Compare Models
```http
POST /api/ml/models/compare

Body:
{
  "dataset_id": "uuid",
  "target_column": "target",
  "task_type": "classification",
  "models": ["random_forest", "xgboost", "logistic"],
  "cv": 5
}

Response:
{
  "status": "success",
  "comparison": [
    {
      "model": "xgboost",
      "mean_score": 0.95,
      "std_score": 0.02
    },
    ...
  ]
}
```

#### Hyperparameter Tuning
```http
POST /api/ml/models/tune

Body:
{
  "dataset_id": "uuid",
  "target_column": "target",
  "task_type": "classification",
  "algorithm": "random_forest",
  "tuning_method": "optuna",  // grid_search, random_search, optuna
  "n_trials": 100,
  "cv": 5
}

Response:
{
  "status": "success",
  "job_id": "uuid",
  "message": "Hyperparameter tuning job started"
}
```

### Model Deployment

#### Deploy Model
```http
POST /api/ml/models/deploy

Body:
{
  "training_job_id": "uuid",
  "model_name": "my_model",
  "version": "1.0.0",
  "description": "Model description",
  "tags": ["production", "v1"],
  "promote_to_production": true
}

Response:
{
  "status": "success",
  "model_id": "uuid",
  "message": "Model deployed successfully"
}
```

#### List Deployed Models
```http
GET /api/ml/models/deployed?name=my_model&status=production

Response:
{
  "status": "success",
  "models": [
    {
      "model_id": "uuid",
      "name": "my_model",
      "version": "1.0.0",
      "algorithm": "random_forest",
      "status": "production",
      "created_at": "2024-01-01T00:00:00",
      "metrics": {...}
    }
  ]
}
```

#### Promote Model
```http
POST /api/ml/models/{model_id}/promote

Response:
{
  "status": "success",
  "message": "Model promoted to production"
}
```

#### Rollback Model
```http
POST /api/ml/models/{model_name}/rollback?to_version=1.0.0

Response:
{
  "status": "success",
  "model_id": "uuid",
  "message": "Rolled back to model uuid"
}
```

#### Create A/B Test
```http
POST /api/ml/models/ab-test

Body:
{
  "model_a_id": "uuid_a",
  "model_b_id": "uuid_b",
  "test_name": "model_comparison",
  "split_ratio": 0.5
}

Response:
{
  "status": "success",
  "config": {...}
}
```

#### Make Prediction
```http
POST /api/ml/models/predict

Body:
{
  "model_id": "uuid",  // OR ab_test_name
  "features": {
    "feature_1": 1.0,
    "feature_2": 2.0,
    ...
  },
  "user_id": "user123"  // For A/B testing
}

Response:
{
  "status": "success",
  "model_id": "uuid",
  "prediction": [1],
  "prediction_proba": [[0.2, 0.8]]
}
```

## Python SDK Usage

### Basic Classification Example

```python
from app.ml import DataPreparation, ModelSelector, TrainingDashboard, ModelEvaluator, ModelDeployment
import pandas as pd

# 1. Load data
df = pd.read_csv("data.csv")
X = df.drop(columns=["target"])
y = df["target"]

# 2. Data Preparation
data_prep = DataPreparation()

# Clean data
df_clean = data_prep.clean_data(df, missing_strategy="mean")
X = df_clean.drop(columns=["target"])
y = df_clean["target"]

# Select features
X_selected, features = data_prep.select_features(
    X, y, method="tree_importance", n_features=10
)

# Split data
X_train, X_val, X_test, y_train, y_val, y_test = data_prep.split_data(
    X_selected, y, test_size=0.2, validation_size=0.1, stratify=True
)

# Scale features
X_train = data_prep.scale_features(X_train, method="standard", fit=True)
X_val = data_prep.scale_features(X_val, method="standard", fit=False)
X_test = data_prep.scale_features(X_test, method="standard", fit=False)

# 3. Model Selection
model_selector = ModelSelector(task_type="classification")

# Compare models
comparison = model_selector.compare_models(
    X_train, y_train, models=["random_forest", "xgboost"], cv=5
)
print(comparison)

# Hyperparameter tuning
results = model_selector.optuna_search(
    X_train, y_train, model_name="random_forest", n_trials=100
)
print(f"Best params: {results['best_params']}")

# 4. Training with Monitoring
dashboard = TrainingDashboard(task_type="classification", patience=10)
model = dashboard.train_with_monitoring(
    model_selector.best_model, X_train, y_train, X_val, y_val
)

# 5. Evaluation
evaluator = ModelEvaluator(task_type="classification")
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)

eval_results = evaluator.evaluate(y_test, y_pred, y_pred_proba)
print(evaluator.generate_evaluation_report())

# Plot evaluation metrics
evaluator.plot_confusion_matrix(y_test, y_pred, save_path="confusion_matrix.png")
evaluator.plot_roc_curve(y_test, y_pred_proba[:, 1], save_path="roc_curve.png")

# 6. Deployment
deployment = ModelDeployment(models_dir="models")
model_id = deployment.save_model(
    model=model,
    name="my_classifier",
    version="1.0.0",
    task_type="classification",
    algorithm="random_forest",
    metrics=eval_results,
    hyperparameters=results["best_params"],
    feature_names=features,
    target_name="target",
    training_samples=len(X_train),
)

# Promote to production
deployment.promote_to_production(model_id)

# Make predictions
loaded_model, metadata = deployment.load_model(model_id)
predictions = loaded_model.predict(X_test)
```

### Regression Example

```python
# Similar to classification, but use task_type="regression"
model_selector = ModelSelector(task_type="regression")
dashboard = TrainingDashboard(task_type="regression")
evaluator = ModelEvaluator(task_type="regression")

# The API is the same, but metrics will be R², RMSE, MAE, etc.
```

### Ensemble Methods

```python
# Voting Ensemble
voting_ensemble = model_selector.create_voting_ensemble(
    models=["random_forest", "xgboost", "logistic"],
    voting="soft"
)
voting_ensemble.fit(X_train, y_train)

# Stacking Ensemble
stacking_ensemble = model_selector.create_stacking_ensemble(
    base_models=["random_forest", "xgboost"],
    meta_model="logistic",
    cv=3
)
stacking_ensemble.fit(X_train, y_train)
```

### A/B Testing

```python
# Setup A/B test
ab_config = deployment.setup_ab_test(
    model_a_id="model_a_id",
    model_b_id="model_b_id",
    test_name="my_ab_test",
    split_ratio=0.5
)

# Make predictions with A/B test
predictions, model_used = deployment.predict_ab_test(
    test_name="my_ab_test",
    X=X_test,
    user_id="user123"
)
```

## Database Models

The platform includes the following database models for tracking:

- **MLTrainingJob**: Training job records and status
- **MLExperiment**: Hyperparameter tuning experiments
- **MLModelVersion**: Model version tracking
- **MLPredictionLog**: Prediction logging for monitoring
- **MLDataset**: Dataset registry
- **MLFeatureStore**: Feature engineering and storage

## Dependencies

```
scikit-learn==1.5.2
xgboost==2.1.3
lightgbm==4.5.0
matplotlib==3.9.3
seaborn==0.13.2
joblib==1.4.2
optuna==4.1.0
pandas==2.2.3
numpy==1.26.4
```

## Best Practices

1. **Data Preparation**:
   - Always clean your data before training
   - Use appropriate feature scaling for algorithms that require it
   - Select relevant features to improve model performance and reduce overfitting

2. **Model Selection**:
   - Compare multiple algorithms before settling on one
   - Use cross-validation to get robust performance estimates
   - Tune hyperparameters for better performance

3. **Training**:
   - Monitor training progress with the dashboard
   - Use early stopping to prevent overfitting
   - Keep validation set separate from test set

4. **Evaluation**:
   - Evaluate on a held-out test set
   - Look at multiple metrics, not just accuracy
   - Analyze prediction errors and edge cases

5. **Deployment**:
   - Version your models
   - Test new models in staging before promoting to production
   - Use A/B testing to compare models in production
   - Monitor model performance over time
   - Keep rollback capability for quick recovery

## Troubleshooting

### Common Issues

1. **Memory errors**: Reduce batch size or use sampling for large datasets
2. **Slow training**: Use faster algorithms or reduce hyperparameter search space
3. **Poor performance**: Try different feature engineering, algorithms, or hyperparameters
4. **Overfitting**: Use regularization, reduce model complexity, or get more data

## Support

For issues or questions, please check the documentation or contact the development team.
