"""
Pre-built Stock Screen Templates

Provides ready-to-use screening templates based on proven strategies:
- Minervini SEPA (Specific Entry Point Analysis)
- O'Neil CAN SLIM
- Momentum Leaders
- Breakout Candidates
- Gap-Up Today
"""
from typing import Dict, Any, List, Optional
from app.services.advanced_screener import FilterCriteria


class ScreenTemplates:
    """Pre-built screening templates"""

    @staticmethod
    def minervini_sepa() -> FilterCriteria:
        """
        Mark Minervini's SEPA (Specific Entry Point Analysis) criteria

        Key criteria:
        - Price > $5 (liquid stocks)
        - Passes Minervini Trend Template
        - RS Rating > 70
        - Price within 0-15% of SMA50
        - SMA50 > SMA200 (uptrend)
        - Above EMA21
        - Consolidation pattern (VCP)
        """
        return FilterCriteria(
            min_price=5.0,
            min_rs_rating=70.0,
            min_pct_above_sma_50=0.0,
            max_pct_above_sma_50=15.0,
            above_sma_50=True,
            above_ema_21=True,
            sma_50_above_sma_200=True,
            minervini_template=True,
            patterns=["VCP"],
            min_pattern_confidence=0.6,
            min_avg_volume=500000,
        )

    @staticmethod
    def canslim() -> FilterCriteria:
        """
        William O'Neil's CAN SLIM criteria

        C = Current quarterly earnings (not screened - requires fundamental data)
        A = Annual earnings growth (not screened - requires fundamental data)
        N = New highs, products, management
        S = Supply and demand (volume)
        L = Leader or laggard (RS Rating)
        I = Institutional sponsorship (not screened)
        M = Market direction

        Focus on L (Leader), S (Supply/Demand), N (New highs)
        """
        return FilterCriteria(
            min_price=10.0,
            min_rs_rating=80.0,  # Leaders only
            min_avg_volume=1000000,  # Good liquidity
            above_sma_50=True,
            above_sma_200=True,
            sma_50_above_sma_200=True,
            min_pct_above_sma_50=-5.0,  # Near or above SMA50
            max_pct_above_sma_50=20.0,
            patterns=["Cup and Handle", "VCP", "Ascending Triangle"],
            min_pattern_confidence=0.6,
        )

    @staticmethod
    def momentum_leaders() -> FilterCriteria:
        """
        High momentum stocks with strong relative strength

        Criteria:
        - Strong RS Rating (> 85)
        - Positive price momentum
        - Above all major moving averages
        - High volume
        """
        return FilterCriteria(
            min_price=10.0,
            min_rs_rating=85.0,
            min_price_change_pct=15.0,  # 15% gain in last 20 days
            price_change_period=20,
            above_sma_50=True,
            above_sma_200=True,
            above_ema_21=True,
            sma_50_above_sma_200=True,
            min_avg_volume=1000000,
        )

    @staticmethod
    def breakout_candidates() -> FilterCriteria:
        """
        Stocks setting up for potential breakouts

        Criteria:
        - In consolidation
        - Strong base (Minervini template)
        - High RS rating
        - Near 52-week high area
        - Volume dry-up during consolidation
        """
        return FilterCriteria(
            min_price=5.0,
            min_rs_rating=75.0,
            minervini_template=True,
            min_pct_above_sma_50=0.0,
            max_pct_above_sma_50=10.0,
            above_sma_50=True,
            sma_50_above_sma_200=True,
            patterns=["VCP", "Cup and Handle", "Ascending Triangle", "Flat Base"],
            min_pattern_confidence=0.65,
            in_consolidation=True,
            max_consolidation_days=60,
        )

    @staticmethod
    def gap_up_today() -> FilterCriteria:
        """
        Stocks that gapped up today with volume

        Criteria:
        - Gap up > 2%
        - Above average volume
        - In uptrend (above SMA50)
        - Decent RS rating
        """
        return FilterCriteria(
            min_price=5.0,
            gap_up_today=True,
            min_gap_pct=2.0,
            min_volume=500000,
            above_sma_50=True,
            min_rs_rating=60.0,
        )

    @staticmethod
    def high_tight_flag() -> FilterCriteria:
        """
        High Tight Flag pattern - O'Neil's strongest pattern

        Criteria:
        - Price doubled in 8 weeks or less (100%+ gain)
        - Tight consolidation (3-5 weeks)
        - Very high RS rating
        - Above all MAs
        """
        return FilterCriteria(
            min_price=10.0,
            min_price_change_pct=50.0,  # At least 50% gain
            price_change_period=40,  # Over ~8 weeks
            min_rs_rating=90.0,
            above_sma_50=True,
            above_sma_200=True,
            sma_50_above_sma_200=True,
            min_avg_volume=500000,
            in_consolidation=True,
            max_consolidation_days=25,  # ~5 weeks
        )

    @staticmethod
    def pullback_to_support() -> FilterCriteria:
        """
        Stocks pulling back to key support (SMA50)

        Criteria:
        - Near SMA50 (within 5%)
        - Strong uptrend (SMA50 > SMA200)
        - High RS rating
        - Looking for bounce opportunity
        """
        return FilterCriteria(
            min_price=5.0,
            min_pct_above_sma_50=-5.0,  # Can be slightly below
            max_pct_above_sma_50=2.0,   # But not far above
            sma_50_above_sma_200=True,
            min_rs_rating=70.0,
            min_avg_volume=500000,
        )

    @staticmethod
    def pocket_pivot() -> FilterCriteria:
        """
        Pocket Pivot setup - volume spike on up day

        Criteria:
        - High RS rating
        - Above SMA50
        - Volume significantly above average
        - Positive day
        """
        return FilterCriteria(
            min_price=5.0,
            min_rs_rating=75.0,
            above_sma_50=True,
            above_ema_21=True,
            min_volume=1000000,
            min_price_change_pct=1.0,  # Positive day
            price_change_period=1,
        )

    @staticmethod
    def strong_foundation() -> FilterCriteria:
        """
        Stocks with strong technical foundation

        Criteria:
        - All MAs aligned (EMA21 > SMA50 > SMA200)
        - High RS rating
        - Good volume
        - Positive momentum
        """
        return FilterCriteria(
            min_price=5.0,
            above_ema_21=True,
            above_sma_50=True,
            above_sma_200=True,
            sma_50_above_sma_200=True,
            min_rs_rating=70.0,
            min_avg_volume=500000,
            min_price_change_pct=0.0,  # Positive or flat
        )

    @staticmethod
    def post_ipo_base() -> FilterCriteria:
        """
        Recent IPOs building first base

        Criteria:
        - Strong RS rating
        - Building base above SMA50
        - Good volume
        """
        return FilterCriteria(
            min_price=15.0,
            min_rs_rating=80.0,
            above_sma_50=True,
            min_pct_above_sma_50=0.0,
            max_pct_above_sma_50=15.0,
            patterns=["VCP", "Cup and Handle"],
            min_pattern_confidence=0.6,
            min_avg_volume=1000000,
        )

    @staticmethod
    def get_all_templates() -> Dict[str, Dict[str, Any]]:
        """Get all available templates with metadata"""
        return {
            "MINERVINI_SEPA": {
                "name": "Minervini SEPA",
                "description": "Mark Minervini's Specific Entry Point Analysis",
                "category": "Growth",
                "difficulty": "Advanced",
                "criteria": ScreenTemplates.minervini_sepa(),
            },
            "CANSLIM": {
                "name": "O'Neil CAN SLIM",
                "description": "William O'Neil's CAN SLIM methodology",
                "category": "Growth",
                "difficulty": "Intermediate",
                "criteria": ScreenTemplates.canslim(),
            },
            "MOMENTUM_LEADERS": {
                "name": "Momentum Leaders",
                "description": "High momentum stocks with strong relative strength",
                "category": "Momentum",
                "difficulty": "Beginner",
                "criteria": ScreenTemplates.momentum_leaders(),
            },
            "BREAKOUT_CANDIDATES": {
                "name": "Breakout Candidates",
                "description": "Stocks setting up for potential breakouts",
                "category": "Breakout",
                "difficulty": "Intermediate",
                "criteria": ScreenTemplates.breakout_candidates(),
            },
            "GAP_UP_TODAY": {
                "name": "Gap-Up Today",
                "description": "Stocks that gapped up today with volume",
                "category": "Momentum",
                "difficulty": "Beginner",
                "criteria": ScreenTemplates.gap_up_today(),
            },
            "HIGH_TIGHT_FLAG": {
                "name": "High Tight Flag",
                "description": "O'Neil's strongest pattern - extreme momentum",
                "category": "Breakout",
                "difficulty": "Advanced",
                "criteria": ScreenTemplates.high_tight_flag(),
            },
            "PULLBACK_TO_SUPPORT": {
                "name": "Pullback to Support",
                "description": "Quality pullbacks to SMA50 support",
                "category": "Pullback",
                "difficulty": "Intermediate",
                "criteria": ScreenTemplates.pullback_to_support(),
            },
            "POCKET_PIVOT": {
                "name": "Pocket Pivot",
                "description": "Volume spike on up day - Gil Morales",
                "category": "Momentum",
                "difficulty": "Advanced",
                "criteria": ScreenTemplates.pocket_pivot(),
            },
            "STRONG_FOUNDATION": {
                "name": "Strong Foundation",
                "description": "Stocks with aligned moving averages and strength",
                "category": "Quality",
                "difficulty": "Beginner",
                "criteria": ScreenTemplates.strong_foundation(),
            },
            "POST_IPO_BASE": {
                "name": "Post-IPO Base",
                "description": "Recent IPOs building first major base",
                "category": "Growth",
                "difficulty": "Advanced",
                "criteria": ScreenTemplates.post_ipo_base(),
            },
        }

    @staticmethod
    def get_template(template_type: str) -> Optional[FilterCriteria]:
        """Get a specific template by type"""
        templates = ScreenTemplates.get_all_templates()
        template = templates.get(template_type.upper())
        return template["criteria"] if template else None


# Global instance
screen_templates = ScreenTemplates()
