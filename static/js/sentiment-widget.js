/**
 * News Sentiment Widget
 * Real-time sentiment analysis and news feed integration
 */

class SentimentWidget {
    constructor() {
        this.currentSymbol = 'AAPL';
        this.refreshInterval = null;
        this.autoRefreshEnabled = true;
        this.refreshIntervalMs = 5 * 60 * 1000; // 5 minutes

        this.elements = {
            scoreDisplay: document.getElementById('sentiment-score-display'),
            labelDisplay: document.getElementById('sentiment-label-display'),
            positiveCount: document.getElementById('sentiment-positive-count'),
            negativeCount: document.getElementById('sentiment-negative-count'),
            neutralCount: document.getElementById('sentiment-neutral-count'),
            trendDisplay: document.getElementById('sentiment-trend-display'),
            alertsContainer: document.getElementById('sentiment-alerts'),
            alertBanner: document.getElementById('sentiment-alert-banner'),
            alertMessage: document.getElementById('sentiment-alert-message'),
            feedContent: document.getElementById('news-feed-content'),
            loading: document.getElementById('sentiment-loading'),
            refreshBtn: document.getElementById('refresh-sentiment'),
        };

        this.init();
    }

    init() {
        // Set up refresh button
        if (this.elements.refreshBtn) {
            this.elements.refreshBtn.addEventListener('click', () => {
                this.loadSentiment(this.currentSymbol, true);
            });
        }

        // Listen for symbol changes from the main dashboard
        document.addEventListener('symbolChanged', (event) => {
            this.updateSymbol(event.detail.symbol);
        });

        // Start auto-refresh
        if (this.autoRefreshEnabled) {
            this.startAutoRefresh();
        }
    }

    updateSymbol(symbol) {
        // Extract just the symbol without exchange prefix
        const cleanSymbol = symbol.includes(':') ? symbol.split(':')[1] : symbol;

        if (this.currentSymbol !== cleanSymbol) {
            this.currentSymbol = cleanSymbol;
            this.loadSentiment(cleanSymbol);
        }
    }

    async loadSentiment(symbol, forceRefresh = false) {
        if (!symbol) return;

        try {
            this.showLoading(true);

            // Fetch sentiment feed
            const response = await fetch(
                `/api/sentiment/feed/${symbol}?limit=20&include_breaking=true${forceRefresh ? '&cache=false' : ''}`
            );

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();

            if (data.success) {
                this.renderSentiment(data);
            } else {
                this.showError('Failed to load sentiment data');
            }

        } catch (error) {
            console.error('Error loading sentiment:', error);
            this.showError(error.message || 'Failed to load sentiment data');
        } finally {
            this.showLoading(false);
        }
    }

    renderSentiment(data) {
        // Update sentiment summary
        const currentSentiment = data.current_sentiment || {};
        const stats = data.stats || {};

        // Score display
        const score = currentSentiment.score || 0;
        const label = currentSentiment.label || 'neutral';
        const trend = currentSentiment.trend || 'stable';

        if (this.elements.scoreDisplay) {
            this.elements.scoreDisplay.textContent = score.toFixed(2);
            this.elements.scoreDisplay.className = `sentiment-score sentiment-score--${label}`;
        }

        if (this.elements.labelDisplay) {
            this.elements.labelDisplay.textContent = this.formatLabel(label);
            this.elements.labelDisplay.className = `sentiment-status sentiment-status--${label}`;
        }

        // Stats
        if (this.elements.positiveCount) {
            this.elements.positiveCount.textContent = stats.positive_count || 0;
        }
        if (this.elements.negativeCount) {
            this.elements.negativeCount.textContent = stats.negative_count || 0;
        }
        if (this.elements.neutralCount) {
            this.elements.neutralCount.textContent = stats.neutral_count || 0;
        }
        if (this.elements.trendDisplay) {
            this.elements.trendDisplay.textContent = this.formatTrend(trend);
            this.elements.trendDisplay.className = `stat-value trend--${trend}`;
        }

        // Show alerts if sentiment shift detected
        if (currentSentiment.shift_detected) {
            this.showAlert(
                `Sentiment Shift Detected: ${trend === 'improving' ? 'Turning Positive' : 'Turning Negative'}`,
                trend === 'improving' ? 'info' : 'warning'
            );
        } else {
            this.hideAlert();
        }

        // Render news feed
        this.renderNewsFeed(data.feed || []);
    }

    renderNewsFeed(articles) {
        if (!this.elements.feedContent) return;

        if (!articles || articles.length === 0) {
            this.elements.feedContent.innerHTML = `
                <div class="no-news">
                    <p>No recent news available for ${this.currentSymbol}</p>
                </div>
            `;
            return;
        }

        const feedHTML = articles.map(article => this.createArticleCard(article)).join('');
        this.elements.feedContent.innerHTML = feedHTML;

        // Add click handlers to article links
        this.elements.feedContent.querySelectorAll('.news-article-link').forEach(link => {
            link.addEventListener('click', (e) => {
                // Track click analytics if needed
                console.log('Article clicked:', link.href);
            });
        });
    }

    createArticleCard(article) {
        const publishedDate = new Date(article.published_at);
        const timeAgo = this.formatTimeAgo(publishedDate);

        const sentimentClass = article.sentiment_label || 'neutral';
        const sentimentColor = article.sentiment_color || '#6b7280';
        const isBreaking = article.is_breaking;

        return `
            <div class="news-article ${isBreaking ? 'news-article--breaking' : ''}">
                ${isBreaking ? '<div class="breaking-badge">BREAKING</div>' : ''}

                <div class="news-article-header">
                    <div class="news-source">${this.escapeHtml(article.source || 'Unknown')}</div>
                    <div class="news-time">${timeAgo}</div>
                </div>

                <h4 class="news-title">
                    <a href="${this.escapeHtml(article.url)}"
                       target="_blank"
                       rel="noopener noreferrer"
                       class="news-article-link">
                        ${this.escapeHtml(article.title)}
                    </a>
                </h4>

                <p class="news-summary">${this.escapeHtml(article.summary)}</p>

                <div class="news-footer">
                    <div class="sentiment-indicator sentiment-indicator--${sentimentClass}"
                         style="background-color: ${sentimentColor}">
                        <span class="sentiment-score">${article.sentiment_score >= 0 ? '+' : ''}${article.sentiment_score.toFixed(2)}</span>
                        <span class="sentiment-label">${this.formatLabel(article.sentiment_label)}</span>
                    </div>
                    ${article.confidence ? `<div class="confidence-badge">Confidence: ${(article.confidence * 100).toFixed(0)}%</div>` : ''}
                </div>
            </div>
        `;
    }

    showAlert(message, type = 'info') {
        if (!this.elements.alertsContainer || !this.elements.alertMessage) return;

        this.elements.alertMessage.textContent = message;
        this.elements.alertBanner.className = `alert-banner alert-banner--${type}`;
        this.elements.alertsContainer.style.display = 'block';
    }

    hideAlert() {
        if (this.elements.alertsContainer) {
            this.elements.alertsContainer.style.display = 'none';
        }
    }

    showLoading(show) {
        if (this.elements.loading) {
            this.elements.loading.style.display = show ? 'flex' : 'none';
        }
    }

    showError(message) {
        if (this.elements.feedContent) {
            this.elements.feedContent.innerHTML = `
                <div class="error-message">
                    <p>⚠️ ${this.escapeHtml(message)}</p>
                    <button onclick="sentimentWidget.loadSentiment('${this.currentSymbol}', true)">Retry</button>
                </div>
            `;
        }
    }

    startAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }

        this.refreshInterval = setInterval(() => {
            if (this.currentSymbol && this.autoRefreshEnabled) {
                console.log('Auto-refreshing sentiment for', this.currentSymbol);
                this.loadSentiment(this.currentSymbol);
            }
        }, this.refreshIntervalMs);
    }

    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }

    // Utility methods
    formatLabel(label) {
        if (!label) return 'Neutral';
        return label.charAt(0).toUpperCase() + label.slice(1);
    }

    formatTrend(trend) {
        const trendMap = {
            'improving': '↗ Improving',
            'deteriorating': '↘ Deteriorating',
            'stable': '→ Stable',
        };
        return trendMap[trend] || trend;
    }

    formatTimeAgo(date) {
        const seconds = Math.floor((new Date() - date) / 1000);

        const intervals = {
            year: 31536000,
            month: 2592000,
            week: 604800,
            day: 86400,
            hour: 3600,
            minute: 60,
        };

        for (const [unit, secondsInUnit] of Object.entries(intervals)) {
            const interval = Math.floor(seconds / secondsInUnit);
            if (interval >= 1) {
                return `${interval} ${unit}${interval === 1 ? '' : 's'} ago`;
            }
        }

        return 'Just now';
    }

    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    destroy() {
        this.stopAutoRefresh();
    }
}

// Initialize widget when DOM is ready
let sentimentWidget;

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        sentimentWidget = new SentimentWidget();
    });
} else {
    sentimentWidget = new SentimentWidget();
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SentimentWidget;
}
