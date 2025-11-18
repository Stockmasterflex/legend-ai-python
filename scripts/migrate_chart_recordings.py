"""
Migration script for Chart Recordings table
Run this to ensure the chart_recordings table exists
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, inspect, text
from app.config import get_settings
from app.models import Base, ChartRecording
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_table_exists(engine, table_name):
    """Check if a table exists in the database"""
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()


def migrate():
    """Create chart_recordings table if it doesn't exist"""
    settings = get_settings()
    engine = create_engine(settings.database_url)

    logger.info("Starting chart recordings migration...")

    # Check if table exists
    if check_table_exists(engine, 'chart_recordings'):
        logger.info("✓ chart_recordings table already exists")
    else:
        logger.info("Creating chart_recordings table...")

        # Create only the ChartRecording table
        ChartRecording.__table__.create(bind=engine, checkfirst=True)

        logger.info("✓ chart_recordings table created successfully")

    # Verify table structure
    inspector = inspect(engine)
    columns = inspector.get_columns('chart_recordings')

    logger.info(f"Table structure verified: {len(columns)} columns")
    for col in columns:
        logger.info(f"  - {col['name']}: {col['type']}")

    logger.info("Migration completed successfully!")


if __name__ == "__main__":
    migrate()
