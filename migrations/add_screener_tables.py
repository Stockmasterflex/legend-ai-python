"""
Database migration to add screener tables

Creates tables for:
- saved_screens: User-defined custom screens
- screen_results: Historical screen execution results
- scheduled_scans: Scheduled scan execution log
"""
import logging
from sqlalchemy import text

from app.services.database import get_db_service
from app.models import Base, SavedScreen, ScreenResult, ScheduledScan

logger = logging.getLogger(__name__)


def upgrade():
    """Create screener tables"""
    try:
        db_service = get_db_service()
        engine = db_service.engine

        # Create tables if they don't exist
        Base.metadata.create_all(
            engine,
            tables=[
                SavedScreen.__table__,
                ScreenResult.__table__,
                ScheduledScan.__table__
            ]
        )

        logger.info("✅ Screener tables created successfully")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to create screener tables: {e}")
        return False


def downgrade():
    """Drop screener tables"""
    try:
        db_service = get_db_service()
        engine = db_service.engine

        # Drop tables in reverse order (to handle foreign keys)
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS scheduled_scans CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS screen_results CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS saved_screens CASCADE"))
            conn.commit()

        logger.info("✅ Screener tables dropped successfully")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to drop screener tables: {e}")
        return False


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)

    print("Running screener tables migration...")
    success = upgrade()

    if success:
        print("\n✅ Migration completed successfully!")
        print("\nNew tables created:")
        print("  - saved_screens: Custom stock screens")
        print("  - screen_results: Historical screen results")
        print("  - scheduled_scans: Scheduled scan logs")
    else:
        print("\n❌ Migration failed. Check logs for details.")
