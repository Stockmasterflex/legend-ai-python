"""
Chart-IMG service for generating trading charts with indicators
Pro plan: 500 daily calls, 10/sec rate limit, no watermark
Supports: RSI, EMA 21, SMA 50, Volume, Support/Resistance, Long Position drawings
Enhanced with multi-timeframe presets, Redis-backed rate limiting and graceful degradation
"""
import logging
import asyncio
from typing import Optional, Dict, Any, List
import httpx
from datetime import datetime
from uuid import uuid4
from copy import deepcopy
from redis.asyncio import Redis

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class ChartingService:
    """Generate trading charts using Chart-IMG API with indicators and drawings"""

    BASE_URL = "https://api.chart-img.com/v2/tradingview/advanced-chart/storage"
    RATE_LIMIT_DELAY = 0.1  # 100ms = 10 calls/sec
    MAX_PARAMETERS = 5  # Max studies + drawings combined; gracefully degrade if needed

    CHART_PRESETS = {
        "breakout": ["EMA21", "SMA50"],  # Simplified: removed RSI to reduce clutter
        "swing": ["EMA21", "SMA50"],      # Simplified: core moving averages only
        "momentum": ["EMA21", "SMA50"],   # Simplified: reduced from 3 EMAs
        "support": ["EMA21", "SMA50"],    # Simplified: focus on key levels
        "minimal": ["EMA21"],             # New: ultra-minimal for clarity
    }

    CORE_STUDIES_ORDER = ["EMA21", "SMA50"]  # Simplified: focus on key moving averages
    STUDIES_CONFIG = {
        "EMA21": {
            "name": "Moving Average Exponential",
            "input": {"length": 21, "source": "close"},
            "override": {
                "Plot.linewidth": 2,
                "Plot.plottype": "line",
                "Plot.color": "rgb(96,165,250)"
            }
        },
        "EMA50": {
            "name": "Moving Average Exponential",
            "input": {"length": 50, "source": "close"},
            "override": {
                "Plot.linewidth": 2,
                "Plot.plottype": "line",
                "Plot.color": "#2196F3"
            }
        },
        "EMA200": {
            "name": "Moving Average Exponential",
            "input": {"length": 200, "source": "close"},
            "override": {
                "Plot.linewidth": 2,
                "Plot.plottype": "line",
                "Plot.color": "rgb(156,39,176)"
            }
        },
        "SMA50": {
            "name": "Moving Average",
            "input": {"length": 50, "source": "close"},
            "override": {
                "Plot.linewidth": 2,
                "Plot.plottype": "line",
                "Plot.color": "rgb(239,68,68)"
            }
        },
        "SMA200": {
            "name": "Moving Average",
            "input": {"length": 200, "source": "close"},
            "override": {
                "Plot.linewidth": 2,
                "Plot.plottype": "line",
                "Plot.color": "rgb(255,193,7)"
            }
        },
        "MACD": {
            "name": "MACD",
            "input": {"fastLength": 12, "slowLength": 26, "signalLength": 9},
            "override": {"Plot.linewidth": 2}
        },
        "RSI": {
            "name": "Relative Strength Index",
            "input": {"length": 14, "smoothingLine": "SMA", "smoothingLength": 14},
            "override": {
                "Plot.linewidth": 1,
                "Plot.plottype": "line",
                "Plot.color": "rgb(126,87,194)",
                "UpperLimit.value": 70,
                "LowerLimit.value": 30
            },
            "forceOverlay": False
        }
    }

    def __init__(self):
        self.api_key = settings.chart_img_api_key  # Use the robust property
        self.daily_limit = settings.chartimg_daily_limit
        self.rate_limit = 10  # 10 calls/sec
        self.fallback_mode = False  # Graceful degradation flag
        self.redis: Redis = Redis.from_url(settings.redis_url, decode_responses=True)

        # Debug: Log API key status
        logger.info(f"🎨 ChartingService initialized - API key present: {bool(self.api_key)}")
        if not self.api_key:
            logger.warning("⚠️ Chart-IMG API key not found in any environment variable (CHART_IMG_API_KEY, CHARTIMG_API_KEY, etc.)")
        else:
            logger.info(f"🎨 Chart-IMG API key loaded successfully (length: {len(self.api_key)})")

    async def _check_rate_limit(self):
        """Global burst (10/sec) + daily quota (500/day) enforcement"""
        try:
            if not await self._consume_burst_token():
                logger.warning("⚠️ Burst rate limit hit")
                return False
            usage = await self._get_daily_usage()
            if usage >= self.daily_limit:
                logger.warning("⚠️ Chart-IMG daily quota exhausted. Using fallback charts.")
                self.fallback_mode = True
                return False
            await self._increment_daily_usage()
            return True
        except Exception as e:
            logger.error(f"⚠️ Rate limit check failed: {e}. Allowing request to proceed.")
            # On Redis error, allow the request to proceed rather than blocking
            return True

    async def _consume_burst_token(self) -> bool:
        """Shared 10 req/sec limit using Redis sorted set"""
        now_ms = int(datetime.utcnow().timestamp() * 1000)
        token_id = f"{now_ms}-{uuid4().hex}"
        key = "chartimg:burst"
        pipeline = self.redis.pipeline()
        pipeline.zremrangebyscore(key, 0, now_ms - 1000)
        pipeline.zadd(key, {token_id: now_ms})
        pipeline.zcard(key)
        pipeline.expire(key, 2)
        _, _, count, _ = await pipeline.execute()
        if count > self.rate_limit:
            await self.redis.zrem(key, token_id)
            return False
        return True

    async def _get_daily_usage(self) -> int:
        value = await self.redis.get(self._daily_usage_key)
        return int(value or 0)

    async def _increment_daily_usage(self):
        key = self._daily_usage_key
        usage = await self.redis.incr(key)
        if usage == 1:
            await self.redis.expire(key, 86400)

    @property
    def _daily_usage_key(self) -> str:
        today = datetime.utcnow().strftime("%Y%m%d")
        return f"chartimg:usage:{today}"

    def _get_fallback_url(self, ticker: str, timeframe: str = "1day") -> str:
        """
        Return None instead of SVG fallback to trigger proper error handling
        SVG fallbacks were causing confusion - better to return None and let calling code handle it
        """
        logger.warning(f"📊 Returning None for {ticker} ({timeframe}) - Chart-IMG unavailable")
        return None

    def _build_chart_payload(
        self,
        ticker: str,
        timeframe: str = "1day",
        width: int = 1200,
        height: int = 600,
        entry: Optional[float] = None,
        stop: Optional[float] = None,
        target: Optional[float] = None,
        support: Optional[float] = None,
        resistance: Optional[float] = None,
        overlays: Optional[List[str]] = None,
        pattern_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Build Chart-IMG request payload with smart parameter management

        Gracefully degrade studies if we're approaching MAX_PARAMETERS limit
        """
        if overlays is None:
            overlays = self._resolve_overlays("breakout")

        # Convert ticker to TradingView format
        tv_symbol = self._format_ticker(ticker)

        # Convert timeframe to Chart-IMG format
        interval = self._resolve_interval(timeframe)

        # Build core studies with controlled parameter count
        studies = self._build_studies(overlays)

        # Build drawings (entry/stop/target) - try to fit within MAX_PARAMETERS
        drawings = []
        parameter_count = len(studies)

        # Add long position drawing if we have space (reserves 1 parameter slot)
        if entry and stop and target and parameter_count < self.MAX_PARAMETERS:
            drawings.append(
                self._build_long_position_drawing(entry, stop, target, pattern_name)
            )
            parameter_count += 1

        payload = {
            "symbol": tv_symbol,
            "interval": interval,
            "width": width,
            "height": height,
            "theme": "dark",
            "hideVolume": False,
            "studies": studies,
            "drawings": drawings,
            "timezone": "America/New_York"
        }

        # Add support/resistance if space available
        if (support or resistance) and parameter_count < self.MAX_PARAMETERS:
            if support:
                payload["support_level"] = support
            if resistance:
                payload["resistance_level"] = resistance

        return payload

    def _build_studies(self, overlays: List[str]) -> List[Dict[str, Any]]:
        """Build a deterministic set of studies focused on EMA21, SMA50, and RSI"""
        overlays = [(overlay or "").upper().strip() for overlay in (overlays or [])]
        studies = []

        # Always include the core studies first
        for key in self.CORE_STUDIES_ORDER:
            config = self.STUDIES_CONFIG.get(key)
            if config:
                studies.append(deepcopy(config))

        # Try to append additional overlays (if any) without exceeding MAX_PARAMETERS
        for overlay in overlays:
            if overlay in self.CORE_STUDIES_ORDER:
                continue
            if len(studies) >= self.MAX_PARAMETERS - 1:
                logger.warning(
                    f"⚠️ Skipping extra overlays due to MAX_PARAMETERS limit: {overlay}"
                )
                break
            config = self.STUDIES_CONFIG.get(overlay)
            if config:
                studies.append(deepcopy(config))

        # Trim if somehow we exceeded the available slots
        if len(studies) > self.MAX_PARAMETERS - 1:
            studies = studies[: self.MAX_PARAMETERS - 1]

        return studies

    def _build_long_position_drawing(
        self, entry: float, stop: float, target: float, pattern_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Build a long position drawing annotation with optional pattern label"""
        drawing = {
            "name": "Long Position",
            "input": {
                "startDatetime": datetime.now().isoformat() + "Z",
                "entryPrice": round(entry, 2),
                "targetPrice": round(target, 2),
                "stopPrice": round(stop, 2)
            },
            "override": {
                "fillBackground": True,
                "showPrice": True,
                "showStats": True
            }
        }

    def _resolve_overlays(self, preset: str) -> List[str]:
        """Return overlays for named preset"""
        preset_key = (preset or "breakout").lower()
        return self.CHART_PRESETS.get(preset_key, self.CHART_PRESETS["breakout"])

    def _resolve_interval(self, timeframe: str) -> str:
        """Convert timeframe string to Chart-IMG interval format"""
        timeframe_map = {
            "1day": "1D",
            "1D": "1D",
            "daily": "1D",
            "1week": "1W",
            "1W": "1W",
            "weekly": "1W",
            "60min": "60",
            "60m": "60",
            "1hour": "60",
            "1H": "60",
            "4hour": "240",
            "4H": "240",
            "15min": "15",
            "15m": "15",
            "5min": "5",
            "5m": "5"
        }
        resolved = timeframe_map.get(timeframe.lower(), "1D")
        logger.debug(f"Resolved timeframe {timeframe} -> {resolved}")
        return resolved

    def _format_ticker(self, ticker: str) -> str:
        """Convert ticker symbol to TradingView format (EXCHANGE:SYMBOL)"""
        ticker = ticker.upper().strip()

        # Common US stocks mapping - try NASDAQ first as it's most common
        us_exchanges = {
            "AAPL": "NASDAQ", "MSFT": "NASDAQ", "NVDA": "NASDAQ",
            "AMZN": "NASDAQ", "TSLA": "NASDAQ", "META": "NASDAQ",
            "NFLX": "NASDAQ", "GOOGL": "NASDAQ", "JPM": "NYSE",
            "BAC": "NYSE", "WMT": "NYSE", "JNJ": "NYSE",
            "PG": "NYSE", "V": "NYSE", "MA": "NYSE",
            "SPY": "NASDAQ", "QQQ": "NASDAQ", "DIA": "NASDAQ",
            "IWM": "NASDAQ", "BTCUSDT": "BINANCE", "ETHUSD": "COINBASE"
        }

        exchange = us_exchanges.get(ticker, "NASDAQ")
        return f"{exchange}:{ticker}"

    def _get_symbol_candidates(self, ticker: str) -> list[str]:
        """Get list of symbol format candidates to try (NASDAQ first, then NYSE, then others)"""
        ticker = ticker.upper().strip()

        # Try NASDAQ first (most common), then NYSE, then the mapped format
        primary = self._format_ticker(ticker)
        candidates = [
            f"NASDAQ:{ticker}",
            f"NYSE:{ticker}",
        ]

        # Add the mapped format if it's different
        if primary not in candidates:
            candidates.append(primary)

        return candidates

    async def generate_chart(
        self,
        ticker: str,
        timeframe: str = "1day",
        width: int = 1200,
        height: int = 600,
        entry: Optional[float] = None,
        stop: Optional[float] = None,
        target: Optional[float] = None,
        support: Optional[float] = None,
        resistance: Optional[float] = None,
        overlays: Optional[List[str]] = None,
        preset: str = "breakout",
        pattern_name: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate a chart with indicators and drawings using Chart-IMG API

        Args:
            ticker: Stock symbol (e.g., NVDA)
            timeframe: "1day", "1week", "60min", etc.
            width: Chart width in pixels
            height: Chart height in pixels
            entry: Entry price for long position drawing
            stop: Stop loss price for long position drawing
            target: Target price for long position drawing
            support: Support level price
            resistance: Resistance level price
            overlays: Optional custom overlays; otherwise a preset is used
            preset: Preset name (breakout, swing, momentum, support)

        Returns:
            URL of the generated chart image
        """
        logger.info(f"🎨 Starting chart generation for {ticker} on {timeframe} with preset {preset}")

        # Check if API key is available
        if not self.api_key or self.api_key.lower().startswith('dev'):
            logger.error(f"❌ Chart-IMG API key not configured for {ticker}")
            raise ValueError("Chart-IMG API key not configured. Please set the CHART_IMG_API_KEY environment variable.")

        # Check cache first (24h TTL)
        if self.redis:
            try:
                cache_key = f"chartimg:{ticker}:{timeframe}:{entry}:{stop}:{target}"
                cached_url = await self.redis.get(cache_key)
                if cached_url:
                    logger.info(f"💾 Chart cache HIT for {ticker}")
                    return cached_url.decode() if isinstance(cached_url, bytes) else cached_url
            except Exception as e:
                logger.warning(f"Cache lookup failed: {e}")
        
        try:
            # Check rate limiting
            rate_limit_ok = await self._check_rate_limit()
            logger.info(f"📊 Rate limit check for {ticker}: {'PASS' if rate_limit_ok else 'FAIL'}")
            if not rate_limit_ok:
                logger.warning(f"⚠️ Rate limit hit for {ticker}, using fallback")
                return self._get_fallback_url(ticker, timeframe)

            # Apply rate limit delay
            await asyncio.sleep(self.RATE_LIMIT_DELAY)

            # Build Chart-IMG request payload
            payload = self._build_chart_payload(
                ticker, timeframe, width, height,
                entry, stop, target, support, resistance,
                overlays or self._resolve_overlays(preset),
                pattern_name
            )

            # Make API request with exponential backoff (max 4 retries)
            logger.info(f"📡 Making Chart-IMG API request for {ticker} with API key present: {bool(self.api_key)}")
            max_retries = 4
            retry_delay = 1.0  # Start with 1 second
            
            for attempt in range(max_retries):
                try:
                    async with httpx.AsyncClient(timeout=30.0) as client:
                        start_time = datetime.now()
                        response = await client.post(
                            self.BASE_URL,
                            json=payload,
                            headers={
                                "x-api-key": self.api_key,
                                "Content-Type": "application/json"
                            }
                        )
                        duration = (datetime.now() - start_time).total_seconds()
                    
                    logger.info(f"📡 Chart-IMG response status: {response.status_code} for {ticker} (attempt {attempt + 1}/{max_retries}, {duration:.2f}s)")
                    
                    if response.status_code == 200:
                        break  # Success, exit retry loop
                    elif response.status_code == 429:  # Rate limit
                        if attempt < max_retries - 1:
                            logger.warning(f"⏳ Rate limited, retrying in {retry_delay}s...")
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 2  # Exponential backoff
                            continue
                    elif response.status_code >= 500:  # Server error
                        if attempt < max_retries - 1:
                            logger.warning(f"⏳ Server error, retrying in {retry_delay}s...")
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 2
                            continue
                    else:
                        break  # Client error, don't retry
                
                except (httpx.TimeoutException, httpx.NetworkError) as e:
                    if attempt < max_retries - 1:
                        logger.warning(f"⏳ Network error, retrying in {retry_delay}s: {e}")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2
                        continue
                    else:
                        raise

            if response.status_code == 200:
                data = response.json()
                # Chart-IMG can return different response structures:
                # 1. {"success": true, "data": {"url": "...", "expires_at": "..."}}
                # 2. {"url": "...", "expires_at": "..."}
                # 3. {"imageUrl": "..."}
                chart_url = None
                if data.get("success") and data.get("data"):
                    # Nested structure
                    chart_url = data["data"].get("url")
                    expires_at = data["data"].get("expires_at", "N/A")
                else:
                    # Direct structure (same as build_analyze_chart)
                    chart_url = data.get("url") or data.get("imageUrl") or data.get("image_url")
                    expires_at = data.get("expires_at", "N/A")

                if chart_url:
                    logger.info(f"✅ Chart generated for {ticker} ({timeframe}): {chart_url[:60]}... (expires: {expires_at})")
                    
                    # Cache for 24h (86400 seconds)
                    if self.redis:
                        try:
                            cache_key = f"chartimg:{ticker}:{timeframe}:{entry}:{stop}:{target}"
                            await self.redis.setex(cache_key, 86400, chart_url)
                            logger.debug(f"💾 Cached chart URL for {ticker} (24h TTL)")
                        except Exception as e:
                            logger.warning(f"Failed to cache chart URL: {e}")
                    
                    return chart_url
                else:
                    logger.warning(f"⚠️ Chart-IMG response missing URL for {ticker}: {data}")
                    return self._get_fallback_url(ticker, timeframe)
            else:
                logger.warning(
                    f"⚠️ Chart-IMG error {response.status_code} for {ticker}: "
                    f"{response.text[:100]}"
                )
                return self._get_fallback_url(ticker, timeframe)

        except Exception as e:
            logger.warning(f"⚠️ Chart generation error for {ticker}: {e}")
            return self._get_fallback_url(ticker, timeframe)

    async def generate_multi_timeframe_charts(
        self,
        ticker: str,
        timeframes: Optional[List[str]] = None,
        entry: Optional[float] = None,
        stop: Optional[float] = None,
        target: Optional[float] = None,
        overlays: Optional[List[str]] = None,
        preset: str = "breakout"
    ) -> Dict[str, str]:
        """
        Generate charts for multiple timeframes concurrently

        Args:
            ticker: Stock symbol
            timeframes: List of timeframe strings (default: ["1D", "1W", "60m"])
            entry: Entry price
            stop: Stop loss
            target: Target price
            overlays: Indicators to include

        Returns:
            Dict mapping timeframe -> chart_url (only successful charts)
        """
        if timeframes is None:
            timeframes = ["1day", "1week", "60min"]

        # Generate charts concurrently
        chart_tasks = [
            self.generate_chart(
                ticker=ticker,
                timeframe=tf,
                entry=entry,
                stop=stop,
                target=target,
                overlays=overlays,
                preset=preset
            )
            for tf in timeframes
        ]

        urls = await asyncio.gather(*chart_tasks)

        result = {}
        for tf, url in zip(timeframes, urls):
            if url:
                result[tf] = url
                logger.info(f"✅ Generated chart for {ticker} @ {tf}")
            else:
                logger.warning(f"⚠️ Failed to generate chart for {ticker} @ {tf}")

        return result

    async def generate_thumbnail(
        self,
        ticker: str,
        timeframe: str = "1day",
        preset: str = "breakout"
    ) -> Optional[str]:
        """Generate lightweight thumbnails for watchlist cards."""
        return await self.generate_chart(
            ticker=ticker,
            timeframe=timeframe,
            width=400,
            height=225,
            preset=preset
        )

    async def get_usage_stats(self) -> Dict[str, Any]:
        """Expose usage telemetry for dashboard health cards."""
        return {
            "daily_usage": await self._get_daily_usage(),
            "daily_limit": self.daily_limit,
            "burst_limit": self.rate_limit,
            "fallback_mode": self.fallback_mode
        }

    async def get_chart_batch(
        self,
        tickers: List[str],
        timeframe: str = "1day"
    ) -> Dict[str, Optional[str]]:
        """
        Generate charts for multiple tickers with rate limiting

        Args:
            tickers: List of stock symbols
            timeframe: Chart timeframe

        Returns:
            Dict mapping ticker -> chart URL
        """
        results = {}

        for ticker in tickers:
            chart_url = await self.generate_chart(ticker, timeframe)
            results[ticker] = chart_url

        return results


# Singleton instance
_charting_service: Optional[ChartingService] = None

def get_charting_service() -> ChartingService:
    """Get or create charting service singleton"""
    global _charting_service
    if _charting_service is None:
        _charting_service = ChartingService()
    return _charting_service
