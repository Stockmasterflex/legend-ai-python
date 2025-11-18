"""
Historical playback engine for time-traveling through market data
Provides controlled replay of historical data with speed control and annotations
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import asyncio
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    HistoricalPlayback,
    PlaybackAnnotation,
    Ticker,
    ReplayBookmark,
    SharedReplay
)
from app.services.market_data import MarketDataService
from app.services.database import DatabaseService
import pandas as pd
import json
import secrets


class PlaybackEngine:
    """
    Historical data playback engine with speed control and pause/resume functionality
    """

    def __init__(self, db_service: DatabaseService, market_data_service: MarketDataService):
        self.db = db_service
        self.market_data = market_data_service
        self.active_playbacks: Dict[int, Dict[str, Any]] = {}  # In-memory playback state

    async def create_playback(
        self,
        user_id: str,
        ticker_symbol: str,
        start_date: datetime,
        end_date: datetime,
        interval: str = "1day"
    ) -> Dict[str, Any]:
        """
        Create a new historical playback session

        Args:
            user_id: User identifier
            ticker_symbol: Stock ticker
            start_date: Beginning of playback period
            end_date: End of playback period
            interval: Data interval (1min, 5min, 1hour, 1day)

        Returns:
            Playback session data including ID and initial state
        """
        # Get or create ticker
        with self.db.get_db() as session:
            ticker = session.query(Ticker).filter(Ticker.symbol == ticker_symbol.upper()).first()
            if not ticker:
                ticker = Ticker(symbol=ticker_symbol.upper(), name=ticker_symbol.upper())
                session.add(ticker)
                session.commit()
                session.refresh(ticker)

            # Create playback session
            playback = HistoricalPlayback(
                user_id=user_id,
                ticker_id=ticker.id,
                start_date=start_date,
                end_date=end_date,
                current_position=start_date,
                interval=interval,
                status="paused",
                playback_speed=1.0
            )
            session.add(playback)
            session.commit()
            session.refresh(playback)

            playback_id = playback.id

        # Fetch historical data
        await self._load_playback_data(playback_id, ticker_symbol, start_date, end_date, interval)

        return {
            "playback_id": playback_id,
            "ticker": ticker_symbol,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "current_position": start_date.isoformat(),
            "status": "paused",
            "interval": interval,
            "playback_speed": 1.0
        }

    async def _load_playback_data(
        self,
        playback_id: int,
        ticker: str,
        start_date: datetime,
        end_date: datetime,
        interval: str
    ):
        """Load and cache historical data for playback"""
        # Calculate required bars
        days_diff = (end_date - start_date).days
        outputsize = max(100, min(5000, days_diff + 50))  # Buffer for safety

        # Fetch data from market data service
        data = await self.market_data.get_time_series(
            ticker=ticker,
            interval=interval,
            outputsize=outputsize
        )

        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame({
            'timestamp': pd.to_datetime(data['t'], unit='s'),
            'open': data['o'],
            'high': data['h'],
            'low': data['l'],
            'close': data['c'],
            'volume': data['v']
        })

        # Filter to requested date range
        df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]
        df = df.sort_values('timestamp').reset_index(drop=True)

        # Store in active playbacks
        self.active_playbacks[playback_id] = {
            'data': df,
            'current_index': 0,
            'status': 'paused',
            'speed': 1.0
        }

    async def play(self, playback_id: int, speed: float = 1.0) -> Dict[str, Any]:
        """
        Start or resume playback

        Args:
            playback_id: Playback session ID
            speed: Playback speed multiplier (0.5x, 1x, 2x, etc.)

        Returns:
            Updated playback state
        """
        with self.db.get_db() as session:
            playback = session.get(HistoricalPlayback, playback_id)
            if not playback:
                raise ValueError(f"Playback {playback_id} not found")

            playback.status = "playing"
            playback.playback_speed = speed
            session.commit()

        if playback_id in self.active_playbacks:
            self.active_playbacks[playback_id]['status'] = 'playing'
            self.active_playbacks[playback_id]['speed'] = speed

        return await self.get_playback_state(playback_id)

    async def pause(self, playback_id: int) -> Dict[str, Any]:
        """Pause playback"""
        with self.db.get_db() as session:
            playback = session.get(HistoricalPlayback, playback_id)
            if not playback:
                raise ValueError(f"Playback {playback_id} not found")

            playback.status = "paused"
            session.commit()

        if playback_id in self.active_playbacks:
            self.active_playbacks[playback_id]['status'] = 'paused'

        return await self.get_playback_state(playback_id)

    async def seek(self, playback_id: int, target_date: datetime) -> Dict[str, Any]:
        """
        Jump to a specific point in time

        Args:
            playback_id: Playback session ID
            target_date: Date/time to jump to

        Returns:
            Updated playback state
        """
        if playback_id not in self.active_playbacks:
            raise ValueError(f"Playback {playback_id} not loaded")

        df = self.active_playbacks[playback_id]['data']

        # Find closest timestamp
        closest_idx = (df['timestamp'] - target_date).abs().argmin()

        self.active_playbacks[playback_id]['current_index'] = closest_idx

        with self.db.get_db() as session:
            playback = session.get(HistoricalPlayback, playback_id)
            if playback:
                playback.current_position = df.iloc[closest_idx]['timestamp']
                session.commit()

        return await self.get_playback_state(playback_id)

    async def step(self, playback_id: int, steps: int = 1) -> Dict[str, Any]:
        """
        Move forward/backward by N bars

        Args:
            playback_id: Playback session ID
            steps: Number of bars to move (positive=forward, negative=backward)

        Returns:
            Updated playback state with new data
        """
        if playback_id not in self.active_playbacks:
            raise ValueError(f"Playback {playback_id} not loaded")

        state = self.active_playbacks[playback_id]
        df = state['data']

        # Calculate new index
        new_index = max(0, min(len(df) - 1, state['current_index'] + steps))
        state['current_index'] = new_index

        # Update database
        with self.db.get_db() as session:
            playback = session.get(HistoricalPlayback, playback_id)
            if playback:
                playback.current_position = df.iloc[new_index]['timestamp']
                session.commit()

        return await self.get_playback_state(playback_id)

    async def get_playback_state(self, playback_id: int) -> Dict[str, Any]:
        """Get current playback state including visible data"""
        with self.db.get_db() as session:
            playback = session.get(HistoricalPlayback, playback_id)
            if not playback:
                raise ValueError(f"Playback {playback_id} not found")

            ticker = session.get(Ticker, playback.ticker_id)

            state = {
                "playback_id": playback.id,
                "ticker": ticker.symbol if ticker else "UNKNOWN",
                "start_date": playback.start_date.isoformat(),
                "end_date": playback.end_date.isoformat(),
                "current_position": playback.current_position.isoformat(),
                "status": playback.status,
                "playback_speed": playback.playback_speed,
                "interval": playback.interval
            }

        # Add current data if loaded
        if playback_id in self.active_playbacks:
            memory_state = self.active_playbacks[playback_id]
            df = memory_state['data']
            current_idx = memory_state['current_index']

            # Return data up to current position (simulating "present")
            visible_data = df.iloc[:current_idx + 1]

            state['current_bar'] = {
                'timestamp': df.iloc[current_idx]['timestamp'].isoformat(),
                'open': float(df.iloc[current_idx]['open']),
                'high': float(df.iloc[current_idx]['high']),
                'low': float(df.iloc[current_idx]['low']),
                'close': float(df.iloc[current_idx]['close']),
                'volume': int(df.iloc[current_idx]['volume'])
            }

            state['visible_data'] = {
                'timestamps': visible_data['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist(),
                'open': visible_data['open'].tolist(),
                'high': visible_data['high'].tolist(),
                'low': visible_data['low'].tolist(),
                'close': visible_data['close'].tolist(),
                'volume': visible_data['volume'].tolist()
            }

            state['progress'] = {
                'current_bar': current_idx + 1,
                'total_bars': len(df),
                'percentage': round((current_idx + 1) / len(df) * 100, 2)
            }

        return state

    async def add_annotation(
        self,
        playback_id: int,
        annotation_type: str,
        title: str,
        content: str,
        timestamp: Optional[datetime] = None,
        price_level: Optional[float] = None,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Add an annotation to the playback

        Args:
            playback_id: Playback session ID
            annotation_type: Type of annotation (note, entry, exit, pattern, support, resistance)
            title: Annotation title
            content: Annotation content
            timestamp: Optional specific timestamp (defaults to current position)
            price_level: Optional price level for visual markers
            metadata: Optional additional metadata

        Returns:
            Created annotation
        """
        with self.db.get_db() as session:
            playback = session.get(HistoricalPlayback, playback_id)
            if not playback:
                raise ValueError(f"Playback {playback_id} not found")

            # Use current position if no timestamp specified
            if timestamp is None:
                timestamp = playback.current_position

            annotation = PlaybackAnnotation(
                playback_id=playback_id,
                timestamp=timestamp,
                annotation_type=annotation_type,
                title=title,
                content=content,
                price_level=price_level,
                metadata=json.dumps(metadata) if metadata else None
            )
            session.add(annotation)
            session.commit()
            session.refresh(annotation)

            return {
                "annotation_id": annotation.id,
                "playback_id": playback_id,
                "timestamp": annotation.timestamp.isoformat(),
                "type": annotation.annotation_type,
                "title": annotation.title,
                "content": annotation.content,
                "price_level": annotation.price_level,
                "metadata": json.loads(annotation.metadata) if annotation.metadata else None
            }

    async def get_annotations(self, playback_id: int) -> List[Dict[str, Any]]:
        """Get all annotations for a playback session"""
        with self.db.get_db() as session:
            annotations = session.query(PlaybackAnnotation).filter(
                PlaybackAnnotation.playback_id == playback_id
            ).order_by(PlaybackAnnotation.timestamp).all()

            return [
                {
                    "annotation_id": ann.id,
                    "timestamp": ann.timestamp.isoformat(),
                    "type": ann.annotation_type,
                    "title": ann.title,
                    "content": ann.content,
                    "price_level": ann.price_level,
                    "metadata": json.loads(ann.metadata) if ann.metadata else None
                }
                for ann in annotations
            ]

    async def create_bookmark(
        self,
        user_id: str,
        playback_id: int,
        name: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create a bookmark for a playback session"""
        with self.db.get_db() as session:
            bookmark = ReplayBookmark(
                user_id=user_id,
                playback_id=playback_id,
                bookmark_name=name,
                description=description,
                tags=json.dumps(tags) if tags else None
            )
            session.add(bookmark)
            session.commit()
            session.refresh(bookmark)

            return {
                "bookmark_id": bookmark.id,
                "playback_id": playback_id,
                "name": bookmark.bookmark_name,
                "description": bookmark.description,
                "tags": json.loads(bookmark.tags) if bookmark.tags else [],
                "created_at": bookmark.created_at.isoformat()
            }

    async def share_replay(
        self,
        playback_id: int,
        user_id: str,
        title: str,
        description: Optional[str] = None,
        is_public: bool = False,
        expiration_days: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create a shareable link for a replay

        Args:
            playback_id: Playback session ID
            user_id: User creating the share
            title: Share title
            description: Optional description
            is_public: Whether the replay is publicly accessible
            expiration_days: Optional expiration in days

        Returns:
            Share information including unique token
        """
        share_token = secrets.token_urlsafe(32)

        expiration_date = None
        if expiration_days:
            expiration_date = datetime.utcnow() + timedelta(days=expiration_days)

        with self.db.get_db() as session:
            shared_replay = SharedReplay(
                playback_id=playback_id,
                share_token=share_token,
                shared_by=user_id,
                title=title,
                description=description,
                is_public=is_public,
                expiration_date=expiration_date
            )
            session.add(shared_replay)
            session.commit()
            session.refresh(shared_replay)

            return {
                "share_id": shared_replay.id,
                "share_token": share_token,
                "share_url": f"/replay/shared/{share_token}",
                "title": title,
                "is_public": is_public,
                "expiration_date": expiration_date.isoformat() if expiration_date else None,
                "created_at": shared_replay.created_at.isoformat()
            }

    async def get_shared_replay(self, share_token: str) -> Dict[str, Any]:
        """Get a shared replay by its token"""
        with self.db.get_db() as session:
            shared = session.query(SharedReplay).filter(
                SharedReplay.share_token == share_token
            ).first()

            if not shared:
                raise ValueError("Shared replay not found")

            # Check expiration
            if shared.expiration_date and shared.expiration_date < datetime.utcnow():
                raise ValueError("Shared replay has expired")

            # Increment view count
            shared.view_count += 1
            session.commit()

            # Get playback data
            playback = session.get(HistoricalPlayback, shared.playback_id)
            ticker = session.get(Ticker, playback.ticker_id)

            return {
                "share_id": shared.id,
                "title": shared.title,
                "description": shared.description,
                "shared_by": shared.shared_by,
                "view_count": shared.view_count,
                "playback": {
                    "playback_id": playback.id,
                    "ticker": ticker.symbol,
                    "start_date": playback.start_date.isoformat(),
                    "end_date": playback.end_date.isoformat(),
                    "interval": playback.interval
                }
            }

    async def list_user_playbacks(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """List all playback sessions for a user"""
        with self.db.get_db() as session:
            playbacks = session.query(HistoricalPlayback).filter(
                HistoricalPlayback.user_id == user_id
            ).order_by(HistoricalPlayback.created_at.desc()).limit(limit).all()

            result = []
            for playback in playbacks:
                ticker = session.get(Ticker, playback.ticker_id)
                result.append({
                    "playback_id": playback.id,
                    "ticker": ticker.symbol if ticker else "UNKNOWN",
                    "start_date": playback.start_date.isoformat(),
                    "end_date": playback.end_date.isoformat(),
                    "current_position": playback.current_position.isoformat(),
                    "status": playback.status,
                    "interval": playback.interval,
                    "created_at": playback.created_at.isoformat()
                })

            return result
