from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any, Union
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
    data: Optional[Dict[str, Any]] = Field(None, description="Pattern analysis result")
    error: Optional[str] = Field(None, description="Error message if request failed")
    cached: bool = Field(False, description="Whether result was served from cache")
    api_used: str = Field("unknown", description="Data source used (cache, twelvedata, finnhub, alphavantage, yahoo)")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")


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


@router.post("/detect", response_model=PatternResponse)
async def detect_pattern(request: PatternRequest):
    """Detect Chart Pattern for Any Stock"""
    import time
    start_time = time.time()
    cache = get_cache_service()

    try:
        ticker = request.ticker.upper().strip()

        # Validate ticker format
        if not ticker or not ticker.replace(".", "").replace("-", "").isalnum():
            raise HTTPException(status_code=400, detail="Invalid ticker symbol format")

        logger.info(f"🔍 Analyzing pattern for {ticker}")

        # 1. Try cache first
        cached_result = await cache.get_pattern(ticker=ticker, interval=request.interval)
        if cached_result:
            # Convert cached dict back to PatternResult
            if isinstance(cached_result.get("timestamp"), str):
                cached_result["timestamp"] = datetime.fromisoformat(cached_result["timestamp"])

            # Just return the cached dict directly (it should be clean)
            processing_time = time.time() - start_time
            return PatternResponse(
                success=True,
                data=cached_result,
                error=None,
                cached=True,
                api_used="cache",
                processing_time=round(processing_time, 2)
            )

        # 2. Cache miss - fetch from API
        price_data = await market_data_service.get_time_series(
            ticker=ticker,
            interval=request.interval,
            outputsize=500
        )

        if not price_data:
            raise HTTPException(status_code=404, detail=f"No price data available for {ticker}")

        api_used = price_data.get("source", "unknown")

        # Get SPY data for RS
        spy_data = await market_data_service.get_time_series("SPY", "1day", 500)

        # Run pattern detection
        result = None
        if request.use_advanced_patterns:
            advanced_detector = get_pattern_detector()
            detected_patterns = advanced_detector.detect_all_patterns(price_data, ticker)
            
            if detected_patterns:
                best_pattern = max(detected_patterns, key=lambda p: p.get('confidence', 0))
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
                        f"✓ Confidence: {best_pattern['confidence']*100:.1f}%"
                    ],
                    analysis=f"Legend AI detected {best_pattern['pattern']} with {best_pattern['confidence']*100:.0f}% confidence.",
                    timestamp=datetime.now(),
                    current_price=best_pattern.get('current_price'),
                    support_start=best_pattern.get('metadata', {}).get('bottom'),
                    support_end=best_pattern.get('metadata', {}).get('bottom')
                )
            else:
                detector = PatternDetector()
                result = await detector.analyze_ticker(ticker=ticker, price_data=price_data, spy_data=spy_data)
        else:
            detector = PatternDetector()
            result = await detector.analyze_ticker(ticker=ticker, price_data=price_data, spy_data=spy_data)

        if not result:
            raise HTTPException(status_code=500, detail=f"Pattern analysis failed for {ticker}")

        # Generate chart
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
        except Exception:
            pass

        # Convert to dict (sanitizes numpy types)
        result_dict = result.to_dict()

        # Cache result
        await cache.set_pattern(ticker, request.interval, result_dict)

        return PatternResponse(
            success=True,
            data=result_dict,
            error=None,
            cached=False,
            api_used=api_used,
            processing_time=round(time.time() - start_time, 2)
        )

    except Exception as e:
        return PatternResponse(
            success=False,
            data=None,
            error=str(e),
            cached=False,
            api_used="error",
            processing_time=round(time.time() - start_time, 2)
        )


def _catalog_description(name: str) -> str:
    """Helper to return descriptions for patterns."""
    return {
        "Cup & Handle": "Bullish continuation pattern. A U-shaped cup followed by a short handle.",
        "VCP": "Volatility Contraction Pattern. A series of tighter and tighter price contractions.",
        "Double Bottom": "Reversal pattern with two distinct lows at a similar price level.",
        "Ascending Triangle": "Bullish continuation. Flat top resistance with rising support trendline.",
        "Descending Triangle": "Bearish continuation. Flat bottom support with falling resistance trendline.",
        "Bull Flag": "Bullish continuation. A short channel sloping against the trend after a sharp rise.",
        "Bear Flag": "Bearish continuation. A short channel sloping against the trend after a sharp drop.",
        "Head & Shoulders": "Bearish reversal. Three peaks with the middle one being the highest.",
        "Inverse Head & Shoulders": "Bullish reversal. Three troughs with the middle one being the lowest.",
    }.get(name, "Algorithmic pattern detection.")


@router.get("/catalog")
async def get_pattern_catalog() -> Dict[str, Any]:
    """
    List all available patterns with metadata grouped by category.
    Used for populating the frontend scanner UI.
    """

    # Define Categories
    categories = {
        "Classical": ["Head & Shoulders", "Head & Shoulders Inverse", "Double Bottom", "Double Top", "Triple Bottom", "Triple Top", "Triangle Ascending", "Triangle Descending", "Triangle Symmetrical"],
        "Trend Continuation": ["Bull Flag", "Bear Flag", "Pennant", "Channel Up", "Channel Down"],
        "Trend Reversal": ["Wedge Rising", "Wedge Falling", "Rounding Bottom", "Rounding Top"],
        "SEPA / Minervini": ["VCP (Volatility Contraction)", "MMU VCP", "Volatility Dry-Up", "Cheat Entry"],
        "Specialist": ["Cup & Handle", "Broadening Top", "Broadening Bottom", "Adam & Eve Double Bottom"],
        "Candlestick": ["Hammer", "Shooting Star", "Doji", "Engulfing Bullish", "Engulfing Bearish"]
    }

    # Helper to find type
    def get_type(name):
        lower = name.lower()
        if "bull" in lower or "ascending" in lower or "cup" in lower or "bottom" in lower:
            return "Bullish"
        if "bear" in lower or "descending" in lower or "top" in lower:
            return "Bearish"
        return "Neutral"

    catalog = {}

    # 1. Populate from Enum
    for pattern_type in PatternType:
        name = pattern_type.value
        found_cat = "Other"
        for cat, patterns in categories.items():
            if name in patterns or any(p in name for p in patterns):
                found_cat = cat
                break

        if found_cat not in catalog:
            catalog[found_cat] = []

        catalog[found_cat].append({
            "name": name,
            "type": get_type(name),
            "description": _catalog_description(name),
            "enabled": True
        })

    # 2. Add extra patterns not in Enum yet (for future proofing UI)
    extras = [
        ("SEPA / Minervini", "MMU VCP", "Bullish"),
        ("Candlestick", "Hammer", "Bullish"),
        ("Candlestick", "Shooting Star", "Bearish"),
        ("Trend Continuation", "Bull Flag", "Bullish"),
    ]

    for cat, name, ptype in extras:
        if cat not in catalog:
            catalog[cat] = []
        # Check if already exists
        if not any(p['name'] == name for p in catalog[cat]):
             catalog[cat].append({
                "name": name,
                "type": ptype,
                "description": _catalog_description(name),
                "enabled": True
            })

    # Convert to list for easier frontend consumption
    result_list = []
    for cat, patterns in catalog.items():
        result_list.append({
            "category": cat,
            "patterns": patterns
        })

    return {
        "count": sum(len(c["patterns"]) for c in result_list),
        "categories": result_list
    }

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
