"""
Learning Center Service
Manages educational content, tutorials, and user learning progress
"""

from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.models import LearningContent, UserLearningProgress


# Educational content library
LEARNING_CONTENT = [
    # Pattern Education
    {
        "content_key": "vcp_deep_dive",
        "title": "VCP Pattern Deep Dive",
        "category": "pattern",
        "content_type": "article",
        "difficulty": "intermediate",
        "estimated_time": 15,
        "order_index": 1,
        "content": """
# Understanding VCP (Volatility Contraction Pattern)

## What is VCP?

The Volatility Contraction Pattern (VCP) was popularized by Mark Minervini, a champion stock trader.
It's a pattern that shows decreasing volatility over time, indicating strong hands accumulating shares.

## Key Characteristics

1. **Multiple Contractions**: Look for 2-4 pullbacks, each shallower than the last
2. **Volume Dry-Up**: Volume should decrease during consolidation
3. **Tight Price Action**: Later consolidations should be very tight (1-2%)
4. **Strong Prior Trend**: Pattern works best after a strong uptrend

## How to Trade VCP

### Entry Point
- Enter when price breaks above the last contraction on increasing volume
- Ideal entry is within 5% of the breakout point

### Stop Loss
- Place stop below the last contraction low
- Risk should be 5-8% maximum

### Target
- Aim for previous high or 20-30% gain
- Trail stop as stock advances

## Example Scorecard

A strong VCP should score:
- Contraction Count: 3-4 contractions (25 points)
- Volume Pattern: Clear dry-up (25 points)
- Tightness: Final contraction <2% (25 points)
- Structure: Clean, organized pattern (25 points)

Total Score: 80+ indicates excellent pattern
""",
    },
    {
        "content_key": "cup_handle_guide",
        "title": "Cup & Handle Pattern Guide",
        "category": "pattern",
        "content_type": "article",
        "difficulty": "beginner",
        "estimated_time": 10,
        "order_index": 2,
        "content": """
# Cup & Handle Pattern

## Overview

The Cup & Handle is a bullish continuation pattern that resembles a tea cup.
It's one of the most reliable patterns for swing trading.

## Cup Formation

The cup should have:
- **U-Shape**: Rounded bottom, not V-shaped
- **Duration**: 1-6 months typically
- **Depth**: 12-33% correction is ideal
- **Equal Highs**: Left and right rim should be similar

## Handle Formation

The handle should:
- **Drift Down**: Slight downward drift or sideways
- **Duration**: 1-4 weeks
- **Depth**: Less than 1/3 of cup depth
- **Volume**: Should decrease

## Trading Rules

### Entry
- Buy when price breaks above handle high
- Volume should be 50%+ above average

### Stop Loss
- Below handle low or mid-point of handle

### Target
- Measure cup depth and add to breakout point
- Minimum target: cup depth × 100%

## What to Avoid

❌ V-shaped cups
❌ Deep handles (>50% of cup)
❌ Breakout on low volume
❌ Choppy, erratic price action
""",
    },
    {
        "content_key": "relative_strength",
        "title": "Understanding Relative Strength",
        "category": "strategy",
        "content_type": "article",
        "difficulty": "intermediate",
        "estimated_time": 12,
        "order_index": 3,
        "content": """
# Relative Strength Analysis

## What is Relative Strength?

Relative Strength (RS) measures how a stock performs compared to the overall market.
It's NOT the same as RSI (Relative Strength Index).

## Why It Matters

- Leading stocks show strong RS before breakouts
- RS rating >80 means stock is outperforming 80% of market
- William O'Neil's research: winning stocks average RS of 87

## How Legend AI Calculates RS

We compare the stock's price change vs S&P 500 over:
- 3 months: 40% weight
- 6 months: 30% weight
- 9 months: 20% weight
- 12 months: 10% weight

## Trading with RS

### Buy Signals
✅ RS > 80 (top 20% of market)
✅ RS trending higher
✅ RS stays strong during pullbacks

### Warning Signs
⚠️ RS < 70
⚠️ RS declining while price rises
⚠️ RS breaks below 50

## Pro Tip

Look for stocks with RS >85 that are forming patterns.
These have the highest probability of success.
""",
    },
    # Trading Strategy
    {
        "content_key": "minervini_strategy",
        "title": "Mark Minervini's SEPA Method",
        "category": "strategy",
        "content_type": "article",
        "difficulty": "advanced",
        "estimated_time": 20,
        "order_index": 4,
        "content": """
# SEPA: Specific Entry Point Analysis

Mark Minervini's methodology for finding and trading superperformance stocks.

## The Trend Template

Stock must meet ALL criteria:

1. **Price Above Moving Averages**
   - Stock above 150-day and 200-day MA
   - 150-day MA above 200-day MA

2. **Moving Average Alignment**
   - 50-day MA > 150-day MA > 200-day MA
   - All MAs trending up

3. **Relative Strength**
   - RS Rating > 70, ideally > 80
   - Stock outperforming market

4. **Price Action**
   - Current price within 25% of 52-week high
   - Current price at least 30% above 52-week low

5. **Stage Analysis**
   - Stock in Stage 2 (advancing phase)
   - Not extended or in Stage 3/4

## Entry Criteria

Wait for VCP or tight consolidation:
- Multiple contractions showing tightness
- Volume drying up
- Entry within 5% of pivot point

## Risk Management

- Risk 1-3% per trade
- Cut losses at 7-8%
- Position size based on stop distance
- Build positions gradually

## Exit Strategy

- Trail stop as stock advances
- Take partial profits at 20-25%
- Exit if breaks below 10-week MA on volume
""",
    },
    # Glossary Terms
    {
        "content_key": "glossary_pivot",
        "title": "What is a Pivot Point?",
        "category": "glossary",
        "content_type": "article",
        "difficulty": "beginner",
        "estimated_time": 3,
        "order_index": 10,
        "content": """
# Pivot Point

## Definition

A pivot point is the optimal buy point in a chart pattern. It's where price breaks
through resistance and begins a new upward move.

## Common Pivot Points

- **Cup & Handle**: Top of the handle
- **VCP**: Top of last contraction
- **Flat Base**: High of the base
- **Ascending Triangle**: Resistance line

## How to Use

1. Identify the pattern
2. Draw a horizontal line at the high point
3. Enter when price breaks above on volume
4. Enter within 5% of pivot for best results

## Risk Management

Stop loss is typically 7-8% below pivot point or at pattern low.
""",
    },
    {
        "content_key": "glossary_volume_dryup",
        "title": "What is Volume Dry-Up?",
        "category": "glossary",
        "content_type": "article",
        "difficulty": "beginner",
        "estimated_time": 3,
        "order_index": 11,
        "content": """
# Volume Dry-Up

## Definition

Volume dry-up occurs when trading volume decreases significantly during a consolidation.
This indicates sellers are exhausted and supply is drying up.

## Why It Matters

- Shows lack of selling pressure
- Indicates strong hands holding shares
- Sets up explosive breakout on volume surge

## How to Identify

1. Compare volume to 50-day average
2. Look for 40-60% below average during consolidation
3. Volume should expand on breakout (50%+ above average)

## What Legend AI Looks For

Our scanner checks:
- Volume trend during consolidation
- Volume spike on breakout
- Consistency of low volume during pattern
""",
    },
    # Best Practices
    {
        "content_key": "position_sizing",
        "title": "Proper Position Sizing",
        "category": "best_practice",
        "content_type": "article",
        "difficulty": "intermediate",
        "estimated_time": 10,
        "order_index": 20,
        "content": """
# Position Sizing: The Key to Longevity

## Why Position Sizing Matters

Position sizing is MORE important than entry or exit.
Poor sizing can turn winners into losers or blow up your account.

## The Formula

```
Position Size = (Account Size × Risk %) / (Entry Price - Stop Loss)
```

## Example

- Account: $100,000
- Risk: 2% ($2,000)
- Entry: $50
- Stop: $46
- Risk per share: $4

Position Size = $2,000 / $4 = 500 shares

## Risk Levels by Experience

- **Beginner**: 1% per trade
- **Intermediate**: 1-2% per trade
- **Advanced**: 2-3% per trade
- **Never**: >5% per trade

## Legend AI Integration

Our platform automatically calculates position size based on:
- Your account size
- Risk tolerance
- Stop loss distance
- Pattern quality

## Rules to Live By

1. Never risk more than 2-3% on one trade
2. Scale into positions, don't go all-in
3. Adjust size based on setup quality
4. Reduce size in choppy markets
""",
    },
]


class LearningCenterService:
    """Service for managing learning center content"""

    @staticmethod
    async def init_content(db: Session):
        """Initialize learning content in database"""
        for content_data in LEARNING_CONTENT:
            existing = db.query(LearningContent).filter(
                LearningContent.content_key == content_data["content_key"]
            ).first()

            if not existing:
                content = LearningContent(**content_data)
                db.add(content)

        db.commit()

    @staticmethod
    async def get_all_content(
        db: Session,
        category: Optional[str] = None,
        difficulty: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get all learning content with optional filters"""
        query = db.query(LearningContent)

        if category:
            query = query.filter(LearningContent.category == category)
        if difficulty:
            query = query.filter(LearningContent.difficulty == difficulty)

        content_list = query.order_by(LearningContent.order_index).all()

        return [
            {
                "id": content.id,
                "key": content.content_key,
                "title": content.title,
                "category": content.category,
                "content_type": content.content_type,
                "difficulty": content.difficulty,
                "estimated_time": content.estimated_time,
                "video_url": content.video_url,
            }
            for content in content_list
        ]

    @staticmethod
    async def get_content(
        db: Session,
        content_key: str
    ) -> Optional[Dict[str, Any]]:
        """Get specific learning content"""
        content = db.query(LearningContent).filter(
            LearningContent.content_key == content_key
        ).first()

        if not content:
            return None

        return {
            "id": content.id,
            "key": content.content_key,
            "title": content.title,
            "category": content.category,
            "content_type": content.content_type,
            "difficulty": content.difficulty,
            "estimated_time": content.estimated_time,
            "content": content.content,
            "video_url": content.video_url,
        }

    @staticmethod
    async def track_progress(
        db: Session,
        user_id: str,
        content_key: str,
        progress: int,
        completed: bool = False
    ) -> Dict[str, Any]:
        """Track user progress on learning content"""
        # Get content
        content = db.query(LearningContent).filter(
            LearningContent.content_key == content_key
        ).first()

        if not content:
            raise ValueError(f"Content '{content_key}' not found")

        # Get or create progress record
        user_progress = db.query(UserLearningProgress).filter(
            UserLearningProgress.user_id == user_id,
            UserLearningProgress.content_id == content.id
        ).first()

        if not user_progress:
            user_progress = UserLearningProgress(
                user_id=user_id,
                content_id=content.id,
                progress=progress
            )
            db.add(user_progress)
        else:
            user_progress.progress = progress
            user_progress.last_viewed_at = datetime.utcnow()

        if completed:
            user_progress.completed = True
            user_progress.completed_at = datetime.utcnow()

        db.commit()
        db.refresh(user_progress)

        return {
            "content_key": content_key,
            "progress": user_progress.progress,
            "completed": user_progress.completed,
        }

    @staticmethod
    async def get_user_progress(
        db: Session,
        user_id: str
    ) -> List[Dict[str, Any]]:
        """Get all learning progress for user"""
        progress_records = db.query(
            LearningContent, UserLearningProgress
        ).join(
            UserLearningProgress,
            LearningContent.id == UserLearningProgress.content_id
        ).filter(
            UserLearningProgress.user_id == user_id
        ).all()

        return [
            {
                "content_key": content.content_key,
                "title": content.title,
                "category": content.category,
                "progress": progress.progress,
                "completed": progress.completed,
                "last_viewed": progress.last_viewed_at.isoformat(),
            }
            for content, progress in progress_records
        ]

    @staticmethod
    async def toggle_bookmark(
        db: Session,
        user_id: str,
        content_key: str
    ) -> Dict[str, Any]:
        """Bookmark or unbookmark content"""
        content = db.query(LearningContent).filter(
            LearningContent.content_key == content_key
        ).first()

        if not content:
            raise ValueError(f"Content '{content_key}' not found")

        # Get or create progress record
        user_progress = db.query(UserLearningProgress).filter(
            UserLearningProgress.user_id == user_id,
            UserLearningProgress.content_id == content.id
        ).first()

        if not user_progress:
            user_progress = UserLearningProgress(
                user_id=user_id,
                content_id=content.id,
                bookmarked=True
            )
            db.add(user_progress)
        else:
            user_progress.bookmarked = not user_progress.bookmarked

        db.commit()
        db.refresh(user_progress)

        return {
            "content_key": content_key,
            "bookmarked": user_progress.bookmarked,
        }

    @staticmethod
    async def get_bookmarks(
        db: Session,
        user_id: str
    ) -> List[Dict[str, Any]]:
        """Get user's bookmarked content"""
        bookmarks = db.query(
            LearningContent, UserLearningProgress
        ).join(
            UserLearningProgress,
            LearningContent.id == UserLearningProgress.content_id
        ).filter(
            UserLearningProgress.user_id == user_id,
            UserLearningProgress.bookmarked == True
        ).all()

        return [
            {
                "id": content.id,
                "key": content.content_key,
                "title": content.title,
                "category": content.category,
                "difficulty": content.difficulty,
            }
            for content, _ in bookmarks
        ]

    @staticmethod
    async def get_categories(db: Session) -> List[Dict[str, Any]]:
        """Get all content categories with counts"""
        categories = db.query(
            LearningContent.category,
            func.count(LearningContent.id).label('count')
        ).group_by(LearningContent.category).all()

        category_info = {
            "pattern": {"name": "Pattern Education", "icon": "🎯", "description": "Learn chart patterns"},
            "strategy": {"name": "Trading Strategies", "icon": "📈", "description": "Proven trading methods"},
            "glossary": {"name": "Trading Glossary", "icon": "📖", "description": "Key terms defined"},
            "best_practice": {"name": "Best Practices", "icon": "⭐", "description": "Trading wisdom"},
        }

        return [
            {
                "key": cat,
                "name": category_info.get(cat, {}).get("name", cat),
                "icon": category_info.get(cat, {}).get("icon", "📄"),
                "description": category_info.get(cat, {}).get("description", ""),
                "count": count,
            }
            for cat, count in categories
        ]
