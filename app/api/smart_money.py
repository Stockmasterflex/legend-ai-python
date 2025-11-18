"""
Smart Money API Endpoints

Provides REST API access to smart money tracking data
"""

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List
from datetime import datetime
from pathlib import Path
import logging

from app.services.smart_money import (
    get_dark_pool_service,
    get_institutional_service,
    get_block_trade_service,
    get_analytics_service
)
from app.services.smart_money.models import (
    DarkPoolPrint,
    InstitutionalHolder,
    InsiderTransaction,
    BlockTrade,
    SmartMoneyFlow,
    SmartMoneyIndicators,
    SmartMoneyAlert
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/smart-money", tags=["Smart Money"])

# Setup templates
templates_dir = Path(__file__).parent.parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))


# ============================================================================
# Dashboard UI
# ============================================================================

@router.get("/dashboard", response_class=HTMLResponse)
async def smart_money_dashboard(request: Request):
    """
    Smart Money Analytics Dashboard UI

    Interactive dashboard for tracking:
    - Dark pool prints and activity
    - Institutional ownership and flows
    - Block trades and unusual options activity
    - Smart money indicators and alerts
    """
    return templates.TemplateResponse(
        "smart_money_dashboard.html",
        {"request": request}
    )


# ============================================================================
# Dark Pool Endpoints
# ============================================================================

@router.get("/dark-pool/{symbol}/prints", response_model=List[DarkPoolPrint])
async def get_dark_pool_prints(
    symbol: str,
    limit: int = Query(50, ge=1, le=500),
    min_size: Optional[int] = None,
    min_value: Optional[float] = None
):
    """
    Get real-time dark pool prints for a symbol

    - **symbol**: Stock ticker symbol
    - **limit**: Maximum number of prints to return (1-500)
    - **min_size**: Minimum share size filter
    - **min_value**: Minimum dollar value filter
    """
    try:
        service = get_dark_pool_service()
        prints = await service.get_realtime_prints(
            symbol=symbol.upper(),
            limit=limit,
            min_size=min_size,
            min_value=min_value
        )
        return prints
    except Exception as e:
        logger.error(f"Error getting dark pool prints: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dark-pool/{symbol}/summary")
async def get_dark_pool_summary(
    symbol: str,
    date: Optional[str] = None
):
    """
    Get daily dark pool summary

    - **symbol**: Stock ticker symbol
    - **date**: Date in YYYY-MM-DD format (defaults to today)
    """
    try:
        service = get_dark_pool_service()

        date_obj = None
        if date:
            date_obj = datetime.fromisoformat(date)

        summary = await service.get_daily_summary(symbol.upper(), date_obj)
        return summary
    except Exception as e:
        logger.error(f"Error getting dark pool summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dark-pool/{symbol}/patterns")
async def get_dark_pool_patterns(
    symbol: str,
    days: int = Query(30, ge=1, le=90)
):
    """
    Get historical dark pool patterns

    - **symbol**: Stock ticker symbol
    - **days**: Number of days to analyze (1-90)
    """
    try:
        service = get_dark_pool_service()
        patterns = await service.get_historical_patterns(symbol.upper(), days)
        return patterns
    except Exception as e:
        logger.error(f"Error getting dark pool patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dark-pool/{symbol}/unusual")
async def get_unusual_dark_pool_activity(
    symbol: str,
    lookback_days: int = Query(30, ge=1, le=90)
):
    """
    Detect unusual dark pool activity

    - **symbol**: Stock ticker symbol
    - **lookback_days**: Days to compare against (1-90)
    """
    try:
        service = get_dark_pool_service()
        unusual = await service.detect_unusual_activity(symbol.upper(), lookback_days)
        return unusual
    except Exception as e:
        logger.error(f"Error detecting unusual activity: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Institutional Ownership Endpoints
# ============================================================================

@router.get("/institutional/{symbol}/holders", response_model=List[InstitutionalHolder])
async def get_top_institutional_holders(
    symbol: str,
    limit: int = Query(20, ge=1, le=100)
):
    """
    Get top institutional holders

    - **symbol**: Stock ticker symbol
    - **limit**: Number of top holders to return (1-100)
    """
    try:
        service = get_institutional_service()
        holders = await service.get_top_holders(symbol.upper(), limit)
        return holders
    except Exception as e:
        logger.error(f"Error getting top holders: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/institutional/{symbol}/changes")
async def get_institutional_changes(
    symbol: str,
    change_type: Optional[str] = Query(None, regex="^(increased|decreased|new|sold_out)$")
):
    """
    Get recent institutional position changes

    - **symbol**: Stock ticker symbol
    - **change_type**: Filter by change type (increased, decreased, new, sold_out)
    """
    try:
        service = get_institutional_service()
        changes = await service.get_recent_changes(symbol.upper(), change_type)
        return changes
    except Exception as e:
        logger.error(f"Error getting institutional changes: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/institutional/{symbol}/flow")
async def get_institutional_flow(
    symbol: str,
    quarters: int = Query(1, ge=1, le=8)
):
    """
    Get institutional money flow

    - **symbol**: Stock ticker symbol
    - **quarters**: Number of quarters to analyze (1-8)
    """
    try:
        service = get_institutional_service()
        flow = await service.get_institutional_flow(symbol.upper(), quarters)
        return flow
    except Exception as e:
        logger.error(f"Error getting institutional flow: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/institutional/{symbol}/insiders", response_model=List[InsiderTransaction])
async def get_insider_transactions(
    symbol: str,
    days: int = Query(90, ge=1, le=365),
    transaction_type: Optional[str] = None
):
    """
    Get insider transactions

    - **symbol**: Stock ticker symbol
    - **days**: Number of days to look back (1-365)
    - **transaction_type**: Filter by transaction type (Buy, Sell, etc.)
    """
    try:
        service = get_institutional_service()
        transactions = await service.get_insider_transactions(
            symbol.upper(),
            days,
            transaction_type
        )
        return transactions
    except Exception as e:
        logger.error(f"Error getting insider transactions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/institutional/{symbol}/insider-sentiment")
async def get_insider_sentiment(
    symbol: str,
    days: int = Query(90, ge=1, le=365)
):
    """
    Analyze insider trading sentiment

    - **symbol**: Stock ticker symbol
    - **days**: Number of days to analyze (1-365)
    """
    try:
        service = get_institutional_service()
        sentiment = await service.analyze_insider_sentiment(symbol.upper(), days)
        return sentiment
    except Exception as e:
        logger.error(f"Error analyzing insider sentiment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Block Trade Endpoints
# ============================================================================

@router.get("/blocks/{symbol}/recent", response_model=List[BlockTrade])
async def get_recent_block_trades(
    symbol: str,
    hours: int = Query(24, ge=1, le=168),
    min_value: Optional[float] = None
):
    """
    Get recent block trades

    - **symbol**: Stock ticker symbol
    - **hours**: Number of hours to look back (1-168)
    - **min_value**: Minimum dollar value filter
    """
    try:
        service = get_block_trade_service()
        trades = await service.get_recent_blocks(
            symbol.upper(),
            hours,
            min_value=min_value
        )
        return trades
    except Exception as e:
        logger.error(f"Error getting recent blocks: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/blocks/{symbol}/options", response_model=List[BlockTrade])
async def get_unusual_options(
    symbol: str,
    hours: int = Query(24, ge=1, le=168),
    min_premium: Optional[float] = None
):
    """
    Get unusual options activity

    - **symbol**: Stock ticker symbol
    - **hours**: Number of hours to look back (1-168)
    - **min_premium**: Minimum premium filter
    """
    try:
        service = get_block_trade_service()
        options = await service.get_unusual_options_activity(
            symbol.upper(),
            hours,
            min_premium
        )
        return options
    except Exception as e:
        logger.error(f"Error getting unusual options: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/blocks/{symbol}/options-positioning")
async def get_options_positioning(
    symbol: str,
    days: int = Query(7, ge=1, le=30)
):
    """
    Analyze options positioning

    - **symbol**: Stock ticker symbol
    - **days**: Number of days to analyze (1-30)
    """
    try:
        service = get_block_trade_service()
        positioning = await service.analyze_options_positioning(symbol.upper(), days)
        return positioning
    except Exception as e:
        logger.error(f"Error analyzing options positioning: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/blocks/{symbol}/volume-spike")
async def detect_volume_spike(
    symbol: str,
    current_volume: int,
    threshold: float = Query(2.0, ge=1.0, le=10.0)
):
    """
    Detect volume spikes

    - **symbol**: Stock ticker symbol
    - **current_volume**: Current volume to compare
    - **threshold**: Multiple of average volume to trigger (1.0-10.0)
    """
    try:
        service = get_block_trade_service()
        spike = await service.detect_volume_spikes(
            symbol.upper(),
            current_volume,
            threshold
        )
        return spike
    except Exception as e:
        logger.error(f"Error detecting volume spike: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/blocks/{symbol}/divergence")
async def detect_divergence(
    symbol: str,
    price_change: float,
    days: int = Query(5, ge=1, le=30)
):
    """
    Detect smart money divergence

    - **symbol**: Stock ticker symbol
    - **price_change**: Percentage price change over period
    - **days**: Number of days to analyze (1-30)
    """
    try:
        service = get_block_trade_service()
        divergence = await service.detect_smart_money_divergence(
            symbol.upper(),
            price_change,
            days
        )
        return divergence
    except Exception as e:
        logger.error(f"Error detecting divergence: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Analytics Endpoints
# ============================================================================

@router.get("/analytics/{symbol}/flow", response_model=SmartMoneyFlow)
async def get_smart_money_flow(
    symbol: str,
    date: Optional[str] = None,
    total_volume: Optional[int] = None
):
    """
    Get comprehensive smart money flow

    - **symbol**: Stock ticker symbol
    - **date**: Date in YYYY-MM-DD format (defaults to today)
    - **total_volume**: Total market volume for ratio calculation
    """
    try:
        service = get_analytics_service()

        date_obj = None
        if date:
            date_obj = datetime.fromisoformat(date)

        flow = await service.get_smart_money_flow(
            symbol.upper(),
            date_obj,
            total_volume
        )
        return flow
    except Exception as e:
        logger.error(f"Error getting smart money flow: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/{symbol}/indicators", response_model=SmartMoneyIndicators)
async def get_smart_money_indicators(
    symbol: str,
    price_change: Optional[float] = None
):
    """
    Get comprehensive smart money indicators

    - **symbol**: Stock ticker symbol
    - **price_change**: Recent price change percentage for divergence analysis
    """
    try:
        service = get_analytics_service()
        indicators = await service.get_smart_money_indicators(
            symbol.upper(),
            price_change
        )
        return indicators
    except Exception as e:
        logger.error(f"Error getting smart money indicators: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/{symbol}/dashboard")
async def get_dashboard_data(
    symbol: str,
    price_change: Optional[float] = None,
    total_volume: Optional[int] = None
):
    """
    Get complete smart money dashboard data

    - **symbol**: Stock ticker symbol
    - **price_change**: Recent price change percentage
    - **total_volume**: Total market volume
    """
    try:
        service = get_analytics_service()
        dashboard = await service.get_dashboard_data(
            symbol.upper(),
            price_change,
            total_volume
        )
        return dashboard
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts/{symbol}", response_model=List[SmartMoneyAlert])
async def get_smart_money_alerts(
    symbol: str,
    hours: int = Query(24, ge=1, le=168),
    severity: Optional[str] = Query(None, regex="^(low|medium|high)$")
):
    """
    Get smart money alerts

    - **symbol**: Stock ticker symbol
    - **hours**: Number of hours to look back (1-168)
    - **severity**: Filter by severity (low, medium, high)
    """
    try:
        service = get_block_trade_service()
        alerts = await service.get_alerts(symbol.upper(), hours, severity)
        return alerts
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Demo/Testing Endpoints
# ============================================================================

@router.post("/demo/{symbol}/generate-data")
async def generate_demo_data(
    symbol: str,
    days: int = Query(7, ge=1, le=30)
):
    """
    Generate sample data for testing (demo purposes only)

    - **symbol**: Stock ticker symbol
    - **days**: Number of days of data to generate
    """
    try:
        dp_service = get_dark_pool_service()
        inst_service = get_institutional_service()
        block_service = get_block_trade_service()

        # Generate sample data for all services
        await dp_service.generate_sample_data(symbol.upper(), days)
        await inst_service.generate_sample_data(symbol.upper())
        await block_service.generate_sample_data(symbol.upper(), days)

        return {
            "status": "success",
            "message": f"Generated {days} days of sample data for {symbol}",
            "symbol": symbol.upper(),
            "days": days
        }
    except Exception as e:
        logger.error(f"Error generating demo data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
