/**
 * Kagi Chart Implementation
 * Japanese charting technique that emphasizes trend reversals
 */

class KagiChart extends CanvasChart {
    constructor(containerId, options = {}) {
        super(containerId, options);

        this.reversalAmount = options.reversalAmount || 'ATR'; // 'ATR' or percentage
        this.reversalPercentage = options.reversalPercentage || 4; // 4% default
        this.atrPeriod = options.atrPeriod || 14;
        this.lineColor = {
            thick: options.thickColor || '#00ff41',
            thin: options.thinColor || '#ff0050'
        };
        this.lineWidth = {
            thick: 3,
            thin: 1
        };

        this.kagiLines = [];
        this.viewport = {
            start: 0,
            end: 100,
            priceMin: 0,
            priceMax: 0
        };
    }

    /**
     * Convert price data to Kagi lines
     */
    calculateKagiLines(priceData) {
        if (!priceData || priceData.length === 0) return [];

        // Calculate reversal amount
        let reversalAmount = this.reversalAmount;
        if (reversalAmount === 'ATR') {
            reversalAmount = this.calculateATR(priceData, this.atrPeriod);
        } else {
            // Use percentage of first price
            reversalAmount = priceData[0].close * (this.reversalPercentage / 100);
        }

        const lines = [];
        let currentPrice = priceData[0].close;
        let direction = null; // 'up' or 'down'
        let lineStart = { price: currentPrice, index: 0 };
        let prevSwing = currentPrice;

        for (let i = 1; i < priceData.length; i++) {
            const price = priceData[i].close;

            if (direction === null) {
                // First move
                if (price > currentPrice + reversalAmount) {
                    direction = 'up';
                    lines.push({
                        start: lineStart,
                        end: { price, index: i },
                        direction: 'up',
                        thick: false
                    });
                    currentPrice = price;
                    lineStart = { price, index: i };
                    prevSwing = lineStart.price;
                } else if (price < currentPrice - reversalAmount) {
                    direction = 'down';
                    lines.push({
                        start: lineStart,
                        end: { price, index: i },
                        direction: 'down',
                        thick: false
                    });
                    currentPrice = price;
                    lineStart = { price, index: i };
                    prevSwing = lineStart.price;
                }
            } else if (direction === 'up') {
                if (price > currentPrice) {
                    // Continue upward - update current line
                    if (lines.length > 0) {
                        lines[lines.length - 1].end = { price, index: i };
                    }
                    currentPrice = price;

                    // Check if line should be thick
                    if (price > prevSwing) {
                        lines[lines.length - 1].thick = true;
                    }
                } else if (price < currentPrice - reversalAmount) {
                    // Reversal to down
                    direction = 'down';
                    lineStart = { price: currentPrice, index: i - 1 };
                    lines.push({
                        start: lineStart,
                        end: { price, index: i },
                        direction: 'down',
                        thick: price < prevSwing
                    });
                    prevSwing = currentPrice;
                    currentPrice = price;
                    lineStart = { price, index: i };
                }
            } else if (direction === 'down') {
                if (price < currentPrice) {
                    // Continue downward - update current line
                    if (lines.length > 0) {
                        lines[lines.length - 1].end = { price, index: i };
                    }
                    currentPrice = price;

                    // Check if line should be thick
                    if (price < prevSwing) {
                        lines[lines.length - 1].thick = true;
                    }
                } else if (price > currentPrice + reversalAmount) {
                    // Reversal to up
                    direction = 'up';
                    lineStart = { price: currentPrice, index: i - 1 };
                    lines.push({
                        start: lineStart,
                        end: { price, index: i },
                        direction: 'up',
                        thick: price > prevSwing
                    });
                    prevSwing = currentPrice;
                    currentPrice = price;
                    lineStart = { price, index: i };
                }
            }
        }

        return lines;
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
        this.kagiLines = this.calculateKagiLines(data);

        // Calculate viewport
        if (this.kagiLines.length > 0) {
            const prices = this.kagiLines.flatMap(l => [l.start.price, l.end.price]);
            this.viewport.priceMin = Math.min(...prices);
            this.viewport.priceMax = Math.max(...prices);

            const maxIndex = Math.max(...this.kagiLines.map(l => l.end.index));
            this.viewport.end = Math.min(100, maxIndex);
        }

        this.render();
    }

    render() {
        if (!this.kagiLines || this.kagiLines.length === 0) return;

        this.clearCanvas();

        const padding = { top: 20, right: 80, bottom: 30, left: 10 };
        const chartWidth = this.options.width - padding.left - padding.right;
        const chartHeight = this.options.height - padding.top - padding.bottom;

        // Filter visible lines
        const visibleLines = this.kagiLines.filter(line =>
            line.end.index >= this.viewport.start && line.start.index <= this.viewport.end
        );

        if (visibleLines.length === 0) return;

        // Calculate scales
        const priceRange = this.viewport.priceMax - this.viewport.priceMin;
        const timeRange = this.viewport.end - this.viewport.start;

        const priceToY = (price) => {
            return padding.top + chartHeight * (1 - (price - this.viewport.priceMin) / priceRange);
        };

        const indexToX = (index) => {
            return padding.left + ((index - this.viewport.start) / timeRange) * chartWidth;
        };

        // Draw Kagi lines
        this.ctx.lineCap = 'round';
        this.ctx.lineJoin = 'round';

        visibleLines.forEach(line => {
            const x1 = indexToX(line.start.index);
            const y1 = priceToY(line.start.price);
            const x2 = indexToX(line.end.index);
            const y2 = priceToY(line.end.price);

            // Set style based on thick/thin and direction
            if (line.thick) {
                this.ctx.strokeStyle = this.lineColor.thick;
                this.ctx.lineWidth = this.lineWidth.thick;
            } else {
                this.ctx.strokeStyle = this.lineColor.thin;
                this.ctx.lineWidth = this.lineWidth.thin;
            }

            // Draw vertical line first, then horizontal to connect
            this.ctx.beginPath();
            this.ctx.moveTo(x1, y1);
            this.ctx.lineTo(x1, y2);
            this.ctx.lineTo(x2, y2);
            this.ctx.stroke();
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
            this.viewport.end = Math.min(this.data.length, center + newRange / 2);
        } else {
            const newRange = currentRange * zoomFactor;
            const center = (this.viewport.start + this.viewport.end) / 2;
            this.viewport.start = Math.max(0, center - newRange / 2);
            this.viewport.end = Math.min(this.data.length, center + newRange / 2);
        }

        this.render();
    }

    handleDrag(start, end) {
        const dx = end.x - start.x;
        const chartWidth = this.options.width - 90;
        const timeRange = this.viewport.end - this.viewport.start;
        const timeDelta = -(dx / chartWidth) * timeRange;

        const newStart = this.viewport.start + timeDelta;
        const newEnd = this.viewport.end + timeDelta;

        if (newStart >= 0 && newEnd <= this.data.length) {
            this.viewport.start = newStart;
            this.viewport.end = newEnd;
            this.render();
        }

        this.dragStart = end;
    }

    setReversalAmount(amount) {
        this.reversalAmount = amount;
        if (this.data) {
            this.setData(this.data);
        }
    }

    setReversalPercentage(percentage) {
        this.reversalPercentage = percentage;
        if (this.data && this.reversalAmount !== 'ATR') {
            this.setData(this.data);
        }
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { KagiChart };
}
