/**
 * Chart UI Controller
 * Manages the user interface for chart type selection and controls
 */

class ChartUIController {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            throw new Error(`Container ${containerId} not found`);
        }

        this.currentChart = null;
        this.currentChartType = 'candlestick';
        this.symbol = 'AAPL';
        this.timeframe = '1h';
        this.data = null;

        this.indicatorBuilder = new IndicatorBuilder();
        this.alertSystem = new AlertSystem();
        this.backtestEngine = new BacktestingEngine();

        this.initialize();
    }

    initialize() {
        this.createUI();
        this.attachEventListeners();
        this.loadDefaultChart();
    }

    createUI() {
        this.container.innerHTML = `
            <div class="chart-container-wrapper">
                <!-- Toolbar -->
                <div class="chart-toolbar">
                    <div class="toolbar-section">
                        <label>Symbol:</label>
                        <input type="text" id="symbol-input" value="${this.symbol}" />

                        <label>Timeframe:</label>
                        <select id="timeframe-select">
                            <option value="1m">1 Minute</option>
                            <option value="5m">5 Minutes</option>
                            <option value="15m">15 Minutes</option>
                            <option value="1h" selected>1 Hour</option>
                            <option value="4h">4 Hours</option>
                            <option value="1d">1 Day</option>
                            <option value="1w">1 Week</option>
                        </select>

                        <button id="load-chart-btn" class="btn-primary">Load</button>
                    </div>

                    <div class="toolbar-section">
                        <label>Chart Type:</label>
                        <select id="chart-type-select">
                            <option value="candlestick">Candlestick</option>
                            <option value="renko">Renko</option>
                            <option value="kagi">Kagi</option>
                            <option value="point-figure">Point & Figure</option>
                            <option value="market-profile">Market Profile</option>
                            <option value="footprint">Footprint</option>
                        </select>
                    </div>

                    <div class="toolbar-section">
                        <label>Drawing Tools:</label>
                        <button id="tool-trendline" class="btn-tool" data-tool="trendline">Trend Line</button>
                        <button id="tool-fibonacci" class="btn-tool" data-tool="fibonacci">Fibonacci</button>
                        <button id="tool-horizontal" class="btn-tool" data-tool="horizontal">Horizontal</button>
                        <button id="tool-rectangle" class="btn-tool" data-tool="rectangle">Rectangle</button>
                        <button id="tool-pattern" class="btn-tool" data-tool="pattern">Harmonic</button>
                    </div>

                    <div class="toolbar-section">
                        <button id="add-indicator-btn" class="btn-secondary">Add Indicator</button>
                        <button id="create-alert-btn" class="btn-secondary">Create Alert</button>
                        <button id="backtest-btn" class="btn-secondary">Backtest</button>
                    </div>

                    <div class="toolbar-section">
                        <label>Export:</label>
                        <button id="export-png-btn" class="btn-export">PNG</button>
                        <button id="export-svg-btn" class="btn-export">SVG</button>
                        <button id="export-pdf-btn" class="btn-export">PDF</button>
                        <button id="record-video-btn" class="btn-export">Record</button>
                    </div>
                </div>

                <!-- Chart Canvas -->
                <div id="chart-canvas-container" class="chart-canvas"></div>

                <!-- Sidebar Panels -->
                <div class="chart-sidebar">
                    <!-- Indicators Panel -->
                    <div id="indicators-panel" class="panel" style="display: none;">
                        <h3>Indicators</h3>
                        <div id="indicator-list"></div>
                        <button id="close-indicators-btn" class="btn-close">Close</button>
                    </div>

                    <!-- Alerts Panel -->
                    <div id="alerts-panel" class="panel" style="display: none;">
                        <h3>Alerts</h3>
                        <div id="alert-list"></div>
                        <button id="close-alerts-btn" class="btn-close">Close</button>
                    </div>

                    <!-- Backtest Panel -->
                    <div id="backtest-panel" class="panel" style="display: none;">
                        <h3>Backtest Strategy</h3>
                        <div id="backtest-config"></div>
                        <button id="run-backtest-btn" class="btn-primary">Run Backtest</button>
                        <div id="backtest-results"></div>
                        <button id="close-backtest-btn" class="btn-close">Close</button>
                    </div>
                </div>

                <!-- Chart Settings Panel -->
                <div id="chart-settings-panel" class="settings-panel" style="display: none;">
                    <h3>Chart Settings</h3>
                    <div id="chart-settings-content"></div>
                    <button id="apply-settings-btn" class="btn-primary">Apply</button>
                    <button id="close-settings-btn" class="btn-close">Close</button>
                </div>
            </div>
        `;

        // Add CSS
        this.addStyles();
    }

    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .chart-container-wrapper {
                display: flex;
                flex-direction: column;
                height: 100%;
                position: relative;
            }

            .chart-toolbar {
                display: flex;
                gap: 20px;
                padding: 10px;
                background: #1a1a2e;
                border-bottom: 2px solid #00ff41;
                flex-wrap: wrap;
            }

            .toolbar-section {
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .toolbar-section label {
                color: #00ff41;
                font-weight: bold;
                font-size: 12px;
            }

            .toolbar-section input,
            .toolbar-section select {
                background: #16213e;
                color: #00ff41;
                border: 1px solid #00ff41;
                padding: 5px 10px;
                border-radius: 4px;
                font-family: monospace;
            }

            .btn-primary, .btn-secondary, .btn-tool, .btn-export, .btn-close {
                padding: 6px 12px;
                border: 1px solid #00ff41;
                background: #16213e;
                color: #00ff41;
                cursor: pointer;
                border-radius: 4px;
                font-family: monospace;
                font-size: 12px;
                transition: all 0.2s;
            }

            .btn-primary:hover, .btn-secondary:hover, .btn-tool:hover, .btn-export:hover {
                background: #00ff41;
                color: #1a1a2e;
            }

            .btn-tool.active {
                background: #00ff41;
                color: #1a1a2e;
            }

            .chart-canvas {
                flex: 1;
                background: #1a1a2e;
                position: relative;
            }

            .chart-sidebar {
                position: absolute;
                right: 0;
                top: 60px;
                width: 300px;
                max-height: calc(100% - 60px);
                overflow-y: auto;
                z-index: 100;
            }

            .panel, .settings-panel {
                background: #16213e;
                border: 2px solid #00ff41;
                padding: 15px;
                margin: 10px;
                border-radius: 8px;
                box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
            }

            .panel h3, .settings-panel h3 {
                color: #00ff41;
                margin: 0 0 15px 0;
                font-family: monospace;
            }

            .settings-panel {
                position: absolute;
                right: 320px;
                top: 60px;
                width: 350px;
                z-index: 99;
            }

            #indicator-list, #alert-list {
                max-height: 400px;
                overflow-y: auto;
            }

            .indicator-item, .alert-item {
                background: #1a1a2e;
                padding: 10px;
                margin-bottom: 8px;
                border-radius: 4px;
                border: 1px solid #00ff41;
            }

            .indicator-item h4, .alert-item h4 {
                color: #00ff41;
                margin: 0 0 5px 0;
                font-size: 14px;
            }

            .indicator-item p, .alert-item p {
                color: #aaa;
                margin: 0;
                font-size: 12px;
            }

            .btn-close {
                margin-top: 15px;
                width: 100%;
            }

            #backtest-results {
                margin-top: 15px;
                padding: 10px;
                background: #1a1a2e;
                border-radius: 4px;
                color: #00ff41;
                font-family: monospace;
                font-size: 12px;
            }
        `;
        document.head.appendChild(style);
    }

    attachEventListeners() {
        // Load chart button
        document.getElementById('load-chart-btn').addEventListener('click', () => {
            this.symbol = document.getElementById('symbol-input').value;
            this.timeframe = document.getElementById('timeframe-select').value;
            this.loadChart();
        });

        // Chart type change
        document.getElementById('chart-type-select').addEventListener('change', (e) => {
            this.currentChartType = e.target.value;
            this.updateChart();
        });

        // Drawing tools
        document.querySelectorAll('.btn-tool').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tool = e.target.dataset.tool;
                this.activateDrawingTool(tool);

                // Toggle active state
                document.querySelectorAll('.btn-tool').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
            });
        });

        // Panel toggles
        document.getElementById('add-indicator-btn').addEventListener('click', () => {
            this.togglePanel('indicators-panel');
        });

        document.getElementById('create-alert-btn').addEventListener('click', () => {
            this.togglePanel('alerts-panel');
        });

        document.getElementById('backtest-btn').addEventListener('click', () => {
            this.togglePanel('backtest-panel');
        });

        // Panel close buttons
        document.getElementById('close-indicators-btn').addEventListener('click', () => {
            this.hidePanel('indicators-panel');
        });

        document.getElementById('close-alerts-btn').addEventListener('click', () => {
            this.hidePanel('alerts-panel');
        });

        document.getElementById('close-backtest-btn').addEventListener('click', () => {
            this.hidePanel('backtest-panel');
        });

        // Export buttons
        document.getElementById('export-png-btn').addEventListener('click', () => {
            this.exportChart('png');
        });

        document.getElementById('export-svg-btn').addEventListener('click', () => {
            this.exportChart('svg');
        });

        document.getElementById('export-pdf-btn').addEventListener('click', () => {
            this.exportChart('pdf');
        });

        document.getElementById('record-video-btn').addEventListener('click', () => {
            this.toggleVideoRecording();
        });
    }

    async loadDefaultChart() {
        await this.loadChart();
    }

    async loadChart() {
        try {
            // Fetch data from API
            const response = await fetch('/api/charts/data/ohlcv', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    symbol: this.symbol,
                    timeframe: this.timeframe,
                    limit: 500
                })
            });

            const result = await response.json();

            if (result.success) {
                this.data = result.data;
                this.updateChart();
            } else {
                console.error('Failed to load chart data');
            }
        } catch (error) {
            console.error('Error loading chart:', error);
        }
    }

    updateChart() {
        if (!this.data) return;

        // Destroy existing chart
        if (this.currentChart) {
            this.currentChart.destroy();
        }

        // Create new chart based on type
        const chartContainer = 'chart-canvas-container';

        switch (this.currentChartType) {
            case 'renko':
                this.currentChart = new RenkoChart(chartContainer, {
                    theme: 'dark',
                    responsive: true
                });
                break;

            case 'kagi':
                this.currentChart = new KagiChart(chartContainer, {
                    theme: 'dark',
                    responsive: true
                });
                break;

            case 'point-figure':
                this.currentChart = new PointFigureChart(chartContainer, {
                    theme: 'dark',
                    responsive: true
                });
                break;

            case 'market-profile':
                this.currentChart = new MarketProfileChart(chartContainer, {
                    theme: 'dark',
                    responsive: true
                });
                break;

            case 'footprint':
                this.currentChart = new FootprintChart(chartContainer, {
                    theme: 'dark',
                    responsive: true
                });
                break;

            default:
                // Default candlestick chart
                this.currentChart = new CanvasChart(chartContainer, {
                    theme: 'dark',
                    responsive: true
                });
        }

        // Set data
        this.currentChart.setData(this.data);
    }

    activateDrawingTool(tool) {
        if (!this.currentChart || !this.currentChart.annotationManager) {
            this.currentChart.annotationManager = new AnnotationManager(this.currentChart);
        }

        this.currentChart.annotationManager.setTool(tool);

        if (tool === 'pattern') {
            this.detectHarmonicPatterns();
        }
    }

    detectHarmonicPatterns() {
        if (!this.currentChart) return;

        const patternDetector = new HarmonicPatternAnnotation(this.currentChart.annotationManager);
        const patterns = patternDetector.autoDetect(this.data);

        console.log(`Detected ${patterns.length} harmonic patterns`);
    }

    togglePanel(panelId) {
        const panel = document.getElementById(panelId);
        if (panel.style.display === 'none') {
            // Hide all other panels
            document.querySelectorAll('.panel').forEach(p => p.style.display = 'none');
            panel.style.display = 'block';

            // Load panel content
            if (panelId === 'indicators-panel') {
                this.loadIndicatorsPanel();
            } else if (panelId === 'alerts-panel') {
                this.loadAlertsPanel();
            } else if (panelId === 'backtest-panel') {
                this.loadBacktestPanel();
            }
        } else {
            panel.style.display = 'none';
        }
    }

    hidePanel(panelId) {
        document.getElementById(panelId).style.display = 'none';
    }

    loadIndicatorsPanel() {
        // Populate with available indicators
        const indicatorList = document.getElementById('indicator-list');
        const indicators = ['SMA', 'EMA', 'RSI', 'MACD', 'BB', 'ATR'];

        indicatorList.innerHTML = indicators.map(ind => `
            <div class="indicator-item">
                <h4>${ind}</h4>
                <button onclick="chartUI.addIndicator('${ind}')" class="btn-secondary">Add</button>
            </div>
        `).join('');
    }

    loadAlertsPanel() {
        const alertList = document.getElementById('alert-list');
        const alerts = this.alertSystem.getAllAlerts();

        alertList.innerHTML = alerts.map(alert => `
            <div class="alert-item">
                <h4>${alert.name}</h4>
                <p>${alert.message}</p>
                <button onclick="chartUI.deleteAlert(${alert.id})" class="btn-close">Delete</button>
            </div>
        `).join('');
    }

    loadBacktestPanel() {
        const config = document.getElementById('backtest-config');
        config.innerHTML = `
            <label>Strategy Name:</label>
            <input type="text" id="strategy-name" value="Simple MA Cross" />

            <label>Initial Capital:</label>
            <input type="number" id="initial-capital" value="10000" />

            <button id="run-backtest-btn" class="btn-primary">Run Backtest</button>
        `;

        document.getElementById('run-backtest-btn').addEventListener('click', () => {
            this.runBacktest();
        });
    }

    addIndicator(type) {
        // Add indicator to chart
        console.log(`Adding ${type} indicator`);
        // Implementation would calculate and display indicator
    }

    deleteAlert(id) {
        this.alertSystem.deleteAlert(id);
        this.loadAlertsPanel();
    }

    async runBacktest() {
        const strategyName = document.getElementById('strategy-name').value;
        const initialCapital = parseFloat(document.getElementById('initial-capital').value);

        // Create simple strategy
        this.backtestEngine.createStrategy({
            name: strategyName,
            entryCondition: (ctx) => {
                // Simple MA cross strategy
                return ctx.bar > 50; // Dummy condition
            },
            exitCondition: (ctx) => {
                return false; // Hold
            },
            stopLoss: 2,
            takeProfit: 5
        });

        // Run backtest
        const results = this.backtestEngine.runBacktest(strategyName, this.data, initialCapital);
        const report = this.backtestEngine.generateReport(strategyName);

        // Display results
        const resultsDiv = document.getElementById('backtest-results');
        resultsDiv.innerHTML = `
            <h4>Results</h4>
            <p>Total Return: ${report.summary.totalReturnPercent}</p>
            <p>Win Rate: ${report.summary.winRate}</p>
            <p>Profit Factor: ${report.summary.profitFactor}</p>
            <p>Max Drawdown: ${report.summary.maxDrawdown}</p>
            <p>Total Trades: ${report.summary.totalTrades}</p>
        `;
    }

    async exportChart(format) {
        if (!this.currentChart) return;

        const exporter = new ChartExportManager(this.currentChart);

        switch (format) {
            case 'png':
                await exporter.downloadPNG(`${this.symbol}_${this.timeframe}.png`);
                break;
            case 'svg':
                await exporter.downloadSVG(`${this.symbol}_${this.timeframe}.svg`);
                break;
            case 'pdf':
                await exporter.exportPDF(`${this.symbol}_${this.timeframe}.pdf`);
                break;
        }
    }

    toggleVideoRecording() {
        const btn = document.getElementById('record-video-btn');

        if (!this.videoRecording) {
            const exporter = new ChartExportManager(this.currentChart);
            this.videoRecording = exporter.startRecording();
            btn.textContent = 'Stop Recording';
            btn.style.background = '#ff0050';
        } else {
            this.videoRecording.stop();
            this.videoRecording = null;
            btn.textContent = 'Record';
            btn.style.background = '#16213e';
        }
    }
}

// Initialize when page loads
let chartUI;
document.addEventListener('DOMContentLoaded', () => {
    // Wait for all chart libraries to load
    if (typeof RenkoChart !== 'undefined') {
        chartUI = new ChartUIController('advanced-charts-container');
    }
});

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ChartUIController };
}
