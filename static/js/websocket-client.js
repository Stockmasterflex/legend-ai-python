/**
 * WebSocket Client with Real-Time Streaming
 *
 * Features:
 * - Automatic reconnection with exponential backoff
 * - Message queue management for high-frequency updates
 * - Throttled DOM updates (max 10/sec)
 * - Batch DOM updates for performance
 * - Memory leak prevention
 * - Heartbeat/ping-pong mechanism
 * - Connection health monitoring
 */

class WebSocketClient {
    constructor(options = {}) {
        // Configuration
        this.config = {
            url: options.url || this._getWebSocketURL(),
            userId: options.userId || 'default',
            reconnectDelay: options.reconnectDelay || 1000,
            maxReconnectDelay: options.maxReconnectDelay || 30000,
            reconnectBackoffMultiplier: options.reconnectBackoffMultiplier || 1.5,
            heartbeatInterval: options.heartbeatInterval || 30000,
            maxMessagesPerSecond: options.maxMessagesPerSecond || 10,
            batchUpdateDelay: options.batchUpdateDelay || 100,
            maxQueueSize: options.maxQueueSize || 1000
        };

        // WebSocket connection
        this.ws = null;
        this.connectionId = null;

        // Connection state
        this.connected = false;
        this.reconnecting = false;
        this.reconnectAttempts = 0;
        this.reconnectTimer = null;

        // Heartbeat
        this.heartbeatTimer = null;
        this.lastPongTime = null;

        // Message queue for high-frequency updates
        this.messageQueue = [];
        this.processingQueue = false;

        // DOM update batching
        this.pendingUpdates = new Map();
        this.updateBatchTimer = null;

        // Subscriptions
        this.subscriptions = new Set();

        // Event handlers
        this.handlers = {
            'connection': [],
            'price_update': [],
            'pattern_alert': [],
            'alert_trigger': [],
            'market_status': [],
            'subscription': [],
            'history': [],
            'error': [],
            'disconnect': []
        };

        // Performance tracking
        this.stats = {
            messagesReceived: 0,
            messagesSent: 0,
            updatesApplied: 0,
            reconnects: 0,
            errors: 0,
            lastMessageTime: null
        };

        // Throttling
        this.messageTimestamps = [];

        // Data cache (for change detection)
        this.dataCache = new Map();
    }

    /**
     * Get WebSocket URL based on current page location
     */
    _getWebSocketURL() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host;
        return `${protocol}//${host}/api/ws?user_id=${this.config.userId}`;
    }

    /**
     * Connect to WebSocket server
     */
    connect() {
        if (this.ws && (this.ws.readyState === WebSocket.CONNECTING || this.ws.readyState === WebSocket.OPEN)) {
            console.log('[WS] Already connected or connecting');
            return;
        }

        try {
            console.log(`[WS] Connecting to ${this.config.url}...`);
            this.ws = new WebSocket(this.config.url);

            this.ws.onopen = this._handleOpen.bind(this);
            this.ws.onmessage = this._handleMessage.bind(this);
            this.ws.onerror = this._handleError.bind(this);
            this.ws.onclose = this._handleClose.bind(this);

        } catch (error) {
            console.error('[WS] Connection error:', error);
            this._scheduleReconnect();
        }
    }

    /**
     * Disconnect from WebSocket server
     */
    disconnect() {
        console.log('[WS] Disconnecting...');
        this.connected = false;

        // Clear timers
        if (this.heartbeatTimer) {
            clearInterval(this.heartbeatTimer);
            this.heartbeatTimer = null;
        }

        if (this.reconnectTimer) {
            clearTimeout(this.reconnectTimer);
            this.reconnectTimer = null;
        }

        if (this.updateBatchTimer) {
            clearTimeout(this.updateBatchTimer);
            this.updateBatchTimer = null;
        }

        // Close WebSocket
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }

        // Clear queues to prevent memory leaks
        this.messageQueue = [];
        this.pendingUpdates.clear();
        this.dataCache.clear();

        this._emit('disconnect', {});
    }

    /**
     * Handle WebSocket open event
     */
    _handleOpen(event) {
        console.log('[WS] Connected successfully');
        this.connected = true;
        this.reconnecting = false;
        this.reconnectAttempts = 0;

        // Start heartbeat
        this._startHeartbeat();

        this._emit('connection', { status: 'connected' });
    }

    /**
     * Handle incoming WebSocket message
     */
    _handleMessage(event) {
        try {
            const message = JSON.parse(event.data);
            this.stats.messagesReceived++;
            this.stats.lastMessageTime = new Date();

            // Check throttling
            if (this._shouldThrottle()) {
                // Add to queue instead of processing immediately
                this._enqueueMessage(message);
                return;
            }

            this._processMessage(message);

        } catch (error) {
            console.error('[WS] Error parsing message:', error);
            this.stats.errors++;
        }
    }

    /**
     * Handle WebSocket error
     */
    _handleError(error) {
        console.error('[WS] WebSocket error:', error);
        this.stats.errors++;
        this._emit('error', { error: error.message || 'Unknown error' });
    }

    /**
     * Handle WebSocket close event
     */
    _handleClose(event) {
        console.log('[WS] Connection closed:', event.code, event.reason);
        this.connected = false;

        // Clear heartbeat
        if (this.heartbeatTimer) {
            clearInterval(this.heartbeatTimer);
            this.heartbeatTimer = null;
        }

        // Schedule reconnect if not intentional disconnect
        if (event.code !== 1000) {
            this._scheduleReconnect();
        }

        this._emit('disconnect', { code: event.code, reason: event.reason });
    }

    /**
     * Schedule reconnection with exponential backoff
     */
    _scheduleReconnect() {
        if (this.reconnecting) {
            return;
        }

        this.reconnecting = true;
        this.reconnectAttempts++;
        this.stats.reconnects++;

        const delay = Math.min(
            this.config.reconnectDelay * Math.pow(this.config.reconnectBackoffMultiplier, this.reconnectAttempts - 1),
            this.config.maxReconnectDelay
        );

        console.log(`[WS] Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})...`);

        this.reconnectTimer = setTimeout(() => {
            this.connect();
        }, delay);
    }

    /**
     * Start heartbeat mechanism
     */
    _startHeartbeat() {
        if (this.heartbeatTimer) {
            clearInterval(this.heartbeatTimer);
        }

        this.heartbeatTimer = setInterval(() => {
            if (this.connected) {
                this.send({ type: 'ping' });
            }
        }, this.config.heartbeatInterval);
    }

    /**
     * Check if message rate should be throttled
     */
    _shouldThrottle() {
        const now = Date.now();

        // Remove timestamps older than 1 second
        this.messageTimestamps = this.messageTimestamps.filter(t => now - t < 1000);

        // Check if we've exceeded the rate limit
        return this.messageTimestamps.length >= this.config.maxMessagesPerSecond;
    }

    /**
     * Record message timestamp for throttling
     */
    _recordMessageProcessed() {
        this.messageTimestamps.push(Date.now());
    }

    /**
     * Enqueue message for later processing
     */
    _enqueueMessage(message) {
        if (this.messageQueue.length >= this.config.maxQueueSize) {
            // Drop oldest message to prevent memory issues
            this.messageQueue.shift();
            console.warn('[WS] Message queue full, dropping oldest message');
        }

        this.messageQueue.push(message);

        // Start processing queue if not already processing
        if (!this.processingQueue) {
            this._processQueue();
        }
    }

    /**
     * Process queued messages
     */
    async _processQueue() {
        if (this.processingQueue || this.messageQueue.length === 0) {
            return;
        }

        this.processingQueue = true;

        while (this.messageQueue.length > 0) {
            // Check throttling
            if (this._shouldThrottle()) {
                // Wait a bit before processing more
                await new Promise(resolve => setTimeout(resolve, 100));
                continue;
            }

            const message = this.messageQueue.shift();
            this._processMessage(message);
        }

        this.processingQueue = false;
    }

    /**
     * Process a single message
     */
    _processMessage(message) {
        this._recordMessageProcessed();

        const messageType = message.type;

        // Handle special message types
        if (messageType === 'pong') {
            this.lastPongTime = new Date();
            return;
        }

        if (messageType === 'connection') {
            this.connectionId = message.connection_id;
        }

        // Emit to registered handlers
        this._emit(messageType, message);
    }

    /**
     * Send message to server
     */
    send(message) {
        if (!this.connected || !this.ws || this.ws.readyState !== WebSocket.OPEN) {
            console.warn('[WS] Cannot send message, not connected');
            return false;
        }

        try {
            this.ws.send(JSON.stringify(message));
            this.stats.messagesSent++;
            return true;
        } catch (error) {
            console.error('[WS] Error sending message:', error);
            return false;
        }
    }

    /**
     * Subscribe to a data stream
     */
    subscribe(channel, ticker = null) {
        const subscription = ticker ? `${channel}:${ticker}` : channel;

        if (this.subscriptions.has(subscription)) {
            console.log(`[WS] Already subscribed to ${subscription}`);
            return;
        }

        const message = {
            type: 'subscribe',
            channel: channel,
        };

        if (ticker) {
            message.ticker = ticker;
        }

        if (this.send(message)) {
            this.subscriptions.add(subscription);
            console.log(`[WS] Subscribed to ${subscription}`);
        }
    }

    /**
     * Unsubscribe from a data stream
     */
    unsubscribe(channel, ticker = null) {
        const subscription = ticker ? `${channel}:${ticker}` : channel;

        if (!this.subscriptions.has(subscription)) {
            return;
        }

        const message = {
            type: 'unsubscribe',
            channel: channel,
        };

        if (ticker) {
            message.ticker = ticker;
        }

        if (this.send(message)) {
            this.subscriptions.delete(subscription);
            console.log(`[WS] Unsubscribed from ${subscription}`);
        }
    }

    /**
     * Register event handler
     */
    on(event, handler) {
        if (!this.handlers[event]) {
            this.handlers[event] = [];
        }
        this.handlers[event].push(handler);
    }

    /**
     * Unregister event handler
     */
    off(event, handler) {
        if (!this.handlers[event]) {
            return;
        }
        this.handlers[event] = this.handlers[event].filter(h => h !== handler);
    }

    /**
     * Emit event to registered handlers
     */
    _emit(event, data) {
        const handlers = this.handlers[event] || [];
        handlers.forEach(handler => {
            try {
                handler(data);
            } catch (error) {
                console.error(`[WS] Error in event handler for ${event}:`, error);
            }
        });
    }

    /**
     * Schedule DOM update with batching
     */
    scheduleDOMUpdate(key, updateFn) {
        // Store the update function
        this.pendingUpdates.set(key, updateFn);

        // Clear existing timer
        if (this.updateBatchTimer) {
            clearTimeout(this.updateBatchTimer);
        }

        // Schedule batch update
        this.updateBatchTimer = setTimeout(() => {
            this._applyBatchedUpdates();
        }, this.config.batchUpdateDelay);
    }

    /**
     * Apply all batched DOM updates
     */
    _applyBatchedUpdates() {
        if (this.pendingUpdates.size === 0) {
            return;
        }

        // Use requestAnimationFrame for optimal rendering
        requestAnimationFrame(() => {
            const updates = Array.from(this.pendingUpdates.entries());

            // Apply all updates
            updates.forEach(([key, updateFn]) => {
                try {
                    updateFn();
                    this.stats.updatesApplied++;
                } catch (error) {
                    console.error(`[WS] Error applying update for ${key}:`, error);
                }
            });

            this.pendingUpdates.clear();
        });
    }

    /**
     * Update DOM element only if value changed
     */
    updateElementIfChanged(element, newValue, formatter = null) {
        if (!element) {
            return false;
        }

        const key = element.id || element.dataset.key;
        if (!key) {
            console.warn('[WS] Element has no id or data-key, cannot track changes');
            return false;
        }

        const oldValue = this.dataCache.get(key);
        if (oldValue === newValue) {
            return false; // No change
        }

        this.dataCache.set(key, newValue);

        // Schedule DOM update
        this.scheduleDOMUpdate(key, () => {
            const formattedValue = formatter ? formatter(newValue) : newValue;

            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                element.value = formattedValue;
            } else {
                element.textContent = formattedValue;
            }
        });

        return true;
    }

    /**
     * Get connection statistics
     */
    getStats() {
        return {
            ...this.stats,
            connected: this.connected,
            reconnecting: this.reconnecting,
            reconnectAttempts: this.reconnectAttempts,
            subscriptions: Array.from(this.subscriptions),
            queueSize: this.messageQueue.length,
            pendingUpdates: this.pendingUpdates.size,
            cacheSize: this.dataCache.size
        };
    }

    /**
     * Clear data cache to prevent memory leaks
     */
    clearCache() {
        this.dataCache.clear();
        console.log('[WS] Cache cleared');
    }
}

// Export for use in other scripts
window.WebSocketClient = WebSocketClient;
