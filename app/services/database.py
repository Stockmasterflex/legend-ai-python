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

    # -------------------- Watchlist (Raw SQL hotfix) --------------------
    def ensure_watchlist_table(self):
        try:
            if not self.engine:
                return
            dialect_name = getattr(self.engine, "dialect", None)
            dialect_name = getattr(dialect_name, "name", "")
            with self.engine.begin() as conn:
                if dialect_name == "postgresql":
                    conn.execute(text(
                        """
                        create table if not exists watchlist (
                          id serial primary key,
                          user_id text not null default 'default',
                          symbol text not null,
                          reason text,
                          tags text,
                          status text default 'Watching',
                          created_at timestamptz default now()
                        );
                        """
                    ))
                    conn.execute(text("alter table watchlist add column if not exists user_id text"))
                    conn.execute(text("alter table watchlist alter column user_id set default 'default'"))
                    conn.execute(text("update watchlist set user_id = 'default' where user_id is null"))
                    conn.execute(text("alter table watchlist alter column user_id set not null"))
                    conn.execute(text("alter table watchlist add column if not exists tags text"))
                    conn.execute(text("alter table watchlist add column if not exists status text default 'Watching'"))
                    conn.execute(text(
                        """
                        do $$ begin
                          if exists (select 1 from pg_constraint where conname = 'watchlist_symbol_key') then
                            alter table watchlist drop constraint watchlist_symbol_key;
                          end if;
                        end $$;
                        """
                    ))
                    conn.execute(text("create unique index if not exists watchlist_user_symbol_idx on watchlist (user_id, symbol)"))
                elif dialect_name == "sqlite":
                    conn.execute(text(
                        """
                        create table if not exists watchlist (
                          id integer primary key autoincrement,
                          user_id text default 'default',
                          symbol text not null,
                          reason text,
                          tags text,
                          status text default 'Watching',
                          created_at timestamp default CURRENT_TIMESTAMP
                        );
                        """
                    ))
                    columns = set()
                    try:
                        rows = conn.execute(text("pragma table_info('watchlist')"))
                        columns = {row[1] for row in rows}
                    except Exception:
                        columns = set()
                    if "user_id" not in columns:
                        conn.execute(text("alter table watchlist add column user_id text"))
                    conn.execute(text("update watchlist set user_id = 'default' where user_id is null"))
                    if "tags" not in columns:
                        conn.execute(text("alter table watchlist add column tags text"))
                    if "status" not in columns:
                        conn.execute(text("alter table watchlist add column status text default 'Watching'"))
                    conn.execute(text("create unique index if not exists watchlist_user_symbol_idx on watchlist (user_id, symbol)"))
                else:
                    conn.execute(text(
                        """
                        create table if not exists watchlist (
                          id integer primary key auto_increment,
                          user_id varchar(255) default 'default',
                          symbol varchar(32) not null,
                          reason text,
                          tags text,
                          status varchar(32) default 'Watching',
                          created_at timestamp default CURRENT_TIMESTAMP
                        );
                        """
                    ))
                    conn.execute(text("create unique index if not exists watchlist_user_symbol_idx on watchlist (user_id, symbol)"))
        except Exception as e:
            logger.warning(f"Could not ensure watchlist table: {e}")

    def get_watchlist_items(self, user_id: str = "default") -> List[Dict[str, Any]]:
        """Return watchlist items from Postgres. Never raise; returns []."""
        try:
            if not self.engine:
                return []
            self.ensure_watchlist_table()
            with self.engine.begin() as conn:
                rows = conn.execute(
                    text(
                        "select id, symbol, reason, tags, status, created_at from watchlist where user_id = :u order by created_at desc"
                    ),
                    {"u": user_id},
                )
                results = []
                for r in rows:
                    added = r[5]
                    if added is not None and hasattr(added, "isoformat"):
                        added_value = added.isoformat()
                    else:
                        added_value = str(added) if added is not None else None
                    results.append(
                        {
                            "id": r[0],
                            "ticker": r[1],
                            "reason": r[2],
                            "tags": r[3],
                            "status": r[4],
                            "added_at": added_value,
                        }
                    )
                return results
        except Exception as e:
            logger.warning(f"get_watchlist_items fallback: {e}")
            return []

    def add_watchlist_symbol(
        self,
        symbol: str,
        reason: str = None,
        tags: str = None,
        status: str = "Watching",
        user_id: str = "default",
    ) -> bool:
        try:
            if not self.engine:
                return False
            self.ensure_watchlist_table()
            with self.engine.begin() as conn:
                conn.execute(
                    text(
                        """
                        insert into watchlist (user_id, symbol, reason, tags, status)
                        values (:u, :s, :r, :t, :st)
                        on conflict (user_id, symbol)
                        do update set reason = excluded.reason, tags = excluded.tags, status = excluded.status
                        """
                    ),
                    {"u": user_id, "s": symbol.upper(), "r": reason, "t": tags, "st": status},
                )
            return True
        except Exception as e:
            logger.warning(f"add_watchlist_symbol failed: {e}")
            return False

    def remove_watchlist_symbol(self, symbol: str, user_id: str = "default") -> bool:
        try:
            if not self.engine:
                return False
            self.ensure_watchlist_table()
            with self.engine.begin() as conn:
                result = conn.execute(
                    text("delete from watchlist where user_id = :u and symbol = :s"),
                    {"u": user_id, "s": symbol.upper()},
                )
                return result.rowcount > 0
        except Exception as e:
            logger.warning(f"remove_watchlist_symbol failed: {e}")
            return False

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
