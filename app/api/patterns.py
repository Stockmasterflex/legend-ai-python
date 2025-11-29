from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from pathlib import Path
from datetime import datetime
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

logger = logging.getLogger(__name__)

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
                    resistance=None  # Could add support_end or resistance level
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
                resistance=None  # Could add support_end or resistance level
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
