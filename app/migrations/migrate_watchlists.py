"""
Migration script for watchlist feature enhancement
Migrates from simple watchlist to multi-watchlist with groups
"""

import logging
from typing import Dict, Any
from sqlalchemy import text

from app.services.database import get_database_service
from app.models import WatchlistGroup, Watchlist

logger = logging.getLogger(__name__)


def migrate_watchlist_data():
    """
    Migrate existing watchlist data to new schema:
    1. Create default watchlist group for each user
    2. Migrate existing watchlist items to use groups
    3. Preserve all existing data
    """
    db_service = get_database_service()

    try:
        with db_service.get_db() as db:
            logger.info("Starting watchlist migration...")

            # Check if old watchlist table exists
            try:
                old_items = db.execute(
                    text("SELECT id, symbol, reason, tags, status, created_at FROM watchlist")
                ).fetchall()

                if old_items:
                    logger.info(f"Found {len(old_items)} items in old watchlist table")

                    # Create default group for migration
                    default_group = WatchlistGroup(
                        user_id="default",
                        name="Main Watchlist",
                        description="Migrated from legacy watchlist",
                        color="#3B82F6",
                        position=0,
                        is_default=True
                    )
                    db.add(default_group)
                    db.flush()  # Get the ID

                    logger.info(f"Created default watchlist group (ID: {default_group.id})")

                    # Migrate items
                    migrated = 0
                    for item in old_items:
                        try:
                            # Get or create ticker
                            ticker = db_service.get_or_create_ticker(item.symbol)

                            # Check if item already exists in new schema
                            existing = db.query(Watchlist).filter(
                                Watchlist.ticker_id == ticker.id,
                                Watchlist.user_id == "default"
                            ).first()

                            if not existing:
                                # Create new watchlist item
                                new_item = Watchlist(
                                    user_id="default",
                                    group_id=default_group.id,
                                    ticker_id=ticker.id,
                                    status=item.status or "Watching",
                                    reason=item.reason,
                                    notes=item.tags,  # Old tags go to notes
                                    position=migrated
                                )
                                db.add(new_item)
                                migrated += 1
                        except Exception as e:
                            logger.warning(f"Error migrating item {item.symbol}: {e}")
                            continue

                    db.commit()
                    logger.info(f"✅ Successfully migrated {migrated} watchlist items")

                else:
                    logger.info("No items found in old watchlist table - nothing to migrate")

            except Exception as e:
                # Old table might not exist - that's ok
                logger.info(f"Old watchlist table not found or error accessing it: {e}")

            # Get unique users from new watchlists table
            users = db.execute(
                text("SELECT DISTINCT user_id FROM watchlists WHERE group_id IS NULL")
            ).fetchall()

            if users:
                logger.info(f"Found {len(users)} users with ungrouped watchlist items")

                for (user_id,) in users:
                    # Check if user already has a default group
                    existing_group = db.query(WatchlistGroup).filter(
                        WatchlistGroup.user_id == user_id,
                        WatchlistGroup.is_default == True
                    ).first()

                    if not existing_group:
                        # Create default group
                        default_group = WatchlistGroup(
                            user_id=user_id,
                            name="Main Watchlist",
                            description="Default watchlist",
                            color="#3B82F6",
                            position=0,
                            is_default=True
                        )
                        db.add(default_group)
                        db.flush()

                        # Assign ungrouped items to default group
                        db.execute(
                            text(
                                "UPDATE watchlists SET group_id = :group_id "
                                "WHERE user_id = :user_id AND group_id IS NULL"
                            ),
                            {"group_id": default_group.id, "user_id": user_id}
                        )

                        logger.info(f"Created default group for user {user_id}")

                db.commit()
                logger.info("✅ Migration completed successfully")
            else:
                logger.info("No ungrouped items found - migration not needed")

            return {"success": True, "message": "Migration completed"}

    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return {"success": False, "error": str(e)}


def create_sample_watchlists():
    """Create sample watchlist groups and items for demonstration"""
    db_service = get_database_service()

    try:
        with db_service.get_db() as db:
            logger.info("Creating sample watchlist data...")

            # Create sample groups
            groups = [
                {
                    "name": "Swing Trades",
                    "description": "Medium-term swing trade setups",
                    "color": "#10B981",
                    "strategy": "Swing Trading",
                    "position": 0
                },
                {
                    "name": "Day Trading",
                    "description": "Intraday momentum plays",
                    "color": "#F59E0B",
                    "strategy": "Day Trading",
                    "position": 1
                },
                {
                    "name": "Long-term Holdings",
                    "description": "Quality stocks for position trading",
                    "color": "#6366F1",
                    "strategy": "Position Trading",
                    "position": 2
                }
            ]

            created_groups = []
            for group_data in groups:
                group = WatchlistGroup(user_id="default", **group_data)
                db.add(group)
                db.flush()
                created_groups.append(group)

            # Sample tickers for each group
            sample_items = [
                # Swing Trades
                ("AAPL", created_groups[0].id, "VCP", 85, "#10B981"),
                ("MSFT", created_groups[0].id, "Cup & Handle", 78, "#3B82F6"),
                ("NVDA", created_groups[0].id, "Ascending Triangle", 92, "#EF4444"),

                # Day Trading
                ("TSLA", created_groups[1].id, "Bull Flag", 88, "#F59E0B"),
                ("AMD", created_groups[1].id, "Breakout", 76, "#10B981"),

                # Long-term
                ("GOOGL", created_groups[2].id, None, 82, "#6366F1"),
                ("AMZN", created_groups[2].id, None, 79, "#8B5CF6"),
            ]

            for symbol, group_id, pattern, strength, color in sample_items:
                ticker = db_service.get_or_create_ticker(symbol)

                item = Watchlist(
                    user_id="default",
                    group_id=group_id,
                    ticker_id=ticker.id,
                    pattern_type=pattern,
                    strength_score=strength,
                    color=color,
                    status="Watching"
                )
                db.add(item)

            db.commit()
            logger.info("✅ Sample watchlist data created")

            return {"success": True, "message": "Sample data created"}

    except Exception as e:
        logger.error(f"Error creating sample data: {e}")
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("=" * 60)
    print("Watchlist Migration Script")
    print("=" * 60)

    # Run migration
    result = migrate_watchlist_data()
    print(f"\nMigration Result: {result}")

    # Optionally create sample data
    create_samples = input("\nCreate sample watchlist data? (y/n): ")
    if create_samples.lower() == 'y':
        result = create_sample_watchlists()
        print(f"\nSample Data Result: {result}")

    print("\n✅ Done!")
