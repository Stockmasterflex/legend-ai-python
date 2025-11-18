/**
 * Risk management resource
 */

import type { AxiosInstance } from 'axios';
import type { PositionSizeRequest, PositionSize } from '../types';

export class RiskResource {
  constructor(private client: AxiosInstance) {}

  /**
   * Calculate position size using 2% risk rule
   */
  async calculatePosition(request: PositionSizeRequest): Promise<PositionSize> {
    const response = await this.client.post<PositionSize>('/api/risk/calculate-position', {
      ...request,
      risk_percentage: request.risk_percentage || 2.0,
    });
    return response.data;
  }
}
