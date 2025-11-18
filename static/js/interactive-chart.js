/**
 * Legend AI Interactive Chart System
 * Built with Lightweight Charts by TradingView
 *
 * Features:
 * - Candlestick charts with zoom/pan
 * - Volume bars
 * - Multiple timeframes
 * - Technical indicators
 * - Drawing tools
 * - Pattern annotations
 * - Chart presets
 * - Export/share functionality
 */

class InteractiveChart {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.container = document.getElementById(containerId);
        if (!this.container) {
            throw new Error(`Container ${containerId} not found`);
        }

        // Chart instance and series
        this.chart = null;
        this.candleSeries = null;
        this.volumeSeries = null;
        this.indicatorSeries = {};
        this.drawings = [];
        this.annotations = [];

        // Data
        this.symbol = options.symbol || '';
        this.timeframe = options.timeframe || '1D';
        this.candleData = [];
        this.volumeData = [];

        // State
        this.activeIndicators = new Set();
        this.activeDrawingTool = null;
        this.currentPreset = 'clean';
        this.drawingMode = false;

        // Initialize
        this.init();
    }

    init() {
        // Create chart container structure
        this.createChartUI();

        // Initialize Lightweight Charts
        this.initChart();

        // Setup event listeners
        this.setupEventListeners();
    }

    createChartUI() {
        this.container.innerHTML = `
            <div class="interactive-chart-wrapper">
                <!-- Toolbar -->
                <div class="chart-toolbar">
                    <div class="toolbar-section">
                        <button class="toolbar-btn" data-action="timeframe" data-value="1D" title="1 Day">1D</button>
                        <button class="toolbar-btn" data-action="timeframe" data-value="1W" title="1 Week">1W</button>
                        <button class="toolbar-btn" data-action="timeframe" data-value="1M" title="1 Month">1M</button>
                    </div>

                    <div class="toolbar-section">
                        <div class="dropdown">
                            <button class="toolbar-btn dropdown-toggle" data-toggle="indicators">
                                <span class="icon">📊</span> Indicators
                            </button>
                            <div class="dropdown-menu" data-menu="indicators">
                                <label class="dropdown-item">
                                    <input type="checkbox" data-indicator="ema21"> EMA 21
                                </label>
                                <label class="dropdown-item">
                                    <input type="checkbox" data-indicator="sma50"> SMA 50
                                </label>
                                <label class="dropdown-item">
                                    <input type="checkbox" data-indicator="sma200"> SMA 200
                                </label>
                                <label class="dropdown-item">
                                    <input type="checkbox" data-indicator="bb"> Bollinger Bands
                                </label>
                                <label class="dropdown-item">
                                    <input type="checkbox" data-indicator="vwap"> VWAP
                                </label>
                                <label class="dropdown-item">
                                    <input type="checkbox" data-indicator="volume_profile"> Volume Profile
                                </label>
                            </div>
                        </div>
                    </div>

                    <div class="toolbar-section">
                        <div class="dropdown">
                            <button class="toolbar-btn dropdown-toggle" data-toggle="drawings">
                                <span class="icon">✏️</span> Draw
                            </button>
                            <div class="dropdown-menu" data-menu="drawings">
                                <button class="dropdown-item" data-drawing="hline">Horizontal Line</button>
                                <button class="dropdown-item" data-drawing="trendline">Trend Line</button>
                                <button class="dropdown-item" data-drawing="fibonacci">Fibonacci</button>
                                <button class="dropdown-item" data-drawing="rectangle">Rectangle</button>
                                <button class="dropdown-item" data-drawing="clear">Clear All</button>
                            </div>
                        </div>
                    </div>

                    <div class="toolbar-section">
                        <div class="dropdown">
                            <button class="toolbar-btn dropdown-toggle" data-toggle="presets">
                                <span class="icon">⚙️</span> Preset
                            </button>
                            <div class="dropdown-menu" data-menu="presets">
                                <button class="dropdown-item" data-preset="clean">Clean</button>
                                <button class="dropdown-item" data-preset="technical">Technical</button>
                                <button class="dropdown-item" data-preset="minervini">Minervini</button>
                                <button class="dropdown-item" data-preset="custom">Custom</button>
                            </div>
                        </div>
                    </div>

                    <div class="toolbar-section">
                        <div class="dropdown">
                            <button class="toolbar-btn dropdown-toggle" data-toggle="export">
                                <span class="icon">💾</span> Export
                            </button>
                            <div class="dropdown-menu" data-menu="export">
                                <button class="dropdown-item" data-export="png">Download PNG</button>
                                <button class="dropdown-item" data-export="clipboard">Copy to Clipboard</button>
                                <button class="dropdown-item" data-export="share">Share URL</button>
                                <button class="dropdown-item" data-export="print">Print</button>
                            </div>
                        </div>
                    </div>

                    <div class="toolbar-section ml-auto">
                        <button class="toolbar-btn" data-action="refresh" title="Refresh">
                            <span class="icon">🔄</span>
                        </button>
                        <button class="toolbar-btn" data-action="fullscreen" title="Fullscreen">
                            <span class="icon">⛶</span>
                        </button>
                    </div>
                </div>

                <!-- Chart Container -->
                <div class="chart-main" id="${this.containerId}-chart"></div>

                <!-- Status Bar -->
                <div class="chart-status">
                    <div class="status-item">
                        <span class="status-label">Symbol:</span>
                        <span class="status-value" id="${this.containerId}-symbol">${this.symbol}</span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">O:</span>
                        <span class="status-value" id="${this.containerId}-open">--</span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">H:</span>
                        <span class="status-value" id="${this.containerId}-high">--</span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">L:</span>
                        <span class="status-value" id="${this.containerId}-low">--</span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">C:</span>
                        <span class="status-value" id="${this.containerId}-close">--</span>
                    </div>
                    <div class="status-item">
                        <span class="status-label">Vol:</span>
                        <span class="status-value" id="${this.containerId}-volume">--</span>
                    </div>
                </div>
            </div>
        `;

        this.chartContainer = this.container.querySelector('.chart-main');
    }

    initChart() {
        // Chart options matching cyberpunk theme
        this.chart = LightweightCharts.createChart(this.chartContainer, {
            layout: {
                background: { color: '#0a0e1a' },
                textColor: '#d1d4dc',
            },
            grid: {
                vertLines: { color: '#1a1f2e' },
                horzLines: { color: '#1a1f2e' },
            },
            crosshair: {
                mode: LightweightCharts.CrosshairMode.Normal,
                vertLine: {
                    color: '#00ffff',
                    width: 1,
                    style: LightweightCharts.LineStyle.Dashed,
                },
                horzLine: {
                    color: '#00ffff',
                    width: 1,
                    style: LightweightCharts.LineStyle.Dashed,
                },
            },
            rightPriceScale: {
                borderColor: '#2e3748',
            },
            timeScale: {
                borderColor: '#2e3748',
                timeVisible: true,
                secondsVisible: false,
            },
            handleScroll: {
                mouseWheel: true,
                pressedMouseMove: true,
                horzTouchDrag: true,
                vertTouchDrag: true,
            },
            handleScale: {
                axisPressedMouseMove: true,
                mouseWheel: true,
                pinch: true,
            },
        });

        // Add candlestick series
        this.candleSeries = this.chart.addCandlestickSeries({
            upColor: '#00ff88',
            downColor: '#ff0066',
            borderUpColor: '#00ff88',
            borderDownColor: '#ff0066',
            wickUpColor: '#00ff88',
            wickDownColor: '#ff0066',
        });

        // Add volume series
        this.volumeSeries = this.chart.addHistogramSeries({
            color: '#26a69a',
            priceFormat: {
                type: 'volume',
            },
            priceScaleId: 'volume',
            scaleMargins: {
                top: 0.8,
                bottom: 0,
            },
        });

        // Subscribe to crosshair move for status bar updates
        this.chart.subscribeCrosshairMove((param) => {
            this.updateStatusBar(param);
        });

        // Handle resize
        new ResizeObserver(() => {
            this.chart.applyOptions({
                width: this.chartContainer.clientWidth,
                height: this.chartContainer.clientHeight,
            });
        }).observe(this.chartContainer);
    }

    setupEventListeners() {
        // Timeframe buttons
        this.container.querySelectorAll('[data-action="timeframe"]').forEach(btn => {
            btn.addEventListener('click', () => {
                this.changeTimeframe(btn.dataset.value);
                // Update active state
                this.container.querySelectorAll('[data-action="timeframe"]').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            });
        });

        // Indicator toggles
        this.container.querySelectorAll('[data-indicator]').forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                const indicator = checkbox.dataset.indicator;
                if (checkbox.checked) {
                    this.addIndicator(indicator);
                } else {
                    this.removeIndicator(indicator);
                }
            });
        });

        // Drawing tools
        this.container.querySelectorAll('[data-drawing]').forEach(btn => {
            btn.addEventListener('click', () => {
                const tool = btn.dataset.drawing;
                if (tool === 'clear') {
                    this.clearDrawings();
                } else {
                    this.activateDrawingTool(tool);
                }
            });
        });

        // Presets
        this.container.querySelectorAll('[data-preset]').forEach(btn => {
            btn.addEventListener('click', () => {
                this.applyPreset(btn.dataset.preset);
            });
        });

        // Export actions
        this.container.querySelectorAll('[data-export]').forEach(btn => {
            btn.addEventListener('click', () => {
                this.export(btn.dataset.export);
            });
        });

        // Dropdown toggles
        this.container.querySelectorAll('[data-toggle]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const menuName = btn.dataset.toggle;
                const menu = this.container.querySelector(`[data-menu="${menuName}"]`);

                // Close other dropdowns
                this.container.querySelectorAll('.dropdown-menu').forEach(m => {
                    if (m !== menu) m.classList.remove('show');
                });

                menu.classList.toggle('show');
            });
        });

        // Close dropdowns when clicking outside
        document.addEventListener('click', () => {
            this.container.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.classList.remove('show');
            });
        });

        // Refresh button
        this.container.querySelector('[data-action="refresh"]')?.addEventListener('click', () => {
            this.refresh();
        });

        // Fullscreen button
        this.container.querySelector('[data-action="fullscreen"]')?.addEventListener('click', () => {
            this.toggleFullscreen();
        });
    }

    async loadData(symbol, timeframe = this.timeframe) {
        this.symbol = symbol;
        this.timeframe = timeframe;

        try {
            const response = await fetch(`/api/charts/data?symbol=${symbol}&timeframe=${timeframe}`);
            if (!response.ok) throw new Error('Failed to load chart data');

            const data = await response.json();

            this.candleData = data.candles;
            this.volumeData = data.volume;

            this.candleSeries.setData(this.candleData);
            this.volumeSeries.setData(this.volumeData);

            // Update symbol display
            const symbolEl = this.container.querySelector(`#${this.containerId}-symbol`);
            if (symbolEl) symbolEl.textContent = symbol;

            // Fit content
            this.chart.timeScale().fitContent();

            return data;
        } catch (error) {
            console.error('Error loading chart data:', error);
            throw error;
        }
    }

    updateStatusBar(param) {
        if (!param.time || !param.seriesData) return;

        const data = param.seriesData.get(this.candleSeries);
        if (!data) return;

        const updateElement = (id, value, formatter = (v) => v) => {
            const el = this.container.querySelector(`#${this.containerId}-${id}`);
            if (el) el.textContent = formatter(value);
        };

        const priceFormatter = (val) => val.toFixed(2);
        const volumeFormatter = (val) => {
            if (val >= 1e9) return (val / 1e9).toFixed(2) + 'B';
            if (val >= 1e6) return (val / 1e6).toFixed(2) + 'M';
            if (val >= 1e3) return (val / 1e3).toFixed(2) + 'K';
            return val.toFixed(0);
        };

        updateElement('open', data.open, priceFormatter);
        updateElement('high', data.high, priceFormatter);
        updateElement('low', data.low, priceFormatter);
        updateElement('close', data.close, priceFormatter);

        const volumeData = param.seriesData.get(this.volumeSeries);
        if (volumeData) {
            updateElement('volume', volumeData.value, volumeFormatter);
        }
    }

    changeTimeframe(timeframe) {
        this.timeframe = timeframe;
        if (this.symbol) {
            this.loadData(this.symbol, timeframe);
        }
    }

    addIndicator(indicator) {
        if (this.activeIndicators.has(indicator)) return;
        this.activeIndicators.add(indicator);

        // Calculate and add indicator
        const series = ChartIndicators.add(this.chart, indicator, this.candleData, this.volumeData);
        if (series) {
            this.indicatorSeries[indicator] = series;
        }
    }

    removeIndicator(indicator) {
        if (!this.activeIndicators.has(indicator)) return;
        this.activeIndicators.delete(indicator);

        // Remove indicator series
        const series = this.indicatorSeries[indicator];
        if (series) {
            if (Array.isArray(series)) {
                series.forEach(s => this.chart.removeSeries(s));
            } else {
                this.chart.removeSeries(series);
            }
            delete this.indicatorSeries[indicator];
        }
    }

    activateDrawingTool(tool) {
        this.activeDrawingTool = tool;
        this.drawingMode = true;

        // Visual feedback
        this.chartContainer.style.cursor = 'crosshair';

        // Add drawing interaction
        ChartDrawings.activate(this.chart, tool, (drawing) => {
            this.drawings.push(drawing);
            this.saveDrawings();
        });
    }

    clearDrawings() {
        ChartDrawings.clearAll(this.chart, this.drawings);
        this.drawings = [];
        this.saveDrawings();
    }

    saveDrawings() {
        // Save drawings to localStorage per ticker
        const key = `chart_drawings_${this.symbol}`;
        localStorage.setItem(key, JSON.stringify(this.drawings));
    }

    loadDrawings() {
        // Load drawings from localStorage
        const key = `chart_drawings_${this.symbol}`;
        const saved = localStorage.getItem(key);
        if (saved) {
            try {
                this.drawings = JSON.parse(saved);
                this.drawings.forEach(drawing => {
                    ChartDrawings.restore(this.chart, drawing);
                });
            } catch (error) {
                console.error('Error loading drawings:', error);
            }
        }
    }

    addPatternAnnotation(pattern) {
        const annotation = ChartAnnotations.create(this.chart, pattern);
        this.annotations.push(annotation);
    }

    applyPreset(presetName) {
        this.currentPreset = presetName;

        // Clear all indicators
        this.activeIndicators.forEach(indicator => {
            this.removeIndicator(indicator);
        });

        // Uncheck all indicator checkboxes
        this.container.querySelectorAll('[data-indicator]').forEach(checkbox => {
            checkbox.checked = false;
        });

        const presets = {
            clean: [],
            technical: ['ema21', 'sma50', 'sma200', 'bb', 'vwap'],
            minervini: ['ema21', 'sma50'],
            custom: [] // User will manually select
        };

        const indicators = presets[presetName] || [];
        indicators.forEach(indicator => {
            const checkbox = this.container.querySelector(`[data-indicator="${indicator}"]`);
            if (checkbox) {
                checkbox.checked = true;
                this.addIndicator(indicator);
            }
        });
    }

    async export(type) {
        switch (type) {
            case 'png':
                await this.exportPNG();
                break;
            case 'clipboard':
                await this.exportClipboard();
                break;
            case 'share':
                await this.shareURL();
                break;
            case 'print':
                this.print();
                break;
        }
    }

    async exportPNG() {
        try {
            const canvas = this.chartContainer.querySelector('canvas');
            if (!canvas) throw new Error('Chart canvas not found');

            const dataUrl = canvas.toDataURL('image/png');
            const link = document.createElement('a');
            link.download = `${this.symbol}_${this.timeframe}_chart.png`;
            link.href = dataUrl;
            link.click();
        } catch (error) {
            console.error('Error exporting PNG:', error);
            alert('Failed to export PNG');
        }
    }

    async exportClipboard() {
        try {
            const canvas = this.chartContainer.querySelector('canvas');
            if (!canvas) throw new Error('Chart canvas not found');

            canvas.toBlob(async (blob) => {
                await navigator.clipboard.write([
                    new ClipboardItem({ 'image/png': blob })
                ]);
                alert('Chart copied to clipboard!');
            });
        } catch (error) {
            console.error('Error copying to clipboard:', error);
            alert('Failed to copy to clipboard');
        }
    }

    async shareURL() {
        const state = {
            symbol: this.symbol,
            timeframe: this.timeframe,
            indicators: Array.from(this.activeIndicators),
            preset: this.currentPreset
        };

        const encoded = btoa(JSON.stringify(state));
        const url = `${window.location.origin}${window.location.pathname}?chart=${encoded}`;

        try {
            await navigator.clipboard.writeText(url);
            alert('Share URL copied to clipboard!');
        } catch (error) {
            // Fallback: show in prompt
            prompt('Share this URL:', url);
        }
    }

    print() {
        window.print();
    }

    refresh() {
        if (this.symbol) {
            this.loadData(this.symbol, this.timeframe);
        }
    }

    toggleFullscreen() {
        if (!document.fullscreenElement) {
            this.container.requestFullscreen?.() ||
            this.container.webkitRequestFullscreen?.() ||
            this.container.msRequestFullscreen?.();
        } else {
            document.exitFullscreen?.() ||
            document.webkitExitFullscreen?.() ||
            document.msExitFullscreen?.();
        }
    }

    destroy() {
        if (this.chart) {
            this.chart.remove();
            this.chart = null;
        }
    }
}

// Export for use in other modules
window.InteractiveChart = InteractiveChart;
