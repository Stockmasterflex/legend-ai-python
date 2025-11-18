/**
 * Strategy Backtesting Engine
 * Allows users to backtest trading strategies on historical data
 */

class BacktestingEngine {
    constructor() {
        this.strategies = new Map();
        this.results = new Map();
    }

    /**
     * Create a trading strategy
     */
    createStrategy(config) {
        const strategy = {
            name: config.name,
            entryCondition: config.entryCondition, // Function returning true/false
            exitCondition: config.exitCondition, // Function returning true/false
            stopLoss: config.stopLoss || null, // Percentage or absolute value
            takeProfit: config.takeProfit || null, // Percentage or absolute value
            trailingStop: config.trailingStop || null,
            positionSize: config.positionSize || 100, // Percentage of capital
            maxPositions: config.maxPositions || 1,
            direction: config.direction || 'both', // 'long', 'short', 'both'
            timeframe: config.timeframe || '1h'
        };

        this.strategies.set(strategy.name, strategy);
        return strategy;
    }

    /**
     * Run backtest on historical data
     */
    runBacktest(strategyName, data, initialCapital = 10000, config = {}) {
        const strategy = this.strategies.get(strategyName);
        if (!strategy) {
            throw new Error(`Strategy ${strategyName} not found`);
        }

        const results = {
            strategyName,
            initialCapital,
            finalCapital: initialCapital,
            totalReturn: 0,
            totalReturnPercent: 0,
            trades: [],
            openPositions: [],
            equity: [initialCapital],
            drawdown: [],
            maxDrawdown: 0,
            winRate: 0,
            profitFactor: 0,
            sharpeRatio: 0,
            startDate: data[0].timestamp,
            endDate: data[data.length - 1].timestamp
        };

        let capital = initialCapital;
        let positions = [];
        let peakCapital = initialCapital;

        // Calculate indicators if needed
        const indicators = this.calculateIndicators(data, config.indicators || {});

        // Iterate through data
        for (let i = 1; i < data.length; i++) {
            const currentBar = data[i];
            const context = {
                data: data.slice(0, i + 1),
                indicators: this.sliceIndicators(indicators, i),
                capital,
                positions,
                bar: i
            };

            // Check exit conditions for open positions
            positions = positions.filter(position => {
                const exitSignal = this.checkExit(position, currentBar, strategy, context);

                if (exitSignal) {
                    // Close position
                    const pnl = this.calculatePnL(position, currentBar.close);
                    capital += pnl.total;

                    results.trades.push({
                        entryTime: position.entryTime,
                        exitTime: currentBar.timestamp,
                        entryPrice: position.entryPrice,
                        exitPrice: currentBar.close,
                        quantity: position.quantity,
                        direction: position.direction,
                        pnl: pnl.net,
                        pnlPercent: pnl.percent,
                        reason: exitSignal.reason
                    });

                    return false; // Remove from positions
                }

                return true; // Keep position
            });

            // Check entry conditions
            if (positions.length < strategy.maxPositions) {
                const entrySignal = this.checkEntry(strategy, context);

                if (entrySignal) {
                    const positionSize = (capital * (strategy.positionSize / 100));
                    const quantity = positionSize / currentBar.close;
                    const commission = this.calculateCommission(positionSize, config.commission);

                    const position = {
                        entryTime: currentBar.timestamp,
                        entryPrice: currentBar.close,
                        quantity,
                        direction: entrySignal.direction,
                        stopLoss: strategy.stopLoss,
                        takeProfit: strategy.takeProfit,
                        trailingStop: strategy.trailingStop,
                        highestPrice: currentBar.close,
                        lowestPrice: currentBar.close
                    };

                    positions.push(position);
                    capital -= commission;
                }
            }

            // Update trailing stops
            positions.forEach(position => {
                if (position.trailingStop) {
                    position.highestPrice = Math.max(position.highestPrice, currentBar.high);
                    position.lowestPrice = Math.min(position.lowestPrice, currentBar.low);
                }
            });

            // Calculate current equity
            const positionValue = positions.reduce((sum, pos) => {
                return sum + this.calculatePnL(pos, currentBar.close).total;
            }, 0);

            const currentEquity = capital + positionValue;
            results.equity.push(currentEquity);

            // Calculate drawdown
            peakCapital = Math.max(peakCapital, currentEquity);
            const drawdown = ((peakCapital - currentEquity) / peakCapital) * 100;
            results.drawdown.push(drawdown);
            results.maxDrawdown = Math.max(results.maxDrawdown, drawdown);
        }

        // Close any remaining positions
        positions.forEach(position => {
            const pnl = this.calculatePnL(position, data[data.length - 1].close);
            capital += pnl.total;

            results.trades.push({
                entryTime: position.entryTime,
                exitTime: data[data.length - 1].timestamp,
                entryPrice: position.entryPrice,
                exitPrice: data[data.length - 1].close,
                quantity: position.quantity,
                direction: position.direction,
                pnl: pnl.net,
                pnlPercent: pnl.percent,
                reason: 'end-of-data'
            });
        });

        // Calculate final statistics
        results.finalCapital = capital;
        results.totalReturn = capital - initialCapital;
        results.totalReturnPercent = ((capital - initialCapital) / initialCapital) * 100;

        const winningTrades = results.trades.filter(t => t.pnl > 0);
        const losingTrades = results.trades.filter(t => t.pnl < 0);

        results.winRate = (winningTrades.length / results.trades.length) * 100;

        const totalWins = winningTrades.reduce((sum, t) => sum + t.pnl, 0);
        const totalLosses = Math.abs(losingTrades.reduce((sum, t) => sum + t.pnl, 0));
        results.profitFactor = totalLosses > 0 ? totalWins / totalLosses : Infinity;

        results.sharpeRatio = this.calculateSharpeRatio(results.equity);

        this.results.set(strategyName, results);
        return results;
    }

    /**
     * Check entry conditions
     */
    checkEntry(strategy, context) {
        try {
            const signal = strategy.entryCondition(context);

            if (signal === true) {
                return { direction: strategy.direction === 'both' ? 'long' : strategy.direction };
            } else if (typeof signal === 'object') {
                return signal; // { direction: 'long' or 'short' }
            }

            return null;
        } catch (error) {
            console.error('Entry condition error:', error);
            return null;
        }
    }

    /**
     * Check exit conditions
     */
    checkExit(position, currentBar, strategy, context) {
        // Check stop loss
        if (position.stopLoss) {
            const stopPrice = position.direction === 'long'
                ? position.entryPrice * (1 - position.stopLoss / 100)
                : position.entryPrice * (1 + position.stopLoss / 100);

            if ((position.direction === 'long' && currentBar.low <= stopPrice) ||
                (position.direction === 'short' && currentBar.high >= stopPrice)) {
                return { reason: 'stop-loss' };
            }
        }

        // Check take profit
        if (position.takeProfit) {
            const targetPrice = position.direction === 'long'
                ? position.entryPrice * (1 + position.takeProfit / 100)
                : position.entryPrice * (1 - position.takeProfit / 100);

            if ((position.direction === 'long' && currentBar.high >= targetPrice) ||
                (position.direction === 'short' && currentBar.low <= targetPrice)) {
                return { reason: 'take-profit' };
            }
        }

        // Check trailing stop
        if (position.trailingStop) {
            const trailPrice = position.direction === 'long'
                ? position.highestPrice * (1 - position.trailingStop / 100)
                : position.lowestPrice * (1 + position.trailingStop / 100);

            if ((position.direction === 'long' && currentBar.low <= trailPrice) ||
                (position.direction === 'short' && currentBar.high >= trailPrice)) {
                return { reason: 'trailing-stop' };
            }
        }

        // Check exit condition
        try {
            if (strategy.exitCondition({ ...context, position })) {
                return { reason: 'exit-signal' };
            }
        } catch (error) {
            console.error('Exit condition error:', error);
        }

        return null;
    }

    /**
     * Calculate P&L for a position
     */
    calculatePnL(position, currentPrice) {
        const direction = position.direction === 'long' ? 1 : -1;
        const priceDiff = (currentPrice - position.entryPrice) * direction;
        const gross = priceDiff * position.quantity;
        const net = gross; // Can subtract fees here
        const percent = (priceDiff / position.entryPrice) * 100 * direction;

        return { gross, net, total: position.entryPrice * position.quantity + net, percent };
    }

    /**
     * Calculate commission
     */
    calculateCommission(positionSize, commissionRate = 0.001) {
        return positionSize * commissionRate;
    }

    /**
     * Calculate Sharpe Ratio
     */
    calculateSharpeRatio(equityCurve, riskFreeRate = 0.02) {
        const returns = [];
        for (let i = 1; i < equityCurve.length; i++) {
            returns.push((equityCurve[i] - equityCurve[i - 1]) / equityCurve[i - 1]);
        }

        const avgReturn = returns.reduce((a, b) => a + b, 0) / returns.length;
        const variance = returns.reduce((sum, r) => sum + Math.pow(r - avgReturn, 2), 0) / returns.length;
        const stdDev = Math.sqrt(variance);

        const annualizedReturn = avgReturn * 252; // Assuming daily data
        const annualizedStdDev = stdDev * Math.sqrt(252);

        return (annualizedReturn - riskFreeRate) / annualizedStdDev;
    }

    /**
     * Calculate indicators for backtesting
     */
    calculateIndicators(data, indicatorConfigs) {
        const indicators = {};

        // This would use IndicatorBuilder from indicator-builder.js
        // For now, return empty object
        return indicators;
    }

    /**
     * Slice indicators to current bar
     */
    sliceIndicators(indicators, index) {
        const sliced = {};
        for (const [name, values] of Object.entries(indicators)) {
            if (Array.isArray(values)) {
                sliced[name] = values.slice(0, index + 1);
            } else {
                sliced[name] = values;
            }
        }
        return sliced;
    }

    /**
     * Get backtest results
     */
    getResults(strategyName) {
        return this.results.get(strategyName);
    }

    /**
     * Generate performance report
     */
    generateReport(strategyName) {
        const results = this.results.get(strategyName);
        if (!results) return null;

        const trades = results.trades;
        const winningTrades = trades.filter(t => t.pnl > 0);
        const losingTrades = trades.filter(t => t.pnl < 0);

        return {
            summary: {
                totalTrades: trades.length,
                winningTrades: winningTrades.length,
                losingTrades: losingTrades.length,
                winRate: results.winRate.toFixed(2) + '%',
                profitFactor: results.profitFactor.toFixed(2),
                sharpeRatio: results.sharpeRatio.toFixed(2),
                maxDrawdown: results.maxDrawdown.toFixed(2) + '%',
                totalReturn: results.totalReturn.toFixed(2),
                totalReturnPercent: results.totalReturnPercent.toFixed(2) + '%'
            },
            trades: {
                avgWin: winningTrades.length > 0
                    ? (winningTrades.reduce((sum, t) => sum + t.pnl, 0) / winningTrades.length).toFixed(2)
                    : 0,
                avgLoss: losingTrades.length > 0
                    ? (losingTrades.reduce((sum, t) => sum + t.pnl, 0) / losingTrades.length).toFixed(2)
                    : 0,
                largestWin: Math.max(...trades.map(t => t.pnl), 0).toFixed(2),
                largestLoss: Math.min(...trades.map(t => t.pnl), 0).toFixed(2),
                avgHoldTime: this.calculateAvgHoldTime(trades)
            },
            equity: results.equity,
            drawdown: results.drawdown,
            allTrades: trades
        };
    }

    calculateAvgHoldTime(trades) {
        if (trades.length === 0) return '0h';

        const totalTime = trades.reduce((sum, t) => {
            return sum + (new Date(t.exitTime) - new Date(t.entryTime));
        }, 0);

        const avgMs = totalTime / trades.length;
        const hours = Math.floor(avgMs / (1000 * 60 * 60));
        const minutes = Math.floor((avgMs % (1000 * 60 * 60)) / (1000 * 60));

        return `${hours}h ${minutes}m`;
    }

    /**
     * Compare multiple strategies
     */
    compareStrategies(strategyNames) {
        const comparison = {};

        strategyNames.forEach(name => {
            const results = this.results.get(name);
            if (results) {
                comparison[name] = {
                    totalReturn: results.totalReturnPercent,
                    sharpeRatio: results.sharpeRatio,
                    maxDrawdown: results.maxDrawdown,
                    winRate: results.winRate,
                    profitFactor: results.profitFactor,
                    totalTrades: results.trades.length
                };
            }
        });

        return comparison;
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { BacktestingEngine };
}
