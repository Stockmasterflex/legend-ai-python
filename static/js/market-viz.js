/**
 * Market Visualization Dashboard
 *
 * Interactive visualizations for:
 * 1. Sector Heatmap
 * 2. Stock Screener Heatmap
 * 3. Pattern Distribution Map
 * 4. Correlation Matrix
 * 5. Market Breadth Dashboard
 */

// Configuration
const CONFIG = {
    autoRefreshInterval: 5 * 60 * 1000, // 5 minutes
    apiBaseUrl: window.location.origin,
    chartLayout: {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0.3)',
        font: {
            family: 'Inter, sans-serif',
            color: '#e5e7eb'
        },
        margin: { t: 40, r: 20, b: 80, l: 80 },
        hoverlabel: {
            bgcolor: '#1f2937',
            bordercolor: '#3b82f6',
            font: { color: '#e5e7eb' }
        }
    }
};

// Auto-refresh timer
let autoRefreshTimer = null;

/**
 * Initialize dashboard
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Market Visualization Dashboard Initializing...');

    // Load all visualizations
    loadMarketBreadth();
    loadSectorHeatmap();
    loadStockScreener();
    loadPatternDistribution();
    loadCorrelationMatrix();

    // Setup auto-refresh
    setupAutoRefresh();

    // Refresh all button
    document.getElementById('refresh-all').addEventListener('click', refreshAll);
});

/**
 * Setup auto-refresh mechanism
 */
function setupAutoRefresh() {
    if (autoRefreshTimer) {
        clearInterval(autoRefreshTimer);
    }

    autoRefreshTimer = setInterval(() => {
        console.log('🔄 Auto-refreshing all visualizations...');
        refreshAll();
    }, CONFIG.autoRefreshInterval);

    console.log(`✅ Auto-refresh enabled (every ${CONFIG.autoRefreshInterval / 1000 / 60} minutes)`);
}

/**
 * Refresh all visualizations
 */
function refreshAll() {
    loadMarketBreadth();
    loadSectorHeatmap();
    loadStockScreener();
    loadPatternDistribution();
    loadCorrelationMatrix();
}

/**
 * 1. Load Market Breadth Dashboard
 */
async function loadMarketBreadth() {
    try {
        const response = await fetch(`${CONFIG.apiBaseUrl}/api/visualizations/breadth`);
        const result = await response.json();

        if (!result.success) {
            throw new Error(result.detail || 'Failed to load market breadth data');
        }

        const data = result.data;
        const breadth = data.market_breadth;
        const regime = data.regime_details;
        const sectorRotation = data.sector_rotation || {};

        // Update stats
        document.getElementById('adv-decline').textContent = `${breadth.advance_decline_ratio}%`;
        document.getElementById('adv-decline').className = `stat-value ${breadth.advance_decline_ratio > 50 ? 'positive' : 'negative'}`;

        document.getElementById('above-50').textContent = `${breadth.pct_above_50ema}%`;
        document.getElementById('above-50').className = `stat-value ${breadth.pct_above_50ema > 50 ? 'positive' : 'negative'}`;

        document.getElementById('above-200').textContent = `${breadth.pct_above_200ema}%`;
        document.getElementById('above-200').className = `stat-value ${breadth.pct_above_200ema > 50 ? 'positive' : 'negative'}`;

        document.getElementById('new-highs').textContent = breadth.new_highs_52w;
        document.getElementById('new-lows').textContent = breadth.new_lows_52w;
        document.getElementById('market-regime').textContent = data.regime;

        // Sector rotation wheel
        if (sectorRotation.top_performers && sectorRotation.bottom_performers) {
            renderSectorRotationWheel(sectorRotation);
        }

        // Update timestamp
        const timestamp = new Date(data.timestamp).toLocaleTimeString();
        document.getElementById('breadth-updated').textContent = `Updated: ${timestamp}`;

        console.log('✅ Market breadth loaded');

    } catch (error) {
        console.error('❌ Failed to load market breadth:', error);
        showError('breadth-updated', error.message);
    }
}

/**
 * Render sector rotation wheel
 */
function renderSectorRotationWheel(rotation) {
    const topPerformers = rotation.top_performers || [];
    const bottomPerformers = rotation.bottom_performers || [];

    const labels = [
        ...topPerformers.map(s => `${s.name} (+${s.performance}%)`),
        ...bottomPerformers.map(s => `${s.name} (${s.performance}%)`)
    ];

    const values = [
        ...topPerformers.map(s => Math.abs(s.performance)),
        ...bottomPerformers.map(s => Math.abs(s.performance))
    ];

    const colors = [
        ...topPerformers.map(() => '#22c55e'),
        ...bottomPerformers.map(() => '#ef4444')
    ];

    const data = [{
        type: 'pie',
        labels: labels,
        values: values,
        marker: {
            colors: colors,
            line: { color: '#1f2937', width: 2 }
        },
        hole: 0.4,
        textinfo: 'label+percent',
        textposition: 'outside',
        hovertemplate: '<b>%{label}</b><br>%{value:.2f}%<extra></extra>'
    }];

    const layout = {
        ...CONFIG.chartLayout,
        title: {
            text: 'Sector Rotation (Top & Bottom Performers)',
            font: { size: 16, color: '#3b82f6' }
        },
        showlegend: false,
        height: 400
    };

    Plotly.newPlot('sector-rotation-wheel', data, layout, { responsive: true, displayModeBar: false });
}

/**
 * 2. Load Sector Heatmap
 */
async function loadSectorHeatmap() {
    const period = document.getElementById('sector-period').value;

    try {
        const response = await fetch(`${CONFIG.apiBaseUrl}/api/visualizations/sectors?period=${period}`);
        const result = await response.json();

        if (!result.success) {
            throw new Error(result.detail || 'Failed to load sector data');
        }

        const sectors = result.data.sectors;

        // Prepare treemap data
        const labels = sectors.map(s => s.name);
        const parents = sectors.map(() => '');
        const values = sectors.map(s => s.market_cap);
        const texts = sectors.map(s => `${s.name}<br>${s.performance > 0 ? '+' : ''}${s.performance}%`);
        const colors = sectors.map(s => s.performance);

        const data = [{
            type: 'treemap',
            labels: labels,
            parents: parents,
            values: values,
            text: texts,
            textposition: 'middle center',
            marker: {
                colors: colors,
                colorscale: [
                    [0, '#ef4444'],
                    [0.5, '#fbbf24'],
                    [1, '#22c55e']
                ],
                cmid: 0,
                colorbar: {
                    title: 'Performance %',
                    thickness: 20,
                    len: 0.7
                },
                line: { color: '#1f2937', width: 2 }
            },
            hovertemplate: '<b>%{label}</b><br>Performance: %{color:.2f}%<br>Size: Market Cap<extra></extra>'
        }];

        const layout = {
            ...CONFIG.chartLayout,
            title: {
                text: `Sector Performance - ${period.replace('1', '')}`,
                font: { size: 18, color: '#3b82f6' }
            },
            height: 500
        };

        Plotly.newPlot('sector-heatmap', data, layout, { responsive: true, displayModeBar: false });

        // Add click handler for drill-down
        document.getElementById('sector-heatmap').on('plotly_click', (data) => {
            const ticker = sectors[data.points[0].pointNumber].ticker;
            console.log(`🔍 Clicked sector: ${ticker}`);
            // TODO: Implement drill-down to individual stocks
        });

        // Update timestamp
        const timestamp = new Date(result.data.timestamp).toLocaleTimeString();
        document.getElementById('sector-updated').textContent = `Updated: ${timestamp}`;

        console.log('✅ Sector heatmap loaded');

    } catch (error) {
        console.error('❌ Failed to load sector heatmap:', error);
        showError('sector-updated', error.message);
    }
}

/**
 * 3. Load Stock Screener Heatmap
 */
async function loadStockScreener() {
    const universe = document.getElementById('screener-universe').value;
    const colorBy = document.getElementById('screener-color').value;
    const sizeBy = document.getElementById('screener-size').value;

    try {
        const response = await fetch(
            `${CONFIG.apiBaseUrl}/api/visualizations/screener?universe=${universe}&color_by=${colorBy}&size_by=${sizeBy}&limit=100`
        );
        const result = await response.json();

        if (!result.success) {
            throw new Error(result.detail || 'Failed to load screener data');
        }

        const stocks = result.data.stocks;

        // Prepare treemap data
        const labels = stocks.map(s => s.ticker);
        const parents = stocks.map(s => s.sector || '');
        const values = stocks.map(s => s[sizeBy]);
        const colors = stocks.map(s => s[colorBy]);
        const texts = stocks.map(s =>
            `${s.ticker}<br>${colorBy === 'change' ? (s.change > 0 ? '+' : '') + s.change + '%' : colorBy === 'rs_rating' ? 'RS: ' + s.rs_rating : 'Vol: ' + s.volume}`
        );

        const data = [{
            type: 'treemap',
            labels: labels,
            parents: parents,
            values: values,
            text: texts,
            textposition: 'middle center',
            marker: {
                colors: colors,
                colorscale: colorBy === 'change' ? [
                    [0, '#ef4444'],
                    [0.5, '#fbbf24'],
                    [1, '#22c55e']
                ] : 'Viridis',
                cmid: colorBy === 'change' ? 0 : null,
                colorbar: {
                    title: colorBy === 'change' ? '% Change' : colorBy === 'rs_rating' ? 'RS Rating' : 'Volume',
                    thickness: 20,
                    len: 0.7
                },
                line: { color: '#1f2937', width: 1 }
            },
            hovertemplate: '<b>%{label}</b><br>Price: $%{customdata[0]}<br>Change: %{customdata[1]}%<br>RS: %{customdata[2]}<extra></extra>',
            customdata: stocks.map(s => [s.price, s.change, s.rs_rating])
        }];

        const layout = {
            ...CONFIG.chartLayout,
            title: {
                text: `Stock Screener - ${universe.toUpperCase()} (Color: ${colorBy}, Size: ${sizeBy})`,
                font: { size: 18, color: '#3b82f6' }
            },
            height: 600
        };

        Plotly.newPlot('stock-screener', data, layout, { responsive: true, displayModeBar: false });

        // Add click handler
        document.getElementById('stock-screener').on('plotly_click', (data) => {
            const ticker = stocks[data.points[0].pointNumber].ticker;
            console.log(`🔍 Clicked stock: ${ticker}`);
            // TODO: Open analysis for clicked stock
        });

        // Update timestamp
        const timestamp = new Date(result.data.timestamp).toLocaleTimeString();
        document.getElementById('screener-updated').textContent = `Updated: ${timestamp}`;

        console.log('✅ Stock screener loaded');

    } catch (error) {
        console.error('❌ Failed to load stock screener:', error);
        showError('screener-updated', error.message);
    }
}

/**
 * 4. Load Pattern Distribution Map
 */
async function loadPatternDistribution() {
    const universe = document.getElementById('pattern-universe').value;

    try {
        const response = await fetch(
            `${CONFIG.apiBaseUrl}/api/visualizations/patterns?universe=${universe}&min_score=0.5`
        );
        const result = await response.json();

        if (!result.success) {
            throw new Error(result.detail || 'Failed to load pattern data');
        }

        const patternCounts = result.data.pattern_counts;
        const patterns = result.data.patterns;

        // Prepare sunburst data
        const labels = ['All Patterns', ...Object.keys(patternCounts)];
        const parents = ['', ...Object.keys(patternCounts).map(() => 'All Patterns')];
        const values = [
            Object.values(patternCounts).reduce((a, b) => a + b, 0),
            ...Object.values(patternCounts)
        ];

        const colors = [
            '#3b82f6',
            ...Object.keys(patternCounts).map((_, i) => {
                const hue = (i * 360 / Object.keys(patternCounts).length);
                return `hsl(${hue}, 70%, 60%)`;
            })
        ];

        const data = [{
            type: 'sunburst',
            labels: labels,
            parents: parents,
            values: values,
            marker: {
                colors: colors,
                line: { color: '#1f2937', width: 2 }
            },
            branchvalues: 'total',
            hovertemplate: '<b>%{label}</b><br>Count: %{value}<br>%{percentParent}<extra></extra>'
        }];

        const layout = {
            ...CONFIG.chartLayout,
            title: {
                text: `Pattern Distribution - ${universe.toUpperCase()} (${patterns.length} patterns detected)`,
                font: { size: 16, color: '#3b82f6' }
            },
            height: 500,
            sunburstcolorway: colors
        };

        Plotly.newPlot('pattern-distribution', data, layout, { responsive: true, displayModeBar: false });

        // Add click handler
        document.getElementById('pattern-distribution').on('plotly_sunburstclick', (data) => {
            console.log(`🔍 Clicked pattern: ${data.points[0].label}`);
            // TODO: Show stocks with this pattern
        });

        console.log('✅ Pattern distribution loaded');

    } catch (error) {
        console.error('❌ Failed to load pattern distribution:', error);
        showError('pattern-distribution', 'Failed to load patterns');
    }
}

/**
 * 5. Load Correlation Matrix
 */
async function loadCorrelationMatrix() {
    const period = document.getElementById('correlation-period').value;
    const tickers = 'SPY,QQQ,IWM,DIA,XLK,XLF,XLV,XLE';

    try {
        const response = await fetch(
            `${CONFIG.apiBaseUrl}/api/visualizations/correlation?tickers=${tickers}&period=${period}`
        );
        const result = await response.json();

        if (!result.success) {
            throw new Error(result.detail || 'Failed to load correlation data');
        }

        const matrix = result.data.correlation_matrix;
        const tickerList = result.data.tickers;

        // Extract correlation values for heatmap
        const zValues = matrix.map(row => row.map(cell => cell.correlation));

        const data = [{
            type: 'heatmap',
            x: tickerList,
            y: tickerList,
            z: zValues,
            colorscale: [
                [0, '#ef4444'],
                [0.5, '#fbbf24'],
                [1, '#22c55e']
            ],
            zmin: -1,
            zmax: 1,
            colorbar: {
                title: 'Correlation',
                thickness: 20,
                len: 0.7
            },
            hovertemplate: '<b>%{x} vs %{y}</b><br>Correlation: %{z:.3f}<extra></extra>'
        }];

        const layout = {
            ...CONFIG.chartLayout,
            title: {
                text: `Correlation Matrix - ${period} Days`,
                font: { size: 16, color: '#3b82f6' }
            },
            xaxis: {
                title: '',
                tickangle: -45,
                color: '#e5e7eb'
            },
            yaxis: {
                title: '',
                color: '#e5e7eb'
            },
            height: 500
        };

        Plotly.newPlot('correlation-matrix', data, layout, { responsive: true, displayModeBar: false });

        // Display leaders/laggers
        const leaders = result.data.leaders || [];
        const laggers = result.data.laggers || [];

        console.log('📊 Market Leaders:', leaders);
        console.log('📉 Market Laggers:', laggers);
        console.log('✅ Correlation matrix loaded');

    } catch (error) {
        console.error('❌ Failed to load correlation matrix:', error);
        showError('correlation-matrix', 'Failed to load correlation');
    }
}

/**
 * Show error message
 */
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = `Error: ${message}`;
        element.style.color = '#ef4444';
    }
}

/**
 * Format large numbers
 */
function formatNumber(num) {
    if (num >= 1e9) return `$${(num / 1e9).toFixed(2)}B`;
    if (num >= 1e6) return `$${(num / 1e6).toFixed(2)}M`;
    if (num >= 1e3) return `$${(num / 1e3).toFixed(2)}K`;
    return `$${num.toFixed(2)}`;
}

console.log('✅ Market Visualization Dashboard Loaded');
