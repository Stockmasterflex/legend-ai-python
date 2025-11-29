from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.services.news import news_service

router = APIRouter(prefix="/api/news", tags=["News"])

@router.get("/general")
async def get_general_news(category: str = "general"):
    """Get latest market news with sentiment"""
    return await news_service.get_market_news(category)

@router.get("/company/{symbol}")
async def get_company_news(symbol: str):
    """Get news for a specific company"""
    return await news_service.get_company_news(symbol)
