"""
Venue Selection and Smart Routing
Selects optimal execution venues based on pricing, liquidity, and historical performance
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)


@dataclass
class VenueInfo:
    """Information about a trading venue"""
    venue_id: int
    name: str
    venue_type: str  # "broker", "dark_pool", "exchange"
    commission_rate: float
    commission_type: str  # "per_share", "percentage", "flat"
    min_commission: float
    liquidity_score: float  # 0-100
    avg_fill_quality: float  # Historical fill quality metric
    supports_dark_pool: bool
    supports_iceberg: bool
    is_active: bool


@dataclass
class VenueScore:
    """Venue with calculated score"""
    venue: VenueInfo
    total_score: float
    cost_score: float
    liquidity_score: float
    quality_score: float
    reasoning: str


class VenueSelector:
    """
    Smart venue selection based on multiple criteria:
    - Cost (commissions)
    - Liquidity
    - Historical fill quality
    - Order characteristics
    """

    def __init__(
        self,
        cost_weight: float = 0.4,
        liquidity_weight: float = 0.3,
        quality_weight: float = 0.3
    ):
        """
        Initialize venue selector with scoring weights

        Args:
            cost_weight: Weight for cost considerations (0-1)
            liquidity_weight: Weight for liquidity (0-1)
            quality_weight: Weight for historical fill quality (0-1)
        """
        # Normalize weights
        total = cost_weight + liquidity_weight + quality_weight
        self.cost_weight = cost_weight / total
        self.liquidity_weight = liquidity_weight / total
        self.quality_weight = quality_weight / total

        logger.info(
            f"📊 VenueSelector initialized - "
            f"Weights: Cost={self.cost_weight:.2f}, "
            f"Liquidity={self.liquidity_weight:.2f}, "
            f"Quality={self.quality_weight:.2f}"
        )

    def select_best_venue(
        self,
        venues: List[VenueInfo],
        ticker: str,
        quantity: int,
        price: float,
        order_size_category: str = "medium"  # "small", "medium", "large"
    ) -> Optional[VenueScore]:
        """
        Select the best venue for an order

        Args:
            venues: List of available venues
            ticker: Stock ticker
            quantity: Order quantity
            price: Expected execution price
            order_size_category: Size category of the order

        Returns:
            VenueScore with the best venue and scoring details
        """

        if not venues:
            logger.warning("⚠️ No venues available for selection")
            return None

        # Filter to active venues only
        active_venues = [v for v in venues if v.is_active]

        if not active_venues:
            logger.warning("⚠️ No active venues available")
            return None

        # Score each venue
        scored_venues = []

        for venue in active_venues:
            score = self._score_venue(venue, ticker, quantity, price, order_size_category)
            scored_venues.append(score)

        # Sort by total score (descending)
        scored_venues.sort(key=lambda x: x.total_score, reverse=True)

        best = scored_venues[0]

        logger.info(
            f"✅ Selected venue: {best.venue.name} "
            f"(Score: {best.total_score:.2f}, "
            f"Cost: {best.cost_score:.2f}, "
            f"Liquidity: {best.liquidity_score:.2f}, "
            f"Quality: {best.quality_score:.2f})"
        )

        return best

    def _score_venue(
        self,
        venue: VenueInfo,
        ticker: str,
        quantity: int,
        price: float,
        order_size_category: str
    ) -> VenueScore:
        """Score a single venue"""

        # Calculate cost score (lower cost = higher score)
        cost_score = self._calculate_cost_score(venue, quantity, price)

        # Liquidity score (already 0-100, normalize to 0-1)
        liquidity_score = venue.liquidity_score / 100.0

        # Adjust liquidity importance based on order size
        if order_size_category == "large":
            # For large orders, liquidity is more important
            liquidity_score *= 1.2
        elif order_size_category == "small":
            # For small orders, liquidity is less critical
            liquidity_score *= 0.8

        # Quality score (already 0-100, normalize to 0-1)
        quality_score = (venue.avg_fill_quality or 50.0) / 100.0

        # Calculate weighted total score
        total_score = (
            self.cost_weight * cost_score +
            self.liquidity_weight * liquidity_score +
            self.quality_weight * quality_score
        )

        reasoning = self._generate_reasoning(
            venue, cost_score, liquidity_score, quality_score, order_size_category
        )

        return VenueScore(
            venue=venue,
            total_score=total_score,
            cost_score=cost_score,
            liquidity_score=liquidity_score,
            quality_score=quality_score,
            reasoning=reasoning
        )

    def _calculate_cost_score(
        self,
        venue: VenueInfo,
        quantity: int,
        price: float
    ) -> float:
        """
        Calculate cost score (0-1, higher is better/cheaper)

        Returns normalized score where 0 = most expensive, 1 = cheapest
        """

        order_value = quantity * price

        if venue.commission_type == "per_share":
            commission = max(venue.min_commission, quantity * venue.commission_rate)
        elif venue.commission_type == "percentage":
            commission = max(venue.min_commission, order_value * venue.commission_rate)
        else:  # flat
            commission = venue.commission_rate

        # Calculate commission as basis points of order value
        if order_value > 0:
            commission_bps = (commission / order_value) * 10000
        else:
            commission_bps = 0

        # Convert to score: lower commission = higher score
        # Assume max reasonable commission is 50 bps
        max_commission_bps = 50.0
        cost_score = 1.0 - min(commission_bps / max_commission_bps, 1.0)

        return cost_score

    def _generate_reasoning(
        self,
        venue: VenueInfo,
        cost_score: float,
        liquidity_score: float,
        quality_score: float,
        order_size: str
    ) -> str:
        """Generate human-readable reasoning for venue selection"""

        strengths = []
        if cost_score > 0.8:
            strengths.append("low cost")
        if liquidity_score > 0.7:
            strengths.append("high liquidity")
        if quality_score > 0.7:
            strengths.append("excellent fill quality")

        if strengths:
            return f"{venue.name} selected for {', '.join(strengths)}"
        else:
            return f"{venue.name} selected as best available option"


class SmartRouter:
    """
    Smart order router that distributes orders across multiple venues
    """

    def __init__(self, venue_selector: Optional[VenueSelector] = None):
        self.venue_selector = venue_selector or VenueSelector()

    def route_order(
        self,
        venues: List[VenueInfo],
        ticker: str,
        total_quantity: int,
        price: float,
        use_multiple_venues: bool = True,
        max_venues: int = 3
    ) -> List[Tuple[VenueInfo, int]]:
        """
        Route an order across one or more venues

        Args:
            venues: Available venues
            ticker: Stock ticker
            total_quantity: Total order quantity
            price: Expected price
            use_multiple_venues: Whether to split across venues
            max_venues: Maximum number of venues to use

        Returns:
            List of (venue, quantity) tuples
        """

        if not use_multiple_venues or total_quantity < 1000:
            # Small orders go to single best venue
            best = self.venue_selector.select_best_venue(
                venues, ticker, total_quantity, price, "small"
            )

            if best:
                logger.info(f"📍 Routing to single venue: {best.venue.name}")
                return [(best.venue, total_quantity)]
            else:
                return []

        # Large orders can be split across venues
        order_size = "large" if total_quantity >= 5000 else "medium"

        # Score all venues
        scored_venues = []
        for venue in venues:
            if venue.is_active:
                score = self.venue_selector._score_venue(
                    venue, ticker, total_quantity, price, order_size
                )
                scored_venues.append(score)

        # Sort by score
        scored_venues.sort(key=lambda x: x.total_score, reverse=True)

        # Select top venues
        selected_venues = scored_venues[:max_venues]

        # Allocate quantity based on scores
        total_score = sum(v.total_score for v in selected_venues)

        allocations = []
        allocated = 0

        for i, venue_score in enumerate(selected_venues):
            if i == len(selected_venues) - 1:
                # Last venue gets remainder
                quantity = total_quantity - allocated
            else:
                # Allocate proportionally to score
                proportion = venue_score.total_score / total_score
                quantity = int(total_quantity * proportion)
                allocated += quantity

            if quantity > 0:
                allocations.append((venue_score.venue, quantity))

        logger.info(
            f"📍 Smart routing across {len(allocations)} venues: "
            f"{', '.join([f'{v.name}({q})' for v, q in allocations])}"
        )

        return allocations

    def select_dark_pool_venues(
        self,
        venues: List[VenueInfo],
        ticker: str,
        quantity: int,
        price: float
    ) -> List[VenueInfo]:
        """
        Select dark pool venues for potential price improvement

        Args:
            venues: Available venues
            ticker: Stock ticker
            quantity: Order quantity
            price: Expected price

        Returns:
            List of dark pool venues, ordered by preference
        """

        # Filter to dark pool venues
        dark_pools = [
            v for v in venues
            if v.supports_dark_pool and v.is_active
        ]

        if not dark_pools:
            return []

        # Score dark pools
        scored = []
        for venue in dark_pools:
            score = self.venue_selector._score_venue(
                venue, ticker, quantity, price, "medium"
            )
            scored.append(score)

        # Sort by quality and liquidity (less emphasis on cost for dark pools)
        scored.sort(
            key=lambda x: (x.quality_score * 0.6 + x.liquidity_score * 0.4),
            reverse=True
        )

        selected_venues = [s.venue for s in scored]

        logger.info(
            f"🌑 Selected {len(selected_venues)} dark pool venues: "
            f"{', '.join([v.name for v in selected_venues[:3]])}"
        )

        return selected_venues


class VenuePerformanceTracker:
    """Track and update venue performance metrics"""

    def __init__(self):
        self.performance_data: Dict[int, Dict[str, Any]] = {}

    def record_fill(
        self,
        venue_id: int,
        fill_time_ms: float,
        slippage_bps: float,
        price_improvement_bps: float
    ):
        """Record a fill execution for performance tracking"""

        if venue_id not in self.performance_data:
            self.performance_data[venue_id] = {
                "total_orders": 0,
                "total_fill_time_ms": 0,
                "total_slippage_bps": 0,
                "total_price_improvement_bps": 0,
                "fills": 0
            }

        data = self.performance_data[venue_id]
        data["total_orders"] += 1
        data["total_fill_time_ms"] += fill_time_ms
        data["total_slippage_bps"] += slippage_bps
        data["total_price_improvement_bps"] += price_improvement_bps
        data["fills"] += 1

        logger.debug(
            f"📊 Recorded fill for venue {venue_id}: "
            f"{fill_time_ms:.0f}ms, slippage={slippage_bps:.2f}bps"
        )

    def get_venue_metrics(self, venue_id: int) -> Optional[Dict[str, float]]:
        """Get average performance metrics for a venue"""

        if venue_id not in self.performance_data:
            return None

        data = self.performance_data[venue_id]
        fills = data["fills"]

        if fills == 0:
            return None

        return {
            "avg_fill_time_ms": data["total_fill_time_ms"] / fills,
            "avg_slippage_bps": data["total_slippage_bps"] / fills,
            "avg_price_improvement_bps": data["total_price_improvement_bps"] / fills,
            "fill_rate": (fills / data["total_orders"]) * 100 if data["total_orders"] > 0 else 0
        }

    def get_all_metrics(self) -> Dict[int, Dict[str, float]]:
        """Get metrics for all venues"""

        return {
            venue_id: self.get_venue_metrics(venue_id)
            for venue_id in self.performance_data.keys()
        }
