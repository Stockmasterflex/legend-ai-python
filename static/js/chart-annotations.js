/**
 * Chart Pattern Annotations Module
 * Automatically highlights detected patterns with markers and labels
 */

const ChartAnnotations = {
    activeAnnotations: new Map(),

    /**
     * Create a pattern annotation
     * @param {Chart} chart - Lightweight Charts instance
     * @param {Object} pattern - Pattern data from backend
     */
    create(chart, pattern) {
        const id = pattern.id || `pattern_${Date.now()}`;

        const annotation = {
            id,
            pattern: pattern.pattern_type || pattern.name,
            confidence: pattern.confidence || 0,
            entry: pattern.entry_price,
            stop: pattern.stop_loss,
            target: pattern.target_price,
            timestamp: pattern.timestamp || pattern.time,
            markers: []
        };

        // Add pattern highlight zone
        if (pattern.zone_start && pattern.zone_end) {
            this.addPatternZone(chart, annotation, pattern);
        }

        // Add entry/stop/target markers
        this.addTradingMarkers(chart, annotation);

        // Add pattern label
        this.addPatternLabel(chart, annotation);

        // Add risk zone shading
        this.addRiskZone(chart, annotation);

        this.activeAnnotations.set(id, annotation);

        return annotation;
    },

    /**
     * Add pattern highlight zone
     */
    addPatternZone(chart, annotation, pattern) {
        // Create a shaded area for the pattern
        const zoneSeries = chart.addHistogramSeries({
            color: this.getPatternColor(pattern.pattern_type, 0.1),
            priceFormat: { type: 'price' },
            priceLineVisible: false,
            lastValueVisible: false,
        });

        annotation.zoneSeries = zoneSeries;
    },

    /**
     * Add trading markers (entry, stop, target)
     */
    addTradingMarkers(chart, annotation) {
        const markers = [];

        // Entry marker
        if (annotation.entry && annotation.timestamp) {
            markers.push({
                time: annotation.timestamp,
                position: 'belowBar',
                color: '#00ff88',
                shape: 'arrowUp',
                text: `Entry: $${annotation.entry.toFixed(2)}`
            });

            // Add entry price line
            const entrySeries = chart.addLineSeries({
                color: '#00ff88',
                lineWidth: 2,
                lineStyle: LightweightCharts.LineStyle.Dashed,
                priceLineVisible: false,
                lastValueVisible: false,
                title: 'Entry'
            });

            annotation.entrySeries = entrySeries;
        }

        // Stop loss marker
        if (annotation.stop && annotation.timestamp) {
            markers.push({
                time: annotation.timestamp,
                position: 'belowBar',
                color: '#ff0066',
                shape: 'circle',
                text: `Stop: $${annotation.stop.toFixed(2)}`
            });

            // Add stop price line
            const stopSeries = chart.addLineSeries({
                color: '#ff0066',
                lineWidth: 2,
                lineStyle: LightweightCharts.LineStyle.Dashed,
                priceLineVisible: false,
                lastValueVisible: false,
                title: 'Stop Loss'
            });

            annotation.stopSeries = stopSeries;
        }

        // Target marker
        if (annotation.target && annotation.timestamp) {
            markers.push({
                time: annotation.timestamp,
                position: 'aboveBar',
                color: '#ffaa00',
                shape: 'arrowDown',
                text: `Target: $${annotation.target.toFixed(2)}`
            });

            // Add target price line
            const targetSeries = chart.addLineSeries({
                color: '#ffaa00',
                lineWidth: 2,
                lineStyle: LightweightCharts.LineStyle.Dashed,
                priceLineVisible: false,
                lastValueVisible: false,
                title: 'Target'
            });

            annotation.targetSeries = targetSeries;
        }

        annotation.markers = markers;
    },

    /**
     * Add pattern label with confidence score
     */
    addPatternLabel(chart, annotation) {
        if (!annotation.timestamp) return;

        const confidencePercent = (annotation.confidence * 100).toFixed(0);
        const labelText = `${annotation.pattern} (${confidencePercent}%)`;

        // Create label as a marker
        const label = {
            time: annotation.timestamp,
            position: 'aboveBar',
            color: this.getPatternColor(annotation.pattern),
            shape: 'square',
            text: labelText,
            size: 2
        };

        annotation.markers.push(label);
    },

    /**
     * Add risk zone shading
     */
    addRiskZone(chart, annotation) {
        if (!annotation.entry || !annotation.stop || !annotation.timestamp) return;

        // Create a histogram series for the risk zone (between entry and stop)
        const riskSeries = chart.addHistogramSeries({
            color: 'rgba(255, 0, 102, 0.15)',
            priceFormat: { type: 'price' },
            priceLineVisible: false,
            lastValueVisible: false,
        });

        annotation.riskSeries = riskSeries;
    },

    /**
     * Get color for pattern type
     */
    getPatternColor(patternType, alpha = 1) {
        const colors = {
            'bull_flag': '#00ff88',
            'cup_handle': '#00ffff',
            'double_bottom': '#9966ff',
            'ascending_triangle': '#ffaa00',
            'breakout': '#ff00ff',
            'consolidation': '#00aaff',
            'vcp': '#ff6600',
            'flat_base': '#66ff00',
            'default': '#00ffff'
        };

        const color = colors[patternType?.toLowerCase()] || colors.default;

        // Convert hex to rgba if alpha is provided
        if (alpha < 1) {
            const r = parseInt(color.slice(1, 3), 16);
            const g = parseInt(color.slice(3, 5), 16);
            const b = parseInt(color.slice(5, 7), 16);
            return `rgba(${r}, ${g}, ${b}, ${alpha})`;
        }

        return color;
    },

    /**
     * Add multiple pattern markers to candle series
     */
    addMarkersToSeries(candleSeries, patterns) {
        if (!patterns || patterns.length === 0) return;

        const markers = [];

        patterns.forEach(pattern => {
            const annotation = this.activeAnnotations.get(pattern.id);
            if (annotation && annotation.markers) {
                markers.push(...annotation.markers);
            }
        });

        if (markers.length > 0) {
            candleSeries.setMarkers(markers);
        }
    },

    /**
     * Create divergence annotation
     */
    createDivergence(chart, divergenceData) {
        const id = `divergence_${Date.now()}`;

        const annotation = {
            id,
            type: 'divergence',
            divergenceType: divergenceData.type, // bullish, bearish
            points: divergenceData.points,
            markers: []
        };

        // Add divergence line
        const lineSeries = chart.addLineSeries({
            color: divergenceData.type === 'bullish' ? '#00ff88' : '#ff0066',
            lineWidth: 2,
            lineStyle: LightweightCharts.LineStyle.Dotted,
            priceLineVisible: false,
            lastValueVisible: false,
            title: `${divergenceData.type} Divergence`
        });

        lineSeries.setData(divergenceData.points.map(p => ({
            time: p.time,
            value: p.price
        })));

        annotation.series = lineSeries;

        // Add markers at divergence points
        divergenceData.points.forEach((point, i) => {
            annotation.markers.push({
                time: point.time,
                position: i === 0 ? 'belowBar' : 'aboveBar',
                color: divergenceData.type === 'bullish' ? '#00ff88' : '#ff0066',
                shape: 'circle',
                text: `D${i + 1}`
            });
        });

        this.activeAnnotations.set(id, annotation);

        return annotation;
    },

    /**
     * Create support/resistance level annotation
     */
    createLevel(chart, levelData) {
        const id = `level_${Date.now()}`;

        const annotation = {
            id,
            type: 'level',
            levelType: levelData.type, // support, resistance
            price: levelData.price,
            strength: levelData.strength || 1
        };

        // Add level line
        const lineSeries = chart.addLineSeries({
            color: levelData.type === 'support' ? '#00ff88' : '#ff0066',
            lineWidth: 1 + annotation.strength,
            lineStyle: LightweightCharts.LineStyle.Dashed,
            priceLineVisible: false,
            lastValueVisible: false,
            title: `${levelData.type} @ ${levelData.price.toFixed(2)}`
        });

        annotation.series = lineSeries;

        this.activeAnnotations.set(id, annotation);

        return annotation;
    },

    /**
     * Create volume spike annotation
     */
    createVolumeSpike(chart, spikeData) {
        const id = `volume_spike_${Date.now()}`;

        const annotation = {
            id,
            type: 'volume_spike',
            time: spikeData.time,
            volume: spikeData.volume,
            averageVolume: spikeData.averageVolume,
            ratio: spikeData.ratio
        };

        // Add marker
        annotation.marker = {
            time: spikeData.time,
            position: 'belowBar',
            color: '#ffaa00',
            shape: 'circle',
            text: `Vol: ${spikeData.ratio.toFixed(1)}x`
        };

        this.activeAnnotations.set(id, annotation);

        return annotation;
    },

    /**
     * Remove annotation
     */
    remove(chart, id) {
        const annotation = this.activeAnnotations.get(id);
        if (!annotation) return;

        // Remove series
        ['zoneSeries', 'entrySeries', 'stopSeries', 'targetSeries', 'riskSeries', 'series'].forEach(key => {
            if (annotation[key]) {
                chart.removeSeries(annotation[key]);
            }
        });

        this.activeAnnotations.delete(id);
    },

    /**
     * Clear all annotations
     */
    clearAll(chart) {
        this.activeAnnotations.forEach((annotation, id) => {
            this.remove(chart, id);
        });
        this.activeAnnotations.clear();
    },

    /**
     * Get all annotations
     */
    getAll() {
        return Array.from(this.activeAnnotations.values());
    },

    /**
     * Export annotations data
     */
    export() {
        return this.getAll().map(annotation => ({
            id: annotation.id,
            pattern: annotation.pattern,
            confidence: annotation.confidence,
            entry: annotation.entry,
            stop: annotation.stop,
            target: annotation.target,
            timestamp: annotation.timestamp
        }));
    },

    /**
     * Import annotations data
     */
    import(chart, annotationsData) {
        annotationsData.forEach(data => {
            this.create(chart, data);
        });
    }
};

// Export for use
window.ChartAnnotations = ChartAnnotations;
