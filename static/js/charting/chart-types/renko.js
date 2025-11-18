/**
 * Renko Chart Implementation
 * Filters out time and focuses only on price movements
 */

class RenkoChart extends CanvasChart {
    constructor(containerId, options = {}) {
        super(containerId, options);

        this.brickSize = options.brickSize || 'ATR'; // 'ATR' or fixed number
        this.atrPeriod = options.atrPeriod || 14;
        this.brickColor = {
            up: options.upColor || '#00ff41',
            down: options.downColor || '#ff0050'
        };

        this.renkoBricks = [];
        this.viewport = {
            start: 0,
            end: 100,
            priceMin: 0,
            priceMax: 0
        };
    }

    /**
     * Convert OHLC data to Renko bricks
     */
    calculateRenkoBricks(ohlcData) {
        if (!ohlcData || ohlcData.length === 0) return [];

        // Calculate brick size from ATR if needed
        let brickSize = this.brickSize;
        if (brickSize === 'ATR') {
            brickSize = this.calculateATR(ohlcData, this.atrPeriod);
        }

        const bricks = [];
        let currentPrice = ohlcData[0].close;
        let brickOpen = Math.floor(currentPrice / brickSize) * brickSize;

        for (const candle of ohlcData) {
            const close = candle.close;

            // Check for upward bricks
            while (close >= brickOpen + brickSize) {
                bricks.push({
                    open: brickOpen,
                    close: brickOpen + brickSize,
                    direction: 'up',
                    timestamp: candle.timestamp
                });
                brickOpen += brickSize;
            }

            // Check for downward bricks
            while (close <= brickOpen - brickSize) {
                bricks.push({
                    open: brickOpen,
                    close: brickOpen - brickSize,
                    direction: 'down',
                    timestamp: candle.timestamp
                });
                brickOpen -= brickSize;
            }
        }

        return bricks;
    }

    /**
     * Calculate Average True Range for brick size
     */
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

        // Calculate ATR (simple moving average of true ranges)
        const recent = trueRanges.slice(-period);
        const atr = recent.reduce((sum, tr) => sum + tr, 0) / recent.length;

        return atr || 1;
    }

    setData(data) {
        this.data = data;
        this.renkoBricks = this.calculateRenkoBricks(data);

        // Calculate viewport
        if (this.renkoBricks.length > 0) {
            const prices = this.renkoBricks.flatMap(b => [b.open, b.close]);
            this.viewport.priceMin = Math.min(...prices);
            this.viewport.priceMax = Math.max(...prices);
            this.viewport.end = Math.min(100, this.renkoBricks.length);
        }

        this.render();
    }

    render() {
        if (!this.renkoBricks || this.renkoBricks.length === 0) return;

        this.clearCanvas();

        const padding = { top: 20, right: 80, bottom: 30, left: 10 };
        const chartWidth = this.options.width - padding.left - padding.right;
        const chartHeight = this.options.height - padding.top - padding.bottom;

        // Calculate visible bricks
        const visibleBricks = this.renkoBricks.slice(
            Math.max(0, this.viewport.start),
            Math.min(this.renkoBricks.length, this.viewport.end)
        );

        if (visibleBricks.length === 0) return;

        // Calculate brick width
        const brickWidth = chartWidth / visibleBricks.length;
        const maxBrickWidth = 50;
        const effectiveBrickWidth = Math.min(brickWidth * 0.8, maxBrickWidth);

        // Price scale
        const priceRange = this.viewport.priceMax - this.viewport.priceMin;
        const priceToY = (price) => {
            return padding.top + chartHeight * (1 - (price - this.viewport.priceMin) / priceRange);
        };

        // Draw bricks
        visibleBricks.forEach((brick, index) => {
            const x = padding.left + index * brickWidth + (brickWidth - effectiveBrickWidth) / 2;
            const y1 = priceToY(brick.open);
            const y2 = priceToY(brick.close);
            const height = Math.abs(y2 - y1);

            this.ctx.fillStyle = brick.direction === 'up' ? this.brickColor.up : this.brickColor.down;
            this.ctx.fillRect(x, Math.min(y1, y2), effectiveBrickWidth, height);

            // Draw border
            this.ctx.strokeStyle = this.options.theme === 'dark' ? '#000' : '#fff';
            this.ctx.lineWidth = 1;
            this.ctx.strokeRect(x, Math.min(y1, y2), effectiveBrickWidth, height);
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
            this.viewport.end = Math.min(this.renkoBricks.length, center + newRange / 2);
        } else {
            const newRange = currentRange * zoomFactor;
            const center = (this.viewport.start + this.viewport.end) / 2;
            this.viewport.start = Math.max(0, center - newRange / 2);
            this.viewport.end = Math.min(this.renkoBricks.length, center + newRange / 2);
        }

        this.render();
    }

    handleDrag(start, end) {
        const dx = end.x - start.x;
        const brickWidth = (this.options.width - 90) / (this.viewport.end - this.viewport.start);
        const brickDelta = -dx / brickWidth;

        const newStart = this.viewport.start + brickDelta;
        const newEnd = this.viewport.end + brickDelta;

        if (newStart >= 0 && newEnd <= this.renkoBricks.length) {
            this.viewport.start = newStart;
            this.viewport.end = newEnd;
            this.render();
        }

        this.dragStart = end;
    }

    setBrickSize(size) {
        this.brickSize = size;
        if (this.data) {
            this.setData(this.data);
        }
    }

    setATRPeriod(period) {
        this.atrPeriod = period;
        if (this.data && this.brickSize === 'ATR') {
            this.setData(this.data);
        }
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { RenkoChart };
}
