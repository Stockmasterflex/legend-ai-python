/**
 * Chart Core - Base charting infrastructure
 * Provides foundation for all custom chart types
 */

class ChartCore {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.container = document.getElementById(containerId);
        if (!this.container) {
            throw new Error(`Container ${containerId} not found`);
        }

        this.options = {
            width: options.width || this.container.clientWidth,
            height: options.height || this.container.clientHeight || 500,
            theme: options.theme || 'dark',
            responsive: options.responsive !== false,
            ...options
        };

        this.data = null;
        this.annotations = [];
        this.indicators = [];
        this.destroyed = false;

        this.setupContainer();
        this.setupResizeObserver();
    }

    setupContainer() {
        this.container.style.position = 'relative';
        this.container.style.width = '100%';
        this.container.style.height = `${this.options.height}px`;
    }

    setupResizeObserver() {
        if (!this.options.responsive) return;

        this.resizeObserver = new ResizeObserver(entries => {
            if (this.destroyed) return;
            for (const entry of entries) {
                const { width, height } = entry.contentRect;
                this.handleResize(width, height);
            }
        });

        this.resizeObserver.observe(this.container);
    }

    handleResize(width, height) {
        // Override in subclasses
    }

    setData(data) {
        this.data = data;
        this.render();
    }

    render() {
        // Override in subclasses
        throw new Error('render() must be implemented by subclass');
    }

    addAnnotation(annotation) {
        this.annotations.push(annotation);
        this.renderAnnotations();
    }

    removeAnnotation(id) {
        this.annotations = this.annotations.filter(a => a.id !== id);
        this.renderAnnotations();
    }

    renderAnnotations() {
        // Override in subclasses
    }

    addIndicator(indicator) {
        this.indicators.push(indicator);
        this.renderIndicators();
    }

    removeIndicator(id) {
        this.indicators = this.indicators.filter(i => i.id !== id);
        this.renderIndicators();
    }

    renderIndicators() {
        // Override in subclasses
    }

    exportImage(format = 'png', scale = 2) {
        // Override in subclasses
        throw new Error('exportImage() must be implemented by subclass');
    }

    exportSVG() {
        // Override in subclasses
        throw new Error('exportSVG() must be implemented by subclass');
    }

    destroy() {
        this.destroyed = true;
        if (this.resizeObserver) {
            this.resizeObserver.disconnect();
        }
        this.container.innerHTML = '';
    }
}

/**
 * Canvas-based Chart for high-performance rendering
 */
class CanvasChart extends ChartCore {
    constructor(containerId, options = {}) {
        super(containerId, options);
        this.setupCanvas();
    }

    setupCanvas() {
        this.canvas = document.createElement('canvas');
        this.canvas.style.width = '100%';
        this.canvas.style.height = '100%';
        this.canvas.width = this.options.width * (window.devicePixelRatio || 1);
        this.canvas.height = this.options.height * (window.devicePixelRatio || 1);

        this.ctx = this.canvas.getContext('2d', {
            alpha: false,
            desynchronized: true // Performance optimization
        });

        // Scale for HiDPI displays
        const dpr = window.devicePixelRatio || 1;
        this.ctx.scale(dpr, dpr);

        this.container.appendChild(this.canvas);

        // Add overlay canvas for annotations
        this.overlayCanvas = document.createElement('canvas');
        this.overlayCanvas.style.position = 'absolute';
        this.overlayCanvas.style.top = '0';
        this.overlayCanvas.style.left = '0';
        this.overlayCanvas.style.width = '100%';
        this.overlayCanvas.style.height = '100%';
        this.overlayCanvas.width = this.canvas.width;
        this.overlayCanvas.height = this.canvas.height;
        this.overlayCtx = this.overlayCanvas.getContext('2d');
        this.overlayCtx.scale(dpr, dpr);

        this.container.appendChild(this.overlayCanvas);

        this.setupInteraction();
    }

    setupInteraction() {
        this.isDragging = false;
        this.dragStart = null;
        this.hoveredElement = null;

        this.overlayCanvas.addEventListener('mousedown', this.onMouseDown.bind(this));
        this.overlayCanvas.addEventListener('mousemove', this.onMouseMove.bind(this));
        this.overlayCanvas.addEventListener('mouseup', this.onMouseUp.bind(this));
        this.overlayCanvas.addEventListener('wheel', this.onWheel.bind(this));
        this.overlayCanvas.addEventListener('dblclick', this.onDoubleClick.bind(this));
    }

    onMouseDown(e) {
        const rect = this.overlayCanvas.getBoundingClientRect();
        this.isDragging = true;
        this.dragStart = {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };
    }

    onMouseMove(e) {
        const rect = this.overlayCanvas.getBoundingClientRect();
        const point = {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };

        if (this.isDragging && this.dragStart) {
            this.handleDrag(this.dragStart, point);
        } else {
            this.handleHover(point);
        }
    }

    onMouseUp(e) {
        if (this.isDragging && this.dragStart) {
            const rect = this.overlayCanvas.getBoundingClientRect();
            const point = {
                x: e.clientX - rect.left,
                y: e.clientY - rect.top
            };
            this.handleDragEnd(this.dragStart, point);
        }
        this.isDragging = false;
        this.dragStart = null;
    }

    onWheel(e) {
        e.preventDefault();
        this.handleZoom(e.deltaY > 0 ? 'out' : 'in', e);
    }

    onDoubleClick(e) {
        const rect = this.overlayCanvas.getBoundingClientRect();
        const point = {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };
        this.handleDoubleClick(point);
    }

    handleDrag(start, end) {
        // Override in subclasses
    }

    handleDragEnd(start, end) {
        // Override in subclasses
    }

    handleHover(point) {
        // Override in subclasses
    }

    handleZoom(direction, event) {
        // Override in subclasses
    }

    handleDoubleClick(point) {
        // Override in subclasses
    }

    handleResize(width, height) {
        this.options.width = width;
        this.options.height = height;

        const dpr = window.devicePixelRatio || 1;
        this.canvas.width = width * dpr;
        this.canvas.height = height * dpr;
        this.overlayCanvas.width = width * dpr;
        this.overlayCanvas.height = height * dpr;

        this.ctx.scale(dpr, dpr);
        this.overlayCtx.scale(dpr, dpr);

        this.render();
    }

    clearCanvas(ctx = this.ctx) {
        ctx.clearRect(0, 0, this.options.width, this.options.height);
    }

    exportImage(format = 'png', scale = 2) {
        const tempCanvas = document.createElement('canvas');
        tempCanvas.width = this.options.width * scale;
        tempCanvas.height = this.options.height * scale;
        const tempCtx = tempCanvas.getContext('2d');
        tempCtx.scale(scale, scale);

        // Draw background
        tempCtx.fillStyle = this.options.theme === 'dark' ? '#1a1a2e' : '#ffffff';
        tempCtx.fillRect(0, 0, this.options.width, this.options.height);

        // Draw main canvas
        tempCtx.drawImage(this.canvas, 0, 0, this.options.width, this.options.height);

        // Draw overlay
        tempCtx.drawImage(this.overlayCanvas, 0, 0, this.options.width, this.options.height);

        return tempCanvas.toDataURL(`image/${format}`, 1.0);
    }

    destroy() {
        this.overlayCanvas.removeEventListener('mousedown', this.onMouseDown);
        this.overlayCanvas.removeEventListener('mousemove', this.onMouseMove);
        this.overlayCanvas.removeEventListener('mouseup', this.onMouseUp);
        this.overlayCanvas.removeEventListener('wheel', this.onWheel);
        this.overlayCanvas.removeEventListener('dblclick', this.onDoubleClick);
        super.destroy();
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ChartCore, CanvasChart };
}
