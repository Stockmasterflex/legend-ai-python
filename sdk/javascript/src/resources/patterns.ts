/**
 * Pattern detection resource
 */

import type { AxiosInstance } from 'axios';
import type { PatternDetectRequest, PatternDetectResponse, PatternResult } from '../types';

export class PatternsResource {
  constructor(private client: AxiosInstance) {}

  /**
   * Detect chart patterns for a ticker
   *
   * @param ticker - Stock ticker symbol (e.g., "AAPL")
   * @param options - Detection options
   * @returns Pattern detection result
   *
   * @example
   * ```typescript
   * const pattern = await client.patterns.detect('AAPL', {
   *   interval: '1day'
   * });
   * console.log(`Pattern: ${pattern.pattern}, Score: ${pattern.score}`);
   * ```
   */
  async detect(
    ticker: string,
    options: Omit<PatternDetectRequest, 'ticker'> = {}
  ): Promise<PatternResult> {
    const response = await this.client.post<PatternDetectResponse>('/api/patterns/detect', {
      ticker,
      interval: options.interval || '1day',
      use_yahoo_fallback: options.use_yahoo_fallback || false,
    });
    return response.data.data;
  }

  /**
   * Check pattern service health
   */
  async health(): Promise<Record<string, any>> {
    const response = await this.client.get('/api/patterns/health');
    return response.data;
  }
}
