"""
Crypto Data Source Integrations

Supports:
- Binance API (spot, futures, funding rates)
- Coinbase API (spot prices, exchange flows)
- CoinGecko (market data, rankings)
- Real-time WebSocket pricing
"""

import httpx
import asyncio
import json
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import time
import logging
from decimal import Decimal

from app.config import get_settings

logger = logging.getLogger(__name__)


class BinanceClient:
    """
    Binance API client for crypto market data

    Features:
    - Spot prices and OHLCV data
    - Futures data (funding rates, open interest)
    - Exchange flow tracking
    - Real-time ticker data
    - No API key required for public data
    """

    def __init__(self):
        self.settings = get_settings()
        self.base_url = "https://api.binance.com"
        self.futures_url = "https://fapi.binance.com"
        self.client = httpx.AsyncClient(timeout=30.0)

        # Rate limiting: 1200 requests/minute for public endpoints
        self.rate_limit = 1200
        self.requests_this_minute = 0
        self.minute_start = time.time()

    async def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits"""
        now = time.time()

        # Reset counter every minute
        if now - self.minute_start >= 60:
            self.requests_this_minute = 0
            self.minute_start = now

        # Check if we've hit the limit
        if self.requests_this_minute >= self.rate_limit:
            logger.warning(f"⚠️ Binance rate limit reached ({self.rate_limit} req/min)")
            return False

        return True

    async def _make_request(self, base_url: str, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Make API request with rate limiting"""
        if not await self._check_rate_limit():
            await asyncio.sleep(1)  # Wait a bit before retrying
            return None

        try:
            url = f"{base_url}{endpoint}"
            logger.info(f"📡 Binance API call: {endpoint}")

            response = await self.client.get(url, params=params or {})
            self.requests_this_minute += 1

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"🚫 Binance HTTP error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.exception(f"💥 Binance request failed: {e}")
            return None

    async def get_ticker_price(self, symbol: str = "BTCUSDT") -> Optional[Dict[str, Any]]:
        """
        Get current ticker price

        Args:
            symbol: Trading pair (e.g., "BTCUSDT", "ETHUSDT")

        Returns:
            {
                "symbol": "BTCUSDT",
                "price": "43250.50"
            }
        """
        return await self._make_request(self.base_url, "/api/v3/ticker/price", {"symbol": symbol})

    async def get_24h_ticker(self, symbol: str = "BTCUSDT") -> Optional[Dict[str, Any]]:
        """
        Get 24h ticker statistics

        Returns:
            {
                "symbol": "BTCUSDT",
                "priceChange": "1250.50",
                "priceChangePercent": "2.98",
                "lastPrice": "43250.50",
                "volume": "123456.789",
                "quoteVolume": "5345678901.23",
                "openPrice": "42000.00",
                "highPrice": "43500.00",
                "lowPrice": "41800.00"
            }
        """
        return await self._make_request(self.base_url, "/api/v3/ticker/24hr", {"symbol": symbol})

    async def get_klines(
        self,
        symbol: str = "BTCUSDT",
        interval: str = "1h",
        limit: int = 500
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get OHLCV candlestick data

        Args:
            symbol: Trading pair
            interval: Candlestick interval (1m, 5m, 15m, 1h, 4h, 1d, 1w)
            limit: Number of candles (max 1000)

        Returns:
            List of:
            {
                "t": timestamp,
                "o": open,
                "h": high,
                "l": low,
                "c": close,
                "v": volume,
                "qv": quote_volume
            }
        """
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": min(limit, 1000)
        }

        data = await self._make_request(self.base_url, "/api/v3/klines", params)

        if not data:
            return None

        # Transform to our format
        result = []
        for candle in data:
            result.append({
                "t": int(candle[0]),  # Open time
                "o": float(candle[1]),  # Open
                "h": float(candle[2]),  # High
                "l": float(candle[3]),  # Low
                "c": float(candle[4]),  # Close
                "v": float(candle[5]),  # Volume
                "qv": float(candle[7])  # Quote volume
            })

        return result

    async def get_funding_rate(self, symbol: str = "BTCUSDT") -> Optional[Dict[str, Any]]:
        """
        Get current funding rate for perpetual futures

        Returns:
            {
                "symbol": "BTCUSDT",
                "fundingRate": "0.0001",
                "fundingTime": 1234567890000
            }
        """
        return await self._make_request(
            self.futures_url,
            "/fapi/v1/premiumIndex",
            {"symbol": symbol}
        )

    async def get_open_interest(self, symbol: str = "BTCUSDT") -> Optional[Dict[str, Any]]:
        """
        Get current open interest for futures

        Returns:
            {
                "symbol": "BTCUSDT",
                "openInterest": "12345.678",
                "time": 1234567890000
            }
        """
        return await self._make_request(
            self.futures_url,
            "/fapi/v1/openInterest",
            {"symbol": symbol}
        )

    async def get_long_short_ratio(self, symbol: str = "BTCUSDT", period: str = "5m") -> Optional[List[Dict[str, Any]]]:
        """
        Get long/short ratio (top trader sentiment)

        Args:
            symbol: Trading pair
            period: Time period (5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d)

        Returns:
            List of:
            {
                "symbol": "BTCUSDT",
                "longShortRatio": "1.25",
                "longAccount": "0.55",
                "shortAccount": "0.45",
                "timestamp": 1234567890000
            }
        """
        return await self._make_request(
            self.futures_url,
            "/futures/data/globalLongShortAccountRatio",
            {"symbol": symbol, "period": period, "limit": 30}
        )

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


class CoinbaseClient:
    """
    Coinbase API client for crypto market data

    Features:
    - Spot prices
    - Exchange rate data
    - Historical pricing
    - No API key required for public data
    """

    def __init__(self):
        self.settings = get_settings()
        self.base_url = "https://api.coinbase.com"
        self.client = httpx.AsyncClient(timeout=30.0)

    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Make API request"""
        try:
            url = f"{self.base_url}{endpoint}"
            logger.info(f"📡 Coinbase API call: {endpoint}")

            response = await self.client.get(url, params=params or {})

            if response.status_code == 200:
                data = response.json()
                return data.get("data")
            else:
                logger.error(f"🚫 Coinbase HTTP error: {response.status_code}")
                return None

        except Exception as e:
            logger.exception(f"💥 Coinbase request failed: {e}")
            return None

    async def get_spot_price(self, currency_pair: str = "BTC-USD") -> Optional[Dict[str, Any]]:
        """
        Get current spot price

        Returns:
            {
                "base": "BTC",
                "currency": "USD",
                "amount": "43250.50"
            }
        """
        return await self._make_request(f"/v2/prices/{currency_pair}/spot")

    async def get_exchange_rates(self, currency: str = "BTC") -> Optional[Dict[str, Any]]:
        """
        Get exchange rates for a currency

        Returns:
            {
                "currency": "BTC",
                "rates": {
                    "USD": "43250.50",
                    "EUR": "39800.25",
                    ...
                }
            }
        """
        return await self._make_request(f"/v2/exchange-rates", {"currency": currency})

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


class CoinGeckoClient:
    """
    CoinGecko API client for comprehensive crypto market data

    Features:
    - Market data for 10,000+ coins
    - Rankings and market cap data
    - Historical price data
    - DeFi metrics
    - No API key required (free tier: 10-30 calls/min)
    """

    def __init__(self):
        self.settings = get_settings()
        self.base_url = "https://api.coingecko.com/api/v3"
        self.client = httpx.AsyncClient(timeout=30.0)

        # Rate limiting: ~30 calls/minute for free tier
        self.rate_limit = 30
        self.requests_this_minute = 0
        self.minute_start = time.time()

    async def _check_rate_limit(self) -> bool:
        """Check if we're within rate limits"""
        now = time.time()

        # Reset counter every minute
        if now - self.minute_start >= 60:
            self.requests_this_minute = 0
            self.minute_start = now

        # Check if we've hit the limit
        if self.requests_this_minute >= self.rate_limit:
            logger.warning(f"⚠️ CoinGecko rate limit reached ({self.rate_limit} req/min)")
            return False

        return True

    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Optional[Any]:
        """Make API request with rate limiting"""
        if not await self._check_rate_limit():
            await asyncio.sleep(2)  # Wait before retrying
            return None

        try:
            url = f"{self.base_url}{endpoint}"
            logger.info(f"📡 CoinGecko API call: {endpoint}")

            response = await self.client.get(url, params=params or {})
            self.requests_this_minute += 1

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"🚫 CoinGecko HTTP error: {response.status_code}")
                return None

        except Exception as e:
            logger.exception(f"💥 CoinGecko request failed: {e}")
            return None

    async def get_price(
        self,
        coin_ids: str = "bitcoin",
        vs_currencies: str = "usd",
        include_market_cap: bool = True,
        include_24h_vol: bool = True,
        include_24h_change: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Get current price for coins

        Args:
            coin_ids: Comma-separated coin IDs (e.g., "bitcoin,ethereum")
            vs_currencies: Comma-separated currencies (e.g., "usd,eur")

        Returns:
            {
                "bitcoin": {
                    "usd": 43250.50,
                    "usd_market_cap": 845000000000,
                    "usd_24h_vol": 28000000000,
                    "usd_24h_change": 2.5
                }
            }
        """
        params = {
            "ids": coin_ids,
            "vs_currencies": vs_currencies,
            "include_market_cap": include_market_cap,
            "include_24h_vol": include_24h_vol,
            "include_24h_change": include_24h_change
        }

        return await self._make_request("/simple/price", params)

    async def get_coin_market_data(self, coin_id: str = "bitcoin") -> Optional[Dict[str, Any]]:
        """
        Get comprehensive market data for a coin

        Returns:
            {
                "id": "bitcoin",
                "symbol": "btc",
                "name": "Bitcoin",
                "market_data": {
                    "current_price": {"usd": 43250.50},
                    "market_cap": {"usd": 845000000000},
                    "total_volume": {"usd": 28000000000},
                    "price_change_percentage_24h": 2.5,
                    "market_cap_rank": 1,
                    "circulating_supply": 19500000,
                    "total_supply": 21000000
                }
            }
        """
        return await self._make_request(f"/coins/{coin_id}")

    async def get_top_coins(
        self,
        vs_currency: str = "usd",
        order: str = "market_cap_desc",
        per_page: int = 100,
        page: int = 1
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get top coins by market cap

        Returns:
            List of coins with market data
        """
        params = {
            "vs_currency": vs_currency,
            "order": order,
            "per_page": per_page,
            "page": page,
            "sparkline": False
        }

        return await self._make_request("/coins/markets", params)

    async def get_market_chart(
        self,
        coin_id: str = "bitcoin",
        vs_currency: str = "usd",
        days: int = 7
    ) -> Optional[Dict[str, Any]]:
        """
        Get historical market data (price, market cap, volume)

        Returns:
            {
                "prices": [[timestamp, price], ...],
                "market_caps": [[timestamp, market_cap], ...],
                "total_volumes": [[timestamp, volume], ...]
            }
        """
        params = {
            "vs_currency": vs_currency,
            "days": days
        }

        return await self._make_request(f"/coins/{coin_id}/market_chart", params)

    async def get_global_market_data(self) -> Optional[Dict[str, Any]]:
        """
        Get global crypto market data

        Returns:
            {
                "total_market_cap": {"usd": 1700000000000},
                "total_volume": {"usd": 85000000000},
                "market_cap_percentage": {
                    "btc": 49.5,
                    "eth": 18.2
                },
                "market_cap_change_percentage_24h_usd": 1.8
            }
        """
        data = await self._make_request("/global")
        return data.get("data") if data else None

    async def get_defi_market_data(self) -> Optional[Dict[str, Any]]:
        """
        Get DeFi market data

        Returns:
            {
                "defi_market_cap": "125000000000",
                "eth_market_cap": "400000000000",
                "defi_to_eth_ratio": "31.25",
                "trading_volume_24h": "8500000000",
                "defi_dominance": "7.35",
                "top_coin_name": "Lido Staked Ether",
                "top_coin_defi_dominance": 18.5
            }
        """
        return await self._make_request("/global/decentralized_finance_defi")

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


class CryptoDataService:
    """
    Unified crypto data service with multi-source fallback

    Priority order:
    1. Binance (most comprehensive, fastest)
    2. CoinGecko (broad coverage, good for altcoins)
    3. Coinbase (reliable fallback)
    """

    def __init__(self):
        self.binance = BinanceClient()
        self.coingecko = CoinGeckoClient()
        self.coinbase = CoinbaseClient()

    async def get_realtime_price(self, symbol: str = "BTC", quote_currency: str = "USDT") -> Optional[Dict[str, Any]]:
        """
        Get real-time price with multi-source fallback

        Returns:
            {
                "symbol": "BTC",
                "price": 43250.50,
                "source": "binance",
                "timestamp": 1234567890
            }
        """
        # Try Binance first
        binance_symbol = f"{symbol}{quote_currency}"
        ticker = await self.binance.get_ticker_price(binance_symbol)

        if ticker:
            return {
                "symbol": symbol,
                "price": float(ticker["price"]),
                "source": "binance",
                "timestamp": int(time.time())
            }

        # Fallback to CoinGecko
        coin_id_map = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "BNB": "binancecoin",
            "SOL": "solana",
            "ADA": "cardano",
            "XRP": "ripple",
            "DOT": "polkadot",
            "DOGE": "dogecoin",
            "AVAX": "avalanche-2",
            "MATIC": "matic-network"
        }

        coin_id = coin_id_map.get(symbol, symbol.lower())
        price_data = await self.coingecko.get_price(coin_id, "usd")

        if price_data and coin_id in price_data:
            return {
                "symbol": symbol,
                "price": float(price_data[coin_id]["usd"]),
                "source": "coingecko",
                "timestamp": int(time.time())
            }

        # Last resort: Coinbase
        coinbase_pair = f"{symbol}-USD"
        spot = await self.coinbase.get_spot_price(coinbase_pair)

        if spot:
            return {
                "symbol": symbol,
                "price": float(spot["amount"]),
                "source": "coinbase",
                "timestamp": int(time.time())
            }

        logger.error(f"Failed to get price for {symbol} from all sources")
        return None

    async def close(self):
        """Close all clients"""
        await self.binance.close()
        await self.coingecko.close()
        await self.coinbase.close()


# Global instance
crypto_data_service = CryptoDataService()
