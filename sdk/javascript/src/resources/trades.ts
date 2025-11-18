/**
 * Trade management resource
 */

import type { AxiosInstance } from 'axios';
import type { CreateTradeRequest } from '../types';

export class TradesResource {
  constructor(private client: AxiosInstance) {}

  /**
   * Create a new trade entry
   */
  async create(request: CreateTradeRequest): Promise<{ trade_id: number }> {
    const response = await this.client.post('/api/trades/create', request);
    return response.data;
  }
}
