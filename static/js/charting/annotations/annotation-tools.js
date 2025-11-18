/**
 * Interactive Annotation Tools
 * Provides drawing tools for trend lines, Fibonacci, patterns, etc.
 */

class AnnotationManager {
    constructor(chart) {
        this.chart = chart;
        this.annotations = [];
        this.currentTool = null;
        this.drawingState = null;
        this.selectedAnnotation = null;
        this.nextId = 1;
    }

    setTool(toolType) {
        this.currentTool = toolType;
        this.drawingState = null;
    }

    handleMouseDown(point, chartData) {
        if (!this.currentTool) return;

        const pricePoint = this.chart.screenToPrice(point);

        switch (this.currentTool) {
            case 'trendline':
                this.drawingState = { type: 'trendline', start: pricePoint };
                break;
            case 'fibonacci':
                this.drawingState = { type: 'fibonacci', start: pricePoint };
                break;
            case 'horizontal':
                this.addHorizontalLine(pricePoint.price);
                break;
            case 'vertical':
                this.addVerticalLine(pricePoint.time);
                break;
            case 'rectangle':
                this.drawingState = { type: 'rectangle', start: pricePoint };
                break;
            case 'triangle':
                this.drawingState = { type: 'triangle', points: [pricePoint] };
                break;
            case 'support-resistance':
                this.drawingState = { type: 'support-resistance', start: pricePoint };
                break;
            default:
                console.warn('Unknown tool:', this.currentTool);
        }
    }

    handleMouseMove(point) {
        if (!this.drawingState) return;

        const pricePoint = this.chart.screenToPrice(point);
        this.drawingState.current = pricePoint;

        // Trigger redraw
        this.chart.render();
    }

    handleMouseUp(point) {
        if (!this.drawingState) return;

        const pricePoint = this.chart.screenToPrice(point);

        switch (this.drawingState.type) {
            case 'trendline':
                this.addTrendLine(this.drawingState.start, pricePoint);
                break;
            case 'fibonacci':
                this.addFibonacci(this.drawingState.start, pricePoint);
                break;
            case 'rectangle':
                this.addRectangle(this.drawingState.start, pricePoint);
                break;
            case 'triangle':
                this.drawingState.points.push(pricePoint);
                if (this.drawingState.points.length >= 3) {
                    this.addTriangle(this.drawingState.points);
                    this.drawingState = null;
                }
                return; // Don't clear state yet
            case 'support-resistance':
                this.addSupportResistanceZone(this.drawingState.start, pricePoint);
                break;
        }

        this.drawingState = null;
        this.chart.render();
    }

    addTrendLine(start, end, options = {}) {
        const annotation = {
            id: this.nextId++,
            type: 'trendline',
            start,
            end,
            color: options.color || '#00ff41',
            width: options.width || 2,
            style: options.style || 'solid', // 'solid', 'dashed', 'dotted'
            extend: options.extend || false
        };

        this.annotations.push(annotation);
        return annotation.id;
    }

    addFibonacci(start, end, options = {}) {
        const levels = options.levels || [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0];
        const annotation = {
            id: this.nextId++,
            type: 'fibonacci',
            start,
            end,
            levels,
            colors: options.colors || {
                0: '#808080',
                0.236: '#ff0000',
                0.382: '#ff8000',
                0.5: '#ffff00',
                0.618: '#00ff00',
                0.786: '#0080ff',
                1.0: '#808080'
            },
            showLabels: options.showLabels !== false
        };

        this.annotations.push(annotation);
        return annotation.id;
    }

    addHorizontalLine(price, options = {}) {
        const annotation = {
            id: this.nextId++,
            type: 'horizontal',
            price,
            color: options.color || '#00bfff',
            width: options.width || 1,
            style: options.style || 'solid',
            label: options.label || ''
        };

        this.annotations.push(annotation);
        return annotation.id;
    }

    addVerticalLine(time, options = {}) {
        const annotation = {
            id: this.nextId++,
            type: 'vertical',
            time,
            color: options.color || '#00bfff',
            width: options.width || 1,
            style: options.style || 'solid',
            label: options.label || ''
        };

        this.annotations.push(annotation);
        return annotation.id;
    }

    addRectangle(start, end, options = {}) {
        const annotation = {
            id: this.nextId++,
            type: 'rectangle',
            start,
            end,
            fillColor: options.fillColor || 'rgba(0, 191, 255, 0.2)',
            borderColor: options.borderColor || '#00bfff',
            borderWidth: options.borderWidth || 1
        };

        this.annotations.push(annotation);
        return annotation.id;
    }

    addTriangle(points, options = {}) {
        const annotation = {
            id: this.nextId++,
            type: 'triangle',
            points,
            fillColor: options.fillColor || 'rgba(255, 255, 0, 0.2)',
            borderColor: options.borderColor || '#ffff00',
            borderWidth: options.borderWidth || 2
        };

        this.annotations.push(annotation);
        return annotation.id;
    }

    addSupportResistanceZone(start, end, options = {}) {
        const annotation = {
            id: this.nextId++,
            type: 'support-resistance',
            start,
            end,
            color: options.color || 'rgba(255, 255, 0, 0.3)',
            label: options.label || ''
        };

        this.annotations.push(annotation);
        return annotation.id;
    }

    removeAnnotation(id) {
        this.annotations = this.annotations.filter(a => a.id !== id);
        this.chart.render();
    }

    clearAll() {
        this.annotations = [];
        this.chart.render();
    }

    render(ctx, viewport) {
        // Render all annotations
        this.annotations.forEach(annotation => {
            this.renderAnnotation(ctx, annotation, viewport);
        });

        // Render annotation being drawn
        if (this.drawingState && this.drawingState.current) {
            const tempAnnotation = { ...this.drawingState };
            tempAnnotation.end = tempAnnotation.current;
            this.renderAnnotation(ctx, tempAnnotation, viewport);
        }
    }

    renderAnnotation(ctx, annotation, viewport) {
        switch (annotation.type) {
            case 'trendline':
                this.renderTrendLine(ctx, annotation, viewport);
                break;
            case 'fibonacci':
                this.renderFibonacci(ctx, annotation, viewport);
                break;
            case 'horizontal':
                this.renderHorizontalLine(ctx, annotation, viewport);
                break;
            case 'vertical':
                this.renderVerticalLine(ctx, annotation, viewport);
                break;
            case 'rectangle':
                this.renderRectangle(ctx, annotation, viewport);
                break;
            case 'triangle':
                this.renderTriangle(ctx, annotation, viewport);
                break;
            case 'support-resistance':
                this.renderSupportResistanceZone(ctx, annotation, viewport);
                break;
        }
    }

    renderTrendLine(ctx, annotation, viewport) {
        const start = this.chart.priceToScreen(annotation.start);
        const end = this.chart.priceToScreen(annotation.end);

        if (!start || !end) return;

        ctx.strokeStyle = annotation.color;
        ctx.lineWidth = annotation.width;

        if (annotation.style === 'dashed') {
            ctx.setLineDash([5, 5]);
        } else if (annotation.style === 'dotted') {
            ctx.setLineDash([2, 2]);
        } else {
            ctx.setLineDash([]);
        }

        ctx.beginPath();
        ctx.moveTo(start.x, start.y);
        ctx.lineTo(end.x, end.y);
        ctx.stroke();

        ctx.setLineDash([]);
    }

    renderFibonacci(ctx, annotation, viewport) {
        const start = this.chart.priceToScreen(annotation.start);
        const end = this.chart.priceToScreen(annotation.end);

        if (!start || !end) return;

        const priceRange = annotation.end.price - annotation.start.price;

        annotation.levels.forEach(level => {
            const price = annotation.start.price + priceRange * level;
            const y = this.chart.priceToScreen({ price, time: annotation.start.time })?.y;

            if (!y) return;

            // Draw line
            ctx.strokeStyle = annotation.colors[level] || '#808080';
            ctx.lineWidth = level === 0.618 ? 2 : 1;
            ctx.setLineDash([3, 3]);
            ctx.beginPath();
            ctx.moveTo(start.x, y);
            ctx.lineTo(end.x, y);
            ctx.stroke();

            // Draw label
            if (annotation.showLabels) {
                ctx.fillStyle = annotation.colors[level] || '#808080';
                ctx.font = '12px monospace';
                ctx.textAlign = 'right';
                ctx.fillText(`${(level * 100).toFixed(1)}% (${price.toFixed(2)})`, end.x - 5, y - 5);
            }
        });

        ctx.setLineDash([]);
    }

    renderHorizontalLine(ctx, annotation, viewport) {
        const point = this.chart.priceToScreen({ price: annotation.price, time: viewport.start });

        if (!point) return;

        ctx.strokeStyle = annotation.color;
        ctx.lineWidth = annotation.width;

        if (annotation.style === 'dashed') {
            ctx.setLineDash([5, 5]);
        } else if (annotation.style === 'dotted') {
            ctx.setLineDash([2, 2]);
        } else {
            ctx.setLineDash([]);
        }

        ctx.beginPath();
        ctx.moveTo(0, point.y);
        ctx.lineTo(viewport.width, point.y);
        ctx.stroke();

        ctx.setLineDash([]);

        // Draw label
        if (annotation.label) {
            ctx.fillStyle = annotation.color;
            ctx.font = '12px monospace';
            ctx.textAlign = 'left';
            ctx.fillText(annotation.label, 5, point.y - 5);
        }
    }

    renderVerticalLine(ctx, annotation, viewport) {
        const point = this.chart.priceToScreen({ price: viewport.priceMin, time: annotation.time });

        if (!point) return;

        ctx.strokeStyle = annotation.color;
        ctx.lineWidth = annotation.width;

        if (annotation.style === 'dashed') {
            ctx.setLineDash([5, 5]);
        } else if (annotation.style === 'dotted') {
            ctx.setLineDash([2, 2]);
        } else {
            ctx.setLineDash([]);
        }

        ctx.beginPath();
        ctx.moveTo(point.x, 0);
        ctx.lineTo(point.x, viewport.height);
        ctx.stroke();

        ctx.setLineDash([]);

        // Draw label
        if (annotation.label) {
            ctx.fillStyle = annotation.color;
            ctx.font = '12px monospace';
            ctx.textAlign = 'center';
            ctx.fillText(annotation.label, point.x, 15);
        }
    }

    renderRectangle(ctx, annotation, viewport) {
        const start = this.chart.priceToScreen(annotation.start);
        const end = this.chart.priceToScreen(annotation.end);

        if (!start || !end) return;

        const x = Math.min(start.x, end.x);
        const y = Math.min(start.y, end.y);
        const width = Math.abs(end.x - start.x);
        const height = Math.abs(end.y - start.y);

        // Fill
        ctx.fillStyle = annotation.fillColor;
        ctx.fillRect(x, y, width, height);

        // Border
        ctx.strokeStyle = annotation.borderColor;
        ctx.lineWidth = annotation.borderWidth;
        ctx.strokeRect(x, y, width, height);
    }

    renderTriangle(ctx, annotation, viewport) {
        if (annotation.points.length < 3) return;

        const points = annotation.points.map(p => this.chart.priceToScreen(p)).filter(p => p);

        if (points.length < 3) return;

        // Fill
        ctx.fillStyle = annotation.fillColor;
        ctx.beginPath();
        ctx.moveTo(points[0].x, points[0].y);
        ctx.lineTo(points[1].x, points[1].y);
        ctx.lineTo(points[2].x, points[2].y);
        ctx.closePath();
        ctx.fill();

        // Border
        ctx.strokeStyle = annotation.borderColor;
        ctx.lineWidth = annotation.borderWidth;
        ctx.stroke();
    }

    renderSupportResistanceZone(ctx, annotation, viewport) {
        const start = this.chart.priceToScreen(annotation.start);
        const end = this.chart.priceToScreen(annotation.end);

        if (!start || !end) return;

        const y = Math.min(start.y, end.y);
        const height = Math.abs(end.y - start.y);

        // Draw zone
        ctx.fillStyle = annotation.color;
        ctx.fillRect(0, y, viewport.width, height);

        // Draw label
        if (annotation.label) {
            ctx.fillStyle = '#fff';
            ctx.font = 'bold 12px monospace';
            ctx.textAlign = 'left';
            ctx.fillText(annotation.label, 5, y + height / 2);
        }
    }

    getAnnotationAtPoint(point) {
        // Check if point is near any annotation
        // Returns annotation ID if found, null otherwise
        for (let i = this.annotations.length - 1; i >= 0; i--) {
            const annotation = this.annotations[i];
            if (this.isPointNearAnnotation(point, annotation)) {
                return annotation.id;
            }
        }
        return null;
    }

    isPointNearAnnotation(point, annotation) {
        // Simple distance check - can be enhanced
        const threshold = 5; // pixels

        switch (annotation.type) {
            case 'trendline':
                return this.isPointNearLine(point, annotation.start, annotation.end, threshold);
            case 'horizontal':
                return Math.abs(point.y - annotation.price) < threshold;
            // Add more cases as needed
            default:
                return false;
        }
    }

    isPointNearLine(point, start, end, threshold) {
        // Calculate distance from point to line segment
        const startScreen = this.chart.priceToScreen(start);
        const endScreen = this.chart.priceToScreen(end);

        if (!startScreen || !endScreen) return false;

        const A = point.x - startScreen.x;
        const B = point.y - startScreen.y;
        const C = endScreen.x - startScreen.x;
        const D = endScreen.y - startScreen.y;

        const dot = A * C + B * D;
        const lenSq = C * C + D * D;
        let param = -1;

        if (lenSq !== 0) param = dot / lenSq;

        let xx, yy;

        if (param < 0) {
            xx = startScreen.x;
            yy = startScreen.y;
        } else if (param > 1) {
            xx = endScreen.x;
            yy = endScreen.y;
        } else {
            xx = startScreen.x + param * C;
            yy = startScreen.y + param * D;
        }

        const dx = point.x - xx;
        const dy = point.y - yy;

        return Math.sqrt(dx * dx + dy * dy) < threshold;
    }

    exportAnnotations() {
        return JSON.stringify(this.annotations);
    }

    importAnnotations(json) {
        try {
            this.annotations = JSON.parse(json);
            this.chart.render();
        } catch (e) {
            console.error('Failed to import annotations:', e);
        }
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AnnotationManager };
}
