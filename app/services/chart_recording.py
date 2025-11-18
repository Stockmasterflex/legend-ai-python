"""
Chart Recording Service
Handles screen recording, video processing, and sharing functionality
"""

import os
import uuid
import json
import logging
from typing import Optional, Dict, List, Any
from datetime import datetime
from pathlib import Path
import aiofiles
import hashlib

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models import ChartRecording, Ticker

logger = logging.getLogger(__name__)


class ChartRecordingService:
    """Service for managing chart recordings and analysis videos"""

    def __init__(self, storage_path: str = "/app/data/recordings"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _generate_share_token(self) -> str:
        """Generate unique share token"""
        return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:32]

    def _generate_filename(self, recording_id: int, format: str = "webm") -> str:
        """Generate unique filename for recording"""
        return f"recording_{recording_id}_{uuid.uuid4().hex[:8]}.{format}"

    async def create_recording(
        self,
        db: AsyncSession,
        ticker_symbol: str,
        title: str,
        user_id: str = "default",
        description: Optional[str] = None,
        has_audio: bool = False,
        is_timelapse: bool = False
    ) -> ChartRecording:
        """Create a new chart recording entry"""

        # Get ticker_id if exists
        ticker_id = None
        result = await db.execute(
            select(Ticker).where(Ticker.symbol == ticker_symbol.upper())
        )
        ticker = result.scalar_one_or_none()
        if ticker:
            ticker_id = ticker.id

        # Create recording entry
        recording = ChartRecording(
            ticker_id=ticker_id,
            ticker_symbol=ticker_symbol.upper(),
            user_id=user_id,
            title=title,
            description=description,
            video_url="",  # Will be updated after upload
            share_token=self._generate_share_token(),
            has_audio=has_audio,
            is_timelapse=is_timelapse,
            status="processing"
        )

        db.add(recording)
        await db.commit()
        await db.refresh(recording)

        logger.info(f"Created recording {recording.id} for {ticker_symbol}")
        return recording

    async def save_video_file(
        self,
        recording_id: int,
        video_data: bytes,
        format: str = "webm",
        resolution: Optional[str] = None
    ) -> str:
        """Save video file to storage"""

        filename = self._generate_filename(recording_id, format)
        filepath = self.storage_path / filename

        async with aiofiles.open(filepath, 'wb') as f:
            await f.write(video_data)

        logger.info(f"Saved video file: {filepath} ({len(video_data)} bytes)")

        return f"/recordings/{filename}"

    async def save_thumbnail(
        self,
        recording_id: int,
        thumbnail_data: bytes,
        format: str = "jpg"
    ) -> str:
        """Save thumbnail image"""

        filename = f"thumb_{recording_id}_{uuid.uuid4().hex[:8]}.{format}"
        filepath = self.storage_path / filename

        async with aiofiles.open(filepath, 'wb') as f:
            await f.write(thumbnail_data)

        logger.info(f"Saved thumbnail: {filepath}")

        return f"/recordings/{filename}"

    async def update_recording_metadata(
        self,
        db: AsyncSession,
        recording_id: int,
        video_url: str,
        thumbnail_url: Optional[str] = None,
        duration_seconds: Optional[int] = None,
        file_size_bytes: Optional[int] = None,
        resolution: Optional[str] = None,
        video_format: str = "webm"
    ) -> ChartRecording:
        """Update recording metadata after processing"""

        update_data = {
            "video_url": video_url,
            "status": "ready",
            "video_format": video_format
        }

        if thumbnail_url:
            update_data["thumbnail_url"] = thumbnail_url
        if duration_seconds:
            update_data["duration_seconds"] = duration_seconds
        if file_size_bytes:
            update_data["file_size_bytes"] = file_size_bytes
        if resolution:
            update_data["resolution"] = resolution

        await db.execute(
            update(ChartRecording)
            .where(ChartRecording.id == recording_id)
            .values(**update_data)
        )
        await db.commit()

        result = await db.execute(
            select(ChartRecording).where(ChartRecording.id == recording_id)
        )
        recording = result.scalar_one()

        logger.info(f"Updated recording {recording_id} metadata")
        return recording

    async def add_annotations(
        self,
        db: AsyncSession,
        recording_id: int,
        annotations: List[Dict[str, Any]]
    ) -> ChartRecording:
        """Add or update annotations to recording"""

        await db.execute(
            update(ChartRecording)
            .where(ChartRecording.id == recording_id)
            .values(
                annotations=annotations,
                has_annotations=True
            )
        )
        await db.commit()

        result = await db.execute(
            select(ChartRecording).where(ChartRecording.id == recording_id)
        )

        logger.info(f"Added {len(annotations)} annotations to recording {recording_id}")
        return result.scalar_one()

    async def add_bookmarks(
        self,
        db: AsyncSession,
        recording_id: int,
        bookmarks: List[Dict[str, Any]]
    ) -> ChartRecording:
        """Add bookmarks to recording"""

        await db.execute(
            update(ChartRecording)
            .where(ChartRecording.id == recording_id)
            .values(bookmarks=bookmarks)
        )
        await db.commit()

        result = await db.execute(
            select(ChartRecording).where(ChartRecording.id == recording_id)
        )

        logger.info(f"Added {len(bookmarks)} bookmarks to recording {recording_id}")
        return result.scalar_one()

    async def save_drawing_data(
        self,
        db: AsyncSession,
        recording_id: int,
        drawing_data: List[Dict[str, Any]]
    ) -> ChartRecording:
        """Save drawing tools replay data"""

        await db.execute(
            update(ChartRecording)
            .where(ChartRecording.id == recording_id)
            .values(drawing_data=drawing_data)
        )
        await db.commit()

        result = await db.execute(
            select(ChartRecording).where(ChartRecording.id == recording_id)
        )

        logger.info(f"Saved drawing data for recording {recording_id}")
        return result.scalar_one()

    async def get_recording(
        self,
        db: AsyncSession,
        recording_id: int
    ) -> Optional[ChartRecording]:
        """Get recording by ID"""

        result = await db.execute(
            select(ChartRecording).where(ChartRecording.id == recording_id)
        )
        return result.scalar_one_or_none()

    async def get_recording_by_token(
        self,
        db: AsyncSession,
        share_token: str
    ) -> Optional[ChartRecording]:
        """Get recording by share token"""

        result = await db.execute(
            select(ChartRecording).where(ChartRecording.share_token == share_token)
        )
        recording = result.scalar_one_or_none()

        # Increment view count
        if recording:
            await db.execute(
                update(ChartRecording)
                .where(ChartRecording.id == recording.id)
                .values(
                    view_count=ChartRecording.view_count + 1,
                    last_viewed_at=datetime.utcnow()
                )
            )
            await db.commit()

        return recording

    async def list_recordings(
        self,
        db: AsyncSession,
        ticker_symbol: Optional[str] = None,
        user_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[ChartRecording]:
        """List recordings with optional filters"""

        query = select(ChartRecording)

        if ticker_symbol:
            query = query.where(ChartRecording.ticker_symbol == ticker_symbol.upper())

        if user_id:
            query = query.where(ChartRecording.user_id == user_id)

        query = query.order_by(ChartRecording.created_at.desc()).limit(limit).offset(offset)

        result = await db.execute(query)
        return result.scalars().all()

    async def update_share_settings(
        self,
        db: AsyncSession,
        recording_id: int,
        is_public: Optional[bool] = None,
        embed_enabled: Optional[bool] = None
    ) -> ChartRecording:
        """Update sharing settings"""

        update_data = {}
        if is_public is not None:
            update_data["is_public"] = is_public
        if embed_enabled is not None:
            update_data["embed_enabled"] = embed_enabled

        if update_data:
            await db.execute(
                update(ChartRecording)
                .where(ChartRecording.id == recording_id)
                .values(**update_data)
            )
            await db.commit()

        result = await db.execute(
            select(ChartRecording).where(ChartRecording.id == recording_id)
        )

        logger.info(f"Updated share settings for recording {recording_id}")
        return result.scalar_one()

    async def add_social_link(
        self,
        db: AsyncSession,
        recording_id: int,
        platform: str,
        url: str
    ) -> ChartRecording:
        """Add social media link"""

        update_data = {}
        if platform == "youtube":
            update_data["youtube_url"] = url
        elif platform == "twitter":
            update_data["twitter_url"] = url

        if update_data:
            await db.execute(
                update(ChartRecording)
                .where(ChartRecording.id == recording_id)
                .values(**update_data)
            )
            await db.commit()

        result = await db.execute(
            select(ChartRecording).where(ChartRecording.id == recording_id)
        )

        logger.info(f"Added {platform} link for recording {recording_id}")
        return result.scalar_one()

    async def delete_recording(
        self,
        db: AsyncSession,
        recording_id: int
    ) -> bool:
        """Delete recording and associated files"""

        recording = await self.get_recording(db, recording_id)
        if not recording:
            return False

        # Delete files
        if recording.video_url:
            filepath = self.storage_path / Path(recording.video_url).name
            if filepath.exists():
                filepath.unlink()

        if recording.thumbnail_url:
            filepath = self.storage_path / Path(recording.thumbnail_url).name
            if filepath.exists():
                filepath.unlink()

        # Delete database entry
        await db.delete(recording)
        await db.commit()

        logger.info(f"Deleted recording {recording_id}")
        return True

    def generate_embed_code(self, recording: ChartRecording, base_url: str) -> str:
        """Generate HTML embed code"""

        embed_url = f"{base_url}/recordings/embed/{recording.share_token}"

        return f"""<iframe
    src="{embed_url}"
    width="800"
    height="600"
    frameborder="0"
    allowfullscreen
></iframe>"""

    def generate_share_url(self, recording: ChartRecording, base_url: str) -> str:
        """Generate shareable URL"""

        return f"{base_url}/recordings/view/{recording.share_token}"
