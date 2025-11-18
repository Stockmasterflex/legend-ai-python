"""
ML Training Platform Usage Examples

This script demonstrates how to use the ML training platform for:
1. Data preparation and feature engineering
2. Model selection and training
3. Hyperparameter tuning
4. Model evaluation
5. Model deployment and A/B testing
"""

import pandas as pd
import numpy as np
from sklearn.datasets import make_classification, make_regression

from app.ml import (
    DataPreparation,
    ModelSelector,
    TrainingDashboard,
    ModelEvaluator,
    ModelDeployment,
)


def example_classification():
    """Example: Classification task with complete pipeline"""
    print("=" * 80)
    print("CLASSIFICATION EXAMPLE")
    print("=" * 80)

    # 1. Generate sample data
    print("\n1. Generating sample classification data...")
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        random_state=42,
    )

    # Convert to DataFrame
    feature_names = [f"feature_{i}" for i in range(20)]
    df = pd.DataFrame(X, columns=feature_names)
    df["target"] = y

    print(f"   Dataset shape: {df.shape}")
    print(f"   Target distribution: {df['target'].value_counts().to_dict()}")

    # 2. Data Preparation
    print("\n2. Data Preparation...")
    data_prep = DataPreparation()

    # Clean data
    df_clean = data_prep.clean_data(
        df,
        missing_strategy="mean",
        outlier_method="iqr",
        outlier_threshold=3.0,
    )

    # Feature selection
    X = df_clean.drop(columns=["target"])
    y = df_clean["target"]

    X_selected, selected_features = data_prep.select_features(
        X,
        y,
        method="tree_importance",
        n_features=10,
        task_type="classification",
    )

    print(f"   Selected {len(selected_features)} features: {selected_features[:5]}...")

    # Split data
    X_train, X_val, X_test, y_train, y_val, y_test = data_prep.split_data(
        X_selected,
        y,
        test_size=0.2,
        validation_size=0.1,
        stratify=True,
    )

    # Scale features
    X_train_scaled = data_prep.scale_features(X_train, method="standard", fit=True)
    X_val_scaled = data_prep.scale_features(X_val, method="standard", fit=False)
    X_test_scaled = data_prep.scale_features(X_test, method="standard", fit=False)

    print(f"   Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")

    # 3. Model Selection and Comparison
    print("\n3. Comparing different models...")
    model_selector = ModelSelector(task_type="classification")

    comparison = model_selector.compare_models(
        X_train_scaled,
        y_train,
        models=["random_forest", "xgboost", "logistic"],
        cv=5,
    )

    print(f"\n   Model Comparison:\n{comparison}")

    # 4. Hyperparameter Tuning
    print("\n4. Hyperparameter tuning (Random Forest)...")
    tuning_results = model_selector.random_search(
        X_train_scaled,
        y_train,
        model_name="random_forest",
        n_iter=20,
        cv=3,
    )

    print(f"   Best parameters: {tuning_results['best_params']}")
    print(f"   Best CV score: {tuning_results['best_score']:.4f}")

    # 5. Training with Monitoring
    print("\n5. Training final model with monitoring...")
    dashboard = TrainingDashboard(
        task_type="classification",
        metric="accuracy",
        patience=10,
    )

    best_model = model_selector.best_model
    best_model = dashboard.train_with_monitoring(
        best_model,
        X_train_scaled,
        y_train,
        X_val_scaled,
        y_val,
    )

    training_summary = dashboard.get_summary()
    print(f"   Training time: {training_summary['training_time_seconds']:.2f}s")
    print(f"   Best score: {training_summary['best_score']:.4f}")

    # 6. Model Evaluation
    print("\n6. Evaluating model on test set...")
    evaluator = ModelEvaluator(task_type="classification")

    y_pred = best_model.predict(X_test_scaled)
    y_pred_proba = best_model.predict_proba(X_test_scaled)

    eval_results = evaluator.evaluate(
        y_test.values,
        y_pred,
        y_pred_proba,
    )

    print(f"   Accuracy: {eval_results['accuracy']:.4f}")
    print(f"   F1-Score: {eval_results['weighted_avg_f1']:.4f}")
    print(f"   ROC-AUC: {eval_results.get('roc_auc', 'N/A')}")

    # Generate evaluation report
    print("\n" + evaluator.generate_evaluation_report())

    # 7. Model Deployment
    print("\n7. Deploying model...")
    deployment = ModelDeployment(models_dir="models")

    model_id = deployment.save_model(
        model=best_model,
        name="classification_model",
        version="1.0.0",
        task_type="classification",
        algorithm="random_forest",
        metrics=eval_results,
        hyperparameters=tuning_results["best_params"],
        feature_names=selected_features,
        target_name="target",
        training_samples=len(X_train),
        description="Example classification model",
        tags=["example", "classification"],
    )

    print(f"   Model deployed: {model_id}")

    # Promote to production
    deployment.promote_to_production(model_id)
    print(f"   Model promoted to production")

    # 8. Make Predictions
    print("\n8. Making predictions with deployed model...")
    loaded_model, metadata = deployment.load_model(model_id)

    # Make predictions on a few test samples
    sample_predictions = loaded_model.predict(X_test_scaled[:5])
    print(f"   Sample predictions: {sample_predictions}")

    print("\n" + "=" * 80)
    print("Classification example completed successfully!")
    print("=" * 80)


def example_regression():
    """Example: Regression task"""
    print("\n" + "=" * 80)
    print("REGRESSION EXAMPLE")
    print("=" * 80)

    # 1. Generate sample data
    print("\n1. Generating sample regression data...")
    X, y = make_regression(
        n_samples=1000,
        n_features=15,
        n_informative=10,
        noise=0.1,
        random_state=42,
    )

    feature_names = [f"feature_{i}" for i in range(15)]
    df = pd.DataFrame(X, columns=feature_names)
    df["target"] = y

    print(f"   Dataset shape: {df.shape}")

    # 2. Data Preparation
    print("\n2. Data Preparation...")
    data_prep = DataPreparation()

    X = df.drop(columns=["target"])
    y = df["target"]

    # Split data
    X_train, X_test, y_train, y_test = data_prep.split_data(
        X, y, test_size=0.2
    )

    # Scale features
    X_train_scaled = data_prep.scale_features(X_train, method="standard", fit=True)
    X_test_scaled = data_prep.scale_features(X_test, method="standard", fit=False)

    # 3. Model Training
    print("\n3. Training regression model...")
    model_selector = ModelSelector(task_type="regression")

    # Compare models
    comparison = model_selector.compare_models(
        X_train_scaled,
        y_train,
        models=["random_forest", "xgboost", "ridge"],
        cv=5,
    )

    print(f"\n   Model Comparison:\n{comparison}")

    # Train best model
    best_model_name = comparison.iloc[0]["model"]
    model = model_selector.models[best_model_name]
    model.fit(X_train_scaled, y_train)

    # 4. Evaluation
    print("\n4. Evaluating model...")
    evaluator = ModelEvaluator(task_type="regression")

    y_pred = model.predict(X_test_scaled)
    eval_results = evaluator.evaluate(y_test.values, y_pred)

    print(f"   R² Score: {eval_results['r2']:.4f}")
    print(f"   RMSE: {eval_results['rmse']:.4f}")
    print(f"   MAE: {eval_results['mae']:.4f}")

    print("\n" + evaluator.generate_evaluation_report())

    print("\n" + "=" * 80)
    print("Regression example completed successfully!")
    print("=" * 80)


def example_ensemble():
    """Example: Ensemble methods"""
    print("\n" + "=" * 80)
    print("ENSEMBLE METHODS EXAMPLE")
    print("=" * 80)

    # Generate data
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)

    feature_names = [f"feature_{i}" for i in range(20)]
    X_df = pd.DataFrame(X, columns=feature_names)

    # Split data
    data_prep = DataPreparation()
    X_train, X_test, y_train, y_test = data_prep.split_data(
        X_df, pd.Series(y), test_size=0.2
    )

    # 1. Voting Ensemble
    print("\n1. Creating Voting Ensemble...")
    model_selector = ModelSelector(task_type="classification")

    voting_ensemble = model_selector.create_voting_ensemble(
        models=["random_forest", "xgboost", "logistic"],
        voting="soft",
    )

    voting_ensemble.fit(X_train, y_train)
    voting_score = voting_ensemble.score(X_test, y_test)
    print(f"   Voting Ensemble Accuracy: {voting_score:.4f}")

    # 2. Stacking Ensemble
    print("\n2. Creating Stacking Ensemble...")
    stacking_ensemble = model_selector.create_stacking_ensemble(
        base_models=["random_forest", "xgboost"],
        meta_model="logistic",
        cv=3,
    )

    stacking_ensemble.fit(X_train, y_train)
    stacking_score = stacking_ensemble.score(X_test, y_test)
    print(f"   Stacking Ensemble Accuracy: {stacking_score:.4f}")

    print("\n" + "=" * 80)
    print("Ensemble methods example completed successfully!")
    print("=" * 80)


def example_ab_testing():
    """Example: A/B testing between models"""
    print("\n" + "=" * 80)
    print("A/B TESTING EXAMPLE")
    print("=" * 80)

    # Generate data
    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    feature_names = [f"feature_{i}" for i in range(20)]
    X_df = pd.DataFrame(X, columns=feature_names)

    # Train two different models
    data_prep = DataPreparation()
    X_train, X_test, y_train, y_test = data_prep.split_data(
        X_df, pd.Series(y), test_size=0.2
    )

    model_selector = ModelSelector(task_type="classification")

    # Model A: Random Forest
    model_a = model_selector.models["random_forest"]
    model_a.fit(X_train, y_train)

    # Model B: XGBoost
    model_b = model_selector.models["xgboost"]
    model_b.fit(X_train, y_train)

    # Deploy both models
    deployment = ModelDeployment(models_dir="models")

    evaluator = ModelEvaluator(task_type="classification")

    # Deploy Model A
    y_pred_a = model_a.predict(X_test)
    eval_a = evaluator.evaluate(y_test.values, y_pred_a)

    model_a_id = deployment.save_model(
        model=model_a,
        name="ab_test_model",
        version="1.0.0",
        task_type="classification",
        algorithm="random_forest",
        metrics=eval_a,
        hyperparameters={},
        feature_names=feature_names,
        target_name="target",
        training_samples=len(X_train),
        description="Model A for A/B test",
    )

    # Deploy Model B
    y_pred_b = model_b.predict(X_test)
    eval_b = evaluator.evaluate(y_test.values, y_pred_b)

    model_b_id = deployment.save_model(
        model=model_b,
        name="ab_test_model",
        version="2.0.0",
        task_type="classification",
        algorithm="xgboost",
        metrics=eval_b,
        hyperparameters={},
        feature_names=feature_names,
        target_name="target",
        training_samples=len(X_train),
        description="Model B for A/B test",
    )

    # Setup A/B test
    print("\n1. Setting up A/B test...")
    ab_config = deployment.setup_ab_test(
        model_a_id=model_a_id,
        model_b_id=model_b_id,
        test_name="model_comparison_test",
        split_ratio=0.5,
    )

    print(f"   A/B test created: {ab_config['test_name']}")
    print(f"   Model A accuracy: {eval_a['accuracy']:.4f}")
    print(f"   Model B accuracy: {eval_b['accuracy']:.4f}")

    # Make predictions with A/B test
    print("\n2. Making predictions with A/B test...")
    for i in range(5):
        predictions, model_used = deployment.predict_ab_test(
            test_name="model_comparison_test",
            X=X_test.iloc[[i]],
            user_id=f"user_{i}",
        )
        print(f"   User {i}: Model {model_used.split('_')[-1][:8]} -> Prediction: {predictions[0]}")

    print("\n" + "=" * 80)
    print("A/B testing example completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    # Run all examples
    example_classification()
    print("\n" * 2)

    example_regression()
    print("\n" * 2)

    example_ensemble()
    print("\n" * 2)

    example_ab_testing()

    print("\n" * 2)
    print("=" * 80)
    print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
    print("=" * 80)
