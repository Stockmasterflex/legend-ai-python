/**
 * Footprint Chart Implementation
 * Shows bid/ask volume at each price level within each candle
 */

class FootprintChart extends CanvasChart {
    constructor(containerId, options = {}) {
        super(containerId, options);

        this.tickSize = options.tickSize || 0.1;
        this.showDelta = options.showDelta !== false;
        this.showImbalance = options.showImbalance !== false;
        this.imbalanceRatio = options.imbalanceRatio || 1.5; // 1.5:1 ratio for imbalance
        this.colors = {
            bidVolume: options.bidColor || '#ff0050',
            askVolume: options.askColor || '#00ff41',
            delta: {
                positive: options.deltaPositiveColor || '#00ff41',
                negative: options.deltaNegativeColor || '#ff0050'
            },
            imbalance: {
                bid: options.imbalanceBidColor || 'rgba(255, 0, 80, 0.3)',
                ask: options.imbalanceAskColor || 'rgba(0, 255, 65, 0.3)'
            }
        };

        this.candles = [];
        this.viewport = {
            start: 0,
            end: 50,
            priceMin: 0,
            priceMax: 0
        };
    }

    /**
     * Process tick data to create footprint candles
     * Note: Requires tick-level data with bid/ask volume
     */
    calculateFootprint(tickData) {
        if (!tickData || tickData.length === 0) return [];

        // Group ticks into candles (by time period)
        const candles = this.groupIntoCandles(tickData);

        // For each candle, calculate bid/ask volume at each price level
        const footprintCandles = candles.map(candle => {
            const priceMap = new Map(); // price -> { bid, ask, delta }

            candle.ticks.forEach(tick => {
                const priceLevel = this.roundToTick(tick.price);

                if (!priceMap.has(priceLevel)) {
                    priceMap.set(priceLevel, { bid: 0, ask: 0, delta: 0 });
                }

                const level = priceMap.get(priceLevel);

                // Determine if trade was at bid or ask
                // Uptick = ask (buyer initiated), Downtick = bid (seller initiated)
                if (tick.aggressor === 'buy' || tick.delta > 0) {
                    level.ask += tick.volume;
                    level.delta += tick.volume;
                } else {
                    level.bid += tick.volume;
                    level.delta -= tick.volume;
                }
            });

            // Find imbalances
            const imbalances = [];
            for (const [price, level] of priceMap.entries()) {
                const total = level.bid + level.ask;
                if (total > 0) {
                    const bidRatio = level.bid / total;
                    const askRatio = level.ask / total;

                    if (bidRatio >= (this.imbalanceRatio / (this.imbalanceRatio + 1))) {
                        imbalances.push({ price, type: 'bid', ratio: bidRatio });
                    } else if (askRatio >= (this.imbalanceRatio / (this.imbalanceRatio + 1))) {
                        imbalances.push({ price, type: 'ask', ratio: askRatio });
                    }
                }
            }

            return {
                timestamp: candle.timestamp,
                open: candle.open,
                high: candle.high,
                low: candle.low,
                close: candle.close,
                priceMap,
                imbalances,
                totalDelta: Array.from(priceMap.values()).reduce((sum, l) => sum + l.delta, 0)
            };
        });

        return footprintCandles;
    }

    groupIntoCandles(tickData) {
        // Group ticks by time period (e.g., 5 minutes, 1 hour)
        const candlePeriod = 5 * 60 * 1000; // 5 minutes in milliseconds
        const candles = [];
        let currentCandle = null;

        tickData.forEach(tick => {
            const candleTime = Math.floor(tick.timestamp / candlePeriod) * candlePeriod;

            if (!currentCandle || currentCandle.timestamp !== candleTime) {
                if (currentCandle) candles.push(currentCandle);

                currentCandle = {
                    timestamp: candleTime,
                    open: tick.price,
                    high: tick.price,
                    low: tick.price,
                    close: tick.price,
                    ticks: []
                };
            }

            currentCandle.high = Math.max(currentCandle.high, tick.price);
            currentCandle.low = Math.min(currentCandle.low, tick.price);
            currentCandle.close = tick.price;
            currentCandle.ticks.push(tick);
        });

        if (currentCandle) candles.push(currentCandle);

        return candles;
    }

    roundToTick(price) {
        return Math.round(price / this.tickSize) * this.tickSize;
    }

    setData(data) {
        // If data has tick-level info, use it
        // Otherwise, simulate from OHLCV (less accurate but works)
        if (data && data[0] && data[0].ticks) {
            this.candles = this.calculateFootprint(data);
        } else {
            this.candles = this.simulateFootprint(data);
        }

        if (this.candles.length > 0) {
            const allPrices = this.candles.flatMap(c =>
                Array.from(c.priceMap.keys())
            );
            this.viewport.priceMin = Math.min(...allPrices);
            this.viewport.priceMax = Math.max(...allPrices);
            this.viewport.end = Math.min(50, this.candles.length);
        }

        this.render();
    }

    /**
     * Simulate footprint data from OHLCV when tick data is not available
     */
    simulateFootprint(ohlcvData) {
        return ohlcvData.map(candle => {
            const priceMap = new Map();
            const priceLevels = this.getPriceLevels(candle.low, candle.high);

            // Distribute volume across price levels
            // This is a simulation - real footprint needs tick data
            const volumePerLevel = candle.volume / priceLevels.length;

            priceLevels.forEach(price => {
                // Simulate bid/ask split based on price movement
                const isRising = candle.close > candle.open;
                const bidRatio = isRising ? 0.4 : 0.6;
                const askRatio = 1 - bidRatio;

                const bid = volumePerLevel * bidRatio * (0.8 + Math.random() * 0.4);
                const ask = volumePerLevel * askRatio * (0.8 + Math.random() * 0.4);

                priceMap.set(price, {
                    bid: Math.round(bid),
                    ask: Math.round(ask),
                    delta: Math.round(ask - bid)
                });
            });

            // Find imbalances
            const imbalances = [];
            for (const [price, level] of priceMap.entries()) {
                const total = level.bid + level.ask;
                if (total > 0) {
                    const bidRatio = level.bid / total;
                    const askRatio = level.ask / total;

                    if (bidRatio >= (this.imbalanceRatio / (this.imbalanceRatio + 1))) {
                        imbalances.push({ price, type: 'bid', ratio: bidRatio });
                    } else if (askRatio >= (this.imbalanceRatio / (this.imbalanceRatio + 1))) {
                        imbalances.push({ price, type: 'ask', ratio: askRatio });
                    }
                }
            }

            return {
                timestamp: candle.timestamp,
                open: candle.open,
                high: candle.high,
                low: candle.low,
                close: candle.close,
                priceMap,
                imbalances,
                totalDelta: Array.from(priceMap.values()).reduce((sum, l) => sum + l.delta, 0)
            };
        });
    }

    getPriceLevels(low, high) {
        const levels = [];
        const startLevel = Math.floor(low / this.tickSize) * this.tickSize;
        const endLevel = Math.ceil(high / this.tickSize) * this.tickSize;

        for (let price = startLevel; price <= endLevel; price += this.tickSize) {
            levels.push(parseFloat(price.toFixed(6)));
        }

        return levels;
    }

    render() {
        if (!this.candles || this.candles.length === 0) return;

        this.clearCanvas();

        const padding = { top: 20, right: 80, bottom: 30, left: 10 };
        const chartWidth = this.options.width - padding.left - padding.right;
        const chartHeight = this.options.height - padding.top - padding.bottom;

        // Get visible candles
        const visibleCandles = this.candles.slice(
            Math.max(0, Math.floor(this.viewport.start)),
            Math.min(this.candles.length, Math.ceil(this.viewport.end))
        );

        if (visibleCandles.length === 0) return;

        const candleWidth = chartWidth / visibleCandles.length;
        const maxCandleWidth = 100;
        const effectiveCandleWidth = Math.min(candleWidth * 0.95, maxCandleWidth);

        const priceRange = this.viewport.priceMax - this.viewport.priceMin;
        const tickHeight = (chartHeight / priceRange) * this.tickSize;

        const priceToY = (price) => {
            return padding.top + chartHeight * (1 - (price - this.viewport.priceMin) / priceRange);
        };

        // Draw each candle's footprint
        visibleCandles.forEach((candle, index) => {
            const x = padding.left + index * candleWidth + (candleWidth - effectiveCandleWidth) / 2;

            // Draw imbalances as background
            if (this.showImbalance) {
                candle.imbalances.forEach(imbalance => {
                    const y = priceToY(imbalance.price);
                    this.ctx.fillStyle = imbalance.type === 'bid'
                        ? this.colors.imbalance.bid
                        : this.colors.imbalance.ask;
                    this.ctx.fillRect(x, y, effectiveCandleWidth, tickHeight);
                });
            }

            // Draw bid/ask volumes at each price level
            const sortedPrices = Array.from(candle.priceMap.keys()).sort((a, b) => b - a);

            sortedPrices.forEach(price => {
                const level = candle.priceMap.get(price);
                const y = priceToY(price);

                const totalVolume = level.bid + level.ask;
                if (totalVolume === 0) return;

                // Calculate column widths
                const bidWidth = (level.bid / totalVolume) * effectiveCandleWidth;
                const askWidth = (level.ask / totalVolume) * effectiveCandleWidth;

                // Draw bid volume (left side)
                this.ctx.fillStyle = this.colors.bidVolume;
                this.ctx.fillRect(x, y, bidWidth, tickHeight);

                // Draw ask volume (right side)
                this.ctx.fillStyle = this.colors.askVolume;
                this.ctx.fillRect(x + effectiveCandleWidth - askWidth, y, askWidth, tickHeight);

                // Draw volume numbers if space allows
                if (effectiveCandleWidth > 50 && tickHeight > 10) {
                    this.ctx.fillStyle = this.options.theme === 'dark' ? '#fff' : '#000';
                    this.ctx.font = '9px monospace';
                    this.ctx.textAlign = 'center';

                    // Show delta or bid/ask
                    if (this.showDelta) {
                        const deltaText = level.delta > 0 ? `+${level.delta}` : `${level.delta}`;
                        this.ctx.fillStyle = level.delta > 0
                            ? this.colors.delta.positive
                            : this.colors.delta.negative;
                        this.ctx.fillText(deltaText, x + effectiveCandleWidth / 2, y + tickHeight / 2 + 3);
                    } else {
                        this.ctx.fillText(
                            `${level.bid}x${level.ask}`,
                            x + effectiveCandleWidth / 2,
                            y + tickHeight / 2 + 3
                        );
                    }
                }
            });

            // Draw candle outline
            this.ctx.strokeStyle = this.options.theme === 'dark' ? '#555' : '#ccc';
            this.ctx.lineWidth = 1;
            this.ctx.strokeRect(x, priceToY(candle.high), effectiveCandleWidth, priceToY(candle.low) - priceToY(candle.high));
        });

        // Draw price scale
        this.drawPriceScale(padding, chartHeight, priceToY);

        // Render annotations and indicators
        this.renderAnnotations();
        this.renderIndicators();
    }

    drawPriceScale(padding, chartHeight, priceToY) {
        const numLabels = 20;
        const priceStep = (this.viewport.priceMax - this.viewport.priceMin) / numLabels;

        this.ctx.fillStyle = this.options.theme === 'dark' ? '#aaa' : '#555';
        this.ctx.font = '11px monospace';
        this.ctx.textAlign = 'left';

        for (let i = 0; i <= numLabels; i++) {
            const price = this.viewport.priceMin + i * priceStep;
            const y = priceToY(price);

            // Draw grid line
            this.ctx.strokeStyle = this.options.theme === 'dark' ? '#2a2a3e' : '#e0e0e0';
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
            this.viewport.end = Math.min(this.candles.length, center + newRange / 2);
        } else {
            const newRange = currentRange * zoomFactor;
            const center = (this.viewport.start + this.viewport.end) / 2;
            this.viewport.start = Math.max(0, center - newRange / 2);
            this.viewport.end = Math.min(this.candles.length, center + newRange / 2);
        }

        this.render();
    }

    handleDrag(start, end) {
        const dx = end.x - start.x;
        const chartWidth = this.options.width - 90;
        const visibleRange = this.viewport.end - this.viewport.start;
        const candleDelta = -(dx / chartWidth) * visibleRange;

        const newStart = this.viewport.start + candleDelta;
        const newEnd = this.viewport.end + candleDelta;

        if (newStart >= 0 && newEnd <= this.candles.length) {
            this.viewport.start = newStart;
            this.viewport.end = newEnd;
            this.render();
        }

        this.dragStart = end;
    }

    setTickSize(size) {
        this.tickSize = size;
        if (this.data) {
            this.setData(this.data);
        }
    }

    toggleDelta() {
        this.showDelta = !this.showDelta;
        this.render();
    }

    toggleImbalance() {
        this.showImbalance = !this.showImbalance;
        this.render();
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { FootprintChart };
}
