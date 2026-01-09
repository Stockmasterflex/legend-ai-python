from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from pathlib import Path
from datetime import datetime, timezone
import logging

from app.core.detector_base import PatternType
from app.core.pattern_detector import PatternDetector, PatternResult
from app.core.pattern_engine.detector import get_pattern_detector
from app.core.pattern_engine.export import PatternExporter
from app.core.pattern_engine.filter import PatternFilter
from app.core.pattern_engine.scoring import PatternScorer
from app.services.market_data import market_data_service
from app.services.cache import get_cache_service
from app.services.charting import get_charting_service
from app.services.pattern_scanner import pattern_scanner_service
from app.services.universe_store import universe_store

logger = logging.getLogger(__name__)
charting_service = get_charting_service()

router = APIRouter(prefix="/api/patterns", tags=["patterns"])
_pattern_filter = PatternFilter()
_pattern_scorer = PatternScorer()
_pattern_exporter = PatternExporter()


class PatternRequest(BaseModel):
    """Request model for pattern detection"""
    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL, TSLA, SPY)", example="AAPL")
    interval: str = Field("1day", description="Time interval: 1min, 5min, 15min, 30min, 1h, 4h, 1day, 1week", example="1day")
    use_yahoo_fallback: bool = Field(True, description="Use Yahoo Finance as fallback data source")
    use_advanced_patterns: bool = Field(True, description="Use advanced pattern detection engine (recommended)")

    @field_validator("interval")
    @classmethod
    def validate_interval(cls, v: str) -> str:
        allowed = {"1min", "5min", "15min", "30min", "1h", "4h", "1day", "1week"}
        if v not in allowed:
            raise ValueError(f"Invalid interval. Must be one of: {', '.join(allowed)}")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "ticker": "AAPL",
                "interval": "1day",
                "use_yahoo_fallback": True
            }
        }


class PatternResponse(BaseModel):
    """Response model for pattern detection"""
    success: bool = Field(..., description="Whether the request was successful")
    data: Optional[PatternResult] = Field(None, description="Pattern analysis result")
    error: Optional[str] = Field(None, description="Error message if request failed")
    cached: bool = Field(False, description="Whether result was served from cache")
    api_used: str = Field("unknown", description="Data source used (cache, twelvedata, finnhub, alphavantage, yahoo)")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "ticker": "AAPL",
                    "pattern": "Cup and Handle",
                    "score": 8.5,
                    "entry": 175.50,
                    "stop": 168.00,
                    "target": 190.25,
                    "support_start": 170.00,
                    "support_end": 172.00,
                    "risk_reward_ratio": 2.1,
                    "chart_url": "https://chart-img.com/AAPL",
                    "timestamp": "2024-01-15T10:30:00"
                },
                "error": None,
                "cached": False,
                "api_used": "twelvedata",
                "processing_time": 1.23
            }
        }

# --------------------------------------------------------------------------- #
# New API request/response models
# --------------------------------------------------------------------------- #
class ScanTickersRequest(BaseModel):
    tickers: List[str]
    interval: str = Field("1day", description="Time interval such as 1day or 1h")
    apply_filters: bool = Field(True, description="Apply PatternFilter to results")
    min_score: float = Field(6.0, ge=0.0, le=10.0, description="Minimum score to include")
    filter_config: Optional[Dict[str, Any]] = Field(None, description="Filter configuration to forward to PatternFilter")


class ScanTickersResponse(BaseModel):
    success: bool
    as_of: datetime
    results: List[Dict[str, Any]]
    errors: Dict[str, Any] = Field(default_factory=dict)
    count: int
    meta: Optional[Dict[str, Any]] = None

    class Config:
        arbitrary_types_allowed = True


class FilterRequest(BaseModel):
    patterns: List[Dict[str, Any]]
    filter_config: Optional[Dict[str, Any]] = None


class FilterResponse(BaseModel):
    results: List[Dict[str, Any]]
    count: int

    class Config:
        arbitrary_types_allowed = True


class ScoreRequest(BaseModel):
    pattern: Dict[str, Any]


class ScoreResponse(BaseModel):
    score: float
    components: Dict[str, float]


class ExportRequest(BaseModel):
    patterns: List[Dict[str, Any]]
    format: str = Field("csv", description="csv | json | excel | clipboard")
    filename: Optional[str] = None
    output_dir: Optional[str] = None


class ExportResponse(BaseModel):
    success: bool
    location: Optional[str] = None
    copied: bool = False


@router.post("/detect",
             response_model=PatternResponse,
             summary="Detect Chart Pattern",
             responses={
                 200: {
                     "description": "Successful pattern detection",
                     "content": {
                         "application/json": {
                             "example": {
                                 "success": True,
                                 "data": {
                                     "ticker": "AAPL",
                                     "pattern": "Cup and Handle",
                                     "score": 8.5,
                                     "entry": 175.50,
                                     "stop": 168.00,
                                     "target": 190.25,
                                     "support_start": 170.00,
                                     "support_end": 172.00,
                                     "risk_reward_ratio": 2.1,
                                     "chart_url": "https://chart-img.com/chart.png",
                                     "timestamp": "2024-01-15T10:30:00"
                                 },
                                 "error": None,
                                 "cached": False,
                                 "api_used": "twelvedata",
                                 "processing_time": 1.23
                             }
                         }
                     }
                 },
                 400: {
                     "description": "Bad Request - Invalid ticker format",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "Invalid ticker symbol format"
                             }
                         }
                     }
                 },
                 404: {
                     "description": "Not Found - No price data available",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "No price data available for INVALID"
                             }
                         }
                     }
                 }
             })
async def detect_pattern(request: PatternRequest):
    """
    🎯 **Detect Chart Pattern for Any Stock**

    Analyzes price action and detects bullish chart patterns with AI-powered scoring.

    ## Features

    - ✅ Multi-source data (TwelveData → Finnhub → AlphaVantage → Yahoo)
    - ✅ Smart caching (1-hour TTL)
    - ✅ Automatic chart generation with indicators
    - ✅ Entry, stop, and target levels
    - ✅ Risk/reward ratio calculation

    ## Supported Patterns

    - Cup and Handle
    - Bullish Flag
    - Ascending Triangle
    - Double Bottom
    - And more...

    ## Example Usage

    **Python:**
    ```python
    import requests

    response = requests.post(
        'https://your-api.com/api/patterns/detect',
        json={'ticker': 'AAPL', 'interval': '1day'}
    )

    result = response.json()
    if result['success']:
        print(f"Pattern: {result['data']['pattern']}")
        print(f"Score: {result['data']['score']}/10")
        print(f"Entry: ${result['data']['entry']}")
    ```

    **cURL:**
    ```bash
    curl -X POST "https://your-api.com/api/patterns/detect" \\
      -H "Content-Type: application/json" \\
      -d '{"ticker": "AAPL", "interval": "1day"}'
    ```

    **JavaScript:**
    ```javascript
    const response = await fetch('/api/patterns/detect', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ticker: 'AAPL', interval: '1day'})
    });
    const result = await response.json();
    ```

    ## Response Fields

    | Field | Type | Description |
    |-------|------|-------------|
    | `success` | boolean | Request success status |
    | `data.pattern` | string | Detected pattern name |
    | `data.score` | float | Confidence score (0-10) |
    | `data.entry` | float | Suggested entry price |
    | `data.stop` | float | Stop loss price |
    | `data.target` | float | Target price |
    | `data.chart_url` | string | Generated chart URL |
    | `cached` | boolean | Served from cache? |
    | `processing_time` | float | Processing time (seconds) |

    ## Notes

    - Cached results are refreshed hourly
    - Chart URLs include support/resistance levels
    - Processing time typically < 2 seconds

    ---

    **Replaces legacy endpoint:** `POST /webhook/pattern-signal`
    """
    import time
    start_time = time.time()
    cache = get_cache_service()

    try:
        ticker = request.ticker.upper().strip()

        # Validate ticker format
        if not ticker or not ticker.replace(".", "").replace("-", "").isalnum():
            raise HTTPException(
                status_code=400,
                detail="Invalid ticker symbol format"
            )

        logger.info(f"🔍 Analyzing pattern for {ticker}")

        # 1. Try cache first
        cached_result = await cache.get_pattern(ticker=ticker, interval=request.interval)
        if cached_result:
            # Convert cached dict back to PatternResult
            # Convert ISO timestamp string back to datetime
            from datetime import datetime
            if isinstance(cached_result.get("timestamp"), str):
                cached_result["timestamp"] = datetime.fromisoformat(cached_result["timestamp"])

            result = PatternResult(**cached_result)

            # Always regenerate fresh chart URLs with latest indicators
            try:
                charting = get_charting_service()
                chart_url = await charting.generate_chart(
                    ticker=ticker,
                    timeframe=request.interval,
                    entry=result.entry,
                    stop=result.stop,
                    target=result.target,
                    support=result.support_start,
                    resistance=None,
                    pattern_name=f"{result.pattern} Entry"
                )
                if chart_url:
                    result.chart_url = chart_url
                    logger.info(f"📊 Chart regenerated for {ticker}: {chart_url[:60]}...")
            except Exception as e:
                logger.warning(f"⚠️ Chart regeneration failed for {ticker}: {e}")

            processing_time = time.time() - start_time

            logger.info(f"⚡ Cache hit for {ticker}: {result.pattern} ({result.score}/10) in {processing_time:.2f}s")

            return PatternResponse(
                success=True,
                data=result,
                error=None,
                cached=True,
                api_used="cache",
                processing_time=round(processing_time, 2)
            )

        # 2. Cache miss - fetch from API (uses smart multi-source fallback)
        logger.info(f"📡 Cache miss for {ticker}, fetching from API")

        # Get price data (tries TwelveData → Finnhub → AlphaVantage → Yahoo)
        price_data = await market_data_service.get_time_series(
            ticker=ticker,
            interval=request.interval,
            outputsize=500
        )

        if not price_data:
            raise HTTPException(
                status_code=404,
                detail=f"No price data available for {ticker}"
            )

        api_used = price_data.get("source", "unknown")

        # Get SPY data for RS calculation
        spy_data = await market_data_service.get_time_series(
            ticker="SPY",
            interval="1day",
            outputsize=500
        )

        # Run pattern detection - use advanced engine by default
        if request.use_advanced_patterns:
            logger.info(f"Using Legend AI Pattern Engine for {ticker}")
            advanced_detector = get_pattern_detector()
            detected_patterns = advanced_detector.detect_all_patterns(price_data, ticker)
            
            if detected_patterns:
                # Use the highest confidence pattern
                best_pattern = max(detected_patterns, key=lambda p: p.get('confidence', 0))
                
                # Convert to PatternResult format
                from datetime import datetime
                result = PatternResult(
                    ticker=ticker,
                    pattern=best_pattern['pattern'],
                    score=best_pattern['score'],
                    entry=best_pattern['entry'],
                    stop=best_pattern['stop'],
                    target=best_pattern['target'],
                    risk_reward=best_pattern['risk_reward'],
                    criteria_met=[
                        f"✓ {best_pattern['pattern']} confirmed" if best_pattern.get('confirmed') else f"⚠ {best_pattern['pattern']} pending confirmation",
                        f"✓ Confidence: {best_pattern['confidence']*100:.1f}%",
                        f"✓ Risk/Reward: {best_pattern['risk_reward']:.2f}:1"
                    ],
                    analysis=f"Legend AI detected {best_pattern['pattern']} with {best_pattern['confidence']*100:.0f}% confidence. Pattern width: {best_pattern.get('width', 0)} bars.",
                    timestamp=datetime.now(),
                    current_price=best_pattern.get('current_price'),
                    support_start=best_pattern.get('metadata', {}).get('bottom1') or best_pattern.get('metadata', {}).get('bottom'),
                    support_end=best_pattern.get('metadata', {}).get('bottom2') or best_pattern.get('metadata', {}).get('bottom'),
                )
                
                logger.info(f"✅ Legend AI detected {len(detected_patterns)} patterns, using best: {result.pattern} (score: {result.score})")
            else:
                logger.info(f"No advanced patterns found for {ticker}, falling back to basic detector")
                # Fallback to original detector
                detector = PatternDetector()
                result = await detector.analyze_ticker(
                    ticker=ticker,
                    price_data=price_data,
                    spy_data=spy_data
                )
        else:
            # Use original Minervini-style detector
            logger.info(f"Using basic pattern detection for {ticker}")
            detector = PatternDetector()
            result = await detector.analyze_ticker(
                ticker=ticker,
                price_data=price_data,
                spy_data=spy_data
            )

        if not result:
            raise HTTPException(
                status_code=500,
                detail=f"Pattern analysis failed for {ticker}"
            )

        # Generate chart with indicators and drawings
        try:
            charting = get_charting_service()
            chart_url = await charting.generate_chart(
                ticker=ticker,
                timeframe=request.interval,
                entry=result.entry,
                stop=result.stop,
                target=result.target,
                support=result.support_start,
                resistance=None,
                pattern_name=f"{result.pattern} Entry"
            )
            if chart_url:
                result.chart_url = chart_url
                logger.info(f"📊 Chart generated for {ticker}: {chart_url[:60]}...")
            else:
                logger.warning(f"⚠️ Chart service returned None for {ticker}")
                result.chart_url = None
        except Exception as e:
            logger.warning(f"⚠️ Chart generation failed for {ticker}: {e}")
            result.chart_url = None

        # Cache the result (1 hour TTL)
        await cache.set_pattern(ticker, request.interval, result.to_dict())

        processing_time = time.time() - start_time

        logger.info(f"✅ Pattern detected for {ticker}: {result.pattern} ({result.score}/10) in {processing_time:.2f}s")

        return PatternResponse(
            success=True,
            data=result,
            error=None,
            cached=False,
            api_used=api_used,
            processing_time=round(processing_time, 2)
        )

    except HTTPException:
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"💥 Pattern detection failed for {request.ticker}: {e}")

        return PatternResponse(
            success=False,
            data=None,
            error=str(e),
            cached=False,
            api_used="error",
            processing_time=round(processing_time, 2)
        )


@router.get("/health")
async def patterns_health():
    """Health check for patterns service"""
    cache_status = "unknown"
    market_data_status = "unknown"

    try:
        cache = get_cache_service()
        cache_health = await cache.health_check()
        cache_status = cache_health["status"]
    except Exception as e:
        logger.warning(f"Cache health check failed: {e}")
        cache_status = "disconnected"

    try:
        # Test market data service with a quick request
        test_data = await market_data_service.get_time_series("AAPL", "1day", 1)
        market_data_status = "connected" if test_data else "error"
    except Exception as e:
        logger.warning(f"Market data health check failed: {e}")
        market_data_status = "disconnected"

    return {
        "status": "healthy",
        "market_data_service": market_data_status,
        "redis_cache": cache_status,
        "pattern_detector": "ready"
    }


@router.get("/cache/stats")
async def cache_stats():
    """Get cache statistics"""
    try:
        cache = get_cache_service()
        stats = await cache.get_cache_stats()
        return {
            "status": "success",
            "cache_stats": stats
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def _parse_as_of(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except Exception:
            pass
    return datetime.utcnow()


def _catalog_description(name: str) -> str:
    return {
        "Cup & Handle": "Rounded base with shallow handle forming below highs.",
        "Double Bottom": "Two swing lows forming a W near support.",
        "Triangle Ascending": "Rising higher lows against horizontal resistance.",
        "Triangle Descending": "Lower highs pressing against support.",
        "Triangle Symmetrical": "Converging highs/lows signaling volatility compression.",
        "VCP (Volatility Contraction)": "Mark Minervini style contraction leading to breakout.",
    }.get(name, "Pattern generated by the Legend AI detection engine.")


@router.post("/scan", response_model=ScanTickersResponse)
async def scan_tickers(
    request: ScanTickersRequest,
) -> ScanTickersResponse:
    """Scan multiple tickers for patterns using the pattern engine + scoring."""
    if not request.tickers:
        raise HTTPException(status_code=400, detail="tickers list is required")

    try:
        payload = await pattern_scanner_service.scan_with_pattern_engine(
            tickers=request.tickers,
            interval=request.interval,
            apply_filters=request.apply_filters,
            min_score=request.min_score,
            filter_config=request.filter_config,
        )
    except Exception as exc:
        logger.exception("scan_tickers_failed: %s", exc)
        raise HTTPException(status_code=500, detail="scan_failed") from exc

    results = payload.get("results", [])
    return ScanTickersResponse(
        success=True,
        as_of=_parse_as_of(payload.get("as_of")),
        results=results,
        errors=payload.get("errors", {}),
        count=len(results),
        meta=payload.get("meta"),
    )


@router.post("/scan-universe", response_model=ScanTickersResponse)
async def scan_universe_patterns(
    min_score: float = Query(4.0, ge=0.0, le=10.0, description="Minimum pattern score"),
    limit: int = Query(20, ge=1, le=50, description="Max results to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination (batch processing)"),
) -> ScanTickersResponse:
    """
    Scan full universe (518+ cached symbols) for top patterns with batch processing.

    - Excludes Outside Day pattern
    - Prioritizes VCP, Cup & Handle, Flags, Pennants, Triangles, Wedges
    - Returns top 10-20 results ranked by score
    - Includes Chart-IMG URLs for inline display
    - Uses BATCH_SIZE=10 for memory-efficient processing
    """

    # Memory optimization: Process in batches to avoid OOM
    BATCH_SIZE = 10

    # Check cache first
    cache_key = f"universe_scan:v3:min{min_score}:limit{limit}:offset{offset}"
    try:
        cached = await get_cache_service().get(cache_key)
        if cached:
            logger.info("Returning cached universe scan results")
            return ScanTickersResponse(**cached)
    except Exception as e:
        logger.debug(f"Cache retrieval failed: {e}")

    # Get universe symbols
    try:
        await universe_store.seed()
        universe = await universe_store.get_all()
        all_tickers = list(universe.keys())
        total_symbols = len(all_tickers)
        logger.info(f"Universe loaded: {total_symbols} symbols")
    except Exception as e:
        logger.error(f"Failed to load universe: {e}")
        # Fallback to small set
        all_tickers = ["AAPL", "NVDA", "TSLA", "GOOGL", "META", "MSFT", "AMZN"]
        total_symbols = len(all_tickers)

    # Apply offset for pagination (if scanning in chunks)
    if offset > 0:
        all_tickers = all_tickers[offset:]
        logger.info(f"Starting scan from offset {offset}, {len(all_tickers)} symbols remaining")

    # Batch processing for memory efficiency
    all_results = []
    total_batches = (len(all_tickers) + BATCH_SIZE - 1) // BATCH_SIZE

    for batch_num in range(total_batches):
        start_idx = batch_num * BATCH_SIZE
        end_idx = min(start_idx + BATCH_SIZE, len(all_tickers))
        batch_tickers = all_tickers[start_idx:end_idx]

        logger.info(f"Processing batch {batch_num + 1}/{total_batches}: {len(batch_tickers)} symbols")

        try:
            batch_payload = await pattern_scanner_service.scan_with_pattern_engine(
                tickers=batch_tickers,
                interval="1day",
                apply_filters=True,
                min_score=min_score,
                filter_config={"exclude_patterns": ["Outside Day"]},
            )
            batch_results = batch_payload.get("results", [])
            all_results.extend(batch_results)
            logger.info(f"Batch {batch_num + 1} found {len(batch_results)} patterns")
        except Exception as exc:
            logger.warning(f"Batch {batch_num + 1} scan failed: {exc}")
            continue

    logger.info(f"Total patterns found: {len(all_results)} from {len(all_tickers)} symbols")

    # Get top results and generate charts
    results = all_results
    results = sorted(results, key=lambda x: x.get("score", 0), reverse=True)[:limit]

    # Generate chart URLs for top results (rate-limited to avoid hitting daily quota)
    for result in results:
        ticker = result.get("ticker")
        if not result.get("chart_url"):
            try:
                chart_url = await charting_service.generate_chart(
                    ticker=ticker,
                    interval="1day",
                    entry=result.get("entry"),
                    stop=result.get("stop"),
                    target=result.get("target"),
                )
                result["chart_url"] = chart_url
            except Exception as e:
                logger.warning(f"Chart generation failed for {ticker}: {e}")
                result["chart_url"] = None

    # Sanitize results: convert non-JSON-serializable objects to JSON-safe types
    def sanitize_value(value):
        """Recursively convert non-JSON-serializable types to JSON-safe types."""
        if isinstance(value, datetime):
            return value.isoformat()
        elif hasattr(value, 'item'):  # numpy int/float types
            return value.item()
        elif hasattr(value, 'tolist'):  # numpy arrays
            return value.tolist()
        elif isinstance(value, dict):
            return {k: sanitize_value(v) for k, v in value.items()}
        elif isinstance(value, (list, tuple)):
            return [sanitize_value(item) for item in value]
        return value

    for result in results:
        for key, value in list(result.items()):
            result[key] = sanitize_value(value)

    response_data = ScanTickersResponse(
        success=True,
        as_of=datetime.now(timezone.utc),
        results=results,
        errors={},
        count=len(results),
        meta={
            "universe_size": total_symbols,
            "scanned": len(all_tickers),
            "batches": total_batches,
            "offset": offset,
            "cached": False,
        }
    )

    # Cache for 6 hours (longer cache for full universe scans)
    try:
        await get_cache_service().set(cache_key, response_data.model_dump(mode='json'), ttl=21600)
    except Exception as e:
        logger.debug(f"Cache storage failed: {e}")

    return response_data


@router.post("/scan-quick", response_model=ScanTickersResponse)
async def scan_quick_patterns(
    min_score: float = Query(4.0, ge=0.0, le=10.0, description="Minimum pattern score"),
    limit: int = Query(20, ge=1, le=50, description="Max results to return"),
) -> ScanTickersResponse:
    """
    Quick scan of top 15 core mega-cap stocks (15-25 second response time).

    - Scans most liquid, highest volume stocks (AAPL, MSFT, NVDA, etc.)
    - Excludes Outside Day pattern
    - Prioritizes VCP, Cup & Handle, Flags, Pennants, Triangles, Wedges
    - Returns top results ranked by score
    - Includes Chart-IMG URLs for inline display
    - Optimized for fast response time (~15-25 seconds)
    - Uses 1-hour cache for instant subsequent requests
    """

    # Check cache first (1-hour cache for quick scans)
    cache_key = f"quick_scan:v3:min{min_score}:limit{limit}"  # v3 = 15 core mega-caps
    try:
        cached = await get_cache_service().get(cache_key)
        if cached:
            logger.info("Returning cached quick scan results")
            return ScanTickersResponse(**cached)
    except Exception as e:
        logger.debug(f"Cache retrieval failed: {e}")

    # Get universe and filter to top 100 most liquid stocks
    try:
        await universe_store.seed()
        universe = await universe_store.get_all()

        # Use only top 15 core mega-cap stocks for reliable <25 second scan
        # These are the most liquid, highest volume stocks
        quick_tickers = [
            "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN",  # Tech giants
            "META", "TSLA", "JPM", "V", "MA",          # Finance leaders
            "WMT", "JNJ", "UNH", "XOM", "PG"           # Blue chips
        ]
        # 15 stocks × 1.5s avg = 22.5 seconds (within 30s timeout)

        logger.info(f"Quick scan: {len(quick_tickers)} high-liquidity symbols")
    except Exception as e:
        logger.error(f"Failed to load universe for quick scan: {e}")
        # Fallback to 15 core mega-caps
        quick_tickers = [
            "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN",
            "META", "TSLA", "JPM", "V", "MA",
            "WMT", "JNJ", "UNH", "XOM", "PG"
        ]

    # Scan with pattern engine (no batching needed for 15 symbols)
    try:
        payload = await pattern_scanner_service.scan_with_pattern_engine(
            tickers=quick_tickers,
            interval="1day",
            apply_filters=True,
            min_score=min_score,
            filter_config={"exclude_patterns": ["Outside Day"]},
        )
    except Exception as exc:
        logger.exception("Quick scan failed: %s", exc)
        raise HTTPException(status_code=500, detail="Quick scan failed") from exc

    # Get top results
    results = payload.get("results", [])
    results = sorted(results, key=lambda x: x.get("score", 0), reverse=True)[:limit]

    # Generate chart URLs for top results
    for result in results:
        ticker = result.get("ticker")
        if not result.get("chart_url"):
            try:
                chart_url = await charting_service.generate_chart(
                    ticker=ticker,
                    interval="1day",
                    entry=result.get("entry"),
                    stop=result.get("stop"),
                    target=result.get("target"),
                )
                result["chart_url"] = chart_url
            except Exception as e:
                logger.warning(f"Chart generation failed for {ticker}: {e}")
                result["chart_url"] = None

    # Sanitize results: convert non-JSON-serializable objects to JSON-safe types
    def sanitize_value(value):
        """Recursively convert non-JSON-serializable types to JSON-safe types."""
        if isinstance(value, datetime):
            return value.isoformat()
        elif hasattr(value, 'item'):  # numpy int/float types
            return value.item()
        elif hasattr(value, 'tolist'):  # numpy arrays
            return value.tolist()
        elif isinstance(value, dict):
            return {k: sanitize_value(v) for k, v in value.items()}
        elif isinstance(value, (list, tuple)):
            return [sanitize_value(item) for item in value]
        return value

    for result in results:
        for key, value in list(result.items()):
            result[key] = sanitize_value(value)

    response_data = ScanTickersResponse(
        success=True,
        as_of=datetime.now(timezone.utc),
        results=results,
        errors={},
        count=len(results),
        meta={
            "universe_size": len(quick_tickers),
            "scan_type": "quick",
            "cached": False,
        }
    )

    # Cache for 1 hour (quicker refresh for fast scans)
    try:
        await get_cache_service().set(cache_key, response_data.model_dump(mode='json'), ttl=3600)
    except Exception as e:
        logger.debug(f"Cache storage failed: {e}")

    return response_data


@router.post("/scan-quick/warmup")
async def warmup_quick_scan():
    """
    Pre-populate cache for instant first load.

    Runs a quick scan and caches the results so the first user
    gets instant results instead of waiting 20-25 seconds.
    """
    try:
        result = await scan_quick_patterns()
        return {
            "success": True,
            "cached": True,
            "count": result.count,
            "message": "Cache warmed up successfully"
        }
    except Exception as e:
        logger.error(f"Cache warmup failed: {e}")
        return {
            "success": False,
            "cached": False,
            "error": str(e)
        }


@router.post("/filter", response_model=FilterResponse)
async def filter_patterns(
    request: FilterRequest,
) -> FilterResponse:
    """Apply filters to pattern results."""
    filtered = _pattern_filter.apply_filters(request.patterns, request.filter_config)
    return FilterResponse(results=filtered, count=len(filtered))


@router.post("/score", response_model=ScoreResponse)
async def score_pattern(
    request: ScoreRequest,
) -> ScoreResponse:
    """Return a score breakdown for a pattern."""
    components, total = _pattern_scorer.score_pattern(request.pattern)
    return ScoreResponse(score=total, components=components.to_dict())


@router.post("/export", response_model=ExportResponse)
async def export_patterns(
    request: ExportRequest,
) -> ExportResponse:
    """Export pattern results to disk or clipboard."""
    if not request.patterns:
        raise HTTPException(status_code=400, detail="No patterns provided for export")

    fmt = request.format.lower()
    output_dir = Path(request.output_dir or "exports")
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    def _resolve_filename(ext: str) -> Path:
        if request.filename:
            return output_dir / request.filename
        return output_dir / f"patterns_{timestamp}.{ext}"

    if fmt == "csv":
        location = _pattern_exporter.to_csv(request.patterns, str(_resolve_filename("csv")))
        return ExportResponse(success=True, location=location)
    if fmt == "json":
        location = _pattern_exporter.to_json(request.patterns, str(_resolve_filename("json")))
        return ExportResponse(success=True, location=location)
    if fmt in {"excel", "xlsx"}:
        location = _pattern_exporter.to_excel(request.patterns, str(_resolve_filename("xlsx")))
        return ExportResponse(success=True, location=location)
    if fmt == "clipboard":
        text = _pattern_exporter.to_clipboard(request.patterns)
        return ExportResponse(success=True, location=text, copied=True)

    raise HTTPException(status_code=400, detail=f"Unsupported export format: {request.format}")


@router.get("/catalog")
async def get_pattern_catalog() -> Dict[str, Any]:
    """List all available patterns with short descriptions."""
    catalog = []
    for pattern_type in PatternType:
        name = pattern_type.value
        catalog.append({"name": name, "description": _catalog_description(name)})

    # Frequently requested swing pattern
    catalog.append(
        {
            "name": "MMU VCP",
            "description": "Minervini style volatility contraction pivot (most requested swing setup).",
        }
    )

    return {"count": len(catalog), "patterns": catalog}
