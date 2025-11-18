"""
Trade Journal API
Endpoints for comprehensive trade journaling with lessons learned
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

from app.services.database import get_db
from app.services.trade_journal_service import TradeJournalService

router = APIRouter(prefix="/api/journal", tags=["Trade Journal"])


# Pydantic models
class LogEntryRequest(BaseModel):
    portfolio_id: int = Field(..., description="Portfolio ID")
    symbol: str = Field(..., description="Stock symbol")
    quantity: float = Field(..., gt=0, description="Number of shares")
    entry_price: float = Field(..., gt=0, description="Entry price")
    entry_reason: str = Field(..., description="Why entering this trade")
    setup_type: Optional[str] = Field(None, description="Pattern/setup (e.g., VCP, Cup & Handle)")
    screenshot_url: Optional[str] = Field(None, description="Chart screenshot URL")
    emotions: Optional[str] = Field(None, description="Emotional state")
    tags: Optional[List[str]] = Field(None, description="Tags for categorization")
    position_id: Optional[int] = Field(None, description="Associated position ID")


class LogExitRequest(BaseModel):
    portfolio_id: int = Field(..., description="Portfolio ID")
    symbol: str = Field(..., description="Stock symbol")
    quantity: float = Field(..., gt=0, description="Number of shares sold")
    exit_price: float = Field(..., gt=0, description="Exit price")
    entry_price: float = Field(..., gt=0, description="Original entry price")
    exit_reason: str = Field(..., description="Why exiting this trade")
    lessons_learned: Optional[str] = Field(None, description="Key lessons from this trade")
    mistakes_made: Optional[str] = Field(None, description="What went wrong")
    what_went_well: Optional[str] = Field(None, description="What went right")
    screenshot_url: Optional[str] = Field(None, description="Exit chart screenshot URL")
    emotions: Optional[str] = Field(None, description="Emotional state during exit")
    trade_grade: Optional[str] = Field(None, description="Trade grade (A+ to F)")
    tags: Optional[List[str]] = Field(None, description="Tags")
    position_id: Optional[int] = Field(None, description="Associated position ID")


class UpdateJournalRequest(BaseModel):
    lessons_learned: Optional[str] = None
    mistakes_made: Optional[str] = None
    what_went_well: Optional[str] = None
    trade_grade: Optional[str] = None
    emotions: Optional[str] = None
    tags: Optional[str] = None


@router.post("/entry", summary="Log a trade entry")
async def log_entry(
    request: LogEntryRequest,
    db: Session = Depends(get_db)
):
    """
    Log a trade entry with detailed notes

    Parameters:
    - **portfolio_id**: Portfolio ID
    - **symbol**: Stock symbol
    - **quantity**: Number of shares
    - **entry_price**: Entry price per share
    - **entry_reason**: Why you're entering this trade
    - **setup_type**: Pattern/setup type (optional)
    - **screenshot_url**: Chart screenshot URL (optional)
    - **emotions**: Emotional state (optional)
    - **tags**: Tags for categorization (optional)

    Returns the journal entry
    """
    service = TradeJournalService(db)

    try:
        entry = await service.log_entry(
            portfolio_id=request.portfolio_id,
            symbol=request.symbol,
            quantity=request.quantity,
            entry_price=request.entry_price,
            entry_reason=request.entry_reason,
            setup_type=request.setup_type,
            screenshot_url=request.screenshot_url,
            emotions=request.emotions,
            tags=request.tags,
            position_id=request.position_id
        )

        return {
            "success": True,
            "entry": {
                "id": entry.id,
                "symbol": request.symbol,
                "trade_type": entry.trade_type,
                "quantity": entry.quantity,
                "price": entry.price,
                "entry_reason": entry.entry_reason,
                "setup_type": entry.setup_type,
                "traded_at": entry.traded_at.isoformat() if entry.traded_at else None
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/exit", summary="Log a trade exit")
async def log_exit(
    request: LogExitRequest,
    db: Session = Depends(get_db)
):
    """
    Log a trade exit with reflection and lessons learned

    Parameters:
    - **portfolio_id**: Portfolio ID
    - **symbol**: Stock symbol
    - **quantity**: Number of shares sold
    - **exit_price**: Exit price
    - **entry_price**: Original entry price
    - **exit_reason**: Why exiting
    - **lessons_learned**: Key takeaways (optional)
    - **mistakes_made**: What went wrong (optional)
    - **what_went_well**: What went right (optional)
    - **screenshot_url**: Exit chart screenshot (optional)
    - **emotions**: Emotional state (optional)
    - **trade_grade**: Grade A+ to F (optional)
    - **tags**: Tags (optional)

    Returns the journal entry with P&L calculations
    """
    service = TradeJournalService(db)

    try:
        entry = await service.log_exit(
            portfolio_id=request.portfolio_id,
            symbol=request.symbol,
            quantity=request.quantity,
            exit_price=request.exit_price,
            entry_price=request.entry_price,
            exit_reason=request.exit_reason,
            lessons_learned=request.lessons_learned,
            mistakes_made=request.mistakes_made,
            what_went_well=request.what_went_well,
            screenshot_url=request.screenshot_url,
            emotions=request.emotions,
            trade_grade=request.trade_grade,
            tags=request.tags,
            position_id=request.position_id
        )

        return {
            "success": True,
            "exit": {
                "id": entry.id,
                "symbol": request.symbol,
                "trade_type": entry.trade_type,
                "quantity": entry.quantity,
                "exit_price": entry.price,
                "profit_loss": entry.profit_loss,
                "profit_loss_pct": entry.profit_loss_pct,
                "exit_reason": entry.exit_reason,
                "lessons_learned": entry.lessons_learned,
                "trade_grade": entry.trade_grade,
                "traded_at": entry.traded_at.isoformat() if entry.traded_at else None
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{journal_id}", summary="Update journal entry")
async def update_entry(
    journal_id: int,
    request: UpdateJournalRequest,
    db: Session = Depends(get_db)
):
    """
    Update an existing journal entry

    Useful for adding reflections after the trade

    Parameters:
    - **journal_id**: Journal entry ID
    - Fields to update (all optional)

    Returns updated journal entry
    """
    service = TradeJournalService(db)

    try:
        # Filter out None values
        updates = {k: v for k, v in request.dict().items() if v is not None}

        entry = await service.update_journal_entry(journal_id, **updates)

        return {
            "success": True,
            "message": "Journal entry updated",
            "entry_id": entry.id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{portfolio_id}/entries", summary="Get journal entries")
async def get_entries(
    portfolio_id: int,
    trade_type: Optional[str] = Query(None, description="Filter by trade type (entry/exit)"),
    symbol: Optional[str] = Query(None, description="Filter by symbol"),
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated)"),
    limit: int = Query(default=50, ge=1, le=200, description="Max entries to return"),
    db: Session = Depends(get_db)
):
    """
    Get journal entries with filters

    Parameters:
    - **portfolio_id**: Portfolio ID
    - **trade_type**: Filter by type (entry/exit) - optional
    - **symbol**: Filter by symbol - optional
    - **tags**: Filter by tags - optional
    - **limit**: Maximum entries (1-200)

    Returns list of journal entries
    """
    service = TradeJournalService(db)

    try:
        tags_list = tags.split(",") if tags else None

        entries = await service.get_journal_entries(
            portfolio_id=portfolio_id,
            trade_type=trade_type,
            symbol=symbol,
            tags=tags_list,
            limit=limit
        )

        return {
            "success": True,
            "entries": entries,
            "count": len(entries)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{portfolio_id}/statistics", summary="Get journal statistics")
async def get_statistics(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    """
    Get statistics from the trade journal

    Parameters:
    - **portfolio_id**: Portfolio ID

    Returns:
    - Trade statistics (win rate, avg P&L, etc.)
    - Setup type performance
    - Tag distribution
    - Grade distribution
    - Recent lessons learned
    """
    service = TradeJournalService(db)

    try:
        stats = await service.get_journal_statistics(portfolio_id)

        return {
            "success": True,
            "statistics": stats
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/entry/{journal_id}", summary="Get detailed trade review")
async def get_trade_review(
    journal_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed review of a specific trade

    Parameters:
    - **journal_id**: Journal entry ID

    Returns complete trade details with related entries
    """
    service = TradeJournalService(db)

    try:
        review = await service.get_trade_review(journal_id)

        return {
            "success": True,
            "trade_review": review
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{portfolio_id}/lessons", summary="Get all lessons learned")
async def get_lessons(
    portfolio_id: int,
    limit: int = Query(default=20, ge=1, le=100, description="Max lessons to return"),
    db: Session = Depends(get_db)
):
    """
    Get all lessons learned from trades

    Parameters:
    - **portfolio_id**: Portfolio ID
    - **limit**: Maximum lessons (1-100)

    Returns list of lessons from recent trades
    """
    service = TradeJournalService(db)

    try:
        stats = await service.get_journal_statistics(portfolio_id)
        lessons = stats.get("recent_lessons", [])[:limit]

        return {
            "success": True,
            "lessons": lessons,
            "count": len(lessons)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
