"""
News API Router - Market news with sentiment analysis
"""

from fastapi import APIRouter, Query

from app.services.news import news_service

router = APIRouter(prefix="/api/news", tags=["News"])


@router.get("/general", summary="Get market news")
async def get_general_news(
    category: str = Query(
        default="general", description="News category: general, forex, crypto, merger"
    )
):
    """
    Get latest market news with sentiment analysis

    Returns up to 10 news items with headline, summary, source,
    and AI-powered sentiment analysis (Positive/Negative/Neutral).
    """
    return await news_service.get_market_news(category)


@router.get("/company/{symbol}", summary="Get company news")
async def get_company_news(
    symbol: str,
    days: int = Query(default=7, ge=1, le=30, description="Days of history"),
):
    """
    Get news for a specific company with sentiment analysis

    Returns up to 5 recent news items for the given stock symbol.
    """
    return await news_service.get_company_news(symbol.upper(), days)


@router.get("/sentiment/{symbol}", summary="Get news sentiment summary")
async def get_sentiment(symbol: str):
    """
    Get overall news sentiment for a stock

    Analyzes recent news and returns:
    - Overall sentiment (bullish/bearish/neutral)
    - Average sentiment score (-1 to 1)
    - Count of positive/negative/neutral articles
    """
    return await news_service.get_market_sentiment(symbol.upper())


@router.get("/trending", summary="Get trending market news")
async def get_trending_news():
    """
    Get trending market news across categories

    Returns combined news from general market, forex, and crypto categories.
    """
    general = await news_service.get_market_news("general")
    crypto = await news_service.get_market_news("crypto")

    # Combine and sort by timestamp
    all_news = general + crypto
    all_news.sort(key=lambda x: x.get("timestamp") or 0, reverse=True)

    return {
        "news": all_news[:15],
        "categories": {"general": len(general), "crypto": len(crypto)},
    }
