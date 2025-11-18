"""
API endpoints for ML-based pattern detection.

Provides endpoints for ML pattern detection, model training, and evaluation.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import numpy as np
from datetime import datetime

from app.ml.models.ensemble_model import EnsemblePatternDetector
from app.ml.models.random_forest_model import RandomForestPatternDetector
from app.ml.models.xgboost_model import XGBoostPatternDetector
from app.ml.models.neural_network_model import NeuralNetworkPatternDetector
from app.ml.features.feature_engineering import FeatureEngineer
from app.ml.training.training_pipeline import TrainingPipeline
from app.ml.evaluation.backtesting import Backtester, ModelComparator
from app.ml.data.data_collector import DataCollector
from app.services.market_data import MarketDataService
import pandas as pd


router = APIRouter(prefix="/api/ml", tags=["ML Pattern Detection"])

# Global model instances (loaded from disk)
ensemble_model: Optional[EnsemblePatternDetector] = None
feature_engineer = FeatureEngineer()
market_data_service = MarketDataService()


# Request/Response Models

class MLDetectionRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")
    interval: str = Field(default="1day", description="Time interval")
    model_type: str = Field(default="ensemble", description="Model type: rf, xgboost, nn, ensemble")
    threshold: float = Field(default=0.5, ge=0.0, le=1.0, description="Classification threshold")
    include_rule_based: bool = Field(default=True, description="Include rule-based scores")


class MLDetectionResponse(BaseModel):
    success: bool
    ticker: str
    ml_score: float
    ml_label: int
    confidence: float
    model_type: str
    rule_based_score: Optional[float] = None
    combined_score: Optional[float] = None
    features: Optional[Dict[str, float]] = None
    details: Optional[Dict[str, Any]] = None
    timestamp: str


class TrainingRequest(BaseModel):
    tickers: List[str] = Field(..., description="List of tickers for training data")
    years: int = Field(default=5, ge=1, le=10, description="Years of historical data")
    model_type: str = Field(default="ensemble", description="Model type to train")
    tune_hyperparameters: bool = Field(default=False, description="Enable hyperparameter tuning")
    examples_per_pattern: int = Field(default=100, description="Target examples per pattern type")


class TrainingStatusResponse(BaseModel):
    status: str
    message: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    metrics: Optional[Dict] = None


class ModelInfoResponse(BaseModel):
    model_loaded: bool
    model_type: Optional[str] = None
    n_features: Optional[int] = None
    last_trained: Optional[str] = None
    performance_metrics: Optional[Dict] = None


# Helper Functions

def load_model(model_type: str = "ensemble", model_name: Optional[str] = None):
    """Load a trained model from disk."""
    global ensemble_model

    if model_type == "ensemble":
        ensemble_model = EnsemblePatternDetector()
        if model_name:
            ensemble_model.load(model_name)
        else:
            # Try to load most recent model
            from pathlib import Path
            model_dir = Path('models/ensemble')
            if model_dir.exists():
                json_files = list(model_dir.glob('ensemble_*_metadata.json'))
                if json_files:
                    latest = max(json_files, key=lambda p: p.stat().st_mtime)
                    model_name = latest.stem.replace('_metadata', '')
                    ensemble_model.load(model_name)
                    return True
        return True
    return False


async def compute_ml_score(
    ticker: str,
    interval: str,
    model_type: str,
    threshold: float
) -> Dict:
    """Compute ML pattern detection score for a ticker."""
    # Fetch historical data
    data = await market_data_service.get_historical_data(ticker, interval, outputsize=500)

    if not data or 'values' not in data:
        raise HTTPException(status_code=404, detail="Unable to fetch market data")

    # Convert to DataFrame
    df = pd.DataFrame(data['values'])
    df['datetime'] = pd.to_datetime(df['datetime'])

    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.sort_values('datetime').reset_index(drop=True)

    # Compute features
    features_df = feature_engineer.compute_all_features(df)

    if features_df.empty:
        raise HTTPException(status_code=400, detail="Unable to compute features")

    # Get features from latest data point
    latest_features = features_df.iloc[-1]
    feature_names = feature_engineer.get_feature_names(features_df)
    X = np.array([[latest_features[name] for name in feature_names if name in latest_features.index]])

    # Handle NaN
    X = np.nan_to_num(X, nan=0.0, posinf=1e10, neginf=-1e10)

    # Get ML predictions
    if model_type == "ensemble" and ensemble_model and ensemble_model.is_trained:
        predictions = ensemble_model.predict_with_details(X)
        ml_score = float(predictions['ensemble'][0])
        ml_label = int(predictions['ensemble_labels'][0])

        details = {
            'random_forest_score': float(predictions['random_forest'][0]),
            'xgboost_score': float(predictions['xgboost'][0]),
            'neural_network_score': float(predictions['neural_network'][0])
        }
    else:
        raise HTTPException(status_code=503, detail="ML model not loaded")

    # Extract key features
    feature_dict = {name: float(latest_features[name]) for name in feature_names[:20] if name in latest_features.index}

    return {
        'ml_score': ml_score,
        'ml_label': ml_label,
        'confidence': abs(ml_score - 0.5) * 2,  # Distance from decision boundary
        'features': feature_dict,
        'details': details
    }


# API Endpoints

@router.post("/detect", response_model=MLDetectionResponse)
async def detect_ml_patterns(request: MLDetectionRequest):
    """
    Detect patterns using ML models.

    Returns ML-based pattern detection scores with optional rule-based comparison.
    """
    try:
        # Compute ML score
        ml_result = await compute_ml_score(
            request.ticker,
            request.interval,
            request.model_type,
            request.threshold
        )

        # Optionally combine with rule-based score
        combined_score = None
        rule_based_score = None

        if request.include_rule_based:
            # Import rule-based detector
            from app.core.detectors.vcp_detector import VCPDetector

            # Fetch data for rule-based detection
            data = await market_data_service.get_historical_data(
                request.ticker,
                request.interval,
                outputsize=200
            )

            if data and 'values' in data:
                df = pd.DataFrame(data['values'])
                df['datetime'] = pd.to_datetime(df['datetime'])

                for col in ['open', 'high', 'low', 'close', 'volume']:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

                df = df.sort_values('datetime').reset_index(drop=True)

                # Run rule-based detector
                vcp_detector = VCPDetector()
                result = vcp_detector.detect(df)

                if result:
                    rule_based_score = result.score / 10.0  # Normalize to 0-1

                    # Combine scores (weighted average: 60% ML, 40% rule-based)
                    combined_score = 0.6 * ml_result['ml_score'] + 0.4 * rule_based_score

        return MLDetectionResponse(
            success=True,
            ticker=request.ticker,
            ml_score=ml_result['ml_score'],
            ml_label=ml_result['ml_label'],
            confidence=ml_result['confidence'],
            model_type=request.model_type,
            rule_based_score=rule_based_score,
            combined_score=combined_score,
            features=ml_result['features'],
            details=ml_result['details'],
            timestamp=datetime.now().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting patterns: {str(e)}")


@router.post("/train")
async def train_ml_model(request: TrainingRequest, background_tasks: BackgroundTasks):
    """
    Train ML models on historical data.

    This is a long-running task that runs in the background.
    """
    try:
        # Start training in background
        background_tasks.add_task(
            run_training,
            request.tickers,
            request.years,
            request.model_type,
            request.tune_hyperparameters,
            request.examples_per_pattern
        )

        return TrainingStatusResponse(
            status="started",
            message=f"Training {request.model_type} model on {len(request.tickers)} tickers",
            started_at=datetime.now().isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting training: {str(e)}")


async def run_training(
    tickers: List[str],
    years: int,
    model_type: str,
    tune_hyperparameters: bool,
    examples_per_pattern: int
):
    """Background task to run model training."""
    try:
        # Collect data
        data_collector = DataCollector(market_data_service)
        labeled_patterns = await data_collector.create_labeled_dataset(
            tickers=tickers,
            years=years,
            examples_per_pattern=examples_per_pattern
        )

        if not labeled_patterns:
            print("No labeled patterns collected")
            return

        # Train model
        pipeline = TrainingPipeline()
        train_patterns, val_patterns, test_patterns = pipeline.split_data(labeled_patterns)

        model, metrics = pipeline.train_model(
            model_type=model_type,
            train_patterns=train_patterns,
            val_patterns=val_patterns,
            tune_hyperparameters=tune_hyperparameters
        )

        # Save model
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        model.save(f"{model_type}_trained_{timestamp}")

        # Backtest
        backtester = Backtester()
        X_test, y_test, _ = pipeline.prepare_features(test_patterns)
        backtest_results = backtester.backtest_model(model, X_test, y_test, test_patterns)

        # Save results
        backtester.save_backtest_results(backtest_results, model_type)

        print(f"Training complete for {model_type}")
        print(backtester.generate_report(backtest_results))

    except Exception as e:
        print(f"Error during training: {str(e)}")


@router.get("/model/info", response_model=ModelInfoResponse)
async def get_model_info():
    """Get information about the currently loaded ML model."""
    global ensemble_model

    if ensemble_model is None or not ensemble_model.is_trained:
        return ModelInfoResponse(model_loaded=False)

    return ModelInfoResponse(
        model_loaded=True,
        model_type="ensemble",
        n_features=len(ensemble_model.rf_model.feature_names) if ensemble_model.rf_model.feature_names else None,
        last_trained=None,  # Would need to store this in metadata
        performance_metrics=None  # Would need to load from saved metrics
    )


@router.post("/model/load")
async def load_ml_model(model_name: Optional[str] = None, model_type: str = "ensemble"):
    """Load a trained model from disk."""
    try:
        success = load_model(model_type, model_name)

        if success:
            return {
                "success": True,
                "message": f"Model {model_type} loaded successfully",
                "model_name": model_name or "latest"
            }
        else:
            raise HTTPException(status_code=404, detail="Model not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")


@router.get("/models/list")
async def list_available_models():
    """List all available trained models."""
    from pathlib import Path

    models = {
        'ensemble': [],
        'random_forest': [],
        'xgboost': [],
        'neural_network': []
    }

    # Scan model directories
    for model_type in models.keys():
        model_dir = Path(f'models/{model_type}')
        if model_dir.exists():
            json_files = list(model_dir.glob('*_metadata.json'))
            for json_file in json_files:
                model_name = json_file.stem.replace('_metadata', '')
                models[model_type].append({
                    'name': model_name,
                    'created': datetime.fromtimestamp(json_file.stat().st_mtime).isoformat()
                })

    return models


@router.get("/health")
async def ml_health_check():
    """Health check for ML service."""
    global ensemble_model

    return {
        "status": "healthy",
        "model_loaded": ensemble_model is not None and ensemble_model.is_trained,
        "feature_engineer_ready": feature_engineer is not None,
        "timestamp": datetime.now().isoformat()
    }
