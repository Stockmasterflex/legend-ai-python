"""
Comprehensive MTF API Endpoints
Provides comprehensive multi-timeframe analysis with scoring, timing, and alerts
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging
from dataclasses import asdict

from app.services.mtf_comprehensive import get_comprehensive_mtf_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/mtf", tags=["mtf_comprehensive"])


class MTFAnalysisRequest(BaseModel):
    """Request for comprehensive MTF analysis"""
    ticker: str = Field(..., description="Stock symbol to analyze")
    previous_score: Optional[float] = Field(None, description="Previous MTF score for delta alerts", ge=0, le=10)
    include_dashboard: bool = Field(True, description="Include full dashboard in response")


class MTFAnalysisResponse(BaseModel):
    """Response with comprehensive MTF analysis"""
    success: bool
    ticker: str
    timestamp: str

    # Summary
    summary: Dict[str, Any]

    # Score
    mtf_score: float
    score_category: str
    trade_recommendation: str

    # Alignment
    alignment_type: str
    is_aligned: bool
    bullish_timeframes: List[str]
    bearish_timeframes: List[str]

    # Entry timing
    entry_signal: str
    entry_confidence: float
    optimal_entry_tf: str

    # Alerts
    total_alerts: int
    high_priority_alerts: int
    alerts: List[Dict[str, Any]]

    # Detailed data (optional)
    dashboard: Optional[str] = None
    full_report: Optional[str] = None


@router.get("/health")
async def mtf_health():
    """Health check for comprehensive MTF service"""
    return {
        "status": "healthy",
        "service": "Comprehensive Multi-Timeframe System",
        "features": [
            "Timeframe Alignment (1M, 1W, 1D, 4H, 1H)",
            "MTF Scoring (0-10 scale)",
            "Entry Timing Optimization",
            "Divergence Detection",
            "Alert Generation",
            "Dashboard Generation"
        ],
        "version": "2.0"
    }


@router.post("/analyze", response_model=MTFAnalysisResponse)
async def analyze_comprehensive_mtf(request: MTFAnalysisRequest):
    """
    Comprehensive Multi-Timeframe Analysis

    Performs complete MTF analysis including:
    - Multi-timeframe alignment (Monthly, Weekly, Daily, 4H, 1H)
    - MTF scoring (0-10 scale)
    - Entry timing optimization
    - Divergence detection
    - Alert generation
    - Dashboard creation

    Args:
        request: Analysis request with ticker

    Returns:
        Comprehensive MTF analysis result

    Example:
        POST /api/mtf/analyze
        {
            "ticker": "NVDA",
            "include_dashboard": true
        }

        Response:
        {
            "success": true,
            "ticker": "NVDA",
            "mtf_score": 8.5,
            "score_category": "Excellent",
            "trade_recommendation": "Strong Buy",
            "alignment_type": "All Bullish",
            "entry_signal": "buy",
            "alerts": [...]
        }
    """
    try:
        ticker = request.ticker.upper().strip()

        if not ticker:
            raise HTTPException(status_code=400, detail="Ticker is required")

        logger.info(f"🔍 Starting comprehensive MTF analysis for {ticker}")

        service = get_comprehensive_mtf_service()

        # Run comprehensive analysis
        result = await service.analyze_comprehensive(ticker, request.previous_score)

        # Format alerts
        alerts = []
        for alert in result.alerts:
            alerts.append({
                "type": alert.alert_type.value,
                "severity": alert.severity.value,
                "title": alert.title,
                "message": alert.message,
                "timeframes": alert.timeframes_affected,
                "recommendation": alert.recommendation,
                "suggested_action": alert.suggested_action
            })

        # Build response
        response = MTFAnalysisResponse(
            success=True,
            ticker=ticker,
            timestamp=result.timestamp.isoformat(),
            summary=result.summary,
            mtf_score=result.mtf_score.overall_score,
            score_category=result.mtf_score.category,
            trade_recommendation=result.trade_recommendation,
            alignment_type=result.alignment.alignment_type.replace("_", " ").title(),
            is_aligned=result.alignment.is_aligned,
            bullish_timeframes=result.alignment.bullish_timeframes,
            bearish_timeframes=result.alignment.bearish_timeframes,
            entry_signal=result.entry_timing.current_signal.signal_type,
            entry_confidence=result.entry_timing.current_signal.confidence,
            optimal_entry_tf=result.entry_timing.optimal_entry_tf,
            total_alerts=len(result.alerts),
            high_priority_alerts=len([a for a in result.alerts if a.severity.value in ["critical", "high"]]),
            alerts=alerts,
            dashboard=service.dashboard_generator.format_dashboard_text(result.dashboard) if request.include_dashboard else None,
            full_report=service.format_comprehensive_report(result, include_dashboard=True)
        )

        logger.info(f"✅ Comprehensive MTF analysis complete for {ticker}: {result.mtf_score.overall_score}/10")

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in comprehensive MTF analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analyze/{ticker}")
async def quick_mtf_analysis(
    ticker: str,
    include_dashboard: bool = Query(False, description="Include dashboard in response")
):
    """
    Quick MTF Analysis (GET endpoint)

    Shorthand endpoint for quick analysis without JSON body.

    Args:
        ticker: Stock symbol
        include_dashboard: Include dashboard text

    Returns:
        Quick MTF analysis result
    """
    try:
        request = MTFAnalysisRequest(
            ticker=ticker,
            include_dashboard=include_dashboard
        )

        return await analyze_comprehensive_mtf(request)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Quick MTF analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/dashboard")
async def get_mtf_dashboard(request: MTFAnalysisRequest):
    """
    Get MTF Dashboard Only

    Returns formatted dashboard text for display

    Args:
        request: Analysis request

    Returns:
        Dashboard text
    """
    try:
        ticker = request.ticker.upper().strip()

        service = get_comprehensive_mtf_service()
        result = await service.analyze_comprehensive(ticker)

        dashboard_text = service.dashboard_generator.format_dashboard_text(result.dashboard)

        return {
            "success": True,
            "ticker": ticker,
            "dashboard": dashboard_text
        }

    except Exception as e:
        logger.error(f"Dashboard generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/alerts")
async def get_mtf_alerts(request: MTFAnalysisRequest):
    """
    Get MTF Alerts Only

    Returns only alert information

    Args:
        request: Analysis request

    Returns:
        Alert list
    """
    try:
        ticker = request.ticker.upper().strip()

        service = get_comprehensive_mtf_service()
        result = await service.analyze_comprehensive(ticker, request.previous_score)

        alerts = []
        for alert in result.alerts:
            alerts.append({
                "id": alert.alert_id,
                "type": alert.alert_type.value,
                "severity": alert.severity.value,
                "title": alert.title,
                "message": alert.message,
                "timeframes": alert.timeframes_affected,
                "recommendation": alert.recommendation,
                "suggested_action": alert.suggested_action,
                "timestamp": alert.timestamp.isoformat()
            })

        return {
            "success": True,
            "ticker": ticker,
            "total_alerts": len(alerts),
            "critical_alerts": len([a for a in alerts if a["severity"] == "critical"]),
            "high_alerts": len([a for a in alerts if a["severity"] == "high"]),
            "alerts": alerts
        }

    except Exception as e:
        logger.error(f"Alert generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/score")
async def get_mtf_score(request: MTFAnalysisRequest):
    """
    Get MTF Score Only

    Returns only scoring information

    Args:
        request: Analysis request

    Returns:
        MTF score and breakdown
    """
    try:
        ticker = request.ticker.upper().strip()

        service = get_comprehensive_mtf_service()
        result = await service.analyze_comprehensive(ticker)

        return {
            "success": True,
            "ticker": ticker,
            "mtf_score": result.mtf_score.overall_score,
            "category": result.mtf_score.category,
            "trade_recommendation": result.trade_recommendation,
            "score_breakdown": {
                "trend_alignment": result.mtf_score.trend_alignment_score,
                "momentum": result.mtf_score.momentum_score,
                "volume": result.mtf_score.volume_score,
                "patterns": result.mtf_score.pattern_score
            },
            "scoring_notes": result.mtf_score.scoring_notes
        }

    except Exception as e:
        logger.error(f"Score calculation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/entry-timing")
async def get_entry_timing(request: MTFAnalysisRequest):
    """
    Get Entry Timing Only

    Returns optimal entry timing analysis

    Args:
        request: Analysis request

    Returns:
        Entry timing details
    """
    try:
        ticker = request.ticker.upper().strip()

        service = get_comprehensive_mtf_service()
        result = await service.analyze_comprehensive(ticker)

        signal = result.entry_timing.current_signal

        return {
            "success": True,
            "ticker": ticker,
            "optimal_entry_tf": result.entry_timing.optimal_entry_tf,
            "signal": {
                "type": signal.signal_type,
                "confidence": signal.confidence,
                "entry_price": signal.entry_price,
                "stop_loss": signal.stop_loss,
                "take_profit": signal.take_profit,
                "risk_reward_ratio": signal.risk_reward_ratio,
                "entry_reason": signal.entry_reason,
                "higher_tf_confirmed": signal.higher_tf_confirmed,
                "volume_confirmed": signal.volume_confirmed,
                "pattern_confirmed": signal.pattern_confirmed
            },
            "timing_notes": result.entry_timing.timing_notes,
            "wait_for": result.entry_timing.wait_for,
            "alternative_entries": [
                {
                    "timeframe": alt.entry_timeframe,
                    "type": alt.signal_type,
                    "confidence": alt.confidence,
                    "entry_price": alt.entry_price
                }
                for alt in result.entry_timing.alternative_entries
            ]
        }

    except Exception as e:
        logger.error(f"Entry timing calculation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/report/{ticker}")
async def get_full_report(
    ticker: str,
    format: str = Query("text", description="Report format: text or json")
):
    """
    Get Full MTF Report

    Returns complete analysis report in text or JSON format

    Args:
        ticker: Stock symbol
        format: Report format (text or json)

    Returns:
        Full report
    """
    try:
        ticker = ticker.upper().strip()

        service = get_comprehensive_mtf_service()
        result = await service.analyze_comprehensive(ticker)

        if format == "text":
            report = service.format_comprehensive_report(result, include_dashboard=True)

            return {
                "success": True,
                "ticker": ticker,
                "format": "text",
                "report": report
            }

        else:  # JSON format
            return {
                "success": True,
                "ticker": ticker,
                "format": "json",
                "report": {
                    "summary": result.summary,
                    "mtf_score": asdict(result.mtf_score),
                    "alignment": asdict(result.alignment),
                    "divergences": [asdict(d) for d in result.divergences],
                    "entry_timing": {
                        "optimal_tf": result.entry_timing.optimal_entry_tf,
                        "signal": asdict(result.entry_timing.current_signal),
                        "timing_notes": result.entry_timing.timing_notes,
                        "wait_for": result.entry_timing.wait_for
                    },
                    "alerts": [
                        {
                            "type": a.alert_type.value,
                            "severity": a.severity.value,
                            "title": a.title,
                            "message": a.message
                        }
                        for a in result.alerts
                    ],
                    "timeframe_data": {
                        tf: asdict(data)
                        for tf, data in result.timeframe_data.items()
                    }
                }
            }

    except Exception as e:
        logger.error(f"Report generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
