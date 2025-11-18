"""
Tests for ML Training Platform
"""

import pytest
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


@pytest.fixture
def classification_data():
    """Generate sample classification data"""
    X, y = make_classification(
        n_samples=200,
        n_features=10,
        n_informative=7,
        n_redundant=3,
        random_state=42,
    )
    feature_names = [f"feature_{i}" for i in range(10)]
    df = pd.DataFrame(X, columns=feature_names)
    df["target"] = y
    return df


@pytest.fixture
def regression_data():
    """Generate sample regression data"""
    X, y = make_regression(
        n_samples=200,
        n_features=10,
        n_informative=7,
        noise=0.1,
        random_state=42,
    )
    feature_names = [f"feature_{i}" for i in range(10)]
    df = pd.DataFrame(X, columns=feature_names)
    df["target"] = y
    return df


class TestDataPreparation:
    """Test data preparation functionality"""

    def test_clean_data(self, classification_data):
        """Test data cleaning"""
        data_prep = DataPreparation()

        # Add some missing values
        df = classification_data.copy()
        df.loc[0:5, "feature_0"] = np.nan

        # Clean data
        df_clean = data_prep.clean_data(df, missing_strategy="mean")

        assert df_clean.isnull().sum().sum() == 0
        assert len(df_clean) <= len(df)

    def test_feature_selection(self, classification_data):
        """Test feature selection"""
        data_prep = DataPreparation()

        X = classification_data.drop(columns=["target"])
        y = classification_data["target"]

        X_selected, features = data_prep.select_features(
            X, y, method="tree_importance", n_features=5
        )

        assert len(features) == 5
        assert X_selected.shape[1] == 5

    def test_data_split(self, classification_data):
        """Test train/test split"""
        data_prep = DataPreparation()

        X = classification_data.drop(columns=["target"])
        y = classification_data["target"]

        X_train, X_test, y_train, y_test = data_prep.split_data(
            X, y, test_size=0.2, stratify=True
        )

        assert len(X_train) + len(X_test) == len(X)
        assert len(y_train) + len(y_test) == len(y)

    def test_feature_scaling(self, classification_data):
        """Test feature scaling"""
        data_prep = DataPreparation()

        X = classification_data.drop(columns=["target"])

        X_scaled = data_prep.scale_features(X, method="standard", fit=True)

        # Check that mean is approximately 0 and std is approximately 1
        assert np.abs(X_scaled.mean().mean()) < 0.1
        assert np.abs(X_scaled.std().mean() - 1.0) < 0.1


class TestModelSelection:
    """Test model selection functionality"""

    def test_compare_models_classification(self, classification_data):
        """Test model comparison for classification"""
        X = classification_data.drop(columns=["target"])
        y = classification_data["target"]

        model_selector = ModelSelector(task_type="classification")
        comparison = model_selector.compare_models(
            X, y, models=["random_forest", "logistic"], cv=3
        )

        assert len(comparison) == 2
        assert "mean_score" in comparison.columns

    def test_compare_models_regression(self, regression_data):
        """Test model comparison for regression"""
        X = regression_data.drop(columns=["target"])
        y = regression_data["target"]

        model_selector = ModelSelector(task_type="regression")
        comparison = model_selector.compare_models(
            X, y, models=["random_forest", "ridge"], cv=3
        )

        assert len(comparison) == 2
        assert "mean_score" in comparison.columns

    def test_voting_ensemble(self, classification_data):
        """Test voting ensemble creation"""
        X = classification_data.drop(columns=["target"])
        y = classification_data["target"]

        model_selector = ModelSelector(task_type="classification")
        ensemble = model_selector.create_voting_ensemble(
            models=["random_forest", "logistic"]
        )

        ensemble.fit(X, y)
        predictions = ensemble.predict(X[:10])

        assert len(predictions) == 10

    def test_stacking_ensemble(self, classification_data):
        """Test stacking ensemble creation"""
        X = classification_data.drop(columns=["target"])
        y = classification_data["target"]

        model_selector = ModelSelector(task_type="classification")
        ensemble = model_selector.create_stacking_ensemble(
            base_models=["random_forest", "logistic"], cv=2
        )

        ensemble.fit(X, y)
        predictions = ensemble.predict(X[:10])

        assert len(predictions) == 10


class TestTrainingDashboard:
    """Test training dashboard functionality"""

    def test_training_monitoring(self, classification_data):
        """Test training with monitoring"""
        X = classification_data.drop(columns=["target"])
        y = classification_data["target"]

        # Split data
        data_prep = DataPreparation()
        X_train, X_test, y_train, y_test = data_prep.split_data(X, y, test_size=0.2)

        # Train with monitoring
        model_selector = ModelSelector(task_type="classification")
        dashboard = TrainingDashboard(task_type="classification", patience=5)

        model = model_selector.models["random_forest"]
        trained_model = dashboard.train_with_monitoring(model, X_train, y_train)

        # Check training history
        history = dashboard.get_history_dataframe()
        assert len(history) > 0

        summary = dashboard.get_summary()
        assert "total_epochs" in summary
        assert "training_time_seconds" in summary


class TestModelEvaluator:
    """Test model evaluation functionality"""

    def test_classification_evaluation(self, classification_data):
        """Test classification evaluation"""
        X = classification_data.drop(columns=["target"])
        y = classification_data["target"]

        # Train a simple model
        data_prep = DataPreparation()
        X_train, X_test, y_train, y_test = data_prep.split_data(X, y, test_size=0.2)

        model_selector = ModelSelector(task_type="classification")
        model = model_selector.models["random_forest"]
        model.fit(X_train, y_train)

        # Evaluate
        evaluator = ModelEvaluator(task_type="classification")
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)

        results = evaluator.evaluate(y_test.values, y_pred, y_pred_proba)

        assert "accuracy" in results
        assert "weighted_avg_f1" in results
        assert "confusion_matrix" in results

    def test_regression_evaluation(self, regression_data):
        """Test regression evaluation"""
        X = regression_data.drop(columns=["target"])
        y = regression_data["target"]

        # Train a simple model
        data_prep = DataPreparation()
        X_train, X_test, y_train, y_test = data_prep.split_data(X, y, test_size=0.2)

        model_selector = ModelSelector(task_type="regression")
        model = model_selector.models["random_forest"]
        model.fit(X_train, y_train)

        # Evaluate
        evaluator = ModelEvaluator(task_type="regression")
        y_pred = model.predict(X_test)

        results = evaluator.evaluate(y_test.values, y_pred)

        assert "r2" in results
        assert "rmse" in results
        assert "mae" in results

    def test_evaluation_report(self, classification_data):
        """Test evaluation report generation"""
        X = classification_data.drop(columns=["target"])
        y = classification_data["target"]

        data_prep = DataPreparation()
        X_train, X_test, y_train, y_test = data_prep.split_data(X, y, test_size=0.2)

        model_selector = ModelSelector(task_type="classification")
        model = model_selector.models["random_forest"]
        model.fit(X_train, y_train)

        evaluator = ModelEvaluator(task_type="classification")
        y_pred = model.predict(X_test)
        evaluator.evaluate(y_test.values, y_pred)

        report = evaluator.generate_evaluation_report()

        assert "MODEL EVALUATION REPORT" in report
        assert "Accuracy" in report


class TestModelDeployment:
    """Test model deployment functionality"""

    def test_save_and_load_model(self, classification_data, tmp_path):
        """Test model save and load"""
        X = classification_data.drop(columns=["target"])
        y = classification_data["target"]

        # Train a model
        data_prep = DataPreparation()
        X_train, X_test, y_train, y_test = data_prep.split_data(X, y, test_size=0.2)

        model_selector = ModelSelector(task_type="classification")
        model = model_selector.models["random_forest"]
        model.fit(X_train, y_train)

        # Save model
        deployment = ModelDeployment(models_dir=str(tmp_path))

        model_id = deployment.save_model(
            model=model,
            name="test_model",
            version="1.0.0",
            task_type="classification",
            algorithm="random_forest",
            metrics={"accuracy": 0.95},
            hyperparameters={},
            feature_names=X.columns.tolist(),
            target_name="target",
            training_samples=len(X_train),
        )

        # Load model
        loaded_model, metadata = deployment.load_model(model_id)

        # Verify
        assert metadata.model_id == model_id
        assert metadata.name == "test_model"
        assert metadata.version == "1.0.0"

        # Test predictions
        predictions = loaded_model.predict(X_test)
        assert len(predictions) == len(X_test)

    def test_model_promotion(self, classification_data, tmp_path):
        """Test model promotion to production"""
        X = classification_data.drop(columns=["target"])
        y = classification_data["target"]

        data_prep = DataPreparation()
        X_train, X_test, y_train, y_test = data_prep.split_data(X, y, test_size=0.2)

        model_selector = ModelSelector(task_type="classification")
        model = model_selector.models["random_forest"]
        model.fit(X_train, y_train)

        deployment = ModelDeployment(models_dir=str(tmp_path))

        model_id = deployment.save_model(
            model=model,
            name="promotion_test",
            version="1.0.0",
            task_type="classification",
            algorithm="random_forest",
            metrics={"accuracy": 0.95},
            hyperparameters={},
            feature_names=X.columns.tolist(),
            target_name="target",
            training_samples=len(X_train),
        )

        # Promote to production
        deployment.promote_to_production(model_id)

        # Verify
        _, metadata = deployment.load_model(model_id)
        from app.ml.deployment import ModelStatus

        assert metadata.status == ModelStatus.PRODUCTION

    def test_model_versioning(self, classification_data, tmp_path):
        """Test model versioning"""
        X = classification_data.drop(columns=["target"])
        y = classification_data["target"]

        data_prep = DataPreparation()
        X_train, X_test, y_train, y_test = data_prep.split_data(X, y, test_size=0.2)

        model_selector = ModelSelector(task_type="classification")
        model = model_selector.models["random_forest"]
        model.fit(X_train, y_train)

        deployment = ModelDeployment(models_dir=str(tmp_path))

        # Save version 1.0.0
        model_id_v1 = deployment.save_model(
            model=model,
            name="versioned_model",
            version="1.0.0",
            task_type="classification",
            algorithm="random_forest",
            metrics={"accuracy": 0.90},
            hyperparameters={},
            feature_names=X.columns.tolist(),
            target_name="target",
            training_samples=len(X_train),
        )

        # Save version 2.0.0
        model_id_v2 = deployment.save_model(
            model=model,
            name="versioned_model",
            version="2.0.0",
            task_type="classification",
            algorithm="random_forest",
            metrics={"accuracy": 0.95},
            hyperparameters={},
            feature_names=X.columns.tolist(),
            target_name="target",
            training_samples=len(X_train),
        )

        # List all versions
        models = deployment.list_models(name="versioned_model")

        assert len(models) == 2
        assert model_id_v1 != model_id_v2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
