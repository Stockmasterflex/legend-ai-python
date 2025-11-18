/**
 * Export Manager for Charts
 * Handles image, SVG, PDF, and video exports
 */

class ChartExportManager {
    constructor(chart) {
        this.chart = chart;
        this.recorder = null;
        this.recordedChunks = [];
    }

    /**
     * Export chart as high-resolution PNG/JPG
     */
    exportImage(format = 'png', scale = 2, quality = 1.0) {
        return new Promise((resolve, reject) => {
            try {
                // Create temporary canvas with higher resolution
                const tempCanvas = document.createElement('canvas');
                const width = this.chart.options.width;
                const height = this.chart.options.height;

                tempCanvas.width = width * scale;
                tempCanvas.height = height * scale;

                const ctx = tempCanvas.getContext('2d');
                ctx.scale(scale, scale);

                // Fill background
                ctx.fillStyle = this.chart.options.theme === 'dark' ? '#1a1a2e' : '#ffffff';
                ctx.fillRect(0, 0, width, height);

                // Draw chart
                this.renderChartToContext(ctx, width, height);

                // Convert to data URL
                const mimeType = format === 'jpg' ? 'image/jpeg' : 'image/png';
                const dataUrl = tempCanvas.toDataURL(mimeType, quality);

                resolve(dataUrl);
            } catch (error) {
                reject(error);
            }
        });
    }

    /**
     * Export chart as SVG
     */
    exportSVG() {
        return new Promise((resolve, reject) => {
            try {
                const width = this.chart.options.width;
                const height = this.chart.options.height;

                // Create SVG element
                const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                svg.setAttribute('width', width);
                svg.setAttribute('height', height);
                svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');

                // Add background
                const bg = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                bg.setAttribute('width', width);
                bg.setAttribute('height', height);
                bg.setAttribute('fill', this.chart.options.theme === 'dark' ? '#1a1a2e' : '#ffffff');
                svg.appendChild(bg);

                // Render chart elements to SVG
                this.renderChartToSVG(svg, width, height);

                // Serialize SVG
                const serializer = new XMLSerializer();
                const svgString = serializer.serializeToString(svg);

                // Create data URL
                const dataUrl = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgString);

                resolve(dataUrl);
            } catch (error) {
                reject(error);
            }
        });
    }

    /**
     * Export chart as PDF
     */
    async exportPDF(filename = 'chart.pdf', options = {}) {
        // Note: This requires jsPDF library to be loaded
        if (typeof window.jspdf === 'undefined') {
            throw new Error('jsPDF library not loaded. Please include jsPDF script.');
        }

        const { jsPDF } = window.jspdf;

        const orientation = options.orientation || 'landscape';
        const format = options.format || 'a4';

        const pdf = new jsPDF({
            orientation,
            unit: 'px',
            format
        });

        // Get page dimensions
        const pageWidth = pdf.internal.pageSize.getWidth();
        const pageHeight = pdf.internal.pageSize.getHeight();

        // Export chart as high-res image
        const imageData = await this.exportImage('png', 2);

        // Calculate dimensions to fit page
        const chartWidth = this.chart.options.width;
        const chartHeight = this.chart.options.height;
        const ratio = Math.min(pageWidth / chartWidth, pageHeight / chartHeight) * 0.9;

        const finalWidth = chartWidth * ratio;
        const finalHeight = chartHeight * ratio;
        const x = (pageWidth - finalWidth) / 2;
        const y = (pageHeight - finalHeight) / 2;

        // Add image to PDF
        pdf.addImage(imageData, 'PNG', x, y, finalWidth, finalHeight);

        // Add metadata
        if (options.title) {
            pdf.setFontSize(16);
            pdf.text(options.title, pageWidth / 2, 20, { align: 'center' });
        }

        if (options.metadata) {
            pdf.setFontSize(10);
            let metaY = pageHeight - 20;
            Object.entries(options.metadata).forEach(([key, value]) => {
                pdf.text(`${key}: ${value}`, 20, metaY);
                metaY += 12;
            });
        }

        // Download PDF
        pdf.save(filename);

        return pdf;
    }

    /**
     * Start recording chart interactions as video
     */
    startRecording(options = {}) {
        if (!this.chart.canvas) {
            throw new Error('Chart must use canvas rendering for video recording');
        }

        const canvas = this.chart.canvas;
        const stream = canvas.captureStream(options.fps || 30);

        this.recorder = new MediaRecorder(stream, {
            mimeType: options.mimeType || 'video/webm',
            videoBitsPerSecond: options.bitrate || 2500000
        });

        this.recordedChunks = [];

        this.recorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                this.recordedChunks.push(event.data);
            }
        };

        this.recorder.onstop = () => {
            this.saveRecording(options.filename || 'chart-recording.webm');
        };

        this.recorder.start();

        return {
            stop: () => this.stopRecording(),
            pause: () => this.recorder.pause(),
            resume: () => this.recorder.resume()
        };
    }

    /**
     * Stop video recording
     */
    stopRecording() {
        if (this.recorder && this.recorder.state !== 'inactive') {
            this.recorder.stop();
        }
    }

    /**
     * Save recorded video
     */
    saveRecording(filename) {
        const blob = new Blob(this.recordedChunks, { type: 'video/webm' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();

        URL.revokeObjectURL(url);
        this.recordedChunks = [];
    }

    /**
     * Download file from data URL
     */
    downloadDataUrl(dataUrl, filename) {
        const a = document.createElement('a');
        a.href = dataUrl;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }

    /**
     * Export as PNG and download
     */
    async downloadPNG(filename = 'chart.png', scale = 2) {
        const dataUrl = await this.exportImage('png', scale);
        this.downloadDataUrl(dataUrl, filename);
    }

    /**
     * Export as JPG and download
     */
    async downloadJPG(filename = 'chart.jpg', scale = 2, quality = 0.95) {
        const dataUrl = await this.exportImage('jpg', scale, quality);
        this.downloadDataUrl(dataUrl, filename);
    }

    /**
     * Export as SVG and download
     */
    async downloadSVG(filename = 'chart.svg') {
        const dataUrl = await this.exportSVG();
        this.downloadDataUrl(dataUrl, filename);
    }

    /**
     * Copy chart to clipboard
     */
    async copyToClipboard(format = 'png') {
        try {
            if (format === 'png') {
                const dataUrl = await this.exportImage('png', 2);
                const blob = await (await fetch(dataUrl)).blob();

                await navigator.clipboard.write([
                    new ClipboardItem({ 'image/png': blob })
                ]);

                return true;
            }
        } catch (error) {
            console.error('Failed to copy to clipboard:', error);
            return false;
        }
    }

    /**
     * Render chart to canvas context
     */
    renderChartToContext(ctx, width, height) {
        // Save original context
        const originalCtx = this.chart.ctx;
        const originalOverlayCtx = this.chart.overlayCtx;

        // Temporarily use export context
        this.chart.ctx = ctx;
        this.chart.overlayCtx = ctx;

        // Render chart
        this.chart.render();

        // Restore original context
        this.chart.ctx = originalCtx;
        this.chart.overlayCtx = originalOverlayCtx;
    }

    /**
     * Render chart to SVG element
     */
    renderChartToSVG(svg, width, height) {
        // This is a simplified SVG renderer
        // A full implementation would need to convert all canvas operations to SVG

        if (this.chart.data && this.chart.data.length > 0) {
            // Create a group for the chart
            const chartGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            chartGroup.setAttribute('id', 'chart-data');

            // Render data as SVG paths
            // This is chart-type specific and would need to be implemented for each type
            if (this.chart.renderToSVG) {
                this.chart.renderToSVG(chartGroup, width, height);
            } else {
                // Fallback: render as polyline for simple line charts
                const points = this.chart.data.map((d, i) => {
                    const x = (i / this.chart.data.length) * width;
                    const y = height - ((d.close - this.chart.viewport.priceMin) /
                        (this.chart.viewport.priceMax - this.chart.viewport.priceMin)) * height;
                    return `${x},${y}`;
                }).join(' ');

                const polyline = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
                polyline.setAttribute('points', points);
                polyline.setAttribute('fill', 'none');
                polyline.setAttribute('stroke', '#00ff41');
                polyline.setAttribute('stroke-width', '2');

                chartGroup.appendChild(polyline);
            }

            svg.appendChild(chartGroup);
        }

        // Add title if present
        if (this.chart.options.title) {
            const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            text.setAttribute('x', width / 2);
            text.setAttribute('y', 20);
            text.setAttribute('text-anchor', 'middle');
            text.setAttribute('fill', this.chart.options.theme === 'dark' ? '#ffffff' : '#000000');
            text.setAttribute('font-size', '16');
            text.setAttribute('font-family', 'monospace');
            text.textContent = this.chart.options.title;
            svg.appendChild(text);
        }
    }

    /**
     * Batch export multiple charts
     */
    async batchExport(charts, format = 'png', options = {}) {
        const exports = [];

        for (const chart of charts) {
            const exporter = new ChartExportManager(chart);
            const dataUrl = await exporter.exportImage(format, options.scale || 2);
            exports.push({
                chart: chart.options.id || 'chart',
                dataUrl
            });
        }

        return exports;
    }

    /**
     * Create time-lapse video from chart updates
     */
    async createTimeLapse(dataSequence, fps = 10, duration = 10) {
        if (!this.chart.canvas) {
            throw new Error('Chart must use canvas rendering');
        }

        const frameCount = fps * duration;
        const dataPerFrame = Math.ceil(dataSequence.length / frameCount);

        // Start recording
        const recording = this.startRecording({ fps });

        // Update chart with each data slice
        for (let i = 0; i < frameCount; i++) {
            const dataSlice = dataSequence.slice(0, (i + 1) * dataPerFrame);
            this.chart.setData(dataSlice);

            // Wait for next frame
            await new Promise(resolve => setTimeout(resolve, 1000 / fps));
        }

        // Stop recording
        recording.stop();
    }

    /**
     * Export chart configuration
     */
    exportConfig() {
        return {
            type: this.chart.constructor.name,
            options: this.chart.options,
            annotations: this.chart.annotations,
            indicators: this.chart.indicators,
            viewport: this.chart.viewport
        };
    }

    /**
     * Export chart data
     */
    exportData(format = 'json') {
        switch (format) {
            case 'json':
                return JSON.stringify(this.chart.data, null, 2);

            case 'csv':
                return this.convertToCSV(this.chart.data);

            case 'excel':
                return this.convertToExcel(this.chart.data);

            default:
                throw new Error(`Unsupported data format: ${format}`);
        }
    }

    /**
     * Convert data to CSV
     */
    convertToCSV(data) {
        if (!data || data.length === 0) return '';

        const headers = Object.keys(data[0]);
        const csv = [headers.join(',')];

        data.forEach(row => {
            csv.push(headers.map(header => row[header]).join(','));
        });

        return csv.join('\n');
    }

    /**
     * Convert data to Excel (requires SheetJS library)
     */
    convertToExcel(data) {
        if (typeof XLSX === 'undefined') {
            throw new Error('SheetJS library not loaded');
        }

        const ws = XLSX.utils.json_to_sheet(data);
        const wb = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(wb, ws, 'Chart Data');

        return XLSX.write(wb, { bookType: 'xlsx', type: 'array' });
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ChartExportManager };
}
