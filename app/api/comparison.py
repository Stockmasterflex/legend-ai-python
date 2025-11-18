"""
Multi-Ticker Comparison API Endpoints
"""
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging

from app.services.ticker_comparison import ticker_comparison_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/comparison", tags=["comparison"])


class ComparisonRequest(BaseModel):
    """Request model for multi-ticker comparison."""
    tickers: List[str] = Field(..., min_items=2, max_items=9, description="2-9 tickers to compare")
    interval: str = Field(default="1day", description="Time interval (1day, 1hour, etc.)")
    bars: int = Field(default=252, ge=10, le=1000, description="Number of bars to fetch")
    benchmark: str = Field(default="SPY", description="Benchmark symbol for relative strength")


class PairTradingRequest(BaseModel):
    """Request model for pair trading analysis."""
    ticker1: str = Field(..., description="First ticker symbol")
    ticker2: str = Field(..., description="Second ticker symbol")
    interval: str = Field(default="1day", description="Time interval")
    bars: int = Field(default=252, ge=10, le=1000, description="Number of bars")


class RSRankingRequest(BaseModel):
    """Request model for relative strength ranking."""
    tickers: List[str] = Field(..., min_items=2, description="Tickers to rank")
    benchmark: str = Field(default="SPY", description="Benchmark symbol")
    interval: str = Field(default="1day", description="Time interval")
    bars: int = Field(default=100, ge=10, le=500, description="Number of bars")


@router.post("/compare")
async def compare_tickers(request: ComparisonRequest) -> Dict[str, Any]:
    """
    Compare multiple tickers side-by-side with comprehensive analytics.

    Features:
    - Multi-chart synchronized data
    - Metrics comparison table
    - Relative strength analysis
    - Correlation matrix
    - Leader/laggard identification

    Example:
        POST /api/comparison/compare
        {
            "tickers": ["AAPL", "MSFT", "GOOGL", "META"],
            "interval": "1day",
            "bars": 252,
            "benchmark": "SPY"
        }
    """
    try:
        logger.info(f"Comparing tickers: {request.tickers}")

        result = await ticker_comparison_service.compare_tickers(
            tickers=request.tickers,
            interval=request.interval,
            bars=request.bars,
            benchmark=request.benchmark,
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except Exception as e:
        logger.error(f"Error in compare_tickers endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")


@router.get("/compare")
async def compare_tickers_get(
    tickers: str = Query(..., description="Comma-separated list of tickers (e.g., 'AAPL,MSFT,GOOGL')"),
    interval: str = Query(default="1day", description="Time interval"),
    bars: int = Query(default=252, ge=10, le=1000, description="Number of bars"),
    benchmark: str = Query(default="SPY", description="Benchmark symbol"),
) -> Dict[str, Any]:
    """
    GET endpoint for comparing tickers (alternative to POST).

    Example:
        GET /api/comparison/compare?tickers=AAPL,MSFT,GOOGL&interval=1day&bars=252&benchmark=SPY
    """
    ticker_list = [t.strip().upper() for t in tickers.split(",")]

    if len(ticker_list) < 2:
        raise HTTPException(status_code=400, detail="At least 2 tickers required")

    if len(ticker_list) > 9:
        raise HTTPException(status_code=400, detail="Maximum 9 tickers allowed")

    request = ComparisonRequest(
        tickers=ticker_list,
        interval=interval,
        bars=bars,
        benchmark=benchmark,
    )

    return await compare_tickers(request)


@router.post("/pair-trading")
async def pair_trading_analysis(request: PairTradingRequest) -> Dict[str, Any]:
    """
    Analyze pair trading opportunities between two tickers.

    Features:
    - Spread chart (price ratio)
    - Z-score calculations (rolling)
    - Mean reversion signals
    - Cointegration test (Engle-Granger)
    - Hedge ratio calculation

    Example:
        POST /api/comparison/pair-trading
        {
            "ticker1": "GLD",
            "ticker2": "GDX",
            "interval": "1day",
            "bars": 252
        }
    """
    try:
        logger.info(f"Pair trading analysis: {request.ticker1} vs {request.ticker2}")

        result = await ticker_comparison_service.pair_trading_analysis(
            ticker1=request.ticker1,
            ticker2=request.ticker2,
            interval=request.interval,
            bars=request.bars,
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except Exception as e:
        logger.error(f"Error in pair_trading_analysis endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Pair trading analysis failed: {str(e)}")


@router.get("/pair-trading")
async def pair_trading_analysis_get(
    ticker1: str = Query(..., description="First ticker symbol"),
    ticker2: str = Query(..., description="Second ticker symbol"),
    interval: str = Query(default="1day", description="Time interval"),
    bars: int = Query(default=252, ge=10, le=1000, description="Number of bars"),
) -> Dict[str, Any]:
    """
    GET endpoint for pair trading analysis.

    Example:
        GET /api/comparison/pair-trading?ticker1=GLD&ticker2=GDX&interval=1day&bars=252
    """
    request = PairTradingRequest(
        ticker1=ticker1.upper(),
        ticker2=ticker2.upper(),
        interval=interval,
        bars=bars,
    )

    return await pair_trading_analysis(request)


@router.post("/relative-strength")
async def relative_strength_ranking(request: RSRankingRequest) -> Dict[str, Any]:
    """
    Rank tickers by relative strength vs benchmark.

    Features:
    - RS rank (1-99 scale)
    - RS slope (momentum)
    - Delta vs benchmark (outperformance %)
    - Best/worst performers identification

    Example:
        POST /api/comparison/relative-strength
        {
            "tickers": ["AAPL", "MSFT", "GOOGL", "META", "NVDA"],
            "benchmark": "SPY",
            "interval": "1day",
            "bars": 100
        }
    """
    try:
        logger.info(f"RS ranking for {len(request.tickers)} tickers vs {request.benchmark}")

        result = await ticker_comparison_service.relative_strength_ranking(
            tickers=request.tickers,
            benchmark=request.benchmark,
            interval=request.interval,
            bars=request.bars,
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return result

    except Exception as e:
        logger.error(f"Error in relative_strength_ranking endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"RS ranking failed: {str(e)}")


@router.get("/relative-strength")
async def relative_strength_ranking_get(
    tickers: str = Query(..., description="Comma-separated list of tickers"),
    benchmark: str = Query(default="SPY", description="Benchmark symbol"),
    interval: str = Query(default="1day", description="Time interval"),
    bars: int = Query(default=100, ge=10, le=500, description="Number of bars"),
) -> Dict[str, Any]:
    """
    GET endpoint for relative strength ranking.

    Example:
        GET /api/comparison/relative-strength?tickers=AAPL,MSFT,GOOGL,META&benchmark=SPY
    """
    ticker_list = [t.strip().upper() for t in tickers.split(",")]

    if len(ticker_list) < 2:
        raise HTTPException(status_code=400, detail="At least 2 tickers required")

    request = RSRankingRequest(
        tickers=ticker_list,
        benchmark=benchmark,
        interval=interval,
        bars=bars,
    )

    return await relative_strength_ranking(request)


@router.get("/health")
async def health_check():
    """Health check endpoint for comparison service."""
    return {
        "status": "healthy",
        "service": "ticker_comparison",
        "version": "1.0.0",
    }
