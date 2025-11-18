"""
ML Training Platform API Endpoints
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd
import numpy as np
import uuid
import io
import logging

from app.ml import (
    DataPreparation,
    ModelSelector,
    TrainingDashboard,
    ModelEvaluator,
    ModelDeployment,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ml", tags=["ML Training"])

# Global instances
data_prep = DataPreparation()
deployment = ModelDeployment()

# In-memory storage for training jobs (in production, use database)
training_jobs: Dict[str, Dict] = {}
datasets: Dict[str, pd.DataFrame] = {}


# ============================================================================
# Pydantic Models
# ============================================================================

class DataCleaningRequest(BaseModel):
    dataset_id: str
    missing_strategy: str = Field(default="mean", description="mean, median, mode, drop, forward_fill, backward_fill")
    outlier_method: str = Field(default="iqr", description="iqr, zscore, none")
    outlier_threshold: float = 3.0


class FeatureSelectionRequest(BaseModel):
    dataset_id: str
    target_column: str
    method: str = Field(default="correlation", description="correlation, mutual_info, rfe, tree_importance, statistical")
    n_features: Optional[int] = None
    task_type: str = "classification"
    threshold: float = 0.1


class DataSplitRequest(BaseModel):
    dataset_id: str
    target_column: str
    test_size: float = 0.2
    validation_size: Optional[float] = None
    stratify: bool = False
    random_state: int = 42


class ModelTrainingRequest(BaseModel):
    dataset_id: str
    target_column: str
    task_type: str = Field(default="classification", description="classification or regression")
    algorithm: str = Field(default="random_forest", description="Model algorithm")
    hyperparameters: Optional[Dict[str, Any]] = None
    test_size: float = 0.2
    validation_size: Optional[float] = None
    scaling_method: Optional[str] = Field(default="standard", description="standard, minmax, robust, none")
    feature_selection: Optional[Dict[str, Any]] = None
    cross_validation: Optional[int] = None
    early_stopping: bool = True
    early_stopping_patience: int = 10


class HyperparameterTuningRequest(BaseModel):
    dataset_id: str
    target_column: str
    task_type: str = "classification"
    algorithm: str = "random_forest"
    tuning_method: str = Field(default="grid_search", description="grid_search, random_search, optuna")
    param_grid: Optional[Dict[str, List]] = None
    n_iter: int = 50  # For random_search
    n_trials: int = 100  # For optuna
    cv: int = 5
    scoring: Optional[str] = None


class ModelComparisonRequest(BaseModel):
    dataset_id: str
    target_column: str
    task_type: str = "classification"
    models: List[str]
    cv: int = 5
    scoring: Optional[str] = None


class ModelDeploymentRequest(BaseModel):
    training_job_id: str
    model_name: str
    version: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    promote_to_production: bool = False


class ABTestRequest(BaseModel):
    model_a_id: str
    model_b_id: str
    test_name: str
    split_ratio: float = 0.5


class PredictionRequest(BaseModel):
    model_id: Optional[str] = None
    ab_test_name: Optional[str] = None
    features: Dict[str, Any]
    user_id: Optional[str] = None


# ============================================================================
# Data Management Endpoints
# ============================================================================

@router.post("/datasets/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    name: Optional[str] = None,
    target_column: Optional[str] = None,
):
    """Upload a dataset for ML training"""
    try:
        # Read file
        contents = await file.read()

        # Determine file type and read accordingly
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Use CSV or Excel.")

        # Generate dataset ID
        dataset_id = str(uuid.uuid4())
        datasets[dataset_id] = df

        # Get dataset info
        dataset_info = {
            "dataset_id": dataset_id,
            "name": name or file.filename,
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "target_column": target_column,
            "dtypes": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "sample_data": df.head(5).to_dict(orient="records"),
        }

        logger.info(f"Dataset uploaded: {dataset_id}")
        return dataset_info

    except Exception as e:
        logger.error(f"Error uploading dataset: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/datasets/{dataset_id}")
async def get_dataset_info(dataset_id: str):
    """Get information about a dataset"""
    if dataset_id not in datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")

    df = datasets[dataset_id]

    return {
        "dataset_id": dataset_id,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "numeric_stats": df.describe().to_dict(),
    }


@router.get("/datasets")
async def list_datasets():
    """List all uploaded datasets"""
    return [
        {
            "dataset_id": dataset_id,
            "rows": len(df),
            "columns": len(df.columns),
        }
        for dataset_id, df in datasets.items()
    ]


# ============================================================================
# Data Preparation Endpoints
# ============================================================================

@router.post("/data/clean")
async def clean_data(request: DataCleaningRequest):
    """Clean data by handling missing values and outliers"""
    if request.dataset_id not in datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        df = datasets[request.dataset_id].copy()

        cleaned_df = data_prep.clean_data(
            df,
            missing_strategy=request.missing_strategy,
            outlier_method=request.outlier_method,
            outlier_threshold=request.outlier_threshold,
        )

        # Store cleaned dataset
        cleaned_id = f"{request.dataset_id}_cleaned"
        datasets[cleaned_id] = cleaned_df

        return {
            "status": "success",
            "original_dataset_id": request.dataset_id,
            "cleaned_dataset_id": cleaned_id,
            "original_rows": len(df),
            "cleaned_rows": len(cleaned_df),
            "rows_removed": len(df) - len(cleaned_df),
        }

    except Exception as e:
        logger.error(f"Error cleaning data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/data/select-features")
async def select_features(request: FeatureSelectionRequest):
    """Select important features using various methods"""
    if request.dataset_id not in datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        df = datasets[request.dataset_id].copy()

        if request.target_column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Target column '{request.target_column}' not found")

        X = df.drop(columns=[request.target_column])
        y = df[request.target_column]

        # Select only numeric columns
        X_numeric = X.select_dtypes(include=[np.number])

        X_selected, selected_features = data_prep.select_features(
            X_numeric,
            y,
            method=request.method,
            n_features=request.n_features,
            task_type=request.task_type,
            threshold=request.threshold,
        )

        # Get feature importance report
        importance_report = data_prep.get_feature_importance_report()

        return {
            "status": "success",
            "original_features": len(X_numeric.columns),
            "selected_features": len(selected_features),
            "feature_names": selected_features,
            "feature_importance": importance_report.to_dict(orient="records") if importance_report is not None else None,
        }

    except Exception as e:
        logger.error(f"Error selecting features: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/data/split")
async def split_data(request: DataSplitRequest):
    """Split data into train/test or train/val/test sets"""
    if request.dataset_id not in datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        df = datasets[request.dataset_id].copy()

        if request.target_column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Target column '{request.target_column}' not found")

        X = df.drop(columns=[request.target_column])
        y = df[request.target_column]

        result = data_prep.split_data(
            X,
            y,
            test_size=request.test_size,
            validation_size=request.validation_size,
            stratify=request.stratify,
            random_state=request.random_state,
        )

        if request.validation_size:
            X_train, X_val, X_test, y_train, y_val, y_test = result
            return {
                "status": "success",
                "train_samples": len(X_train),
                "validation_samples": len(X_val),
                "test_samples": len(X_test),
            }
        else:
            X_train, X_test, y_train, y_test = result
            return {
                "status": "success",
                "train_samples": len(X_train),
                "test_samples": len(X_test),
            }

    except Exception as e:
        logger.error(f"Error splitting data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Model Training Endpoints
# ============================================================================

@router.post("/models/train")
async def train_model(request: ModelTrainingRequest, background_tasks: BackgroundTasks):
    """Train a machine learning model"""
    if request.dataset_id not in datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Create training job
    job_id = str(uuid.uuid4())
    training_jobs[job_id] = {
        "job_id": job_id,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "request": request.dict(),
    }

    # Start training in background
    background_tasks.add_task(_train_model_background, job_id, request)

    return {
        "status": "success",
        "job_id": job_id,
        "message": "Training job started",
    }


async def _train_model_background(job_id: str, request: ModelTrainingRequest):
    """Background task for model training"""
    try:
        training_jobs[job_id]["status"] = "running"
        training_jobs[job_id]["started_at"] = datetime.now().isoformat()

        # Get data
        df = datasets[request.dataset_id].copy()

        if request.target_column not in df.columns:
            raise ValueError(f"Target column '{request.target_column}' not found")

        X = df.drop(columns=[request.target_column])
        y = df[request.target_column]

        # Handle categorical columns
        X = data_prep.encode_categorical(X)

        # Select only numeric columns
        X = X.select_dtypes(include=[np.number])

        # Feature selection if requested
        if request.feature_selection:
            X, selected_features = data_prep.select_features(
                X, y,
                **request.feature_selection
            )

        # Split data
        if request.validation_size:
            X_train, X_val, X_test, y_train, y_val, y_test = data_prep.split_data(
                X, y,
                test_size=request.test_size,
                validation_size=request.validation_size,
                stratify=(request.task_type == "classification"),
            )
        else:
            X_train, X_test, y_train, y_test = data_prep.split_data(
                X, y,
                test_size=request.test_size,
                stratify=(request.task_type == "classification"),
            )
            X_val, y_val = None, None

        # Scale features if requested
        if request.scaling_method and request.scaling_method != "none":
            X_train = data_prep.scale_features(X_train, method=request.scaling_method, fit=True)
            X_test = data_prep.scale_features(X_test, method=request.scaling_method, fit=False)
            if X_val is not None:
                X_val = data_prep.scale_features(X_val, method=request.scaling_method, fit=False)

        # Initialize model selector
        model_selector = ModelSelector(task_type=request.task_type)

        # Get model
        if request.algorithm not in model_selector.models:
            raise ValueError(f"Algorithm '{request.algorithm}' not supported")

        model = model_selector.models[request.algorithm]

        # Set hyperparameters if provided
        if request.hyperparameters:
            model.set_params(**request.hyperparameters)

        # Initialize training dashboard
        dashboard = TrainingDashboard(
            task_type=request.task_type,
            patience=request.early_stopping_patience if request.early_stopping else 999,
        )

        # Train model with monitoring
        model = dashboard.train_with_monitoring(
            model, X_train, y_train, X_val, y_val
        )

        # Evaluate model
        evaluator = ModelEvaluator(task_type=request.task_type)

        y_pred = model.predict(X_test)
        y_pred_proba = None
        if hasattr(model, "predict_proba"):
            y_pred_proba = model.predict_proba(X_test)

        eval_results = evaluator.evaluate(
            y_test.values, y_pred, y_pred_proba
        )

        # Store results
        training_jobs[job_id]["status"] = "completed"
        training_jobs[job_id]["completed_at"] = datetime.now().isoformat()
        training_jobs[job_id]["results"] = {
            "model": model,
            "evaluation": eval_results,
            "training_history": dashboard.get_history_dataframe().to_dict(orient="records"),
            "training_summary": dashboard.get_summary(),
            "feature_names": X.columns.tolist(),
        }

        logger.info(f"Training job {job_id} completed successfully")

    except Exception as e:
        logger.error(f"Training job {job_id} failed: {e}")
        training_jobs[job_id]["status"] = "failed"
        training_jobs[job_id]["error"] = str(e)
        training_jobs[job_id]["completed_at"] = datetime.now().isoformat()


@router.get("/models/train/{job_id}")
async def get_training_job(job_id: str):
    """Get training job status and results"""
    if job_id not in training_jobs:
        raise HTTPException(status_code=404, detail="Training job not found")

    job = training_jobs[job_id].copy()

    # Remove model object from response (can't serialize)
    if "results" in job and "model" in job["results"]:
        job["results"] = {k: v for k, v in job["results"].items() if k != "model"}

    return job


@router.post("/models/compare")
async def compare_models(request: ModelComparisonRequest):
    """Compare multiple models using cross-validation"""
    if request.dataset_id not in datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        df = datasets[request.dataset_id].copy()

        if request.target_column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Target column '{request.target_column}' not found")

        X = df.drop(columns=[request.target_column])
        y = df[request.target_column]

        # Encode categorical and select numeric
        X = data_prep.encode_categorical(X)
        X = X.select_dtypes(include=[np.number])

        # Initialize model selector
        model_selector = ModelSelector(task_type=request.task_type)

        # Compare models
        comparison = model_selector.compare_models(
            X, y,
            models=request.models,
            cv=request.cv,
            scoring=request.scoring,
        )

        return {
            "status": "success",
            "comparison": comparison.to_dict(orient="records"),
        }

    except Exception as e:
        logger.error(f"Error comparing models: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/models/tune")
async def tune_hyperparameters(request: HyperparameterTuningRequest, background_tasks: BackgroundTasks):
    """Perform hyperparameter tuning"""
    if request.dataset_id not in datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Create tuning job
    job_id = str(uuid.uuid4())
    training_jobs[job_id] = {
        "job_id": job_id,
        "status": "pending",
        "type": "hyperparameter_tuning",
        "created_at": datetime.now().isoformat(),
        "request": request.dict(),
    }

    # Start tuning in background
    background_tasks.add_task(_tune_hyperparameters_background, job_id, request)

    return {
        "status": "success",
        "job_id": job_id,
        "message": "Hyperparameter tuning job started",
    }


async def _tune_hyperparameters_background(job_id: str, request: HyperparameterTuningRequest):
    """Background task for hyperparameter tuning"""
    try:
        training_jobs[job_id]["status"] = "running"
        training_jobs[job_id]["started_at"] = datetime.now().isoformat()

        # Get data
        df = datasets[request.dataset_id].copy()

        if request.target_column not in df.columns:
            raise ValueError(f"Target column '{request.target_column}' not found")

        X = df.drop(columns=[request.target_column])
        y = df[request.target_column]

        # Encode categorical and select numeric
        X = data_prep.encode_categorical(X)
        X = X.select_dtypes(include=[np.number])

        # Initialize model selector
        model_selector = ModelSelector(task_type=request.task_type)

        # Perform tuning
        if request.tuning_method == "grid_search":
            results = model_selector.grid_search(
                X, y,
                model_name=request.algorithm,
                param_grid=request.param_grid,
                cv=request.cv,
                scoring=request.scoring,
            )
        elif request.tuning_method == "random_search":
            results = model_selector.random_search(
                X, y,
                model_name=request.algorithm,
                param_distributions=request.param_grid,
                n_iter=request.n_iter,
                cv=request.cv,
                scoring=request.scoring,
            )
        elif request.tuning_method == "optuna":
            results = model_selector.optuna_search(
                X, y,
                model_name=request.algorithm,
                n_trials=request.n_trials,
                cv=request.cv,
                scoring=request.scoring,
            )
        else:
            raise ValueError(f"Unknown tuning method: {request.tuning_method}")

        # Store results
        training_jobs[job_id]["status"] = "completed"
        training_jobs[job_id]["completed_at"] = datetime.now().isoformat()
        training_jobs[job_id]["results"] = {
            "best_params": results["best_params"],
            "best_score": results["best_score"],
            "model": model_selector.best_model,
        }

        logger.info(f"Hyperparameter tuning job {job_id} completed successfully")

    except Exception as e:
        logger.error(f"Hyperparameter tuning job {job_id} failed: {e}")
        training_jobs[job_id]["status"] = "failed"
        training_jobs[job_id]["error"] = str(e)
        training_jobs[job_id]["completed_at"] = datetime.now().isoformat()


# ============================================================================
# Model Deployment Endpoints
# ============================================================================

@router.post("/models/deploy")
async def deploy_model(request: ModelDeploymentRequest):
    """Deploy a trained model"""
    if request.training_job_id not in training_jobs:
        raise HTTPException(status_code=404, detail="Training job not found")

    job = training_jobs[request.training_job_id]

    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail="Training job not completed")

    try:
        # Get trained model and results
        model = job["results"]["model"]
        evaluation = job["results"]["evaluation"]
        feature_names = job["results"]["feature_names"]
        training_request = job["request"]

        # Save model
        model_id = deployment.save_model(
            model=model,
            name=request.model_name,
            version=request.version,
            task_type=training_request["task_type"],
            algorithm=training_request["algorithm"],
            metrics=evaluation,
            hyperparameters=training_request.get("hyperparameters", {}),
            feature_names=feature_names,
            target_name=training_request["target_column"],
            training_samples=job["results"]["training_summary"].get("total_epochs", 0),
            description=request.description,
            tags=request.tags,
        )

        # Promote to production if requested
        if request.promote_to_production:
            deployment.promote_to_production(model_id)

        return {
            "status": "success",
            "model_id": model_id,
            "message": "Model deployed successfully",
        }

    except Exception as e:
        logger.error(f"Error deploying model: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/deployed")
async def list_deployed_models(
    name: Optional[str] = None,
    status: Optional[str] = None,
):
    """List deployed models"""
    from app.ml.deployment import ModelStatus

    try:
        status_enum = ModelStatus(status) if status else None
        models = deployment.list_models(name=name, status=status_enum)

        return {
            "status": "success",
            "models": [
                {
                    "model_id": m.model_id,
                    "name": m.name,
                    "version": m.version,
                    "algorithm": m.algorithm,
                    "status": m.status.value,
                    "created_at": m.created_at.isoformat(),
                    "metrics": m.metrics,
                }
                for m in models
            ],
        }

    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/models/{model_id}/promote")
async def promote_model(model_id: str):
    """Promote a model to production"""
    try:
        deployment.promote_to_production(model_id)
        return {
            "status": "success",
            "message": f"Model {model_id} promoted to production",
        }
    except Exception as e:
        logger.error(f"Error promoting model: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/models/{name}/rollback")
async def rollback_model(name: str, to_version: Optional[str] = None):
    """Rollback to a previous model version"""
    try:
        model_id = deployment.rollback_model(name, to_version)

        if model_id:
            return {
                "status": "success",
                "model_id": model_id,
                "message": f"Rolled back to model {model_id}",
            }
        else:
            raise HTTPException(status_code=404, detail="No suitable model found for rollback")

    except Exception as e:
        logger.error(f"Error rolling back model: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/models/ab-test")
async def create_ab_test(request: ABTestRequest):
    """Create an A/B test between two models"""
    try:
        config = deployment.setup_ab_test(
            model_a_id=request.model_a_id,
            model_b_id=request.model_b_id,
            test_name=request.test_name,
            split_ratio=request.split_ratio,
        )

        return {
            "status": "success",
            "config": config,
        }

    except Exception as e:
        logger.error(f"Error creating A/B test: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/models/predict")
async def predict(request: PredictionRequest):
    """Make a prediction using a deployed model or A/B test"""
    try:
        # Convert features dict to DataFrame
        X = pd.DataFrame([request.features])

        if request.ab_test_name:
            # A/B test prediction
            predictions, model_id = deployment.predict_ab_test(
                test_name=request.ab_test_name,
                X=X,
                user_id=request.user_id,
            )
        elif request.model_id:
            # Direct model prediction
            model, metadata = deployment.load_model(request.model_id)
            predictions = model.predict(X)
            model_id = request.model_id
        else:
            raise HTTPException(status_code=400, detail="Must provide either model_id or ab_test_name")

        # Get prediction probabilities if available
        proba = None
        if request.model_id and not request.ab_test_name:
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(X).tolist()

        return {
            "status": "success",
            "model_id": model_id,
            "prediction": predictions.tolist(),
            "prediction_proba": proba,
        }

    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))
