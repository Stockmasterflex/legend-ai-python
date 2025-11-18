/**
 * WebGL-accelerated chart renderer
 * Provides high-performance rendering for large datasets
 */

class WebGLRenderer {
    constructor(canvas) {
        this.canvas = canvas;
        this.gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');

        if (!this.gl) {
            throw new Error('WebGL not supported');
        }

        this.programs = {};
        this.buffers = {};
        this.initialize();
    }

    initialize() {
        const gl = this.gl;

        // Set clear color
        gl.clearColor(0.1, 0.1, 0.18, 1.0);
        gl.enable(gl.BLEND);
        gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

        // Create shader programs
        this.programs.line = this.createProgram(
            this.vertexShaderSource,
            this.fragmentShaderSource
        );

        this.programs.candle = this.createProgram(
            this.candleVertexShaderSource,
            this.candleFragmentShaderSource
        );
    }

    get vertexShaderSource() {
        return `
            attribute vec2 a_position;
            attribute vec4 a_color;
            uniform vec2 u_resolution;
            uniform vec2 u_scale;
            uniform vec2 u_offset;
            varying vec4 v_color;

            void main() {
                vec2 scaled = (a_position + u_offset) * u_scale;
                vec2 clipSpace = (scaled / u_resolution) * 2.0 - 1.0;
                gl_Position = vec4(clipSpace * vec2(1, -1), 0, 1);
                v_color = a_color;
            }
        `;
    }

    get fragmentShaderSource() {
        return `
            precision mediump float;
            varying vec4 v_color;

            void main() {
                gl_FragColor = v_color;
            }
        `;
    }

    get candleVertexShaderSource() {
        return `
            attribute vec2 a_position;
            attribute vec2 a_size;
            attribute vec4 a_color;
            uniform vec2 u_resolution;
            uniform vec2 u_scale;
            uniform vec2 u_offset;
            varying vec4 v_color;

            void main() {
                vec2 scaled = (a_position + u_offset) * u_scale;
                vec2 clipSpace = (scaled / u_resolution) * 2.0 - 1.0;
                gl_Position = vec4(clipSpace * vec2(1, -1), 0, 1);
                gl_PointSize = a_size.x;
                v_color = a_color;
            }
        `;
    }

    get candleFragmentShaderSource() {
        return `
            precision mediump float;
            varying vec4 v_color;

            void main() {
                gl_FragColor = v_color;
            }
        `;
    }

    createProgram(vertexSource, fragmentSource) {
        const gl = this.gl;

        const vertexShader = this.createShader(gl.VERTEX_SHADER, vertexSource);
        const fragmentShader = this.createShader(gl.FRAGMENT_SHADER, fragmentSource);

        const program = gl.createProgram();
        gl.attachShader(program, vertexShader);
        gl.attachShader(program, fragmentShader);
        gl.linkProgram(program);

        if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
            console.error('Program link error:', gl.getProgramInfoLog(program));
            gl.deleteProgram(program);
            return null;
        }

        return program;
    }

    createShader(type, source) {
        const gl = this.gl;
        const shader = gl.createShader(type);
        gl.shaderSource(shader, source);
        gl.compileShader(shader);

        if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
            console.error('Shader compile error:', gl.getShaderInfoLog(shader));
            gl.deleteShader(shader);
            return null;
        }

        return shader;
    }

    /**
     * Render line chart with WebGL
     */
    renderLine(data, viewport, color = [0, 1, 0.25, 1]) {
        const gl = this.gl;
        const program = this.programs.line;

        gl.useProgram(program);

        // Prepare data
        const vertices = [];
        const colors = [];

        data.forEach((point, i) => {
            if (point.x >= viewport.minX && point.x <= viewport.maxX) {
                vertices.push(point.x, point.y);
                colors.push(...color);
            }
        });

        // Create buffers
        const positionBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW);

        const colorBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(colors), gl.STATIC_DRAW);

        // Set attributes
        const positionLocation = gl.getAttribLocation(program, 'a_position');
        gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
        gl.enableVertexAttribArray(positionLocation);
        gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);

        const colorLocation = gl.getAttribLocation(program, 'a_color');
        gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
        gl.enableVertexAttribArray(colorLocation);
        gl.vertexAttribPointer(colorLocation, 4, gl.FLOAT, false, 0, 0);

        // Set uniforms
        const resolutionLocation = gl.getUniformLocation(program, 'u_resolution');
        gl.uniform2f(resolutionLocation, gl.canvas.width, gl.canvas.height);

        const scaleLocation = gl.getUniformLocation(program, 'u_scale');
        gl.uniform2f(scaleLocation, viewport.scaleX, viewport.scaleY);

        const offsetLocation = gl.getUniformLocation(program, 'u_offset');
        gl.uniform2f(offsetLocation, viewport.offsetX, viewport.offsetY);

        // Draw
        gl.drawArrays(gl.LINE_STRIP, 0, vertices.length / 2);

        // Cleanup
        gl.deleteBuffer(positionBuffer);
        gl.deleteBuffer(colorBuffer);
    }

    /**
     * Render candlestick chart with WebGL
     */
    renderCandles(candles, viewport) {
        const gl = this.gl;

        // Render wicks
        candles.forEach(candle => {
            this.renderLine([
                { x: candle.x, y: candle.high },
                { x: candle.x, y: candle.low }
            ], viewport, candle.color);
        });

        // Render bodies
        const program = this.programs.candle;
        gl.useProgram(program);

        const vertices = [];
        const sizes = [];
        const colors = [];

        candles.forEach(candle => {
            if (candle.x >= viewport.minX && candle.x <= viewport.maxX) {
                const bodyTop = Math.max(candle.open, candle.close);
                const bodyBottom = Math.min(candle.open, candle.close);
                const bodyHeight = bodyTop - bodyBottom;

                // Create rectangle for body
                vertices.push(candle.x, bodyTop);
                sizes.push(candle.width, bodyHeight);
                colors.push(...candle.color);
            }
        });

        // Create buffers and render
        // (Similar to renderLine but for rectangles)
    }

    /**
     * Clear canvas
     */
    clear() {
        const gl = this.gl;
        gl.clear(gl.COLOR_BUFFER_BIT);
    }

    /**
     * Resize canvas
     */
    resize(width, height) {
        this.canvas.width = width;
        this.canvas.height = height;
        this.gl.viewport(0, 0, width, height);
    }

    /**
     * Dispose of resources
     */
    dispose() {
        const gl = this.gl;

        Object.values(this.programs).forEach(program => {
            if (program) gl.deleteProgram(program);
        });

        Object.values(this.buffers).forEach(buffer => {
            if (buffer) gl.deleteBuffer(buffer);
        });
    }
}

/**
 * Data Decimation for performance optimization
 */
class DataDecimator {
    /**
     * Decimate data based on zoom level
     * Uses Largest Triangle Three Buckets (LTTB) algorithm
     */
    static decimate(data, threshold) {
        if (data.length <= threshold) {
            return data;
        }

        const decimated = [];
        const bucketSize = (data.length - 2) / (threshold - 2);

        // Always include first point
        decimated.push(data[0]);

        for (let i = 0; i < threshold - 2; i++) {
            const avgRangeStart = Math.floor((i + 1) * bucketSize) + 1;
            const avgRangeEnd = Math.floor((i + 2) * bucketSize) + 1;
            const avgRangeLength = avgRangeEnd - avgRangeStart;

            let avgX = 0;
            let avgY = 0;

            for (let j = avgRangeStart; j < avgRangeEnd; j++) {
                avgX += data[j].timestamp || j;
                avgY += data[j].close;
            }

            avgX /= avgRangeLength;
            avgY /= avgRangeLength;

            const rangeStart = Math.floor(i * bucketSize) + 1;
            const rangeEnd = Math.floor((i + 1) * bucketSize) + 1;

            const pointAX = data[decimated.length - 1].timestamp || decimated.length - 1;
            const pointAY = data[decimated.length - 1].close;

            let maxArea = -1;
            let maxAreaPoint = null;

            for (let j = rangeStart; j < rangeEnd; j++) {
                const pointX = data[j].timestamp || j;
                const pointY = data[j].close;

                const area = Math.abs(
                    (pointAX - avgX) * (pointY - pointAY) -
                    (pointAX - pointX) * (avgY - pointAY)
                ) * 0.5;

                if (area > maxArea) {
                    maxArea = area;
                    maxAreaPoint = data[j];
                }
            }

            decimated.push(maxAreaPoint);
        }

        // Always include last point
        decimated.push(data[data.length - 1]);

        return decimated;
    }

    /**
     * Simple downsampling by taking every nth point
     */
    static downsample(data, factor) {
        if (factor <= 1) return data;

        const downsampled = [];
        for (let i = 0; i < data.length; i += factor) {
            downsampled.push(data[i]);
        }

        return downsampled;
    }

    /**
     * Min-Max downsampling (preserves peaks and troughs)
     */
    static minMaxDownsample(data, bucketSize) {
        if (bucketSize <= 1) return data;

        const downsampled = [];

        for (let i = 0; i < data.length; i += bucketSize) {
            const bucket = data.slice(i, i + bucketSize);

            if (bucket.length === 0) continue;

            const min = bucket.reduce((min, d) => d.low < min.low ? d : min);
            const max = bucket.reduce((max, d) => d.high > max.high ? d : max);

            if (min !== max) {
                downsampled.push(min, max);
            } else {
                downsampled.push(min);
            }
        }

        return downsampled;
    }
}

/**
 * Lazy loading manager for historical data
 */
class LazyDataLoader {
    constructor(dataProvider, chunkSize = 500) {
        this.dataProvider = dataProvider;
        this.chunkSize = chunkSize;
        this.loadedRanges = [];
        this.cache = new Map();
        this.loading = new Set();
    }

    /**
     * Load data for a specific range
     */
    async loadRange(start, end) {
        const cacheKey = `${start}-${end}`;

        // Check if already loaded
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        // Check if currently loading
        if (this.loading.has(cacheKey)) {
            return new Promise(resolve => {
                const checkInterval = setInterval(() => {
                    if (this.cache.has(cacheKey)) {
                        clearInterval(checkInterval);
                        resolve(this.cache.get(cacheKey));
                    }
                }, 100);
            });
        }

        // Mark as loading
        this.loading.add(cacheKey);

        try {
            // Load data from provider
            const data = await this.dataProvider.getData(start, end);

            // Cache the data
            this.cache.set(cacheKey, data);

            // Track loaded range
            this.loadedRanges.push({ start, end });

            return data;
        } finally {
            this.loading.delete(cacheKey);
        }
    }

    /**
     * Get data for viewport (loads if needed)
     */
    async getViewportData(viewportStart, viewportEnd, buffer = 100) {
        const start = viewportStart - buffer;
        const end = viewportEnd + buffer;

        // Calculate chunks to load
        const chunks = this.calculateChunks(start, end);

        // Load all chunks
        const chunkData = await Promise.all(
            chunks.map(chunk => this.loadRange(chunk.start, chunk.end))
        );

        // Merge and return
        return this.mergeChunks(chunkData);
    }

    /**
     * Calculate which chunks need to be loaded
     */
    calculateChunks(start, end) {
        const chunks = [];
        let current = Math.floor(start / this.chunkSize) * this.chunkSize;

        while (current < end) {
            const chunkEnd = Math.min(current + this.chunkSize, end);

            // Check if this chunk is already loaded
            const isLoaded = this.loadedRanges.some(
                range => range.start <= current && range.end >= chunkEnd
            );

            if (!isLoaded) {
                chunks.push({ start: current, end: chunkEnd });
            }

            current += this.chunkSize;
        }

        return chunks;
    }

    /**
     * Merge multiple chunks of data
     */
    mergeChunks(chunks) {
        return chunks.flat().sort((a, b) => a.timestamp - b.timestamp);
    }

    /**
     * Clear cache
     */
    clearCache() {
        this.cache.clear();
        this.loadedRanges = [];
    }

    /**
     * Prefetch data for upcoming viewport
     */
    async prefetch(currentStart, currentEnd, direction = 'forward') {
        const range = currentEnd - currentStart;

        if (direction === 'forward') {
            await this.loadRange(currentEnd, currentEnd + range);
        } else {
            await this.loadRange(currentStart - range, currentStart);
        }
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { WebGLRenderer, DataDecimator, LazyDataLoader };
}
