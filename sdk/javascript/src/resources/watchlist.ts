/**
 * Watchlist resource
 */

import type { AxiosInstance } from 'axios';
import type { WatchlistItem, WatchlistAddRequest } from '../types';

export class WatchlistResource {
  constructor(private client: AxiosInstance) {}

  /**
   * Get all watchlist items
   */
  async list(userId: string = 'default'): Promise<WatchlistItem[]> {
    const response = await this.client.get(`/api/watchlist?user_id=${userId}`);
    return response.data.items;
  }

  /**
   * Add ticker to watchlist
   */
  async add(ticker: string, options: Omit<WatchlistAddRequest, 'ticker'> = {}): Promise<void> {
    await this.client.post('/api/watchlist/add', {
      ticker,
      user_id: options.user_id || 'default',
      ...options,
    });
  }

  /**
   * Remove ticker from watchlist
   */
  async remove(ticker: string, userId: string = 'default'): Promise<void> {
    await this.client.delete(`/api/watchlist/remove/${ticker}?user_id=${userId}`);
  }
}
