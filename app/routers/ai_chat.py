"""
AI Chat Router - Conversational AI Financial Assistant
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
import logging

from app.ai.assistant import AIFinancialAssistant

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ai", tags=["AI Assistant"])

# Initialize AI assistant (singleton pattern)
_ai_assistant: Optional[AIFinancialAssistant] = None


def get_ai_assistant() -> AIFinancialAssistant:
    """Get or create AI assistant instance"""
    global _ai_assistant
    if _ai_assistant is None:
        try:
            _ai_assistant = AIFinancialAssistant()
        except Exception as e:
            logger.error(f"Failed to initialize AI assistant: {e}")
            raise HTTPException(
                status_code=503,
                detail="AI Assistant is not available. Please check OPENAI_API_KEY configuration."
            )
    return _ai_assistant


class ChatRequest(BaseModel):
    """Chat request for AI assistant"""
    message: str = Field(..., description="User message or question", example="What are the best tech stocks right now?")
    symbol: Optional[str] = Field(None, description="Stock symbol for context (optional)", example="AAPL")
    include_market_data: bool = Field(True, description="Include live market data in context")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for history tracking")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Analyze TSLA for me",
                "symbol": "TSLA",
                "include_market_data": True,
                "conversation_id": None
            }
        }


class AnalyzeStockRequest(BaseModel):
    """Stock analysis request"""
    symbol: str = Field(..., description="Stock ticker symbol (e.g., AAPL, TSLA, NVDA)", example="AAPL")

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL"
            }
        }


class CompareStocksRequest(BaseModel):
    """Stock comparison request"""
    symbols: List[str] = Field(..., description="List of stock symbols (2-5)", example=["AAPL", "MSFT", "GOOGL"])

    class Config:
        json_schema_extra = {
            "example": {
                "symbols": ["AAPL", "MSFT", "GOOGL"]
            }
        }


class ExplainPatternRequest(BaseModel):
    """Pattern explanation request"""
    pattern_name: str = Field(..., description="Name of chart pattern to explain", example="Cup and Handle")

    class Config:
        json_schema_extra = {
            "example": {
                "pattern_name": "Cup and Handle"
            }
        }


@router.post("/chat",
             summary="Chat with AI Assistant",
             responses={
                 200: {
                     "description": "Successful chat response",
                     "content": {
                         "application/json": {
                             "example": {
                                 "response": "Based on current market data, here are the top tech stocks...",
                                 "symbol": None,
                                 "conversation_id": "conv_123"
                             }
                         }
                     }
                 }
             })
async def chat(request: ChatRequest):
    """
    🤖 **Chat with AI Financial Assistant**

    Have a conversation with an AI assistant that understands trading and markets.

    ## Capabilities

    - 💬 Answer trading questions
    - 📊 Analyze specific stocks with real-time data
    - 📚 Explain technical concepts and patterns
    - 🎓 Provide educational insights
    - 📈 Give market overview

    ## Example Usage

    **Python:**
    ```python
    import requests

    response = requests.post(
        'https://your-api.com/api/ai/chat',
        json={
            'message': 'What are the best tech stocks?',
            'include_market_data': True
        }
    )

    result = response.json()
    print(result['response'])
    ```

    **cURL:**
    ```bash
    curl -X POST "https://your-api.com/api/ai/chat" \\
      -H "Content-Type: application/json" \\
      -d '{
        "message": "Analyze TSLA for me",
        "symbol": "TSLA",
        "include_market_data": true
      }'
    ```

    **JavaScript:**
    ```javascript
    const response = await fetch('/api/ai/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        message: 'What are the best tech stocks?',
        include_market_data: true
      })
    });
    const result = await response.json();
    ```

    ## Tips

    - Include `symbol` for stock-specific questions
    - Set `include_market_data: true` for real-time insights
    - Use `conversation_id` to maintain context across messages

    ---

    **⚠️ Disclaimer:** Educational tool only, not financial advice.
    """
    try:
        assistant = get_ai_assistant()

        response = await assistant.chat(
            user_message=request.message,
            symbol=request.symbol,
            include_market_data=request.include_market_data,
            conversation_id=request.conversation_id
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze",
             summary="AI Stock Analysis",
             responses={
                 200: {
                     "description": "Comprehensive stock analysis",
                     "content": {
                         "application/json": {
                             "example": {
                                 "symbol": "AAPL",
                                 "analysis": "Apple (AAPL) is showing strong technical setup...",
                                 "pattern": "Bullish Flag",
                                 "score": 8.5,
                                 "recommendation": "Consider entry on pullback to support"
                             }
                         }
                     }
                 }
             })
async def analyze_stock(request: AnalyzeStockRequest):
    """
    📊 **Get Comprehensive AI Stock Analysis**

    Get a detailed AI-powered analysis of any stock.

    ## What You Get

    - 📈 Technical setup and trend analysis
    - 🎯 Pattern detection and interpretation
    - 💪 Key support/resistance levels
    - ⚖️ Risk assessment
    - 💡 Potential trading opportunities
    - 🎓 Educational insights

    ## Example Usage

    **Python:**
    ```python
    import requests

    response = requests.post(
        'https://your-api.com/api/ai/analyze',
        json={'symbol': 'AAPL'}
    )

    analysis = response.json()
    print(analysis['analysis'])
    ```

    **cURL:**
    ```bash
    curl -X POST "https://your-api.com/api/ai/analyze" \\
      -H "Content-Type: application/json" \\
      -d '{"symbol": "AAPL"}'
    ```

    **JavaScript:**
    ```javascript
    const response = await fetch('/api/ai/analyze', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({symbol: 'AAPL'})
    });
    const analysis = await response.json();
    ```

    ## Response Format

    Returns comprehensive analysis including:
    - Current technical setup
    - Pattern identification
    - Entry/exit suggestions
    - Risk/reward assessment
    - Market context
    """
    try:
        assistant = get_ai_assistant()

        analysis = await assistant.analyze_stock(request.symbol)

        return analysis

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis error for {request.symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare")
async def compare_stocks(request: CompareStocksRequest):
    """
    AI-powered comparison of multiple stocks

    Compare up to 5 stocks across:
    - Technical strength
    - Pattern quality
    - Risk/reward ratio
    - Best trading timeframe

    **Example:**
    ```json
    {
        "symbols": ["AAPL", "MSFT", "GOOGL"]
    }
    ```
    """
    try:
        if len(request.symbols) < 2:
            raise HTTPException(
                status_code=400,
                detail="Need at least 2 symbols to compare"
            )

        if len(request.symbols) > 5:
            raise HTTPException(
                status_code=400,
                detail="Maximum 5 symbols can be compared at once"
            )

        assistant = get_ai_assistant()

        comparison = await assistant.compare_stocks(request.symbols)

        return comparison

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Comparison error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain-pattern")
async def explain_pattern(request: ExplainPatternRequest):
    """
    Get detailed explanation of a chart pattern

    Learn about:
    - Pattern identification
    - Market psychology
    - Trading strategies
    - Success rates
    - Common pitfalls

    **Example:**
    ```json
    {
        "pattern_name": "Cup and Handle"
    }
    ```
    """
    try:
        assistant = get_ai_assistant()

        explanation = await assistant.explain_pattern(request.pattern_name)

        return explanation

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Pattern explanation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clear-history")
async def clear_conversation_history():
    """
    Clear conversation history

    Useful to start a fresh conversation
    """
    try:
        assistant = get_ai_assistant()
        assistant.clear_history()

        return {"message": "Conversation history cleared"}

    except Exception as e:
        logger.error(f"Clear history error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def ai_status():
    """Check AI assistant availability"""
    try:
        assistant = get_ai_assistant()
        return {
            "status": "operational",
            "model": assistant.model,
            "features": [
                "conversational_chat",
                "stock_analysis",
                "stock_comparison",
                "pattern_education",
                "natural_language_queries",
                "smart_suggestions",
                "learning_mode",
                "voice_commands"
            ]
        }
    except Exception as e:
        return {
            "status": "unavailable",
            "error": str(e)
        }


# New Enhanced Endpoints

class SimilarSetupsRequest(BaseModel):
    """Request for finding similar stock setups"""
    reference_symbol: str = Field(..., description="Reference stock ticker", example="AAPL")
    top_n: int = Field(5, description="Number of similar stocks to return", example=5, ge=1, le=20)

    class Config:
        json_schema_extra = {
            "example": {
                "reference_symbol": "AAPL",
                "top_n": 5
            }
        }


class EntryTimingRequest(BaseModel):
    """Request for entry timing suggestions"""
    symbol: str = Field(..., description="Stock ticker symbol", example="TSLA")

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "TSLA"
            }
        }


class PatternQuizRequest(BaseModel):
    """Request for pattern quiz"""
    difficulty: str = Field("medium", description="Quiz difficulty", example="medium")

    class Config:
        json_schema_extra = {
            "example": {
                "difficulty": "medium"
            }
        }


class StrategyTutorialRequest(BaseModel):
    """Request for strategy tutorial"""
    strategy: str = Field(..., description="Trading strategy name", example="breakout")

    class Config:
        json_schema_extra = {
            "example": {
                "strategy": "breakout"
            }
        }


class EntryRulesRequest(BaseModel):
    """Request for entry rules teaching"""
    pattern: str = Field(..., description="Chart pattern name", example="Cup and Handle")

    class Config:
        json_schema_extra = {
            "example": {
                "pattern": "Cup and Handle"
            }
        }


class VoiceCommandRequest(BaseModel):
    """Request for voice command processing"""
    command: str = Field(..., description="Voice command text (transcribed)", example="Show me AAPL analysis")

    class Config:
        json_schema_extra = {
            "example": {
                "command": "Show me AAPL analysis"
            }
        }


@router.post("/similar-setups",
             summary="Find Similar Stock Setups",
             responses={
                 200: {
                     "description": "List of stocks with similar technical setups",
                     "content": {
                         "application/json": {
                             "example": {
                                 "reference_symbol": "AAPL",
                                 "reference_pattern": "Cup and Handle",
                                 "similar_stocks": [
                                     {
                                         "symbol": "MSFT",
                                         "pattern": "Cup and Handle",
                                         "confidence": 75.5,
                                         "similarity_score": 0.755
                                     }
                                 ]
                             }
                         }
                     }
                 }
             })
async def find_similar_setups(request: SimilarSetupsRequest):
    """
    🔍 **Find Stocks with Similar Technical Setups**

    Get smart suggestions for stocks with similar patterns and setups.

    ## What You Get

    - 📊 Stocks with similar chart patterns
    - 🎯 Confidence scores for each match
    - 📈 Pattern descriptions
    - 💡 Actionable suggestions

    ## Use Cases

    - "Show me setups like AAPL"
    - "Find similar patterns to NVDA"
    - "What stocks look like TSLA?"

    **Example:**
    ```python
    import requests

    response = requests.post(
        'https://your-api.com/api/ai/similar-setups',
        json={'reference_symbol': 'AAPL', 'top_n': 5}
    )
    ```
    """
    try:
        assistant = get_ai_assistant()
        result = await assistant.find_similar_setups(
            reference_symbol=request.reference_symbol,
            top_n=request.top_n
        )
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Similar setups error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/entry-timing",
             summary="Get Entry Timing Suggestions",
             responses={
                 200: {
                     "description": "Entry timing analysis and suggestions"
                 }
             })
async def get_entry_timing(request: EntryTimingRequest):
    """
    ⏰ **Get Smart Entry Timing Suggestions**

    AI-powered analysis of optimal entry points for a stock.

    ## What You Get

    - 🎯 Specific entry price levels
    - 🛡️ Stop loss recommendations
    - 📈 Price targets
    - ⚖️ Risk/reward ratios
    - 💡 Multiple entry scenarios

    ## Suggestion Types

    - **Pattern-based**: Entries based on chart patterns
    - **Support bounce**: Entries near support levels
    - **Breakout setup**: Entries on resistance breakouts

    **Example:**
    ```python
    response = requests.post(
        'https://your-api.com/api/ai/entry-timing',
        json={'symbol': 'TSLA'}
    )
    ```
    """
    try:
        assistant = get_ai_assistant()
        result = await assistant.suggest_entry_timing(request.symbol)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Entry timing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/quiz",
             summary="Generate Pattern Quiz",
             responses={
                 200: {
                     "description": "Interactive quiz questions"
                 }
             })
async def generate_quiz(request: PatternQuizRequest):
    """
    🎓 **Interactive Pattern Recognition Quiz**

    Test and improve your pattern recognition skills.

    ## Difficulty Levels

    - **Easy**: Basic pattern identification
    - **Medium**: Pattern characteristics and trading rules
    - **Hard**: Advanced pattern analysis and strategy

    ## Features

    - Multiple choice questions
    - Detailed explanations
    - Instant feedback
    - Track your progress

    **Example:**
    ```python
    response = requests.post(
        'https://your-api.com/api/ai/quiz',
        json={'difficulty': 'medium'}
    )
    ```
    """
    try:
        assistant = get_ai_assistant()
        result = await assistant.generate_pattern_quiz(request.difficulty)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Quiz generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tutorial",
             summary="Get Strategy Tutorial",
             responses={
                 200: {
                     "description": "Comprehensive strategy tutorial"
                 }
             })
async def get_tutorial(request: StrategyTutorialRequest):
    """
    📚 **Strategy Tutorials**

    Learn trading strategies with step-by-step guides.

    ## Available Strategies

    - **Breakout**: Trading breakouts from consolidation
    - **Pullback**: Buying pullbacks in uptrends
    - **VCP**: Volatility Contraction Pattern
    - **Reversal**: Trading reversal patterns
    - And more...

    ## Tutorial Includes

    - Strategy overview
    - Step-by-step execution
    - Key rules and guidelines
    - Real example trades
    - Common mistakes to avoid

    **Example:**
    ```python
    response = requests.post(
        'https://your-api.com/api/ai/tutorial',
        json={'strategy': 'breakout'}
    )
    ```
    """
    try:
        assistant = get_ai_assistant()
        result = await assistant.get_strategy_tutorial(request.strategy)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Tutorial error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/entry-rules",
             summary="Learn Pattern Entry Rules",
             responses={
                 200: {
                     "description": "Detailed entry rules for a pattern"
                 }
             })
async def get_entry_rules(request: EntryRulesRequest):
    """
    📋 **Pattern Entry Rules**

    Learn exact entry rules for specific chart patterns.

    ## What You Learn

    - ✅ Exact entry point
    - 🔔 Confirmation signals
    - 🛡️ Stop loss placement
    - 🎯 Price target calculation
    - 💡 Real-world examples

    ## Covered Patterns

    - Cup and Handle
    - VCP (Volatility Contraction Pattern)
    - Ascending/Descending Triangles
    - Bull/Bear Flags
    - And more...

    **Example:**
    ```python
    response = requests.post(
        'https://your-api.com/api/ai/entry-rules',
        json={'pattern': 'Cup and Handle'}
    )
    ```
    """
    try:
        assistant = get_ai_assistant()
        result = await assistant.teach_entry_rules(request.pattern)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Entry rules error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/voice-command",
             summary="Process Voice Command",
             responses={
                 200: {
                     "description": "Voice command response"
                 }
             })
async def process_voice_command(request: VoiceCommandRequest):
    """
    🎤 **Voice Command Processing**

    Process transcribed voice commands for hands-free trading analysis.

    ## Supported Commands

    - "Show me AAPL analysis"
    - "Find VCP patterns"
    - "Compare NVDA and AMD"
    - "What's TSLA doing?"
    - "Explain Cup and Handle pattern"
    - "Give me entry timing for MSFT"

    ## How It Works

    1. Voice is transcribed to text (client-side)
    2. Text sent to this endpoint
    3. Natural language processing detects intent
    4. Appropriate analysis is performed
    5. Response returned (can be converted to speech client-side)

    **Example:**
    ```python
    # After voice transcription
    response = requests.post(
        'https://your-api.com/api/ai/voice-command',
        json={'command': 'Show me AAPL analysis'}
    )
    ```
    """
    try:
        import time
        start_time = time.time()

        assistant = get_ai_assistant()

        # Process as regular chat (already has NL parsing)
        result = await assistant.chat(
            user_message=request.command,
            include_market_data=True
        )

        execution_time = (time.time() - start_time) * 1000  # Convert to ms

        # Add voice-specific metadata
        result['voice_command'] = True
        result['execution_time_ms'] = execution_time
        result['original_command'] = request.command

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Voice command error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
