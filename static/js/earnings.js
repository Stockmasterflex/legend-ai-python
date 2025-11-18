/**
 * Earnings Calendar Module
 * Handles earnings tracking, visualization, and export
 */
(function() {
    'use strict';

    const EarningsCalendar = {
        state: {
            earningsData: [],
            filteredData: [],
            daysAhead: 30,
            sectorFilter: '',
            watchlistEarnings: []
        },

        init() {
            this.cacheDom();
            this.bindEvents();
            this.loadEarningsCalendar();
        },

        cacheDom() {
            this.dom = {
                refreshBtn: document.getElementById('earnings-refresh'),
                exportBtn: document.getElementById('earnings-export'),
                daysAheadSelect: document.getElementById('earnings-days-ahead'),
                sectorFilter: document.getElementById('earnings-sector-filter'),
                calendarGrid: document.getElementById('earnings-calendar-grid'),
                loading: document.getElementById('earnings-loading'),
                totalCount: document.getElementById('earnings-total-count'),
                thisWeekCount: document.getElementById('earnings-this-week'),
                watchlistCount: document.getElementById('earnings-watchlist-count'),
                analysisPanel: document.getElementById('earnings-analysis-panel'),
                analysisTicker: document.getElementById('earnings-analysis-ticker'),
                analysisContent: document.getElementById('earnings-analysis-content'),
                analysisClose: document.getElementById('earnings-analysis-close')
            };
        },

        bindEvents() {
            if (this.dom.refreshBtn) {
                this.dom.refreshBtn.addEventListener('click', () => this.loadEarningsCalendar());
            }
            if (this.dom.exportBtn) {
                this.dom.exportBtn.addEventListener('click', () => this.exportCalendar());
            }
            if (this.dom.daysAheadSelect) {
                this.dom.daysAheadSelect.addEventListener('change', (e) => {
                    this.state.daysAhead = parseInt(e.target.value);
                    this.loadEarningsCalendar();
                });
            }
            if (this.dom.sectorFilter) {
                this.dom.sectorFilter.addEventListener('change', (e) => {
                    this.state.sectorFilter = e.target.value;
                    this.filterAndRender();
                });
            }
            if (this.dom.analysisClose) {
                this.dom.analysisClose.addEventListener('click', () => this.closeAnalysis());
            }
        },

        async loadEarningsCalendar() {
            this.showLoading(true);

            try {
                const response = await fetch(`/api/earnings/calendar?days_ahead=${this.state.daysAhead}`);
                const data = await response.json();

                if (data.success) {
                    this.state.earningsData = data.earnings || [];
                    this.filterAndRender();
                    this.updateStats();
                    this.showToast('Earnings calendar loaded', 'success');
                } else {
                    throw new Error('Failed to load earnings calendar');
                }
            } catch (error) {
                console.error('Error loading earnings:', error);
                this.showToast('Failed to load earnings calendar', 'error');
                this.dom.calendarGrid.innerHTML = '<div class="error-message">Failed to load earnings data. Please try again.</div>';
            } finally {
                this.showLoading(false);
            }

            // Also load watchlist earnings
            this.loadWatchlistEarnings();
        },

        async loadWatchlistEarnings() {
            try {
                const response = await fetch('/api/earnings/watchlist');
                const data = await response.json();

                if (data.success) {
                    this.state.watchlistEarnings = data.earnings || [];
                    this.updateStats();
                }
            } catch (error) {
                console.error('Error loading watchlist earnings:', error);
            }
        },

        filterAndRender() {
            let filtered = this.state.earningsData;

            // Apply sector filter
            if (this.state.sectorFilter) {
                filtered = filtered.filter(e => e.sector === this.state.sectorFilter);
            }

            this.state.filteredData = filtered;
            this.renderCalendar();
        },

        renderCalendar() {
            if (!this.state.filteredData || this.state.filteredData.length === 0) {
                this.dom.calendarGrid.innerHTML = '<div class="empty-state">No earnings found for the selected period.</div>';
                return;
            }

            // Group by date
            const grouped = this.groupByDate(this.state.filteredData);

            let html = '';
            for (const [date, events] of Object.entries(grouped)) {
                html += this.renderDateGroup(date, events);
            }

            this.dom.calendarGrid.innerHTML = html;

            // Bind click events for analysis
            this.dom.calendarGrid.querySelectorAll('.earnings-item').forEach(item => {
                item.addEventListener('click', () => {
                    const ticker = item.dataset.ticker;
                    const date = item.dataset.date;
                    this.showAnalysis(ticker, date);
                });
            });
        },

        groupByDate(earnings) {
            const grouped = {};

            earnings.forEach(event => {
                const date = event.earnings_date ? event.earnings_date.split('T')[0] : 'Unknown';
                if (!grouped[date]) {
                    grouped[date] = [];
                }
                grouped[date].push(event);
            });

            // Sort by date
            return Object.fromEntries(
                Object.entries(grouped).sort((a, b) => a[0].localeCompare(b[0]))
            );
        },

        renderDateGroup(date, events) {
            const dateObj = new Date(date);
            const isToday = this.isToday(dateObj);
            const dayName = dateObj.toLocaleDateString('en-US', { weekday: 'long' });
            const displayDate = dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

            let html = `
                <div class="earnings-date-group ${isToday ? 'earnings-date-today' : ''}">
                    <div class="earnings-date-header">
                        <h3>${displayDate} <span class="day-name">${dayName}</span></h3>
                        <span class="earnings-count">${events.length} ${events.length === 1 ? 'company' : 'companies'}</span>
                    </div>
                    <div class="earnings-items">
            `;

            events.forEach(event => {
                html += this.renderEarningsItem(event, date);
            });

            html += `
                    </div>
                </div>
            `;

            return html;
        },

        renderEarningsItem(event, date) {
            const ticker = event.ticker || 'N/A';
            const beatRate = event.historical_beat_rate !== undefined ? (event.historical_beat_rate * 100).toFixed(0) : 'N/A';
            const avgSurprise = event.historical_avg_surprise !== undefined ? event.historical_avg_surprise.toFixed(1) : 'N/A';
            const reportTime = event.report_time || 'TNS';
            const epsEstimate = event.eps_estimate !== null ? `$${event.eps_estimate.toFixed(2)}` : 'N/A';

            // Color code by beat rate
            let beatRateClass = 'beat-rate-neutral';
            if (beatRate !== 'N/A') {
                const rate = parseFloat(beatRate);
                if (rate >= 75) beatRateClass = 'beat-rate-high';
                else if (rate >= 50) beatRateClass = 'beat-rate-medium';
                else beatRateClass = 'beat-rate-low';
            }

            // Check if in watchlist
            const inWatchlist = this.state.watchlistEarnings.some(w => w.ticker === ticker);

            return `
                <div class="earnings-item ${beatRateClass} ${inWatchlist ? 'in-watchlist' : ''}"
                     data-ticker="${ticker}"
                     data-date="${date}">
                    <div class="earnings-item-header">
                        <div class="ticker-info">
                            <span class="ticker-symbol">${ticker}</span>
                            ${inWatchlist ? '<span class="watchlist-badge">★</span>' : ''}
                        </div>
                        <span class="report-time ${reportTime === 'BMO' ? 'time-bmo' : reportTime === 'AMC' ? 'time-amc' : 'time-tns'}">${reportTime}</span>
                    </div>
                    <div class="earnings-item-body">
                        <div class="earnings-metric">
                            <span class="metric-label">EPS Est.</span>
                            <span class="metric-value">${epsEstimate}</span>
                        </div>
                        <div class="earnings-metric">
                            <span class="metric-label">Beat Rate</span>
                            <span class="metric-value">${beatRate}%</span>
                        </div>
                        <div class="earnings-metric">
                            <span class="metric-label">Avg Surprise</span>
                            <span class="metric-value">${avgSurprise}%</span>
                        </div>
                    </div>
                </div>
            `;
        },

        async showAnalysis(ticker, date) {
            this.dom.analysisTicker.textContent = ticker;
            this.dom.analysisPanel.style.display = 'block';
            this.dom.analysisContent.innerHTML = '<div class="loading-spinner"></div><p>Loading analysis...</p>';

            try {
                // Fetch historical beat/miss data
                const historyResponse = await fetch(`/api/earnings/ticker/${ticker}/history?limit=8`);
                const historyData = await historyResponse.json();

                // Fetch historical reactions
                const reactionsResponse = await fetch(`/api/earnings/ticker/${ticker}/reactions/historical?limit=8`);
                const reactionsData = await reactionsResponse.json();

                // Render analysis
                this.renderAnalysis(ticker, historyData.data, reactionsData.data);
            } catch (error) {
                console.error('Error loading analysis:', error);
                this.dom.analysisContent.innerHTML = '<div class="error-message">Failed to load analysis</div>';
            }
        },

        renderAnalysis(ticker, historyData, reactionsData) {
            const beatRate = (historyData.beat_rate * 100).toFixed(0);
            const avgSurprise = historyData.avg_surprise_pct.toFixed(1);
            const medianSurprise = historyData.median_surprise_pct.toFixed(1);

            const avgGap = reactionsData.avg_gap_pct ? reactionsData.avg_gap_pct.toFixed(2) : 'N/A';
            const avgDayMove = reactionsData.avg_day_move_pct ? reactionsData.avg_day_move_pct.toFixed(2) : 'N/A';
            const avgVolume = reactionsData.avg_volume_ratio ? reactionsData.avg_volume_ratio.toFixed(1) : 'N/A';

            let html = `
                <div class="analysis-section">
                    <h4>Historical Performance</h4>
                    <div class="analysis-stats">
                        <div class="stat">
                            <span class="stat-label">Total Reports</span>
                            <span class="stat-value">${historyData.total_reports}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Beats</span>
                            <span class="stat-value stat-success">${historyData.beats}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Misses</span>
                            <span class="stat-value stat-danger">${historyData.misses}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Beat Rate</span>
                            <span class="stat-value">${beatRate}%</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Avg Surprise</span>
                            <span class="stat-value">${avgSurprise}%</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Median Surprise</span>
                            <span class="stat-value">${medianSurprise}%</span>
                        </div>
                    </div>
                </div>

                <div class="analysis-section">
                    <h4>Historical Price Reaction</h4>
                    <div class="analysis-stats">
                        <div class="stat">
                            <span class="stat-label">Analyzed</span>
                            <span class="stat-value">${reactionsData.total_analyzed}</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Avg Gap</span>
                            <span class="stat-value">${avgGap}%</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Avg Day Move</span>
                            <span class="stat-value">${avgDayMove}%</span>
                        </div>
                        <div class="stat">
                            <span class="stat-label">Avg Volume Ratio</span>
                            <span class="stat-value">${avgVolume}x</span>
                        </div>
                    </div>
                </div>

                <div class="analysis-section">
                    <h4>Recent Earnings History</h4>
                    <div class="earnings-history-table">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>EPS Est.</th>
                                    <th>EPS Act.</th>
                                    <th>Surprise</th>
                                </tr>
                            </thead>
                            <tbody>
            `;

            (historyData.history || []).slice(0, 8).forEach(event => {
                const date = event.earnings_date ? new Date(event.earnings_date).toLocaleDateString() : 'N/A';
                const epsEst = event.eps_estimate !== null ? `$${event.eps_estimate.toFixed(2)}` : 'N/A';
                const epsAct = event.eps_actual !== null ? `$${event.eps_actual.toFixed(2)}` : 'N/A';
                const surprise = event.surprise_pct !== null ? `${event.surprise_pct.toFixed(1)}%` : 'N/A';
                const surpriseClass = event.surprise_pct > 0 ? 'stat-success' : event.surprise_pct < 0 ? 'stat-danger' : '';

                html += `
                    <tr>
                        <td>${date}</td>
                        <td>${epsEst}</td>
                        <td>${epsAct}</td>
                        <td class="${surpriseClass}">${surprise}</td>
                    </tr>
                `;
            });

            html += `
                            </tbody>
                        </table>
                    </div>
                </div>
            `;

            this.dom.analysisContent.innerHTML = html;
        },

        closeAnalysis() {
            this.dom.analysisPanel.style.display = 'none';
        },

        updateStats() {
            this.dom.totalCount.textContent = this.state.filteredData.length;

            // Count this week's earnings
            const now = new Date();
            const oneWeek = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
            const thisWeek = this.state.filteredData.filter(e => {
                if (!e.earnings_date) return false;
                const date = new Date(e.earnings_date);
                return date >= now && date <= oneWeek;
            });
            this.dom.thisWeekCount.textContent = thisWeek.length;

            // Watchlist count
            this.dom.watchlistCount.textContent = this.state.watchlistEarnings.length;
        },

        async exportCalendar() {
            try {
                const format = prompt('Export format (json, csv, ical):', 'ical');
                if (!format) return;

                const response = await fetch(`/api/earnings/export/calendar?format=${format}&days_ahead=${this.state.daysAhead}`);
                const data = await response.json();

                if (data.success) {
                    if (format === 'ical') {
                        // Download as .ics file
                        const blob = new Blob([data.data], { type: 'text/calendar' });
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = 'earnings_calendar.ics';
                        a.click();
                        window.URL.revokeObjectURL(url);
                    } else if (format === 'csv') {
                        // Download as CSV
                        const blob = new Blob([data.data], { type: 'text/csv' });
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = 'earnings_calendar.csv';
                        a.click();
                        window.URL.revokeObjectURL(url);
                    } else {
                        // JSON - copy to clipboard
                        navigator.clipboard.writeText(JSON.stringify(data.data, null, 2));
                        this.showToast('JSON copied to clipboard', 'success');
                    }
                } else {
                    throw new Error('Export failed');
                }
            } catch (error) {
                console.error('Export error:', error);
                this.showToast('Export failed', 'error');
            }
        },

        showLoading(show) {
            if (this.dom.loading) {
                this.dom.loading.style.display = show ? 'flex' : 'none';
            }
        },

        showToast(message, type = 'info') {
            // Use existing toast function if available
            if (typeof toast === 'function') {
                toast(message, type);
            } else {
                console.log(`[${type}] ${message}`);
            }
        },

        isToday(date) {
            const today = new Date();
            return date.toDateString() === today.toDateString();
        }
    };

    // Initialize when earnings tab is shown
    document.addEventListener('DOMContentLoaded', () => {
        // Wait a bit for dashboard to initialize
        setTimeout(() => {
            EarningsCalendar.init();
        }, 500);
    });

    // Expose to global scope if needed
    window.EarningsCalendar = EarningsCalendar;
})();
