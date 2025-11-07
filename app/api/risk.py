"""
Risk Management and Position Sizing API
Professional position calculator for swing traders
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import logging

from app.services.risk_calculator import get_risk_calculator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/risk", tags=["risk"])


def _evaluate_rr(ratio: float) -> str:
    """Evaluate risk:reward ratio quality"""
    if ratio >= 2.0:
        return "✅ Excellent (2:1+) - High probability trade"
    elif ratio >= 1.5:
        return "✅ Good (1.5:1+) - Solid setup"
    elif ratio >= 1.0:
        return "⚠️ Fair (1:1) - Marginal risk:reward"
    else:
        return "❌ Poor (<1:1) - Skip this trade"


class PositionRequest(BaseModel):
    """Request for position size calculation"""
    account_size: float = Field(..., gt=0, description="Total account size in $")
    entry_price: float = Field(..., gt=0, description="Entry price per share in $")
    stop_loss_price: float = Field(..., gt=0, description="Stop loss price per share in $")
    target_price: float = Field(..., gt=0, description="Target/take profit price per share in $")
    risk_percentage: Optional[float] = Field(0.02, ge=0.01, le=0.05, description="Risk per trade (1-5%)")
    win_rate: Optional[float] = Field(None, ge=0, le=1, description="Historical win rate (0-1) for Kelly Criterion")


class BreakEvenRequest(BaseModel):
    """Request for break-even calculation"""
    entry_price: float = Field(..., gt=0, description="Entry price per share in $")
    position_size: int = Field(..., gt=0, description="Number of shares")
    commission_per_share: Optional[float] = Field(0.01, ge=0, description="Commission cost per share")


class RecoveryRequest(BaseModel):
    """Request for recovery calculation"""
    starting_account: float = Field(..., gt=0, description="Starting account size in $")
    current_account: float = Field(..., gt=0, description="Current account size in $")


@router.get("/health")
async def risk_health():
    """Health check for risk calculator service"""
    return {
        "status": "healthy",
        "service": "risk management",
        "features": ["position_sizing", "kelly_criterion", "breakeven", "recovery"]
    }


@router.post("/calculate-position")
async def calculate_position(request: PositionRequest):
    """
    Calculate optimal position size using the 2% risk rule

    The 2% rule: Never risk more than 2% of your account on any single trade.
    This is the golden rule of professional trading - it allows you to survive
    50 consecutive losses while still having capital to trade.

    Args:
        request: Position calculation parameters

    Returns:
        Detailed position sizing with multiple strategies

    Example:
        {
            "account_size": 100000,
            "entry_price": 178.50,
            "stop_loss_price": 175.00,
            "target_price": 185.00,
            "risk_percentage": 0.02,
            "win_rate": 0.62
        }

        Response: Position sizing with 2% rule, Kelly Criterion, conservative/aggressive options
    """
    try:
        calculator = get_risk_calculator()

        # Calculate position size
        result = calculator.calculate_position_size(
            account_size=request.account_size,
            entry_price=request.entry_price,
            stop_loss_price=request.stop_loss_price,
            target_price=request.target_price,
            risk_percentage=request.risk_percentage,
            win_rate=request.win_rate
        )

        return {
            "success": True,
            "position_sizing": {
                "account_size": f"${result.account_size:,.2f}",
                "risk_per_trade": f"${result.risk_per_trade:,.2f}",
                "recommended_position_size": result.position_size,
                "position_size_dollars": f"${result.position_size_dollars:,.2f}",
                "notes": result.notes or []
            },
            "entry_exit": {
                "entry_price": f"${result.entry_price:.2f}",
                "stop_loss_price": f"${result.stop_loss_price:.2f}",
                "target_price": f"${result.target_price:.2f}",
                "risk_distance": f"${result.risk_distance:.2f}",
                "reward_distance": f"${result.reward_distance:.2f}",
                "risk_percentage": f"{result.risk_percentage:.2f}%",
                "reward_percentage": f"{result.reward_percentage:.2f}%"
            },
            "risk_reward": {
                "ratio": f"{result.risk_reward_ratio:.2f}:1",
                "expected_value": f"${result.expected_value:,.2f}" if result.expected_value else "N/A",
                "evaluation": _evaluate_rr(result.risk_reward_ratio)
            },
            "alternatives": {
                "conservative_size": result.conservative_position_size,
                "conservative_dollars": f"${result.conservative_position_size * result.entry_price:,.2f}",
                "aggressive_size": result.aggressive_position_size,
                "aggressive_dollars": f"${result.aggressive_position_size * result.entry_price:,.2f}"
            },
            "kelly_criterion": {
                "position_size": result.kelly_position_size,
                "percentage": f"{result.kelly_position_percentage:.2f}%" if result.kelly_position_percentage else "N/A",
                "note": "Kelly uses 50% safety factor (Kelly/2) for conservative sizing"
            } if result.kelly_position_size else None
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error calculating position size: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/breakeven")
async def calculate_breakeven(request: BreakEvenRequest):
    """
    Calculate break-even price accounting for commissions

    Many traders forget to account for trading commissions in their planning.
    This calculates the exact breakeven price needed.

    Args:
        request: Entry price, position size, and commissions

    Returns:
        Break-even analysis
    """
    try:
        calculator = get_risk_calculator()
        result = calculator.calculate_break_even_points(
            entry_price=request.entry_price,
            position_size=request.position_size,
            commission_per_share=request.commission_per_share
        )

        return {
            "success": True,
            "entry_price": f"${result['entry_price']:.2f}",
            "breakeven_price": f"${result['breakeven_price']:.2f}",
            "commission_impact": f"${result['commission_impact']:.2f}",
            "commission_percentage": f"{result['commission_percentage']:.2f}%",
            "warning": result['notes']
        }

    except Exception as e:
        logger.error(f"Error calculating breakeven: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/recovery")
async def calculate_recovery(request: RecoveryRequest):
    """
    Calculate profit needed to recover from losses

    Shows how much profit is needed to recover from a drawdown.
    Important for understanding recovery difficulty.

    Args:
        request: Starting and current account sizes

    Returns:
        Recovery metrics
    """
    try:
        calculator = get_risk_calculator()
        result = calculator.calculate_account_recovery(
            starting_account=request.starting_account,
            current_account=request.current_account
        )

        if result["status"] == "profitable":
            return {
                "success": True,
                "status": "profitable",
                "profit_amount": f"${result['profit_amount']:,.2f}",
                "profit_percentage": f"{result['profit_percentage']:.2f}%",
                "message": "🎉 Account is in profit!"
            }
        else:
            return {
                "success": True,
                "status": "recovering",
                "loss_amount": f"${result['loss_amount']:,.2f}",
                "loss_percentage": f"{result['loss_percentage']:.2f}%",
                "recovery_needed_dollars": f"${result['recovery_needed_dollars']:,.2f}",
                "recovery_needed_percentage": f"{result['recovery_needed_percentage']:.2f}%",
                "warning": result['warning'],
                "note": "⚠️ Remember: Losses hurt more than wins help (asymmetric)"
            }

    except Exception as e:
        logger.error(f"Error calculating recovery: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rules")
async def get_risk_rules():
    """
    Get professional risk management rules for swing traders

    Returns:
        Best practices and guidelines
    """
    return {
        "success": True,
        "rules": {
            "1_percent_rule": {
                "rule": "Never risk more than 2% of account per trade",
                "reason": "Allows survival of 50 consecutive losses",
                "benefit": "Maintains capital for future trading"
            },
            "risk_reward_ratio": {
                "minimum": "1:1",
                "good": "1.5:1",
                "excellent": "2:1 or better",
                "rule": "Only take trades where reward > risk"
            },
            "position_sizing": {
                "rule": "Position size = Risk Amount / Risk Distance",
                "example": "$2,000 risk / $3.50 stop distance = 571 shares",
                "importance": "Correct sizing is CRITICAL for profitability"
            },
            "kelly_criterion": {
                "rule": "f* = (bp - q) / b where b=reward/risk, p=win%, q=loss%",
                "usage": "Calculate optimal Kelly, then use Kelly/2 for safety",
                "note": "Full Kelly can lead to ruin even with positive expectancy"
            }
        },
        "donts": {
            "1": "❌ Don't trade without stops",
            "2": "❌ Don't average down on losing positions",
            "3": "❌ Don't trade with more than 2% risk",
            "4": "❌ Don't use leverage unless you know exactly what you're doing",
            "5": "❌ Don't let winners turn into losers (take profits!)",
            "6": "❌ Don't revenge trade after a loss"
        }
    }
