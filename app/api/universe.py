"""
Universe Scanner API Endpoints

Provides endpoints for scanning S&P 500 and NASDAQ 100 for pattern setups.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging

from app.services.universe import universe_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/universe", tags=["universe"])


class ScanRequest(BaseModel):
    """Request model for universe scan"""
    min_score: float = 7.0
    max_results: int = 20
    pattern_types: Optional[List[str]] = None  # Filter by patterns: ["VCP", "Cup & Handle"]


class ScanResult(BaseModel):
    """Scan result model"""
    ticker: str
    pattern: str
    score: float
    entry: float
    stop: float
    target: float
    risk_reward: float
    current_price: Optional[float]
    source: str  # "SP500" or "NASDAQ100"


class ScanResponse(BaseModel):
    """Response model for scan"""
    success: bool
    results: List[ScanResult]
    total_scanned: int
    total_found: int
    cached: bool
    scan_time: Optional[float] = None


@router.get("/health")
async def health():
    """Health check for universe service"""
    return {
        "status": "healthy",
        "message": "Universe scanner ready"
    }


@router.get("/tickers")
async def get_universe_tickers():
    """
    Get full universe ticker list (S&P 500 + NASDAQ 100)
    
    Returns:
        List of all tickers in the universe
    """
    try:
        universe = await universe_service.get_full_universe()
        
        return {
            "success": True,
            "total": len(universe),
            "tickers": [item["ticker"] for item in universe],
            "sources": {
                "SP500": len([u for u in universe if u["source"] == "SP500"]),
                "NASDAQ100": len([u for u in universe if u["source"] == "NASDAQ100"])
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting universe: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scan", response_model=ScanResponse)
async def scan_universe(request: ScanRequest):
    """
    Scan full universe (S&P 500 + NASDAQ 100) for pattern setups
    
    This endpoint is rate-limited and cached to avoid API abuse.
    Results are cached for 24 hours.
    
    Args:
        request: Scan configuration
        
    Returns:
        Top pattern setups sorted by score
        
    Example:
        POST /api/universe/scan
        {
            "min_score": 7.5,
            "max_results": 10,
            "pattern_types": ["VCP", "Cup & Handle"]
        }
    """
    try:
        import time
        start_time = time.time()
        
        logger.info(f"🔍 Starting universe scan (min_score={request.min_score}, max={request.max_results})")
        
        # Run scan
        results = await universe_service.scan_universe(
            min_score=request.min_score,
            max_results=request.max_results,
            pattern_types=request.pattern_types
        )
        
        scan_time = time.time() - start_time
        
        # Check if results were cached
        cached = scan_time < 1.0  # If it took < 1s, it was probably cached
        
        logger.info(f"✅ Universe scan complete: {len(results)} setups found in {scan_time:.2f}s")
        
        return ScanResponse(
            success=True,
            results=[ScanResult(**r) for r in results],
            total_scanned=600,  # Approximate
            total_found=len(results),
            cached=cached,
            scan_time=round(scan_time, 2)
        )
        
    except Exception as e:
        logger.error(f"Universe scan error: {e}")
        return ScanResponse(
            success=False,
            results=[],
            total_scanned=0,
            total_found=0,
            cached=False,
            scan_time=0
        )


@router.post("/scan/quick")
async def quick_scan():
    """
    Quick scan of top 50 most liquid stocks
    
    Faster alternative to full universe scan for quick insights.
    Uses cached data when available.
    
    Returns:
        Top 10 setups from high-volume stocks
    """
    try:
        # Define top 50 most liquid stocks
        top_50 = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK.B",
            "V", "UNH", "JPM", "WMT", "MA", "PG", "HD", "CVX",
            "ABBV", "KO", "PEP", "COST", "MRK", "ADBE", "CSCO", "TMO",
            "ACN", "NFLX", "ABT", "WFC", "DHR", "BAC", "NKE", "TXN",
            "DIS", "VZ", "QCOM", "INTC", "INTU", "ORCL", "AMD", "CMCSA",
            "CRM", "RTX", "HON", "AMGN", "NEE", "COP", "IBM", "LOW",
            "CAT", "SPGI"
        ]
        
        from app.core.pattern_detector import PatternDetector
        detector = PatternDetector()
        results = []
        
        for ticker in top_50[:30]:  # Scan first 30 for speed
            try:
                # Check cache
                from app.services.cache import get_cache_service
                cache = get_cache_service()
                cached_pattern = await cache.get_pattern(ticker, "1day")
                
                if cached_pattern:
                    from app.core.pattern_detector import PatternResult
                    from datetime import datetime
                    if isinstance(cached_pattern.get("timestamp"), str):
                        cached_pattern["timestamp"] = datetime.fromisoformat(cached_pattern["timestamp"])
                    
                    pattern_result = PatternResult(**cached_pattern)
                    
                    if pattern_result.score >= 7.0:
                        results.append({
                            "ticker": ticker,
                            "pattern": pattern_result.pattern,
                            "score": pattern_result.score,
                            "entry": pattern_result.entry,
                            "stop": pattern_result.stop,
                            "target": pattern_result.target
                        })
                        
            except Exception as e:
                logger.debug(f"Quick scan {ticker} error: {e}")
                continue
        
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "success": True,
            "results": results[:10],
            "scanned": len(top_50[:30]),
            "message": "Quick scan of top liquid stocks (cached data)"
        }
        
    except Exception as e:
        logger.error(f"Quick scan error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sp500")
async def get_sp500():
    """Get S&P 500 ticker list"""
    try:
        tickers = await universe_service.get_sp500_tickers()
        return {
            "success": True,
            "total": len(tickers),
            "tickers": tickers
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nasdaq100")
async def get_nasdaq100():
    """Get NASDAQ 100 ticker list"""
    try:
        tickers = await universe_service.get_nasdaq100_tickers()
        return {
            "success": True,
            "total": len(tickers),
            "tickers": tickers
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

