"""
Database service for Legend AI
Phase 1.5: Database Integration
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Optional, List, Dict, Any
import logging

from app.config import get_settings
from app.models import Base, Ticker, PatternScan, Watchlist, ScanLog

logger = logging.getLogger(__name__)

class DatabaseService:
    """Database service for Legend AI operations"""

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = None
        self.SessionLocal = None

    def init_db(self):
        """Initialize database connection and create tables"""
        try:
            # Create engine with proper configuration
            connect_args = {}
            if self.database_url.startswith("sqlite"):
                connect_args["check_same_thread"] = False
                self.engine = create_engine(
                    self.database_url,
                    connect_args=connect_args,
                    poolclass=StaticPool
                )
            else:
                self.engine = create_engine(self.database_url)

            # Create session factory
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

            # Create tables
            Base.metadata.create_all(bind=self.engine)

            logger.info("Database initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    def get_db(self) -> Session:
        """Get database session"""
        if not self.SessionLocal:
            raise RuntimeError("Database not initialized. Call init_db() first.")
        return self.SessionLocal()

    def close_db(self):
        """Close database connections"""
        if self.engine:
            self.engine.dispose()

    def health_check(self) -> Dict[str, Any]:
        """Check database health"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                return {"status": "healthy", "connection": True}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    # Ticker operations
    def get_or_create_ticker(self, symbol: str, name: str = None) -> Ticker:
        """Get or create ticker record"""
        with self.get_db() as db:
            ticker = db.query(Ticker).filter(Ticker.symbol == symbol.upper()).first()
            if not ticker:
                ticker = Ticker(symbol=symbol.upper(), name=name)
                db.add(ticker)
                db.commit()
                db.refresh(ticker)
            return ticker

    def get_tickers(self, limit: int = 100) -> List[Ticker]:
        """Get list of tickers"""
        with self.get_db() as db:
            return db.query(Ticker).limit(limit).all()

    # Pattern operations
    def save_pattern_scan(self, ticker_symbol: str, pattern_data: Dict[str, Any]) -> PatternScan:
        """Save pattern scan result"""
        with self.get_db() as db:
            ticker = self.get_or_create_ticker(ticker_symbol, pattern_data.get("name"))

            scan = PatternScan(
                ticker_id=ticker.id,
                pattern_type=pattern_data.get("pattern", "UNKNOWN"),
                score=pattern_data.get("score", 0),
                entry_price=pattern_data.get("entry"),
                stop_price=pattern_data.get("stop"),
                target_price=pattern_data.get("target"),
                risk_reward_ratio=pattern_data.get("risk_reward"),
                criteria_met=str(pattern_data.get("criteria_met", [])),
                analysis=pattern_data.get("analysis", ""),
                current_price=pattern_data.get("current_price"),
                volume_dry_up=pattern_data.get("volume_dry_up", False),
                consolidation_days=pattern_data.get("consolidation_days")
            )

            db.add(scan)
            db.commit()
            db.refresh(scan)
            return scan

    def get_recent_scans(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent pattern scans with ticker info"""
        with self.get_db() as db:
            results = db.query(
                PatternScan, Ticker.symbol
            ).join(Ticker).order_by(
                PatternScan.scanned_at.desc()
            ).limit(limit).all()

            return [{
                "id": scan.id,
                "ticker": symbol,
                "pattern": scan.pattern_type,
                "score": scan.score,
                "entry": scan.entry_price,
                "stop": scan.stop_price,
                "target": scan.target_price,
                "scanned_at": scan.scanned_at.isoformat()
            } for scan, symbol in results]

    # Watchlist operations
    def add_to_watchlist(self, user_id: str, ticker_symbol: str, notes: str = None) -> Watchlist:
        """Add ticker to user watchlist"""
        with self.get_db() as db:
            ticker = self.get_or_create_ticker(ticker_symbol)

            # Check if already exists
            existing = db.query(Watchlist).filter(
                Watchlist.user_id == user_id,
                Watchlist.ticker_id == ticker.id
            ).first()

            if existing:
                if notes:
                    existing.notes = notes
                db.commit()
                return existing

            watchlist_item = Watchlist(
                user_id=user_id,
                ticker_id=ticker.id,
                notes=notes
            )

            db.add(watchlist_item)
            db.commit()
            db.refresh(watchlist_item)
            return watchlist_item

    def get_watchlist(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user watchlist"""
        with self.get_db() as db:
            results = db.query(
                Watchlist, Ticker.symbol, Ticker.name
            ).join(Ticker).filter(
                Watchlist.user_id == user_id
            ).all()

            return [{
                "id": item.id,
                "ticker": symbol,
                "name": name,
                "added_at": item.added_at.isoformat(),
                "notes": item.notes
            } for item, symbol, name in results]

    # Scan logging
    def log_scan(self, scan_type: str, tickers_scanned: int, patterns_found: int,
                 status: str = "completed", error_message: str = None) -> ScanLog:
        """Log a scanning operation"""
        with self.get_db() as db:
            scan_log = ScanLog(
                scan_type=scan_type,
                tickers_scanned=tickers_scanned,
                patterns_found=patterns_found,
                status=status,
                error_message=error_message
            )

            db.add(scan_log)
            db.commit()
            db.refresh(scan_log)
            return scan_log

# Global database service instance
_db_service: Optional[DatabaseService] = None

def get_database_service() -> DatabaseService:
    """Get global database service instance"""
    global _db_service
    if _db_service is None:
        settings = get_settings()
        _db_service = DatabaseService(settings.database_url)
        _db_service.init_db()
    return _db_service
