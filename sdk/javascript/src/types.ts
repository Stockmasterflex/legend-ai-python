/**
 * Type definitions for Legend AI SDK
 */

export interface PatternDetectRequest {
  ticker: string;
  interval?: '1day' | '1week' | '1hour' | '4hour';
  use_yahoo_fallback?: boolean;
}

export interface PatternResult {
  pattern: string;
  score: number;
  entry: number;
  stop: number;
  target: number;
  risk_reward_ratio: number;
  chart_url?: string;
  rs_rating?: number;
  criteria_met?: Record<string, any>;
}

export interface PatternDetectResponse {
  success: boolean;
  data: PatternResult;
  error?: string;
  cached: boolean;
  api_used?: string;
  processing_time?: number;
}

export interface ChartGenerateRequest {
  ticker: string;
  interval?: string;
  entry?: number;
  stop?: number;
  target?: number;
  indicators?: string[];
}

export interface ChartResult {
  chart_url: string;
  cached: boolean;
  processing_time?: number;
}

export interface ChartGenerateResponse {
  success: boolean;
  chart_url: string;
  error?: string;
  cached: boolean;
  processing_time?: number;
}

export interface UniverseScanRequest {
  universe?: 'SP500' | 'NASDAQ100' | 'CUSTOM';
  min_score?: number;
  max_results?: number;
  pattern_types?: string[];
}

export interface ScanResult {
  ticker: string;
  pattern: string;
  score: number;
  entry: number;
  stop: number;
  target: number;
  chart_url?: string;
}

export interface UniverseScanResponse {
  success: boolean;
  results: ScanResult[];
  total_scanned: number;
  total_found: number;
  cached: boolean;
}

export interface AIChatRequest {
  message: string;
  symbol?: string;
  include_market_data?: boolean;
  conversation_id?: string;
}

export interface AIResponse {
  response: string;
  conversation_id?: string;
  processing_time?: number;
}

export interface AIAnalyzeRequest {
  symbol: string;
}

export interface WatchlistItem {
  id: number;
  ticker: string;
  status: 'Watching' | 'Breaking Out' | 'Triggered' | 'Completed' | 'Skipped';
  target_entry?: number;
  target_stop?: number;
  reason?: string;
  added_at?: string;
}

export interface WatchlistAddRequest {
  ticker: string;
  user_id?: string;
  reason?: string;
  target_entry?: number;
  target_stop?: number;
}

export interface PositionSizeRequest {
  account_size: number;
  entry_price: number;
  stop_loss_price: number;
  target_price?: number;
  risk_percentage?: number;
}

export interface PositionSize {
  position_size: number;
  risk_amount: number;
  kelly_criterion?: number;
  breakeven?: number;
}

export interface CreateTradeRequest {
  ticker: string;
  entry_price: number;
  stop_loss: number;
  target_price?: number;
  position_size?: number;
  risk_amount?: number;
}

export interface MarketInternalsResponse {
  breadth: Record<string, any>;
  regime: 'bull' | 'bear' | 'neutral';
  advance_decline: Record<string, any>;
}

export interface HealthResponse {
  status: 'healthy' | 'degraded' | 'unhealthy';
  telegram: string;
  redis: string;
  version: string;
  universe: Record<string, any>;
  keys: Record<string, boolean>;
  issues: string[];
  warnings: string[];
}

export interface VersionResponse {
  version: string;
  build_sha: string;
  build_time: string;
}
