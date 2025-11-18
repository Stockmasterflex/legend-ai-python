"""
Advanced Risk Management API
Professional position sizing and portfolio heat monitoring
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import logging

from app.services.advanced_risk_manager import get_risk_manager
from app.services.portfolio_heat_monitor import get_heat_monitor
from app.services.risk_visualizer import get_visualizer
from app.core.risk_models import PortfolioPosition

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/advanced-risk", tags=["advanced-risk"])


# ============================================================================
# REQUEST MODELS
# ============================================================================

class KellyRequest(BaseModel):
    """Kelly Criterion calculation request"""
    account_size: float = Field(..., gt=0, description="Total account value in $")
    win_rate: float = Field(..., gt=0, lt=1, description="Historical win rate (0-1)")
    avg_win_dollars: float = Field(..., gt=0, description="Average winning trade in $")
    avg_loss_dollars: float = Field(..., gt=0, description="Average losing trade in $")
    kelly_fraction: str = Field("half", description="Kelly fraction: 'full', 'half', or 'quarter'")
    entry_price: Optional[float] = Field(None, gt=0, description="Optional entry price")
    stop_loss: Optional[float] = Field(None, gt=0, description="Optional stop loss")


class FixedFractionalRequest(BaseModel):
    """Fixed fractional position sizing request"""
    account_size: float = Field(..., gt=0)
    entry_price: float = Field(..., gt=0)
    stop_loss: float = Field(..., gt=0)
    risk_percentage: float = Field(0.02, gt=0, le=0.10, description="Risk per trade (default 2%)")
    max_positions: int = Field(10, gt=0, description="Max concurrent positions")
    correlation_adjustment: float = Field(1.0, gt=0, le=1, description="Correlation adjustment (0-1)")


class VolatilityBasedRequest(BaseModel):
    """Volatility-based position sizing request"""
    account_size: float = Field(..., gt=0)
    entry_price: float = Field(..., gt=0)
    atr: float = Field(..., gt=0, description="Average True Range in $")
    atr_multiplier: float = Field(2.0, gt=0, description="Stop distance in ATR units")
    risk_percentage: float = Field(0.02, gt=0, le=0.10)
    vix: Optional[float] = Field(None, gt=0, description="VIX level for regime detection")
    atr_period: int = Field(14, gt=0, description="ATR calculation period")


class DynamicScalingRequest(BaseModel):
    """Dynamic position scaling request"""
    account_size: float = Field(..., gt=0)
    entry_price: float = Field(..., gt=0)
    stop_loss: float = Field(..., gt=0)
    confidence_score: float = Field(..., ge=0, le=100, description="Setup confidence (0-100)")
    market_regime: str = Field("normal", description="'bull', 'normal', or 'bear'")
    base_risk_pct: float = Field(0.02, gt=0, le=0.10)


class PositionInput(BaseModel):
    """Input for a single position"""
    symbol: str
    shares: int = Field(..., gt=0)
    entry_price: float = Field(..., gt=0)
    current_price: float = Field(..., gt=0)
    stop_loss: float = Field(..., gt=0)
    target: float = Field(..., gt=0)
    entry_date: str = Field(..., description="ISO format date")
    sector: Optional[str] = None


class PortfolioHeatRequest(BaseModel):
    """Portfolio heat calculation request"""
    positions: List[PositionInput]
    cash: float = Field(..., ge=0)
    max_portfolio_risk_pct: float = Field(10.0, gt=0, le=50)
    max_single_position_pct: float = Field(20.0, gt=0, le=100)
    max_sector_concentration_pct: float = Field(30.0, gt=0, le=100)


class CompareMethodsRequest(BaseModel):
    """Compare all position sizing methods"""
    account_size: float = Field(..., gt=0)
    entry_price: float = Field(..., gt=0)
    stop_loss: float = Field(..., gt=0)
    win_rate: float = Field(..., gt=0, lt=1)
    avg_win: float = Field(..., gt=0)
    avg_loss: float = Field(..., gt=0)
    atr: Optional[float] = Field(None, gt=0)
    vix: Optional[float] = Field(None, gt=0)


# ============================================================================
# ENDPOINTS - KELLY CRITERION
# ============================================================================

@router.post("/kelly-criterion")
async def calculate_kelly(request: KellyRequest):
    """
    Calculate Kelly Criterion position sizing

    The Kelly Criterion is an optimal position sizing formula that maximizes
    long-term growth while minimizing risk of ruin.

    Formula: f* = (p × b - q) / b
    where p = win rate, q = loss rate, b = win/loss ratio

    Most professionals use Kelly/2 or Kelly/4 for safety.

    Returns:
        Kelly percentage, position size, edge, risk of ruin
    """
    try:
        manager = get_risk_manager()

        result = manager.calculate_kelly_criterion(
            account_size=request.account_size,
            win_rate=request.win_rate,
            avg_win_dollars=request.avg_win_dollars,
            avg_loss_dollars=request.avg_loss_dollars,
            kelly_fraction=request.kelly_fraction,
            entry_price=request.entry_price,
            stop_loss=request.stop_loss
        )

        return {
            'success': True,
            'kelly_criterion': {
                'kelly_percentage': f"{result.kelly_percentage:.2f}%",
                'kelly_fraction': result.kelly_fraction,
                'adjusted_percentage': f"{result.adjusted_percentage:.2f}%",
                'position_size': result.position_size,
                'position_dollars': f"${result.position_dollars:,.2f}",
                'trading_edge': f"${result.edge:,.2f}",
                'risk_of_ruin': f"{result.risk_of_ruin:.2f}%",
                'notes': result.notes
            },
            'interpretation': {
                'full_kelly': f"{result.kelly_percentage:.2f}%",
                'half_kelly': f"{result.kelly_percentage / 2:.2f}% (recommended)",
                'quarter_kelly': f"{result.kelly_percentage / 4:.2f}% (conservative)",
                'recommendation': (
                    'Use Kelly/2 or Kelly/4 for safety' if result.kelly_percentage > 10
                    else 'Kelly fraction appears reasonable'
                )
            }
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Kelly calculation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS - FIXED FRACTIONAL
# ============================================================================

@router.post("/fixed-fractional")
async def calculate_fixed_fractional(request: FixedFractionalRequest):
    """
    Fixed Fractional Position Sizing

    The most common professional method. Risk a fixed percentage
    (typically 1-2%) of account per trade.

    Features:
    - Account size tracking
    - Position heat limits
    - Correlation adjustments

    Returns:
        Position size, risk amount, position heat
    """
    try:
        manager = get_risk_manager()

        result = manager.calculate_fixed_fractional(
            account_size=request.account_size,
            entry_price=request.entry_price,
            stop_loss=request.stop_loss,
            risk_percentage=request.risk_percentage,
            max_positions=request.max_positions,
            correlation_adjustment=request.correlation_adjustment
        )

        return {
            'success': True,
            'position_sizing': {
                'account_size': f"${result.account_size:,.2f}",
                'risk_percentage': f"{result.risk_percentage:.2f}%",
                'risk_dollars': f"${result.risk_dollars:,.2f}",
                'position_size': result.position_size,
                'position_dollars': f"${result.position_dollars:,.2f}",
                'position_heat': f"{result.position_heat:.2f}%",
                'max_concurrent_positions': result.max_positions
            },
            'risk_analysis': {
                'per_trade_risk': f"${result.risk_dollars:,.2f}",
                'max_total_risk': f"{result.max_positions * result.risk_percentage:.0f}%",
                'max_total_dollars': f"${result.max_positions * result.risk_dollars:,.2f}"
            },
            'notes': result.notes
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Fixed fractional error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS - VOLATILITY-BASED SIZING
# ============================================================================

@router.post("/volatility-based")
async def calculate_volatility_based(request: VolatilityBasedRequest):
    """
    Volatility-Based Position Sizing (ATR)

    Adjusts position size based on market volatility:
    - Higher volatility = smaller position
    - Lower volatility = larger position

    Uses ATR (Average True Range) for stop placement
    and VIX for regime detection.

    Returns:
        Volatility-adjusted position size
    """
    try:
        manager = get_risk_manager()

        result = manager.calculate_volatility_based(
            account_size=request.account_size,
            entry_price=request.entry_price,
            atr=request.atr,
            atr_multiplier=request.atr_multiplier,
            risk_percentage=request.risk_percentage,
            vix=request.vix,
            atr_period=request.atr_period
        )

        return {
            'success': True,
            'volatility_sizing': {
                'atr': f"${result.atr:.2f}",
                'atr_period': result.atr_period,
                'atr_multiplier': result.atr_multiplier,
                'stop_distance': f"${result.stop_distance:.2f}",
                'position_size': result.position_size,
                'position_dollars': f"${result.position_dollars:,.2f}"
            },
            'volatility_regime': {
                'regime': result.volatility_regime.value,
                'vix': result.vix,
                'adjustment_multiplier': result.volatility_adjustment,
                'description': self._get_regime_description(result.volatility_regime.value)
            },
            'notes': result.notes
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Volatility-based error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS - DYNAMIC SCALING
# ============================================================================

@router.post("/dynamic-scaling")
async def calculate_dynamic_scaling(request: DynamicScalingRequest):
    """
    Dynamic Position Scaling

    Scales position size based on:
    - Confidence in setup (0-100)
    - Market regime (bull/normal/bear)
    - Recent performance

    Returns:
        Dynamically scaled position size
    """
    try:
        manager = get_risk_manager()

        result = manager.calculate_dynamic_scaling(
            account_size=request.account_size,
            entry_price=request.entry_price,
            stop_loss=request.stop_loss,
            confidence_score=request.confidence_score,
            market_regime=request.market_regime,
            base_risk_pct=request.base_risk_pct
        )

        return {
            'success': True,
            'dynamic_sizing': {
                'base_risk': f"{request.base_risk_pct * 100:.1f}%",
                'adjusted_risk': f"{result.risk_percentage:.2f}%",
                'position_size': result.position_size,
                'position_dollars': f"${result.position_dollars:,.2f}",
                'risk_dollars': f"${result.risk_dollars:,.2f}"
            },
            'scaling_factors': {
                'confidence_score': request.confidence_score,
                'market_regime': request.market_regime
            },
            'notes': result.notes
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Dynamic scaling error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS - PORTFOLIO HEAT
# ============================================================================

@router.post("/portfolio-heat")
async def calculate_portfolio_heat(request: PortfolioHeatRequest):
    """
    Portfolio Heat Monitor

    Track portfolio-level risk metrics:
    - Total risk across all positions
    - Sector concentration limits
    - Position heat
    - Heat score (0-100)

    Returns:
        Comprehensive portfolio risk analysis
    """
    try:
        # Convert input positions to PortfolioPosition objects
        positions = []
        for pos in request.positions:
            positions.append(PortfolioPosition(
                symbol=pos.symbol,
                shares=pos.shares,
                entry_price=pos.entry_price,
                current_price=pos.current_price,
                stop_loss=pos.stop_loss,
                target=pos.target,
                entry_date=datetime.fromisoformat(pos.entry_date),
                sector=pos.sector
            ))

        # Get monitor
        monitor = get_heat_monitor(
            max_portfolio_risk_pct=request.max_portfolio_risk_pct,
            max_single_position_pct=request.max_single_position_pct,
            max_sector_concentration_pct=request.max_sector_concentration_pct
        )

        # Calculate heat
        heat = monitor.calculate_portfolio_heat(
            positions=positions,
            cash=request.cash
        )

        # Generate visualizations
        visualizer = get_visualizer()
        viz_data = monitor.generate_visualization_data(heat)

        return {
            'success': True,
            'portfolio_summary': {
                'total_account_value': f"${heat.total_account_value:,.2f}",
                'total_positions_value': f"${heat.total_positions_value:,.2f}",
                'total_cash': f"${heat.total_cash:,.2f}",
                'num_positions': heat.num_positions,
                'heat_score': heat.heat_score,
                'is_overheated': heat.is_overheated
            },
            'risk_metrics': {
                'total_risk_dollars': f"${heat.total_risk_dollars:,.2f}",
                'total_risk_percentage': f"{heat.total_risk_percentage:.2f}%",
                'largest_position_pct': f"{heat.largest_position_pct:.2f}%",
                'largest_risk_pct': f"{heat.largest_risk_pct:.2f}%"
            },
            'limits': {
                'max_portfolio_risk': f"{heat.max_portfolio_risk_pct}%",
                'max_single_position': f"{heat.max_single_position_pct}%",
                'max_sector_concentration': f"{heat.max_sector_concentration_pct}%"
            },
            'sector_concentration': heat.sector_concentration,
            'warnings': heat.warnings,
            'visualization_data': {
                'heat_map': viz_data.heat_map,
                'position_sizes': viz_data.position_sizes,
                'position_risks': viz_data.position_risks
            }
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Portfolio heat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS - VISUALIZATION
# ============================================================================

@router.post("/portfolio-heat/dashboard")
async def get_risk_dashboard(request: PortfolioHeatRequest):
    """
    Complete Risk Dashboard

    Returns all visualizations and charts for a comprehensive
    risk management dashboard.

    Includes:
    - Heat gauge
    - Risk pyramid
    - Position comparisons
    - Heat map
    - Sector concentration
    """
    try:
        # Convert positions
        positions = []
        for pos in request.positions:
            positions.append(PortfolioPosition(
                symbol=pos.symbol,
                shares=pos.shares,
                entry_price=pos.entry_price,
                current_price=pos.current_price,
                stop_loss=pos.stop_loss,
                target=pos.target,
                entry_date=datetime.fromisoformat(pos.entry_date),
                sector=pos.sector
            ))

        # Calculate heat
        monitor = get_heat_monitor(
            request.max_portfolio_risk_pct,
            request.max_single_position_pct,
            request.max_sector_concentration_pct
        )
        heat = monitor.calculate_portfolio_heat(positions, request.cash)

        # Generate visualizations
        viz_data = monitor.generate_visualization_data(heat)
        visualizer = get_visualizer()

        dashboard = visualizer.generate_risk_dashboard(heat, viz_data)

        return {
            'success': True,
            'dashboard': dashboard
        }

    except Exception as e:
        logger.error(f"Dashboard generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENDPOINTS - COMPARISON
# ============================================================================

@router.post("/compare-methods")
async def compare_all_methods(request: CompareMethodsRequest):
    """
    Compare All Position Sizing Methods

    Calculates position size using all available methods:
    - Fixed Fractional (1%, 2%)
    - Kelly Criterion (half, quarter)
    - ATR-based (if ATR provided)

    Returns:
        Side-by-side comparison of all methods
    """
    try:
        manager = get_risk_manager()

        results = manager.compare_methods(
            account_size=request.account_size,
            entry_price=request.entry_price,
            stop_loss=request.stop_loss,
            win_rate=request.win_rate,
            avg_win=request.avg_win,
            avg_loss=request.avg_loss,
            atr=request.atr,
            vix=request.vix
        )

        comparison = {}

        # Fixed 2%
        if 'fixed_2pct' in results:
            r = results['fixed_2pct']
            comparison['fixed_2_percent'] = {
                'position_size': r.position_size,
                'position_dollars': f"${r.position_dollars:,.2f}",
                'risk_dollars': f"${r.risk_dollars:,.2f}",
                'method': 'Fixed Fractional 2%'
            }

        # Fixed 1%
        if 'fixed_1pct' in results:
            r = results['fixed_1pct']
            comparison['fixed_1_percent'] = {
                'position_size': r.position_size,
                'position_dollars': f"${r.position_dollars:,.2f}",
                'risk_dollars': f"${r.risk_dollars:,.2f}",
                'method': 'Fixed Fractional 1%'
            }

        # Kelly Half
        if 'kelly_half' in results:
            r = results['kelly_half']
            comparison['kelly_half'] = {
                'position_size': r.position_size,
                'position_dollars': f"${r.position_dollars:,.2f}",
                'kelly_percentage': f"{r.adjusted_percentage:.2f}%",
                'method': 'Kelly Criterion (Half)'
            }

        # Kelly Quarter
        if 'kelly_quarter' in results:
            r = results['kelly_quarter']
            comparison['kelly_quarter'] = {
                'position_size': r.position_size,
                'position_dollars': f"${r.position_dollars:,.2f}",
                'kelly_percentage': f"{r.adjusted_percentage:.2f}%",
                'method': 'Kelly Criterion (Quarter)'
            }

        # ATR-based
        if 'atr_based' in results:
            r = results['atr_based']
            comparison['atr_based'] = {
                'position_size': r.position_size,
                'position_dollars': f"${r.position_dollars:,.2f}",
                'stop_distance': f"${r.stop_distance:.2f}",
                'method': 'ATR-Based Volatility'
            }

        return {
            'success': True,
            'comparison': comparison,
            'recommendation': self._get_sizing_recommendation(results)
        }

    except Exception as e:
        logger.error(f"Method comparison error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# HELPER METHODS
# ============================================================================

def _get_regime_description(regime: str) -> str:
    """Get volatility regime description"""
    descriptions = {
        'low': 'Low volatility - favorable for larger positions',
        'normal': 'Normal volatility - standard position sizing',
        'elevated': 'Elevated volatility - reduce position sizes',
        'high': 'High volatility - significantly reduce exposure'
    }
    return descriptions.get(regime, 'Unknown regime')


def _get_sizing_recommendation(results: dict) -> str:
    """Generate recommendation from comparison results"""
    # Get all position sizes
    sizes = []
    if 'fixed_2pct' in results:
        sizes.append(('Fixed 2%', results['fixed_2pct'].position_size))
    if 'kelly_half' in results:
        sizes.append(('Kelly/2', results['kelly_half'].position_size))

    if not sizes:
        return "Insufficient data for recommendation"

    # Calculate average
    avg_size = sum(s[1] for s in sizes) / len(sizes)

    return (
        f"Average recommended size: {int(avg_size)} shares. "
        f"Consider using conservative methods (Fixed 1-2% or Kelly/4) for safety."
    )


@router.get("/health")
async def health_check():
    """Health check for advanced risk management service"""
    return {
        "status": "healthy",
        "service": "advanced_risk_management",
        "features": [
            "kelly_criterion",
            "fixed_fractional",
            "volatility_based",
            "dynamic_scaling",
            "portfolio_heat",
            "risk_visualization"
        ]
    }
