"""
Chart Recording API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from pathlib import Path
import logging

from app.services.database import get_db
from app.services.chart_recording import ChartRecordingService
from app.models import ChartRecording

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/recordings", tags=["Chart Recordings"])
recording_service = ChartRecordingService()

# Template path for recording UI
TEMPLATE_PATH = Path(__file__).resolve().parents[2] / "templates" / "chart_recording.html"


# Pydantic Models
class RecordingCreate(BaseModel):
    ticker_symbol: str = Field(..., description="Stock ticker symbol")
    title: str = Field(..., description="Recording title")
    description: Optional[str] = Field(None, description="Recording description")
    user_id: str = Field(default="default", description="User ID")
    has_audio: bool = Field(default=False, description="Recording has audio")
    is_timelapse: bool = Field(default=False, description="Is time-lapse recording")


class RecordingResponse(BaseModel):
    id: int
    ticker_symbol: str
    title: str
    description: Optional[str]
    video_url: str
    thumbnail_url: Optional[str]
    duration_seconds: Optional[int]
    file_size_bytes: Optional[int]
    resolution: Optional[str]
    has_annotations: bool
    has_audio: bool
    is_timelapse: bool
    share_token: str
    is_public: bool
    view_count: int
    embed_enabled: bool
    youtube_url: Optional[str]
    twitter_url: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class AnnotationData(BaseModel):
    timestamp: float = Field(..., description="Timestamp in seconds")
    type: str = Field(..., description="Annotation type (text, arrow, highlight, etc.)")
    data: Dict[str, Any] = Field(..., description="Annotation data")
    position: Optional[Dict[str, float]] = Field(None, description="Position {x, y}")


class BookmarkData(BaseModel):
    timestamp: float = Field(..., description="Timestamp in seconds")
    label: str = Field(..., description="Bookmark label")
    description: Optional[str] = Field(None, description="Bookmark description")


class ShareSettings(BaseModel):
    is_public: Optional[bool] = None
    embed_enabled: Optional[bool] = None


class SocialLinkData(BaseModel):
    platform: str = Field(..., description="Platform (youtube, twitter)")
    url: str = Field(..., description="Social media URL")


# Endpoints
@router.post("/create", response_model=RecordingResponse)
async def create_recording(
    data: RecordingCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new chart recording"""

    recording = await recording_service.create_recording(
        db=db,
        ticker_symbol=data.ticker_symbol,
        title=data.title,
        user_id=data.user_id,
        description=data.description,
        has_audio=data.has_audio,
        is_timelapse=data.is_timelapse
    )

    return recording


@router.post("/{recording_id}/upload", response_model=RecordingResponse)
async def upload_video(
    recording_id: int,
    video: UploadFile = File(...),
    thumbnail: Optional[UploadFile] = File(None),
    duration_seconds: Optional[int] = Form(None),
    resolution: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """Upload video file for recording"""

    # Get recording
    recording = await recording_service.get_recording(db, recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")

    # Determine format from filename
    format = video.filename.split('.')[-1] if video.filename else "webm"

    # Read video data
    video_data = await video.read()
    file_size = len(video_data)

    # Save video file
    video_url = await recording_service.save_video_file(
        recording_id=recording_id,
        video_data=video_data,
        format=format,
        resolution=resolution
    )

    # Save thumbnail if provided
    thumbnail_url = None
    if thumbnail:
        thumbnail_data = await thumbnail.read()
        thumb_format = thumbnail.filename.split('.')[-1] if thumbnail.filename else "jpg"
        thumbnail_url = await recording_service.save_thumbnail(
            recording_id=recording_id,
            thumbnail_data=thumbnail_data,
            format=thumb_format
        )

    # Update recording metadata
    updated_recording = await recording_service.update_recording_metadata(
        db=db,
        recording_id=recording_id,
        video_url=video_url,
        thumbnail_url=thumbnail_url,
        duration_seconds=duration_seconds,
        file_size_bytes=file_size,
        resolution=resolution,
        video_format=format
    )

    return updated_recording


@router.post("/{recording_id}/annotations", response_model=RecordingResponse)
async def add_annotations(
    recording_id: int,
    annotations: List[AnnotationData],
    db: AsyncSession = Depends(get_db)
):
    """Add annotations to recording"""

    recording = await recording_service.get_recording(db, recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")

    annotations_data = [ann.dict() for ann in annotations]
    updated_recording = await recording_service.add_annotations(
        db=db,
        recording_id=recording_id,
        annotations=annotations_data
    )

    return updated_recording


@router.post("/{recording_id}/bookmarks", response_model=RecordingResponse)
async def add_bookmarks(
    recording_id: int,
    bookmarks: List[BookmarkData],
    db: AsyncSession = Depends(get_db)
):
    """Add bookmarks to recording"""

    recording = await recording_service.get_recording(db, recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")

    bookmarks_data = [bm.dict() for bm in bookmarks]
    updated_recording = await recording_service.add_bookmarks(
        db=db,
        recording_id=recording_id,
        bookmarks=bookmarks_data
    )

    return updated_recording


@router.post("/{recording_id}/drawing-data")
async def save_drawing_data(
    recording_id: int,
    drawing_data: List[Dict[str, Any]],
    db: AsyncSession = Depends(get_db)
):
    """Save drawing tools replay data"""

    recording = await recording_service.get_recording(db, recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")

    await recording_service.save_drawing_data(
        db=db,
        recording_id=recording_id,
        drawing_data=drawing_data
    )

    return {"status": "success"}


@router.get("/{recording_id}", response_model=RecordingResponse)
async def get_recording(
    recording_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get recording by ID"""

    recording = await recording_service.get_recording(db, recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")

    return recording


@router.get("/view/{share_token}", response_model=RecordingResponse)
async def view_recording(
    share_token: str,
    db: AsyncSession = Depends(get_db)
):
    """View recording by share token (increments view count)"""

    recording = await recording_service.get_recording_by_token(db, share_token)
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")

    if not recording.is_public:
        raise HTTPException(status_code=403, detail="Recording is private")

    return recording


@router.get("/list", response_model=List[RecordingResponse])
async def list_recordings(
    ticker_symbol: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """List recordings with optional filters"""

    recordings = await recording_service.list_recordings(
        db=db,
        ticker_symbol=ticker_symbol,
        user_id=user_id,
        limit=limit,
        offset=offset
    )

    return recordings


@router.put("/{recording_id}/share-settings", response_model=RecordingResponse)
async def update_share_settings(
    recording_id: int,
    settings: ShareSettings,
    db: AsyncSession = Depends(get_db)
):
    """Update sharing settings"""

    recording = await recording_service.get_recording(db, recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")

    updated_recording = await recording_service.update_share_settings(
        db=db,
        recording_id=recording_id,
        is_public=settings.is_public,
        embed_enabled=settings.embed_enabled
    )

    return updated_recording


@router.post("/{recording_id}/social-link", response_model=RecordingResponse)
async def add_social_link(
    recording_id: int,
    link_data: SocialLinkData,
    db: AsyncSession = Depends(get_db)
):
    """Add social media link"""

    recording = await recording_service.get_recording(db, recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")

    updated_recording = await recording_service.add_social_link(
        db=db,
        recording_id=recording_id,
        platform=link_data.platform,
        url=link_data.url
    )

    return updated_recording


@router.delete("/{recording_id}")
async def delete_recording(
    recording_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete recording"""

    success = await recording_service.delete_recording(db, recording_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recording not found")

    return {"status": "deleted", "recording_id": recording_id}


@router.get("/{recording_id}/embed-code")
async def get_embed_code(
    recording_id: int,
    base_url: str = Query(..., description="Base URL for embed"),
    db: AsyncSession = Depends(get_db)
):
    """Get HTML embed code"""

    recording = await recording_service.get_recording(db, recording_id)
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")

    if not recording.embed_enabled:
        raise HTTPException(status_code=403, detail="Embedding is disabled")

    embed_code = recording_service.generate_embed_code(recording, base_url)
    share_url = recording_service.generate_share_url(recording, base_url)

    return {
        "embed_code": embed_code,
        "share_url": share_url,
        "share_token": recording.share_token
    }


# HTML UI Routes (not under /api prefix)
ui_router = APIRouter(prefix="/recordings", tags=["Recording UI"])


@ui_router.get("/ui", response_class=HTMLResponse)
async def get_recording_ui():
    """
    Serve the Chart Recording UI

    Features:
    - Screen recording with annotations
    - Voice-over narration support
    - Drawing tools replay
    - Time-lapse mode
    - Video management and editing
    - Sharing features (links, embeds, social media)
    - Enhanced playback with speed controls
    - Bookmarks and annotation navigation
    """
    try:
        html_content = TEMPLATE_PATH.read_text(encoding="utf-8")
        logger.info("🎥 Serving chart recording UI")
        return html_content
    except Exception as e:
        logger.error(f"Error loading recording UI: {e}")
        return f"""
        <html>
        <head>
            <title>Legend AI - Recording Error</title>
        </head>
        <body>
            <h1>Error Loading Recording UI</h1>
            <p>{str(e)}</p>
        </body>
        </html>
        """
