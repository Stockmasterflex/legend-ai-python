"""
Price Forecasting API Endpoints
Provides AI-powered price predictions and forecasting capabilities
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime
import pandas as pd
import numpy as np

from app.services.market_data import market_data_service
from app.ml.price_forecaster import PriceForecastingService
from app.ml.forecast_visualization import ForecastVisualizer
from app.ml.model_performance import PerformanceTracker

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/forecast", tags=["forecasting"])

# Global instances (in production, these would be managed via dependency injection)
forecasting_services = {}  # Cache of trained models


class ForecastRequest(BaseModel):
    """Request model for price forecasting"""
    ticker: str = Field(..., description="Stock ticker symbol", example="AAPL")
    interval: str = Field("1day", description="Time interval", example="1day")
    model_type: str = Field("ensemble", description="Model type: ensemble, lstm, rf, xgboost, lightgbm", example="ensemble")
    forecast_days: int = Field(5, description="Number of days to forecast ahead", ge=1, le=30, example=5)
    return_confidence: bool = Field(True, description="Include confidence intervals")
    return_visualization: bool = Field(False, description="Include chart visualization")

    class Config:
        json_schema_extra = {
            "example": {
                "ticker": "AAPL",
                "interval": "1day",
                "model_type": "ensemble",
                "forecast_days": 5,
                "return_confidence": True,
                "return_visualization": False
            }
        }


class TrainModelRequest(BaseModel):
    """Request model for training a forecast model"""
    ticker: str = Field(..., description="Stock ticker symbol", example="AAPL")
    interval: str = Field("1day", description="Time interval", example="1day")
    model_type: str = Field("ensemble", description="Model type", example="ensemble")
    lookback_days: int = Field(252, description="Days of historical data to use", ge=100, le=1000, example=252)
    test_size: float = Field(0.2, description="Fraction of data for testing", ge=0.1, le=0.4, example=0.2)
    save_model: bool = Field(True, description="Save trained model for future use")

    class Config:
        json_schema_extra = {
            "example": {
                "ticker": "AAPL",
                "interval": "1day",
                "model_type": "ensemble",
                "lookback_days": 252,
                "test_size": 0.2,
                "save_model": True
            }
        }


class ForecastResponse(BaseModel):
    """Response model for forecasting"""
    success: bool = Field(..., description="Whether request was successful")
    ticker: str = Field(..., description="Stock ticker symbol")
    current_price: Optional[float] = Field(None, description="Current stock price")
    forecast_dates: Optional[List[str]] = Field(None, description="Forecast dates")
    forecasted_prices: Optional[List[float]] = Field(None, description="Forecasted prices")
    confidence_lower: Optional[List[float]] = Field(None, description="Lower confidence bound")
    confidence_upper: Optional[List[float]] = Field(None, description="Upper confidence bound")
    predicted_returns: Optional[List[float]] = Field(None, description="Predicted returns (%)")
    model_type: Optional[str] = Field(None, description="Model type used")
    visualization: Optional[Dict[str, Any]] = Field(None, description="Chart visualization data")
    error: Optional[str] = Field(None, description="Error message if failed")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "ticker": "AAPL",
                "current_price": 175.50,
                "forecast_dates": ["2025-01-01", "2025-01-02", "2025-01-03"],
                "forecasted_prices": [176.20, 177.50, 178.10],
                "confidence_lower": [174.00, 175.00, 176.00],
                "confidence_upper": [178.50, 180.00, 180.50],
                "predicted_returns": [0.40, 1.14, 1.48],
                "model_type": "ensemble"
            }
        }


@router.post("/predict", response_model=ForecastResponse)
async def predict_price(request: ForecastRequest):
    """
    Predict future stock prices using AI models

    - **ticker**: Stock symbol to forecast
    - **model_type**: Type of model (ensemble, lstm, rf, xgboost, lightgbm)
    - **forecast_days**: Number of days to forecast ahead
    - **return_confidence**: Include confidence intervals
    """
    try:
        logger.info(f"Forecasting request for {request.ticker} using {request.model_type}")

        # Get historical data
        df = await market_data_service.get_price_data(
            request.ticker,
            interval=request.interval,
            use_fallback=True
        )

        if df is None or len(df) < 100:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient data for {request.ticker}. Need at least 100 data points."
            )

        # Get or create forecasting service
        model_key = f"{request.ticker}_{request.model_type}"

        if model_key not in forecasting_services:
            # Try to load existing model or create new one
            forecaster = PriceForecastingService(
                model_type=request.model_type,
                use_ensemble=(request.model_type == "ensemble")
            )

            try:
                forecaster.load_model(f"{request.ticker}_{request.model_type}")
                logger.info(f"Loaded existing model for {request.ticker}")
            except Exception:
                # Train new model if no saved model exists
                logger.info(f"No saved model found, training new model for {request.ticker}")
                forecaster.train_model(df, save_model=True, model_name=f"{request.ticker}_{request.model_type}")

            forecasting_services[model_key] = forecaster
        else:
            forecaster = forecasting_services[model_key]

        # Make forecast
        forecast_result = forecaster.forecast_future(
            df,
            n_days=request.forecast_days,
            confidence_level=0.9
        )

        # Get current price
        current_price = float(df['close'].iloc[-1])

        # Calculate predicted returns
        forecasted_prices = forecast_result['forecasted_prices']
        predicted_returns = [
            ((price - current_price) / current_price) * 100
            for price in forecasted_prices
        ]

        # Generate visualization if requested
        visualization = None
        if request.return_visualization:
            try:
                visualizer = ForecastVisualizer()
                forecast_dates_dt = [datetime.fromisoformat(d) for d in forecast_result['forecast_dates']]

                viz_result = visualizer.create_probability_cone(
                    historical_prices=df['close'].tail(60),
                    forecast_dates=forecast_dates_dt,
                    forecast_prices=np.array(forecasted_prices),
                    confidence_intervals=[(
                        np.array(forecast_result['confidence_lower']),
                        np.array(forecast_result['confidence_upper'])
                    )],
                    confidence_levels=[0.9],
                    title=f"{request.ticker} Price Forecast"
                )
                visualization = viz_result
            except Exception as viz_error:
                logger.warning(f"Visualization failed: {viz_error}")

        return ForecastResponse(
            success=True,
            ticker=request.ticker,
            current_price=current_price,
            forecast_dates=forecast_result['forecast_dates'],
            forecasted_prices=forecasted_prices,
            confidence_lower=forecast_result.get('confidence_lower'),
            confidence_upper=forecast_result.get('confidence_upper'),
            predicted_returns=predicted_returns,
            model_type=request.model_type,
            visualization=visualization
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Forecast failed for {request.ticker}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Forecasting failed: {str(e)}")


@router.post("/train")
async def train_model(request: TrainModelRequest, background_tasks: BackgroundTasks):
    """
    Train a forecasting model on historical data

    - **ticker**: Stock symbol to train on
    - **model_type**: Type of model to train
    - **lookback_days**: Days of historical data to use for training
    - **save_model**: Whether to save the trained model
    """
    try:
        logger.info(f"Training {request.model_type} model for {request.ticker}")

        # Get historical data
        df = await market_data_service.get_price_data(
            request.ticker,
            interval=request.interval,
            use_fallback=True
        )

        if df is None or len(df) < request.lookback_days:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient data. Have {len(df) if df is not None else 0}, need {request.lookback_days}"
            )

        # Limit to lookback period
        df = df.tail(request.lookback_days)

        # Create and train forecaster
        forecaster = PriceForecastingService(
            model_type=request.model_type,
            use_ensemble=(request.model_type == "ensemble")
        )

        training_metrics = forecaster.train_model(
            df,
            test_size=request.test_size,
            save_model=request.save_model,
            model_name=f"{request.ticker}_{request.model_type}"
        )

        # Cache the trained model
        model_key = f"{request.ticker}_{request.model_type}"
        forecasting_services[model_key] = forecaster

        return {
            "success": True,
            "ticker": request.ticker,
            "model_type": request.model_type,
            "training_metrics": training_metrics,
            "message": f"Model trained successfully on {len(df)} samples"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Training failed for {request.ticker}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")


@router.get("/models")
async def list_models():
    """
    List all currently loaded forecast models
    """
    return {
        "success": True,
        "loaded_models": list(forecasting_services.keys()),
        "count": len(forecasting_services)
    }


@router.get("/model-info/{ticker}/{model_type}")
async def get_model_info(ticker: str, model_type: str):
    """
    Get information about a specific model
    """
    model_key = f"{ticker}_{model_type}"

    if model_key not in forecasting_services:
        raise HTTPException(status_code=404, detail=f"Model not found: {model_key}")

    forecaster = forecasting_services[model_key]
    info = forecaster.get_model_info()

    return {
        "success": True,
        "ticker": ticker,
        "model_info": info
    }


@router.get("/feature-importance/{ticker}/{model_type}")
async def get_feature_importance(ticker: str, model_type: str, top_n: int = 20):
    """
    Get feature importance for a trained model
    """
    model_key = f"{ticker}_{model_type}"

    if model_key not in forecasting_services:
        raise HTTPException(status_code=404, detail=f"Model not found: {model_key}")

    try:
        forecaster = forecasting_services[model_key]
        importance = forecaster.get_feature_importance(top_n=top_n)

        return {
            "success": True,
            "ticker": ticker,
            "model_type": model_type,
            "feature_importance": importance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get feature importance: {str(e)}")


@router.post("/backtest")
async def backtest_model(
    ticker: str,
    model_type: str = "ensemble",
    window_size: int = 100,
    forecast_horizon: int = 1
):
    """
    Perform backtesting on a model

    - **ticker**: Stock symbol
    - **model_type**: Type of model to backtest
    - **window_size**: Size of training window
    - **forecast_horizon**: Days ahead to predict
    """
    try:
        logger.info(f"Backtesting {model_type} model for {ticker}")

        # Get historical data
        df = await market_data_service.get_price_data(
            ticker,
            interval="1day",
            use_fallback=True
        )

        if df is None or len(df) < window_size + forecast_horizon + 50:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient data for backtesting. Need at least {window_size + 50} samples."
            )

        # Create forecaster
        model_key = f"{ticker}_{model_type}"
        if model_key in forecasting_services:
            forecaster = forecasting_services[model_key]
        else:
            # Train a new model
            forecaster = PriceForecastingService(model_type=model_type)
            forecaster.train_model(df.head(window_size))

        # Perform backtest
        tracker = PerformanceTracker()
        backtest_results = tracker.backtest_model(
            forecaster,
            df,
            window_size=window_size,
            forecast_horizon=forecast_horizon,
            step_size=5  # Step 5 days forward each iteration
        )

        # Generate performance report
        report = tracker.generate_performance_report(model_type, backtest_results)

        return {
            "success": True,
            "ticker": ticker,
            "backtest_results": backtest_results,
            "performance_report": report
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Backtesting failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Backtesting failed: {str(e)}")


@router.delete("/model/{ticker}/{model_type}")
async def delete_model(ticker: str, model_type: str):
    """
    Remove a model from cache
    """
    model_key = f"{ticker}_{model_type}"

    if model_key in forecasting_services:
        del forecasting_services[model_key]
        return {
            "success": True,
            "message": f"Model {model_key} removed from cache"
        }
    else:
        raise HTTPException(status_code=404, detail=f"Model not found: {model_key}")
