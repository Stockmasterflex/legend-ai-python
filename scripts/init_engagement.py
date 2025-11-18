#!/usr/bin/env python3
"""
Initialize Engagement System
Seeds achievements and learning content into database
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Achievement, LearningContent
from app.services.engagement import ACHIEVEMENTS
from app.services.learning_center import LEARNING_CONTENT
from app.config import get_settings


def init_database():
    """Initialize database and create tables"""
    settings = get_settings()

    # Use database URL from settings, fallback to SQLite
    database_url = settings.database_url or "sqlite:///./legend_ai.db"

    print(f"Connecting to database: {database_url}")

    engine = create_engine(database_url, echo=True)

    # Create all tables
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created")

    return engine


def seed_achievements(session):
    """Seed achievement definitions"""
    print("\nSeeding achievements...")

    for ach_data in ACHIEVEMENTS:
        existing = session.query(Achievement).filter(
            Achievement.achievement_key == ach_data["achievement_key"]
        ).first()

        if not existing:
            achievement = Achievement(**ach_data)
            session.add(achievement)
            print(f"  + {ach_data['name']}")
        else:
            print(f"  - {ach_data['name']} (already exists)")

    session.commit()
    print("✓ Achievements seeded")


def seed_learning_content(session):
    """Seed learning content"""
    print("\nSeeding learning content...")

    for content_data in LEARNING_CONTENT:
        existing = session.query(LearningContent).filter(
            LearningContent.content_key == content_data["content_key"]
        ).first()

        if not existing:
            content = LearningContent(**content_data)
            session.add(content)
            print(f"  + {content_data['title']}")
        else:
            print(f"  - {content_data['title']} (already exists)")

    session.commit()
    print("✓ Learning content seeded")


def main():
    """Main initialization function"""
    print("=" * 60)
    print("Legend AI - Engagement System Initialization")
    print("=" * 60)

    try:
        # Initialize database
        engine = init_database()

        # Create session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Seed data
        seed_achievements(session)
        seed_learning_content(session)

        # Close session
        session.close()

        print("\n" + "=" * 60)
        print("✓ Engagement system initialized successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Start the server: uvicorn app.main:app --reload")
        print("2. Visit: http://localhost:8000/static/engagement.html")
        print("3. Initialize via API: POST /api/engagement/admin/init")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
