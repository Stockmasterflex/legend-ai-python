/**
 * AI assistant resource
 */

import type { AxiosInstance } from 'axios';
import type { AIChatRequest, AIAnalyzeRequest, AIResponse } from '../types';

export class AIResource {
  constructor(private client: AxiosInstance) {}

  /**
   * Chat with AI trading assistant
   *
   * @param message - Your message/question
   * @param options - Chat options
   * @returns AI response
   */
  async chat(message: string, options: Omit<AIChatRequest, 'message'> = {}): Promise<AIResponse> {
    const response = await this.client.post('/api/ai/chat', {
      message,
      ...options,
    });
    return response.data;
  }

  /**
   * Get AI-powered stock analysis
   *
   * @param symbol - Stock ticker symbol
   * @returns Analysis
   */
  async analyze(symbol: string): Promise<Record<string, any>> {
    const response = await this.client.post('/api/ai/analyze', { symbol });
    return response.data;
  }
}
