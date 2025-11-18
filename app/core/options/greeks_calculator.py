"""
Options Greeks Calculator
Calculates Delta, Gamma, Theta, Vega, Rho using Black-Scholes model
"""
import numpy as np
from scipy.stats import norm
from typing import Dict, Optional
from datetime import datetime, timedelta


class GreeksCalculator:
    """Calculate options Greeks using Black-Scholes model"""

    @staticmethod
    def _d1(S: float, K: float, T: float, r: float, sigma: float) -> float:
        """Calculate d1 component of Black-Scholes"""
        return (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    @staticmethod
    def _d2(d1: float, sigma: float, T: float) -> float:
        """Calculate d2 component of Black-Scholes"""
        return d1 - sigma * np.sqrt(T)

    def calculate_greeks(
        self,
        spot_price: float,
        strike: float,
        time_to_expiry: float,  # in years
        risk_free_rate: float,
        volatility: float,
        option_type: str = "call"
    ) -> Dict[str, float]:
        """
        Calculate all Greeks for an option

        Args:
            spot_price: Current stock price
            strike: Strike price
            time_to_expiry: Time to expiration in years
            risk_free_rate: Risk-free interest rate (annualized)
            volatility: Implied volatility (annualized)
            option_type: 'call' or 'put'

        Returns:
            Dict with delta, gamma, theta, vega, rho, and theoretical price
        """
        if time_to_expiry <= 0:
            return self._calculate_greeks_at_expiry(spot_price, strike, option_type)

        S = spot_price
        K = strike
        T = time_to_expiry
        r = risk_free_rate
        sigma = volatility

        # Calculate d1 and d2
        d1 = self._d1(S, K, T, r, sigma)
        d2 = self._d2(d1, sigma, T)

        # Calculate Greeks
        if option_type.lower() == "call":
            delta = norm.cdf(d1)
            theta = (
                -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                - r * K * np.exp(-r * T) * norm.cdf(d2)
            ) / 365  # Convert to daily theta
            rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100  # Per 1% change
            price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:  # put
            delta = -norm.cdf(-d1)
            theta = (
                -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                + r * K * np.exp(-r * T) * norm.cdf(-d2)
            ) / 365  # Convert to daily theta
            rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100  # Per 1% change
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

        # Gamma and Vega are same for calls and puts
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        vega = S * norm.pdf(d1) * np.sqrt(T) / 100  # Per 1% change in IV

        return {
            "delta": round(delta, 4),
            "gamma": round(gamma, 4),
            "theta": round(theta, 4),
            "vega": round(vega, 4),
            "rho": round(rho, 4),
            "price": round(price, 2)
        }

    def _calculate_greeks_at_expiry(
        self,
        spot_price: float,
        strike: float,
        option_type: str
    ) -> Dict[str, float]:
        """Calculate Greeks for expired options"""
        if option_type.lower() == "call":
            price = max(0, spot_price - strike)
            delta = 1.0 if spot_price > strike else 0.0
        else:
            price = max(0, strike - spot_price)
            delta = -1.0 if strike > spot_price else 0.0

        return {
            "delta": delta,
            "gamma": 0.0,
            "theta": 0.0,
            "vega": 0.0,
            "rho": 0.0,
            "price": round(price, 2)
        }

    def calculate_time_to_expiry(
        self,
        expiry_date: datetime,
        current_date: Optional[datetime] = None
    ) -> float:
        """
        Calculate time to expiry in years (using trading days)

        Args:
            expiry_date: Expiration date
            current_date: Current date (defaults to now)

        Returns:
            Time to expiry in years
        """
        if current_date is None:
            current_date = datetime.now()

        days_to_expiry = (expiry_date - current_date).days

        # Use 252 trading days per year
        return max(days_to_expiry / 252.0, 0.0001)  # Minimum to avoid division by zero


class ImpliedVolatilityCalculator:
    """Calculate implied volatility using Newton-Raphson method"""

    def __init__(self):
        self.greeks_calc = GreeksCalculator()

    def calculate_iv(
        self,
        market_price: float,
        spot_price: float,
        strike: float,
        time_to_expiry: float,
        risk_free_rate: float,
        option_type: str = "call",
        max_iterations: int = 100,
        tolerance: float = 0.0001
    ) -> Optional[float]:
        """
        Calculate implied volatility using Newton-Raphson method

        Args:
            market_price: Current option price
            spot_price: Current stock price
            strike: Strike price
            time_to_expiry: Time to expiration in years
            risk_free_rate: Risk-free rate
            option_type: 'call' or 'put'
            max_iterations: Maximum iterations
            tolerance: Convergence tolerance

        Returns:
            Implied volatility or None if calculation fails
        """
        # Initial guess for volatility
        sigma = 0.3

        for i in range(max_iterations):
            greeks = self.greeks_calc.calculate_greeks(
                spot_price, strike, time_to_expiry,
                risk_free_rate, sigma, option_type
            )

            price_diff = greeks["price"] - market_price
            vega = greeks["vega"] * 100  # Convert back to per 100% change

            # Check convergence
            if abs(price_diff) < tolerance:
                return round(sigma, 4)

            # Avoid division by zero
            if abs(vega) < 1e-10:
                return None

            # Newton-Raphson update
            sigma = sigma - price_diff / vega

            # Keep sigma in reasonable bounds
            sigma = max(0.001, min(sigma, 5.0))

        return None  # Did not converge
