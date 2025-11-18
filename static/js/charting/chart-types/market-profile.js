/**
 * Market Profile Chart Implementation
 * Shows price distribution over time with TPO (Time Price Opportunity)
 */

class MarketProfileChart extends CanvasChart {
    constructor(containerId, options = {}) {
        super(containerId, options);

        this.tickSize = options.tickSize || 0.5;
        this.timePerLetter = options.timePerLetter || 30; // minutes
        this.showValueArea = options.showValueArea !== false;
        this.valueAreaPercent = options.valueAreaPercent || 70; // 70% of volume
        this.colors = {
            tpo: options.tpoColor || '#00bfff',
            poc: options.pocColor || '#ffff00', // Point of Control
            valueArea: options.valueAreaColor || 'rgba(0, 255, 65, 0.2)'
        };

        this.profile = null;
        this.viewport = {
            sessionStart: 0,
            sessionEnd: 1,
            priceMin: 0,
            priceMax: 0
        };
    }

    /**
     * Calculate Market Profile from price data
     */
    calculateProfile(priceData) {
        if (!priceData || priceData.length === 0) return null;

        // Group data by sessions (typically daily)
        const sessions = this.groupBySessions(priceData);

        // Calculate TPO for each session
        const profileData = sessions.map(session => {
            const tpoMap = new Map(); // price level -> count
            const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
            let letterIndex = 0;

            // Sort session data by time
            const sortedData = [...session.data].sort((a, b) => a.timestamp - b.timestamp);

            // Process each time period
            for (let i = 0; i < sortedData.length; i++) {
                const candle = sortedData[i];
                const letter = letters[letterIndex % letters.length];

                // Calculate price levels touched in this period
                const priceLevels = this.getPriceLevels(candle.low, candle.high);

                priceLevels.forEach(price => {
                    if (!tpoMap.has(price)) {
                        tpoMap.set(price, { count: 0, letters: [] });
                    }
                    const tpo = tpoMap.get(price);
                    tpo.count++;
                    tpo.letters.push(letter);
                });

                // Move to next letter every timePerLetter minutes
                if ((i + 1) % Math.ceil(this.timePerLetter / (session.data[0].timeframe || 5)) === 0) {
                    letterIndex++;
                }
            }

            // Find Point of Control (POC) - price with most TPOs
            let poc = null;
            let maxCount = 0;
            for (const [price, tpo] of tpoMap.entries()) {
                if (tpo.count > maxCount) {
                    maxCount = tpo.count;
                    poc = price;
                }
            }

            // Calculate Value Area (70% of TPOs around POC)
            const totalTPOs = Array.from(tpoMap.values()).reduce((sum, tpo) => sum + tpo.count, 0);
            const targetTPOs = totalTPOs * (this.valueAreaPercent / 100);

            const valueArea = this.calculateValueArea(tpoMap, poc, targetTPOs);

            return {
                date: session.date,
                tpoMap,
                poc,
                valueArea,
                priceRange: {
                    high: Math.max(...tpoMap.keys()),
                    low: Math.min(...tpoMap.keys())
                }
            };
        });

        return profileData;
    }

    groupBySessions(priceData) {
        const sessions = [];
        let currentSession = null;

        priceData.forEach(candle => {
            const date = new Date(candle.timestamp);
            const dateKey = date.toISOString().split('T')[0];

            if (!currentSession || currentSession.date !== dateKey) {
                currentSession = { date: dateKey, data: [] };
                sessions.push(currentSession);
            }

            currentSession.data.push(candle);
        });

        return sessions;
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

    calculateValueArea(tpoMap, poc, targetTPOs) {
        if (!poc) return { high: 0, low: 0 };

        const sortedPrices = Array.from(tpoMap.keys()).sort((a, b) => a - b);
        const pocIndex = sortedPrices.indexOf(poc);

        let vaHigh = pocIndex;
        let vaLow = pocIndex;
        let currentTPOs = tpoMap.get(poc).count;

        // Expand value area up and down from POC
        while (currentTPOs < targetTPOs) {
            const aboveTPO = vaHigh < sortedPrices.length - 1
                ? tpoMap.get(sortedPrices[vaHigh + 1]).count
                : 0;
            const belowTPO = vaLow > 0
                ? tpoMap.get(sortedPrices[vaLow - 1]).count
                : 0;

            if (aboveTPO >= belowTPO && vaHigh < sortedPrices.length - 1) {
                vaHigh++;
                currentTPOs += aboveTPO;
            } else if (vaLow > 0) {
                vaLow--;
                currentTPOs += belowTPO;
            } else if (vaHigh < sortedPrices.length - 1) {
                vaHigh++;
                currentTPOs += aboveTPO;
            } else {
                break;
            }
        }

        return {
            high: sortedPrices[vaHigh],
            low: sortedPrices[vaLow]
        };
    }

    setData(data) {
        this.data = data;
        this.profile = this.calculateProfile(data);

        if (this.profile && this.profile.length > 0) {
            const allPrices = this.profile.flatMap(session =>
                Array.from(session.tpoMap.keys())
            );
            this.viewport.priceMin = Math.min(...allPrices);
            this.viewport.priceMax = Math.max(...allPrices);
            this.viewport.sessionEnd = Math.min(1, this.profile.length);
        }

        this.render();
    }

    render() {
        if (!this.profile || this.profile.length === 0) return;

        this.clearCanvas();

        const padding = { top: 20, right: 80, bottom: 30, left: 60 };
        const chartWidth = this.options.width - padding.left - padding.right;
        const chartHeight = this.options.height - padding.top - padding.bottom;

        // Get visible sessions
        const visibleSessions = this.profile.slice(
            Math.floor(this.viewport.sessionStart),
            Math.ceil(this.viewport.sessionEnd)
        );

        if (visibleSessions.length === 0) return;

        const sessionWidth = chartWidth / visibleSessions.length;
        const priceRange = this.viewport.priceMax - this.viewport.priceMin;
        const tickHeight = (chartHeight / priceRange) * this.tickSize;

        const priceToY = (price) => {
            return padding.top + chartHeight * (1 - (price - this.viewport.priceMin) / priceRange);
        };

        // Draw each session
        visibleSessions.forEach((session, sessionIndex) => {
            const x = padding.left + sessionIndex * sessionWidth;

            // Find max TPO count for scaling
            const maxTPO = Math.max(...Array.from(session.tpoMap.values()).map(t => t.count));
            const tpoWidth = (sessionWidth * 0.9) / maxTPO;

            // Draw value area if enabled
            if (this.showValueArea && session.valueArea) {
                const vaTop = priceToY(session.valueArea.high);
                const vaBottom = priceToY(session.valueArea.low);

                this.ctx.fillStyle = this.colors.valueArea;
                this.ctx.fillRect(x, vaTop, sessionWidth * 0.9, vaBottom - vaTop);
            }

            // Draw TPO profile
            const sortedPrices = Array.from(session.tpoMap.keys()).sort((a, b) => b - a);

            sortedPrices.forEach(price => {
                const tpo = session.tpoMap.get(price);
                const y = priceToY(price);
                const width = tpo.count * tpoWidth;

                // Different color for POC
                if (price === session.poc) {
                    this.ctx.fillStyle = this.colors.poc;
                } else {
                    this.ctx.fillStyle = this.colors.tpo;
                }

                this.ctx.fillRect(x, y, width, tickHeight);

                // Draw TPO letters for detailed view
                if (sessionWidth > 100 && tickHeight > 12) {
                    this.ctx.fillStyle = this.options.theme === 'dark' ? '#000' : '#fff';
                    this.ctx.font = '10px monospace';
                    this.ctx.textAlign = 'left';
                    this.ctx.fillText(tpo.letters.join(''), x + 2, y + tickHeight - 2);
                }
            });

            // Draw session date
            this.ctx.fillStyle = this.options.theme === 'dark' ? '#aaa' : '#555';
            this.ctx.font = '11px monospace';
            this.ctx.textAlign = 'center';
            this.ctx.fillText(
                session.date,
                x + sessionWidth / 2,
                this.options.height - 10
            );
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
        this.ctx.textAlign = 'right';

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

            // Draw price label (left side)
            this.ctx.fillText(
                price.toFixed(2),
                padding.left - 5,
                y + 4
            );
        }
    }

    handleZoom(direction, event) {
        const zoomFactor = 1.1;

        if (direction === 'in') {
            const currentRange = this.viewport.priceMax - this.viewport.priceMin;
            const newRange = currentRange / zoomFactor;
            const center = (this.viewport.priceMin + this.viewport.priceMax) / 2;
            this.viewport.priceMin = center - newRange / 2;
            this.viewport.priceMax = center + newRange / 2;
        } else {
            const currentRange = this.viewport.priceMax - this.viewport.priceMin;
            const newRange = currentRange * zoomFactor;
            const center = (this.viewport.priceMin + this.viewport.priceMax) / 2;
            this.viewport.priceMin = center - newRange / 2;
            this.viewport.priceMax = center + newRange / 2;
        }

        this.render();
    }

    handleDrag(start, end) {
        const dy = end.y - start.y;
        const chartHeight = this.options.height - 50;
        const priceRange = this.viewport.priceMax - this.viewport.priceMin;
        const priceDelta = -(dy / chartHeight) * priceRange;

        this.viewport.priceMin += priceDelta;
        this.viewport.priceMax += priceDelta;
        this.render();

        this.dragStart = end;
    }

    setTickSize(size) {
        this.tickSize = size;
        if (this.data) {
            this.setData(this.data);
        }
    }

    setValueAreaPercent(percent) {
        this.valueAreaPercent = percent;
        if (this.data) {
            this.setData(this.data);
        }
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { MarketProfileChart };
}
