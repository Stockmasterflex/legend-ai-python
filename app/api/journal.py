"""
Trade journal API - Log and analyze trades
"""
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
import csv
from io import StringIO
from fastapi.responses import StreamingResponse

from app.services.database import get_database_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/journal", tags=["journal"])

class TradeCreate(BaseModel):
    ticker: str
    pattern: Optional[str] = None
    entry_date: date
    entry_price: float
    stop_price: float
    target_price: Optional[float] = None
    shares: int
    notes: Optional[str] = None
    
    @field_validator("ticker")
    @classmethod
    def uppercase_ticker(cls, v: str) -> str:
        return v.upper().strip()

class TradeUpdate(BaseModel):
    exit_date: Optional[date] = None
    exit_price: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class TradeResponse(BaseModel):
    id: int
    ticker: str
    pattern: Optional[str]
    entry_date: str
    entry_price: float
    stop_price: float
    target_price: Optional[float]
    exit_date: Optional[str]
    exit_price: Optional[float]
    shares: int
    profit_loss: Optional[float]
    r_multiple: Optional[float]
    status: str
    notes: Optional[str]
    created_at: str

class JournalStats(BaseModel):
    total_trades: int
    open_trades: int
    closed_trades: int
    win_rate: float
    avg_r_multiple: float
    total_profit_loss: float
    largest_win: float
    largest_loss: float
    avg_win: float
    avg_loss: float
    expectancy: float
    profit_factor: float

@router.post("/trade", response_model=Dict[str, Any])
async def log_trade(trade: TradeCreate):
    """Log a new trade to the journal"""
    try:
        db = get_database_service()
        
        # Insert trade into database
        from sqlalchemy import text
        with db.engine.begin() as conn:
            result = conn.execute(
                text("""
                    INSERT INTO trades (
                        ticker, pattern, entry_date, entry_price, stop_price,
                        target_price, shares, notes, status, created_at
                    )
                    VALUES (
                        :ticker, :pattern, :entry_date, :entry_price, :stop_price,
                        :target_price, :shares, :notes, 'Open', NOW()
                    )
                    RETURNING id
                """),
                {
                    "ticker": trade.ticker,
                    "pattern": trade.pattern,
                    "entry_date": trade.entry_date,
                    "entry_price": trade.entry_price,
                    "stop_price": trade.stop_price,
                    "target_price": trade.target_price,
                    "shares": trade.shares,
                    "notes": trade.notes
                }
            )
            trade_id = result.fetchone()[0]
        
        logger.info(f"Trade logged: {trade.ticker} @ ${trade.entry_price} x {trade.shares} shares")
        
        return {
            "success": True,
            "trade_id": trade_id,
            "message": f"Trade {trade.ticker} logged successfully"
        }
    
    except Exception as e:
        logger.error(f"Failed to log trade: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to log trade: {str(e)}")

@router.get("/trades", response_model=List[TradeResponse])
async def get_trades(
    status: Optional[str] = None,
    ticker: Optional[str] = None,
    limit: int = 100
):
    """Get all trades with optional filters"""
    try:
        db = get_database_service()
        
        from sqlalchemy import text
        
        # Build query with filters
        query = """
            SELECT 
                id, ticker, pattern, entry_date, entry_price, stop_price,
                target_price, exit_date, exit_price, shares, profit_loss,
                r_multiple, status, notes, created_at
            FROM trades
            WHERE 1=1
        """
        
        params = {"limit": limit}
        
        if status:
            query += " AND status = :status"
            params["status"] = status
        
        if ticker:
            query += " AND ticker = :ticker"
            params["ticker"] = ticker.upper()
        
        query += " ORDER BY entry_date DESC LIMIT :limit"
        
        with db.engine.connect() as conn:
            result = conn.execute(text(query), params)
            rows = result.fetchall()
        
        trades = []
        for row in rows:
            trades.append(TradeResponse(
                id=row[0],
                ticker=row[1],
                pattern=row[2],
                entry_date=str(row[3]) if row[3] else None,
                entry_price=row[4],
                stop_price=row[5],
                target_price=row[6],
                exit_date=str(row[7]) if row[7] else None,
                exit_price=row[8],
                shares=row[9],
                profit_loss=row[10],
                r_multiple=row[11],
                status=row[12],
                notes=row[13],
                created_at=str(row[14]) if row[14] else None
            ))
        
        return trades
    
    except Exception as e:
        logger.error(f"Failed to fetch trades: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch trades: {str(e)}")

@router.put("/trade/{trade_id}")
async def update_trade(trade_id: int, update: TradeUpdate):
    """Update a trade (usually to close it)"""
    try:
        db = get_database_service()
        
        from sqlalchemy import text
        
        # Fetch current trade
        with db.engine.connect() as conn:
            result = conn.execute(
                text("SELECT entry_price, stop_price, shares FROM trades WHERE id = :id"),
                {"id": trade_id}
            )
            row = result.fetchone()
            
            if not row:
                raise HTTPException(status_code=404, detail="Trade not found")
            
            entry_price, stop_price, shares = row[0], row[1], row[2]
        
        # Calculate P&L and R-multiple if closing
        profit_loss = None
        r_multiple = None
        
        if update.exit_price is not None:
            profit_loss = (update.exit_price - entry_price) * shares
            risk_per_share = abs(entry_price - stop_price)
            profit_per_share = update.exit_price - entry_price
            r_multiple = profit_per_share / risk_per_share if risk_per_share > 0 else 0
        
        # Build update query
        set_clauses = []
        params = {"id": trade_id}
        
        if update.exit_date is not None:
            set_clauses.append("exit_date = :exit_date")
            params["exit_date"] = update.exit_date
        
        if update.exit_price is not None:
            set_clauses.append("exit_price = :exit_price")
            set_clauses.append("profit_loss = :profit_loss")
            set_clauses.append("r_multiple = :r_multiple")
            params["exit_price"] = update.exit_price
            params["profit_loss"] = profit_loss
            params["r_multiple"] = r_multiple
        
        if update.status is not None:
            set_clauses.append("status = :status")
            params["status"] = update.status
        
        if update.notes is not None:
            set_clauses.append("notes = :notes")
            params["notes"] = update.notes
        
        if not set_clauses:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        query = f"UPDATE trades SET {', '.join(set_clauses)} WHERE id = :id"
        
        with db.engine.begin() as conn:
            conn.execute(text(query), params)
        
        logger.info(f"Trade {trade_id} updated")
        
        return {
            "success": True,
            "trade_id": trade_id,
            "profit_loss": round(profit_loss, 2) if profit_loss else None,
            "r_multiple": round(r_multiple, 2) if r_multiple else None
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update trade: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update trade: {str(e)}")

@router.get("/stats", response_model=JournalStats)
async def get_stats():
    """Calculate trade journal statistics"""
    try:
        db = get_database_service()
        
        from sqlalchemy import text
        
        with db.engine.connect() as conn:
            # Get all closed trades
            result = conn.execute(
                text("""
                    SELECT 
                        COUNT(*) as total,
                        COUNT(CASE WHEN status = 'Open' THEN 1 END) as open_count,
                        COUNT(CASE WHEN status != 'Open' THEN 1 END) as closed_count,
                        COUNT(CASE WHEN profit_loss > 0 THEN 1 END) as wins,
                        AVG(CASE WHEN profit_loss IS NOT NULL THEN r_multiple END) as avg_r,
                        SUM(CASE WHEN profit_loss IS NOT NULL THEN profit_loss ELSE 0 END) as total_pl,
                        MAX(CASE WHEN profit_loss > 0 THEN profit_loss END) as max_win,
                        MIN(CASE WHEN profit_loss < 0 THEN profit_loss END) as max_loss,
                        AVG(CASE WHEN profit_loss > 0 THEN profit_loss END) as avg_win,
                        AVG(CASE WHEN profit_loss < 0 THEN profit_loss END) as avg_loss,
                        SUM(CASE WHEN profit_loss > 0 THEN profit_loss ELSE 0 END) as total_wins,
                        SUM(CASE WHEN profit_loss < 0 THEN ABS(profit_loss) ELSE 0 END) as total_losses
                    FROM trades
                """)
            )
            row = result.fetchone()
        
        total_trades = row[0] or 0
        open_trades = row[1] or 0
        closed_trades = row[2] or 0
        wins = row[3] or 0
        avg_r = row[4] or 0.0
        total_pl = row[5] or 0.0
        max_win = row[6] or 0.0
        max_loss = row[7] or 0.0
        avg_win = row[8] or 0.0
        avg_loss = row[9] or 0.0
        total_wins = row[10] or 0.0
        total_losses = row[11] or 0.0
        
        # Calculate metrics
        win_rate = (wins / closed_trades * 100) if closed_trades > 0 else 0.0
        
        # Expectancy = (Win% * Avg Win) - (Loss% * Avg Loss)
        loss_rate = 100 - win_rate if closed_trades > 0 else 0.0
        expectancy = (win_rate / 100 * avg_win) - (loss_rate / 100 * abs(avg_loss)) if closed_trades > 0 else 0.0
        
        # Profit Factor = Gross Wins / Gross Losses
        profit_factor = total_wins / total_losses if total_losses > 0 else 0.0
        
        return JournalStats(
            total_trades=total_trades,
            open_trades=open_trades,
            closed_trades=closed_trades,
            win_rate=round(win_rate, 2),
            avg_r_multiple=round(avg_r, 2),
            total_profit_loss=round(total_pl, 2),
            largest_win=round(max_win, 2),
            largest_loss=round(max_loss, 2),
            avg_win=round(avg_win, 2),
            avg_loss=round(avg_loss, 2),
            expectancy=round(expectancy, 2),
            profit_factor=round(profit_factor, 2)
        )
    
    except Exception as e:
        logger.error(f"Failed to calculate stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to calculate stats: {str(e)}")

@router.get("/export")
async def export_trades():
    """Export trades to CSV"""
    try:
        db = get_database_service()
        
        from sqlalchemy import text
        
        with db.engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT 
                        ticker, pattern, entry_date, entry_price, stop_price,
                        target_price, exit_date, exit_price, shares, profit_loss,
                        r_multiple, status, notes
                    FROM trades
                    ORDER BY entry_date DESC
                """)
            )
            rows = result.fetchall()
        
        # Create CSV
        output = StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            "Ticker", "Pattern", "Entry Date", "Entry Price", "Stop Price",
            "Target Price", "Exit Date", "Exit Price", "Shares", "P&L",
            "R Multiple", "Status", "Notes"
        ])
        
        # Data
        for row in rows:
            writer.writerow(row)
        
        output.seek(0)
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=trades_{datetime.now().strftime('%Y%m%d')}.csv"
            }
        )
    
    except Exception as e:
        logger.error(f"Failed to export trades: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to export trades: {str(e)}")

