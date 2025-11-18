/**
 * Custom Indicator Builder
 * Allows users to create custom indicators using formulas and combine indicators
 */

class IndicatorBuilder {
    constructor() {
        this.indicators = new Map();
        this.builtInIndicators = this.initializeBuiltInIndicators();
    }

    /**
     * Initialize built-in indicators
     */
    initializeBuiltInIndicators() {
        return {
            SMA: {
                name: 'Simple Moving Average',
                params: ['period'],
                calculate: (data, period = 20) => {
                    return this.calculateSMA(data, period);
                }
            },
            EMA: {
                name: 'Exponential Moving Average',
                params: ['period'],
                calculate: (data, period = 20) => {
                    return this.calculateEMA(data, period);
                }
            },
            RSI: {
                name: 'Relative Strength Index',
                params: ['period'],
                calculate: (data, period = 14) => {
                    return this.calculateRSI(data, period);
                }
            },
            MACD: {
                name: 'Moving Average Convergence Divergence',
                params: ['fastPeriod', 'slowPeriod', 'signalPeriod'],
                calculate: (data, fastPeriod = 12, slowPeriod = 26, signalPeriod = 9) => {
                    return this.calculateMACD(data, fastPeriod, slowPeriod, signalPeriod);
                }
            },
            BB: {
                name: 'Bollinger Bands',
                params: ['period', 'stdDev'],
                calculate: (data, period = 20, stdDev = 2) => {
                    return this.calculateBollingerBands(data, period, stdDev);
                }
            },
            ATR: {
                name: 'Average True Range',
                params: ['period'],
                calculate: (data, period = 14) => {
                    return this.calculateATR(data, period);
                }
            },
            STOCH: {
                name: 'Stochastic Oscillator',
                params: ['kPeriod', 'dPeriod'],
                calculate: (data, kPeriod = 14, dPeriod = 3) => {
                    return this.calculateStochastic(data, kPeriod, dPeriod);
                }
            },
            ADX: {
                name: 'Average Directional Index',
                params: ['period'],
                calculate: (data, period = 14) => {
                    return this.calculateADX(data, period);
                }
            },
            OBV: {
                name: 'On Balance Volume',
                params: [],
                calculate: (data) => {
                    return this.calculateOBV(data);
                }
            }
        };
    }

    /**
     * Create a custom indicator from a formula
     */
    createCustomIndicator(name, formula, params = {}) {
        const indicator = {
            name,
            formula,
            params,
            type: 'custom',
            calculate: (data) => {
                return this.evaluateFormula(formula, data, params);
            }
        };

        this.indicators.set(name, indicator);
        return indicator;
    }

    /**
     * Evaluate a formula against data
     * Supports operations like: SMA(close, 20), EMA(close, 50), close > SMA(close, 20)
     */
    evaluateFormula(formula, data, params) {
        const context = {
            data,
            params,
            close: data.map(d => d.close),
            open: data.map(d => d.open),
            high: data.map(d => d.high),
            low: data.map(d => d.low),
            volume: data.map(d => d.volume),
            // Built-in functions
            SMA: (arr, period) => this.calculateSMA(
                arr.map((v, i) => ({ close: v })),
                period
            ),
            EMA: (arr, period) => this.calculateEMA(
                arr.map((v, i) => ({ close: v })),
                period
            ),
            RSI: (arr, period) => this.calculateRSI(
                arr.map((v, i) => ({ close: v })),
                period
            ),
            MAX: (arr, period) => this.rollingMax(arr, period),
            MIN: (arr, period) => this.rollingMin(arr, period),
            STD: (arr, period) => this.rollingStd(arr, period),
            SUM: (arr, period) => this.rollingSum(arr, period),
            ABS: (arr) => arr.map(v => Math.abs(v)),
            // Comparison operators
            crossOver: (a, b) => this.detectCrossOver(a, b),
            crossUnder: (a, b) => this.detectCrossUnder(a, b)
        };

        try {
            // Use Function constructor to evaluate formula in context
            const func = new Function(...Object.keys(context), `return ${formula}`);
            return func(...Object.values(context));
        } catch (error) {
            console.error('Formula evaluation error:', error);
            throw new Error(`Invalid formula: ${error.message}`);
        }
    }

    /**
     * Calculate Simple Moving Average
     */
    calculateSMA(data, period) {
        const result = [];

        for (let i = 0; i < data.length; i++) {
            if (i < period - 1) {
                result.push(null);
                continue;
            }

            let sum = 0;
            for (let j = 0; j < period; j++) {
                sum += data[i - j].close;
            }

            result.push(sum / period);
        }

        return result;
    }

    /**
     * Calculate Exponential Moving Average
     */
    calculateEMA(data, period) {
        const result = [];
        const multiplier = 2 / (period + 1);

        // Start with SMA for first value
        let ema = 0;
        for (let i = 0; i < period; i++) {
            ema += data[i].close;
        }
        ema = ema / period;

        for (let i = 0; i < data.length; i++) {
            if (i < period - 1) {
                result.push(null);
            } else if (i === period - 1) {
                result.push(ema);
            } else {
                ema = (data[i].close - ema) * multiplier + ema;
                result.push(ema);
            }
        }

        return result;
    }

    /**
     * Calculate RSI
     */
    calculateRSI(data, period) {
        const result = [];
        const gains = [];
        const losses = [];

        // Calculate price changes
        for (let i = 1; i < data.length; i++) {
            const change = data[i].close - data[i - 1].close;
            gains.push(change > 0 ? change : 0);
            losses.push(change < 0 ? -change : 0);
        }

        // Calculate average gains and losses
        for (let i = 0; i < data.length; i++) {
            if (i < period) {
                result.push(null);
                continue;
            }

            const avgGain = gains.slice(i - period, i).reduce((a, b) => a + b, 0) / period;
            const avgLoss = losses.slice(i - period, i).reduce((a, b) => a + b, 0) / period;

            if (avgLoss === 0) {
                result.push(100);
            } else {
                const rs = avgGain / avgLoss;
                const rsi = 100 - (100 / (1 + rs));
                result.push(rsi);
            }
        }

        return result;
    }

    /**
     * Calculate MACD
     */
    calculateMACD(data, fastPeriod, slowPeriod, signalPeriod) {
        const fastEMA = this.calculateEMA(data, fastPeriod);
        const slowEMA = this.calculateEMA(data, slowPeriod);

        const macdLine = fastEMA.map((fast, i) => {
            if (fast === null || slowEMA[i] === null) return null;
            return fast - slowEMA[i];
        });

        // Calculate signal line (EMA of MACD)
        const macdData = macdLine.map((value, i) => ({ close: value || 0 }));
        const signalLine = this.calculateEMA(macdData, signalPeriod);

        const histogram = macdLine.map((macd, i) => {
            if (macd === null || signalLine[i] === null) return null;
            return macd - signalLine[i];
        });

        return {
            macd: macdLine,
            signal: signalLine,
            histogram
        };
    }

    /**
     * Calculate Bollinger Bands
     */
    calculateBollingerBands(data, period, stdDev) {
        const sma = this.calculateSMA(data, period);
        const upper = [];
        const lower = [];

        for (let i = 0; i < data.length; i++) {
            if (i < period - 1) {
                upper.push(null);
                lower.push(null);
                continue;
            }

            // Calculate standard deviation
            const slice = data.slice(i - period + 1, i + 1);
            const mean = sma[i];
            const variance = slice.reduce((sum, d) => sum + Math.pow(d.close - mean, 2), 0) / period;
            const std = Math.sqrt(variance);

            upper.push(mean + stdDev * std);
            lower.push(mean - stdDev * std);
        }

        return {
            upper,
            middle: sma,
            lower
        };
    }

    /**
     * Calculate ATR
     */
    calculateATR(data, period) {
        const trueRanges = [null]; // First value is null

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

        // Calculate ATR as EMA of true ranges
        const trData = trueRanges.map(tr => ({ close: tr || 0 }));
        return this.calculateEMA(trData, period);
    }

    /**
     * Calculate Stochastic Oscillator
     */
    calculateStochastic(data, kPeriod, dPeriod) {
        const kValues = [];

        for (let i = 0; i < data.length; i++) {
            if (i < kPeriod - 1) {
                kValues.push(null);
                continue;
            }

            const slice = data.slice(i - kPeriod + 1, i + 1);
            const high = Math.max(...slice.map(d => d.high));
            const low = Math.min(...slice.map(d => d.low));
            const close = data[i].close;

            const k = ((close - low) / (high - low)) * 100;
            kValues.push(k);
        }

        // Calculate %D (SMA of %K)
        const kData = kValues.map(k => ({ close: k || 0 }));
        const dValues = this.calculateSMA(kData, dPeriod);

        return {
            k: kValues,
            d: dValues
        };
    }

    /**
     * Calculate ADX
     */
    calculateADX(data, period) {
        const plusDM = [null];
        const minusDM = [null];

        // Calculate +DM and -DM
        for (let i = 1; i < data.length; i++) {
            const highDiff = data[i].high - data[i - 1].high;
            const lowDiff = data[i - 1].low - data[i].low;

            plusDM.push(highDiff > lowDiff && highDiff > 0 ? highDiff : 0);
            minusDM.push(lowDiff > highDiff && lowDiff > 0 ? lowDiff : 0);
        }

        // Calculate ATR
        const atr = this.calculateATR(data, period);

        // Calculate +DI and -DI
        const plusDI = plusDM.map((dm, i) => {
            if (!dm || !atr[i]) return null;
            return (dm / atr[i]) * 100;
        });

        const minusDI = minusDM.map((dm, i) => {
            if (!dm || !atr[i]) return null;
            return (dm / atr[i]) * 100;
        });

        // Calculate DX
        const dx = plusDI.map((pdi, i) => {
            if (!pdi || !minusDI[i]) return null;
            const sum = pdi + minusDI[i];
            if (sum === 0) return 0;
            return (Math.abs(pdi - minusDI[i]) / sum) * 100;
        });

        // Calculate ADX (smoothed DX)
        const dxData = dx.map(d => ({ close: d || 0 }));
        const adx = this.calculateEMA(dxData, period);

        return {
            adx,
            plusDI,
            minusDI
        };
    }

    /**
     * Calculate OBV
     */
    calculateOBV(data) {
        const obv = [data[0].volume];

        for (let i = 1; i < data.length; i++) {
            if (data[i].close > data[i - 1].close) {
                obv.push(obv[i - 1] + data[i].volume);
            } else if (data[i].close < data[i - 1].close) {
                obv.push(obv[i - 1] - data[i].volume);
            } else {
                obv.push(obv[i - 1]);
            }
        }

        return obv;
    }

    // Helper functions

    rollingMax(arr, period) {
        const result = [];
        for (let i = 0; i < arr.length; i++) {
            if (i < period - 1) {
                result.push(null);
            } else {
                result.push(Math.max(...arr.slice(i - period + 1, i + 1)));
            }
        }
        return result;
    }

    rollingMin(arr, period) {
        const result = [];
        for (let i = 0; i < arr.length; i++) {
            if (i < period - 1) {
                result.push(null);
            } else {
                result.push(Math.min(...arr.slice(i - period + 1, i + 1)));
            }
        }
        return result;
    }

    rollingStd(arr, period) {
        const result = [];
        for (let i = 0; i < arr.length; i++) {
            if (i < period - 1) {
                result.push(null);
            } else {
                const slice = arr.slice(i - period + 1, i + 1);
                const mean = slice.reduce((a, b) => a + b, 0) / period;
                const variance = slice.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / period;
                result.push(Math.sqrt(variance));
            }
        }
        return result;
    }

    rollingSum(arr, period) {
        const result = [];
        for (let i = 0; i < arr.length; i++) {
            if (i < period - 1) {
                result.push(null);
            } else {
                result.push(arr.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0));
            }
        }
        return result;
    }

    detectCrossOver(a, b) {
        // Detect when a crosses over b
        const result = [];
        for (let i = 0; i < a.length; i++) {
            if (i === 0 || !a[i] || !b[i] || !a[i - 1] || !b[i - 1]) {
                result.push(false);
            } else {
                result.push(a[i - 1] <= b[i - 1] && a[i] > b[i]);
            }
        }
        return result;
    }

    detectCrossUnder(a, b) {
        // Detect when a crosses under b
        const result = [];
        for (let i = 0; i < a.length; i++) {
            if (i === 0 || !a[i] || !b[i] || !a[i - 1] || !b[i - 1]) {
                result.push(false);
            } else {
                result.push(a[i - 1] >= b[i - 1] && a[i] < b[i]);
            }
        }
        return result;
    }

    /**
     * Combine multiple indicators
     */
    combineIndicators(indicators, combinationLogic) {
        // combinationLogic can be 'AND', 'OR', or a custom function
        const results = indicators.map(ind => ind.values);

        if (combinationLogic === 'AND') {
            return results[0].map((_, i) => {
                return results.every(r => r[i]);
            });
        } else if (combinationLogic === 'OR') {
            return results[0].map((_, i) => {
                return results.some(r => r[i]);
            });
        } else if (typeof combinationLogic === 'function') {
            return results[0].map((_, i) => {
                const values = results.map(r => r[i]);
                return combinationLogic(values);
            });
        }

        throw new Error('Invalid combination logic');
    }

    /**
     * Get indicator by name
     */
    getIndicator(name) {
        return this.indicators.get(name) || this.builtInIndicators[name];
    }

    /**
     * List all available indicators
     */
    listIndicators() {
        return {
            builtin: Object.keys(this.builtInIndicators),
            custom: Array.from(this.indicators.keys())
        };
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { IndicatorBuilder };
}
