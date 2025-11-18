/**
 * Chart Integration Helper
 * Provides simple interface to replace static Chart-IMG with interactive charts
 */

const ChartIntegration = {
    charts: new Map(),
    useInteractive: true, // Toggle to enable/disable interactive charts

    /**
     * Initialize or update a chart in a container
     *
     * @param {string} containerId - DOM element ID
     * @param {string} symbol - Stock ticker symbol
     * @param {string} timeframe - Timeframe (1D, 1W, 1M)
     * @param {Object} options - Additional options
     * @returns {Promise<InteractiveChart|null>}
     */
    async initChart(containerId, symbol, timeframe = '1D', options = {}) {
        try {
            // Check if we should use interactive charts
            if (!this.useInteractive) {
                console.log('Interactive charts disabled, using fallback');
                return null;
            }

            // Clean up existing chart if present
            if (this.charts.has(containerId)) {
                const existingChart = this.charts.get(containerId);
                existingChart.destroy();
                this.charts.delete(containerId);
            }

            // Create new interactive chart
            const chart = new InteractiveChart(containerId, {
                symbol,
                timeframe,
                ...options
            });

            // Load data
            await chart.loadData(symbol, timeframe);

            // Add pattern annotations if provided
            if (options.patterns && options.patterns.length > 0) {
                options.patterns.forEach(pattern => {
                    chart.addPatternAnnotation(pattern);
                });
            }

            // Apply preset if specified
            if (options.preset) {
                chart.applyPreset(options.preset);
            }

            // Store chart instance
            this.charts.set(containerId, chart);

            return chart;
        } catch (error) {
            console.error('Error initializing interactive chart:', error);
            return null;
        }
    },

    /**
     * Load chart from URL state (for sharing)
     */
    loadFromURL() {
        const params = new URLSearchParams(window.location.search);
        const chartState = params.get('chart');

        if (!chartState) return null;

        try {
            const state = JSON.parse(atob(chartState));
            return state;
        } catch (error) {
            console.error('Error parsing chart state:', error);
            return null;
        }
    },

    /**
     * Replace static chart image with interactive chart
     *
     * @param {string} containerId - Container ID
     * @param {string} staticImageUrl - URL of static chart image
     * @param {string} symbol - Stock symbol
     * @param {string} timeframe - Timeframe
     */
    async replaceStaticChart(containerId, staticImageUrl, symbol, timeframe = '1D') {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container ${containerId} not found`);
            return null;
        }

        // Check if interactive charts are enabled
        if (!this.useInteractive) {
            // Show static image
            container.innerHTML = `<img src="${staticImageUrl}" alt="${symbol} chart" class="chart-image" />`;
            return null;
        }

        // Clear container and show loading state
        container.innerHTML = `
            <div class="chart-loading">
                <div>Loading interactive chart...</div>
            </div>
        `;

        try {
            // Initialize interactive chart
            const chart = await this.initChart(containerId, symbol, timeframe);

            if (!chart) {
                // Fallback to static image
                container.innerHTML = `<img src="${staticImageUrl}" alt="${symbol} chart" class="chart-image" />`;
            }

            return chart;
        } catch (error) {
            console.error('Error replacing static chart:', error);
            // Fallback to static image
            container.innerHTML = `<img src="${staticImageUrl}" alt="${symbol} chart" class="chart-image" />`;
            return null;
        }
    },

    /**
     * Update existing chart with new data
     */
    async updateChart(containerId, symbol, timeframe = '1D') {
        const chart = this.charts.get(containerId);

        if (!chart) {
            // Chart doesn't exist, create it
            return await this.initChart(containerId, symbol, timeframe);
        }

        // Update existing chart
        try {
            await chart.loadData(symbol, timeframe);
            return chart;
        } catch (error) {
            console.error('Error updating chart:', error);
            return null;
        }
    },

    /**
     * Get chart instance
     */
    getChart(containerId) {
        return this.charts.get(containerId);
    },

    /**
     * Destroy chart
     */
    destroyChart(containerId) {
        const chart = this.charts.get(containerId);
        if (chart) {
            chart.destroy();
            this.charts.delete(containerId);
        }
    },

    /**
     * Destroy all charts
     */
    destroyAll() {
        this.charts.forEach((chart, containerId) => {
            chart.destroy();
        });
        this.charts.clear();
    },

    /**
     * Toggle between interactive and static charts
     */
    toggleInteractive(enabled) {
        this.useInteractive = enabled;

        // Save preference to localStorage
        localStorage.setItem('legend_ai_interactive_charts', enabled ? 'true' : 'false');

        console.log(`Interactive charts ${enabled ? 'enabled' : 'disabled'}`);
    },

    /**
     * Initialize from localStorage preference
     */
    init() {
        const preference = localStorage.getItem('legend_ai_interactive_charts');

        // Default to true if not set
        if (preference === null) {
            this.useInteractive = true;
        } else {
            this.useInteractive = preference === 'true';
        }

        console.log('Chart Integration initialized:', {
            interactive: this.useInteractive
        });

        // Check for chart state in URL
        const urlState = this.loadFromURL();
        if (urlState) {
            console.log('Chart state loaded from URL:', urlState);
            return urlState;
        }

        return null;
    },

    /**
     * Show chart in a modal/fullscreen view
     */
    showFullscreen(containerId) {
        const chart = this.charts.get(containerId);
        if (chart) {
            chart.toggleFullscreen();
        }
    },

    /**
     * Export chart as PNG
     */
    async exportPNG(containerId) {
        const chart = this.charts.get(containerId);
        if (chart) {
            await chart.exportPNG();
        }
    },

    /**
     * Share chart URL
     */
    async shareChart(containerId) {
        const chart = this.charts.get(containerId);
        if (chart) {
            await chart.shareURL();
        }
    },

    /**
     * Apply preset to chart
     */
    applyPreset(containerId, presetName) {
        const chart = this.charts.get(containerId);
        if (chart) {
            chart.applyPreset(presetName);
        }
    },

    /**
     * Add indicator to chart
     */
    addIndicator(containerId, indicator) {
        const chart = this.charts.get(containerId);
        if (chart) {
            chart.addIndicator(indicator);
        }
    },

    /**
     * Remove indicator from chart
     */
    removeIndicator(containerId, indicator) {
        const chart = this.charts.get(containerId);
        if (chart) {
            chart.removeIndicator(indicator);
        }
    },

    /**
     * Activate drawing tool
     */
    activateDrawing(containerId, tool) {
        const chart = this.charts.get(containerId);
        if (chart) {
            chart.activateDrawingTool(tool);
        }
    },

    /**
     * Clear all drawings
     */
    clearDrawings(containerId) {
        const chart = this.charts.get(containerId);
        if (chart) {
            chart.clearDrawings();
        }
    }
};

// Auto-initialize on page load
if (typeof window !== 'undefined') {
    window.ChartIntegration = ChartIntegration;

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            ChartIntegration.init();
        });
    } else {
        ChartIntegration.init();
    }
}
