/**
 * Chart Recording Video Player
 * Enhanced video player with playback controls, annotations, and bookmarks
 */

class RecordingPlayer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            throw new Error(`Container ${containerId} not found`);
        }

        this.videoElement = null;
        this.recording = null;
        this.currentTime = 0;
        this.isPlaying = false;
        this.playbackSpeed = 1.0;
        this.annotationOverlay = null;
        this.bookmarksList = [];
    }

    /**
     * Initialize player with recording data
     */
    async init(recordingId) {
        // Fetch recording data
        this.recording = await this.fetchRecording(recordingId);

        // Build player UI
        this.buildPlayerUI();

        // Setup event listeners
        this.setupEventListeners();

        // Load annotations and bookmarks
        this.loadAnnotations();
        this.loadBookmarks();
    }

    /**
     * Fetch recording from API
     */
    async fetchRecording(recordingId) {
        try {
            const response = await fetch(`/api/recordings/${recordingId}`);
            if (!response.ok) {
                throw new Error(`Failed to fetch recording: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching recording:', error);
            throw error;
        }
    }

    /**
     * Build player UI
     */
    buildPlayerUI() {
        this.container.innerHTML = `
            <div class="recording-player">
                <!-- Video container -->
                <div class="video-container" style="position: relative;">
                    <video id="video-player" controls style="width: 100%; max-width: 100%;">
                        <source src="${this.recording.video_url}" type="video/${this.recording.video_format}">
                        Your browser does not support the video tag.
                    </video>

                    <!-- Annotation overlay -->
                    <canvas id="annotation-overlay" style="
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        pointer-events: none;
                    "></canvas>
                </div>

                <!-- Player controls -->
                <div class="player-controls" style="margin-top: 15px;">
                    <!-- Playback speed -->
                    <div class="speed-controls" style="margin-bottom: 10px;">
                        <label for="speed-select">Speed:</label>
                        <select id="speed-select" class="form-select form-select-sm" style="width: auto; display: inline-block;">
                            <option value="0.25">0.25x</option>
                            <option value="0.5">0.5x</option>
                            <option value="0.75">0.75x</option>
                            <option value="1" selected>1x</option>
                            <option value="1.25">1.25x</option>
                            <option value="1.5">1.5x</option>
                            <option value="2">2x</option>
                        </select>
                    </div>

                    <!-- Bookmarks -->
                    <div class="bookmarks-section" style="margin-bottom: 10px;">
                        <h6>Bookmarks</h6>
                        <div id="bookmarks-list"></div>
                    </div>

                    <!-- Annotation timeline -->
                    <div class="annotation-timeline" style="margin-bottom: 10px;">
                        <h6>Annotations Timeline</h6>
                        <div id="annotation-markers" style="
                            position: relative;
                            height: 20px;
                            background: #f0f0f0;
                            border-radius: 4px;
                        "></div>
                    </div>
                </div>

                <!-- Recording info -->
                <div class="recording-info" style="margin-top: 15px;">
                    <h5>${this.recording.title}</h5>
                    <p class="text-muted">${this.recording.description || ''}</p>
                    <div class="meta-info">
                        <span class="badge bg-primary">${this.recording.ticker_symbol}</span>
                        <span class="badge bg-secondary">${this.formatDuration(this.recording.duration_seconds)}</span>
                        <span class="badge bg-info">${this.recording.view_count} views</span>
                        ${this.recording.has_annotations ? '<span class="badge bg-success">Annotated</span>' : ''}
                        ${this.recording.has_audio ? '<span class="badge bg-warning">Audio</span>' : ''}
                    </div>
                </div>

                <!-- Share options -->
                <div class="share-options" style="margin-top: 15px;">
                    <h6>Share</h6>
                    <div class="btn-group" role="group">
                        <button id="copy-link-btn" class="btn btn-sm btn-outline-primary">Copy Link</button>
                        <button id="get-embed-btn" class="btn btn-sm btn-outline-secondary">Get Embed Code</button>
                        ${this.recording.youtube_url ? `<a href="${this.recording.youtube_url}" target="_blank" class="btn btn-sm btn-outline-danger">YouTube</a>` : ''}
                    </div>
                </div>
            </div>
        `;

        this.videoElement = document.getElementById('video-player');
        this.annotationOverlay = document.getElementById('annotation-overlay');
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Video playback events
        this.videoElement.addEventListener('timeupdate', () => {
            this.currentTime = this.videoElement.currentTime;
            this.updateAnnotationOverlay();
        });

        this.videoElement.addEventListener('play', () => {
            this.isPlaying = true;
        });

        this.videoElement.addEventListener('pause', () => {
            this.isPlaying = false;
        });

        // Speed control
        const speedSelect = document.getElementById('speed-select');
        speedSelect.addEventListener('change', (e) => {
            this.setPlaybackSpeed(parseFloat(e.target.value));
        });

        // Copy link button
        const copyLinkBtn = document.getElementById('copy-link-btn');
        copyLinkBtn.addEventListener('click', () => {
            this.copyShareLink();
        });

        // Embed code button
        const getEmbedBtn = document.getElementById('get-embed-btn');
        getEmbedBtn.addEventListener('click', () => {
            this.showEmbedCode();
        });
    }

    /**
     * Load and display annotations
     */
    loadAnnotations() {
        if (!this.recording.annotations || this.recording.annotations.length === 0) {
            return;
        }

        const timeline = document.getElementById('annotation-markers');
        const duration = this.recording.duration_seconds;

        this.recording.annotations.forEach((annotation, index) => {
            const position = (annotation.timestamp / duration) * 100;

            const marker = document.createElement('div');
            marker.style.cssText = `
                position: absolute;
                left: ${position}%;
                top: 0;
                width: 3px;
                height: 100%;
                background: #FF0000;
                cursor: pointer;
            `;
            marker.title = `${annotation.type} at ${this.formatTime(annotation.timestamp)}`;
            marker.addEventListener('click', () => {
                this.seekTo(annotation.timestamp);
            });

            timeline.appendChild(marker);
        });
    }

    /**
     * Load and display bookmarks
     */
    loadBookmarks() {
        if (!this.recording.bookmarks || this.recording.bookmarks.length === 0) {
            document.getElementById('bookmarks-list').innerHTML = '<p class="text-muted">No bookmarks</p>';
            return;
        }

        const bookmarksList = document.getElementById('bookmarks-list');
        bookmarksList.innerHTML = '';

        this.recording.bookmarks.forEach((bookmark, index) => {
            const bookmarkElement = document.createElement('div');
            bookmarkElement.className = 'bookmark-item';
            bookmarkElement.style.cssText = `
                padding: 8px;
                margin-bottom: 5px;
                background: #f8f9fa;
                border-radius: 4px;
                cursor: pointer;
            `;
            bookmarkElement.innerHTML = `
                <strong>${bookmark.label}</strong>
                <span class="text-muted ms-2">${this.formatTime(bookmark.timestamp)}</span>
                ${bookmark.description ? `<p class="mb-0 small">${bookmark.description}</p>` : ''}
            `;
            bookmarkElement.addEventListener('click', () => {
                this.seekTo(bookmark.timestamp);
            });

            bookmarksList.appendChild(bookmarkElement);
        });
    }

    /**
     * Update annotation overlay based on current time
     */
    updateAnnotationOverlay() {
        if (!this.recording.annotations || this.recording.annotations.length === 0) {
            return;
        }

        const canvas = this.annotationOverlay;
        const ctx = canvas.getContext('2d');

        // Match canvas size to video
        const rect = this.videoElement.getBoundingClientRect();
        canvas.width = rect.width;
        canvas.height = rect.height;

        // Clear previous annotations
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw active annotations (with 2-second display window)
        const activeAnnotations = this.recording.annotations.filter(ann =>
            Math.abs(ann.timestamp - this.currentTime) < 2
        );

        activeAnnotations.forEach(annotation => {
            this.drawAnnotation(ctx, annotation);
        });
    }

    /**
     * Draw annotation on canvas
     */
    drawAnnotation(ctx, annotation) {
        const { type, data, position } = annotation;

        ctx.save();

        switch (type) {
            case 'text':
                ctx.font = data.font || '16px Arial';
                ctx.fillStyle = data.color || '#FF0000';
                ctx.fillText(data.text, position.x, position.y);
                break;

            case 'arrow':
                this.drawArrow(ctx, position.x, position.y, data.endX, data.endY, data.color || '#FF0000');
                break;

            case 'highlight':
                ctx.fillStyle = data.color || 'rgba(255, 255, 0, 0.3)';
                ctx.fillRect(position.x, position.y, data.width, data.height);
                break;

            case 'circle':
                ctx.strokeStyle = data.color || '#FF0000';
                ctx.lineWidth = data.width || 2;
                ctx.beginPath();
                ctx.arc(position.x, position.y, data.radius, 0, 2 * Math.PI);
                ctx.stroke();
                break;
        }

        ctx.restore();
    }

    /**
     * Draw arrow helper
     */
    drawArrow(ctx, fromX, fromY, toX, toY, color) {
        const headlen = 10;
        const angle = Math.atan2(toY - fromY, toX - fromX);

        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(fromX, fromY);
        ctx.lineTo(toX, toY);
        ctx.lineTo(toX - headlen * Math.cos(angle - Math.PI / 6), toY - headlen * Math.sin(angle - Math.PI / 6));
        ctx.moveTo(toX, toY);
        ctx.lineTo(toX - headlen * Math.cos(angle + Math.PI / 6), toY - headlen * Math.sin(angle + Math.PI / 6));
        ctx.stroke();
    }

    /**
     * Set playback speed
     */
    setPlaybackSpeed(speed) {
        this.playbackSpeed = speed;
        this.videoElement.playbackRate = speed;
        console.log(`Playback speed set to ${speed}x`);
    }

    /**
     * Seek to specific time
     */
    seekTo(timestamp) {
        this.videoElement.currentTime = timestamp;
        console.log(`Seeked to ${this.formatTime(timestamp)}`);
    }

    /**
     * Copy share link to clipboard
     */
    async copyShareLink() {
        const shareUrl = `${window.location.origin}/recordings/view/${this.recording.share_token}`;

        try {
            await navigator.clipboard.writeText(shareUrl);
            alert('Share link copied to clipboard!');
        } catch (error) {
            console.error('Failed to copy link:', error);
            // Fallback
            prompt('Copy this link:', shareUrl);
        }
    }

    /**
     * Show embed code
     */
    async showEmbedCode() {
        try {
            const baseUrl = window.location.origin;
            const response = await fetch(
                `/api/recordings/${this.recording.id}/embed-code?base_url=${encodeURIComponent(baseUrl)}`
            );

            if (!response.ok) {
                throw new Error('Failed to get embed code');
            }

            const data = await response.json();

            // Show in modal or prompt
            prompt('Copy this embed code:', data.embed_code);
        } catch (error) {
            console.error('Error getting embed code:', error);
            alert('Failed to get embed code');
        }
    }

    /**
     * Format time (seconds to MM:SS)
     */
    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }

    /**
     * Format duration
     */
    formatDuration(seconds) {
        if (seconds < 60) {
            return `${seconds}s`;
        }
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return secs > 0 ? `${mins}m ${secs}s` : `${mins}m`;
    }

    /**
     * Play video
     */
    play() {
        this.videoElement.play();
    }

    /**
     * Pause video
     */
    pause() {
        this.videoElement.pause();
    }

    /**
     * Toggle play/pause
     */
    togglePlayPause() {
        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = RecordingPlayer;
}
