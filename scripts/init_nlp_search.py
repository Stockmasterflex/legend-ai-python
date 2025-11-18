"""
Database initialization script for NLP Search tables
Run this script to create the required tables for NLP search functionality
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.services.database import get_async_engine
from app.models import Base, SearchHistory, QuerySuggestion
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_nlp_tables():
    """Create NLP search tables in the database"""
    engine = get_async_engine()

    try:
        async with engine.begin() as conn:
            logger.info("Creating NLP search tables...")

            # Create SearchHistory table
            await conn.run_sync(SearchHistory.__table__.create, checkfirst=True)
            logger.info("✓ Created search_history table")

            # Create QuerySuggestion table
            await conn.run_sync(QuerySuggestion.__table__.create, checkfirst=True)
            logger.info("✓ Created query_suggestions table")

            # Insert initial query suggestions
            await conn.execute(text("""
                INSERT INTO query_suggestions (suggestion_text, category, popularity_score, context_patterns, example_queries)
                VALUES
                    ('Find VCP patterns in tech stocks', 'pattern', 10.0, '["vcp"]', '["find vcp in tech", "tech vcp patterns"]'),
                    ('Show me breakouts above $100', 'price', 8.0, '["breakout"]', '["breakouts over 100", "stocks breaking out above 100"]'),
                    ('Which stocks are pulling back to 21 EMA?', 'indicator', 7.0, '["pullback"]', '["pullback to ema", "21 ema pullback"]'),
                    ('Compare AAPL and MSFT patterns', 'comparison', 6.0, '[]', '["compare aapl msft", "aapl vs msft"]'),
                    ('Analyze NVDA chart', 'analyze', 9.0, '[]', '["analyze nvidia", "nvda analysis"]'),
                    ('Show top setups today', 'scan', 10.0, '[]', '["best setups", "top patterns today"]'),
                    ('Find cup and handle patterns', 'pattern', 8.0, '["cup_and_handle"]', '["cup handle", "cup with handle patterns"]'),
                    ('Stocks near 50 day moving average', 'indicator', 7.0, '["sma50_pullback"]', '["50ma bounce", "near 50 sma"]'),
                    ('Tech stocks breaking out', 'sector', 8.0, '["breakout"]', '["technology breakouts", "tech sector breakouts"]'),
                    ('High RS rating stocks', 'metric', 7.0, '[]', '["relative strength", "strong rs rating"]')
                ON CONFLICT (suggestion_text) DO NOTHING
            """))
            logger.info("✓ Inserted initial query suggestions")

            await conn.commit()

        logger.info("✅ NLP search tables initialized successfully!")

    except Exception as e:
        logger.error(f"❌ Error initializing tables: {str(e)}")
        raise

    finally:
        await engine.dispose()


async def verify_tables():
    """Verify that tables were created successfully"""
    engine = get_async_engine()

    try:
        async with engine.connect() as conn:
            # Check if tables exist
            result = await conn.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name IN ('search_history', 'query_suggestions')
            """))

            tables = [row[0] for row in result]

            if 'search_history' in tables:
                logger.info("✓ search_history table exists")
            else:
                logger.warning("⚠ search_history table not found")

            if 'query_suggestions' in tables:
                logger.info("✓ query_suggestions table exists")
            else:
                logger.warning("⚠ query_suggestions table not found")

            # Count suggestions
            result = await conn.execute(text("SELECT COUNT(*) FROM query_suggestions"))
            count = result.scalar()
            logger.info(f"✓ Found {count} query suggestions")

    except Exception as e:
        logger.error(f"❌ Error verifying tables: {str(e)}")
        raise

    finally:
        await engine.dispose()


if __name__ == "__main__":
    print("=" * 60)
    print("NLP Search Database Initialization")
    print("=" * 60)
    print()

    # Run initialization
    asyncio.run(init_nlp_tables())

    print()
    print("=" * 60)
    print("Verification")
    print("=" * 60)
    print()

    # Verify
    asyncio.run(verify_tables())

    print()
    print("=" * 60)
    print("Done!")
    print("=" * 60)
