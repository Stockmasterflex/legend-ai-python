"""
Chart-IMG service for generating trading charts with indicators
Pro plan: 500 daily calls, 10/sec rate limit, no watermark
Supports: RSI, EMA 21, SMA 50, Volume, Support/Resistance, Long Position drawings
"""
import logging
import asyncio
from typing import Optional, Dict, Any, List
import httpx
from datetime import datetime
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class ChartingService:
    """Generate trading charts using Chart-IMG API with indicators and drawings"""

    BASE_URL = "https://api.chart-img.com/v2/tradingview/advanced-chart"
    RATE_LIMIT_DELAY = 0.1  # 100ms = 10 calls/sec
    MAX_PARAMETERS = 5  # Max studies + drawings combined

    def __init__(self):
        self.api_key = settings.chartimg_api_key
        self.daily_limit = settings.chartimg_daily_limit
        self.rate_limit = 10  # 10 calls/sec
        self.call_count = 0
        self.last_reset = datetime.now()
        self.request_queue = asyncio.Queue()

    async def _check_rate_limit(self):
        """Check daily rate limit"""
        now = datetime.now()
        if (now - self.last_reset).total_seconds() >= 86400:
            self.call_count = 0
            self.last_reset = now

        if self.call_count >= self.daily_limit:
            logger.warning(f"⚠️ Chart-IMG daily limit reached ({self.daily_limit})")
            return False

        self.call_count += 1
        return True

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
        resistance: Optional[float] = None
    ) -> Optional[str]:
        """
        Generate a chart with indicators and drawings using Chart-IMG API

        Args:
            ticker: Stock symbol (e.g., NVDA)
            timeframe: "1day" or "1week"
            width: Chart width in pixels
            height: Chart height in pixels
            entry: Entry price for long position drawing
            stop: Stop loss price for long position drawing
            target: Target price for long position drawing
            support: Support level price
            resistance: Resistance level price

        Returns:
            URL of the generated chart image
        """
        try:
            # Check rate limiting
            if not await self._check_rate_limit():
                return self._get_fallback_url(ticker)

            # Apply rate limit delay
            await asyncio.sleep(self.RATE_LIMIT_DELAY)

            # Build Chart-IMG request payload
            payload = self._build_chart_payload(
                ticker, timeframe, width, height,
                entry, stop, target, support, resistance
            )

            # Make API request
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.BASE_URL,
                    json=payload,
                    headers={
                        "x-api-key": self.api_key,
                        "Content-Type": "application/json"
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    chart_url = data.get("url")
                    logger.info(f"✅ Chart generated for {ticker}: {chart_url}")
                    return chart_url
                else:
                    logger.warning(
                        f"⚠️ Chart-IMG error {response.status_code} for {ticker}: "
                        f"{response.text}"
                    )
                    return self._get_fallback_url(ticker)

        except Exception as e:
            logger.warning(f"⚠️ Chart generation error for {ticker}: {e}")
            return self._get_fallback_url(ticker)

    def _build_chart_payload(
        self,
        ticker: str,
        timeframe: str,
        width: int,
        height: int,
        entry: Optional[float],
        stop: Optional[float],
        target: Optional[float],
        support: Optional[float],
        resistance: Optional[float]
    ) -> Dict[str, Any]:
        """Build JSON payload for Chart-IMG API request"""

        # Convert ticker to TradingView format
        tv_symbol = self._format_ticker(ticker)

        # Convert timeframe to Chart-IMG format
        interval = "1D" if "day" in timeframe else "1W"

        # Build studies (indicators)
        studies = [
            {
                "name": "Relative Strength Index",
                "input": {
                    "length": 14,
                    "smoothingLine": "SMA",
                    "smoothingLength": 14
                },
                "override": {
                    "Plot.linewidth": 2,
                    "Plot.plottype": "line",
                    "Plot.color": "rgb(126,87,194)",
                    "UpperLimit.visible": True,
                    "UpperLimit.value": 70,
                    "LowerLimit.visible": True,
                    "LowerLimit.value": 30
                }
            },
            {
                "name": "Moving Average Exponential",
                "input": {
                    "length": 21,
                    "source": "close"
                },
                "override": {
                    "Plot.linewidth": 2,
                    "Plot.color": "rgb(255,109,0)"
                }
            },
            {
                "name": "Moving Average",
                "input": {
                    "length": 50,
                    "source": "close",
                    "smoothingLine": "SMA"
                },
                "override": {
                    "Plot.linewidth": 2,
                    "Plot.color": "rgb(67,160,71)"
                }
            },
            {
                "name": "Volume",
                "forceOverlay": False,
                "override": {
                    "Volume.plottype": "columns",
                    "Volume.color.0": "rgba(247,82,95,0.5)",
                    "Volume.color.1": "rgba(34,171,148,0.5)"
                }
            }
        ]

        # Build drawings (annotations)
        drawings = []

        # Add long position drawing if entry/stop/target provided
        if entry and stop and target:
            drawings.append({
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
            })

        # Add support/resistance lines (if we have room, we already have 4 studies)
        # We can add max 1 more (5 total), so choose based on which is more important
        if support and len(drawings) < 1:
            drawings.append({
                "name": "Horizontal Line",
                "input": {
                    "price": round(support, 2),
                    "text": "Support"
                },
                "override": {
                    "lineColor": "rgb(67,160,71)",
                    "textColor": "rgb(67,160,71)",
                    "lineStyle": 1
                }
            })

        # Build final payload
        payload = {
            "symbol": tv_symbol,
            "interval": interval,
            "width": width,
            "height": height,
            "theme": "dark",
            "studies": studies[:4],  # Max 4 studies (leaving room for drawings)
            "drawings": drawings,  # Up to 1 drawing to stay within 5 parameter limit
            "override": {}
        }

        return payload

    def _format_ticker(self, ticker: str) -> str:
        """Convert ticker symbol to TradingView format (EXCHANGE:SYMBOL)"""
        ticker = ticker.upper().strip()

        # Common US stocks mapping
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

    def _get_fallback_url(self, ticker: str) -> str:
        """Get fallback TradingView embed URL when Chart-IMG fails"""
        logger.info(f"📊 Using fallback TradingView embed for {ticker}")
        return (
            f"https://www.tradingview.com/widgetembed/?symbol={ticker.upper()}"
            f"&interval=D&hidesidetoolbar=0&hidetopmenu=0&style=1&locale=en"
            f"&withdateranges=1"
        )

    async def get_chart_batch(
        self,
        tickers: list[str],
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
