"""
Macro Events Router
- Economic Calendar
- Historical Impact Analysis
- Market Regime Detection
- Countdown Timers
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import logging

from app.services.macro_events import MacroEventsService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/macro", tags=["Macro Events"])


class EconomicCalendarRequest(BaseModel):
    """Economic calendar request"""
    start_date: Optional[datetime] = Field(None, description="Start date (default: today)")
    end_date: Optional[datetime] = Field(None, description="End date (default: 30 days from now)")
    importance: Optional[str] = Field(None, description="Filter by importance: HIGH, MEDIUM, LOW")
    event_type: Optional[str] = Field(None, description="Filter by event type: FOMC, CPI, PPI, GDP, etc.")


class EventImpactRequest(BaseModel):
    """Historical event impact request"""
    event_type: str = Field(..., description="Event type: FOMC, CPI, PPI, GDP, NFP, etc.")
    symbol: str = Field("SPY", description="Symbol to analyze (default: SPY)")
    lookback_periods: int = Field(10, ge=1, le=50, description="Number of past events to analyze")


class NextEventRequest(BaseModel):
    """Next event countdown request"""
    event_type: Optional[str] = Field(None, description="Specific event type to search for")


@router.get("/calendar")
async def get_economic_calendar(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    importance: Optional[str] = Query(None, description="Filter by importance: HIGH, MEDIUM, LOW"),
    event_type: Optional[str] = Query(None, description="Filter by event type: FOMC, CPI, etc.")
):
    """
    Get economic calendar with upcoming events

    **Features:**
    - Fed meetings (FOMC)
    - CPI/PPI releases
    - GDP reports
    - Unemployment data (NFP)
    - Earnings seasons
    - Options expiration dates
    - Dividend dates

    **Returns:**
    - Event details with dates and times
    - Previous, forecast, and actual values
    - Importance ratings
    - Countdown timers
    - Event descriptions

    **Example:**
    ```
    GET /api/macro/calendar?importance=HIGH
    ```

    **Response:**
    ```json
    [
      {
        "event_type": "FOMC",
        "event_name": "FOMC Meeting Decision",
        "event_date": "2025-03-19T14:00:00",
        "importance": "HIGH",
        "countdown": {
          "days": 45,
          "hours": 14,
          "minutes": 30,
          "human_readable": "45d 14h"
        }
      }
    ]
    ```
    """
    try:
        service = MacroEventsService()

        # Parse dates
        start_dt = datetime.fromisoformat(start_date) if start_date else None
        end_dt = datetime.fromisoformat(end_date) if end_date else None

        events = await service.get_economic_calendar(
            start_date=start_dt,
            end_date=end_dt,
            importance=importance,
            event_type=event_type
        )

        await service.close()

        return {
            "success": True,
            "count": len(events),
            "events": events
        }

    except Exception as e:
        logger.error(f"Error fetching economic calendar: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/impact/historical")
async def get_historical_impact(request: EventImpactRequest):
    """
    Analyze historical market reaction to macro events

    **Analysis includes:**
    - Average market reaction (1 hour, 1 day, 1 week)
    - Volatility changes
    - Sector performance
    - Pattern success rates during events
    - Direction and magnitude statistics

    **Example Request:**
    ```json
    {
      "event_type": "FOMC",
      "symbol": "SPY",
      "lookback_periods": 10
    }
    ```

    **Response:**
    ```json
    {
      "event_type": "FOMC",
      "symbol": "SPY",
      "periods_analyzed": 10,
      "average_reaction": {
        "1_day": {
          "mean_change": 1.2,
          "median_change": 1.1,
          "std_dev": 0.8,
          "positive_rate": 65.0,
          "max_move": 2.5
        }
      },
      "sector_performance": {
        "Technology": 0.5,
        "Financials": 1.8
      }
    }
    ```
    """
    try:
        service = MacroEventsService()

        impact = await service.get_historical_impact(
            event_type=request.event_type,
            symbol=request.symbol,
            lookback_periods=request.lookback_periods
        )

        await service.close()

        return {
            "success": True,
            "data": impact
        }

    except Exception as e:
        logger.error(f"Error analyzing event impact: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/regime/current")
async def get_current_market_regime(
    symbols: Optional[List[str]] = Query(None, description="Symbols to analyze (default: SPY, QQQ, IWM)")
):
    """
    Detect current market regime

    **Analyzes:**
    - Bull/bear/sideways market
    - High/low volatility environment
    - Rate environment (rising/falling/stable)
    - Seasonal patterns
    - VIX levels and percentiles
    - Market breadth
    - Trend strength

    **Returns:**
    - Current regime classification
    - Confidence score
    - Trading implications
    - Position sizing recommendations
    - Sector recommendations

    **Example:**
    ```
    GET /api/macro/regime/current
    ```

    **Response:**
    ```json
    {
      "regime_type": "BULL",
      "volatility_regime": "LOW_VOL",
      "rate_environment": "STABLE",
      "vix_level": 14.5,
      "confidence_score": 87.3,
      "trading_implications": {
        "position_sizing": "NORMAL to AGGRESSIVE",
        "pattern_reliability": "HIGH",
        "recommended_stop": "7-8% below entry"
      }
    }
    ```
    """
    try:
        service = MacroEventsService()

        regime = await service.detect_market_regime(symbols=symbols)

        await service.close()

        return {
            "success": True,
            "regime": regime
        }

    except Exception as e:
        logger.error(f"Error detecting market regime: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/countdown/next")
async def get_next_event_countdown(
    event_type: Optional[str] = Query(None, description="Specific event type (FOMC, CPI, etc.)")
):
    """
    Get countdown to next major event

    **Features:**
    - Time remaining to next Fed decision
    - Earnings season countdown
    - Options expiration dates
    - Next CPI/GDP/NFP release

    **Example:**
    ```
    GET /api/macro/countdown/next?event_type=FOMC
    ```

    **Response:**
    ```json
    {
      "event": {
        "event_type": "FOMC",
        "event_name": "FOMC Meeting Decision",
        "event_date": "2025-03-19T14:00:00"
      },
      "countdown": {
        "days": 45,
        "hours": 14,
        "minutes": 30,
        "total_hours": 1094,
        "human_readable": "45d 14h"
      },
      "upcoming_events": [...]
    }
    ```
    """
    try:
        service = MacroEventsService()

        countdown = await service.get_next_event_countdown(event_type=event_type)

        await service.close()

        return {
            "success": True,
            "data": countdown
        }

    except Exception as e:
        logger.error(f"Error getting event countdown: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/events/upcoming")
async def get_upcoming_high_impact_events(
    days_ahead: int = Query(30, ge=1, le=90, description="Number of days to look ahead")
):
    """
    Get all upcoming high-impact events

    Quick access to the most important events in the next N days.

    **Example:**
    ```
    GET /api/macro/events/upcoming?days_ahead=30
    ```

    **Returns:**
    - Only HIGH importance events
    - Sorted by date
    - Includes countdown timers
    """
    try:
        service = MacroEventsService()

        events = await service.get_economic_calendar(
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=days_ahead),
            importance="HIGH"
        )

        # Sort by date
        events.sort(key=lambda x: x["event_date"])

        await service.close()

        return {
            "success": True,
            "days_ahead": days_ahead,
            "count": len(events),
            "events": events
        }

    except Exception as e:
        logger.error(f"Error fetching upcoming events: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard")
async def get_macro_dashboard():
    """
    Get comprehensive macro dashboard

    **Combines:**
    - Next 5 high-impact events with countdowns
    - Current market regime
    - Recent event impacts
    - Trading recommendations based on regime

    **Example:**
    ```
    GET /api/macro/dashboard
    ```

    **Returns:**
    Complete overview of macro environment and upcoming events
    """
    try:
        service = MacroEventsService()

        # Get upcoming events
        upcoming = await service.get_economic_calendar(
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=60),
            importance="HIGH"
        )
        upcoming.sort(key=lambda x: x["event_date"])

        # Get current regime
        regime = await service.detect_market_regime()

        # Get next event countdown
        next_event = await service.get_next_event_countdown()

        await service.close()

        return {
            "success": True,
            "dashboard": {
                "next_event": next_event,
                "upcoming_events": upcoming[:5],
                "current_regime": regime,
                "last_updated": datetime.now().isoformat()
            }
        }

    except Exception as e:
        logger.error(f"Error generating macro dashboard: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
