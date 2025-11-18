/**
 * Chart Recorder - Screen Recording and Sharing
 * Handles chart recording, annotations, and video sharing
 */

class ChartRecorder {
    constructor() {
        this.mediaRecorder = null;
        this.recordedChunks = [];
        this.stream = null;
        this.isRecording = false;
        this.isPaused = false;
        this.startTime = null;
        this.currentRecordingId = null;
        this.annotations = [];
        this.bookmarks = [];
        this.drawingData = [];
        this.audioEnabled = false;
        this.canvas = null;
        this.ctx = null;
    }

    /**
     * Initialize recorder with chart element
     */
    async init(chartElementId, options = {}) {
        this.chartElement = document.getElementById(chartElementId);
        if (!this.chartElement) {
            throw new Error(`Chart element ${chartElementId} not found`);
        }

        this.options = {
            mimeType: 'video/webm;codecs=vp9',
            audioBitsPerSecond: 128000,
            videoBitsPerSecond: 2500000,
            includeAudio: options.includeAudio || false,
            timeLapse: options.timeLapse || false,
            timeLapseSpeed: options.timeLapseSpeed || 2.0,
            ...options
        };

        // Initialize drawing canvas overlay
        this.initDrawingCanvas();
    }

    /**
     * Initialize drawing canvas for annotations
     */
    initDrawingCanvas() {
        const rect = this.chartElement.getBoundingClientRect();

        this.canvas = document.createElement('canvas');
        this.canvas.id = 'recording-canvas';
        this.canvas.width = rect.width;
        this.canvas.height = rect.height;
        this.canvas.style.position = 'absolute';
        this.canvas.style.top = rect.top + 'px';
        this.canvas.style.left = rect.left + 'px';
        this.canvas.style.zIndex = '1000';
        this.canvas.style.pointerEvents = 'none';
        this.canvas.style.display = 'none';

        document.body.appendChild(this.canvas);
        this.ctx = this.canvas.getContext('2d');
    }

    /**
     * Start recording
     */
    async startRecording() {
        try {
            // Capture screen/chart area
            const displayMediaOptions = {
                video: {
                    displaySurface: "browser",
                    width: { ideal: 1920 },
                    height: { ideal: 1080 },
                    frameRate: this.options.timeLapse ? 60 : 30
                },
                audio: this.options.includeAudio
            };

            this.stream = await navigator.mediaDevices.getDisplayMedia(displayMediaOptions);

            // Add audio track if enabled
            if (this.options.includeAudio) {
                const audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
                audioStream.getAudioTracks().forEach(track => {
                    this.stream.addTrack(track);
                });
            }

            // Setup media recorder
            const options = {
                mimeType: this.options.mimeType,
                videoBitsPerSecond: this.options.videoBitsPerSecond
            };

            this.mediaRecorder = new MediaRecorder(this.stream, options);
            this.recordedChunks = [];

            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.recordedChunks.push(event.data);
                }
            };

            this.mediaRecorder.onstop = () => {
                this.handleRecordingComplete();
            };

            this.mediaRecorder.start(100); // Collect data every 100ms
            this.isRecording = true;
            this.startTime = Date.now();
            this.canvas.style.display = 'block';

            console.log('Recording started');

            return true;
        } catch (error) {
            console.error('Failed to start recording:', error);
            throw error;
        }
    }

    /**
     * Stop recording
     */
    async stopRecording() {
        if (!this.mediaRecorder || !this.isRecording) {
            return;
        }

        this.mediaRecorder.stop();
        this.stream.getTracks().forEach(track => track.stop());
        this.isRecording = false;
        this.canvas.style.display = 'none';

        console.log('Recording stopped');
    }

    /**
     * Pause recording
     */
    pauseRecording() {
        if (this.mediaRecorder && this.isRecording && !this.isPaused) {
            this.mediaRecorder.pause();
            this.isPaused = true;
            console.log('Recording paused');
        }
    }

    /**
     * Resume recording
     */
    resumeRecording() {
        if (this.mediaRecorder && this.isRecording && this.isPaused) {
            this.mediaRecorder.resume();
            this.isPaused = false;
            console.log('Recording resumed');
        }
    }

    /**
     * Add annotation at current time
     */
    addAnnotation(type, data, position = null) {
        const timestamp = (Date.now() - this.startTime) / 1000;

        const annotation = {
            timestamp,
            type,
            data,
            position: position || { x: 0, y: 0 }
        };

        this.annotations.push(annotation);

        // Draw annotation on canvas
        this.drawAnnotation(annotation);

        console.log('Annotation added:', annotation);
        return annotation;
    }

    /**
     * Add bookmark at current time
     */
    addBookmark(label, description = '') {
        const timestamp = (Date.now() - this.startTime) / 1000;

        const bookmark = {
            timestamp,
            label,
            description
        };

        this.bookmarks.push(bookmark);
        console.log('Bookmark added:', bookmark);
        return bookmark;
    }

    /**
     * Draw annotation on canvas
     */
    drawAnnotation(annotation) {
        if (!this.ctx) return;

        const { type, data, position } = annotation;

        this.ctx.save();

        switch (type) {
            case 'text':
                this.ctx.font = data.font || '16px Arial';
                this.ctx.fillStyle = data.color || '#FF0000';
                this.ctx.fillText(data.text, position.x, position.y);
                break;

            case 'arrow':
                this.drawArrow(position.x, position.y, data.endX, data.endY, data.color || '#FF0000');
                break;

            case 'highlight':
                this.ctx.fillStyle = data.color || 'rgba(255, 255, 0, 0.3)';
                this.ctx.fillRect(position.x, position.y, data.width, data.height);
                break;

            case 'circle':
                this.ctx.strokeStyle = data.color || '#FF0000';
                this.ctx.lineWidth = data.width || 2;
                this.ctx.beginPath();
                this.ctx.arc(position.x, position.y, data.radius, 0, 2 * Math.PI);
                this.ctx.stroke();
                break;

            case 'line':
                this.ctx.strokeStyle = data.color || '#FF0000';
                this.ctx.lineWidth = data.width || 2;
                this.ctx.beginPath();
                this.ctx.moveTo(position.x, position.y);
                this.ctx.lineTo(data.endX, data.endY);
                this.ctx.stroke();
                break;
        }

        this.ctx.restore();

        // Save drawing action
        this.drawingData.push({
            timestamp: (Date.now() - this.startTime) / 1000,
            ...annotation
        });
    }

    /**
     * Draw arrow helper
     */
    drawArrow(fromX, fromY, toX, toY, color) {
        const headlen = 10;
        const angle = Math.atan2(toY - fromY, toX - fromX);

        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.moveTo(fromX, fromY);
        this.ctx.lineTo(toX, toY);
        this.ctx.lineTo(toX - headlen * Math.cos(angle - Math.PI / 6), toY - headlen * Math.sin(angle - Math.PI / 6));
        this.ctx.moveTo(toX, toY);
        this.ctx.lineTo(toX - headlen * Math.cos(angle + Math.PI / 6), toY - headlen * Math.sin(angle + Math.PI / 6));
        this.ctx.stroke();
    }

    /**
     * Clear all annotations from canvas
     */
    clearAnnotations() {
        if (this.ctx) {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        }
        console.log('Annotations cleared');
    }

    /**
     * Handle recording complete
     */
    async handleRecordingComplete() {
        const blob = new Blob(this.recordedChunks, {
            type: this.options.mimeType
        });

        const duration = (Date.now() - this.startTime) / 1000;

        console.log(`Recording complete: ${duration}s, ${blob.size} bytes`);

        return {
            blob,
            duration,
            annotations: this.annotations,
            bookmarks: this.bookmarks,
            drawingData: this.drawingData
        };
    }

    /**
     * Upload recording to server
     */
    async uploadRecording(recordingId, blob, thumbnailBlob = null, metadata = {}) {
        const formData = new FormData();
        formData.append('video', blob, 'recording.webm');

        if (thumbnailBlob) {
            formData.append('thumbnail', thumbnailBlob, 'thumbnail.jpg');
        }

        if (metadata.duration_seconds) {
            formData.append('duration_seconds', metadata.duration_seconds);
        }
        if (metadata.resolution) {
            formData.append('resolution', metadata.resolution);
        }

        try {
            const response = await fetch(`/api/recordings/${recordingId}/upload`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`);
            }

            const result = await response.json();
            console.log('Upload successful:', result);
            return result;
        } catch (error) {
            console.error('Upload error:', error);
            throw error;
        }
    }

    /**
     * Save annotations to server
     */
    async saveAnnotations(recordingId) {
        try {
            const response = await fetch(`/api/recordings/${recordingId}/annotations`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.annotations)
            });

            if (!response.ok) {
                throw new Error(`Failed to save annotations: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error saving annotations:', error);
            throw error;
        }
    }

    /**
     * Save bookmarks to server
     */
    async saveBookmarks(recordingId) {
        try {
            const response = await fetch(`/api/recordings/${recordingId}/bookmarks`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.bookmarks)
            });

            if (!response.ok) {
                throw new Error(`Failed to save bookmarks: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error saving bookmarks:', error);
            throw error;
        }
    }

    /**
     * Save drawing data to server
     */
    async saveDrawingData(recordingId) {
        try {
            const response = await fetch(`/api/recordings/${recordingId}/drawing-data`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.drawingData)
            });

            if (!response.ok) {
                throw new Error(`Failed to save drawing data: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error saving drawing data:', error);
            throw error;
        }
    }

    /**
     * Create new recording on server
     */
    async createRecording(tickerSymbol, title, description = '', options = {}) {
        try {
            const response = await fetch('/api/recordings/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    ticker_symbol: tickerSymbol,
                    title,
                    description,
                    user_id: options.user_id || 'default',
                    has_audio: this.options.includeAudio || false,
                    is_timelapse: this.options.timeLapse || false
                })
            });

            if (!response.ok) {
                throw new Error(`Failed to create recording: ${response.statusText}`);
            }

            const result = await response.json();
            this.currentRecordingId = result.id;
            console.log('Recording created:', result);
            return result;
        } catch (error) {
            console.error('Error creating recording:', error);
            throw error;
        }
    }

    /**
     * Generate thumbnail from video
     */
    async generateThumbnail(videoBlob) {
        return new Promise((resolve, reject) => {
            const video = document.createElement('video');
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');

            video.onloadeddata = () => {
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                video.currentTime = 1; // Seek to 1 second
            };

            video.onseeked = () => {
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                canvas.toBlob((blob) => {
                    resolve(blob);
                }, 'image/jpeg', 0.9);
            };

            video.onerror = reject;

            const url = URL.createObjectURL(videoBlob);
            video.src = url;
        });
    }

    /**
     * Complete recording workflow
     */
    async completeRecording(tickerSymbol, title, description = '') {
        // Create recording entry
        const recording = await this.createRecording(tickerSymbol, title, description);

        // Stop recording and get data
        await this.stopRecording();
        const { blob, duration } = await this.handleRecordingComplete();

        // Generate thumbnail
        const thumbnailBlob = await this.generateThumbnail(blob);

        // Upload video and thumbnail
        await this.uploadRecording(recording.id, blob, thumbnailBlob, {
            duration_seconds: Math.round(duration),
            resolution: `${this.canvas.width}x${this.canvas.height}`
        });

        // Save annotations and bookmarks
        if (this.annotations.length > 0) {
            await this.saveAnnotations(recording.id);
        }
        if (this.bookmarks.length > 0) {
            await this.saveBookmarks(recording.id);
        }
        if (this.drawingData.length > 0) {
            await this.saveDrawingData(recording.id);
        }

        console.log('Recording workflow complete:', recording.id);
        return recording;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChartRecorder;
}
