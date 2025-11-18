"""
Options Strategy Builder
Build and analyze options strategies with risk/reward calculations
"""
import httpx
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timedelta
import asyncio
import logging
from enum import Enum
import pandas as pd
import numpy as np
from dataclasses import dataclass

from app.config import get_settings
from app.services.cache import get_cache_service
from app.services.options_data import get_options_service

logger = logging.getLogger(__name__)


class StrategyType(str, Enum):
    COVERED_CALL = "covered_call"
    PROTECTIVE_PUT = "protective_put"
    BULL_CALL_SPREAD = "bull_call_spread"
    BEAR_PUT_SPREAD = "bear_put_spread"
    IRON_CONDOR = "iron_condor"
    BUTTERFLY = "butterfly"
    STRADDLE = "straddle"
    STRANGLE = "strangle"


@dataclass
class OptionLeg:
    """Represents a single option leg"""
    option_type: str  # "call" or "put"
    strike: float
    expiration: str
    action: str  # "buy" or "sell"
    quantity: int
    price: float
    delta: float = 0.0
    gamma: float = 0.0
    theta: float = 0.0
    vega: float = 0.0


@dataclass
class Strategy:
    """Represents a complete options strategy"""
    name: str
    strategy_type: StrategyType
    legs: List[OptionLeg]
    stock_position: Optional[int] = None  # For covered calls, protective puts
    stock_price: float = 0.0


class OptionsStrategyBuilder:
    """
    Build and analyze options strategies

    Features:
    - Covered calls
    - Protective puts
    - Vertical spreads
    - Risk/reward analysis
    - Greeks for full strategy
    """

    def __init__(self):
        self.settings = get_settings()
        self.cache = get_cache_service()
        self.options_service = get_options_service()

    async def build_covered_call(
        self,
        symbol: str,
        stock_quantity: int = 100,
        target_delta: float = 0.30,
        expiration: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Build covered call strategy

        Sell OTM calls against long stock position

        Args:
            symbol: Stock ticker
            stock_quantity: Number of shares owned (multiples of 100)
            target_delta: Target delta for sold call (0.30 = 30 delta)
            expiration: Expiration date, defaults to 30-45 days out

        Returns:
            Covered call strategy with P&L analysis
        """
        cache_key = f"covered_call:{symbol}:{stock_quantity}:{target_delta}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        try:
            # Get options chain
            chain = await self.options_service.get_options_chain(symbol, expiration)

            calls = chain.get("calls", [])
            if not calls:
                return {"error": "No call options available"}

            # Find call closest to target delta
            target_call = min(
                calls,
                key=lambda x: abs(x.get("delta", 0) - target_delta)
            )

            # Calculate strategy details
            contracts = stock_quantity // 100
            premium_collected = target_call.get("bid", 0) * 100 * contracts
            strike = target_call.get("strike")

            # Calculate stock cost (assume current mid-strike as proxy for stock price)
            strikes = [c["strike"] for c in calls]
            stock_price = sorted(strikes)[len(strikes) // 2]

            strategy = {
                "strategy_type": "covered_call",
                "symbol": symbol,
                "stock_position": {
                    "quantity": stock_quantity,
                    "price": stock_price,
                    "value": stock_price * stock_quantity
                },
                "call_sold": {
                    "strike": strike,
                    "premium": target_call.get("bid", 0),
                    "contracts": contracts,
                    "total_premium": premium_collected,
                    "delta": target_call.get("delta"),
                    "theta": target_call.get("theta"),
                    "expiration": chain.get("expiration")
                },
                "analysis": {
                    "max_profit": (strike - stock_price) * stock_quantity + premium_collected,
                    "max_loss": stock_price * stock_quantity - premium_collected,  # Stock goes to 0
                    "breakeven": stock_price - (premium_collected / stock_quantity),
                    "return_if_called": ((strike - stock_price) * stock_quantity + premium_collected) / (stock_price * stock_quantity) * 100,
                    "downside_protection": premium_collected / (stock_price * stock_quantity) * 100,
                    "probability_profit": 50 + (target_delta * 50)  # Approximation
                },
                "greeks": {
                    "delta": stock_quantity - (target_call.get("delta", 0) * contracts * 100),
                    "theta": target_call.get("theta", 0) * contracts * 100,
                    "vega": -target_call.get("vega", 0) * contracts * 100
                },
                "recommendation": self._get_covered_call_recommendation(
                    stock_price,
                    strike,
                    premium_collected,
                    target_call.get("implied_volatility", 0)
                )
            }

            await self.cache.set(cache_key, strategy, ttl=600)
            return strategy

        except Exception as e:
            logger.error(f"Error building covered call for {symbol}: {e}")
            return {"error": str(e)}

    async def build_protective_put(
        self,
        symbol: str,
        stock_quantity: int = 100,
        protection_level: float = 0.05,  # 5% below current price
        expiration: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Build protective put strategy

        Buy OTM puts to hedge long stock position

        Args:
            symbol: Stock ticker
            stock_quantity: Number of shares owned
            protection_level: How far OTM (0.05 = 5% below stock price)
            expiration: Expiration date

        Returns:
            Protective put strategy with analysis
        """
        cache_key = f"protective_put:{symbol}:{stock_quantity}:{protection_level}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        try:
            chain = await self.options_service.get_options_chain(symbol, expiration)

            puts = chain.get("puts", [])
            if not puts:
                return {"error": "No put options available"}

            # Estimate stock price from strikes
            strikes = [p["strike"] for p in puts]
            stock_price = sorted(strikes)[len(strikes) // 2]

            # Find put at desired protection level
            target_strike = stock_price * (1 - protection_level)
            target_put = min(
                puts,
                key=lambda x: abs(x.get("strike", 0) - target_strike)
            )

            contracts = stock_quantity // 100
            put_cost = target_put.get("ask", 0) * 100 * contracts

            strategy = {
                "strategy_type": "protective_put",
                "symbol": symbol,
                "stock_position": {
                    "quantity": stock_quantity,
                    "price": stock_price,
                    "value": stock_price * stock_quantity
                },
                "put_bought": {
                    "strike": target_put.get("strike"),
                    "premium": target_put.get("ask", 0),
                    "contracts": contracts,
                    "total_cost": put_cost,
                    "delta": target_put.get("delta"),
                    "theta": target_put.get("theta"),
                    "expiration": chain.get("expiration")
                },
                "analysis": {
                    "max_loss": (stock_price - target_put.get("strike")) * stock_quantity + put_cost,
                    "max_profit": "Unlimited",
                    "breakeven": stock_price + (put_cost / stock_quantity),
                    "insurance_cost": put_cost / (stock_price * stock_quantity) * 100,
                    "protection_starts_at": target_put.get("strike"),
                    "protection_percentage": ((stock_price - target_put.get("strike")) / stock_price) * 100
                },
                "greeks": {
                    "delta": stock_quantity + (target_put.get("delta", 0) * contracts * 100),
                    "theta": target_put.get("theta", 0) * contracts * 100,
                    "vega": target_put.get("vega", 0) * contracts * 100
                },
                "recommendation": self._get_protective_put_recommendation(
                    protection_level,
                    put_cost,
                    stock_price * stock_quantity
                )
            }

            await self.cache.set(cache_key, strategy, ttl=600)
            return strategy

        except Exception as e:
            logger.error(f"Error building protective put for {symbol}: {e}")
            return {"error": str(e)}

    async def build_vertical_spread(
        self,
        symbol: str,
        spread_type: str = "bull_call",
        width: float = 5.0,  # Strike width
        expiration: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Build vertical spread strategy

        Args:
            symbol: Stock ticker
            spread_type: "bull_call", "bear_put", "bull_put", "bear_call"
            width: Distance between strikes
            expiration: Expiration date

        Returns:
            Vertical spread strategy with analysis
        """
        cache_key = f"vertical_spread:{symbol}:{spread_type}:{width}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        try:
            chain = await self.options_service.get_options_chain(symbol, expiration)

            if spread_type in ["bull_call", "bear_call"]:
                options = chain.get("calls", [])
                option_type = "call"
            else:
                options = chain.get("puts", [])
                option_type = "put"

            if len(options) < 2:
                return {"error": f"Insufficient {option_type} options"}

            # Find ATM strike
            strikes = sorted([opt["strike"] for opt in options])
            atm_strike = strikes[len(strikes) // 2]

            # For bull spreads, buy ATM and sell OTM
            # For bear spreads, sell ATM and buy OTM
            if spread_type in ["bull_call", "bull_put"]:
                long_strike = atm_strike
                short_strike = atm_strike + width
            else:  # bear spreads
                long_strike = atm_strike + width
                short_strike = atm_strike

            # Find options at these strikes
            long_option = next((opt for opt in options if opt["strike"] == long_strike), None)
            short_option = next((opt for opt in options if opt["strike"] == short_strike), None)

            if not long_option or not short_option:
                return {"error": "Could not find options at target strikes"}

            # Calculate costs and P&L
            long_cost = long_option.get("ask", 0) * 100
            short_credit = short_option.get("bid", 0) * 100
            net_debit = long_cost - short_credit

            if spread_type in ["bull_call", "bear_put"]:
                max_profit = (width * 100) - net_debit
                max_loss = net_debit
            else:  # credit spreads
                max_profit = abs(net_debit)
                max_loss = (width * 100) - abs(net_debit)

            strategy = {
                "strategy_type": spread_type,
                "symbol": symbol,
                "legs": {
                    "long": {
                        "type": option_type,
                        "strike": long_strike,
                        "premium": long_option.get("ask"),
                        "cost": long_cost,
                        "delta": long_option.get("delta"),
                        "theta": long_option.get("theta")
                    },
                    "short": {
                        "type": option_type,
                        "strike": short_strike,
                        "premium": short_option.get("bid"),
                        "credit": short_credit,
                        "delta": short_option.get("delta"),
                        "theta": short_option.get("theta")
                    }
                },
                "analysis": {
                    "net_debit": net_debit,
                    "max_profit": max_profit,
                    "max_loss": max_loss,
                    "risk_reward_ratio": max_profit / max_loss if max_loss > 0 else 0,
                    "breakeven": self._calculate_spread_breakeven(
                        spread_type,
                        long_strike,
                        short_strike,
                        net_debit
                    ),
                    "probability_profit": self._estimate_spread_pop(
                        long_option.get("delta", 0),
                        short_option.get("delta", 0),
                        spread_type
                    )
                },
                "greeks": {
                    "delta": long_option.get("delta", 0) - short_option.get("delta", 0),
                    "theta": long_option.get("theta", 0) - short_option.get("theta", 0),
                    "vega": long_option.get("vega", 0) - short_option.get("vega", 0)
                },
                "payoff_diagram": self._generate_payoff_points(
                    spread_type,
                    long_strike,
                    short_strike,
                    net_debit,
                    width
                )
            }

            await self.cache.set(cache_key, strategy, ttl=600)
            return strategy

        except Exception as e:
            logger.error(f"Error building vertical spread for {symbol}: {e}")
            return {"error": str(e)}

    def _calculate_spread_breakeven(
        self,
        spread_type: str,
        long_strike: float,
        short_strike: float,
        net_debit: float
    ) -> float:
        """Calculate breakeven for vertical spread"""
        if spread_type == "bull_call":
            return long_strike + (net_debit / 100)
        elif spread_type == "bear_put":
            return long_strike - (net_debit / 100)
        elif spread_type == "bull_put":
            return short_strike - (abs(net_debit) / 100)
        else:  # bear_call
            return short_strike + (abs(net_debit) / 100)

    def _estimate_spread_pop(
        self,
        long_delta: float,
        short_delta: float,
        spread_type: str
    ) -> float:
        """Estimate probability of profit for spread"""
        if spread_type in ["bull_call", "bull_put"]:
            # Bullish spreads profit if stock rises
            return (1 - abs(short_delta)) * 100
        else:
            # Bearish spreads profit if stock falls
            return abs(short_delta) * 100

    def _generate_payoff_points(
        self,
        spread_type: str,
        long_strike: float,
        short_strike: float,
        net_debit: float,
        width: float
    ) -> List[Dict[str, float]]:
        """
        Generate payoff diagram points for visualization

        Returns:
            List of {"price": x, "pnl": y} points
        """
        points = []

        # Generate price range (±20% from strikes)
        min_price = min(long_strike, short_strike) * 0.8
        max_price = max(long_strike, short_strike) * 1.2
        step = (max_price - min_price) / 50

        for price in np.arange(min_price, max_price, step):
            pnl = self._calculate_spread_pnl(
                price,
                spread_type,
                long_strike,
                short_strike,
                net_debit
            )
            points.append({"price": round(price, 2), "pnl": round(pnl, 2)})

        return points

    def _calculate_spread_pnl(
        self,
        stock_price: float,
        spread_type: str,
        long_strike: float,
        short_strike: float,
        net_debit: float
    ) -> float:
        """Calculate P&L for spread at given stock price"""
        if spread_type == "bull_call":
            long_value = max(0, stock_price - long_strike) * 100
            short_value = max(0, stock_price - short_strike) * 100
            return long_value - short_value - net_debit

        elif spread_type == "bear_put":
            long_value = max(0, long_strike - stock_price) * 100
            short_value = max(0, short_strike - stock_price) * 100
            return long_value - short_value - net_debit

        elif spread_type == "bull_put":
            long_value = max(0, long_strike - stock_price) * 100
            short_value = max(0, short_strike - stock_price) * 100
            return abs(net_debit) - (long_value - short_value)

        else:  # bear_call
            long_value = max(0, stock_price - long_strike) * 100
            short_value = max(0, stock_price - short_strike) * 100
            return abs(net_debit) - (long_value - short_value)

    def _get_covered_call_recommendation(
        self,
        stock_price: float,
        strike: float,
        premium: float,
        iv: float
    ) -> str:
        """Generate recommendation for covered call"""
        return_if_called = ((strike - stock_price) + (premium / 100)) / stock_price * 100

        if iv > 50:
            return f"Excellent - High IV ({iv:.1f}%) provides {return_if_called:.1f}% return if called"
        elif return_if_called > 2:
            return f"Good - {return_if_called:.1f}% return if called"
        else:
            return "Fair - Consider waiting for higher IV"

    def _get_protective_put_recommendation(
        self,
        protection_level: float,
        cost: float,
        position_value: float
    ) -> str:
        """Generate recommendation for protective put"""
        insurance_pct = cost / position_value * 100

        if insurance_pct < 2:
            return f"Excellent - Only {insurance_pct:.1f}% cost for {protection_level*100:.0f}% protection"
        elif insurance_pct < 5:
            return f"Good - {insurance_pct:.1f}% insurance cost"
        else:
            return f"Expensive - {insurance_pct:.1f}% cost, consider wider protection"

    async def close(self):
        """Cleanup"""
        pass


# Singleton instance
_strategy_builder: Optional[OptionsStrategyBuilder] = None


def get_strategy_builder() -> OptionsStrategyBuilder:
    """Get or create strategy builder singleton"""
    global _strategy_builder
    if _strategy_builder is None:
        _strategy_builder = OptionsStrategyBuilder()
    return _strategy_builder
