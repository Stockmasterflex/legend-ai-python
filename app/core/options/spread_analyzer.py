"""
Options Spread Analyzer and Strategy Builder
Analyzes and visualizes option spreads and strategies
"""
import numpy as np
from typing import Dict, List, Tuple, Optional
from .greeks_calculator import GreeksCalculator


class SpreadAnalyzer:
    """Analyze options spreads and calculate P&L profiles"""

    def __init__(self):
        self.greeks_calc = GreeksCalculator()

    def calculate_vertical_spread(
        self,
        long_strike: float,
        short_strike: float,
        spread_type: str,  # 'call' or 'put'
        debit: float,  # Net debit paid (long premium - short premium)
        spot_price: float,
        num_contracts: int = 1
    ) -> Dict[str, any]:
        """
        Calculate P&L profile for vertical spread

        Args:
            long_strike: Strike of long leg
            short_strike: Strike of short leg
            spread_type: 'call' or 'put'
            debit: Net debit paid
            spot_price: Current stock price
            num_contracts: Number of contracts

        Returns:
            Dict with max_profit, max_loss, breakeven, risk_reward, P&L profile
        """
        multiplier = num_contracts * 100

        if spread_type == "call":
            # Bull call spread
            max_profit = (short_strike - long_strike - debit) * multiplier
            max_loss = debit * multiplier
            breakeven = long_strike + debit
        else:  # put
            # Bear put spread
            max_profit = (long_strike - short_strike - debit) * multiplier
            max_loss = debit * multiplier
            breakeven = long_strike - debit

        risk_reward = abs(max_profit / max_loss) if max_loss != 0 else 0

        # Generate P&L profile
        price_range = np.linspace(
            min(long_strike, short_strike) * 0.8,
            max(long_strike, short_strike) * 1.2,
            100
        )

        pnl_profile = []
        for price in price_range:
            pnl = self._calculate_spread_pnl(
                price, long_strike, short_strike, spread_type, debit, num_contracts
            )
            pnl_profile.append({"price": round(price, 2), "pnl": round(pnl, 2)})

        # Current P&L
        current_pnl = self._calculate_spread_pnl(
            spot_price, long_strike, short_strike, spread_type, debit, num_contracts
        )

        return {
            "spread_type": f"{spread_type}_spread",
            "long_strike": long_strike,
            "short_strike": short_strike,
            "max_profit": round(max_profit, 2),
            "max_loss": round(max_loss, 2),
            "breakeven": round(breakeven, 2),
            "risk_reward_ratio": round(risk_reward, 2),
            "current_pnl": round(current_pnl, 2),
            "pnl_profile": pnl_profile,
            "width": abs(short_strike - long_strike),
            "debit": debit
        }

    def calculate_iron_condor(
        self,
        put_long_strike: float,
        put_short_strike: float,
        call_short_strike: float,
        call_long_strike: float,
        credit: float,  # Net credit received
        spot_price: float,
        num_contracts: int = 1
    ) -> Dict[str, any]:
        """
        Calculate P&L profile for iron condor

        Args:
            put_long_strike: Long put strike
            put_short_strike: Short put strike
            call_short_strike: Short call strike
            call_long_strike: Long call strike
            credit: Net credit received
            spot_price: Current stock price
            num_contracts: Number of contracts

        Returns:
            Dict with max_profit, max_loss, breakevens, P&L profile
        """
        multiplier = num_contracts * 100

        # Iron condor is net credit strategy
        max_profit = credit * multiplier

        # Max loss is the wider wing minus credit
        put_wing_width = put_short_strike - put_long_strike
        call_wing_width = call_long_strike - call_short_strike
        max_wing_width = max(put_wing_width, call_wing_width)

        max_loss = (max_wing_width - credit) * multiplier

        # Breakevens
        lower_breakeven = put_short_strike - credit
        upper_breakeven = call_short_strike + credit

        risk_reward = abs(max_profit / max_loss) if max_loss != 0 else 0

        # Generate P&L profile
        price_range = np.linspace(
            put_long_strike * 0.9,
            call_long_strike * 1.1,
            100
        )

        pnl_profile = []
        for price in price_range:
            # Calculate P&L for each leg
            long_put_pnl = max(0, put_long_strike - price) * multiplier
            short_put_pnl = -max(0, put_short_strike - price) * multiplier
            short_call_pnl = -max(0, price - call_short_strike) * multiplier
            long_call_pnl = max(0, price - call_long_strike) * multiplier

            total_pnl = (
                long_put_pnl + short_put_pnl + short_call_pnl + long_call_pnl
                + credit * multiplier
            )

            pnl_profile.append({"price": round(price, 2), "pnl": round(total_pnl, 2)})

        # Current P&L
        current_pnl = next(
            (p["pnl"] for p in pnl_profile if abs(p["price"] - spot_price) < 0.5),
            0
        )

        return {
            "spread_type": "iron_condor",
            "put_long_strike": put_long_strike,
            "put_short_strike": put_short_strike,
            "call_short_strike": call_short_strike,
            "call_long_strike": call_long_strike,
            "max_profit": round(max_profit, 2),
            "max_loss": round(max_loss, 2),
            "lower_breakeven": round(lower_breakeven, 2),
            "upper_breakeven": round(upper_breakeven, 2),
            "risk_reward_ratio": round(risk_reward, 2),
            "current_pnl": round(current_pnl, 2),
            "pnl_profile": pnl_profile,
            "credit": credit,
            "probability_of_profit": round(
                (upper_breakeven - lower_breakeven) / spot_price * 100, 2
            )
        }

    def calculate_butterfly(
        self,
        lower_strike: float,
        middle_strike: float,
        upper_strike: float,
        option_type: str,  # 'call' or 'put'
        debit: float,
        spot_price: float,
        num_contracts: int = 1
    ) -> Dict[str, any]:
        """
        Calculate P&L profile for butterfly spread

        Args:
            lower_strike: Lower wing strike
            middle_strike: Body strike (2x short)
            upper_strike: Upper wing strike
            option_type: 'call' or 'put'
            debit: Net debit paid
            spot_price: Current stock price
            num_contracts: Number of contracts

        Returns:
            Dict with max_profit, max_loss, breakevens, P&L profile
        """
        multiplier = num_contracts * 100

        # Max profit at middle strike
        max_profit = (middle_strike - lower_strike - debit) * multiplier
        max_loss = debit * multiplier

        # Breakevens
        lower_breakeven = lower_strike + debit
        upper_breakeven = upper_strike - debit

        risk_reward = abs(max_profit / max_loss) if max_loss != 0 else 0

        # Generate P&L profile
        price_range = np.linspace(lower_strike * 0.9, upper_strike * 1.1, 100)

        pnl_profile = []
        for price in price_range:
            if option_type == "call":
                # Long 1 lower strike, short 2 middle strikes, long 1 upper strike
                pnl = (
                    max(0, price - lower_strike)
                    - 2 * max(0, price - middle_strike)
                    + max(0, price - upper_strike)
                    - debit
                ) * multiplier
            else:  # put
                pnl = (
                    max(0, lower_strike - price)
                    - 2 * max(0, middle_strike - price)
                    + max(0, upper_strike - price)
                    - debit
                ) * multiplier

            pnl_profile.append({"price": round(price, 2), "pnl": round(pnl, 2)})

        # Current P&L
        current_pnl = next(
            (p["pnl"] for p in pnl_profile if abs(p["price"] - spot_price) < 0.5),
            0
        )

        return {
            "spread_type": f"{option_type}_butterfly",
            "lower_strike": lower_strike,
            "middle_strike": middle_strike,
            "upper_strike": upper_strike,
            "max_profit": round(max_profit, 2),
            "max_loss": round(max_loss, 2),
            "lower_breakeven": round(lower_breakeven, 2),
            "upper_breakeven": round(upper_breakeven, 2),
            "risk_reward_ratio": round(risk_reward, 2),
            "current_pnl": round(current_pnl, 2),
            "pnl_profile": pnl_profile,
            "debit": debit
        }

    def calculate_straddle(
        self,
        strike: float,
        call_price: float,
        put_price: float,
        spot_price: float,
        num_contracts: int = 1,
        is_long: bool = True
    ) -> Dict[str, any]:
        """
        Calculate P&L profile for straddle (long or short)

        Args:
            strike: Strike price (same for call and put)
            call_price: Call option price
            put_price: Put option price
            spot_price: Current stock price
            num_contracts: Number of contracts
            is_long: True for long straddle, False for short straddle

        Returns:
            Dict with breakevens, max profit/loss, P&L profile
        """
        multiplier = num_contracts * 100
        total_premium = call_price + put_price

        if is_long:
            # Long straddle - pay premium, unlimited profit potential
            max_loss = total_premium * multiplier
            max_profit = float('inf')  # Unlimited
            lower_breakeven = strike - total_premium
            upper_breakeven = strike + total_premium
        else:
            # Short straddle - receive premium, unlimited loss potential
            max_profit = total_premium * multiplier
            max_loss = float('inf')  # Unlimited
            lower_breakeven = strike - total_premium
            upper_breakeven = strike + total_premium

        # Generate P&L profile
        price_range = np.linspace(strike * 0.7, strike * 1.3, 100)

        pnl_profile = []
        for price in price_range:
            call_pnl = max(0, price - strike) - call_price
            put_pnl = max(0, strike - price) - put_price

            if is_long:
                total_pnl = (call_pnl + put_pnl) * multiplier
            else:
                total_pnl = -(call_pnl + put_pnl) * multiplier

            pnl_profile.append({"price": round(price, 2), "pnl": round(total_pnl, 2)})

        # Current P&L
        current_pnl = next(
            (p["pnl"] for p in pnl_profile if abs(p["price"] - spot_price) < 0.5),
            0
        )

        return {
            "spread_type": "long_straddle" if is_long else "short_straddle",
            "strike": strike,
            "call_price": call_price,
            "put_price": put_price,
            "total_premium": total_premium,
            "max_profit": max_profit if max_profit != float('inf') else "Unlimited",
            "max_loss": max_loss if max_loss != float('inf') else "Unlimited",
            "lower_breakeven": round(lower_breakeven, 2),
            "upper_breakeven": round(upper_breakeven, 2),
            "current_pnl": round(current_pnl, 2),
            "pnl_profile": pnl_profile
        }

    def _calculate_spread_pnl(
        self,
        price: float,
        long_strike: float,
        short_strike: float,
        spread_type: str,
        debit: float,
        num_contracts: int
    ) -> float:
        """Calculate P&L for vertical spread at given price"""
        multiplier = num_contracts * 100

        if spread_type == "call":
            long_value = max(0, price - long_strike)
            short_value = max(0, price - short_strike)
        else:  # put
            long_value = max(0, long_strike - price)
            short_value = max(0, short_strike - price)

        pnl = (long_value - short_value - debit) * multiplier
        return pnl

    def analyze_strategy_greeks(
        self,
        legs: List[Dict],
        spot_price: float,
        time_to_expiry: float,
        risk_free_rate: float = 0.05
    ) -> Dict[str, float]:
        """
        Calculate total Greeks for multi-leg strategy

        Args:
            legs: List of option legs with strike, type, position (1 for long, -1 for short), quantity
            spot_price: Current stock price
            time_to_expiry: Time to expiration in years
            risk_free_rate: Risk-free rate

        Returns:
            Dict with total delta, gamma, theta, vega, rho
        """
        total_greeks = {
            "delta": 0,
            "gamma": 0,
            "theta": 0,
            "vega": 0,
            "rho": 0
        }

        for leg in legs:
            strike = leg["strike"]
            option_type = leg["type"]
            position = leg.get("position", 1)  # 1 for long, -1 for short
            quantity = leg.get("quantity", 1)
            iv = leg.get("iv", 0.3)  # Default IV

            greeks = self.greeks_calc.calculate_greeks(
                spot_price=spot_price,
                strike=strike,
                time_to_expiry=time_to_expiry,
                risk_free_rate=risk_free_rate,
                volatility=iv,
                option_type=option_type
            )

            # Aggregate Greeks
            for greek in total_greeks:
                total_greeks[greek] += greeks[greek] * position * quantity

        # Round results
        for greek in total_greeks:
            total_greeks[greek] = round(total_greeks[greek], 4)

        return total_greeks
