# Chart Recording and Sharing Feature

## Overview

The Chart Recording and Sharing feature allows users to record their chart analysis sessions, add annotations and voice-over narration, and share their analysis videos with others.

## Features

### 1. Screen Recording
- **Chart Capture**: Record chart area with high-quality video (WebM/VP9 format)
- **Voice-over Narration**: Optional audio recording for explaining analysis
- **Drawing Tools**: Real-time annotation tools during recording
- **Time-lapse Mode**: Speed up recording playback for longer sessions
- **Pause/Resume**: Control recording flow as needed

### 2. Annotation Tools
- **Text**: Add text labels to highlight key areas
- **Arrow**: Point to specific chart features
- **Highlight**: Emphasize important zones
- **Circle**: Mark significant points
- **Line**: Draw trend lines and support/resistance levels

### 3. Video Management
- **Cloud Storage**: Videos stored in `/app/data/recordings/`
- **Organization**: Filter by ticker symbol and user
- **Metadata**: Automatic capture of duration, resolution, file size
- **Thumbnails**: Auto-generated video thumbnails
- **Status Tracking**: Processing, ready, or failed states

### 4. Sharing Features
- **Shareable Links**: Unique token-based URLs for each recording
- **Embed Codes**: HTML iframe code for external websites
- **Public/Private**: Control recording visibility
- **View Tracking**: Monitor view counts and last viewed time
- **Social Media**: Export links for YouTube, Twitter, etc.

### 5. Playback Features
- **Speed Controls**: 0.25x to 2x playback speed
- **Bookmarks**: Navigate to specific timestamps
- **Annotation Timeline**: Visual markers for annotations
- **Interactive Overlays**: Annotations display at correct timestamps
- **Jump to Points**: Click bookmarks or annotations to seek

## API Endpoints

### Recording Management

#### Create Recording
```http
POST /api/recordings/create
Content-Type: application/json

{
  "ticker_symbol": "AAPL",
  "title": "AAPL Cup & Handle Breakout",
  "description": "Analysis of AAPL forming cup & handle pattern",
  "user_id": "default",
  "has_audio": true,
  "is_timelapse": false
}
```

#### Upload Video
```http
POST /api/recordings/{recording_id}/upload
Content-Type: multipart/form-data

video: <video_file.webm>
thumbnail: <thumbnail.jpg>
duration_seconds: 120
resolution: "1920x1080"
```

#### Add Annotations
```http
POST /api/recordings/{recording_id}/annotations
Content-Type: application/json

[
  {
    "timestamp": 15.5,
    "type": "arrow",
    "data": {
      "endX": 200,
      "endY": 150,
      "color": "#FF0000"
    },
    "position": {"x": 100, "y": 100}
  }
]
```

#### Add Bookmarks
```http
POST /api/recordings/{recording_id}/bookmarks
Content-Type: application/json

[
  {
    "timestamp": 30.0,
    "label": "Breakout Point",
    "description": "Price breaks above resistance"
  }
]
```

### Viewing and Sharing

#### Get Recording
```http
GET /api/recordings/{recording_id}
```

#### View by Share Token
```http
GET /api/recordings/view/{share_token}
```

#### List Recordings
```http
GET /api/recordings/list?ticker_symbol=AAPL&limit=20&offset=0
```

#### Get Embed Code
```http
GET /api/recordings/{recording_id}/embed-code?base_url=https://yoursite.com
```

#### Update Share Settings
```http
PUT /api/recordings/{recording_id}/share-settings
Content-Type: application/json

{
  "is_public": true,
  "embed_enabled": true
}
```

#### Add Social Link
```http
POST /api/recordings/{recording_id}/social-link
Content-Type: application/json

{
  "platform": "youtube",
  "url": "https://youtube.com/watch?v=..."
}
```

#### Delete Recording
```http
DELETE /api/recordings/{recording_id}
```

## Database Schema

### chart_recordings Table

```sql
CREATE TABLE chart_recordings (
    id SERIAL PRIMARY KEY,
    ticker_id INTEGER REFERENCES tickers(id),
    user_id VARCHAR(100),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    ticker_symbol VARCHAR(10),

    -- Video metadata
    video_url TEXT NOT NULL,
    thumbnail_url TEXT,
    duration_seconds INTEGER,
    file_size_bytes INTEGER,
    video_format VARCHAR(20) DEFAULT 'webm',
    resolution VARCHAR(20),

    -- Recording features
    has_annotations BOOLEAN DEFAULT FALSE,
    has_audio BOOLEAN DEFAULT FALSE,
    is_timelapse BOOLEAN DEFAULT FALSE,
    playback_speed FLOAT DEFAULT 1.0,

    -- Annotations and bookmarks (JSON)
    annotations JSON,
    bookmarks JSON,
    drawing_data JSON,

    -- Sharing
    share_token VARCHAR(100) UNIQUE,
    is_public BOOLEAN DEFAULT FALSE,
    view_count INTEGER DEFAULT 0,
    embed_enabled BOOLEAN DEFAULT TRUE,

    -- Social sharing
    youtube_url TEXT,
    twitter_url TEXT,

    -- Status
    status VARCHAR(20) DEFAULT 'processing',
    error_message TEXT,

    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    last_viewed_at TIMESTAMP WITH TIME ZONE
);
```

## Frontend Usage

### Access the UI

Navigate to: `http://localhost:8000/recordings/ui`

### Recording Workflow

1. **Enter Details**:
   - Ticker symbol
   - Recording title
   - Description (optional)
   - Enable audio/time-lapse (optional)

2. **Start Recording**:
   - Click "Start Recording" button
   - Grant screen capture permissions
   - Select the chart area to record

3. **Annotate During Recording**:
   - Use drawing tools to annotate
   - Add bookmarks at key moments
   - Add voice narration if audio enabled

4. **Stop and Save**:
   - Click "Stop & Save"
   - Video is processed and uploaded
   - Thumbnail is auto-generated
   - Annotations and bookmarks are saved

5. **Share**:
   - Copy shareable link
   - Get embed code
   - Export to social media

### JavaScript Integration

```javascript
// Initialize recorder
const recorder = new ChartRecorder();

await recorder.init('chart-container', {
    includeAudio: true,
    timeLapse: false
});

// Start recording
await recorder.startRecording();

// Add annotation
recorder.addAnnotation('text', {
    text: 'Breakout!',
    color: '#FF0000',
    font: '20px Arial'
}, { x: 100, y: 100 });

// Add bookmark
recorder.addBookmark('Key Level', 'Support level tested');

// Stop and upload
const recording = await recorder.completeRecording(
    'AAPL',
    'My Analysis',
    'Detailed description'
);
```

### Video Player

```javascript
// Initialize player
const player = new RecordingPlayer('player-container');

// Load recording
await player.init(recordingId);

// Control playback
player.setPlaybackSpeed(1.5);
player.seekTo(30.0);
player.play();
```

## File Storage

- **Location**: `/app/data/recordings/`
- **Video Files**: `recording_{id}_{uuid}.webm`
- **Thumbnails**: `thumb_{id}_{uuid}.jpg`
- **Access**: Files served via `/recordings/` mount point

## Migration

Run the migration script to create the database table:

```bash
python scripts/migrate_chart_recordings.py
```

Or, the table will be auto-created on app startup via SQLAlchemy's `create_all()`.

## Security Considerations

1. **Share Tokens**: 32-character SHA256 hash for security
2. **Public/Private**: Control who can view recordings
3. **User Isolation**: Recordings filtered by user_id
4. **File Access**: Static files served only through configured routes
5. **Input Validation**: Pydantic models validate all API inputs

## Browser Requirements

- **Screen Capture API**: Chrome 72+, Firefox 66+, Safari 13+
- **MediaRecorder API**: Modern browsers with VP9 codec support
- **Canvas API**: For annotation overlay
- **File API**: For video upload

## Future Enhancements

1. **Video Editing**: Trim, cut, and merge recordings
2. **Cloud Upload**: S3, Cloudinary, or YouTube direct upload
3. **Real-time Collaboration**: Multiple users annotating together
4. **AI Transcription**: Auto-generate captions from audio
5. **Template Library**: Pre-made annotation templates
6. **Mobile Support**: iOS/Android recording capabilities

## Troubleshooting

### Recording Not Starting
- Ensure browser permissions for screen capture
- Check console for errors
- Verify WebM/VP9 codec support

### Upload Failing
- Check file size limits
- Verify network connectivity
- Ensure storage path exists and is writable

### Annotations Not Appearing
- Verify annotations array is not empty
- Check timestamp values are within video duration
- Ensure canvas overlay is properly positioned

## Support

For issues or feature requests, contact the development team or file an issue in the repository.
