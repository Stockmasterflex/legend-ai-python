/**
 * Universe scanning resource
 */

import type { AxiosInstance } from 'axios';
import type { UniverseScanRequest, UniverseScanResponse, ScanResult } from '../types';

export class UniverseResource {
  constructor(private client: AxiosInstance) {}

  /**
   * Scan market universe for patterns
   *
   * @param options - Scan options
   * @returns Scan results
   *
   * @example
   * ```typescript
   * const results = await client.universe.scan({
   *   universe: 'SP500',
   *   min_score: 8.0,
   *   max_results: 10
   * });
   * ```
   */
  async scan(options: UniverseScanRequest = {}): Promise<ScanResult[]> {
    const response = await this.client.post<UniverseScanResponse>('/api/universe/scan', {
      universe: options.universe || 'SP500',
      min_score: options.min_score || 7.0,
      max_results: options.max_results || 20,
      pattern_types: options.pattern_types,
    });
    return response.data.results;
  }

  /**
   * Get list of tickers in universe
   */
  async getTickers(universe: string = 'SP500'): Promise<string[]> {
    const response = await this.client.get(`/api/universe/tickers?universe=${universe}`);
    return response.data.tickers;
  }
}
