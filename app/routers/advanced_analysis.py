"""
Advanced Technical Analysis Router
- 50+ Chart Patterns
- Automated Trendlines
- Fibonacci Levels
- Support/Resistance Detection
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import logging

from app.data.market_data import MarketDataService
from app.detectors.advanced.patterns import AdvancedPatternDetector, PatternType
from app.technicals.trendlines import (
    AutoTrendlineDetector,
    detect_horizontal_support_resistance
)
from app.technicals.fibonacci import FibonacciCalculator
from app.core.rate_limiter import limiter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/advanced", tags=["Advanced Analysis"])

# Initialize services
market_data = MarketDataService()
pattern_detector = AdvancedPatternDetector(min_confidence=60.0)
trendline_detector = AutoTrendlineDetector()
fib_calculator = FibonacciCalculator()


class PatternDetectionRequest(BaseModel):
    """Advanced pattern detection request"""
    symbol: str = Field(..., description="Stock ticker symbol")
    timeframe: str = Field("daily", description="Timeframe (daily, weekly)")
    min_confidence: float = Field(60.0, ge=0, le=100, description="Minimum pattern confidence")


class TrendlineRequest(BaseModel):
    """Trendline detection request"""
    symbol: str = Field(..., description="Stock ticker symbol")
    lookback_period: Optional[int] = Field(100, description="How far back to analyze")
    min_touches: int = Field(3, description="Minimum touches for valid trendline")


class FibonacciRequest(BaseModel):
    """Fibonacci levels request"""
    symbol: str = Field(..., description="Stock ticker symbol")
    lookback: int = Field(100, description="Lookback period for swing detection")


class ManualFibonacciRequest(BaseModel):
    """Manual Fibonacci calculation"""
    high: float = Field(..., description="Swing high price")
    low: float = Field(..., description="Swing low price")
    direction: str = Field("uptrend", description="'uptrend' or 'downtrend'")
    current_price: Optional[float] = Field(None, description="Current price")


@router.post("/patterns/detect")
@limiter.limit("30/minute")
async def detect_advanced_patterns(request: PatternDetectionRequest):
    """
    Detect 50+ advanced chart patterns using ML-enhanced algorithms

    **Patterns detected:**
    - Continuation: Flags, Pennants, Triangles, Wedges, Rectangles
    - Reversal: Head & Shoulders, Double/Triple Tops/Bottoms, Cup & Handle
    - Candlestick: Hammers, Engulfing, Stars, Soldiers/Crows
    - Gaps: Breakaway, Runaway, Exhaustion, Island Reversals
    - Advanced: Harmonic patterns (Gartley, Bat, Butterfly)

    **Returns:**
    - Pattern type and confidence score
    - Entry/exit levels
    - Price targets and stop losses
    - Win probability based on historical data
    - Detailed descriptions

    **Example:**
    ```json
    {
        "symbol": "AAPL",
        "timeframe": "daily",
        "min_confidence": 70.0
    }
    ```
    """
    try:
        # Fetch price data
        df = await market_data.get_price_data(
            symbol=request.symbol,
            period="6mo",
            interval="1d"
        )

        if df is None or df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No data available for {request.symbol}"
            )

        # Detect patterns
        detector = AdvancedPatternDetector(min_confidence=request.min_confidence)
        patterns = detector.detect_all_patterns(df, timeframe=request.timeframe)

        # Convert to dict format
        patterns_dict = [p.to_dict() for p in patterns]

        return {
            "symbol": request.symbol,
            "timeframe": request.timeframe,
            "patterns_detected": len(patterns_dict),
            "patterns": patterns_dict,
            "summary": {
                "total_patterns": len(patterns_dict),
                "bullish_patterns": len([
                    p for p in patterns_dict
                    if p.get('expected_move', 0) > 0
                ]),
                "bearish_patterns": len([
                    p for p in patterns_dict
                    if p.get('expected_move', 0) < 0
                ]),
                "highest_confidence": max([p['confidence'] for p in patterns_dict]) if patterns_dict else 0
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Pattern detection error for {request.symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/trendlines/detect")
@limiter.limit("30/minute")
async def detect_trendlines(request: TrendlineRequest):
    """
    Automatically detect support and resistance trendlines

    **Features:**
    - ML-based trendline identification
    - Support and resistance lines
    - Price channels
    - Strength scoring based on touches
    - Break detection

    **Returns:**
    - Support trendlines (drawn under price)
    - Resistance trendlines (drawn above price)
    - Trendline equation (slope + intercept)
    - Strength score and number of touches

    **Example:**
    ```json
    {
        "symbol": "TSLA",
        "lookback_period": 100,
        "min_touches": 3
    }
    ```
    """
    try:
        # Fetch price data
        df = await market_data.get_price_data(
            symbol=request.symbol,
            period="6mo",
            interval="1d"
        )

        if df is None or df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No data available for {request.symbol}"
            )

        # Detect trendlines
        detector = AutoTrendlineDetector(min_touches=request.min_touches)
        trendlines = detector.detect_all_trendlines(df, request.lookback_period)

        # Detect channels
        channels = detector.detect_channels(df, request.lookback_period)

        # Detect horizontal S/R
        horizontal = detect_horizontal_support_resistance(
            df,
            lookback=request.lookback_period,
            min_touches=request.min_touches
        )

        return {
            "symbol": request.symbol,
            "support_trendlines": [tl.to_dict() for tl in trendlines['support']],
            "resistance_trendlines": [tl.to_dict() for tl in trendlines['resistance']],
            "channels": [ch.to_dict() for ch in channels],
            "horizontal_levels": horizontal,
            "summary": {
                "total_support_lines": len(trendlines['support']),
                "total_resistance_lines": len(trendlines['resistance']),
                "total_channels": len(channels),
                "horizontal_support": len(horizontal['support']),
                "horizontal_resistance": len(horizontal['resistance'])
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Trendline detection error for {request.symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fibonacci/auto")
@limiter.limit("30/minute")
async def calculate_fibonacci_auto(request: FibonacciRequest):
    """
    Automatically calculate Fibonacci retracement and extension levels

    **Features:**
    - Automatic swing high/low detection
    - Fibonacci retracement levels (23.6%, 38.2%, 50%, 61.8%, 78.6%)
    - Fibonacci extension levels (127.2%, 141.4%, 161.8%, 200%, 261.8%)
    - Identifies nearest support/resistance levels

    **Returns:**
    - Detected swing points
    - All Fibonacci levels
    - Nearest support/resistance from current price
    - Trend direction

    **Example:**
    ```json
    {
        "symbol": "NVDA",
        "lookback": 100
    }
    ```
    """
    try:
        # Fetch price data
        df = await market_data.get_price_data(
            symbol=request.symbol,
            period="6mo",
            interval="1d"
        )

        if df is None or df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No data available for {request.symbol}"
            )

        # Calculate Fibonacci levels
        fib_levels = fib_calculator.calculate_auto_fibonacci(df, request.lookback)

        return {
            "symbol": request.symbol,
            "fibonacci_levels": [fib.to_dict() for fib in fib_levels],
            "count": len(fib_levels)
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fibonacci calculation error for {request.symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fibonacci/manual")
async def calculate_fibonacci_manual(request: ManualFibonacciRequest):
    """
    Calculate Fibonacci levels for manually specified swing points

    **Use case:**
    When you've identified a specific swing high and low on your chart

    **Example:**
    ```json
    {
        "high": 150.50,
        "low": 130.00,
        "direction": "uptrend",
        "current_price": 145.00
    }
    ```
    """
    try:
        current_price = request.current_price or request.high

        fib = fib_calculator.calculate_manual_fibonacci(
            high=request.high,
            low=request.low,
            direction=request.direction,
            current_price=current_price
        )

        return {
            "fibonacci_levels": fib.to_dict()
        }

    except Exception as e:
        logger.error(f"Manual Fibonacci calculation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patterns/list")
async def list_all_patterns():
    """
    Get list of all 50+ supported chart patterns

    **Pattern Categories:**
    - Continuation Patterns
    - Reversal Patterns
    - Gap Patterns
    - Candlestick Patterns
    - Harmonic Patterns
    """
    patterns_by_category = {
        "continuation": [
            "Bull Flag", "Bear Flag", "Bull Pennant", "Bear Pennant",
            "Ascending Triangle", "Descending Triangle", "Symmetrical Triangle",
            "Rising Wedge", "Falling Wedge", "Rectangle (Bullish)", "Rectangle (Bearish)"
        ],
        "reversal": [
            "Head and Shoulders", "Inverse Head and Shoulders",
            "Double Top", "Double Bottom", "Triple Top", "Triple Bottom",
            "Rounding Top", "Rounding Bottom", "Cup and Handle", "Inverse Cup and Handle",
            "Diamond Top", "Diamond Bottom", "Broadening Top", "Broadening Bottom"
        ],
        "gaps": [
            "Breakaway Gap (Bull)", "Breakaway Gap (Bear)",
            "Runaway Gap (Bull)", "Runaway Gap (Bear)",
            "Exhaustion Gap (Bull)", "Exhaustion Gap (Bear)",
            "Island Reversal (Bull)", "Island Reversal (Bear)"
        ],
        "candlestick": [
            "Hammer", "Inverted Hammer", "Hanging Man", "Shooting Star",
            "Bullish Engulfing", "Bearish Engulfing",
            "Morning Star", "Evening Star",
            "Piercing Line", "Dark Cloud Cover",
            "Three White Soldiers", "Three Black Crows",
            "Doji", "Dragonfly Doji", "Gravestone Doji",
            "Bullish Harami", "Bearish Harami"
        ],
        "harmonic": [
            "Gartley Pattern", "Bat Pattern", "Butterfly Pattern",
            "Crab Pattern", "Shark Pattern", "Cypher Pattern",
            "Elliott Wave (5 waves)", "Elliott Wave (ABC correction)"
        ]
    }

    total = sum(len(patterns) for patterns in patterns_by_category.values())

    return {
        "total_patterns": total,
        "patterns_by_category": patterns_by_category,
        "pattern_types": [pt.value for pt in PatternType]
    }


@router.post("/comprehensive-analysis")
@limiter.limit("15/minute")
async def comprehensive_technical_analysis(symbol: str = Query(..., description="Stock ticker")):
    """
    **Ultimate Technical Analysis** - Everything at once!

    Combines:
    - Advanced pattern detection (50+ patterns)
    - Automated trendlines
    - Fibonacci levels
    - Support/resistance
    - Channels

    This is the most comprehensive analysis endpoint.

    **Example:** `/api/advanced/comprehensive-analysis?symbol=AAPL`
    """
    try:
        # Fetch price data
        df = await market_data.get_price_data(
            symbol=symbol,
            period="6mo",
            interval="1d"
        )

        if df is None or df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No data available for {symbol}"
            )

        # Run all analyses in parallel conceptually (sequential for now)

        # 1. Patterns
        patterns = pattern_detector.detect_all_patterns(df)

        # 2. Trendlines
        trendlines = trendline_detector.detect_all_trendlines(df, lookback_period=100)
        channels = trendline_detector.detect_channels(df, lookback_period=100)

        # 3. Fibonacci
        fib_levels = fib_calculator.calculate_auto_fibonacci(df, lookback=100)

        # 4. Horizontal S/R
        horizontal = detect_horizontal_support_resistance(df, lookback=100)

        # 5. Current price context
        current_price = df['close'].iloc[-1]

        return {
            "symbol": symbol,
            "current_price": float(current_price),
            "analysis": {
                "patterns": {
                    "detected": [p.to_dict() for p in patterns],
                    "count": len(patterns),
                    "bullish_count": len([p for p in patterns if p.expected_move and p.expected_move > 0]),
                    "bearish_count": len([p for p in patterns if p.expected_move and p.expected_move < 0])
                },
                "trendlines": {
                    "support": [tl.to_dict() for tl in trendlines['support']],
                    "resistance": [tl.to_dict() for tl in trendlines['resistance']],
                    "channels": [ch.to_dict() for ch in channels]
                },
                "fibonacci": [fib.to_dict() for fib in fib_levels],
                "horizontal_levels": horizontal
            },
            "summary": {
                "total_patterns": len(patterns),
                "total_trendlines": len(trendlines['support']) + len(trendlines['resistance']),
                "total_channels": len(channels),
                "fibonacci_swings": len(fib_levels)
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Comprehensive analysis error for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
