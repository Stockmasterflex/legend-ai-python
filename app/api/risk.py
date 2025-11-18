"""
Risk Management and Position Sizing API
Professional position calculator for swing traders
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import logging

from app.services.risk_calculator import get_risk_calculator
from app.services.portfolio_risk import (
    get_portfolio_risk_service,
    Portfolio,
    Position
)
import numpy as np
import pandas as pd
from typing import List, Dict, Any

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


# ==================== PORTFOLIO RISK ENDPOINTS ====================


class PositionInput(BaseModel):
    """Position input for portfolio risk calculations"""
    symbol: str
    quantity: float = Field(..., description="Number of shares")
    entry_price: float = Field(..., gt=0, description="Entry price")
    current_price: float = Field(..., gt=0, description="Current price")
    sector: Optional[str] = None
    delta: float = Field(1.0, description="Position delta (1.0 for stocks)")
    gamma: float = Field(0.0, description="Position gamma")
    vega: float = Field(0.0, description="Position vega")
    theta: float = Field(0.0, description="Position theta")


class PortfolioInput(BaseModel):
    """Portfolio input for risk calculations"""
    positions: List[PositionInput]
    cash: float = Field(0.0, ge=0, description="Cash position")
    name: str = Field("Portfolio", description="Portfolio name")


class VaRRequest(BaseModel):
    """Request for Value at Risk calculation"""
    returns: List[float] = Field(..., description="Historical returns array")
    portfolio_value: float = Field(..., gt=0, description="Current portfolio value")
    confidence_levels: List[float] = Field([0.95, 0.99], description="Confidence levels")
    time_horizon_days: int = Field(1, gt=0, description="Time horizon in days")
    num_simulations: int = Field(10000, gt=0, description="Monte Carlo simulations")


class StressTestRequest(BaseModel):
    """Request for stress testing"""
    portfolio: PortfolioInput
    scenario_type: str = Field(..., description="Type: market_crash, sector_shock, custom")
    crash_severity: Optional[float] = Field(-0.30, description="Market crash severity")
    sector: Optional[str] = Field(None, description="Sector for sector shock")
    sector_shock: Optional[float] = Field(-0.20, description="Sector shock magnitude")
    custom_shocks: Optional[Dict[str, float]] = Field(None, description="Custom shocks by symbol")


class DrawdownRequest(BaseModel):
    """Request for drawdown analysis"""
    equity_curve: List[float] = Field(..., description="Portfolio value time series")
    dates: Optional[List[str]] = Field(None, description="Optional dates for equity curve")


class RiskAttributionRequest(BaseModel):
    """Request for risk attribution"""
    portfolio: PortfolioInput
    returns_data: Dict[str, List[float]] = Field(..., description="Returns data by symbol")


@router.post("/portfolio/var")
async def calculate_portfolio_var(request: VaRRequest):
    """
    Calculate Value at Risk (VaR) using multiple methods

    Calculates VaR using:
    - Historical Simulation: Non-parametric, uses actual historical returns
    - Parametric (Variance-Covariance): Assumes normal distribution
    - Monte Carlo: Simulates future returns using fitted distribution

    Args:
        request: VaR calculation parameters

    Returns:
        VaR results for all methods and confidence levels
    """
    try:
        service = get_portfolio_risk_service()
        returns_array = np.array(request.returns)

        if len(returns_array) == 0:
            raise HTTPException(status_code=400, detail="Returns array cannot be empty")

        # Calculate VaR using all methods
        var_results = service.calculate_all_var_methods(
            returns=returns_array,
            portfolio_value=request.portfolio_value,
            confidence_levels=request.confidence_levels,
            time_horizon_days=request.time_horizon_days,
            num_simulations=request.num_simulations
        )

        # Format results
        formatted_results = {}
        for method, results in var_results.items():
            formatted_results[method] = []
            for var_result in results:
                formatted_results[method].append({
                    "confidence_level": f"{var_result.confidence_level*100:.0f}%",
                    "var_amount": f"${var_result.var_amount:,.2f}",
                    "var_percent": f"{var_result.var_percent:.2f}%",
                    "time_horizon_days": var_result.time_horizon_days,
                    "portfolio_value": f"${var_result.portfolio_value:,.2f}",
                    "method": var_result.method,
                    "additional_info": var_result.additional_info
                })

        return {
            "success": True,
            "var_results": formatted_results,
            "summary": {
                "portfolio_value": f"${request.portfolio_value:,.2f}",
                "time_horizon": f"{request.time_horizon_days} day(s)",
                "methods": ["Historical Simulation", "Parametric", "Monte Carlo"],
                "interpretation": "VaR represents the maximum expected loss at a given confidence level"
            }
        }

    except Exception as e:
        logger.error(f"Error calculating VaR: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/portfolio/stress-test")
async def stress_test_portfolio(request: StressTestRequest):
    """
    Run stress tests on portfolio

    Supports multiple scenario types:
    - market_crash: Uniform market decline
    - sector_shock: Sector-specific shock
    - custom: Custom shocks by position

    Args:
        request: Stress test parameters

    Returns:
        Stress test results with portfolio impact
    """
    try:
        service = get_portfolio_risk_service()

        # Build portfolio
        positions = [
            Position(
                symbol=p.symbol,
                quantity=p.quantity,
                entry_price=p.entry_price,
                current_price=p.current_price,
                sector=p.sector,
                delta=p.delta,
                gamma=p.gamma,
                vega=p.vega,
                theta=p.theta
            )
            for p in request.portfolio.positions
        ]

        portfolio = Portfolio(
            positions=positions,
            cash=request.portfolio.cash,
            name=request.portfolio.name
        )

        # Run appropriate stress test
        if request.scenario_type == "market_crash":
            result = service.stress_test_market_crash(
                portfolio,
                crash_severity=request.crash_severity
            )
        elif request.scenario_type == "sector_shock":
            if not request.sector:
                raise HTTPException(status_code=400, detail="Sector required for sector_shock")
            result = service.stress_test_sector_shock(
                portfolio,
                sector=request.sector,
                shock=request.sector_shock
            )
        elif request.scenario_type == "custom":
            if not request.custom_shocks:
                raise HTTPException(status_code=400, detail="Custom shocks required for custom scenario")
            result = service.stress_test_historical_scenario(
                portfolio,
                scenario_shocks=request.custom_shocks,
                scenario_name="Custom Scenario",
                description="User-defined stress scenario"
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unknown scenario type: {request.scenario_type}")

        return {
            "success": True,
            "scenario": {
                "name": result.scenario_name,
                "type": result.scenario_type,
                "description": result.description
            },
            "impact": {
                "portfolio_loss": f"${result.portfolio_loss:,.2f}",
                "portfolio_loss_percent": f"{result.portfolio_loss_percent:.2f}%",
                "portfolio_value": f"${portfolio.total_market_value:,.2f}",
                "stressed_value": f"${portfolio.total_market_value + result.portfolio_loss:,.2f}"
            },
            "position_impacts": {
                symbol: f"${loss:,.2f}"
                for symbol, loss in result.position_impacts.items()
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error running stress test: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/portfolio/greeks")
async def calculate_portfolio_greeks_endpoint(portfolio: PortfolioInput):
    """
    Calculate portfolio Greeks

    Greeks measure portfolio sensitivity to market factors:
    - Delta: Sensitivity to price changes (directional exposure)
    - Gamma: Rate of change of delta (convexity)
    - Vega: Sensitivity to volatility changes
    - Theta: Sensitivity to time decay

    Args:
        portfolio: Portfolio data

    Returns:
        Portfolio Greeks and hedging suggestions
    """
    try:
        service = get_portfolio_risk_service()

        # Build portfolio
        positions = [
            Position(
                symbol=p.symbol,
                quantity=p.quantity,
                entry_price=p.entry_price,
                current_price=p.current_price,
                sector=p.sector,
                delta=p.delta,
                gamma=p.gamma,
                vega=p.vega,
                theta=p.theta
            )
            for p in portfolio.positions
        ]

        portfolio_obj = Portfolio(
            positions=positions,
            cash=portfolio.cash,
            name=portfolio.name
        )

        # Calculate Greeks
        greeks = service.calculate_portfolio_greeks(portfolio_obj)

        # Calculate hedging suggestions
        hedging = service.calculate_hedging_suggestions(portfolio_obj, target_delta=0.0)

        return {
            "success": True,
            "portfolio_greeks": {
                "delta": f"{greeks.portfolio_delta:,.2f}",
                "gamma": f"{greeks.portfolio_gamma:,.4f}",
                "vega": f"{greeks.portfolio_vega:,.2f}",
                "theta": f"{greeks.portfolio_theta:,.2f}",
                "delta_exposure": f"${greeks.delta_exposure:,.2f}"
            },
            "position_greeks": greeks.position_greeks,
            "hedging_suggestions": hedging,
            "interpretation": {
                "delta": "Total directional exposure. Positive = bullish, Negative = bearish",
                "gamma": "Rate of delta change. High gamma = rapid delta changes",
                "vega": "Volatility exposure. Positive = benefits from vol increase",
                "theta": "Time decay. Negative = loses value over time"
            }
        }

    except Exception as e:
        logger.error(f"Error calculating Greeks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/portfolio/drawdown")
async def calculate_portfolio_drawdown(request: DrawdownRequest):
    """
    Calculate comprehensive drawdown metrics

    Analyzes historical drawdowns including:
    - Maximum drawdown and duration
    - Average drawdown
    - Current drawdown status
    - Recovery time analysis
    - All underwater periods

    Args:
        request: Equity curve data

    Returns:
        Comprehensive drawdown analysis
    """
    try:
        service = get_portfolio_risk_service()

        # Create equity curve series
        equity_values = request.equity_curve
        if request.dates:
            equity_series = pd.Series(
                equity_values,
                index=pd.to_datetime(request.dates)
            )
        else:
            equity_series = pd.Series(equity_values)

        # Calculate drawdowns
        result = service.calculate_drawdowns(equity_series)

        return {
            "success": True,
            "drawdown_metrics": {
                "max_drawdown": f"${result.max_drawdown:,.2f}",
                "max_drawdown_percent": f"{result.max_drawdown_percent:.2f}%",
                "average_drawdown": f"${result.average_drawdown:,.2f}",
                "average_drawdown_percent": f"{result.average_drawdown_percent:.2f}%",
                "current_drawdown": f"${result.current_drawdown:,.2f}",
                "current_drawdown_percent": f"{result.current_drawdown_percent:.2f}%",
                "max_drawdown_duration_days": result.max_drawdown_duration_days,
                "average_recovery_days": result.recovery_time_days
            },
            "underwater_periods": result.underwater_periods,
            "status": "In drawdown" if result.current_drawdown < 0 else "At peak",
            "interpretation": {
                "max_drawdown": "Largest peak-to-trough decline",
                "recovery_time": "Average days to recover from drawdowns",
                "current_status": f"{'Currently underwater' if result.current_drawdown < 0 else 'Currently at new peak'}"
            }
        }

    except Exception as e:
        logger.error(f"Error calculating drawdown: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/portfolio/risk-attribution")
async def calculate_risk_attribution_endpoint(request: RiskAttributionRequest):
    """
    Calculate risk attribution across portfolio

    Breaks down portfolio risk by:
    - Individual positions (marginal and total contribution)
    - Sectors
    - Concentration metrics

    Args:
        request: Portfolio and returns data

    Returns:
        Comprehensive risk attribution analysis
    """
    try:
        service = get_portfolio_risk_service()

        # Build portfolio
        positions = [
            Position(
                symbol=p.symbol,
                quantity=p.quantity,
                entry_price=p.entry_price,
                current_price=p.current_price,
                sector=p.sector,
                delta=p.delta,
                gamma=p.gamma,
                vega=p.vega,
                theta=p.theta
            )
            for p in request.portfolio.positions
        ]

        portfolio = Portfolio(
            positions=positions,
            cash=request.portfolio.cash,
            name=request.portfolio.name
        )

        # Convert returns data to numpy arrays
        returns_data = {
            symbol: np.array(returns)
            for symbol, returns in request.returns_data.items()
        }

        # Calculate risk attribution
        result = service.calculate_risk_attribution(portfolio, returns_data)

        return {
            "success": True,
            "total_risk": {
                "portfolio_volatility": f"{result.total_risk:.2f}%",
                "annualized_volatility": f"{result.total_risk * np.sqrt(252):.2f}%"
            },
            "risk_by_position": {
                symbol: {
                    "risk_contribution": f"{risk:.4f}%",
                    "percent_of_total_risk": f"{result.risk_contribution_percent[symbol]:.2f}%",
                    "marginal_risk": f"{result.marginal_risk[symbol]:.4f}%"
                }
                for symbol, risk in result.risk_by_position.items()
            },
            "risk_by_sector": {
                sector: f"{risk:.4f}%"
                for sector, risk in result.risk_by_sector.items()
            },
            "concentration_metrics": {
                "herfindahl_index": f"{result.concentration_metrics['herfindahl_index']:.4f}",
                "effective_positions": f"{result.concentration_metrics['effective_number_of_positions']:.2f}",
                "largest_position": f"{result.concentration_metrics['largest_position_weight']*100:.2f}%",
                "top_5_concentration": f"{result.concentration_metrics['top_5_concentration']*100:.2f}%",
                "diversification_ratio": f"{result.concentration_metrics['diversification_ratio']:.2f}"
            },
            "interpretation": {
                "herfindahl_index": "Lower is more diversified (1/N = perfectly diversified)",
                "effective_positions": "Number of 'equivalent' equal-weighted positions",
                "marginal_risk": "Risk added by increasing position by 1%",
                "diversification_ratio": "Higher is better (>1 = diversified)"
            }
        }

    except Exception as e:
        logger.error(f"Error calculating risk attribution: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/portfolio/health")
async def portfolio_risk_health():
    """Health check for portfolio risk service"""
    return {
        "status": "healthy",
        "service": "portfolio risk measurement",
        "features": [
            "Value at Risk (Historical, Parametric, Monte Carlo)",
            "Stress Testing (Market Crash, Sector Shock, Custom)",
            "Portfolio Greeks (Delta, Gamma, Vega, Theta)",
            "Drawdown Analysis",
            "Risk Attribution"
        ],
        "version": "1.0.0"
    }
