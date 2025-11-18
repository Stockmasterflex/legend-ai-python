"""
Pattern recognition training API endpoints
Educational quiz system for learning chart patterns
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List

from app.services.pattern_training import PatternTrainingEngine
from app.services.database import DatabaseService
from app.services.market_data import MarketDataService
from app.core.detector_factory import DetectorFactory
from app.config import get_settings

router = APIRouter(prefix="/api/training", tags=["Pattern Training"])


# Request/Response Models
class GenerateQuizRequest(BaseModel):
    ticker: Optional[str] = Field(None, description="Specific ticker (random if None)")
    difficulty: str = Field(default="medium", description="Difficulty: easy, medium, hard")
    pattern_type: Optional[str] = Field(None, description="Specific pattern to quiz on")


class SubmitAnswerRequest(BaseModel):
    user_id: str = Field(..., description="User identifier")
    answer: str = Field(..., description="User's answer")
    time_taken_seconds: Optional[int] = Field(None, description="Time taken to answer")


# Dependency injection
def get_training_engine() -> PatternTrainingEngine:
    settings = get_settings()
    db_service = DatabaseService(settings.database_url)
    market_data_service = MarketDataService(db_service)
    detector_factory = DetectorFactory()
    return PatternTrainingEngine(db_service, market_data_service, detector_factory)


@router.post("/quiz/generate")
async def generate_quiz(
    request: GenerateQuizRequest,
    engine: PatternTrainingEngine = Depends(get_training_engine)
):
    """
    Generate a pattern recognition quiz

    Creates a new quiz with a chart and multiple choice answers.
    Difficulty levels affect chart complexity and number of options.
    """
    try:
        result = await engine.generate_quiz(
            ticker_symbol=request.ticker,
            difficulty=request.difficulty,
            pattern_type=request.pattern_type
        )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/quiz/{quiz_id}/submit")
async def submit_answer(
    quiz_id: int,
    request: SubmitAnswerRequest,
    engine: PatternTrainingEngine = Depends(get_training_engine)
):
    """
    Submit and grade a quiz answer

    Returns whether the answer is correct, the explanation, and score.
    Score includes time bonus for quick answers.
    """
    try:
        result = await engine.submit_answer(
            quiz_id=quiz_id,
            user_id=request.user_id,
            user_answer=request.answer,
            time_taken_seconds=request.time_taken_seconds
        )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stats/{user_id}")
async def get_user_stats(
    user_id: str,
    engine: PatternTrainingEngine = Depends(get_training_engine)
):
    """
    Get training statistics for a user

    Returns comprehensive stats including accuracy, pattern-specific performance,
    streaks, strengths, and weaknesses.
    """
    try:
        result = await engine.get_user_stats(user_id)
        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/leaderboard")
async def get_leaderboard(
    limit: int = 10,
    engine: PatternTrainingEngine = Depends(get_training_engine)
):
    """
    Get top performers leaderboard

    Returns rankings based on average scores and accuracy.
    """
    try:
        result = await engine.get_leaderboard(limit)
        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/recommendations/{user_id}")
async def get_recommendations(
    user_id: str,
    engine: PatternTrainingEngine = Depends(get_training_engine)
):
    """
    Get personalized practice recommendations

    Returns tailored suggestions based on user's performance history.
    """
    try:
        result = await engine.get_practice_recommendations(user_id)
        return {"success": True, "data": {"recommendations": result}}

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/patterns")
async def list_pattern_types():
    """
    List all available pattern types for quizzes

    Returns complete list of patterns that can be tested.
    """
    return {
        "success": True,
        "data": {
            "patterns": PatternTrainingEngine.PATTERN_TYPES,
            "count": len(PatternTrainingEngine.PATTERN_TYPES)
        }
    }


@router.get("/difficulties")
async def list_difficulties():
    """
    List available difficulty levels

    Returns difficulty levels with their characteristics.
    """
    return {
        "success": True,
        "data": {
            "difficulties": {
                level: {
                    "bars": config["bars"],
                    "options_count": config["options_count"]
                }
                for level, config in PatternTrainingEngine.DIFFICULTY_LEVELS.items()
            }
        }
    }
