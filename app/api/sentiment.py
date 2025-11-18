"""
Sentiment Analysis API Endpoints
Real-time news sentiment, trends, and breaking news alerts
"""
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime, timedelta

from app.services.sentiment_service import get_sentiment_service
from app.services.cache import get_cache_service

router = APIRouter(prefix="/api/sentiment", tags=["sentiment"])
logger = logging.getLogger(__name__)


@router.get("/news/{symbol}")
async def get_news(
    symbol: str,
    limit: int = Query(50, ge=1, le=100, description="Number of articles to return"),
    use_cache: bool = Query(True, description="Use cached results"),
) -> JSONResponse:
    """
    Get aggregated news articles for a ticker from multiple sources

    - **symbol**: Stock ticker symbol (e.g., AAPL, TSLA)
    - **limit**: Maximum number of articles to return (1-100)
    - **use_cache**: Whether to use cached results

    Returns news from Alpha Vantage, Finnhub, NewsAPI, and other sources
    """
    try:
        sentiment_service = get_sentiment_service()
        articles = await sentiment_service.aggregate_news(
            symbol=symbol.upper(),
            limit=limit,
            use_cache=use_cache
        )

        return JSONResponse({
            "success": True,
            "symbol": symbol.upper(),
            "count": len(articles),
            "articles": articles,
        })

    except Exception as e:
        logger.error(f"Error fetching news for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")


@router.get("/news/{symbol}/with-sentiment")
async def get_news_with_sentiment(
    symbol: str,
    limit: int = Query(50, ge=1, le=100, description="Number of articles to return"),
    analyzer: Optional[str] = Query(None, description="Sentiment analyzer: vader, finbert, openai"),
    use_cache: bool = Query(True, description="Use cached results"),
) -> JSONResponse:
    """
    Get news articles with AI-powered sentiment analysis

    - **symbol**: Stock ticker symbol
    - **limit**: Maximum number of articles
    - **analyzer**: Sentiment analyzer to use (vader, finbert, openai)
    - **use_cache**: Whether to use cached results

    Returns news articles with sentiment scores, labels, and confidence
    """
    try:
        sentiment_service = get_sentiment_service()
        articles = await sentiment_service.get_news_with_sentiment(
            symbol=symbol.upper(),
            limit=limit,
            use_cache=use_cache,
            analyzer=analyzer
        )

        # Calculate aggregate statistics
        if articles:
            avg_sentiment = sum(a.get("sentiment", {}).get("score", 0) for a in articles) / len(articles)
            positive_count = sum(1 for a in articles if a.get("sentiment", {}).get("sentiment_label") == "positive")
            negative_count = sum(1 for a in articles if a.get("sentiment", {}).get("sentiment_label") == "negative")
            neutral_count = sum(1 for a in articles if a.get("sentiment", {}).get("sentiment_label") == "neutral")
        else:
            avg_sentiment = 0
            positive_count = negative_count = neutral_count = 0

        return JSONResponse({
            "success": True,
            "symbol": symbol.upper(),
            "count": len(articles),
            "summary": {
                "average_sentiment": round(avg_sentiment, 4),
                "positive_count": positive_count,
                "negative_count": negative_count,
                "neutral_count": neutral_count,
                "analyzer_used": analyzer or "vader",
            },
            "articles": articles,
        })

    except Exception as e:
        logger.error(f"Error fetching news with sentiment for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=f"Error analyzing sentiment: {str(e)}")


@router.get("/score/{symbol}")
async def get_sentiment_score(
    symbol: str,
    hours_back: int = Query(24, ge=1, le=168, description="Hours to look back (max 7 days)"),
) -> JSONResponse:
    """
    Get current sentiment score and trend for a ticker

    - **symbol**: Stock ticker symbol
    - **hours_back**: How many hours of history to analyze (1-168)

    Returns:
    - Current sentiment score (-1 to 1)
    - Sentiment label (positive/negative/neutral)
    - Trend analysis (improving/deteriorating/stable)
    - Sentiment shift detection
    - Article counts by sentiment
    """
    try:
        sentiment_service = get_sentiment_service()
        trend = await sentiment_service.get_sentiment_trend(
            symbol=symbol.upper(),
            hours_back=hours_back
        )

        return JSONResponse({
            "success": True,
            **trend,
        })

    except Exception as e:
        logger.error(f"Error getting sentiment score for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=f"Error calculating sentiment: {str(e)}")


@router.get("/trend/{symbol}")
async def get_sentiment_trend(
    symbol: str,
    hours_back: int = Query(24, ge=1, le=168, description="Hours to analyze"),
) -> JSONResponse:
    """
    Get detailed sentiment trend analysis

    Includes:
    - Historical sentiment progression
    - Sentiment shift detection
    - Positive/negative/neutral distribution
    - Breaking news impact
    """
    try:
        sentiment_service = get_sentiment_service()
        trend = await sentiment_service.get_sentiment_trend(
            symbol=symbol.upper(),
            hours_back=hours_back
        )

        return JSONResponse({
            "success": True,
            "trend": trend,
        })

    except Exception as e:
        logger.error(f"Error getting sentiment trend for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=f"Error analyzing trend: {str(e)}")


@router.get("/breaking/{symbol}")
async def get_breaking_news(
    symbol: str,
    hours_back: int = Query(2, ge=1, le=24, description="Hours to look back for breaking news"),
) -> JSONResponse:
    """
    Get breaking news alerts for a ticker

    Filters for urgent/breaking news based on keywords:
    - "breaking"
    - "alert"
    - "urgent"
    - "emergency"
    - "halt"

    Returns recent breaking news with sentiment analysis
    """
    try:
        sentiment_service = get_sentiment_service()
        breaking = await sentiment_service.get_breaking_news(
            symbol=symbol.upper(),
            hours_back=hours_back
        )

        return JSONResponse({
            "success": True,
            "symbol": symbol.upper(),
            "breaking_count": len(breaking),
            "hours_analyzed": hours_back,
            "breaking_news": breaking,
        })

    except Exception as e:
        logger.error(f"Error getting breaking news for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching breaking news: {str(e)}")


@router.post("/analyze")
async def analyze_text_sentiment(
    request: Request,
) -> JSONResponse:
    """
    Analyze sentiment of arbitrary text

    Request body:
    ```json
    {
        "text": "Your text to analyze",
        "analyzer": "vader"  // optional: vader, finbert, openai
    }
    ```

    Returns sentiment score, label, and confidence
    """
    try:
        body = await request.json()
        text = body.get("text")
        analyzer = body.get("analyzer")

        if not text:
            raise HTTPException(status_code=400, detail="Text is required")

        sentiment_service = get_sentiment_service()
        result = await sentiment_service.analyze_sentiment(text, analyzer)

        return JSONResponse({
            "success": True,
            "sentiment": result,
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing text sentiment: {e}")
        raise HTTPException(status_code=500, detail=f"Error analyzing sentiment: {str(e)}")


@router.get("/usage")
async def get_sentiment_api_usage() -> JSONResponse:
    """
    Get API usage statistics for sentiment data sources

    Returns usage counts and limits for:
    - Alpha Vantage
    - Finnhub
    - NewsAPI
    - Benzinga
    """
    try:
        sentiment_service = get_sentiment_service()
        usage = await sentiment_service.get_usage_stats()

        return JSONResponse({
            "success": True,
            "usage": usage,
        })

    except Exception as e:
        logger.error(f"Error getting sentiment API usage: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching usage stats: {str(e)}")


@router.get("/feed/{symbol}")
async def get_sentiment_feed(
    symbol: str,
    limit: int = Query(20, ge=1, le=50, description="Number of items in feed"),
    include_breaking: bool = Query(True, description="Highlight breaking news"),
) -> JSONResponse:
    """
    Get formatted news feed for dashboard widget

    Optimized response for UI display:
    - Quick-read summaries
    - Sentiment indicators
    - Breaking news flags
    - Time-ordered feed
    """
    try:
        sentiment_service = get_sentiment_service()

        # Get news with sentiment
        articles = await sentiment_service.get_news_with_sentiment(
            symbol=symbol.upper(),
            limit=limit,
            use_cache=True
        )

        # Format for feed widget
        feed_items = []
        for article in articles:
            sentiment = article.get("sentiment", {})

            # Create quick-read summary (first 150 chars)
            summary = article.get("summary", article.get("title", ""))
            if len(summary) > 150:
                summary = summary[:147] + "..."

            # Determine sentiment indicator color
            score = sentiment.get("score", 0)
            if score > 0.05:
                indicator = "positive"
                indicator_color = "#22c55e"  # green
            elif score < -0.05:
                indicator = "negative"
                indicator_color = "#ef4444"  # red
            else:
                indicator = "neutral"
                indicator_color = "#6b7280"  # gray

            feed_items.append({
                "id": hash(article.get("url", "")),
                "title": article.get("title"),
                "summary": summary,
                "url": article.get("url"),
                "source": article.get("source"),
                "published_at": article.get("published_at"),
                "is_breaking": article.get("is_breaking", False),
                "sentiment_score": round(score, 3),
                "sentiment_label": sentiment.get("sentiment_label", "neutral"),
                "sentiment_indicator": indicator,
                "sentiment_color": indicator_color,
                "confidence": round(sentiment.get("confidence", 0), 2),
            })

        # Get current sentiment trend
        trend = await sentiment_service.get_sentiment_trend(symbol.upper(), hours_back=24)

        return JSONResponse({
            "success": True,
            "symbol": symbol.upper(),
            "feed": feed_items,
            "current_sentiment": {
                "score": trend.get("current_sentiment", 0),
                "label": trend.get("sentiment_label", "neutral"),
                "trend": trend.get("trend", "stable"),
                "shift_detected": trend.get("shift_detected", False),
            },
            "stats": {
                "total_articles": len(feed_items),
                "breaking_count": trend.get("breaking_news_count", 0),
                "positive_count": trend.get("positive_count", 0),
                "negative_count": trend.get("negative_count", 0),
                "neutral_count": trend.get("neutral_count", 0),
            }
        })

    except Exception as e:
        logger.error(f"Error getting sentiment feed for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching sentiment feed: {str(e)}")


@router.get("/impact/{symbol}")
async def get_news_impact(
    symbol: str,
    hours_back: int = Query(24, ge=1, le=168, description="Hours to analyze"),
) -> JSONResponse:
    """
    Analyze correlation between news sentiment and price/volume impact

    Returns:
    - News impact scores
    - Pattern invalidation warnings
    - Opportunity alerts
    - Top impact news articles
    """
    try:
        sentiment_service = get_sentiment_service()
        impact = await sentiment_service.analyze_news_impact(
            symbol=symbol.upper(),
            hours_back=hours_back
        )

        return JSONResponse({
            "success": True,
            **impact,
        })

    except Exception as e:
        logger.error(f"Error analyzing news impact for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=f"Error analyzing impact: {str(e)}")


@router.get("/volume-correlation/{symbol}")
async def get_volume_correlation(
    symbol: str,
    hours_back: int = Query(24, ge=1, le=168, description="Hours to analyze"),
) -> JSONResponse:
    """
    Analyze correlation between news frequency and volume changes

    Returns news intensity and volume spike indicators
    """
    try:
        sentiment_service = get_sentiment_service()
        correlation = await sentiment_service.get_volume_correlation(
            symbol=symbol.upper(),
            hours_back=hours_back
        )

        return JSONResponse({
            "success": True,
            **correlation,
        })

    except Exception as e:
        logger.error(f"Error analyzing volume correlation for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=f"Error analyzing correlation: {str(e)}")
