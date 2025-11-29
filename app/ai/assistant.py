"""
AI Financial Assistant - Conversational AI for Trading
Beats Intellectia's AI agent with GPT-4 + RAG architecture
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

# Check if openai is available
try:
    from openai import AsyncOpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    AsyncOpenAI = None

from app.detectors.advanced.patterns import AdvancedPatternDetector
from app.services.market_data import MarketDataService
from app.technicals.fibonacci import FibonacciCalculator
from app.technicals.trendlines import AutoTrendlineDetector

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are Legend AI, an expert financial assistant and trading advisor with deep knowledge of:
- Technical analysis (chart patterns, indicators, trendlines)
- Fundamental analysis (company metrics, financials)
- Market psychology and sentiment
- Risk management and position sizing
- Trading strategies (day trading, swing trading, long-term investing)

You provide clear, actionable insights backed by data. You:
1. Answer questions with specific facts and numbers
2. Explain technical concepts in simple terms
3. Cite sources and data when giving recommendations
4. Always include risk warnings when appropriate
5. Help users make informed decisions without giving direct financial advice

Your responses are:
- Concise but thorough (2-4 paragraphs)
- Data-driven with specific metrics
- Educational and empowering
- Professional yet friendly

IMPORTANT DISCLAIMERS:
- You are an educational tool, not a registered financial advisor
- You don't guarantee returns or promise profits
- Users should do their own research and consult professionals
- Past performance doesn't guarantee future results

Current date: {current_date}
"""


class AIFinancialAssistant:
    """
    Conversational AI Financial Assistant
    Uses GPT-4/Claude/Gemini via OpenRouter (or direct OpenAI) + RAG

    Cost-optimized: Uses OpenRouter by default (3-10x cheaper than direct OpenAI!)
    """

    def __init__(self, model: Optional[str] = None, temperature: float = 0.7):
        if not OPENAI_AVAILABLE:
            raise ImportError("openai package not installed. Run: pip install openai")

        # Check for OpenRouter first (cheaper!)
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")

        if openrouter_key:
            # Use OpenRouter (MUCH cheaper!)
            self.client = AsyncOpenAI(
                api_key=openrouter_key, base_url="https://openrouter.ai/api/v1"
            )
            # Default to Claude 3.5 Sonnet (best value: ~$3/1M tokens)
            self.model = model or os.getenv("AI_MODEL", "anthropic/claude-3.5-sonnet")
            self.provider = "OpenRouter"
            logger.info(f"🤖 AI Assistant using OpenRouter with model: {self.model}")

        elif openai_key:
            # Fallback to direct OpenAI
            self.client = AsyncOpenAI(api_key=openai_key)
            self.model = model or "gpt-4-turbo-preview"
            self.provider = "OpenAI"
            logger.info(f"🤖 AI Assistant using OpenAI with model: {self.model}")

        else:
            raise ValueError(
                "No AI API key found! Set either:\n"
                "- OPENROUTER_API_KEY (recommended - cheaper)\n"
                "- OPENAI_API_KEY (fallback)"
            )

        self.temperature = temperature

        # Initialize analysis tools
        self.market_data = MarketDataService()
        self.pattern_detector = AdvancedPatternDetector(min_confidence=60.0)
        self.trendline_detector = AutoTrendlineDetector()
        self.fib_calculator = FibonacciCalculator()

        # Conversation history (session-based, should be stored per user)
        self.conversation_history: List[Dict] = []

    async def chat(
        self,
        user_message: str,
        symbol: Optional[str] = None,
        include_market_data: bool = True,
        conversation_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Chat with the AI assistant

        Args:
            user_message: User's question or message
            symbol: Optional stock symbol for context
            include_market_data: Whether to fetch live market data for context
            conversation_id: Optional ID to maintain conversation history

        Returns:
            Dict with AI response and metadata
        """
        try:
            # Build context from market data if symbol provided
            context = ""

            if symbol and include_market_data:
                context = await self._build_market_context(symbol)

            # Build messages for GPT-4
            messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT.format(
                        current_date=datetime.now().strftime("%Y-%m-%d")
                    ),
                }
            ]

            # Add conversation history if available
            if self.conversation_history:
                messages.extend(self.conversation_history[-10:])  # Last 10 messages

            # Add context from market data
            if context:
                messages.append(
                    {"role": "system", "content": f"CURRENT MARKET DATA:\n{context}"}
                )

            # Add user message
            messages.append({"role": "user", "content": user_message})

            # Call GPT-4
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=800,
            )

            assistant_message = response.choices[0].message.content

            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append(
                {"role": "assistant", "content": assistant_message}
            )

            # Keep only last 20 messages to avoid token limits
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]

            return {
                "response": assistant_message,
                "symbol": symbol,
                "timestamp": datetime.now().isoformat(),
                "model": self.model,
                "context_included": bool(context),
                "conversation_id": conversation_id,
            }

        except Exception as e:
            logger.error(f"AI Assistant error: {e}")
            return {
                "response": "I apologize, but I encountered an error processing your request. Please try again.",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    async def analyze_stock(self, symbol: str) -> Dict[str, Any]:
        """
        Comprehensive AI-powered stock analysis

        Args:
            symbol: Stock ticker

        Returns:
            Detailed analysis with AI insights
        """
        try:
            # Gather all analysis data
            context = await self._build_market_context(symbol)

            # Ask AI for comprehensive analysis
            analysis_prompt = f"""Provide a comprehensive analysis of {symbol} based on the following data:

{context}

Please structure your analysis with:
1. **Current Technical Setup** - What the charts are showing
2. **Key Levels** - Important support/resistance and price targets
3. **Pattern Analysis** - Detected patterns and their implications
4. **Risk Assessment** - Potential risks and risk management suggestions
5. **Trading Opportunities** - Potential entry/exit strategies (if any)
6. **Summary** - Overall outlook and recommendation

Be specific with price levels and percentages."""

            messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT.format(
                        current_date=datetime.now().strftime("%Y-%m-%d")
                    ),
                },
                {"role": "user", "content": analysis_prompt},
            ]

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.5,  # Lower temperature for analysis
                max_tokens=1200,
            )

            analysis = response.choices[0].message.content

            return {
                "symbol": symbol,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat(),
                "raw_data": json.loads(context) if context.startswith("{") else None,
            }

        except Exception as e:
            logger.error(f"Stock analysis error for {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": str(e),
                "analysis": "Unable to complete analysis at this time.",
            }

    async def compare_stocks(self, symbols: List[str]) -> Dict[str, Any]:
        """
        AI-powered comparison of multiple stocks

        Args:
            symbols: List of stock tickers to compare

        Returns:
            Comparative analysis
        """
        try:
            if len(symbols) < 2:
                return {"error": "Need at least 2 symbols to compare"}

            if len(symbols) > 5:
                return {"error": "Maximum 5 symbols can be compared at once"}

            # Gather data for all symbols
            contexts = {}
            for symbol in symbols:
                contexts[symbol] = await self._build_market_context(symbol)

            # Build comparison prompt
            context_text = "\n\n".join(
                [f"=== {sym} ===\n{ctx}" for sym, ctx in contexts.items()]
            )

            comparison_prompt = f"""Compare these stocks and recommend which one(s) offer the best risk/reward for:
1. Day trading
2. Swing trading
3. Long-term investing

{context_text}

For each stock, evaluate:
- Technical strength (trend, patterns, indicators)
- Risk level (volatility, recent patterns)
- Potential reward (price targets, pattern projections)
- Best trading timeframe

Conclude with a clear ranking and reasoning."""

            messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT.format(
                        current_date=datetime.now().strftime("%Y-%m-%d")
                    ),
                },
                {"role": "user", "content": comparison_prompt},
            ]

            response = await self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.6, max_tokens=1500
            )

            comparison = response.choices[0].message.content

            return {
                "symbols": symbols,
                "comparison": comparison,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Stock comparison error: {e}")
            return {
                "symbols": symbols,
                "error": str(e),
                "comparison": "Unable to complete comparison at this time.",
            }

    async def explain_pattern(self, pattern_name: str) -> Dict[str, Any]:
        """
        Explain a chart pattern in detail

        Args:
            pattern_name: Name of the pattern (e.g., "Cup and Handle")

        Returns:
            Educational explanation
        """
        try:
            explain_prompt = f"""Explain the "{pattern_name}" chart pattern in detail:

1. **What it is** - Visual description and how to identify it
2. **Psychology** - What market forces create this pattern
3. **How to trade it** - Entry points, stop loss placement, price targets
4. **Success rate** - Historical probability and reliability
5. **Example** - Describe a typical scenario
6. **Common mistakes** - What to watch out for

Make it educational but practical."""

            messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT.format(
                        current_date=datetime.now().strftime("%Y-%m-%d")
                    ),
                },
                {"role": "user", "content": explain_prompt},
            ]

            response = await self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.7, max_tokens=1000
            )

            explanation = response.choices[0].message.content

            return {
                "pattern": pattern_name,
                "explanation": explanation,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Pattern explanation error: {e}")
            return {
                "pattern": pattern_name,
                "error": str(e),
                "explanation": "Unable to provide explanation at this time.",
            }

    async def _build_market_context(self, symbol: str) -> str:
        """
        Build comprehensive market context for RAG

        Gathers:
        - Current price and recent performance
        - Detected patterns
        - Technical indicators
        - Trendlines and support/resistance
        - Fibonacci levels
        """
        try:
            # Fetch market data
            df = await self.market_data.get_price_data(
                symbol=symbol, period="3mo", interval="1d"
            )

            if df is None or df.empty:
                return f"Unable to fetch data for {symbol}"

            # Current price info
            latest = df.iloc[-1]
            current_price = latest["close"]
            prev_close = df.iloc[-2]["close"] if len(df) > 1 else current_price
            change = (current_price - prev_close) / prev_close * 100

            # Calculate indicators
            sma_20 = df["close"].tail(20).mean()
            sma_50 = df["close"].tail(50).mean() if len(df) >= 50 else None
            sma_200 = df["close"].tail(200).mean() if len(df) >= 200 else None

            rsi = None
            if len(df) >= 14:
                delta = df["close"].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = (100 - (100 / (1 + rs))).iloc[-1]

            # Detect patterns
            patterns = self.pattern_detector.detect_all_patterns(df)
            top_patterns = patterns[:5]  # Top 5 patterns

            # Detect trendlines
            trendlines = self.trendline_detector.detect_all_trendlines(
                df, lookback_period=100
            )
            top_support = trendlines["support"][:2]
            top_resistance = trendlines["resistance"][:2]

            # Calculate Fibonacci
            fib_levels = self.fib_calculator.calculate_auto_fibonacci(df, lookback=100)
            main_fib = fib_levels[0] if fib_levels else None

            # Build context string
            context = f"""
**{symbol} - Market Data Analysis**

**Current Price:** ${current_price:.2f} ({'+' if change > 0 else ''}{change:.2f}% from previous close)

**Moving Averages:**
- 20-day SMA: ${sma_20:.2f} (Price is {'above' if current_price > sma_20 else 'below'})
{f"- 50-day SMA: ${sma_50:.2f} (Price is {'above' if current_price > sma_50 else 'below'})" if sma_50 else ""}
{f"- 200-day SMA: ${sma_200:.2f} (Price is {'above' if current_price > sma_200 else 'below'})" if sma_200 else ""}

**Technical Indicators:**
{f"- RSI(14): {rsi:.1f} ({'Overbought' if rsi > 70 else 'Oversold' if rsi < 30 else 'Neutral'})" if rsi else "- RSI: Not enough data"}

**Detected Patterns (Top {len(top_patterns)}):**
"""

            for i, pattern in enumerate(top_patterns, 1):
                context += f"\n{i}. {pattern.pattern_type.value} - {pattern.confidence:.1f}% confidence"
                context += f"\n   {pattern.description}"
                if pattern.target_price:
                    context += f"\n   Target: ${pattern.target_price:.2f}"
                if pattern.stop_loss:
                    context += f"\n   Stop Loss: ${pattern.stop_loss:.2f}"

            if not top_patterns:
                context += "\n- No significant patterns detected above 60% confidence"

            context += "\n\n**Key Support Levels:**"
            for i, tl in enumerate(top_support, 1):
                current_level = tl.get_price_at_index(len(df) - 1)
                context += f"\n{i}. ${current_level:.2f} ({tl.strength:.0f}% strength, {tl.touches} touches)"

            if not top_support:
                context += "\n- No strong support trendlines detected"

            context += "\n\n**Key Resistance Levels:**"
            for i, tl in enumerate(top_resistance, 1):
                current_level = tl.get_price_at_index(len(df) - 1)
                context += f"\n{i}. ${current_level:.2f} ({tl.strength:.0f}% strength, {tl.touches} touches)"

            if not top_resistance:
                context += "\n- No strong resistance trendlines detected"

            if main_fib:
                context += f"\n\n**Fibonacci Levels ({main_fib.direction}):**"
                context += f"\n- Swing High: ${main_fib.swing_high:.2f}"
                context += f"\n- Swing Low: ${main_fib.swing_low:.2f}"

                nearest_support = main_fib._find_nearest_support()
                nearest_resistance = main_fib._find_nearest_resistance()

                if nearest_support:
                    context += f"\n- Nearest Support: ${nearest_support['price']:.2f} ({nearest_support['ratio']:.1%} Fib)"
                if nearest_resistance:
                    context += f"\n- Nearest Resistance: ${nearest_resistance['price']:.2f} ({nearest_resistance['ratio']:.1%} Fib)"

            # Recent volatility
            returns = df["close"].pct_change().tail(20)
            volatility = returns.std() * np.sqrt(252) * 100  # Annualized
            context += f"\n\n**Volatility:** {volatility:.1f}% (annualized, 20-day)"

            # Volume analysis
            avg_volume = df["volume"].tail(20).mean()
            latest_volume = latest["volume"]
            volume_ratio = latest_volume / avg_volume

            context += "\n\n**Volume:**"
            context += f"\n- Latest: {latest_volume:,.0f}"
            context += f"\n- 20-day avg: {avg_volume:,.0f}"
            context += f"\n- Ratio: {volume_ratio:.2f}x {'(High)' if volume_ratio > 1.5 else '(Normal)' if volume_ratio > 0.7 else '(Low)'}"

            return context.strip()

        except Exception as e:
            logger.error(f"Error building market context for {symbol}: {e}")
            return f"Error gathering data for {symbol}: {str(e)}"

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


# Import numpy for volatility calculation
import numpy as np
