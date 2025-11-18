"""
ML Training Platform Module

This module provides comprehensive machine learning capabilities including:
- Data preparation and feature engineering
- Model selection and hyperparameter tuning
- Real-time training monitoring
- Model evaluation and metrics
- Model deployment and versioning
"""

from .data_preparation import DataPreparation
from .model_selection import ModelSelector
from .training import TrainingDashboard
from .evaluation import ModelEvaluator
from .deployment import ModelDeployment

__all__ = [
    "DataPreparation",
    "ModelSelector",
    "TrainingDashboard",
    "ModelEvaluator",
    "ModelDeployment",
]
