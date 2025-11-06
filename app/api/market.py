from fastapi import APIRouter
import httpx
import logging
from typing import Dict

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/market", tags=["market"])

@router.get("/internals")
async def get_market_internals():
    """Get market internals and regime"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            spy = await client.get("https://query1.finance.yahoo.com/v8/finance/chart/SPY?interval=1d&range=5d")
            vix = await client.get("https://query1.finance.yahoo.com/v8/finance/chart/^VIX?interval=1d&range=5d")
            
            spy_data = spy.json()
            vix_data = vix.json()
            
            spy_close = spy_data["chart"]["result"][0]["indicators"]["quote"][0]["close"][-1]
            vix_close = vix_data["chart"]["result"][0]["indicators"]["quote"][0]["close"][-1]
            
            regime = "Uptrend" if vix_close < 20 else "Pressure" if vix_close < 30 else "Downtrend"
            
            return {
                "spy_price": round(spy_close, 2),
                "vix": round(vix_close, 2),
                "regime": regime,
                "market_status": "Open" if 9.5 <= datetime.now().hour < 16 else "Closed"
            }
    except:
        return {"regime": "Unknown", "vix": 0, "spy_price": 0}

from datetime import datetime

