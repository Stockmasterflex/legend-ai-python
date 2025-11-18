"""
Earnings tracking service for comprehensive earnings analysis
Fetches earnings calendar, historical beat/miss data, and analyzes price reactions
"""
import httpx
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import asyncio
import logging
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
import numpy as np

from app.config import get_settings
from app.services.cache import get_cache_service
from app.services.market_data import market_data_service
from app.models import EarningsCalendar, EarningsReaction, EarningsAlert, Ticker

logger = logging.getLogger(__name__)


class EarningsService:
    """
    Comprehensive earnings tracking service

    Features:
    - Earnings calendar with upcoming dates
    - Historical beat/miss data
    - Pre/post-earnings price reaction analysis
    - Volatility and volume patterns
    - Multi-source data fetching (Finnhub, Alpha Vantage, Yahoo)
    """

    def __init__(self):
        self.settings = get_settings()
        self.cache = get_cache_service()
        self.client = httpx.AsyncClient(timeout=30.0)

    async def get_earnings_calendar(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        ticker: Optional[str] = None,
        db: Optional[AsyncSession] = None
    ) -> List[Dict[str, Any]]:
        """
        Get earnings calendar for specified date range or ticker

        Args:
            start_date: Start date for calendar (default: today)
            end_date: End date for calendar (default: 30 days from start)
            ticker: Specific ticker to filter (optional)
            db: Database session

        Returns:
            List of earnings events with dates, estimates, and historical data
        """
        if not start_date:
            start_date = datetime.now()
        if not end_date:
            end_date = start_date + timedelta(days=30)

        # Try cache first
        cache_key = f"earnings_calendar:{ticker or 'all'}:{start_date.date()}:{end_date.date()}"
        cached = await self.cache.get(cache_key)
        if cached:
            logger.info(f"⚡ Cache hit for earnings calendar")
            return cached

        # Fetch from APIs
        calendar_data = []

        # Finnhub earnings calendar
        finnhub_data = await self._fetch_finnhub_calendar(start_date, end_date, ticker)
        if finnhub_data:
            calendar_data.extend(finnhub_data)

        # Alpha Vantage earnings
        if ticker and not finnhub_data:
            av_data = await self._fetch_alpha_vantage_earnings(ticker)
            if av_data:
                calendar_data.extend(av_data)

        # Cache for 6 hours
        await self.cache.set(cache_key, calendar_data, ttl=21600)

        return calendar_data

    async def _fetch_finnhub_calendar(
        self,
        start_date: datetime,
        end_date: datetime,
        ticker: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Fetch earnings calendar from Finnhub API"""
        try:
            if not self.settings.finnhub_api_key:
                logger.warning("Finnhub API key not configured")
                return []

            url = "https://finnhub.io/api/v1/calendar/earnings"
            params = {
                "token": self.settings.finnhub_api_key,
                "from": start_date.strftime("%Y-%m-%d"),
                "to": end_date.strftime("%Y-%m-%d")
            }

            if ticker:
                params["symbol"] = ticker.upper()

            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            earnings_list = []
            for item in data.get("earningsCalendar", []):
                earnings_list.append({
                    "ticker": item.get("symbol"),
                    "earnings_date": datetime.strptime(item.get("date"), "%Y-%m-%d") if item.get("date") else None,
                    "fiscal_quarter": item.get("quarter"),
                    "fiscal_year": item.get("year"),
                    "eps_estimate": item.get("epsEstimate"),
                    "eps_actual": item.get("epsActual"),
                    "revenue_estimate": item.get("revenueEstimate"),
                    "revenue_actual": item.get("revenueActual"),
                    "report_time": "TNS",  # Finnhub doesn't provide this
                    "source": "finnhub"
                })

            logger.info(f"✅ Fetched {len(earnings_list)} earnings from Finnhub")
            return earnings_list

        except Exception as e:
            logger.error(f"Error fetching Finnhub earnings calendar: {e}")
            return []

    async def _fetch_alpha_vantage_earnings(self, ticker: str) -> List[Dict[str, Any]]:
        """Fetch earnings data from Alpha Vantage"""
        try:
            if not self.settings.alpha_vantage_api_key:
                logger.warning("Alpha Vantage API key not configured")
                return []

            url = "https://www.alphavantage.co/query"
            params = {
                "function": "EARNINGS",
                "symbol": ticker.upper(),
                "apikey": self.settings.alpha_vantage_api_key
            }

            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            earnings_list = []

            # Parse quarterly earnings
            for item in data.get("quarterlyEarnings", [])[:8]:  # Last 2 years
                report_date = item.get("reportedDate")
                earnings_list.append({
                    "ticker": ticker.upper(),
                    "earnings_date": datetime.strptime(report_date, "%Y-%m-%d") if report_date else None,
                    "fiscal_quarter": item.get("fiscalDateEnding", "")[:7],  # YYYY-MM
                    "fiscal_year": None,
                    "eps_estimate": float(item.get("estimatedEPS", 0)) if item.get("estimatedEPS") != "None" else None,
                    "eps_actual": float(item.get("reportedEPS", 0)) if item.get("reportedEPS") != "None" else None,
                    "revenue_estimate": None,
                    "revenue_actual": None,
                    "report_time": "TNS",
                    "source": "alphavantage",
                    "surprise": float(item.get("surprise", 0)) if item.get("surprise") else None,
                    "surprise_pct": float(item.get("surprisePercentage", 0)) if item.get("surprisePercentage") else None
                })

            logger.info(f"✅ Fetched {len(earnings_list)} earnings from Alpha Vantage")
            return earnings_list

        except Exception as e:
            logger.error(f"Error fetching Alpha Vantage earnings: {e}")
            return []

    async def get_historical_beat_miss(
        self,
        ticker: str,
        limit: int = 8
    ) -> Dict[str, Any]:
        """
        Get historical beat/miss data for a ticker

        Args:
            ticker: Stock ticker symbol
            limit: Number of past earnings to analyze

        Returns:
            {
                "ticker": "AAPL",
                "total_reports": 8,
                "beats": 6,
                "misses": 2,
                "beat_rate": 0.75,
                "avg_surprise_pct": 3.2,
                "history": [...]
            }
        """
        cache_key = f"earnings_history:{ticker}:{limit}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        # Fetch historical earnings
        earnings_data = await self._fetch_alpha_vantage_earnings(ticker)

        if not earnings_data:
            return {
                "ticker": ticker,
                "total_reports": 0,
                "beats": 0,
                "misses": 0,
                "beat_rate": 0,
                "avg_surprise_pct": 0,
                "history": []
            }

        # Filter to only reported earnings with actuals
        reported = [e for e in earnings_data if e.get("eps_actual") is not None][:limit]

        beats = 0
        misses = 0
        surprises = []

        for earning in reported:
            eps_actual = earning.get("eps_actual", 0)
            eps_estimate = earning.get("eps_estimate", 0)

            if eps_estimate and eps_actual:
                surprise_pct = earning.get("surprise_pct")
                if surprise_pct is None:
                    surprise_pct = ((eps_actual - eps_estimate) / abs(eps_estimate)) * 100

                surprises.append(surprise_pct)

                if eps_actual > eps_estimate:
                    beats += 1
                else:
                    misses += 1

        total_reports = len(reported)
        beat_rate = beats / total_reports if total_reports > 0 else 0
        avg_surprise = np.mean(surprises) if surprises else 0

        result = {
            "ticker": ticker,
            "total_reports": total_reports,
            "beats": beats,
            "misses": misses,
            "beat_rate": beat_rate,
            "avg_surprise_pct": float(avg_surprise),
            "median_surprise_pct": float(np.median(surprises)) if surprises else 0,
            "std_surprise_pct": float(np.std(surprises)) if surprises else 0,
            "history": reported
        }

        # Cache for 24 hours
        await self.cache.set(cache_key, result, ttl=86400)
        return result

    async def analyze_earnings_reaction(
        self,
        ticker: str,
        earnings_date: datetime,
        eps_actual: Optional[float] = None,
        eps_estimate: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Analyze price reaction to earnings

        Calculates:
        - Gap percentage
        - Intraday move
        - Volume change
        - Historical average reaction
        - Volatility impact

        Args:
            ticker: Stock ticker
            earnings_date: Date of earnings report
            eps_actual: Actual EPS (if available)
            eps_estimate: Estimated EPS (if available)

        Returns:
            Comprehensive earnings reaction analysis
        """
        try:
            # Fetch price data around earnings date
            # Get 30 days before and 30 days after
            start_date = earnings_date - timedelta(days=30)
            end_date = earnings_date + timedelta(days=30)

            price_data = await market_data_service.get_time_series(
                ticker=ticker,
                interval="1day",
                outputsize=100
            )

            if not price_data or not price_data.get("t"):
                logger.warning(f"No price data for {ticker}")
                return {"error": "No price data available"}

            # Convert timestamps to dates
            dates = [datetime.fromtimestamp(ts) for ts in price_data["t"]]
            df = pd.DataFrame({
                "date": dates,
                "open": price_data["o"],
                "high": price_data["h"],
                "low": price_data["l"],
                "close": price_data["c"],
                "volume": price_data["v"]
            })

            # Find the earnings date in the data
            earnings_idx = None
            for i, date in enumerate(df["date"]):
                if date.date() >= earnings_date.date():
                    earnings_idx = i
                    break

            if earnings_idx is None or earnings_idx == 0:
                logger.warning(f"Earnings date not found in price data for {ticker}")
                return {"error": "Earnings date not in price data range"}

            # Pre-earnings data (day before)
            pre_idx = earnings_idx - 1
            pre_close = df.iloc[pre_idx]["close"]
            pre_volume = df.iloc[pre_idx]["volume"]

            # Post-earnings data (earnings day)
            post_open = df.iloc[earnings_idx]["open"]
            post_close = df.iloc[earnings_idx]["close"]
            post_high = df.iloc[earnings_idx]["high"]
            post_low = df.iloc[earnings_idx]["low"]
            post_volume = df.iloc[earnings_idx]["volume"]

            # Calculate metrics
            gap_pct = ((post_open - pre_close) / pre_close) * 100
            day_move_pct = ((post_close - pre_close) / pre_close) * 100
            intraday_high_pct = ((post_high - post_open) / post_open) * 100
            intraday_low_pct = ((post_low - post_open) / post_open) * 100
            intraday_move = max(abs(intraday_high_pct), abs(intraday_low_pct))

            # Volume analysis
            avg_volume = df["volume"].iloc[:pre_idx].tail(20).mean()
            volume_ratio = post_volume / avg_volume if avg_volume > 0 else 1

            # Multi-day reaction
            week_move_pct = None
            month_move_pct = None

            if earnings_idx + 5 < len(df):
                week_close = df.iloc[earnings_idx + 5]["close"]
                week_move_pct = ((week_close - pre_close) / pre_close) * 100

            if earnings_idx + 20 < len(df):
                month_close = df.iloc[earnings_idx + 20]["close"]
                month_move_pct = ((month_close - pre_close) / pre_close) * 100

            # Calculate surprise if we have estimates
            eps_surprise_pct = None
            if eps_actual and eps_estimate and eps_estimate != 0:
                eps_surprise_pct = ((eps_actual - eps_estimate) / abs(eps_estimate)) * 100

            result = {
                "ticker": ticker,
                "earnings_date": earnings_date.isoformat(),
                "pre_close_price": float(pre_close),
                "pre_volume": int(pre_volume),
                "post_open_price": float(post_open),
                "post_close_price": float(post_close),
                "post_volume": int(post_volume),
                "gap_percent": float(gap_pct),
                "day_move_percent": float(day_move_pct),
                "intraday_move_percent": float(intraday_move),
                "volume_ratio": float(volume_ratio),
                "week_move_percent": float(week_move_pct) if week_move_pct else None,
                "month_move_percent": float(month_move_pct) if month_move_pct else None,
                "eps_surprise_pct": float(eps_surprise_pct) if eps_surprise_pct else None,
                "analysis": self._generate_reaction_analysis(
                    gap_pct, day_move_pct, volume_ratio, eps_surprise_pct
                )
            }

            return result

        except Exception as e:
            logger.error(f"Error analyzing earnings reaction for {ticker}: {e}")
            return {"error": str(e)}

    def _generate_reaction_analysis(
        self,
        gap_pct: float,
        day_move_pct: float,
        volume_ratio: float,
        eps_surprise_pct: Optional[float]
    ) -> str:
        """Generate human-readable analysis of earnings reaction"""

        analysis_parts = []

        # Gap analysis
        if abs(gap_pct) > 5:
            direction = "gapped up" if gap_pct > 0 else "gapped down"
            analysis_parts.append(f"Strong {abs(gap_pct):.1f}% {direction} on earnings")
        elif abs(gap_pct) > 2:
            direction = "higher" if gap_pct > 0 else "lower"
            analysis_parts.append(f"Moderate {abs(gap_pct):.1f}% gap {direction}")
        else:
            analysis_parts.append(f"Minimal gap of {gap_pct:.1f}%")

        # Day move analysis
        if abs(day_move_pct) > 10:
            direction = "gain" if day_move_pct > 0 else "loss"
            analysis_parts.append(f"Significant {abs(day_move_pct):.1f}% {direction} on the day")

        # Volume analysis
        if volume_ratio > 3:
            analysis_parts.append(f"Exceptional volume at {volume_ratio:.1f}x average")
        elif volume_ratio > 2:
            analysis_parts.append(f"High volume at {volume_ratio:.1f}x average")
        elif volume_ratio > 1.5:
            analysis_parts.append(f"Above-average volume at {volume_ratio:.1f}x normal")

        # Surprise correlation
        if eps_surprise_pct:
            if abs(eps_surprise_pct) > 10:
                beat_miss = "beat" if eps_surprise_pct > 0 else "miss"
                analysis_parts.append(f"Large {abs(eps_surprise_pct):.1f}% earnings {beat_miss}")

        return ". ".join(analysis_parts) + "."

    async def get_historical_reactions(
        self,
        ticker: str,
        limit: int = 8
    ) -> Dict[str, Any]:
        """
        Get historical earnings reaction patterns for a ticker

        Returns average gap, volume, and price movement patterns
        """
        cache_key = f"earnings_reactions:{ticker}:{limit}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        # Get historical earnings dates
        historical_earnings = await self._fetch_alpha_vantage_earnings(ticker)

        if not historical_earnings:
            return {
                "ticker": ticker,
                "total_analyzed": 0,
                "avg_gap_pct": 0,
                "avg_day_move_pct": 0,
                "avg_volume_ratio": 0,
                "reactions": []
            }

        # Analyze each earnings event
        reactions = []
        for earning in historical_earnings[:limit]:
            if earning.get("earnings_date"):
                reaction = await self.analyze_earnings_reaction(
                    ticker,
                    earning["earnings_date"],
                    earning.get("eps_actual"),
                    earning.get("eps_estimate")
                )

                if "error" not in reaction:
                    reactions.append(reaction)

        # Calculate averages
        if reactions:
            avg_gap = np.mean([r["gap_percent"] for r in reactions if r.get("gap_percent")])
            avg_day_move = np.mean([r["day_move_percent"] for r in reactions if r.get("day_move_percent")])
            avg_volume = np.mean([r["volume_ratio"] for r in reactions if r.get("volume_ratio")])
        else:
            avg_gap = avg_day_move = avg_volume = 0

        result = {
            "ticker": ticker,
            "total_analyzed": len(reactions),
            "avg_gap_pct": float(avg_gap),
            "avg_day_move_pct": float(avg_day_move),
            "avg_volume_ratio": float(avg_volume),
            "reactions": reactions
        }

        # Cache for 24 hours
        await self.cache.set(cache_key, result, ttl=86400)
        return result

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Global service instance
_earnings_service: Optional[EarningsService] = None


def get_earnings_service() -> EarningsService:
    """Get or create earnings service singleton"""
    global _earnings_service
    if _earnings_service is None:
        _earnings_service = EarningsService()
    return _earnings_service
