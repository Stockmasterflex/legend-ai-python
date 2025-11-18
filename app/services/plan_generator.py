"""
AI-Powered Trade Plan Generator
Integrates pattern detection, risk management, and AI analysis
to create comprehensive multi-scenario trade plans
"""
import logging
import json
from typing import Optional, Dict, Any, List
from datetime import datetime
from dataclasses import dataclass

from app.services.market_data import market_data_service
from app.services.risk_calculator import get_risk_calculator
from app.core.pattern_detector import PatternDetector
from app.ai.assistant import AIFinancialAssistant

logger = logging.getLogger(__name__)


@dataclass
class ScenarioAnalysis:
    """Multi-scenario price target analysis"""
    best_case_target: float
    best_case_rr: float
    base_case_target: float
    base_case_rr: float
    worst_case_target: Optional[float]
    worst_case_rr: Optional[float]
    probability_estimates: Dict[str, float]  # {'best': 0.2, 'base': 0.6, 'worst': 0.2}


@dataclass
class EntryZone:
    """Entry zone with optimal entry point"""
    low: float
    high: float
    optimal: float
    reasoning: str


@dataclass
class StopLevels:
    """Stop loss levels and invalidation"""
    initial_stop: float
    trailing_stop: Optional[float]
    invalidation_price: float
    reasoning: str


@dataclass
class TradePlanData:
    """Complete trade plan data structure"""
    # Ticker info
    ticker: str
    current_price: float

    # Pattern analysis
    pattern_type: str
    pattern_score: float
    pattern_analysis: str

    # Entry/Stop/Target
    entry_zone: EntryZone
    stop_levels: StopLevels
    scenario_analysis: ScenarioAnalysis

    # Position sizing
    position_size: int
    position_value: float
    risk_amount: float

    # AI Analysis
    ai_notes: str
    checklist: List[str]
    risk_factors: List[str]

    # Chart
    chart_url: Optional[str] = None


class PlanGenerator:
    """AI-powered trade plan generator"""

    def __init__(self):
        self.pattern_detector = PatternDetector()
        self.risk_calculator = get_risk_calculator()
        self.ai_assistant = None  # Will initialize when needed

    async def generate_plan(
        self,
        ticker: str,
        account_size: float = 10000.0,
        risk_percentage: float = 2.0,
        timeframe: str = "1day",
        strategy: str = "swing",
        user_notes: Optional[str] = None
    ) -> TradePlanData:
        """
        Generate comprehensive AI-powered trade plan

        Args:
            ticker: Stock symbol
            account_size: Trading account size
            risk_percentage: Risk per trade (default 2%)
            timeframe: Chart timeframe (1day, 1week, etc)
            strategy: Trading strategy (swing, position, momentum)
            user_notes: Optional user notes for context

        Returns:
            TradePlanData with complete analysis
        """
        logger.info(f"📊 Generating AI trade plan for {ticker}")

        # 1. Fetch market data
        price_data = await market_data_service.get_time_series(
            ticker=ticker,
            interval=timeframe,
            outputsize=500
        )

        if not price_data:
            raise ValueError(f"Unable to fetch price data for {ticker}")

        # 2. Get SPY data for market context
        spy_data = await market_data_service.get_time_series(
            ticker="SPY",
            interval=timeframe,
            outputsize=500
        )

        # 3. Detect pattern
        pattern_result = await self.pattern_detector.analyze_ticker(
            ticker, price_data, spy_data
        )

        if not pattern_result:
            raise ValueError(f"No pattern detected for {ticker}")

        current_price = pattern_result.current_price

        # 4. Calculate entry zones
        entry_zone = self._calculate_entry_zone(
            pattern_result, current_price, price_data
        )

        # 5. Calculate stop levels
        stop_levels = self._calculate_stop_levels(
            pattern_result, current_price, price_data, entry_zone
        )

        # 6. Calculate multi-scenario targets
        scenario_analysis = self._calculate_scenarios(
            pattern_result, current_price, entry_zone, stop_levels
        )

        # 7. Calculate position sizing
        position_calc = self.risk_calculator.calculate_position_size(
            account_size=account_size,
            entry_price=entry_zone.optimal,
            stop_loss_price=stop_levels.initial_stop,
            target_price=scenario_analysis.base_case_target,
            risk_percentage=risk_percentage / 100
        )

        # 8. Generate AI analysis
        ai_notes = await self._generate_ai_analysis(
            ticker, pattern_result, entry_zone, stop_levels,
            scenario_analysis, user_notes
        )

        # 9. Generate checklist
        checklist = self._generate_checklist(pattern_result, strategy)

        # 10. Identify risk factors
        risk_factors = self._identify_risk_factors(
            pattern_result, scenario_analysis, position_calc
        )

        # 11. Get chart URL
        chart_url = await self._get_chart_url(ticker, timeframe)

        return TradePlanData(
            ticker=ticker,
            current_price=current_price,
            pattern_type=pattern_result.pattern,
            pattern_score=pattern_result.score,
            pattern_analysis=pattern_result.analysis,
            entry_zone=entry_zone,
            stop_levels=stop_levels,
            scenario_analysis=scenario_analysis,
            position_size=position_calc.position_size,
            position_value=position_calc.position_size_dollars,
            risk_amount=position_calc.risk_per_trade,
            ai_notes=ai_notes,
            checklist=checklist,
            risk_factors=risk_factors,
            chart_url=chart_url
        )

    def _calculate_entry_zone(
        self,
        pattern_result,
        current_price: float,
        price_data: List[Dict]
    ) -> EntryZone:
        """Calculate optimal entry zone based on pattern"""

        # Base entry from pattern detection
        pattern_entry = pattern_result.entry

        # Calculate entry zone (2-3% range around pattern entry)
        zone_range = pattern_entry * 0.025  # 2.5% range

        entry_low = pattern_entry - (zone_range / 2)
        entry_high = pattern_entry + (zone_range / 2)

        # Optimal entry is at the lower end of the zone for better R:R
        optimal = entry_low + (zone_range * 0.3)

        # Adjust based on current price position
        if current_price < entry_low:
            reasoning = f"Price ${current_price:.2f} is below entry zone. Wait for breakout confirmation."
        elif current_price > entry_high:
            reasoning = f"Price ${current_price:.2f} is above entry zone. Pattern may have triggered."
        else:
            reasoning = f"Price ${current_price:.2f} is within entry zone. Consider staged entry."

        return EntryZone(
            low=entry_low,
            high=entry_high,
            optimal=optimal,
            reasoning=reasoning
        )

    def _calculate_stop_levels(
        self,
        pattern_result,
        current_price: float,
        price_data: List[Dict],
        entry_zone: EntryZone
    ) -> StopLevels:
        """Calculate stop loss and invalidation levels"""

        # Initial stop from pattern
        initial_stop = pattern_result.stop

        # Calculate invalidation price (pattern breakdown level)
        # Typically 3-5% below the stop
        invalidation_price = initial_stop * 0.97

        # Trailing stop (20% above initial stop as price rises)
        trailing_stop = None
        if current_price > entry_zone.optimal * 1.05:
            trailing_stop = current_price * 0.98  # 2% trailing stop

        reasoning = (
            f"Initial stop at ${initial_stop:.2f} protects pattern structure. "
            f"Pattern invalidates below ${invalidation_price:.2f}."
        )

        return StopLevels(
            initial_stop=initial_stop,
            trailing_stop=trailing_stop,
            invalidation_price=invalidation_price,
            reasoning=reasoning
        )

    def _calculate_scenarios(
        self,
        pattern_result,
        current_price: float,
        entry_zone: EntryZone,
        stop_levels: StopLevels
    ) -> ScenarioAnalysis:
        """Calculate best/base/worst case scenarios"""

        # Risk distance
        risk_distance = abs(entry_zone.optimal - stop_levels.initial_stop)

        # Base case: Pattern target from detector
        base_case_target = pattern_result.target
        base_reward = abs(base_case_target - entry_zone.optimal)
        base_case_rr = base_reward / risk_distance if risk_distance > 0 else 0

        # Best case: 1.5x the base case target
        best_case_target = entry_zone.optimal + (base_reward * 1.5)
        best_reward = abs(best_case_target - entry_zone.optimal)
        best_case_rr = best_reward / risk_distance if risk_distance > 0 else 0

        # Worst case: Partial profit before reversal (0.5x base target)
        worst_case_target = entry_zone.optimal + (base_reward * 0.5)
        worst_reward = abs(worst_case_target - entry_zone.optimal)
        worst_case_rr = worst_reward / risk_distance if risk_distance > 0 else 0

        # Probability estimates based on pattern score
        score = pattern_result.score
        if score >= 8.5:
            probs = {'best': 0.3, 'base': 0.5, 'worst': 0.2}
        elif score >= 7.0:
            probs = {'best': 0.2, 'base': 0.6, 'worst': 0.2}
        else:
            probs = {'best': 0.15, 'base': 0.5, 'worst': 0.35}

        return ScenarioAnalysis(
            best_case_target=best_case_target,
            best_case_rr=best_case_rr,
            base_case_target=base_case_target,
            base_case_rr=base_case_rr,
            worst_case_target=worst_case_target,
            worst_case_rr=worst_case_rr,
            probability_estimates=probs
        )

    async def _generate_ai_analysis(
        self,
        ticker: str,
        pattern_result,
        entry_zone: EntryZone,
        stop_levels: StopLevels,
        scenario_analysis: ScenarioAnalysis,
        user_notes: Optional[str]
    ) -> str:
        """Generate AI-powered trade analysis"""

        try:
            # Initialize AI assistant if needed
            if self.ai_assistant is None:
                self.ai_assistant = AIFinancialAssistant()

            # Build context for AI
            context = f"""
Generate a professional trade plan analysis for {ticker}:

Pattern Detected: {pattern_result.pattern} (Score: {pattern_result.score}/10)
Current Price: ${pattern_result.current_price:.2f}
Entry Zone: ${entry_zone.low:.2f} - ${entry_zone.high:.2f} (Optimal: ${entry_zone.optimal:.2f})
Stop Loss: ${stop_levels.initial_stop:.2f}
Targets:
- Best Case: ${scenario_analysis.best_case_target:.2f} ({scenario_analysis.best_case_rr:.2f}R)
- Base Case: ${scenario_analysis.base_case_target:.2f} ({scenario_analysis.base_case_rr:.2f}R)
- Worst Case: ${scenario_analysis.worst_case_target:.2f} ({scenario_analysis.worst_case_rr:.2f}R)

Pattern Analysis: {pattern_result.analysis}

{f'User Notes: {user_notes}' if user_notes else ''}

Provide a concise analysis covering:
1. Pattern strength and key levels
2. Entry timing and execution strategy
3. Risk management approach
4. Exit strategy for each scenario
5. Key factors to monitor

Keep it professional and actionable (max 300 words).
"""

            # Get AI analysis
            response = await self.ai_assistant.chat(
                message=context,
                user_id="system"
            )

            return response.get("response", "AI analysis unavailable")

        except Exception as e:
            logger.warning(f"AI analysis failed: {e}")
            return f"""
**Pattern Analysis**
{pattern_result.pattern} detected with {pattern_result.score}/10 confidence.

**Entry Strategy**
Enter in stages between ${entry_zone.low:.2f} and ${entry_zone.high:.2f},
with optimal entry at ${entry_zone.optimal:.2f}.

**Risk Management**
Stop loss: ${stop_levels.initial_stop:.2f}
Risk: ${abs(entry_zone.optimal - stop_levels.initial_stop):.2f} per share

**Targets**
- Base target: ${scenario_analysis.base_case_target:.2f} ({scenario_analysis.base_case_rr:.1f}R)
- Best case: ${scenario_analysis.best_case_target:.2f} ({scenario_analysis.best_case_rr:.1f}R)
"""

    def _generate_checklist(
        self,
        pattern_result,
        strategy: str
    ) -> List[str]:
        """Generate pre-trade checklist"""

        checklist = [
            "✓ Verify pattern is still valid (not broken)",
            "✓ Check market trend (SPY/QQQ direction)",
            "✓ Confirm volume profile supports pattern",
            "✓ Review recent news/earnings calendar",
            "✓ Verify entry zone alignment with current price",
            "✓ Set stop loss order immediately after entry",
            "✓ Calculate exact position size before entry",
            "✓ Review risk/reward ratio is favorable (>1.5R)",
        ]

        # Add strategy-specific items
        if strategy == "swing":
            checklist.extend([
                "✓ Check for upcoming catalysts (earnings, FDA, etc)",
                "✓ Verify sufficient liquidity for position size"
            ])
        elif strategy == "momentum":
            checklist.extend([
                "✓ Confirm strong relative strength vs market",
                "✓ Check for increasing volume on up days"
            ])

        return checklist

    def _identify_risk_factors(
        self,
        pattern_result,
        scenario_analysis: ScenarioAnalysis,
        position_calc
    ) -> List[str]:
        """Identify key risk factors for the trade"""

        risk_factors = []

        # Pattern score risks
        if pattern_result.score < 7.0:
            risk_factors.append("⚠️ Pattern confidence below 7/10 - higher risk setup")

        # Risk/reward risks
        if scenario_analysis.base_case_rr < 1.5:
            risk_factors.append("⚠️ Base case R:R below 1.5:1 - unfavorable risk/reward")

        # Position size risks
        if position_calc.notes:
            for note in position_calc.notes:
                if "⚠️" in note:
                    risk_factors.append(note)

        # Market condition risks (could enhance with market analysis)
        risk_factors.append("⚠️ Monitor market conditions - trade may fail in weak market")

        return risk_factors

    async def _get_chart_url(self, ticker: str, timeframe: str) -> Optional[str]:
        """Get chart URL for the ticker"""
        try:
            from app.services.chart import get_chart_service
            chart_service = get_chart_service()
            chart_url = await chart_service.get_chart_url(
                ticker=ticker,
                interval=timeframe,
                indicators=["sma20", "sma50", "volume"]
            )
            return chart_url
        except Exception as e:
            logger.warning(f"Failed to get chart URL: {e}")
            return None


# Global instance
_plan_generator: Optional[PlanGenerator] = None


def get_plan_generator() -> PlanGenerator:
    """Get or create plan generator singleton"""
    global _plan_generator
    if _plan_generator is None:
        _plan_generator = PlanGenerator()
    return _plan_generator
