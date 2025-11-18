"""
Options Data Service with Multi-Source Integration
Provides comprehensive options data from Tradier, CBOE, and other sources
"""
import httpx
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timedelta
import asyncio
import logging
from enum import Enum
import pandas as pd
import numpy as np
from scipy.stats import norm

from app.config import get_settings
from app.services.cache import get_cache_service

logger = logging.getLogger(__name__)


class OptionsDataSource(str, Enum):
    TRADIER = "tradier"
    CBOE = "cboe"
    UNUSUAL_WHALES = "unusual_whales"
    CACHE = "cache"


class OptionType(str, Enum):
    CALL = "call"
    PUT = "put"


class OptionsDataService:
    """
    Unified options data service with multi-source support

    Features:
    - Real-time options chains
    - Unusual options activity detection
    - Put/Call ratio analysis
    - Open interest analysis
    - IV percentile calculations
    - Greeks calculations
    - Flow and dark pool data
    """

    def __init__(self):
        self.settings = get_settings()
        self.cache = get_cache_service()
        self.client = httpx.AsyncClient(timeout=30.0)

        # API base URLs
        self.tradier_base = (
            "https://sandbox.tradier.com/v1"
            if self.settings.tradier_sandbox
            else "https://api.tradier.com/v1"
        )
        self.cboe_base = "https://cdn.cboe.com/api/global"

        # Usage tracking
        self.usage_key_prefix = "options_api_usage"

    async def get_options_chain(
        self,
        symbol: str,
        expiration: Optional[str] = None,
        strike_range: Optional[Tuple[float, float]] = None
    ) -> Dict[str, Any]:
        """
        Get options chain for a symbol

        Args:
            symbol: Stock ticker
            expiration: Expiration date (YYYY-MM-DD), defaults to nearest
            strike_range: (min_strike, max_strike) to filter strikes

        Returns:
            Dictionary with calls and puts data
        """
        cache_key = f"options_chain:{symbol}:{expiration or 'nearest'}"

        # Check cache first
        cached = await self.cache.get(cache_key)
        if cached:
            logger.info(f"✓ Options chain cache hit for {symbol}")
            return cached

        try:
            # Try Tradier first (most comprehensive)
            if self.settings.tradier_api_key:
                chain = await self._get_tradier_chain(symbol, expiration, strike_range)
                if chain:
                    await self.cache.set(cache_key, chain, ttl=300)  # 5 min cache
                    return chain

            # Fallback to CBOE
            if self.settings.cboe_api_key:
                chain = await self._get_cboe_chain(symbol, expiration, strike_range)
                if chain:
                    await self.cache.set(cache_key, chain, ttl=300)
                    return chain

            raise Exception("No options data source available")

        except Exception as e:
            logger.error(f"Error getting options chain for {symbol}: {e}")
            return {"error": str(e), "calls": [], "puts": []}

    async def _get_tradier_chain(
        self,
        symbol: str,
        expiration: Optional[str],
        strike_range: Optional[Tuple[float, float]]
    ) -> Optional[Dict[str, Any]]:
        """Get options chain from Tradier"""
        try:
            # Get expirations if not specified
            if not expiration:
                exp_response = await self.client.get(
                    f"{self.tradier_base}/markets/options/expirations",
                    headers={
                        "Authorization": f"Bearer {self.settings.tradier_api_key}",
                        "Accept": "application/json"
                    },
                    params={"symbol": symbol}
                )
                exp_data = exp_response.json()
                expirations = exp_data.get("expirations", {}).get("date", [])
                expiration = expirations[0] if expirations else None

                if not expiration:
                    logger.warning(f"No expirations found for {symbol}")
                    return None

            # Get options chain
            response = await self.client.get(
                f"{self.tradier_base}/markets/options/chains",
                headers={
                    "Authorization": f"Bearer {self.settings.tradier_api_key}",
                    "Accept": "application/json"
                },
                params={
                    "symbol": symbol,
                    "expiration": expiration,
                    "greeks": "true"
                }
            )

            await self._increment_usage(OptionsDataSource.TRADIER)

            if response.status_code != 200:
                logger.error(f"Tradier API error: {response.status_code}")
                return None

            data = response.json()
            options = data.get("options", {}).get("option", [])

            if not options:
                return {"calls": [], "puts": [], "expiration": expiration}

            # Filter and organize options
            calls = []
            puts = []

            for opt in options:
                # Apply strike range filter if specified
                if strike_range:
                    strike = float(opt.get("strike", 0))
                    if strike < strike_range[0] or strike > strike_range[1]:
                        continue

                option_data = {
                    "symbol": opt.get("symbol"),
                    "strike": float(opt.get("strike", 0)),
                    "bid": float(opt.get("bid", 0)),
                    "ask": float(opt.get("ask", 0)),
                    "last": float(opt.get("last", 0)),
                    "volume": int(opt.get("volume", 0)),
                    "open_interest": int(opt.get("open_interest", 0)),
                    "implied_volatility": float(opt.get("greeks", {}).get("mid_iv", 0)) * 100,
                    "delta": float(opt.get("greeks", {}).get("delta", 0)),
                    "gamma": float(opt.get("greeks", {}).get("gamma", 0)),
                    "theta": float(opt.get("greeks", {}).get("theta", 0)),
                    "vega": float(opt.get("greeks", {}).get("vega", 0)),
                    "rho": float(opt.get("greeks", {}).get("rho", 0)),
                }

                if opt.get("option_type") == "call":
                    calls.append(option_data)
                else:
                    puts.append(option_data)

            return {
                "symbol": symbol,
                "expiration": expiration,
                "calls": calls,
                "puts": puts,
                "source": "tradier"
            }

        except Exception as e:
            logger.error(f"Error fetching Tradier chain: {e}")
            return None

    async def _get_cboe_chain(
        self,
        symbol: str,
        expiration: Optional[str],
        strike_range: Optional[Tuple[float, float]]
    ) -> Optional[Dict[str, Any]]:
        """Get options chain from CBOE (delayed data, free)"""
        try:
            # CBOE provides delayed options data via their API
            response = await self.client.get(
                f"{self.cboe_base}/delayed_quotes/options/{symbol}.json"
            )

            await self._increment_usage(OptionsDataSource.CBOE)

            if response.status_code != 200:
                return None

            data = response.json()
            # Parse CBOE data structure (simplified example)
            # CBOE data structure varies, this is a placeholder

            return {
                "symbol": symbol,
                "expiration": expiration,
                "calls": [],
                "puts": [],
                "source": "cboe",
                "note": "CBOE data is delayed 15 minutes"
            }

        except Exception as e:
            logger.error(f"Error fetching CBOE chain: {e}")
            return None

    async def get_unusual_activity(
        self,
        symbol: Optional[str] = None,
        min_premium: float = 30000,
        min_volume_oi_ratio: float = 2.0
    ) -> List[Dict[str, Any]]:
        """
        Detect unusual options activity

        Args:
            symbol: Specific symbol or None for market-wide scan
            min_premium: Minimum premium threshold ($)
            min_volume_oi_ratio: Minimum volume/OI ratio for unusual activity

        Returns:
            List of unusual options trades
        """
        cache_key = f"unusual_activity:{symbol or 'market'}:{min_premium}:{min_volume_oi_ratio}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        try:
            unusual_trades = []

            # Get options chain
            chain = await self.get_options_chain(symbol) if symbol else None

            if chain:
                # Analyze both calls and puts
                for opt in chain.get("calls", []) + chain.get("puts", []):
                    volume = opt.get("volume", 0)
                    oi = opt.get("open_interest", 1)  # Avoid division by zero
                    premium = opt.get("last", 0) * volume * 100  # Contract value

                    # Check for unusual activity
                    vol_oi_ratio = volume / oi if oi > 0 else 0

                    if premium >= min_premium and vol_oi_ratio >= min_volume_oi_ratio:
                        unusual_trades.append({
                            "symbol": opt.get("symbol"),
                            "strike": opt.get("strike"),
                            "type": "call" if "C" in opt.get("symbol", "") else "put",
                            "volume": volume,
                            "open_interest": oi,
                            "vol_oi_ratio": round(vol_oi_ratio, 2),
                            "premium": round(premium, 2),
                            "iv": opt.get("implied_volatility", 0),
                            "sentiment": "bullish" if "C" in opt.get("symbol", "") else "bearish"
                        })

            # Sort by premium (largest trades first)
            unusual_trades.sort(key=lambda x: x["premium"], reverse=True)

            await self.cache.set(cache_key, unusual_trades, ttl=300)  # 5 min cache
            return unusual_trades

        except Exception as e:
            logger.error(f"Error detecting unusual activity: {e}")
            return []

    async def get_put_call_ratio(
        self,
        symbol: str,
        expiration: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculate put/call ratios

        Returns:
            Dictionary with volume and OI based P/C ratios
        """
        cache_key = f"put_call_ratio:{symbol}:{expiration or 'nearest'}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        try:
            chain = await self.get_options_chain(symbol, expiration)

            calls = chain.get("calls", [])
            puts = chain.get("puts", [])

            # Calculate volume-based P/C ratio
            call_volume = sum(opt.get("volume", 0) for opt in calls)
            put_volume = sum(opt.get("volume", 0) for opt in puts)
            volume_pc_ratio = put_volume / call_volume if call_volume > 0 else 0

            # Calculate OI-based P/C ratio
            call_oi = sum(opt.get("open_interest", 0) for opt in calls)
            put_oi = sum(opt.get("open_interest", 0) for opt in puts)
            oi_pc_ratio = put_oi / call_oi if call_oi > 0 else 0

            result = {
                "symbol": symbol,
                "expiration": chain.get("expiration"),
                "call_volume": call_volume,
                "put_volume": put_volume,
                "volume_pc_ratio": round(volume_pc_ratio, 3),
                "call_oi": call_oi,
                "put_oi": put_oi,
                "oi_pc_ratio": round(oi_pc_ratio, 3),
                "sentiment": self._interpret_pc_ratio(volume_pc_ratio),
                "timestamp": datetime.now().isoformat()
            }

            await self.cache.set(cache_key, result, ttl=300)
            return result

        except Exception as e:
            logger.error(f"Error calculating P/C ratio: {e}")
            return {"error": str(e)}

    def _interpret_pc_ratio(self, ratio: float) -> str:
        """Interpret put/call ratio sentiment"""
        if ratio > 1.5:
            return "very_bearish"
        elif ratio > 1.0:
            return "bearish"
        elif ratio > 0.7:
            return "neutral"
        elif ratio > 0.5:
            return "bullish"
        else:
            return "very_bullish"

    async def get_open_interest_analysis(
        self,
        symbol: str,
        expiration: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze open interest distribution

        Returns:
            OI analysis with support/resistance levels
        """
        cache_key = f"oi_analysis:{symbol}:{expiration or 'nearest'}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        try:
            chain = await self.get_options_chain(symbol, expiration)

            calls = chain.get("calls", [])
            puts = chain.get("puts", [])

            # Find max pain (strike with highest total OI)
            strike_oi = {}
            for opt in calls + puts:
                strike = opt.get("strike")
                oi = opt.get("open_interest", 0)
                strike_oi[strike] = strike_oi.get(strike, 0) + oi

            max_pain_strike = max(strike_oi.items(), key=lambda x: x[1])[0] if strike_oi else 0

            # Find call and put walls (strikes with unusually high OI)
            call_oi_by_strike = {opt["strike"]: opt["open_interest"] for opt in calls}
            put_oi_by_strike = {opt["strike"]: opt["open_interest"] for opt in puts}

            avg_call_oi = np.mean(list(call_oi_by_strike.values())) if call_oi_by_strike else 0
            avg_put_oi = np.mean(list(put_oi_by_strike.values())) if put_oi_by_strike else 0

            call_walls = [
                {"strike": k, "oi": v}
                for k, v in call_oi_by_strike.items()
                if v > avg_call_oi * 2
            ]
            put_walls = [
                {"strike": k, "oi": v}
                for k, v in put_oi_by_strike.items()
                if v > avg_put_oi * 2
            ]

            result = {
                "symbol": symbol,
                "expiration": chain.get("expiration"),
                "max_pain": max_pain_strike,
                "total_call_oi": sum(call_oi_by_strike.values()),
                "total_put_oi": sum(put_oi_by_strike.values()),
                "call_walls": sorted(call_walls, key=lambda x: x["oi"], reverse=True)[:5],
                "put_walls": sorted(put_walls, key=lambda x: x["oi"], reverse=True)[:5],
                "resistance_levels": [w["strike"] for w in call_walls[:3]],
                "support_levels": [w["strike"] for w in put_walls[:3]],
            }

            await self.cache.set(cache_key, result, ttl=600)
            return result

        except Exception as e:
            logger.error(f"Error analyzing open interest: {e}")
            return {"error": str(e)}

    async def get_iv_percentile(
        self,
        symbol: str,
        lookback_days: int = 252
    ) -> Dict[str, Any]:
        """
        Calculate IV percentile (current IV vs historical IV distribution)

        Args:
            symbol: Stock ticker
            lookback_days: Historical period for percentile calculation

        Returns:
            IV percentile and rank
        """
        cache_key = f"iv_percentile:{symbol}:{lookback_days}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        try:
            # Get current ATM options IV
            chain = await self.get_options_chain(symbol)

            # Find ATM option (closest to current price)
            # In production, you'd fetch current stock price
            calls = chain.get("calls", [])
            if not calls:
                return {"error": "No options data available"}

            # Get mid-strike as proxy for ATM
            strikes = [opt["strike"] for opt in calls]
            mid_strike = sorted(strikes)[len(strikes) // 2]

            atm_option = next((opt for opt in calls if opt["strike"] == mid_strike), None)
            current_iv = atm_option.get("implied_volatility", 0) if atm_option else 0

            # In production, fetch historical IV data
            # For now, simulate with mock data
            # historical_ivs = await self._get_historical_iv(symbol, lookback_days)

            # Mock calculation (replace with real historical data)
            mock_iv_range = (current_iv * 0.5, current_iv * 1.5)
            iv_percentile = 50.0  # Placeholder
            iv_rank = 50.0  # Placeholder

            result = {
                "symbol": symbol,
                "current_iv": round(current_iv, 2),
                "iv_percentile": iv_percentile,
                "iv_rank": iv_rank,
                "52_week_iv_low": round(mock_iv_range[0], 2),
                "52_week_iv_high": round(mock_iv_range[1], 2),
                "interpretation": self._interpret_iv_percentile(iv_percentile),
                "lookback_days": lookback_days
            }

            await self.cache.set(cache_key, result, ttl=3600)
            return result

        except Exception as e:
            logger.error(f"Error calculating IV percentile: {e}")
            return {"error": str(e)}

    def _interpret_iv_percentile(self, percentile: float) -> str:
        """Interpret IV percentile"""
        if percentile > 80:
            return "very_high_iv"
        elif percentile > 60:
            return "high_iv"
        elif percentile > 40:
            return "normal_iv"
        elif percentile > 20:
            return "low_iv"
        else:
            return "very_low_iv"

    async def calculate_greeks(
        self,
        spot_price: float,
        strike: float,
        time_to_expiry: float,  # In years
        volatility: float,  # Annualized
        risk_free_rate: float = 0.05,
        option_type: str = "call"
    ) -> Dict[str, float]:
        """
        Calculate Black-Scholes Greeks

        Args:
            spot_price: Current stock price
            strike: Strike price
            time_to_expiry: Time to expiration in years
            volatility: Implied volatility (decimal, e.g., 0.30 for 30%)
            risk_free_rate: Risk-free rate (decimal)
            option_type: "call" or "put"

        Returns:
            Dictionary with delta, gamma, theta, vega, rho
        """
        try:
            # Black-Scholes formula
            d1 = (np.log(spot_price / strike) + (risk_free_rate + 0.5 * volatility ** 2) * time_to_expiry) / \
                 (volatility * np.sqrt(time_to_expiry))
            d2 = d1 - volatility * np.sqrt(time_to_expiry)

            # Delta
            if option_type == "call":
                delta = norm.cdf(d1)
            else:
                delta = norm.cdf(d1) - 1

            # Gamma (same for calls and puts)
            gamma = norm.pdf(d1) / (spot_price * volatility * np.sqrt(time_to_expiry))

            # Theta (time decay)
            if option_type == "call":
                theta = (-spot_price * norm.pdf(d1) * volatility / (2 * np.sqrt(time_to_expiry)) -
                        risk_free_rate * strike * np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(d2)) / 365
            else:
                theta = (-spot_price * norm.pdf(d1) * volatility / (2 * np.sqrt(time_to_expiry)) +
                        risk_free_rate * strike * np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(-d2)) / 365

            # Vega (same for calls and puts)
            vega = spot_price * norm.pdf(d1) * np.sqrt(time_to_expiry) / 100

            # Rho
            if option_type == "call":
                rho = strike * time_to_expiry * np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(d2) / 100
            else:
                rho = -strike * time_to_expiry * np.exp(-risk_free_rate * time_to_expiry) * norm.cdf(-d2) / 100

            return {
                "delta": round(delta, 4),
                "gamma": round(gamma, 4),
                "theta": round(theta, 4),
                "vega": round(vega, 4),
                "rho": round(rho, 4)
            }

        except Exception as e:
            logger.error(f"Error calculating Greeks: {e}")
            return {"error": str(e)}

    async def _increment_usage(self, source: OptionsDataSource):
        """Increment API usage counter"""
        try:
            key = f"{self.usage_key_prefix}:{source.value}"
            current = await self.cache.get(key) or 0
            await self.cache.set(key, int(current) + 1, ttl=86400)
        except Exception as e:
            logger.warning(f"Error incrementing usage for {source}: {e}")

    async def get_usage_stats(self) -> Dict[str, Any]:
        """Get API usage statistics"""
        try:
            tradier_usage = await self.cache.get(f"{self.usage_key_prefix}:tradier") or 0
            cboe_usage = await self.cache.get(f"{self.usage_key_prefix}:cboe") or 0

            return {
                "tradier": {
                    "used": int(tradier_usage),
                    "limit": self.settings.tradier_daily_limit,
                    "remaining": self.settings.tradier_daily_limit - int(tradier_usage)
                },
                "cboe": {
                    "used": int(cboe_usage),
                    "limit": self.settings.cboe_daily_limit,
                    "remaining": self.settings.cboe_daily_limit - int(cboe_usage)
                }
            }
        except Exception as e:
            logger.error(f"Error getting usage stats: {e}")
            return {"error": str(e)}

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Singleton instance
_options_service: Optional[OptionsDataService] = None


def get_options_service() -> OptionsDataService:
    """Get or create options data service singleton"""
    global _options_service
    if _options_service is None:
        _options_service = OptionsDataService()
    return _options_service
