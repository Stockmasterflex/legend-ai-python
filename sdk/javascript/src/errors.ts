/**
 * Error classes for Legend AI SDK
 */

export class LegendAIError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'LegendAIError';
  }
}

export class APIError extends LegendAIError {
  constructor(message: string) {
    super(message);
    this.name = 'APIError';
  }
}

export class RateLimitError extends LegendAIError {
  constructor(message: string) {
    super(message);
    this.name = 'RateLimitError';
  }
}

export class ValidationError extends LegendAIError {
  constructor(message: string) {
    super(message);
    this.name = 'ValidationError';
  }
}
