import httpx
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import logging

from app.config import get_settings

logger = logging.getLogger(__name__)


@dataclass
class ChartConfig:
    """Chart configuration matching Chart-IMG PRO API"""
    ticker: str
    interval: str = "1D"
    entry: Optional[float] = None
    stop: Optional[float] = None
    target: Optional[float] = None

    # Indicators
    show_volume: bool = True
    show_ema10: bool = True
    show_ema21: bool = True
    show_sma50: bool = True
    show_sma150: bool = True
    show_sma200: bool = True


class ChartGenerator:
    """
    Chart generation using Chart-IMG PRO API

    Matches n8n Chart_Generator_V2_Complete functionality
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.chart-img.com/v2/tradingview/advanced-chart/storage"
        self.client = httpx.AsyncClient(timeout=30.0)

    async def generate_chart(self, config: ChartConfig) -> Dict[str, Any]:
        """
        Generate annotated chart with entry/stop/target

        Matches n8n Chart_Generator_V2_Complete.json logic

        Returns: {
            "url": "https://chart-img.com/...",
            "success": true
        }
        """
        try:
            # Build request body matching n8n Chart_Generator_V2_Complete format
            symbol = self._normalize_symbol(config.ticker)
            interval = self._resolve_interval(config.interval)

            request_body = {
                "symbol": symbol,
                "interval": interval,
                "width": 1280,
                "height": 720,
                "theme": "dark",
                "studies": self._build_studies(config),
                "drawings": self._build_drawings(config) if (config.entry or config.stop or config.target) else []
            }

            logger.info(f"🎨 Generating chart for {config.ticker} -> {symbol}")

            response = await self.client.post(
                self.base_url,
                json=request_body,
                headers={
                    "X-API-KEY": self.api_key,
                    "Content-Type": "application/json"
                }
            )

            response.raise_for_status()
            result = response.json()

            if "url" in result and result["url"].startswith("http"):
                logger.info(f"✅ Chart generated successfully: {result['url']}")
                return {
                    "success": True,
                    "url": result["url"],
                    "ticker": config.ticker,
                    "interval": config.interval
                }
            else:
                logger.error(f"🚫 Chart generation failed: {result}")
                return {
                    "success": False,
                    "error": "Chart generation failed",
                    "response": result
                }

        except httpx.HTTPStatusError as e:
            logger.error(f"🚫 Chart-IMG API error: {e.response.status_code} - {e.response.text}")
            return {
                "success": False,
                "error": f"API error: {e.response.status_code}",
                "details": e.response.text
            }
        except Exception as e:
            logger.error(f"💥 Chart generation error: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _build_studies(self, config: ChartConfig) -> List[Dict[str, Any]]:
        """Build indicator studies for Chart-IMG API - matching Analysis page setup"""
        studies = []

        # Volume (most important - shows market participation)
        if config.show_volume:
            studies.append({
                "name": "Volume",
                "input": {}
            })

        # 21 EMA (key short-term trend indicator)
        if config.show_ema21:
            studies.append({
                "name": "Moving Average Exponential",
                "input": {"length": 21}
            })

        # 50 SMA (major support/resistance level)
        if config.show_sma50:
            studies.append({
                "name": "Moving Average",
                "input": {"length": 50}
            })

        return studies

    def _build_drawings(self, config: ChartConfig) -> List[Dict[str, Any]]:
        """Build entry/stop/target line drawings with Long Position annotation"""
        drawings = []

        if config.entry and config.stop:
            # Long Position Entry (green line)
            drawings.append({
                "name": "Horizontal Line",
                "input": {"price": config.entry, "text": f"LONG ${config.entry:.2f}"},
                "override": {
                    "lineColor": "rgb(16, 185, 129)",  # Emerald-500
                    "lineWidth": 2,
                    "showPrice": True,
                    "textColor": "rgb(16, 185, 129)"
                }
            })

            # Stop Loss (red line)
            drawings.append({
                "name": "Horizontal Line",
                "input": {"price": config.stop, "text": f"STOP ${config.stop:.2f}"},
                "override": {
                    "lineColor": "rgb(239, 68, 68)",  # Red-500
                    "lineWidth": 2,
                    "lineStyle": 2,  # Dashed
                    "showPrice": True,
                    "textColor": "rgb(239, 68, 68)"
                }
            })

        # Target line (if provided)
        if config.target and len(drawings) < 5:
            drawings.append({
                "name": "Horizontal Line",
                "input": {"price": config.target, "text": f"TARGET ${config.target:.2f}"},
                "override": {
                    "lineColor": "rgb(34, 197, 94)",  # Green-500
                    "lineWidth": 2,
                    "lineStyle": 2,  # Dashed
                    "showPrice": True,
                    "textColor": "rgb(34, 197, 94)"
                }
            })

        return drawings

    def _normalize_symbol(self, ticker: str) -> str:
        """Normalize ticker symbol to Chart-IMG format (matches n8n logic)"""
        if ":" in ticker:
            return ticker

        upper = ticker.upper()

        # NASDAQ stocks
        nasdaq_stocks = {
            'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'META', 'NVDA', 'TSLA',
            'NFLX', 'AMD', 'INTC', 'PYPL', 'COIN', 'CRWD', 'ZM', 'ZS', 'TEAM',
            'DOCU', 'OKTA', 'ROKU', 'SQ', 'SHOP', 'UBER', 'LYFT', 'SPOT'
        }

        # NYSE stocks
        nyse_stocks = {
            'JPM', 'BAC', 'WMT', 'JNJ', 'PG', 'UNH', 'V', 'MA', 'DIS', 'HD',
            'GS', 'BRK', 'BRK.A', 'BRK.B', 'KO', 'VZ', 'PFE', 'CVX', 'XOM'
        }

        if upper in nasdaq_stocks:
            return f"NASDAQ:{upper}"
        elif upper in nyse_stocks:
            return f"NYSE:{upper}"
        else:
            return f"NASDAQ:{upper}"  # Default to NASDAQ

    def _resolve_interval(self, interval: str) -> str:
        """Resolve interval to Chart-IMG format (matches n8n logic)"""
        if not interval:
            return "1D"

        lower = interval.lower()
        upper = interval.upper()

        # Map common variations
        interval_map = {
            '1d': '1D', 'd': '1D', 'day': '1D', 'daily': '1D',
            '1w': '1W', 'w': '1W', 'week': '1W', 'weekly': '1W',
            '1h': '1h', '60': '1h', '60m': '1h', 'hour': '1h',
            '4h': '4h', '240': '4h',
            '2h': '2h', '120': '2h',
            '30m': '30m', '30': '30m',
            '15m': '15m', '15': '15m',
            '5m': '5m', '5': '5m',
            '1m': '1m', '1min': '1m', '1minute': '1m',
            '1M': '1M', 'M': '1M', 'month': '1M', 'monthly': '1M'
        }

        resolved = interval_map.get(lower) or interval_map.get(upper)
        if resolved:
            return resolved

        # Handle numeric patterns
        import re
        minute_match = re.match(r'^(\d+)(m|min|minute)$', lower)
        if minute_match:
            return f"{minute_match.group(1)}m"

        hour_match = re.match(r'^(\d+)h$', lower)
        if hour_match:
            return f"{hour_match.group(1)}h"

        return "1D"  # Default

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Global instance
def get_chart_generator() -> ChartGenerator:
    """Get global chart generator instance"""
    settings = get_settings()
    return ChartGenerator(settings.chart_img_api_key)
