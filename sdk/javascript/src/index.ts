/**
 * Legend AI JavaScript/TypeScript SDK
 *
 * Professional SDK for the Legend AI Trading Pattern Scanner API
 *
 * @example
 * ```typescript
 * import { LegendAI } from '@legend-ai/sdk';
 *
 * const client = new LegendAI();
 * const pattern = await client.patterns.detect('AAPL');
 * console.log(`Pattern: ${pattern.pattern}, Score: ${pattern.score}`);
 * ```
 */

export { LegendAI } from './client';
export { LegendAIError, APIError, RateLimitError, ValidationError } from './errors';
export * from './types';
