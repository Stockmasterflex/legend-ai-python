"""
Database service for Legend AI
Phase 1.5: Database Integration
"""

from sqlalchemy import create_engine, text, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool, QueuePool
from typing import Optional, List, Dict, Any, Callable
import logging
import os
import hashlib
import json
from functools import wraps

from app.config import get_settings
from app.models import Base, Ticker, PatternScan, Watchlist, ScanLog

logger = logging.getLogger(__name__)

def cache_query(ttl: int = 300, key_prefix: str = "db"):
    """Decorator to cache database query results in Redis"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(self, *args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key_parts = [key_prefix, func.__name__]

            # Add args and kwargs to cache key
            if args:
                cache_key_parts.append(hashlib.md5(str(args).encode()).hexdigest()[:8])
            if kwargs:
                cache_key_parts.append(hashlib.md5(str(sorted(kwargs.items())).encode()).hexdigest()[:8])

            cache_key = ":".join(cache_key_parts)

            # Try to get from cache
            try:
                from app.services.cache import get_cache_service
                cache = get_cache_service()
                cached_result = await cache.get(cache_key)
                if cached_result is not None:
                    logger.debug(f"Cache hit for {cache_key}")
                    return cached_result
            except Exception as e:
                logger.debug(f"Cache get failed: {e}")

            # Execute function and cache result
            result = func(self, *args, **kwargs)

            try:
                from app.services.cache import get_cache_service
                cache = get_cache_service()
                await cache.set(cache_key, result, ttl=ttl)
                logger.debug(f"Cached result for {cache_key} (ttl={ttl}s)")
            except Exception as e:
                logger.debug(f"Cache set failed: {e}")

            return result

        @wraps(func)
        def sync_wrapper(self, *args, **kwargs):
            # For sync functions, just execute without caching
            # In production, you'd want to handle this differently
            return func(self, *args, **kwargs)

        # Return async wrapper if function is async, else sync wrapper
        import inspect
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator

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
            engine_kwargs = {
                "echo": False,  # Set to True for SQL logging in development
                "future": True,  # Use SQLAlchemy 2.0 style
            }

            if not self.database_url:
                logger.warning("DATABASE_URL not set. Falling back to local SQLite database.")
                self.database_url = "sqlite:///./legend_ai.db"

            if self.database_url.startswith("sqlite"):
                connect_args["check_same_thread"] = False
                engine_kwargs["connect_args"] = connect_args
                engine_kwargs["poolclass"] = StaticPool
                self.engine = create_engine(self.database_url, **engine_kwargs)
            else:
                # PostgreSQL connection pooling configuration
                # Optimized for Railway deployment with limited connections
                pool_size = int(os.getenv("DB_POOL_SIZE", "5"))  # Reduced from default 5 for Railway
                max_overflow = int(os.getenv("DB_MAX_OVERFLOW", "10"))  # Max additional connections
                pool_timeout = int(os.getenv("DB_POOL_TIMEOUT", "30"))  # Seconds to wait for connection
                pool_recycle = int(os.getenv("DB_POOL_RECYCLE", "3600"))  # Recycle connections after 1 hour
                pool_pre_ping = os.getenv("DB_POOL_PRE_PING", "true").lower() == "true"  # Test connections before use

                engine_kwargs.update({
                    "poolclass": QueuePool,
                    "pool_size": pool_size,
                    "max_overflow": max_overflow,
                    "pool_timeout": pool_timeout,
                    "pool_recycle": pool_recycle,
                    "pool_pre_ping": pool_pre_ping,  # Verify connections are alive
                    "connect_args": {
                        "connect_timeout": 10,  # Connection timeout in seconds
                        "options": "-c statement_timeout=30000"  # 30 second query timeout
                    }
                })

                self.engine = create_engine(self.database_url, **engine_kwargs)

                # Log connection pool events in debug mode
                if os.getenv("DEBUG", "").lower() == "true":
                    @event.listens_for(self.engine, "connect")
                    def receive_connect(dbapi_conn, connection_record):
                        logger.debug("Database connection established")

                    @event.listens_for(self.engine, "checkout")
                    def receive_checkout(dbapi_conn, connection_record, connection_proxy):
                        logger.debug("Connection checked out from pool")

            # Create session factory with optimized settings
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
                expire_on_commit=False  # Don't expire objects after commit for better performance
            )

            # Create tables
            Base.metadata.create_all(bind=self.engine)

            logger.info(f"Database initialized successfully (pool_size={engine_kwargs.get('pool_size', 'N/A')})")

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
                pool_status = self.get_pool_status()
                return {
                    "status": "healthy",
                    "connection": True,
                    "pool": pool_status
                }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}

    def get_pool_status(self) -> Dict[str, Any]:
        """Get connection pool statistics"""
        if not self.engine or not hasattr(self.engine.pool, 'size'):
            return {"status": "not_available"}

        pool = self.engine.pool
        return {
            "size": pool.size(),
            "checked_in": pool.checkedin(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow(),
            "total_connections": pool.size() + pool.overflow()
        }

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

    def save_pattern_scans_batch(self, scans_data: List[Dict[str, Any]]) -> int:
        """Save multiple pattern scans in a single transaction (optimized bulk insert)"""
        if not scans_data:
            return 0

        try:
            with self.get_db() as db:
                # Pre-fetch all tickers to avoid N+1 queries
                symbols = {scan.get("ticker_symbol") for scan in scans_data if scan.get("ticker_symbol")}
                existing_tickers = {
                    t.symbol: t for t in db.query(Ticker).filter(Ticker.symbol.in_(symbols)).all()
                }

                # Create missing tickers
                new_tickers = []
                for symbol in symbols:
                    if symbol not in existing_tickers:
                        ticker = Ticker(symbol=symbol.upper())
                        new_tickers.append(ticker)
                        existing_tickers[symbol] = ticker

                if new_tickers:
                    db.bulk_save_objects(new_tickers)
                    db.flush()  # Get IDs for new tickers

                # Build scan objects
                scans = []
                for data in scans_data:
                    symbol = data.get("ticker_symbol")
                    if not symbol:
                        continue

                    ticker = existing_tickers.get(symbol)
                    if not ticker:
                        continue

                    scan = PatternScan(
                        ticker_id=ticker.id,
                        pattern_type=data.get("pattern", "UNKNOWN"),
                        score=data.get("score", 0),
                        entry_price=data.get("entry"),
                        stop_price=data.get("stop"),
                        target_price=data.get("target"),
                        risk_reward_ratio=data.get("risk_reward"),
                        criteria_met=str(data.get("criteria_met", [])),
                        analysis=data.get("analysis", ""),
                        current_price=data.get("current_price"),
                        volume_dry_up=data.get("volume_dry_up", False),
                        consolidation_days=data.get("consolidation_days")
                    )
                    scans.append(scan)

                if scans:
                    db.bulk_save_objects(scans)
                    db.commit()

                return len(scans)

        except Exception as e:
            logger.error(f"Failed to save pattern scans batch: {e}")
            raise

    def get_recent_scans(self, limit: int = 50, pattern_type: str = None, min_score: float = None) -> List[Dict[str, Any]]:
        """Get recent pattern scans with ticker info (optimized with filters)"""
        with self.get_db() as db:
            query = db.query(
                PatternScan.id,
                PatternScan.pattern_type,
                PatternScan.score,
                PatternScan.entry_price,
                PatternScan.stop_price,
                PatternScan.target_price,
                PatternScan.scanned_at,
                Ticker.symbol
            ).join(Ticker)

            # Apply filters
            if pattern_type:
                query = query.filter(PatternScan.pattern_type == pattern_type)
            if min_score is not None:
                query = query.filter(PatternScan.score >= min_score)

            results = query.order_by(
                PatternScan.scanned_at.desc()
            ).limit(limit).all()

            return [{
                "id": row.id,
                "ticker": row.symbol,
                "pattern": row.pattern_type,
                "score": row.score,
                "entry": row.entry_price,
                "stop": row.stop_price,
                "target": row.target_price,
                "scanned_at": row.scanned_at.isoformat()
            } for row in results]

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
            with self.engine.begin() as conn:
                conn.execute(text(
                    """
                    create table if not exists watchlist (
                      id serial primary key,
                      symbol text unique not null,
                      reason text,
                      tags text,
                      status text default 'Watching',
                      created_at timestamptz default now()
                    );
                    """
                ))
        except Exception as e:
            logger.warning(f"Could not ensure watchlist table: {e}")

    def get_watchlist_items(self) -> List[Dict[str, Any]]:
        """Return watchlist items from Postgres. Never raise; returns []."""
        try:
            if not self.engine:
                return []
            self.ensure_watchlist_table()
            with self.engine.begin() as conn:
                rows = conn.execute(text("select id, symbol, reason, tags, status, created_at from watchlist order by created_at desc"))
                return [
                    {
                        "id": r[0],
                        "ticker": r[1],
                        "reason": r[2],
                        "tags": [tag.strip() for tag in (r[3] or "").split(",") if tag.strip()],
                        "status": r[4],
                        "added_at": r[5].isoformat() if r[5] else None,
                    }
                    for r in rows
                ]
        except Exception as e:
            logger.warning(f"get_watchlist_items fallback: {e}")
            return []

    def add_watchlist_symbol(self, symbol: str, reason: str = None, tags: str = None, status: str = "Watching") -> bool:
        try:
            if not self.engine:
                return False
            self.ensure_watchlist_table()
            with self.engine.begin() as conn:
                conn.execute(
                    text("insert into watchlist (symbol, reason, tags, status) values (:s, :r, :t, :st) on conflict(symbol) do update set reason=excluded.reason, tags=excluded.tags, status=excluded.status"),
                    {"s": symbol.upper(), "r": reason, "t": tags, "st": status}
                )
            return True
        except Exception as e:
            logger.warning(f"add_watchlist_symbol failed: {e}")
            return False

    def log_alert(
        self, ticker: str, alert_type: str, message: str, metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Log alert to database"""
        try:
            if not self.engine:
                return False
            from datetime import datetime
            import json
            
            with self.engine.connect() as conn:
                conn.execute(
                    text("""
                        INSERT INTO alert_logs (ticker, alert_type, message, metadata, created_at)
                        VALUES (:ticker, :alert_type, :message, :metadata, :created_at)
                    """),
                    {
                        "ticker": ticker,
                        "alert_type": alert_type,
                        "message": message,
                        "metadata": json.dumps(metadata) if metadata else None,
                        "created_at": datetime.utcnow()
                    }
                )
                conn.commit()
            return True
        except Exception as e:
            logger.warning(f"Failed to log alert for {ticker}: {e}")
            return False
    
    def update_watchlist_symbol(self, symbol: str, reason: Optional[str] = None, tags: Optional[str] = None, status: Optional[str] = None) -> bool:
        try:
            if not self.engine:
                return False
            self.ensure_watchlist_table()
            with self.engine.begin() as conn:
                result = conn.execute(
                    text(
                        """
                        update watchlist
                        set
                          reason = coalesce(:reason, reason),
                          tags = coalesce(:tags, tags),
                          status = coalesce(:status, status)
                        where symbol = :symbol
                        """
                    ),
                    {"reason": reason, "tags": tags, "status": status, "symbol": symbol.upper()},
                )
            return result.rowcount > 0
        except Exception as e:
            logger.warning(f"update_watchlist_symbol failed: {e}")
            return False

    def remove_watchlist_symbol(self, symbol: str) -> bool:
        try:
            if not self.engine:
                return False
            self.ensure_watchlist_table()
            with self.engine.begin() as conn:
                result = conn.execute(
                    text("delete from watchlist where symbol = :symbol"),
                    {"symbol": symbol.upper()},
                )
            return result.rowcount > 0
        except Exception as e:
            logger.warning(f"remove_watchlist_symbol failed: {e}")
            return False

    def get_universe_symbols(self, limit: Optional[int] = None) -> List["UniverseSymbol"]:
        """Return symbols stored in the universe_symbols table."""
        from app.models import UniverseSymbol

        with self.get_db() as db:
            query = db.query(UniverseSymbol)
            if limit:
                query = query.limit(limit)
            return query.order_by(UniverseSymbol.symbol).all()

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
