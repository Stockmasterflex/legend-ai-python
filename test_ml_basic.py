"""
Basic ML Platform Test (No pytest required)
"""

import sys
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification

# Import ML modules
from app.ml import (
    DataPreparation,
    ModelSelector,
    ModelEvaluator,
    ModelDeployment,
)


def test_data_preparation():
    """Test data preparation"""
    print("\n" + "=" * 80)
    print("TEST 1: Data Preparation")
    print("=" * 80)

    # Generate data
    X, y = make_classification(n_samples=200, n_features=10, random_state=42)
    feature_names = [f"feature_{i}" for i in range(10)]
    df = pd.DataFrame(X, columns=feature_names)
    df["target"] = y

    print(f"✓ Generated dataset: {df.shape}")

    # Test data cleaning
    data_prep = DataPreparation()
    df_clean = data_prep.clean_data(df, missing_strategy="mean")
    print(f"✓ Data cleaned: {df_clean.shape}")

    # Test feature selection
    X = df_clean.drop(columns=["target"])
    y = df_clean["target"]

    X_selected, features = data_prep.select_features(
        X, y, method="tree_importance", n_features=5
    )
    print(f"✓ Feature selection: {len(features)} features selected")
    print(f"  Selected features: {features}")

    # Test data splitting
    X_train, X_test, y_train, y_test = data_prep.split_data(
        X_selected, y, test_size=0.2, stratify=True
    )
    print(f"✓ Data split: Train={len(X_train)}, Test={len(X_test)}")

    # Test feature scaling
    X_train_scaled = data_prep.scale_features(X_train, method="standard", fit=True)
    X_test_scaled = data_prep.scale_features(X_test, method="standard", fit=False)
    print(f"✓ Feature scaling: Mean={X_train_scaled.mean().mean():.3f}, Std={X_train_scaled.std().mean():.3f}")

    print("\n✅ Data Preparation Test PASSED")
    return True


def test_model_selection():
    """Test model selection"""
    print("\n" + "=" * 80)
    print("TEST 2: Model Selection")
    print("=" * 80)

    # Generate data
    X, y = make_classification(n_samples=200, n_features=10, random_state=42)
    df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(10)])

    print(f"✓ Generated dataset: {df.shape}")

    # Test model comparison
    model_selector = ModelSelector(task_type="classification")
    print(f"✓ Model selector initialized with {len(model_selector.models)} models")

    comparison = model_selector.compare_models(
        df, pd.Series(y), models=["random_forest", "logistic"], cv=3
    )
    print(f"✓ Model comparison complete:")
    print(comparison.to_string())

    # Test voting ensemble
    ensemble = model_selector.create_voting_ensemble(
        models=["random_forest", "logistic"]
    )
    print(f"✓ Voting ensemble created")

    print("\n✅ Model Selection Test PASSED")
    return True


def test_model_training():
    """Test model training and evaluation"""
    print("\n" + "=" * 80)
    print("TEST 3: Model Training and Evaluation")
    print("=" * 80)

    # Generate data
    X, y = make_classification(n_samples=200, n_features=10, random_state=42)
    df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(10)])

    print(f"✓ Generated dataset: {df.shape}")

    # Split data
    data_prep = DataPreparation()
    X_train, X_test, y_train, y_test = data_prep.split_data(
        df, pd.Series(y), test_size=0.2
    )

    # Train model
    model_selector = ModelSelector(task_type="classification")
    model = model_selector.models["random_forest"]
    model.fit(X_train, y_train)
    print(f"✓ Model trained: Random Forest")

    # Evaluate
    evaluator = ModelEvaluator(task_type="classification")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)

    results = evaluator.evaluate(y_test.values, y_pred, y_pred_proba)
    print(f"✓ Model evaluated:")
    print(f"  Accuracy: {results['accuracy']:.4f}")
    print(f"  F1-Score: {results['weighted_avg_f1']:.4f}")

    print("\n✅ Model Training Test PASSED")
    return True


def test_model_deployment():
    """Test model deployment"""
    print("\n" + "=" * 80)
    print("TEST 4: Model Deployment")
    print("=" * 80)

    # Generate data
    X, y = make_classification(n_samples=200, n_features=10, random_state=42)
    df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(10)])

    print(f"✓ Generated dataset: {df.shape}")

    # Train model
    data_prep = DataPreparation()
    X_train, X_test, y_train, y_test = data_prep.split_data(
        df, pd.Series(y), test_size=0.2
    )

    model_selector = ModelSelector(task_type="classification")
    model = model_selector.models["random_forest"]
    model.fit(X_train, y_train)

    # Deploy model
    deployment = ModelDeployment(models_dir="models_test")

    model_id = deployment.save_model(
        model=model,
        name="test_model",
        version="1.0.0",
        task_type="classification",
        algorithm="random_forest",
        metrics={"accuracy": 0.95},
        hyperparameters={},
        feature_names=df.columns.tolist(),
        target_name="target",
        training_samples=len(X_train),
    )
    print(f"✓ Model saved: {model_id}")

    # Load model
    loaded_model, metadata = deployment.load_model(model_id)
    print(f"✓ Model loaded: {metadata.name} v{metadata.version}")

    # Make predictions
    predictions = loaded_model.predict(X_test[:5])
    print(f"✓ Predictions made: {predictions}")

    # Promote to production
    deployment.promote_to_production(model_id)
    print(f"✓ Model promoted to production")

    # List models
    models = deployment.list_models(name="test_model")
    print(f"✓ Listed {len(models)} models")

    print("\n✅ Model Deployment Test PASSED")
    return True


def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("ML TRAINING PLATFORM - BASIC TESTS")
    print("=" * 80)

    tests = [
        test_data_preparation,
        test_model_selection,
        test_model_training,
        test_model_deployment,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"\n❌ Test FAILED with error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")

    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
