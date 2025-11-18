"""
TradingView Integration API
Handles webhooks, alerts, sync, and strategy management
"""

from fastapi import APIRouter, HTTPException, Request, Header, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
import logging

from app.services.tradingview import tradingview_service
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()
router = APIRouter()


# Request/Response Models
class TradingViewWebhookPayload(BaseModel):
    """TradingView webhook payload schema"""
    ticker: Optional[str] = Field(None, description="Stock ticker symbol")
    symbol: Optional[str] = Field(None, description="Alternative symbol field")
    alert_name: Optional[str] = Field(None, description="Name of the alert in TradingView")
    message: Optional[str] = Field(None, description="Alert message")
    close: Optional[float] = Field(None, description="Close price")
    price: Optional[float] = Field(None, description="Alternative price field")
    time: Optional[str] = Field(None, description="Timestamp")
    timenow: Optional[str] = Field(None, description="Alternative timestamp field")
    interval: Optional[str] = Field(None, description="Timeframe (1m, 5m, 1h, 1D, etc.)")
    timeframe: Optional[str] = Field(None, description="Alternative timeframe field")
    strategy: Optional[str] = Field(None, description="Strategy name")
    strategy_name: Optional[str] = Field(None, description="Alternative strategy name")

    # Indicator values
    rsi: Optional[float] = None
    macd: Optional[float] = None
    ema: Optional[float] = None
    sma: Optional[float] = None
    volume: Optional[float] = None
    bb_upper: Optional[float] = None
    bb_lower: Optional[float] = None

    # Custom fields
    extra: Optional[Dict[str, Any]] = Field(default_factory=dict)

    class Config:
        extra = "allow"  # Allow additional fields


class WebhookResponse(BaseModel):
    """Webhook processing response"""
    success: bool
    alert_id: Optional[int] = None
    symbol: Optional[str] = None
    alert_type: Optional[str] = None
    action: Optional[str] = None
    error: Optional[str] = None


class AlertQueryResponse(BaseModel):
    """Alert query response"""
    success: bool
    count: int
    alerts: List[Dict[str, Any]]


class SyncPatternRequest(BaseModel):
    """Sync pattern to TradingView request"""
    pattern_scan_id: int


class SyncWatchlistRequest(BaseModel):
    """Sync watchlist to TradingView request"""
    watchlist_ids: List[int]


class ImportStrategyRequest(BaseModel):
    """Import TradingView strategy request"""
    name: str
    description: str
    strategy_config: Dict[str, Any]
    pine_script_code: Optional[str] = None


class BacktestStrategyRequest(BaseModel):
    """Backtest strategy request"""
    strategy_id: int
    symbols: List[str]
    start_date: str
    end_date: str


# Database dependency
def get_db():
    """Get database session"""
    from app.lifecycle import engine
    from sqlalchemy.orm import sessionmaker

    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/webhooks/tradingview", response_model=WebhookResponse)
async def tradingview_webhook(
    request: Request,
    payload: TradingViewWebhookPayload,
    x_tradingview_signature: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    TradingView Webhook Receiver

    Receives alerts from TradingView and processes them:
    - Validates signatures (if configured)
    - Rate limiting by IP
    - Parses alert data
    - Processes different alert types
    - Confirms patterns with Legend AI
    - Logs to database

    **Webhook Setup in TradingView:**
    1. Create alert in TradingView
    2. Set webhook URL: `https://your-domain.com/api/tradingview/webhooks/tradingview`
    3. Configure alert message as JSON:
    ```json
    {
        "ticker": "{{ticker}}",
        "close": {{close}},
        "time": "{{time}}",
        "interval": "{{interval}}",
        "alert_name": "My Alert",
        "message": "Pattern detected"
    }
    ```
    """
    try:
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"

        # Rate limiting
        if not tradingview_service.check_rate_limit(client_ip):
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Max 100 requests per minute."
            )

        # Signature validation (if secret is configured)
        if hasattr(settings, 'tradingview_webhook_secret') and settings.tradingview_webhook_secret:
            body = await request.body()
            signature = x_tradingview_signature or ""

            if not tradingview_service.verify_signature(
                body,
                signature,
                settings.tradingview_webhook_secret
            ):
                logger.warning(f"Invalid webhook signature from {client_ip}")
                raise HTTPException(status_code=401, detail="Invalid signature")

        # Convert payload to dict
        payload_dict = payload.dict(exclude_none=True)

        # Process webhook
        result = await tradingview_service.process_webhook(
            db=db,
            payload=payload_dict,
            ip_address=client_ip
        )

        if result["success"]:
            return WebhookResponse(**result)
        else:
            raise HTTPException(status_code=400, detail=result.get("error", "Processing failed"))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts", response_model=AlertQueryResponse)
async def get_alerts(
    symbol: Optional[str] = None,
    alert_type: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get Recent TradingView Alerts

    Query parameters:
    - symbol: Filter by ticker symbol (e.g., "AAPL")
    - alert_type: Filter by type (price, indicator, pattern, breakout, stop_loss)
    - limit: Maximum number of alerts to return (default 50)
    """
    try:
        alerts = await tradingview_service.get_recent_alerts(
            db=db,
            symbol=symbol,
            alert_type=alert_type,
            limit=limit
        )

        return AlertQueryResponse(
            success=True,
            count=len(alerts),
            alerts=alerts
        )

    except Exception as e:
        logger.error(f"Error fetching alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync/pattern")
async def sync_pattern_to_tradingview(
    request: SyncPatternRequest,
    db: Session = Depends(get_db)
):
    """
    Push Legend AI Pattern to TradingView

    Creates a sync record for a detected pattern that can be used
    to create TradingView alerts programmatically.
    """
    try:
        from app.models import PatternScan

        pattern_scan = db.query(PatternScan).filter(
            PatternScan.id == request.pattern_scan_id
        ).first()

        if not pattern_scan:
            raise HTTPException(status_code=404, detail="Pattern scan not found")

        result = await tradingview_service.sync_pattern_to_tradingview(
            db=db,
            pattern_scan=pattern_scan
        )

        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error syncing pattern: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync/watchlist")
async def sync_watchlist_to_tradingview(
    request: SyncWatchlistRequest,
    db: Session = Depends(get_db)
):
    """
    Sync Legend AI Watchlist to TradingView

    Creates sync records for watchlist items that can be used
    to create TradingView alerts.
    """
    try:
        result = await tradingview_service.sync_watchlist_to_tradingview(
            db=db,
            watchlist_ids=request.watchlist_ids
        )

        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error syncing watchlist: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/strategies/import")
async def import_tradingview_strategy(
    request: ImportStrategyRequest,
    db: Session = Depends(get_db)
):
    """
    Import TradingView Strategy

    Import a TradingView strategy for backtesting against Legend AI data.

    Strategy config should include:
    - timeframe: "1D", "4H", etc.
    - indicators: ["RSI", "MACD", "EMA"]
    - entry_conditions: {...}
    - exit_conditions: {...}
    - risk_reward_ratio: 2.0
    - win_rate: 0.65
    - profit_factor: 1.8
    """
    try:
        result = await tradingview_service.import_strategy(
            db=db,
            name=request.name,
            description=request.description,
            strategy_config=request.strategy_config,
            pine_script_code=request.pine_script_code
        )

        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error importing strategy: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/strategies/backtest")
async def backtest_tradingview_strategy(
    request: BacktestStrategyRequest,
    db: Session = Depends(get_db)
):
    """
    Backtest TradingView Strategy

    Run a backtest of an imported TradingView strategy against Legend AI data.

    Returns performance metrics:
    - Total trades
    - Win rate
    - Profit factor
    - Max drawdown
    - Sharpe ratio
    """
    try:
        result = await tradingview_service.backtest_strategy(
            db=db,
            strategy_id=request.strategy_id,
            symbols=request.symbols,
            start_date=request.start_date,
            end_date=request.end_date
        )

        if result["success"]:
            return result
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error backtesting strategy: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/strategies")
async def list_strategies(
    db: Session = Depends(get_db)
):
    """
    List Imported TradingView Strategies

    Returns all strategies imported from TradingView.
    """
    try:
        from app.models import TradingViewStrategy

        strategies = db.query(TradingViewStrategy).all()

        return {
            "success": True,
            "count": len(strategies),
            "strategies": [
                {
                    "id": s.id,
                    "name": s.name,
                    "description": s.description,
                    "timeframe": s.timeframe,
                    "win_rate": s.win_rate,
                    "profit_factor": s.profit_factor,
                    "max_drawdown": s.max_drawdown,
                    "legend_optimized": s.legend_optimized,
                    "created_at": s.created_at.isoformat() if s.created_at else None
                }
                for s in strategies
            ]
        }

    except Exception as e:
        logger.error(f"Error listing strategies: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """TradingView Integration Health Check"""
    return {
        "status": "ok",
        "service": "tradingview_integration",
        "version": "1.0.0"
    }
