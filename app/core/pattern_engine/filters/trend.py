
"""
Trend Template Filter
Classifies stocks into Trend Tiers (1, 2, 3) based on Minervini/CANSLIM criteria.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any

class TrendTemplateFilter:
    """
    Classifies stock trend quality.
    Tier 1: Strong Leader (Above 50, 150, 200 MA, 200 rising, near highs)
    Tier 2: Emerging (Above 50, 50 rising, maybe no 200 history)
    Tier 3: Weak/Contrarian
    """
    
    def check_tier(self, data: pd.DataFrame) -> str:
        """
        Determine the trend tier.
        Dataframe must have 'close' and sufficient history.
        """
        if len(data) < 50:
            return "TIER_2" # Assume emerging if short history
            
        close = data['close'].iloc[-1]
        
        # Calculate MAs
        ma50 = data['close'].rolling(50).mean().iloc[-1]
        
        # Check Tier 1 conditions
        if len(data) >= 200:
            ma150 = data['close'].rolling(150).mean().iloc[-1]
            ma200 = data['close'].rolling(200).mean().iloc[-1]
            
            # Simple check for Trend Template
            # 1. Price > 150 and > 200
            cond1 = close > ma150 and close > ma200
            # 2. 150 > 200
            cond2 = ma150 > ma200
            # 3. 200 trending up? (Compare to 1 month ago)
            ma200_prev = data['close'].rolling(200).mean().iloc[-22]
            cond3 = ma200 > ma200_prev
            # 4. Price > 50
            cond4 = close > ma50
            # 5. Near 52-week high (within 25%)
            year_high = data['close'].rolling(250, min_periods=1).max().iloc[-1]
            cond5 = close >= year_high * 0.75
            
            if cond1 and cond2 and cond3 and cond4 and cond5:
                return "TIER_1"

        # Tier 2: Above 50, 50 rising
        ma50_prev = data['close'].rolling(50).mean().iloc[-10] # 2 weeks ago
        if close > ma50 and ma50 > ma50_prev:
            return "TIER_2"
            
        return "TIER_3"
