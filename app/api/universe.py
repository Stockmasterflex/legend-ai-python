"""
Universe Scanner API Endpoints

Provides endpoints for scanning S&P 500 and NASDAQ 100 for pattern setups.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from app.services.universe import universe_service
from app.services.universe_data import (
    get_nasdaq,
    get_sp500,
    get_quick_scan_universe,
)
from app.services.market_data import market_data_service
from app.services.cache import get_cache_service
from app.services.universe_store import universe_store
from app.core.pattern_detector import PatternDetector, PatternResult

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


class QuickScanRequest(BaseModel):
    """Request payload for the quick scan endpoint"""

    universe: str = "nasdaq100"
    limit: int = 25
    min_score: float = 7.0
    min_rs: float = 60.0
    pattern_types: Optional[List[str]] = None
    timeframe: str = "1day"
    sector: Optional[str] = None
    max_atr_percent: Optional[float] = None


def _normalize_pattern_filters(patterns: Optional[List[str]]) -> set[str]:
    """Map UI pattern labels to internal detector names."""
    if not patterns:
        return set()
    alias_map = {
        "vcp": {
            "vcp",
            "volatility contraction",
            "pullback to 21 ema",
            "pullback to 21",
        },
        "cup & handle": {
            "cup & handle",
            "cup handle",
            "cup-and-handle",
        },
        "flat base": {
            "flat base",
            "pullback to 50",
            "pullback to 50 sma",
            "pullback to 50-day",
        },
        "breakout": {
            "breakout",
            "ascending triangle",
            "symmetrical triangle",
            "triangle",
            "rising wedge",
            "falling wedge",
            "head & shoulders",
            "inverse head & shoulders",
        },
    }
    normalized = set()
    for raw in patterns:
        if not raw:
            continue
        slug = (
            raw.replace("&amp;", "&")
            .replace("-", " ")
            .strip()
            .lower()
        )
        if slug in {"", "all"}:
            continue
        slug = " ".join(slug.split())
        for canonical, aliases in alias_map.items():
            if slug == canonical or slug in aliases:
                normalized.add(canonical)
                break
    return normalized


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


def _compute_atr_percent(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> Optional[float]:
    """Calculate ATR as a percent of the latest close price."""

    try:
        if not highs or not lows or not closes or len(closes) <= period:
            return None

        true_ranges = []
        for idx in range(1, len(closes)):
            high = highs[idx]
            low = lows[idx]
            prev_close = closes[idx - 1]
            tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
            true_ranges.append(tr)

        if len(true_ranges) < period:
            return None

        recent_tr = true_ranges[-period:]
        atr = sum(recent_tr) / period if recent_tr else 0
        latest_close = closes[-1]

        if not latest_close:
            return None

        return round((atr / latest_close) * 100, 2)
    except Exception:
        return None


@router.post("/scan/quick")
async def quick_scan(request: QuickScanRequest):
    """Responsive quick scan aligned with dashboard contract."""

    universe_map = {
        "nasdaq100": ("NASDAQ 100", get_nasdaq),
        "sp500": ("S&P 500", get_sp500),
        "focus": ("Trend Template", get_quick_scan_universe),
    }

    try:
        metadata_map = await universe_store.get_all()
        sector_filter = (request.sector or "").strip().lower() or None
        requested_interval = (request.timeframe or "1day").lower()
        interval = "1week" if "week" in requested_interval else "1day"

        universe_key = request.universe.lower().strip()
        label, universe_fn = universe_map.get(universe_key, ("Focus", get_quick_scan_universe))
        tickers = universe_fn()

        def _matches_sector(symbol: str) -> bool:
            if not sector_filter:
                return True
            meta = metadata_map.get(symbol.upper())
            if not meta or not meta.get("sector"):
                return False
            return meta["sector"].strip().lower() == sector_filter

        filtered_universe = [ticker for ticker in tickers if _matches_sector(ticker)]
        if not filtered_universe:
            filtered_universe = tickers

        scan_limit = max(5, min(request.limit, len(filtered_universe)))
        pool_size = min(len(filtered_universe), max(scan_limit * 2, scan_limit + 10))
        tickers_to_scan = filtered_universe[:pool_size]

        detector = PatternDetector()
        cache = get_cache_service()
        cache_hits = 0
        spy_data = await market_data_service.get_time_series(
            "SPY",
            interval,
            400 if interval == "1day" else 260,
        )

        normalized_patterns = _normalize_pattern_filters(request.pattern_types)

        rows: List[Dict[str, Any]] = []

        for ticker in tickers_to_scan:
            price_data = None
            pattern_result = None

            try:
                cache_interval = interval
                cached_pattern = await cache.get_pattern(ticker, cache_interval)
                if cached_pattern:
                    cache_hits += 1
                    if isinstance(cached_pattern.get("timestamp"), str):
                        cached_pattern["timestamp"] = datetime.fromisoformat(cached_pattern["timestamp"])

                    pattern_result = PatternResult(**cached_pattern)

                if pattern_result is None:
                    price_data = await market_data_service.get_time_series(ticker, interval, 400)
                    if not price_data:
                        continue

                    pattern_result = await detector.analyze_ticker(ticker, price_data, spy_data)

                    if pattern_result:
                        await cache.set_pattern(ticker, cache_interval, pattern_result.to_dict())

                if pattern_result is None:
                    continue

                if pattern_result.score < request.min_score:
                    continue

                rs_rating = pattern_result.rs_rating
                if request.min_rs and (rs_rating is None or rs_rating < request.min_rs):
                    continue

                if request.pattern_types:
                    pattern_name = (pattern_result.pattern or "").strip().lower()
                    if normalized_patterns and pattern_name not in normalized_patterns:
                        continue

                if price_data is None:
                    price_data = await market_data_service.get_time_series(ticker, interval, 200)

                atr_percent = None
                if price_data and all(k in price_data for k in ("h", "l", "c")):
                    atr_percent = _compute_atr_percent(price_data["h"], price_data["l"], price_data["c"])

                if request.max_atr_percent and atr_percent and atr_percent > request.max_atr_percent:
                    continue

                meta = metadata_map.get(ticker.upper())

                rows.append({
                    "ticker": ticker,
                    "pattern": pattern_result.pattern,
                    "score": pattern_result.score,
                    "entry": pattern_result.entry,
                    "stop": pattern_result.stop,
                    "target": pattern_result.target,
                    "rs_rating": rs_rating,
                    "atr_percent": atr_percent,
                    "current_price": pattern_result.current_price,
                    "source": label,
                    "sector": meta.get("sector") if meta else None,
                    "timeframe": interval,
                    "chart_url": pattern_result.chart_url,
                })

            except Exception as ticker_error:
                logger.debug(f"Quick scan error for {ticker}: {ticker_error}")
                continue

        rows.sort(key=lambda item: item.get("score", 0), reverse=True)
        limited_rows = rows[: scan_limit]
        stats_payload = {
            "universe": label,
            "requested_universe": request.universe,
            "candidates": len(filtered_universe),
            "scanned": len(tickers_to_scan),
            "cache_hits": cache_hits,
            "min_score": request.min_score,
            "min_rs": request.min_rs,
            "timeframe": interval,
            "sector_filter": sector_filter or "all",
        }

        return {
            "success": True,
            "data": limited_rows,
            "stats": stats_payload,
            "message": f"Quick scan completed for {label}",
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


@router.post("/seed")
async def seed_universe_manual():
    """
    Manually trigger universe seeding

    This endpoint forces a refresh of the universe store, loading all
    S&P 500 and NASDAQ 100 tickers with metadata. Use this if:
    - Health check shows "seeded": false
    - Top setups are timing out
    - After Railway deployment to ensure universe is populated

    Returns:
        Dictionary with success status and number of symbols loaded
    """
    try:
        logger.info("🔄 Manual universe seed triggered")
        result = await universe_store.seed(force=True)
        symbol_count = len(result) if isinstance(result, dict) else 0

        logger.info(f"✅ Universe seeded successfully: {symbol_count} symbols")

        return {
            "success": True,
            "symbols_loaded": symbol_count,
            "message": f"Universe seeded with {symbol_count} symbols",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Manual universe seed failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to seed universe: {str(e)}"
        )
