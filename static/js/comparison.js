/**
 * Multi-Ticker Comparison Module
 * Handles all comparison features including multi-charts, metrics table, RS, correlation, and pair trading
 */

// State management
let comparisonData = null;
let currentView = 'charts';
let sortColumn = null;
let sortDirection = 'desc';

// Initialize comparison module
function initComparison() {
    // Main comparison button
    const analyzeBtn = document.getElementById('comparison-analyze-btn');
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', handleComparisonAnalyze);
    }

    // Export CSV button
    const exportBtn = document.getElementById('comparison-export-csv-btn');
    if (exportBtn) {
        exportBtn.addEventListener('click', handleExportCSV);
    }

    // Sub-tab switching
    const subtabs = document.querySelectorAll('.comparison-subtab');
    subtabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            switchComparisonView(e.target.dataset.comparisonView);
        });
    });

    // Pair trading button
    const pairBtn = document.getElementById('pair-analyze-btn');
    if (pairBtn) {
        pairBtn.addEventListener('click', handlePairTradingAnalyze);
    }

    // Table sorting
    const sortableHeaders = document.querySelectorAll('.metrics-table th.sortable');
    sortableHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const sortKey = header.dataset.sort;
            handleTableSort(sortKey);
        });
    });
}

// Handle comparison analyze
async function handleComparisonAnalyze() {
    const tickersInput = document.getElementById('comparison-tickers').value.trim();
    const benchmark = document.getElementById('comparison-benchmark').value.trim() || 'SPY';
    const interval = document.getElementById('comparison-interval').value;
    const bars = parseInt(document.getElementById('comparison-bars').value) || 252;

    if (!tickersInput) {
        showToast('Please enter at least 2 tickers', 'error');
        return;
    }

    const tickers = tickersInput.split(',').map(t => t.trim().toUpperCase()).filter(t => t);

    if (tickers.length < 2) {
        showToast('Please enter at least 2 tickers', 'error');
        return;
    }

    if (tickers.length > 9) {
        showToast('Maximum 9 tickers allowed', 'error');
        return;
    }

    // Show loading
    showComparisonLoading(true);

    try {
        const response = await fetch('/api/comparison/compare', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                tickers,
                benchmark,
                interval,
                bars,
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        comparisonData = data;
        renderComparisonResults(data);
        showToast('Comparison completed successfully', 'success');
    } catch (error) {
        console.error('Comparison error:', error);
        showToast(`Comparison failed: ${error.message}`, 'error');
    } finally {
        showComparisonLoading(false);
    }
}

// Render comparison results based on current view
function renderComparisonResults(data) {
    switch (currentView) {
        case 'charts':
            renderMultiChartView(data);
            break;
        case 'metrics':
            renderMetricsTable(data);
            break;
        case 'relative-strength':
            renderRelativeStrength(data);
            break;
        case 'correlation':
            renderCorrelation(data);
            break;
        default:
            renderMultiChartView(data);
    }
}

// Render multi-chart grid
function renderMultiChartView(data) {
    const gridContainer = document.getElementById('comparison-chart-grid');
    if (!gridContainer) return;

    gridContainer.innerHTML = '';

    const tickers = data.tickers || [];
    const chartData = data.chart_data || {};

    // Create grid layout
    const gridCols = tickers.length <= 4 ? 2 : 3;
    gridContainer.style.display = 'grid';
    gridContainer.style.gridTemplateColumns = `repeat(${gridCols}, 1fr)`;
    gridContainer.style.gap = '1rem';

    tickers.forEach(ticker => {
        const tickerData = chartData[ticker];
        if (!tickerData || tickerData.error) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'chart-error';
            errorDiv.innerHTML = `
                <h4>${ticker}</h4>
                <p class="error-text">${tickerData?.error || 'No data available'}</p>
            `;
            gridContainer.appendChild(errorDiv);
            return;
        }

        const chartContainer = document.createElement('div');
        chartContainer.className = 'comparison-chart-item';
        chartContainer.innerHTML = `
            <div class="chart-header">
                <h4>${ticker}</h4>
                <span class="chart-price">$${getLatestPrice(tickerData)}</span>
            </div>
            <div class="mini-chart" data-ticker="${ticker}">
                <canvas id="chart-${ticker}"></canvas>
            </div>
        `;
        gridContainer.appendChild(chartContainer);

        // Render mini chart using Chart.js
        setTimeout(() => renderMiniChart(ticker, tickerData), 0);
    });
}

// Render mini chart for a ticker
function renderMiniChart(ticker, data) {
    const canvas = document.getElementById(`chart-${ticker}`);
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const closes = data.close || [];
    const timestamps = data.timestamps || [];

    // Simple line chart
    const chartData = {
        labels: timestamps.map(t => new Date(t * 1000).toLocaleDateString()),
        datasets: [{
            label: ticker,
            data: closes,
            borderColor: getTickerColor(ticker),
            backgroundColor: 'transparent',
            borderWidth: 2,
            tension: 0.1,
            pointRadius: 0,
        }]
    };

    new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                x: {
                    display: false,
                },
                y: {
                    display: true,
                    position: 'right',
                }
            },
            interaction: {
                mode: 'index',
                intersect: false,
            }
        }
    });
}

// Render metrics comparison table
function renderMetricsTable(data) {
    const tableBody = document.querySelector('#comparison-metrics-table tbody');
    if (!tableBody) return;

    tableBody.innerHTML = '';

    const tickers = data.tickers || [];
    const metrics = data.metrics || {};
    const relativeStrength = data.relative_strength || {};

    if (tickers.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="10" class="placeholder-text">No data available</td></tr>';
        return;
    }

    // Build rows
    const rows = tickers.map(ticker => {
        const m = metrics[ticker] || {};
        const rs = relativeStrength[ticker] || {};

        return {
            ticker,
            current_price: m.current_price || 0,
            returns_1d: m.returns_1d || 0,
            returns_5d: m.returns_5d || 0,
            returns_20d: m.returns_20d || 0,
            returns_60d: m.returns_60d || 0,
            volatility_20d: m.volatility_20d || 0,
            volume_ratio: m.volume_ratio || 0,
            rs_rank: rs.rank || 0,
            dist_from_high_pct: m.dist_from_high_pct || 0,
        };
    });

    // Sort if column is selected
    if (sortColumn) {
        rows.sort((a, b) => {
            const aVal = a[sortColumn] || 0;
            const bVal = b[sortColumn] || 0;
            return sortDirection === 'asc' ? aVal - bVal : bVal - aVal;
        });
    }

    // Render rows
    rows.forEach((row, index) => {
        const tr = document.createElement('tr');

        // Highlight top performers
        if (sortColumn && index === 0) {
            tr.classList.add('highlight-leader');
        }

        tr.innerHTML = `
            <td><strong>${row.ticker}</strong></td>
            <td>${formatNumber(row.current_price, 2)}</td>
            <td class="${getChangeClass(row.returns_1d)}">${formatPercent(row.returns_1d)}</td>
            <td class="${getChangeClass(row.returns_5d)}">${formatPercent(row.returns_5d)}</td>
            <td class="${getChangeClass(row.returns_20d)}">${formatPercent(row.returns_20d)}</td>
            <td class="${getChangeClass(row.returns_60d)}">${formatPercent(row.returns_60d)}</td>
            <td>${formatNumber(row.volatility_20d, 2)}%</td>
            <td>${formatNumber(row.volume_ratio, 2)}x</td>
            <td>${formatNumber(row.rs_rank, 0)}</td>
            <td class="${getChangeClass(row.dist_from_high_pct)}">${formatPercent(row.dist_from_high_pct)}</td>
        `;
        tableBody.appendChild(tr);
    });
}

// Render relative strength view
function renderRelativeStrength(data) {
    const rankingsContainer = document.getElementById('rs-rankings-container');
    const leadersContainer = document.getElementById('rs-leaders-list');
    const laggardsContainer = document.getElementById('rs-laggards-list');

    if (!rankingsContainer || !data.relative_strength) return;

    const tickers = data.tickers || [];
    const rsData = data.relative_strength || {};

    // Build rankings
    const rankings = tickers.map(ticker => ({
        ticker,
        rank: rsData[ticker]?.rank || 0,
        slope: rsData[ticker]?.slope || 0,
        delta: rsData[ticker]?.delta_vs_benchmark || 0,
        strength: rsData[ticker]?.strength_label || 'Unknown',
    })).sort((a, b) => b.rank - a.rank);

    // Render rankings
    rankingsContainer.innerHTML = rankings.map(r => `
        <div class="rs-ranking-item">
            <div class="rs-ticker">${r.ticker}</div>
            <div class="rs-rank ${getRSClass(r.rank)}">${r.rank}</div>
            <div class="rs-strength">${r.strength}</div>
            <div class="rs-delta ${getChangeClass(r.delta)}">${formatPercent(r.delta)}</div>
        </div>
    `).join('');

    // Render leaders (top 30%)
    const leaderCount = Math.max(1, Math.floor(rankings.length * 0.3));
    const leaders = rankings.slice(0, leaderCount);
    leadersContainer.innerHTML = leaders.map(l => `
        <div class="leader-item">${l.ticker} (${l.rank})</div>
    `).join('');

    // Render laggards (bottom 30%)
    const laggardCount = Math.max(1, Math.floor(rankings.length * 0.3));
    const laggards = rankings.slice(-laggardCount);
    laggardsContainer.innerHTML = laggards.map(l => `
        <div class="laggard-item">${l.ticker} (${l.rank})</div>
    `).join('');
}

// Render correlation matrices
function renderCorrelation(data) {
    const priceMatrixContainer = document.getElementById('price-correlation-matrix');
    const volumeMatrixContainer = document.getElementById('volume-correlation-matrix');

    if (!data.correlation_matrix) return;

    const corrData = data.correlation_matrix;
    const tickers = corrData.tickers || [];

    // Render price correlation
    if (priceMatrixContainer && corrData.price_correlation) {
        priceMatrixContainer.innerHTML = renderCorrelationMatrix(
            tickers,
            corrData.price_correlation
        );
    }

    // Render volume correlation
    if (volumeMatrixContainer && corrData.volume_correlation) {
        volumeMatrixContainer.innerHTML = renderCorrelationMatrix(
            tickers,
            corrData.volume_correlation
        );
    }
}

// Render correlation matrix HTML
function renderCorrelationMatrix(tickers, matrix) {
    let html = '<table class="correlation-matrix"><thead><tr><th></th>';

    // Header row
    tickers.forEach(ticker => {
        html += `<th>${ticker}</th>`;
    });
    html += '</tr></thead><tbody>';

    // Data rows
    tickers.forEach(ticker1 => {
        html += `<tr><th>${ticker1}</th>`;
        tickers.forEach(ticker2 => {
            const value = matrix[ticker1]?.[ticker2];
            const colorClass = getCorrelationClass(value);
            html += `<td class="${colorClass}">${formatNumber(value, 2)}</td>`;
        });
        html += '</tr>';
    });

    html += '</tbody></table>';
    return html;
}

// Handle pair trading analysis
async function handlePairTradingAnalyze() {
    const ticker1 = document.getElementById('pair-ticker1').value.trim().toUpperCase();
    const ticker2 = document.getElementById('pair-ticker2').value.trim().toUpperCase();
    const interval = document.getElementById('comparison-interval').value;
    const bars = parseInt(document.getElementById('comparison-bars').value) || 252;

    if (!ticker1 || !ticker2) {
        showToast('Please enter both tickers', 'error');
        return;
    }

    const loadingEl = document.getElementById('pair-trading-loading');
    if (loadingEl) loadingEl.hidden = false;

    try {
        const response = await fetch('/api/comparison/pair-trading', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticker1, ticker2, interval, bars }),
        });

        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const data = await response.json();
        if (data.error) throw new Error(data.error);

        renderPairTradingResults(data);
        showToast('Pair trading analysis complete', 'success');
    } catch (error) {
        console.error('Pair trading error:', error);
        showToast(`Analysis failed: ${error.message}`, 'error');
    } finally {
        if (loadingEl) loadingEl.hidden = true;
    }
}

// Render pair trading results
function renderPairTradingResults(data) {
    // Render spread chart
    renderPairChart('pair-spread-canvas', data.timestamps, data.spread, 'Spread');

    // Render z-score chart
    renderPairChart('pair-zscore-canvas', data.timestamps, data.z_scores, 'Z-Score');

    // Render statistics
    const statsContainer = document.getElementById('pair-stats-container');
    if (statsContainer && data.statistics && data.cointegration) {
        statsContainer.innerHTML = `
            <div class="stat-item">
                <span class="stat-label">Current Spread:</span>
                <span class="stat-value">${formatNumber(data.statistics.current_spread, 4)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Current Z-Score:</span>
                <span class="stat-value ${getZScoreClass(data.statistics.current_zscore)}">
                    ${formatNumber(data.statistics.current_zscore, 2)}
                </span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Spread Mean:</span>
                <span class="stat-value">${formatNumber(data.statistics.spread_mean, 4)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Spread StdDev:</span>
                <span class="stat-value">${formatNumber(data.statistics.spread_std, 4)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Hedge Ratio:</span>
                <span class="stat-value">${formatNumber(data.hedge_ratio, 4)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Cointegration:</span>
                <span class="stat-value ${data.cointegration.is_cointegrated ? 'positive' : 'negative'}">
                    ${data.cointegration.result} (p=${formatNumber(data.cointegration.p_value, 4)})
                </span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Signal:</span>
                <span class="stat-value signal-${data.signals?.current_signal?.toLowerCase()}">
                    ${data.signals?.current_signal || 'NONE'}
                </span>
            </div>
        `;
    }
}

// Render pair trading chart
function renderPairChart(canvasId, timestamps, data, label) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: timestamps.map(t => new Date(t * 1000).toLocaleDateString()),
            datasets: [{
                label,
                data,
                borderColor: '#00d4ff',
                backgroundColor: 'rgba(0, 212, 255, 0.1)',
                borderWidth: 2,
                tension: 0.1,
                pointRadius: 0,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false },
            },
            scales: {
                x: { display: true },
                y: { display: true }
            }
        }
    });
}

// Switch comparison view
function switchComparisonView(view) {
    currentView = view;

    // Update subtab buttons
    document.querySelectorAll('.comparison-subtab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.comparisonView === view);
    });

    // Hide all views
    document.querySelectorAll('.comparison-view').forEach(v => {
        v.hidden = true;
    });

    // Show selected view
    const viewEl = document.getElementById(`comparison-view-${view}`);
    if (viewEl) {
        viewEl.hidden = false;
    }

    // Re-render if we have data
    if (comparisonData) {
        renderComparisonResults(comparisonData);
    }
}

// Handle table sorting
function handleTableSort(column) {
    if (sortColumn === column) {
        sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
        sortColumn = column;
        sortDirection = 'desc';
    }

    if (comparisonData) {
        renderMetricsTable(comparisonData);
    }
}

// Export metrics to CSV
function handleExportCSV() {
    if (!comparisonData || !comparisonData.metrics) {
        showToast('No data to export', 'error');
        return;
    }

    const tickers = comparisonData.tickers || [];
    const metrics = comparisonData.metrics || {};
    const rs = comparisonData.relative_strength || {};

    // Build CSV
    let csv = 'Ticker,Price,1D %,5D %,20D %,60D %,Volatility,Volume Ratio,RS Rank,Dist from High\n';

    tickers.forEach(ticker => {
        const m = metrics[ticker] || {};
        const r = rs[ticker] || {};
        csv += [
            ticker,
            m.current_price || '',
            m.returns_1d || '',
            m.returns_5d || '',
            m.returns_20d || '',
            m.returns_60d || '',
            m.volatility_20d || '',
            m.volume_ratio || '',
            r.rank || '',
            m.dist_from_high_pct || '',
        ].join(',') + '\n';
    });

    // Download
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `comparison_${Date.now()}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);

    showToast('CSV exported successfully', 'success');
}

// Helper: Show/hide loading
function showComparisonLoading(show) {
    const loadingEl = document.getElementById('comparison-loading');
    if (loadingEl) {
        loadingEl.hidden = !show;
    }
}

// Helper: Get latest price
function getLatestPrice(data) {
    const closes = data.close || [];
    return closes.length > 0 ? closes[closes.length - 1].toFixed(2) : '—';
}

// Helper: Get ticker color (for charts)
function getTickerColor(ticker) {
    const colors = ['#00d4ff', '#ff006e', '#00ff88', '#ffaa00', '#aa00ff', '#ff0044', '#00aaff', '#ffff00', '#00ffff'];
    const hash = ticker.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    return colors[hash % colors.length];
}

// Helper: Get change class
function getChangeClass(value) {
    if (!value) return '';
    return value >= 0 ? 'positive' : 'negative';
}

// Helper: Get RS class
function getRSClass(rank) {
    if (rank >= 80) return 'rs-very-strong';
    if (rank >= 60) return 'rs-strong';
    if (rank >= 40) return 'rs-neutral';
    if (rank >= 20) return 'rs-weak';
    return 'rs-very-weak';
}

// Helper: Get correlation class
function getCorrelationClass(value) {
    if (value === null || value === undefined) return '';
    if (value >= 0.7) return 'corr-high';
    if (value >= 0.3) return 'corr-medium';
    if (value >= -0.3) return 'corr-low';
    if (value >= -0.7) return 'corr-medium-neg';
    return 'corr-high-neg';
}

// Helper: Get z-score class
function getZScoreClass(zscore) {
    if (!zscore) return '';
    const abs = Math.abs(zscore);
    if (abs >= 2) return 'zscore-extreme';
    if (abs >= 1) return 'zscore-moderate';
    return 'zscore-normal';
}

// Helper: Format number
function formatNumber(value, decimals = 2) {
    if (value === null || value === undefined) return '—';
    return Number(value).toFixed(decimals);
}

// Helper: Format percent
function formatPercent(value) {
    if (value === null || value === undefined) return '—';
    const sign = value >= 0 ? '+' : '';
    return `${sign}${value.toFixed(2)}%`;
}

// Helper: Show toast notification
function showToast(message, type = 'info') {
    // Reuse existing toast system from dashboard.js
    if (typeof window.showToast === 'function') {
        window.showToast(message, type);
    } else {
        console.log(`[${type.toUpperCase()}] ${message}`);
    }
}

// Initialize on DOM load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initComparison);
} else {
    initComparison();
}

// Export for external use
window.ComparisonModule = {
    init: initComparison,
    switchView: switchComparisonView,
};
