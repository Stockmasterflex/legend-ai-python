"""
Execution API Endpoints
Provides REST API for intelligent trade execution system
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime

from app.services.execution.execution_service import get_execution_service
from app.services.execution.venue_selection import VenueInfo
from app.services.execution.dark_pool import DarkPoolVenue

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/execution", tags=["execution"])


# Request/Response Models

class CreateExecutionOrderRequest(BaseModel):
    """Request to create execution order"""
    ticker: str = Field(..., description="Stock ticker symbol")
    side: str = Field(..., description="Order side: buy or sell")
    quantity: int = Field(..., gt=0, description="Total quantity to execute")
    algo_type: str = Field(default="twap", description="Algorithm: twap, vwap, is, or pov")
    duration_minutes: int = Field(default=60, gt=0, description="Execution window in minutes")
    limit_price: Optional[float] = Field(None, description="Optional limit price")
    algo_params: Optional[Dict[str, Any]] = Field(None, description="Algorithm-specific parameters")


class VenueSelectionRequest(BaseModel):
    """Request for venue selection"""
    ticker: str
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    use_smart_routing: bool = Field(default=True, description="Use multi-venue routing")


class IcebergOrderRequest(BaseModel):
    """Request to create iceberg order"""
    ticker: str
    side: str
    total_quantity: int = Field(..., gt=0)
    display_quantity: int = Field(..., gt=0, description="Visible quantity")
    limit_price: Optional[float] = None


class DarkPoolRoutingRequest(BaseModel):
    """Request for dark pool routing"""
    ticker: str
    side: str
    quantity: int = Field(..., gt=0)
    limit_price: float = Field(..., gt=0)
    nbbo_mid: float = Field(..., gt=0, description="NBBO midpoint price")
    strategy: str = Field(default="hybrid", description="aggressive, passive, or hybrid")


class ExecutionAnalysisRequest(BaseModel):
    """Request for execution analysis"""
    order_id: str
    ticker: str
    side: str
    total_quantity: int
    fills: List[Dict[str, Any]]
    arrival_price: Optional[float] = None
    benchmarks: Optional[Dict[str, float]] = None
    market_volume: Optional[int] = None


# API Endpoints

@router.get("/health")
async def execution_health():
    """Health check for execution system"""
    service = get_execution_service()
    summary = service.get_execution_summary()

    return {
        "status": "healthy",
        "service": "intelligent trade execution",
        "version": summary["version"],
        "algorithms": summary["capabilities"]["algorithms"]
    }


@router.get("/capabilities")
async def get_capabilities():
    """Get execution system capabilities"""
    try:
        service = get_execution_service()
        summary = service.get_execution_summary()

        return {
            "success": True,
            "capabilities": summary["capabilities"]
        }

    except Exception as e:
        logger.error(f"Error getting capabilities: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/orders/create")
async def create_execution_order(request: CreateExecutionOrderRequest):
    """
    Create a new execution order using specified algorithm

    Available algorithms:
    - **TWAP**: Time-Weighted Average Price - equal slices over time
    - **VWAP**: Volume-Weighted Average Price - slices based on volume patterns
    - **IS**: Implementation Shortfall - front-loaded execution
    - **POV**: Percentage of Volume - executes as % of market volume

    Example algo_params:
    - TWAP: {"num_slices": 10, "randomize_timing": true}
    - VWAP: {"volume_profile": [0.15, 0.12, ...]}
    - IS: {"urgency": 0.7}
    - POV: {"target_pov": 10.0, "estimated_daily_volume": 1000000}
    """
    try:
        service = get_execution_service()

        result = service.create_execution_order(
            ticker=request.ticker,
            side=request.side,
            quantity=request.quantity,
            algo_type=request.algo_type,
            duration_minutes=request.duration_minutes,
            limit_price=request.limit_price,
            algo_params=request.algo_params or {}
        )

        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("error"))

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating execution order: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/venues/select")
async def select_venues(request: VenueSelectionRequest):
    """
    Select optimal venues for order execution

    Uses smart routing to distribute orders across venues based on:
    - Commission costs
    - Liquidity
    - Historical fill quality
    """
    try:
        service = get_execution_service()

        # Mock venues for demo (in production, would query from database)
        mock_venues = _get_mock_venues()

        allocations = service.select_venues(
            ticker=request.ticker,
            quantity=request.quantity,
            price=request.price,
            available_venues=mock_venues,
            use_smart_routing=request.use_smart_routing
        )

        return {
            "success": True,
            "ticker": request.ticker,
            "total_quantity": request.quantity,
            "venues_selected": len(allocations),
            "allocations": allocations
        }

    except Exception as e:
        logger.error(f"Error selecting venues: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/orders/iceberg")
async def create_iceberg_order(request: IcebergOrderRequest):
    """
    Create an iceberg order (large order with hidden quantity)

    Iceberg orders display only a portion of the total quantity,
    hiding the rest to minimize market impact.
    """
    try:
        if request.display_quantity > request.total_quantity:
            raise HTTPException(
                status_code=400,
                detail="Display quantity cannot exceed total quantity"
            )

        service = get_execution_service()

        result = service.create_iceberg_order(
            ticker=request.ticker,
            side=request.side,
            total_quantity=request.total_quantity,
            display_quantity=request.display_quantity,
            limit_price=request.limit_price
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating iceberg order: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/darkpool/route")
async def route_to_dark_pools(request: DarkPoolRoutingRequest):
    """
    Route order to dark pools for price improvement

    Strategies:
    - **aggressive**: Sweep all dark pools quickly (IOC orders)
    - **passive**: Post to best dark pools and wait (DAY orders)
    - **hybrid**: Post to top 2-3 pools (balanced approach)

    Dark pools can provide:
    - Price improvement vs NBBO
    - Reduced market impact
    - Size discovery for large orders
    """
    try:
        service = get_execution_service()

        # Mock dark pools for demo
        mock_dark_pools = _get_mock_dark_pools()

        result = service.route_to_dark_pools(
            ticker=request.ticker,
            side=request.side,
            quantity=request.quantity,
            limit_price=request.limit_price,
            nbbo_mid=request.nbbo_mid,
            dark_pools=mock_dark_pools,
            strategy=request.strategy
        )

        return result

    except Exception as e:
        logger.error(f"Error routing to dark pools: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analytics/analyze")
async def analyze_execution(request: ExecutionAnalysisRequest):
    """
    Analyze execution quality and generate comprehensive report

    Provides:
    - Slippage measurements (vs arrival, VWAP, TWAP)
    - Fill quality grading (A+ to F)
    - Cost breakdown (commission + slippage)
    - Market impact analysis
    - Venue performance breakdown
    - Actionable improvement suggestions
    """
    try:
        service = get_execution_service()

        result = service.analyze_execution(
            order_id=request.order_id,
            ticker=request.ticker,
            side=request.side,
            total_quantity=request.total_quantity,
            fills=request.fills,
            arrival_price=request.arrival_price,
            benchmarks=request.benchmarks,
            market_volume=request.market_volume
        )

        return result

    except Exception as e:
        logger.error(f"Error analyzing execution: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/algorithms")
async def get_algorithms():
    """
    Get information about available execution algorithms
    """
    return {
        "success": True,
        "algorithms": {
            "TWAP": {
                "name": "Time-Weighted Average Price",
                "description": "Splits order into equal slices distributed evenly over time",
                "use_case": "Best for orders where timing is not critical",
                "parameters": {
                    "num_slices": "Number of slices (optional, auto-calculated if not provided)",
                    "randomize_timing": "Add random jitter to slice times (default: true)",
                    "randomize_size": "Randomize slice sizes slightly (default: true)"
                }
            },
            "VWAP": {
                "name": "Volume-Weighted Average Price",
                "description": "Adjusts slice sizes based on historical volume patterns",
                "use_case": "Best for blending with market volume, minimizing market impact",
                "parameters": {
                    "volume_profile": "Custom intraday volume profile (optional)",
                    "randomize_timing": "Add random jitter to slice times (default: true)",
                    "randomize_size": "Randomize slice sizes slightly (default: true)"
                }
            },
            "IS": {
                "name": "Implementation Shortfall",
                "description": "Front-loaded execution that balances urgency vs. market impact",
                "use_case": "Best for urgent orders where delay is costly",
                "parameters": {
                    "urgency": "Urgency level 0-1 (0=patient, 1=aggressive, default: 0.5)",
                    "randomize_timing": "Add random jitter to slice times (default: true)",
                    "randomize_size": "Randomize slice sizes slightly (default: true)"
                }
            },
            "POV": {
                "name": "Percentage of Volume",
                "description": "Executes as a target percentage of market volume",
                "use_case": "Best for large orders that need to track market participation",
                "parameters": {
                    "target_pov": "Target % of market volume (default: 10.0)",
                    "estimated_daily_volume": "Estimated daily volume for the security",
                    "randomize_timing": "Add random jitter to slice times (default: true)",
                    "randomize_size": "Randomize slice sizes slightly (default: true)"
                }
            }
        }
    }


@router.get("/demo")
async def execution_demo():
    """
    Get a comprehensive demo showing execution system capabilities
    """
    return {
        "success": True,
        "demo": {
            "scenario": "Execute 10,000 shares of AAPL using VWAP algorithm",
            "examples": {
                "1_create_order": {
                    "endpoint": "POST /api/execution/orders/create",
                    "request": {
                        "ticker": "AAPL",
                        "side": "buy",
                        "quantity": 10000,
                        "algo_type": "vwap",
                        "duration_minutes": 120,
                        "limit_price": 175.50
                    },
                    "response_summary": "Returns execution plan with 13 slices over 120 minutes"
                },
                "2_venue_selection": {
                    "endpoint": "POST /api/execution/venues/select",
                    "request": {
                        "ticker": "AAPL",
                        "quantity": 10000,
                        "price": 175.50,
                        "use_smart_routing": True
                    },
                    "response_summary": "Smart routes across 3 venues: Alpaca (4000), IB (3500), Schwab (2500)"
                },
                "3_iceberg_order": {
                    "endpoint": "POST /api/execution/orders/iceberg",
                    "request": {
                        "ticker": "AAPL",
                        "side": "buy",
                        "total_quantity": 10000,
                        "display_quantity": 500,
                        "limit_price": 175.50
                    },
                    "response_summary": "Creates iceberg with 500 shares visible, 9500 hidden"
                },
                "4_dark_pool_routing": {
                    "endpoint": "POST /api/execution/darkpool/route",
                    "request": {
                        "ticker": "AAPL",
                        "side": "buy",
                        "quantity": 10000,
                        "limit_price": 175.50,
                        "nbbo_mid": 175.45,
                        "strategy": "hybrid"
                    },
                    "response_summary": "Routes to 3 dark pools for potential price improvement"
                },
                "5_execution_analysis": {
                    "endpoint": "POST /api/execution/analytics/analyze",
                    "description": "After execution completes, analyze quality",
                    "metrics_provided": [
                        "Slippage vs arrival price: 3.2 bps",
                        "Slippage vs VWAP: -1.5 bps (price improvement!)",
                        "Fill rate: 100%",
                        "Quality grade: A",
                        "Total cost: $245.30 (commission + slippage)",
                        "Dark pool fills: 2,800 shares (28%)"
                    ]
                }
            }
        }
    }


# Helper functions for mock data

def _get_mock_venues() -> List[VenueInfo]:
    """Get mock venue data for demo"""
    return [
        VenueInfo(
            venue_id=1,
            name="Alpaca",
            venue_type="broker",
            commission_rate=0.0,
            commission_type="per_share",
            min_commission=0.0,
            liquidity_score=85.0,
            avg_fill_quality=88.0,
            supports_dark_pool=False,
            supports_iceberg=True,
            is_active=True
        ),
        VenueInfo(
            venue_id=2,
            name="Interactive Brokers",
            venue_type="broker",
            commission_rate=0.0035,
            commission_type="per_share",
            min_commission=0.35,
            liquidity_score=95.0,
            avg_fill_quality=92.0,
            supports_dark_pool=True,
            supports_iceberg=True,
            is_active=True
        ),
        VenueInfo(
            venue_id=3,
            name="Charles Schwab",
            venue_type="broker",
            commission_rate=0.0,
            commission_type="per_share",
            min_commission=0.0,
            liquidity_score=90.0,
            avg_fill_quality=89.0,
            supports_dark_pool=False,
            supports_iceberg=True,
            is_active=True
        ),
        VenueInfo(
            venue_id=4,
            name="TD Ameritrade",
            venue_type="broker",
            commission_rate=0.0,
            commission_type="per_share",
            min_commission=0.0,
            liquidity_score=88.0,
            avg_fill_quality=87.0,
            supports_dark_pool=False,
            supports_iceberg=False,
            is_active=True
        )
    ]


def _get_mock_dark_pools() -> List[DarkPoolVenue]:
    """Get mock dark pool data for demo"""
    return [
        DarkPoolVenue(
            venue_id=10,
            name="Sigma X (Goldman)",
            min_size=100,
            max_size=None,
            typical_spread_improvement_bps=2.5,
            fill_rate=45.0,
            avg_fill_time_ms=150.0,
            supports_midpoint_peg=True,
            supports_size_discovery=True,
            is_active=True
        ),
        DarkPoolVenue(
            venue_id=11,
            name="UBS ATS",
            min_size=100,
            max_size=50000,
            typical_spread_improvement_bps=2.0,
            fill_rate=38.0,
            avg_fill_time_ms=200.0,
            supports_midpoint_peg=True,
            supports_size_discovery=False,
            is_active=True
        ),
        DarkPoolVenue(
            venue_id=12,
            name="Instinet BlockMatch",
            min_size=500,
            max_size=None,
            typical_spread_improvement_bps=3.0,
            fill_rate=52.0,
            avg_fill_time_ms=120.0,
            supports_midpoint_peg=True,
            supports_size_discovery=True,
            is_active=True
        )
    ]
