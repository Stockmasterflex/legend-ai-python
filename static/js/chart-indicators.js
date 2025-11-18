/**
 * Technical Indicators Module
 * Calculates and renders technical indicators on Lightweight Charts
 */

const ChartIndicators = {
    /**
     * Add an indicator to the chart
     */
    add(chart, indicatorName, candleData, volumeData) {
        const method = this[indicatorName];
        if (!method) {
            console.error(`Indicator ${indicatorName} not found`);
            return null;
        }
        return method.call(this, chart, candleData, volumeData);
    },

    /**
     * EMA 21
     */
    ema21(chart, candleData) {
        const emaData = this.calculateEMA(candleData, 21);
        const series = chart.addLineSeries({
            color: '#00ffff',
            lineWidth: 2,
            title: 'EMA 21',
            priceLineVisible: false,
        });
        series.setData(emaData);
        return series;
    },

    /**
     * SMA 50
     */
    sma50(chart, candleData) {
        const smaData = this.calculateSMA(candleData, 50);
        const series = chart.addLineSeries({
            color: '#ff00ff',
            lineWidth: 2,
            title: 'SMA 50',
            priceLineVisible: false,
        });
        series.setData(smaData);
        return series;
    },

    /**
     * SMA 200
     */
    sma200(chart, candleData) {
        const smaData = this.calculateSMA(candleData, 200);
        const series = chart.addLineSeries({
            color: '#ffaa00',
            lineWidth: 2,
            title: 'SMA 200',
            priceLineVisible: false,
        });
        series.setData(smaData);
        return series;
    },

    /**
     * Bollinger Bands
     */
    bb(chart, candleData) {
        const bbData = this.calculateBollingerBands(candleData, 20, 2);

        const upperSeries = chart.addLineSeries({
            color: '#9966ff',
            lineWidth: 1,
            title: 'BB Upper',
            priceLineVisible: false,
            lineStyle: LightweightCharts.LineStyle.Dashed,
        });

        const middleSeries = chart.addLineSeries({
            color: '#9966ff',
            lineWidth: 1,
            title: 'BB Middle',
            priceLineVisible: false,
        });

        const lowerSeries = chart.addLineSeries({
            color: '#9966ff',
            lineWidth: 1,
            title: 'BB Lower',
            priceLineVisible: false,
            lineStyle: LightweightCharts.LineStyle.Dashed,
        });

        upperSeries.setData(bbData.upper);
        middleSeries.setData(bbData.middle);
        lowerSeries.setData(bbData.lower);

        return [upperSeries, middleSeries, lowerSeries];
    },

    /**
     * VWAP (Volume Weighted Average Price)
     */
    vwap(chart, candleData, volumeData) {
        const vwapData = this.calculateVWAP(candleData, volumeData);
        const series = chart.addLineSeries({
            color: '#00ff88',
            lineWidth: 2,
            title: 'VWAP',
            priceLineVisible: false,
        });
        series.setData(vwapData);
        return series;
    },

    /**
     * Volume Profile (simplified as histogram overlay)
     */
    volume_profile(chart, candleData, volumeData) {
        // Create volume profile by price levels
        const profileData = this.calculateVolumeProfile(candleData, volumeData);

        // For now, show as markers on the chart
        // In a full implementation, this would be a custom overlay
        const series = chart.addLineSeries({
            color: 'rgba(255, 255, 255, 0.1)',
            lineWidth: 1,
            title: 'Volume Profile',
            priceLineVisible: false,
        });

        return series;
    },

    // ========== Calculation Methods ==========

    /**
     * Calculate Exponential Moving Average
     */
    calculateEMA(data, period) {
        if (data.length < period) return [];

        const emaData = [];
        const multiplier = 2 / (period + 1);

        // Calculate initial SMA as first EMA value
        let sum = 0;
        for (let i = 0; i < period; i++) {
            sum += data[i].close;
        }
        let ema = sum / period;
        emaData.push({ time: data[period - 1].time, value: ema });

        // Calculate EMA for remaining data points
        for (let i = period; i < data.length; i++) {
            ema = (data[i].close - ema) * multiplier + ema;
            emaData.push({ time: data[i].time, value: ema });
        }

        return emaData;
    },

    /**
     * Calculate Simple Moving Average
     */
    calculateSMA(data, period) {
        if (data.length < period) return [];

        const smaData = [];

        for (let i = period - 1; i < data.length; i++) {
            let sum = 0;
            for (let j = 0; j < period; j++) {
                sum += data[i - j].close;
            }
            const sma = sum / period;
            smaData.push({ time: data[i].time, value: sma });
        }

        return smaData;
    },

    /**
     * Calculate Bollinger Bands
     */
    calculateBollingerBands(data, period, stdDev) {
        if (data.length < period) return { upper: [], middle: [], lower: [] };

        const upper = [];
        const middle = [];
        const lower = [];

        for (let i = period - 1; i < data.length; i++) {
            // Calculate SMA (middle band)
            let sum = 0;
            for (let j = 0; j < period; j++) {
                sum += data[i - j].close;
            }
            const sma = sum / period;

            // Calculate standard deviation
            let variance = 0;
            for (let j = 0; j < period; j++) {
                const diff = data[i - j].close - sma;
                variance += diff * diff;
            }
            const std = Math.sqrt(variance / period);

            const time = data[i].time;
            upper.push({ time, value: sma + (stdDev * std) });
            middle.push({ time, value: sma });
            lower.push({ time, value: sma - (stdDev * std) });
        }

        return { upper, middle, lower };
    },

    /**
     * Calculate VWAP
     */
    calculateVWAP(candleData, volumeData) {
        if (candleData.length !== volumeData.length) {
            console.error('Candle and volume data length mismatch');
            return [];
        }

        const vwapData = [];
        let cumulativeTPV = 0; // Cumulative (Typical Price * Volume)
        let cumulativeVolume = 0;

        for (let i = 0; i < candleData.length; i++) {
            const candle = candleData[i];
            const volume = volumeData[i].value;

            // Typical Price = (High + Low + Close) / 3
            const typicalPrice = (candle.high + candle.low + candle.close) / 3;

            cumulativeTPV += typicalPrice * volume;
            cumulativeVolume += volume;

            const vwap = cumulativeVolume > 0 ? cumulativeTPV / cumulativeVolume : typicalPrice;

            vwapData.push({ time: candle.time, value: vwap });
        }

        return vwapData;
    },

    /**
     * Calculate Volume Profile
     */
    calculateVolumeProfile(candleData, volumeData, numBins = 50) {
        if (candleData.length === 0) return [];

        // Find price range
        let minPrice = Infinity;
        let maxPrice = -Infinity;

        candleData.forEach(candle => {
            minPrice = Math.min(minPrice, candle.low);
            maxPrice = Math.max(maxPrice, candle.high);
        });

        const priceRange = maxPrice - minPrice;
        const binSize = priceRange / numBins;

        // Initialize bins
        const bins = Array(numBins).fill(0);

        // Distribute volume across price levels
        candleData.forEach((candle, i) => {
            const volume = volumeData[i]?.value || 0;
            const avgPrice = (candle.high + candle.low) / 2;
            const binIndex = Math.min(
                Math.floor((avgPrice - minPrice) / binSize),
                numBins - 1
            );
            bins[binIndex] += volume;
        });

        // Convert to chart data
        const profileData = bins.map((volume, i) => ({
            price: minPrice + (i * binSize) + (binSize / 2),
            volume: volume
        }));

        return profileData;
    },

    /**
     * Calculate RSI (for future use)
     */
    calculateRSI(data, period = 14) {
        if (data.length < period + 1) return [];

        const rsiData = [];
        const changes = [];

        // Calculate price changes
        for (let i = 1; i < data.length; i++) {
            changes.push(data[i].close - data[i - 1].close);
        }

        // Calculate initial average gain and loss
        let avgGain = 0;
        let avgLoss = 0;

        for (let i = 0; i < period; i++) {
            if (changes[i] > 0) {
                avgGain += changes[i];
            } else {
                avgLoss += Math.abs(changes[i]);
            }
        }

        avgGain /= period;
        avgLoss /= period;

        // Calculate RSI
        for (let i = period; i < changes.length; i++) {
            const rs = avgLoss === 0 ? 100 : avgGain / avgLoss;
            const rsi = 100 - (100 / (1 + rs));

            rsiData.push({
                time: data[i + 1].time,
                value: rsi
            });

            // Update averages
            const change = changes[i];
            const gain = change > 0 ? change : 0;
            const loss = change < 0 ? Math.abs(change) : 0;

            avgGain = ((avgGain * (period - 1)) + gain) / period;
            avgLoss = ((avgLoss * (period - 1)) + loss) / period;
        }

        return rsiData;
    },

    /**
     * Calculate MACD (for future use)
     */
    calculateMACD(data, fastPeriod = 12, slowPeriod = 26, signalPeriod = 9) {
        const fastEMA = this.calculateEMA(data, fastPeriod);
        const slowEMA = this.calculateEMA(data, slowPeriod);

        if (fastEMA.length === 0 || slowEMA.length === 0) return { macd: [], signal: [], histogram: [] };

        // Calculate MACD line
        const macdLine = [];
        const startIndex = slowEMA.length - fastEMA.length;

        for (let i = 0; i < slowEMA.length; i++) {
            const fastValue = fastEMA[i + startIndex]?.value || 0;
            const slowValue = slowEMA[i]?.value || 0;
            macdLine.push({
                time: slowEMA[i].time,
                value: fastValue - slowValue
            });
        }

        // Calculate signal line (EMA of MACD)
        const signalLine = [];
        const multiplier = 2 / (signalPeriod + 1);

        if (macdLine.length < signalPeriod) return { macd: macdLine, signal: [], histogram: [] };

        // Initial signal value (SMA)
        let sum = 0;
        for (let i = 0; i < signalPeriod; i++) {
            sum += macdLine[i].value;
        }
        let signal = sum / signalPeriod;
        signalLine.push({ time: macdLine[signalPeriod - 1].time, value: signal });

        // Calculate remaining signal values (EMA)
        for (let i = signalPeriod; i < macdLine.length; i++) {
            signal = (macdLine[i].value - signal) * multiplier + signal;
            signalLine.push({ time: macdLine[i].time, value: signal });
        }

        // Calculate histogram
        const histogram = [];
        for (let i = 0; i < signalLine.length; i++) {
            const macdIndex = i + (signalPeriod - 1);
            histogram.push({
                time: signalLine[i].time,
                value: macdLine[macdIndex].value - signalLine[i].value
            });
        }

        return { macd: macdLine, signal: signalLine, histogram };
    }
};

// Export for use
window.ChartIndicators = ChartIndicators;
