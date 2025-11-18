"""
API endpoints for AI-powered market analysis
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import logging

from app.services.ai_market_analysis import get_ai_market_analysis_service
from app.services.scheduler import get_scheduler_service

logger = logging.getLogger(__name__)
router = APIRouter()


# Request/Response Models
class ChartAnalysisRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")
    chart_url: Optional[str] = Field(None, description="Chart URL (will be generated if not provided)")
    use_vision: bool = Field(True, description="Use GPT-4 Vision for analysis")


class ChartAnalysisResponse(BaseModel):
    success: bool
    ticker: str
    analysis: Dict[str, Any]
    error: Optional[str] = None


class NewsSentimentRequest(BaseModel):
    ticker: Optional[str] = Field(None, description="Stock ticker (None for general market)")
    max_articles: int = Field(10, description="Maximum articles to analyze")


class NewsSentimentResponse(BaseModel):
    success: bool
    sentiment: str
    score: float
    articles_analyzed: int
    detailed_sentiments: Optional[List[Dict]] = None
    error: Optional[str] = None


class NaturalLanguageQueryRequest(BaseModel):
    query: str = Field(..., description="Natural language query")
    user_id: str = Field("api", description="User identifier")


class NaturalLanguageQueryResponse(BaseModel):
    success: bool
    query: str
    interpretation: Optional[Dict] = None
    response: str
    results: Optional[Dict] = None
    execution_time_ms: Optional[float] = None
    error: Optional[str] = None


class MarketBriefResponse(BaseModel):
    success: bool
    brief: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@router.post("/analysis/chart", response_model=ChartAnalysisResponse)
async def analyze_chart(request: ChartAnalysisRequest):
    """
    Analyze chart using AI vision models

    Provides technical analysis including:
    - Support/resistance levels
    - Trend analysis
    - Pattern recognition
    - Risk assessment
    - Trade ideas
    """
    try:
        service = get_ai_market_analysis_service()

        chart_url = request.chart_url

        # If no chart URL provided, generate one
        if not chart_url:
            from app.config import get_settings
            settings = get_settings()
            base_url = settings.auto_webhook_url or "http://localhost:8000"

            import httpx
            async with httpx.AsyncClient() as client:
                chart_response = await client.post(
                    f"{base_url}/api/charts/generate",
                    json={"ticker": request.ticker, "interval": "1D"}
                )

                if chart_response.status_code == 200:
                    result = chart_response.json()
                    if result.get("success") and result.get("chart_url"):
                        chart_url = result["chart_url"]

        if not chart_url:
            raise HTTPException(status_code=400, detail="Chart URL not provided and generation failed")

        analysis = await service.analyze_chart(
            ticker=request.ticker,
            chart_url=chart_url,
            use_vision=request.use_vision
        )

        return ChartAnalysisResponse(
            success=True,
            ticker=request.ticker,
            analysis=analysis
        )

    except Exception as e:
        logger.error(f"Chart analysis error: {e}")
        return ChartAnalysisResponse(
            success=False,
            ticker=request.ticker,
            analysis={},
            error=str(e)
        )


@router.post("/analysis/news-sentiment", response_model=NewsSentimentResponse)
async def analyze_news_sentiment(request: NewsSentimentRequest):
    """
    Analyze news sentiment for a ticker or general market

    Scrapes recent news and performs AI sentiment analysis
    """
    try:
        service = get_ai_market_analysis_service()

        # First scrape news
        await service.scrape_news(ticker=request.ticker, limit=request.max_articles)

        # Then analyze sentiment
        sentiment = await service.analyze_news_sentiment(
            ticker=request.ticker,
            max_articles=request.max_articles
        )

        return NewsSentimentResponse(
            success=True,
            sentiment=sentiment.get("sentiment", "neutral"),
            score=sentiment.get("score", 0.0),
            articles_analyzed=sentiment.get("articles_analyzed", 0),
            detailed_sentiments=sentiment.get("detailed_sentiments", [])
        )

    except Exception as e:
        logger.error(f"News sentiment analysis error: {e}")
        return NewsSentimentResponse(
            success=False,
            sentiment="neutral",
            score=0.0,
            articles_analyzed=0,
            error=str(e)
        )


@router.get("/analysis/market-brief", response_model=MarketBriefResponse)
async def get_market_brief():
    """
    Get daily AI-generated market brief

    Includes:
    - Market summary
    - Top movers analysis
    - Sector performance
    - Pattern highlights
    - Risk factors
    - Trade ideas
    """
    try:
        service = get_ai_market_analysis_service()

        # Check for existing brief today
        from app.services.database import get_database_service
        from app.models import MarketBrief
        from datetime import datetime

        db = get_database_service()
        with db.get_session() as session:
            today = datetime.now().date()
            recent_brief = session.query(MarketBrief).filter(
                MarketBrief.brief_date >= datetime.combine(today, datetime.min.time())
            ).order_by(MarketBrief.generated_at.desc()).first()

            if recent_brief:
                import json
                brief_data = {
                    "id": recent_brief.id,
                    "market_summary": recent_brief.market_summary,
                    "top_movers": json.loads(recent_brief.top_movers) if recent_brief.top_movers else [],
                    "sector_performance": json.loads(recent_brief.sector_performance) if recent_brief.sector_performance else {},
                    "pattern_highlights": json.loads(recent_brief.pattern_highlights) if recent_brief.pattern_highlights else [],
                    "risk_factors": json.loads(recent_brief.risk_factors) if recent_brief.risk_factors else [],
                    "trade_ideas": json.loads(recent_brief.trade_ideas) if recent_brief.trade_ideas else [],
                    "sentiment": recent_brief.market_sentiment,
                    "sentiment_score": recent_brief.sentiment_score,
                    "generated_at": recent_brief.generated_at.isoformat()
                }

                return MarketBriefResponse(success=True, brief=brief_data)

        # Generate new brief
        brief = await service.generate_daily_brief()

        return MarketBriefResponse(success=True, brief=brief)

    except Exception as e:
        logger.error(f"Market brief error: {e}")
        return MarketBriefResponse(success=False, error=str(e))


@router.post("/analysis/query", response_model=NaturalLanguageQueryResponse)
async def process_natural_language_query(request: NaturalLanguageQueryRequest):
    """
    Process natural language queries about markets

    Examples:
    - "Find bullish setups in tech sector"
    - "Show me stocks breaking out"
    - "What's the market sentiment today?"
    """
    try:
        service = get_ai_market_analysis_service()

        result = await service.process_natural_language_query(
            query=request.query,
            user_id=request.user_id
        )

        return NaturalLanguageQueryResponse(
            success=True,
            query=result.get("query"),
            interpretation=result.get("interpretation"),
            response=result.get("response"),
            results=result.get("results"),
            execution_time_ms=result.get("execution_time_ms")
        )

    except Exception as e:
        logger.error(f"NL query processing error: {e}")
        return NaturalLanguageQueryResponse(
            success=False,
            query=request.query,
            response=f"Error processing query: {str(e)}",
            error=str(e)
        )


@router.post("/analysis/scrape-news")
async def scrape_news(ticker: Optional[str] = None, limit: int = 20):
    """
    Scrape news articles for a ticker or general market
    """
    try:
        service = get_ai_market_analysis_service()

        articles = await service.scrape_news(ticker=ticker, limit=limit)

        return {
            "success": True,
            "articles_scraped": len(articles),
            "articles": articles
        }

    except Exception as e:
        logger.error(f"News scraping error: {e}")
        return {
            "success": False,
            "error": str(e),
            "articles_scraped": 0,
            "articles": []
        }


@router.post("/analysis/trigger-brief")
async def trigger_daily_brief():
    """
    Manually trigger generation and sending of daily market brief
    (Useful for testing)
    """
    try:
        scheduler = get_scheduler_service()
        await scheduler.trigger_manual_brief()

        return {
            "success": True,
            "message": "Daily brief triggered successfully"
        }

    except Exception as e:
        logger.error(f"Error triggering brief: {e}")
        return {
            "success": False,
            "error": str(e)
        }


@router.get("/analysis/history/{ticker}")
async def get_analysis_history(ticker: str, limit: int = 10):
    """
    Get historical AI analysis for a ticker
    """
    try:
        from app.services.database import get_database_service
        from app.models import MarketAnalysis, Ticker

        db = get_database_service()
        with db.get_session() as session:
            ticker_obj = session.query(Ticker).filter(Ticker.symbol == ticker.upper()).first()

            if not ticker_obj:
                return {
                    "success": False,
                    "error": "Ticker not found",
                    "analyses": []
                }

            analyses = session.query(MarketAnalysis).filter(
                MarketAnalysis.ticker_id == ticker_obj.id
            ).order_by(MarketAnalysis.created_at.desc()).limit(limit).all()

            import json

            results = []
            for analysis in analyses:
                results.append({
                    "id": analysis.id,
                    "analysis_type": analysis.analysis_type,
                    "ai_model": analysis.ai_model,
                    "trend_direction": analysis.trend_direction,
                    "sentiment_score": analysis.sentiment_score,
                    "confidence_score": analysis.confidence_score,
                    "support_levels": json.loads(analysis.support_levels) if analysis.support_levels else [],
                    "resistance_levels": json.loads(analysis.resistance_levels) if analysis.resistance_levels else [],
                    "created_at": analysis.created_at.isoformat()
                })

            return {
                "success": True,
                "ticker": ticker.upper(),
                "analyses": results
            }

    except Exception as e:
        logger.error(f"Error getting analysis history: {e}")
        return {
            "success": False,
            "error": str(e),
            "analyses": []
        }
