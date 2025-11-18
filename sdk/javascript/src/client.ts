/**
 * Main client for Legend AI API
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import { APIError, RateLimitError, ValidationError } from './errors';
import { PatternsResource } from './resources/patterns';
import { ChartsResource } from './resources/charts';
import { UniverseResource } from './resources/universe';
import { AIResource } from './resources/ai';
import { WatchlistResource } from './resources/watchlist';
import { RiskResource } from './resources/risk';
import { TradesResource } from './resources/trades';
import { MarketResource } from './resources/market';
import type { HealthResponse, VersionResponse } from './types';

export interface LegendAIOptions {
  /** API key for authentication (optional) */
  apiKey?: string;
  /** Base URL for the API */
  baseURL?: string;
  /** Request timeout in milliseconds */
  timeout?: number;
}

/**
 * Legend AI API Client
 *
 * @example
 * ```typescript
 * const client = new LegendAI();
 * const pattern = await client.patterns.detect('AAPL');
 * console.log(pattern.score);
 * ```
 */
export class LegendAI {
  private client: AxiosInstance;

  /** Pattern detection resource */
  public readonly patterns: PatternsResource;
  /** Chart generation resource */
  public readonly charts: ChartsResource;
  /** Universe scanning resource */
  public readonly universe: UniverseResource;
  /** AI assistant resource */
  public readonly ai: AIResource;
  /** Watchlist management resource */
  public readonly watchlist: WatchlistResource;
  /** Risk management resource */
  public readonly risk: RiskResource;
  /** Trade tracking resource */
  public readonly trades: TradesResource;
  /** Market data resource */
  public readonly market: MarketResource;

  constructor(options: LegendAIOptions = {}) {
    const {
      apiKey,
      baseURL = 'https://legend-ai-python-production.up.railway.app',
      timeout = 30000,
    } = options;

    // Create axios instance
    this.client = axios.create({
      baseURL,
      timeout,
      headers: {
        'Content-Type': 'application/json',
        ...(apiKey && { 'X-API-Key': apiKey }),
      },
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response) {
          const status = error.response.status;
          const data = error.response.data as any;
          const message = data?.error || data?.detail || 'Unknown error';

          if (status === 429) {
            throw new RateLimitError(message);
          } else if (status === 400) {
            throw new ValidationError(message);
          } else {
            throw new APIError(`${status}: ${message}`);
          }
        }
        throw new APIError(error.message);
      }
    );

    // Initialize resources
    this.patterns = new PatternsResource(this.client);
    this.charts = new ChartsResource(this.client);
    this.universe = new UniverseResource(this.client);
    this.ai = new AIResource(this.client);
    this.watchlist = new WatchlistResource(this.client);
    this.risk = new RiskResource(this.client);
    this.trades = new TradesResource(this.client);
    this.market = new MarketResource(this.client);
  }

  /**
   * Get API health status
   */
  async health(): Promise<HealthResponse> {
    const response = await this.client.get<HealthResponse>('/health');
    return response.data;
  }

  /**
   * Get API version information
   */
  async version(): Promise<VersionResponse> {
    const response = await this.client.get<VersionResponse>('/api/version');
    return response.data;
  }
}
