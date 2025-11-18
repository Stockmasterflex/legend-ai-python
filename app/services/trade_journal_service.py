"""
Trade Journal Service
Manages comprehensive trade journaling with notes, screenshots, and lessons learned
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
import logging

from app.models import TradeJournal, Portfolio, Position, Ticker

logger = logging.getLogger(__name__)


class TradeJournalService:
    """Service for trade journal management"""

    def __init__(self, db: Session):
        self.db = db

    async def log_entry(
        self,
        portfolio_id: int,
        symbol: str,
        quantity: float,
        entry_price: float,
        entry_reason: str,
        setup_type: Optional[str] = None,
        screenshot_url: Optional[str] = None,
        emotions: Optional[str] = None,
        tags: Optional[List[str]] = None,
        position_id: Optional[int] = None
    ) -> TradeJournal:
        """
        Log a trade entry

        Args:
            portfolio_id: Portfolio ID
            symbol: Stock symbol
            quantity: Number of shares
            entry_price: Entry price
            entry_reason: Why entering this trade
            setup_type: Pattern/setup used (e.g., "VCP", "Cup & Handle")
            screenshot_url: URL to chart screenshot
            emotions: Emotional state during entry
            tags: List of tags
            position_id: Associated position ID

        Returns:
            TradeJournal entry
        """
        # Get or create ticker
        ticker = self.db.query(Ticker).filter(Ticker.symbol == symbol).first()
        if not ticker:
            ticker = Ticker(symbol=symbol, name=symbol)
            self.db.add(ticker)
            self.db.commit()
            self.db.refresh(ticker)

        # Create journal entry
        tags_str = ",".join(tags) if tags else None

        journal_entry = TradeJournal(
            portfolio_id=portfolio_id,
            position_id=position_id,
            ticker_id=ticker.id,
            trade_type="entry",
            quantity=quantity,
            price=entry_price,
            entry_reason=entry_reason,
            setup_type=setup_type,
            screenshot_url=screenshot_url,
            emotions=emotions,
            tags=tags_str,
            traded_at=datetime.utcnow()
        )

        self.db.add(journal_entry)
        self.db.commit()
        self.db.refresh(journal_entry)

        logger.info(f"Logged entry for {symbol} in portfolio {portfolio_id}")
        return journal_entry

    async def log_exit(
        self,
        portfolio_id: int,
        symbol: str,
        quantity: float,
        exit_price: float,
        entry_price: float,
        exit_reason: str,
        lessons_learned: Optional[str] = None,
        mistakes_made: Optional[str] = None,
        what_went_well: Optional[str] = None,
        screenshot_url: Optional[str] = None,
        emotions: Optional[str] = None,
        trade_grade: Optional[str] = None,
        tags: Optional[List[str]] = None,
        position_id: Optional[int] = None
    ) -> TradeJournal:
        """
        Log a trade exit with reflection

        Args:
            portfolio_id: Portfolio ID
            symbol: Stock symbol
            quantity: Number of shares sold
            exit_price: Exit price
            entry_price: Original entry price (for P&L calculation)
            exit_reason: Why exiting this trade
            lessons_learned: Key lessons from this trade
            mistakes_made: What went wrong
            what_went_well: What went right
            screenshot_url: URL to exit chart screenshot
            emotions: Emotional state during exit
            trade_grade: Grade for this trade (A+ to F)
            tags: List of tags (e.g., ["win", "breakout"])
            position_id: Associated position ID

        Returns:
            TradeJournal entry
        """
        # Get ticker
        ticker = self.db.query(Ticker).filter(Ticker.symbol == symbol).first()
        if not ticker:
            ticker = Ticker(symbol=symbol, name=symbol)
            self.db.add(ticker)
            self.db.commit()
            self.db.refresh(ticker)

        # Calculate P&L
        profit_loss = (exit_price - entry_price) * quantity
        profit_loss_pct = ((exit_price - entry_price) / entry_price) * 100 if entry_price > 0 else 0

        # Auto-add win/loss tags
        auto_tags = tags or []
        if profit_loss > 0:
            auto_tags.append("win")
        else:
            auto_tags.append("loss")

        tags_str = ",".join(auto_tags) if auto_tags else None

        # Create journal entry
        journal_entry = TradeJournal(
            portfolio_id=portfolio_id,
            position_id=position_id,
            ticker_id=ticker.id,
            trade_type="exit",
            quantity=quantity,
            price=exit_price,
            exit_reason=exit_reason,
            lessons_learned=lessons_learned,
            mistakes_made=mistakes_made,
            what_went_well=what_went_well,
            screenshot_url=screenshot_url,
            emotions=emotions,
            trade_grade=trade_grade,
            profit_loss=profit_loss,
            profit_loss_pct=profit_loss_pct,
            tags=tags_str,
            traded_at=datetime.utcnow()
        )

        self.db.add(journal_entry)
        self.db.commit()
        self.db.refresh(journal_entry)

        logger.info(f"Logged exit for {symbol} in portfolio {portfolio_id}, P&L: ${profit_loss:.2f}")
        return journal_entry

    async def update_journal_entry(
        self,
        journal_id: int,
        **kwargs
    ) -> TradeJournal:
        """
        Update an existing journal entry

        Args:
            journal_id: Journal entry ID
            **kwargs: Fields to update

        Returns:
            Updated journal entry
        """
        entry = self.db.query(TradeJournal).filter(TradeJournal.id == journal_id).first()
        if not entry:
            raise ValueError(f"Journal entry {journal_id} not found")

        # Update fields
        for key, value in kwargs.items():
            if hasattr(entry, key):
                setattr(entry, key, value)

        entry.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(entry)

        return entry

    async def get_journal_entries(
        self,
        portfolio_id: int,
        trade_type: Optional[str] = None,
        symbol: Optional[str] = None,
        tags: Optional[List[str]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 50
    ) -> List[Dict]:
        """
        Get journal entries with filters

        Args:
            portfolio_id: Portfolio ID
            trade_type: Filter by trade type ("entry", "exit")
            symbol: Filter by symbol
            tags: Filter by tags
            start_date: Start date for filtering
            end_date: End date for filtering
            limit: Maximum number of entries

        Returns:
            List of journal entries with ticker info
        """
        query = self.db.query(TradeJournal).filter(TradeJournal.portfolio_id == portfolio_id)

        if trade_type:
            query = query.filter(TradeJournal.trade_type == trade_type)

        if symbol:
            ticker = self.db.query(Ticker).filter(Ticker.symbol == symbol).first()
            if ticker:
                query = query.filter(TradeJournal.ticker_id == ticker.id)

        if start_date:
            query = query.filter(TradeJournal.traded_at >= start_date)

        if end_date:
            query = query.filter(TradeJournal.traded_at <= end_date)

        # Filter by tags if provided
        if tags:
            for tag in tags:
                query = query.filter(TradeJournal.tags.like(f"%{tag}%"))

        query = query.order_by(desc(TradeJournal.traded_at)).limit(limit)
        entries = query.all()

        # Format response with ticker info
        result = []
        for entry in entries:
            ticker = self.db.query(Ticker).filter(Ticker.id == entry.ticker_id).first()
            entry_dict = {
                "id": entry.id,
                "symbol": ticker.symbol if ticker else "Unknown",
                "trade_type": entry.trade_type,
                "quantity": entry.quantity,
                "price": entry.price,
                "entry_reason": entry.entry_reason,
                "exit_reason": entry.exit_reason,
                "setup_type": entry.setup_type,
                "screenshot_url": entry.screenshot_url,
                "lessons_learned": entry.lessons_learned,
                "emotions": entry.emotions,
                "tags": entry.tags.split(",") if entry.tags else [],
                "r_multiple": entry.r_multiple,
                "profit_loss": entry.profit_loss,
                "profit_loss_pct": entry.profit_loss_pct,
                "trade_grade": entry.trade_grade,
                "mistakes_made": entry.mistakes_made,
                "what_went_well": entry.what_went_well,
                "traded_at": entry.traded_at.isoformat() if entry.traded_at else None
            }
            result.append(entry_dict)

        return result

    async def get_journal_statistics(self, portfolio_id: int) -> Dict:
        """
        Get statistics from the trade journal

        Returns:
            Statistics about trades, lessons, and patterns
        """
        entries = self.db.query(TradeJournal).filter(
            TradeJournal.portfolio_id == portfolio_id
        ).all()

        exits = [e for e in entries if e.trade_type == "exit"]
        wins = [e for e in exits if e.profit_loss and e.profit_loss > 0]
        losses = [e for e in exits if e.profit_loss and e.profit_loss < 0]

        # Calculate statistics
        total_trades = len(exits)
        win_rate = (len(wins) / total_trades * 100) if total_trades > 0 else 0

        total_profit = sum([e.profit_loss for e in wins]) if wins else 0
        total_loss = sum([e.profit_loss for e in losses]) if losses else 0
        net_pnl = total_profit + total_loss

        avg_win = total_profit / len(wins) if wins else 0
        avg_loss = total_loss / len(losses) if losses else 0

        # Count by setup type
        setup_counts = {}
        for entry in entries:
            if entry.setup_type and entry.trade_type == "entry":
                setup_counts[entry.setup_type] = setup_counts.get(entry.setup_type, 0) + 1

        # Most common tags
        tag_counts = {}
        for entry in entries:
            if entry.tags:
                for tag in entry.tags.split(","):
                    tag = tag.strip()
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # Grade distribution
        grade_counts = {}
        for entry in exits:
            if entry.trade_grade:
                grade_counts[entry.trade_grade] = grade_counts.get(entry.trade_grade, 0) + 1

        # Recent lessons (last 10)
        recent_lessons = []
        for entry in sorted(exits, key=lambda x: x.traded_at, reverse=True)[:10]:
            if entry.lessons_learned:
                ticker = self.db.query(Ticker).filter(Ticker.id == entry.ticker_id).first()
                recent_lessons.append({
                    "symbol": ticker.symbol if ticker else "Unknown",
                    "date": entry.traded_at.strftime("%Y-%m-%d") if entry.traded_at else None,
                    "lesson": entry.lessons_learned
                })

        return {
            "total_trades": total_trades,
            "wins": len(wins),
            "losses": len(losses),
            "win_rate_pct": round(win_rate, 2),
            "net_pnl": round(net_pnl, 2),
            "avg_win": round(avg_win, 2),
            "avg_loss": round(avg_loss, 2),
            "total_profit": round(total_profit, 2),
            "total_loss": round(total_loss, 2),
            "setup_type_counts": setup_counts,
            "tag_counts": tag_counts,
            "grade_distribution": grade_counts,
            "recent_lessons": recent_lessons
        }

    async def get_trade_review(self, journal_id: int) -> Dict:
        """
        Get detailed review of a specific trade

        Args:
            journal_id: Journal entry ID

        Returns:
            Comprehensive trade review
        """
        entry = self.db.query(TradeJournal).filter(TradeJournal.id == journal_id).first()
        if not entry:
            raise ValueError(f"Journal entry {journal_id} not found")

        ticker = self.db.query(Ticker).filter(Ticker.id == entry.ticker_id).first()

        # Find related entries (same position)
        related_entries = []
        if entry.position_id:
            related = self.db.query(TradeJournal).filter(
                TradeJournal.position_id == entry.position_id,
                TradeJournal.id != entry.id
            ).all()

            for rel in related:
                related_entries.append({
                    "id": rel.id,
                    "trade_type": rel.trade_type,
                    "quantity": rel.quantity,
                    "price": rel.price,
                    "traded_at": rel.traded_at.isoformat() if rel.traded_at else None
                })

        return {
            "id": entry.id,
            "symbol": ticker.symbol if ticker else "Unknown",
            "trade_type": entry.trade_type,
            "quantity": entry.quantity,
            "price": entry.price,
            "entry_reason": entry.entry_reason,
            "exit_reason": entry.exit_reason,
            "setup_type": entry.setup_type,
            "screenshot_url": entry.screenshot_url,
            "lessons_learned": entry.lessons_learned,
            "emotions": entry.emotions,
            "tags": entry.tags.split(",") if entry.tags else [],
            "r_multiple": entry.r_multiple,
            "profit_loss": entry.profit_loss,
            "profit_loss_pct": entry.profit_loss_pct,
            "trade_grade": entry.trade_grade,
            "mistakes_made": entry.mistakes_made,
            "what_went_well": entry.what_went_well,
            "traded_at": entry.traded_at.isoformat() if entry.traded_at else None,
            "related_entries": related_entries
        }
