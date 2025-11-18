/**
 * Alert Condition Builder and Notification System
 * Allows users to create alerts based on indicator conditions
 */

class AlertSystem {
    constructor() {
        this.alerts = new Map();
        this.alertHistory = [];
        this.nextId = 1;
        this.checkInterval = null;
        this.notificationCallback = null;
    }

    /**
     * Create a new alert
     */
    createAlert(config) {
        const alert = {
            id: this.nextId++,
            name: config.name || `Alert ${this.nextId}`,
            condition: config.condition, // Function that returns true/false
            message: config.message || 'Alert triggered',
            enabled: config.enabled !== false,
            frequency: config.frequency || 'once', // 'once', 'per-bar', 'continuous'
            sound: config.sound !== false,
            notification: config.notification !== false,
            email: config.email || null,
            webhook: config.webhook || null,
            triggered: false,
            lastTriggered: null,
            triggerCount: 0,
            createdAt: Date.now()
        };

        this.alerts.set(alert.id, alert);
        return alert.id;
    }

    /**
     * Create alert from formula
     */
    createFormulaAlert(name, formula, message, options = {}) {
        const condition = (data, indicators) => {
            try {
                const func = new Function('data', 'indicators', `return ${formula}`);
                return func(data, indicators);
            } catch (error) {
                console.error('Alert formula error:', error);
                return false;
            }
        };

        return this.createAlert({
            name,
            condition,
            message,
            ...options
        });
    }

    /**
     * Common alert templates
     */
    createPriceCrossAlert(symbol, targetPrice, direction = 'above') {
        return this.createAlert({
            name: `${symbol} crosses ${direction} ${targetPrice}`,
            condition: (data) => {
                const current = data[data.length - 1];
                const previous = data[data.length - 2];

                if (direction === 'above') {
                    return previous.close <= targetPrice && current.close > targetPrice;
                } else {
                    return previous.close >= targetPrice && current.close < targetPrice;
                }
            },
            message: `${symbol} has crossed ${direction} ${targetPrice}`
        });
    }

    createIndicatorCrossAlert(name, indicator1, indicator2, direction = 'above') {
        return this.createAlert({
            name,
            condition: (data, indicators) => {
                const ind1 = indicators[indicator1];
                const ind2 = indicators[indicator2];

                if (!ind1 || !ind2) return false;

                const current1 = ind1[ind1.length - 1];
                const current2 = ind2[ind2.length - 1];
                const previous1 = ind1[ind1.length - 2];
                const previous2 = ind2[ind2.length - 2];

                if (direction === 'above') {
                    return previous1 <= previous2 && current1 > current2;
                } else {
                    return previous1 >= previous2 && current1 < current2;
                }
            },
            message: `${indicator1} crossed ${direction} ${indicator2}`
        });
    }

    createRSIAlert(threshold, direction = 'above') {
        return this.createAlert({
            name: `RSI ${direction} ${threshold}`,
            condition: (data, indicators) => {
                const rsi = indicators.RSI;
                if (!rsi) return false;

                const current = rsi[rsi.length - 1];
                const previous = rsi[rsi.length - 2];

                if (direction === 'above') {
                    return previous <= threshold && current > threshold;
                } else {
                    return previous >= threshold && current < threshold;
                }
            },
            message: `RSI has crossed ${direction} ${threshold}`
        });
    }

    createVolumeAlert(threshold, comparison = 'greater') {
        return this.createAlert({
            name: `Volume ${comparison} than ${threshold}`,
            condition: (data) => {
                const current = data[data.length - 1];

                if (comparison === 'greater') {
                    return current.volume > threshold;
                } else {
                    return current.volume < threshold;
                }
            },
            message: `Volume is ${comparison} than ${threshold}`
        });
    }

    createPercentChangeAlert(percent, direction = 'up') {
        return this.createAlert({
            name: `Price ${direction} ${percent}%`,
            condition: (data) => {
                const current = data[data.length - 1];
                const previous = data[data.length - 2];

                const change = ((current.close - previous.close) / previous.close) * 100;

                if (direction === 'up') {
                    return change >= percent;
                } else {
                    return change <= -percent;
                }
            },
            message: `Price moved ${direction} by ${percent}%`
        });
    }

    /**
     * Check all alerts against current data
     */
    checkAlerts(data, indicators = {}) {
        const triggeredAlerts = [];

        for (const [id, alert] of this.alerts.entries()) {
            if (!alert.enabled) continue;

            try {
                const isTriggered = alert.condition(data, indicators);

                if (isTriggered) {
                    // Check frequency rules
                    if (alert.frequency === 'once' && alert.triggered) {
                        continue; // Already triggered, skip
                    }

                    if (alert.frequency === 'per-bar') {
                        const currentTime = data[data.length - 1].timestamp;
                        if (alert.lastTriggered === currentTime) {
                            continue; // Already triggered this bar
                        }
                    }

                    // Trigger alert
                    this.triggerAlert(id, data);
                    triggeredAlerts.push(alert);
                }
            } catch (error) {
                console.error(`Alert ${id} evaluation error:`, error);
            }
        }

        return triggeredAlerts;
    }

    /**
     * Trigger an alert
     */
    triggerAlert(id, data) {
        const alert = this.alerts.get(id);
        if (!alert) return;

        alert.triggered = true;
        alert.lastTriggered = data[data.length - 1].timestamp;
        alert.triggerCount++;

        const alertEvent = {
            id: alert.id,
            name: alert.name,
            message: alert.message,
            timestamp: Date.now(),
            price: data[data.length - 1].close
        };

        this.alertHistory.push(alertEvent);

        // Play sound
        if (alert.sound) {
            this.playAlertSound();
        }

        // Show notification
        if (alert.notification) {
            this.showNotification(alertEvent);
        }

        // Send email
        if (alert.email) {
            this.sendEmail(alert.email, alertEvent);
        }

        // Call webhook
        if (alert.webhook) {
            this.callWebhook(alert.webhook, alertEvent);
        }

        // Call custom callback
        if (this.notificationCallback) {
            this.notificationCallback(alertEvent);
        }
    }

    /**
     * Play alert sound
     */
    playAlertSound() {
        // Create a simple beep sound
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
    }

    /**
     * Show browser notification
     */
    showNotification(alertEvent) {
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification(alertEvent.name, {
                body: alertEvent.message,
                icon: '/static/images/alert-icon.png',
                badge: '/static/images/alert-badge.png'
            });
        } else if ('Notification' in window && Notification.permission !== 'denied') {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    this.showNotification(alertEvent);
                }
            });
        }
    }

    /**
     * Send email notification
     */
    async sendEmail(email, alertEvent) {
        try {
            await fetch('/api/alerts/email', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    to: email,
                    subject: `Alert: ${alertEvent.name}`,
                    body: `${alertEvent.message}\n\nPrice: ${alertEvent.price}\nTime: ${new Date(alertEvent.timestamp).toLocaleString()}`
                })
            });
        } catch (error) {
            console.error('Failed to send email alert:', error);
        }
    }

    /**
     * Call webhook
     */
    async callWebhook(webhook, alertEvent) {
        try {
            await fetch(webhook, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(alertEvent)
            });
        } catch (error) {
            console.error('Failed to call webhook:', error);
        }
    }

    /**
     * Start automatic alert checking
     */
    startAutoCheck(dataProvider, interval = 5000) {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
        }

        this.checkInterval = setInterval(() => {
            const data = dataProvider.getData();
            const indicators = dataProvider.getIndicators();
            this.checkAlerts(data, indicators);
        }, interval);
    }

    /**
     * Stop automatic alert checking
     */
    stopAutoCheck() {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
            this.checkInterval = null;
        }
    }

    /**
     * Update alert
     */
    updateAlert(id, updates) {
        const alert = this.alerts.get(id);
        if (!alert) return false;

        Object.assign(alert, updates);
        return true;
    }

    /**
     * Enable/disable alert
     */
    toggleAlert(id) {
        const alert = this.alerts.get(id);
        if (!alert) return false;

        alert.enabled = !alert.enabled;
        return alert.enabled;
    }

    /**
     * Reset alert (for 'once' frequency alerts)
     */
    resetAlert(id) {
        const alert = this.alerts.get(id);
        if (!alert) return false;

        alert.triggered = false;
        alert.lastTriggered = null;
        return true;
    }

    /**
     * Delete alert
     */
    deleteAlert(id) {
        return this.alerts.delete(id);
    }

    /**
     * Get all alerts
     */
    getAllAlerts() {
        return Array.from(this.alerts.values());
    }

    /**
     * Get alert by ID
     */
    getAlert(id) {
        return this.alerts.get(id);
    }

    /**
     * Get alert history
     */
    getHistory(limit = 100) {
        return this.alertHistory.slice(-limit);
    }

    /**
     * Clear alert history
     */
    clearHistory() {
        this.alertHistory = [];
    }

    /**
     * Set notification callback
     */
    setNotificationCallback(callback) {
        this.notificationCallback = callback;
    }

    /**
     * Export alerts
     */
    exportAlerts() {
        return JSON.stringify(Array.from(this.alerts.values()));
    }

    /**
     * Import alerts
     */
    importAlerts(json) {
        try {
            const alerts = JSON.parse(json);
            alerts.forEach(alert => {
                this.alerts.set(alert.id, alert);
                this.nextId = Math.max(this.nextId, alert.id + 1);
            });
        } catch (error) {
            console.error('Failed to import alerts:', error);
        }
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AlertSystem };
}
