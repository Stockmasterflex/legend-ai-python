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
    """Chat request"""
    message: str = Field(..., description="User message")
    symbol: Optional[str] = Field(None, description="Stock symbol for context")
    include_market_data: bool = Field(True, description="Include live market data in context")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for history")


class AnalyzeStockRequest(BaseModel):
    """Stock analysis request"""
    symbol: str = Field(..., description="Stock ticker symbol")


class CompareStocksRequest(BaseModel):
    """Stock comparison request"""
    symbols: List[str] = Field(..., description="List of stock symbols (2-5)")


class ExplainPatternRequest(BaseModel):
    """Pattern explanation request"""
    pattern_name: str = Field(..., description="Name of chart pattern")


@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat with AI Financial Assistant

    The AI assistant can:
    - Answer questions about trading and markets
    - Analyze specific stocks with real-time data
    - Explain technical concepts and patterns
    - Provide educational insights

    **Note:** This is an educational tool, not financial advice.
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


@router.post("/analyze")
async def analyze_stock(request: AnalyzeStockRequest):
    """
    Get comprehensive AI-powered stock analysis

    Provides:
    - Technical setup and trend analysis
    - Pattern detection and interpretation
    - Key support/resistance levels
    - Risk assessment
    - Potential trading opportunities

    **Example:**
    ```json
    {
        "symbol": "AAPL"
    }
    ```
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
