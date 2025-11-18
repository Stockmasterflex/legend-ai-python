/**
 * Chart Drawing Tools Module
 * Enables interactive drawing on Lightweight Charts
 */

const ChartDrawings = {
    activeDrawings: new Map(),
    currentTool: null,
    drawingCallback: null,

    /**
     * Activate a drawing tool
     */
    activate(chart, tool, callback) {
        this.currentTool = tool;
        this.drawingCallback = callback;

        const handlers = {
            hline: () => this.activateHorizontalLine(chart),
            trendline: () => this.activateTrendLine(chart),
            fibonacci: () => this.activateFibonacci(chart),
            rectangle: () => this.activateRectangle(chart)
        };

        const handler = handlers[tool];
        if (handler) {
            handler();
        } else {
            console.error(`Unknown drawing tool: ${tool}`);
        }
    },

    /**
     * Horizontal Line Tool
     */
    activateHorizontalLine(chart) {
        let clickHandler;

        clickHandler = (param) => {
            if (!param.point) return;

            const price = param.seriesData.values().next().value?.close ||
                         chart.timeScale().coordinateToPrice(param.point.y);

            if (!price) return;

            const drawing = this.createHorizontalLine(chart, price);

            if (this.drawingCallback) {
                this.drawingCallback({
                    type: 'hline',
                    price: price,
                    id: drawing.id
                });
            }

            // Remove click handler after drawing
            chart.unsubscribeClick(clickHandler);
        };

        chart.subscribeClick(clickHandler);
    },

    /**
     * Trend Line Tool
     */
    activateTrendLine(chart) {
        let points = [];
        let clickHandler;

        clickHandler = (param) => {
            if (!param.point || !param.time) return;

            const price = param.seriesData.values().next().value?.close ||
                         chart.timeScale().coordinateToPrice(param.point.y);

            if (!price) return;

            points.push({ time: param.time, price: price });

            if (points.length === 2) {
                const drawing = this.createTrendLine(chart, points[0], points[1]);

                if (this.drawingCallback) {
                    this.drawingCallback({
                        type: 'trendline',
                        points: points,
                        id: drawing.id
                    });
                }

                chart.unsubscribeClick(clickHandler);
                points = [];
            }
        };

        chart.subscribeClick(clickHandler);
    },

    /**
     * Fibonacci Retracement Tool
     */
    activateFibonacci(chart) {
        let points = [];
        let clickHandler;

        clickHandler = (param) => {
            if (!param.point || !param.time) return;

            const price = param.seriesData.values().next().value?.close ||
                         chart.timeScale().coordinateToPrice(param.point.y);

            if (!price) return;

            points.push({ time: param.time, price: price });

            if (points.length === 2) {
                const drawing = this.createFibonacci(chart, points[0], points[1]);

                if (this.drawingCallback) {
                    this.drawingCallback({
                        type: 'fibonacci',
                        points: points,
                        id: drawing.id
                    });
                }

                chart.unsubscribeClick(clickHandler);
                points = [];
            }
        };

        chart.subscribeClick(clickHandler);
    },

    /**
     * Rectangle Tool
     */
    activateRectangle(chart) {
        let points = [];
        let clickHandler;

        clickHandler = (param) => {
            if (!param.point || !param.time) return;

            const price = param.seriesData.values().next().value?.close ||
                         chart.timeScale().coordinateToPrice(param.point.y);

            if (!price) return;

            points.push({ time: param.time, price: price });

            if (points.length === 2) {
                const drawing = this.createRectangle(chart, points[0], points[1]);

                if (this.drawingCallback) {
                    this.drawingCallback({
                        type: 'rectangle',
                        points: points,
                        id: drawing.id
                    });
                }

                chart.unsubscribeClick(clickHandler);
                points = [];
            }
        };

        chart.subscribeClick(clickHandler);
    },

    /**
     * Create a horizontal line
     */
    createHorizontalLine(chart, price, options = {}) {
        const id = options.id || `hline_${Date.now()}`;
        const color = options.color || '#00ffff';
        const lineWidth = options.lineWidth || 2;

        const lineSeries = chart.addLineSeries({
            color: color,
            lineWidth: lineWidth,
            priceLineVisible: false,
            lastValueVisible: false,
            crosshairMarkerVisible: false,
            title: options.title || `H-Line ${price.toFixed(2)}`
        });

        // Create horizontal line by setting same price for all visible time points
        // This is a workaround - ideally we'd use price lines but those don't persist
        const timeScale = chart.timeScale();
        const visibleRange = timeScale.getVisibleRange();

        // For now, just create markers
        chart.createPriceLine = chart.createPriceLine || function(opts) {
            // Lightweight Charts doesn't have createPriceLine in all versions
            // We'll use markers as fallback
            return null;
        };

        const priceLine = {
            price: price,
            color: color,
            lineWidth: lineWidth,
            lineStyle: LightweightCharts.LineStyle.Solid,
            axisLabelVisible: true,
            title: options.title || 'H-Line'
        };

        // Store the drawing
        this.activeDrawings.set(id, {
            type: 'hline',
            series: lineSeries,
            price: price,
            options: priceLine
        });

        return { id, series: lineSeries };
    },

    /**
     * Create a trend line
     */
    createTrendLine(chart, point1, point2, options = {}) {
        const id = options.id || `trendline_${Date.now()}`;
        const color = options.color || '#ffaa00';

        const lineSeries = chart.addLineSeries({
            color: color,
            lineWidth: 2,
            priceLineVisible: false,
            lastValueVisible: false,
            title: options.title || 'Trend Line'
        });

        // Calculate line points
        const lineData = this.interpolateLine(point1, point2);
        lineSeries.setData(lineData);

        this.activeDrawings.set(id, {
            type: 'trendline',
            series: lineSeries,
            points: [point1, point2]
        });

        return { id, series: lineSeries };
    },

    /**
     * Create Fibonacci retracement levels
     */
    createFibonacci(chart, point1, point2, options = {}) {
        const id = options.id || `fib_${Date.now()}`;
        const levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1];
        const colors = ['#ff0066', '#ff6600', '#ffaa00', '#ffff00', '#00ff88', '#00ffff', '#9966ff'];

        const series = [];
        const priceDiff = point2.price - point1.price;

        levels.forEach((level, i) => {
            const price = point1.price + (priceDiff * level);
            const levelSeries = chart.addLineSeries({
                color: colors[i],
                lineWidth: 1,
                lineStyle: LightweightCharts.LineStyle.Dashed,
                priceLineVisible: false,
                lastValueVisible: false,
                title: `Fib ${(level * 100).toFixed(1)}%`
            });

            series.push(levelSeries);
        });

        this.activeDrawings.set(id, {
            type: 'fibonacci',
            series: series,
            points: [point1, point2],
            levels: levels
        });

        return { id, series: series };
    },

    /**
     * Create a rectangle zone
     */
    createRectangle(chart, point1, point2, options = {}) {
        const id = options.id || `rect_${Date.now()}`;
        const color = options.color || 'rgba(255, 0, 102, 0.2)';

        // Create filled area using histogram series
        const areaSeries = chart.addHistogramSeries({
            color: color,
            priceFormat: {
                type: 'price',
            },
            priceLineVisible: false,
            lastValueVisible: false,
            title: options.title || 'Zone'
        });

        // Create rectangle data
        const rectData = this.createRectangleData(point1, point2);
        areaSeries.setData(rectData);

        this.activeDrawings.set(id, {
            type: 'rectangle',
            series: areaSeries,
            points: [point1, point2]
        });

        return { id, series: areaSeries };
    },

    /**
     * Interpolate line between two points
     */
    interpolateLine(point1, point2) {
        // For simplicity, just return the two points
        // In a more sophisticated version, we'd interpolate based on visible time range
        return [
            { time: point1.time, value: point1.price },
            { time: point2.time, value: point2.price }
        ];
    },

    /**
     * Create rectangle data
     */
    createRectangleData(point1, point2) {
        const data = [];
        const startTime = Math.min(point1.time, point2.time);
        const endTime = Math.max(point1.time, point2.time);
        const price = Math.max(point1.price, point2.price);
        const height = Math.abs(point2.price - point1.price);

        // Create bars for the rectangle
        // This is simplified - in production, we'd need actual time points
        data.push(
            { time: startTime, value: height, color: 'rgba(255, 0, 102, 0.2)' },
            { time: endTime, value: height, color: 'rgba(255, 0, 102, 0.2)' }
        );

        return data;
    },

    /**
     * Restore a saved drawing
     */
    restore(chart, drawingData) {
        const restoreMethods = {
            hline: (data) => this.createHorizontalLine(chart, data.price, {
                id: data.id,
                ...data.options
            }),
            trendline: (data) => this.createTrendLine(chart, data.points[0], data.points[1], {
                id: data.id
            }),
            fibonacci: (data) => this.createFibonacci(chart, data.points[0], data.points[1], {
                id: data.id
            }),
            rectangle: (data) => this.createRectangle(chart, data.points[0], data.points[1], {
                id: data.id
            })
        };

        const method = restoreMethods[drawingData.type];
        if (method) {
            method(drawingData);
        }
    },

    /**
     * Clear all drawings
     */
    clearAll(chart, drawings) {
        this.activeDrawings.forEach((drawing) => {
            if (Array.isArray(drawing.series)) {
                drawing.series.forEach(s => chart.removeSeries(s));
            } else if (drawing.series) {
                chart.removeSeries(drawing.series);
            }
        });
        this.activeDrawings.clear();
    },

    /**
     * Remove a specific drawing
     */
    remove(chart, id) {
        const drawing = this.activeDrawings.get(id);
        if (!drawing) return;

        if (Array.isArray(drawing.series)) {
            drawing.series.forEach(s => chart.removeSeries(s));
        } else if (drawing.series) {
            chart.removeSeries(drawing.series);
        }

        this.activeDrawings.delete(id);
    },

    /**
     * Get all active drawings
     */
    getAll() {
        return Array.from(this.activeDrawings.entries()).map(([id, drawing]) => ({
            id,
            type: drawing.type,
            points: drawing.points,
            price: drawing.price,
            options: drawing.options,
            levels: drawing.levels
        }));
    }
};

// Export for use
window.ChartDrawings = ChartDrawings;
