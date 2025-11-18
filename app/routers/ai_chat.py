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
                "pattern_education"
            ]
        }
    except Exception as e:
        return {
            "status": "unavailable",
            "error": str(e)
        }
