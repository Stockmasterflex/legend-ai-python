"""
Pattern Validation API Endpoints
Track and analyze pattern performance
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from app.services.pattern_validation import PatternValidationService


router = APIRouter()
validation_service = PatternValidationService()


class PatternOutcomeRequest(BaseModel):
    """Request to record pattern outcome"""
    scan_id: int
    outcome: str  # 'hit_target', 'hit_stop', 'expired', 'partial'
    outcome_price: float
    actual_gain_loss: float
    notes: Optional[str] = None


class BacktestRequest(BaseModel):
    """Request for pattern backtest"""
    pattern_type: str
    ticker_symbol: str
    start_date: str
    end_date: str


@router.get("/performance")
async def get_pattern_performance(
    pattern_type: Optional[str] = None,
    min_samples: int = Query(5, ge=1, description="Minimum number of samples")
):
    """
    Get performance metrics for all patterns or specific pattern type

    Returns win rates, average gain/loss, and other statistics
    """
    try:
        performance = await validation_service.get_pattern_performance(
            pattern_type=pattern_type,
            min_samples=min_samples
        )

        return {
            "success": True,
            "data": performance,
            "count": len(performance)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/leaderboard")
async def get_pattern_leaderboard(limit: int = Query(10, ge=1, le=50)):
    """
    Get top performing patterns ranked by win rate

    Shows the best patterns to trade
    """
    try:
        leaderboard = await validation_service.get_pattern_leaderboard(limit=limit)

        return {
            "success": True,
            "data": leaderboard,
            "count": len(leaderboard)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/to-disable")
async def get_patterns_to_disable(
    min_samples: int = Query(20, ge=10),
    max_win_rate: float = Query(35.0, ge=0, le=100)
):
    """
    Get list of patterns that should be disabled due to poor performance

    These patterns have low win rates with sufficient sample size
    """
    try:
        to_disable = await validation_service.get_patterns_to_disable(
            min_samples=min_samples,
            max_win_rate=max_win_rate
        )

        return {
            "success": True,
            "patterns_to_disable": to_disable,
            "count": len(to_disable),
            "criteria": {
                "min_samples": min_samples,
                "max_win_rate": max_win_rate
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/record-outcome")
async def record_pattern_outcome(request: PatternOutcomeRequest):
    """
    Manually record the outcome of a pattern prediction

    Use this to track whether patterns hit targets or stops
    """
    try:
        await validation_service.record_pattern_outcome(
            scan_id=request.scan_id,
            outcome=request.outcome,
            outcome_price=request.outcome_price,
            actual_gain_loss=request.actual_gain_loss,
            notes=request.notes
        )

        return {
            "success": True,
            "message": f"Outcome recorded for scan {request.scan_id}"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/auto-validate")
async def auto_validate_patterns(
    lookback_days: int = Query(30, ge=1, le=180, description="Days to look back")
):
    """
    Automatically validate patterns by checking if targets/stops were hit

    This checks historical price data to determine outcomes
    """
    try:
        validated_count = await validation_service.auto_validate_patterns(
            lookback_days=lookback_days
        )

        return {
            "success": True,
            "validated_count": validated_count,
            "message": f"Validated {validated_count} patterns"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recent-validations")
async def get_recent_validations(
    days: int = Query(7, ge=1, le=90),
    limit: int = Query(50, ge=1, le=200)
):
    """
    Get recently validated patterns with outcomes

    Shows which patterns hit targets or stops
    """
    try:
        validations = await validation_service.get_recent_validations(
            days=days,
            limit=limit
        )

        return {
            "success": True,
            "data": validations,
            "count": len(validations)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary")
async def get_validation_summary():
    """
    Get overall validation statistics

    Shows total patterns, validation rate, and success rate
    """
    try:
        summary = await validation_service.get_validation_summary()

        return {
            "success": True,
            "data": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/backtest")
async def backtest_pattern(request: BacktestRequest):
    """
    Backtest a pattern on historical data

    Tests how the pattern would have performed in the past
    """
    try:
        start_date = datetime.fromisoformat(request.start_date)
        end_date = datetime.fromisoformat(request.end_date)

        results = await validation_service.backtest_pattern(
            pattern_type=request.pattern_type,
            ticker_symbol=request.ticker_symbol,
            start_date=start_date,
            end_date=end_date
        )

        return {
            "success": True,
            "data": results
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard")
async def get_validation_dashboard():
    """
    Get comprehensive validation dashboard data

    Includes summary, leaderboard, recent validations, and poor performers
    """
    try:
        # Get all dashboard data in parallel would be ideal
        # For now, sequential
        summary = await validation_service.get_validation_summary()
        leaderboard = await validation_service.get_pattern_leaderboard(limit=5)
        recent = await validation_service.get_recent_validations(days=7, limit=10)
        to_disable = await validation_service.get_patterns_to_disable()

        return {
            "success": True,
            "data": {
                "summary": summary,
                "top_patterns": leaderboard,
                "recent_validations": recent,
                "poor_performers": to_disable
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
