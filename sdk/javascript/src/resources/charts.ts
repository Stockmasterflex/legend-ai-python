/**
 * Chart generation resource
 */

import type { AxiosInstance } from 'axios';
import type { ChartGenerateRequest, ChartGenerateResponse, ChartResult } from '../types';

export class ChartsResource {
  constructor(private client: AxiosInstance) {}

  /**
   * Generate a professional chart
   *
   * @param ticker - Stock ticker symbol
   * @param options - Chart options
   * @returns Chart generation result
   */
  async generate(
    ticker: string,
    options: Omit<ChartGenerateRequest, 'ticker'> = {}
  ): Promise<ChartResult> {
    const response = await this.client.post<ChartGenerateResponse>('/api/charts/generate', {
      ticker,
      ...options,
    });
    return {
      chart_url: response.data.chart_url,
      cached: response.data.cached,
      processing_time: response.data.processing_time,
    };
  }
}
