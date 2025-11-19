#!/usr/bin/env python3
"""
Database Migration Runner
Creates tables and runs any pending migrations
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy import text, inspect
from app.models import Base
from app.services.database import DatabaseService

# Color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'


async def run_migrations():
    """Run database migrations"""
    print(f"{BLUE}Starting database migrations...{NC}\n")

    try:
        # Initialize database service
        db_service = DatabaseService()
        await db_service.init_db()

        print(f"{GREEN}✓ Database connection established{NC}")

        # Get engine from db_service
        engine = db_service.engine

        # Check existing tables
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        print(f"\n{BLUE}Existing tables:{NC}")
        for table in existing_tables:
            print(f"  - {table}")

        # Get all model tables
        model_tables = Base.metadata.tables.keys()

        print(f"\n{BLUE}Required tables:{NC}")
        for table in model_tables:
            if table in existing_tables:
                print(f"  {GREEN}✓{NC} {table}")
            else:
                print(f"  {YELLOW}+{NC} {table} (will be created)")

        # Create all tables
        print(f"\n{BLUE}Creating missing tables...{NC}")
        Base.metadata.create_all(bind=engine)
        print(f"{GREEN}✓ All tables created/verified{NC}")

        # Run custom migrations
        print(f"\n{BLUE}Running custom migrations...{NC}")

        # Migration 1: Add indexes if not exist
        async with db_service.get_session() as session:
            try:
                # Check if indexes exist and create if needed
                await session.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_pattern_scans_ticker_id ON pattern_scans(ticker_id);
                """))
                await session.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_pattern_scans_scanned_at ON pattern_scans(scanned_at);
                """))
                await session.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_watchlists_user_id ON watchlists(user_id);
                """))
                await session.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_watchlists_ticker_id ON watchlists(ticker_id);
                """))
                await session.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_alert_logs_ticker_id ON alert_logs(ticker_id);
                """))
                await session.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_alert_logs_user_id ON alert_logs(user_id);
                """))
                await session.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_alert_logs_created_at ON alert_logs(created_at);
                """))

                await session.commit()
                print(f"  {GREEN}✓{NC} Database indexes created")
            except Exception as e:
                print(f"  {YELLOW}⚠{NC} Index creation: {str(e)}")

        # Migration 2: Add new columns for pattern validation (if not exist)
        async with db_service.get_session() as session:
            try:
                await session.execute(text("""
                    ALTER TABLE pattern_scans
                    ADD COLUMN IF NOT EXISTS actual_outcome VARCHAR(50),
                    ADD COLUMN IF NOT EXISTS outcome_date TIMESTAMP,
                    ADD COLUMN IF NOT EXISTS outcome_price NUMERIC(10, 2),
                    ADD COLUMN IF NOT EXISTS was_successful BOOLEAN,
                    ADD COLUMN IF NOT EXISTS actual_gain_loss NUMERIC(10, 2);
                """))
                await session.commit()
                print(f"  {GREEN}✓{NC} Pattern validation columns added")
            except Exception as e:
                print(f"  {YELLOW}⚠{NC} Column addition: {str(e)}")

        # Migration 3: Add alert preferences columns
        async with db_service.get_session() as session:
            try:
                await session.execute(text("""
                    ALTER TABLE watchlists
                    ADD COLUMN IF NOT EXISTS alert_on_pattern BOOLEAN DEFAULT true,
                    ADD COLUMN IF NOT EXISTS alert_on_price_target BOOLEAN DEFAULT true,
                    ADD COLUMN IF NOT EXISTS alert_on_stop_loss BOOLEAN DEFAULT true,
                    ADD COLUMN IF NOT EXISTS alert_frequency VARCHAR(50) DEFAULT 'once';
                """))
                await session.commit()
                print(f"  {GREEN}✓{NC} Alert preference columns added")
            except Exception as e:
                print(f"  {YELLOW}⚠{NC} Alert columns: {str(e)}")

        print(f"\n{GREEN}✓ All migrations completed successfully!{NC}")
        return True

    except Exception as e:
        print(f"\n{RED}❌ Migration failed: {str(e)}{NC}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point"""
    result = asyncio.run(run_migrations())
    return 0 if result else 1


if __name__ == "__main__":
    sys.exit(main())
