/**
 * Real-Time Dashboard Integration
 *
 * Integrates WebSocket client with the dashboard for live updates.
 */

class RealtimeDashboard {
    constructor() {
        this.ws = null;
        this.priceUpdateElements = new Map();
        this.notificationQueue = [];
        this.maxNotifications = 5;
    }

    /**
     * Initialize WebSocket connection and subscriptions
     */
    async initialize() {
        console.log('[Dashboard] Initializing real-time updates...');

        // Create WebSocket client
        this.ws = new WebSocketClient({
            userId: this._getUserId(),
            maxMessagesPerSecond: 10,
            batchUpdateDelay: 100
        });

        // Register event handlers
        this._registerHandlers();

        // Connect
        this.ws.connect();

        // Setup UI
        this._setupUI();
    }

    /**
     * Get user ID from session/localStorage or use default
     */
    _getUserId() {
        return localStorage.getItem('user_id') || 'default';
    }

    /**
     * Register WebSocket event handlers
     */
    _registerHandlers() {
        // Connection status
        this.ws.on('connection', (data) => {
            console.log('[Dashboard] Connected:', data);
            this._updateConnectionStatus('connected');
            this._subscribeToWatchlist();
        });

        this.ws.on('disconnect', (data) => {
            console.log('[Dashboard] Disconnected:', data);
            this._updateConnectionStatus('disconnected');
        });

        // Price updates
        this.ws.on('price_update', (data) => {
            this._handlePriceUpdate(data);
        });

        // Pattern alerts
        this.ws.on('pattern_alert', (data) => {
            this._handlePatternAlert(data);
        });

        // Alert triggers
        this.ws.on('alert_trigger', (data) => {
            this._handleAlertTrigger(data);
        });

        // Market status
        this.ws.on('market_status', (data) => {
            this._handleMarketStatus(data);
        });

        // Subscription confirmations
        this.ws.on('subscription', (data) => {
            console.log('[Dashboard] Subscription:', data);
        });

        // Historical data
        this.ws.on('history', (data) => {
            console.log('[Dashboard] History received:', data);
            if (data.messages && data.messages.length > 0) {
                // Process historical messages
                data.messages.forEach(msg => {
                    if (msg.type === 'price_update') {
                        this._handlePriceUpdate(msg, true);
                    }
                });
            }
        });

        // Errors
        this.ws.on('error', (data) => {
            console.error('[Dashboard] WebSocket error:', data);
            this._showNotification('WebSocket Error', data.message || 'Unknown error', 'error');
        });
    }

    /**
     * Subscribe to watchlist tickers
     */
    async _subscribeToWatchlist() {
        try {
            // Fetch watchlist from API
            const response = await fetch('/api/watchlist');
            if (!response.ok) {
                throw new Error('Failed to fetch watchlist');
            }

            const watchlist = await response.json();

            // Subscribe to each ticker
            watchlist.forEach(item => {
                const ticker = item.ticker?.symbol || item.symbol;
                if (ticker) {
                    this.ws.subscribe('ticker', ticker);
                }
            });

            // Subscribe to alerts and patterns
            this.ws.subscribe('patterns');
            this.ws.subscribe('alerts');
            this.ws.subscribe('market_status');

            console.log(`[Dashboard] Subscribed to ${watchlist.length} tickers`);

        } catch (error) {
            console.error('[Dashboard] Error subscribing to watchlist:', error);
        }
    }

    /**
     * Handle price update
     */
    _handlePriceUpdate(data, isHistory = false) {
        const ticker = data.ticker;

        // Update price in watchlist table
        const priceElement = document.querySelector(`[data-ticker="${ticker}"] .price`);
        if (priceElement) {
            this.ws.updateElementIfChanged(
                priceElement,
                data.price,
                (val) => `$${val.toFixed(2)}`
            );

            // Update price element ID for tracking
            if (!priceElement.id) {
                priceElement.id = `price-${ticker}`;
            }
        }

        // Update change
        const changeElement = document.querySelector(`[data-ticker="${ticker}"] .change`);
        if (changeElement) {
            this.ws.updateElementIfChanged(
                changeElement,
                data.change_percent,
                (val) => {
                    const sign = val >= 0 ? '+' : '';
                    return `${sign}${val.toFixed(2)}%`;
                }
            );

            // Update color based on change
            this.ws.scheduleDOMUpdate(`change-color-${ticker}`, () => {
                changeElement.className = 'change ' + (data.change_percent >= 0 ? 'positive' : 'negative');
            });

            if (!changeElement.id) {
                changeElement.id = `change-${ticker}`;
            }
        }

        // Update volume
        const volumeElement = document.querySelector(`[data-ticker="${ticker}"] .volume`);
        if (volumeElement) {
            this.ws.updateElementIfChanged(
                volumeElement,
                data.volume,
                (val) => this._formatVolume(val)
            );

            if (!volumeElement.id) {
                volumeElement.id = `volume-${ticker}`;
            }
        }

        // Show notification for significant price moves (not for history)
        if (!isHistory && Math.abs(data.change_percent) >= 2.0) {
            this._showNotification(
                `${ticker} Price Alert`,
                `Price: $${data.price.toFixed(2)} (${data.change_percent >= 0 ? '+' : ''}${data.change_percent.toFixed(2)}%)`,
                data.change_percent >= 0 ? 'success' : 'warning'
            );
        }
    }

    /**
     * Handle pattern alert
     */
    _handlePatternAlert(data) {
        console.log('[Dashboard] Pattern alert:', data);

        // Show notification
        this._showNotification(
            `🎯 ${data.pattern_type} Detected`,
            `${data.ticker} - Entry: $${data.entry_price.toFixed(2)}, R/R: ${data.risk_reward_ratio.toFixed(2)}`,
            'info'
        );

        // Add visual indicator to watchlist
        const row = document.querySelector(`[data-ticker="${data.ticker}"]`);
        if (row) {
            this.ws.scheduleDOMUpdate(`pattern-${data.ticker}`, () => {
                row.classList.add('pattern-detected');
                setTimeout(() => {
                    row.classList.remove('pattern-detected');
                }, 5000);
            });
        }

        // Play sound (if enabled)
        this._playNotificationSound();
    }

    /**
     * Handle alert trigger
     */
    _handleAlertTrigger(data) {
        console.log('[Dashboard] Alert triggered:', data);

        // Show notification
        this._showNotification(
            `🔔 Alert: ${data.ticker}`,
            data.message,
            'warning'
        );

        // Highlight row
        const row = document.querySelector(`[data-ticker="${data.ticker}"]`);
        if (row) {
            this.ws.scheduleDOMUpdate(`alert-${data.ticker}`, () => {
                row.classList.add('alert-triggered');
                setTimeout(() => {
                    row.classList.remove('alert-triggered');
                }, 10000);
            });
        }

        // Play sound
        this._playNotificationSound();
    }

    /**
     * Handle market status change
     */
    _handleMarketStatus(data) {
        console.log('[Dashboard] Market status:', data);

        const statusElement = document.getElementById('market-status');
        if (statusElement) {
            this.ws.updateElementIfChanged(
                statusElement,
                data.status,
                (val) => {
                    const statusText = val === 'open' ? '🟢 Market Open' : '🔴 Market Closed';
                    return statusText;
                }
            );

            // Update status class
            this.ws.scheduleDOMUpdate('market-status-class', () => {
                statusElement.className = `market-status ${data.status}`;
            });
        }

        // Show notification
        const message = data.status === 'open'
            ? 'Market is now open for trading'
            : `Market is closed${data.next_open ? `. Next open: ${new Date(data.next_open).toLocaleString()}` : ''}`;

        this._showNotification('Market Status', message, 'info');
    }

    /**
     * Update connection status indicator
     */
    _updateConnectionStatus(status) {
        const indicator = document.getElementById('ws-connection-status');
        if (indicator) {
            this.ws.scheduleDOMUpdate('connection-status', () => {
                indicator.className = `ws-status ${status}`;
                indicator.title = status === 'connected' ? 'Connected to real-time updates' : 'Disconnected';

                const dot = indicator.querySelector('.status-dot');
                if (dot) {
                    dot.textContent = status === 'connected' ? '🟢' : '🔴';
                }

                const text = indicator.querySelector('.status-text');
                if (text) {
                    text.textContent = status === 'connected' ? 'Live' : 'Offline';
                }
            });
        }
    }

    /**
     * Show notification
     */
    _showNotification(title, message, type = 'info') {
        // Add to queue
        this.notificationQueue.push({ title, message, type, timestamp: Date.now() });

        // Keep only recent notifications
        if (this.notificationQueue.length > this.maxNotifications) {
            this.notificationQueue.shift();
        }

        // Update notification container
        this._updateNotificationUI();

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            this.notificationQueue = this.notificationQueue.filter(n => n.timestamp !== this.notificationQueue[0]?.timestamp);
            this._updateNotificationUI();
        }, 5000);
    }

    /**
     * Update notification UI
     */
    _updateNotificationUI() {
        const container = document.getElementById('notification-container');
        if (!container) {
            return;
        }

        this.ws.scheduleDOMUpdate('notifications', () => {
            container.innerHTML = this.notificationQueue.map((n, index) => `
                <div class="notification ${n.type} slide-in" style="animation-delay: ${index * 0.1}s">
                    <div class="notification-title">${n.title}</div>
                    <div class="notification-message">${n.message}</div>
                    <button class="notification-close" onclick="realtimeDashboard._dismissNotification(${n.timestamp})">×</button>
                </div>
            `).join('');
        });
    }

    /**
     * Dismiss notification
     */
    _dismissNotification(timestamp) {
        this.notificationQueue = this.notificationQueue.filter(n => n.timestamp !== timestamp);
        this._updateNotificationUI();
    }

    /**
     * Play notification sound
     */
    _playNotificationSound() {
        if (!this._isSoundEnabled()) {
            return;
        }

        // Create a simple beep using Web Audio API
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.value = 800;
            oscillator.type = 'sine';

            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);

            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.5);
        } catch (error) {
            console.error('[Dashboard] Error playing sound:', error);
        }
    }

    /**
     * Check if sound is enabled
     */
    _isSoundEnabled() {
        return localStorage.getItem('notifications_sound') !== 'false';
    }

    /**
     * Setup UI elements
     */
    _setupUI() {
        // Add connection status indicator if it doesn't exist
        if (!document.getElementById('ws-connection-status')) {
            const statusHTML = `
                <div id="ws-connection-status" class="ws-status disconnected">
                    <span class="status-dot">🔴</span>
                    <span class="status-text">Offline</span>
                </div>
            `;

            const header = document.querySelector('header') || document.querySelector('.dashboard-header');
            if (header) {
                const statusDiv = document.createElement('div');
                statusDiv.innerHTML = statusHTML;
                header.appendChild(statusDiv.firstElementChild);
            }
        }

        // Add notification container if it doesn't exist
        if (!document.getElementById('notification-container')) {
            const notificationHTML = `
                <div id="notification-container" class="notification-container"></div>
            `;

            document.body.insertAdjacentHTML('beforeend', notificationHTML);
        }

        // Add stats display
        this._addStatsDisplay();
    }

    /**
     * Add WebSocket stats display
     */
    _addStatsDisplay() {
        if (document.getElementById('ws-stats')) {
            return;
        }

        const statsHTML = `
            <div id="ws-stats" class="ws-stats" style="display: none;">
                <h4>WebSocket Stats</h4>
                <div id="ws-stats-content"></div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', statsHTML);

        // Update stats every 5 seconds
        setInterval(() => {
            this._updateStatsDisplay();
        }, 5000);
    }

    /**
     * Update stats display
     */
    _updateStatsDisplay() {
        const statsElement = document.getElementById('ws-stats-content');
        if (!statsElement) {
            return;
        }

        const stats = this.ws.getStats();

        this.ws.scheduleDOMUpdate('ws-stats', () => {
            statsElement.innerHTML = `
                <div>Connected: ${stats.connected ? '✅' : '❌'}</div>
                <div>Messages Received: ${stats.messagesReceived}</div>
                <div>Messages Sent: ${stats.messagesSent}</div>
                <div>Updates Applied: ${stats.updatesApplied}</div>
                <div>Reconnects: ${stats.reconnects}</div>
                <div>Errors: ${stats.errors}</div>
                <div>Queue Size: ${stats.queueSize}</div>
                <div>Pending Updates: ${stats.pendingUpdates}</div>
                <div>Cache Size: ${stats.cacheSize}</div>
                <div>Subscriptions: ${stats.subscriptions.length}</div>
            `;
        });
    }

    /**
     * Format volume for display
     */
    _formatVolume(volume) {
        if (volume >= 1000000) {
            return `${(volume / 1000000).toFixed(2)}M`;
        } else if (volume >= 1000) {
            return `${(volume / 1000).toFixed(2)}K`;
        }
        return volume.toString();
    }

    /**
     * Subscribe to a ticker
     */
    subscribeTicker(ticker) {
        if (this.ws && this.ws.connected) {
            this.ws.subscribe('ticker', ticker);
        }
    }

    /**
     * Unsubscribe from a ticker
     */
    unsubscribeTicker(ticker) {
        if (this.ws && this.ws.connected) {
            this.ws.unsubscribe('ticker', ticker);
        }
    }

    /**
     * Toggle stats display
     */
    toggleStats() {
        const statsElement = document.getElementById('ws-stats');
        if (statsElement) {
            statsElement.style.display = statsElement.style.display === 'none' ? 'block' : 'none';
        }
    }

    /**
     * Cleanup and disconnect
     */
    destroy() {
        if (this.ws) {
            this.ws.disconnect();
            this.ws = null;
        }
    }
}

// Global instance
let realtimeDashboard = null;

// Auto-initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    realtimeDashboard = new RealtimeDashboard();
    realtimeDashboard.initialize();
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (realtimeDashboard) {
        realtimeDashboard.destroy();
    }
});

// Export for external use
window.realtimeDashboard = realtimeDashboard;
