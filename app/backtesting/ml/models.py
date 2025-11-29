"""
ML Model Types and Configurations
Defines available model types for ML-based trading strategies
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


class ModelType(str, Enum):
    """Available ML model types for trading"""
    
    # Classification Models
    LOGISTIC_REGRESSION = "logistic_regression"
    RANDOM_FOREST = "random_forest"
    GRADIENT_BOOSTING = "gradient_boosting"
    XGB_CLASSIFIER = "xgb_classifier"
    LIGHTGBM_CLASSIFIER = "lightgbm_classifier"
    SVM = "svm"
    
    # Regression Models
    LINEAR_REGRESSION = "linear_regression"
    RIDGE = "ridge"
    LASSO = "lasso"
    ELASTIC_NET = "elastic_net"
    XGB_REGRESSOR = "xgb_regressor"
    LIGHTGBM_REGRESSOR = "lightgbm_regressor"
    
    # Neural Networks
    MLP = "mlp"
    LSTM = "lstm"
    TRANSFORMER = "transformer"
    
    # Ensemble Methods
    VOTING = "voting"
    STACKING = "stacking"
    BAGGING = "bagging"
    
    # Specialized Trading Models
    REINFORCEMENT_LEARNING = "reinforcement_learning"
    SIGNAL_CLASSIFIER = "signal_classifier"
    REGIME_DETECTOR = "regime_detector"


@dataclass
class ModelConfig:
    """Configuration for ML models"""
    model_type: ModelType
    hyperparameters: Dict[str, Any] = field(default_factory=dict)
    feature_columns: List[str] = field(default_factory=list)
    target_column: str = "target"
    train_test_split: float = 0.8
    validation_split: float = 0.1
    use_cross_validation: bool = True
    cv_folds: int = 5
    random_seed: int = 42
    early_stopping: bool = True
    early_stopping_rounds: int = 10


# Default hyperparameter spaces for optimization
DEFAULT_PARAM_SPACES: Dict[ModelType, Dict[str, List[Any]]] = {
    ModelType.RANDOM_FOREST: {
        "n_estimators": [50, 100, 200, 500],
        "max_depth": [3, 5, 10, 15, 20, None],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "max_features": ["sqrt", "log2", None],
    },
    ModelType.GRADIENT_BOOSTING: {
        "n_estimators": [50, 100, 200],
        "learning_rate": [0.01, 0.05, 0.1, 0.2],
        "max_depth": [3, 5, 7],
        "min_samples_split": [2, 5, 10],
        "subsample": [0.7, 0.8, 0.9, 1.0],
    },
    ModelType.XGB_CLASSIFIER: {
        "n_estimators": [50, 100, 200, 500],
        "learning_rate": [0.01, 0.05, 0.1, 0.2],
        "max_depth": [3, 5, 7, 9],
        "min_child_weight": [1, 3, 5],
        "subsample": [0.7, 0.8, 0.9],
        "colsample_bytree": [0.7, 0.8, 0.9],
        "gamma": [0, 0.1, 0.2],
    },
    ModelType.LIGHTGBM_CLASSIFIER: {
        "n_estimators": [50, 100, 200, 500],
        "learning_rate": [0.01, 0.05, 0.1],
        "max_depth": [3, 5, 7, -1],
        "num_leaves": [15, 31, 63, 127],
        "min_child_samples": [10, 20, 50],
        "subsample": [0.7, 0.8, 0.9],
        "colsample_bytree": [0.7, 0.8, 0.9],
    },
    ModelType.LOGISTIC_REGRESSION: {
        "C": [0.001, 0.01, 0.1, 1, 10],
        "penalty": ["l1", "l2"],
        "solver": ["lbfgs", "liblinear", "saga"],
        "max_iter": [100, 500, 1000],
    },
    ModelType.SVM: {
        "C": [0.1, 1, 10, 100],
        "kernel": ["rbf", "linear", "poly"],
        "gamma": ["scale", "auto", 0.01, 0.1],
    },
    ModelType.MLP: {
        "hidden_layer_sizes": [(64,), (128,), (64, 32), (128, 64), (128, 64, 32)],
        "activation": ["relu", "tanh"],
        "learning_rate_init": [0.001, 0.01, 0.1],
        "alpha": [0.0001, 0.001, 0.01],
        "batch_size": [32, 64, 128],
    },
    ModelType.LSTM: {
        "units": [32, 64, 128],
        "layers": [1, 2, 3],
        "dropout": [0.1, 0.2, 0.3],
        "learning_rate": [0.001, 0.01],
        "batch_size": [32, 64],
        "sequence_length": [10, 20, 50],
    },
}


def get_default_params(model_type: ModelType) -> Dict[str, List[Any]]:
    """Get default hyperparameter space for a model type"""
    return DEFAULT_PARAM_SPACES.get(model_type, {})


def get_model_description(model_type: ModelType) -> str:
    """Get human-readable description of model type"""
    descriptions = {
        ModelType.LOGISTIC_REGRESSION: "Binary classification using logistic function. Good baseline for signal prediction.",
        ModelType.RANDOM_FOREST: "Ensemble of decision trees. Robust, handles non-linear relationships well.",
        ModelType.GRADIENT_BOOSTING: "Sequential ensemble building. Often achieves best performance on tabular data.",
        ModelType.XGB_CLASSIFIER: "Extreme Gradient Boosting. Fast, regularized, handles missing values.",
        ModelType.LIGHTGBM_CLASSIFIER: "Light Gradient Boosting. Very fast training, memory efficient.",
        ModelType.SVM: "Support Vector Machine. Good for high-dimensional feature spaces.",
        ModelType.MLP: "Multi-Layer Perceptron. Neural network for complex patterns.",
        ModelType.LSTM: "Long Short-Term Memory. Best for sequential/time-series patterns.",
        ModelType.TRANSFORMER: "Attention-based architecture. State-of-the-art for sequence modeling.",
        ModelType.REINFORCEMENT_LEARNING: "Learn optimal trading policy through trial and error.",
        ModelType.SIGNAL_CLASSIFIER: "Specialized model for buy/sell/hold signal classification.",
        ModelType.REGIME_DETECTOR: "Identify market regimes (bull/bear/sideways) for adaptive strategies.",
    }
    return descriptions.get(model_type, "No description available.")


def get_model_complexity(model_type: ModelType) -> str:
    """Get complexity rating for model type"""
    complexity = {
        ModelType.LOGISTIC_REGRESSION: "low",
        ModelType.LINEAR_REGRESSION: "low",
        ModelType.RIDGE: "low",
        ModelType.LASSO: "low",
        ModelType.ELASTIC_NET: "low",
        ModelType.SVM: "medium",
        ModelType.RANDOM_FOREST: "medium",
        ModelType.GRADIENT_BOOSTING: "medium",
        ModelType.XGB_CLASSIFIER: "medium",
        ModelType.XGB_REGRESSOR: "medium",
        ModelType.LIGHTGBM_CLASSIFIER: "medium",
        ModelType.LIGHTGBM_REGRESSOR: "medium",
        ModelType.MLP: "high",
        ModelType.LSTM: "high",
        ModelType.TRANSFORMER: "high",
        ModelType.REINFORCEMENT_LEARNING: "high",
        ModelType.VOTING: "medium",
        ModelType.STACKING: "high",
        ModelType.BAGGING: "medium",
        ModelType.SIGNAL_CLASSIFIER: "medium",
        ModelType.REGIME_DETECTOR: "medium",
    }
    return complexity.get(model_type, "unknown")
