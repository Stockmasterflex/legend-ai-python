"""
Volatility Surface Analysis
Analyzes implied volatility across strikes and expirations
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from scipy.interpolate import griddata
from .greeks_calculator import ImpliedVolatilityCalculator


class VolatilitySurfaceAnalyzer:
    """Analyze and visualize volatility surface"""

    def __init__(self):
        self.iv_calc = ImpliedVolatilityCalculator()

    def calculate_iv_surface(
        self,
        options_data: List[Dict],
        spot_price: float,
        risk_free_rate: float = 0.05
    ) -> pd.DataFrame:
        """
        Calculate IV surface from options chain data

        Args:
            options_data: List of option contracts with price, strike, expiry, type
            spot_price: Current stock price
            risk_free_rate: Risk-free rate

        Returns:
            DataFrame with strike, expiry, moneyness, IV, option_type
        """
        surface_data = []

        for option in options_data:
            strike = option.get("strike")
            expiry = option.get("expiry")
            option_type = option.get("type", "call")
            market_price = option.get("price", 0)
            time_to_expiry = option.get("time_to_expiry", 0)

            if not all([strike, expiry, market_price > 0, time_to_expiry > 0]):
                continue

            # Calculate IV
            iv = self.iv_calc.calculate_iv(
                market_price=market_price,
                spot_price=spot_price,
                strike=strike,
                time_to_expiry=time_to_expiry,
                risk_free_rate=risk_free_rate,
                option_type=option_type
            )

            if iv is not None:
                moneyness = spot_price / strike

                surface_data.append({
                    "strike": strike,
                    "expiry": expiry,
                    "time_to_expiry": time_to_expiry,
                    "moneyness": round(moneyness, 4),
                    "iv": iv,
                    "option_type": option_type,
                    "market_price": market_price
                })

        return pd.DataFrame(surface_data)

    def calculate_volatility_skew(
        self,
        options_data: List[Dict],
        spot_price: float,
        expiry_filter: Optional[str] = None
    ) -> Dict[str, List]:
        """
        Calculate volatility skew (IV vs strike)

        Args:
            options_data: Options chain data
            spot_price: Current stock price
            expiry_filter: Filter to specific expiration date

        Returns:
            Dict with strikes and corresponding IVs for calls and puts
        """
        df = self.calculate_iv_surface(options_data, spot_price)

        if df.empty:
            return {"strikes": [], "call_ivs": [], "put_ivs": []}

        if expiry_filter:
            df = df[df["expiry"] == expiry_filter]

        # Separate calls and puts
        calls = df[df["option_type"] == "call"].sort_values("strike")
        puts = df[df["option_type"] == "put"].sort_values("strike")

        # Merge on strike
        merged = pd.merge(
            calls[["strike", "iv"]],
            puts[["strike", "iv"]],
            on="strike",
            how="outer",
            suffixes=("_call", "_put")
        ).sort_values("strike")

        return {
            "strikes": merged["strike"].tolist(),
            "call_ivs": merged["iv_call"].fillna(0).tolist(),
            "put_ivs": merged["iv_put"].fillna(0).tolist(),
            "atm_strike": self._find_atm_strike(merged["strike"].tolist(), spot_price)
        }

    def calculate_term_structure(
        self,
        options_data: List[Dict],
        spot_price: float,
        strike_filter: Optional[float] = None
    ) -> Dict[str, List]:
        """
        Calculate volatility term structure (IV vs time to expiry)

        Args:
            options_data: Options chain data
            spot_price: Current stock price
            strike_filter: Filter to specific strike (default: ATM)

        Returns:
            Dict with expiries and corresponding IVs
        """
        df = self.calculate_iv_surface(options_data, spot_price)

        if df.empty:
            return {"expiries": [], "days_to_expiry": [], "ivs": []}

        # Filter to ATM options if no strike specified
        if strike_filter is None:
            df = df[abs(df["moneyness"] - 1.0) < 0.05]  # Within 5% of ATM
        else:
            df = df[abs(df["strike"] - strike_filter) < 0.01]

        # Group by expiry and average IV
        term_structure = df.groupby(["expiry", "time_to_expiry"])["iv"].mean().reset_index()
        term_structure = term_structure.sort_values("time_to_expiry")

        return {
            "expiries": term_structure["expiry"].tolist(),
            "days_to_expiry": (term_structure["time_to_expiry"] * 252).round().astype(int).tolist(),
            "ivs": term_structure["iv"].round(4).tolist()
        }

    def detect_iv_crush_risk(
        self,
        current_iv: float,
        historical_iv: List[float],
        earnings_date: Optional[datetime] = None,
        current_date: Optional[datetime] = None
    ) -> Dict[str, any]:
        """
        Detect IV crush risk (especially around earnings)

        Args:
            current_iv: Current implied volatility
            historical_iv: Historical IV values
            earnings_date: Next earnings date
            current_date: Current date

        Returns:
            Dict with IV percentile, crush risk level, and metrics
        """
        if not historical_iv:
            return {
                "iv_percentile": None,
                "crush_risk": "unknown",
                "current_iv": current_iv
            }

        # Calculate IV percentile
        iv_percentile = self._calculate_percentile(current_iv, historical_iv)

        # Calculate average IV and standard deviation
        avg_iv = np.mean(historical_iv)
        std_iv = np.std(historical_iv)

        # Determine crush risk
        crush_risk = "low"
        if iv_percentile > 80:
            crush_risk = "high"
        elif iv_percentile > 60:
            crush_risk = "medium"

        # Check if earnings is approaching
        days_to_earnings = None
        if earnings_date and current_date:
            days_to_earnings = (earnings_date - current_date).days
            if days_to_earnings <= 7 and iv_percentile > 60:
                crush_risk = "high"

        return {
            "current_iv": round(current_iv, 4),
            "iv_percentile": round(iv_percentile, 1),
            "avg_historical_iv": round(avg_iv, 4),
            "iv_std_dev": round(std_iv, 4),
            "crush_risk": crush_risk,
            "days_to_earnings": days_to_earnings,
            "iv_rank": round((current_iv - min(historical_iv)) / (max(historical_iv) - min(historical_iv)) * 100, 1) if len(historical_iv) > 1 else None
        }

    def interpolate_surface(
        self,
        surface_df: pd.DataFrame,
        grid_size: int = 50
    ) -> Dict[str, np.ndarray]:
        """
        Interpolate volatility surface for smooth visualization

        Args:
            surface_df: DataFrame from calculate_iv_surface
            grid_size: Grid resolution

        Returns:
            Dict with grid coordinates and interpolated IV values
        """
        if surface_df.empty:
            return {
                "moneyness_grid": np.array([]),
                "time_grid": np.array([]),
                "iv_grid": np.array([])
            }

        # Create grid
        moneyness_range = np.linspace(
            surface_df["moneyness"].min(),
            surface_df["moneyness"].max(),
            grid_size
        )
        time_range = np.linspace(
            surface_df["time_to_expiry"].min(),
            surface_df["time_to_expiry"].max(),
            grid_size
        )

        moneyness_grid, time_grid = np.meshgrid(moneyness_range, time_range)

        # Interpolate IV values
        points = surface_df[["moneyness", "time_to_expiry"]].values
        values = surface_df["iv"].values

        iv_grid = griddata(
            points,
            values,
            (moneyness_grid, time_grid),
            method="cubic",
            fill_value=np.nan
        )

        return {
            "moneyness_grid": moneyness_grid.tolist(),
            "time_grid": time_grid.tolist(),
            "iv_grid": iv_grid.tolist()
        }

    @staticmethod
    def _calculate_percentile(value: float, data: List[float]) -> float:
        """Calculate percentile of value in data"""
        return (sum(1 for x in data if x <= value) / len(data)) * 100

    @staticmethod
    def _find_atm_strike(strikes: List[float], spot_price: float) -> float:
        """Find the strike closest to ATM"""
        return min(strikes, key=lambda x: abs(x - spot_price))
