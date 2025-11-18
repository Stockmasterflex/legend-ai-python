"""
Options Analytics API Endpoints
Advanced options analytics including chain analysis, flow, volatility surface, and strategies
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

from app.services.options_data import get_options_data_service
from app.core.options import (
    GreeksCalculator,
    VolatilitySurfaceAnalyzer,
    MaxPainCalculator,
    SpreadAnalyzer
)

router = APIRouter(prefix="/api/options", tags=["Options Analytics"])

# Initialize services
greeks_calc = GreeksCalculator()
vol_surface = VolatilitySurfaceAnalyzer()
max_pain_calc = MaxPainCalculator()
spread_analyzer = SpreadAnalyzer()


# ============================================================================
# Request/Response Models
# ============================================================================

class GreeksRequest(BaseModel):
    spot_price: float = Field(..., description="Current stock price")
    strike: float = Field(..., description="Strike price")
    time_to_expiry: float = Field(..., description="Time to expiration in years")
    volatility: float = Field(..., description="Implied volatility")
    risk_free_rate: float = Field(0.05, description="Risk-free rate")
    option_type: str = Field("call", description="'call' or 'put'")


class VerticalSpreadRequest(BaseModel):
    long_strike: float
    short_strike: float
    spread_type: str = Field(..., description="'call' or 'put'")
    debit: float = Field(..., description="Net debit paid")
    spot_price: float
    num_contracts: int = 1


class IronCondorRequest(BaseModel):
    put_long_strike: float
    put_short_strike: float
    call_short_strike: float
    call_long_strike: float
    credit: float
    spot_price: float
    num_contracts: int = 1


class StraddleRequest(BaseModel):
    strike: float
    call_price: float
    put_price: float
    spot_price: float
    num_contracts: int = 1
    is_long: bool = True


# ============================================================================
# OPTIONS CHAIN ENDPOINTS
# ============================================================================

@router.get("/chain/{symbol}")
async def get_options_chain(
    symbol: str,
    expiry: Optional[str] = None,
    include_greeks: bool = True
):
    """
    Get options chain with Greeks and analytics

    - **symbol**: Stock ticker
    - **expiry**: Specific expiration date (YYYY-MM-DD) or None for all
    - **include_greeks**: Calculate Greeks for each option
    """
    try:
        options_service = get_options_data_service()
        chain = await options_service.get_options_chain(
            symbol=symbol,
            expiry_date=expiry,
            include_greeks=include_greeks
        )
        return chain

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chain/{symbol}/max-pain")
async def get_max_pain(symbol: str, expiry: Optional[str] = None):
    """
    Calculate max pain strike for options chain

    - **symbol**: Stock ticker
    - **expiry**: Expiration date filter
    """
    try:
        options_service = get_options_data_service()
        chain = await options_service.get_options_chain(
            symbol=symbol,
            expiry_date=expiry,
            include_greeks=False
        )

        # Combine calls and puts for max pain calculation
        all_options = []
        for call in chain.get("calls", []):
            all_options.append({**call, "type": "call"})
        for put in chain.get("puts", []):
            all_options.append({**put, "type": "put"})

        max_pain_result = max_pain_calc.calculate_max_pain(all_options)

        return {
            "symbol": symbol,
            "expiry": expiry,
            **max_pain_result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chain/{symbol}/oi-analysis")
async def get_oi_analysis(symbol: str, expiry: Optional[str] = None):
    """
    Analyze open interest distribution

    - **symbol**: Stock ticker
    - **expiry**: Expiration date filter
    """
    try:
        options_service = get_options_data_service()
        chain = await options_service.get_options_chain(
            symbol=symbol,
            expiry_date=expiry,
            include_greeks=False
        )

        spot_price = chain.get("spot_price", 150.0)

        # Combine calls and puts
        all_options = []
        for call in chain.get("calls", []):
            all_options.append({**call, "type": "call"})
        for put in chain.get("puts", []):
            all_options.append({**put, "type": "put"})

        oi_analysis = max_pain_calc.analyze_open_interest(all_options, spot_price)

        return {
            "symbol": symbol,
            "expiry": expiry,
            "spot_price": spot_price,
            **oi_analysis
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chain/{symbol}/unusual-activity")
async def get_unusual_activity_for_symbol(
    symbol: str,
    volume_threshold: float = 2.0
):
    """
    Detect unusual options activity for a symbol

    - **symbol**: Stock ticker
    - **volume_threshold**: Volume/OI ratio threshold
    """
    try:
        options_service = get_options_data_service()
        chain = await options_service.get_options_chain(
            symbol=symbol,
            expiry_date=None,
            include_greeks=False
        )

        # Combine calls and puts
        all_options = []
        for call in chain.get("calls", []):
            all_options.append({**call, "type": "call"})
        for put in chain.get("puts", []):
            all_options.append({**put, "type": "put"})

        unusual = max_pain_calc.detect_unusual_activity(all_options, volume_threshold)

        return {
            "symbol": symbol,
            "unusual_contracts": unusual,
            "count": len(unusual)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chain/{symbol}/gamma-exposure")
async def get_gamma_exposure(symbol: str, expiry: Optional[str] = None):
    """
    Calculate dealer gamma exposure (GEX)

    - **symbol**: Stock ticker
    - **expiry**: Expiration date filter
    """
    try:
        options_service = get_options_data_service()
        chain = await options_service.get_options_chain(
            symbol=symbol,
            expiry_date=expiry,
            include_greeks=True
        )

        spot_price = chain.get("spot_price", 150.0)

        # Combine calls and puts
        all_options = []
        for call in chain.get("calls", []):
            all_options.append({**call, "type": "call"})
        for put in chain.get("puts", []):
            all_options.append({**put, "type": "put"})

        gex = max_pain_calc.calculate_gamma_exposure(all_options, spot_price)

        return {
            "symbol": symbol,
            "expiry": expiry,
            **gex
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# OPTIONS FLOW ENDPOINTS
# ============================================================================

@router.get("/flow/{symbol}")
async def get_options_flow(
    symbol: str,
    limit: int = Query(100, le=500, description="Max trades to return")
):
    """
    Get real-time options flow/trades

    - **symbol**: Stock ticker
    - **limit**: Maximum number of trades
    """
    try:
        options_service = get_options_data_service()
        flow = await options_service.get_options_flow(symbol, limit)

        return {
            "symbol": symbol,
            "trades": flow,
            "count": len(flow)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flow/unusual")
async def get_market_unusual_activity(
    symbol: Optional[str] = None,
    min_premium: float = Query(50000, description="Minimum premium"),
    min_volume: int = Query(500, description="Minimum volume")
):
    """
    Get unusual options activity across the market

    - **symbol**: Filter by symbol (None for all)
    - **min_premium**: Minimum premium threshold
    - **min_volume**: Minimum volume threshold
    """
    try:
        options_service = get_options_data_service()
        unusual = await options_service.get_unusual_activity(
            symbol=symbol,
            min_premium=min_premium,
            min_volume=min_volume
        )

        return {
            "unusual_activity": unusual,
            "count": len(unusual)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/flow/darkpool/{symbol}")
async def get_darkpool_prints(
    symbol: str,
    min_size: int = Query(10000, description="Minimum trade size")
):
    """
    Get darkpool options prints

    - **symbol**: Stock ticker
    - **min_size**: Minimum trade size
    """
    try:
        options_service = get_options_data_service()
        darkpool = await options_service.get_darkpool_prints(symbol, min_size)

        return {
            "symbol": symbol,
            "darkpool_trades": darkpool,
            "count": len(darkpool)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# VOLATILITY SURFACE ENDPOINTS
# ============================================================================

@router.get("/volatility/{symbol}/surface")
async def get_volatility_surface(symbol: str):
    """
    Get volatility surface data (IV by strike and expiration)

    - **symbol**: Stock ticker
    """
    try:
        options_service = get_options_data_service()
        chain = await options_service.get_options_chain(
            symbol=symbol,
            expiry_date=None,
            include_greeks=False
        )

        spot_price = chain.get("spot_price", 150.0)

        # Prepare options data for surface calculation
        options_data = []
        for call in chain.get("calls", []):
            options_data.append({
                "strike": call["strike"],
                "expiry": call["expiry"],
                "type": "call",
                "price": call.get("last_price", 0),
                "time_to_expiry": greeks_calc.calculate_time_to_expiry(
                    datetime.strptime(call["expiry"], "%Y-%m-%d")
                )
            })

        # Calculate surface
        surface_df = vol_surface.calculate_iv_surface(options_data, spot_price)

        # Convert DataFrame to dict for JSON response
        surface_data = surface_df.to_dict(orient="records") if not surface_df.empty else []

        return {
            "symbol": symbol,
            "spot_price": spot_price,
            "surface_data": surface_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/volatility/{symbol}/skew")
async def get_volatility_skew(
    symbol: str,
    expiry: Optional[str] = None
):
    """
    Get volatility skew (IV vs strike)

    - **symbol**: Stock ticker
    - **expiry**: Filter to specific expiration
    """
    try:
        options_service = get_options_data_service()
        chain = await options_service.get_options_chain(
            symbol=symbol,
            expiry_date=expiry,
            include_greeks=False
        )

        spot_price = chain.get("spot_price", 150.0)

        # Prepare options data
        options_data = []
        for option_type, options_list in [("call", chain.get("calls", [])), ("put", chain.get("puts", []))]:
            for option in options_list:
                options_data.append({
                    "strike": option["strike"],
                    "expiry": option["expiry"],
                    "type": option_type,
                    "price": option.get("last_price", 0),
                    "time_to_expiry": greeks_calc.calculate_time_to_expiry(
                        datetime.strptime(option["expiry"], "%Y-%m-%d")
                    )
                })

        skew = vol_surface.calculate_volatility_skew(
            options_data,
            spot_price,
            expiry_filter=expiry
        )

        return {
            "symbol": symbol,
            "expiry": expiry,
            "spot_price": spot_price,
            **skew
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/volatility/{symbol}/term-structure")
async def get_term_structure(
    symbol: str,
    strike: Optional[float] = None
):
    """
    Get volatility term structure (IV vs time to expiry)

    - **symbol**: Stock ticker
    - **strike**: Filter to specific strike (None for ATM)
    """
    try:
        options_service = get_options_data_service()
        chain = await options_service.get_options_chain(
            symbol=symbol,
            expiry_date=None,
            include_greeks=False
        )

        spot_price = chain.get("spot_price", 150.0)

        # Prepare options data
        options_data = []
        for call in chain.get("calls", []):
            options_data.append({
                "strike": call["strike"],
                "expiry": call["expiry"],
                "type": "call",
                "price": call.get("last_price", 0),
                "time_to_expiry": greeks_calc.calculate_time_to_expiry(
                    datetime.strptime(call["expiry"], "%Y-%m-%d")
                )
            })

        term_structure = vol_surface.calculate_term_structure(
            options_data,
            spot_price,
            strike_filter=strike
        )

        return {
            "symbol": symbol,
            "strike_filter": strike or "ATM",
            "spot_price": spot_price,
            **term_structure
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# STRATEGY BUILDER ENDPOINTS
# ============================================================================

@router.post("/strategies/vertical-spread")
async def analyze_vertical_spread(request: VerticalSpreadRequest):
    """
    Analyze vertical spread (bull call or bear put)

    Calculate P&L profile, max profit/loss, breakevens, and risk/reward
    """
    try:
        result = spread_analyzer.calculate_vertical_spread(
            long_strike=request.long_strike,
            short_strike=request.short_strike,
            spread_type=request.spread_type,
            debit=request.debit,
            spot_price=request.spot_price,
            num_contracts=request.num_contracts
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/strategies/iron-condor")
async def analyze_iron_condor(request: IronCondorRequest):
    """
    Analyze iron condor spread

    Calculate P&L profile, max profit/loss, breakevens, and probability of profit
    """
    try:
        result = spread_analyzer.calculate_iron_condor(
            put_long_strike=request.put_long_strike,
            put_short_strike=request.put_short_strike,
            call_short_strike=request.call_short_strike,
            call_long_strike=request.call_long_strike,
            credit=request.credit,
            spot_price=request.spot_price,
            num_contracts=request.num_contracts
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/strategies/straddle")
async def analyze_straddle(request: StraddleRequest):
    """
    Analyze straddle (long or short)

    Calculate P&L profile, breakevens, and risk metrics
    """
    try:
        result = spread_analyzer.calculate_straddle(
            strike=request.strike,
            call_price=request.call_price,
            put_price=request.put_price,
            spot_price=request.spot_price,
            num_contracts=request.num_contracts,
            is_long=request.is_long
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/greeks/calculate")
async def calculate_greeks(request: GreeksRequest):
    """
    Calculate Greeks for a single option

    Returns delta, gamma, theta, vega, rho, and theoretical price
    """
    try:
        greeks = greeks_calc.calculate_greeks(
            spot_price=request.spot_price,
            strike=request.strike,
            time_to_expiry=request.time_to_expiry,
            risk_free_rate=request.risk_free_rate,
            volatility=request.volatility,
            option_type=request.option_type
        )

        return greeks

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
