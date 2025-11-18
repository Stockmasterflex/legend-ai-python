"""
Execution Analytics Service

Tracks and analyzes order execution quality including:
- Fill quality
- Slippage tracking
- Best execution analysis
- Order routing statistics
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel
from collections import defaultdict
import statistics

from app.brokers.base import Order, OrderStatus, ExecutionReport

logger = logging.getLogger(__name__)


class ExecutionMetrics(BaseModel):
    """Execution quality metrics"""
    order_id: str
    symbol: str
    side: str
    order_type: str

    # Fill metrics
    requested_qty: float
    filled_qty: float
    fill_rate: float  # Percentage filled

    # Price metrics
    limit_price: Optional[float] = None
    avg_fill_price: Optional[float] = None
    market_price_at_order: Optional[float] = None

    # Slippage
    slippage: Optional[float] = None  # Dollar amount
    slippage_percent: Optional[float] = None
    slippage_bps: Optional[int] = None  # Basis points

    # Timing
    order_time: datetime
    fill_time: Optional[datetime] = None
    execution_duration_ms: Optional[int] = None

    # Quality score (0-100)
    execution_quality_score: float

    # Metadata
    exchange: Optional[str] = None
    time_in_force: str


class AggregateExecutionStats(BaseModel):
    """Aggregate execution statistics"""
    total_orders: int
    filled_orders: int
    partially_filled_orders: int
    canceled_orders: int
    rejected_orders: int

    # Fill rate
    avg_fill_rate: float
    total_volume: float

    # Slippage statistics
    avg_slippage_bps: Optional[float] = None
    median_slippage_bps: Optional[float] = None
    total_slippage_cost: float = 0.0

    # Timing statistics
    avg_execution_duration_ms: Optional[float] = None
    median_execution_duration_ms: Optional[float] = None

    # Quality metrics
    avg_execution_quality: float
    orders_with_price_improvement: int = 0
    price_improvement_amount: float = 0.0

    # By order type
    order_type_breakdown: Dict[str, int]

    # By symbol
    top_symbols: List[Dict[str, Any]]

    # Time range
    start_date: datetime
    end_date: datetime


class ExecutionAnalyticsService:
    """
    Service for tracking and analyzing execution quality.

    Monitors fills, slippage, timing, and routing to ensure best execution.
    """

    def __init__(self):
        """Initialize execution analytics service"""
        self._execution_history: List[ExecutionMetrics] = []
        self._execution_reports: List[ExecutionReport] = []

    def record_execution(
        self,
        order: Order,
        market_price_at_order: Optional[float] = None,
    ) -> ExecutionMetrics:
        """
        Record order execution for analysis.

        Args:
            order: Filled or partially filled order
            market_price_at_order: Market price when order was placed

        Returns:
            ExecutionMetrics: Execution metrics
        """
        # Calculate fill rate
        fill_rate = (order.filled_qty / order.quantity * 100) if order.quantity > 0 else 0

        # Calculate slippage
        slippage = None
        slippage_percent = None
        slippage_bps = None

        if order.avg_fill_price and market_price_at_order:
            # For buys: positive slippage = paid more than market
            # For sells: positive slippage = received less than market
            if order.side.value == "buy":
                slippage = order.avg_fill_price - market_price_at_order
            else:
                slippage = market_price_at_order - order.avg_fill_price

            slippage_percent = (slippage / market_price_at_order * 100) if market_price_at_order > 0 else 0
            slippage_bps = int(slippage_percent * 100)  # Convert to basis points

        # Calculate execution duration
        execution_duration_ms = None
        if order.created_at and order.filled_at:
            duration = order.filled_at - order.created_at
            execution_duration_ms = int(duration.total_seconds() * 1000)

        # Calculate execution quality score (0-100)
        quality_score = self._calculate_quality_score(
            fill_rate=fill_rate,
            slippage_bps=slippage_bps,
            execution_duration_ms=execution_duration_ms,
            order_type=order.order_type.value,
        )

        metrics = ExecutionMetrics(
            order_id=order.order_id or "",
            symbol=order.symbol,
            side=order.side.value,
            order_type=order.order_type.value,
            requested_qty=order.quantity,
            filled_qty=order.filled_qty,
            fill_rate=fill_rate,
            limit_price=order.price,
            avg_fill_price=order.avg_fill_price,
            market_price_at_order=market_price_at_order,
            slippage=slippage,
            slippage_percent=slippage_percent,
            slippage_bps=slippage_bps,
            order_time=order.created_at or datetime.now(),
            fill_time=order.filled_at,
            execution_duration_ms=execution_duration_ms,
            execution_quality_score=quality_score,
            time_in_force=order.time_in_force.value,
        )

        self._execution_history.append(metrics)
        logger.info(
            f"Execution recorded: {order.symbol} {order.side.value} "
            f"{order.filled_qty}/{order.quantity} @ {order.avg_fill_price} "
            f"(quality: {quality_score:.1f})"
        )

        return metrics

    def add_execution_report(self, report: ExecutionReport) -> None:
        """
        Add detailed execution report.

        Args:
            report: Execution report from broker
        """
        self._execution_reports.append(report)

    def get_execution_metrics(self, order_id: str) -> Optional[ExecutionMetrics]:
        """
        Get execution metrics for specific order.

        Args:
            order_id: Order ID

        Returns:
            Optional[ExecutionMetrics]: Metrics or None
        """
        for metrics in self._execution_history:
            if metrics.order_id == order_id:
                return metrics
        return None

    def get_aggregate_stats(
        self,
        symbol: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> AggregateExecutionStats:
        """
        Get aggregate execution statistics.

        Args:
            symbol: Filter by symbol (optional)
            start_date: Filter by start date (optional)
            end_date: Filter by end date (optional)

        Returns:
            AggregateExecutionStats: Aggregate statistics
        """
        # Filter executions
        filtered = self._execution_history

        if symbol:
            filtered = [e for e in filtered if e.symbol == symbol]

        if start_date:
            filtered = [e for e in filtered if e.order_time >= start_date]

        if end_date:
            filtered = [e for e in filtered if e.order_time <= end_date]

        if not filtered:
            # Return empty stats
            return AggregateExecutionStats(
                total_orders=0,
                filled_orders=0,
                partially_filled_orders=0,
                canceled_orders=0,
                rejected_orders=0,
                avg_fill_rate=0.0,
                total_volume=0.0,
                avg_execution_quality=0.0,
                order_type_breakdown={},
                top_symbols=[],
                start_date=start_date or datetime.now(),
                end_date=end_date or datetime.now(),
            )

        # Calculate statistics
        total_orders = len(filtered)
        filled_orders = len([e for e in filtered if e.fill_rate == 100])
        partially_filled = len([e for e in filtered if 0 < e.fill_rate < 100])

        avg_fill_rate = statistics.mean([e.fill_rate for e in filtered])
        total_volume = sum(e.filled_qty for e in filtered)

        # Slippage statistics
        slippages = [e.slippage_bps for e in filtered if e.slippage_bps is not None]
        avg_slippage_bps = statistics.mean(slippages) if slippages else None
        median_slippage_bps = statistics.median(slippages) if slippages else None

        slippage_costs = [
            abs(e.slippage * e.filled_qty)
            for e in filtered
            if e.slippage is not None
        ]
        total_slippage_cost = sum(slippage_costs)

        # Timing statistics
        durations = [e.execution_duration_ms for e in filtered if e.execution_duration_ms is not None]
        avg_duration = statistics.mean(durations) if durations else None
        median_duration = statistics.median(durations) if durations else None

        # Quality metrics
        avg_quality = statistics.mean([e.execution_quality_score for e in filtered])

        # Price improvement
        price_improvements = [
            e for e in filtered
            if e.slippage is not None and (
                (e.side == "buy" and e.slippage < 0) or
                (e.side == "sell" and e.slippage > 0)
            )
        ]
        price_improvement_amount = sum([abs(e.slippage * e.filled_qty) for e in price_improvements])

        # Order type breakdown
        order_type_counts = defaultdict(int)
        for e in filtered:
            order_type_counts[e.order_type] += 1

        # Top symbols by volume
        symbol_volumes = defaultdict(float)
        for e in filtered:
            symbol_volumes[e.symbol] += e.filled_qty

        top_symbols = [
            {"symbol": sym, "volume": vol}
            for sym, vol in sorted(symbol_volumes.items(), key=lambda x: x[1], reverse=True)[:10]
        ]

        return AggregateExecutionStats(
            total_orders=total_orders,
            filled_orders=filled_orders,
            partially_filled_orders=partially_filled,
            canceled_orders=0,  # Not tracked in execution metrics
            rejected_orders=0,  # Not tracked in execution metrics
            avg_fill_rate=avg_fill_rate,
            total_volume=total_volume,
            avg_slippage_bps=avg_slippage_bps,
            median_slippage_bps=median_slippage_bps,
            total_slippage_cost=total_slippage_cost,
            avg_execution_duration_ms=avg_duration,
            median_execution_duration_ms=median_duration,
            avg_execution_quality=avg_quality,
            orders_with_price_improvement=len(price_improvements),
            price_improvement_amount=price_improvement_amount,
            order_type_breakdown=dict(order_type_counts),
            top_symbols=top_symbols,
            start_date=start_date or min(e.order_time for e in filtered),
            end_date=end_date or max(e.order_time for e in filtered),
        )

    def get_slippage_analysis(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Get detailed slippage analysis.

        Args:
            symbol: Filter by symbol (optional)

        Returns:
            Dict with slippage analysis
        """
        filtered = self._execution_history
        if symbol:
            filtered = [e for e in filtered if e.symbol == symbol]

        slippages = [e.slippage_bps for e in filtered if e.slippage_bps is not None]

        if not slippages:
            return {"error": "No slippage data available"}

        return {
            "total_executions": len(filtered),
            "executions_with_slippage": len(slippages),
            "avg_slippage_bps": statistics.mean(slippages),
            "median_slippage_bps": statistics.median(slippages),
            "min_slippage_bps": min(slippages),
            "max_slippage_bps": max(slippages),
            "stdev_slippage_bps": statistics.stdev(slippages) if len(slippages) > 1 else 0,
            "positive_slippage_count": len([s for s in slippages if s > 0]),
            "negative_slippage_count": len([s for s in slippages if s < 0]),
            "zero_slippage_count": len([s for s in slippages if s == 0]),
        }

    def _calculate_quality_score(
        self,
        fill_rate: float,
        slippage_bps: Optional[int],
        execution_duration_ms: Optional[int],
        order_type: str,
    ) -> float:
        """
        Calculate execution quality score (0-100).

        Factors:
        - Fill rate (40% weight)
        - Slippage (40% weight)
        - Speed (20% weight)
        """
        score = 0.0

        # Fill rate component (40 points max)
        score += (fill_rate / 100) * 40

        # Slippage component (40 points max)
        if slippage_bps is not None:
            # Good: < 5 bps, Acceptable: < 10 bps, Poor: > 20 bps
            if slippage_bps <= 5:
                slippage_score = 40
            elif slippage_bps <= 10:
                slippage_score = 30
            elif slippage_bps <= 20:
                slippage_score = 20
            else:
                slippage_score = max(0, 40 - slippage_bps)
            score += slippage_score
        else:
            # No slippage data (market orders), give neutral score
            score += 30

        # Speed component (20 points max)
        if execution_duration_ms is not None:
            # Good: < 100ms, Acceptable: < 1000ms, Poor: > 5000ms
            if execution_duration_ms <= 100:
                speed_score = 20
            elif execution_duration_ms <= 1000:
                speed_score = 15
            elif execution_duration_ms <= 5000:
                speed_score = 10
            else:
                speed_score = 5
            score += speed_score
        else:
            # No timing data, give neutral score
            score += 15

        return min(100, max(0, score))

    def clear_history(self, before_date: Optional[datetime] = None) -> int:
        """
        Clear execution history.

        Args:
            before_date: Clear records before this date (None for all)

        Returns:
            int: Number of records cleared
        """
        if before_date is None:
            count = len(self._execution_history)
            self._execution_history.clear()
            self._execution_reports.clear()
            logger.info(f"Cleared all execution history ({count} records)")
            return count

        original_count = len(self._execution_history)
        self._execution_history = [
            e for e in self._execution_history
            if e.order_time >= before_date
        ]
        self._execution_reports = [
            r for r in self._execution_reports
            if r.order_time >= before_date
        ]

        cleared = original_count - len(self._execution_history)
        logger.info(f"Cleared {cleared} execution records before {before_date}")
        return cleared
