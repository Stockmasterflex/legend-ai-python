"""
Database Models for ML Training Platform
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class TaskType(str, enum.Enum):
    """ML task types"""
    CLASSIFICATION = "classification"
    REGRESSION = "regression"


class TrainingStatus(str, enum.Enum):
    """Training job status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class MLTrainingJob(Base):
    """Training job records"""
    __tablename__ = "ml_training_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    task_type = Column(Enum(TaskType), nullable=False)
    algorithm = Column(String, nullable=False)
    status = Column(Enum(TrainingStatus), default=TrainingStatus.PENDING, nullable=False)

    # Data configuration
    dataset_name = Column(String)
    feature_columns = Column(JSON)  # List of feature column names
    target_column = Column(String)
    train_samples = Column(Integer)
    test_samples = Column(Integer)
    validation_samples = Column(Integer)

    # Model configuration
    hyperparameters = Column(JSON)  # Model hyperparameters
    data_preprocessing = Column(JSON)  # Preprocessing configuration

    # Training results
    best_score = Column(Float)
    best_epoch = Column(Integer)
    training_time_seconds = Column(Float)
    evaluation_metrics = Column(JSON)  # All evaluation metrics

    # Model information
    model_id = Column(String)  # Reference to deployed model
    model_path = Column(String)  # Path to saved model file

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    error_message = Column(Text)

    # User/creator
    created_by = Column(String)

    # Additional info
    tags = Column(JSON)  # List of tags
    notes = Column(Text)


class MLExperiment(Base):
    """Experiment tracking for hyperparameter tuning"""
    __tablename__ = "ml_experiments"

    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)

    # Related training job
    training_job_id = Column(String, index=True)

    # Experiment configuration
    search_method = Column(String)  # grid_search, random_search, optuna
    param_space = Column(JSON)  # Parameter search space
    n_trials = Column(Integer)  # Number of trials/iterations

    # Results
    best_params = Column(JSON)
    best_score = Column(Float)
    all_trials = Column(JSON)  # All trial results

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))

    # User
    created_by = Column(String)


class MLModelVersion(Base):
    """Model version tracking"""
    __tablename__ = "ml_model_versions"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False, index=True)
    version = Column(String, nullable=False)

    # Model info
    algorithm = Column(String)
    task_type = Column(Enum(TaskType))

    # Training info
    training_job_id = Column(String, index=True)
    training_samples = Column(Integer)
    feature_names = Column(JSON)
    target_name = Column(String)

    # Performance metrics
    metrics = Column(JSON)
    hyperparameters = Column(JSON)

    # Deployment info
    status = Column(String)  # staged, production, archived
    deployed_at = Column(DateTime(timezone=True))
    archived_at = Column(DateTime(timezone=True))

    # File info
    file_path = Column(String)
    file_size_bytes = Column(Integer)
    checksum = Column(String)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(String)
    description = Column(Text)
    tags = Column(JSON)


class MLPredictionLog(Base):
    """Log predictions for monitoring and A/B testing"""
    __tablename__ = "ml_prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(String, unique=True, index=True)

    # Model info
    model_id = Column(String, index=True)
    model_version = Column(String)

    # A/B testing
    ab_test_name = Column(String, index=True)
    ab_test_variant = Column(String)  # 'A' or 'B'

    # Input/Output
    input_features = Column(JSON)
    prediction = Column(JSON)  # Can be single value or array
    prediction_proba = Column(JSON)  # Prediction probabilities if available

    # Performance
    inference_time_ms = Column(Float)

    # Ground truth (if available for evaluation)
    true_value = Column(JSON)
    is_correct = Column(Boolean)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(String, index=True)
    session_id = Column(String)


class MLDataset(Base):
    """Dataset registry for ML training"""
    __tablename__ = "ml_datasets"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)

    # Dataset info
    file_path = Column(String)
    file_size_bytes = Column(Integer)
    row_count = Column(Integer)
    column_count = Column(Integer)

    # Schema
    columns_info = Column(JSON)  # Column names, types, stats
    target_column = Column(String)
    task_type = Column(Enum(TaskType))

    # Statistics
    missing_values = Column(JSON)  # Missing value counts per column
    class_distribution = Column(JSON)  # For classification tasks

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String)
    tags = Column(JSON)
    is_active = Column(Boolean, default=True)


class MLFeatureStore(Base):
    """Feature engineering and storage"""
    __tablename__ = "ml_feature_store"

    id = Column(Integer, primary_key=True, index=True)
    feature_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)

    # Feature definition
    feature_type = Column(String)  # numerical, categorical, text, etc.
    transformation = Column(JSON)  # Transformation logic/code
    dependencies = Column(JSON)  # List of source columns

    # Statistics
    statistics = Column(JSON)  # Mean, std, min, max, etc.
    importance_score = Column(Float)

    # Usage tracking
    used_in_models = Column(JSON)  # List of model IDs using this feature
    usage_count = Column(Integer, default=0)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(String)
    is_active = Column(Boolean, default=True)
