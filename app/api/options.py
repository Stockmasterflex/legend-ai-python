"""
Options API Endpoints
Provides access to options data, screeners, strategies, and pattern integration
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

from app.services.options_data import get_options_service
from app.services.options_screener import get_options_screener
from app.services.options_strategy import get_strategy_builder
from app.services.options_pattern_integration import get_pattern_enhancer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/options", tags=["options"])


# Request/Response Models
class OptionsChainRequest(BaseModel):
    """Request model for options chain"""
    symbol: str = Field(..., description="Stock ticker symbol", example="AAPL")
    expiration: Optional[str] = Field(None, description="Expiration date (YYYY-MM-DD)", example="2025-12-19")
    min_strike: Optional[float] = Field(None, description="Minimum strike price", example=150.0)
    max_strike: Optional[float] = Field(None, description="Maximum strike price", example=200.0)


class UnusualActivityRequest(BaseModel):
    """Request model for unusual options activity"""
    symbol: Optional[str] = Field(None, description="Stock ticker or None for market-wide scan", example="TSLA")
    min_premium: float = Field(30000, description="Minimum premium threshold ($)", example=50000)
    min_volume_oi_ratio: float = Field(2.0, description="Minimum volume/OI ratio", example=2.5)


class HighIVScanRequest(BaseModel):
    """Request model for high IV rank scan"""
    symbols: Optional[List[str]] = Field(None, description="Symbols to scan, or None for default watchlist")
    min_iv_rank: float = Field(70.0, description="Minimum IV rank percentile", example=75.0)
    max_results: int = Field(50, description="Maximum results to return", example=25)


class StrategyRequest(BaseModel):
    """Request model for options strategy"""
    symbol: str = Field(..., description="Stock ticker symbol", example="AAPL")
    strategy_type: str = Field(..., description="Strategy type: covered_call, protective_put, bull_call, bear_put", example="covered_call")
    stock_quantity: Optional[int] = Field(100, description="Stock quantity (for covered calls/protective puts)", example=100)
    target_delta: Optional[float] = Field(0.30, description="Target delta (for covered calls)", example=0.30)
    protection_level: Optional[float] = Field(0.05, description="Protection level (for protective puts)", example=0.05)
    spread_width: Optional[float] = Field(5.0, description="Strike width (for spreads)", example=5.0)
    expiration: Optional[str] = Field(None, description="Expiration date", example="2025-12-19")


class PatternEnhanceRequest(BaseModel):
    """Request model for pattern enhancement with options data"""
    symbol: str = Field(..., description="Stock ticker symbol", example="AAPL")
    pattern_result: Dict[str, Any] = Field(..., description="Pattern detection result")
    include_strategies: bool = Field(False, description="Include strategy suggestions", example=True)


# Endpoints
@router.post("/chain",
             summary="Get Options Chain",
             description="Retrieve options chain data with strikes, Greeks, volume, and open interest")
async def get_options_chain(request: OptionsChainRequest):
    """Get options chain for a symbol"""
    try:
        options_service = get_options_service()

        strike_range = None
        if request.min_strike and request.max_strike:
            strike_range = (request.min_strike, request.max_strike)

        chain = await options_service.get_options_chain(
            symbol=request.symbol,
            expiration=request.expiration,
            strike_range=strike_range
        )

        if "error" in chain:
            raise HTTPException(status_code=400, detail=chain["error"])

        return {
            "success": True,
            "data": chain,
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting options chain: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/unusual-activity",
             summary="Detect Unusual Options Activity",
             description="Find unusual options trades with high volume and premium")
async def get_unusual_activity(request: UnusualActivityRequest):
    """Detect unusual options activity"""
    try:
        options_service = get_options_service()

        unusual = await options_service.get_unusual_activity(
            symbol=request.symbol,
            min_premium=request.min_premium,
            min_volume_oi_ratio=request.min_volume_oi_ratio
        )

        return {
            "success": True,
            "data": unusual,
            "count": len(unusual),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error detecting unusual activity: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/put-call-ratio/{symbol}",
            summary="Get Put/Call Ratio",
            description="Calculate put/call ratio for volume and open interest")
async def get_put_call_ratio(
    symbol: str,
    expiration: Optional[str] = Query(None, description="Expiration date (YYYY-MM-DD)")
):
    """Get put/call ratio for a symbol"""
    try:
        options_service = get_options_service()

        pc_ratio = await options_service.get_put_call_ratio(
            symbol=symbol,
            expiration=expiration
        )

        if "error" in pc_ratio:
            raise HTTPException(status_code=400, detail=pc_ratio["error"])

        return {
            "success": True,
            "data": pc_ratio,
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting P/C ratio: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/open-interest/{symbol}",
            summary="Analyze Open Interest",
            description="Get open interest analysis with max pain and support/resistance levels")
async def get_open_interest_analysis(
    symbol: str,
    expiration: Optional[str] = Query(None, description="Expiration date (YYYY-MM-DD)")
):
    """Get open interest analysis"""
    try:
        options_service = get_options_service()

        oi_analysis = await options_service.get_open_interest_analysis(
            symbol=symbol,
            expiration=expiration
        )

        if "error" in oi_analysis:
            raise HTTPException(status_code=400, detail=oi_analysis["error"])

        return {
            "success": True,
            "data": oi_analysis,
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing open interest: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/iv-percentile/{symbol}",
            summary="Get IV Percentile",
            description="Calculate IV percentile and rank vs historical")
async def get_iv_percentile(
    symbol: str,
    lookback_days: int = Query(252, description="Historical lookback period in days")
):
    """Get IV percentile"""
    try:
        options_service = get_options_service()

        iv_data = await options_service.get_iv_percentile(
            symbol=symbol,
            lookback_days=lookback_days
        )

        if "error" in iv_data:
            raise HTTPException(status_code=400, detail=iv_data["error"])

        return {
            "success": True,
            "data": iv_data,
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting IV percentile: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/screener/high-iv",
             summary="Scan High IV Stocks",
             description="Screen for stocks with high implied volatility rank")
async def scan_high_iv(request: HighIVScanRequest):
    """Scan for high IV rank stocks"""
    try:
        screener = get_options_screener()

        results = await screener.scan_high_iv_stocks(
            symbols=request.symbols,
            min_iv_rank=request.min_iv_rank,
            max_results=request.max_results
        )

        return {
            "success": True,
            "data": results,
            "count": len(results),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error scanning high IV stocks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/screener/unusual-volume/{symbol}",
            summary="Detect Unusual Volume",
            description="Detect unusual options volume spikes vs average")
async def detect_unusual_volume(
    symbol: str,
    lookback_days: int = Query(20, description="Days to compare against average")
):
    """Detect unusual volume for a symbol"""
    try:
        screener = get_options_screener()

        unusual_vol = await screener.detect_unusual_volume(
            symbol=symbol,
            lookback_days=lookback_days
        )

        if "error" in unusual_vol:
            raise HTTPException(status_code=400, detail=unusual_vol["error"])

        return {
            "success": True,
            "data": unusual_vol,
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error detecting unusual volume: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/screener/block-trades/{symbol}",
            summary="Detect Block Trades",
            description="Find large institutional block trades")
async def detect_block_trades(
    symbol: str,
    min_premium: float = Query(100000, description="Minimum premium for block trade ($)")
):
    """Detect block trades"""
    try:
        screener = get_options_screener()

        blocks = await screener.detect_block_trades(
            symbol=symbol,
            min_premium=min_premium
        )

        return {
            "success": True,
            "data": blocks,
            "count": len(blocks),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error detecting block trades: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/screener/sweeps/{symbol}",
            summary="Detect Sweep Orders",
            description="Find aggressive sweep orders indicating urgency")
async def detect_sweeps(
    symbol: str,
    min_premium: float = Query(50000, description="Minimum premium threshold ($)")
):
    """Detect sweep orders"""
    try:
        screener = get_options_screener()

        sweeps = await screener.detect_sweeps(
            symbol=symbol,
            min_premium=min_premium
        )

        return {
            "success": True,
            "data": sweeps,
            "count": len(sweeps),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error detecting sweeps: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/screener/dark-pool/{symbol}",
            summary="Detect Dark Pool Activity",
            description="Find off-exchange dark pool trades")
async def detect_dark_pool(
    symbol: str,
    min_size: int = Query(10000, description="Minimum share size")
):
    """Detect dark pool activity"""
    try:
        screener = get_options_screener()

        dark_pool = await screener.detect_dark_pool_activity(
            symbol=symbol,
            min_size=min_size
        )

        return {
            "success": True,
            "data": dark_pool,
            "count": len(dark_pool),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error detecting dark pool activity: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/screener/comprehensive/{symbol}",
            summary="Comprehensive Options Scan",
            description="Run all screeners on a symbol for complete analysis")
async def comprehensive_scan(symbol: str):
    """Run comprehensive options scan"""
    try:
        screener = get_options_screener()

        report = await screener.comprehensive_scan(symbol)

        if "error" in report:
            raise HTTPException(status_code=400, detail=report["error"])

        return {
            "success": True,
            "data": report,
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in comprehensive scan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/strategy/covered-call",
             summary="Build Covered Call",
             description="Create covered call strategy with P&L analysis")
async def build_covered_call(request: StrategyRequest):
    """Build covered call strategy"""
    try:
        strategy_builder = get_strategy_builder()

        strategy = await strategy_builder.build_covered_call(
            symbol=request.symbol,
            stock_quantity=request.stock_quantity or 100,
            target_delta=request.target_delta or 0.30,
            expiration=request.expiration
        )

        if "error" in strategy:
            raise HTTPException(status_code=400, detail=strategy["error"])

        return {
            "success": True,
            "data": strategy,
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error building covered call: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/strategy/protective-put",
             summary="Build Protective Put",
             description="Create protective put hedge with cost analysis")
async def build_protective_put(request: StrategyRequest):
    """Build protective put strategy"""
    try:
        strategy_builder = get_strategy_builder()

        strategy = await strategy_builder.build_protective_put(
            symbol=request.symbol,
            stock_quantity=request.stock_quantity or 100,
            protection_level=request.protection_level or 0.05,
            expiration=request.expiration
        )

        if "error" in strategy:
            raise HTTPException(status_code=400, detail=strategy["error"])

        return {
            "success": True,
            "data": strategy,
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error building protective put: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/strategy/vertical-spread",
             summary="Build Vertical Spread",
             description="Create bull/bear spread with risk/reward visualization")
async def build_vertical_spread(request: StrategyRequest):
    """Build vertical spread strategy"""
    try:
        strategy_builder = get_strategy_builder()

        strategy = await strategy_builder.build_vertical_spread(
            symbol=request.symbol,
            spread_type=request.strategy_type,  # bull_call, bear_put, etc.
            width=request.spread_width or 5.0,
            expiration=request.expiration
        )

        if "error" in strategy:
            raise HTTPException(status_code=400, detail=strategy["error"])

        return {
            "success": True,
            "data": strategy,
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error building vertical spread: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pattern/enhance",
             summary="Enhance Pattern with Options Flow",
             description="Add options flow analysis to pattern detection result")
async def enhance_pattern(request: PatternEnhanceRequest):
    """Enhance pattern with options flow"""
    try:
        enhancer = get_pattern_enhancer()

        enhanced = await enhancer.enhance_pattern(
            symbol=request.symbol,
            pattern_result=request.pattern_result,
            include_strategies=request.include_strategies
        )

        return {
            "success": True,
            "data": enhanced,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error enhancing pattern: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/greeks/calculate",
            summary="Calculate Greeks",
            description="Calculate Black-Scholes Greeks for an option")
async def calculate_greeks(
    spot_price: float = Query(..., description="Current stock price"),
    strike: float = Query(..., description="Strike price"),
    time_to_expiry: float = Query(..., description="Time to expiration (years)"),
    volatility: float = Query(..., description="Implied volatility (decimal, e.g., 0.30)"),
    risk_free_rate: float = Query(0.05, description="Risk-free rate (decimal)"),
    option_type: str = Query("call", description="Option type: call or put")
):
    """Calculate option Greeks"""
    try:
        options_service = get_options_service()

        greeks = await options_service.calculate_greeks(
            spot_price=spot_price,
            strike=strike,
            time_to_expiry=time_to_expiry,
            volatility=volatility,
            risk_free_rate=risk_free_rate,
            option_type=option_type
        )

        if "error" in greeks:
            raise HTTPException(status_code=400, detail=greeks["error"])

        return {
            "success": True,
            "data": greeks,
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating Greeks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usage",
            summary="Get API Usage Stats",
            description="Get options API usage statistics")
async def get_usage_stats():
    """Get API usage statistics"""
    try:
        options_service = get_options_service()
        stats = await options_service.get_usage_stats()

        return {
            "success": True,
            "data": stats,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error getting usage stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
