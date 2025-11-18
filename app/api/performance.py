"""
Performance Analytics API
Endpoints for portfolio performance analysis and benchmarking
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field

from app.services.database import get_db
from app.services.performance_service import PerformanceService

router = APIRouter(prefix="/api/performance", tags=["Performance Analytics"])


@router.get("/{portfolio_id}/returns", summary="Calculate portfolio returns")
async def calculate_returns(
    portfolio_id: int,
    period: str = Query(default="daily", description="Period: daily, weekly, or monthly"),
    db: Session = Depends(get_db)
):
    """
    Calculate portfolio returns for different time periods

    Parameters:
    - **portfolio_id**: Portfolio ID
    - **period**: Time period (daily/weekly/monthly)

    Returns:
    - Current value, total return, annualized return
    """
    service = PerformanceService(db)

    try:
        returns = await service.calculate_returns(portfolio_id, period)
        return {
            "success": True,
            "returns": returns
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{portfolio_id}/benchmark", summary="Compare to benchmark")
async def benchmark_comparison(
    portfolio_id: int,
    benchmark: str = Query(default="SPY", description="Benchmark symbol (default: SPY)"),
    period_days: int = Query(default=30, description="Comparison period in days"),
    db: Session = Depends(get_db)
):
    """
    Compare portfolio performance to a benchmark

    Parameters:
    - **portfolio_id**: Portfolio ID
    - **benchmark**: Benchmark ticker symbol (default: SPY)
    - **period_days**: Number of days for comparison

    Returns:
    - Portfolio return, benchmark return, alpha, relative performance
    """
    service = PerformanceService(db)

    try:
        comparison = await service.benchmark_comparison(
            portfolio_id,
            benchmark_symbol=benchmark,
            period_days=period_days
        )
        return {
            "success": True,
            "comparison": comparison
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{portfolio_id}/performers", summary="Get best and worst performers")
async def get_performers(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    """
    Get best and worst performing positions

    Parameters:
    - **portfolio_id**: Portfolio ID

    Returns:
    - Top 5 best performers
    - Top 5 worst performers
    """
    service = PerformanceService(db)

    try:
        performers = await service.get_best_worst_performers(portfolio_id)
        return {
            "success": True,
            "performers": performers
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{portfolio_id}/risk-adjusted", summary="Calculate risk-adjusted returns")
async def risk_adjusted_returns(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    """
    Calculate risk-adjusted return metrics

    Parameters:
    - **portfolio_id**: Portfolio ID

    Returns:
    - Sharpe ratio, Sortino ratio, max drawdown, volatility
    """
    service = PerformanceService(db)

    try:
        metrics = await service.calculate_risk_adjusted_returns(portfolio_id)
        return {
            "success": True,
            "risk_adjusted_metrics": metrics
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{portfolio_id}/summary", summary="Get comprehensive performance summary")
async def performance_summary(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    """
    Get comprehensive performance summary

    Parameters:
    - **portfolio_id**: Portfolio ID

    Returns:
    - Returns, benchmark comparison, best/worst performers
    - Risk-adjusted metrics, trade statistics
    """
    service = PerformanceService(db)

    try:
        summary = await service.get_performance_summary(portfolio_id)
        return {
            "success": True,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
