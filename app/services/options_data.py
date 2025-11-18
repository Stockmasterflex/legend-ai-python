"""
Options Data Service
Fetches options chains, flow data, and unusual activity
"""
import httpx
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import asyncio
import logging
import json

from app.config import get_settings
from app.services.cache import get_cache_service
from app.core.options import GreeksCalculator, MaxPainCalculator

logger = logging.getLogger(__name__)


class OptionsDataService:
    """Service for fetching and processing options data"""

    def __init__(self):
        self.settings = get_settings()
        self.cache = get_cache_service()
        self.client = httpx.AsyncClient(timeout=30.0)
        self.greeks_calc = GreeksCalculator()
        self.max_pain_calc = MaxPainCalculator()

    async def get_options_chain(
        self,
        symbol: str,
        expiry_date: Optional[str] = None,
        include_greeks: bool = True
    ) -> Dict[str, Any]:
        """
        Get options chain for a symbol

        Args:
            symbol: Stock ticker
            expiry_date: Specific expiry date (YYYY-MM-DD), or None for all
            include_greeks: Calculate Greeks for each option

        Returns:
            Dict with calls, puts, and metadata
        """
        cache_key = f"options_chain:{symbol}:{expiry_date or 'all'}"

        # Check cache first (5-minute TTL for options data)
        cached = await self.cache.get(cache_key)
        if cached:
            logger.info(f"Cache hit for options chain: {symbol}")
            return cached

        try:
            # Get options data from Finnhub
            chain_data = await self._fetch_from_finnhub(symbol, expiry_date)

            if include_greeks and chain_data:
                chain_data = await self._enrich_with_greeks(chain_data, symbol)

            # Cache for 5 minutes
            await self.cache.set(cache_key, chain_data, ttl=300)

            return chain_data

        except Exception as e:
            logger.error(f"Error fetching options chain for {symbol}: {e}")
            return {"calls": [], "puts": [], "error": str(e)}

    async def _fetch_from_finnhub(
        self,
        symbol: str,
        expiry_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fetch options chain from Finnhub"""
        # Note: In production, this would use the actual Finnhub API
        # For now, returning mock data structure

        url = f"https://finnhub.io/api/v1/stock/option-chain"
        params = {
            "symbol": symbol,
            "token": self.settings.finnhub_api_key
        }

        if expiry_date:
            params["date"] = expiry_date

        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Transform Finnhub data to our format
            return self._transform_finnhub_data(data, symbol)

        except Exception as e:
            logger.warning(f"Finnhub API error for {symbol}: {e}")
            # Return mock data for development
            return self._generate_mock_chain(symbol, expiry_date)

    def _transform_finnhub_data(self, data: Dict, symbol: str) -> Dict[str, Any]:
        """Transform Finnhub response to our format"""
        calls = []
        puts = []

        for option in data.get("data", []):
            option_dict = {
                "strike": option.get("strike"),
                "expiry": option.get("expiration"),
                "last_price": option.get("lastPrice", 0),
                "bid": option.get("bid", 0),
                "ask": option.get("ask", 0),
                "volume": option.get("volume", 0),
                "open_interest": option.get("openInterest", 0),
                "implied_volatility": option.get("impliedVolatility", 0),
                "delta": option.get("delta", 0),
                "gamma": option.get("gamma", 0),
                "theta": option.get("theta", 0),
                "vega": option.get("vega", 0),
            }

            if option.get("type") == "Call":
                calls.append(option_dict)
            else:
                puts.append(option_dict)

        return {
            "symbol": symbol,
            "calls": calls,
            "puts": puts,
            "timestamp": datetime.now().isoformat()
        }

    def _generate_mock_chain(self, symbol: str, expiry_date: Optional[str] = None) -> Dict[str, Any]:
        """Generate mock options chain for development/testing"""
        # Use a base price (in production, fetch actual stock price)
        spot_price = 150.0

        # Generate strikes around the current price
        strikes = [round(spot_price + i * 5, 2) for i in range(-10, 11)]

        # Use near-term expiry if not specified
        if not expiry_date:
            expiry_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

        calls = []
        puts = []

        time_to_expiry = (datetime.strptime(expiry_date, "%Y-%m-%d") - datetime.now()).days / 252.0

        for strike in strikes:
            # Mock option prices based on simple intrinsic value + time value
            call_intrinsic = max(0, spot_price - strike)
            put_intrinsic = max(0, strike - spot_price)

            time_value = 5.0 * (time_to_expiry ** 0.5)  # Simple time decay

            call_price = call_intrinsic + time_value
            put_price = put_intrinsic + time_value

            # Mock volume and OI (higher near ATM)
            distance_from_atm = abs(strike - spot_price)
            volume_factor = max(100, 1000 - distance_from_atm * 10)

            calls.append({
                "strike": strike,
                "expiry": expiry_date,
                "last_price": round(call_price, 2),
                "bid": round(call_price * 0.98, 2),
                "ask": round(call_price * 1.02, 2),
                "volume": int(volume_factor * (0.8 + 0.4 * hash(str(strike)) % 100 / 100)),
                "open_interest": int(volume_factor * 5 * (0.8 + 0.4 * hash(str(strike + 1)) % 100 / 100)),
                "implied_volatility": 0.25 + 0.1 * (abs(strike - spot_price) / spot_price),
            })

            puts.append({
                "strike": strike,
                "expiry": expiry_date,
                "last_price": round(put_price, 2),
                "bid": round(put_price * 0.98, 2),
                "ask": round(put_price * 1.02, 2),
                "volume": int(volume_factor * 0.9 * (0.8 + 0.4 * hash(str(strike + 2)) % 100 / 100)),
                "open_interest": int(volume_factor * 4.5 * (0.8 + 0.4 * hash(str(strike + 3)) % 100 / 100)),
                "implied_volatility": 0.28 + 0.12 * (abs(strike - spot_price) / spot_price),
            })

        return {
            "symbol": symbol,
            "spot_price": spot_price,
            "calls": calls,
            "puts": puts,
            "timestamp": datetime.now().isoformat()
        }

    async def _enrich_with_greeks(self, chain_data: Dict, symbol: str) -> Dict[str, Any]:
        """Calculate Greeks for each option in the chain"""
        # Get current stock price
        spot_price = chain_data.get("spot_price", 150.0)
        risk_free_rate = 0.05

        for option in chain_data.get("calls", []) + chain_data.get("puts", []):
            strike = option["strike"]
            expiry = option["expiry"]
            option_type = "call" if option in chain_data.get("calls", []) else "put"

            # Calculate time to expiry
            expiry_dt = datetime.strptime(expiry, "%Y-%m-%d")
            time_to_expiry = self.greeks_calc.calculate_time_to_expiry(expiry_dt)

            # Use IV from option or default
            iv = option.get("implied_volatility", 0.3)

            # Calculate Greeks
            greeks = self.greeks_calc.calculate_greeks(
                spot_price=spot_price,
                strike=strike,
                time_to_expiry=time_to_expiry,
                risk_free_rate=risk_free_rate,
                volatility=iv,
                option_type=option_type
            )

            # Add Greeks to option
            option.update(greeks)

        return chain_data

    async def get_unusual_activity(
        self,
        symbol: Optional[str] = None,
        min_premium: float = 50000,
        min_volume: int = 500
    ) -> List[Dict[str, Any]]:
        """
        Detect unusual options activity

        Args:
            symbol: Filter by symbol (None for all)
            min_premium: Minimum premium threshold
            min_volume: Minimum volume threshold

        Returns:
            List of unusual options contracts
        """
        cache_key = f"unusual_activity:{symbol or 'all'}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        try:
            # In production, fetch from data provider
            # For now, generate mock unusual activity
            unusual = self._generate_mock_unusual_activity(symbol, min_premium, min_volume)

            # Cache for 2 minutes
            await self.cache.set(cache_key, unusual, ttl=120)

            return unusual

        except Exception as e:
            logger.error(f"Error fetching unusual activity: {e}")
            return []

    def _generate_mock_unusual_activity(
        self,
        symbol: Optional[str],
        min_premium: float,
        min_volume: int
    ) -> List[Dict[str, Any]]:
        """Generate mock unusual activity for development"""
        symbols = [symbol] if symbol else ["AAPL", "TSLA", "NVDA", "SPY", "QQQ"]

        unusual = []

        for sym in symbols:
            # Generate 2-3 unusual contracts per symbol
            for i in range(2):
                expiry = (datetime.now() + timedelta(days=7 + i * 7)).strftime("%Y-%m-%d")
                strike = 150 + i * 10

                unusual.append({
                    "symbol": sym,
                    "strike": strike,
                    "expiry": expiry,
                    "type": "call" if i % 2 == 0 else "put",
                    "volume": min_volume * (2 + i),
                    "open_interest": min_volume // 2,
                    "premium": min_premium * (1.5 + i * 0.5),
                    "last_price": 5.50 + i * 2,
                    "volume_oi_ratio": 4.0 + i,
                    "timestamp": datetime.now().isoformat(),
                    "sentiment": "bullish" if i % 2 == 0 else "bearish"
                })

        return sorted(unusual, key=lambda x: x["premium"], reverse=True)[:20]

    async def get_options_flow(
        self,
        symbol: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get real-time options flow/trades

        Args:
            symbol: Stock ticker
            limit: Max number of trades to return

        Returns:
            List of recent options trades
        """
        cache_key = f"options_flow:{symbol}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        try:
            # In production, fetch from real-time data provider
            flow = self._generate_mock_flow(symbol, limit)

            # Cache for 1 minute
            await self.cache.set(cache_key, flow, ttl=60)

            return flow

        except Exception as e:
            logger.error(f"Error fetching options flow for {symbol}: {e}")
            return []

    def _generate_mock_flow(self, symbol: str, limit: int) -> List[Dict[str, Any]]:
        """Generate mock options flow data"""
        flow = []

        now = datetime.now()

        for i in range(min(limit, 50)):
            timestamp = now - timedelta(minutes=i)

            flow.append({
                "symbol": symbol,
                "timestamp": timestamp.isoformat(),
                "strike": 150 + (i % 20 - 10) * 5,
                "expiry": (now + timedelta(days=7 + i % 30)).strftime("%Y-%m-%d"),
                "type": "call" if i % 3 != 0 else "put",
                "trade_type": ["sweep", "block", "split", "single"][i % 4],
                "size": 100 * (i % 10 + 1),
                "price": 5.0 + (i % 10) * 0.5,
                "premium": (100 * (i % 10 + 1)) * (5.0 + (i % 10) * 0.5) * 100,
                "side": "ask" if i % 2 == 0 else "bid",
                "sentiment": "bullish" if i % 2 == 0 else "bearish"
            })

        return flow

    async def get_darkpool_prints(
        self,
        symbol: str,
        min_size: int = 10000
    ) -> List[Dict[str, Any]]:
        """
        Get darkpool options prints

        Args:
            symbol: Stock ticker
            min_size: Minimum trade size

        Returns:
            List of darkpool trades
        """
        cache_key = f"darkpool:{symbol}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        try:
            # Mock darkpool data
            darkpool = self._generate_mock_darkpool(symbol, min_size)

            await self.cache.set(cache_key, darkpool, ttl=180)

            return darkpool

        except Exception as e:
            logger.error(f"Error fetching darkpool for {symbol}: {e}")
            return []

    def _generate_mock_darkpool(self, symbol: str, min_size: int) -> List[Dict[str, Any]]:
        """Generate mock darkpool data"""
        darkpool = []
        now = datetime.now()

        for i in range(10):
            darkpool.append({
                "symbol": symbol,
                "timestamp": (now - timedelta(hours=i)).isoformat(),
                "size": min_size * (2 + i),
                "price": 150 + i * 0.5,
                "type": "options" if i % 2 == 0 else "equity",
                "exchange": ["CBOE", "PHLX", "ISE", "AMEX"][i % 4]
            })

        return darkpool

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Singleton instance
_options_data_service = None


def get_options_data_service() -> OptionsDataService:
    """Get or create options data service singleton"""
    global _options_data_service
    if _options_data_service is None:
        _options_data_service = OptionsDataService()
    return _options_data_service
