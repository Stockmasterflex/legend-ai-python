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

from app.services.market_data import MarketDataService
from app.detectors.advanced.patterns import AdvancedPatternDetector, PatternType
from app.technicals.trendlines import (
    AutoTrendlineDetector,
    detect_horizontal_support_resistance
)
from app.technicals.fibonacci import FibonacciCalculator
from app.core.market_seasonality import MarketSeasonalityAnalyzer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/advanced", tags=["Advanced Analysis"])

# Initialize services
market_data = MarketDataService()
pattern_detector = AdvancedPatternDetector(min_confidence=60.0)
trendline_detector = AutoTrendlineDetector()
fib_calculator = FibonacciCalculator()
seasonality_analyzer = MarketSeasonalityAnalyzer()


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


class SeasonalityRequest(BaseModel):
    """Market seasonality analysis request"""
    symbol: str = Field(..., description="Stock ticker symbol")
    include_options_data: bool = Field(False, description="Include options expiration analysis")
    include_earnings_data: bool = Field(False, description="Include earnings season analysis")


@router.post("/seasonality/analyze")
async def analyze_market_seasonality(request: SeasonalityRequest):
    """
    **Comprehensive Market Seasonality & Historical Pattern Analysis**

    Analyzes historical patterns and seasonality effects including:

    **1. Seasonal Patterns:**
    - Best/worst months for trading
    - Quarterly performance trends
    - Week of month patterns
    - Day of week performance
    - Current period rankings

    **2. Election Cycle Analysis:**
    - Presidential cycle effects
    - Pre/post election patterns
    - Mid-term election impact
    - Current cycle phase
    - Policy impact assessment

    **3. Options Expiration Effects:**
    - OPEX week detection
    - Triple witching identification
    - Pre/post OPEX drift patterns
    - Historical OPEX volatility
    - Pin risk levels

    **4. Earnings Season Analysis:**
    - Current earnings season
    - Peak earnings week detection
    - Pre/post announcement drift
    - Sector rotation signals
    - Earnings volatility premium

    **5. Market Cycle Detection:**
    - Bull/bear regime classification
    - Accumulation/distribution phases
    - Trend strength measurement
    - Volatility regime
    - Support/resistance levels
    - Regime transition probabilities

    **Returns:**
    Complete seasonality report with:
    - All pattern analyses
    - Composite favorability score (0-100)
    - Key insights and warnings
    - Actionable recommendations

    **Example:**
    ```json
    {
        "symbol": "SPY",
        "include_options_data": true,
        "include_earnings_data": true
    }
    ```
    """
    try:
        # Fetch price data (2+ years for good seasonality analysis)
        df = await market_data.get_price_data(
            symbol=request.symbol,
            period="5y",
            interval="1d"
        )

        if df is None or df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No data available for {request.symbol}"
            )

        # Prepare data for analyzer
        from datetime import datetime

        price_data = {
            "c": df['close'].tolist(),
            "h": df['high'].tolist(),
            "l": df['low'].tolist(),
            "v": df['volume'].tolist()
        }

        dates = [datetime.fromtimestamp(ts.timestamp()) for ts in df.index]

        # Run comprehensive seasonality analysis
        report = await seasonality_analyzer.analyze_complete_seasonality(
            ticker=request.symbol,
            price_data=price_data,
            dates=dates,
            current_date=datetime.now(),
            options_data=None,  # Would fetch from options API if available
            earnings_dates=None  # Would fetch from earnings API if available
        )

        # Format response
        return {
            "ticker": report.ticker,
            "analysis_date": report.analysis_date.isoformat(),
            "composite_score": round(report.composite_score, 2),
            "seasonal_patterns": {
                "best_months": report.seasonal_patterns.best_months,
                "worst_months": report.seasonal_patterns.worst_months,
                "best_quarters": report.seasonal_patterns.best_quarters,
                "worst_quarters": report.seasonal_patterns.worst_quarters,
                "best_days": report.seasonal_patterns.best_days_of_week,
                "worst_days": report.seasonal_patterns.worst_days_of_week,
                "current_rankings": {
                    "month": report.seasonal_patterns.current_month_rank,
                    "quarter": report.seasonal_patterns.current_quarter_rank,
                    "week": report.seasonal_patterns.current_week_rank,
                    "day": report.seasonal_patterns.current_day_rank
                }
            },
            "election_cycle": {
                "current_phase": report.election_cycle.current_phase.value,
                "years_until_election": report.election_cycle.years_until_election,
                "current_phase_performance": {
                    "avg_return": round(report.election_cycle.current_phase_avg_return * 100, 2),
                    "volatility": round(report.election_cycle.current_phase_volatility * 100, 2)
                },
                "pre_election_pattern": report.election_cycle.pre_election_pattern,
                "post_election_pattern": report.election_cycle.post_election_pattern,
                "policy_impact_score": round(report.election_cycle.policy_impact_score, 2)
            },
            "options_expiration": {
                "is_opex_week": report.options_expiration.is_opex_week,
                "days_to_opex": report.options_expiration.days_to_opex,
                "is_triple_witching": report.options_expiration.is_triple_witching,
                "drift_pattern": report.options_expiration.opex_drift_pattern,
                "historical_patterns": {
                    "pre_opex_return": round(report.options_expiration.pre_opex_avg_return * 100, 2),
                    "post_opex_return": round(report.options_expiration.post_opex_avg_return * 100, 2),
                    "opex_volatility": round(report.options_expiration.opex_week_volatility * 100, 2)
                }
            },
            "earnings_season": {
                "current_season": report.earnings_season.current_season,
                "is_peak_week": report.earnings_season.is_peak_earnings_week,
                "days_into_season": report.earnings_season.days_into_season,
                "historical_drift": {
                    "pre_announcement": round(report.earnings_season.pre_announcement_drift * 100, 2),
                    "post_announcement": round(report.earnings_season.post_announcement_drift * 100, 2)
                },
                "volatility_premium": round(report.earnings_season.earnings_volatility_premium * 100, 2),
                "sector_rotation": report.earnings_season.sector_rotation_signal
            },
            "market_cycle": {
                "current_regime": report.market_cycle.current_regime.value,
                "confidence": round(report.market_cycle.regime_confidence, 2),
                "days_in_regime": report.market_cycle.days_in_regime,
                "scores": {
                    "bull_bear": round(report.market_cycle.bull_bear_score, 2),
                    "accumulation_distribution": round(report.market_cycle.accumulation_distribution_score, 2),
                    "trend_strength": round(report.market_cycle.trend_strength, 2)
                },
                "volatility_regime": report.market_cycle.volatility_regime,
                "support_levels": [round(level, 2) for level in report.market_cycle.support_levels],
                "resistance_levels": [round(level, 2) for level in report.market_cycle.resistance_levels]
            },
            "insights": report.key_insights,
            "warnings": report.warnings,
            "recommendation": {
                "overall_favorability": "bullish" if report.composite_score > 60 else "bearish" if report.composite_score < 40 else "neutral",
                "score": round(report.composite_score, 2),
                "confidence": "high" if report.market_cycle.regime_confidence > 70 else "medium" if report.market_cycle.regime_confidence > 50 else "low"
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Seasonality analysis error for {request.symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/seasonality/election-cycle")
async def get_election_cycle_info():
    """
    Get current election cycle information

    Returns information about the presidential election cycle including:
    - Current phase (Year 1-4, pre/post election, mid-term)
    - Historical performance by cycle phase
    - Years until next election
    - Typical market patterns for current phase

    **Example:** `/api/advanced/seasonality/election-cycle`
    """
    try:
        from datetime import datetime

        analyzer = MarketSeasonalityAnalyzer()
        current_date = datetime.now()
        current_phase = analyzer._get_election_cycle_phase(current_date)
        years_until = analyzer._years_until_next_election(current_date)

        # Historical patterns by phase
        phase_characteristics = {
            "year_1": {
                "name": "Post-Election Year",
                "typical_performance": "Below Average",
                "characteristics": "Market adjusts to new administration policies",
                "avg_return_range": "-2% to +8%"
            },
            "year_2": {
                "name": "Mid-Term Year",
                "typical_performance": "Below Average",
                "characteristics": "Political uncertainty, mid-term elections",
                "avg_return_range": "0% to +10%"
            },
            "year_3": {
                "name": "Pre-Election Year",
                "typical_performance": "Best Performance",
                "characteristics": "Policy stimulus, incumbent seeks re-election",
                "avg_return_range": "+10% to +20%"
            },
            "year_4": {
                "name": "Election Year",
                "typical_performance": "Above Average",
                "characteristics": "Market optimism, policy promises",
                "avg_return_range": "+5% to +15%"
            }
        }

        return {
            "current_phase": current_phase.value,
            "current_year": current_date.year,
            "years_until_election": years_until,
            "next_election_year": current_date.year + years_until,
            "phase_info": phase_characteristics,
            "recommendation": "Historically, Year 3 (pre-election) shows strongest returns, while Year 1 (post-election) tends to be weakest"
        }

    except Exception as e:
        logger.error(f"Election cycle info error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/seasonality/monthly-patterns")
async def get_monthly_seasonal_patterns():
    """
    Get historical monthly seasonal patterns

    Returns typical market performance by month based on historical data.
    Useful for identifying seasonally strong/weak periods.

    **Example:** `/api/advanced/seasonality/monthly-patterns`
    """
    # Historical S&P 500 monthly performance (average)
    monthly_patterns = {
        "January": {"avg_return": 1.0, "win_rate": 0.62, "rank": 4, "characteristics": "January Effect, tax-loss selling reversal"},
        "February": {"avg_return": 0.3, "win_rate": 0.54, "rank": 8, "characteristics": "Often volatile, earnings season"},
        "March": {"avg_return": 1.1, "win_rate": 0.63, "rank": 3, "characteristics": "Quarter-end, triple witching"},
        "April": {"avg_return": 1.5, "win_rate": 0.66, "rank": 1, "characteristics": "Tax refunds, historically strong"},
        "May": {"avg_return": 0.2, "win_rate": 0.55, "rank": 9, "characteristics": "Sell in May and go away"},
        "June": {"avg_return": 0.1, "win_rate": 0.52, "rank": 10, "characteristics": "Summer doldrums begin"},
        "July": {"avg_return": 1.2, "win_rate": 0.64, "rank": 2, "characteristics": "Mid-year rally, vacation season"},
        "August": {"avg_return": -0.1, "win_rate": 0.49, "rank": 11, "characteristics": "Historically weakest month"},
        "September": {"avg_return": -0.5, "win_rate": 0.45, "rank": 12, "characteristics": "Weakest month, back to work"},
        "October": {"avg_return": 0.8, "win_rate": 0.59, "rank": 6, "characteristics": "Volatile, turnaround month"},
        "November": {"avg_return": 1.0, "win_rate": 0.62, "rank": 5, "characteristics": "Holiday rally begins"},
        "December": {"avg_return": 1.1, "win_rate": 0.65, "rank": 3, "characteristics": "Santa Claus rally, window dressing"}
    }

    return {
        "monthly_patterns": monthly_patterns,
        "insights": [
            "April historically shows the strongest performance",
            "September is typically the weakest month",
            "November-January period shows strong 'Santa Claus Rally'",
            "Summer months (May-September) tend to underperform"
        ]
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "advanced_analysis"}
