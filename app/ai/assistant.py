"""
AI Financial Assistant - Conversational AI for Trading
Beats Intellectia's AI agent with GPT-4 + RAG architecture
Enhanced with Natural Language Queries, Smart Suggestions, Learning Mode, and Voice Commands
"""
import os
import logging
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import json
import random

# Check if openai is available
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    AsyncOpenAI = None

from app.services.market_data import MarketDataService
from app.detectors.advanced.patterns import AdvancedPatternDetector, PatternType
from app.technicals.trendlines import AutoTrendlineDetector
from app.technicals.fibonacci import FibonacciCalculator

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


# Natural Language Query Patterns
NL_QUERY_PATTERNS = {
    'show_patterns': r'(show|find|get|list|display)\s+(?:me\s+)?(\w+)\s+patterns?\s*(today|this week|now)?',
    'stock_status': r'(what\'?s|how\'?s|show|analyze)\s+([A-Z]{1,5})\s+(doing|looking|status)?',
    'find_breakouts': r'(find|show|get|list)\s+(\w+\s+)?breakouts?',
    'compare': r'compare\s+([A-Z]{1,5})\s+(?:vs|and|to)\s+([A-Z]{1,5})',
    'entry_timing': r'(when|entry|timing)\s+(should|to|for)\s+(enter|buy)\s+([A-Z]{1,5})',
    'pattern_explanation': r'(explain|what is|teach|learn)\s+(.+?)\s+pattern',
    'best_stocks': r'(best|top|good)\s+(\w+\s+)?(?:stocks?|tickers?)',
    'voice_command': r'^(show|find|compare|analyze|explain)\s+',
}


class QueryIntent:
    """Detected intent from natural language query"""
    def __init__(
        self,
        intent_type: str,
        entities: Dict[str, Any],
        confidence: float,
        original_query: str
    ):
        self.intent_type = intent_type
        self.entities = entities
        self.confidence = confidence
        self.original_query = original_query


class AIFinancialAssistant:
    """
    Conversational AI Financial Assistant
    Uses GPT-4/Claude/Gemini via OpenRouter (or direct OpenAI) + RAG

    Cost-optimized: Uses OpenRouter by default (3-10x cheaper than direct OpenAI!)
    """

    def __init__(
        self,
        model: Optional[str] = None,
        temperature: float = 0.7
    ):
        if not OPENAI_AVAILABLE:
            raise ImportError("openai package not installed. Run: pip install openai")

        # Check for OpenRouter first (cheaper!)
        openrouter_key = os.getenv("OPENROUTER_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")

        if openrouter_key:
            # Use OpenRouter (MUCH cheaper!)
            self.client = AsyncOpenAI(
                api_key=openrouter_key,
                base_url="https://openrouter.ai/api/v1"
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

    def parse_natural_language_query(self, query: str) -> Optional[QueryIntent]:
        """
        Parse natural language query to detect intent and extract entities

        Examples:
        - "Show me VCP patterns today" -> show_patterns intent, VCP entity
        - "What's AAPL doing?" -> stock_status intent, AAPL entity
        - "Find tech breakouts" -> find_breakouts intent, tech sector entity
        - "Compare NVDA vs AMD" -> compare intent, [NVDA, AMD] entities
        """
        query_lower = query.lower()

        # Try to match each pattern
        for intent_name, pattern in NL_QUERY_PATTERNS.items():
            match = re.search(pattern, query_lower, re.IGNORECASE)
            if match:
                entities = {}

                if intent_name == 'show_patterns':
                    entities['pattern_type'] = match.group(2).upper()
                    entities['timeframe'] = match.group(3) if match.group(3) else 'today'

                elif intent_name == 'stock_status':
                    entities['symbol'] = match.group(2).upper()

                elif intent_name == 'find_breakouts':
                    sector = match.group(2).strip() if match.group(2) else None
                    entities['sector'] = sector

                elif intent_name == 'compare':
                    entities['symbols'] = [match.group(1).upper(), match.group(2).upper()]

                elif intent_name == 'entry_timing':
                    entities['symbol'] = match.group(4).upper()

                elif intent_name == 'pattern_explanation':
                    entities['pattern_name'] = match.group(2).strip()

                elif intent_name == 'best_stocks':
                    sector = match.group(2).strip() if match.group(2) else None
                    entities['sector'] = sector

                return QueryIntent(
                    intent_type=intent_name,
                    entities=entities,
                    confidence=0.85,
                    original_query=query
                )

        # No pattern matched, return None (will fallback to general chat)
        return None

    async def find_similar_setups(
        self,
        reference_symbol: str,
        top_n: int = 5
    ) -> Dict[str, Any]:
        """
        Find stocks with similar technical setups to the reference symbol

        Args:
            reference_symbol: Reference stock ticker
            top_n: Number of similar stocks to return

        Returns:
            Dict with similar stocks and their similarity scores
        """
        try:
            # Get reference stock data and patterns
            ref_df = await self.market_data.get_price_data(
                symbol=reference_symbol,
                period="3mo",
                interval="1d"
            )

            if ref_df is None or ref_df.empty:
                return {"error": f"Could not fetch data for {reference_symbol}"}

            # Detect patterns on reference stock
            ref_patterns = self.pattern_detector.detect_all_patterns(ref_df)

            if not ref_patterns:
                return {
                    "reference_symbol": reference_symbol,
                    "similar_stocks": [],
                    "message": "No patterns detected on reference stock"
                }

            # Get the top pattern from reference
            top_ref_pattern = ref_patterns[0]

            # Common stock universe to search (you can expand this)
            search_universe = [
                "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "AMD",
                "CRM", "ADBE", "NFLX", "DIS", "PYPL", "INTC", "CSCO", "ORCL",
                "QCOM", "TXN", "AVGO", "NOW", "SNOW", "DDOG", "CRWD", "ZS"
            ]

            # Remove reference symbol from search
            search_universe = [s for s in search_universe if s != reference_symbol]

            similar_stocks = []

            # Search for similar patterns (simplified - in production, use parallel processing)
            for symbol in search_universe[:15]:  # Limit to avoid rate limits
                try:
                    df = await self.market_data.get_price_data(
                        symbol=symbol,
                        period="3mo",
                        interval="1d"
                    )

                    if df is None or df.empty:
                        continue

                    patterns = self.pattern_detector.detect_all_patterns(df)

                    # Check if any pattern matches the reference pattern type
                    for pattern in patterns:
                        if pattern.pattern_type == top_ref_pattern.pattern_type:
                            similar_stocks.append({
                                "symbol": symbol,
                                "pattern": pattern.pattern_type.value,
                                "confidence": pattern.confidence,
                                "similarity_score": min(pattern.confidence / 100, 1.0),
                                "description": pattern.description
                            })
                            break

                except Exception as e:
                    logger.warning(f"Error analyzing {symbol}: {e}")
                    continue

            # Sort by similarity score
            similar_stocks.sort(key=lambda x: x['similarity_score'], reverse=True)

            return {
                "reference_symbol": reference_symbol,
                "reference_pattern": top_ref_pattern.pattern_type.value,
                "similar_stocks": similar_stocks[:top_n],
                "total_found": len(similar_stocks)
            }

        except Exception as e:
            logger.error(f"Error finding similar setups: {e}")
            return {
                "reference_symbol": reference_symbol,
                "error": str(e)
            }

    async def suggest_entry_timing(self, symbol: str) -> Dict[str, Any]:
        """
        Suggest optimal entry timing for a stock based on technical analysis

        Args:
            symbol: Stock ticker

        Returns:
            Dict with entry timing suggestions
        """
        try:
            df = await self.market_data.get_price_data(
                symbol=symbol,
                period="3mo",
                interval="1d"
            )

            if df is None or df.empty:
                return {"error": f"Could not fetch data for {symbol}"}

            current_price = df.iloc[-1]['close']

            # Detect patterns and trendlines
            patterns = self.pattern_detector.detect_all_patterns(df)
            trendlines = self.trendline_detector.detect_all_trendlines(df, lookback_period=100)

            # Find nearest support/resistance
            supports = trendlines['support']
            resistances = trendlines['resistance']

            nearest_support = None
            nearest_resistance = None

            if supports:
                support_prices = [s.get_price_at_index(len(df) - 1) for s in supports]
                nearest_support = min(support_prices, key=lambda x: abs(x - current_price))

            if resistances:
                resistance_prices = [r.get_price_at_index(len(df) - 1) for r in resistances]
                nearest_resistance = min(resistance_prices, key=lambda x: abs(x - current_price))

            # Calculate risk/reward
            if nearest_support and nearest_resistance:
                potential_reward = nearest_resistance - current_price
                potential_risk = current_price - nearest_support
                risk_reward = potential_reward / potential_risk if potential_risk > 0 else 0
            else:
                risk_reward = None

            # Generate suggestions
            suggestions = []

            if patterns:
                top_pattern = patterns[0]
                if top_pattern.confidence > 70:
                    suggestions.append({
                        "type": "pattern_based",
                        "message": f"Strong {top_pattern.pattern_type.value} pattern detected",
                        "action": "Consider entry on confirmation",
                        "entry_price": top_pattern.entry_price if hasattr(top_pattern, 'entry_price') else current_price,
                        "stop_loss": top_pattern.stop_loss if hasattr(top_pattern, 'stop_loss') else nearest_support,
                        "target": top_pattern.target_price if hasattr(top_pattern, 'target_price') else nearest_resistance
                    })

            if nearest_support:
                distance_to_support = ((current_price - nearest_support) / current_price) * 100
                if distance_to_support < 3:
                    suggestions.append({
                        "type": "support_bounce",
                        "message": f"Price near support at ${nearest_support:.2f}",
                        "action": "Watch for bounce confirmation",
                        "entry_price": nearest_support,
                        "stop_loss": nearest_support * 0.98,
                        "risk_reward": risk_reward
                    })

            if nearest_resistance:
                distance_to_resistance = ((nearest_resistance - current_price) / current_price) * 100
                if distance_to_resistance < 2:
                    suggestions.append({
                        "type": "breakout_setup",
                        "message": f"Price approaching resistance at ${nearest_resistance:.2f}",
                        "action": "Wait for breakout above resistance",
                        "entry_price": nearest_resistance * 1.01,
                        "stop_loss": nearest_support,
                        "target": nearest_resistance + (nearest_resistance - current_price)
                    })

            return {
                "symbol": symbol,
                "current_price": current_price,
                "suggestions": suggestions,
                "support_level": nearest_support,
                "resistance_level": nearest_resistance,
                "risk_reward_ratio": risk_reward,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error suggesting entry timing for {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": str(e)
            }

    async def chat(
        self,
        user_message: str,
        symbol: Optional[str] = None,
        include_market_data: bool = True,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Chat with the AI assistant - Enhanced with Natural Language Understanding

        Args:
            user_message: User's question or message
            symbol: Optional stock symbol for context
            include_market_data: Whether to fetch live market data for context
            conversation_id: Optional ID to maintain conversation history

        Returns:
            Dict with AI response and metadata
        """
        try:
            # Parse natural language query first
            intent = self.parse_natural_language_query(user_message)

            # Route to appropriate handler based on intent
            if intent:
                logger.info(f"Detected intent: {intent.intent_type} with entities: {intent.entities}")

                if intent.intent_type == 'stock_status':
                    # Direct stock analysis
                    symbol = intent.entities.get('symbol')
                    analysis = await self.analyze_stock(symbol)
                    return {
                        "response": analysis.get('analysis', ''),
                        "intent": intent.intent_type,
                        "symbol": symbol,
                        "timestamp": datetime.now().isoformat(),
                        "model": self.model
                    }

                elif intent.intent_type == 'compare':
                    # Stock comparison
                    symbols = intent.entities.get('symbols', [])
                    comparison = await self.compare_stocks(symbols)
                    return {
                        "response": comparison.get('comparison', ''),
                        "intent": intent.intent_type,
                        "symbols": symbols,
                        "timestamp": datetime.now().isoformat(),
                        "model": self.model
                    }

                elif intent.intent_type == 'pattern_explanation':
                    # Pattern education
                    pattern_name = intent.entities.get('pattern_name', '')
                    explanation = await self.explain_pattern(pattern_name)
                    return {
                        "response": explanation.get('explanation', ''),
                        "intent": intent.intent_type,
                        "pattern": pattern_name,
                        "timestamp": datetime.now().isoformat(),
                        "model": self.model
                    }

                elif intent.intent_type == 'entry_timing':
                    # Entry timing suggestion
                    symbol = intent.entities.get('symbol')
                    timing = await self.suggest_entry_timing(symbol)

                    # Format response nicely
                    if 'error' not in timing:
                        response_text = f"**Entry Timing Analysis for {symbol}**\n\n"
                        response_text += f"Current Price: ${timing['current_price']:.2f}\n\n"

                        if timing['suggestions']:
                            response_text += "**Suggestions:**\n"
                            for i, sug in enumerate(timing['suggestions'], 1):
                                response_text += f"\n{i}. {sug['message']}\n"
                                response_text += f"   - Action: {sug['action']}\n"
                                if sug.get('entry_price'):
                                    response_text += f"   - Entry: ${sug['entry_price']:.2f}\n"
                                if sug.get('stop_loss'):
                                    response_text += f"   - Stop: ${sug['stop_loss']:.2f}\n"
                                if sug.get('target'):
                                    response_text += f"   - Target: ${sug['target']:.2f}\n"
                        else:
                            response_text += "No clear entry setup at the moment. Wait for better technical confirmation."
                    else:
                        response_text = f"Error: {timing.get('error')}"

                    return {
                        "response": response_text,
                        "intent": intent.intent_type,
                        "symbol": symbol,
                        "data": timing,
                        "timestamp": datetime.now().isoformat(),
                        "model": self.model
                    }

            # No specific intent detected, fall back to general chat
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
                    )
                }
            ]

            # Add conversation history if available
            if self.conversation_history:
                messages.extend(self.conversation_history[-10:])  # Last 10 messages

            # Add context from market data
            if context:
                messages.append({
                    "role": "system",
                    "content": f"CURRENT MARKET DATA:\n{context}"
                })

            # Add user message
            messages.append({
                "role": "user",
                "content": user_message
            })

            # Call GPT-4
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=800
            )

            assistant_message = response.choices[0].message.content

            # Update conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            # Keep only last 20 messages to avoid token limits
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]

            return {
                "response": assistant_message,
                "symbol": symbol,
                "timestamp": datetime.now().isoformat(),
                "model": self.model,
                "context_included": bool(context),
                "conversation_id": conversation_id
            }

        except Exception as e:
            logger.error(f"AI Assistant error: {e}")
            return {
                "response": "I apologize, but I encountered an error processing your request. Please try again.",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
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
                    )
                },
                {
                    "role": "user",
                    "content": analysis_prompt
                }
            ]

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.5,  # Lower temperature for analysis
                max_tokens=1200
            )

            analysis = response.choices[0].message.content

            return {
                "symbol": symbol,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat(),
                "raw_data": json.loads(context) if context.startswith("{") else None
            }

        except Exception as e:
            logger.error(f"Stock analysis error for {symbol}: {e}")
            return {
                "symbol": symbol,
                "error": str(e),
                "analysis": "Unable to complete analysis at this time."
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
            context_text = "\n\n".join([
                f"=== {sym} ===\n{ctx}"
                for sym, ctx in contexts.items()
            ])

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
                    )
                },
                {
                    "role": "user",
                    "content": comparison_prompt
                }
            ]

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.6,
                max_tokens=1500
            )

            comparison = response.choices[0].message.content

            return {
                "symbols": symbols,
                "comparison": comparison,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Stock comparison error: {e}")
            return {
                "symbols": symbols,
                "error": str(e),
                "comparison": "Unable to complete comparison at this time."
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
                    )
                },
                {
                    "role": "user",
                    "content": explain_prompt
                }
            ]

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )

            explanation = response.choices[0].message.content

            return {
                "pattern": pattern_name,
                "explanation": explanation,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Pattern explanation error: {e}")
            return {
                "pattern": pattern_name,
                "error": str(e),
                "explanation": "Unable to provide explanation at this time."
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
                symbol=symbol,
                period="3mo",
                interval="1d"
            )

            if df is None or df.empty:
                return f"Unable to fetch data for {symbol}"

            # Current price info
            latest = df.iloc[-1]
            current_price = latest['close']
            prev_close = df.iloc[-2]['close'] if len(df) > 1 else current_price
            change = ((current_price - prev_close) / prev_close * 100)

            # Calculate indicators
            sma_20 = df['close'].tail(20).mean()
            sma_50 = df['close'].tail(50).mean() if len(df) >= 50 else None
            sma_200 = df['close'].tail(200).mean() if len(df) >= 200 else None

            rsi = None
            if len(df) >= 14:
                delta = df['close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi = (100 - (100 / (1 + rs))).iloc[-1]

            # Detect patterns
            patterns = self.pattern_detector.detect_all_patterns(df)
            top_patterns = patterns[:5]  # Top 5 patterns

            # Detect trendlines
            trendlines = self.trendline_detector.detect_all_trendlines(df, lookback_period=100)
            top_support = trendlines['support'][:2]
            top_resistance = trendlines['resistance'][:2]

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
            returns = df['close'].pct_change().tail(20)
            volatility = returns.std() * np.sqrt(252) * 100  # Annualized
            context += f"\n\n**Volatility:** {volatility:.1f}% (annualized, 20-day)"

            # Volume analysis
            avg_volume = df['volume'].tail(20).mean()
            latest_volume = latest['volume']
            volume_ratio = latest_volume / avg_volume

            context += f"\n\n**Volume:**"
            context += f"\n- Latest: {latest_volume:,.0f}"
            context += f"\n- 20-day avg: {avg_volume:,.0f}"
            context += f"\n- Ratio: {volume_ratio:.2f}x {'(High)' if volume_ratio > 1.5 else '(Normal)' if volume_ratio > 0.7 else '(Low)'}"

            return context.strip()

        except Exception as e:
            logger.error(f"Error building market context for {symbol}: {e}")
            return f"Error gathering data for {symbol}: {str(e)}"

    async def generate_pattern_quiz(self, difficulty: str = "medium") -> Dict[str, Any]:
        """
        Generate an interactive quiz about chart patterns

        Args:
            difficulty: Quiz difficulty - "easy", "medium", or "hard"

        Returns:
            Dict with quiz questions
        """
        try:
            # Define quiz questions by difficulty
            questions_pool = {
                "easy": [
                    {
                        "question": "What is a VCP pattern?",
                        "options": [
                            "A) Volatility Contraction Pattern",
                            "B) Volume Change Pattern",
                            "C) Vertical Cup Pattern",
                            "D) Value Comparison Pattern"
                        ],
                        "correct": 0,
                        "explanation": "VCP stands for Volatility Contraction Pattern, developed by Mark Minervini. It shows decreasing volatility in price consolidations."
                    },
                    {
                        "question": "In a Cup and Handle pattern, what does the 'handle' represent?",
                        "options": [
                            "A) Final breakout point",
                            "B) A final shakeout before breakout",
                            "C) The highest price point",
                            "D) The lowest price point"
                        ],
                        "correct": 1,
                        "explanation": "The handle is a small consolidation or pullback that forms after the cup, serving as a final shakeout before the breakout."
                    }
                ],
                "medium": [
                    {
                        "question": "What is the typical success rate of a well-formed Ascending Triangle pattern?",
                        "options": [
                            "A) 40-50%",
                            "B) 60-70%",
                            "C) 75-85%",
                            "D) 90-95%"
                        ],
                        "correct": 1,
                        "explanation": "Ascending triangles have a success rate of around 60-70% when properly identified with good volume confirmation."
                    },
                    {
                        "question": "Where should you place a stop loss on a Bull Flag pattern?",
                        "options": [
                            "A) Above the flag's upper trendline",
                            "B) Below the flag's lower trendline",
                            "C) At the flag's midpoint",
                            "D) Below the flagpole"
                        ],
                        "correct": 1,
                        "explanation": "Stop loss should be placed just below the flag's lower trendline to protect against a failed breakout."
                    }
                ],
                "hard": [
                    {
                        "question": "In a Head and Shoulders pattern, what confirms the pattern completion?",
                        "options": [
                            "A) Formation of the right shoulder",
                            "B) Break below the neckline on increased volume",
                            "C) Price reaching the head's level",
                            "D) Equal heights of both shoulders"
                        ],
                        "correct": 1,
                        "explanation": "A Head and Shoulders pattern is confirmed only when price breaks below the neckline on increased volume."
                    },
                    {
                        "question": "What is the measured move target for a Symmetrical Triangle breakout?",
                        "options": [
                            "A) Height of the triangle added to breakout point",
                            "B) Widest part of triangle added to breakout point",
                            "C) 50% of triangle height added to breakout",
                            "D) No standard target"
                        ],
                        "correct": 1,
                        "explanation": "The measured move is the widest part (height) of the triangle, projected from the breakout point in the direction of the breakout."
                    }
                ]
            }

            # Get questions for the specified difficulty
            questions = questions_pool.get(difficulty, questions_pool["medium"])

            # Shuffle and select 3-5 questions
            selected_questions = random.sample(questions, min(len(questions), 3))

            return {
                "quiz_type": "pattern_recognition",
                "difficulty": difficulty,
                "questions": selected_questions,
                "total_questions": len(selected_questions),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error generating quiz: {e}")
            return {
                "error": str(e),
                "quiz_type": "pattern_recognition"
            }

    async def get_strategy_tutorial(self, strategy: str) -> Dict[str, Any]:
        """
        Get detailed tutorial on a trading strategy

        Args:
            strategy: Strategy name (e.g., "breakout", "pullback", "reversal")

        Returns:
            Dict with tutorial content
        """
        try:
            tutorials = {
                "breakout": {
                    "title": "Breakout Trading Strategy",
                    "overview": "Breakout trading involves entering positions when price breaks through key resistance or support levels.",
                    "steps": [
                        "1. Identify consolidation or trading range",
                        "2. Mark clear resistance level with at least 2-3 touches",
                        "3. Wait for volume spike (1.5x average) on breakout",
                        "4. Enter when price closes above resistance",
                        "5. Place stop below recent consolidation low",
                        "6. Target: 2-3x the risk (2:1 or 3:1 R:R)"
                    ],
                    "rules": [
                        "Never chase - wait for confirmation",
                        "Volume must increase on breakout",
                        "Avoid breakouts on low volume",
                        "Check overall market trend",
                        "Use 1-2% position sizing"
                    ],
                    "example": "AAPL breaks $150 resistance on 2x volume after 3-week consolidation. Entry: $150.50, Stop: $147 (below consolidation), Target: $157 (2:1 R:R)"
                },
                "pullback": {
                    "title": "Pullback Trading Strategy",
                    "overview": "Trading pullbacks to moving averages in an established uptrend.",
                    "steps": [
                        "1. Identify strong uptrend (price above 50-day MA)",
                        "2. Wait for pullback to key MA (20, 50, or 200-day)",
                        "3. Look for reversal candlesticks at MA",
                        "4. Enter when price bounces with volume",
                        "5. Stop below the MA or swing low",
                        "6. Target: Previous high or resistance"
                    ],
                    "rules": [
                        "Only trade in direction of trend",
                        "Pullback should be 5-15% max",
                        "Watch for volume drying up on pullback",
                        "Increased volume on bounce is bullish",
                        "Avoid catching falling knives"
                    ],
                    "example": "NVDA in uptrend pulls back to 50-day MA at $480. Hammer candle forms. Entry: $485 on bounce, Stop: $475 (below MA), Target: $510 (previous high)"
                },
                "vcp": {
                    "title": "Volatility Contraction Pattern (VCP)",
                    "overview": "Mark Minervini's VCP strategy - trading stocks showing tightening price action before breakout.",
                    "steps": [
                        "1. Identify stock in Stage 2 uptrend",
                        "2. Look for 3-4 contractions (T1, T2, T3)",
                        "3. Each pullback should be shallower than previous",
                        "4. Volume should decrease on each pullback",
                        "5. Enter on volume breakout above pivot",
                        "6. Stop at T3 low or 7-8% max"
                    ],
                    "rules": [
                        "Stock must be above 200-day MA",
                        "Relative strength should be strong",
                        "Minimum 3 contractions required",
                        "Volume contraction is critical",
                        "Buy on first green day above pivot"
                    ],
                    "example": "TSLA consolidates 3 times: T1 (-12%), T2 (-8%), T3 (-4%). Volume decreases each time. Breakout at $250 on 3x volume. Entry: $251, Stop: $230"
                }
            }

            tutorial = tutorials.get(strategy.lower())

            if not tutorial:
                # Use AI to generate custom tutorial
                prompt = f"""Create a comprehensive tutorial on the {strategy} trading strategy.

Include:
1. Overview
2. Step-by-step execution
3. Key rules
4. Example trade

Make it practical and educational."""

                messages = [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT.format(current_date=datetime.now().strftime("%Y-%m-%d"))
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]

                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000
                )

                tutorial = {
                    "title": f"{strategy.title()} Trading Strategy",
                    "content": response.choices[0].message.content,
                    "generated": True
                }

            return {
                "strategy": strategy,
                "tutorial": tutorial,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error getting tutorial: {e}")
            return {
                "strategy": strategy,
                "error": str(e)
            }

    async def teach_entry_rules(self, pattern: str) -> Dict[str, Any]:
        """
        Teach specific entry rules for a chart pattern

        Args:
            pattern: Chart pattern name

        Returns:
            Dict with entry rules and examples
        """
        try:
            entry_rules = {
                "Cup and Handle": {
                    "entry_point": "Buy when price breaks above the handle's resistance on increased volume",
                    "confirmation": [
                        "Price closes above handle high",
                        "Volume 40-50% above average",
                        "Handle should be in upper half of cup",
                        "Cup depth ideally 12-30%"
                    ],
                    "stop_loss": "Place stop just below handle low (typically 7-8% from entry)",
                    "target": "Depth of cup added to breakout point",
                    "example": "Cup: $40-$50-$45, Handle: $50-$48. Entry: $50.20, Stop: $46.50, Target: $60 (cup depth $10)"
                },
                "VCP": {
                    "entry_point": "Buy on first green day above pivot point with volume surge",
                    "confirmation": [
                        "At least 3 contractions (T1, T2, T3)",
                        "Each contraction shallower than previous",
                        "Volume decreases in each pullback",
                        "Volume spike on breakout (2x average)"
                    ],
                    "stop_loss": "7-8% below entry or below T3 low",
                    "target": "Initial target: depth of T1 added to breakout",
                    "example": "T1: -10%, T2: -6%, T3: -3%. Pivot at $100. Entry: $100.50 on volume, Stop: $92.50, Target: $110"
                },
                "Ascending Triangle": {
                    "entry_point": "Buy when price breaks above flat resistance on volume",
                    "confirmation": [
                        "At least 2-3 touches of resistance",
                        "Higher lows forming support trendline",
                        "Volume contraction during formation",
                        "Volume expansion on breakout"
                    ],
                    "stop_loss": "Below the most recent higher low",
                    "target": "Height of triangle added to breakout point",
                    "example": "Resistance at $50, triangle height $5. Entry: $50.50, Stop: $47, Target: $55"
                }
            }

            rules = entry_rules.get(pattern)

            if not rules:
                # Generate AI-based rules
                prompt = f"""Provide detailed entry rules for the {pattern} chart pattern.

Include:
1. Exact entry point
2. Confirmation signals (3-4 points)
3. Stop loss placement
4. Price target calculation
5. Specific example with numbers

Be precise and practical."""

                messages = [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT.format(current_date=datetime.now().strftime("%Y-%m-%d"))
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]

                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.5,
                    max_tokens=800
                )

                rules = {
                    "content": response.choices[0].message.content,
                    "generated": True
                }

            return {
                "pattern": pattern,
                "entry_rules": rules,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error teaching entry rules: {e}")
            return {
                "pattern": pattern,
                "error": str(e)
            }

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


# Import numpy for volatility calculation
import numpy as np
