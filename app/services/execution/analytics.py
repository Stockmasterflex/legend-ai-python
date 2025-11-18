"""
Execution Analytics
Measures slippage, fill quality, cost analysis, and provides improvement suggestions
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import statistics

logger = logging.getLogger(__name__)


@dataclass
class Fill:
    """Represents a single fill"""
    fill_id: str
    timestamp: datetime
    quantity: int
    price: float
    venue_id: Optional[int] = None
    venue_name: Optional[str] = None
    commission: float = 0.0


@dataclass
class ExecutionReport:
    """Comprehensive execution quality report"""
    order_id: str
    ticker: str
    side: str
    total_quantity: int
    filled_quantity: int
    avg_fill_price: float

    # Benchmark prices
    arrival_price: Optional[float]
    vwap_benchmark: Optional[float]
    twap_benchmark: Optional[float]
    close_price: Optional[float]

    # Slippage metrics (in basis points)
    slippage_vs_arrival: Optional[float]
    slippage_vs_vwap: Optional[float]
    slippage_vs_twap: Optional[float]
    slippage_vs_close: Optional[float]

    # Cost metrics
    total_commission: float
    total_cost: float  # Commission + slippage
    cost_per_share: float

    # Performance metrics
    fill_rate: float  # % of order filled
    execution_time_seconds: float
    price_improvement: float  # If positive, we did better than expected

    # Market impact
    participation_rate: Optional[float]  # % of market volume
    market_impact_bps: Optional[float]

    # Venue breakdown
    venue_fills: Dict[str, int]  # venue_name -> quantity
    dark_pool_fills: int
    dark_pool_fill_rate: float

    # Quality score
    overall_quality_score: float  # 0-100
    quality_grade: str  # A+, A, B, C, D, F

    # Suggestions
    improvement_suggestions: List[str]


class ExecutionAnalyzer:
    """
    Analyzes execution quality and provides insights
    """

    def __init__(self):
        self.fills_cache: Dict[str, List[Fill]] = {}

    def analyze_execution(
        self,
        order_id: str,
        ticker: str,
        side: str,
        total_quantity: int,
        fills: List[Fill],
        arrival_price: Optional[float] = None,
        vwap_benchmark: Optional[float] = None,
        twap_benchmark: Optional[float] = None,
        close_price: Optional[float] = None,
        market_volume: Optional[int] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> ExecutionReport:
        """
        Analyze execution quality and generate comprehensive report

        Args:
            order_id: Order identifier
            ticker: Stock ticker
            side: "buy" or "sell"
            total_quantity: Total order quantity
            fills: List of fills
            arrival_price: Price when order was received
            vwap_benchmark: Market VWAP during execution
            twap_benchmark: Market TWAP during execution
            close_price: Closing price (for end-of-day analysis)
            market_volume: Total market volume during execution period
            start_time: Execution start time
            end_time: Execution end time

        Returns:
            ExecutionReport with detailed analysis
        """

        # Calculate basic metrics
        filled_quantity = sum(f.quantity for f in fills)
        fill_rate = (filled_quantity / total_quantity * 100) if total_quantity > 0 else 0

        # Calculate average fill price (quantity-weighted)
        total_value = sum(f.quantity * f.price for f in fills)
        avg_fill_price = total_value / filled_quantity if filled_quantity > 0 else 0

        # Calculate execution time
        if start_time and end_time:
            execution_time_seconds = (end_time - start_time).total_seconds()
        else:
            execution_time_seconds = 0

        # Calculate slippage vs benchmarks
        slippage_arrival = self._calculate_slippage_bps(
            avg_fill_price, arrival_price, side
        ) if arrival_price else None

        slippage_vwap = self._calculate_slippage_bps(
            avg_fill_price, vwap_benchmark, side
        ) if vwap_benchmark else None

        slippage_twap = self._calculate_slippage_bps(
            avg_fill_price, twap_benchmark, side
        ) if twap_benchmark else None

        slippage_close = self._calculate_slippage_bps(
            avg_fill_price, close_price, side
        ) if close_price else None

        # Calculate costs
        total_commission = sum(f.commission for f in fills)
        cost_per_share = total_commission / filled_quantity if filled_quantity > 0 else 0

        # Slippage cost (in dollars)
        slippage_cost = 0
        if arrival_price and filled_quantity > 0:
            slippage_cost = abs(avg_fill_price - arrival_price) * filled_quantity

        total_cost = total_commission + slippage_cost

        # Price improvement (negative slippage is good)
        price_improvement = -slippage_arrival if slippage_arrival else 0

        # Market impact and participation
        participation_rate = None
        if market_volume and market_volume > 0:
            participation_rate = (filled_quantity / market_volume) * 100

        market_impact_bps = self._estimate_market_impact(
            filled_quantity, market_volume, slippage_arrival
        )

        # Venue breakdown
        venue_fills = {}
        dark_pool_fills = 0

        for fill in fills:
            venue_name = fill.venue_name or "Unknown"
            venue_fills[venue_name] = venue_fills.get(venue_name, 0) + fill.quantity

            # Count dark pool fills (simplified - would need venue metadata)
            if "dark" in venue_name.lower():
                dark_pool_fills += fill.quantity

        dark_pool_fill_rate = (dark_pool_fills / filled_quantity * 100) if filled_quantity > 0 else 0

        # Calculate quality score
        quality_score, quality_grade = self._calculate_quality_score(
            slippage_arrival, fill_rate, participation_rate, dark_pool_fill_rate
        )

        # Generate improvement suggestions
        suggestions = self._generate_suggestions(
            slippage_arrival, slippage_vwap, fill_rate, participation_rate,
            dark_pool_fill_rate, execution_time_seconds, total_quantity
        )

        report = ExecutionReport(
            order_id=order_id,
            ticker=ticker,
            side=side,
            total_quantity=total_quantity,
            filled_quantity=filled_quantity,
            avg_fill_price=avg_fill_price,
            arrival_price=arrival_price,
            vwap_benchmark=vwap_benchmark,
            twap_benchmark=twap_benchmark,
            close_price=close_price,
            slippage_vs_arrival=slippage_arrival,
            slippage_vs_vwap=slippage_vwap,
            slippage_vs_twap=slippage_twap,
            slippage_vs_close=slippage_close,
            total_commission=total_commission,
            total_cost=total_cost,
            cost_per_share=cost_per_share,
            fill_rate=fill_rate,
            execution_time_seconds=execution_time_seconds,
            price_improvement=price_improvement,
            participation_rate=participation_rate,
            market_impact_bps=market_impact_bps,
            venue_fills=venue_fills,
            dark_pool_fills=dark_pool_fills,
            dark_pool_fill_rate=dark_pool_fill_rate,
            overall_quality_score=quality_score,
            quality_grade=quality_grade,
            improvement_suggestions=suggestions
        )

        logger.info(
            f"📊 Execution Report: {ticker} - {filled_quantity}/{total_quantity} shares, "
            f"Avg: ${avg_fill_price:.2f}, Slippage: {slippage_arrival:.2f}bps, "
            f"Grade: {quality_grade}"
        )

        return report

    def _calculate_slippage_bps(
        self,
        fill_price: float,
        benchmark_price: Optional[float],
        side: str
    ) -> Optional[float]:
        """
        Calculate slippage in basis points

        For buys: positive slippage = paid more than benchmark (bad)
        For sells: positive slippage = received less than benchmark (bad)
        """
        if benchmark_price is None or benchmark_price == 0:
            return None

        if side.lower() == "buy":
            slippage = ((fill_price - benchmark_price) / benchmark_price) * 10000
        else:  # sell
            slippage = ((benchmark_price - fill_price) / benchmark_price) * 10000

        return slippage

    def _estimate_market_impact(
        self,
        quantity: int,
        market_volume: Optional[int],
        slippage_bps: Optional[float]
    ) -> Optional[float]:
        """Estimate market impact component of slippage"""

        if market_volume is None or market_volume == 0:
            return None

        participation = quantity / market_volume

        # Simple model: impact scales with participation
        # This is a simplified estimate
        if slippage_bps is not None:
            # Assume ~50% of slippage is market impact, rest is spread
            estimated_impact = abs(slippage_bps) * 0.5 * (participation * 10)
            return min(estimated_impact, abs(slippage_bps))  # Cap at total slippage

        return None

    def _calculate_quality_score(
        self,
        slippage_bps: Optional[float],
        fill_rate: float,
        participation_rate: Optional[float],
        dark_pool_rate: float
    ) -> Tuple[float, str]:
        """
        Calculate overall execution quality score (0-100)

        Scoring factors:
        - Slippage (40%): Lower is better
        - Fill rate (30%): Higher is better
        - Participation rate (15%): Lower is better (less market impact)
        - Dark pool usage (15%): Higher is better (price improvement)
        """

        scores = []
        weights = []

        # Slippage score (40%)
        if slippage_bps is not None:
            if slippage_bps <= 0:  # Price improvement
                slippage_score = 100
            elif slippage_bps < 5:  # Excellent
                slippage_score = 90
            elif slippage_bps < 10:  # Good
                slippage_score = 75
            elif slippage_bps < 20:  # Fair
                slippage_score = 60
            elif slippage_bps < 30:  # Poor
                slippage_score = 40
            else:  # Bad
                slippage_score = 20

            scores.append(slippage_score)
            weights.append(0.4)

        # Fill rate score (30%)
        fill_score = fill_rate  # 0-100
        scores.append(fill_score)
        weights.append(0.3)

        # Participation rate score (15%)
        if participation_rate is not None:
            if participation_rate < 5:  # Low impact
                participation_score = 100
            elif participation_rate < 10:
                participation_score = 80
            elif participation_rate < 20:
                participation_score = 60
            else:
                participation_score = 40

            scores.append(participation_score)
            weights.append(0.15)

        # Dark pool score (15%)
        if dark_pool_rate > 30:  # High dark pool usage
            dark_pool_score = 100
        elif dark_pool_rate > 15:
            dark_pool_score = 80
        elif dark_pool_rate > 5:
            dark_pool_score = 60
        else:
            dark_pool_score = 40

        scores.append(dark_pool_score)
        weights.append(0.15)

        # Weighted average
        if sum(weights) > 0:
            overall_score = sum(s * w for s, w in zip(scores, weights)) / sum(weights)
        else:
            overall_score = 50

        # Assign grade
        if overall_score >= 95:
            grade = "A+"
        elif overall_score >= 90:
            grade = "A"
        elif overall_score >= 85:
            grade = "A-"
        elif overall_score >= 80:
            grade = "B+"
        elif overall_score >= 75:
            grade = "B"
        elif overall_score >= 70:
            grade = "B-"
        elif overall_score >= 65:
            grade = "C+"
        elif overall_score >= 60:
            grade = "C"
        elif overall_score >= 55:
            grade = "C-"
        elif overall_score >= 50:
            grade = "D"
        else:
            grade = "F"

        return overall_score, grade

    def _generate_suggestions(
        self,
        slippage_arrival: Optional[float],
        slippage_vwap: Optional[float],
        fill_rate: float,
        participation_rate: Optional[float],
        dark_pool_rate: float,
        execution_time: float,
        total_quantity: int
    ) -> List[str]:
        """Generate actionable improvement suggestions"""

        suggestions = []

        # Slippage suggestions
        if slippage_arrival is not None:
            if slippage_arrival > 20:
                suggestions.append(
                    "⚠️ High slippage detected. Consider using more order slices or "
                    "extending execution time window to reduce market impact."
                )
            elif slippage_arrival > 10:
                suggestions.append(
                    "💡 Moderate slippage. Try using VWAP algorithm or iceberg orders "
                    "to blend with market volume."
                )

        # VWAP comparison
        if slippage_vwap is not None and slippage_arrival is not None:
            if slippage_vwap < slippage_arrival - 5:
                suggestions.append(
                    "✅ Execution beat VWAP. Consider using VWAP algorithm more often "
                    "for similar order sizes."
                )

        # Fill rate suggestions
        if fill_rate < 95:
            suggestions.append(
                f"⚠️ Only {fill_rate:.1f}% filled. Consider using more aggressive "
                "limit prices or market orders for critical fills."
            )

        # Participation suggestions
        if participation_rate is not None:
            if participation_rate > 15:
                suggestions.append(
                    f"⚠️ High participation rate ({participation_rate:.1f}%). "
                    "Extend execution window or use POV algorithm to reduce market impact."
                )
            elif participation_rate < 3:
                suggestions.append(
                    f"✅ Low participation rate ({participation_rate:.1f}%). "
                    "Good stealth execution with minimal market impact."
                )

        # Dark pool suggestions
        if dark_pool_rate < 10 and total_quantity > 1000:
            suggestions.append(
                "💡 Low dark pool usage. Consider routing larger slices to dark pools "
                "for potential price improvement."
            )
        elif dark_pool_rate > 40:
            suggestions.append(
                f"✅ High dark pool fill rate ({dark_pool_rate:.1f}%). "
                "Excellent price improvement opportunity captured."
            )

        # Execution speed
        if execution_time > 3600:  # More than 1 hour
            suggestions.append(
                "💡 Long execution time. Monitor for adverse price movements "
                "and consider using Implementation Shortfall algorithm for urgent orders."
            )

        # If everything looks good
        if not suggestions:
            suggestions.append(
                "✅ Excellent execution quality. Current strategy is performing well."
            )

        return suggestions


class BenchmarkCalculator:
    """Calculate benchmark prices for execution analysis"""

    @staticmethod
    def calculate_vwap(prices: List[float], volumes: List[int]) -> float:
        """
        Calculate Volume-Weighted Average Price

        Args:
            prices: List of prices
            volumes: List of volumes (same length as prices)

        Returns:
            VWAP
        """
        if len(prices) != len(volumes) or len(prices) == 0:
            raise ValueError("Prices and volumes must have same non-zero length")

        total_value = sum(p * v for p, v in zip(prices, volumes))
        total_volume = sum(volumes)

        if total_volume == 0:
            return 0

        return total_value / total_volume

    @staticmethod
    def calculate_twap(prices: List[float]) -> float:
        """
        Calculate Time-Weighted Average Price

        Args:
            prices: List of prices

        Returns:
            TWAP (simple average)
        """
        if not prices:
            return 0

        return statistics.mean(prices)

    @staticmethod
    def calculate_arrival_price(
        prices: List[float],
        timestamps: List[datetime],
        arrival_time: datetime
    ) -> Optional[float]:
        """
        Get the price at or closest to arrival time

        Args:
            prices: List of prices
            timestamps: List of timestamps
            arrival_time: Order arrival time

        Returns:
            Price closest to arrival time
        """
        if not prices or len(prices) != len(timestamps):
            return None

        # Find closest timestamp to arrival
        min_diff = float('inf')
        closest_price = None

        for price, ts in zip(prices, timestamps):
            diff = abs((ts - arrival_time).total_seconds())
            if diff < min_diff:
                min_diff = diff
                closest_price = price

        return closest_price


class PerformanceTracker:
    """Track execution performance over time"""

    def __init__(self):
        self.execution_history: List[ExecutionReport] = []

    def add_execution(self, report: ExecutionReport):
        """Add execution report to history"""
        self.execution_history.append(report)
        logger.info(f"📈 Added execution to history: {report.order_id}")

    def get_statistics(self, ticker: Optional[str] = None) -> Dict[str, Any]:
        """
        Get aggregate statistics across executions

        Args:
            ticker: Filter by ticker (None = all tickers)

        Returns:
            Dictionary of statistics
        """
        reports = self.execution_history
        if ticker:
            reports = [r for r in reports if r.ticker == ticker]

        if not reports:
            return {"message": "No execution history"}

        return {
            "total_executions": len(reports),
            "avg_quality_score": statistics.mean(r.overall_quality_score for r in reports),
            "avg_slippage_bps": statistics.mean(
                r.slippage_vs_arrival for r in reports if r.slippage_vs_arrival is not None
            ),
            "avg_fill_rate": statistics.mean(r.fill_rate for r in reports),
            "total_quantity_traded": sum(r.filled_quantity for r in reports),
            "total_commission": sum(r.total_commission for r in reports),
            "avg_dark_pool_rate": statistics.mean(r.dark_pool_fill_rate for r in reports),
            "best_execution": max(reports, key=lambda r: r.overall_quality_score).order_id,
            "worst_execution": min(reports, key=lambda r: r.overall_quality_score).order_id
        }
