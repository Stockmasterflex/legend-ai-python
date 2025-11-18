/**
 * Harmonic Pattern Recognition and Drawing
 * Detects Gartley, Butterfly, Bat, Crab, and other harmonic patterns
 */

class HarmonicPatternDetector {
    constructor(tolerance = 0.05) {
        this.tolerance = tolerance; // 5% tolerance for Fibonacci ratios

        // Harmonic pattern definitions
        this.patterns = {
            gartley: {
                name: 'Gartley',
                ratios: {
                    AB_XA: [0.618],
                    BC_AB: [0.382, 0.886],
                    CD_BC: [1.13, 1.618],
                    AD_XA: [0.786]
                }
            },
            butterfly: {
                name: 'Butterfly',
                ratios: {
                    AB_XA: [0.786],
                    BC_AB: [0.382, 0.886],
                    CD_BC: [1.618, 2.24],
                    AD_XA: [1.27, 1.618]
                }
            },
            bat: {
                name: 'Bat',
                ratios: {
                    AB_XA: [0.382, 0.5],
                    BC_AB: [0.382, 0.886],
                    CD_BC: [1.618, 2.618],
                    AD_XA: [0.886]
                }
            },
            crab: {
                name: 'Crab',
                ratios: {
                    AB_XA: [0.382, 0.618],
                    BC_AB: [0.382, 0.886],
                    CD_BC: [2.24, 3.618],
                    AD_XA: [1.618]
                }
            },
            shark: {
                name: 'Shark',
                ratios: {
                    AB_XA: [1.13, 1.618],
                    BC_AB: [1.618, 2.24],
                    CD_BC: [0.886, 1.13],
                    AD_XA: [0.886, 1.13]
                }
            },
            cypher: {
                name: 'Cypher',
                ratios: {
                    AB_XA: [0.382, 0.618],
                    BC_AB: [1.13, 1.414],
                    CD_BC: [0.618, 0.786],
                    CD_XC: [0.786]
                }
            }
        };
    }

    /**
     * Scan price data for harmonic patterns
     */
    detectPatterns(priceData, minBars = 20, maxBars = 100) {
        const patterns = [];

        // Identify swing points (peaks and troughs)
        const swingPoints = this.findSwingPoints(priceData);

        // Look for 5-point patterns (X, A, B, C, D)
        for (let i = 0; i < swingPoints.length - 4; i++) {
            const X = swingPoints[i];
            const A = swingPoints[i + 1];
            const B = swingPoints[i + 2];
            const C = swingPoints[i + 3];
            const D = swingPoints[i + 4];

            // Check if pattern spans appropriate time
            const barSpan = D.index - X.index;
            if (barSpan < minBars || barSpan > maxBars) continue;

            // Check if pattern is valid structure (alternating peaks/troughs)
            if (!this.isValidStructure(X, A, B, C, D)) continue;

            // Check against each harmonic pattern
            for (const [patternType, patternDef] of Object.entries(this.patterns)) {
                if (this.matchesPattern(X, A, B, C, D, patternDef)) {
                    const pattern = {
                        type: patternType,
                        name: patternDef.name,
                        points: { X, A, B, C, D },
                        bullish: D.price < X.price,
                        prz: this.calculatePRZ(X, A, B, C, D, patternDef), // Potential Reversal Zone
                        targets: this.calculateTargets(X, A, B, C, D)
                    };

                    patterns.push(pattern);
                }
            }
        }

        return patterns;
    }

    /**
     * Find swing points (local peaks and troughs)
     */
    findSwingPoints(priceData, lookback = 5) {
        const swingPoints = [];

        for (let i = lookback; i < priceData.length - lookback; i++) {
            const current = priceData[i];
            let isPeak = true;
            let isTrough = true;

            // Check if current point is higher/lower than surrounding points
            for (let j = i - lookback; j <= i + lookback; j++) {
                if (j === i) continue;

                if (current.high <= priceData[j].high) isPeak = false;
                if (current.low >= priceData[j].low) isTrough = false;
            }

            if (isPeak) {
                swingPoints.push({
                    index: i,
                    price: current.high,
                    timestamp: current.timestamp,
                    type: 'peak'
                });
            } else if (isTrough) {
                swingPoints.push({
                    index: i,
                    price: current.low,
                    timestamp: current.timestamp,
                    type: 'trough'
                });
            }
        }

        return swingPoints;
    }

    /**
     * Check if 5 points form a valid pattern structure
     */
    isValidStructure(X, A, B, C, D) {
        // For bullish pattern: X peak, A trough, B peak, C trough, D peak
        // For bearish pattern: X trough, A peak, B trough, C peak, D trough

        if (X.type === 'peak') {
            return A.type === 'trough' && B.type === 'peak' &&
                   C.type === 'trough' && D.type === 'peak';
        } else {
            return A.type === 'peak' && B.type === 'trough' &&
                   C.type === 'peak' && D.type === 'trough';
        }
    }

    /**
     * Check if points match a harmonic pattern definition
     */
    matchesPattern(X, A, B, C, D, patternDef) {
        const XA = Math.abs(A.price - X.price);
        const AB = Math.abs(B.price - A.price);
        const BC = Math.abs(C.price - B.price);
        const CD = Math.abs(D.price - C.price);
        const AD = Math.abs(D.price - A.price);
        const XC = Math.abs(C.price - X.price);

        // Check AB/XA ratio
        const AB_XA = AB / XA;
        if (!this.matchesRatio(AB_XA, patternDef.ratios.AB_XA)) return false;

        // Check BC/AB ratio
        const BC_AB = BC / AB;
        if (!this.matchesRatio(BC_AB, patternDef.ratios.BC_AB)) return false;

        // Check CD/BC ratio
        const CD_BC = CD / BC;
        if (!this.matchesRatio(CD_BC, patternDef.ratios.CD_BC)) return false;

        // Check AD/XA ratio
        const AD_XA = AD / XA;
        if (patternDef.ratios.AD_XA) {
            if (!this.matchesRatio(AD_XA, patternDef.ratios.AD_XA)) return false;
        }

        // Check CD/XC ratio (for patterns like Cypher)
        if (patternDef.ratios.CD_XC) {
            const CD_XC = CD / XC;
            if (!this.matchesRatio(CD_XC, patternDef.ratios.CD_XC)) return false;
        }

        return true;
    }

    /**
     * Check if actual ratio matches expected ratio (with tolerance)
     */
    matchesRatio(actual, expected) {
        if (!Array.isArray(expected)) expected = [expected];

        for (const exp of expected) {
            const diff = Math.abs(actual - exp) / exp;
            if (diff <= this.tolerance) return true;
        }

        return false;
    }

    /**
     * Calculate Potential Reversal Zone
     */
    calculatePRZ(X, A, B, C, D, patternDef) {
        const XA = A.price - X.price;
        const BC = C.price - B.price;

        // PRZ is typically at the D point
        // Calculate expected range based on pattern ratios
        const expectedRatios = patternDef.ratios.AD_XA || [0.786];
        const priceRange = expectedRatios.map(ratio => X.price + XA * ratio);

        return {
            center: D.price,
            range: [Math.min(...priceRange), Math.max(...priceRange)]
        };
    }

    /**
     * Calculate profit targets based on Fibonacci levels
     */
    calculateTargets(X, A, B, C, D) {
        const AD = D.price - A.price;

        return {
            target1: D.price + AD * 0.382,
            target2: D.price + AD * 0.618,
            target3: D.price + AD * 1.0,
            stopLoss: D.price - AD * 0.236
        };
    }
}

/**
 * Harmonic Pattern Annotation
 */
class HarmonicPatternAnnotation {
    constructor(annotationManager) {
        this.annotationManager = annotationManager;
        this.detector = new HarmonicPatternDetector();
        this.detectedPatterns = [];
    }

    /**
     * Auto-detect patterns in price data
     */
    autoDetect(priceData) {
        this.detectedPatterns = this.detector.detectPatterns(priceData);

        // Add annotations for each detected pattern
        this.detectedPatterns.forEach(pattern => {
            this.drawPattern(pattern);
        });

        return this.detectedPatterns;
    }

    /**
     * Manually draw a harmonic pattern
     */
    drawPattern(pattern) {
        const { X, A, B, C, D } = pattern.points;
        const color = pattern.bullish ? '#00ff41' : '#ff0050';

        // Draw lines connecting points
        this.annotationManager.addTrendLine(X, A, { color, width: 2 });
        this.annotationManager.addTrendLine(A, B, { color, width: 2 });
        this.annotationManager.addTrendLine(B, C, { color, width: 2 });
        this.annotationManager.addTrendLine(C, D, { color, width: 2 });

        // Draw XA, XB, XC, XD lines (lightly)
        const lightColor = pattern.bullish ? 'rgba(0, 255, 65, 0.3)' : 'rgba(255, 0, 80, 0.3)';
        this.annotationManager.addTrendLine(X, C, { color: lightColor, width: 1, style: 'dashed' });
        this.annotationManager.addTrendLine(X, D, { color: lightColor, width: 1, style: 'dashed' });

        // Draw PRZ zone
        if (pattern.prz) {
            this.annotationManager.addSupportResistanceZone(
                { price: pattern.prz.range[0], time: D.timestamp },
                { price: pattern.prz.range[1], time: D.timestamp },
                { color: 'rgba(255, 255, 0, 0.2)', label: 'PRZ' }
            );
        }

        // Draw targets
        if (pattern.targets) {
            const targetColor = 'rgba(0, 191, 255, 0.5)';
            this.annotationManager.addHorizontalLine(pattern.targets.target1, {
                color: targetColor,
                style: 'dashed',
                label: 'T1'
            });
            this.annotationManager.addHorizontalLine(pattern.targets.target2, {
                color: targetColor,
                style: 'dashed',
                label: 'T2'
            });
            this.annotationManager.addHorizontalLine(pattern.targets.target3, {
                color: targetColor,
                style: 'dashed',
                label: 'T3'
            });
            this.annotationManager.addHorizontalLine(pattern.targets.stopLoss, {
                color: '#ff0000',
                style: 'dashed',
                label: 'SL'
            });
        }

        // Add pattern label
        // (would need text annotation support in AnnotationManager)
    }

    /**
     * Get pattern information
     */
    getPatternInfo(pattern) {
        const { X, A, B, C, D } = pattern.points;

        return {
            type: pattern.name,
            direction: pattern.bullish ? 'Bullish' : 'Bearish',
            points: {
                X: { price: X.price, time: X.timestamp },
                A: { price: A.price, time: A.timestamp },
                B: { price: B.price, time: B.timestamp },
                C: { price: C.price, time: C.timestamp },
                D: { price: D.price, time: D.timestamp }
            },
            prz: pattern.prz,
            targets: pattern.targets,
            ratios: this.calculateActualRatios(X, A, B, C, D)
        };
    }

    calculateActualRatios(X, A, B, C, D) {
        const XA = Math.abs(A.price - X.price);
        const AB = Math.abs(B.price - A.price);
        const BC = Math.abs(C.price - B.price);
        const CD = Math.abs(D.price - C.price);
        const AD = Math.abs(D.price - A.price);

        return {
            AB_XA: (AB / XA).toFixed(3),
            BC_AB: (BC / AB).toFixed(3),
            CD_BC: (CD / BC).toFixed(3),
            AD_XA: (AD / XA).toFixed(3)
        };
    }

    /**
     * Clear all harmonic pattern annotations
     */
    clearPatterns() {
        this.detectedPatterns = [];
        // Would need to track annotation IDs to remove specific ones
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { HarmonicPatternDetector, HarmonicPatternAnnotation };
}
