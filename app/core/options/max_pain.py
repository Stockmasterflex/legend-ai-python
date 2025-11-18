"""
Max Pain Calculator
Calculates the strike price where option holders lose the most money
"""
from typing import Dict, List, Tuple
import pandas as pd


class MaxPainCalculator:
    """Calculate max pain and analyze open interest"""

    def calculate_max_pain(
        self,
        options_chain: List[Dict]
    ) -> Dict[str, any]:
        """
        Calculate max pain strike (where most options expire worthless)

        Args:
            options_chain: List of options with strike, type, open_interest, price

        Returns:
            Dict with max_pain_strike, total_pain, and breakdown by strike
        """
        if not options_chain:
            return {
                "max_pain_strike": None,
                "total_pain": 0,
                "pain_by_strike": []
            }

        # Group by strike
        df = pd.DataFrame(options_chain)

        # Get unique strikes
        strikes = sorted(df["strike"].unique())

        pain_by_strike = []

        for test_strike in strikes:
            # Calculate total pain if stock closes at this strike
            call_pain = 0
            put_pain = 0

            for _, option in df.iterrows():
                strike = option["strike"]
                oi = option.get("open_interest", 0)
                option_type = option.get("type", "call")

                if option_type == "call" and test_strike > strike:
                    # Calls are ITM - option writers pay out
                    call_pain += (test_strike - strike) * oi * 100
                elif option_type == "put" and test_strike < strike:
                    # Puts are ITM - option writers pay out
                    put_pain += (strike - test_strike) * oi * 100

            total_pain = call_pain + put_pain

            pain_by_strike.append({
                "strike": strike,
                "total_pain": round(total_pain, 2),
                "call_pain": round(call_pain, 2),
                "put_pain": round(put_pain, 2)
            })

        # Find strike with minimum pain (max pain for option holders)
        if pain_by_strike:
            max_pain_entry = min(pain_by_strike, key=lambda x: x["total_pain"])
            max_pain_strike = max_pain_entry["strike"]
            max_pain_value = max_pain_entry["total_pain"]
        else:
            max_pain_strike = None
            max_pain_value = 0

        return {
            "max_pain_strike": max_pain_strike,
            "total_pain": max_pain_value,
            "pain_by_strike": pain_by_strike
        }

    def analyze_open_interest(
        self,
        options_chain: List[Dict],
        spot_price: float
    ) -> Dict[str, any]:
        """
        Analyze open interest distribution

        Args:
            options_chain: List of options with strike, type, open_interest
            spot_price: Current stock price

        Returns:
            Dict with OI analysis including put/call ratio, concentrations
        """
        if not options_chain:
            return {
                "total_call_oi": 0,
                "total_put_oi": 0,
                "put_call_ratio": 0,
                "oi_concentrations": []
            }

        df = pd.DataFrame(options_chain)

        # Calculate totals
        call_oi = df[df["type"] == "call"]["open_interest"].sum()
        put_oi = df[df["type"] == "put"]["open_interest"].sum()

        put_call_ratio = put_oi / call_oi if call_oi > 0 else 0

        # Find OI concentrations (strikes with high OI)
        oi_by_strike = df.groupby("strike").agg({
            "open_interest": "sum"
        }).reset_index()
        oi_by_strike = oi_by_strike.sort_values("open_interest", ascending=False)

        # Get top 5 strikes by OI
        concentrations = []
        for _, row in oi_by_strike.head(5).iterrows():
            strike = row["strike"]
            total_oi = row["open_interest"]

            # Get call and put OI at this strike
            strike_calls = df[(df["strike"] == strike) & (df["type"] == "call")]
            strike_puts = df[(df["strike"] == strike) & (df["type"] == "put")]

            call_oi_strike = strike_calls["open_interest"].sum() if not strike_calls.empty else 0
            put_oi_strike = strike_puts["open_interest"].sum() if not strike_puts.empty else 0

            concentrations.append({
                "strike": strike,
                "total_oi": int(total_oi),
                "call_oi": int(call_oi_strike),
                "put_oi": int(put_oi_strike),
                "distance_from_spot": round((strike - spot_price) / spot_price * 100, 2)
            })

        return {
            "total_call_oi": int(call_oi),
            "total_put_oi": int(put_oi),
            "put_call_ratio": round(put_call_ratio, 2),
            "oi_concentrations": concentrations,
            "total_oi": int(call_oi + put_oi)
        }

    def detect_unusual_activity(
        self,
        options_chain: List[Dict],
        volume_threshold: float = 2.0
    ) -> List[Dict]:
        """
        Detect unusual options activity (high volume relative to OI)

        Args:
            options_chain: List of options with volume, open_interest
            volume_threshold: Volume/OI ratio threshold for unusual activity

        Returns:
            List of options with unusual activity
        """
        unusual_contracts = []

        for option in options_chain:
            volume = option.get("volume", 0)
            oi = option.get("open_interest", 1)  # Avoid division by zero

            if volume == 0:
                continue

            volume_oi_ratio = volume / oi if oi > 0 else float('inf')

            # Flag if volume is unusually high
            if volume_oi_ratio >= volume_threshold or (volume > 1000 and oi < 100):
                unusual_contracts.append({
                    "strike": option["strike"],
                    "expiry": option.get("expiry"),
                    "type": option["type"],
                    "volume": volume,
                    "open_interest": oi,
                    "volume_oi_ratio": round(volume_oi_ratio, 2),
                    "price": option.get("price", 0),
                    "implied_premium": round(volume * option.get("price", 0) * 100, 2)
                })

        # Sort by volume
        unusual_contracts.sort(key=lambda x: x["volume"], reverse=True)

        return unusual_contracts[:20]  # Return top 20

    def calculate_gamma_exposure(
        self,
        options_chain: List[Dict],
        spot_price: float
    ) -> Dict[str, any]:
        """
        Calculate dealer gamma exposure (GEX)

        Args:
            options_chain: List of options with strike, type, OI, gamma
            spot_price: Current stock price

        Returns:
            Dict with gamma exposure by strike and total GEX
        """
        gamma_by_strike = {}
        total_gex = 0

        for option in options_chain:
            strike = option["strike"]
            oi = option.get("open_interest", 0)
            gamma = option.get("gamma", 0)
            option_type = option["type"]

            # Dealer gamma exposure (dealers are short options)
            # Positive GEX = dealers buy when price rises (resistance)
            # Negative GEX = dealers sell when price rises (support)
            if option_type == "call":
                gex = -gamma * oi * 100 * spot_price * spot_price / 100
            else:  # put
                gex = gamma * oi * 100 * spot_price * spot_price / 100

            if strike not in gamma_by_strike:
                gamma_by_strike[strike] = 0

            gamma_by_strike[strike] += gex
            total_gex += gex

        # Convert to list and sort
        gex_data = [
            {"strike": strike, "gex": round(gex, 2)}
            for strike, gex in gamma_by_strike.items()
        ]
        gex_data.sort(key=lambda x: x["strike"])

        # Find zero gamma level
        zero_gamma = self._find_zero_gamma(gex_data)

        return {
            "total_gex": round(total_gex, 2),
            "gex_by_strike": gex_data,
            "zero_gamma_level": zero_gamma,
            "spot_price": spot_price
        }

    @staticmethod
    def _find_zero_gamma(gex_data: List[Dict]) -> float:
        """Find the strike where gamma flips from positive to negative"""
        if not gex_data:
            return None

        for i in range(len(gex_data) - 1):
            current_gex = gex_data[i]["gex"]
            next_gex = gex_data[i + 1]["gex"]

            if current_gex > 0 and next_gex < 0:
                return gex_data[i]["strike"]
            elif current_gex < 0 and next_gex > 0:
                return gex_data[i + 1]["strike"]

        return None
