/**
 * Market data resource
 */

import type { AxiosInstance } from 'axios';
import type { MarketInternalsResponse } from '../types';

export class MarketResource {
  constructor(private client: AxiosInstance) {}

  /**
   * Get market internals (breadth, advance/decline, regime)
   */
  async internals(): Promise<MarketInternalsResponse> {
    const response = await this.client.get<MarketInternalsResponse>('/api/market/internals');
    return response.data;
  }

  /**
   * Get market breadth metrics
   */
  async breadth(): Promise<Record<string, any>> {
    const response = await this.client.get('/api/market/breadth');
    return response.data;
  }

  /**
   * Get market regime classification
   */
  async regime(): Promise<Record<string, any>> {
    const response = await this.client.get('/api/market/regime');
    return response.data;
  }
}
