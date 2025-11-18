"""
Earnings tracking API endpoints
Provides comprehensive earnings calendar, analysis, and alerts
"""
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta
import logging

from app.services.earnings import get_earnings_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/earnings", tags=["earnings"])


class EarningsCalendarResponse(BaseModel):
    """Earnings calendar response"""
    success: bool
    total: int
    earnings: List[dict]


class EarningsAnalysisResponse(BaseModel):
    """Earnings analysis response"""
    success: bool
    ticker: str
    data: dict


class EarningsAlertConfig(BaseModel):
    """Earnings alert configuration"""
    ticker: str
    alert_before_earnings: bool = True
    days_before: int = 7
    alert_on_surprise: bool = True
    surprise_threshold: float = 5.0
    alert_on_gap: bool = True
    gap_threshold: float = 3.0
    alert_on_volume: bool = True
    volume_threshold: float = 2.0


@router.get("/health")
async def earnings_health():
    """Health check for earnings service"""
    return {
        "status": "healthy",
        "service": "earnings tracking",
        "features": [
            "earnings_calendar",
            "beat_miss_analysis",
            "price_reaction",
            "alerts",
            "calendar_export"
        ]
    }


@router.get("/calendar", response_model=EarningsCalendarResponse)
async def get_earnings_calendar(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    ticker: Optional[str] = Query(None, description="Filter by ticker symbol"),
    days_ahead: Optional[int] = Query(30, description="Number of days to look ahead")
):
    """
    Get earnings calendar for upcoming dates

    Returns earnings dates, consensus estimates, and historical performance
    for stocks reporting in the specified date range.

    Query Parameters:
    - start_date: Start date (defaults to today)
    - end_date: End date (defaults to start + days_ahead)
    - ticker: Filter by specific ticker
    - days_ahead: Number of days to look ahead (default: 30)

    Returns:
        List of earnings events with:
        - Ticker symbol
        - Earnings date and time (BMO/AMC)
        - EPS and revenue estimates
        - Historical beat/miss rate
        - Average price reaction
    """
    try:
        earnings_service = get_earnings_service()

        # Parse dates
        start = datetime.strptime(start_date, "%Y-%m-%d") if start_date else datetime.now()
        end = datetime.strptime(end_date, "%Y-%m-%d") if end_date else start + timedelta(days=days_ahead)

        # Get calendar
        calendar_data = await earnings_service.get_earnings_calendar(
            start_date=start,
            end_date=end,
            ticker=ticker
        )

        # Enrich with historical data for each ticker
        enriched_data = []
        seen_tickers = set()

        for event in calendar_data:
            event_ticker = event.get("ticker")
            if not event_ticker:
                continue

            # Get historical beat/miss for this ticker (once per ticker)
            if event_ticker not in seen_tickers:
                historical = await earnings_service.get_historical_beat_miss(event_ticker, limit=8)
                event["historical_beat_rate"] = historical.get("beat_rate", 0)
                event["historical_avg_surprise"] = historical.get("avg_surprise_pct", 0)
                seen_tickers.add(event_ticker)

            enriched_data.append(event)

        # Sort by date
        enriched_data.sort(key=lambda x: x.get("earnings_date") or datetime.max)

        return EarningsCalendarResponse(
            success=True,
            total=len(enriched_data),
            earnings=enriched_data
        )

    except Exception as e:
        logger.error(f"Error fetching earnings calendar: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ticker/{ticker}/history", response_model=EarningsAnalysisResponse)
async def get_earnings_history(
    ticker: str,
    limit: int = Query(8, description="Number of past earnings to analyze")
):
    """
    Get historical earnings beat/miss data for a ticker

    Returns:
    - Total earnings reports analyzed
    - Beat/miss count and percentage
    - Average surprise percentage
    - Detailed history of past earnings
    """
    try:
        earnings_service = get_earnings_service()
        ticker = ticker.upper()

        historical_data = await earnings_service.get_historical_beat_miss(ticker, limit)

        return EarningsAnalysisResponse(
            success=True,
            ticker=ticker,
            data=historical_data
        )

    except Exception as e:
        logger.error(f"Error fetching earnings history for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ticker/{ticker}/reaction", response_model=EarningsAnalysisResponse)
async def get_earnings_reaction(
    ticker: str,
    earnings_date: str = Query(..., description="Earnings date (YYYY-MM-DD)"),
    eps_actual: Optional[float] = Query(None, description="Actual EPS"),
    eps_estimate: Optional[float] = Query(None, description="Estimated EPS")
):
    """
    Analyze price reaction to specific earnings event

    Returns comprehensive analysis including:
    - Gap percentage (pre-close to post-open)
    - Day move percentage
    - Intraday volatility
    - Volume ratio vs average
    - Multi-day reaction (1 week, 1 month)
    """
    try:
        earnings_service = get_earnings_service()
        ticker = ticker.upper()

        # Parse date
        date = datetime.strptime(earnings_date, "%Y-%m-%d")

        # Get reaction analysis
        reaction_data = await earnings_service.analyze_earnings_reaction(
            ticker=ticker,
            earnings_date=date,
            eps_actual=eps_actual,
            eps_estimate=eps_estimate
        )

        if "error" in reaction_data:
            raise HTTPException(status_code=404, detail=reaction_data["error"])

        return EarningsAnalysisResponse(
            success=True,
            ticker=ticker,
            data=reaction_data
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")
    except Exception as e:
        logger.error(f"Error analyzing earnings reaction for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ticker/{ticker}/reactions/historical", response_model=EarningsAnalysisResponse)
async def get_historical_reactions(
    ticker: str,
    limit: int = Query(8, description="Number of past earnings to analyze")
):
    """
    Get historical earnings reaction patterns

    Analyzes past earnings events to identify typical price reaction patterns:
    - Average gap percentage
    - Average day move
    - Average volume increase
    - Individual reaction details
    """
    try:
        earnings_service = get_earnings_service()
        ticker = ticker.upper()

        reactions_data = await earnings_service.get_historical_reactions(ticker, limit)

        return EarningsAnalysisResponse(
            success=True,
            ticker=ticker,
            data=reactions_data
        )

    except Exception as e:
        logger.error(f"Error fetching historical reactions for {ticker}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/upcoming")
async def get_upcoming_earnings(
    days: int = Query(7, description="Number of days to look ahead"),
    sector: Optional[str] = Query(None, description="Filter by sector")
):
    """
    Get upcoming earnings in the next N days

    Quick endpoint for checking what's reporting soon.
    Useful for daily morning briefings.
    """
    try:
        earnings_service = get_earnings_service()

        start = datetime.now()
        end = start + timedelta(days=days)

        calendar_data = await earnings_service.get_earnings_calendar(
            start_date=start,
            end_date=end
        )

        # Group by date
        by_date = {}
        for event in calendar_data:
            date_key = event.get("earnings_date").strftime("%Y-%m-%d") if event.get("earnings_date") else "Unknown"
            if date_key not in by_date:
                by_date[date_key] = []
            by_date[date_key].append(event)

        return {
            "success": True,
            "start_date": start.strftime("%Y-%m-%d"),
            "end_date": end.strftime("%Y-%m-%d"),
            "total_events": len(calendar_data),
            "by_date": by_date
        }

    except Exception as e:
        logger.error(f"Error fetching upcoming earnings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/watchlist")
async def get_watchlist_earnings():
    """
    Get earnings dates for all stocks in watchlist

    Returns upcoming earnings for watchlist stocks so traders
    can prepare for potential volatility.
    """
    try:
        from app.api.watchlist import watchlist_service
        earnings_service = get_earnings_service()

        # Get watchlist
        watchlist_items = await watchlist_service.get_watchlist()

        if not watchlist_items:
            return {
                "success": True,
                "message": "Watchlist is empty",
                "earnings": []
            }

        # Get earnings for each watchlist ticker
        watchlist_earnings = []
        for item in watchlist_items:
            ticker = item.get("ticker", "").upper()

            # Get next 90 days of earnings
            calendar = await earnings_service.get_earnings_calendar(
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=90),
                ticker=ticker
            )

            if calendar:
                # Get historical data
                historical = await earnings_service.get_historical_beat_miss(ticker, limit=8)

                for event in calendar:
                    event["watchlist_reason"] = item.get("reason", "")
                    event["watchlist_status"] = item.get("status", "")
                    event["historical_beat_rate"] = historical.get("beat_rate", 0)
                    event["avg_surprise_pct"] = historical.get("avg_surprise_pct", 0)

                watchlist_earnings.extend(calendar)

        # Sort by date
        watchlist_earnings.sort(key=lambda x: x.get("earnings_date") or datetime.max)

        return {
            "success": True,
            "total": len(watchlist_earnings),
            "earnings": watchlist_earnings
        }

    except Exception as e:
        logger.error(f"Error fetching watchlist earnings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/alerts/configure")
async def configure_earnings_alerts(config: EarningsAlertConfig):
    """
    Configure earnings alerts for a ticker

    Set up custom alerts for:
    - Upcoming earnings (N days before)
    - Earnings surprises (beat/miss threshold)
    - Price gaps (% threshold)
    - Volume spikes (multiple of average)
    """
    try:
        # TODO: Store alert config in database
        # For now, return success
        return {
            "success": True,
            "message": f"Earnings alerts configured for {config.ticker}",
            "config": config.dict()
        }

    except Exception as e:
        logger.error(f"Error configuring earnings alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/export/calendar")
async def export_calendar(
    format: str = Query("json", description="Export format: json, csv, ical"),
    days_ahead: int = Query(30, description="Number of days to include")
):
    """
    Export earnings calendar in various formats

    Supports:
    - JSON (default)
    - CSV (for spreadsheets)
    - iCal (for Google Calendar, Apple Calendar)
    """
    try:
        earnings_service = get_earnings_service()

        # Get calendar data
        start = datetime.now()
        end = start + timedelta(days=days_ahead)

        calendar_data = await earnings_service.get_earnings_calendar(
            start_date=start,
            end_date=end
        )

        if format == "json":
            return {
                "success": True,
                "format": "json",
                "data": calendar_data
            }

        elif format == "csv":
            # Convert to CSV format
            import csv
            import io

            output = io.StringIO()
            if calendar_data:
                writer = csv.DictWriter(output, fieldnames=calendar_data[0].keys())
                writer.writeheader()
                writer.writerows(calendar_data)

            return {
                "success": True,
                "format": "csv",
                "data": output.getvalue()
            }

        elif format == "ical":
            # Generate iCal format for calendar import
            ical_events = []
            for event in calendar_data:
                ticker = event.get("ticker", "")
                date = event.get("earnings_date")
                if date:
                    ical_events.append(f"""BEGIN:VEVENT
DTSTART:{date.strftime('%Y%m%d')}
SUMMARY:{ticker} Earnings Report
DESCRIPTION:EPS Estimate: ${event.get('eps_estimate', 'N/A')}
END:VEVENT""")

            ical_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Legend AI//Earnings Calendar//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
{chr(10).join(ical_events)}
END:VCALENDAR"""

            return {
                "success": True,
                "format": "ical",
                "data": ical_content
            }

        else:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")

    except Exception as e:
        logger.error(f"Error exporting calendar: {e}")
        raise HTTPException(status_code=500, detail=str(e))
