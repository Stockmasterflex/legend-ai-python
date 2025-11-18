"""
Machine Learning Integration for Backtesting
Feature engineering, model training, hyperparameter optimization, and ensemble methods
"""

from .features import FeatureEngineer, TechnicalFeatures, PriceFeatures, VolumeFeatures
from .models import MLModel, ModelTrainer
from .optimization import HyperparameterOptimizer, OptimizationType
from .ensemble import EnsembleModel, EnsembleType

__all__ = [
    "FeatureEngineer",
    "TechnicalFeatures",
    "PriceFeatures",
    "VolumeFeatures",
    "MLModel",
    "ModelTrainer",
    "HyperparameterOptimizer",
    "OptimizationType",
    "EnsembleModel",
    "EnsembleType",
]
