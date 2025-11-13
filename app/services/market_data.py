"""
Enhanced Market Data Service with Multi-Source Fallback
Intelligently manages API limits across TwelveData, Finnhub, and Alpha Vantage
"""
import httpx
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import asyncio
import logging
from enum import Enum

from app.config import get_settings
from app.services.cache import get_cache_service

logger = logging.getLogger(__name__)


class DataSource(str, Enum):
    TWELVE_DATA = "twelvedata"
    FINNHUB = "finnhub"
    ALPHA_VANTAGE = "alphavantage"
    YAHOO = "yahoo"
    CACHE = "cache"


class MarketDataService:
    """
    Unified market data service with intelligent multi-source fallback

    Priority order:
    1. Redis Cache (instant)
    2. TwelveData (primary, 800 calls/day)
    3. Finnhub (fallback, 60 calls/day)
    4. Alpha Vantage (fallback, 500 calls/day)
    5. Yahoo Finance (last resort, unlimited but may be blocked)
    """

    def __init__(self):
        self.settings = get_settings()
        self.cache = get_cache_service()
        self.client = httpx.AsyncClient(timeout=30.0)

        # API usage tracking (persisted in Redis)
        self.usage_key_prefix = "api_usage"

    async def get_usage_stats(self) -> Dict[str, Any]:
        """Get current API usage for all sources"""
        try:
            twelve_usage = await self.cache.get(f"{self.usage_key_prefix}:twelvedata") or 0
            finnhub_usage = await self.cache.get(f"{self.usage_key_prefix}:finnhub") or 0
            alpha_usage = await self.cache.get(f"{self.usage_key_prefix}:alphavantage") or 0

            return {
                "twelvedata": {
                    "used": int(twelve_usage),
                    "limit": self.settings.twelvedata_daily_limit,
                    "remaining": self.settings.twelvedata_daily_limit - int(twelve_usage),
                    "percent": (int(twelve_usage) / self.settings.twelvedata_daily_limit) * 100
                },
                "finnhub": {
                    "used": int(finnhub_usage),
                    "limit": self.settings.finnhub_daily_limit,
                    "remaining": self.settings.finnhub_daily_limit - int(finnhub_usage),
                    "percent": (int(finnhub_usage) / self.settings.finnhub_daily_limit) * 100
                },
                "alphavantage": {
                    "used": int(alpha_usage),
                    "limit": self.settings.alpha_vantage_daily_limit,
                    "remaining": self.settings.alpha_vantage_daily_limit - int(alpha_usage),
                    "percent": (int(alpha_usage) / self.settings.alpha_vantage_daily_limit) * 100
                }
            }
        except Exception as e:
            logger.warning(f"Error getting usage stats: {e}")
            return {"error": str(e)}

    async def _increment_usage(self, source: DataSource):
        """Increment API usage counter (resets daily at midnight)"""
        try:
            key = f"{self.usage_key_prefix}:{source.value}"
            current = await self.cache.get(key) or 0
            await self.cache.set(key, int(current) + 1, ttl=86400)  # 24 hours
        except Exception as e:
            logger.warning(f"Error incrementing usage for {source}: {e}")

    async def _check_rate_limit(self, source: DataSource) -> bool:
        """Check if we can make a request to this source"""
        try:
            key = f"{self.usage_key_prefix}:{source.value}"
            current = await self.cache.get(key) or 0

            limits = {
                DataSource.TWELVE_DATA: self.settings.twelvedata_daily_limit,
                DataSource.FINNHUB: self.settings.finnhub_daily_limit,
                DataSource.ALPHA_VANTAGE: self.settings.alpha_vantage_daily_limit
            }

            limit = limits.get(source, 999999)
            can_request = int(current) < limit

            if not can_request:
                logger.warning(f"⚠️ {source.value} daily limit reached ({current}/{limit})")

            return can_request
        except Exception as e:
            logger.warning(f"Error checking rate limit: {e}")
            return True  # Fail open

    async def get_time_series(
        self,
        ticker: str,
        interval: str = "1day",
        outputsize: int = 500
    ) -> Optional[Dict[str, Any]]:
        """
        Get OHLCV time series data with intelligent fallback

        Returns:
            {
                "c": [closes],
                "o": [opens],
                "h": [highs],
                "l": [lows],
                "v": [volumes],
                "t": [timestamps],
                "source": "twelvedata" | "finnhub" | "alphavantage" | "yahoo",
                "cached": bool
            }
        """
        # 1. Try cache first
        cache_key = f"timeseries:{ticker}:{interval}"
        cached_data = await self.cache.get(cache_key)
        if cached_data:
            logger.info(f"⚡ Cache hit for {ticker}")
            cached_data["cached"] = True
            cached_data["source"] = DataSource.CACHE
            return cached_data

        # 2. Try TwelveData (primary) only if API key configured
        if self.settings.twelvedata_api_key and await self._check_rate_limit(DataSource.TWELVE_DATA):
            data = await self._get_from_twelvedata(ticker, interval, outputsize)
            if data:
                await self._increment_usage(DataSource.TWELVE_DATA)
                await self.cache.set(cache_key, data, ttl=900)  # 15 min cache
                data["cached"] = False
                data["source"] = DataSource.TWELVE_DATA
                return data

        # 3. Try Finnhub (fallback 1)
        if self.settings.finnhub_api_key and await self._check_rate_limit(DataSource.FINNHUB):
            data = await self._get_from_finnhub(ticker, interval, outputsize)
            if data:
                await self._increment_usage(DataSource.FINNHUB)
                await self.cache.set(cache_key, data, ttl=900)
                data["cached"] = False
                data["source"] = DataSource.FINNHUB
                return data

        # 4. Try Alpha Vantage (fallback 2)
        if self.settings.alpha_vantage_api_key and await self._check_rate_limit(DataSource.ALPHA_VANTAGE):
            data = await self._get_from_alpha_vantage(ticker, interval, outputsize)
            if data:
                await self._increment_usage(DataSource.ALPHA_VANTAGE)
                await self.cache.set(cache_key, data, ttl=900)
                data["cached"] = False
                data["source"] = DataSource.ALPHA_VANTAGE
                return data

        # 5. Try Yahoo Finance (last resort)
        data = await self._get_from_yahoo(ticker, interval)
        if data:
            await self.cache.set(cache_key, data, ttl=900)
            data["cached"] = False
            data["source"] = DataSource.YAHOO
            return data

        logger.error(f"❌ All data sources failed for {ticker}")
        return None

    async def _get_from_twelvedata(
        self,
        ticker: str,
        interval: str,
        outputsize: int
    ) -> Optional[Dict[str, Any]]:
        """Get data from TwelveData"""
        try:
            url = "https://api.twelvedata.com/time_series"
            params = {
                "symbol": ticker,
                "interval": interval,
                "outputsize": min(outputsize, 5000),
                "format": "json",
                **({"apikey": self.settings.twelvedata_api_key} if self.settings.twelvedata_api_key else {}),
            }

            logger.info(f"📡 TwelveData: {ticker}")
            response = await self.client.get(url, params=params)

            if response.status_code != 200:
                logger.warning(f"TwelveData HTTP {response.status_code}")
                return None

            data = response.json()

            if "status" in data and data["status"] == "error":
                logger.warning(f"TwelveData error: {data.get('message')}")
                return None

            if "values" not in data:
                return None

            # Transform to standard format
            result = {"c": [], "o": [], "h": [], "l": [], "v": [], "t": []}

            for value in reversed(data["values"]):
                try:
                    result["c"].append(float(value["close"]))
                    result["o"].append(float(value["open"]))
                    result["h"].append(float(value["high"]))
                    result["l"].append(float(value["low"]))
                    result["v"].append(float(value["volume"]))
                    result["t"].append(value["datetime"])
                except (ValueError, KeyError):
                    continue

            if len(result["c"]) < 50:
                logger.warning(f"Insufficient TwelveData data: {len(result['c'])} points")
                return None

            return result

        except Exception as e:
            logger.error(f"TwelveData error: {e}")
            return None

    async def _get_from_finnhub(
        self,
        ticker: str,
        interval: str,
        outputsize: int
    ) -> Optional[Dict[str, Any]]:
        """Get data from Finnhub"""
        try:
            # Finnhub uses resolution: 1, 5, 15, 30, 60, D, W, M
            resolution_map = {
                "1min": "1",
                "5min": "5",
                "15min": "15",
                "30min": "30",
                "1hour": "60",
                "1day": "D",
                "1week": "W",
                "1month": "M"
            }
            resolution = resolution_map.get(interval, "D")

            # Calculate time range
            now = int(datetime.now().timestamp())
            days_back = 500 if resolution == "D" else 30
            from_ts = now - (days_back * 86400)

            url = "https://finnhub.io/api/v1/stock/candle"
            params = {
                "symbol": ticker,
                "resolution": resolution,
                "from": from_ts,
                "to": now,
                "token": self.settings.finnhub_api_key
            }

            logger.info(f"📡 Finnhub: {ticker}")
            response = await self.client.get(url, params=params)

            if response.status_code != 200:
                logger.warning(f"Finnhub HTTP {response.status_code}")
                return None

            data = response.json()

            if data.get("s") != "ok":
                logger.warning(f"Finnhub status: {data.get('s')}")
                return None

            # Transform to standard format
            result = {
                "c": data.get("c", []),
                "o": data.get("o", []),
                "h": data.get("h", []),
                "l": data.get("l", []),
                "v": data.get("v", []),
                "t": [datetime.fromtimestamp(ts).isoformat() for ts in data.get("t", [])]
            }

            if len(result["c"]) < 50:
                logger.warning(f"Insufficient Finnhub data: {len(result['c'])} points")
                return None

            return result

        except Exception as e:
            logger.error(f"Finnhub error: {e}")
            return None

    async def _get_from_alpha_vantage(
        self,
        ticker: str,
        interval: str,
        outputsize: int
    ) -> Optional[Dict[str, Any]]:
        """Get data from Alpha Vantage"""
        try:
            # Alpha Vantage function mapping
            if interval in ["1min", "5min", "15min", "30min", "60min"]:
                function = "TIME_SERIES_INTRADAY"
                interval_param = interval
            else:
                function = "TIME_SERIES_DAILY"
                interval_param = None

            url = "https://www.alphavantage.co/query"
            params = {
                "function": function,
                "symbol": ticker,
                "apikey": self.settings.alpha_vantage_api_key,
                "outputsize": "full" if outputsize > 100 else "compact"
            }

            if interval_param:
                params["interval"] = interval_param

            logger.info(f"📡 Alpha Vantage: {ticker}")
            response = await self.client.get(url, params=params)

            if response.status_code != 200:
                logger.warning(f"Alpha Vantage HTTP {response.status_code}")
                return None

            data = response.json()

            # Find the time series data
            time_series_key = None
            for key in data.keys():
                if "Time Series" in key:
                    time_series_key = key
                    break

            if not time_series_key:
                logger.warning("No Alpha Vantage time series data")
                return None

            series = data[time_series_key]

            # Transform to standard format
            result = {"c": [], "o": [], "h": [], "l": [], "v": [], "t": []}

            for timestamp, values in sorted(series.items()):
                try:
                    result["c"].append(float(values.get("4. close", 0)))
                    result["o"].append(float(values.get("1. open", 0)))
                    result["h"].append(float(values.get("2. high", 0)))
                    result["l"].append(float(values.get("3. low", 0)))
                    result["v"].append(float(values.get("5. volume", 0)))
                    result["t"].append(timestamp)
                except (ValueError, KeyError):
                    continue

            if len(result["c"]) < 50:
                logger.warning(f"Insufficient Alpha Vantage data: {len(result['c'])} points")
                return None

            return result

        except Exception as e:
            logger.error(f"Alpha Vantage error: {e}")
            return None

    async def _get_from_yahoo(
        self,
        ticker: str,
        interval: str
    ) -> Optional[Dict[str, Any]]:
        """Get data from Yahoo Finance (last resort)"""
        try:
            interval_map = {
                "1min": "1m",
                "5min": "5m",
                "15min": "15m",
                "30min": "30m",
                "1hour": "1h",
                "1day": "1d",
                "1week": "1wk",
                "1month": "1mo"
            }
            yahoo_interval = interval_map.get(interval, "1d")

            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            params = {
                "interval": yahoo_interval,
                "range": "5y"
            }

            logger.info(f"📡 Yahoo Finance: {ticker}")
            response = await self.client.get(url, params=params)

            if response.status_code != 200:
                return None

            data = response.json()
            result_data = data.get("chart", {}).get("result", [{}])[0]

            if result_data.get("error"):
                return None

            quote = result_data.get("indicators", {}).get("quote", [{}])[0]
            timestamps = result_data.get("timestamp", [])

            if not quote or not timestamps:
                return None

            # Filter nulls and build result
            closes = [x for x in quote.get("close", []) if x is not None]
            opens = [x for x in quote.get("open", []) if x is not None]
            highs = [x for x in quote.get("high", []) if x is not None]
            lows = [x for x in quote.get("low", []) if x is not None]
            volumes = [x for x in quote.get("volume", []) if x is not None]

            min_length = min(len(closes), len(opens), len(highs), len(lows), len(volumes))

            if min_length < 50:
                return None

            return {
                "c": closes[:min_length],
                "o": opens[:min_length],
                "h": highs[:min_length],
                "l": lows[:min_length],
                "v": volumes[:min_length],
                "t": [datetime.fromtimestamp(ts).isoformat() for ts in timestamps[:min_length]]
            }

        except Exception as e:
            logger.error(f"Yahoo Finance error: {e}")
            return None

    async def get_quote(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Get current quote from best available source"""
        # Try TwelveData first
        if await self._check_rate_limit(DataSource.TWELVE_DATA):
            try:
                url = "https://api.twelvedata.com/quote"
                params = {
                    "symbol": ticker,
                    "apikey": self.settings.twelvedata_api_key
                }

                response = await self.client.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    if "close" in data:
                        await self._increment_usage(DataSource.TWELVE_DATA)
                        return data
            except Exception as e:
                logger.error(f"Quote error: {e}")

        # Fallback to time series and get latest
        series = await self.get_time_series(ticker, interval="1day", outputsize=1)
        if series and len(series["c"]) > 0:
            return {
                "symbol": ticker,
                "close": series["c"][-1],
                "open": series["o"][-1],
                "high": series["h"][-1],
                "low": series["l"][-1],
                "volume": series["v"][-1],
                "timestamp": series["t"][-1]
            }

        return None

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Global instance
market_data_service = MarketDataService()
