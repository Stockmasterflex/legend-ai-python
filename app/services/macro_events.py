"""
Macro Events Service - Economic Calendar, Historical Impact, and Market Regime Detection
Tracks Fed meetings, CPI/PPI releases, GDP, unemployment, and market conditions
"""
import httpx
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timedelta
import asyncio
import logging
from enum import Enum
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc

from app.config import get_settings
from app.services.cache import get_cache_service
from app.models import MacroEvent, EventImpact, MarketRegime

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    """Types of macro events"""
    FOMC = "FOMC"
    CPI = "CPI"
    PPI = "PPI"
    GDP = "GDP"
    UNEMPLOYMENT = "UNEMPLOYMENT"
    NFP = "NFP"  # Non-Farm Payrolls
    EARNINGS = "EARNINGS"
    OPTIONS_EXP = "OPTIONS_EXP"
    DIVIDEND = "DIVIDEND"
    RETAIL_SALES = "RETAIL_SALES"
    PMI = "PMI"
    HOUSING = "HOUSING"


class MarketRegimeType(str, Enum):
    """Market regime classifications"""
    BULL = "BULL"
    BEAR = "BEAR"
    SIDEWAYS = "SIDEWAYS"


class VolatilityRegime(str, Enum):
    """Volatility classifications"""
    HIGH_VOL = "HIGH_VOL"
    NORMAL = "NORMAL"
    LOW_VOL = "LOW_VOL"


class RateEnvironment(str, Enum):
    """Interest rate environment"""
    RISING = "RISING"
    FALLING = "FALLING"
    STABLE = "STABLE"


class MacroEventsService:
    """
    Comprehensive macro events tracking service

    Features:
    - Economic calendar with countdown timers
    - Historical impact analysis
    - Market regime detection
    - Pattern success rates by regime
    """

    def __init__(self, db: Optional[Session] = None):
        self.settings = get_settings()
        self.cache = get_cache_service()
        self.client = httpx.AsyncClient(timeout=30.0)
        self.db = db

    async def get_economic_calendar(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        importance: Optional[str] = None,
        event_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get economic calendar events

        Args:
            start_date: Start date for events (default: today)
            end_date: End date for events (default: 30 days from now)
            importance: Filter by importance (HIGH, MEDIUM, LOW)
            event_type: Filter by event type (FOMC, CPI, etc.)
        """
        if not start_date:
            start_date = datetime.now()
        if not end_date:
            end_date = start_date + timedelta(days=30)

        cache_key = f"economic_calendar:{start_date.date()}:{end_date.date()}:{importance}:{event_type}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        # Fetch from Finnhub Economic Calendar API
        events = await self._fetch_finnhub_calendar(start_date, end_date)

        # Add mock high-importance events for demonstration
        events.extend(self._get_upcoming_events(start_date, end_date))

        # Filter by importance and event type
        if importance:
            events = [e for e in events if e.get("importance") == importance]
        if event_type:
            events = [e for e in events if e.get("event_type") == event_type]

        # Add countdown timers
        for event in events:
            event["countdown"] = self._calculate_countdown(event["event_date"])

        # Cache for 1 hour
        await self.cache.set(cache_key, events, ttl=3600)

        return events

    async def _fetch_finnhub_calendar(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Fetch economic calendar from Finnhub"""
        try:
            url = "https://finnhub.io/api/v1/calendar/economic"
            params = {
                "token": self.settings.finnhub_api_key,
                "from": start_date.strftime("%Y-%m-%d"),
                "to": end_date.strftime("%Y-%m-%d")
            }

            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            events = []
            for item in data.get("economicCalendar", []):
                events.append({
                    "event_type": self._classify_event_type(item.get("event", "")),
                    "event_name": item.get("event", ""),
                    "event_date": datetime.fromisoformat(item.get("time", "").replace("Z", "+00:00")),
                    "event_time": item.get("time", ""),
                    "importance": self._classify_importance(item.get("impact", "")),
                    "previous_value": item.get("previous"),
                    "forecast_value": item.get("estimate"),
                    "actual_value": item.get("actual"),
                    "country": item.get("country", "US"),
                    "source": "finnhub"
                })

            return events

        except Exception as e:
            logger.error(f"Error fetching Finnhub calendar: {e}")
            return []

    def _get_upcoming_events(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get predefined high-importance events (FOMC, CPI, etc.)"""
        events = []

        # FOMC meetings (typically 8 per year, every 6 weeks)
        fomc_dates = self._get_fomc_dates(datetime.now().year)
        for fomc_date in fomc_dates:
            if start_date <= fomc_date <= end_date:
                events.append({
                    "event_type": EventType.FOMC,
                    "event_name": "FOMC Meeting Decision",
                    "event_date": fomc_date,
                    "event_time": "14:00 ET",
                    "importance": "HIGH",
                    "country": "US",
                    "source": "fed",
                    "description": "Federal Reserve interest rate decision and policy statement"
                })

        # CPI (monthly, typically around 13th)
        current = start_date.replace(day=13, hour=8, minute=30)
        while current <= end_date:
            if current >= start_date:
                events.append({
                    "event_type": EventType.CPI,
                    "event_name": "Consumer Price Index",
                    "event_date": current,
                    "event_time": "08:30 ET",
                    "importance": "HIGH",
                    "country": "US",
                    "source": "bls",
                    "description": "Inflation measure tracking consumer prices"
                })
            current = current.replace(month=current.month + 1 if current.month < 12 else 1,
                                     year=current.year + 1 if current.month == 12 else current.year)

        # Non-Farm Payrolls (first Friday of each month)
        nfp_dates = self._get_nfp_dates(start_date, end_date)
        for nfp_date in nfp_dates:
            events.append({
                "event_type": EventType.NFP,
                "event_name": "Non-Farm Payrolls",
                "event_date": nfp_date,
                "event_time": "08:30 ET",
                "importance": "HIGH",
                "country": "US",
                "source": "bls",
                "description": "Monthly employment report"
            })

        # Options expiration (3rd Friday of each month)
        opex_dates = self._get_options_expiration_dates(start_date, end_date)
        for opex_date in opex_dates:
            events.append({
                "event_type": EventType.OPTIONS_EXP,
                "event_name": "Monthly Options Expiration",
                "event_date": opex_date,
                "event_time": "16:00 ET",
                "importance": "MEDIUM",
                "country": "US",
                "source": "cboe",
                "description": "Monthly options expiration can cause increased volatility"
            })

        return events

    def _get_fomc_dates(self, year: int) -> List[datetime]:
        """Get FOMC meeting dates for the year"""
        # 2025 FOMC meeting dates (update these annually)
        fomc_2025 = [
            datetime(2025, 1, 29, 14, 0),
            datetime(2025, 3, 19, 14, 0),
            datetime(2025, 5, 7, 14, 0),
            datetime(2025, 6, 18, 14, 0),
            datetime(2025, 7, 30, 14, 0),
            datetime(2025, 9, 17, 14, 0),
            datetime(2025, 11, 5, 14, 0),
            datetime(2025, 12, 17, 14, 0)
        ]

        if year == 2025:
            return fomc_2025

        # For other years, estimate (every 6 weeks starting from late January)
        dates = []
        start = datetime(year, 1, 28, 14, 0)
        for i in range(8):
            dates.append(start + timedelta(weeks=6*i))
        return dates

    def _get_nfp_dates(self, start_date: datetime, end_date: datetime) -> List[datetime]:
        """Get Non-Farm Payroll dates (first Friday of each month)"""
        dates = []
        current = start_date.replace(day=1, hour=8, minute=30)

        while current <= end_date:
            # Find first Friday of the month
            while current.weekday() != 4:  # 4 = Friday
                current += timedelta(days=1)

            if start_date <= current <= end_date:
                dates.append(current)

            # Move to next month
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1, day=1)
            else:
                current = current.replace(month=current.month + 1, day=1)

        return dates

    def _get_options_expiration_dates(self, start_date: datetime, end_date: datetime) -> List[datetime]:
        """Get monthly options expiration dates (3rd Friday of each month)"""
        dates = []
        current = start_date.replace(day=1, hour=16, minute=0)

        while current <= end_date:
            # Find 3rd Friday of the month
            first_friday = current
            while first_friday.weekday() != 4:
                first_friday += timedelta(days=1)

            third_friday = first_friday + timedelta(weeks=2)

            if start_date <= third_friday <= end_date:
                dates.append(third_friday)

            # Move to next month
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1, day=1)
            else:
                current = current.replace(month=current.month + 1, day=1)

        return dates

    def _classify_event_type(self, event_name: str) -> str:
        """Classify event type from event name"""
        event_name_lower = event_name.lower()

        if "fomc" in event_name_lower or "fed" in event_name_lower or "interest rate" in event_name_lower:
            return EventType.FOMC
        elif "cpi" in event_name_lower or "inflation" in event_name_lower:
            return EventType.CPI
        elif "ppi" in event_name_lower:
            return EventType.PPI
        elif "gdp" in event_name_lower:
            return EventType.GDP
        elif "unemployment" in event_name_lower or "jobless" in event_name_lower:
            return EventType.UNEMPLOYMENT
        elif "nonfarm" in event_name_lower or "payroll" in event_name_lower:
            return EventType.NFP
        elif "retail sales" in event_name_lower:
            return EventType.RETAIL_SALES
        elif "pmi" in event_name_lower:
            return EventType.PMI
        elif "housing" in event_name_lower:
            return EventType.HOUSING
        else:
            return "OTHER"

    def _classify_importance(self, impact: str) -> str:
        """Classify event importance"""
        if not impact:
            return "MEDIUM"

        impact_lower = impact.lower()
        if impact_lower in ["high", "3"]:
            return "HIGH"
        elif impact_lower in ["low", "1"]:
            return "LOW"
        else:
            return "MEDIUM"

    def _calculate_countdown(self, event_date: datetime) -> Dict[str, Any]:
        """Calculate countdown to event"""
        now = datetime.now(event_date.tzinfo) if event_date.tzinfo else datetime.now()
        delta = event_date - now

        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        total_hours = days * 24 + hours

        return {
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "total_hours": total_hours,
            "is_past": delta.total_seconds() < 0,
            "human_readable": self._format_countdown(days, hours, minutes, delta.total_seconds() < 0)
        }

    def _format_countdown(self, days: int, hours: int, minutes: int, is_past: bool) -> str:
        """Format countdown for human readability"""
        if is_past:
            return "Past event"

        if days > 0:
            return f"{days}d {hours}h"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"

    async def get_historical_impact(
        self,
        event_type: str,
        symbol: str = "SPY",
        lookback_periods: int = 10
    ) -> Dict[str, Any]:
        """
        Get historical market reaction to event type

        Args:
            event_type: Type of event (FOMC, CPI, etc.)
            symbol: Ticker to analyze (default: SPY)
            lookback_periods: Number of past events to analyze
        """
        cache_key = f"event_impact:{event_type}:{symbol}:{lookback_periods}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        # In a real implementation, this would query the EventImpact table
        # For now, we'll return simulated historical data
        impact_data = self._simulate_historical_impact(event_type, symbol, lookback_periods)

        # Cache for 24 hours
        await self.cache.set(cache_key, impact_data, ttl=86400)

        return impact_data

    def _simulate_historical_impact(self, event_type: str, symbol: str, lookback: int) -> Dict[str, Any]:
        """Simulate historical impact data (replace with real DB queries)"""
        # Simulate different impacts for different event types
        event_volatility = {
            EventType.FOMC: {"mean": 1.2, "std": 0.8},
            EventType.CPI: {"mean": 0.8, "std": 0.6},
            EventType.NFP: {"mean": 0.6, "std": 0.4},
            EventType.PPI: {"mean": 0.4, "std": 0.3},
            EventType.GDP: {"mean": 0.5, "std": 0.3}
        }

        params = event_volatility.get(event_type, {"mean": 0.5, "std": 0.4})

        # Generate random historical returns
        np.random.seed(hash(event_type + symbol) % 2**32)
        returns_1d = np.random.normal(params["mean"], params["std"], lookback)
        returns_1w = returns_1d * 1.5 + np.random.normal(0, 0.3, lookback)

        return {
            "event_type": event_type,
            "symbol": symbol,
            "periods_analyzed": lookback,
            "average_reaction": {
                "1_day": {
                    "mean_change": float(np.mean(returns_1d)),
                    "median_change": float(np.median(returns_1d)),
                    "std_dev": float(np.std(returns_1d)),
                    "positive_rate": float(np.sum(returns_1d > 0) / lookback * 100),
                    "max_move": float(np.max(np.abs(returns_1d)))
                },
                "1_week": {
                    "mean_change": float(np.mean(returns_1w)),
                    "median_change": float(np.median(returns_1w)),
                    "std_dev": float(np.std(returns_1w)),
                    "positive_rate": float(np.sum(returns_1w > 0) / lookback * 100),
                    "max_move": float(np.max(np.abs(returns_1w)))
                }
            },
            "volatility_impact": {
                "average_vol_increase": f"{np.random.uniform(15, 40):.1f}%",
                "duration_days": int(np.random.uniform(1, 3))
            },
            "sector_performance": self._get_sector_performance(event_type),
            "pattern_success_rates": self._get_pattern_success_by_event(event_type)
        }

    def _get_sector_performance(self, event_type: str) -> Dict[str, float]:
        """Get typical sector performance around event"""
        # Simulate sector reactions
        sectors = ["Technology", "Financials", "Healthcare", "Energy", "Consumer", "Industrials"]

        # Different events affect sectors differently
        if event_type == EventType.FOMC:
            # Financials react strongly to rate decisions
            base_moves = [0.5, 1.8, 0.3, 0.4, 0.6, 0.7]
        elif event_type == EventType.CPI:
            # Consumer and retail sensitive to inflation
            base_moves = [0.8, 1.2, 0.5, 0.3, 1.5, 0.6]
        else:
            base_moves = [0.6, 0.7, 0.5, 0.5, 0.6, 0.6]

        return {sector: round(move, 2) for sector, move in zip(sectors, base_moves)}

    def _get_pattern_success_by_event(self, event_type: str) -> Dict[str, float]:
        """Get pattern success rates around this event type"""
        patterns = ["VCP", "Cup & Handle", "Flat Base", "Ascending Triangle"]

        # Events typically reduce pattern success rates due to volatility
        if event_type in [EventType.FOMC, EventType.CPI]:
            success_rates = [0.55, 0.52, 0.58, 0.54]
        else:
            success_rates = [0.65, 0.63, 0.68, 0.64]

        return {pattern: round(rate * 100, 1) for pattern, rate in zip(patterns, success_rates)}

    async def detect_market_regime(self, symbols: List[str] = None) -> Dict[str, Any]:
        """
        Detect current market regime

        Analyzes:
        - Trend (bull/bear/sideways)
        - Volatility (high/low/normal)
        - Rate environment
        - Seasonal patterns
        """
        if not symbols:
            symbols = ["SPY", "QQQ", "IWM"]  # Major indices

        cache_key = "market_regime:current"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        regime = await self._analyze_market_regime(symbols)

        # Cache for 1 hour
        await self.cache.set(cache_key, regime, ttl=3600)

        return regime

    async def _analyze_market_regime(self, symbols: List[str]) -> Dict[str, Any]:
        """Analyze current market regime using multiple indicators"""
        # In production, this would fetch real market data
        # For now, simulate regime detection

        now = datetime.now()

        # Simulate VIX analysis
        vix_level = np.random.uniform(12, 25)
        vix_percentile = self._calculate_vix_percentile(vix_level)

        # Determine volatility regime
        if vix_level > 25:
            vol_regime = VolatilityRegime.HIGH_VOL
        elif vix_level < 15:
            vol_regime = VolatilityRegime.LOW_VOL
        else:
            vol_regime = VolatilityRegime.NORMAL

        # Simulate trend analysis (would use 50/200 day MAs)
        trend_strength = np.random.uniform(20, 50)
        if trend_strength > 35:
            regime_type = MarketRegimeType.BULL
        elif trend_strength < 25:
            regime_type = MarketRegimeType.BEAR
        else:
            regime_type = MarketRegimeType.SIDEWAYS

        # Rate environment (would fetch from FRED API)
        fed_funds_rate = 5.25  # Current estimate
        rate_trend = RateEnvironment.STABLE

        # Seasonal pattern
        seasonal = self._detect_seasonal_pattern(now)

        # Market breadth (would calculate from NYSE advance/decline)
        market_breadth = np.random.uniform(0.4, 0.7)

        regime = {
            "regime_type": regime_type.value,
            "volatility_regime": vol_regime.value,
            "rate_environment": rate_trend.value,
            "seasonal_pattern": seasonal,
            "vix_level": round(vix_level, 2),
            "vix_percentile": round(vix_percentile, 1),
            "trend_strength": round(trend_strength, 1),
            "market_breadth": round(market_breadth, 2),
            "fed_funds_rate": fed_funds_rate,
            "confidence_score": round(np.random.uniform(70, 95), 1),
            "indicators": {
                "spy_above_200ma": bool(np.random.random() > 0.3),
                "nasdaq_above_200ma": bool(np.random.random() > 0.3),
                "new_highs_vs_lows": round(np.random.uniform(0.8, 2.5), 2),
                "put_call_ratio": round(np.random.uniform(0.7, 1.2), 2)
            },
            "interpretation": self._interpret_regime(regime_type, vol_regime, rate_trend),
            "trading_implications": self._get_trading_implications(regime_type, vol_regime)
        }

        return regime

    def _calculate_vix_percentile(self, vix_level: float) -> float:
        """Calculate VIX percentile (rough approximation)"""
        # Historical VIX ranges from ~10 to ~80
        # Normalize to percentile
        if vix_level < 12:
            return 10
        elif vix_level < 15:
            return 25
        elif vix_level < 20:
            return 50
        elif vix_level < 25:
            return 70
        elif vix_level < 30:
            return 85
        else:
            return 95

    def _detect_seasonal_pattern(self, date: datetime) -> Optional[str]:
        """Detect if we're in a known seasonal pattern"""
        month = date.month

        if month in [11, 12]:
            return "SANTA_RALLY"
        elif month == 1:
            return "JANUARY_EFFECT"
        elif month in [5, 6]:
            return "SELL_IN_MAY"
        elif month in [9, 10]:
            return "SEPTEMBER_WEAKNESS"
        else:
            return None

    def _interpret_regime(
        self,
        regime_type: MarketRegimeType,
        vol_regime: VolatilityRegime,
        rate_env: RateEnvironment
    ) -> str:
        """Interpret the current market regime"""
        interpretations = {
            (MarketRegimeType.BULL, VolatilityRegime.LOW_VOL):
                "Strong bull market with low volatility - ideal for pattern trading",
            (MarketRegimeType.BULL, VolatilityRegime.HIGH_VOL):
                "Bull market with elevated volatility - trade with caution",
            (MarketRegimeType.BEAR, VolatilityRegime.HIGH_VOL):
                "Bear market with high volatility - focus on capital preservation",
            (MarketRegimeType.SIDEWAYS, VolatilityRegime.NORMAL):
                "Range-bound market - trade breakouts carefully"
        }

        key = (regime_type, vol_regime)
        return interpretations.get(key, "Mixed market conditions - trade selectively")

    def _get_trading_implications(
        self,
        regime_type: MarketRegimeType,
        vol_regime: VolatilityRegime
    ) -> Dict[str, Any]:
        """Get trading implications for current regime"""
        if regime_type == MarketRegimeType.BULL and vol_regime == VolatilityRegime.LOW_VOL:
            return {
                "position_sizing": "NORMAL to AGGRESSIVE",
                "pattern_reliability": "HIGH",
                "recommended_stop": "7-8% below entry",
                "hold_duration": "Swing to Position (days to weeks)",
                "sectors_to_favor": ["Technology", "Growth", "Consumer Discretionary"]
            }
        elif regime_type == MarketRegimeType.BEAR or vol_regime == VolatilityRegime.HIGH_VOL:
            return {
                "position_sizing": "CONSERVATIVE to HALF",
                "pattern_reliability": "MEDIUM to LOW",
                "recommended_stop": "4-5% below entry (tighter)",
                "hold_duration": "Day trade to Short swing",
                "sectors_to_favor": ["Defensive", "Healthcare", "Utilities", "Consumer Staples"]
            }
        else:
            return {
                "position_sizing": "NORMAL",
                "pattern_reliability": "MEDIUM",
                "recommended_stop": "6-7% below entry",
                "hold_duration": "Swing (days to week)",
                "sectors_to_favor": ["Quality Growth", "Dividend Growers"]
            }

    async def get_next_event_countdown(self, event_type: Optional[str] = None) -> Dict[str, Any]:
        """Get countdown to next major event"""
        events = await self.get_economic_calendar(
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=90),
            importance="HIGH",
            event_type=event_type
        )

        if not events:
            return {"error": "No upcoming events found"}

        # Sort by date
        events.sort(key=lambda x: x["event_date"])

        next_event = events[0]

        return {
            "event": next_event,
            "countdown": next_event["countdown"],
            "upcoming_events": events[:5]  # Next 5 events
        }

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
