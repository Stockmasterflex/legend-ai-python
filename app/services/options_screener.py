"""
Options Screener Service
Scans for high IV stocks, unusual activity, sweeps, and dark pool trades
"""
import httpx
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import asyncio
import logging
from enum import Enum
import pandas as pd
import numpy as np

from app.config import get_settings
from app.services.cache import get_cache_service
from app.services.options_data import get_options_service

logger = logging.getLogger(__name__)


class ActivityType(str, Enum):
    SWEEP = "sweep"
    BLOCK = "block"
    SPLIT = "split"
    UNUSUAL_VOLUME = "unusual_volume"
    DARK_POOL = "dark_pool"


class Sentiment(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


class OptionsScreener:
    """
    Advanced options screener for finding trading opportunities

    Features:
    - High IV rank stocks
    - Unusual volume detection
    - Large block trades
    - Sweep detection
    - Dark pool activity
    """

    def __init__(self):
        self.settings = get_settings()
        self.cache = get_cache_service()
        self.options_service = get_options_service()
        self.client = httpx.AsyncClient(timeout=30.0)

        # Screener thresholds
        self.min_volume_for_unusual = 1000
        self.block_trade_min_premium = 100000  # $100k
        self.sweep_min_legs = 4  # Minimum exchanges hit
        self.dark_pool_min_size = 10000  # shares

    async def scan_high_iv_stocks(
        self,
        symbols: Optional[List[str]] = None,
        min_iv_rank: float = 70.0,
        max_results: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Scan for stocks with high IV rank

        Args:
            symbols: List of symbols to scan, or None for market-wide
            min_iv_rank: Minimum IV rank percentile (0-100)
            max_results: Maximum results to return

        Returns:
            List of high IV stocks with details
        """
        cache_key = f"high_iv_scan:{min_iv_rank}:{max_results}"

        cached = await self.cache.get(cache_key)
        if cached:
            logger.info(f"✓ High IV scan cache hit")
            return cached

        try:
            # Default watchlist if none provided
            if not symbols:
                symbols = await self._get_default_watchlist()

            high_iv_stocks = []

            # Scan each symbol
            for symbol in symbols[:max_results]:  # Limit to avoid rate limits
                try:
                    iv_data = await self.options_service.get_iv_percentile(symbol)

                    if iv_data.get("iv_rank", 0) >= min_iv_rank:
                        high_iv_stocks.append({
                            "symbol": symbol,
                            "current_iv": iv_data.get("current_iv"),
                            "iv_rank": iv_data.get("iv_rank"),
                            "iv_percentile": iv_data.get("iv_percentile"),
                            "52w_iv_low": iv_data.get("52_week_iv_low"),
                            "52w_iv_high": iv_data.get("52_week_iv_high"),
                            "interpretation": iv_data.get("interpretation"),
                            "timestamp": datetime.now().isoformat()
                        })

                    # Small delay to avoid rate limits
                    await asyncio.sleep(0.1)

                except Exception as e:
                    logger.warning(f"Error scanning {symbol}: {e}")
                    continue

            # Sort by IV rank (highest first)
            high_iv_stocks.sort(key=lambda x: x["iv_rank"], reverse=True)

            await self.cache.set(cache_key, high_iv_stocks, ttl=900)  # 15 min cache
            return high_iv_stocks[:max_results]

        except Exception as e:
            logger.error(f"Error scanning high IV stocks: {e}")
            return []

    async def detect_unusual_volume(
        self,
        symbol: str,
        lookback_days: int = 20
    ) -> Dict[str, Any]:
        """
        Detect unusual options volume spikes

        Args:
            symbol: Stock ticker
            lookback_days: Days to compare against average

        Returns:
            Unusual volume analysis
        """
        cache_key = f"unusual_volume:{symbol}:{lookback_days}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        try:
            # Get current options chain
            chain = await self.options_service.get_options_chain(symbol)

            calls = chain.get("calls", [])
            puts = chain.get("puts", [])

            # Calculate current total volume
            current_call_volume = sum(opt.get("volume", 0) for opt in calls)
            current_put_volume = sum(opt.get("volume", 0) for opt in puts)
            total_volume = current_call_volume + current_put_volume

            # In production, fetch historical average volume
            # For now, use mock data
            avg_volume = total_volume * 0.7  # Simulate 30% above average
            volume_ratio = total_volume / avg_volume if avg_volume > 0 else 0

            # Find most active strikes
            call_volume_by_strike = {}
            put_volume_by_strike = {}

            for opt in calls:
                strike = opt["strike"]
                call_volume_by_strike[strike] = call_volume_by_strike.get(strike, 0) + opt.get("volume", 0)

            for opt in puts:
                strike = opt["strike"]
                put_volume_by_strike[strike] = put_volume_by_strike.get(strike, 0) + opt.get("volume", 0)

            # Top strikes by volume
            top_call_strikes = sorted(
                call_volume_by_strike.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]

            top_put_strikes = sorted(
                put_volume_by_strike.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]

            result = {
                "symbol": symbol,
                "current_call_volume": current_call_volume,
                "current_put_volume": current_put_volume,
                "total_volume": total_volume,
                "avg_volume": int(avg_volume),
                "volume_ratio": round(volume_ratio, 2),
                "is_unusual": volume_ratio > 2.0,
                "top_call_strikes": [{"strike": k, "volume": v} for k, v in top_call_strikes],
                "top_put_strikes": [{"strike": k, "volume": v} for k, v in top_put_strikes],
                "sentiment": "bullish" if current_call_volume > current_put_volume else "bearish",
                "timestamp": datetime.now().isoformat()
            }

            await self.cache.set(cache_key, result, ttl=300)
            return result

        except Exception as e:
            logger.error(f"Error detecting unusual volume for {symbol}: {e}")
            return {"error": str(e)}

    async def detect_block_trades(
        self,
        symbol: str,
        min_premium: float = 100000
    ) -> List[Dict[str, Any]]:
        """
        Detect large block trades (institutional activity)

        Args:
            symbol: Stock ticker
            min_premium: Minimum premium for block trade ($)

        Returns:
            List of detected block trades
        """
        cache_key = f"block_trades:{symbol}:{min_premium}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        try:
            # Get options chain
            chain = await self.options_service.get_options_chain(symbol)

            block_trades = []

            for opt in chain.get("calls", []) + chain.get("puts", []):
                volume = opt.get("volume", 0)
                last_price = opt.get("last", 0)
                premium = volume * last_price * 100  # Contract value

                # Detect blocks: high premium, low volume (single large trade)
                if premium >= min_premium and volume < 500:  # Large $ but concentrated
                    block_trades.append({
                        "symbol": opt.get("symbol"),
                        "strike": opt.get("strike"),
                        "type": "call" if "C" in opt.get("symbol", "") else "put",
                        "volume": volume,
                        "premium": round(premium, 2),
                        "price": last_price,
                        "open_interest": opt.get("open_interest", 0),
                        "iv": opt.get("implied_volatility", 0),
                        "activity_type": "block",
                        "sentiment": "bullish" if "C" in opt.get("symbol", "") else "bearish",
                        "timestamp": datetime.now().isoformat()
                    })

            # Sort by premium (largest first)
            block_trades.sort(key=lambda x: x["premium"], reverse=True)

            await self.cache.set(cache_key, block_trades, ttl=300)
            return block_trades

        except Exception as e:
            logger.error(f"Error detecting block trades for {symbol}: {e}")
            return []

    async def detect_sweeps(
        self,
        symbol: str,
        min_premium: float = 50000
    ) -> List[Dict[str, Any]]:
        """
        Detect sweep orders (aggressive multi-exchange orders)

        Sweeps indicate urgency and strong conviction

        Args:
            symbol: Stock ticker
            min_premium: Minimum premium threshold

        Returns:
            List of detected sweep orders
        """
        cache_key = f"sweeps:{symbol}:{min_premium}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        try:
            # Get unusual activity (sweeps are subset of unusual activity)
            unusual = await self.options_service.get_unusual_activity(
                symbol,
                min_premium=min_premium,
                min_volume_oi_ratio=1.5
            )

            sweeps = []

            for trade in unusual:
                # Heuristic: High volume + high premium + above ask = likely sweep
                # In production, you'd need real-time trade data with exchange info
                volume = trade.get("volume", 0)
                premium = trade.get("premium", 0)

                # Sweep characteristics:
                # 1. Large premium
                # 2. Executed quickly (inferred from volume spike)
                # 3. Multiple exchanges (would need Level 2 data)
                if premium >= min_premium and volume > 500:
                    sweeps.append({
                        **trade,
                        "activity_type": "sweep",
                        "aggression": "high",
                        "conviction": "strong",
                        "note": "Detected via volume/premium heuristic"
                    })

            await self.cache.set(cache_key, sweeps, ttl=300)
            return sweeps

        except Exception as e:
            logger.error(f"Error detecting sweeps for {symbol}: {e}")
            return []

    async def detect_dark_pool_activity(
        self,
        symbol: str,
        min_size: int = 10000
    ) -> List[Dict[str, Any]]:
        """
        Detect dark pool activity (off-exchange large trades)

        Note: Requires data feed from Unusual Whales or similar provider

        Args:
            symbol: Stock ticker
            min_size: Minimum share size

        Returns:
            List of dark pool prints
        """
        cache_key = f"dark_pool:{symbol}:{min_size}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        try:
            # This requires a specialized data provider like Unusual Whales
            # For now, return mock structure
            dark_pool_trades = []

            if self.settings.unusual_whales_api_key:
                # Example API call structure (pseudo-code)
                # response = await self.client.get(
                #     "https://api.unusualwhales.com/darkpool",
                #     headers={"Authorization": f"Bearer {self.settings.unusual_whales_api_key}"},
                #     params={"symbol": symbol, "min_size": min_size}
                # )
                # dark_pool_trades = response.json()

                # For now, return placeholder
                dark_pool_trades = [{
                    "symbol": symbol,
                    "size": min_size,
                    "price": 0.0,
                    "premium": 0.0,
                    "exchange": "dark_pool",
                    "sentiment": "neutral",
                    "note": "Requires Unusual Whales API key",
                    "timestamp": datetime.now().isoformat()
                }]

            await self.cache.set(cache_key, dark_pool_trades, ttl=300)
            return dark_pool_trades

        except Exception as e:
            logger.error(f"Error detecting dark pool activity for {symbol}: {e}")
            return []

    async def comprehensive_scan(
        self,
        symbol: str
    ) -> Dict[str, Any]:
        """
        Run all screeners on a symbol

        Returns:
            Comprehensive activity report
        """
        cache_key = f"comprehensive_scan:{symbol}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        try:
            # Run all scans concurrently
            results = await asyncio.gather(
                self.detect_unusual_volume(symbol),
                self.detect_block_trades(symbol),
                self.detect_sweeps(symbol),
                self.detect_dark_pool_activity(symbol),
                self.options_service.get_put_call_ratio(symbol),
                self.options_service.get_open_interest_analysis(symbol),
                return_exceptions=True
            )

            unusual_volume, blocks, sweeps, dark_pool, pc_ratio, oi_analysis = results

            # Calculate overall activity score
            activity_score = 0
            if isinstance(unusual_volume, dict) and unusual_volume.get("is_unusual"):
                activity_score += 30
            if isinstance(blocks, list) and len(blocks) > 0:
                activity_score += 25
            if isinstance(sweeps, list) and len(sweeps) > 0:
                activity_score += 30
            if isinstance(dark_pool, list) and len(dark_pool) > 0:
                activity_score += 15

            report = {
                "symbol": symbol,
                "scan_time": datetime.now().isoformat(),
                "activity_score": activity_score,
                "activity_level": self._interpret_activity_score(activity_score),
                "unusual_volume": unusual_volume if isinstance(unusual_volume, dict) else {},
                "block_trades": blocks if isinstance(blocks, list) else [],
                "sweeps": sweeps if isinstance(sweeps, list) else [],
                "dark_pool": dark_pool if isinstance(dark_pool, list) else [],
                "put_call_ratio": pc_ratio if isinstance(pc_ratio, dict) else {},
                "open_interest": oi_analysis if isinstance(oi_analysis, dict) else {},
                "summary": self._generate_summary(
                    activity_score,
                    unusual_volume,
                    blocks,
                    sweeps,
                    pc_ratio
                )
            }

            await self.cache.set(cache_key, report, ttl=300)
            return report

        except Exception as e:
            logger.error(f"Error in comprehensive scan for {symbol}: {e}")
            return {"error": str(e)}

    def _interpret_activity_score(self, score: int) -> str:
        """Interpret activity score"""
        if score >= 80:
            return "very_high"
        elif score >= 60:
            return "high"
        elif score >= 40:
            return "moderate"
        elif score >= 20:
            return "low"
        else:
            return "very_low"

    def _generate_summary(
        self,
        score: int,
        unusual_volume: Any,
        blocks: List,
        sweeps: List,
        pc_ratio: Dict
    ) -> str:
        """Generate human-readable summary"""
        summary_parts = []

        if score >= 60:
            summary_parts.append("High options activity detected")

        if isinstance(unusual_volume, dict) and unusual_volume.get("is_unusual"):
            ratio = unusual_volume.get("volume_ratio", 0)
            summary_parts.append(f"Volume {ratio}x above average")

        if blocks and len(blocks) > 0:
            summary_parts.append(f"{len(blocks)} large block trade(s)")

        if sweeps and len(sweeps) > 0:
            summary_parts.append(f"{len(sweeps)} sweep order(s)")

        if isinstance(pc_ratio, dict):
            sentiment = pc_ratio.get("sentiment", "neutral")
            summary_parts.append(f"Overall sentiment: {sentiment}")

        return " | ".join(summary_parts) if summary_parts else "Normal activity levels"

    async def _get_default_watchlist(self) -> List[str]:
        """Get default watchlist for scanning"""
        # Common high-volume tickers
        return [
            "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "AMD",
            "SPY", "QQQ", "IWM", "DIA",  # ETFs
            "NFLX", "BABA", "UBER", "SQ", "SHOP", "COIN"
        ]

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Singleton instance
_screener: Optional[OptionsScreener] = None


def get_options_screener() -> OptionsScreener:
    """Get or create options screener singleton"""
    global _screener
    if _screener is None:
        _screener = OptionsScreener()
    return _screener
