"""
Historical playback API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.services.playback import PlaybackEngine
from app.services.database import DatabaseService
from app.services.market_data import MarketDataService
from app.config import get_settings

router = APIRouter(prefix="/api/playback", tags=["Historical Playback"])


# Request/Response Models
class CreatePlaybackRequest(BaseModel):
    user_id: str = Field(..., description="User identifier")
    ticker: str = Field(..., description="Stock ticker symbol")
    start_date: str = Field(..., description="Start date (ISO format)")
    end_date: str = Field(..., description="End date (ISO format)")
    interval: str = Field(default="1day", description="Data interval")


class PlaybackControlRequest(BaseModel):
    speed: Optional[float] = Field(default=1.0, description="Playback speed multiplier")


class SeekRequest(BaseModel):
    target_date: str = Field(..., description="Target date to jump to (ISO format)")


class StepRequest(BaseModel):
    steps: int = Field(default=1, description="Number of bars to move (positive=forward, negative=backward)")


class AddAnnotationRequest(BaseModel):
    annotation_type: str = Field(..., description="Type of annotation")
    title: str = Field(..., description="Annotation title")
    content: str = Field(..., description="Annotation content")
    timestamp: Optional[str] = Field(None, description="Specific timestamp (ISO format)")
    price_level: Optional[float] = Field(None, description="Price level for marker")
    metadata: Optional[dict] = Field(None, description="Additional metadata")


class CreateBookmarkRequest(BaseModel):
    name: str = Field(..., description="Bookmark name")
    description: Optional[str] = Field(None, description="Bookmark description")
    tags: Optional[List[str]] = Field(None, description="Tags")


class ShareReplayRequest(BaseModel):
    title: str = Field(..., description="Share title")
    description: Optional[str] = Field(None, description="Share description")
    is_public: bool = Field(default=False, description="Public accessibility")
    expiration_days: Optional[int] = Field(None, description="Expiration in days")


# Dependency injection
def get_playback_engine() -> PlaybackEngine:
    settings = get_settings()
    db_service = DatabaseService(settings.database_url)
    market_data_service = MarketDataService(db_service)
    return PlaybackEngine(db_service, market_data_service)


@router.post("/create")
async def create_playback(
    request: CreatePlaybackRequest,
    engine: PlaybackEngine = Depends(get_playback_engine)
):
    """
    Create a new historical playback session

    Creates a new playback session for time-traveling through historical market data.
    """
    try:
        start_date = datetime.fromisoformat(request.start_date.replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(request.end_date.replace('Z', '+00:00'))

        result = await engine.create_playback(
            user_id=request.user_id,
            ticker_symbol=request.ticker,
            start_date=start_date,
            end_date=end_date,
            interval=request.interval
        )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{playback_id}/play")
async def play_playback(
    playback_id: int,
    request: PlaybackControlRequest,
    engine: PlaybackEngine = Depends(get_playback_engine)
):
    """
    Start or resume playback with optional speed control

    Speed multipliers: 0.5x (slow), 1x (normal), 2x (fast), 5x (very fast)
    """
    try:
        result = await engine.play(playback_id, request.speed)
        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{playback_id}/pause")
async def pause_playback(
    playback_id: int,
    engine: PlaybackEngine = Depends(get_playback_engine)
):
    """
    Pause playback

    Freezes playback at the current position.
    """
    try:
        result = await engine.pause(playback_id)
        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{playback_id}/seek")
async def seek_playback(
    playback_id: int,
    request: SeekRequest,
    engine: PlaybackEngine = Depends(get_playback_engine)
):
    """
    Jump to a specific point in time

    Allows instant navigation to any date within the playback range.
    """
    try:
        target_date = datetime.fromisoformat(request.target_date.replace('Z', '+00:00'))
        result = await engine.seek(playback_id, target_date)
        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{playback_id}/step")
async def step_playback(
    playback_id: int,
    request: StepRequest,
    engine: PlaybackEngine = Depends(get_playback_engine)
):
    """
    Move forward or backward by N bars

    Use positive steps to move forward, negative to move backward.
    """
    try:
        result = await engine.step(playback_id, request.steps)
        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{playback_id}/state")
async def get_playback_state(
    playback_id: int,
    engine: PlaybackEngine = Depends(get_playback_engine)
):
    """
    Get current playback state

    Returns current position, visible data, and playback controls.
    """
    try:
        result = await engine.get_playback_state(playback_id)
        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{playback_id}/annotate")
async def add_annotation(
    playback_id: int,
    request: AddAnnotationRequest,
    engine: PlaybackEngine = Depends(get_playback_engine)
):
    """
    Add an annotation to the playback

    Annotation types: note, entry, exit, pattern, support, resistance
    """
    try:
        timestamp = None
        if request.timestamp:
            timestamp = datetime.fromisoformat(request.timestamp.replace('Z', '+00:00'))

        result = await engine.add_annotation(
            playback_id=playback_id,
            annotation_type=request.annotation_type,
            title=request.title,
            content=request.content,
            timestamp=timestamp,
            price_level=request.price_level,
            metadata=request.metadata
        )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{playback_id}/annotations")
async def get_annotations(
    playback_id: int,
    engine: PlaybackEngine = Depends(get_playback_engine)
):
    """
    Get all annotations for a playback session

    Returns chronologically ordered list of all annotations.
    """
    try:
        result = await engine.get_annotations(playback_id)
        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{playback_id}/bookmark")
async def create_bookmark(
    playback_id: int,
    user_id: str,
    request: CreateBookmarkRequest,
    engine: PlaybackEngine = Depends(get_playback_engine)
):
    """
    Create a bookmark for a playback session

    Bookmarks allow quick access to important replay sessions.
    """
    try:
        result = await engine.create_bookmark(
            user_id=user_id,
            playback_id=playback_id,
            name=request.name,
            description=request.description,
            tags=request.tags
        )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{playback_id}/share")
async def share_replay(
    playback_id: int,
    user_id: str,
    request: ShareReplayRequest,
    engine: PlaybackEngine = Depends(get_playback_engine)
):
    """
    Create a shareable link for a replay

    Generates a unique share URL that can be sent to others.
    """
    try:
        result = await engine.share_replay(
            playback_id=playback_id,
            user_id=user_id,
            title=request.title,
            description=request.description,
            is_public=request.is_public,
            expiration_days=request.expiration_days
        )

        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/shared/{share_token}")
async def get_shared_replay(
    share_token: str,
    engine: PlaybackEngine = Depends(get_playback_engine)
):
    """
    Access a shared replay by token

    Public endpoint for accessing shared replays.
    """
    try:
        result = await engine.get_shared_replay(share_token)
        return {"success": True, "data": result}

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/user/{user_id}/list")
async def list_user_playbacks(
    user_id: str,
    limit: int = 50,
    engine: PlaybackEngine = Depends(get_playback_engine)
):
    """
    List all playback sessions for a user

    Returns most recent playback sessions.
    """
    try:
        result = await engine.list_user_playbacks(user_id, limit)
        return {"success": True, "data": result, "count": len(result)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
