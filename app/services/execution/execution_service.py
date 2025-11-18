"""
Execution Service Orchestrator
Main service that coordinates all execution components
"""

import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from .algorithms import AlgorithmFactory, OrderSlice, MarketData
from .venue_selection import VenueSelector, SmartRouter, VenueInfo
from .order_slicer import OrderSlicer, AdaptiveSlicer, SlicedOrder
from .analytics import ExecutionAnalyzer, Fill, ExecutionReport
from .dark_pool import DarkPoolRouter, DarkPoolVenue, SizeDiscovery, PriceImprovementTracker

logger = logging.getLogger(__name__)


class ExecutionService:
    """
    Main execution service that orchestrates intelligent trade execution
    """

    def __init__(self):
        self.venue_selector = VenueSelector()
        self.smart_router = SmartRouter(self.venue_selector)
        self.order_slicer = OrderSlicer()
        self.adaptive_slicer = AdaptiveSlicer(self.order_slicer)
        self.execution_analyzer = ExecutionAnalyzer()
        self.dark_pool_router = DarkPoolRouter()
        self.size_discovery = SizeDiscovery()
        self.price_improvement_tracker = PriceImprovementTracker()

        logger.info("✅ ExecutionService initialized")

    def create_execution_order(
        self,
        ticker: str,
        side: str,
        quantity: int,
        algo_type: str = "twap",
        duration_minutes: int = 60,
        limit_price: Optional[float] = None,
        algo_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new execution order using specified algorithm

        Args:
            ticker: Stock ticker
            side: "buy" or "sell"
            quantity: Total quantity to execute
            algo_type: "twap", "vwap", "is", or "pov"
            duration_minutes: Execution time window
            limit_price: Optional limit price
            algo_params: Algorithm-specific parameters

        Returns:
            Order details including order_id and execution plan
        """

        order_id = f"EXEC_{ticker}_{uuid.uuid4().hex[:8].upper()}"
        algo_params = algo_params or {}

        logger.info(
            f"📋 Creating execution order: {order_id} - {side.upper()} {quantity} {ticker} "
            f"using {algo_type.upper()} over {duration_minutes}min"
        )

        # Create execution algorithm
        try:
            algorithm = AlgorithmFactory.create_algorithm(
                algo_type=algo_type,
                ticker=ticker,
                side=side,
                total_quantity=quantity,
                duration_minutes=duration_minutes,
                **algo_params
            )
        except ValueError as e:
            logger.error(f"❌ Failed to create algorithm: {e}")
            return {
                "success": False,
                "error": str(e)
            }

        # Generate execution slices
        slices = algorithm.generate_slices()

        # Create execution plan
        execution_plan = {
            "order_id": order_id,
            "ticker": ticker,
            "side": side,
            "total_quantity": quantity,
            "algo_type": algo_type,
            "duration_minutes": duration_minutes,
            "limit_price": limit_price,
            "num_slices": len(slices),
            "slices": [
                {
                    "quantity": s.quantity,
                    "scheduled_time": s.scheduled_time.isoformat(),
                    "is_iceberg": s.is_iceberg
                }
                for s in slices
            ],
            "created_at": datetime.now().isoformat(),
            "status": "pending"
        }

        logger.info(
            f"✅ Execution order created: {order_id} with {len(slices)} slices"
        )

        return {
            "success": True,
            "execution_plan": execution_plan
        }

    def select_venues(
        self,
        ticker: str,
        quantity: int,
        price: float,
        available_venues: List[VenueInfo],
        use_smart_routing: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Select optimal venues for order execution

        Args:
            ticker: Stock ticker
            quantity: Order quantity
            price: Expected price
            available_venues: List of available venues
            use_smart_routing: Whether to use multi-venue routing

        Returns:
            List of venue allocations
        """

        if not available_venues:
            logger.warning("⚠️ No venues available for selection")
            return []

        if use_smart_routing:
            # Smart route across multiple venues
            allocations = self.smart_router.route_order(
                venues=available_venues,
                ticker=ticker,
                total_quantity=quantity,
                price=price,
                use_multiple_venues=True,
                max_venues=3
            )
        else:
            # Single best venue
            best = self.venue_selector.select_best_venue(
                venues=available_venues,
                ticker=ticker,
                quantity=quantity,
                price=price
            )

            if best:
                allocations = [(best.venue, quantity)]
            else:
                allocations = []

        # Format results
        venue_allocations = [
            {
                "venue_id": venue.venue_id,
                "venue_name": venue.name,
                "quantity": qty,
                "commission_rate": venue.commission_rate,
                "liquidity_score": venue.liquidity_score
            }
            for venue, qty in allocations
        ]

        logger.info(
            f"📍 Selected {len(venue_allocations)} venues for {ticker}"
        )

        return venue_allocations

    def create_iceberg_order(
        self,
        ticker: str,
        side: str,
        total_quantity: int,
        display_quantity: int,
        limit_price: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Create an iceberg order (large order with hidden quantity)

        Args:
            ticker: Stock ticker
            side: "buy" or "sell"
            total_quantity: Total order quantity
            display_quantity: Visible quantity
            limit_price: Optional limit price

        Returns:
            Iceberg order details
        """

        order_id = f"ICE_{ticker}_{uuid.uuid4().hex[:8].upper()}"

        logger.info(
            f"🧊 Creating iceberg order: {order_id} - {side.upper()} {total_quantity} {ticker} "
            f"(display: {display_quantity})"
        )

        # Create iceberg clips
        clips = self.order_slicer.create_iceberg_order(
            total_quantity=total_quantity,
            display_quantity=display_quantity
        )

        return {
            "success": True,
            "order_id": order_id,
            "ticker": ticker,
            "side": side,
            "total_quantity": total_quantity,
            "display_quantity": display_quantity,
            "hidden_quantity": total_quantity - display_quantity,
            "num_clips": len(clips),
            "limit_price": limit_price,
            "clips": [
                {
                    "clip_id": c.slice_id,
                    "quantity": c.quantity,
                    "display": c.display_quantity
                }
                for c in clips
            ]
        }

    def route_to_dark_pools(
        self,
        ticker: str,
        side: str,
        quantity: int,
        limit_price: float,
        nbbo_mid: float,
        dark_pools: List[DarkPoolVenue],
        strategy: str = "hybrid"
    ) -> Dict[str, Any]:
        """
        Route order to dark pools for price improvement

        Args:
            ticker: Stock ticker
            side: "buy" or "sell"
            quantity: Order quantity
            limit_price: Limit price
            nbbo_mid: NBBO midpoint
            dark_pools: Available dark pools
            strategy: "aggressive", "passive", or "hybrid"

        Returns:
            Dark pool routing details
        """

        logger.info(
            f"🌑 Routing {quantity} {ticker} to dark pools ({strategy} strategy)"
        )

        # Route to dark pools
        dark_orders = self.dark_pool_router.route_to_dark_pools(
            ticker=ticker,
            side=side,
            quantity=quantity,
            limit_price=limit_price,
            nbbo_mid=nbbo_mid,
            dark_pools=dark_pools,
            strategy=strategy
        )

        # Size discovery
        discovered_sizes = self.size_discovery.probe_for_size(
            ticker=ticker,
            side=side,
            estimated_size=quantity,
            dark_pools=dark_pools,
            nbbo_mid=nbbo_mid
        )

        return {
            "success": True,
            "ticker": ticker,
            "quantity": quantity,
            "strategy": strategy,
            "dark_pool_orders": len(dark_orders),
            "venues": [o.venue_name for o in dark_orders],
            "discovered_liquidity": sum(discovered_sizes.values()),
            "orders": [
                {
                    "order_id": o.order_id,
                    "venue": o.venue_name,
                    "quantity": o.quantity,
                    "time_in_force": o.time_in_force,
                    "peg_to_midpoint": o.peg_to_midpoint
                }
                for o in dark_orders
            ]
        }

    def analyze_execution(
        self,
        order_id: str,
        ticker: str,
        side: str,
        total_quantity: int,
        fills: List[Dict[str, Any]],
        arrival_price: Optional[float] = None,
        benchmarks: Optional[Dict[str, float]] = None,
        market_volume: Optional[int] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Analyze execution quality and generate report

        Args:
            order_id: Order ID
            ticker: Stock ticker
            side: "buy" or "sell"
            total_quantity: Total order quantity
            fills: List of fill dictionaries
            arrival_price: Price at order arrival
            benchmarks: Dict with vwap, twap, close prices
            market_volume: Market volume during execution
            start_time: Execution start time
            end_time: Execution end time

        Returns:
            Execution quality report
        """

        logger.info(f"📊 Analyzing execution quality for {order_id}")

        # Convert fill dicts to Fill objects
        fill_objects = [
            Fill(
                fill_id=f["fill_id"],
                timestamp=datetime.fromisoformat(f["timestamp"]) if isinstance(f["timestamp"], str) else f["timestamp"],
                quantity=f["quantity"],
                price=f["price"],
                venue_id=f.get("venue_id"),
                venue_name=f.get("venue_name"),
                commission=f.get("commission", 0.0)
            )
            for f in fills
        ]

        benchmarks = benchmarks or {}

        # Analyze execution
        report = self.execution_analyzer.analyze_execution(
            order_id=order_id,
            ticker=ticker,
            side=side,
            total_quantity=total_quantity,
            fills=fill_objects,
            arrival_price=arrival_price,
            vwap_benchmark=benchmarks.get("vwap"),
            twap_benchmark=benchmarks.get("twap"),
            close_price=benchmarks.get("close"),
            market_volume=market_volume,
            start_time=start_time,
            end_time=end_time
        )

        # Convert report to dict
        return {
            "success": True,
            "report": {
                "order_id": report.order_id,
                "ticker": report.ticker,
                "fill_rate": f"{report.fill_rate:.1f}%",
                "avg_fill_price": f"${report.avg_fill_price:.2f}",
                "slippage_vs_arrival": f"{report.slippage_vs_arrival:.2f} bps" if report.slippage_vs_arrival else None,
                "slippage_vs_vwap": f"{report.slippage_vs_vwap:.2f} bps" if report.slippage_vs_vwap else None,
                "total_commission": f"${report.total_commission:.2f}",
                "total_cost": f"${report.total_cost:.2f}",
                "quality_score": report.overall_quality_score,
                "quality_grade": report.quality_grade,
                "dark_pool_fills": report.dark_pool_fills,
                "dark_pool_rate": f"{report.dark_pool_fill_rate:.1f}%",
                "venue_breakdown": report.venue_fills,
                "suggestions": report.improvement_suggestions
            }
        }

    def get_execution_summary(self) -> Dict[str, Any]:
        """
        Get summary of execution system capabilities

        Returns:
            System capabilities and status
        """

        return {
            "status": "operational",
            "capabilities": {
                "algorithms": ["TWAP", "VWAP", "Implementation Shortfall", "Percentage of Volume"],
                "features": [
                    "Smart venue selection",
                    "Multi-venue routing",
                    "Order slicing with randomization",
                    "Iceberg orders",
                    "Dark pool routing",
                    "Size discovery",
                    "Execution analytics",
                    "Slippage measurement",
                    "Price improvement tracking"
                ],
                "analytics": [
                    "Slippage vs arrival price",
                    "Slippage vs VWAP/TWAP",
                    "Fill quality grading",
                    "Market impact analysis",
                    "Cost breakdown",
                    "Improvement suggestions"
                ]
            },
            "version": "1.0.0"
        }


# Global instance
_execution_service: Optional[ExecutionService] = None


def get_execution_service() -> ExecutionService:
    """Get or create execution service singleton"""
    global _execution_service
    if _execution_service is None:
        _execution_service = ExecutionService()
    return _execution_service
