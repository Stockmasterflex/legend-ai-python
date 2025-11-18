"""
Tutorial and Onboarding Service
Handles interactive tutorials, tooltips, and user onboarding
"""

from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.models import TutorialProgress


# Tutorial definitions
TUTORIALS = {
    "onboarding": {
        "key": "onboarding",
        "name": "Welcome to Legend AI",
        "description": "Learn the basics of pattern scanning and analysis",
        "steps": [
            {
                "step": 1,
                "title": "Welcome to Legend AI",
                "content": "Legend AI helps you detect profitable trading patterns using advanced algorithms. Let's get started!",
                "action": "next",
                "tooltip_target": None,
            },
            {
                "step": 2,
                "title": "Pattern Detection",
                "content": "Use the Pattern Scanner to find VCP, Cup & Handle, and other powerful setups in real-time.",
                "action": "highlight",
                "tooltip_target": "#pattern-scanner",
            },
            {
                "step": 3,
                "title": "Stock Analysis",
                "content": "Click any stock to see detailed technical analysis, entry points, and risk/reward ratios.",
                "action": "highlight",
                "tooltip_target": "#analyze-button",
            },
            {
                "step": 4,
                "title": "Watchlist",
                "content": "Add promising setups to your watchlist and get alerts when they trigger.",
                "action": "highlight",
                "tooltip_target": "#watchlist",
            },
            {
                "step": 5,
                "title": "Learning Center",
                "content": "Visit the Learning Center to master pattern recognition and trading strategies.",
                "action": "highlight",
                "tooltip_target": "#learning-center",
            },
            {
                "step": 6,
                "title": "You're All Set!",
                "content": "Start scanning for patterns and level up your trading game. Happy trading!",
                "action": "complete",
                "tooltip_target": None,
            },
        ],
    },
    "vcp_pattern": {
        "key": "vcp_pattern",
        "name": "Understanding VCP Patterns",
        "description": "Learn about Volatility Contraction Patterns",
        "steps": [
            {
                "step": 1,
                "title": "What is VCP?",
                "content": "VCP (Volatility Contraction Pattern) is a consolidation where price volatility decreases over time, signaling accumulation.",
                "action": "next",
            },
            {
                "step": 2,
                "title": "Key Characteristics",
                "content": "Look for: 1) Decreasing volatility, 2) Volume dry-up, 3) Tight price action, 4) Multiple contractions",
                "action": "next",
            },
            {
                "step": 3,
                "title": "Entry Points",
                "content": "Best entry is when price breaks above the pivot point on increasing volume.",
                "action": "next",
            },
            {
                "step": 4,
                "title": "Try It Out",
                "content": "Run a VCP scan to see live examples in the market!",
                "action": "complete",
                "tooltip_target": "#vcp-scan-button",
            },
        ],
    },
    "cup_handle": {
        "key": "cup_handle",
        "name": "Cup & Handle Pattern",
        "description": "Master the classic Cup & Handle breakout pattern",
        "steps": [
            {
                "step": 1,
                "title": "Cup & Handle Basics",
                "content": "The Cup & Handle is a bullish continuation pattern shaped like a tea cup with a handle.",
                "action": "next",
            },
            {
                "step": 2,
                "title": "The Cup",
                "content": "The cup forms a 'U' shape showing a rounded bottom. Avoid 'V' shaped patterns - they're not ideal.",
                "action": "next",
            },
            {
                "step": 3,
                "title": "The Handle",
                "content": "After the cup, a small downward drift forms the handle. This is the final shakeout before breakout.",
                "action": "next",
            },
            {
                "step": 4,
                "title": "Breakout Point",
                "content": "Buy when price breaks above the handle's high point on strong volume.",
                "action": "complete",
            },
        ],
    },
    "risk_management": {
        "key": "risk_management",
        "name": "Risk Management 101",
        "description": "Learn proper position sizing and stop loss placement",
        "steps": [
            {
                "step": 1,
                "title": "Why Risk Management?",
                "content": "Protecting your capital is more important than making profits. One bad trade shouldn't wipe you out.",
                "action": "next",
            },
            {
                "step": 2,
                "title": "The 2% Rule",
                "content": "Never risk more than 2% of your account on a single trade. This keeps you in the game long-term.",
                "action": "next",
            },
            {
                "step": 3,
                "title": "Stop Loss Placement",
                "content": "Place stops below key support levels or the pattern's pivot point. Never move stops down!",
                "action": "next",
            },
            {
                "step": 4,
                "title": "Position Sizing",
                "content": "Legend AI calculates optimal position size based on your account size and risk tolerance.",
                "action": "complete",
                "tooltip_target": "#risk-calculator",
            },
        ],
    },
}

# Tooltip definitions for UI elements
TOOLTIPS = {
    "pattern-scanner": {
        "title": "Pattern Scanner",
        "content": "Scan thousands of stocks for profitable patterns in seconds",
        "placement": "bottom",
    },
    "vcp-score": {
        "title": "VCP Score",
        "content": "Higher scores (>80) indicate stronger patterns with better probability of success",
        "placement": "top",
    },
    "entry-price": {
        "title": "Entry Price",
        "content": "Recommended price to enter the trade based on pattern analysis",
        "placement": "top",
    },
    "stop-loss": {
        "title": "Stop Loss",
        "content": "Exit price to limit losses if trade doesn't work out",
        "placement": "top",
    },
    "risk-reward": {
        "title": "Risk/Reward Ratio",
        "content": "Aim for minimum 2:1 ratio. This means potential profit is 2x the potential loss",
        "placement": "top",
    },
    "volume-analysis": {
        "title": "Volume Analysis",
        "content": "Volume should decrease during consolidation and surge on breakout",
        "placement": "right",
    },
    "relative-strength": {
        "title": "Relative Strength",
        "content": "Measures stock performance vs. market. Look for RS > 70",
        "placement": "right",
    },
}


class TutorialService:
    """Service for managing tutorials and onboarding"""

    @staticmethod
    async def get_tutorial(tutorial_key: str) -> Optional[Dict[str, Any]]:
        """Get tutorial definition"""
        return TUTORIALS.get(tutorial_key)

    @staticmethod
    async def get_all_tutorials() -> List[Dict[str, Any]]:
        """Get all available tutorials"""
        return [
            {
                "key": tutorial["key"],
                "name": tutorial["name"],
                "description": tutorial["description"],
                "total_steps": len(tutorial["steps"]),
            }
            for tutorial in TUTORIALS.values()
        ]

    @staticmethod
    async def get_user_tutorial_progress(
        db: Session,
        user_id: str,
        tutorial_key: str
    ) -> Optional[Dict[str, Any]]:
        """Get user's progress in a tutorial"""
        progress = db.query(TutorialProgress).filter(
            TutorialProgress.user_id == user_id,
            TutorialProgress.tutorial_key == tutorial_key
        ).first()

        if not progress:
            return None

        tutorial = TUTORIALS.get(tutorial_key)
        if not tutorial:
            return None

        return {
            "tutorial_key": tutorial_key,
            "current_step": progress.step_number,
            "total_steps": len(tutorial["steps"]),
            "completed": progress.completed,
            "skipped": progress.skipped,
            "last_viewed_at": progress.last_viewed_at.isoformat() if progress.last_viewed_at else None,
        }

    @staticmethod
    async def start_tutorial(
        db: Session,
        user_id: str,
        tutorial_key: str
    ) -> Dict[str, Any]:
        """Start or resume a tutorial"""
        # Check if tutorial exists
        tutorial = TUTORIALS.get(tutorial_key)
        if not tutorial:
            raise ValueError(f"Tutorial '{tutorial_key}' not found")

        # Get or create progress
        progress = db.query(TutorialProgress).filter(
            TutorialProgress.user_id == user_id,
            TutorialProgress.tutorial_key == tutorial_key
        ).first()

        if not progress:
            progress = TutorialProgress(
                user_id=user_id,
                tutorial_key=tutorial_key,
                step_number=1
            )
            db.add(progress)
        else:
            # Reset if completed or skipped
            if progress.completed or progress.skipped:
                progress.step_number = 1
                progress.completed = False
                progress.skipped = False

        progress.last_viewed_at = datetime.utcnow()
        db.commit()
        db.refresh(progress)

        # Return first step
        current_step = tutorial["steps"][progress.step_number - 1]

        return {
            "tutorial": {
                "key": tutorial["key"],
                "name": tutorial["name"],
                "description": tutorial["description"],
            },
            "current_step": progress.step_number,
            "total_steps": len(tutorial["steps"]),
            "step_data": current_step,
        }

    @staticmethod
    async def next_step(
        db: Session,
        user_id: str,
        tutorial_key: str
    ) -> Dict[str, Any]:
        """Move to next tutorial step"""
        tutorial = TUTORIALS.get(tutorial_key)
        if not tutorial:
            raise ValueError(f"Tutorial '{tutorial_key}' not found")

        progress = db.query(TutorialProgress).filter(
            TutorialProgress.user_id == user_id,
            TutorialProgress.tutorial_key == tutorial_key
        ).first()

        if not progress:
            raise ValueError("Tutorial not started")

        # Move to next step
        progress.step_number += 1
        progress.last_viewed_at = datetime.utcnow()

        # Check if completed
        if progress.step_number > len(tutorial["steps"]):
            progress.completed = True
            progress.completed_at = datetime.utcnow()
            db.commit()

            return {
                "completed": True,
                "tutorial_key": tutorial_key,
            }

        db.commit()
        db.refresh(progress)

        # Return next step
        current_step = tutorial["steps"][progress.step_number - 1]

        return {
            "tutorial": {
                "key": tutorial["key"],
                "name": tutorial["name"],
            },
            "current_step": progress.step_number,
            "total_steps": len(tutorial["steps"]),
            "step_data": current_step,
            "completed": False,
        }

    @staticmethod
    async def skip_tutorial(
        db: Session,
        user_id: str,
        tutorial_key: str
    ) -> Dict[str, Any]:
        """Skip a tutorial"""
        progress = db.query(TutorialProgress).filter(
            TutorialProgress.user_id == user_id,
            TutorialProgress.tutorial_key == tutorial_key
        ).first()

        if not progress:
            # Create skipped record
            progress = TutorialProgress(
                user_id=user_id,
                tutorial_key=tutorial_key,
                step_number=0,
                skipped=True
            )
            db.add(progress)
        else:
            progress.skipped = True

        db.commit()

        return {
            "tutorial_key": tutorial_key,
            "skipped": True,
        }

    @staticmethod
    async def get_tooltip(tooltip_key: str) -> Optional[Dict[str, Any]]:
        """Get tooltip definition"""
        return TOOLTIPS.get(tooltip_key)

    @staticmethod
    async def get_all_tooltips() -> Dict[str, Dict[str, Any]]:
        """Get all tooltip definitions"""
        return TOOLTIPS

    @staticmethod
    async def should_show_onboarding(db: Session, user_id: str) -> bool:
        """Check if user should see onboarding tutorial"""
        # Check if user has started or completed onboarding
        progress = db.query(TutorialProgress).filter(
            TutorialProgress.user_id == user_id,
            TutorialProgress.tutorial_key == "onboarding"
        ).first()

        # Show onboarding if not started or if not completed/skipped
        if not progress:
            return True

        return not (progress.completed or progress.skipped)
