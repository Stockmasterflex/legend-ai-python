"""
Risk Analytics API
Endpoints for risk management, correlation analysis, and diversification
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field

from app.services.database import get_db
from app.services.risk_analytics_service import RiskAnalyticsService

router = APIRouter(prefix="/api/risk-analytics", tags=["Risk Analytics"])


# Pydantic models
class PositionSizeRequest(BaseModel):
    portfolio_id: int = Field(..., description="Portfolio ID")
    symbol: str = Field(..., description="Stock symbol")
    entry_price: float = Field(..., gt=0, description="Entry price")
    stop_loss: float = Field(..., gt=0, description="Stop loss price")
    risk_percent: float = Field(default=2.0, ge=0.5, le=5.0, description="Risk % per trade (0.5-5%)")
    use_kelly: bool = Field(default=False, description="Use Kelly Criterion")
    win_rate: Optional[float] = Field(None, ge=0, le=1, description="Historical win rate (0-1)")
    avg_win_loss_ratio: Optional[float] = Field(None, gt=0, description="Avg win/loss ratio")


@router.post("/position-size", summary="Calculate optimal position size")
async def calculate_position_size(
    request: PositionSizeRequest,
    db: Session = Depends(get_db)
):
    """
    Calculate optimal position size based on risk parameters

    Uses the 2% rule by default, with optional Kelly Criterion calculation

    Parameters:
    - **portfolio_id**: Portfolio ID
    - **symbol**: Stock symbol
    - **entry_price**: Intended entry price
    - **stop_loss**: Stop loss price
    - **risk_percent**: Risk per trade (default 2%)
    - **use_kelly**: Enable Kelly Criterion (optional)
    - **win_rate**: Historical win rate for Kelly (required if use_kelly=true)
    - **avg_win_loss_ratio**: Avg win/loss ratio for Kelly (required if use_kelly=true)

    Returns:
    - Recommended shares, position value, risk metrics
    - Kelly Criterion sizing (if enabled)
    - Conservative and aggressive alternatives
    """
    service = RiskAnalyticsService(db)

    try:
        sizing = await service.calculate_position_size(
            portfolio_id=request.portfolio_id,
            symbol=request.symbol,
            entry_price=request.entry_price,
            stop_loss=request.stop_loss,
            risk_percent=request.risk_percent,
            use_kelly=request.use_kelly,
            win_rate=request.win_rate,
            avg_win_loss_ratio=request.avg_win_loss_ratio
        )
        return {
            "success": True,
            "sizing": sizing
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{portfolio_id}/portfolio-heat", summary="Calculate portfolio heat")
async def portfolio_heat(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    """
    Calculate portfolio heat (total risk exposure)

    Portfolio heat shows the total % of portfolio at risk across all positions

    Parameters:
    - **portfolio_id**: Portfolio ID

    Returns:
    - Total heat %, risk level, recommendations
    - Individual position risks
    - Max recommended heat threshold
    """
    service = RiskAnalyticsService(db)

    try:
        heat = await service.calculate_portfolio_heat(portfolio_id)
        return {
            "success": True,
            "portfolio_heat": heat
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{portfolio_id}/correlation-matrix", summary="Calculate correlation matrix")
async def correlation_matrix(
    portfolio_id: int,
    period_days: int = Query(default=60, ge=30, le=365, description="Historical period in days"),
    db: Session = Depends(get_db)
):
    """
    Calculate correlation matrix for portfolio positions

    Shows how positions move together (correlation)

    Parameters:
    - **portfolio_id**: Portfolio ID
    - **period_days**: Historical period for calculation (30-365 days)

    Returns:
    - Correlation matrix
    - List of symbols
    - Highly correlated pairs (correlation > 0.7)
    - Average correlation
    """
    service = RiskAnalyticsService(db)

    try:
        correlation = await service.calculate_correlation_matrix(
            portfolio_id,
            period_days=period_days
        )
        return {
            "success": True,
            "correlation": correlation
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{portfolio_id}/diversification-score", summary="Calculate diversification score")
async def diversification_score(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    """
    Calculate portfolio diversification score (0-100)

    Evaluates diversification based on:
    - Number of positions
    - Sector diversity
    - Position size concentration
    - Correlation between positions

    Parameters:
    - **portfolio_id**: Portfolio ID

    Returns:
    - Diversification score (0-100)
    - Letter grade (A+ to F)
    - Factor breakdown
    - Recommendations for improvement
    """
    service = RiskAnalyticsService(db)

    try:
        score = await service.calculate_diversification_score(portfolio_id)
        return {
            "success": True,
            "diversification": score
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{portfolio_id}/risk-summary", summary="Get comprehensive risk summary")
async def risk_summary(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    """
    Get comprehensive risk analytics summary

    Parameters:
    - **portfolio_id**: Portfolio ID

    Returns:
    - Portfolio heat
    - Diversification score
    - Average correlation
    - Risk recommendations
    """
    service = RiskAnalyticsService(db)

    try:
        # Get all risk metrics
        heat = await service.calculate_portfolio_heat(portfolio_id)
        diversification = await service.calculate_diversification_score(portfolio_id)
        correlation = await service.calculate_correlation_matrix(portfolio_id)

        return {
            "success": True,
            "risk_summary": {
                "portfolio_heat": {
                    "total_heat_pct": heat["total_heat_pct"],
                    "risk_level": heat["risk_level"],
                    "recommendation": heat["recommendation"]
                },
                "diversification": {
                    "score": diversification["score"],
                    "grade": diversification["grade"],
                    "recommendations": diversification["recommendations"]
                },
                "correlation": {
                    "avg_correlation": correlation.get("avg_correlation", 0),
                    "high_correlations": correlation.get("high_correlations", [])
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
