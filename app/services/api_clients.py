import httpx
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import asyncio
import time

from app.config import get_settings


class TwelveDataClient:
    """
    TwelveData API client with rate limiting and caching

    Limits: 800 calls/day (currently ~150/day = 19% usage)
    Base URL: https://api.twelvedata.com
    """

    def __init__(self):
        self.settings = get_settings()
        self.base_url = "https://api.twelvedata.com"
        self.client = httpx.AsyncClient(timeout=30.0)

        # Rate limiting: max 800 calls per day
        self.daily_limit = 800
        self.calls_today = 0
        self.reset_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

    async def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits"""
        now = datetime.now()

        # Reset counter daily
        if now >= self.reset_time:
            self.calls_today = 0
            self.reset_time = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

        # Check if we've hit the limit
        if self.calls_today >= self.daily_limit:
            print(f"⚠️ TwelveData daily limit reached ({self.daily_limit} calls)")
            return False

        return True

    async def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make API request with rate limiting and error handling"""
        if not await self._check_rate_limit():
            return None

        try:
            # Add API key to params
            params["apikey"] = self.settings.twelvedata_api_key

            url = f"{self.base_url}/{endpoint}"
            print(f"📡 TwelveData API call: {endpoint} for {params.get('symbol', 'unknown')}")

            response = await self.client.get(url, params=params)
            self.calls_today += 1

            if response.status_code == 200:
                data = response.json()

                # Check for API errors
                if "status" in data and data["status"] == "error":
                    print(f"🚫 TwelveData API error: {data.get('message', 'Unknown error')}")
                    return None

                return data
            else:
                print(f"🚫 TwelveData HTTP error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"💥 TwelveData request failed: {e}")
            return None

    async def get_time_series(
        self,
        ticker: str,
        interval: str = "1day",
        outputsize: int = 100
    ) -> Optional[Dict[str, Any]]:
        """
        Get OHLCV time series data

        Args:
            ticker: Stock symbol (e.g., "AAPL")
            interval: Time interval ("1day", "1week", "1month", etc.)
            outputsize: Number of data points (max varies by interval)

        Returns:
            {
                "c": [closes],
                "o": [opens],
                "h": [highs],
                "l": [lows],
                "v": [volumes],
                "t": [timestamps]
            }
        """
        params = {
            "symbol": ticker,
            "interval": interval,
            "outputsize": min(outputsize, 5000),  # API limit
            "format": "json"
        }

        data = await self._make_request("time_series", params)

        if not data or "values" not in data:
            return None

        # Transform TwelveData format to our internal format
        values = data["values"]

        # Convert timestamps and extract OHLCV
        result = {
            "c": [],  # closes
            "o": [],  # opens
            "h": [],  # highs
            "l": [],  # lows
            "v": [],  # volumes
            "t": []   # timestamps
        }

        for value in reversed(values):  # TwelveData returns newest first
            try:
                result["c"].append(float(value["close"]))
                result["o"].append(float(value["open"]))
                result["h"].append(float(value["high"]))
                result["l"].append(float(value["low"]))
                result["v"].append(float(value["volume"]))
                result["t"].append(value["datetime"])
            except (ValueError, KeyError):
                continue

        # Validate we got data
        if len(result["c"]) < 50:
            print(f"⚠️ Insufficient data for {ticker}: {len(result['c'])} points")
            return None

        return result

    async def get_quote(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get current quote data

        Returns:
            {
                "symbol": "AAPL",
                "name": "Apple Inc",
                "exchange": "NASDAQ",
                "datetime": "2023-11-06 16:00:00",
                "open": "179.18",
                "high": "179.25",
                "low": "175.58",
                "close": "179.23",
                "volume": "63791288",
                "previous_close": "178.02"
            }
        """
        params = {
            "symbol": ticker,
            "format": "json"
        }

        return await self._make_request("quote", params)

    async def get_statistics(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Get stock statistics (52w high/low, etc.)

        Note: This endpoint might not be available in free tier
        """
        params = {
            "symbol": ticker,
            "format": "json"
        }

        return await self._make_request("statistics", params)

    async def get_usage_stats(self) -> Dict[str, Any]:
        """Get current API usage statistics"""
        return {
            "calls_today": self.calls_today,
            "daily_limit": self.daily_limit,
            "usage_percent": (self.calls_today / self.daily_limit) * 100,
            "reset_time": self.reset_time.isoformat()
        }

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Global instance
twelve_data_client = TwelveDataClient()


# Yahoo Finance fallback (for compatibility during migration)
class YahooFinanceClient:
    """
    Yahoo Finance API client (fallback during migration)

    Uses the same API endpoints as the n8n workflow for compatibility
    """

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get_time_series(
        self,
        ticker: str,
        interval: str = "1d",
        range_param: str = "5y"
    ) -> Optional[Dict[str, Any]]:
        """
        Get OHLCV data from Yahoo Finance (same as n8n workflow)

        Returns same format as TwelveData for compatibility
        """
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            params = {
                "interval": interval,
                "range": range_param
            }

            print(f"📡 Yahoo Finance API call: {ticker}")

            response = await self.client.get(url, params=params)

            if response.status_code != 200:
                print(f"🚫 Yahoo Finance HTTP error: {response.status_code}")
                return None

            data = response.json()

            # Check for Yahoo Finance errors
            result = data.get("chart", {}).get("result", [{}])[0]
            if result.get("error"):
                print(f"🚫 Yahoo Finance error: {result['error']['description']}")
                return None

            # Extract quote data
            quote = result.get("indicators", {}).get("quote", [{}])[0]
            timestamps = result.get("timestamp", [])

            if not quote or not timestamps:
                print("⚠️ No quote data in Yahoo Finance response")
                return None

            # Extract OHLCV (filter out nulls)
            closes = [x for x in quote.get("close", []) if x is not None]
            opens = [x for x in quote.get("open", []) if x is not None]
            highs = [x for x in quote.get("high", []) if x is not None]
            lows = [x for x in quote.get("low", []) if x is not None]
            volumes = [x for x in quote.get("volume", []) if x is not None]

            # Convert timestamps
            datetime_strings = [datetime.fromtimestamp(ts).isoformat() for ts in timestamps]

            # Validate data length
            min_length = min(len(closes), len(opens), len(highs), len(lows), len(volumes))
            if min_length < 50:
                print(f"⚠️ Insufficient Yahoo Finance data for {ticker}: {min_length} points")
                return None

            return {
                "c": closes[:min_length],
                "o": opens[:min_length],
                "h": highs[:min_length],
                "l": lows[:min_length],
                "v": volumes[:min_length],
                "t": datetime_strings[:min_length]
            }

        except Exception as e:
            print(f"💥 Yahoo Finance request failed: {e}")
            return None

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Global instance for migration
yahoo_client = YahooFinanceClient()
