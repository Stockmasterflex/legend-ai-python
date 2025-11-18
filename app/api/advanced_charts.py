"""
Advanced Charting API Endpoints
Provides endpoints for custom chart types, indicators, and analysis
"""

from fastapi import APIRouter, HTTPException, Query, Body
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime, timedelta
import logging

from app.services.market_data import MarketDataService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/charts", tags=["Advanced Charts"])


# Request/Response Models
class ChartDataRequest(BaseModel):
    symbol: str
    timeframe: str = "1h"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    limit: int = 500


class RenkoChartRequest(ChartDataRequest):
    brick_size: Optional[float] = None  # None = ATR
    atr_period: int = 14


class KagiChartRequest(ChartDataRequest):
    reversal_amount: Optional[float] = None  # None = ATR
    reversal_percentage: float = 4.0
    atr_period: int = 14


class PointFigureRequest(ChartDataRequest):
    box_size: Optional[float] = None  # None = ATR
    reversal_boxes: int = 3
    atr_period: int = 14


class MarketProfileRequest(ChartDataRequest):
    tick_size: float = 0.5
    time_per_letter: int = 30  # minutes
    value_area_percent: float = 70.0


class FootprintChartRequest(ChartDataRequest):
    tick_size: float = 0.1
    show_delta: bool = True
    show_imbalance: bool = True
    imbalance_ratio: float = 1.5


class IndicatorRequest(BaseModel):
    symbol: str
    timeframe: str = "1h"
    indicator: str  # SMA, EMA, RSI, MACD, etc.
    parameters: Dict[str, Any] = {}
    limit: int = 500


class CustomIndicatorRequest(BaseModel):
    symbol: str
    timeframe: str = "1h"
    formula: str
    parameters: Dict[str, Any] = {}
    limit: int = 500


class BacktestRequest(BaseModel):
    symbol: str
    timeframe: str = "1h"
    strategy_config: Dict[str, Any]
    start_date: str
    end_date: str
    initial_capital: float = 10000.0


class AlertRequest(BaseModel):
    symbol: str
    alert_type: str  # price_cross, indicator_cross, etc.
    condition: Dict[str, Any]
    message: str
    notification_settings: Dict[str, Any] = {}


# Chart Data Endpoints
@router.post("/data/ohlcv")
async def get_ohlcv_data(request: ChartDataRequest):
    """Get OHLCV data for standard candlestick charts"""
    try:
        market_data = MarketDataService()

        # Parse dates
        end_date = datetime.fromisoformat(request.end_date) if request.end_date else datetime.now()
        start_date = datetime.fromisoformat(request.start_date) if request.start_date else end_date - timedelta(days=30)

        # Fetch data
        data = await market_data.get_historical_data(
            symbol=request.symbol,
            interval=request.timeframe,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat()
        )

        if not data:
            raise HTTPException(status_code=404, detail="No data found for symbol")

        # Limit results
        data = data[-request.limit:]

        return {
            "success": True,
            "symbol": request.symbol,
            "timeframe": request.timeframe,
            "data": data
        }

    except Exception as e:
        logger.error(f"Error fetching OHLCV data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/data/renko")
async def get_renko_data(request: RenkoChartRequest):
    """Get data formatted for Renko charts"""
    try:
        # First get OHLCV data
        ohlcv_response = await get_ohlcv_data(ChartDataRequest(**request.dict()))
        ohlcv_data = ohlcv_response["data"]

        # Return data with Renko configuration
        # Client-side will calculate Renko bricks
        return {
            "success": True,
            "symbol": request.symbol,
            "chart_type": "renko",
            "config": {
                "brick_size": request.brick_size,
                "atr_period": request.atr_period
            },
            "data": ohlcv_data
        }

    except Exception as e:
        logger.error(f"Error fetching Renko data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/data/kagi")
async def get_kagi_data(request: KagiChartRequest):
    """Get data formatted for Kagi charts"""
    try:
        ohlcv_response = await get_ohlcv_data(ChartDataRequest(**request.dict()))
        ohlcv_data = ohlcv_response["data"]

        return {
            "success": True,
            "symbol": request.symbol,
            "chart_type": "kagi",
            "config": {
                "reversal_amount": request.reversal_amount,
                "reversal_percentage": request.reversal_percentage,
                "atr_period": request.atr_period
            },
            "data": ohlcv_data
        }

    except Exception as e:
        logger.error(f"Error fetching Kagi data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/data/point-figure")
async def get_point_figure_data(request: PointFigureRequest):
    """Get data formatted for Point & Figure charts"""
    try:
        ohlcv_response = await get_ohlcv_data(ChartDataRequest(**request.dict()))
        ohlcv_data = ohlcv_response["data"]

        return {
            "success": True,
            "symbol": request.symbol,
            "chart_type": "point-figure",
            "config": {
                "box_size": request.box_size,
                "reversal_boxes": request.reversal_boxes,
                "atr_period": request.atr_period
            },
            "data": ohlcv_data
        }

    except Exception as e:
        logger.error(f"Error fetching Point & Figure data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/data/market-profile")
async def get_market_profile_data(request: MarketProfileRequest):
    """Get data formatted for Market Profile charts"""
    try:
        ohlcv_response = await get_ohlcv_data(ChartDataRequest(**request.dict()))
        ohlcv_data = ohlcv_response["data"]

        return {
            "success": True,
            "symbol": request.symbol,
            "chart_type": "market-profile",
            "config": {
                "tick_size": request.tick_size,
                "time_per_letter": request.time_per_letter,
                "value_area_percent": request.value_area_percent
            },
            "data": ohlcv_data
        }

    except Exception as e:
        logger.error(f"Error fetching Market Profile data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/data/footprint")
async def get_footprint_data(request: FootprintChartRequest):
    """Get data formatted for Footprint charts"""
    try:
        ohlcv_response = await get_ohlcv_data(ChartDataRequest(**request.dict()))
        ohlcv_data = ohlcv_response["data"]

        return {
            "success": True,
            "symbol": request.symbol,
            "chart_type": "footprint",
            "config": {
                "tick_size": request.tick_size,
                "show_delta": request.show_delta,
                "show_imbalance": request.show_imbalance,
                "imbalance_ratio": request.imbalance_ratio
            },
            "data": ohlcv_data
        }

    except Exception as e:
        logger.error(f"Error fetching Footprint data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Indicator Endpoints
@router.post("/indicators/calculate")
async def calculate_indicator(request: IndicatorRequest):
    """Calculate a technical indicator"""
    try:
        # Get base data
        ohlcv_response = await get_ohlcv_data(
            ChartDataRequest(
                symbol=request.symbol,
                timeframe=request.timeframe,
                limit=request.limit
            )
        )
        ohlcv_data = ohlcv_response["data"]

        # Return data for client-side calculation
        # In a production system, you might calculate server-side
        return {
            "success": True,
            "symbol": request.symbol,
            "indicator": request.indicator,
            "parameters": request.parameters,
            "data": ohlcv_data
        }

    except Exception as e:
        logger.error(f"Error calculating indicator: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/indicators/custom")
async def calculate_custom_indicator(request: CustomIndicatorRequest):
    """Calculate a custom indicator from a formula"""
    try:
        # Get base data
        ohlcv_response = await get_ohlcv_data(
            ChartDataRequest(
                symbol=request.symbol,
                timeframe=request.timeframe,
                limit=request.limit
            )
        )
        ohlcv_data = ohlcv_response["data"]

        return {
            "success": True,
            "symbol": request.symbol,
            "formula": request.formula,
            "parameters": request.parameters,
            "data": ohlcv_data
        }

    except Exception as e:
        logger.error(f"Error calculating custom indicator: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Pattern Detection
@router.get("/patterns/harmonic/{symbol}")
async def detect_harmonic_patterns(
    symbol: str,
    timeframe: str = Query("1h"),
    lookback: int = Query(100, ge=50, le=500)
):
    """Detect harmonic patterns in price data"""
    try:
        # Get data
        ohlcv_response = await get_ohlcv_data(
            ChartDataRequest(symbol=symbol, timeframe=timeframe, limit=lookback)
        )
        ohlcv_data = ohlcv_response["data"]

        # Return data for client-side pattern detection
        return {
            "success": True,
            "symbol": symbol,
            "timeframe": timeframe,
            "data": ohlcv_data
        }

    except Exception as e:
        logger.error(f"Error detecting patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Alert Management
@router.post("/alerts/create")
async def create_alert(request: AlertRequest):
    """Create a new price alert"""
    try:
        # In production, this would save to database
        alert_id = f"alert_{request.symbol}_{datetime.now().timestamp()}"

        return {
            "success": True,
            "alert_id": alert_id,
            "message": "Alert created successfully"
        }

    except Exception as e:
        logger.error(f"Error creating alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts/{alert_id}")
async def get_alert(alert_id: str):
    """Get alert details"""
    # In production, fetch from database
    return {
        "success": True,
        "alert_id": alert_id,
        "status": "active"
    }


@router.delete("/alerts/{alert_id}")
async def delete_alert(alert_id: str):
    """Delete an alert"""
    # In production, delete from database
    return {
        "success": True,
        "message": "Alert deleted"
    }


# Backtesting
@router.post("/backtest/run")
async def run_backtest(request: BacktestRequest):
    """Run a strategy backtest"""
    try:
        # Get historical data
        ohlcv_response = await get_ohlcv_data(
            ChartDataRequest(
                symbol=request.symbol,
                timeframe=request.timeframe,
                start_date=request.start_date,
                end_date=request.end_date
            )
        )
        ohlcv_data = ohlcv_response["data"]

        # Return data for client-side backtesting
        return {
            "success": True,
            "symbol": request.symbol,
            "strategy_config": request.strategy_config,
            "initial_capital": request.initial_capital,
            "data": ohlcv_data
        }

    except Exception as e:
        logger.error(f"Error running backtest: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Export Endpoints
@router.get("/export/{symbol}/csv")
async def export_csv(
    symbol: str,
    timeframe: str = Query("1h"),
    limit: int = Query(500)
):
    """Export chart data as CSV"""
    try:
        ohlcv_response = await get_ohlcv_data(
            ChartDataRequest(symbol=symbol, timeframe=timeframe, limit=limit)
        )
        data = ohlcv_response["data"]

        # Convert to CSV format
        csv_lines = ["timestamp,open,high,low,close,volume"]
        for candle in data:
            csv_lines.append(
                f"{candle['timestamp']},{candle['open']},{candle['high']},"
                f"{candle['low']},{candle['close']},{candle.get('volume', 0)}"
            )

        csv_content = "\n".join(csv_lines)

        return {
            "success": True,
            "format": "csv",
            "content": csv_content
        }

    except Exception as e:
        logger.error(f"Error exporting CSV: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Configuration
@router.get("/config/chart-types")
async def get_chart_types():
    """Get available chart types"""
    return {
        "success": True,
        "chart_types": [
            {
                "id": "candlestick",
                "name": "Candlestick",
                "description": "Traditional OHLC candlestick chart"
            },
            {
                "id": "renko",
                "name": "Renko",
                "description": "Price movement chart filtering out time"
            },
            {
                "id": "kagi",
                "name": "Kagi",
                "description": "Japanese trend chart emphasizing reversals"
            },
            {
                "id": "point-figure",
                "name": "Point & Figure",
                "description": "X and O chart filtering minor movements"
            },
            {
                "id": "market-profile",
                "name": "Market Profile",
                "description": "Volume distribution by price level"
            },
            {
                "id": "footprint",
                "name": "Footprint",
                "description": "Bid/ask volume at each price level"
            }
        ]
    }


@router.get("/config/indicators")
async def get_available_indicators():
    """Get list of available indicators"""
    return {
        "success": True,
        "indicators": [
            {"id": "SMA", "name": "Simple Moving Average", "params": ["period"]},
            {"id": "EMA", "name": "Exponential Moving Average", "params": ["period"]},
            {"id": "RSI", "name": "Relative Strength Index", "params": ["period"]},
            {"id": "MACD", "name": "MACD", "params": ["fast", "slow", "signal"]},
            {"id": "BB", "name": "Bollinger Bands", "params": ["period", "stddev"]},
            {"id": "ATR", "name": "Average True Range", "params": ["period"]},
            {"id": "STOCH", "name": "Stochastic", "params": ["k", "d"]},
            {"id": "ADX", "name": "ADX", "params": ["period"]},
            {"id": "OBV", "name": "On Balance Volume", "params": []}
        ]
    }
