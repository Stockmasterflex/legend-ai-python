/**
 * Point & Figure Chart Implementation
 * Uses Xs and Os to filter out minor price movements
 */

class PointFigureChart extends CanvasChart {
    constructor(containerId, options = {}) {
        super(containerId, options);

        this.boxSize = options.boxSize || 'ATR'; // 'ATR' or fixed number
        this.reversalBoxes = options.reversalBoxes || 3; // Number of boxes for reversal
        this.atrPeriod = options.atrPeriod || 14;
        this.colors = {
            x: options.xColor || '#00ff41',
            o: options.oColor || '#ff0050'
        };

        this.columns = [];
        this.viewport = {
            start: 0,
            end: 50,
            priceMin: 0,
            priceMax: 0
        };
    }

    /**
     * Convert price data to Point & Figure columns
     */
    calculatePFColumns(priceData) {
        if (!priceData || priceData.length === 0) return [];

        // Calculate box size
        let boxSize = this.boxSize;
        if (boxSize === 'ATR') {
            boxSize = this.calculateATR(priceData, this.atrPeriod);
        }

        const columns = [];
        let currentPrice = priceData[0].high;
        let boxBase = Math.floor(currentPrice / boxSize) * boxSize;
        let direction = null; // 'X' or 'O'

        // Start first column
        let currentColumn = {
            type: null,
            boxes: [],
            startIndex: 0
        };

        for (let i = 0; i < priceData.length; i++) {
            const high = priceData[i].high;
            const low = priceData[i].low;

            if (direction === null) {
                // Determine initial direction
                const upBoxes = Math.floor((high - boxBase) / boxSize);
                const downBoxes = Math.floor((boxBase - low) / boxSize);

                if (upBoxes >= 1) {
                    direction = 'X';
                    currentColumn.type = 'X';
                    for (let b = 0; b < upBoxes; b++) {
                        currentColumn.boxes.push(boxBase + b * boxSize);
                    }
                    boxBase += upBoxes * boxSize;
                } else if (downBoxes >= 1) {
                    direction = 'O';
                    currentColumn.type = 'O';
                    for (let b = 0; b < downBoxes; b++) {
                        currentColumn.boxes.push(boxBase - b * boxSize);
                    }
                    boxBase -= downBoxes * boxSize;
                }
            } else if (direction === 'X') {
                // Currently in X column (rising)
                const upBoxes = Math.floor((high - boxBase) / boxSize);

                if (upBoxes >= 1) {
                    // Continue X column
                    for (let b = 0; b < upBoxes; b++) {
                        currentColumn.boxes.push(boxBase + b * boxSize);
                    }
                    boxBase += upBoxes * boxSize;
                } else {
                    // Check for reversal
                    const downBoxes = Math.floor((boxBase - low) / boxSize);
                    if (downBoxes >= this.reversalBoxes) {
                        // Reversal to O
                        columns.push({ ...currentColumn });
                        direction = 'O';
                        boxBase -= boxSize; // Start one box below
                        currentColumn = {
                            type: 'O',
                            boxes: [],
                            startIndex: i
                        };
                        for (let b = 0; b < downBoxes; b++) {
                            currentColumn.boxes.push(boxBase - b * boxSize);
                        }
                        boxBase -= downBoxes * boxSize;
                    }
                }
            } else if (direction === 'O') {
                // Currently in O column (falling)
                const downBoxes = Math.floor((boxBase - low) / boxSize);

                if (downBoxes >= 1) {
                    // Continue O column
                    for (let b = 0; b < downBoxes; b++) {
                        currentColumn.boxes.push(boxBase - b * boxSize);
                    }
                    boxBase -= downBoxes * boxSize;
                } else {
                    // Check for reversal
                    const upBoxes = Math.floor((high - boxBase) / boxSize);
                    if (upBoxes >= this.reversalBoxes) {
                        // Reversal to X
                        columns.push({ ...currentColumn });
                        direction = 'X';
                        boxBase += boxSize; // Start one box above
                        currentColumn = {
                            type: 'X',
                            boxes: [],
                            startIndex: i
                        };
                        for (let b = 0; b < upBoxes; b++) {
                            currentColumn.boxes.push(boxBase + b * boxSize);
                        }
                        boxBase += upBoxes * boxSize;
                    }
                }
            }
        }

        // Add final column
        if (currentColumn.boxes.length > 0) {
            columns.push(currentColumn);
        }

        return columns;
    }

    calculateATR(data, period) {
        if (data.length < period) return (data[0].high - data[0].low) || 1;

        const trueRanges = [];
        for (let i = 1; i < data.length; i++) {
            const high = data[i].high;
            const low = data[i].low;
            const prevClose = data[i - 1].close;

            const tr = Math.max(
                high - low,
                Math.abs(high - prevClose),
                Math.abs(low - prevClose)
            );
            trueRanges.push(tr);
        }

        const recent = trueRanges.slice(-period);
        const atr = recent.reduce((sum, tr) => sum + tr, 0) / recent.length;

        return atr || 1;
    }

    setData(data) {
        this.data = data;
        this.columns = this.calculatePFColumns(data);

        // Calculate viewport
        if (this.columns.length > 0) {
            const allBoxes = this.columns.flatMap(col => col.boxes);
            this.viewport.priceMin = Math.min(...allBoxes);
            this.viewport.priceMax = Math.max(...allBoxes);
            this.viewport.end = Math.min(50, this.columns.length);
        }

        this.render();
    }

    render() {
        if (!this.columns || this.columns.length === 0) return;

        this.clearCanvas();

        const padding = { top: 20, right: 80, bottom: 30, left: 10 };
        const chartWidth = this.options.width - padding.left - padding.right;
        const chartHeight = this.options.height - padding.top - padding.bottom;

        // Get visible columns
        const visibleColumns = this.columns.slice(
            Math.max(0, Math.floor(this.viewport.start)),
            Math.min(this.columns.length, Math.ceil(this.viewport.end))
        );

        if (visibleColumns.length === 0) return;

        // Calculate box size in pixels
        const boxSize = this.boxSize === 'ATR'
            ? this.calculateATR(this.data, this.atrPeriod)
            : this.boxSize;

        const columnWidth = chartWidth / visibleColumns.length;
        const maxColumnWidth = 40;
        const effectiveColumnWidth = Math.min(columnWidth * 0.9, maxColumnWidth);

        // Calculate box height
        const priceRange = this.viewport.priceMax - this.viewport.priceMin;
        const boxHeight = (chartHeight / priceRange) * boxSize;

        const priceToY = (price) => {
            return padding.top + chartHeight * (1 - (price - this.viewport.priceMin) / priceRange);
        };

        // Draw columns
        visibleColumns.forEach((column, colIndex) => {
            const x = padding.left + colIndex * columnWidth + (columnWidth - effectiveColumnWidth) / 2;
            const color = column.type === 'X' ? this.colors.x : this.colors.o;

            this.ctx.strokeStyle = color;
            this.ctx.lineWidth = 2;

            column.boxes.forEach(boxPrice => {
                const y = priceToY(boxPrice);

                if (column.type === 'X') {
                    // Draw X
                    this.ctx.beginPath();
                    this.ctx.moveTo(x, y);
                    this.ctx.lineTo(x + effectiveColumnWidth, y + boxHeight);
                    this.ctx.moveTo(x + effectiveColumnWidth, y);
                    this.ctx.lineTo(x, y + boxHeight);
                    this.ctx.stroke();
                } else {
                    // Draw O
                    this.ctx.beginPath();
                    this.ctx.ellipse(
                        x + effectiveColumnWidth / 2,
                        y + boxHeight / 2,
                        effectiveColumnWidth / 2,
                        boxHeight / 2,
                        0, 0, 2 * Math.PI
                    );
                    this.ctx.stroke();
                }
            });
        });

        // Draw price scale
        this.drawPriceScale(padding, chartHeight, priceToY);

        // Render annotations and indicators
        this.renderAnnotations();
        this.renderIndicators();
    }

    drawPriceScale(padding, chartHeight, priceToY) {
        const numLabels = 10;
        const priceStep = (this.viewport.priceMax - this.viewport.priceMin) / numLabels;

        this.ctx.fillStyle = this.options.theme === 'dark' ? '#aaa' : '#555';
        this.ctx.font = '12px monospace';
        this.ctx.textAlign = 'left';

        for (let i = 0; i <= numLabels; i++) {
            const price = this.viewport.priceMin + i * priceStep;
            const y = priceToY(price);

            // Draw grid line
            this.ctx.strokeStyle = this.options.theme === 'dark' ? '#333' : '#ddd';
            this.ctx.lineWidth = 1;
            this.ctx.beginPath();
            this.ctx.moveTo(padding.left, y);
            this.ctx.lineTo(this.options.width - padding.right, y);
            this.ctx.stroke();

            // Draw price label
            this.ctx.fillText(
                price.toFixed(2),
                this.options.width - padding.right + 5,
                y + 4
            );
        }
    }

    handleZoom(direction, event) {
        const zoomFactor = 1.1;
        const currentRange = this.viewport.end - this.viewport.start;

        if (direction === 'in') {
            const newRange = currentRange / zoomFactor;
            const center = (this.viewport.start + this.viewport.end) / 2;
            this.viewport.start = Math.max(0, center - newRange / 2);
            this.viewport.end = Math.min(this.columns.length, center + newRange / 2);
        } else {
            const newRange = currentRange * zoomFactor;
            const center = (this.viewport.start + this.viewport.end) / 2;
            this.viewport.start = Math.max(0, center - newRange / 2);
            this.viewport.end = Math.min(this.columns.length, center + newRange / 2);
        }

        this.render();
    }

    handleDrag(start, end) {
        const dx = end.x - start.x;
        const chartWidth = this.options.width - 90;
        const visibleColumns = this.viewport.end - this.viewport.start;
        const columnDelta = -(dx / chartWidth) * visibleColumns;

        const newStart = this.viewport.start + columnDelta;
        const newEnd = this.viewport.end + columnDelta;

        if (newStart >= 0 && newEnd <= this.columns.length) {
            this.viewport.start = newStart;
            this.viewport.end = newEnd;
            this.render();
        }

        this.dragStart = end;
    }

    setBoxSize(size) {
        this.boxSize = size;
        if (this.data) {
            this.setData(this.data);
        }
    }

    setReversalBoxes(boxes) {
        this.reversalBoxes = boxes;
        if (this.data) {
            this.setData(this.data);
        }
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { PointFigureChart };
}
